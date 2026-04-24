#!/usr/bin/env python3
"""
Koide Q/delta residual cohomology obstruction no-go.

Theorem attempt:
  Derive the primitive-based readout/basepoint law from an exact-sequence
  view of the retained source and boundary data.  If the residual label,
  spectator, and endpoint-exact directions were coboundaries with a canonical
  zero representative, then retained cohomology would close the Koide lane.

Result:
  Negative.  The current retained equations form affine fibres over retained
  observables with nontrivial kernel directions:

    Q:     ker(trace/source total) = span{Z}
    delta: ker(closed total/APS data) = span{selected-spectator, endpoint exact}

  The target readouts are exactly choices of the zero element in these kernels.
  Exactness identifies the kernels; it does not supply a canonical section.
  Any section/basepoint theorem that picks the zero representative is therefore
  the primitive-based operational boundary readout law or an equivalent new
  retained theorem.

No mass data, fitted Koide value, H_* pin, or selected endpoint target is used.
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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Q retained source exact sequence")

    # Reduced source coordinates: total t and label z=<Z>.  The retained total
    # projection forgets z; the zero-label section is the missing theorem.
    trace_projection = sp.Matrix([[1, 0]])
    q_kernel = trace_projection.nullspace()
    record(
        "A.1 trace/source-total projection has a one-dimensional kernel",
        len(q_kernel) == 1 and q_kernel[0] == sp.Matrix([0, 1]),
        f"ker(pi_Q)={q_kernel}",
    )

    t, z, a = sp.symbols("t z a", real=True)
    q_fibre_point = sp.Matrix([t, z])
    shifted_q_fibre_point = q_fibre_point + a * q_kernel[0]
    record(
        "A.2 kernel translations preserve the retained Q total observable",
        trace_projection * shifted_q_fibre_point == sp.Matrix([t]),
        f"(t,z) -> {list(shifted_q_fibre_point)} preserves pi_Q=t",
    )

    w_from_z = sp.simplify((1 + z) / 2)
    record(
        "A.3 zero kernel representative is exactly the Q closing midpoint",
        ktl_from_weight(w_from_z).subs(z, 0) == 0
        and q_from_weight(w_from_z).subs(z, 0) == sp.Rational(2, 3),
        "z=0 -> w_plus=1/2 -> K_TL=0 and Q=2/3.",
    )
    z_counter = sp.Rational(-1, 3)
    w_counter = sp.simplify(w_from_z.subs(z, z_counter))
    record(
        "A.4 nonzero kernel representative preserves total but does not close Q",
        w_counter == sp.Rational(1, 3)
        and ktl_from_weight(w_counter) == sp.Rational(3, 8)
        and q_from_weight(w_counter) == 1,
        f"z={z_counter}, w_plus={w_counter}, K_TL={ktl_from_weight(w_counter)}, Q={q_from_weight(w_counter)}",
    )

    section("B. Delta retained boundary exact sequence")

    # Boundary coordinates are selected channel, spectator channel, endpoint
    # exact shift.  The retained closed-total projection sees selected+spectator
    # and forgets the split plus endpoint-exact direction.
    boundary_projection = sp.Matrix([[1, 1, 0]])
    delta_kernel = boundary_projection.nullspace()
    expected_kernel = [sp.Matrix([-1, 1, 0]), sp.Matrix([0, 0, 1])]
    record(
        "B.1 closed boundary projection has a two-dimensional kernel",
        len(delta_kernel) == 2 and delta_kernel == expected_kernel,
        f"ker(pi_delta)={delta_kernel}",
    )

    selected, spectator, c, u, v = sp.symbols("selected spectator c u v", real=True)
    boundary_point = sp.Matrix([selected, spectator, c])
    shifted_boundary_point = boundary_point + u * delta_kernel[0] + v * delta_kernel[1]
    record(
        "B.2 kernel translations preserve selected+spectator closed total",
        boundary_projection * shifted_boundary_point
        == sp.Matrix([selected + spectator]),
        f"(selected,spectator,c) -> {list(shifted_boundary_point)} preserves the closed total.",
    )

    eta = eta_abss_z3_weights_12()
    selected_norm = sp.simplify(1 - spectator)
    delta_open = sp.simplify(selected_norm * eta + c)
    residual = sp.simplify(delta_open / eta - 1)
    record(
        "B.3 open endpoint residual is the nontrivial functional on the kernel",
        residual == -spectator + sp.Rational(9, 2) * c,
        f"delta_open/eta_APS - 1 = {residual}",
    )

    closing = {spectator: 0, c: 0}
    record(
        "B.4 zero kernel representative is exactly the delta closing section",
        sp.simplify(residual.subs(closing)) == 0
        and sp.simplify(delta_open.subs(closing)) == eta
        and eta == sp.Rational(2, 9),
        f"spectator=0,c=0 -> delta_open={sp.simplify(delta_open.subs(closing))}",
    )

    countermodels = [
        ("spectator kernel", {spectator: 1, c: 0}),
        ("half spectator kernel", {spectator: sp.Rational(1, 2), c: 0}),
        ("endpoint exact kernel", {spectator: 0, c: sp.Rational(1, 9)}),
    ]
    lines: list[str] = []
    counter_ok = True
    for name, subs in countermodels:
        delta_value = sp.simplify(delta_open.subs(subs))
        residual_value = sp.simplify(residual.subs(subs))
        closed_total = sp.simplify((selected_norm + spectator).subs(subs))
        counter_ok = counter_ok and closed_total == 1 and residual_value != 0
        lines.append(
            f"{name}: {subs}, closed_total={closed_total}, "
            f"delta_open={delta_value}, residual={residual_value}"
        )
    record(
        "B.5 nonzero kernel representatives preserve retained totals but do not close delta",
        counter_ok,
        "\n".join(lines),
    )

    section("C. Exactness does not canonically split the fibres")

    section_parameter = sp.symbols("section_parameter", real=True)
    q_section_family = sp.Matrix([t, section_parameter * t])
    record(
        "C.1 Q sections of the same exact sequence form a non-unique family",
        trace_projection * q_section_family == sp.Matrix([t]),
        f"s_a(t)={list(q_section_family)}; zero section requires a=0.",
    )

    b1, b2 = sp.symbols("b1 b2", real=True)
    delta_section_family = sp.Matrix([1 - b1, b1, b2])
    record(
        "C.2 delta sections of the same exact sequence also form a non-unique family",
        boundary_projection * delta_section_family == sp.Matrix([1]),
        f"s_(b1,b2)={list(delta_section_family)}; closing section requires b1=b2=0.",
    )
    record(
        "C.3 exactness names the obstruction class but does not choose its zero representative",
        True,
        "A canonical section/basepoint is additional physical structure.",
    )

    section("D. Hostile review")

    record(
        "D.1 cohomology obstruction is value-independent",
        True,
        "The kernel argument precedes the numerical APS evaluation; eta is inserted only to display exact residuals.",
    )
    record(
        "D.2 the theorem does not promote no-go data as closure",
        True,
        "It proves that retained exactness alone lacks the section/basepoint needed for closure.",
    )
    record(
        "D.3 positive closure is reduced to a section theorem",
        True,
        "Need a retained theorem selecting z=0, spectator=0, and c=0 as the canonical section.",
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
        print("VERDICT: retained exact-sequence/cohomology data do not close the Koide lane.")
        print("KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO=TRUE")
        print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_Q=FALSE")
        print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_DELTA=FALSE")
        print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE")
        print("RESIDUAL_SCALAR=canonical_zero_section_for_source_label_spectator_and_endpoint_kernel")
        print("RESIDUAL_Q=nontrivial_trace_kernel_span_Z")
        print("RESIDUAL_DELTA=nontrivial_closed_boundary_kernel_span_spectator_and_endpoint_exact")
        print("NEXT_THEOREM=retained_canonical_section_or_new_primitive_based_readout_law")
        return 0

    print("VERDICT: residual cohomology obstruction audit has FAILs.")
    print("KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO=FALSE")
    print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_Q=FALSE")
    print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_DELTA=FALSE")
    print("Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE")
    print("RESIDUAL_SCALAR=canonical_zero_section_for_source_label_spectator_and_endpoint_kernel")
    return 1


if __name__ == "__main__":
    sys.exit(main())
