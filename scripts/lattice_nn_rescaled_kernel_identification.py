#!/usr/bin/env python3
"""NN lattice rescaled-lane kernel identification (Target A.2).

Closes the gravity / scattering subblock side of the bridge plan's
Target A.2: identify the continuum operator T_∞ on observables that are
NOT the slit-detector decoherence vector.

The cleanest probe is the single-source detector amplitude pattern
A(y_d) for a single point source at the origin (no slits, no field, no
blocked nodes), measured on the deterministic-rescale lane at refinement
values h ∈ {0.5, 0.25, 0.125, 0.0625}.

Each h is fit against a small basis of magnitude / phase candidates:

    Magnitude:    Gaussian, constant, power-law
    Phase:        quadratic, linear, constant

If the magnitude is Gaussian-stable (consistent with PR #968's σ_arm
scaling) AND the phase is quadratic-stable, T_∞'s scattering kernel
matches the Schrödinger free-particle propagator

    K(y; L) = sqrt(m_eff / (2πi·L)) · exp(i·m_eff·y² / (2·L))

The effective mass m_eff is extracted two ways:

    (i)  from the quadratic phase coefficient c2 = m_eff / (2·L)
    (ii) from the Gaussian width σ via Schrödinger free-particle
         spreading σ²(L) ≈ (L/m_eff)²  (point-source σ_0 → 0)

If the two extractions agree to ≤ 5%, the identification is positive.
Otherwise the runner reports a sharp bounded null-result that
constrains the candidate space.

Guards:
- Born-clean: total amplitude squared positive, no overflow
- k=0 control: when source field is identically zero, gravity = 0
- Fit convergence: R² ≥ 0.95 for the chosen candidate
- Cross-validation: two m_eff extractions agree to ≤ 5% if claiming
  positive Schrödinger identification

Exit nonzero only on hard runner failures (NaN amplitudes, build
errors). Null-result is a valid scientific outcome and exits zero.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K_PHYS = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
FANOUT = 3.0

H_VALUES = [0.5, 0.25, 0.125, 0.0625]


# ---------------------------------------------------------------------------
# Lattice + propagator (mirror of the rescaled-continuum runner, single
# point source at origin, no slits, no field, no blocked nodes)
# ---------------------------------------------------------------------------

def lattice(spacing: float):
    nl = int(PHYS_L / spacing) + 1
    hw = int(PHYS_W / spacing)
    pos: List[Tuple[float, float]] = []
    adj: Dict[int, List[int]] = defaultdict(list)
    nmap: Dict[Tuple[int, int], int] = {}
    for layer in range(nl):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            pos.append((x, iy * spacing))
            nmap[(layer, iy)] = len(pos) - 1
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for diy in (-1, 0, 1):
                iyn = iy + diy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def propagate_field_free(pos, adj, n, spacing, source_idx, k_phys=K_PHYS):
    """Single-source field-free propagation on the rescaled lane."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[source_idx] = 1.0
    step_scale = spacing / math.sqrt(FANOUT)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx = x2 - x1
            dy = y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += (amps[i]
                        * cmath.exp(1j * k_phys * L)
                        * w / L * step_scale)
    return amps


def measure_amplitude_pattern(spacing: float, k_phys=K_PHYS) -> Optional[Dict]:
    """Return per-detector-y amplitude A(y_d) for a single source at origin."""
    pos, adj, nl, hw, nmap = lattice(spacing)
    n = len(pos)
    det_layer = nl - 1
    det_idx = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1)]
    src = next(i for i, (x, y) in enumerate(pos)
               if abs(x) < 1e-10 and abs(y) < 1e-10)

    amps = propagate_field_free(pos, adj, n, spacing, src, k_phys=k_phys)

    y_d = [pos[d][1] for d in det_idx]
    A = [amps[d] for d in det_idx]
    mag = [abs(a) for a in A]
    phs = [cmath.phase(a) if abs(a) > 0 else 0.0 for a in A]
    p_total = sum(m * m for m in mag)
    nan_or_inf = any(math.isnan(m) or math.isinf(m) for m in mag)

    return {
        "h": spacing,
        "n": n,
        "y_d": y_d,
        "A_re": [a.real for a in A],
        "A_im": [a.imag for a in A],
        "mag": mag,
        "phase_raw": phs,
        "p_total": p_total,
        "nan_or_inf": nan_or_inf,
    }


# ---------------------------------------------------------------------------
# Phase unwrapping + fitting helpers
# ---------------------------------------------------------------------------

def unwrap_phase(phases: List[float]) -> List[float]:
    out = list(phases)
    for i in range(1, len(out)):
        d = out[i] - out[i - 1]
        while d > math.pi:
            out[i] -= 2 * math.pi
            d -= 2 * math.pi
        while d < -math.pi:
            out[i] += 2 * math.pi
            d += 2 * math.pi
    return out


def _r2(y_obs, y_pred) -> float:
    n = len(y_obs)
    if n == 0:
        return float("nan")
    mean_y = sum(y_obs) / n
    ss_tot = sum((y - mean_y) ** 2 for y in y_obs)
    ss_res = sum((yo - yp) ** 2 for yo, yp in zip(y_obs, y_pred))
    if ss_tot <= 0:
        return float("nan")
    return 1.0 - ss_res / ss_tot


def fit_polynomial(xs: List[float], ys: List[float],
                   degree: int) -> Tuple[List[float], float]:
    """Least-squares polynomial fit y = sum c_k x^k. Returns (coeffs, R^2).

    Uses normal equations on the Vandermonde matrix (degree small here).
    """
    m = degree + 1
    n = len(xs)
    if n < m:
        return [float("nan")] * m, float("nan")
    # Normal equations: A^T A c = A^T y
    AtA = [[0.0] * m for _ in range(m)]
    Aty = [0.0] * m
    for x, y in zip(xs, ys):
        powers = [1.0]
        for _ in range(2 * m - 2):
            powers.append(powers[-1] * x)
        for i in range(m):
            for j in range(m):
                AtA[i][j] += powers[i + j]
            Aty[i] += powers[i] * y
    # Solve via Gauss-Jordan elimination
    M = [row[:] + [Aty[i]] for i, row in enumerate(AtA)]
    for k in range(m):
        # pivot
        pivot_row = k
        max_abs = abs(M[k][k])
        for r in range(k + 1, m):
            if abs(M[r][k]) > max_abs:
                pivot_row = r
                max_abs = abs(M[r][k])
        if max_abs < 1e-15:
            return [float("nan")] * m, float("nan")
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]
        # normalize
        pivot = M[k][k]
        for c in range(k, m + 1):
            M[k][c] /= pivot
        # eliminate
        for r in range(m):
            if r != k and abs(M[r][k]) > 1e-30:
                factor = M[r][k]
                for c in range(k, m + 1):
                    M[r][c] -= factor * M[k][c]
    coeffs = [M[i][m] for i in range(m)]
    y_pred = []
    for x in xs:
        v = 0.0
        xp = 1.0
        for c in coeffs:
            v += c * xp
            xp *= x
        y_pred.append(v)
    return coeffs, _r2(ys, y_pred)


def fit_gaussian_magnitude(xs: List[float],
                           ys: List[float]) -> Tuple[Dict, float]:
    """Fit |A(y)| = c0 * exp(-(y - mu)^2 / (2 sigma^2)).

    Take log y = log c0 - (y - mu)^2 / (2 sigma^2); fit a quadratic in y.
    Returns ({c0, mu, sigma}, R^2_in_log_space) where R^2 is reported on
    log magnitudes (the linearization domain).
    """
    pts = [(x, y) for x, y in zip(xs, ys) if y > 0]
    if len(pts) < 3:
        return {"c0": float("nan"), "mu": float("nan"),
                "sigma": float("nan")}, float("nan")
    xs2 = [p[0] for p in pts]
    log_y = [math.log(p[1]) for p in pts]
    coeffs, r2 = fit_polynomial(xs2, log_y, 2)
    a0, a1, a2 = coeffs
    if math.isnan(a2) or a2 >= 0:
        return {"c0": float("nan"), "mu": float("nan"),
                "sigma": float("nan")}, r2
    sigma = math.sqrt(-1.0 / (2.0 * a2))
    mu = a1 * sigma * sigma
    log_c0 = a0 + (mu * mu) / (2.0 * sigma * sigma)
    c0 = math.exp(log_c0)
    # Re-evaluate R^2 in linear-magnitude space
    y_pred = [c0 * math.exp(-(x - mu) ** 2 / (2 * sigma * sigma))
              for x in xs2]
    r2_lin = _r2([p[1] for p in pts], y_pred)
    return {"c0": c0, "mu": mu, "sigma": sigma}, r2_lin


def fit_constant_magnitude(ys: List[float]) -> Tuple[float, float]:
    """Fit |A(y)| = c0 (constant). Returns (c0, R^2)."""
    n = len(ys)
    if n == 0:
        return float("nan"), float("nan")
    c0 = sum(ys) / n
    r2 = _r2(ys, [c0] * n)
    return c0, r2


def fit_powerlaw_magnitude(xs: List[float],
                           ys: List[float]) -> Tuple[Dict, float]:
    """Fit |A(y)| = c0 * |y|^(-alpha). y=0 excluded."""
    pts = [(x, y) for x, y in zip(xs, ys) if y > 0 and abs(x) > 1e-12]
    if len(pts) < 3:
        return {"c0": float("nan"), "alpha": float("nan")}, float("nan")
    log_x = [math.log(abs(p[0])) for p in pts]
    log_y = [math.log(p[1]) for p in pts]
    coeffs, _ = fit_polynomial(log_x, log_y, 1)
    log_c0, m = coeffs
    if math.isnan(m):
        return {"c0": float("nan"), "alpha": float("nan")}, float("nan")
    alpha = -m
    c0 = math.exp(log_c0)
    y_pred = [c0 * (abs(p[0]) ** (-alpha)) for p in pts]
    r2_lin = _r2([p[1] for p in pts], y_pred)
    return {"c0": c0, "alpha": alpha}, r2_lin


# ---------------------------------------------------------------------------
# Per-h candidate fits and reporting
# ---------------------------------------------------------------------------

def fit_at_h(rec: Dict, central_window: float = 6.0) -> Dict:
    """Fit magnitude + phase candidates on the central window around y=0.

    The angular weight exp(-BETA*theta^2) suppresses |y| > about 6
    significantly; restricting the fit to |y| ≤ central_window improves
    sensitivity to the central kernel structure (where the Schrödinger
    propagator's quadratic phase is the cleanest signature).
    """
    mask = [abs(y) <= central_window + 1e-9 for y in rec["y_d"]]
    y_w = [y for y, m in zip(rec["y_d"], mask) if m]
    mag_w = [m for m, k in zip(rec["mag"], mask) if k]
    phs_w_raw = [p for p, k in zip(rec["phase_raw"], mask) if k]

    # Sort by y (ascending) for clean unwrapping
    idx = sorted(range(len(y_w)), key=lambda i: y_w[i])
    y_w = [y_w[i] for i in idx]
    mag_w = [mag_w[i] for i in idx]
    phs_w_raw = [phs_w_raw[i] for i in idx]
    phs_w = unwrap_phase(phs_w_raw)

    out: Dict = {"h": rec["h"], "y_w": y_w, "mag_w": mag_w, "phs_w": phs_w}

    # Magnitude candidates
    g_par, g_r2 = fit_gaussian_magnitude(y_w, mag_w)
    c_c0, c_r2 = fit_constant_magnitude(mag_w)
    p_par, p_r2 = fit_powerlaw_magnitude(y_w, mag_w)
    out["mag_gaussian"] = {**g_par, "r2": g_r2}
    out["mag_constant"] = {"c0": c_c0, "r2": c_r2}
    out["mag_powerlaw"] = {**p_par, "r2": p_r2}

    # Phase candidates
    q_coeffs, q_r2 = fit_polynomial(y_w, phs_w, 2)
    l_coeffs, l_r2 = fit_polynomial(y_w, phs_w, 1)
    k_c0 = sum(phs_w) / max(1, len(phs_w))
    k_r2 = _r2(phs_w, [k_c0] * len(phs_w))
    out["phase_quadratic"] = {
        "c0": q_coeffs[0], "c1": q_coeffs[1], "c2": q_coeffs[2],
        "r2": q_r2,
    }
    out["phase_linear"] = {
        "c0": l_coeffs[0], "c1": l_coeffs[1], "r2": l_r2,
    }
    out["phase_constant"] = {"c0": k_c0, "r2": k_r2}

    return out


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def _print_record_table(rec: Dict) -> None:
    print(f"  detector y_d  |A(y_d)|  arg(A) (raw radians)")
    print("  " + "-" * 56)
    # show full detector layer for transparency
    n = len(rec["y_d"])
    show_idx = list(range(n))
    if n > 25:
        # subsample around center
        center = n // 2
        radius = 12
        show_idx = list(range(max(0, center - radius),
                              min(n, center + radius + 1)))
    for i in show_idx:
        print(f"  {rec['y_d'][i]:+8.4f}     "
              f"{rec['mag'][i]:.4e}   {rec['phase_raw'][i]:+.4f}")


def _print_fits(fits: Dict) -> None:
    h = fits["h"]
    print(f"  h = {h}: |y| ≤ central_window fits")
    g = fits["mag_gaussian"]
    c = fits["mag_constant"]
    p = fits["mag_powerlaw"]
    print(f"    magnitude:")
    print(f"      gaussian   c0={g['c0']:.4e}  mu={g['mu']:+.4f}  "
          f"sigma={g['sigma']:.4f}  R^2={g['r2']:.4f}")
    print(f"      constant   c0={c['c0']:.4e}  R^2={c['r2']:.4f}")
    print(f"      power-law  c0={p['c0']:.4e}  alpha={p['alpha']:+.4f}  "
          f"R^2={p['r2']:.4f}")
    q = fits["phase_quadratic"]
    li = fits["phase_linear"]
    k = fits["phase_constant"]
    print(f"    phase (unwrapped):")
    print(f"      quadratic  c0={q['c0']:+.4f}  c1={q['c1']:+.4f}  "
          f"c2={q['c2']:+.6f}  R^2={q['r2']:.4f}")
    print(f"      linear     c0={li['c0']:+.4f}  c1={li['c1']:+.4f}  "
          f"R^2={li['r2']:.4f}")
    print(f"      constant   c0={k['c0']:+.4f}  R^2={k['r2']:.4f}")


def _best(name_to_r2: Dict[str, float]) -> Tuple[str, float]:
    items = [(k, v) for k, v in name_to_r2.items()
             if v is not None and not math.isnan(v)]
    if not items:
        return "none", float("nan")
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items[0]


def main() -> int:
    print("=" * 100)
    print("NN LATTICE RESCALED-LANE KERNEL IDENTIFICATION (Target A.2)")
    print(f"  Single source at origin, field-free, no slits, no blocked nodes")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, k={K_PHYS}, BETA={BETA}, "
          f"FANOUT={FANOUT}")
    print("=" * 100)
    print()

    # ---- k=0 control: gravity from a single source must be zero ----
    print("Control 1: k=0 single-source field-free amplitude pattern at h=0.5")
    ctrl = measure_amplitude_pattern(0.5, k_phys=0.0)
    if ctrl is None or ctrl["nan_or_inf"]:
        print("  FAIL: control build returned NaN/None")
        return 2
    print(f"  total |A|^2 = {ctrl['p_total']:.6e}  "
          f"(positive, no overflow): "
          f"{'PASS' if ctrl['p_total'] > 0 and not ctrl['nan_or_inf'] else 'FAIL'}")
    # gravity in the symmetric field-free k=0 setup is the centroid drift
    # vs a perfect mirror. With the source at y=0 and no field, the
    # centroid of |A(y_d)|^2 should be 0 by symmetry.
    centroid_ctrl = (sum(m * m * y for m, y in
                         zip(ctrl["mag"], ctrl["y_d"])) /
                     ctrl["p_total"]) if ctrl["p_total"] > 0 else float("nan")
    print(f"  k=0 centroid drift (should vanish by symmetry) = "
          f"{centroid_ctrl:+.3e}: "
          f"{'PASS' if abs(centroid_ctrl) < 1e-10 else 'FAIL'}")
    print()

    # ---- Primary: K_PHYS = 5.0 sweep ----
    print("Primary sweep: K_PHYS = 5.0 (canonical framework value)")
    print(f"  h ∈ {H_VALUES}")
    print()

    records: List[Dict] = []
    fits_per_h: List[Dict] = []
    born_max_p = 0.0
    for h in H_VALUES:
        t0 = time.time()
        rec = measure_amplitude_pattern(h, k_phys=K_PHYS)
        dt = time.time() - t0
        if rec is None or rec["nan_or_inf"]:
            print(f"  h = {h}: FAIL ({dt:.0f}s)")
            return 2
        records.append(rec)
        born_max_p = max(born_max_p, abs(rec["p_total"]))
        print(f"  h = {h}: nodes = {rec['n']}, "
              f"sum |A|^2 = {rec['p_total']:.4e}, time = {dt:.1f}s")
        _print_record_table(rec)
        print()

    print()
    print("=" * 100)
    print("CANDIDATE FITS (central window |y_d| ≤ 6)")
    print("=" * 100)
    print()
    for rec in records:
        f = fit_at_h(rec)
        fits_per_h.append(f)
        _print_fits(f)
        print()

    # ---- Stability and identification ----
    print("=" * 100)
    print("STABILITY ANALYSIS")
    print("=" * 100)
    print()
    print(f"  {'h':>8s}  {'best_mag':>12s}  {'R^2':>7s}  "
          f"{'best_phase':>12s}  {'R^2':>7s}  "
          f"{'sigma':>9s}  {'c2':>10s}")
    print(f"  {'-' * 80}")
    sigma_per_h: List[Tuple[float, float, float]] = []  # (h, sigma, mag_r2)
    c2_per_h: List[Tuple[float, float, float]] = []     # (h, c2, phase_r2)
    for f in fits_per_h:
        mag_r2 = {
            "gaussian": f["mag_gaussian"]["r2"],
            "constant": f["mag_constant"]["r2"],
            "powerlaw": f["mag_powerlaw"]["r2"],
        }
        phs_r2 = {
            "quadratic": f["phase_quadratic"]["r2"],
            "linear": f["phase_linear"]["r2"],
            "constant": f["phase_constant"]["r2"],
        }
        bm, bm_r2 = _best(mag_r2)
        bp, bp_r2 = _best(phs_r2)
        sigma = f["mag_gaussian"]["sigma"]
        c2 = f["phase_quadratic"]["c2"]
        sigma_per_h.append((f["h"], sigma, f["mag_gaussian"]["r2"]))
        c2_per_h.append((f["h"], c2, f["phase_quadratic"]["r2"]))
        print(f"  {f['h']:8.4f}  {bm:>12s}  {bm_r2:7.4f}  "
              f"{bp:>12s}  {bp_r2:7.4f}  "
              f"{sigma:9.4f}  {c2:+10.6f}")

    print()
    # Best-candidate stability across h
    mag_winners = []
    phs_winners = []
    for f in fits_per_h:
        bm, _ = _best({
            "gaussian": f["mag_gaussian"]["r2"],
            "constant": f["mag_constant"]["r2"],
            "powerlaw": f["mag_powerlaw"]["r2"],
        })
        bp, _ = _best({
            "quadratic": f["phase_quadratic"]["r2"],
            "linear": f["phase_linear"]["r2"],
            "constant": f["phase_constant"]["r2"],
        })
        mag_winners.append(bm)
        phs_winners.append(bp)

    mag_stable = all(w == mag_winners[-1] for w in mag_winners[-3:]) \
        if len(mag_winners) >= 3 else False
    phs_stable = all(w == phs_winners[-1] for w in phs_winners[-3:]) \
        if len(phs_winners) >= 3 else False
    print(f"  Magnitude best-candidate winners across h: {mag_winners}")
    print(f"    fine-h stable (last 3 agree): "
          f"{'YES' if mag_stable else 'NO'}  -> {mag_winners[-1] if mag_winners else 'n/a'}")
    print(f"  Phase best-candidate winners across h:     {phs_winners}")
    print(f"    fine-h stable (last 3 agree): "
          f"{'YES' if phs_stable else 'NO'}  -> {phs_winners[-1] if phs_winners else 'n/a'}")
    print()

    # ---- Schrödinger free-particle identification check ----
    print("=" * 100)
    print("SCHRÖDINGER FREE-PARTICLE IDENTIFICATION CHECK")
    print("=" * 100)
    print()
    fine = [f for f in fits_per_h if f["h"] <= 0.125]
    if not fine:
        print("  Insufficient fine-h points; cannot identify.")
        return 0

    finest = fits_per_h[-1]
    print(f"Using finest h = {finest['h']} for kernel parameter extraction.")
    print()

    sigma_finest = finest["mag_gaussian"]["sigma"]
    c2_finest = finest["phase_quadratic"]["c2"]
    mag_r2_finest = finest["mag_gaussian"]["r2"]
    phs_r2_finest = finest["phase_quadratic"]["r2"]

    print(f"  Gaussian magnitude fit R^2  = {mag_r2_finest:.4f}")
    print(f"  Quadratic phase fit R^2     = {phs_r2_finest:.4f}")
    print(f"  Tolerance threshold = 0.95")
    mag_pass = (not math.isnan(mag_r2_finest)) and mag_r2_finest >= 0.95
    phs_pass = (not math.isnan(phs_r2_finest)) and phs_r2_finest >= 0.95
    print(f"  Gaussian-magnitude PASS:  {mag_pass}")
    print(f"  Quadratic-phase   PASS:  {phs_pass}")
    print()

    # m_eff from quadratic phase: c2 = m_eff / (2 L)
    m_eff_phase = 2.0 * PHYS_L * c2_finest
    # m_eff from Gaussian width: sigma ≈ L / m_eff  (point source)
    m_eff_width = (PHYS_L / sigma_finest) if sigma_finest > 0 else float("nan")
    if m_eff_phase != 0 and not math.isnan(m_eff_phase) \
            and not math.isnan(m_eff_width):
        rel_err = abs(m_eff_phase - m_eff_width) / abs(m_eff_phase)
    else:
        rel_err = float("nan")

    print("Two independent m_eff extractions at finest h:")
    print(f"  (i)  from quadratic phase  c2 = m_eff / (2 L):")
    print(f"       c2 = {c2_finest:+.6e}, L = {PHYS_L}")
    print(f"       m_eff_phase = 2 L * c2 = {m_eff_phase:+.6f}")
    print(f"  (ii) from Gaussian width  sigma ≈ L / m_eff (sigma_0 → 0):")
    print(f"       sigma = {sigma_finest:.6f}, L = {PHYS_L}")
    print(f"       m_eff_width = L / sigma = {m_eff_width:+.6f}")
    print()
    print(f"  Relative disagreement |m_phase - m_width| / |m_phase| = "
          f"{rel_err:.4f}")
    print(f"  Tolerance: ≤ 0.05")
    cross_ok = (not math.isnan(rel_err)) and rel_err <= 0.05
    print(f"  Cross-validation PASS:  {cross_ok}")
    print()

    # ---- Stability check across h: are the parameters converging? ----
    print("Per-h Schrödinger parameters across the sweep:")
    print(f"  {'h':>8s}  {'sigma':>10s}  {'c2':>11s}  "
          f"{'m_eff_phase':>11s}  {'m_eff_width':>11s}")
    print(f"  {'-' * 60}")
    for f in fits_per_h:
        sg = f["mag_gaussian"]["sigma"]
        c2 = f["phase_quadratic"]["c2"]
        m_p = 2.0 * PHYS_L * c2 if not math.isnan(c2) else float("nan")
        m_w = PHYS_L / sg if sg and not math.isnan(sg) and sg > 0 else float("nan")
        print(f"  {f['h']:8.4f}  {sg:10.4f}  {c2:+11.6f}  "
              f"{m_p:+11.4f}  {m_w:+11.4f}")
    print()

    # ---- Verdict ----
    print("=" * 100)
    print("VERDICT")
    print("=" * 100)
    print()
    positive = (mag_pass and phs_pass and cross_ok
                and mag_winners[-1] == "gaussian"
                and phs_winners[-1] == "quadratic")

    if positive:
        print("POSITIVE IDENTIFICATION: T_∞'s scattering kernel matches")
        print("the Schrödinger free-particle propagator.")
        print()
        print(f"  K(y_d - 0; L) = sqrt(m_eff/(2πi·L)) · exp(i·m_eff·y_d² / (2L))")
        print(f"  with m_eff ≈ {m_eff_phase:+.4f} (phase),")
        print(f"             ≈ {m_eff_width:+.4f} (width),")
        print(f"  agreement to {rel_err * 100:.2f}%  (tolerance 5%).")
        print()
        print("  Magnitude is Gaussian-stable; phase is quadratic-stable;")
        print("  two independent m_eff extractions cross-validate.")
        print()
        print(f"  This identifies T_∞'s scattering subblock and closes the")
        print(f"  remaining open arm of Target A.2.")
    else:
        print("BOUNDED NULL-RESULT: T_∞'s scattering kernel does NOT match")
        print("a clean Schrödinger free-particle propagator on the rescaled")
        print("lane through h = 0.0625 with K_PHYS = 5.0.")
        print()
        print("Sharp constraints on the candidate space:")
        if mag_winners[-1] == "gaussian" and mag_pass:
            print("  - magnitude is Gaussian-shaped (consistent with PR #968's")
            print("    σ_arm scaling): T_∞'s kernel has Gaussian-decaying mag.")
        else:
            print(f"  - magnitude is NOT Gaussian (best candidate at finest h "
                  f"= '{mag_winners[-1] if mag_winners else 'n/a'}'): rules")
            print("    out a strict Schrödinger-form magnitude.")
        if phs_winners[-1] == "quadratic" and phs_pass:
            print("  - phase is quadratic in y_d: consistent with the geometric")
            print("    free-particle action term, but the m_eff extracted from")
            print("    phase does not match the m_eff implied by the width:")
        else:
            print(f"  - phase is NOT quadratic (best candidate at finest h "
                  f"= '{phs_winners[-1] if phs_winners else 'n/a'}'): rules")
            print("    out a strict Schrödinger-form quadratic phase.")
        if not math.isnan(rel_err):
            print(f"  - cross-validation: m_eff_phase / m_eff_width disagree "
                  f"by {rel_err * 100:.1f}% (> 5%).")
            print(f"    The two m_eff are not the same physical mass scale.")
        print()
        print(f"  Implication: any continuum candidate for T_∞'s scattering")
        print(f"  kernel must reproduce the observed magnitude/phase shapes")
        print(f"  AND the inconsistency between width-based and phase-based")
        print(f"  effective mass. The free-particle Schrödinger propagator")
        print(f"  fails this requirement on the rescaled NN harness with")
        print(f"  K_PHYS = 5.0. This is a class-A bounded null-result that")
        print(f"  constrains the candidate space but does not identify T_∞.")

    print()

    # ---- Secondary K_PHYS = 0 control (do not ship as primary claim) ----
    print("=" * 100)
    print("Secondary control: K_PHYS = 0 at h = 0.25")
    print("(disentangles framework path-integral phase from geometric phase)")
    print("=" * 100)
    print()
    rec0 = measure_amplitude_pattern(0.25, k_phys=0.0)
    if rec0 is not None and not rec0["nan_or_inf"]:
        f0 = fit_at_h(rec0)
        _print_fits(f0)
        print()
        print(f"  At K_PHYS = 0 the per-edge factor reduces to a real")
        print(f"  exp(-BETA*theta^2)/L weight; quadratic phase from the")
        print(f"  geometric path-length term (k * L) is removed. The")
        print(f"  resulting amplitude pattern is purely real-valued and")
        print(f"  carries the lattice's pure angular-weight diffusion")
        print(f"  signature without the framework's path-integral phase.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
