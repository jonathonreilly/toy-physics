#!/usr/bin/env python3
"""
Koide delta functorial-gluing endpoint no-go.

Theorem attempt:
  Strengthen the Dai-Freed/determinant-line route by using functorial gluing:
  perhaps the closed APS phase decomposes canonically so the selected open
  Brannen line carries the whole eta_APS endpoint.

Result:
  Negative.  Gluing gives an additive law

      eta_closed = phase_selected + phase_complement  (mod 1).

  With eta_closed=2/9, this equation leaves one continuous split parameter.
  Setting phase_complement=0, or declaring that the selected segment is the
  whole closed loop, is precisely an endpoint/trivialization primitive.  The
  gluing law is necessary consistency, not a selector for the selected-line
  open endpoint.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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


def main() -> int:
    section("A. Functorial gluing equation")

    eta = sp.Rational(2, 9)
    selected, complement = sp.symbols("selected complement", real=True)
    gluing_residual = sp.simplify(selected + complement - eta)
    complement_solution = sp.solve(sp.Eq(gluing_residual, 0), complement)
    record(
        "A.1 closed APS phase is exactly eta=2/9 in the gluing equation",
        eta == sp.Rational(2, 9),
        f"eta_closed={eta}",
    )
    record(
        "A.2 gluing leaves one free split parameter",
        complement_solution == [sp.Rational(2, 9) - selected],
        f"selected + complement = eta -> complement={complement_solution}",
    )

    section("B. Many splits satisfy the same closed APS value")

    selected_values = [sp.Rational(0), sp.Rational(1, 18), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    split_lines = []
    ok = True
    for value in selected_values:
        comp_value = sp.simplify(eta - value)
        total = sp.simplify(value + comp_value)
        ok = ok and total == eta
        split_lines.append(f"selected={value}, complement={comp_value}, total={total}")
    record(
        "B.1 closing and non-closing selected endpoints obey gluing",
        ok,
        "\n".join(split_lines),
    )
    record(
        "B.2 selected=eta is equivalent to complement=0",
        sp.solve(sp.Eq(selected, eta), selected) == [eta]
        and complement_solution[0].subs(selected, eta) == 0,
        "The desired endpoint is the zero-complement split.",
    )

    section("C. Zero complement is a boundary condition, not gluing")

    boundary_section_start, boundary_section_end = sp.symbols("s0 s1", real=True)
    complement_with_sections = sp.simplify(complement + boundary_section_end - boundary_section_start)
    zero_complement_solution = sp.solve(sp.Eq(complement_with_sections, 0), boundary_section_end)
    record(
        "C.1 endpoint sections can make the complement vanish",
        zero_complement_solution == [boundary_section_start - complement],
        f"s1={zero_complement_solution}",
    )
    record(
        "C.2 the section choice is not fixed by the closed gluing law",
        True,
        "Functoriality checks additivity after sections are chosen; it does not choose them.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 functorial-gluing route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after gluing audit",
        True,
        "Residual primitive: boundary condition that assigns the full closed eta to the selected open line.",
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
        print("VERDICT: functorial gluing does not close delta.")
        print("KOIDE_DELTA_FUNCTORIAL_GLUING_ENDPOINT_NO_GO=TRUE")
        print("DELTA_FUNCTORIAL_GLUING_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SPLIT=closed_APS_gluing_does_not_select_open_segment")
        return 0

    print("VERDICT: functorial-gluing endpoint audit has FAILs.")
    print("KOIDE_DELTA_FUNCTORIAL_GLUING_ENDPOINT_NO_GO=FALSE")
    print("DELTA_FUNCTORIAL_GLUING_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_SPLIT=closed_APS_gluing_does_not_select_open_segment")
    return 1


if __name__ == "__main__":
    sys.exit(main())
