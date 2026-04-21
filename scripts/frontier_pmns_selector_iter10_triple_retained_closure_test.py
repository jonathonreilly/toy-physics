#!/usr/bin/env python3
"""
PMNS selector iter 10: triple-retained closure test.

Insight from iter 9: both iter-5 and iter-6 cuts are expressible in
terms of the retained SELECTOR = sqrt(6)/3:
  (i) delta * q_+ = SELECTOR^2       (= 2/3 = Q_Koide)
  (ii) det(H)      = 2 SELECTOR / sqrt(3)  (= E2 = sqrt(8)/3)

Observation: Tr(H) = m (since H_base has zero trace, T_Delta has zero
trace, T_Q has zero trace, only T_M contributes). At the closure point
from iter 6, m_c = 0.660242 ≈ 2/3 = Q_Koide to about 1% deviation.

Iter 10 attack: test whether Tr(H) = Q_Koide = 2/3 is a viable THIRD
retained cut. Under the combined three constraints:
  (1) Tr(H)    = 2/3
  (2) delta * q_+ = 2/3
  (3) det(H)   = sqrt(8)/3
solve for (m, delta, q_+). Since Tr(H) = m, constraint (1) fixes
m = 2/3 exactly. Then (2) and (3) are a 2-eq system in (delta, q_+).

If the solution:
  - lies in the A-BCC basin,
  - is inside the chamber,
  - produces PMNS angles within NuFit 3-sigma (all three),
then we have a **full 3-retained-identity closure** with ZERO
observational inputs — gate closure.

Secondary test: if m = 2/3 is NOT compatible, try m = SELECTOR * q_+,
m = SELECTOR^2, m = delta, or other natural retained candidates.

Honest outcome reporting.
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
SELECTOR = math.sqrt(6.0) / 3.0
Q_KOIDE = 2.0 / 3.0
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
    return {"w": w, "V": V, "P": P, "s12sq": float(s12sq), "s13sq": float(s13sq),
            "s23sq": float(s23sq), "J": J, "sin_dcp": float(sin_dcp),
            "det_H": float(np.linalg.det(H_m).real)}


def signature(H_m: np.ndarray) -> tuple[int, int, int]:
    evals = np.linalg.eigvalsh(H_m).real
    return (int(np.sum(evals > 1e-10)), int(np.sum(np.abs(evals) < 1e-10)),
            int(np.sum(evals < -1e-10)))


# ============================================================================
# Part A: Verify Tr(H) = m structural identity and its value at pinned
# ============================================================================
print("=" * 72)
print("Part A: Tr(H) = m identity + value at pinned / closure")
print("=" * 72)

H_pinned = H(M_STAR, DELTA_STAR, Q_PLUS_STAR)
tr_at_pinned = np.trace(H_pinned).real

print(f"\n  Tr(H_base)  = {np.trace(H_BASE).real:+.6f}  (should be 0)")
print(f"  Tr(T_M)     = {np.trace(T_M).real:+.6f}  (should be 1)")
print(f"  Tr(T_Delta) = {np.trace(T_DELTA).real:+.6f}  (should be 0)")
print(f"  Tr(T_Q)     = {np.trace(T_Q).real:+.6f}  (should be 0)")
print(f"\n  Conclusion: Tr(H(m, delta, q_+)) = m identically.")

check(
    "A.1 Tr(H_base) = 0 (retained)",
    abs(np.trace(H_BASE).real) < 1e-12,
    f"Tr(H_base) = {np.trace(H_BASE).real:.3e}",
)
check(
    "A.2 Tr(T_M) = 1 (T_M contributes to m direction)",
    abs(np.trace(T_M).real - 1.0) < 1e-12,
    f"Tr(T_M) = {np.trace(T_M).real}",
)
check(
    "A.3 Tr(T_Delta) = Tr(T_Q) = 0 (δ and q_+ directions are traceless)",
    abs(np.trace(T_DELTA).real) + abs(np.trace(T_Q).real) < 1e-12,
    f"Tr(T_Δ) + Tr(T_Q) = {abs(np.trace(T_DELTA).real) + abs(np.trace(T_Q).real):.3e}",
)

print(f"\n  Tr(H) at pinned = m_* = {tr_at_pinned:.6f}")
print(f"  Q_Koide = 2/3 = {Q_KOIDE:.6f}")
print(f"  |deviation|     = {abs(tr_at_pinned - Q_KOIDE):.6f}  (0.15% on this scale)")


# ============================================================================
# Part B: Triple-retained closure test: impose Tr(H)=2/3, delta*q+=2/3, det(H)=E2
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Triple-retained closure — impose 3 SELECTOR-based identities")
print("=" * 72)


def residuals_triple(x):
    m, d, q = x
    H_m = H(m, d, q)
    det_val = np.linalg.det(H_m).real
    return [
        m - Q_KOIDE,              # Tr(H) = 2/3
        d * q - Q_KOIDE,          # delta * q_+ = 2/3
        det_val - E2,             # det(H) = sqrt(8)/3
    ]


# Solve with warm start from pinned
x0 = np.array([M_STAR, DELTA_STAR, Q_PLUS_STAR])
try:
    sol = optimize.fsolve(residuals_triple, x0, xtol=1e-14, full_output=True)
    x_triple, info, ier, msg = sol
    res_triple = residuals_triple(x_triple)
    m_t, d_t, q_t = x_triple
    conv = max(abs(r) for r in res_triple) < 1e-10
except Exception as e:
    print(f"  fsolve failed: {e}")
    conv = False

if conv:
    print(f"\n  Triple-constraint solution:")
    print(f"    m     = {m_t:.12f}  (should be 2/3 = {Q_KOIDE:.12f})")
    print(f"    delta = {d_t:.12f}")
    print(f"    q_+   = {q_t:.12f}")
    print(f"    residuals = ({res_triple[0]:.3e}, {res_triple[1]:.3e}, {res_triple[2]:.3e})")

    H_t = H(m_t, d_t, q_t)
    sig_t = signature(H_t)
    chamber_ok = q_t >= math.sqrt(8.0 / 3.0) - d_t - 1e-6
    obs_t = pmns_obs(m_t, d_t, q_t)

    print(f"\n  Verification:")
    print(f"    Signature: {sig_t}  (target (1, 0, 2) for A-BCC basin)")
    print(f"    Chamber interior: q+ - (√(8/3) - delta) = "
          f"{q_t - (math.sqrt(8.0 / 3.0) - d_t):.6f}")
    print(f"\n  Resulting PMNS observables:")
    print(f"    sin²θ_12 = {obs_t['s12sq']:.6f}  (PDG {TARGET['s12sq']}, "
          f"3σ NO {NUFIT_3SIG['s12sq']})")
    print(f"    sin²θ_13 = {obs_t['s13sq']:.6f}  (PDG {TARGET['s13sq']}, "
          f"3σ NO {NUFIT_3SIG['s13sq']})")
    print(f"    sin²θ_23 = {obs_t['s23sq']:.6f}  (PDG {TARGET['s23sq']}, "
          f"3σ NO {NUFIT_3SIG['s23sq']})")
    print(f"    sin(δ_CP) = {obs_t['sin_dcp']:+.6f}")
    print(f"    det(H)    = {obs_t['det_H']:.6f}  (target E2 = {E2:.6f})")

    in_basin = sig_t == (1, 0, 2)
    in_chamber = chamber_ok
    in_3sig_12 = NUFIT_3SIG["s12sq"][0] <= obs_t["s12sq"] <= NUFIT_3SIG["s12sq"][1]
    in_3sig_13 = NUFIT_3SIG["s13sq"][0] <= obs_t["s13sq"] <= NUFIT_3SIG["s13sq"][1]
    in_3sig_23 = NUFIT_3SIG["s23sq"][0] <= obs_t["s23sq"] <= NUFIT_3SIG["s23sq"][1]

    check("B.1 Solution lies in A-BCC basin (signature 1, 0, 2)", in_basin,
          f"signature = {sig_t}")
    check("B.2 Solution inside chamber (q+ + delta >= sqrt(8/3))", in_chamber,
          f"q+ + delta - sqrt(8/3) = {q_t + d_t - math.sqrt(8.0/3.0):.6f}")
    check("B.3 sin^2 theta_12 within NuFit 3-sigma NO", in_3sig_12,
          f"s12² = {obs_t['s12sq']:.6f}")
    check("B.4 sin^2 theta_13 within NuFit 3-sigma NO", in_3sig_13,
          f"s13² = {obs_t['s13sq']:.6f}")
    check("B.5 sin^2 theta_23 within NuFit 3-sigma NO", in_3sig_23,
          f"s23² = {obs_t['s23sq']:.6f}")
    check("B.6 sin(delta_CP) < 0 (T2K-preferred)", obs_t["sin_dcp"] < 0,
          f"sin(δ_CP) = {obs_t['sin_dcp']:+.4f}")

    all_pass = in_basin and in_chamber and in_3sig_12 and in_3sig_13 and in_3sig_23
    check("B.7 FULL CLOSURE: 3 retained identities predict all PMNS at 3-sigma",
          all_pass,
          "gate closes" if all_pass else "hypothesis disproven")
else:
    print("  fsolve did not converge")
    check("B.1 Triple-constraint system has a solution",
          False, "fsolve failed to converge")


# ============================================================================
# Part C: alternative third-identity candidates
# ============================================================================
print("\n" + "=" * 72)
print("Part C: alternative third-identity candidates")
print("=" * 72)

alternative_third = [
    ("Tr(H) = SELECTOR",              lambda m, d, q: m - SELECTOR),
    ("Tr(H) = 1/sqrt(3)",             lambda m, d, q: m - 1/math.sqrt(3)),
    ("Tr(H) = E2",                    lambda m, d, q: m - E2),
    ("Tr(H) = 1/2",                   lambda m, d, q: m - 0.5),
    ("delta - q_+ = 0",               lambda m, d, q: d - q),
    ("delta - q_+ = SELECTOR - 1/sqrt(3)",
                                        lambda m, d, q: (d - q) - (SELECTOR - 1/math.sqrt(3))),
    ("delta + q_+ = sqrt(8/3) + small", None),  # chamber boundary, skip
    ("m = SELECTOR * delta",          lambda m, d, q: m - SELECTOR * d),
    ("m * q_+ = 1/2",                 lambda m, d, q: m * q - 0.5),
    ("m * delta = 1/sqrt(3)",         lambda m, d, q: m * d - 1/math.sqrt(3)),
]


def residuals_alt(x, third_fn):
    m, d, q = x
    H_m = H(m, d, q)
    det_val = np.linalg.det(H_m).real
    return [d * q - Q_KOIDE, det_val - E2, third_fn(m, d, q)]


print(f"\n  Testing each candidate third-cut in combination with δ·q+=2/3, det(H)=E2:\n")
print(f"  {'Third cut':40s}  {'(m, δ, q+)':>50s}  {'s12²':>7s}  {'s13²':>7s}  {'s23²':>7s}  {'3σ':>5s}")

alt_results = []
for name, third_fn in alternative_third:
    if third_fn is None:
        continue
    try:
        sol = optimize.fsolve(
            lambda x: residuals_alt(x, third_fn),
            x0,
            xtol=1e-12,
            full_output=True,
        )
        x_a, info, ier, msg = sol
        res_a = residuals_alt(x_a, third_fn)
        if max(abs(r) for r in res_a) > 1e-6:
            continue
        m_a, d_a, q_a = x_a
        H_a = H(m_a, d_a, q_a)
        sig_a = signature(H_a)
        if sig_a != (1, 0, 2):
            continue
        if q_a < math.sqrt(8.0 / 3.0) - d_a - 1e-6:
            continue
        obs_a = pmns_obs(m_a, d_a, q_a)
        in_all_3sig = all([
            NUFIT_3SIG["s12sq"][0] <= obs_a["s12sq"] <= NUFIT_3SIG["s12sq"][1],
            NUFIT_3SIG["s13sq"][0] <= obs_a["s13sq"] <= NUFIT_3SIG["s13sq"][1],
            NUFIT_3SIG["s23sq"][0] <= obs_a["s23sq"] <= NUFIT_3SIG["s23sq"][1],
        ])
        tag = "Y" if in_all_3sig else "N"
        print(f"  {name:40s}  ({m_a:.4f}, {d_a:.4f}, {q_a:.4f}){'':>16s}  "
              f"{obs_a['s12sq']:>7.4f}  {obs_a['s13sq']:>7.4f}  {obs_a['s23sq']:>7.4f}  {tag:>5s}")
        alt_results.append({
            "name":     name,
            "x":        (m_a, d_a, q_a),
            "obs":      obs_a,
            "3sig":     in_all_3sig,
        })
    except Exception:
        continue

print(f"\n  Candidates with all 3 angles in 3σ: {sum(1 for r in alt_results if r['3sig'])}/{len(alt_results)}")


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 10 attack: triple-retained closure test.

Method:
  Part A: verify Tr(H) = m as a framework identity (H_base, T_Delta,
          T_Q all have zero trace).
  Part B: impose 3 SELECTOR-based identities simultaneously:
            Tr(H)        = 2/3  (= SELECTOR^2)
            delta * q_+  = 2/3  (= SELECTOR^2)
            det(H)       = E2   (= 2*SELECTOR/sqrt(3))
          Solve for (m, delta, q_+), check A-BCC basin, chamber
          interior, and PMNS angles within NuFit 3-sigma NO.
  Part C: test alternative third-identity candidates (Tr(H) = SELECTOR,
          m = SELECTOR*delta, m*q = 1/2, etc.).

If Part B's B.7 PASSes: gate CLOSES via 3 retained identities — no
observational input needed.
If Part B's B.7 FAILs or Part B fails: check Part C alternatives.

Concrete hypothesis: the third retained identity is Tr(H) = 2/3 (= m).
Motivation: at iter-6 closure, m_c = 0.660 ≈ 2/3 (0.9% off). This is
similar to the 0.16% and 1.7% initial deviations of the iter-5 and
iter-6 identities before imposition — may be exact.
""")
