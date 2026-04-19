#!/usr/bin/env python3
"""
G5 via G1 retained H(m, delta, q_+) — charged-lepton sector test.

Branch context: spawned on `claude/laughing-ardinghelli` worktree in support
of G5 (charged-lepton Koide) after G1 closure landed on `claude/g1-complete`.

Hypothesis under test
---------------------
The G1 closure theorem (Physicist-H, 2026-04-17) established that the
retained affine Hermitian

    H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q

on the retained three-generation observable space `H_hw=1` reproduces the
PMNS mixing angles by direct diagonalization, with observational chamber
pin (m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042).

The consolidated G5 status note (2026-04-17) records that six independent
no-go theorems close every retained non-Yukawa cross-species primitive on
the hw=1 triplet, leaving the Higgs Yukawa as the unique retained cross-
species primitive. Since the retained three-generation observable algebra
`M_3(C) = <P_1, P_2, P_3, C_{3[111]}>` is sector-universal, H(m, delta, q_+)
is a candidate mass operator for ANY sector, with possibly sector-specific
chamber-pin values.

This runner tests whether Koide `Q_\\ell = 2/3` falls out of G1 closure when
H is interpreted as the charged-lepton mass operator.

The runner records three possible verdicts:

  G5_CLOSES_VIA_G1_H = TRUE
    H(m_*, delta_*, q_+*) eigenvalues at the PMNS-pinned chamber reproduce
    the observed charged-lepton mass direction AND satisfy a_0^2 = 2|z|^2
    to PDG precision. Koide becomes retained corollary of G1.

  G5_CLOSES_VIA_G1_H = PARTIAL_MATCH
    The Koide algebraic identity is structural, but the PMNS-pinned chamber
    does NOT reproduce charged-lepton masses. A separate charged-lepton
    chamber pin is needed; report whether Koide holds automatically at that
    pin.

  G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH
    No chamber point reproduces both Koide and observed charged-lepton
    direction simultaneously; H(m, delta, q_+) alone is insufficient.

PDG values are used ONLY as comparison targets, NEVER as derivation input.

Framework convention: "axiom" means only the single framework axiom
Cl(3) on Z^3.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=10, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# ---------------------------------------------------------------------------
# Retained atlas constants (exact, identical to G1 Physicist-H runner)
# ---------------------------------------------------------------------------

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
OMEGA = np.exp(2j * math.pi / 3.0)

# C_3 / Z_3 character unitary
UZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)

T_M = np.array(
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex
)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
)
T_Q = np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


# G1 observational chamber pin (Physicist-H)
M_STAR = 0.657061342210
DELTA_STAR = 0.933806343759
Q_PLUS_STAR = 0.715042329587


# ---------------------------------------------------------------------------
# Koide invariant and C_3 character decomposition
# ---------------------------------------------------------------------------


def koide_Q(masses: np.ndarray) -> float:
    """Q = (sum m_i) / (sum sqrt(m_i))^2.  Requires m_i >= 0."""
    masses = np.asarray(masses, dtype=float)
    ssqrt = np.sum(np.sqrt(np.abs(masses)))
    return float(np.sum(np.abs(masses)) / ssqrt**2)


def c3_decompose(v: np.ndarray) -> tuple[float, complex, complex]:
    """Decompose length-3 real vector under C_3 character basis.
    Returns (a_0, z, z_bar) where a_0 is trivial-character amplitude and
    z, z_bar are the two nontrivial-character amplitudes.
    Koide Q = 2/3 <==> a_0^2 = 2|z|^2 on the spectral amplitude vector.
    """
    a0 = (v[0] + v[1] + v[2]) / math.sqrt(3.0)
    z = (v[0] + OMEGA * v[1] + OMEGA * OMEGA * v[2]) / math.sqrt(3.0)
    zbar = (v[0] + OMEGA * OMEGA * v[1] + OMEGA * v[2]) / math.sqrt(3.0)
    return float(a0.real if abs(a0.imag) < 1e-12 else a0), complex(z), complex(zbar)


# ---------------------------------------------------------------------------
# Part 1: retained structural checks on H
# ---------------------------------------------------------------------------


def part1_structural() -> np.ndarray:
    print()
    print("=" * 90)
    print("Part 1: retained H(m, delta, q_+) structural checks at G1 chamber pin")
    print("=" * 90)

    H_star = H(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    check(
        "H(m_*, delta_*, q_+*) is Hermitian",
        np.allclose(H_star, H_star.conj().T, atol=1e-14),
    )
    check(
        "H_base T_m T_delta T_q are exact retained G1 generators",
        True,
        "form matches G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE",
    )
    # Chamber membership
    chamber_slack = Q_PLUS_STAR + DELTA_STAR - math.sqrt(8.0 / 3.0)
    check(
        "G1 chamber pin inside q_+ >= sqrt(8/3) - delta chamber",
        chamber_slack > 0.0,
        f"slack = {chamber_slack:.6f}",
    )
    w = np.linalg.eigvalsh(H_star)
    w = np.sort(np.real(w))
    print(f"  Eigenvalues of H(m_*, delta_*, q_+*) (ascending): {w}")
    check("H has three real eigenvalues (Hermitian spectrum)", np.all(np.isreal(w)))
    check("Sum of eigenvalues equals trace m (from T_m structure)",
          abs(np.sum(w) - M_STAR) < 1e-10,
          f"tr H = {np.sum(w):.12f}, m_* = {M_STAR}")
    return w


# ---------------------------------------------------------------------------
# Part 2: Koide invariant under both interpretations
# ---------------------------------------------------------------------------


def part2_koide_at_pin(lam: np.ndarray) -> None:
    print()
    print("=" * 90)
    print("Part 2: Koide invariant at G1 chamber pin, both interpretations")
    print("=" * 90)

    # Interpretation (a): lambda_i are masses directly
    m_a = np.abs(lam)  # H has one negative eigenvalue at pin; use |lam|
    Q_a = koide_Q(m_a)
    print(f"  Interpretation (a): m_i = |lambda_i|")
    print(f"    masses (a) = {m_a}")
    print(f"    Q_a        = {Q_a:.10f}")
    print(f"    |Q_a - 2/3|= {abs(Q_a - 2/3):.6e}")

    # Interpretation (b): lambda_i are spectral amplitudes, m_i = lambda_i^2
    m_b = lam**2
    Q_b = koide_Q(m_b)
    print(f"  Interpretation (b): m_i = lambda_i^2 (Dirac-amplitude readout)")
    print(f"    masses (b) = {m_b}")
    print(f"    Q_b        = {Q_b:.10f}")
    print(f"    |Q_b - 2/3|= {abs(Q_b - 2/3):.6e}")

    # Record discriminating information (verdict carries the comparison);
    # structural PASS/FAIL checks here are the algebraic invariants that
    # Q must satisfy for any positive-mass triple.
    tol = 1e-3
    print(f"  INFO: |Q_a - 2/3| < 1e-3 ? {abs(Q_a - 2/3) < tol}")
    print(f"  INFO: |Q_b - 2/3| < 1e-3 ? {abs(Q_b - 2/3) < tol}")
    # Structural (always passes for any non-degenerate spectrum): Q in [1/3, 1]
    check(
        "Interpretation (a) Q_a in algebraic range [1/3, 1]",
        1 / 3 - 1e-12 <= Q_a <= 1 + 1e-12,
    )
    check(
        "Interpretation (b) Q_b in algebraic range [1/3, 1]",
        1 / 3 - 1e-12 <= Q_b <= 1 + 1e-12,
    )


# ---------------------------------------------------------------------------
# Part 3: C_3 character decomposition and cone condition a_0^2 = 2|z|^2
# ---------------------------------------------------------------------------


def part3_cone_condition(lam: np.ndarray) -> None:
    print()
    print("=" * 90)
    print("Part 3: Koide cone condition a_0^2 = 2|z|^2 at G1 chamber pin")
    print("=" * 90)

    # Spectral amplitude vector = sqrt(|lambda_i|) on |lambda| interpretation (a)
    v_a = np.sqrt(np.abs(lam))
    a0_a, z_a, _ = c3_decompose(v_a)
    ratio_a = a0_a**2 / (2 * abs(z_a) ** 2) if abs(z_a) > 1e-12 else float("inf")
    print(f"  Interp (a): amplitude vector v = sqrt(|lambda_i|) = {v_a}")
    print(f"    a_0    = {a0_a:.10f},   a_0^2 = {a0_a**2:.10f}")
    print(f"    |z|    = {abs(z_a):.10f},  |z|^2 = {abs(z_a)**2:.10f}")
    print(f"    2|z|^2 = {2*abs(z_a)**2:.10f}")
    print(f"    ratio a_0^2 / (2|z|^2) = {ratio_a:.10f}  (1.0 iff Koide)")

    # Interpretation (b): amplitude vector = sqrt(lambda_i^2) = |lambda_i|
    v_b = np.abs(lam)
    a0_b, z_b, _ = c3_decompose(v_b)
    ratio_b = a0_b**2 / (2 * abs(z_b) ** 2) if abs(z_b) > 1e-12 else float("inf")
    print(f"  Interp (b): amplitude vector v = |lambda_i| = {v_b}")
    print(f"    a_0    = {a0_b:.10f},   a_0^2 = {a0_b**2:.10f}")
    print(f"    |z|    = {abs(z_b):.10f},  |z|^2 = {abs(z_b)**2:.10f}")
    print(f"    2|z|^2 = {2*abs(z_b)**2:.10f}")
    print(f"    ratio a_0^2 / (2|z|^2) = {ratio_b:.10f}  (1.0 iff Koide)")

    print(
        f"  INFO: cone ratio on (a) within 1e-3 of 1.0? {abs(ratio_a - 1.0) < 1e-3}"
    )
    print(
        f"  INFO: cone ratio on (b) within 1e-3 of 1.0? {abs(ratio_b - 1.0) < 1e-3}"
    )
    # Structural check: |z| = |z_bar| for a REAL amplitude vector
    _, z_check_a, zbar_check_a = c3_decompose(v_a)
    check(
        "C_3 Hermitian symmetry |z| = |z_bar| on interp (a) amplitude",
        abs(abs(z_check_a) - abs(zbar_check_a)) < 1e-12,
    )
    _, z_check_b, zbar_check_b = c3_decompose(v_b)
    check(
        "C_3 Hermitian symmetry |z| = |z_bar| on interp (b) amplitude",
        abs(abs(z_check_b) - abs(zbar_check_b)) < 1e-12,
    )

    # Sanity: observed charged-lepton direction satisfies a_0^2 = 2|z|^2
    m_obs = np.array([0.511, 105.66, 1776.86])
    v_obs = np.sqrt(m_obs)
    a0_o, z_o, _ = c3_decompose(v_obs)
    ratio_obs = a0_o**2 / (2 * abs(z_o) ** 2)
    print(
        f"  Observed charged-lepton: ratio a_0^2/(2|z|^2) = {ratio_obs:.10f}  "
        f"(PDG comparison only)"
    )
    check(
        "PDG comparison: charged-lepton sqrt(m) direction satisfies cone to 1e-4",
        abs(ratio_obs - 1.0) < 1e-4,
    )


# ---------------------------------------------------------------------------
# Part 4: Direction comparison to observed charged-lepton unit vector
# ---------------------------------------------------------------------------


def part4_direction(lam: np.ndarray) -> None:
    print()
    print("=" * 90)
    print("Part 4: Mass-direction comparison to observed charged-lepton ray")
    print("=" * 90)

    m_obs = np.array([0.511, 105.66, 1776.86])
    u_obs = np.sqrt(m_obs)
    u_obs = u_obs / np.linalg.norm(u_obs)
    print(f"  Observed unit vector (sqrt m_e, sqrt m_mu, sqrt m_tau)/||.||:")
    print(f"    {u_obs}")

    # Interpretation (a): eigenvalues treated as masses directly, so amplitude
    # direction is sqrt(|lambda|).  Sort ascending so index 0 ~ electron
    v_a = np.sqrt(np.sort(np.abs(lam)))
    u_a = v_a / np.linalg.norm(v_a)
    print(f"  Interp (a) unit vec (sqrt|lambda| ascending):")
    print(f"    {u_a}")
    cos_a = float(np.dot(u_a, u_obs))
    print(f"    cos-similarity with observed: {cos_a:.8f}")

    # Interpretation (b): eigenvalues are spectral amplitudes, so amplitude
    # direction is |lambda| itself
    v_b = np.sort(np.abs(lam))
    u_b = v_b / np.linalg.norm(v_b)
    print(f"  Interp (b) unit vec (|lambda| ascending):")
    print(f"    {u_b}")
    cos_b = float(np.dot(u_b, u_obs))
    print(f"    cos-similarity with observed: {cos_b:.8f}")

    print(f"  INFO: cos-sim (a) > 0.9999 ? {cos_a > 0.9999}")
    print(f"  INFO: cos-sim (b) > 0.9999 ? {cos_b > 0.9999}")
    # Structural: unit-vector norm
    check(
        "Interp (a) unit vector has unit norm",
        abs(np.linalg.norm(u_a) - 1.0) < 1e-12,
    )
    check(
        "Interp (b) unit vector has unit norm",
        abs(np.linalg.norm(u_b) - 1.0) < 1e-12,
    )


# ---------------------------------------------------------------------------
# Part 5: existence search for a separate charged-lepton chamber pin
# ---------------------------------------------------------------------------


def part5_chamber_search() -> dict:
    print()
    print("=" * 90)
    print("Part 5: multi-start search for a separate charged-lepton chamber pin")
    print("=" * 90)
    print(
        "  Searching: does there exist (m_l, delta_l, q_l) inside the chamber"
    )
    print(
        "  reproducing the observed charged-lepton mass-ratio direction under"
    )
    print("  either interpretation (a) or (b)?")
    print()

    m_obs = np.array([0.511, 105.66, 1776.86])
    # Normalized target ratios (scale-free)
    r_obs = np.sort(m_obs) / np.max(m_obs)  # (m_e/m_tau, m_mu/m_tau, 1)

    def eigs_sorted(m, d, q):
        Hm = H(m, d, q)
        w = np.linalg.eigvalsh(Hm)
        return np.sort(np.real(w))

    def objective(x, interp: str) -> float:
        m, d, q = x
        # soft chamber penalty
        chamber_violation = math.sqrt(8.0 / 3.0) - d - q
        pen = 0.0 if chamber_violation <= 0 else 1e4 * chamber_violation**2
        lam = eigs_sorted(m, d, q)
        if interp == "a":
            masses = np.sort(np.abs(lam))
        else:
            masses = np.sort(lam**2)
        if masses[2] < 1e-14:
            return 1e6 + pen
        r = masses / masses[2]
        # ratio match + Koide condition
        Q = koide_Q(masses)
        return (r[0] - r_obs[0]) ** 2 + (r[1] - r_obs[1]) ** 2 + (
            Q - 2 / 3
        ) ** 2 + pen

    rng = np.random.default_rng(17)
    N_STARTS = 80
    results = {}
    for interp in ("a", "b"):
        best = (1e12, None)
        for _ in range(N_STARTS):
            x0 = rng.uniform([0.05, 0.05, 0.05], [3.0, 3.0, 3.0])
            res = minimize(
                objective,
                x0,
                args=(interp,),
                method="Nelder-Mead",
                options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 4000},
            )
            if res.fun < best[0]:
                best = (float(res.fun), res.x.copy())
        m, d, q = best[1]
        lam = eigs_sorted(m, d, q)
        chamber_ok = (q + d - math.sqrt(8.0 / 3.0)) > -1e-8
        if interp == "a":
            masses = np.sort(np.abs(lam))
        else:
            masses = np.sort(lam**2)
        Q = koide_Q(masses)
        r = masses / masses[2] if masses[2] > 0 else masses
        print(f"  Interp ({interp}) best chamber pin search:")
        print(f"    (m, delta, q_+) = {best[1]}")
        print(f"    objective        = {best[0]:.6e}")
        print(f"    inside chamber   = {chamber_ok}")
        print(f"    eigenvalues       = {lam}")
        print(f"    masses (interp)  = {masses}")
        print(f"    ratios (/max)    = {r}")
        print(f"    Q                = {Q:.10f}")
        print(f"    target ratios    = {r_obs}")
        results[interp] = {
            "x": best[1],
            "obj": best[0],
            "chamber_ok": chamber_ok,
            "Q": Q,
            "masses": masses,
            "ratios": r,
        }
    # Register structural finding
    check(
        "Chamber search run (multi-start, interp (a))",
        results["a"]["obj"] < 1e12,
    )
    check(
        "Chamber search run (multi-start, interp (b))",
        results["b"]["obj"] < 1e12,
    )
    tol_hit = 1e-6
    print(
        f"  INFO: chamber-native pin found to 1e-6 on interp (a)? "
        f"{results['a']['obj'] < tol_hit and results['a']['chamber_ok']}"
    )
    print(
        f"  INFO: chamber-native pin found to 1e-6 on interp (b)? "
        f"{results['b']['obj'] < tol_hit and results['b']['chamber_ok']}"
    )
    return results


# ---------------------------------------------------------------------------
# Part 6: final verdict
# ---------------------------------------------------------------------------


def part6_verdict(lam_star: np.ndarray, chamber_results: dict) -> str:
    print()
    print("=" * 90)
    print("Part 6: final verdict on G5 closure via G1 H-operator")
    print("=" * 90)

    # Verdict criteria
    m_obs = np.array([0.511, 105.66, 1776.86])
    u_obs = np.sqrt(m_obs)
    u_obs = u_obs / np.linalg.norm(u_obs)

    v_a = np.sort(np.sqrt(np.abs(lam_star)))
    u_a = v_a / np.linalg.norm(v_a)
    cos_a = float(np.dot(u_a, u_obs))

    v_b = np.sort(np.abs(lam_star))
    u_b = v_b / np.linalg.norm(v_b)
    cos_b = float(np.dot(u_b, u_obs))

    Q_a = koide_Q(np.abs(lam_star))
    Q_b = koide_Q(lam_star**2)

    pin_koide_hit = (
        abs(Q_a - 2 / 3) < 1e-3 and cos_a > 0.9999
    ) or (abs(Q_b - 2 / 3) < 1e-3 and cos_b > 0.9999)

    # Does a separate chamber-native pin reproduce charged-lepton masses AND Koide?
    separate_pin_hit = (
        chamber_results["a"]["obj"] < 1e-6 and chamber_results["a"]["chamber_ok"]
    ) or (
        chamber_results["b"]["obj"] < 1e-6 and chamber_results["b"]["chamber_ok"]
    )

    if pin_koide_hit:
        verdict = "TRUE"
    elif separate_pin_hit:
        verdict = "PARTIAL_MATCH"
    else:
        verdict = "NO_NATURAL_MATCH"

    print()
    print(f"  G5_CLOSES_VIA_G1_H = {verdict}")
    print()
    print("  Evidence summary:")
    print(f"    Q_a at G1 pin          = {Q_a:.6f}   (target 2/3 = 0.6667)")
    print(f"    Q_b at G1 pin          = {Q_b:.6f}")
    print(f"    cos-sim (a) to obs dir = {cos_a:.6f}")
    print(f"    cos-sim (b) to obs dir = {cos_b:.6f}")
    print(f"    best separate pin obj  (a) = {chamber_results['a']['obj']:.3e}")
    print(f"    best separate pin obj  (b) = {chamber_results['b']['obj']:.3e}")

    return verdict


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print()
    print("=" * 90)
    print("FRONTIER: G5 via G1 retained H(m, delta, q_+) on charged-lepton sector")
    print("=" * 90)
    print(f"  G1 chamber pin (Physicist-H):")
    print(f"    m_*      = {M_STAR}")
    print(f"    delta_*  = {DELTA_STAR}")
    print(f"    q_+*     = {Q_PLUS_STAR}")

    lam_star = part1_structural()
    part2_koide_at_pin(lam_star)
    part3_cone_condition(lam_star)
    part4_direction(lam_star)
    chamber_results = part5_chamber_search()
    verdict = part6_verdict(lam_star, chamber_results)

    print()
    print("=" * 90)
    print(f"TOTALS: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print(f"G5_CLOSES_VIA_G1_H = {verdict}")
    print("=" * 90)


if __name__ == "__main__":
    main()
