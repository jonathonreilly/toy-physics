#!/usr/bin/env python3
"""GW150914 echo search at the frozen-star predicted echo time.

Framework prediction:
  t_echo = 67.7 ms (Kerr, a/M=0.67, 62 M_sun remnant)
  f_echo = 14.8 Hz
  Surface at R_min = N^(1/3) * l_Planck (Planck-scale frozen star)

Method:
  1. Load public GWOSC strain data (4096 Hz, 32s around merger)
  2. Bandpass filter to isolate echo band (10-200 Hz)
  3. Identify merger time from peak strain
  4. Extract post-merger residual (after ringdown dies)
  5. Autocorrelation analysis at predicted echo period
  6. Comb filter / matched filter at t_echo = 67.7 ms
  7. Statistical significance via time-shifted background

Reference: Abedi, Dykaar & Afshordi (2017) arXiv:1612.00266
  claimed 2.9 sigma echoes at ~100 ms in GW150914
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    import h5py
except ImportError:
    print("ERROR: h5py required. pip install h5py")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

T_ECHO_PREDICTED = 0.0677  # seconds (Kerr prediction)
F_ECHO_PREDICTED = 1.0 / T_ECHO_PREDICTED  # ~14.8 Hz
GPS_MERGER = 1126259462.4   # approximate merger time
SAMPLE_RATE = 4096          # Hz

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_strain(filepath: str) -> tuple[np.ndarray, float, float]:
    """Load GWOSC HDF5 strain data. Returns (strain, gps_start, sample_rate)."""
    with h5py.File(filepath, 'r') as f:
        strain = f['strain/Strain'][:]
        gps_start = f['meta/GPSstart'][()]
        duration = f['meta/Duration'][()]
        sr = len(strain) / duration
    return strain, gps_start, sr


# ---------------------------------------------------------------------------
# Signal processing
# ---------------------------------------------------------------------------

def bandpass_filter(data: np.ndarray, sr: float,
                    f_low: float = 10.0, f_high: float = 200.0) -> np.ndarray:
    """Simple FFT-based bandpass filter."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)
    fft_data = np.fft.rfft(data)

    # Apply bandpass
    mask = (freqs >= f_low) & (freqs <= f_high)
    fft_data[~mask] = 0.0

    return np.fft.irfft(fft_data, n=n)


def whiten(data: np.ndarray, sr: float, seg_len: int = 4096) -> np.ndarray:
    """Simple whitening via FFT PSD estimation."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)
    fft_data = np.fft.rfft(data)

    # Estimate PSD from the data itself (rough)
    psd = np.abs(fft_data) ** 2
    # Smooth PSD
    kernel_size = max(1, len(psd) // 100)
    kernel = np.ones(kernel_size) / kernel_size
    psd_smooth = np.convolve(psd, kernel, mode='same')
    psd_smooth = np.maximum(psd_smooth, 1e-50)

    # Whiten
    fft_whitened = fft_data / np.sqrt(psd_smooth)

    return np.fft.irfft(fft_whitened, n=n)


def autocorrelation(data: np.ndarray, max_lag: int) -> np.ndarray:
    """Compute normalized autocorrelation up to max_lag."""
    n = len(data)
    mean = np.mean(data)
    var = np.var(data)
    if var < 1e-50:
        return np.zeros(max_lag)

    data_centered = data - mean
    result = np.zeros(max_lag)
    for lag in range(max_lag):
        if lag >= n:
            break
        result[lag] = np.sum(data_centered[:n-lag] * data_centered[lag:]) / (n * var)

    return result


def comb_filter_snr(data: np.ndarray, sr: float, t_echo: float,
                    n_echoes: int = 10) -> float:
    """Compute SNR of a comb filter at period t_echo.

    Sum the signal at t_merger + k * t_echo for k = 1, 2, ..., n_echoes.
    Compare to the RMS of the surrounding noise.
    """
    echo_samples = int(t_echo * sr)
    if echo_samples <= 0:
        return 0.0

    # Sum at echo times
    echo_sum = 0.0
    n_valid = 0
    for k in range(1, n_echoes + 1):
        idx = k * echo_samples
        if idx < len(data):
            # Take a small window around the echo time
            half_win = max(1, int(0.005 * sr))  # 5ms window
            start = max(0, idx - half_win)
            end = min(len(data), idx + half_win)
            echo_sum += np.sum(data[start:end] ** 2)
            n_valid += (end - start)

    if n_valid == 0:
        return 0.0

    echo_power = echo_sum / n_valid

    # Background: RMS of data away from echo times
    bg_mask = np.ones(len(data), dtype=bool)
    for k in range(1, n_echoes + 1):
        idx = k * echo_samples
        half_win = max(1, int(0.005 * sr))
        start = max(0, idx - half_win)
        end = min(len(data), idx + half_win)
        bg_mask[start:end] = False

    if bg_mask.sum() > 0:
        bg_power = np.mean(data[bg_mask] ** 2)
    else:
        bg_power = np.mean(data ** 2)

    if bg_power < 1e-50:
        return 0.0

    return echo_power / bg_power


def scan_echo_times(data: np.ndarray, sr: float,
                    t_min: float = 0.02, t_max: float = 0.20,
                    n_trials: int = 200, n_echoes: int = 8) -> dict:
    """Scan over echo times and compute SNR at each."""
    t_values = np.linspace(t_min, t_max, n_trials)
    snr_values = np.zeros(n_trials)

    for i, t in enumerate(t_values):
        snr_values[i] = comb_filter_snr(data, sr, t, n_echoes)

    return {
        't_values': t_values,
        'snr_values': snr_values,
        'best_t': t_values[np.argmax(snr_values)],
        'best_snr': np.max(snr_values),
        'predicted_snr': snr_values[np.argmin(np.abs(t_values - T_ECHO_PREDICTED))],
        'mean_snr': np.mean(snr_values),
        'std_snr': np.std(snr_values),
    }


# ---------------------------------------------------------------------------
# Background estimation via time shifts
# ---------------------------------------------------------------------------

def time_shift_background(data_h1: np.ndarray, data_l1: np.ndarray,
                          sr: float, t_echo: float,
                          n_shifts: int = 100, n_echoes: int = 8) -> dict:
    """Estimate background by computing comb-filter SNR on time-shifted data."""
    shift_snrs_h1 = []
    shift_snrs_l1 = []

    for _ in range(n_shifts):
        # Random circular shift (at least 0.5s)
        shift = np.random.randint(int(0.5 * sr), len(data_h1) - int(0.5 * sr))
        shifted_h1 = np.roll(data_h1, shift)
        shifted_l1 = np.roll(data_l1, shift)
        shift_snrs_h1.append(comb_filter_snr(shifted_h1, sr, t_echo, n_echoes))
        shift_snrs_l1.append(comb_filter_snr(shifted_l1, sr, t_echo, n_echoes))

    return {
        'h1_bg_mean': np.mean(shift_snrs_h1),
        'h1_bg_std': np.std(shift_snrs_h1),
        'l1_bg_mean': np.mean(shift_snrs_l1),
        'l1_bg_std': np.std(shift_snrs_l1),
        'h1_bg': np.array(shift_snrs_h1),
        'l1_bg': np.array(shift_snrs_l1),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    np.random.seed(42)

    print("=" * 80)
    print("GW150914 ECHO SEARCH — FROZEN STAR PREDICTION")
    print("=" * 80)
    print()
    print(f"Predicted echo time: {T_ECHO_PREDICTED*1000:.1f} ms")
    print(f"Predicted echo freq: {F_ECHO_PREDICTED:.1f} Hz")
    print(f"Source: Planck-scale frozen star (R_min = N^(1/3) * l_Planck)")
    print()

    # -----------------------------------------------------------------------
    # Load data
    # -----------------------------------------------------------------------
    print("-" * 80)
    print("LOADING DATA")
    print("-" * 80)

    h1_raw, gps_h1, sr_h1 = load_strain("data/H1_GW150914.hdf5")
    l1_raw, gps_l1, sr_l1 = load_strain("data/L1_GW150914.hdf5")

    print(f"  H1: {len(h1_raw)} samples, {sr_h1:.0f} Hz, GPS {gps_h1}")
    print(f"  L1: {len(l1_raw)} samples, {sr_l1:.0f} Hz, GPS {gps_l1}")

    sr = sr_h1
    dt = 1.0 / sr

    # Time array
    t_h1 = gps_h1 + np.arange(len(h1_raw)) / sr
    merger_idx = int((GPS_MERGER - gps_h1) * sr)
    print(f"  Merger at sample {merger_idx} (GPS {GPS_MERGER})")

    # -----------------------------------------------------------------------
    # Preprocessing
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("PREPROCESSING")
    print("-" * 80)

    # Bandpass 10-200 Hz
    h1_bp = bandpass_filter(h1_raw, sr, f_low=10.0, f_high=200.0)
    l1_bp = bandpass_filter(l1_raw, sr, f_low=10.0, f_high=200.0)
    print("  Bandpass filtered: 10-200 Hz")

    # Whiten
    h1_white = whiten(h1_bp, sr)
    l1_white = whiten(l1_bp, sr)
    print("  Whitened")

    # Extract post-merger segment (0.5s to 2.0s after merger)
    post_start = merger_idx + int(0.5 * sr)   # 500ms after merger (ringdown gone)
    post_end = merger_idx + int(2.0 * sr)     # 2s window
    post_end = min(post_end, len(h1_white))

    h1_post = h1_white[post_start:post_end]
    l1_post = l1_white[post_start:post_end]

    print(f"  Post-merger window: {(post_start - merger_idx)/sr*1000:.0f}ms "
          f"to {(post_end - merger_idx)/sr*1000:.0f}ms after merger")
    print(f"  Window length: {len(h1_post)} samples ({len(h1_post)/sr*1000:.0f}ms)")

    # -----------------------------------------------------------------------
    # Test 1: Autocorrelation at predicted echo period
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 1: AUTOCORRELATION")
    print("-" * 80)

    echo_lag = int(T_ECHO_PREDICTED * sr)
    max_lag = int(0.25 * sr)  # up to 250ms
    ac_h1 = autocorrelation(h1_post, max_lag)
    ac_l1 = autocorrelation(l1_post, max_lag)

    print(f"\n  Autocorrelation at predicted echo lag ({echo_lag} samples = "
          f"{T_ECHO_PREDICTED*1000:.1f}ms):")
    print(f"    H1: AC({echo_lag}) = {ac_h1[echo_lag]:.6f}")
    print(f"    L1: AC({echo_lag}) = {ac_l1[echo_lag]:.6f}")

    # Check neighboring lags
    print(f"\n  AC profile around predicted lag:")
    print(f"  {'lag_ms':>8s} {'lag_samp':>8s} {'AC_H1':>10s} {'AC_L1':>10s}")
    for offset in [-10, -5, -2, -1, 0, 1, 2, 5, 10]:
        lag = echo_lag + offset
        if 0 <= lag < max_lag:
            print(f"  {lag/sr*1000:>8.1f} {lag:>8d} {ac_h1[lag]:>10.6f} "
                  f"{ac_l1[lag]:>10.6f}")

    # Find the peak AC in the echo range (50-100ms)
    ac_range_start = int(0.050 * sr)
    ac_range_end = int(0.100 * sr)
    h1_peak_lag = ac_range_start + np.argmax(ac_h1[ac_range_start:ac_range_end])
    l1_peak_lag = ac_range_start + np.argmax(ac_l1[ac_range_start:ac_range_end])

    print(f"\n  Peak AC in 50-100ms range:")
    print(f"    H1: lag={h1_peak_lag/sr*1000:.1f}ms, AC={ac_h1[h1_peak_lag]:.6f}")
    print(f"    L1: lag={l1_peak_lag/sr*1000:.1f}ms, AC={ac_l1[l1_peak_lag]:.6f}")

    # -----------------------------------------------------------------------
    # Test 2: Comb filter SNR at predicted echo time
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 2: COMB FILTER SNR")
    print("-" * 80)

    n_echoes = 8
    snr_h1 = comb_filter_snr(h1_post, sr, T_ECHO_PREDICTED, n_echoes)
    snr_l1 = comb_filter_snr(l1_post, sr, T_ECHO_PREDICTED, n_echoes)

    print(f"\n  Comb filter at t_echo = {T_ECHO_PREDICTED*1000:.1f}ms, "
          f"{n_echoes} echoes:")
    print(f"    H1 power ratio: {snr_h1:.4f}")
    print(f"    L1 power ratio: {snr_l1:.4f}")

    # -----------------------------------------------------------------------
    # Test 3: Scan over echo times
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 3: ECHO TIME SCAN (20-200ms)")
    print("-" * 80)

    scan_h1 = scan_echo_times(h1_post, sr, t_min=0.02, t_max=0.20,
                               n_trials=200, n_echoes=n_echoes)
    scan_l1 = scan_echo_times(l1_post, sr, t_min=0.02, t_max=0.20,
                               n_trials=200, n_echoes=n_echoes)

    print(f"\n  H1 scan:")
    print(f"    Best echo time: {scan_h1['best_t']*1000:.1f}ms (SNR={scan_h1['best_snr']:.4f})")
    print(f"    At predicted 67.7ms: SNR={scan_h1['predicted_snr']:.4f}")
    print(f"    Mean SNR: {scan_h1['mean_snr']:.4f} +/- {scan_h1['std_snr']:.4f}")

    h1_sigma = (scan_h1['predicted_snr'] - scan_h1['mean_snr']) / scan_h1['std_snr'] \
        if scan_h1['std_snr'] > 0 else 0
    print(f"    Predicted vs mean: {h1_sigma:.2f} sigma")

    print(f"\n  L1 scan:")
    print(f"    Best echo time: {scan_l1['best_t']*1000:.1f}ms (SNR={scan_l1['best_snr']:.4f})")
    print(f"    At predicted 67.7ms: SNR={scan_l1['predicted_snr']:.4f}")
    print(f"    Mean SNR: {scan_l1['mean_snr']:.4f} +/- {scan_l1['std_snr']:.4f}")

    l1_sigma = (scan_l1['predicted_snr'] - scan_l1['mean_snr']) / scan_l1['std_snr'] \
        if scan_l1['std_snr'] > 0 else 0
    print(f"    Predicted vs mean: {l1_sigma:.2f} sigma")

    # Top 5 echo times for each detector
    print(f"\n  Top 5 echo times:")
    for det, scan in [("H1", scan_h1), ("L1", scan_l1)]:
        top_idx = np.argsort(scan['snr_values'])[-5:][::-1]
        for rank, idx in enumerate(top_idx):
            print(f"    {det} #{rank+1}: t={scan['t_values'][idx]*1000:.1f}ms, "
                  f"SNR={scan['snr_values'][idx]:.4f}")

    # -----------------------------------------------------------------------
    # Test 4: Time-shift background estimation
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 4: BACKGROUND ESTIMATION (100 time shifts)")
    print("-" * 80)

    bg = time_shift_background(h1_post, l1_post, sr, T_ECHO_PREDICTED,
                                n_shifts=100, n_echoes=n_echoes)

    h1_sig = (snr_h1 - bg['h1_bg_mean']) / bg['h1_bg_std'] \
        if bg['h1_bg_std'] > 0 else 0
    l1_sig = (snr_l1 - bg['l1_bg_mean']) / bg['l1_bg_std'] \
        if bg['l1_bg_std'] > 0 else 0

    print(f"\n  H1:")
    print(f"    Signal power ratio: {snr_h1:.4f}")
    print(f"    Background: {bg['h1_bg_mean']:.4f} +/- {bg['h1_bg_std']:.4f}")
    print(f"    Significance: {h1_sig:.2f} sigma")

    print(f"\n  L1:")
    print(f"    Signal power ratio: {snr_l1:.4f}")
    print(f"    Background: {bg['l1_bg_mean']:.4f} +/- {bg['l1_bg_std']:.4f}")
    print(f"    Significance: {l1_sig:.2f} sigma")

    # Combined significance (Fisher's method or simple quadrature)
    combined_sig = math.sqrt(h1_sig**2 + l1_sig**2) if (h1_sig > 0 and l1_sig > 0) else 0
    print(f"\n  Combined significance: {combined_sig:.2f} sigma (quadrature)")

    # -----------------------------------------------------------------------
    # Test 5: Cross-detector correlation at echo lag
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 5: CROSS-DETECTOR CORRELATION")
    print("-" * 80)

    # Cross-correlation between H1 and L1 post-merger
    min_len = min(len(h1_post), len(l1_post))
    h1_c = h1_post[:min_len]
    l1_c = l1_post[:min_len]

    # Normalize
    h1_n = (h1_c - np.mean(h1_c)) / (np.std(h1_c) + 1e-30)
    l1_n = (l1_c - np.mean(l1_c)) / (np.std(l1_c) + 1e-30)

    # Cross-correlation at zero lag and echo lag
    cc_zero = np.sum(h1_n * l1_n) / min_len
    cc_lags = []
    for lag_ms in [0, 10, 50, 67.7, 100, 135.4, 200]:
        lag_samp = int(lag_ms / 1000 * sr)
        if lag_samp < min_len:
            cc = np.sum(h1_n[:min_len-lag_samp] * l1_n[lag_samp:]) / (min_len - lag_samp)
        else:
            cc = 0.0
        cc_lags.append((lag_ms, cc))

    print(f"\n  Cross-correlation H1 x L1:")
    print(f"  {'lag_ms':>8s} {'CC':>10s}")
    for lag_ms, cc in cc_lags:
        marker = " <-- predicted" if abs(lag_ms - 67.7) < 1 else \
                 " <-- 2x predicted" if abs(lag_ms - 135.4) < 1 else ""
        print(f"  {lag_ms:>8.1f} {cc:>10.6f}{marker}")

    # -----------------------------------------------------------------------
    # Test 6: Different post-merger windows
    # -----------------------------------------------------------------------
    print()
    print("-" * 80)
    print("TEST 6: ECHO SEARCH IN DIFFERENT POST-MERGER WINDOWS")
    print("-" * 80)

    windows = [
        ("0.2-1.0s", 0.2, 1.0),
        ("0.3-1.5s", 0.3, 1.5),
        ("0.5-2.0s", 0.5, 2.0),
        ("1.0-3.0s", 1.0, 3.0),
        ("0.2-3.0s", 0.2, 3.0),
    ]

    print(f"\n  {'window':>12s} {'H1_SNR':>8s} {'L1_SNR':>8s} {'H1_AC':>8s} {'L1_AC':>8s}")
    print(f"  {'-'*50}")

    for label, t_start_w, t_end_w in windows:
        w_start = merger_idx + int(t_start_w * sr)
        w_end = min(merger_idx + int(t_end_w * sr), len(h1_white))
        if w_start >= w_end:
            continue

        h1_w = h1_white[w_start:w_end]
        l1_w = l1_white[w_start:w_end]

        snr_h = comb_filter_snr(h1_w, sr, T_ECHO_PREDICTED, n_echoes)
        snr_l = comb_filter_snr(l1_w, sr, T_ECHO_PREDICTED, n_echoes)

        ac_h = autocorrelation(h1_w, echo_lag + 1)
        ac_l = autocorrelation(l1_w, echo_lag + 1)
        ac_h_val = ac_h[echo_lag] if echo_lag < len(ac_h) else 0
        ac_l_val = ac_l[echo_lag] if echo_lag < len(ac_l) else 0

        print(f"  {label:>12s} {snr_h:>8.4f} {snr_l:>8.4f} "
              f"{ac_h_val:>8.6f} {ac_l_val:>8.6f}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"  Predicted echo time: {T_ECHO_PREDICTED*1000:.1f}ms")
    print(f"  Predicted echo freq: {F_ECHO_PREDICTED:.1f} Hz")
    print()
    print(f"  Autocorrelation at predicted lag:")
    print(f"    H1: {ac_h1[echo_lag]:.6f}")
    print(f"    L1: {ac_l1[echo_lag]:.6f}")
    print()
    print(f"  Comb filter significance (vs time-shift background):")
    print(f"    H1: {h1_sig:.2f} sigma")
    print(f"    L1: {l1_sig:.2f} sigma")
    print(f"    Combined: {combined_sig:.2f} sigma")
    print()

    if combined_sig > 3.0:
        print("  RESULT: SIGNIFICANT echo signal detected at predicted time!")
    elif combined_sig > 2.0:
        print("  RESULT: MARGINAL echo signal at predicted time.")
    elif combined_sig > 1.0:
        print("  RESULT: WEAK hint, not significant. Consistent with noise.")
    else:
        print("  RESULT: No significant echo signal at predicted time.")
        print("  This does NOT invalidate the frozen star prediction —")
        print("  echoes may be too weak to detect with current sensitivity.")

    print()
    print("  CAVEATS:")
    print("  - This is a simplified analysis (not a full matched-filter search)")
    print("  - Proper analysis requires careful PSD estimation, glitch removal,")
    print("    and injection studies to calibrate sensitivity")
    print("  - The 4096 Hz sample rate limits us to echoes above ~10 Hz")
    print("  - Abedi et al. used a more sophisticated method and found 2.9 sigma")
    print("  - A null result here is expected given the simple analysis")

    dt_total = time.time() - t_start
    print(f"\nTotal runtime: {dt_total:.1f}s")


if __name__ == "__main__":
    main()
