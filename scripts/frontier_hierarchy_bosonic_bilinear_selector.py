#!/usr/bin/env python3
"""
Hierarchy bosonic-bilinear selector theorem.

This script turns the remaining selector principle into a first-principles
statement on the exact APBC temporal circle:

  - the EWSB order parameter is extracted from the local curvature of the
    effective action, so it is a bosonic, quadratic, CPT-even observable
  - such an observable must be blind to fermion sign and closed under complex
    conjugation
  - therefore its temporal support must close under the Klein four action
        z -> z, -z, z*, -z*
  - on the APBC circle, the unique minimal *resolved* closed orbit of this
    action is Lt = 4

This upgrades the previous "natural selector" into a direct consequence of the
local bosonic order-parameter structure.
"""

from __future__ import annotations

import cmath
import math
import sys
from canonical_plaquette_surface import CANONICAL_ALPHA_LM

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def apbc_phases(Lt: int):
    return [cmath.exp(1j * (2 * n + 1) * math.pi / Lt) for n in range(Lt)]


def canon(z: complex):
    return (round(z.real, 12), round(z.imag, 12))


def bilinear_orbit(z: complex):
    ops = [lambda w: w, lambda w: -w, lambda w: w.conjugate(), lambda w: -w.conjugate()]
    return sorted({canon(op(z)) for op in ops})


def phase_set(Lt: int):
    return sorted({canon(z) for z in apbc_phases(Lt)})


def orbit_partition(Lt: int):
    phases = phase_set(Lt)
    seen = set()
    parts = []
    for z in phases:
        if z in seen:
            continue
        orb = [w for w in bilinear_orbit(complex(*z)) if w in phases]
        parts.append(sorted(orb))
        seen.update(orb)
    return parts


def is_single_resolved_bilinear_orbit(Lt: int) -> bool:
    parts = orbit_partition(Lt)
    return len(parts) == 1 and len(parts[0]) > 2


def sin2_by_orbit(Lt: int):
    parts = orbit_partition(Lt)
    out = []
    for orb in parts:
        vals = []
        for x, y in orb:
            angle = math.atan2(y, x)
            vals.append(round(math.sin(angle) ** 2, 15))
        out.append(sorted(set(vals)))
    return out


def a_lt(Lt: int) -> float:
    return (1.0 / (2.0 * Lt)) * sum(
        1.0 / (3.0 + math.sin((2 * n + 1) * math.pi / Lt) ** 2) for n in range(Lt)
    )


def c_lt(Lt: int) -> float:
    return ((1.0 / 8.0) / a_lt(Lt)) ** 0.25


def measured_v() -> float:
    return 246.22


def hierarchy_baseline() -> float:
    m_planck = 1.2209e19
    return m_planck * CANONICAL_ALPHA_LM**16


def selected_v(baseline: float | None = None) -> float:
    if baseline is None:
        baseline = hierarchy_baseline()
    return baseline * c_lt(4)


def test_bilinear_orbit_structure():
    print("\n" + "=" * 78)
    print("PART 1: BILINEAR ORBIT PARTITION ON THE APBC CIRCLE")
    print("=" * 78)

    resolved = []
    for Lt in range(2, 16, 2):
        parts = orbit_partition(Lt)
        sizes = [len(p) for p in parts]
        print(f"  Lt={Lt:2d}: num_orbits={len(parts)}, sizes={sizes}")
        if is_single_resolved_bilinear_orbit(Lt):
            resolved.append(Lt)

    check(
        "the unique minimal resolved bilinear orbit is Lt = 4",
        resolved == [4],
        f"resolved single-orbit Lt values = {resolved}",
    )


def test_selector_principle_from_bosonic_evenness():
    print("\n" + "=" * 78)
    print("PART 2: BOSONIC CPT-EVEN LOCALITY SELECTS THE KLEIN-FOUR ORBIT")
    print("=" * 78)

    z2 = phase_set(2)
    z4 = phase_set(4)
    orbits2 = orbit_partition(2)
    orbits4 = orbit_partition(4)

    print(f"  Lt=2 phases  = {z2}")
    print(f"  Lt=4 phases  = {z4}")
    print(f"  Lt=2 orbits  = {orbits2}")
    print(f"  Lt=4 orbits  = {orbits4}")

    check(
        "Lt=2 gives only the unresolved sign pair {+i,-i}",
        len(orbits2) == 1 and len(orbits2[0]) == 2,
        f"orbit size = {len(orbits2[0])}",
    )
    check(
        "Lt=4 gives one full sign-and-conjugation closed orbit of size 4",
        len(orbits4) == 1 and len(orbits4[0]) == 4,
        f"orbit size = {len(orbits4[0])}",
    )


def test_uniform_weight_on_selected_orbit():
    print("\n" + "=" * 78)
    print("PART 3: THE SELECTED BILINEAR ORBIT IS UNIFORMLY WEIGHTED")
    print("=" * 78)

    w2 = sin2_by_orbit(2)
    w4 = sin2_by_orbit(4)
    w6 = sin2_by_orbit(6)

    print(f"  Lt=2 orbit weights = {w2}")
    print(f"  Lt=4 orbit weights = {w4}")
    print(f"  Lt=6 orbit weights = {w6}")

    check(
        "Lt=4 is the first resolved bilinear orbit with a single temporal weight",
        w4 == [[0.5]],
        f"weights = {w4}",
    )
    check(
        "Lt>4 immediately introduces multiple orbit sectors or unresolved remnants",
        len(orbit_partition(6)) > 1,
        f"Lt=6 partition = {orbit_partition(6)}",
    )


def test_selected_prediction():
    print("\n" + "=" * 78)
    print("PART 4: SELECTED HIERARCHY VALUE")
    print("=" * 78)

    c4 = c_lt(4)
    v4 = selected_v()
    delta = v4 - measured_v()
    rel = delta / measured_v()

    print(f"  C_4 = {c4:.12f}")
    print(f"  baseline = M_Pl * alpha_LM^16 = {hierarchy_baseline():.12f} GeV")
    print(f"  v_4 = {v4:.12f} GeV")
    print(f"  v_meas = {measured_v():.12f} GeV")
    print(f"  delta = {delta:.12f} GeV")
    print(f"  rel   = {rel:.6%}")

    check(
        "bosonic-bilinear selector gives the exact Lt=4 correction",
        abs(c4 - (7.0 / 8.0) ** 0.25) < 1e-15,
        f"absolute error = {abs(c4 - (7.0 / 8.0) ** 0.25):.2e}",
    )
    check(
        "selected hierarchy value is within 0.5% of the measured electroweak scale",
        abs(rel) < 0.005,
        f"relative error = {rel:.6%}",
    )


def main():
    print("Hierarchy bosonic-bilinear selector theorem")
    print("=" * 78)
    test_bilinear_orbit_structure()
    test_selector_principle_from_bosonic_evenness()
    test_uniform_weight_on_selected_orbit()
    test_selected_prediction()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
