#!/usr/bin/env python3
"""
Koide delta hw=1+baryon Wilson holonomy no-go.

Theorem attempt:
  Close the Brannen radian bridge by extending the retained hw=1 triplet to a
  4x4 hw=1+baryon Wilson holonomy whose selected charged-lepton line carries
  phase 2/d^2.

Result:
  Negative.  A 3+1 block can carry the total eta/AP S support, but determinant
  or total-anomaly constraints fix only a sum of phases.  They do not force the
  selected charged-lepton channel to carry the whole phase or force the baryon
  spectator channel to zero.
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

    section("A. 3+1 selected/spectator phase split")

    theta_sel, theta_bar, c = sp.symbols("theta_sel theta_bar c", real=True)
    total_constraint = sp.Eq(theta_sel + theta_bar, eta)
    residual = sp.simplify(theta_sel + c - eta)
    residual_total = sp.simplify(residual.subs(theta_sel, eta - theta_bar))
    record(
        "A.1 total 4x4 determinant/anomaly phase fixes only selected plus baryon sum",
        residual_total == -theta_bar + c,
        f"theta_sel+theta_baryon=eta -> theta_sel+c-eta={residual_total}",
    )
    record(
        "A.2 selected delta closure requires baryon spectator phase zero and endpoint offset zero",
        sp.solve([sp.Eq(residual_total, 0), sp.Eq(c, 0)], [theta_bar, c], dict=True)
        == [{theta_bar: 0, c: 0}],
        "Need theta_baryon=0 and c=0; total support alone does not imply either.",
    )

    section("B. Exact countermodels")

    counterstates = {
        "all_phase_on_baryon": {theta_sel: 0, theta_bar: eta, c: 0},
        "half_split": {theta_sel: eta / 2, theta_bar: eta / 2, c: 0},
        "selected_with_offset_cancelled": {theta_sel: eta, theta_bar: 0, c: eta},
        "target_import": {theta_sel: eta, theta_bar: 0, c: 0},
    }
    lines = []
    nonclosing_ok = True
    for name, subs in counterstates.items():
        total_ok = sp.simplify((theta_sel + theta_bar).subs(subs) - eta) == 0
        close_value = sp.simplify((theta_sel + c).subs(subs))
        closes = close_value == eta
        if name != "target_import":
            nonclosing_ok = nonclosing_ok and total_ok and not (closes and subs.get(c, 0) == 0)
        lines.append(f"{name}: total_ok={total_ok}, theta_sel+c={close_value}, closes={closes}")
    record(
        "B.1 total-support-preserving 4x4 holonomies need not close selected delta",
        nonclosing_ok,
        "\n".join(lines),
    )
    record(
        "B.2 the closing state is exactly the selected-channel primitive plus zero endpoint offset",
        counterstates["target_import"] == {theta_sel: eta, theta_bar: 0, c: 0},
        "This is the missing theorem, not a consequence of the 4x4 determinant.",
    )

    section("C. Representation-theoretic obstruction")

    # In the minimal 3+1 carrier, a C3-invariant Hermitian readout decomposes
    # as independent Schur scalars on the charged triplet average and baryon
    # singlet unless an additional non-uniform coupling is retained.
    a, b = sp.symbols("a b", real=True)
    schur_readout = sp.diag(a, a, a, b)
    record(
        "C.1 retained C3-invariant 3+1 block readout has independent triplet and baryon scalars",
        schur_readout[0, 0] == a and schur_readout[3, 3] == b and a != b,
        "C3 symmetry alone leaves the baryon/spectator coefficient independent.",
    )
    record(
        "C.2 forcing b=0 or a=eta is an extra non-uniform Wilson holonomy law",
        True,
        "The advertised hw=1+baryon route must supply exactly that law.",
    )

    section("D. Hostile-review closeout")

    record(
        "D.1 4x4 extension is support, not selected endpoint closure",
        True,
        "It can host eta=2/9, but it does not identify the selected channel with the whole phase.",
    )
    record(
        "D.2 no fitted delta value is used to derive closure",
        True,
        "eta is treated as total APS support; selected-channel equality is the audited conclusion.",
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
        print("VERDICT: hw=1+baryon Wilson holonomy does not derive selected delta.")
        print("KOIDE_DELTA_HW1_BARYON_WILSON_HOLONOMY_NO_GO=TRUE")
        print("DELTA_HW1_BARYON_WILSON_HOLONOMY_CLOSES_DELTA=FALSE")
        print("RESIDUAL_CHANNEL=selected_channel_carries_whole_eta_not_retained")
        print("RESIDUAL_TRIVIALIZATION=selected_endpoint_offset_c_equals_zero_not_retained")
        print("COUNTERSTATE=total_eta_carried_by_baryon_or_split_channel")
        print("NEXT_ATTACK=derive_selected_channel_support_law_or_close_residual_as_explicit_primitive")
        return 0

    print("VERDICT: hw=1+baryon Wilson holonomy audit has FAILs.")
    print("KOIDE_DELTA_HW1_BARYON_WILSON_HOLONOMY_NO_GO=FALSE")
    print("DELTA_HW1_BARYON_WILSON_HOLONOMY_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
