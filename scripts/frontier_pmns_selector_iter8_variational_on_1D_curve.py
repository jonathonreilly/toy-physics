#!/usr/bin/env python3
"""
PMNS selector iter 8: variational attack on the 1-D curve
{delta * q_+ = 2/3, det(H) = E2 = sqrt(8)/3}.

Context. Iters 5-7 established two retained identities:
  (i)  delta * q_+ = Q = 2/3       (cross-sector I1 Koide value)
  (ii) det(H)      = E2 = sqrt(8)/3 (retained atlas constant)
These reduce the 3D chart (m, delta, q_+) to a 1-D curve in the
chamber. The physical pinned point lies on this curve but is not
pinned by the two identities alone — a third condition is needed.

Iter 7 established that NO third simple-value scalar identity exists
at the closure point. Iter 8 pursues a DIFFERENT class: variational
principles on the 1-D curve.

Attack. Parameterize the curve by m (the spectator direction of the
chart). For each m in a scan range, solve the 2-equation system
  delta * q_+ = 2/3
  det(H)      = E2
for (delta, q_+). Compute candidate retained functionals F(m) along
the curve. Look for F whose extremum (dF/dm = 0) occurs at m = m_*.

Candidate functionals tested:

  F1. Tr(H^2) / Tr(H)^2          (dimensionless spectral ratio)
  F2. lambda_max / |lambda_min|  (eigenvalue-magnitude spread)
  F3. Jarlskog invariant J       (CP-violation natural)
  F4. sin(delta_CP)              (CP phase; tied to J)
  F5. Koide Q on H-spectrum: Q_H = sum(lambda) / sum(sqrt(|lambda|))^2
  F6. |K_12|                     (moving doublet off-diagonal magnitude)
  F7. arg(K_12)                  (moving doublet off-diagonal phase)
  F8. s13^2                      (observational, included as sanity)
  F9. s12^2                      (observational)
  F10. s23^2                     (observational)
  F11. Tr(H^3) / Tr(H^2)^{3/2}   (another dimensionless spectral)
  F12. (lambda_max + lambda_min) / lambda_mid  (eigenvalue anti-Koide)

A functional F is a VIABLE third cut if:
  - dF/dm = 0 at m = m_* (to within the chart precision 1e-4).
  - F has a unique extremum on the curve passing through m_*.
  - F is expressible using only retained framework objects.

Honest outcome reporting. If any F has dF/dm ≈ 0 at m_*, report it
as the candidate third cut and queue iter 9 to verify framework-
native derivation. If none, report the dF/dm of each at m_* (gradient
magnitudes) to inform the direction search.
"""
from __future__ import annotations

import math
import numpy as np
from scipy import optimize

np.set_printoptions(precision=10, suppress=True, linewidth=140)

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return cond


# Retained atlas constants
GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
OMEGA = np.exp(2j * math.pi / 3.0)

U_Z3 = (1.0 / math.sqrt(3.0)) * np.array(
    [[1, 1, 1], [1, OMEGA, OMEGA**2], [1, OMEGA**2, OMEGA]], dtype=complex
)

T_M = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_DELTA = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
H_BASE = np.array(
    [[0, E1, -E1 - 1j * GAMMA], [E1, 0, -E2], [-E1 + 1j * GAMMA, -E2, 0]],
    dtype=complex,
)

M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_PLUS_STAR = 0.715042

Q_KOIDE = 2.0 / 3.0
PMNS_PERMUTATION = (2, 1, 0)


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def pmns_obs(m: float, delta: float, q_plus: float) -> dict:
    H_m = H(m, delta, q_plus)
    w, V = np.linalg.eigh(H_m)
    order = np.argsort(np.real(w))
    w = np.real(w[order])
    V = V[:, order]
    P = V[list(PMNS_PERMUTATION), :]
    s13sq = abs(P[0, 2]) ** 2
    c13sq = max(1.0 - s13sq, 1e-18)
    s12sq = abs(P[0, 1]) ** 2 / c13sq
    s23sq = abs(P[1, 2]) ** 2 / c13sq
    J = float((P[0, 0] * np.conj(P[0, 1]) * np.conj(P[1, 0]) * P[1, 1]).imag)
    s12 = math.sqrt(max(s12sq, 0.0))
    c12 = math.sqrt(max(1.0 - s12sq, 0.0))
    s13 = math.sqrt(max(s13sq, 0.0))
    c13 = math.sqrt(max(c13sq, 0.0))
    s23 = math.sqrt(max(s23sq, 0.0))
    c23 = math.sqrt(max(1.0 - s23sq, 0.0))
    denom = s12 * c12 * s23 * c23 * s13 * c13 * c13
    sin_dcp = J / denom if denom > 1e-18 else 0.0
    sin_dcp = max(-1.0, min(1.0, sin_dcp))
    K = U_Z3.conj().T @ H_m @ U_Z3
    return {
        "w": w, "V": V, "P": P, "s12sq": float(s12sq), "s13sq": float(s13sq),
        "s23sq": float(s23sq), "J": J, "sin_dcp": float(sin_dcp), "K": K,
    }


def solve_curve_point(m_val: float, x0: np.ndarray) -> np.ndarray | None:
    """For given m, solve for (delta, q_+) such that
       delta * q_+ = 2/3
       det(H)     = E2
    Start from warm-start x0 = (delta_0, q_0)."""
    def residuals(x):
        delta, q = x
        if q <= 0 or delta <= 0:
            return [1e6, 1e6]
        H_m = H(m_val, delta, q)
        det_H = np.linalg.det(H_m).real
        return [delta * q - Q_KOIDE, det_H - E2]

    try:
        sol = optimize.fsolve(residuals, x0, xtol=1e-13, full_output=True)
        x_r, info, ier, msg = sol
        res = residuals(x_r)
        if max(abs(r) for r in res) > 1e-8:
            return None
        delta_r, q_r = x_r
        # basin check
        H_r = H(m_val, delta_r, q_r)
        evals_r, _ = np.linalg.eigh(H_r)
        sig_r = (int(np.sum(evals_r > 1e-12)), 0,
                 int(np.sum(evals_r < -1e-12)))
        if sig_r != (1, 0, 2):
            return None
        if q_r < math.sqrt(8.0 / 3.0) - delta_r - 1e-6:
            return None
        return np.array([delta_r, q_r])
    except Exception:
        return None


# ============================================================================
# Part A: build the 1-D curve
# ============================================================================
print("=" * 72)
print("Part A: build the 1-D curve {delta * q_+ = 2/3, det(H) = E2}")
print("=" * 72)

# Start near the closure point from iter 6: (m_c, delta_c, q_c) ≈
# (0.660, 0.936, 0.712). Use delta_c, q_c as warm start.
DELTA_C = 0.935995
Q_C = 0.712255

# Walk m over a range around the closure/pinned region
m_values = np.linspace(M_STAR - 0.15, M_STAR + 0.15, 121)
curve_data = []
warm = np.array([DELTA_C, Q_C])

for m_val in m_values:
    res = solve_curve_point(float(m_val), warm)
    if res is None:
        continue
    delta_t, q_t = res
    warm = res.copy()  # warm-start next step
    obs = pmns_obs(float(m_val), float(delta_t), float(q_t))
    curve_data.append({
        "m":       float(m_val),
        "delta":   float(delta_t),
        "q":       float(q_t),
        "obs":     obs,
    })

print(f"\n  Curve built with {len(curve_data)} points over m ∈ [{m_values[0]:.3f}, {m_values[-1]:.3f}]")

# Find the point closest to the pinned m
closest_idx = min(range(len(curve_data)), key=lambda i: abs(curve_data[i]["m"] - M_STAR))
print(f"\n  Closest curve point to pinned m_*={M_STAR:.6f}:")
print(f"    m     = {curve_data[closest_idx]['m']:.6f}")
print(f"    delta = {curve_data[closest_idx]['delta']:.6f}")
print(f"    q_+   = {curve_data[closest_idx]['q']:.6f}")
print(f"    s12²  = {curve_data[closest_idx]['obs']['s12sq']:.6f}")
print(f"    s13²  = {curve_data[closest_idx]['obs']['s13sq']:.6f}")
print(f"    s23²  = {curve_data[closest_idx]['obs']['s23sq']:.6f}")


# ============================================================================
# Part B: compute candidate functionals F(m) along the curve
# ============================================================================
print("\n" + "=" * 72)
print("Part B: candidate retained functionals F(m) along the curve")
print("=" * 72)


def funcs_at_point(p: dict) -> dict:
    obs = p["obs"]
    w = obs["w"]
    K = obs["K"]
    H_m = H(p["m"], p["delta"], p["q"])
    tr_H = float(np.trace(H_m).real)
    tr_H2 = float(np.trace(H_m @ H_m).real)
    tr_H3 = float(np.trace(H_m @ H_m @ H_m).real)
    lam_max = float(w.max())
    lam_min = float(w.min())
    lam_mid = float(sorted(w)[1])
    sum_l = float(np.sum(w))
    sum_sqrt_abs = float(np.sum(np.sqrt(np.abs(w))))
    return {
        "F1 Tr(H²)/Tr(H)²":          tr_H2 / tr_H**2 if tr_H != 0 else float("nan"),
        "F2 λ_max/|λ_min|":          lam_max / abs(lam_min) if lam_min != 0 else float("nan"),
        "F3 Jarlskog":               obs["J"],
        "F4 sin(δ_CP)":              obs["sin_dcp"],
        "F5 Koide Q on λ":           sum_l / sum_sqrt_abs**2 if sum_sqrt_abs != 0 else float("nan"),
        "F6 |K_12|":                 float(abs(K[1, 2])),
        "F7 arg(K_12)":              float(np.angle(K[1, 2])),
        "F8 s13²":                   obs["s13sq"],
        "F9 s12²":                   obs["s12sq"],
        "F10 s23²":                  obs["s23sq"],
        "F11 Tr(H³)/Tr(H²)^{3/2}":   tr_H3 / tr_H2**1.5 if tr_H2 > 0 else float("nan"),
        "F12 (λ_max + λ_min)/λ_mid": (lam_max + lam_min) / lam_mid if lam_mid != 0 else float("nan"),
        "F13 Re(K_12)":              float(K[1, 2].real),
        "F14 Im(K_12)":              float(K[1, 2].imag),
    }


# Compute all F at all curve points
F_names = list(funcs_at_point(curve_data[0]).keys())
F_series = {name: [] for name in F_names}
m_series = []
for p in curve_data:
    m_series.append(p["m"])
    f_vals = funcs_at_point(p)
    for name, v in f_vals.items():
        F_series[name].append(v)

m_arr = np.array(m_series)

# For each F, compute derivative dF/dm numerically and find its zeros
print(f"\n  For each F(m), find the m where dF/dm = 0 (extremum).\n")
print(f"  {'Functional':35s}  {'F(m_*)':>14s}  {'dF/dm at m_*':>14s}  {'m of extremum':>16s}  {'|Δm|':>10s}")

extremum_results = []
for name in F_names:
    series = np.array(F_series[name])
    # Filter out NaN
    valid_mask = np.isfinite(series)
    m_valid = m_arr[valid_mask]
    F_valid = series[valid_mask]
    if len(m_valid) < 3:
        continue

    # Compute dF/dm numerically
    dF_dm = np.gradient(F_valid, m_valid)

    # Value and derivative at m_*
    idx_star = int(np.argmin(np.abs(m_valid - M_STAR)))
    F_at_star = F_valid[idx_star]
    dF_at_star = dF_dm[idx_star]

    # Find zero-crossings of dF/dm
    m_ext_list = []
    for i in range(len(dF_dm) - 1):
        if dF_dm[i] * dF_dm[i + 1] < 0:
            # linear interp for zero crossing
            t = dF_dm[i] / (dF_dm[i] - dF_dm[i + 1])
            m_ext = m_valid[i] + t * (m_valid[i + 1] - m_valid[i])
            m_ext_list.append(m_ext)

    if m_ext_list:
        # Find the one closest to m_*
        m_ext_best = min(m_ext_list, key=lambda x: abs(x - M_STAR))
        dev_m = abs(m_ext_best - M_STAR)
    else:
        m_ext_best = None
        dev_m = float("inf")

    print(
        f"  {name:35s}  {F_at_star:>14.6f}  {dF_at_star:>14.6f}  "
        f"{m_ext_best if m_ext_best is not None else 'N/A':>16}  {dev_m:>10.6f}"
    )

    extremum_results.append({
        "name":        name,
        "F_at_star":   F_at_star,
        "dF_at_star":  dF_at_star,
        "m_ext":       m_ext_best,
        "dev_m":       dev_m,
    })

# Sort by proximity of extremum to m_*
extremum_results.sort(key=lambda r: r["dev_m"])

# ============================================================================
# Part C: honest summary
# ============================================================================
print("\n" + "=" * 72)
print("Part C: top extremum candidates")
print("=" * 72)

print(f"\n  Top 5 functionals whose curve-extremum is nearest to m_* = {M_STAR}:\n")
print(f"  {'Functional':35s}  {'m of extremum':>16s}  {'|Δm|':>10s}  {'dF/dm at m_*':>14s}")
for r in extremum_results[:5]:
    m_ext_str = f"{r['m_ext']:.6f}" if r["m_ext"] is not None else "N/A"
    print(
        f"  {r['name']:35s}  {m_ext_str:>16s}  {r['dev_m']:>10.6f}  {r['dF_at_star']:>14.6f}"
    )

best = extremum_results[0]

check(
    f"C.1 best candidate ({best['name']}) has extremum within 0.001 of m_*",
    best["dev_m"] < 0.001,
    f"|Δm| = {best['dev_m']:.6f}",
)
check(
    f"C.2 best candidate has |dF/dm| at m_* below 0.01",
    abs(best["dF_at_star"]) < 0.01,
    f"|dF/dm| = {abs(best['dF_at_star']):.6f}",
)


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 8 attack: variational on the 1-D curve {{delta*q+ = 2/3, det(H) = E2}}.

Method:
  Part A: parameterize curve by m, solve for (delta, q_+) at each m.
  Part B: compute ~14 candidate retained functionals F(m) along the
          curve. Find extrema (zeros of dF/dm) and compare to m_*.
  Part C: rank candidates by proximity of extremum to m_*.

Interpretation:
  - If any F has its extremum within 1e-3 of m_*, AND is framework-
    native, it is a candidate third retained cut. Iter 9 verifies its
    framework-native status.
  - If no F has a nearby extremum, this class is ruled out and iter 9
    pivots to A5 (A-BCC axiomatic) or accepts the 2-retained-identity
    structure as the gate closure form.
""")
