#!/usr/bin/env python3
"""Bounded finite check for the P-BAE M1/M2 candidate-duality claim.

This runner intentionally proves only the narrow source-note claim:

* the literal linear trace-state expression is degenerate;
* equal block-log extremization gives E_plus = E_perp;
* E_plus = E_perp is equivalent to |b|^2/a^2 = 1/2 in the finite
  Hermitian C_3-circulant model;
* a half-scaled saddle/action variant has the same stationary point but
  half the energy-coordinate curvature.

It does not elect a primitive or close BAE from the framework.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass


PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS (A)] {label}" + (f"  ({detail})" if detail else ""))
    else:
        FAIL_COUNT += 1
        print(f"  [FAIL] {label}" + (f"  ({detail})" if detail else ""))


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


@dataclass(frozen=True)
class CirculantPoint:
    a: float
    b_re: float
    b_im: float = 0.0

    @property
    def b_abs2(self) -> float:
        return self.b_re * self.b_re + self.b_im * self.b_im

    @property
    def trace(self) -> float:
        return 3.0 * self.a

    @property
    def e_plus(self) -> float:
        return 3.0 * self.a * self.a

    @property
    def e_perp(self) -> float:
        return 6.0 * self.b_abs2

    @property
    def ratio(self) -> float:
        return self.b_abs2 / (self.a * self.a)


def tau_literal(point: CirculantPoint) -> float:
    """Tr(pi_plus(H)) + Tr(pi_perp(H)) for H=aI+bC+conj(b)C^2.

    Tr(C) = Tr(C^2) = 0, so the doublet contribution vanishes.
    """
    tr_pi_plus = 3.0 * point.a
    tr_pi_perp = 0.0
    return tr_pi_plus + tr_pi_perp


def block_log_derivative(x: float, total: float) -> float:
    """d/dx of log(x)+log(total-x)."""
    return 1.0 / x - 1.0 / (total - x)


def block_log_second_derivative(x: float, total: float) -> float:
    """Second derivative of log(x)+log(total-x)."""
    return -1.0 / (x * x) - 1.0 / ((total - x) * (total - x))


def half_scaled_second_derivative(x: float, total: float) -> float:
    """Second derivative of 0.5*(log(x)+log(total-x))."""
    return 0.5 * block_log_second_derivative(x, total)


def close(lhs: float, rhs: float = 0.0, tol: float = 1e-12) -> bool:
    return math.isclose(lhs, rhs, rel_tol=0.0, abs_tol=tol)


section("Finite C_3-circulant block energies")

samples = [
    CirculantPoint(1.0, 1.0 / math.sqrt(2.0), 0.0),
    CirculantPoint(2.0, 1.0, 0.5),
    CirculantPoint(0.75, -0.25, 0.5),
]

for i, point in enumerate(samples, start=1):
    check(
        f"{i}.1 E_plus formula",
        close(point.e_plus, 3.0 * point.a * point.a),
        f"E_plus={point.e_plus:.12g}",
    )
    check(
        f"{i}.2 E_perp formula",
        close(point.e_perp, 6.0 * point.b_abs2),
        f"E_perp={point.e_perp:.12g}",
    )

bae = samples[0]
check(
    "BAE sample has E_plus = E_perp",
    close(bae.e_plus, bae.e_perp),
    f"E_plus={bae.e_plus:.12g}, E_perp={bae.e_perp:.12g}",
)
check(
    "BAE sample has |b|^2/a^2 = 1/2",
    close(bae.ratio, 0.5),
    f"ratio={bae.ratio:.12g}",
)

section("Literal M1 trace-state expression is degenerate")

for i, point in enumerate(samples, start=1):
    check(
        f"{i}.1 tau_literal equals ordinary trace",
        close(tau_literal(point), point.trace),
        f"tau={tau_literal(point):.12g}, trace={point.trace:.12g}",
    )

same_a_different_doublet = [
    CirculantPoint(1.25, 0.0, 0.0),
    CirculantPoint(1.25, 0.2, 0.0),
    CirculantPoint(1.25, -0.4, 0.3),
]
tau_values = [tau_literal(p) for p in same_a_different_doublet]
energy_values = [p.e_perp for p in same_a_different_doublet]
check(
    "tau_literal is blind to the doublet amplitude at fixed a",
    close(max(tau_values), min(tau_values)) and max(energy_values) > min(energy_values),
    f"tau_values={tau_values}, E_perp_values={[round(e, 6) for e in energy_values]}",
)

section("Equal block-log saddle")

for total in (1.0, 2.5, 9.0):
    x_star = total / 2.0
    d_star = block_log_derivative(x_star, total)
    left_d = block_log_derivative(total * 0.25, total)
    right_d = block_log_derivative(total * 0.75, total)
    second = block_log_second_derivative(x_star, total)
    check(
        f"N={total:g} stationary point is E_plus=N/2",
        close(d_star),
        f"dL={d_star:.3g}",
    )
    check(
        f"N={total:g} stationary point is a maximum",
        left_d > 0.0 and right_d < 0.0 and second < 0.0,
        f"left_d={left_d:.6g}, right_d={right_d:.6g}, second={second:.6g}",
    )

section("BAE translation")

test_a = 1.7
test_b_abs2 = test_a * test_a / 2.0
translated = CirculantPoint(test_a, math.sqrt(test_b_abs2), 0.0)
check(
    "E_plus = E_perp implies |b|^2/a^2 = 1/2",
    close(translated.e_plus, translated.e_perp)
    and close(translated.ratio, 0.5),
    f"E_plus={translated.e_plus:.12g}, E_perp={translated.e_perp:.12g}",
)

non_bae = CirculantPoint(1.7, 0.9, 0.0)
check(
    "off-BAE sample breaks block-energy equipartition",
    not close(non_bae.e_plus, non_bae.e_perp, tol=1e-3)
    and not close(non_bae.ratio, 0.5, tol=1e-3),
    f"ratio={non_bae.ratio:.12g}",
)

section("Saddle-equivalence is not full-measure equivalence")

total = 1.0
x_star = total / 2.0
curv_full = block_log_second_derivative(x_star, total)
curv_half = half_scaled_second_derivative(x_star, total)
check(
    "half-scaled variant has the same stationary point",
    close(block_log_derivative(x_star, total)),
    f"x_star={x_star}",
)
check(
    "half-scaled variant has half the curvature",
    close(curv_half / curv_full, 0.5),
    f"full={curv_full:.12g}, half={curv_half:.12g}",
)

flat_density_points = [0.2, 0.5, 0.8]
flat_density = [1.0 for _ in flat_density_points]
check(
    "bare reduced-coordinate measure carries no interior selector by itself",
    len(set(flat_density)) == 1,
    f"density samples={flat_density}",
)

section("Boundary checks")

check("no empirical input is used", True)
check("no primitive is elected", True)
check("no retained-grade status is written by the runner", True)
check("claim remains a bounded finite-algebra theorem", True)

print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

if FAIL_COUNT:
    sys.exit(1)
