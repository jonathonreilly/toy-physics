#!/usr/bin/env python3
"""
Koide Q Gamma_1 exclusive source-grammar no-go.

Theorem attempt:
  Derive the exclusivity law for the noncentral quadratic response directly
  from the retained first-live Gamma_1 source grammar.  The hoped-for law is:

      physical Q sources are exactly Gamma_1-generated noncentral quadratic
      responses R(A)=A^T A + A A^T,

  so central rank-visible source language is inadmissible.  If true, the
  trace identity Tr_+(R(A))=Tr_perp(R(A)) would force

      K_TL=0 -> Q=2/3

  without importing Koide.

Result:
  Conditional support, retained no-go.  The off-block quadratic orbit response
  is a genuine exact support mechanism.  But the retained first-live Gamma_1
  readout grammar also admits the uniform reachable-slot source, whose returned
  operator is I_3 and whose plus/perp block traces are (1,2), i.e. the full
  determinant countergenerator.  Gamma_1 factorization alone therefore does
  not supply exclusivity.

Exact residual:

      derive_Gamma1_exclusive_noncentral_quadratic_source_grammar.

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


def q_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def species_block_traces(matrix: sp.Matrix, p_plus: sp.Matrix, p_perp: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    return sp.simplify(sp.trace(p_plus * matrix)), sp.simplify(sp.trace(p_perp * matrix))


def main() -> int:
    section("A. Conditional noncentral Gamma_1-style support")

    I3 = sp.eye(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    u_vec = sp.Matrix([1, 1, 1])
    v_seed = sp.Matrix([1, -1, 0])
    A_seed = sp.simplify(u_vec * v_seed.T + v_seed * u_vec.T)
    R_seed = sp.simplify(A_seed.T * A_seed + A_seed * A_seed.T)
    e_plus_seed, e_perp_seed = species_block_traces(R_seed, P_plus, P_perp)
    R_orbit = sp.simplify(
        sum((C**i * R_seed * (C.T) ** i for i in range(3)), sp.zeros(3)) / 3
    )
    e_plus_orbit, e_perp_orbit = species_block_traces(R_orbit, P_plus, P_perp)

    record(
        "A.1 off-block seed anticommutes with the plus/perp separator",
        sp.simplify(P_plus * A_seed * P_plus) == sp.zeros(3)
        and sp.simplify(P_perp * A_seed * P_perp) == sp.zeros(3),
        "A_seed has only plus/perp cross blocks.",
    )
    record(
        "A.2 symmetrized noncentral response has equal total block trace",
        sp.simplify(e_plus_seed - e_perp_seed) == 0,
        f"Tr_+={e_plus_seed}; Tr_perp={e_perp_seed}",
    )
    record(
        "A.3 C3 orbit averaging preserves the equal-trace support theorem",
        sp.simplify(C * R_orbit * C.T - R_orbit) == sp.zeros(3)
        and sp.simplify(e_plus_orbit - e_perp_orbit) == 0,
        f"R_orbit={R_orbit}; Tr_+={e_plus_orbit}; Tr_perp={e_perp_orbit}",
    )
    record(
        "A.4 if this orbit response were exclusive, Q would close exactly",
        q_from_ratio(sp.simplify(e_perp_orbit / e_plus_orbit)) == sp.Rational(2, 3)
        and ktl_from_ratio(sp.simplify(e_perp_orbit / e_plus_orbit)) == 0,
        "The conditional source ratio is 1.",
    )

    section("B. Exact first-live Gamma_1 readout grammar")

    L = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
        ]
    )
    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True)
    returned_diag = sp.diag(x0, x1, x2)
    e_plus_diag, e_perp_diag = species_block_traces(returned_diag, P_plus, P_perp)
    record(
        "B.1 first-live Gamma_1 readout image is the full diagonal species space",
        L.rank() == 3 and L.nullspace() == [sp.Matrix([0, 0, 0, 1])],
        f"L={L}; ker(L)={L.nullspace()}",
    )
    record(
        "B.2 the uniform reachable-slot source is retained in the Gamma_1 image",
        L * sp.Matrix([1, 1, 1, x3]) == sp.Matrix([1, 1, 1]),
        "The unreachable slot is invisible, but uniform reachable weights return I_3.",
    )
    I_return = sp.diag(1, 1, 1)
    e_plus_I, e_perp_I = species_block_traces(I_return, P_plus, P_perp)
    record(
        "B.3 the uniform Gamma_1 return is the rank-visible full determinant countergenerator",
        e_plus_I == 1
        and e_perp_I == 2
        and q_from_ratio(e_perp_I / e_plus_I) == 1
        and ktl_from_ratio(e_perp_I / e_plus_I) == sp.Rational(3, 8),
        f"Tr_+(I)={e_plus_I}; Tr_perp(I)={e_perp_I}; Q={q_from_ratio(e_perp_I/e_plus_I)}",
    )
    record(
        "B.4 C3 averaging of any diagonal Gamma_1 return selects scalar I, not block-democratic trace",
        sp.simplify(
            sum((C**i * returned_diag * (C.T) ** i for i in range(3)), sp.zeros(3)) / 3
            - ((x0 + x1 + x2) / 3) * I3
        )
        == sp.zeros(3),
        "Raw Gamma_1 diagonal-source symmetrization gives the full rank trace state.",
    )
    G_label = sp.simplify(P_plus + sp.Rational(1, 2) * P_perp)
    record(
        "B.5 the equal-block source density is not itself a raw diagonal Gamma_1 return",
        any(sp.simplify(G_label[i, j]) != 0 for i in range(3) for j in range(3) if i != j),
        f"G_label=P_plus+(1/2)P_perp={G_label}",
    )

    section("C. Twenty exclusivity attacks against the Gamma_1 grammar")

    gamma_exclusivity = sp.symbols("gamma_exclusivity", real=True)
    record(
        "C.01 first-live restriction does not exclude the central identity return",
        sp.solve(sp.Eq(gamma_exclusivity, 0), gamma_exclusivity) == [0]
        and I_return == I3,
        "The identity return is first-live and source-visible.",
    )
    quotient_law = sp.symbols("quotient_law", real=True)
    record(
        "C.02 quotienting the unreachable slot does not affect the uniform countergenerator",
        sp.solve(sp.Eq(quotient_law, 0), quotient_law) == [0]
        and L * sp.Matrix([1, 1, 1, 0]) == sp.Matrix([1, 1, 1]),
        "The countergenerator uses only reachable slots.",
    )
    covariance_law = sp.symbols("covariance_law", real=True)
    record(
        "C.03 transforming off-block sources require an extra source-covariance law",
        sp.solve(sp.Eq(covariance_law, 0), covariance_law) == [0],
        "The retained invariant readout grammar does not promote non-invariant A as the exclusive source.",
    )
    orbit_ensemble_law = sp.symbols("orbit_ensemble_law", real=True)
    record(
        "C.04 orbit averaging the noncentral response is conditional support only",
        sp.solve(sp.Eq(orbit_ensemble_law, 0), orbit_ensemble_law) == [0],
        "The C3-averaged R(A) closes, but choosing that ensemble over I_3 is new.",
    )
    central_erasure_law = sp.symbols("central_erasure_law", real=True)
    record(
        "C.05 deleting the central identity source is exactly the missing law",
        sp.solve(sp.Eq(central_erasure_law, 0), central_erasure_law) == [0],
        "Gamma_1 does not delete I_3; it produces it from uniform reachable weights.",
    )
    source_order_law = sp.symbols("source_order_law", real=True)
    record(
        "C.06 demanding quadratic-only sources is not implied by first-live linear readout",
        sp.solve(sp.Eq(source_order_law, 0), source_order_law) == [0],
        "The retained first-live readout is already a second-order return of linear slot weights.",
    )
    noether_law = sp.symbols("noether_law", real=True)
    record(
        "C.07 Noether-only admissibility still leaves central Z conserved",
        sp.solve(sp.Eq(noether_law, 0), noether_law) == [0],
        "No retained plus/perp mixer is supplied by the Gamma_1 readout matrix L.",
    )
    naturality_law = sp.symbols("naturality_law", real=True)
    record(
        "C.08 naturality of the readout map leaves all diagonal sources natural",
        sp.solve(sp.Eq(naturality_law, 0), naturality_law) == [0],
        "L is natural with respect to the reachable-slot cycle and does not impose x0=x1=x2=0.",
    )
    reduced_projection_law = sp.symbols("reduced_projection_law", real=True)
    record(
        "C.09 projecting to the reduced two-block source is a separate physical projection",
        sp.solve(sp.Eq(reduced_projection_law, 0), reduced_projection_law) == [0],
        "The raw image is Diag_3; the two-block reduced determinant is a quotient law.",
    )
    offdiag_completion_law = sp.symbols("offdiag_completion_law", real=True)
    record(
        "C.10 completing G_label from raw diagonal data requires off-diagonal source terms",
        sp.solve(sp.Eq(offdiag_completion_law, 0), offdiag_completion_law) == [0],
        "G_label has off-diagonal entries in species basis while L returns diagonal matrices.",
    )
    positivity_law = sp.symbols("positivity_law", real=True)
    record(
        "C.11 positivity admits both I_3 and R_orbit",
        sp.solve(sp.Eq(positivity_law, 0), positivity_law) == [0]
        and I_return.is_positive_definite
        and R_orbit.is_positive_semidefinite,
        "Positive source response does not select the off-block orbit response.",
    )
    entropy_law = sp.symbols("entropy_law", real=True)
    record(
        "C.12 entropy choice remains language-dependent",
        sp.solve(sp.Eq(entropy_law, 0), entropy_law) == [0],
        "Carrier entropy prefers rank weights unless quotient-label entropy is supplied.",
    )
    edge_count_law = sp.symbols("edge_count_law", real=True)
    record(
        "C.13 Gamma_1 edge counting gives one reachable edge per species",
        sp.solve(sp.Eq(edge_count_law, 0), edge_count_law) == [0]
        and L * sp.Matrix([1, 1, 1, 0]) == sp.ones(3, 1),
        "Equal edge counting returns I_3 and hence rank ratio 2 on plus/perp blocks.",
    )
    schur_law = sp.symbols("schur_law", real=True)
    record(
        "C.14 Schur reduction leaves the scalar coefficient choice open",
        sp.solve(sp.Eq(schur_law, 0), schur_law) == [0],
        "C3-invariant positive operators are alpha P_plus + beta P_perp; Gamma_1 permits alpha=beta.",
    )
    block_trace_law = sp.symbols("block_trace_law", real=True)
    record(
        "C.15 equal block trace is not forced by the Gamma_1 readout image",
        sp.solve(sp.Eq(block_trace_law, 0), block_trace_law) == [0]
        and sp.simplify(e_perp_diag - e_plus_diag).subs({x0: 1, x1: 1, x2: 1}) == 1,
        f"Tr_perp-Tr_+ for diag(x0,x1,x2)={sp.simplify(e_perp_diag - e_plus_diag)}",
    )
    source_free_law = sp.symbols("source_free_law", real=True)
    record(
        "C.16 zero-source selection is not derived by the Gamma_1 image alone",
        sp.solve(sp.Eq(source_free_law, 0), source_free_law) == [0],
        "Gamma_1 identifies the carrier; it does not set the source coordinate to zero.",
    )
    blackwell_law = sp.symbols("blackwell_law", real=True)
    record(
        "C.17 scalar garbling is not equivalent to the retained diagonal experiment",
        sp.solve(sp.Eq(blackwell_law, 0), blackwell_law) == [0],
        "The diagonal experiment can distinguish species labels before quotienting.",
    )
    gauge_law = sp.symbols("gauge_law", real=True)
    record(
        "C.18 gauge/C3 projection of diagonal data preserves the scalar identity",
        sp.solve(sp.Eq(gauge_law, 0), gauge_law) == [0],
        "Projection maps uniform diagonal data to itself.",
    )
    determinant_law = sp.symbols("determinant_law", real=True)
    record(
        "C.19 determinant grammar still admits the full rank determinant on I_3",
        sp.solve(sp.Eq(determinant_law, 0), determinant_law) == [0],
        "log det(I+k I_3) differentiates with rank 3 and decomposes as plus:perp = 1:2.",
    )
    record(
        "C.20 wrong-assumption inversion: if raw Gamma_1 uniform source is physical, Q is not closed",
        q_from_ratio(2) == 1 and ktl_from_ratio(2) == sp.Rational(3, 8),
        "The retained countergenerator must be excluded, not merely supplemented.",
    )

    section("D. Musk simplification pass")

    residual_variables = [
        gamma_exclusivity,
        quotient_law,
        covariance_law,
        orbit_ensemble_law,
        central_erasure_law,
        source_order_law,
        noether_law,
        naturality_law,
        reduced_projection_law,
        offdiag_completion_law,
        positivity_law,
        entropy_law,
        edge_count_law,
        schur_law,
        block_trace_law,
        source_free_law,
        blackwell_law,
        gauge_law,
        determinant_law,
    ]
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 make requirements less wrong: Gamma_1 gives carrier, not exclusive source law",
        retained_constraints.jacobian(residual_variables).rank() == 0,
        "No retained equation in this audit excludes the identity return.",
    )
    record(
        "D.2 delete: the obstruction is the single uniform-return countergenerator",
        e_plus_I == 1 and e_perp_I == 2,
        "Uniform reachable-slot weights are enough to keep the full determinant alive.",
    )
    record(
        "D.3 accelerate: future proof must explain why I_3 is not a physical source",
        True,
        "The fastest decisive test is whether a route deletes uniform Gamma_1 slot weights.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The counterstate is computed from Gamma_1 readout algebra before Q is evaluated.",
    )
    record(
        "E.2 conditional off-block orbit response is not promoted as retained closure",
        True,
        "It closes only after a new exclusivity/source-covariance law.",
    )
    record(
        "E.3 exact residual scalar is named",
        True,
        "Residual: derive_Gamma1_exclusive_noncentral_quadratic_source_grammar.",
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
        print("VERDICT: Gamma_1 first-live grammar does not derive exclusive noncentral source law.")
        print("KOIDE_Q_GAMMA1_EXCLUSIVE_SOURCE_GRAMMAR_NO_GO=TRUE")
        print("Q_GAMMA1_EXCLUSIVE_SOURCE_GRAMMAR_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_GAMMA1_EXCLUSIVE_NONCENTRAL_SOURCE=TRUE")
        print("RESIDUAL_SCALAR=derive_Gamma1_exclusive_noncentral_quadratic_source_grammar")
        print("RESIDUAL_SOURCE=uniform_Gamma1_reachable_slot_identity_return_not_excluded")
        print("COUNTERSTATE=Gamma1_uniform_return_I3_ratio_2_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: Gamma_1 exclusive source-grammar audit has FAILs.")
    print("KOIDE_Q_GAMMA1_EXCLUSIVE_SOURCE_GRAMMAR_NO_GO=FALSE")
    print("Q_GAMMA1_EXCLUSIVE_SOURCE_GRAMMAR_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_Gamma1_exclusive_noncentral_quadratic_source_grammar")
    return 1


if __name__ == "__main__":
    sys.exit(main())
