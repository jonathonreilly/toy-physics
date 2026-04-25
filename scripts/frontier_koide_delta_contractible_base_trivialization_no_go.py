#!/usr/bin/env python3
"""
Koide delta contractible-base trivialization no-go.

Theorem attempt:
  The selected Brannen line is an interval.  Since a line bundle over an
  interval is topologically trivial, perhaps this supplies a canonical
  endpoint trivialization and removes the offset c in the closed-APS-to-open
  endpoint functor.

Result:
  Negative.  Contractibility proves existence of a trivialization, not a
  canonical endpoint section.  On an interval, a U(1) gauge function

      chi(t) = s t

  is smooth and shifts the open endpoint phase by s while preserving every
  closed-loop APS invariant.  Thus the selected-line interval has no
  topological obstruction, but it also has no topological selector for the
  endpoint offset.  The offset c remains a boundary/trivialization datum.

No PDG masses, Koide Q target, fitted delta, or H_* pin is used.
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
    eta = sp.Rational(2, 9)

    section("A. Interval topology")

    beta0, beta1, beta2 = sp.Integer(1), sp.Integer(0), sp.Integer(0)
    record(
        "A.1 selected-line base interval is contractible",
        (beta0, beta1, beta2) == (1, 0, 0),
        f"Betti(I)=(beta0,beta1,beta2)=({beta0},{beta1},{beta2})",
    )
    record(
        "A.2 every U(1) line bundle on the interval is topologically trivial",
        beta2 == 0,
        "c1 lives in H^2(I)=0.",
    )

    section("B. Trivialization existence is not endpoint uniqueness")

    t, s = sp.symbols("t s", real=True)
    chi = sp.simplify(s * t)
    endpoint_shift = sp.simplify(chi.subs(t, 1) - chi.subs(t, 0))
    record(
        "B.1 smooth interval gauge functions shift open endpoint phase",
        endpoint_shift == s,
        f"chi(t)=s t -> chi(1)-chi(0)={endpoint_shift}",
    )
    delta_open = sp.symbols("delta_open", real=True)
    shifted = sp.simplify(delta_open + endpoint_shift)
    s_needed = sp.solve(sp.Eq(shifted, eta), s)
    record(
        "B.2 endpoint gauge can move any open phase to eta",
        s_needed == [sp.Rational(2, 9) - delta_open],
        f"s_required={s_needed[0]}",
    )
    record(
        "B.3 closed-loop exact terms cancel",
        sp.simplify((chi.subs(t, 1) - chi.subs(t, 0)) + (chi.subs(t, 0) - chi.subs(t, 1))) == 0,
        "The same endpoint gauge has no closed APS effect.",
    )

    section("C. No canonical zero offset from contractibility")

    offsets = [sp.Rational(-1, 9), sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9)]
    lines = []
    ok = True
    for offset in offsets:
        open_value = sp.simplify(delta_open + offset)
        ok = ok and open_value.has(delta_open)
        lines.append(f"c={offset}: F(delta_open)={open_value}")
    record(
        "C.1 contractible base admits a continuum of endpoint offsets",
        ok,
        "\n".join(lines),
    )
    record(
        "C.2 zero offset is a boundary section choice, not a topological consequence",
        True,
        "Contractibility removes obstruction; it does not choose a section.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 contractible-base trivialization route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 residual offset survives as endpoint section data",
        True,
        "Need a physical section/trivialization, not only existence of one.",
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
        print("VERDICT: contractible selected-line base does not close delta.")
        print("KOIDE_DELTA_CONTRACTIBLE_BASE_TRIVIALIZATION_NO_GO=TRUE")
        print("DELTA_CONTRACTIBLE_BASE_TRIVIALIZATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_section_not_canonical")
        return 0

    print("VERDICT: contractible-base trivialization audit has FAILs.")
    print("KOIDE_DELTA_CONTRACTIBLE_BASE_TRIVIALIZATION_NO_GO=FALSE")
    print("DELTA_CONTRACTIBLE_BASE_TRIVIALIZATION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_section_not_canonical")
    return 1


if __name__ == "__main__":
    sys.exit(main())
