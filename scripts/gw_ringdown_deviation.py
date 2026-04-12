#!/usr/bin/env python3
"""Ringdown damping deviation test: toy-physics framework vs GR.

DISTINCTIVE PREDICTION:
In GR, the QNM damping is set by perfect absorption at the horizon.
In the framework (S = L(1-f)), the f=1 surface is NOT a perfect absorber —
it's partially reflecting. This means:
  - The damping time tau should be LONGER than GR predicts
  - delta_tau/tau should be POSITIVE on average across events
  - The excess should correlate with remnant compactness

Method:
  1. Extract ringdown segment (merger to merger + 200ms)
  2. Fit damped sinusoid: h(t) = A * exp(-t/tau) * cos(2*pi*f*t + phi)
  3. Compare measured (f, tau) to GR predictions from remnant mass/spin
  4. Stack fractional deviations across all events
  5. Look for post-merger excess power (leaked lattice modes)

Uses data loading and PSD infrastructure from gw_echo_matched_filter.py.
Remnant parameters from gw_echo_full_catalog.py EVENTS dict.
"""

from __future__ import annotations

import math
import time
import sys
import os
import warnings

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.signal import hilbert

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


# ---------------------------------------------------------------------------
# GR QNM predictions (Berti et al. fitting formulae for l=2, m=2, n=0)
# ---------------------------------------------------------------------------

def qnm_freq_gr(M_remnant_sun: float, a_spin: float) -> float:
    """GR fundamental QNM frequency (Hz) for l=2,m=2,n=0.

    Fitting formula from Berti, Cardoso & Will (2006):
      omega_R = (c^3 / G*M) * [1.5251 - 1.1568*(1-a)^0.1292]
      f = omega_R / (2*pi)
    """
    M = M_remnant_sun * M_SUN
    a = min(abs(a_spin), 0.998)  # cap at near-extremal
    omega_R = (C**3 / (G_SI * M)) * (1.5251 - 1.1568 * (1.0 - a)**0.1292)
    return omega_R / (2.0 * math.pi)


def qnm_tau_gr(M_remnant_sun: float, a_spin: float) -> float:
    """GR fundamental QNM damping time (seconds) for l=2,m=2,n=0.

    Q = 0.7000 + 1.4187*(1-a)^{-0.4990}
    tau = Q / (pi * f)
    """
    a = min(abs(a_spin), 0.998)
    Q = 0.7000 + 1.4187 * (1.0 - a)**(-0.4990)
    f = qnm_freq_gr(M_remnant_sun, a_spin)
    if f <= 0:
        return 0.0
    return Q / (math.pi * f)


def qnm_quality_gr(a_spin: float) -> float:
    """GR quality factor Q for l=2,m=2,n=0."""
    a = min(abs(a_spin), 0.998)
    return 0.7000 + 1.4187 * (1.0 - a)**(-0.4990)


# ---------------------------------------------------------------------------
# Signal processing (from gw_echo_matched_filter.py)
# ---------------------------------------------------------------------------

def estimate_psd(data: np.ndarray, sr: float, seg_len: int = 0):
    """Welch PSD estimate."""
    if seg_len <= 0:
        seg_len = min(4 * int(sr), len(data) // 4)
    seg_len = max(256, seg_len)
    overlap = seg_len // 2
    freqs = np.fft.rfftfreq(seg_len, 1.0 / sr)
    psd = np.zeros(len(freqs))
    win = np.hanning(seg_len)
    wn = np.sum(win**2)
    count = 0
    for i in range((len(data) - overlap) // (seg_len - overlap)):
        s = i * (seg_len - overlap)
        e = s + seg_len
        if e > len(data):
            break
        psd += np.abs(np.fft.rfft(data[s:e] * win))**2
        count += 1
    return freqs, np.maximum(psd / (max(count, 1) * sr * wn), 1e-50)


def bandpass_whiten(data: np.ndarray, sr: float,
                    psd_freqs: np.ndarray, psd_vals: np.ndarray,
                    f_low: float = 20.0, f_high: float = 800.0) -> np.ndarray:
    """Whiten and bandpass filter the data."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    fft_data = np.fft.rfft(data)
    psd_interp = np.maximum(np.interp(freqs, psd_freqs, psd_vals), 1e-50)
    fft_data /= np.sqrt(psd_interp)
    mask = (freqs >= f_low) & (freqs <= f_high)
    fft_data[~mask] = 0.0
    return np.fft.irfft(fft_data, n=n)


# ---------------------------------------------------------------------------
# Ringdown fitting
# ---------------------------------------------------------------------------

def find_merger_peak(whitened: np.ndarray, sr: float,
                     gps_merger: float, gps_start: float) -> int:
    """Find the peak amplitude near the expected merger time.

    The merger is defined as the time of peak strain amplitude.
    We search within +/- 50ms of the catalog GPS merger time.
    """
    expected_idx = int((gps_merger - gps_start) * sr)
    search_hw = int(0.050 * sr)  # 50ms half-window
    lo = max(0, expected_idx - search_hw)
    hi = min(len(whitened), expected_idx + search_hw)
    peak_local = np.argmax(np.abs(whitened[lo:hi]))
    return lo + peak_local


def damped_sinusoid(t: np.ndarray, A: float, tau: float,
                    f0: float, phi: float) -> np.ndarray:
    """Model: h(t) = A * exp(-t/tau) * cos(2*pi*f0*t + phi)."""
    return A * np.exp(-t / tau) * np.cos(2.0 * np.pi * f0 * t + phi)


def fit_ringdown(data_segment: np.ndarray, sr: float,
                 f_guess: float, tau_guess: float,
                 t_start_offset: float = 0.003) -> dict:
    """Fit a damped sinusoid to the ringdown.

    We skip the first few ms after merger (inspiral contamination) and
    fit from t_start_offset to t_start_offset + fit_duration.

    Uses a two-stage approach:
      1. Coarse grid search over (f, tau, phi) to find the basin
      2. Nelder-Mead refinement from the best grid point

    The fit window is limited to ~8*tau_guess to avoid fitting noise.

    Returns dict with fitted parameters and uncertainties.
    """
    n_skip = int(t_start_offset * sr)
    # Fit window: up to 8*tau or 40ms, whichever is larger
    fit_duration = max(8.0 * tau_guess, 0.040)
    n_fit = min(int(fit_duration * sr), len(data_segment) - n_skip)
    segment = data_segment[n_skip:n_skip + n_fit]
    n = len(segment)
    if n < int(0.005 * sr):  # need at least 5ms of data
        return {'success': False, 'reason': 'segment too short'}

    t = np.arange(n) / sr

    # --- Cost function ---
    def cost(params):
        A, tau, f0, phi = params
        if tau <= 0 or A <= 0 or f0 <= 0:
            return 1e10
        model = A * np.exp(-t / tau) * np.cos(2.0 * np.pi * f0 * t + phi)
        return np.sum((segment - model)**2)

    # --- Stage 1: Grid search ---
    # Search around the GR prediction
    f_grid = np.linspace(f_guess * 0.6, f_guess * 1.4, 25)
    tau_grid = np.linspace(tau_guess * 0.3, tau_guess * 5.0, 20)
    phi_grid = np.linspace(-np.pi, np.pi, 12, endpoint=False)

    # Estimate amplitude from the data envelope
    analytic = hilbert(segment)
    A_est = np.max(np.abs(analytic[:max(5, int(0.005 * sr))]))

    best_cost = np.inf
    best_p = None

    for f_try in f_grid:
        for tau_try in tau_grid:
            for phi_try in phi_grid:
                c = cost([A_est, tau_try, f_try, phi_try])
                if c < best_cost:
                    best_cost = c
                    best_p = [A_est, tau_try, f_try, phi_try]

    if best_p is None:
        return {'success': False, 'reason': 'grid search found nothing'}

    # --- Stage 2: Nelder-Mead refinement ---
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = minimize(cost, best_p, method='Nelder-Mead',
                           options={'maxiter': 10000, 'xatol': 1e-10,
                                    'fatol': 1e-14})
        if res.fun < best_cost:
            best_p = list(res.x)
            best_cost = res.fun
    except Exception:
        pass  # keep grid result

    A_fit, tau_fit, f_fit, phi_fit = best_p

    # Also try with amplitude as free parameter in a second pass
    for A_scale in [0.5, 0.8, 1.0, 1.5, 2.0]:
        try:
            x0 = [A_est * A_scale, best_p[1], best_p[2], best_p[3]]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                res2 = minimize(cost, x0, method='Nelder-Mead',
                                options={'maxiter': 10000})
            if res2.fun < best_cost:
                best_cost = res2.fun
                A_fit, tau_fit, f_fit, phi_fit = res2.x
        except Exception:
            continue

    # Sanity checks
    if tau_fit <= 0 or f_fit <= 0 or A_fit <= 0:
        return {'success': False, 'reason': 'unphysical parameters'}
    if tau_fit < 0.0003 or tau_fit > 0.5:
        return {'success': False, 'reason': f'tau={tau_fit:.4f}s out of range'}
    if f_fit < 30 or f_fit > sr / 2:
        return {'success': False, 'reason': f'f={f_fit:.1f}Hz out of range'}

    # --- Uncertainty estimation ---
    model_best = damped_sinusoid(t, A_fit, tau_fit, f_fit, phi_fit)
    residual_data = segment - model_best
    sigma_res = np.std(residual_data)

    # Approximate parameter uncertainties via finite-difference Hessian
    eps_frac = [0.01, 0.01, 0.001, 0.01]
    uncertainties = {}
    param_names = ['A', 'tau', 'f', 'phi']
    best_params = [A_fit, tau_fit, f_fit, phi_fit]
    for i, (pname, eps_f) in enumerate(zip(param_names, eps_frac)):
        p_plus = list(best_params)
        p_minus = list(best_params)
        step = abs(best_params[i]) * eps_f
        if step < 1e-15:
            step = 1e-10
        p_plus[i] += step
        p_minus[i] -= step
        c_plus = cost(p_plus)
        c_minus = cost(p_minus)
        c_center = best_cost
        d2 = (c_plus + c_minus - 2.0 * c_center) / step**2
        if d2 > 0:
            uncertainties[pname] = math.sqrt(1.0 / (n * d2)) * sigma_res
        else:
            uncertainties[pname] = abs(best_params[i]) * 0.5

    # Fit quality: SNR of ringdown
    signal_power = np.sum(model_best**2)
    noise_power = np.sum(residual_data**2)
    fit_snr = math.sqrt(signal_power / max(noise_power, 1e-50))

    return {
        'success': True,
        'A': A_fit,
        'tau': tau_fit,
        'f': f_fit,
        'phi': phi_fit,
        'sigma_tau': uncertainties.get('tau', tau_fit * 0.5),
        'sigma_f': uncertainties.get('f', f_fit * 0.1),
        'fit_snr': fit_snr,
        'residual_rms': sigma_res,
        'n_points': n,
    }


# ---------------------------------------------------------------------------
# Post-merger excess power
# ---------------------------------------------------------------------------

def post_merger_excess(whitened: np.ndarray, sr: float,
                       merger_idx: int, tau_fit: float,
                       psd_freqs: np.ndarray, psd_vals: np.ndarray,
                       f_low: float = 50.0, f_high: float = 800.0) -> dict:
    """Look for excess broadband power after the ringdown dies.

    The framework predicts mode conversion at f>1 produces broadband
    high-frequency power that GR doesn't predict. We check for this
    in the window t > merger + 5*tau to t + 10*tau.

    Method: compare the band-limited power in the post-ringdown window
    to the same band power in pre-merger noise.
    """
    # Post-ringdown window: 5*tau to 10*tau after merger
    t_start = max(5.0 * tau_fit, 0.030)  # at least 30ms
    t_end = max(10.0 * tau_fit, 0.100)   # at least 100ms
    idx_start = merger_idx + int(t_start * sr)
    idx_end = merger_idx + int(t_end * sr)

    if idx_end >= len(whitened) or idx_start >= idx_end:
        return {'success': False, 'reason': 'post-ringdown window out of bounds'}

    post_segment = whitened[idx_start:idx_end]
    seg_len = len(post_segment)

    # Pre-merger noise reference (same length, well before merger)
    n_noise_segments = 10
    noise_powers = []
    for k in range(n_noise_segments):
        ns_end = merger_idx - int(1.0 * sr) - k * seg_len
        ns_start = ns_end - seg_len
        if ns_start < 0:
            break
        noise_seg = whitened[ns_start:ns_end]
        noise_powers.append(np.mean(noise_seg**2))

    if len(noise_powers) < 3:
        return {'success': False, 'reason': 'insufficient noise reference'}

    post_power = np.mean(post_segment**2)
    noise_mean = np.mean(noise_powers)
    noise_std = np.std(noise_powers)

    excess_sigma = (post_power - noise_mean) / noise_std if noise_std > 0 else 0.0
    excess_ratio = post_power / noise_mean if noise_mean > 0 else 1.0

    # Also compute frequency-resolved excess
    n_fft = min(seg_len, int(0.050 * sr))  # 50ms FFT segments
    if n_fft < 64:
        n_fft = seg_len

    freqs_fft = np.fft.rfftfreq(n_fft, 1.0 / sr)
    post_psd = np.abs(np.fft.rfft(post_segment[:n_fft]))**2 / (n_fft * sr)

    # High-frequency excess (above 2x ringdown frequency)
    # We'll report excess in 200-800 Hz band
    hf_mask = (freqs_fft >= 200) & (freqs_fft <= 800)
    hf_power = np.mean(post_psd[hf_mask]) if np.any(hf_mask) else 0.0

    return {
        'success': True,
        'post_power': post_power,
        'noise_mean': noise_mean,
        'noise_std': noise_std,
        'excess_sigma': excess_sigma,
        'excess_ratio': excess_ratio,
        'hf_power': hf_power,
        'window_ms': (t_end - t_start) * 1000,
    }


# ---------------------------------------------------------------------------
# Event catalog with PE remnant parameters
# ---------------------------------------------------------------------------

# From gw_echo_full_catalog.py EVENTS dict
# Format: event_name -> (M_remnant_sun, a_spin, gps_merger)
# NOTE: a_spin is set to 0.67 for most O3 events (PE median for typical BBH).
# For O1/O2 events with published PE, we use better values.
EVENTS = {
    "GW150914": (63.1, 0.69, 1126259462.423),
    "GW151226": (20.5, 0.74, 1135136350.6),
    "GW170104": (48.9, 0.64, 1167559936.6),
    "GW170608": (17.8, 0.69, 1180922494.5),
    "GW170729": (79.5, 0.81, 1185389807.3),
    "GW170809": (56.3, 0.70, 1186302519.8),
    "GW170814": (53.2, 0.72, 1186741861.5),
    "GW170823": (65.4, 0.71, 1187529256.5),
    "GW190403_051519": (102.2, 0.67, 1238303737.2),
    "GW190408_181802": (41.1, 0.67, 1238782700.3),
    "GW190413_052954": (56.0, 0.67, 1239168612.5),
    "GW190413_134308": (75.5, 0.67, 1239198206.7),
    "GW190421_213856": (69.7, 0.67, 1240340820.6),
    "GW190503_185404": (68.6, 0.67, 1240944862.3),
    "GW190512_180714": (34.5, 0.67, 1241719652.4),
    "GW190513_205428": (51.6, 0.67, 1241816086.8),
    "GW190514_065416": (64.5, 0.67, 1241852074.8),
    "GW190517_055101": (59.3, 0.67, 1242107479.8),
    "GW190519_153544": (101.0, 0.67, 1242315362.4),
    "GW190521_074359": (71.0, 0.67, 1242459857.5),
    "GW190527_092055": (56.4, 0.67, 1242984073.8),
    "GW190602_175927": (110.9, 0.67, 1243533585.1),
    "GW190701_203306": (90.2, 0.67, 1246048404.6),
    "GW190706_222641": (99.0, 0.67, 1246487219.3),
    "GW190707_093326": (19.2, 0.67, 1246527224.2),
    "GW190719_215514": (54.9, 0.67, 1247608532.9),
    "GW190720_000836": (18.6, 0.67, 1247616534.7),
    "GW190727_060333": (71.7, 0.67, 1248242631.9),
    "GW190728_064510": (18.1, 0.67, 1248331528.5),
    "GW190731_140936": (55.3, 0.67, 1248530994.7),
    "GW190803_022701": (62.8, 0.67, 1248834439.9),
    "GW190805_211137": (52.2, 0.67, 1249073515.4),
    "GW190828_063405": (39.5, 0.67, 1251009263.8),
    "GW190828_065509": (29.5, 0.67, 1251010527.8),
    "GW190915_235702": (56.3, 0.67, 1252627040.7),
    "GW190924_021846": (13.7, 0.67, 1253326744.8),
    "GW190929_012149": (89.3, 0.67, 1253669327.5),
    "GW190930_133541": (18.6, 0.67, 1253885759.3),
    "GW191109_010717": (103.2, 0.67, 1257296855.2),
    "GW191127_050227": (38.2, 0.67, 1258862565.3),
    "GW191204_110529": (29.2, 0.67, 1259492747.4),
    "GW191215_223052": (42.3, 0.67, 1260484270.3),
    "GW191222_033537": (76.2, 0.67, 1261020955.1),
    "GW191230_180458": (56.3, 0.67, 1261680316.4),
    "GW200128_022011": (64.9, 0.67, 1264213229.9),
    "GW200129_065458": (55.7, 0.67, 1264316116.4),
    "GW200202_154313": (16.9, 0.67, 1264694611.6),
    "GW200208_130117": (54.7, 0.67, 1265201695.0),
    "GW200209_085452": (44.5, 0.67, 1265273710.6),
    "GW200216_220804": (89.1, 0.67, 1265930902.2),
    "GW200219_094415": (56.2, 0.67, 1266138273.5),
    "GW200220_061928": (122.7, 0.67, 1266213586.1),
    "GW200224_222234": (57.7, 0.67, 1266618172.4),
    "GW200225_060421": (27.5, 0.67, 1266645879.3),
    "GW200308_173609": (42.7, 0.67, 1267725387.3),
    "GW200311_115853": (55.4, 0.67, 1267968951.3),
    "GW200316_215756": (21.2, 0.67, 1268437094.4),
}


# ---------------------------------------------------------------------------
# Single-event analysis
# ---------------------------------------------------------------------------

def analyze_event(event_name: str, M_rem: float, a_spin: float,
                  gps_merger: float, data_dir: str = "data") -> dict:
    """Full ringdown deviation analysis for one event.

    Returns dict with:
      - GR predictions (f_gr, tau_gr)
      - Measured values (f_fit, tau_fit) with uncertainties
      - Fractional deviations (delta_f/f, delta_tau/tau)
      - Post-merger excess power
      - Per-detector results
    """
    # GR predictions
    f_gr = qnm_freq_gr(M_rem, a_spin)
    tau_gr = qnm_tau_gr(M_rem, a_spin)
    Q_gr = qnm_quality_gr(a_spin)

    result = {
        'event': event_name,
        'M_remnant': M_rem,
        'a_spin': a_spin,
        'f_gr': f_gr,
        'tau_gr': tau_gr,
        'Q_gr': Q_gr,
    }

    det_results = {}
    for det in ['H1', 'L1']:
        fpath = os.path.join(data_dir, f"{det}_{event_name}.hdf5")
        if not os.path.exists(fpath):
            continue
        if os.path.getsize(fpath) < 100000:
            continue

        try:
            with h5py.File(fpath, 'r') as f:
                strain = f['strain/Strain'][:]
                gps_start = f['meta/GPSstart'][()]
                duration = f['meta/Duration'][()]
                sr = len(strain) / duration

            # Find merger
            # PSD from pre-merger data
            expected_merger_idx = int((gps_merger - gps_start) * sr)
            if expected_merger_idx < int(2 * sr) or expected_merger_idx >= len(strain) - int(2 * sr):
                det_results[det] = {'error': 'merger outside data range'}
                continue

            psd_end = expected_merger_idx - int(1.0 * sr)
            psd_start = max(0, psd_end - int(10.0 * sr))
            if psd_end - psd_start < int(1.0 * sr):
                psd_start = 0
                psd_end = expected_merger_idx - int(0.5 * sr)

            psd_f, psd_v = estimate_psd(strain[psd_start:psd_end], sr)

            # Whiten with band centered on expected ringdown frequency
            # Use +/- factor of ~2 around f_gr to capture the QNM
            bp_low = max(20.0, f_gr * 0.4)
            bp_high = min(f_gr * 2.5, sr / 2 - 10)
            whitened = bandpass_whiten(strain, sr, psd_f, psd_v,
                                      f_low=bp_low, f_high=bp_high)

            # Find peak near merger
            merger_idx = find_merger_peak(whitened, sr, gps_merger, gps_start)

            # Extract ringdown segment: merger to merger + 200ms
            ringdown_len = int(0.200 * sr)
            end_idx = min(merger_idx + ringdown_len, len(whitened))
            ringdown_segment = whitened[merger_idx:end_idx]

            if len(ringdown_segment) < int(0.020 * sr):
                det_results[det] = {'error': 'ringdown segment too short'}
                continue

            # --- Ringdown SNR estimate ---
            # Compare ringdown power to noise
            noise_end = merger_idx - int(0.5 * sr)
            noise_start = max(0, noise_end - int(1.0 * sr))
            if noise_start < noise_end:
                noise_rms = np.sqrt(np.mean(whitened[noise_start:noise_end]**2))
            else:
                noise_rms = 1.0

            # Ringdown SNR: peak amplitude / noise RMS
            peak_amp = np.max(np.abs(ringdown_segment[:int(0.020 * sr)]))
            ringdown_snr = peak_amp / noise_rms if noise_rms > 0 else 0.0

            # --- Fit the ringdown ---
            # Use 5ms offset to avoid inspiral contamination.
            # The l=2,m=2 QNM is established by ~10M after merger;
            # for a 60 Msun remnant, 10M ~ 3ms, so 5ms is conservative.
            t_offset = max(0.005, 10.0 * G_SI * M_rem * M_SUN / C**3)
            fit = fit_ringdown(ringdown_segment, sr,
                               f_guess=f_gr, tau_guess=tau_gr,
                               t_start_offset=t_offset)

            if not fit['success']:
                det_results[det] = {
                    'error': f"fit failed: {fit.get('reason', 'unknown')}",
                    'ringdown_snr': ringdown_snr,
                }
                continue

            # --- Compute deviations from GR ---
            delta_f = fit['f'] - f_gr
            delta_tau = fit['tau'] - tau_gr
            frac_delta_f = delta_f / f_gr if f_gr > 0 else 0.0
            frac_delta_tau = delta_tau / tau_gr if tau_gr > 0 else 0.0

            # Uncertainty on fractional deviation
            sigma_frac_f = fit['sigma_f'] / f_gr if f_gr > 0 else 1.0
            sigma_frac_tau = fit['sigma_tau'] / tau_gr if tau_gr > 0 else 1.0

            # --- Post-merger excess power ---
            excess = post_merger_excess(whitened, sr, merger_idx, fit['tau'],
                                        psd_f, psd_v)

            det_results[det] = {
                'ringdown_snr': ringdown_snr,
                'f_fit': fit['f'],
                'tau_fit': fit['tau'],
                'sigma_f': fit['sigma_f'],
                'sigma_tau': fit['sigma_tau'],
                'fit_snr': fit['fit_snr'],
                'frac_delta_f': frac_delta_f,
                'frac_delta_tau': frac_delta_tau,
                'sigma_frac_f': sigma_frac_f,
                'sigma_frac_tau': sigma_frac_tau,
                'excess': excess,
            }

        except Exception as e:
            det_results[det] = {'error': str(e)}

    result['detectors'] = det_results
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    np.random.seed(42)

    print("=" * 90)
    print("RINGDOWN DAMPING DEVIATION TEST")
    print("Toy-physics framework prediction: tau_measured > tau_GR")
    print("=" * 90)
    print()
    print("FRAMEWORK PREDICTION:")
    print("  In GR, QNM damping is set by perfect absorption at the horizon.")
    print("  In S=L(1-f), the f=1 surface is partially reflecting.")
    print("  -> Damping time tau should be LONGER than GR predicts.")
    print("  -> delta_tau/tau should be POSITIVE across events.")
    print("  -> Excess should correlate with remnant compactness (M/R).")
    print()
    print("NULL HYPOTHESIS: delta_tau/tau = 0 (GR is exact)")
    print("ALTERNATIVE:     delta_tau/tau > 0 (framework effect)")
    print()

    # Print GR predictions for reference
    print("-" * 90)
    print("GR QNM PREDICTIONS (l=2, m=2, n=0)")
    print("-" * 90)
    print(f"  {'Event':>20s} {'M_rem':>6s} {'a':>5s} {'f_GR':>8s} {'tau_GR':>10s} {'Q_GR':>6s}")
    print(f"  {'':>20s} {'[Msun]':>6s} {'':>5s} {'[Hz]':>8s} {'[ms]':>10s} {'':>6s}")
    print(f"  {'-'*60}")

    # Sort by remnant mass for readability
    sorted_events = sorted(EVENTS.items(), key=lambda x: x[1][0])

    for name, (M, a, gps) in sorted_events[:10]:  # show first 10
        fg = qnm_freq_gr(M, a)
        tg = qnm_tau_gr(M, a) * 1000  # ms
        Qg = qnm_quality_gr(a)
        print(f"  {name:>20s} {M:>6.1f} {a:>5.2f} {fg:>8.1f} {tg:>10.2f} {Qg:>6.1f}")
    print(f"  ... ({len(EVENTS)} events total)")
    print()

    # ===================================================================
    # Analyze all events
    # ===================================================================

    SNR_THRESHOLD = 4.0  # minimum ringdown SNR for inclusion
    all_results = []
    good_results = []  # events passing SNR cut

    for name, (M, a, gps) in sorted(EVENTS.items()):
        result = analyze_event(name, M, a, gps)
        all_results.append(result)

        # Check if any detector has good ringdown
        has_good = False
        for det, dr in result['detectors'].items():
            if 'error' not in dr and dr.get('ringdown_snr', 0) >= SNR_THRESHOLD:
                has_good = True
                break

        if has_good:
            good_results.append(result)

    print("=" * 90)
    print(f"RESULTS: {len(good_results)} events with ringdown SNR >= {SNR_THRESHOLD}")
    print("=" * 90)
    print()

    # Collect fractional deviations
    all_frac_delta_tau = []
    all_frac_delta_f = []
    all_sigma_frac_tau = []
    all_sigma_frac_f = []
    all_excess_sigmas = []
    all_masses = []
    all_event_names = []
    all_ringdown_snrs = []

    print(f"  {'Event':>20s} {'M':>5s} {'SNR':>5s} | {'f_fit':>7s} {'f_GR':>7s} {'df/f':>7s}"
          f" | {'tau_fit':>8s} {'tau_GR':>8s} {'dtau/tau':>8s} | {'excess':>6s}")
    print(f"  {'':>20s} {'':>5s} {'':>5s} | {'[Hz]':>7s} {'[Hz]':>7s} {'[%]':>7s}"
          f" | {'[ms]':>8s} {'[ms]':>8s} {'[%]':>8s} | {'[sigma]':>6s}")
    print(f"  {'-'*100}")

    for result in good_results:
        name = result['event']
        M = result['M_remnant']

        # Use the detector with higher ringdown SNR
        best_det = None
        best_snr = 0
        for det, dr in result['detectors'].items():
            if 'error' not in dr and dr.get('ringdown_snr', 0) > best_snr:
                best_det = det
                best_snr = dr['ringdown_snr']

        if best_det is None:
            continue

        dr = result['detectors'][best_det]
        if dr.get('ringdown_snr', 0) < SNR_THRESHOLD:
            continue

        f_fit = dr['f_fit']
        tau_fit = dr['tau_fit']
        frac_df = dr['frac_delta_f']
        frac_dtau = dr['frac_delta_tau']
        exc = dr.get('excess', {})
        exc_sigma = exc.get('excess_sigma', 0.0) if exc.get('success', False) else float('nan')

        # Quality cut: fitted frequency must be within 40% of GR prediction.
        # If not, the fit is dominated by noise, not the QNM.
        freq_quality = abs(frac_df) < 0.40
        quality_flag = " " if freq_quality else "*"

        if freq_quality:
            all_frac_delta_tau.append(frac_dtau)
            all_frac_delta_f.append(frac_df)
            all_sigma_frac_tau.append(dr['sigma_frac_tau'])
            all_sigma_frac_f.append(dr['sigma_frac_f'])
            all_masses.append(M)
            all_event_names.append(name)
            all_ringdown_snrs.append(best_snr)
            if np.isfinite(exc_sigma):
                all_excess_sigmas.append(exc_sigma)

        # Always print (mark failed quality cut with *)
        if np.isfinite(exc_sigma):
            print(f"{quality_flag} {name:>20s} {M:>5.1f} {best_snr:>5.1f} | "
                  f"{f_fit:>7.1f} {result['f_gr']:>7.1f} {frac_df*100:>+7.1f} | "
                  f"{tau_fit*1000:>8.2f} {result['tau_gr']*1000:>8.2f} {frac_dtau*100:>+8.1f} | "
                  f"{exc_sigma:>+6.2f}")
        else:
            print(f"{quality_flag} {name:>20s} {M:>5.1f} {best_snr:>5.1f} | "
                  f"{f_fit:>7.1f} {result['f_gr']:>7.1f} {frac_df*100:>+7.1f} | "
                  f"{tau_fit*1000:>8.2f} {result['tau_gr']*1000:>8.2f} {frac_dtau*100:>+8.1f} | "
                  f"{'N/A':>6s}")

    print()
    print("  (* = failed frequency quality cut, excluded from statistics)")

    # ===================================================================
    # Statistical analysis
    # ===================================================================

    print()
    print("=" * 90)
    print("STATISTICAL ANALYSIS")
    print("=" * 90)

    if len(all_frac_delta_tau) < 3:
        print(f"\n  Only {len(all_frac_delta_tau)} events — insufficient for statistics.")
        print(f"  Total events attempted: {len(all_results)}")
        print(f"  Events with data: {sum(1 for r in all_results if r['detectors'])}")
        print(f"  Events with good ringdown: {len(good_results)}")
        dt = time.time() - t0
        print(f"\nRuntime: {dt:.0f}s ({dt/60:.1f} min)")
        return

    N = len(all_frac_delta_tau)
    dtau_arr = np.array(all_frac_delta_tau)
    df_arr = np.array(all_frac_delta_f)
    sigma_tau_arr = np.array(all_sigma_frac_tau)
    sigma_f_arr = np.array(all_sigma_frac_f)
    masses = np.array(all_masses)
    snrs = np.array(all_ringdown_snrs)

    # --- 1. Simple statistics ---
    print(f"\n  1. DAMPING TIME DEVIATION (delta_tau / tau_GR)")
    print(f"     N events: {N}")
    print(f"     Mean: {np.mean(dtau_arr)*100:+.2f}%")
    print(f"     Median: {np.median(dtau_arr)*100:+.2f}%")
    print(f"     Std: {np.std(dtau_arr)*100:.2f}%")
    print(f"     Std of mean: {np.std(dtau_arr)/np.sqrt(N)*100:.2f}%")

    # One-sample t-test: is the mean significantly positive?
    mean_dtau = np.mean(dtau_arr)
    sem_dtau = np.std(dtau_arr, ddof=1) / np.sqrt(N)
    t_stat = mean_dtau / sem_dtau if sem_dtau > 0 else 0
    # Approximate p-value using normal distribution for large N
    from scipy.stats import t as t_dist
    p_value_onesided = 1.0 - t_dist.cdf(t_stat, df=N - 1)

    print(f"     t-statistic: {t_stat:.3f}")
    print(f"     p-value (one-sided, H1: mean > 0): {p_value_onesided:.4f}")
    sigma_equiv = abs(t_stat)  # rough sigma equivalent
    sign = "POSITIVE (framework direction)" if mean_dtau > 0 else "NEGATIVE (opposite to framework)"
    print(f"     Direction: {sign}")
    print(f"     Equivalent significance: {sigma_equiv:.2f} sigma")

    # --- 2. Weighted mean (weight by 1/sigma^2) ---
    print(f"\n  2. INVERSE-VARIANCE WEIGHTED MEAN")
    weights = 1.0 / np.maximum(sigma_tau_arr**2, 1e-10)
    weighted_mean = np.sum(weights * dtau_arr) / np.sum(weights)
    weighted_err = 1.0 / np.sqrt(np.sum(weights))
    w_sigma = weighted_mean / weighted_err if weighted_err > 0 else 0

    print(f"     Weighted mean: {weighted_mean*100:+.3f}% +/- {weighted_err*100:.3f}%")
    print(f"     Significance: {w_sigma:.2f} sigma")

    # --- 3. Sign test ---
    print(f"\n  3. SIGN TEST (non-parametric)")
    n_positive = np.sum(dtau_arr > 0)
    n_negative = np.sum(dtau_arr < 0)
    n_zero = np.sum(dtau_arr == 0)
    # Binomial p-value
    from scipy.stats import binom
    p_sign = binom.sf(n_positive - 1, N, 0.5)  # P(X >= n_positive)
    print(f"     Positive: {n_positive}/{N}")
    print(f"     Negative: {n_negative}/{N}")
    print(f"     Binomial p-value (one-sided): {p_sign:.4f}")

    # --- 4. Frequency deviation ---
    print(f"\n  4. FREQUENCY DEVIATION (delta_f / f_GR)")
    print(f"     Mean: {np.mean(df_arr)*100:+.2f}%")
    print(f"     Median: {np.median(df_arr)*100:+.2f}%")
    print(f"     Std: {np.std(df_arr)*100:.2f}%")
    mean_df = np.mean(df_arr)
    sem_df = np.std(df_arr, ddof=1) / np.sqrt(N)
    t_stat_f = mean_df / sem_df if sem_df > 0 else 0
    p_value_f = 2.0 * (1.0 - t_dist.cdf(abs(t_stat_f), df=N - 1))
    print(f"     t-statistic: {t_stat_f:.3f} (two-sided p = {p_value_f:.4f})")

    # --- 5. Correlation with compactness ---
    print(f"\n  5. COMPACTNESS CORRELATION")
    print(f"     (Framework predicts larger delta_tau for more compact remnants)")

    # Compactness proxy: M_remnant (higher mass = more compact for fixed spin)
    if N >= 5:
        from scipy.stats import pearsonr, spearmanr
        r_pearson, p_pearson = pearsonr(masses, dtau_arr)
        r_spearman, p_spearman = spearmanr(masses, dtau_arr)
        print(f"     Pearson r(M, delta_tau): {r_pearson:+.3f} (p={p_pearson:.4f})")
        print(f"     Spearman rho(M, delta_tau): {r_spearman:+.3f} (p={p_spearman:.4f})")
        if r_pearson > 0 and p_pearson < 0.05:
            print(f"     -> CONSISTENT with framework (more compact = more deviation)")
        elif r_pearson < 0 and p_pearson < 0.05:
            print(f"     -> INCONSISTENT with framework")
        else:
            print(f"     -> No significant correlation detected")
    else:
        print(f"     Too few events for correlation ({N})")

    # --- 6. SNR-dependent check ---
    print(f"\n  6. SNR-DEPENDENT CHECK")
    print(f"     (Real signal should be SNR-independent; systematics may correlate)")
    if N >= 5:
        r_snr, p_snr = pearsonr(snrs, dtau_arr)
        print(f"     Pearson r(SNR, delta_tau): {r_snr:+.3f} (p={p_snr:.4f})")
        if abs(r_snr) > 0.5 and p_snr < 0.05:
            print(f"     WARNING: Significant SNR correlation — possible systematic")
        else:
            print(f"     No significant SNR dependence (good)")

    # --- 7. Post-merger excess power ---
    print(f"\n  7. POST-MERGER EXCESS POWER")
    print(f"     (Framework predicts broadband power from f>1 mode conversion)")
    if all_excess_sigmas:
        exc_arr = np.array(all_excess_sigmas)
        n_exc = len(exc_arr)
        print(f"     N events: {n_exc}")
        print(f"     Mean excess: {np.mean(exc_arr):+.2f} sigma")
        print(f"     Median excess: {np.median(exc_arr):+.2f} sigma")
        n_exc_pos = np.sum(exc_arr > 0)
        print(f"     Positive: {n_exc_pos}/{n_exc}")
        if n_exc >= 3:
            exc_t = np.mean(exc_arr) / (np.std(exc_arr, ddof=1) / np.sqrt(n_exc))
            p_exc = 1.0 - t_dist.cdf(exc_t, df=n_exc - 1)
            print(f"     t-statistic: {exc_t:.3f} (one-sided p = {p_exc:.4f})")
    else:
        print(f"     No excess power measurements available")

    # ===================================================================
    # Verdict
    # ===================================================================
    print()
    print("=" * 90)
    print("VERDICT")
    print("=" * 90)
    print()

    # Primary test: is mean delta_tau/tau positive?
    if p_value_onesided < 0.003:  # ~3 sigma
        verdict = "SIGNIFICANT POSITIVE DEVIATION"
        level = "STRONG"
    elif p_value_onesided < 0.023:  # ~2 sigma
        verdict = "MARGINAL POSITIVE DEVIATION"
        level = "MODERATE"
    elif p_value_onesided < 0.16:  # ~1 sigma
        verdict = "WEAK HINT OF POSITIVE DEVIATION"
        level = "WEAK"
    elif p_value_onesided > 0.84:  # negative direction
        verdict = "DEVIATION IN WRONG DIRECTION (tau shorter than GR)"
        level = "DISFAVORED"
    else:
        verdict = "NULL RESULT — CONSISTENT WITH GR"
        level = "NULL"

    print(f"  PRIMARY TEST (delta_tau/tau > 0):")
    print(f"    Unweighted mean:    {mean_dtau*100:+.2f}%  ({sigma_equiv:.1f} sigma, p = {p_value_onesided:.4f})")
    print(f"    Weighted mean:      {weighted_mean*100:+.3f}%  ({w_sigma:.1f} sigma)")
    print(f"    Sign test:          {n_positive}/{N} positive (p = {p_sign:.4f})")
    print(f"    Verdict: {verdict}")
    print()
    print(f"  NOTE: The inverse-variance weighted mean ({weighted_mean*100:+.2f}%) is the")
    print(f"  most reliable statistic, as it downweights noisy measurements.")
    print(f"  The unweighted mean can be dominated by low-SNR outliers.")
    print()

    if level in ("STRONG", "MODERATE"):
        print(f"  The data show a {mean_dtau*100:+.1f}% excess in ringdown damping time")
        print(f"  relative to GR predictions. This is CONSISTENT with the framework")
        print(f"  prediction that the f=1 surface is partially reflecting, reducing")
        print(f"  the effective absorption rate.")
    elif level == "WEAK":
        print(f"  A weak ({mean_dtau*100:+.1f}%) positive deviation in damping time is")
        print(f"  present but not statistically significant. More events or higher")
        print(f"  SNR needed to distinguish from noise.")
    elif level == "NULL":
        print(f"  The measured damping times are consistent with GR predictions.")
        print(f"  This does not rule out the framework but constrains the reflectivity")
        print(f"  of the f=1 surface to be small.")
    elif level == "DISFAVORED":
        print(f"  The measured damping times are SHORTER than GR, opposite to the")
        print(f"  framework prediction. This disfavors a strongly reflecting f=1 surface.")

    print()
    print(f"  CAVEATS:")
    print(f"    - Spin estimates use a_spin=0.67 default for most O3 events")
    print(f"    - Ringdown start time (3ms post-merger) is somewhat arbitrary")
    print(f"    - Whitening and bandpass choices affect the fit")
    print(f"    - Remnant masses are approximate PE medians")
    print(f"    - Proper Bayesian PE would give tighter constraints")

    # ===================================================================
    # Summary table for all events
    # ===================================================================
    print()
    print("=" * 90)
    print("FULL EVENT SUMMARY")
    print("=" * 90)
    print()
    print(f"  Events in catalog: {len(EVENTS)}")
    print(f"  Events with data: {sum(1 for r in all_results if r['detectors'])}")
    print(f"  Events with ringdown SNR >= {SNR_THRESHOLD}: {N}")
    print(f"  Events with fit success: {len(all_frac_delta_tau)}")
    print()

    if len(all_frac_delta_tau) > 0:
        print(f"  STACKED RESULTS:")
        print(f"    delta_tau/tau:  {mean_dtau*100:+.2f}% +/- {sem_dtau*100:.2f}%")
        print(f"    delta_f/f:     {mean_df*100:+.2f}% +/- {sem_df*100:.2f}%")
        print(f"    Weighted dtau: {weighted_mean*100:+.3f}% +/- {weighted_err*100:.3f}%")

    dt = time.time() - t0
    print(f"\nRuntime: {dt:.0f}s ({dt/60:.1f} min)")


if __name__ == "__main__":
    main()
