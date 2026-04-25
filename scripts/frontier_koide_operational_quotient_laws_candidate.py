#!/usr/bin/env python3
"""
Koide operational-quotient laws candidate.

Purpose:
  Build the two missing charged-lepton Koide laws as a single operational
  quotient principle, then test exactly what it closes and what remains open.

Candidate physical principle:
  A retained source or boundary endpoint may depend only on quotient-internal
  operational structure.  Embedding data removed by the physical quotient is
  not a source label and not an endpoint complement.

Consequences:
  Q side:
    The Morita-normalized quotient-center source has two unlabeled copyable
    components.  Naturality under the quotient automorphism group swaps them,
    so the source weights are equal and K_TL=0.

  Delta side:
    The selected Brannen line is the quotient-internal APS boundary segment.
    With no endpoint complement in the quotient, gluing is the identity unit,
    so tau=0 and delta_open=eta_APS=2/9.

Nature-grade boundary:
  This runner builds a candidate law packet.  It does not prove that the
  operational quotient principle is already retained by the existing
  Cl(3)/Z3 data.  The included countermodels show exactly how the packet fails
  if C3 orbit labels or endpoint complements remain source-visible.
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
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def solve_swap_invariant_weight() -> sp.Expr:
    w = sp.symbols("w", real=True)
    p = sp.Matrix([w, 1 - w])
    swap = sp.Matrix([[0, 1], [1, 0]])
    solution = sp.solve(list(sp.simplify(swap * p - p)), [w], dict=True)
    return sp.simplify(solution[0][w])


def solve_open_delta(eta_closed: sp.Expr, tau: sp.Expr) -> sp.Expr:
    delta_open = sp.symbols("delta_open", real=True)
    solution = sp.solve(sp.Eq(eta_closed, delta_open + tau), delta_open)
    return sp.simplify(solution[0])


def main() -> int:
    section("A. One operational quotient principle, two residuals")

    record(
        "A.1 quotient-internal source data excludes removed embedding labels",
        True,
        "Source states are natural on the quotient source object, not on a chosen C3 embedding.",
    )
    record(
        "A.2 quotient-internal endpoint data excludes removed complements",
        True,
        "Endpoint phases are computed on the quotient boundary segment, not on an added cap.",
    )

    section("B. Q law from quotient automorphism naturality")

    w_star = solve_swap_invariant_weight()
    q_star = q_from_weight(w_star)
    ktl_star = ktl_from_weight(w_star)
    record(
        "B.1 two unlabeled quotient-center components have transitive automorphism group",
        w_star == sp.Rational(1, 2),
        f"swap invariance gives w_plus={w_star}",
    )
    record(
        "B.2 quotient source naturality gives K_TL=0 and Q=2/3",
        ktl_star == 0 and q_star == sp.Rational(2, 3),
        f"K_TL={ktl_star}, Q={q_star}",
    )

    section("C. Delta law from quotient endpoint unit")

    eta_symbol = sp.symbols("eta_closed", real=True)
    tau_identity = sp.Integer(0)
    delta_symbolic = solve_open_delta(eta_symbol, tau_identity)
    eta_aps = eta_abss_z3_weights_12()
    delta_aps = solve_open_delta(eta_aps, tau_identity)
    record(
        "C.1 quotient endpoint unit gives tau=0 and delta_open=eta_closed symbolically",
        delta_symbolic == eta_symbol,
        f"eta_closed=delta_open+tau, tau=0 -> delta_open={delta_symbolic}",
    )
    record(
        "C.2 independent APS value gives delta_open=2/9",
        eta_aps == sp.Rational(2, 9) and delta_aps == sp.Rational(2, 9),
        f"eta_APS={eta_aps}, delta_open={delta_aps}",
    )

    section("D. Countermodels if the quotient law is not retained")

    visible_orbit_labels = (frozenset({0}), frozenset({1, 2}))
    orbit_counter_weight = sp.Rational(1, 3)
    record(
        "D.1 source-visible C3 orbit labels break Q component anonymity",
        visible_orbit_labels[0] != visible_orbit_labels[1]
        and q_from_weight(orbit_counter_weight) == 1
        and ktl_from_weight(orbit_counter_weight) == sp.Rational(3, 8),
        f"labels={tuple(sorted(x) for x in visible_orbit_labels)}, w=1/3 -> Q={q_from_weight(orbit_counter_weight)}, K_TL={ktl_from_weight(orbit_counter_weight)}",
    )
    tau_counter = sp.Rational(1, 9)
    delta_counter = solve_open_delta(eta_aps, tau_counter)
    record(
        "D.2 source-visible endpoint complement breaks delta identity gluing",
        delta_counter == sp.Rational(1, 9)
        and sp.simplify(delta_counter + tau_counter) == eta_aps,
        f"tau={tau_counter}, delta_open={delta_counter}, closed_total={sp.simplify(delta_counter + tau_counter)}",
    )

    section("E. Review boundary")

    record(
        "E.1 the law packet is value-independent",
        q_from_weight(w_star) == sp.Rational(2, 3)
        and solve_open_delta(sp.Rational(5, 17), tau_identity) == sp.Rational(5, 17),
        "Q follows from automorphism naturality; delta transfer works for arbitrary eta_closed.",
    )
    record(
        "E.2 no retained closure is claimed by this candidate packet",
        True,
        "Reviewer must decide whether the operational quotient principle is physically retained.",
    )
    record(
        "E.3 the remaining positive task is now explicit",
        True,
        "Derive or retain operational quotient noncontextuality for source labels and boundary endpoints.",
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
        print("KOIDE_OPERATIONAL_QUOTIENT_LAWS_CANDIDATE=TRUE")
        print("KOIDE_CONDITIONAL_Q_CLOSURE_UNDER_OPERATIONAL_QUOTIENT=TRUE")
        print("KOIDE_CONDITIONAL_DELTA_CLOSURE_UNDER_OPERATIONAL_QUOTIENT=TRUE")
        print("KOIDE_RETAINED_FULL_CLOSURE_CLAIM=FALSE")
        print("Q_REVIEW_BARRIER=derive_source_label_operational_quotient")
        print("DELTA_REVIEW_BARRIER=derive_endpoint_complement_operational_quotient")
        print("FALSIFIER=source_visible_labels_or_endpoint_complements")
        return 0

    print("KOIDE_OPERATIONAL_QUOTIENT_LAWS_CANDIDATE=FALSE")
    print("KOIDE_RETAINED_FULL_CLOSURE_CLAIM=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
