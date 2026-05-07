"""Block 02 R2.A: exact-arithmetic verification of Theorem (T2).

Verifies the closed-form single-plaquette heat-kernel expectation:
    ⟨(1/N_c) Re Tr U⟩_HK,1plaq(t) = exp(-2 t / 3)
at SU(3) under Block 01's derived t(6) = 1, giving:
    ⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134171190

Crucially, the closed form is exact in TWO characters (the (1,0) and
(0,1) fundamentals) — no NMAX truncation needed by Schur orthogonality.

Companion: docs/BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md
Block: 02

Cross-validates with the Wilson V=1 single-plaquette value 0.4225317396
(from PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06)
to demonstrate the ~21% structural difference between heat-kernel and
Wilson at the framework's β = 6 evaluation.
"""
from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple

import sympy as sp


def dim_su3(p: int, q: int) -> int:
    """Dimension of SU(3) irrep (p, q)."""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def casimir_su3_exact(p: int, q: int) -> Fraction:
    """Quadratic Casimir of SU(3) irrep (p,q): exact rational.

    C_2(p,q) = (p² + p·q + q² + 3 p + 3 q) / 3
    """
    return Fraction(p * p + p * q + q * q + 3 * p + 3 * q, 3)


def conjugate_irrep(p: int, q: int) -> Tuple[int, int]:
    """Conjugate of SU(3) irrep (p,q) is (q,p)."""
    return (q, p)


def schur_overlap(lambda1: Tuple[int, int], lambda2: Tuple[int, int]) -> int:
    """∫ χ_λ1(U) · χ_λ2(U) dU = δ_{λ2, conjugate(λ1)}."""
    return 1 if lambda2 == conjugate_irrep(*lambda1) else 0


def hk_partition_one_plaquette(t: sp.Expr, NMAX: int) -> sp.Expr:
    """Z_HK,1plaq(t) = ∫ P_t(U) dU = 1 (probability normalization).

    Verified by truncated character expansion: only (0,0) trivial rep
    integrates to non-zero (= 1).
    """
    Z = sp.S.Zero
    for p in range(NMAX + 1):
        for q in range(NMAX + 1 - p):
            d = dim_su3(p, q)
            C2 = sp.Rational(p * p + p * q + q * q + 3 * p + 3 * q, 3)
            integrate_chi = sp.S.One if (p, q) == (0, 0) else sp.S.Zero
            Z += d * sp.exp(-t * C2 / 2) * integrate_chi
    return sp.simplify(Z)


def hk_re_tr_expectation_one_plaquette(t: sp.Expr, NMAX: int) -> sp.Expr:
    """⟨Re Tr U⟩_HK,1plaq(t) via Schur orthogonality.

    Re Tr U = (χ_{(1,0)} + χ_{(0,1)}) / 2.
    By Schur (eq. 4 of Block 02 note): only (1,0) and (0,1) contribute.
    Result:
        ⟨Re Tr U⟩ = (1/2) [d_{(0,1)} exp(-t C_2(0,1)/2) + d_{(1,0)} exp(-t C_2(1,0)/2)]
                  = (1/2) · 6 · exp(-2t/3) = 3 exp(-2t/3)
    """
    numerator = sp.S.Zero
    for p in range(NMAX + 1):
        for q in range(NMAX + 1 - p):
            d = dim_su3(p, q)
            C2 = sp.Rational(p * p + p * q + q * q + 3 * p + 3 * q, 3)
            # Numerator: ∫ ((χ_{(1,0)} + χ_{(0,1)})/2) · χ_{(p,q)} dU
            # = (1/2) [δ_{(p,q),(0,1)} + δ_{(p,q),(1,0)}]
            overlap = sp.Rational(1, 2) * (
                schur_overlap((1, 0), (p, q)) + schur_overlap((0, 1), (p, q))
            )
            numerator += d * sp.exp(-t * C2 / 2) * overlap
    return sp.simplify(numerator)


def main() -> None:
    print("=" * 72)
    print("Block 02 R2.A — Exact-Arithmetic Verification of Theorem (T2)")
    print("Companion: docs/BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md")
    print("=" * 72)
    print()

    checks: List[Tuple[str, bool, str]] = []
    t = sp.Symbol('t', positive=True)

    # K1 — partition function = 1 at all NMAX
    Z_at_5 = hk_partition_one_plaquette(t, NMAX=5)
    Z_at_10 = hk_partition_one_plaquette(t, NMAX=10)
    ok = (Z_at_5 == 1) and (Z_at_10 == 1)
    msg = f"Z_HK,1plaq(t) = {Z_at_5} at NMAX=5 and {Z_at_10} at NMAX=10 (expected 1)"
    checks.append(("K1 HK partition function = 1", ok, msg))

    # K2 — numerator at NMAX=5: 3 exp(-2t/3)
    num_5 = hk_re_tr_expectation_one_plaquette(t, NMAX=5)
    expected_num = 3 * sp.exp(-2 * t / 3)
    ok = sp.simplify(num_5 - expected_num) == 0
    msg = f"⟨Re Tr U⟩_numerator(t) = {num_5} at NMAX=5; expected 3 exp(-2t/3)"
    checks.append(("K2 numerator = 3 exp(-2t/3)", ok, msg))

    # K3 — closed form is exact at NMAX=2 already (only (1,0)+(0,1) contribute)
    num_2 = hk_re_tr_expectation_one_plaquette(t, NMAX=2)
    num_5 = hk_re_tr_expectation_one_plaquette(t, NMAX=5)
    num_10 = hk_re_tr_expectation_one_plaquette(t, NMAX=10)
    ok = (sp.simplify(num_2 - num_5) == 0) and (sp.simplify(num_5 - num_10) == 0)
    msg = f"NMAX=2 already matches NMAX=10 — Schur cuts off at fundamental rep"
    checks.append(("K3 exact in 2 characters (no NMAX trunc)", ok, msg))

    # K4 — full result ⟨(1/3) Re Tr U⟩ = exp(-2t/3)
    expectation = num_5 / sp.S(3)  # divide by N_c = 3
    expected = sp.exp(-2 * t / 3)
    ok = sp.simplify(expectation - expected) == 0
    msg = f"⟨P⟩_HK,1plaq(t) = {expectation} = {expected}"
    checks.append(("K4 ⟨P⟩_HK,1plaq(t) = exp(-2t/3)", ok, msg))

    # K5 — at Block 01's t(6) = 1, evaluate
    val_at_t1 = expectation.subs(t, 1)
    val_decimal = sp.N(val_at_t1, 15)
    expected_decimal = sp.N(sp.exp(sp.Rational(-2, 3)), 15)
    ok = sp.simplify(val_at_t1 - sp.exp(sp.Rational(-2, 3))) == 0
    msg = f"⟨P⟩_HK,1plaq(t=1) = {val_at_t1} = exp(-2/3) ≈ {val_decimal}"
    checks.append(("K5 ⟨P⟩_HK,1plaq(6) = exp(-2/3)", ok, msg))

    # K6 — comparison with Wilson V=1 PF result
    wilson_v1 = sp.Float("0.4225317396", 10)
    hk_at_t1 = sp.N(sp.exp(sp.Rational(-2, 3)), 10)
    diff = float(hk_at_t1) - float(wilson_v1)
    rel_diff = diff / float(wilson_v1) * 100
    ok = abs(diff - 0.0908853794) < 1e-6
    msg = (
        f"⟨P⟩_HK − ⟨P⟩_W = {hk_at_t1} − {wilson_v1} = {diff:.10f} "
        f"({rel_diff:.2f}% relative)"
    )
    checks.append(("K6 HK-vs-Wilson 1-plaq diff", ok, msg))

    # K7 — comparison with lattice MC comparator
    mc_compare = 0.5934
    epsilon_witness = 3.030e-4
    diff_to_mc = mc_compare - float(hk_at_t1)
    n_witness = diff_to_mc / epsilon_witness
    msg = (
        f"⟨P⟩_HK,1plaq(6) − ⟨P⟩_MC = {-diff_to_mc:.10f} "
        f"({n_witness:.0f}× ε_witness BELOW MC)"
    )
    checks.append(("K7 HK-vs-MC gap (comparator only)", True, msg))

    # K8 — Schur orthogonality structural check
    # Verify: ∫ χ_{(1,0)} · χ_{(0,1)} dU = 1, others 0
    pairs_to_check = [
        ((1, 0), (0, 1), 1),
        ((1, 0), (1, 0), 0),
        ((1, 0), (1, 1), 0),
        ((1, 0), (2, 0), 0),
        ((0, 1), (1, 0), 1),
    ]
    issues = []
    for l1, l2, expected_val in pairs_to_check:
        actual = schur_overlap(l1, l2)
        if actual != expected_val:
            issues.append(f"Schur({l1},{l2}) = {actual}, expected {expected_val}")
    ok = len(issues) == 0
    msg = "Schur orthogonality verified for fundamental + adjacent reps" if ok else "; ".join(issues)
    checks.append(("K8 Schur orthogonality structural", ok, msg))

    # Print results
    n_pass = sum(1 for _, ok, _ in checks if ok)
    n_total = len(checks)
    for name, ok, msg in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {msg}")
    print()
    print(f"SUMMARY: PASS={n_pass} FAIL={n_total - n_pass}")
    print()
    print("Theorem (T2) verified at SU(3) heat-kernel single-plaquette:")
    print("  ⟨P⟩_HK,1plaq(t) = exp(-2t/3) — exact in 2 characters")
    print("  ⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134171190")
    print()
    print("Comparators (NOT load-bearing):")
    print(f"  Wilson V=1 1-plaq:    0.4225317396  (V=1 PF ODE certified)")
    print(f"  HK 1-plaq (this):     0.5134171190  (Block 02, exp(-2/3))")
    print(f"  Lattice MC thermo:    ≈ 0.5934      (open famous problem)")
    print()
    print("Single-plaquette HK is closer to MC than Wilson 1-plaq is")
    print("(264× ε_witness below MC vs ~565× for Wilson 1-plaq).")
    print("Block 03 attacks thermodynamic ⟨P⟩_HK(6) under Casimir-diagonal")
    print("multi-plaquette structure.")


if __name__ == "__main__":
    main()
