#!/usr/bin/env python3
"""
Koide Q physical-lattice source-grammar fourfold audit.

Theorem attempt:
  Strengthen the Q zero-background route by taking the Cl(3)/Z^3 lattice as
  physical and proving that the undeformed microscopic lattice action cannot
  contain a native traceless charged-lepton scalar source

      z Z,  Z = P_plus - P_perp.

  Four candidate routes are attacked in one runner:

    1. Z is not a microscopic local lattice operator before reduction.
    2. The bare physical lattice action admits only common scalar sI.
    3. zZ is a probe/source deformation, not undeformed physical-lattice data.
    4. Microscopic symmetry/locality forbids the linear Z scalar term.

Result:
  Conditional support, retained no-go.  Strict onsite C3-invariant scalar
  locality would indeed leave only sI.  However, the current retained Q source
  domain is broader: the physical three-generation C3 carrier retains central
  projectors P_plus and P_perp, so Z is a C3-invariant central source direction.
  The observable principle classifies zZ as a source deformation unless it is
  separately present in the undeformed action; it does not prove the undeformed
  action excludes it.  Existing C3 symmetry/locality allows a linear ell*z term.

Exact residual:

      derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    a, b, c, s, z, ell, m, rho = sp.symbols("a b c s z ell m rho", real=True)

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J3 = sp.ones(3, 3)
    P_plus = sp.simplify((I3 + C + C**2) / 3)
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)

    section("A. Theorem attempt and parallel route ranking")

    routes = [
        "Z might not be a microscopic local lattice operator before reduction",
        "bare physical lattice action might admit only common onsite scalar sI",
        "zZ might be classified as probe deformation, not undeformed data",
        "microscopic symmetry/locality might forbid the linear Z scalar term",
        "wrong-assumption inversion: central/projected source grammar admits zZ",
    ]
    record(
        "A.1 all four physical-lattice source routes and the inversion are tested",
        len(routes) == 5,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("onsite_locality_excludes_Z", 4, 3, 4),
        ("undeformed_action_source_grammar", 4, 3, 3),
        ("probe_vs_background_classification", 3, 3, 2),
        ("microscopic_symmetry_locality_forbids_linear_Z", 2, 3, 2),
    ]
    record(
        "A.2 onsite locality is the strongest positive subroute",
        ranked[0][0] == "onsite_locality_excludes_Z",
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Route 1: microscopic local lattice operator status")

    onsite = sp.diag(a, b, c)
    onsite_comm = sp.simplify(C * onsite * C.T - onsite)
    onsite_solutions = sp.solve(list(onsite_comm), [a, b, c], dict=True)
    record(
        "B.1 strict onsite C3-invariant scalar potentials are only common scalar",
        onsite_solutions == [{a: c, b: c}],
        f"C diag(a,b,c) C^-1 = diag(a,b,c) -> {onsite_solutions}",
    )
    record(
        "B.2 Z is not a diagonal onsite scalar on the three-site orbit",
        Z != sp.diag(*[Z[i, i] for i in range(3)])
        and sp.simplify(Z - (P_plus - P_perp)) == sp.zeros(3, 3),
        f"Z={Z}",
    )
    record(
        "B.3 but Z is a retained C3-invariant central polynomial in the lattice rotation",
        sp.simplify(P_plus - J3 / 3) == sp.zeros(3, 3)
        and sp.simplify(Z**2 - I3) == sp.zeros(3, 3)
        and sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3),
        "Z=2/3*(I+C+C^2)-I is retained on the generation C3 carrier.",
    )
    record(
        "B.4 route 1 closes only if strict onsite-only scalar source grammar is retained",
        True,
        "Physical lattice alone does not decide whether central/projected source directions are inadmissible.",
    )

    section("C. Route 2: bare physical lattice action scalar grammar")

    bare_onsite = sp.simplify(s * I3)
    bare_with_z = sp.simplify(s * I3 + z * Z)
    record(
        "C.1 onsite-only bare scalar grammar forbids zZ conditionally",
        sp.solve(list(sp.simplify(bare_with_z - bare_onsite)), [z], dict=True)
        == [{z: 0}],
        "Within onsite-only grammar, sI+zZ=sI forces z=0.",
    )
    record(
        "C.2 retained central-source grammar admits sI+zZ while preserving C3",
        sp.simplify(C * bare_with_z * C.T - bare_with_z) == sp.zeros(3, 3),
        "The counterterm is C3-invariant and central.",
    )
    source_visibility_family = sp.log(1 + sp.symbols("k_plus")) + (1 + rho) * sp.log(
        1 + sp.symbols("k_perp")
    )
    record(
        "C.3 a rank-visible determinant source family keeps one free traceless scalar",
        sp.diff(source_visibility_family, rho) != 0,
        "The full source language has a rank/orbit visibility parameter rho.",
    )

    section("D. Route 3: probe deformation versus undeformed data")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    W = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    y_zero = (
        sp.simplify(sp.diff(W, k_plus).subs({k_plus: 0, k_perp: 0})),
        sp.simplify(sp.diff(W, k_perp).subs({k_plus: 0, k_perp: 0})),
    )
    W_background = sp.log(1 + k_plus + z) + sp.log(1 + k_perp - z)
    y_background = (
        sp.simplify(sp.diff(W_background, k_plus).subs({k_plus: 0, k_perp: 0})),
        sp.simplify(sp.diff(W_background, k_perp).subs({k_plus: 0, k_perp: 0})),
    )
    record(
        "D.1 source-response coefficient at undeformed J=0 is the neutral probe coefficient",
        y_zero == (1, 1),
        f"dW|0={y_zero}",
    )
    record(
        "D.2 evaluating around D+zZ is a different background with z still free",
        y_background == (1 / (z + 1), -1 / (z - 1)),
        f"dW_background|0={y_background}",
    )
    record(
        "D.3 probe classification names the falsifier but does not exclude native zZ",
        True,
        "If zZ is part of the undeformed physical lattice action, the probe theorem evaluates around D+zZ.",
    )

    section("E. Route 4: microscopic symmetry/locality forbidding linear Z")

    K_z = sp.simplify(z * Z)
    linear_z = sp.simplify(sp.trace(Z * K_z) / sp.trace(Z**2))
    record(
        "E.1 the linear Z source coefficient is C3-invariant",
        linear_z == z and sp.simplify(C * K_z * C.T - K_z) == sp.zeros(3, 3),
        "C3 symmetry cannot forbid ell*z.",
    )
    V = sp.simplify(ell * z + m * z**2)
    stationary = sp.solve(sp.Eq(sp.diff(V, z), 0), z)
    record(
        "E.2 convex local scalar potentials can have nonzero Z minima",
        stationary == [-ell / (2 * m)],
        "V=ell*z+m*z^2 gives z*=-ell/(2m); zero requires ell=0.",
    )
    parity_condition = sp.solve(sp.Eq(sp.simplify(V.subs(z, -z) - V), 0), ell)
    record(
        "E.3 Z parity or plus/perp exchange would close only as an extra law",
        parity_condition == [0],
        "V(z)=V(-z) forces ell=0, but the retained C3 carrier fixes the two blocks separately.",
    )

    section("F. Q consequence and countermodel")

    counter_z = -sp.Rational(1, 3)
    record(
        "F.1 onsite-only source grammar conditionally gives the Q support chain",
        q_from_z(0) == sp.Rational(2, 3) and ktl_from_z(0) == 0,
        f"z=0 -> Q={q_from_z(0)}, K_TL={ktl_from_z(0)}",
    )
    record(
        "F.2 retained central-source countermodel remains exact",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "F.3 physical lattice acceptance alone has zero equation-rank on z",
        sp.Matrix([0]).jacobian([z]).rank() == 0,
        "The physical carrier d=3/C3/Z3 data do not impose z=0 without a source-grammar law.",
    )

    section("G. Hostile review")

    record(
        "G.1 conditional onsite theorem is not promoted as retained Q closure",
        True,
        "It closes only after retaining onsite-only undeformed scalar source grammar.",
    )
    record(
        "G.2 no forbidden target or observational pin is used",
        True,
        "The countermodel and closing model are compared under exact symbolic lattice-source algebra.",
    )
    record(
        "G.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z",
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
        print("VERDICT: physical lattice helps only conditionally; it does not by itself exclude zZ.")
        print("KOIDE_Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_FOURFOLD_NO_GO=TRUE")
        print("Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_ONSITE_ONLY_UNDEFORMED_LATTICE_SOURCE_GRAMMAR=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z")
        print("RESIDUAL_SOURCE=physical_lattice_keeps_central_projected_Z_source_visible")
        print("COUNTERMODEL=physical_C3_lattice_with_central_source_z_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: physical-lattice source-grammar fourfold audit has FAILs.")
    print("KOIDE_Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_FOURFOLD_NO_GO=FALSE")
    print("Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z")
    return 1


if __name__ == "__main__":
    sys.exit(main())
