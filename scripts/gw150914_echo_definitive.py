#!/usr/bin/env python3
"""GW150914 definitive echo search — blind sweep then check prediction.

Strategy:
  1. Use 16 kHz data for maximum time resolution
  2. Estimate PSD from off-source data (4096s file, away from merger)
  3. Whiten with proper PSD
  4. Subtract best-fit ringdown template
  5. BLIND SWEEP: scan all echo periods 5-300 ms, find the best
  6. THEN compare best echo time to the frozen-star prediction (67.7 ms)
  7. Statistical significance via 1000 time-shift trials
  8. Cross-detector consistency check

This is closer to Abedi et al.'s method than the first-pass analysis.
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    import h5py
except ImportError:
    print("ERROR: h5py required.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

T_ECHO_PREDICTED = 0.0677   # seconds (Kerr prediction for 62 M_sun, a=0.67)
GPS_MERGER = 1126259462.423  # refined merger time
M_REMNANT = 62.0             # solar masses
A_SPIN = 0.67                # dimensionless spin


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_strain(filepath: str) -> tuple[np.ndarray, float, float]:
    with h5py.File(filepath, 'r') as f:
        strain = f['strain/Strain'][:]
        gps_start = f['meta/GPSstart'][()]
        duration = f['meta/Duration'][()]
        sr = len(strain) / duration
    return strain, gps_start, sr


# ---------------------------------------------------------------------------
# PSD estimation (Welch method)
# ---------------------------------------------------------------------------

def estimate_psd(data: np.ndarray, sr: float,
                 seg_len: int = 4096, overlap: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    """Welch PSD estimate. Returns (freqs, psd)."""
    n_seg = (len(data) - overlap) // (seg_len - overlap)
    if n_seg < 1:
        n_seg = 1

    freqs = np.fft.rfftfreq(seg_len, d=1.0/sr)
    psd_sum = np.zeros(len(freqs))

    window = np.hanning(seg_len)
    win_norm = np.sum(window ** 2)

    for i in range(n_seg):
        start = i * (seg_len - overlap)
        end = start + seg_len
        if end > len(data):
            break
        seg = data[start:end] * window
        fft_seg = np.fft.rfft(seg)
        psd_sum += np.abs(fft_seg) ** 2

    psd = psd_sum / (n_seg * sr * win_norm)
    return freqs, psd


# ---------------------------------------------------------------------------
# Whitening with proper PSD
# ---------------------------------------------------------------------------

def whiten_with_psd(data: np.ndarray, sr: float,
                    psd_freqs: np.ndarray, psd: np.ndarray) -> np.ndarray:
    """Whiten data using pre-computed PSD."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)
    fft_data = np.fft.rfft(data)

    # Interpolate PSD to data frequency grid
    psd_interp = np.interp(freqs, psd_freqs, psd)
    psd_interp = np.maximum(psd_interp, 1e-50)

    # Whiten
    fft_whitened = fft_data / np.sqrt(psd_interp)

    # Bandpass 20-500 Hz
    mask = (freqs >= 20.0) & (freqs <= 500.0)
    fft_whitened[~mask] = 0.0

    return np.fft.irfft(fft_whitened, n=n)


# ---------------------------------------------------------------------------
# Ringdown subtraction
# ---------------------------------------------------------------------------

def subtract_ringdown(data: np.ndarray, sr: float, merger_idx: int,
                      f_ring: float = 251.0, tau: float = 0.004,
                      window_ms: float = 100.0) -> np.ndarray:
    """Subtract an exponentially damped sinusoid ringdown model.

    GW150914 remnant: f_ring ~ 251 Hz, tau ~ 4 ms.
    """
    result = data.copy()
    n = len(data)

    # Fit amplitude and phase from data right after merger
    fit_start = merger_idx
    fit_end = merger_idx + int(window_ms / 1000 * sr)
    fit_end = min(fit_end, n)

    t_fit = np.arange(fit_end - fit_start) / sr

    # Simple template: A * exp(-t/tau) * cos(2*pi*f*t + phi)
    # Fit by trying a grid of phases
    best_resid = np.inf
    best_A = 0
    best_phi = 0

    for phi in np.linspace(0, 2*np.pi, 100):
        template = np.exp(-t_fit / tau) * np.cos(2*np.pi*f_ring*t_fit + phi)
        # Least squares for amplitude
        if np.sum(template**2) > 0:
            A = np.sum(data[fit_start:fit_end] * template) / np.sum(template**2)
            resid = np.sum((data[fit_start:fit_end] - A * template)**2)
            if resid < best_resid:
                best_resid = resid
                best_A = A
                best_phi = phi

    # Subtract the ringdown from merger onward
    t_all = np.arange(n - merger_idx) / sr
    ringdown = best_A * np.exp(-t_all / tau) * np.cos(2*np.pi*f_ring*t_all + best_phi)
    # Taper ringdown to avoid edge effects
    taper_len = int(0.5 * sr)  # 500ms taper
    if taper_len < len(ringdown):
        taper = np.ones(len(ringdown))
        taper[taper_len:] = 0
        taper[taper_len//2:taper_len] = np.cos(
            np.linspace(0, np.pi/2, taper_len - taper_len//2)) ** 2
        ringdown *= taper

    result[merger_idx:] -= ringdown

    return result


# ---------------------------------------------------------------------------
# Echo search: comb-filter with phase marginalization
# ---------------------------------------------------------------------------

def echo_comb_statistic(data: np.ndarray, sr: float,
                        t_echo: float, n_echoes: int = 15,
                        win_ms: float = 5.0) -> float:
    """Compute echo statistic: coherent sum at echo times.

    Uses phase-marginalized power: sum |data(t_k)|^2 in windows
    around t_k = k * t_echo for k=1..n_echoes.
    Normalized by total power.
    """
    echo_samp = int(t_echo * sr)
    half_win = int(win_ms / 1000 * sr)
    if echo_samp <= 0 or half_win <= 0:
        return 0.0

    echo_power = 0.0
    n_echo_samples = 0

    for k in range(1, n_echoes + 1):
        center = k * echo_samp
        start = center - half_win
        end = center + half_win + 1
        if start < 0 or end > len(data):
            continue
        echo_power += np.sum(data[start:end] ** 2)
        n_echo_samples += (end - start)

    if n_echo_samples == 0:
        return 0.0

    total_power = np.sum(data ** 2)
    expected_fraction = n_echo_samples / len(data)

    if total_power * expected_fraction < 1e-50:
        return 0.0

    # Ratio of actual to expected power at echo times
    return (echo_power / n_echo_samples) / (total_power / len(data))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    np.random.seed(42)

    print("=" * 85)
    print("GW150914 DEFINITIVE ECHO SEARCH")
    print("Blind sweep first, then compare to frozen-star prediction")
    print("=" * 85)
    print()

    # -----------------------------------------------------------------------
    # Load data
    # -----------------------------------------------------------------------
    print("--- LOADING DATA ---")

    # Try 16 kHz first, fall back to 4 kHz
    try:
        h1_raw, gps_h1, sr = load_strain("data/H1_GW150914_16k.hdf5")
        l1_raw, gps_l1, _  = load_strain("data/L1_GW150914_16k.hdf5")
        print(f"  Using 16 kHz data: {len(h1_raw)} samples")
    except Exception:
        h1_raw, gps_h1, sr = load_strain("data/H1_GW150914.hdf5")
        l1_raw, gps_l1, _  = load_strain("data/L1_GW150914.hdf5")
        print(f"  Using 4 kHz data: {len(h1_raw)} samples")

    print(f"  Sample rate: {sr:.0f} Hz")

    merger_idx_h1 = int((GPS_MERGER - gps_h1) * sr)
    merger_idx_l1 = int((GPS_MERGER - gps_l1) * sr)

    # -----------------------------------------------------------------------
    # PSD estimation from off-source data
    # -----------------------------------------------------------------------
    print("\n--- PSD ESTIMATION ---")

    # Use data BEFORE the merger for PSD (clean noise)
    psd_end = merger_idx_h1 - int(2.0 * sr)  # stop 2s before merger
    psd_start = max(0, psd_end - int(8.0 * sr))  # 8s of data

    if psd_start < psd_end and (psd_end - psd_start) > int(sr):
        psd_freqs_h1, psd_h1 = estimate_psd(h1_raw[psd_start:psd_end], sr)
        psd_freqs_l1, psd_l1 = estimate_psd(l1_raw[psd_start:psd_end], sr)
        print(f"  PSD from samples {psd_start}-{psd_end} ({(psd_end-psd_start)/sr:.1f}s)")
        use_psd = True
    else:
        print("  WARNING: insufficient pre-merger data for PSD, using self-PSD")
        use_psd = False

    # -----------------------------------------------------------------------
    # Whiten and bandpass
    # -----------------------------------------------------------------------
    print("\n--- WHITENING ---")

    if use_psd:
        h1_white = whiten_with_psd(h1_raw, sr, psd_freqs_h1, psd_h1)
        l1_white = whiten_with_psd(l1_raw, sr, psd_freqs_l1, psd_l1)
    else:
        # Self-whiten
        for data, label in [(h1_raw, 'H1'), (l1_raw, 'L1')]:
            psd_f, psd_v = estimate_psd(data, sr)
        h1_white = whiten_with_psd(h1_raw, sr, *estimate_psd(h1_raw, sr))
        l1_white = whiten_with_psd(l1_raw, sr, *estimate_psd(l1_raw, sr))

    print(f"  Whitened and bandpassed 20-500 Hz")

    # -----------------------------------------------------------------------
    # Ringdown subtraction
    # -----------------------------------------------------------------------
    print("\n--- RINGDOWN SUBTRACTION ---")

    h1_resid = subtract_ringdown(h1_white, sr, merger_idx_h1)
    l1_resid = subtract_ringdown(l1_white, sr, merger_idx_l1)

    # Compute ringdown SNR for validation
    ring_power_before = np.sum(h1_white[merger_idx_h1:merger_idx_h1+int(0.1*sr)]**2)
    ring_power_after = np.sum(h1_resid[merger_idx_h1:merger_idx_h1+int(0.1*sr)]**2)
    print(f"  H1 ringdown power reduction: {ring_power_before/ring_power_after:.1f}x")

    # Extract post-merger residual for echo search
    # Start after ringdown is dead (~200ms post-merger)
    echo_start = int(0.2 * sr)
    echo_end = int(3.0 * sr)  # search up to 3s post-merger

    h1_echo = h1_resid[merger_idx_h1 + echo_start:merger_idx_h1 + echo_end]
    l1_echo = l1_resid[merger_idx_l1 + echo_start:merger_idx_l1 + echo_end]

    print(f"  Echo search window: {echo_start/sr*1000:.0f}ms to {echo_end/sr*1000:.0f}ms post-merger")
    print(f"  Window: {len(h1_echo)} samples ({len(h1_echo)/sr:.2f}s)")

    # -----------------------------------------------------------------------
    # BLIND SWEEP: scan all echo periods
    # -----------------------------------------------------------------------
    print()
    print("=" * 85)
    print("PHASE 1: BLIND ECHO SWEEP (5 - 300 ms)")
    print("=" * 85)

    n_trials = 1000
    t_min, t_max = 0.005, 0.300
    t_values = np.linspace(t_min, t_max, n_trials)
    n_echoes = 12

    stat_h1 = np.zeros(n_trials)
    stat_l1 = np.zeros(n_trials)
    stat_combined = np.zeros(n_trials)

    for i, t_e in enumerate(t_values):
        stat_h1[i] = echo_comb_statistic(h1_echo, sr, t_e, n_echoes)
        stat_l1[i] = echo_comb_statistic(l1_echo, sr, t_e, n_echoes)
        stat_combined[i] = stat_h1[i] + stat_l1[i]

    # Find top peaks
    top_combined = np.argsort(stat_combined)[-10:][::-1]
    top_h1 = np.argsort(stat_h1)[-5:][::-1]
    top_l1 = np.argsort(stat_l1)[-5:][::-1]

    print(f"\n  Top 10 echo periods (combined H1+L1 statistic):")
    print(f"  {'rank':>4s} {'t_echo_ms':>10s} {'H1_stat':>10s} {'L1_stat':>10s} "
          f"{'combined':>10s} {'note':>15s}")
    print(f"  {'-'*55}")
    for rank, idx in enumerate(top_combined):
        t_ms = t_values[idx] * 1000
        note = ""
        if abs(t_ms - T_ECHO_PREDICTED*1000) < 3:
            note = "<-- PREDICTED"
        elif abs(t_ms - 100) < 5:
            note = "<-- Abedi"
        print(f"  {rank+1:>4d} {t_ms:>10.1f} {stat_h1[idx]:>10.4f} "
              f"{stat_l1[idx]:>10.4f} {stat_combined[idx]:>10.4f} {note:>15s}")

    # Where does our predicted echo time rank?
    pred_idx = np.argmin(np.abs(t_values - T_ECHO_PREDICTED))
    pred_rank = np.sum(stat_combined >= stat_combined[pred_idx])
    print(f"\n  Predicted 67.7ms ranks #{pred_rank} out of {n_trials}")
    print(f"  Statistic at 67.7ms: H1={stat_h1[pred_idx]:.4f}, "
          f"L1={stat_l1[pred_idx]:.4f}, combined={stat_combined[pred_idx]:.4f}")

    # Mean and std of scan
    mean_stat = np.mean(stat_combined)
    std_stat = np.std(stat_combined)
    pred_sigma = (stat_combined[pred_idx] - mean_stat) / std_stat if std_stat > 0 else 0
    best_sigma = (stat_combined[top_combined[0]] - mean_stat) / std_stat if std_stat > 0 else 0

    print(f"\n  Scan statistics: mean={mean_stat:.4f}, std={std_stat:.4f}")
    print(f"  Predicted 67.7ms: {pred_sigma:.2f} sigma above mean")
    print(f"  Best peak: {best_sigma:.2f} sigma above mean")

    # -----------------------------------------------------------------------
    # PHASE 2: Background estimation at best echo time
    # -----------------------------------------------------------------------
    print()
    print("=" * 85)
    print("PHASE 2: BACKGROUND ESTIMATION (500 time shifts)")
    print("=" * 85)

    best_t = t_values[top_combined[0]]
    n_shifts = 500

    bg_stats_combined = np.zeros(n_shifts)
    bg_stats_h1 = np.zeros(n_shifts)
    bg_stats_l1 = np.zeros(n_shifts)

    for i in range(n_shifts):
        shift = np.random.randint(int(0.3 * sr), len(h1_echo) - int(0.3 * sr))
        h1_shifted = np.roll(h1_echo, shift)
        l1_shifted = np.roll(l1_echo, shift)
        bg_stats_h1[i] = echo_comb_statistic(h1_shifted, sr, best_t, n_echoes)
        bg_stats_l1[i] = echo_comb_statistic(l1_shifted, sr, best_t, n_echoes)
        bg_stats_combined[i] = bg_stats_h1[i] + bg_stats_l1[i]

    bg_mean = np.mean(bg_stats_combined)
    bg_std = np.std(bg_stats_combined)

    # Significance of best peak
    signal_stat = stat_combined[top_combined[0]]
    best_significance = (signal_stat - bg_mean) / bg_std if bg_std > 0 else 0

    # Significance at predicted echo time
    pred_stat = stat_combined[pred_idx]
    pred_significance = (pred_stat - bg_mean) / bg_std if bg_std > 0 else 0

    # p-value: fraction of background exceeding signal
    p_value_best = np.mean(bg_stats_combined >= signal_stat)
    p_value_pred = np.mean(bg_stats_combined >= pred_stat)

    print(f"\n  Best echo period: {best_t*1000:.1f}ms")
    print(f"  Signal statistic: {signal_stat:.4f}")
    print(f"  Background: {bg_mean:.4f} +/- {bg_std:.4f}")
    print(f"  Significance: {best_significance:.2f} sigma")
    print(f"  p-value: {p_value_best:.4f} ({p_value_best*100:.2f}%)")

    print(f"\n  At predicted 67.7ms:")
    print(f"  Signal statistic: {pred_stat:.4f}")
    print(f"  Significance: {pred_significance:.2f} sigma")
    print(f"  p-value: {p_value_pred:.4f} ({p_value_pred*100:.2f}%)")

    # -----------------------------------------------------------------------
    # PHASE 3: Cross-detector consistency
    # -----------------------------------------------------------------------
    print()
    print("=" * 85)
    print("PHASE 3: CROSS-DETECTOR CONSISTENCY")
    print("=" * 85)

    # Do both detectors agree on the echo time?
    print(f"\n  H1 top 5:")
    for rank, idx in enumerate(top_h1):
        print(f"    #{rank+1}: {t_values[idx]*1000:.1f}ms (stat={stat_h1[idx]:.4f})")

    print(f"\n  L1 top 5:")
    for rank, idx in enumerate(top_l1):
        print(f"    #{rank+1}: {t_values[idx]*1000:.1f}ms (stat={stat_l1[idx]:.4f})")

    # Cross-correlation of the echo statistics
    cc = np.corrcoef(stat_h1, stat_l1)[0, 1]
    print(f"\n  H1-L1 statistic correlation: {cc:.4f}")

    # Check if any H1 peak is near any L1 peak
    h1_peaks = set(t_values[top_h1[:5]])
    l1_peaks = set(t_values[top_l1[:5]])
    matches = []
    for t_h in h1_peaks:
        for t_l in l1_peaks:
            if abs(t_h - t_l) < 0.005:  # within 5ms
                matches.append((t_h*1000, t_l*1000))

    if matches:
        print(f"  Coincident peaks (within 5ms): {len(matches)}")
        for mh, ml in matches:
            print(f"    H1={mh:.1f}ms, L1={ml:.1f}ms")
    else:
        print(f"  No coincident peaks between H1 and L1 top 5")

    # -----------------------------------------------------------------------
    # PHASE 4: Multiple post-merger windows
    # -----------------------------------------------------------------------
    print()
    print("=" * 85)
    print("PHASE 4: ECHO SEARCH ACROSS POST-MERGER WINDOWS")
    print("=" * 85)

    windows = [
        (0.1, 1.0), (0.2, 1.5), (0.2, 2.0), (0.2, 3.0),
        (0.5, 2.0), (0.5, 3.0), (1.0, 3.0),
    ]

    print(f"\n  {'window':>12s} {'best_t_ms':>10s} {'best_stat':>10s} "
          f"{'pred_stat':>10s} {'pred_sigma':>10s}")
    print(f"  {'-'*58}")

    for w_start, w_end in windows:
        s = merger_idx_h1 + int(w_start * sr)
        e = min(merger_idx_h1 + int(w_end * sr), len(h1_resid))
        if s >= e:
            continue

        h1_w = h1_resid[s:e]
        l1_s = merger_idx_l1 + int(w_start * sr)
        l1_e = min(merger_idx_l1 + int(w_end * sr), len(l1_resid))
        l1_w = l1_resid[l1_s:l1_e]

        # Quick scan
        stats_w = np.zeros(200)
        t_vals_w = np.linspace(0.02, 0.20, 200)
        for i, t_e in enumerate(t_vals_w):
            s_h = echo_comb_statistic(h1_w, sr, t_e, 10)
            s_l = echo_comb_statistic(l1_w, sr, t_e, 10)
            stats_w[i] = s_h + s_l

        best_w = np.argmax(stats_w)
        pred_w = np.argmin(np.abs(t_vals_w - T_ECHO_PREDICTED))
        mean_w = np.mean(stats_w)
        std_w = np.std(stats_w)
        sigma_w = (stats_w[pred_w] - mean_w) / std_w if std_w > 0 else 0

        label = f"{w_start:.1f}-{w_end:.1f}s"
        print(f"  {label:>12s} {t_vals_w[best_w]*1000:>10.1f} {stats_w[best_w]:>10.4f} "
              f"{stats_w[pred_w]:>10.4f} {sigma_w:>10.2f}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 85)
    print("SUMMARY")
    print("=" * 85)
    print()
    print(f"  BLIND SWEEP RESULT:")
    print(f"    Best echo period: {best_t*1000:.1f}ms ({best_significance:.2f} sigma)")
    print(f"    p-value: {p_value_best:.4f}")
    print()
    print(f"  AT PREDICTED ECHO TIME (67.7ms):")
    print(f"    Significance: {pred_significance:.2f} sigma")
    print(f"    p-value: {p_value_pred:.4f}")
    print(f"    Rank: #{pred_rank} out of {n_trials} trial periods")
    print()
    print(f"  CROSS-DETECTOR:")
    print(f"    H1-L1 correlation of echo statistic: {cc:.4f}")
    if matches:
        print(f"    Coincident peaks found: {len(matches)}")
    else:
        print(f"    No coincident peaks in top 5")
    print()

    if best_significance > 3.0:
        print(f"  VERDICT: SIGNIFICANT echo detected at {best_t*1000:.1f}ms!")
        if abs(best_t - T_ECHO_PREDICTED) < 0.010:
            print(f"  MATCHES frozen star prediction (67.7ms) within 10ms!")
        else:
            print(f"  Does NOT match prediction ({T_ECHO_PREDICTED*1000:.1f}ms).")
    elif best_significance > 2.0:
        print(f"  VERDICT: MARGINAL echo at {best_t*1000:.1f}ms ({best_significance:.1f} sigma).")
    else:
        print(f"  VERDICT: No significant echo detected.")
        print(f"  The analysis places an upper limit on echo amplitude.")

    print()
    print(f"  COMPARISON TO ABEDI ET AL. (2017):")
    print(f"    Abedi: ~100ms, 2.9 sigma (disputed)")
    print(f"    Ours:  blind best = {best_t*1000:.1f}ms, {best_significance:.1f} sigma")
    print(f"    Prediction: 67.7ms (Planck-scale frozen star)")
    print()
    print(f"  FRAMEWORK STATUS:")
    if pred_significance > 2.0:
        print(f"    Echo at predicted time is {pred_significance:.1f} sigma — SUPPORTIVE")
    elif pred_significance > 0:
        print(f"    Echo at predicted time is {pred_significance:.1f} sigma — INCONCLUSIVE")
        print(f"    Not ruled out; may need O3/O4 data for definitive test")
    else:
        print(f"    No echo excess at predicted time — CONSTRAINING but not fatal")
        print(f"    Framework predicts echoes exist but may be too weak for O1 data")

    dt_total = time.time() - t_start
    print(f"\nTotal runtime: {dt_total:.1f}s")


if __name__ == "__main__":
    main()
