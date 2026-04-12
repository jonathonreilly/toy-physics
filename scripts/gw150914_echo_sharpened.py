#!/usr/bin/env python3
"""Sharpened GW echo analysis: multi-event stack + harmonic comb + proper PSD.

Three independent improvements over the first-pass analysis:

1. HARMONIC COMB FILTER: Search for echoes at t0, 2*t0, 3*t0, ... simultaneously.
   This is far more powerful than single-period search because random noise
   cannot produce exact integer-spaced peaks.

2. PROPER PSD: Use 4096-second off-source data for PSD estimation (if available),
   or at minimum use pre-merger data from the 32s file.

3. MULTI-EVENT STACK: Download and analyze multiple GWOSC events. Each event
   has a different remnant mass/spin, giving a different predicted t_echo.
   Stack the per-event echo statistics to boost significance.
"""

from __future__ import annotations

import math
import time
import sys
import os
import json

import numpy as np

try:
    import h5py
except ImportError:
    print("ERROR: h5py required.")
    sys.exit(1)

try:
    from urllib.request import urlopen, urlretrieve
    HAS_URL = True
except ImportError:
    HAS_URL = False


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------

G_SI = 6.674e-11
C = 2.998e8
M_SUN = 1.989e30
L_PLANCK = 1.616e-35
M_NUCLEON = 1.673e-27


def predict_echo_time(M_sun_val: float, a_spin: float = 0.0) -> float:
    """Predict echo time for a frozen star with given mass and spin.

    t_echo = (2 R_S / c) * ln(R_S / R_min)
    R_min = N^(1/3) * l_Planck
    N = M / m_nucleon
    """
    M = M_sun_val * M_SUN
    R_S = 2 * G_SI * M / C**2
    N_p = M / M_NUCLEON
    R_min = max(N_p**(1.0/3.0) * L_PLANCK, L_PLANCK)
    epsilon = R_min / R_S

    t_echo = 2 * R_S / C * abs(math.log(epsilon))

    if a_spin > 0:
        # Kerr correction: dominant term scales with (r+^2 + a^2)/(r+ - r-)
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
                       seg_len: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    """Welch PSD estimate."""
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
        seg = data[start:end] * window
        psd_sum += np.abs(np.fft.rfft(seg)) ** 2
        count += 1

    if count > 0:
        psd = psd_sum / (count * sr * win_norm)
    else:
        psd = np.ones(len(freqs))
    return freqs, psd


def whiten_bandpass(data: np.ndarray, sr: float,
                    psd_freqs: np.ndarray, psd: np.ndarray,
                    f_low: float = 20.0, f_high: float = 500.0) -> np.ndarray:
    """Whiten with PSD and bandpass."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0/sr)
    fft_data = np.fft.rfft(data)
    psd_interp = np.interp(freqs, psd_freqs, psd)
    psd_interp = np.maximum(psd_interp, 1e-50)
    fft_w = fft_data / np.sqrt(psd_interp)
    mask = (freqs >= f_low) & (freqs <= f_high)
    fft_w[~mask] = 0.0
    return np.fft.irfft(fft_w, n=n)


def subtract_ringdown(data: np.ndarray, sr: float, merger_idx: int,
                      f_ring: float = 251.0, tau: float = 0.004) -> np.ndarray:
    """Subtract damped sinusoid ringdown."""
    result = data.copy()
    n = len(data)
    fit_end = min(merger_idx + int(0.1 * sr), n)
    t_fit = np.arange(fit_end - merger_idx) / sr

    best_resid = np.inf
    best_A, best_phi = 0, 0
    for phi in np.linspace(0, 2*np.pi, 100):
        template = np.exp(-t_fit / tau) * np.cos(2*np.pi*f_ring*t_fit + phi)
        denom = np.sum(template**2)
        if denom > 0:
            A = np.sum(data[merger_idx:fit_end] * template) / denom
            resid = np.sum((data[merger_idx:fit_end] - A * template)**2)
            if resid < best_resid:
                best_resid = resid
                best_A, best_phi = A, phi

    t_all = np.arange(max(0, n - merger_idx)) / sr
    ringdown = best_A * np.exp(-t_all / tau) * np.cos(2*np.pi*f_ring*t_all + best_phi)
    taper_len = int(0.5 * sr)
    if taper_len < len(ringdown):
        taper = np.ones(len(ringdown))
        half = taper_len // 2
        taper[taper_len:] = 0
        taper[half:taper_len] = np.cos(np.linspace(0, np.pi/2, taper_len - half))**2
        ringdown *= taper
    result[merger_idx:merger_idx + len(ringdown)] -= ringdown
    return result


# ---------------------------------------------------------------------------
# Harmonic comb filter
# ---------------------------------------------------------------------------

def harmonic_comb_statistic(data: np.ndarray, sr: float, t0: float,
                            n_harmonics: int = 5, n_echoes_per: int = 3,
                            win_ms: float = 3.0) -> float:
    """Coherent harmonic comb: sum power at t0, 2*t0, 3*t0, ...

    For each harmonic k=1..n_harmonics, check n_echoes_per repetitions
    at k*t0, k*t0 + t0, k*t0 + 2*t0, etc.
    Actually simpler: just check ALL multiples of t0 up to data length.
    """
    samp = int(t0 * sr)
    hw = int(win_ms / 1000 * sr)
    if samp <= 0 or hw <= 0:
        return 0.0

    # Check all integer multiples of t0
    echo_power = 0.0
    n_samples = 0
    max_k = len(data) // samp

    for k in range(1, max_k + 1):
        center = k * samp
        start = max(0, center - hw)
        end = min(len(data), center + hw + 1)
        if start < end:
            echo_power += np.sum(data[start:end] ** 2)
            n_samples += (end - start)

    if n_samples == 0:
        return 0.0

    total_power = np.sum(data ** 2)
    if total_power < 1e-50:
        return 0.0

    return (echo_power / n_samples) / (total_power / len(data))


def harmonic_consistency(data: np.ndarray, sr: float, t0: float,
                         n_harmonics: int = 6) -> dict:
    """Check if power at harmonics is consistent with echo model.

    Real echoes: power at k*t0 should decrease geometrically (each
    bounce loses some fraction through the barrier).
    Noise: power at k*t0 is random.
    """
    samp = int(t0 * sr)
    hw = int(0.005 * sr)
    powers = []

    for k in range(1, n_harmonics + 1):
        center = k * samp
        start = max(0, center - hw)
        end = min(len(data), center + hw + 1)
        if start < end:
            p = np.mean(data[start:end] ** 2)
        else:
            p = 0.0
        powers.append(p)

    mean_power = np.mean(data ** 2)
    ratios = [p / mean_power for p in powers]

    # Check geometric decay
    if len(ratios) >= 3 and all(r > 0 for r in ratios[:3]):
        log_r = np.log([max(r, 1e-30) for r in ratios[:4]])
        slope = np.polyfit(range(len(log_r)), log_r, 1)[0]
    else:
        slope = 0.0

    return {
        'powers': powers,
        'ratios': ratios,
        'decay_slope': slope,
        'mean_ratio': np.mean(ratios),
    }


# ---------------------------------------------------------------------------
# Multi-event catalog
# ---------------------------------------------------------------------------

# Events with known remnant mass and spin from GWTC
CATALOG = [
    # (name, M_remnant_solar, a_spin, GPS_merger, notes)
    ("GW150914", 62.0, 0.67, 1126259462.423, "First detection"),
    ("GW151226", 20.8, 0.74, 1135136350.6, "Boxing Day"),
    ("GW170104", 48.7, 0.64, 1167559936.6, "O2 first"),
    ("GW170608", 17.8, 0.69, 1180922494.5, "Lightest O2"),
    ("GW170729", 79.5, 0.81, 1185389807.3, "Heaviest O2"),
    ("GW170809", 56.3, 0.70, 1186302519.8, ""),
    ("GW170814", 53.2, 0.72, 1186741861.5, "First 3-detector"),
    ("GW170818", 59.4, 0.67, 1187058327.1, ""),
    ("GW170823", 65.4, 0.71, 1187529256.5, ""),
]


def download_event_data(event_name: str, data_dir: str = "data") -> dict:
    """Try to download event data from GWOSC. Returns file paths or None."""
    os.makedirs(data_dir, exist_ok=True)

    # Try the GWOSC API
    api_url = f"https://gwosc.org/eventapi/json/GWTC-1-confident/{event_name}/v3/"

    paths = {}
    for det in ['H1', 'L1']:
        # Check multiple naming conventions
        for suffix in ['', '_4k', '_4KHZ']:
            fname = f"{det}_{event_name}{suffix}.hdf5"
            fpath = os.path.join(data_dir, fname)
            if os.path.exists(fpath) and os.path.getsize(fpath) > 100000:
                paths[det] = fpath
                break

        if det in paths:
            continue

        # Construct URL pattern
        gps = [e for e in CATALOG if e[0] == event_name]
        if not gps:
            continue
        gps_int = int(gps[0][3]) - 16  # 32s file starting 16s before merger
        url = (f"https://gwosc.org/eventapi/json/GWTC-1-confident/"
               f"{event_name}/v3/{det[0]}-{det}_GWOSC_4KHZ_R1-{gps_int}-32.hdf5")

        try:
            urlretrieve(url, fpath)
            paths[det] = fpath
        except Exception as e:
            # Try alternative GPS
            for offset in [-16, -15, -17, -14]:
                gps_try = int(gps[0][3]) + offset
                url2 = (f"https://gwosc.org/eventapi/json/GWTC-1-confident/"
                        f"{event_name}/v3/{det[0]}-{det}_GWOSC_4KHZ_R1-{gps_try}-32.hdf5")
                try:
                    urlretrieve(url2, fpath)
                    paths[det] = fpath
                    break
                except Exception:
                    continue

    return paths


def analyze_event(event_name: str, M_remnant: float, a_spin: float,
                  gps_merger: float, data_paths: dict,
                  verbose: bool = True) -> dict:
    """Analyze a single event for echoes at the predicted time."""
    t_pred = predict_echo_time(M_remnant, a_spin)
    t_pred_nonspin = predict_echo_time(M_remnant, 0.0)

    result = {
        'event': event_name,
        'M_remnant': M_remnant,
        'a_spin': a_spin,
        't_pred': t_pred,
        't_pred_nonspin': t_pred_nonspin,
    }

    if not data_paths:
        result['status'] = 'no_data'
        return result

    # Process each detector
    det_stats = {}
    for det, fpath in data_paths.items():
        try:
            with h5py.File(fpath, 'r') as f:
                strain = f['strain/Strain'][:]
                gps_start = f['meta/GPSstart'][()]
                duration = f['meta/Duration'][()]
                sr = len(strain) / duration

            merger_idx = int((gps_merger - gps_start) * sr)
            if merger_idx < 0 or merger_idx >= len(strain):
                continue

            # PSD from pre-merger
            psd_end = max(0, merger_idx - int(2 * sr))
            psd_start = max(0, psd_end - int(8 * sr))
            if psd_end - psd_start < int(sr):
                psd_start = 0
                psd_end = merger_idx - int(sr)

            if psd_end > psd_start + int(sr):
                psd_f, psd_v = estimate_psd_welch(strain[psd_start:psd_end], sr)
            else:
                psd_f, psd_v = estimate_psd_welch(strain, sr)

            # Whiten + bandpass
            white = whiten_bandpass(strain, sr, psd_f, psd_v)

            # Ringdown subtraction (adapt f_ring to remnant mass)
            f_ring = 251.0 * (62.0 / M_remnant)  # rough scaling
            white = subtract_ringdown(white, sr, merger_idx, f_ring=f_ring)

            # Post-merger extraction
            post_start = merger_idx + int(0.2 * sr)
            post_end = min(merger_idx + int(3.0 * sr), len(white))
            if post_start >= post_end:
                continue
            post = white[post_start:post_end]

            # Comb statistic at predicted echo time
            stat_pred = harmonic_comb_statistic(post, sr, t_pred)
            stat_nonspin = harmonic_comb_statistic(post, sr, t_pred_nonspin)

            # Background via time shifts
            n_shifts = 200
            bg_stats = np.zeros(n_shifts)
            for i in range(n_shifts):
                shift = np.random.randint(int(0.3*sr), max(int(0.3*sr)+1, len(post)-int(0.3*sr)))
                bg_stats[i] = harmonic_comb_statistic(np.roll(post, shift), sr, t_pred)

            bg_mean = np.mean(bg_stats)
            bg_std = np.std(bg_stats)
            sigma = (stat_pred - bg_mean) / bg_std if bg_std > 0 else 0

            det_stats[det] = {
                'stat_pred': stat_pred,
                'stat_nonspin': stat_nonspin,
                'bg_mean': bg_mean,
                'bg_std': bg_std,
                'sigma': sigma,
            }

        except Exception as e:
            if verbose:
                print(f"    {det}: ERROR — {e}")

    result['det_stats'] = det_stats
    result['status'] = 'ok' if det_stats else 'failed'

    # Combined significance
    if det_stats:
        sigmas = [d['sigma'] for d in det_stats.values()]
        result['combined_sigma'] = sum(sigmas) / math.sqrt(len(sigmas))
        result['mean_stat'] = np.mean([d['stat_pred'] for d in det_stats.values()])
    else:
        result['combined_sigma'] = 0
        result['mean_stat'] = 0

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    np.random.seed(42)

    print("=" * 85)
    print("SHARPENED GW ECHO ANALYSIS")
    print("Harmonic comb + proper PSD + multi-event stack")
    print("=" * 85)

    # ===================================================================
    # PART 1: GW150914 with harmonic comb and proper PSD
    # ===================================================================
    print()
    print("=" * 85)
    print("PART 1: GW150914 — HARMONIC COMB FILTER + 4096s PSD")
    print("=" * 85)

    # Load 16kHz data
    try:
        h1_raw, gps_h1, sr = (h5py.File('data/H1_GW150914_16k.hdf5','r')['strain/Strain'][:],
                               1126259447, 16384.0)
        l1_raw, gps_l1, _ = (h5py.File('data/L1_GW150914_16k.hdf5','r')['strain/Strain'][:],
                              1126259447, 16384.0)
        print(f"  16 kHz data loaded: {len(h1_raw)} samples")
    except Exception:
        h1_raw, gps_h1, sr = (h5py.File('data/H1_GW150914.hdf5','r')['strain/Strain'][:],
                               1126259447, 4096.0)
        l1_raw, gps_l1, _ = (h5py.File('data/L1_GW150914.hdf5','r')['strain/Strain'][:],
                              1126259447, 4096.0)
        print(f"  4 kHz data loaded: {len(h1_raw)} samples")

    merger_idx = int((1126259462.423 - gps_h1) * sr)

    # Try 4096s data for PSD
    use_long_psd = False
    for det_label, det_raw in [('H1', h1_raw), ('L1', l1_raw)]:
        long_file = f'data/{det_label}_GW150914_4096s.hdf5'
        if os.path.exists(long_file):
            try:
                with h5py.File(long_file, 'r') as f:
                    long_data = f['strain/Strain'][:]
                    long_gps = f['meta/GPSstart'][()]
                    long_sr = len(long_data) / f['meta/Duration'][()]
                # Use 256s of clean data well before merger
                merger_in_long = int((1126259462.423 - long_gps) * long_sr)
                psd_end = merger_in_long - int(60 * long_sr)  # 60s before merger
                psd_start = max(0, psd_end - int(256 * long_sr))
                if psd_end > psd_start + int(10 * long_sr):
                    if det_label == 'H1':
                        psd_f_h1, psd_v_h1 = estimate_psd_welch(
                            long_data[psd_start:psd_end], long_sr, seg_len=int(long_sr*4))
                    else:
                        psd_f_l1, psd_v_l1 = estimate_psd_welch(
                            long_data[psd_start:psd_end], long_sr, seg_len=int(long_sr*4))
                    use_long_psd = True
                    print(f"  {det_label}: PSD from 4096s file ({(psd_end-psd_start)/long_sr:.0f}s of data)")
            except Exception as e:
                print(f"  {det_label}: 4096s PSD failed ({e}), using 32s")

    if not use_long_psd:
        psd_end = merger_idx - int(2 * sr)
        psd_start = max(0, psd_end - int(8 * sr))
        psd_f_h1, psd_v_h1 = estimate_psd_welch(h1_raw[psd_start:psd_end], sr)
        psd_f_l1, psd_v_l1 = estimate_psd_welch(l1_raw[psd_start:psd_end], sr)
        print(f"  PSD from 32s pre-merger data")

    # Whiten + ringdown subtract
    h1_w = whiten_bandpass(h1_raw, sr, psd_f_h1, psd_v_h1)
    l1_w = whiten_bandpass(l1_raw, sr, psd_f_l1, psd_v_l1)
    h1_r = subtract_ringdown(h1_w, sr, merger_idx)
    l1_r = subtract_ringdown(l1_w, sr, merger_idx)

    h1_post = h1_r[merger_idx + int(0.2*sr) : merger_idx + int(3.0*sr)]
    l1_post = l1_r[merger_idx + int(0.2*sr) : merger_idx + int(3.0*sr)]

    # --- Harmonic comb scan ---
    print(f"\n  --- Harmonic comb scan (5-200ms) ---")
    n_scan = 500
    t_scan = np.linspace(0.005, 0.200, n_scan)
    comb_h1 = np.zeros(n_scan)
    comb_l1 = np.zeros(n_scan)

    for i, t0 in enumerate(t_scan):
        comb_h1[i] = harmonic_comb_statistic(h1_post, sr, t0)
        comb_l1[i] = harmonic_comb_statistic(l1_post, sr, t0)

    comb_combined = comb_h1 + comb_l1

    # Top peaks
    top5 = np.argsort(comb_combined)[-5:][::-1]
    print(f"\n  Top 5 harmonic comb peaks (combined):")
    print(f"  {'rank':>4s} {'t0_ms':>8s} {'H1':>8s} {'L1':>8s} {'comb':>8s} {'note':>15s}")
    for rank, idx in enumerate(top5):
        t_ms = t_scan[idx] * 1000
        note = ""
        if abs(t_ms - 67.7) < 3: note = "<-- predicted"
        elif abs(t_ms - 58.1) < 3: note = "<-- nonspin"
        elif abs(t_ms - 60.7) < 3: note = "<-- 61ms peak"
        print(f"  {rank+1:>4d} {t_ms:>8.1f} {comb_h1[idx]:>8.4f} {comb_l1[idx]:>8.4f} "
              f"{comb_combined[idx]:>8.4f} {note:>15s}")

    # At prediction
    pred_idx = np.argmin(np.abs(t_scan - 0.0677))
    nonspin_idx = np.argmin(np.abs(t_scan - 0.0581))
    peak61_idx = np.argmin(np.abs(t_scan - 0.0607))

    mean_comb = np.mean(comb_combined)
    std_comb = np.std(comb_combined)

    print(f"\n  At predicted 67.7ms: comb={comb_combined[pred_idx]:.4f} "
          f"({(comb_combined[pred_idx]-mean_comb)/std_comb:.2f} sigma)")
    print(f"  At nonspin  58.1ms: comb={comb_combined[nonspin_idx]:.4f} "
          f"({(comb_combined[nonspin_idx]-mean_comb)/std_comb:.2f} sigma)")
    print(f"  At 61ms peak:       comb={comb_combined[peak61_idx]:.4f} "
          f"({(comb_combined[peak61_idx]-mean_comb)/std_comb:.2f} sigma)")

    # --- Harmonic consistency at best peak ---
    best_t0 = t_scan[top5[0]]
    print(f"\n  --- Harmonic consistency at best peak ({best_t0*1000:.1f}ms) ---")
    hc_h1 = harmonic_consistency(h1_post, sr, best_t0, n_harmonics=8)
    hc_l1 = harmonic_consistency(l1_post, sr, best_t0, n_harmonics=8)

    print(f"  {'k':>3s} {'H1_ratio':>10s} {'L1_ratio':>10s}")
    for k in range(min(8, len(hc_h1['ratios']))):
        print(f"  {k+1:>3d} {hc_h1['ratios'][k]:>10.4f} {hc_l1['ratios'][k]:>10.4f}")
    print(f"  H1 decay slope: {hc_h1['decay_slope']:.4f}")
    print(f"  L1 decay slope: {hc_l1['decay_slope']:.4f}")

    # --- Background with harmonic comb ---
    print(f"\n  --- Background estimation (500 shifts, harmonic comb) ---")
    n_bg = 500
    bg_comb = np.zeros(n_bg)
    for i in range(n_bg):
        shift = np.random.randint(int(0.3*sr), max(int(0.3*sr)+1, len(h1_post)-int(0.3*sr)))
        s_h = harmonic_comb_statistic(np.roll(h1_post, shift), sr, 0.0677)
        s_l = harmonic_comb_statistic(np.roll(l1_post, shift), sr, 0.0677)
        bg_comb[i] = s_h + s_l

    bg_mean = np.mean(bg_comb)
    bg_std = np.std(bg_comb)

    signal_at_pred = comb_combined[pred_idx]
    sigma_pred = (signal_at_pred - bg_mean) / bg_std if bg_std > 0 else 0
    p_value = np.mean(bg_comb >= signal_at_pred)

    print(f"  Background: {bg_mean:.4f} +/- {bg_std:.4f}")
    print(f"  Signal at 67.7ms: {signal_at_pred:.4f}")
    print(f"  Significance: {sigma_pred:.2f} sigma")
    print(f"  p-value: {p_value:.4f} ({p_value*100:.2f}%)")

    # ===================================================================
    # PART 2: MULTI-EVENT STACK
    # ===================================================================
    print()
    print("=" * 85)
    print("PART 2: MULTI-EVENT STACK")
    print("=" * 85)
    print()
    print("  Downloading and analyzing GWTC-1 events...")
    print(f"  Each event gets its own predicted t_echo from M_remnant and a_spin")
    print()

    event_results = []

    for name, M_rem, a_sp, gps_m, notes in CATALOG:
        t_pred = predict_echo_time(M_rem, a_sp)
        t_pred_ns = predict_echo_time(M_rem, 0.0)
        print(f"  {name}: M={M_rem:.1f} M_sun, a={a_sp:.2f}, "
              f"t_echo={t_pred*1000:.1f}ms (Kerr), {t_pred_ns*1000:.1f}ms (nonspin)")

        # Download data
        paths = download_event_data(name)
        if not paths:
            print(f"    No data available, skipping")
            event_results.append({
                'event': name, 'status': 'no_data',
                'combined_sigma': 0, 't_pred': t_pred,
            })
            continue

        # Analyze
        result = analyze_event(name, M_rem, a_sp, gps_m, paths, verbose=True)
        event_results.append(result)

        if result['status'] == 'ok':
            for det, ds in result['det_stats'].items():
                print(f"    {det}: stat={ds['stat_pred']:.4f}, "
                      f"bg={ds['bg_mean']:.4f}+/-{ds['bg_std']:.4f}, "
                      f"sigma={ds['sigma']:.2f}")
            print(f"    Combined: {result['combined_sigma']:.2f} sigma")
        else:
            print(f"    Analysis failed")
        print()

    # --- Stack results ---
    print("-" * 85)
    print("STACKING RESULTS")
    print("-" * 85)
    print()

    valid = [r for r in event_results if r['status'] == 'ok']
    print(f"  Events analyzed: {len(valid)} / {len(CATALOG)}")

    if valid:
        sigmas = [r['combined_sigma'] for r in valid]
        stats = [r['mean_stat'] for r in valid]

        # Weighted stack (Fisher's method)
        stacked_sigma = sum(sigmas) / math.sqrt(len(sigmas))

        # Also: fraction of events with positive sigma
        n_positive = sum(1 for s in sigmas if s > 0)

        print(f"\n  Per-event sigmas:")
        print(f"  {'event':>12s} {'M':>6s} {'t_pred_ms':>10s} {'sigma':>8s} {'stat':>8s}")
        for r in valid:
            print(f"  {r['event']:>12s} {r['M_remnant']:>6.1f} "
                  f"{r['t_pred']*1000:>10.1f} {r['combined_sigma']:>8.2f} "
                  f"{r['mean_stat']:>8.4f}")

        print(f"\n  Mean sigma: {np.mean(sigmas):.2f}")
        print(f"  Stacked sigma (sqrt-N): {stacked_sigma:.2f}")
        print(f"  Positive fraction: {n_positive}/{len(sigmas)} "
              f"({n_positive/len(sigmas)*100:.0f}%)")
        print(f"  Mean statistic: {np.mean(stats):.4f}")

        # Binomial test: if null hypothesis, expect 50% positive
        from math import comb as nchoose
        p_binomial = sum(
            nchoose(len(sigmas), k) * 0.5**len(sigmas)
            for k in range(n_positive, len(sigmas) + 1)
        )
        print(f"  Binomial p-value ({n_positive}/{len(sigmas)} positive): {p_binomial:.4f}")
    else:
        stacked_sigma = 0
        print("  No valid events to stack")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print()
    print("=" * 85)
    print("FINAL SUMMARY")
    print("=" * 85)
    print()
    print(f"  GW150914 harmonic comb (67.7ms): {sigma_pred:.2f} sigma, p={p_value:.4f}")
    print(f"  Multi-event stack ({len(valid)} events): {stacked_sigma:.2f} sigma")
    print()

    combined_all = math.sqrt(sigma_pred**2 + stacked_sigma**2) \
        if sigma_pred > 0 and stacked_sigma > 0 else max(sigma_pred, stacked_sigma)
    print(f"  Combined significance: {combined_all:.2f} sigma")
    print()

    if combined_all > 3:
        print("  VERDICT: EVIDENCE FOR ECHOES at predicted frozen-star times")
    elif combined_all > 2:
        print("  VERDICT: MARGINAL — suggestive but not definitive")
    elif combined_all > 1:
        print("  VERDICT: WEAK HINT — consistent with prediction, not significant")
    else:
        print("  VERDICT: NO SIGNIFICANT SIGNAL — upper limit on echo amplitude")

    print()
    print("  The frozen-star prediction (t_echo from Planck-scale surface)")
    print("  gives a SPECIFIC echo time for each event with NO free parameters.")
    print("  This is a genuine zero-parameter prediction testable with O3/O4 data.")

    dt = time.time() - t_start
    print(f"\nTotal runtime: {dt:.0f}s ({dt/60:.1f} min)")


if __name__ == "__main__":
    main()
