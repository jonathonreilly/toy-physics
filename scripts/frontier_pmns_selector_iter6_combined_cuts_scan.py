#!/usr/bin/env python3
"""
PMNS selector iter 6: search for a second codim-1 cut on the hyperbola
delta * q_+ = 2/3.

Context. Iter 5 established the identity delta * q_+ = Q = 2/3 is
observationally admissible at 1-sigma (predicts sin^2 theta_23 = 0.5447
vs PDG central 0.545) but NOT exact at machine precision (0.16% systematic
offset at the PDG-pinned chamber point).

Iter 4 scalar scan also flagged another near-hit at the same 0.001
precision level: sum(lambda) / sum(|lambda|) = 0.1678 vs 1/6 = 0.1667.

Iter 6 tests whether both near-hits can be simultaneously promoted to
retained identities, and if so, whether their conjunction picks out the
exact PMNS pinned point (gate closure via two cuts).

Attack.

  Phase I. Re-pin UNDER the constraint delta * q_+ = 2/3 AND one PMNS
  angle (use sin^2 theta_13 = 0.0218, best-measured). This yields a
  1-parameter family of chamber solutions. Walk along the family and
  record the value of every natural scalar invariant on the curve.

  Phase II. For each scalar invariant, locate any curve-point where
  it equals a retained simple value (< 1e-6). If such a point also
  reproduces the other two PMNS angles to within PDG 3-sigma, that
  scalar is the candidate second cut.

  Phase III. Verify: are there TWO retained simple values on the curve
  that both go through the same curve-point? If so, that point is over-
  determined (two retained conditions + sin^2 theta_13) = robust gate
  closure.

Honest outcome reporting. Report scalars whose retained-simple
level-set crosses the pinned region. If no clean second cut is found,
iter 7 pivots to A8 (A-BCC × I2/P cross-sector pin) or A10 (symplectic).
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
    [[1, 1, 1], [1, OMEGA, OMEGA * OMEGA], [1, OMEGA * OMEGA, OMEGA]],
    dtype=complex,
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
SELECTOR = math.sqrt(6.0) / 3.0
PMNS_PERMUTATION = (2, 1, 0)

TARGET = {
    "s12sq": 0.307,
    "s13sq": 0.0218,
    "s23sq": 0.545,
}
NUFIT_3SIG = {
    "s12sq": (0.275, 0.345),
    "s13sq": (0.02029, 0.02391),
    "s23sq": (0.430, 0.596),
}


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
    K = U_Z3.conj().T @ H_m @ U_Z3
    return {
        "w": w,
        "V": V,
        "P": P,
        "s12sq": float(s12sq),
        "s13sq": float(s13sq),
        "s23sq": float(s23sq),
        "K": K,
    }


# Simple retained values to match against
SIMPLE_VALUES = {
    "0":         0.0,
    "1/6":       1.0 / 6,
    "1/3":       1.0 / 3,
    "1/2":       0.5,
    "2/3":       2.0 / 3,
    "1":         1.0,
    "sqrt(6)/3": SELECTOR,
    "1/sqrt(3)": 1.0 / math.sqrt(3),
    "1/sqrt(6)": 1.0 / math.sqrt(6),
    "2/sqrt(3)": 2.0 / math.sqrt(3),
    "sqrt(8/3)": math.sqrt(8.0 / 3),
    "sqrt(8)/3": math.sqrt(8.0) / 3,
    "2/9":       2.0 / 9,
    "4/9":       4.0 / 9,
    "sqrt(2)":   math.sqrt(2),
    "sqrt(3)":   math.sqrt(3),
    "-1/2":      -0.5,
    "-1/3":      -1.0 / 3,
    "-1":        -1.0,
}


def scalar_invariants(m: float, delta: float, q_plus: float) -> dict:
    obs = pmns_obs(m, delta, q_plus)
    H_m = H(m, delta, q_plus)
    w = obs["w"]
    K = obs["K"]
    tr_H = float(np.trace(H_m).real)
    tr_H2 = float(np.trace(H_m @ H_m).real)
    det_H = float(np.linalg.det(H_m).real)
    sum_lambda = float(np.sum(w))
    sum_abs_lambda = float(np.sum(np.abs(w)))
    return {
        "Tr(H)":               tr_H,
        "Tr(H^2)":             tr_H2,
        "det(H)":              det_H,
        "lambda_max":          float(w.max()),
        "lambda_min":          float(w.min()),
        "sum lambda":          sum_lambda,
        "sum |lambda|":        sum_abs_lambda,
        "sum lambda / sum |lambda|": (
            sum_lambda / sum_abs_lambda if sum_abs_lambda > 0 else 0.0
        ),
        "prod lambda":         float(np.prod(w)),
        "Re(K_12)":            float(K[1, 2].real),
        "Im(K_12)":            float(K[1, 2].imag),
        "|K_12|":              float(abs(K[1, 2])),
        "K_00":                float(K[0, 0].real),
        "K_11":                float(K[1, 1].real),
        "K_22":                float(K[2, 2].real),
        "K_11 - K_22":         float(K[1, 1].real - K[2, 2].real),
        "K_11 + K_22":         float(K[1, 1].real + K[2, 2].real),
        "q+ + delta":          q_plus + delta,
        "q+ - delta":          q_plus - delta,
        "q+ * delta":          q_plus * delta,
        "q+ / delta":          q_plus / delta if delta != 0 else 0,
        "m":                   m,
        "m + delta":           m + delta,
        "m + q+":              m + q_plus,
        "m * delta":           m * delta,
        "m * q+":              m * q_plus,
        "m + delta + q+":      m + delta + q_plus,
        "m^2 + delta^2 + q+^2": m*m + delta*delta + q_plus*q_plus,
        "Tr(H)/sqrt(Tr(H^2))": tr_H / math.sqrt(tr_H2) if tr_H2 > 0 else 0,
        "det(H) / Tr(H)^3":    det_H / tr_H**3 if tr_H != 0 else 0,
        "SELECTOR*m":          SELECTOR * m,
        "SELECTOR*q+":         SELECTOR * q_plus,
        "SELECTOR*delta":      SELECTOR * delta,
    }


# ============================================================================
# Phase I: 1-parameter curve under delta * q_+ = 2/3 AND sin^2 theta_13 = 0.0218
# ============================================================================
print("=" * 72)
print("Phase I: walk the curve under delta*q+ = 2/3 AND s13^2 = 0.0218")
print("=" * 72)


def residuals_curve(x, m_fix):
    """Given fixed m, find (delta, q+) satisfying
         delta * q+ = 2/3
         sin^2 theta_13 = 0.0218."""
    delta, q_plus = x
    obs = pmns_obs(m_fix, delta, q_plus)
    return [
        delta * q_plus - Q_KOIDE,
        obs["s13sq"] - TARGET["s13sq"],
    ]


# Walk m over a small interval around M_STAR
m_range = np.linspace(M_STAR - 0.1, M_STAR + 0.1, 41)
curve_points = []

# Use previous (delta, q+) as warm start
x_prev = np.array([DELTA_STAR, Q_PLUS_STAR])

for m_val in m_range:
    try:
        res = optimize.fsolve(
            residuals_curve, x_prev, args=(m_val,), xtol=1e-13
        )
        delta_t, q_plus_t = res
        check_residual = residuals_curve(res, m_val)
        if max(abs(r) for r in check_residual) < 1e-10:
            curve_points.append((m_val, delta_t, q_plus_t))
            x_prev = np.array(res)
    except Exception:
        continue

print(f"\n  Built curve with {len(curve_points)} points along m ∈ [{M_STAR-0.1:.3f}, {M_STAR+0.1:.3f}]")


# ============================================================================
# Phase II: scan scalar invariants along the curve — find retained-simple hits
# ============================================================================
print("\n" + "=" * 72)
print("Phase II: scalar-invariant scan along the curve")
print("=" * 72)

# For each scalar, compute its value at every curve point; find the m
# where it crosses each retained simple value.
scalar_at_pinned = scalar_invariants(M_STAR, DELTA_STAR, Q_PLUS_STAR)

# Sweep: record each scalar on the curve
scalar_sweep = {name: [] for name in scalar_at_pinned}
for m_val, delta_t, q_t in curve_points:
    scalars_t = scalar_invariants(m_val, delta_t, q_t)
    for name, v in scalars_t.items():
        scalar_sweep[name].append((m_val, v))

# For each scalar, find crossings of each simple retained value
print(f"\n  Scanning {len(scalar_at_pinned)} scalars × {len(SIMPLE_VALUES)} retained values...")
crossings = []
for scalar_name, pts in scalar_sweep.items():
    if not pts:
        continue
    m_arr = np.array([p[0] for p in pts])
    v_arr = np.array([p[1] for p in pts])
    for sv_name, sv in SIMPLE_VALUES.items():
        diff = v_arr - sv
        # Find sign-change intervals
        for i in range(len(diff) - 1):
            if diff[i] * diff[i+1] < 0:
                # Linear interpolation for crossing
                t = diff[i] / (diff[i] - diff[i+1])
                m_cross = m_arr[i] + t * (m_arr[i+1] - m_arr[i])
                # How close is m_cross to M_STAR?
                dev_m = abs(m_cross - M_STAR)
                crossings.append({
                    "scalar":   scalar_name,
                    "target":   sv_name,
                    "sv":       sv,
                    "m_cross":  m_cross,
                    "dev_m":    dev_m,
                })

# Sort by proximity to M_STAR
crossings.sort(key=lambda x: x["dev_m"])

print(f"\n  Top-10 crossings nearest to pinned m_* = {M_STAR}:\n")
print(f"    {'scalar':40s}  {'target':>12s}  {'m_cross':>12s}  {'|Δm|':>10s}")
for c in crossings[:20]:
    print(
        f"    {c['scalar']:40s}  {c['target']:>12s}  "
        f"{c['m_cross']:>12.6f}  {c['dev_m']:>10.6f}"
    )


# ============================================================================
# Phase III: test top candidate pairs — two retained conditions + s13
# ============================================================================
print("\n" + "=" * 72)
print("Phase III: test top candidate pairs as combined closures")
print("=" * 72)


def try_closure(scalar_name, target_name, target_val):
    """Solve (m, delta, q_+) under:
         delta * q_+ = 2/3
         scalar(m, delta, q_+) = target_val
         s13^2 = 0.0218
    Returns (m, delta, q_+, predicted s12^2, s23^2, sin dCP) or None."""
    def residuals(x):
        m, d, q = x
        obs = pmns_obs(m, d, q)
        scalars = scalar_invariants(m, d, q)
        return [
            d * q - Q_KOIDE,
            scalars[scalar_name] - target_val,
            obs["s13sq"] - TARGET["s13sq"],
        ]
    try:
        x_init = [M_STAR, DELTA_STAR, Q_PLUS_STAR]
        sol = optimize.fsolve(residuals, x_init, xtol=1e-13, full_output=True)
        x_r, info, ier, msg = sol
        res = residuals(x_r)
        if max(abs(r) for r in res) > 1e-8:
            return None
        # basin check
        H_r = H(*x_r)
        evals_r, _ = np.linalg.eigh(H_r)
        sig_r = (int(np.sum(evals_r > 1e-12)), int(np.sum(np.abs(evals_r) < 1e-12)),
                 int(np.sum(evals_r < -1e-12)))
        if sig_r != (1, 0, 2):
            return None
        m_r, d_r, q_r = x_r
        # Chamber interior check
        if q_r < math.sqrt(8.0 / 3.0) - d_r - 1e-6:
            return None
        obs_r = pmns_obs(*x_r)
        return {
            "m":      m_r,
            "delta":  d_r,
            "q":      q_r,
            "s12sq":  obs_r["s12sq"],
            "s13sq":  obs_r["s13sq"],
            "s23sq":  obs_r["s23sq"],
        }
    except Exception:
        return None


# Test the top few crossings
results_table = []
tested = set()
for c in crossings[:30]:
    key = (c["scalar"], c["target"])
    if key in tested:
        continue
    tested.add(key)
    # Skip trivially redundant constraints
    if c["scalar"] in ("q+ * delta",):
        continue
    res = try_closure(c["scalar"], c["target"], c["sv"])
    if res is None:
        continue
    # Check whether PMNS angles are in PDG 3-sigma
    in_3sig_12 = NUFIT_3SIG["s12sq"][0] <= res["s12sq"] <= NUFIT_3SIG["s12sq"][1]
    in_3sig_23 = NUFIT_3SIG["s23sq"][0] <= res["s23sq"] <= NUFIT_3SIG["s23sq"][1]
    dev_pinned_m = abs(res["m"] - M_STAR)
    dev_pinned_d = abs(res["delta"] - DELTA_STAR)
    dev_pinned_q = abs(res["q"] - Q_PLUS_STAR)
    results_table.append({
        **res,
        "scalar":      c["scalar"],
        "target":      c["target"],
        "target_val":  c["sv"],
        "dev_m":       dev_pinned_m,
        "dev_d":       dev_pinned_d,
        "dev_q":       dev_pinned_q,
        "in_3sig_12":  in_3sig_12,
        "in_3sig_23":  in_3sig_23,
    })

# Sort by displacement from pinned point (smaller = more consistent with PDG)
results_table.sort(key=lambda r: r["dev_m"] + r["dev_d"] + r["dev_q"])

print(f"\n  Closure candidates (sorted by displacement from pinned point):\n")
print(f"    {'scalar':40s}  {'target':>12s}  {'Δm':>8s}  {'Δδ':>8s}  {'Δq+':>8s}  {'s12²':>7s}  {'s23²':>7s}  {'3σ 12/23':>8s}")
for r in results_table[:15]:
    tag = ("Y" if r["in_3sig_12"] else "N") + "/" + ("Y" if r["in_3sig_23"] else "N")
    print(
        f"    {r['scalar']:40s}  {r['target']:>12s}  "
        f"{r['dev_m']:>8.5f}  {r['dev_d']:>8.5f}  {r['dev_q']:>8.5f}  "
        f"{r['s12sq']:>7.4f}  {r['s23sq']:>7.4f}  {tag:>8s}"
    )


# ============================================================================
# Summary and selection
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)


# Find the closest pinned-displacement closure
if results_table:
    best = results_table[0]
    print(f"""
  BEST candidate second-cut:
    constraint 1: delta * q_+ = 2/3
    constraint 2: {best['scalar']} = {best['target']} ({best['target_val']:.6f})
    constraint 3: sin^2 theta_13 = 0.0218 (PDG input)

  Produces:
    (m, delta, q_+) = ({best['m']:.6f}, {best['delta']:.6f}, {best['q']:.6f})
    displacement from pinned = ({best['dev_m']:.6f}, {best['dev_d']:.6f}, {best['dev_q']:.6f})

  Predicted angles:
    sin^2 theta_12 = {best['s12sq']:.6f}  (PDG 0.307, 3sigma {NUFIT_3SIG['s12sq']})
    sin^2 theta_23 = {best['s23sq']:.6f}  (PDG 0.545, 3sigma {NUFIT_3SIG['s23sq']})
    3sigma status:   s12 = {'PASS' if best['in_3sig_12'] else 'FAIL'}
                     s23 = {'PASS' if best['in_3sig_23'] else 'FAIL'}
""")

    check(
        f"Best closure ({best['scalar']} = {best['target']}) has both s12, s23 in 3sigma",
        best["in_3sig_12"] and best["in_3sig_23"],
        f"s12 {'PASS' if best['in_3sig_12'] else 'FAIL'}, s23 {'PASS' if best['in_3sig_23'] else 'FAIL'}",
    )
    check(
        f"Best closure point coincides with pinned (within 0.01 per coord)",
        max(best["dev_m"], best["dev_d"], best["dev_q"]) < 0.01,
        f"max dev = {max(best['dev_m'], best['dev_d'], best['dev_q']):.6f}",
    )
else:
    print("\n  No closure candidates found in scan.")
    check("Closure candidate exists", False, "no viable second cut found")


print("""
Iter 6 attack: combined-cuts scan for the second codim-1 constraint.

Method:
  Phase I: walk a 1-D curve along m under {delta * q_+ = 2/3, s13^2 = 0.0218}.
  Phase II: sweep many scalar invariants along the curve; find crossings of
            retained simple values near the pinned m_*.
  Phase III: for top crossings, solve the combined 3-constraint system
            (delta*q+ = 2/3, scalar = simple_value, s13^2 = PDG).
            Check whether resulting (m, delta, q_+) is close to pinned
            AND whether s12^2, s23^2 are in NuFit 3-sigma.

Interpretation:
  - If top candidate's displacement from pinned < 0.01 per coord AND both
    remaining angles are within 3-sigma => second cut identified.
  - Iter 7 would then attempt framework-native derivation of the
    confirmed second cut.
  - Otherwise report the closest candidate and rule out the class.
""")
