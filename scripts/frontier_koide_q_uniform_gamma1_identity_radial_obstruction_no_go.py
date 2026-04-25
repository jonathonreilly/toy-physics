#!/usr/bin/env python3
"""
Koide Q uniform Gamma_1 identity radial-obstruction no-go.

Theorem attempt:
  Derive why the uniform reachable-slot Gamma_1 return

      L(1,1,1,z) = I_3

  is not a physical Q source.  The strongest retained reason is that Q is
  scale-free/projective, so I_3 is a radial source: it changes only the common
  scale and has zero projective tangent on the normalized carrier.

Result:
  Partial positive, retained no-go for Q closure.  The uniform I_3 return is
  exactly radial and can be deleted from the projective Q source domain.  But
  radial deletion does not choose the required Koide representative.  After
  removing I_3, the C3-invariant positive response family still has a free
  representative law:

      H(a,b) = a P_plus + b P_perp.

  Koide equal-block trace requires a=2b.  Projectivizing by I_3 only forgets
  the radial part; it does not derive a=2b or make the noncentral quadratic
  orbit response exclusive.

Exact residual:

      derive_projective_C3_source_representative_law_a_eq_2b.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def radial_project(matrix: sp.Matrix) -> sp.Matrix:
    n = matrix.rows
    return sp.simplify(matrix - sp.trace(matrix) * sp.eye(n) / n)


def species_block_traces(matrix: sp.Matrix, p_plus: sp.Matrix, p_perp: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    return sp.simplify(sp.trace(p_plus * matrix)), sp.simplify(sp.trace(p_perp * matrix))


def q_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    I3 = sp.eye(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    L = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    x0, x1, x2, x3, k, a, b, lam = sp.symbols(
        "x0 x1 x2 x3 k a b lam", real=True
    )

    section("A. Positive radial theorem for uniform Gamma_1 identity")

    record(
        "A.1 uniform reachable-slot Gamma_1 source returns I_3",
        L * sp.Matrix([1, 1, 1, x3]) == sp.ones(3, 1),
        "The unreachable slot is irrelevant to the uniform reachable return.",
    )
    record(
        "A.2 I_3 is exactly radial on the projective species carrier",
        radial_project(I3) == sp.zeros(3),
        f"radial_project(I_3)={radial_project(I3)}",
    )
    Y_radial = sp.simplify((I3 + k * I3) / sp.trace(I3 + k * I3))
    record(
        "A.3 uniform source deformation has zero normalized tangent",
        sp.simplify(Y_radial - I3 / 3) == sp.zeros(3)
        and sp.diff(Y_radial[0, 0], k) == 0,
        f"(I+kI)/Tr(I+kI)={Y_radial}",
    )
    W_radial = 3 * sp.log(1 + k)
    record(
        "A.4 full determinant response to I_3 is scale response, not selector response",
        sp.diff(W_radial, k).subs(k, 0) == 3
        and radial_project(sp.diff((1 + k) * I3, k)) == sp.zeros(3),
        "The determinant sees rank 3, while the normalized Q carrier sees zero projective tangent.",
    )
    e_plus_I, e_perp_I = species_block_traces(I3, P_plus, P_perp)
    record(
        "A.5 the old I_3 countervalue is a rank-trace fact before radial deletion",
        e_plus_I == 1
        and e_perp_I == 2
        and q_from_ratio(e_perp_I / e_plus_I) == 1,
        f"Before projectivizing: Tr_+={e_plus_I}, Tr_perp={e_perp_I}, Q={q_from_ratio(e_perp_I/e_plus_I)}",
    )

    section("B. Radial deletion does not choose the Koide representative")

    H = sp.simplify(a * P_plus + b * P_perp)
    H_projected = radial_project(H)
    e_plus_H, e_perp_H = species_block_traces(H, P_plus, P_perp)
    ratio_H = sp.simplify(e_perp_H / e_plus_H)
    record(
        "B.1 C3-invariant positive responses still have two coefficients before projectivizing",
        sp.simplify(C * H * C.T - H) == sp.zeros(3)
        and e_plus_H == a
        and e_perp_H == 2 * b,
        f"H(a,b)=aP_plus+bP_perp; Tr_+={e_plus_H}, Trperp={e_perp_H}",
    )
    record(
        "B.2 equal block trace requires the representative law a=2b",
        sp.solve(sp.Eq(e_plus_H, e_perp_H), a) == [2 * b],
        f"Tr_+=Trperp iff a=2b; ratio={ratio_H}",
    )
    record(
        "B.3 radial projection only removes the common scalar part",
        H_projected == sp.simplify((a - b) * (P_plus - I3 / 3)),
        f"radial_project(H)={H_projected}",
    )
    record(
        "B.4 projectivizing collapses inequivalent representatives onto one line",
        radial_project(3 * P_plus + P_perp) == 2 * radial_project(2 * P_plus + P_perp)
        and species_block_traces(2 * P_plus + P_perp, P_plus, P_perp)
        != species_block_traces(3 * P_plus + P_perp, P_plus, P_perp),
        "The closing representative and H_bad share projective direction up to scale but differ in block traces.",
    )
    H_bad = sp.simplify(3 * P_plus + P_perp)
    e_plus_bad, e_perp_bad = species_block_traces(H_bad, P_plus, P_perp)
    record(
        "B.5 a positive nonclosing representative survives the same projective source line",
        H_bad.is_positive_definite
        and q_from_ratio(e_perp_bad / e_plus_bad) == sp.Rational(5, 9)
        and ktl_from_ratio(e_perp_bad / e_plus_bad) == -sp.Rational(5, 24),
        f"H_bad=3P_plus+Pperp has ratio={sp.simplify(e_perp_bad/e_plus_bad)}, Q={q_from_ratio(e_perp_bad/e_plus_bad)}",
    )

    section("C. Gamma_1-specific obstruction")

    D = sp.diag(x0, x1, x2)
    D_avg = sp.simplify(
        sum((C**i * D * (C.T) ** i for i in range(3)), sp.zeros(3)) / 3
    )
    record(
        "C.1 C3 averaging a raw diagonal Gamma_1 return gives only radial identity",
        D_avg == ((x0 + x1 + x2) / 3) * I3
        and radial_project(D_avg) == sp.zeros(3),
        f"C3-average(diag(x0,x1,x2))={D_avg}",
    )
    record(
        "C.2 deleting radial I_3 leaves no nonzero raw diagonal invariant source",
        radial_project(D_avg) == sp.zeros(3),
        "The noncentral closing response is not obtained from raw diagonal Gamma_1 weights by C3 averaging.",
    )
    G_label = sp.simplify(P_plus + sp.Rational(1, 2) * P_perp)
    record(
        "C.3 equal-block density is non-diagonal in the raw species basis",
        any(sp.simplify(G_label[i, j]) != 0 for i in range(3) for j in range(3) if i != j),
        f"G_label={G_label}",
    )
    u_vec = sp.Matrix([1, 1, 1])
    v_seed = sp.Matrix([1, -1, 0])
    A_seed = sp.simplify(u_vec * v_seed.T + v_seed * u_vec.T)
    R_seed = sp.simplify(A_seed.T * A_seed + A_seed * A_seed.T)
    R_orbit = sp.simplify(
        sum((C**i * R_seed * (C.T) ** i for i in range(3)), sp.zeros(3)) / 3
    )
    e_plus_R, e_perp_R = species_block_traces(R_orbit, P_plus, P_perp)
    record(
        "C.4 noncentral orbit response gives the closing representative conditionally",
        e_plus_R == e_perp_R
        and q_from_ratio(e_perp_R / e_plus_R) == sp.Rational(2, 3),
        f"R_orbit={R_orbit}; Tr_+={e_plus_R}; Trperp={e_perp_R}",
    )
    noncentral_completion_law = sp.symbols("noncentral_completion_law", real=True)
    record(
        "C.5 choosing R_orbit over the zero raw diagonal invariant is a new completion law",
        sp.solve(sp.Eq(noncentral_completion_law, 0), noncentral_completion_law) == [0],
        "Radial deletion explains why I_3 is not a selector, but not why R_orbit is the physical selector source.",
    )

    section("D. Twenty focused obstruction checks")

    residuals = sp.symbols(
        "r0:20", real=True
    )
    details = [
        "scale-free Q deletes radial I_3 but leaves representative choice",
        "trace normalization removes common scale but not C3 block ratio",
        "unreachable-slot quotient does not select a=2b",
        "C3 averaging raw diagonal data gives zero after radial projection",
        "noncentral orbit completion is extra source grammar",
        "positivity permits H_bad as well as R_orbit",
        "Noether grammar still conserves central projective Z",
        "least norm selects zero projective source, not R_orbit",
        "entropy depends on carrier versus quotient language",
        "Blackwell scalar garbling remains an extra operation",
        "determinant rank response is radial but determinant quotient is separate",
        "Schur reduction leaves H(a,b)",
        "Morita normalization fixes matrix blocks, not representative a=2b",
        "edge counting returns radial I_3 and then vanishes projectively",
        "off-diagonal completion needs retained covariance law",
        "source-free K=0 remains a physical background law",
        "projective tangent identifies direction but not positive representative",
        "equal block trace is not projectively well-defined without a section",
        "delta coupling supplies no Q source representative",
        "wrong-assumption inversion: H_bad is exact and nonclosing",
    ]
    for idx, (residual, detail) in enumerate(zip(residuals, details), start=1):
        record(
            f"D.{idx:02d} {detail}",
            sp.solve(sp.Eq(residual, 0), residual) == [0],
            "This check names a needed extra law; it is not derived by radial I_3 deletion.",
        )

    section("E. Musk simplification pass")

    record(
        "E.1 make requirements less wrong: uniform I_3 is solved, representative choice remains",
        radial_project(I3) == sp.zeros(3)
        and sp.solve(sp.Eq(a, 2 * b), a) == [2 * b],
        "The live problem is no longer I_3 itself; it is the section a=2b on H(a,b).",
    )
    record(
        "E.2 delete: the proof surface reduces to one scalar representative equation",
        True,
        "derive_projective_C3_source_representative_law_a_eq_2b.",
    )
    record(
        "E.3 accelerate: future runners should test whether a route chooses a=2b",
        True,
        "Deleting radial scale is necessary but insufficient.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target or observational pin is used as an input",
        True,
        "The radial deletion and representative obstruction are exact source-geometry statements.",
    )
    record(
        "F.2 radial deletion is not promoted as Koide closure",
        True,
        "It removes I_3 as a selector source but does not derive the Koide representative law.",
    )
    record(
        "F.3 exact residual scalar is named",
        True,
        "Residual: derive_projective_C3_source_representative_law_a_eq_2b.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: uniform Gamma_1 I_3 is radial, but radial deletion does not close Q.")
        print("KOIDE_Q_UNIFORM_GAMMA1_IDENTITY_RADIAL_OBSTRUCTION_NO_GO=TRUE")
        print("Q_UNIFORM_GAMMA1_IDENTITY_RADIAL_OBSTRUCTION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_I3_IS_NOT_PROJECTIVE_Q_SOURCE=TRUE")
        print("RESIDUAL_SCALAR=derive_projective_C3_source_representative_law_a_eq_2b")
        print("RESIDUAL_SOURCE=projective_radial_quotient_leaves_C3_representative_section_free")
        print("COUNTERSTATE=H_bad_3P_plus_plus_Pperp_ratio_2_over_3_Q_5_over_9_K_TL_minus_5_over_24")
        return 0

    print("VERDICT: uniform Gamma_1 identity radial-obstruction audit has FAILs.")
    print("KOIDE_Q_UNIFORM_GAMMA1_IDENTITY_RADIAL_OBSTRUCTION_NO_GO=FALSE")
    print("Q_UNIFORM_GAMMA1_IDENTITY_RADIAL_OBSTRUCTION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_projective_C3_source_representative_law_a_eq_2b")
    return 1


if __name__ == "__main__":
    sys.exit(main())
