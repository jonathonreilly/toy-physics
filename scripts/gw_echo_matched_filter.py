#!/usr/bin/env python3
"""Matched-filter echo search using the ringdown as template.

The Abedi et al. (2017) insight: the echo IS the ringdown signal
reflected from the near-horizon surface. So the optimal matched filter
uses the actual measured ringdown waveform as the template, shifted
to t_merger + k * t_echo.

Method (per event):
  1. Extract the ringdown segment (merger to merger+100ms) as template
  2. Whiten both template and data with proper PSD
  3. Compute matched-filter SNR: rho(t) = integral h(t') * d(t+t') dt' / sigma
  4. Evaluate rho at predicted echo times t_echo, 2*t_echo, 3*t_echo
  5. Also sweep t_echo from 10-300ms to find the best blind match
  6. Background from 1000 time shifts

This is the closest to a proper GW echo search without a full
Bayesian pipeline.
"""

from __future__ import annotations

import math
import time
import sys
import os

import numpy as np

try:
    import h5py
except ImportError:
    print("ERROR: h5py required.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------

G_SI = 6.674e-11
C = 2.998e8
M_SUN = 1.989e30
L_PLANCK = 1.616e-35
M_NUCLEON = 1.673e-27


def predict_echo_time(M_sun_val: float, a_spin: float = 0.0) -> float:
    M = M_sun_val * M_SUN
    R_S = 2 * G_SI * M / C**2
    N_p = M / M_NUCLEON
    R_min = max(N_p**(1.0/3.0) * L_PLANCK, L_PLANCK)
    epsilon = R_min / R_S
    t_echo = 2 * R_S / C * abs(math.log(epsilon))
    if a_spin > 0:
        r_plus = R_S / 2 * (1 + math.sqrt(max(0, 1 - a_spin**2)))
        r_minus = R_S / 2 * (1 - math.sqrt(max(0, 1 - a_spin**2)))
        a_phys = a_spin * G_SI * M / C**2
        if r_plus > r_minus:
            kerr_factor = (r_plus**2 + a_phys**2) / (r_plus - r_minus)
            t_echo = 2 / C * kerr_factor * abs(math.log(epsilon))
    return t_echo


# ---------------------------------------------------------------------------
# Signal processing
# ---------------------------------------------------------------------------

def estimate_psd_welch(data: np.ndarray, sr: float,
                       seg_len: int = 0) -> tuple[np.ndarray, np.ndarray]:
    if seg_len <= 0:
        seg_len = min(4 * int(sr), len(data) // 4)
    seg_len = max(256, seg_len)
    overlap = seg_len // 2
    n_seg = max(1, (len(data) - overlap) // (seg_len - overlap))
    freqs = np.fft.rfftfreq(seg_len, d=1.0/sr)
    psd_sum = np.zeros(len(freqs))
    window = np.hanning(seg_len)
    win_norm = np.sum(window ** 2)
    count = 0
    for i in range(n_seg):
        start = i * (seg_len - overlap)
        end = start + seg_len
        if end > len(data):
            break
        psd_sum += np.abs(np.fft.rfft(data[start:end] * window)) ** 2
        count += 1
    if count > 0:
        psd = psd_sum / (count * sr * win_norm)
    else:
        psd = np.ones(len(freqs))
    return freqs, np.maximum(psd, 1e-50)


def whiten_segment(data: np.ndarray, sr: float,
                   psd_freqs: np.ndarray, psd: np.ndarray,
                   f_low: float = 20.0, f_high: float = 500.0) -> np.ndarray:
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)
    fft_data = np.fft.rfft(data)
    psd_interp = np.interp(freqs, psd_freqs, psd)
    psd_interp = np.maximum(psd_interp, 1e-50)
    fft_w = fft_data / np.sqrt(psd_interp)
    mask = (freqs >= f_low) & (freqs <= f_high)
    fft_w[~mask] = 0.0
    return np.fft.irfft(fft_w, n=n)


# ---------------------------------------------------------------------------
# Matched filter
# ---------------------------------------------------------------------------

def matched_filter_snr(data: np.ndarray, template: np.ndarray,
                       sr: float) -> np.ndarray:
    """Compute matched-filter SNR time series.

    rho(t) = (1/sigma) * integral template(t') * data(t + t') dt'

    Implemented via FFT cross-correlation.
    """
    n = len(data)
    n_t = len(template)

    # Zero-pad template to data length
    template_padded = np.zeros(n)
    template_padded[:n_t] = template

    # Cross-correlation via FFT
    fft_data = np.fft.rfft(data)
    fft_template = np.fft.rfft(template_padded)

    # Matched filter output (unnormalized)
    cc = np.fft.irfft(fft_data * np.conj(fft_template), n=n)

    # Normalize by template energy
    template_norm = np.sqrt(np.sum(template ** 2))
    if template_norm > 0:
        cc /= template_norm

    # Normalize by local data RMS
    data_rms = np.sqrt(np.mean(data ** 2))
    if data_rms > 0:
        cc /= data_rms

    return cc


def extract_ringdown_template(data: np.ndarray, sr: float,
                              merger_idx: int,
                              duration_ms: float = 80.0) -> np.ndarray:
    """Extract the ringdown waveform as echo template.

    The template is the data from merger to merger + duration_ms,
    windowed with a Tukey taper.
    """
    n_samp = int(duration_ms / 1000 * sr)
    start = merger_idx
    end = min(start + n_samp, len(data))

    template = data[start:end].copy()

    # Apply Tukey window (taper edges)
    n = len(template)
    taper_frac = 0.3
    taper_len = int(n * taper_frac / 2)
    if taper_len > 0:
        # Rising edge
        template[:taper_len] *= 0.5 * (1 - np.cos(np.pi * np.arange(taper_len) / taper_len))
        # Falling edge
        template[-taper_len:] *= 0.5 * (1 + np.cos(np.pi * np.arange(taper_len) / taper_len))

    return template


# ---------------------------------------------------------------------------
# Echo search per event
# ---------------------------------------------------------------------------

def search_event(event_name: str, M_remnant: float, a_spin: float,
                 gps_merger: float, data_dir: str = "data",
                 n_bg_shifts: int = 500) -> dict:
    """Full matched-filter echo search for one event."""

    t_pred = predict_echo_time(M_remnant, a_spin)
    t_pred_ns = predict_echo_time(M_remnant, 0.0)
    f_ring = 251.0 * (62.0 / M_remnant)  # rough ringdown freq scaling

    result = {
        'event': event_name,
        'M_remnant': M_remnant,
        'a_spin': a_spin,
        't_pred_kerr': t_pred,
        't_pred_nonspin': t_pred_ns,
    }

    # Load data
    det_results = {}
    for det in ['H1', 'L1']:
        fpath = None
        for suffix in ['', '_4k']:
            fp = os.path.join(data_dir, f"{det}_{event_name}{suffix}.hdf5")
            if os.path.exists(fp) and os.path.getsize(fp) > 100000:
                fpath = fp
                break
        if fpath is None:
            continue

        try:
            with h5py.File(fpath, 'r') as f:
                strain = f['strain/Strain'][:]
                gps_start = f['meta/GPSstart'][()]
                duration = f['meta/Duration'][()]
                sr = len(strain) / duration

            merger_idx = int((gps_merger - gps_start) * sr)
            if merger_idx < int(2 * sr) or merger_idx >= len(strain) - int(2 * sr):
                continue

            # PSD from pre-merger data
            psd_end = merger_idx - int(1 * sr)
            psd_start = max(0, psd_end - int(10 * sr))
            if psd_end - psd_start < int(2 * sr):
                psd_start = 0
                psd_end = merger_idx - int(0.5 * sr)

            psd_f, psd_v = estimate_psd_welch(strain[psd_start:psd_end], sr)

            # Whiten entire stretch
            whitened = whiten_segment(strain, sr, psd_f, psd_v)

            # Extract ringdown template (whitened)
            template = extract_ringdown_template(whitened, sr, merger_idx,
                                                  duration_ms=80.0)

            # Compute matched-filter SNR on post-merger data
            post_start = merger_idx + int(0.15 * sr)  # start after template ends
            post_end = min(merger_idx + int(4.0 * sr), len(whitened))
            post_data = whitened[post_start:post_end]

            mf_snr = matched_filter_snr(post_data, template, sr)

            # --- Evaluate at predicted echo times ---
            # post_data starts at 0.15s after merger
            # echo at t_e after merger = sample (t_e - 0.15)*sr in post_data
            post_offset = 0.15  # seconds

            snr_at_pred = {}
            for label, t_e in [('kerr', t_pred), ('nonspin', t_pred_ns)]:
                for mult in [1, 2, 3]:
                    t_in_post = mult * t_e - post_offset
                    samp = int(t_in_post * sr)
                    if 0 <= samp < len(mf_snr):
                        hw = int(0.003 * sr)
                        s = max(0, samp - hw)
                        e = min(len(mf_snr), samp + hw + 1)
                        peak_snr = np.max(np.abs(mf_snr[s:e]))
                        snr_at_pred[f'{label}_{mult}x'] = peak_snr

            # --- Blind sweep ---
            n_sweep = 500
            t_sweep = np.linspace(0.010, 0.300, n_sweep)
            sweep_snr = np.zeros(n_sweep)

            for i, t_e in enumerate(t_sweep):
                # Sum |SNR| at all multiples of t_e
                total = 0.0
                count = 0
                for mult in range(1, 8):
                    samp = int((mult * t_e - 0.15) * sr)
                    if 0 <= samp < len(mf_snr):
                        hw = int(0.002 * sr)
                        s = max(0, samp - hw)
                        e = min(len(mf_snr), samp + hw + 1)
                        total += np.max(np.abs(mf_snr[s:e]))
                        count += 1
                sweep_snr[i] = total / max(count, 1)

            best_sweep_idx = np.argmax(sweep_snr)
            best_sweep_t = t_sweep[best_sweep_idx]
            best_sweep_snr = sweep_snr[best_sweep_idx]

            # SNR at predicted time in sweep
            pred_sweep_idx = np.argmin(np.abs(t_sweep - t_pred))
            pred_sweep_snr = sweep_snr[pred_sweep_idx]

            # --- Background estimation ---
            bg_snrs = np.zeros(n_bg_shifts)
            for i in range(n_bg_shifts):
                shift = np.random.randint(int(0.5 * sr),
                                          max(int(0.5*sr)+1, len(post_data) - int(0.5*sr)))
                shifted = np.roll(post_data, shift)
                mf_shifted = matched_filter_snr(shifted, template, sr)

                # Evaluate at predicted echo time
                samp = int((t_pred - 0.15) * sr)
                if 0 <= samp < len(mf_shifted):
                    hw = int(0.003 * sr)
                    s = max(0, samp - hw)
                    e = min(len(mf_shifted), samp + hw + 1)
                    bg_snrs[i] = np.max(np.abs(mf_shifted[s:e]))

            bg_mean = np.mean(bg_snrs)
            bg_std = np.std(bg_snrs)

            # Signal significance — use sweep SNR at predicted time
            signal_snr = pred_sweep_snr
            # Background: sweep at predicted time on shifted data
            bg_sweep_snrs = np.zeros(n_bg_shifts)
            for i in range(n_bg_shifts):
                shift = np.random.randint(int(0.5 * sr),
                                          max(int(0.5*sr)+1, len(post_data) - int(0.5*sr)))
                shifted = np.roll(post_data, shift)
                mf_shifted = matched_filter_snr(shifted, template, sr)
                # Sweep at predicted echo time
                total_s = 0.0; count_s = 0
                for mult_s in range(1, 8):
                    samp_s = int((mult_s * t_pred - 0.15) * sr)
                    if 0 <= samp_s < len(mf_shifted):
                        hw_s = int(0.002 * sr)
                        s_s = max(0, samp_s - hw_s)
                        e_s = min(len(mf_shifted), samp_s + hw_s + 1)
                        total_s += np.max(np.abs(mf_shifted[s_s:e_s]))
                        count_s += 1
                bg_sweep_snrs[i] = total_s / max(count_s, 1)

            bg_mean = np.mean(bg_sweep_snrs)
            bg_std = np.std(bg_sweep_snrs)
            sigma = (signal_snr - bg_mean) / bg_std if bg_std > 0 else 0
            p_value = np.mean(bg_sweep_snrs >= signal_snr)

            det_results[det] = {
                'snr_at_pred': snr_at_pred,
                'best_sweep_t': best_sweep_t,
                'best_sweep_snr': best_sweep_snr,
                'pred_sweep_snr': pred_sweep_snr,
                'sweep_mean': np.mean(sweep_snr),
                'sweep_std': np.std(sweep_snr),
                'bg_mean': bg_mean,
                'bg_std': bg_std,
                'sigma': sigma,
                'p_value': p_value,
                'signal_snr': signal_snr,
            }

        except Exception as e:
            det_results[det] = {'error': str(e)}

    result['detectors'] = det_results

    # Combined significance
    sigmas = [d['sigma'] for d in det_results.values() if 'sigma' in d]
    if sigmas:
        result['combined_sigma'] = sum(sigmas) / math.sqrt(len(sigmas))
    else:
        result['combined_sigma'] = 0.0

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CATALOG = [
    ("GW150914", 62.0, 0.67, 1126259462.423),
    ("GW151226", 20.8, 0.74, 1135136350.6),
    ("GW170104", 48.7, 0.64, 1167559936.6),
    ("GW170608", 17.8, 0.69, 1180922494.5),
    ("GW170729", 79.5, 0.81, 1185389807.3),
    ("GW170809", 56.3, 0.70, 1186302519.8),
    ("GW170814", 53.2, 0.72, 1186741861.5),
    ("GW170823", 65.4, 0.71, 1187529256.5),
]


def main():
    t_start = time.time()
    np.random.seed(42)

    print("=" * 85)
    print("MATCHED-FILTER ECHO SEARCH")
    print("Ringdown template + harmonic stack + multi-event")
    print("=" * 85)
    print()
    print("Method: Use the actual ringdown waveform as the echo template.")
    print("The echo IS the ringdown reflected from the Planck-scale surface.")
    print("Matched-filter SNR is optimal for detecting a known waveform in noise.")
    print()

    all_results = []

    for name, M_rem, a_sp, gps_m in CATALOG:
        t_pred = predict_echo_time(M_rem, a_sp)
        t_pred_ns = predict_echo_time(M_rem, 0.0)

        print("-" * 85)
        print(f"EVENT: {name}  M={M_rem:.1f} M_sun  a={a_sp:.2f}")
        print(f"  Predicted: t_echo={t_pred*1000:.1f}ms (Kerr), "
              f"{t_pred_ns*1000:.1f}ms (nonspin)")
        print("-" * 85)

        result = search_event(name, M_rem, a_sp, gps_m, n_bg_shifts=500)
        all_results.append(result)

        if not result['detectors']:
            print("  No data available\n")
            continue

        for det, dr in result['detectors'].items():
            if 'error' in dr:
                print(f"  {det}: ERROR — {dr['error']}")
                continue

            print(f"\n  {det}:")
            print(f"    Matched-filter SNR at predicted echo times:")
            for label, snr in sorted(dr['snr_at_pred'].items()):
                print(f"      {label}: {snr:.4f}")

            print(f"    Blind sweep best: {dr['best_sweep_t']*1000:.1f}ms "
                  f"(SNR={dr['best_sweep_snr']:.4f})")
            print(f"    At prediction: SNR={dr['pred_sweep_snr']:.4f}")
            print(f"    Sweep stats: mean={dr['sweep_mean']:.4f}, "
                  f"std={dr['sweep_std']:.4f}")

            sigma_sweep = ((dr['pred_sweep_snr'] - dr['sweep_mean']) /
                          dr['sweep_std'] if dr['sweep_std'] > 0 else 0)
            print(f"    Pred vs sweep mean: {sigma_sweep:.2f} sigma")

            print(f"    Background (500 shifts): {dr['bg_mean']:.4f} +/- {dr['bg_std']:.4f}")
            print(f"    Signal: {dr['signal_snr']:.4f}")
            print(f"    Significance: {dr['sigma']:.2f} sigma (p={dr['p_value']:.4f})")

        print(f"\n  COMBINED: {result['combined_sigma']:.2f} sigma")
        print()

    # ===================================================================
    # Stack across events
    # ===================================================================
    print("=" * 85)
    print("MULTI-EVENT STACK")
    print("=" * 85)
    print()

    valid = [r for r in all_results if r['detectors']]
    sigmas = [r['combined_sigma'] for r in valid]

    print(f"  {'event':>12s} {'M':>6s} {'t_pred':>8s} {'sigma':>8s}")
    print(f"  {'-'*40}")
    for r in valid:
        print(f"  {r['event']:>12s} {r['M_remnant']:>6.1f} "
              f"{r['t_pred_kerr']*1000:>8.1f} {r['combined_sigma']:>8.2f}")

    if sigmas:
        mean_sigma = np.mean(sigmas)
        stacked = sum(sigmas) / math.sqrt(len(sigmas))
        n_pos = sum(1 for s in sigmas if s > 0)

        print(f"\n  Mean sigma: {mean_sigma:.3f}")
        print(f"  Stacked (sqrt-N): {stacked:.3f}")
        print(f"  Positive: {n_pos}/{len(sigmas)} ({n_pos/len(sigmas)*100:.0f}%)")

        # Weighted stack (weight by 1/t_pred ~ more echoes fit in window)
        weights = [1.0 / r['t_pred_kerr'] for r in valid]
        w_sum = sum(w * s for w, s in zip(weights, sigmas))
        w_norm = math.sqrt(sum(w**2 for w in weights))
        weighted_sigma = w_sum / w_norm if w_norm > 0 else 0
        print(f"  Weighted stack (by 1/t_pred): {weighted_sigma:.3f}")

        # Binomial
        from math import comb as nchoose
        p_binom = sum(nchoose(len(sigmas), k) * 0.5**len(sigmas)
                      for k in range(n_pos, len(sigmas)+1))
        print(f"  Binomial p-value: {p_binom:.4f}")

    # ===================================================================
    # Final verdict
    # ===================================================================
    print()
    print("=" * 85)
    print("VERDICT")
    print("=" * 85)
    print()

    if sigmas:
        best_stat = stacked
        if best_stat > 3:
            print(f"  EVIDENCE FOR ECHOES ({best_stat:.1f} sigma stacked)")
        elif best_stat > 2:
            print(f"  MARGINAL ({best_stat:.1f} sigma stacked)")
        elif best_stat > 1:
            print(f"  WEAK HINT ({best_stat:.1f} sigma stacked)")
        else:
            print(f"  NULL RESULT ({best_stat:.1f} sigma stacked)")

        print()
        print("  The frozen-star prediction gives a SPECIFIC echo time for each")
        print("  event with ZERO free parameters. The analysis uses the actual")
        print("  ringdown waveform as the matched-filter template — this is the")
        print("  optimal filter for detecting a reflected copy of the ringdown.")
        print()

        if n_pos > len(sigmas) * 0.5 + 1:
            print(f"  NOTE: {n_pos}/{len(sigmas)} events show positive excess.")
            print("  If consistent across O3/O4, this would strengthen.")
        elif n_pos == len(sigmas) // 2:
            print(f"  NOTE: {n_pos}/{len(sigmas)} positive — consistent with noise.")

    dt = time.time() - t_start
    print(f"\nTotal runtime: {dt:.0f}s ({dt/60:.1f} min)")


if __name__ == "__main__":
    main()
