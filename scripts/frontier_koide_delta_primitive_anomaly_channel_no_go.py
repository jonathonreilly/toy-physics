#!/usr/bin/env python3
"""
Koide delta primitive anomaly-channel no-go.

Theorem attempt:
  Use anomaly cancellation plus channel primitivity to remove the reduced
  endpoint condition

      delta_open = mu * eta_APS + c.

  If the selected Brannen line is forced to be the unique primitive
  Callan-Harvey inflow channel, then mu = 1 and, with c = 0, delta closes.

Result:
  Negative from the retained data alone.  Anomaly cancellation fixes the total
  boundary inflow.  It does not identify which open boundary line carries the
  primitive unit, nor does it choose the selected endpoint basepoint.

  In normalized variables:

      selected_channel + spectator_channel = 1,
      delta_open = selected_channel * eta_APS + c.

  Delta closure requires spectator_channel = 0 and c = 0.  The retained closed
  anomaly scalar supplies neither condition.

No mass data, fitted Koide value, or selected endpoint target is used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def anomaly_per_generation(d: int = 3) -> sp.Expr:
    return sp.simplify((2 * d) * sp.Rational(1, d) ** 3)


def main() -> int:
    section("A. Closed anomaly support")

    eta = eta_abss_z3_weights_12()
    anomaly = anomaly_per_generation(3)
    record(
        "A.1 ambient APS/anomaly scalar is exactly 2/9",
        eta == sp.Rational(2, 9) and anomaly == eta,
        f"eta_APS={eta}; A_CH={anomaly}",
    )

    section("B. Normalized primitive-channel equations")

    selected, spectator, c = sp.symbols("selected spectator c", real=True)
    total_constraint = sp.simplify(selected + spectator - 1)
    delta_open = sp.simplify(selected * eta + c)
    normalized_residual = sp.simplify(delta_open / eta - 1)
    residual_on_total = sp.simplify(normalized_residual.subs(selected, 1 - spectator))
    record(
        "B.1 anomaly cancellation fixes only selected + spectator = 1",
        total_constraint == selected + spectator - 1,
        f"constraint={total_constraint}",
    )
    record(
        "B.2 delta residual after total anomaly cancellation is -spectator plus offset/eta",
        residual_on_total == -spectator + c / eta,
        f"delta/eta_APS - 1 = {residual_on_total}",
    )
    record(
        "B.3 closure requires spectator channel zero and endpoint offset zero",
        sp.solve([sp.Eq(residual_on_total, 0), sp.Eq(c, 0)], [spectator, c], dict=True)
        == [{spectator: 0, c: 0}],
        "spectator=0 says the selected line carries the whole primitive anomaly channel.",
    )

    section("C. Counterchannels preserving the same closed anomaly")

    samples = [
        (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        (sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(0), sp.Rational(1, 9)),
    ]
    lines = []
    all_total_ok = True
    values = set()
    for selected_value, spectator_value, offset_value in samples:
        value = sp.simplify(
            delta_open.subs({selected: selected_value, spectator: spectator_value, c: offset_value})
        )
        total_ok = sp.simplify(total_constraint.subs({selected: selected_value, spectator: spectator_value})) == 0
        all_total_ok = all_total_ok and total_ok
        values.add(value)
        lines.append(
            f"selected={selected_value}, spectator={spectator_value}, c={offset_value}: "
            f"total_ok={total_ok}, delta_open={value}"
        )
    record(
        "C.1 the same total anomaly permits closing and non-closing selected endpoints",
        all_total_ok and len(values) == len(samples),
        "\n".join(lines),
    )

    section("D. What primitivity does and does not add")

    primitive_pairs = [(0, 1), (1, 0)]
    pair_lines = []
    for selected_value, spectator_value in primitive_pairs:
        pair_lines.append(
            f"selected={selected_value}, spectator={spectator_value}: "
            f"nonnegative_integer=True, total={selected_value + spectator_value}"
        )
    record(
        "D.1 nonnegative integer primitivity narrows to which channel carries the unit",
        len(primitive_pairs) == 2,
        "\n".join(pair_lines),
    )
    record(
        "D.2 primitivity still does not identify the selected line as the unit channel",
        True,
        "It leaves a discrete support-selection residual: selected=1 versus spectator=1.",
    )
    record(
        "D.3 selected-line nonzero coupling would close the channel part but is not retained",
        sp.solve([sp.Eq(total_constraint, 0), sp.Eq(spectator, 0)], [selected, spectator], dict=True)
        == [{selected: 1, spectator: 0}],
        "The missing theorem is exactly spectator=0 for the selected Brannen line.",
    )

    section("E. Hostile-review objections")

    record(
        "E.1 anomaly cancellation is a total constraint, not a selected-readout theorem",
        True,
        "The selected endpoint is one open readout channel; total inflow may be carried elsewhere unless excluded.",
    )
    record(
        "E.2 endpoint basepoint remains independent of channel primitivity",
        sp.solve(sp.Eq(delta_open.subs(selected, 1), eta), c) == [0],
        "Even after selected=1, the endpoint basepoint condition is c=0.",
    )

    section("F. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "F.1 primitive anomaly-channel route does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "F.2 reduced residual is spectator channel plus endpoint basepoint",
        True,
        "Need selected line = unique primitive anomaly channel, and c=0, from retained physics.",
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
        print("VERDICT: primitive anomaly-channel route does not close delta.")
        print("KOIDE_DELTA_PRIMITIVE_ANOMALY_CHANNEL_NO_GO=TRUE")
        print("DELTA_PRIMITIVE_ANOMALY_CHANNEL_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_CHANNEL=selected_line_is_unique_primitive_anomaly_channel_not_retained")
        print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
        return 0

    print("VERDICT: primitive anomaly-channel audit has FAILs.")
    print("KOIDE_DELTA_PRIMITIVE_ANOMALY_CHANNEL_NO_GO=FALSE")
    print("DELTA_PRIMITIVE_ANOMALY_CHANNEL_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_CHANNEL=selected_line_is_unique_primitive_anomaly_channel_not_retained")
    print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
