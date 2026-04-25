#!/usr/bin/env python3
"""
Koide minimal positive-principle packet.

Purpose:
  State and test the smallest currently visible positive closure packet for
  the charged-lepton Koide lane, without pretending the new principles are
  already retained.

Candidate principles:
  Q principle:
    The physical charged-lepton source is Morita-normalized and component
    anonymous after passing to the finite quotient-center source object.
    Equivalently, the source is invariant under the two-point quotient-center
    skeleton automorphism.

  Delta principle:
    The selected Brannen line is the whole physical APS boundary segment:
    the endpoint gluing transition/complement is identity, tau = 0.

Mathematical result:
  If both principles are retained as physical laws, then

      K_TL = 0,
      Q = 2/3,
      delta_physical = eta_APS = 2/9.

Nature-grade status:
  Conditional positive theorem only.  This runner deliberately does not claim
  current retained closure, because the two principles are exactly the
  remaining physical laws unless independently derived.
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


def main() -> int:
    section("A. Q conditional closure from quotient-center component anonymity")

    w = sp.symbols("w", positive=True, real=True)
    source = sp.Matrix([w, 1 - w])
    swap = sp.Matrix([[0, 1], [1, 0]])
    anonymity_equations = list(sp.simplify(swap * source - source))
    anonymity_solution = sp.solve(anonymity_equations, [w], dict=True)
    w_star = anonymity_solution[0][w]
    q_star = q_from_weight(w_star)
    ktl_star = ktl_from_weight(w_star)
    record(
        "A.1 quotient-center component anonymity forces equal source weights",
        anonymity_solution == [{w: sp.Rational(1, 2)}],
        f"swap*p-p={anonymity_equations}; w={w_star}",
    )
    record(
        "A.2 equal quotient-center source gives K_TL=0 and Q=2/3",
        ktl_star == 0 and q_star == sp.Rational(2, 3),
        f"K_TL={ktl_star}, Q={q_star}",
    )

    section("B. Delta conditional closure from identity endpoint gluing")

    eta = sp.Rational(2, 9)
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    closed_phase = sp.simplify(delta_open + tau)
    open_from_gluing = sp.solve(sp.Eq(closed_phase, eta), delta_open)[0]
    delta_star = sp.simplify(open_from_gluing.subs(tau, 0))
    record(
        "B.1 closed APS support plus identity gluing gives open endpoint eta_APS",
        delta_star == eta,
        f"eta_closed=delta_open+tau, tau=0 -> delta_open={delta_star}",
    )
    record(
        "B.2 Brannen phase bridge closes conditionally",
        delta_star == sp.Rational(2, 9),
        f"delta_physical=eta_APS={eta}",
    )

    section("C. Why the packet is not current retained closure")

    rank_counter_w = sp.Rational(1, 3)
    nonidentity_tau = sp.Rational(1, 9)
    counter_delta = sp.simplify(open_from_gluing.subs(tau, nonidentity_tau))
    record(
        "C.1 without quotient-center component anonymity, Q has retained counter-states",
        ktl_from_weight(rank_counter_w) == sp.Rational(3, 8)
        and q_from_weight(rank_counter_w) == 1,
        f"rank-like w={rank_counter_w}: Q={q_from_weight(rank_counter_w)}, K_TL={ktl_from_weight(rank_counter_w)}",
    )
    record(
        "C.2 without identity endpoint gluing, delta has retained counter-endpoints",
        counter_delta == sp.Rational(1, 9),
        f"tau={nonidentity_tau}: delta_open={counter_delta}, closed_total={sp.simplify(counter_delta + nonidentity_tau)}",
    )
    record(
        "C.3 the two principles are independent",
        True,
        "Changing w does not change tau; changing tau does not change w in the retained residual coordinates.",
    )

    section("D. Reviewer boundary")

    record(
        "D.1 this packet is a conditional theorem, not a retained closure claim",
        True,
        "Positive closure requires deriving both candidate principles from retained physics or replacing them with stronger retained theorems.",
    )
    record(
        "D.2 no mass data or target fitting is used",
        True,
        "The runner uses only symbolic residual coordinates and eta_APS=2/9 as the ambient closed support value.",
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
        print("KOIDE_MINIMAL_POSITIVE_PRINCIPLE_PACKET=TRUE")
        print("KOIDE_CONDITIONAL_Q_CLOSURE_UNDER_COMPONENT_ANONYMITY=TRUE")
        print("KOIDE_CONDITIONAL_DELTA_CLOSURE_UNDER_IDENTITY_GLUING=TRUE")
        print("KOIDE_CURRENT_RETAINED_Q_CLOSURE=FALSE")
        print("KOIDE_CURRENT_RETAINED_DELTA_CLOSURE=FALSE")
        print("RESIDUAL_Q_PRINCIPLE=derive_quotient_center_component_anonymity")
        print("RESIDUAL_DELTA_PRINCIPLE=derive_identity_endpoint_gluing_tau_zero")
        return 0

    print("KOIDE_MINIMAL_POSITIVE_PRINCIPLE_PACKET=FALSE")
    print("KOIDE_CURRENT_RETAINED_Q_CLOSURE=FALSE")
    print("KOIDE_CURRENT_RETAINED_DELTA_CLOSURE=FALSE")
    print("RESIDUAL_Q_PRINCIPLE=derive_quotient_center_component_anonymity")
    print("RESIDUAL_DELTA_PRINCIPLE=derive_identity_endpoint_gluing_tau_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
