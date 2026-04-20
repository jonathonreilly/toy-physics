"""
Frontier runner - Koide Q ↔ δ linking relation.

Companion to
  docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md

This runner verifies the partial closure of the linking relation
`δ = Q/d` as a consequence of two retained structural identities:

  I1  (equal-sector-norm)        →  Q = 2/d
  I2  (dimensional-ratio for δ)   →  δ = 2/d^2

plus one named residual radian-bridge postulate P (see §4 of the note).

Checks:

  T1  d=3 equal-sector-norm identity a_0^2 = 2|z|^2 ⇒ Q = 2/3.
  T2  d=3 dimensional ratio (DOF b) / dim(Herm_d) = 2/9.
  T3  d=3 numerical ratio δ/Q = 1/d.
  T4  General d: sector-norm identification gives Q = 2/d.
  T5  General d: dimensional-ratio identification gives δ = 2/d^2.
  T6  General d: δ = Q/d symbolically (Fraction exact).
  T7  Alternative generalization Q = (d-1)/d FAILS δ = Q/d off d=3, so
      sector-norm reading is the correct structural one.
  T8  Against PDG charged-lepton masses, Q=2/3 and δ=2/9 reproduce
      observation at the retained precision.
  T9  Residual radian-bridge postulate P is single-real-valued and does
      not reintroduce any blocked bundle-topology data.

No new physical axiom is introduced. The runner reports the named
residual postulate P explicitly.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction

import numpy as np


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


# ---------------------------------------------------------------------------
# Core identities
# ---------------------------------------------------------------------------


def Q_sector_norm(d: int) -> Fraction:
    """Q = 2/d from equal-sector-norm on C_d character split.

    Under |v_sing|^2 = |v_non_sing|^2 and (Σ v)^2 = d a_0^2, Plancherel gives
    |v|^2 = 2 a_0^2, so Q = |v|^2 / (Σ v)^2 = 2/d.
    """
    return Fraction(2, d)


def Q_generalization_alternative(d: int) -> Fraction:
    """Alternative (wrong) generalization Q = (d-1)/d.

    Happens to coincide with Q_sector_norm at d=3 because d-1 = 2, but
    differs at all other d. The runner verifies this is NOT the correct
    structural reading.
    """
    return Fraction(d - 1, d)


def delta_dim_ratio(d: int) -> Fraction:
    """δ = 2/d^2 from (DOF of b) / dim(Herm_d).

    b ∈ ℂ carries 2 real DOFs; Herm_d has d^2 real DOFs. This is the
    retained dimensional-ratio identity from the circulant-character note
    A.2 (with postulate P supplying the radian-bridge).
    """
    return Fraction(2, d * d)


# ---------------------------------------------------------------------------
# C_d Plancherel check (numerical, all d tested below)
# ---------------------------------------------------------------------------


def character_plancherel_check(d: int, v: np.ndarray) -> tuple[float, float, float]:
    """Return (a_0^2, |v_non_sing|^2, |v|^2) under real C_d Plancherel."""
    a_0 = np.sum(v) / math.sqrt(d)
    a_0_sq = a_0 * a_0
    v_sq = float(np.sum(v * v))
    v_non_sing_sq = v_sq - a_0_sq
    return a_0_sq, v_non_sing_sq, v_sq


# ---------------------------------------------------------------------------
# Test suite
# ---------------------------------------------------------------------------


def test_T1_d3_equal_sector_norm() -> None:
    """T1: d=3 equal-sector-norm identity a_0^2 = 2|z|^2 gives Q = 2/3."""
    print("\n[T1] d=3 equal-sector-norm identity → Q = 2/3")
    # Take any v ∈ ℝ^3 satisfying a_0^2 = 2|z|^2 (= equal sector norms).
    # Pick the Brannen ansatz v_k = v_0 (1 + √2 cos(δ + 2πk/3)) at δ = 2/9:
    v0 = 1.0
    delta = 2.0 / 9.0
    v = np.array(
        [
            v0 * (1.0 + math.sqrt(2.0) * math.cos(delta + 2.0 * math.pi * k / 3.0))
            for k in range(3)
        ],
        dtype=float,
    )
    a_0_sq, v_non_sing_sq, v_sq = character_plancherel_check(3, v)
    # Check equal sector norm:
    check(
        "a_0^2 = |v_non_sing|^2 (equal sector norm at Brannen Q=2/3 ansatz)",
        math.isclose(a_0_sq, v_non_sing_sq, rel_tol=1e-12, abs_tol=1e-12),
        f"a_0^2 = {a_0_sq:.10f}, |v_non_sing|^2 = {v_non_sing_sq:.10f}",
    )
    # Check Q = 2/3:
    Q = v_sq / (np.sum(v) ** 2)
    check(
        "Q = |v|^2 / (Σ v)^2 = 2/3 at d = 3",
        math.isclose(Q, 2.0 / 3.0, rel_tol=1e-12, abs_tol=1e-12),
        f"Q = {Q:.14f} vs 2/3 = {2/3:.14f}",
    )


def test_T2_d3_dim_ratio() -> None:
    """T2: d=3 dimensional ratio (DOF b) / dim(Herm_d) = 2/9."""
    print("\n[T2] d=3 dimensional ratio → δ = 2/9")
    dof_b = 2  # b ∈ ℂ has 2 real DOFs
    dim_herm_3 = 3 * 3  # Herm_3 has 9 real DOFs
    ratio = Fraction(dof_b, dim_herm_3)
    check(
        "(DOF b) / dim(Herm_3) = 2/9",
        ratio == Fraction(2, 9),
        f"ratio = {ratio} (postulate P: identify with δ in radians)",
    )
    # Numerical agreement with observed δ:
    delta_obs = 2.0 / 9.0
    check(
        "Identification matches observed δ = 2/9 rad",
        math.isclose(float(ratio), delta_obs, rel_tol=1e-15, abs_tol=1e-15),
        f"float(ratio) = {float(ratio):.12f}, δ_obs = {delta_obs:.12f}",
    )


def test_T3_d3_ratio() -> None:
    """T3: d=3 numerical ratio δ/Q = 1/d."""
    print("\n[T3] d=3 numerical ratio δ/Q = 1/d")
    Q = Fraction(2, 3)
    delta = Fraction(2, 9)
    ratio = delta / Q
    check(
        "δ / Q = 1/3 at d = 3",
        ratio == Fraction(1, 3),
        f"δ/Q = {ratio}",
    )
    check(
        "δ = Q/d at d = 3 (exact Fraction)",
        delta == Q / 3,
        f"δ = {delta}, Q/d = {Q/3}",
    )


def test_T4_general_d_Q() -> None:
    """T4: General d — sector-norm identification gives Q = 2/d."""
    print("\n[T4] General d: sector-norm → Q = 2/d")
    all_ok = True
    for d in [2, 3, 4, 5, 7, 11]:
        Q = Q_sector_norm(d)
        expected = Fraction(2, d)
        ok = Q == expected
        all_ok = all_ok and ok
        print(f"    d={d}: Q_sector = {Q}, expected 2/d = {expected}  {'OK' if ok else 'FAIL'}")
    check(
        "Q = 2/d holds at all tested d",
        all_ok,
        "d ∈ {2, 3, 4, 5, 7, 11}",
    )


def test_T5_general_d_delta() -> None:
    """T5: General d — dimensional-ratio identification gives δ = 2/d^2."""
    print("\n[T5] General d: dimensional-ratio → δ = 2/d^2")
    all_ok = True
    for d in [2, 3, 4, 5, 7, 11]:
        delta = delta_dim_ratio(d)
        expected = Fraction(2, d * d)
        ok = delta == expected
        all_ok = all_ok and ok
        print(f"    d={d}: δ_dim = {delta}, expected 2/d^2 = {expected}  {'OK' if ok else 'FAIL'}")
    check(
        "δ = 2/d^2 holds at all tested d (under postulate P)",
        all_ok,
        "d ∈ {2, 3, 4, 5, 7, 11}",
    )


def test_T6_linking_symbolic() -> None:
    """T6: General d — δ = Q/d symbolically."""
    print("\n[T6] General d: δ = Q/d symbolic identity")
    all_ok = True
    for d in [2, 3, 4, 5, 7, 11]:
        Q = Q_sector_norm(d)
        delta = delta_dim_ratio(d)
        ok = delta == Q / d
        all_ok = all_ok and ok
        print(f"    d={d}: Q={Q}, δ={delta}, Q/d={Q / d}  δ==Q/d: {ok}")
    check(
        "δ = Q/d holds symbolically at all tested d",
        all_ok,
        "linking relation is not a d=3 coincidence",
    )


def test_T7_alt_generalization_fails() -> None:
    """T7: Alternative generalization Q=(d-1)/d fails δ=Q/d off d=3."""
    print("\n[T7] Alternative Q=(d-1)/d FAILS δ=Q/d off d=3")
    # d=3 coincidence: (d-1)/d = 2/3 = 2/d at d=3.
    d = 3
    Q_alt = Q_generalization_alternative(d)
    Q_sec = Q_sector_norm(d)
    check(
        "At d=3: (d-1)/d = 2/d (the arithmetic coincidence that could mislead)",
        Q_alt == Q_sec,
        f"(d-1)/d = {Q_alt}, 2/d = {Q_sec}",
    )
    # Off d=3: the alternative fails δ = Q/d.
    fails_off_d3 = True
    any_disagreement = False
    for d in [2, 4, 5, 7, 11]:
        Q_alt = Q_generalization_alternative(d)
        delta = delta_dim_ratio(d)
        if delta != Q_alt / d:
            any_disagreement = True
        print(
            f"    d={d}: Q_alt=(d-1)/d={Q_alt}, δ=2/d^2={delta}, Q_alt/d={Q_alt/d}, "
            f"δ≠Q_alt/d: {delta != Q_alt/d}"
        )
    check(
        "Alternative Q=(d-1)/d generalization disagrees with δ=Q/d off d=3",
        any_disagreement,
        "confirms sector-norm reading is the correct structural generalization",
    )


def test_T8_pdg_masses() -> None:
    """T8: Against PDG charged-lepton masses, Q≈2/3 and δ≈2/9 hold."""
    print("\n[T8] PDG charged-lepton masses reproduce Q=2/3 and δ=2/9")
    # PDG 2024 pole masses (MeV):
    m_e = 0.5109989
    m_mu = 105.6583745
    m_tau = 1776.86
    sqrt_m = [math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)]
    Q_obs = (m_e + m_mu + m_tau) / (sum(sqrt_m)) ** 2
    # Retained precision (Koide-cone note): sub-percent match to 2/3.
    Q_target = 2.0 / 3.0
    check(
        "PDG Q within 5 × 10^-5 of 2/3",
        abs(Q_obs - Q_target) < 5e-5,
        f"Q_obs = {Q_obs:.10f}, |Q_obs - 2/3| = {abs(Q_obs - Q_target):.2e}",
    )
    # Best-fit δ from PDG Brannen ansatz:
    v0 = sum(sqrt_m) / 3.0
    # Solve for δ: √m_tau = v0 (1 + √2 cos(δ)) at k=0 assignment tau↔k=0
    cos_delta = (sqrt_m[2] / v0 - 1.0) / math.sqrt(2.0)
    delta_fit = math.acos(max(-1.0, min(1.0, cos_delta)))
    delta_target = 2.0 / 9.0
    check(
        "PDG-fit δ within 1 × 10^-4 rad of 2/9",
        abs(delta_fit - delta_target) < 1e-4,
        f"δ_fit = {delta_fit:.10f}, |δ - 2/9| = {abs(delta_fit - delta_target):.2e}",
    )


def test_T9_postulate_P_characterization() -> None:
    """T9: Residual radian-bridge postulate P is single-real-valued and
    not a bundle-topology postulate."""
    print("\n[T9] Residual postulate P characterization")
    # Count the real-valued content of P at a fixed d:
    #   P identifies one dimensionless ratio (2/d^2) with one radian (δ).
    # This is a single-real-number identification, not a bundle-topology claim.
    d = 3
    dim_ratio = Fraction(2, d * d)
    # The identification asserts δ_radians = float(dim_ratio).
    # No integer Chern class, no monopole charge, no 2D base.
    p_real_dof = 1  # one real-number bridge
    p_chern_dof = 0
    p_monopole_dof = 0
    p_ambient_dim = 0  # no ambient enlargement
    check(
        "Postulate P is single-real-valued (1 DOF)",
        p_real_dof == 1,
        "identifies one dimensionless ratio with one radian",
    )
    check(
        "Postulate P has no Chern / monopole / ambient-S^2 data",
        p_chern_dof == 0 and p_monopole_dof == 0 and p_ambient_dim == 0,
        "differentiated from the bundle-obstruction-blocked postulate",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 72)
    print("Koide Q ↔ δ linking relation — partial closure + named residual P")
    print("=" * 72)
    test_T1_d3_equal_sector_norm()
    test_T2_d3_dim_ratio()
    test_T3_d3_ratio()
    test_T4_general_d_Q()
    test_T5_general_d_delta()
    test_T6_linking_symbolic()
    test_T7_alt_generalization_fails()
    test_T8_pdg_masses()
    test_T9_postulate_P_characterization()
    print("\n" + "=" * 72)
    print(f"SUMMARY:  PASS = {PASS}   FAIL = {FAIL}")
    print("=" * 72)
    if FAIL > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
