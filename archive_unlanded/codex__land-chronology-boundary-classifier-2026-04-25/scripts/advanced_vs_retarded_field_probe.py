#!/usr/bin/env python3
"""Chronology lane probe: advanced fields versus retarded support.

Retained causal-field semantics use retarded support: field values at (t, x)
depend on source data in the past cone. An advanced Green-function calculation
can make an earlier field depend on later source choices, but that dependence
is future-boundary import, not a local past-directed signal.
"""

from __future__ import annotations

import math


PASS = 0
FAIL = 0


Source = tuple[int, int, float]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def kernel_weight(x: int, xs: int) -> float:
    return 1.0 / (1.0 + abs(x - xs))


def retarded_field(t: int, x: int, sources: list[Source], c: float = 1.0) -> float:
    total = 0.0
    for ts, xs, strength in sources:
        travel_time = abs(x - xs) / c
        if t >= ts + travel_time:
            total += strength * kernel_weight(x, xs)
    return total


def advanced_field(t: int, x: int, sources: list[Source], c: float = 1.0) -> float:
    total = 0.0
    for ts, xs, strength in sources:
        travel_time = abs(x - xs) / c
        if t <= ts - travel_time:
            total += strength * kernel_weight(x, xs)
    return total


def fmt(value: float) -> str:
    return f"{value:+.6f}"


def main() -> int:
    print("=" * 88)
    print("ADVANCED VS RETARDED FIELD PROBE")
    print("  Test: future dependence is advanced-boundary import, not retarded signaling.")
    print("=" * 88)
    print()

    detector = (3, 0)
    past_probe = (1, 0)
    future_source_on = [(5, 0, 1.0)]
    future_source_off = [(5, 0, 0.0)]
    mixed_sources = [(0, 0, 0.25), (5, 0, 1.0)]

    t_det, x_det = detector
    ret_off = retarded_field(t_det, x_det, future_source_off)
    ret_on = retarded_field(t_det, x_det, future_source_on)
    adv_off = advanced_field(t_det, x_det, future_source_off)
    adv_on = advanced_field(t_det, x_det, future_source_on)

    print(f"Detector event: t={t_det}, x={x_det}")
    print("Future source choice differs only at t=5, x=0.")
    print(f"  retarded off/on = {fmt(ret_off)} / {fmt(ret_on)}")
    print(f"  advanced off/on = {fmt(adv_off)} / {fmt(adv_on)}")
    print()

    check(
        "retarded field at earlier detector ignores future source toggle",
        math.isclose(ret_off, ret_on, abs_tol=1e-15),
        f"Delta={fmt(ret_on - ret_off)}",
    )
    check(
        "advanced field at earlier detector depends on future source toggle",
        not math.isclose(adv_off, adv_on, abs_tol=1e-15),
        f"Delta={fmt(adv_on - adv_off)}",
    )

    t_past, x_past = past_probe
    ret_past = retarded_field(t_past, x_past, mixed_sources)
    adv_past = advanced_field(t_past, x_past, mixed_sources)
    symmetric_past = 0.5 * (ret_past + adv_past)

    check(
        "retarded support uses only sources in the past cone",
        math.isclose(ret_past, 0.25, abs_tol=1e-15),
        f"retarded(t={t_past})={fmt(ret_past)}",
    )
    check(
        "half-advanced plus half-retarded imports future boundary data",
        symmetric_past > ret_past,
        f"symmetric={fmt(symmetric_past)}, retarded={fmt(ret_past)}",
    )
    check(
        "future-boundary classification is the only source of earlier dependence",
        ret_on == ret_off and adv_on != adv_off,
        "classification=advanced/final-boundary import",
    )

    print()
    print("SAFE READ")
    print("  - Retarded support does not change earlier fields when future sources change.")
    print("  - Advanced support does, because future source data were supplied to the solve.")
    print(
        "  - That is a boundary-condition import, not an operational signal inside"
        " the retained retarded framework."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
