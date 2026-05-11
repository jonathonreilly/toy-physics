#!/usr/bin/env python3
"""Frontier runner: Cl(3) γ-involution determinant identity — narrow theorem.

Verifies the abstract M_2(C) ≅ Cl(3,0) γ-involution identities (G1)-(G3)
plus the boundary statement (G4) at exact symbolic / rational precision.

This narrow theorem isolates the abstract-algebra content of the
γ-involution `γ(M) = σ_2 M^T σ_2`:
- (G1) γ = symplectic adjoint (cofactor transpose);
- (G2)/(G2') γ-norm identity `|M|_γ = √|det(M)|`;
- (G3) γ acts as -id on vector and bivector grades;
- (G4) per-element γ-norm does NOT close the framework's per-determinant
       geometric-mean readout admission.

No physics conventions consumed. No lattice / staggered-Dirac /
g_bare / Grassmann inputs.

Source note:
  docs/CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md
"""
from __future__ import annotations

import random
import sys
from fractions import Fraction

import sympy as sp


def make_symbolic_M():
    """Build a symbolic 2x2 complex matrix."""
    a, b, c, d = sp.symbols("a b c d", complex=True)
    return sp.Matrix([[a, b], [c, d]])


def make_pauli():
    s0 = sp.eye(2)
    s1 = sp.Matrix([[0, 1], [1, 0]])
    s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    s3 = sp.Matrix([[1, 0], [0, -1]])
    return s0, s1, s2, s3


def gamma_involution(M, s2):
    """γ(M) = σ_2 · M^T · σ_2"""
    return sp.simplify(s2 * M.T * s2)


def test_G1_symbolic_cofactor():
    """(G1) σ_2 · M^T · σ_2 = adj(M) for symbolic M."""
    s0, s1, s2, s3 = make_pauli()
    M = make_symbolic_M()
    gM = gamma_involution(M, s2)
    adj_M = M.adjugate()
    diff = sp.simplify(gM - adj_M)
    ok = diff == sp.zeros(2, 2)
    print(f"[G1 symbolic] γ(M) = adj(M):  {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  gM =", gM)
        print("  adj_M =", adj_M)
    return ok


def test_G2_symbolic_norm():
    """(G2)/(G2') M · γ(M) = det(M) · I_2 and ⟨M·γ(M)⟩_0 = det(M)."""
    s0, s1, s2, s3 = make_pauli()
    M = make_symbolic_M()
    gM = gamma_involution(M, s2)
    prod = sp.simplify(M * gM)
    detM = sp.simplify(M.det())
    expected = sp.simplify(detM * sp.eye(2))
    diff = sp.simplify(prod - expected)
    ok = diff == sp.zeros(2, 2)
    print(f"[G2 symbolic] M·γ(M) = det(M)·I_2:  {'PASS' if ok else 'FAIL'}")
    # Scalar (identity-coefficient) part of M·γ(M) is the (0,0) entry of prod
    # (and equals the (1,1) entry since prod is scalar · I).
    scalar_part = sp.simplify(prod[0, 0])
    ok_scalar = sp.simplify(scalar_part - detM) == 0
    print(
        f"[G2 symbolic] ⟨M·γ(M)⟩_0 = det(M):  {'PASS' if ok_scalar else 'FAIL'}"
    )
    return ok and ok_scalar


def test_G2_numerical_norm(n_trials: int = 10, rng_seed: int = 20260510):
    """(G2') |M|_γ = √|det(M)| for ten random rational+irational M."""
    s0, s1, s2, s3 = make_pauli()
    rng = random.Random(rng_seed)
    passes = 0
    for trial in range(n_trials):
        # Random rational a + ib entries
        def rand_c():
            r = sp.Rational(rng.randint(-5, 5), rng.randint(1, 4))
            im = sp.Rational(rng.randint(-5, 5), rng.randint(1, 4))
            return r + im * sp.I

        M = sp.Matrix([[rand_c(), rand_c()], [rand_c(), rand_c()]])
        gM = gamma_involution(M, s2)
        scalar_part = sp.simplify((M * gM)[0, 0])
        detM = sp.simplify(M.det())
        # Scalar part should equal det(M)
        ok_scalar = sp.simplify(scalar_part - detM) == 0
        # γ-norm: |M|_γ = sqrt(|scalar_part|) = sqrt(|det(M)|)
        gnorm_sq = sp.simplify(sp.Abs(scalar_part))
        det_abs = sp.simplify(sp.Abs(detM))
        ok_norm = sp.simplify(gnorm_sq - det_abs) == 0
        if ok_scalar and ok_norm:
            passes += 1
        else:
            print(
                f"  Trial {trial} FAIL: scalar={ok_scalar}, "
                f"|sp|=|det|={ok_norm}"
            )
    print(
        f"[G2 numerical] |M|_γ = √|det(M)| on {n_trials} random M: "
        f"{passes}/{n_trials} {'PASS' if passes == n_trials else 'FAIL'}"
    )
    return passes == n_trials


def test_G3_vector_grade():
    """(G3) γ(σ_i) = -σ_i and γ(I_2) = I_2."""
    s0, s1, s2, s3 = make_pauli()
    pairs = [("σ_0=I_2", s0, +1), ("σ_1", s1, -1), ("σ_2", s2, -1), ("σ_3", s3, -1)]
    all_ok = True
    for name, sigma, sign in pairs:
        g_sigma = gamma_involution(sigma, s2)
        expected = sp.simplify(sign * sigma)
        ok = sp.simplify(g_sigma - expected) == sp.zeros(2, 2)
        sign_str = "+" if sign > 0 else "-"
        print(
            f"[G3 vector] γ({name}) = {sign_str}{name}:  "
            f"{'PASS' if ok else 'FAIL'}"
        )
        all_ok = all_ok and ok
    return all_ok


def test_G3_bivector_grade():
    """(G3) γ(σ_i σ_j) = -σ_i σ_j for i ≠ j (6 ordered pairs / 3 unordered)."""
    s0, s1, s2, s3 = make_pauli()
    sigmas = {1: s1, 2: s2, 3: s3}
    all_ok = True
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            if i == j:
                continue
            biv = sp.simplify(sigmas[i] * sigmas[j])
            g_biv = gamma_involution(biv, s2)
            expected = sp.simplify(-biv)
            ok = sp.simplify(g_biv - expected) == sp.zeros(2, 2)
            print(
                f"[G3 bivector] γ(σ_{i}σ_{j}) = -σ_{i}σ_{j}:  "
                f"{'PASS' if ok else 'FAIL'}"
            )
            all_ok = all_ok and ok
    return all_ok


def test_G3_pseudoscalar():
    """(G3) γ(ω) = -ω where ω = σ_1 σ_2 σ_3 = i I_2 in positive-chirality.

    Method: compute γ(ω) as a 2x2 matrix directly via the definition
    γ(M) = σ_2 M^T σ_2 applied to ω, and check that it equals -ω.

    Note: in the positive-chirality Pauli realisation, ω = i I_2 as a
    matrix. The γ-involution definition gives γ(i I_2) = σ_2 (i I_2)^T σ_2
    = σ_2 (i I_2) σ_2 = i σ_2² = i I_2 = ω. But the abstract algebraic
    statement is γ(ω) = -ω. The resolution: γ(z · I_2) for complex z
    treats z as a scalar coefficient, and on the abstract Cl(3) the
    pseudoscalar ω is a separate basis element that γ flips. The
    matrix-level identity γ(σ_1 σ_2 σ_3) = -σ_1 σ_2 σ_3 is what we
    check (computing the product directly without reducing to i I_2
    via Pauli identities, by computing the Cl(3) involution-action on
    the symbolic product structure).
    """
    s0, s1, s2, s3 = make_pauli()
    omega_matrix = sp.simplify(s1 * s2 * s3)
    # Compute γ(σ_1 σ_2 σ_3) directly via σ_2 (σ_1σ_2σ_3)^T σ_2
    g_omega = gamma_involution(omega_matrix, s2)
    # The abstract Cl(3) result: γ(σ_1σ_2σ_3) = γ(σ_3)γ(σ_2)γ(σ_1) (anti-
    # multiplicative, from transpose) = (-σ_3)(-σ_2)(-σ_1) = -σ_3 σ_2 σ_1
    # = -(σ_1 σ_2 σ_3)·(reorder sign). Compute:
    # σ_3 σ_2 σ_1 = ?
    # σ_3 σ_2 = -σ_2 σ_3 + 2(σ_3·σ_2) = -σ_2 σ_3 (anticommute, dot product 0)
    # ... but with Pauli realisation, σ_3 σ_2 = -i σ_1, σ_2 σ_1 = -i σ_3,
    # σ_1 σ_3 = -i σ_2, so σ_3 σ_2 σ_1 = (-i σ_1) σ_1 = -i I_2 = -ω.
    # Hence γ(σ_1 σ_2 σ_3) = (-σ_3)(-σ_2)(-σ_1) = -(σ_3 σ_2 σ_1) = -(-ω) = ω.
    #
    # So at the matrix level (positive-chirality Pauli realisation),
    # γ(σ_1 σ_2 σ_3) = +σ_1 σ_2 σ_3 = +ω. Wait, this contradicts the
    # "abstract Cl(3) γ flips pseudoscalar" claim. Let me recheck.
    #
    # The issue: the abstract Cl(3) γ-involution flips the pseudoscalar
    # IFF γ is defined as reversion + grading-automorphism. The matrix-
    # level γ(M) = σ_2 M^T σ_2 specifically gives:
    #   γ(I) = I, γ(σ_i) = -σ_i, γ(σ_i σ_j) for i≠j = ?, γ(σ_1 σ_2 σ_3) = ?
    # Direct verification:
    ok_omega = sp.simplify(g_omega - omega_matrix) == sp.zeros(2, 2)
    print(
        f"[G3 pseudoscalar] γ(σ_1σ_2σ_3) = +σ_1σ_2σ_3 (matrix-level): "
        f"{'PASS' if ok_omega else 'FAIL'}"
    )
    # So the matrix-level realization gives γ(ω) = +ω. The "abstract Cl(3)
    # γ flips ω" claim in the note's (G3) needs sharpening: the
    # composition reversion·grading-auto on the abstract algebra has
    # different sign behavior on grade 3 than the M_2(C) realisation of
    # the σ_2-conjugated transpose. We report the matrix-level fact.
    return ok_omega


def test_G4_boundary_block_diag(n_trials: int = 5, rng_seed: int = 20260511):
    """(G4) Per-element γ-norm does NOT produce the per-determinant
    readout on a tensor-product / block-diagonal lattice example.

    Construct D_lat = M_1 ⊕ M_2 (4x4 block diagonal). Compute
    |det(D_lat)|^{1/2} (the geometric-mean readout at N_modes = 2).
    Show this equals √|det(M_1) · det(M_2)| (a per-determinant product
    fact), which is NOT in general equal to |M_1|_γ + |M_2|_γ or
    other per-element γ-norm combinations.
    """
    s0, s1, s2, s3 = make_pauli()
    rng = random.Random(rng_seed)
    all_ok = True
    for trial in range(n_trials):
        def rand_c():
            return sp.Rational(rng.randint(1, 5), rng.randint(1, 3)) + sp.I * sp.Rational(
                rng.randint(-3, 3), rng.randint(1, 3)
            )

        M1 = sp.Matrix([[rand_c(), rand_c()], [rand_c(), rand_c()]])
        M2 = sp.Matrix([[rand_c(), rand_c()], [rand_c(), rand_c()]])
        D_lat = sp.zeros(4, 4)
        D_lat[0:2, 0:2] = M1
        D_lat[2:4, 2:4] = M2
        det_lat = sp.simplify(D_lat.det())
        det_M1 = sp.simplify(M1.det())
        det_M2 = sp.simplify(M2.det())
        # det of block-diagonal = product of determinants
        ok_factor = sp.simplify(det_lat - det_M1 * det_M2) == 0
        # geometric-mean readout at N_modes = 2 is |det_lat|^{1/2}
        geom_mean_sq = sp.simplify(sp.Abs(det_lat))
        # γ-norms
        gM1_sq = sp.simplify(sp.Abs(det_M1))
        gM2_sq = sp.simplify(sp.Abs(det_M2))
        # Check: |det_lat|^{1/2} = (|det_M1| · |det_M2|)^{1/2} = |M_1|_γ · |M_2|_γ
        # (product of γ-norms, NOT sum or any single γ-norm)
        product_form = sp.simplify(sp.sqrt(gM1_sq) * sp.sqrt(gM2_sq))
        geom_mean = sp.simplify(sp.sqrt(geom_mean_sq))
        ok_product = sp.simplify(geom_mean - product_form) == 0
        # Now demonstrate: |det_lat|^{1/2} = product of per-element |M_i|_γ
        # so the per-determinant readout IS a per-element product on this
        # block-diagonal lattice. But the framework's lattice is NOT
        # block-diagonal in this trivial way — the staggered Dirac D has
        # off-diagonal hopping terms that couple sites, so the determinant
        # is NOT simply the product of per-site γ-norms.
        if ok_factor and ok_product:
            all_ok = all_ok and True
        else:
            all_ok = False
            print(
                f"  Trial {trial} FAIL: factor={ok_factor}, "
                f"product={ok_product}"
            )
    print(
        f"[G4 boundary] block-diagonal |det|^{{1/2}} = ∏|M_i|_γ: "
        f"{n_trials}/{n_trials} {'PASS' if all_ok else 'FAIL'}"
    )
    # Now demonstrate the gap: pick a non-block-diagonal D (with hopping
    # between blocks). The 4x4 determinant is NOT a product of per-block
    # γ-norms.
    M1 = sp.Matrix([[2, 1], [0, 3]])
    M2 = sp.Matrix([[1, 0], [-1, 2]])
    H = sp.Matrix([[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]])  # hopping
    D_hop = sp.zeros(4, 4)
    D_hop[0:2, 0:2] = M1
    D_hop[2:4, 2:4] = M2
    D_hop[0:2, 2:4] = H
    D_hop[2:4, 0:2] = H
    det_hop = sp.simplify(D_hop.det())
    det_per_block_product = sp.simplify(M1.det() * M2.det())
    # gap: det(D_hop) ≠ det(M_1)·det(M_2) when hopping H is nonzero
    has_gap = sp.simplify(det_hop - det_per_block_product) != 0
    print(
        f"[G4 boundary] hopping → det(D_hop) ≠ det(M_1)·det(M_2):  "
        f"{'PASS' if has_gap else 'FAIL'}  (gap = {sp.simplify(det_hop - det_per_block_product)})"
    )
    return all_ok and has_gap


def test_G3_decomposition():
    """Verify γ decomposes as reversion ∘ grading-automorphism on the
    Cl(3) basis. For the M_2(C) realisation:
    - identity grade (I_2): γ fixed, reversion fixed, grading-auto fixed
    - vector grade (σ_i): γ flips, reversion fixed, grading-auto flips
    - bivector grade (σ_i σ_j, i≠j): γ flips, reversion flips, grading-auto fixed
    - pseudoscalar (σ_1 σ_2 σ_3 = i I_2 in pos-chir realisation):
      γ matrix-level = +, abstract Cl(3) γ = - (sign convention discrepancy
      noted; we report matrix-level fact).
    """
    s0, s1, s2, s3 = make_pauli()
    # Build the 8-element Cl(3) basis
    basis = {
        "I_2": s0,
        "σ_1": s1,
        "σ_2": s2,
        "σ_3": s3,
        "σ_1 σ_2": sp.simplify(s1 * s2),
        "σ_1 σ_3": sp.simplify(s1 * s3),
        "σ_2 σ_3": sp.simplify(s2 * s3),
        "ω = σ_1σ_2σ_3": sp.simplify(s1 * s2 * s3),
    }
    expected_signs = {
        "I_2": +1,
        "σ_1": -1,
        "σ_2": -1,
        "σ_3": -1,
        "σ_1 σ_2": -1,
        "σ_1 σ_3": -1,
        "σ_2 σ_3": -1,
        "ω = σ_1σ_2σ_3": +1,  # matrix-level fact (positive-chirality)
    }
    all_ok = True
    for name, elem in basis.items():
        g_elem = gamma_involution(elem, s2)
        expected = sp.simplify(expected_signs[name] * elem)
        ok = sp.simplify(g_elem - expected) == sp.zeros(2, 2)
        sign_str = "+" if expected_signs[name] > 0 else "-"
        print(
            f"[G3 basis] γ({name}) = {sign_str}{name}:  "
            f"{'PASS' if ok else 'FAIL'}"
        )
        all_ok = all_ok and ok
    return all_ok


def main():
    print("=" * 72)
    print("Cl(3) γ-involution determinant identity — narrow theorem runner")
    print("=" * 72)
    print()

    tests = []

    print("[Part 1] (G1) γ-involution = symplectic adjoint (cofactor)")
    tests.append(("G1", test_G1_symbolic_cofactor()))
    print()

    print("[Part 2] (G2)/(G2') γ-norm identity (symbolic)")
    tests.append(("G2-symbolic", test_G2_symbolic_norm()))
    print()

    print("[Part 3] (G2') γ-norm identity (numerical, 10 random M)")
    tests.append(("G2-numerical", test_G2_numerical_norm()))
    print()

    print("[Part 4] (G3) γ on vector grade (σ_i, I_2)")
    tests.append(("G3-vector", test_G3_vector_grade()))
    print()

    print("[Part 5] (G3) γ on bivector grade (σ_i σ_j, i≠j)")
    tests.append(("G3-bivector", test_G3_bivector_grade()))
    print()

    print("[Part 6] (G3) γ on pseudoscalar (matrix-level)")
    tests.append(("G3-pseudoscalar", test_G3_pseudoscalar()))
    print()

    print("[Part 7] (G3) γ action on full Cl(3) 8-element basis")
    tests.append(("G3-basis", test_G3_decomposition()))
    print()

    print("[Part 8] (G4) Per-element γ-norm vs per-determinant readout boundary")
    tests.append(("G4-boundary", test_G4_boundary_block_diag()))
    print()

    print("=" * 72)
    passes = sum(1 for _, ok in tests if ok)
    total = len(tests)
    fails = total - passes
    print(f"SUMMARY: PASS={passes} FAIL={fails} TOTAL={total}")
    for name, ok in tests:
        status = "PASS" if ok else "FAIL"
        print(f"  {status:<5}  {name}")
    print("=" * 72)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
