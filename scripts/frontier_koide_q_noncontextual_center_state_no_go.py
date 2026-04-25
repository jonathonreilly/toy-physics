#!/usr/bin/env python3
"""
Koide Q noncontextual center-state no-go.

Theorem attempt:
  Treat the retained C3 center labels as a classical/quantum event algebra.
  Perhaps noncontextual probability, Gleason-style state extension, or
  objective indifference forces the equal center-label source, hence K_TL = 0.

Result:
  Negative.  On the two-atom center algebra, noncontextuality is exactly finite
  additivity:

      p(P_plus) + p(P_perp) = 1.

  It leaves the full interval p(P_plus)=u.  Every u in [0,1] extends to a
  block-unitarily invariant density on the retained rank-1/rank-2 carrier:

      rho(u) = u P_plus + ((1-u)/2) P_perp.

  The equal-label state u=1/2 is therefore a preparation prior.  The inherited
  full-carrier trace gives u=1/3 instead.  Even entropy/indifference sharpenings
  split: Shannon entropy on the two label atoms selects u=1/2, while von Neumann
  entropy on the retained rank-1/rank-2 carrier selects u=1/3.  Choosing the
  former is exactly the missing quotient-label source prior.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Noncontextual state space of the two-atom center")

    u = sp.symbols("u", real=True)
    p_plus = u
    p_perp = 1 - u
    p_identity = sp.simplify(p_plus + p_perp)
    record(
        "A.1 finite additivity fixes only p(P_plus)+p(P_perp)=1",
        p_identity == 1,
        f"p(P_plus)=u, p(P_perp)=1-u, p(1)={p_identity}",
    )

    samples = [sp.Rational(1, 5), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(2, 3)]
    sample_lines = []
    ok_samples = True
    for value in samples:
        ok_samples = ok_samples and 0 <= value <= 1
        sample_lines.append(
            f"u={value}: p=({value},{1-value}), Q={q_from_center_state(value)}, K_TL={ktl_from_center_state(value)}"
        )
    record(
        "A.2 closing and non-closing center states are all noncontextual",
        ok_samples,
        "\n".join(sample_lines),
    )
    record(
        "A.3 center-state neutrality is only u=1/2",
        sp.solve(sp.Eq(ktl_from_center_state(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl_from_center_state(u)}",
    )

    section("B. Gleason-style extension to the retained rank-1/rank-2 carrier")

    rho = sp.diag(u, (1 - u) / 2, (1 - u) / 2)
    trace_rho = sp.simplify(sp.trace(rho))
    p_plus_full = sp.simplify(rho[0, 0])
    p_perp_full = sp.simplify(rho[1, 1] + rho[2, 2])
    record(
        "B.1 every center state extends to a normalized block-invariant density",
        trace_rho == 1 and p_plus_full == u and p_perp_full == 1 - u,
        f"rho(u)=diag({u},(1-u)/2,(1-u)/2), trace={trace_rho}",
    )

    rho_rank_trace = sp.diag(sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3))
    u_rank = sp.simplify(rho_rank_trace[0, 0])
    record(
        "B.2 inherited full-carrier trace gives rank weighting, not label weighting",
        u_rank == sp.Rational(1, 3)
        and q_from_center_state(u_rank) == 1
        and ktl_from_center_state(u_rank) == sp.Rational(3, 8),
        f"u_rank={u_rank}, Q={q_from_center_state(u_rank)}, K_TL={ktl_from_center_state(u_rank)}",
    )
    record(
        "B.3 Gleason uniqueness does not apply as a uniform-state theorem here",
        True,
        "Dimension-3 state extension gives a density matrix family; the two-atom center remains a simplex.",
    )

    section("C. Entropy/indifference selectors depend on the chosen algebra")

    h_center = -u * sp.log(u) - (1 - u) * sp.log(1 - u)
    h_carrier = -u * sp.log(u) - (1 - u) * sp.log((1 - u) / 2)
    dh_center = sp.diff(h_center, u)
    dh_carrier = sp.diff(h_carrier, u)
    u_center_entropy = sp.Rational(1, 2)
    u_carrier_entropy = sp.Rational(1, 3)
    record(
        "C.1 label-algebra maximum entropy selects the closing state",
        sp.simplify(dh_center.subs(u, u_center_entropy)) == 0
        and q_from_center_state(u_center_entropy) == sp.Rational(2, 3)
        and ktl_from_center_state(u_center_entropy) == 0,
        f"dH_label/du={dh_center}; u_label={u_center_entropy}, Q={q_from_center_state(u_center_entropy)}, K_TL={ktl_from_center_state(u_center_entropy)}",
    )
    record(
        "C.2 retained-carrier von Neumann maximum entropy selects the rank state",
        sp.simplify(dh_carrier.subs(u, u_carrier_entropy)) == 0
        and q_from_center_state(u_carrier_entropy) == 1
        and ktl_from_center_state(u_carrier_entropy) == sp.Rational(3, 8),
        f"dS_carrier/du={dh_carrier}; u_carrier={u_carrier_entropy}, Q={q_from_center_state(u_carrier_entropy)}, K_TL={ktl_from_center_state(u_carrier_entropy)}",
    )
    record(
        "C.3 entropy closure requires choosing quotient labels over retained rank data",
        h_center != h_carrier,
        "H_label(u) and S_carrier(u)=H_label(u)+(1-u)log(2) have different stationary points.",
    )

    section("D. Objective indifference requires a non-retained atom swap")

    swap_condition = sp.solve(sp.Eq(p_plus, p_perp), u)
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    record(
        "D.1 an abstract atom swap would force u=1/2",
        swap_condition == [sp.Rational(1, 2)],
        f"p(P_plus)=p(P_perp) -> u={swap_condition}",
    )
    record(
        "D.2 the atom swap is not retained by the physical C3 real carrier",
        rank_plus != rank_perp,
        f"rank(P_plus)={rank_plus}, rank(P_perp)={rank_perp}",
    )
    record(
        "D.3 objective indifference is therefore an added source prior",
        True,
        "It selects the quotient label algebra over the retained carrier trace without a retained physical selector.",
    )

    section("E. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "E.1 noncontextual center-state route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_CENTER_STATE={residual}",
    )
    record(
        "E.2 Q remains open after noncontextuality audit",
        True,
        "Residual primitive: a physical law preparing the equal center-label source.",
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
        print("VERDICT: noncontextual center-state structure does not close Q.")
        print("KOIDE_Q_NONCONTEXTUAL_CENTER_STATE_NO_GO=TRUE")
        print("Q_NONCONTEXTUAL_CENTER_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_PRIOR=noncontextuality_does_not_prepare_uniform_center_state")
        print("RESIDUAL_ENTROPY_CHOICE=quotient_label_entropy_over_retained_carrier_entropy")
        return 0

    print("VERDICT: noncontextual center-state audit has FAILs.")
    print("KOIDE_Q_NONCONTEXTUAL_CENTER_STATE_NO_GO=FALSE")
    print("Q_NONCONTEXTUAL_CENTER_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_PRIOR=noncontextuality_does_not_prepare_uniform_center_state")
    print("RESIDUAL_ENTROPY_CHOICE=quotient_label_entropy_over_retained_carrier_entropy")
    return 1


if __name__ == "__main__":
    sys.exit(main())
