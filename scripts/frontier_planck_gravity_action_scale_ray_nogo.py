#!/usr/bin/env python3
"""Audit the gravity/action scale-ray no-go theorem honestly.

This is not a derivation harness. It checks two things:
  - the repo evidence still leaves SI/GeV conversion externally anchored
  - the current admitted gravity/action relations are homogeneous under one
    global unit-map rescaling, so they fix a scale ray rather than an
    absolute anchor
"""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
GRAVITY = ROOT / "docs/GRAVITY_CLEAN_DERIVATION_NOTE.md"
ACTION = ROOT / "docs/ACTION_NORMALIZATION_NOTE.md"
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"
PROGRAM = ROOT / "docs/PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split()).lower()


def main() -> int:
    note = normalized(read_text(NOTE))
    gravity = normalized(read_text(GRAVITY))
    action = normalized(read_text(ACTION))
    physical = normalized(read_text(PHYSICAL))
    program = normalized(read_text(PROGRAM))

    n_pass = 0
    n_fail = 0

    print("Planck gravity/action scale-ray no-go audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY EVIDENCE")
    p = check(
        "gravity note still stops at lattice units",
        "g_n = 1/(4 pi) in lattice units" in gravity
        and "converting to si requires one calibration" in gravity,
        "the retained gravity chain still needs one physical length anchor",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "action normalization still exposes a rescaling degeneracy",
        "rescaling degeneracy" in action
        and "define g as newton's constant" in action,
        "the weak-field coefficient note still fixes normalization only after observational naming of G",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "physical-lattice necessity kills regulator reinterpretation, not the unit-map ray",
        "physical-lattice reading is the unique surviving interpretation" in physical
        and "not an equivalent reading of the same accepted framework surface" in physical,
        "the lattice is physical, but that does not by itself fix the meter/GeV conversion",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "program note still classifies gravity/action as the best open route",
        "best open route" in program and "physical unit map" in program,
        "the branch still treats this as the live theorem target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: HOMOGENEOUS SCALE-RAY CHECKS")
    lambdas = [0.25, 0.5, 1.0, 2.0, 4.0]
    g_lat = 1.0 / (4.0 * math.pi)
    m_lat = 3.0
    r_lat = 11.0
    av_lat = 2.017223509629975847e-17
    vol4_lat = 250.0
    curv_lat = 0.02
    lambda_lat = 0.003
    mg_lat = math.sqrt(2.0 * lambda_lat)

    phi_values = []
    action_values = []
    av_values = []
    mg_ratio_values = []
    gv2_values = []

    print("  lambda        GM/r          S_EH       a*v      m_g^2/Lambda        G v^2")
    for lam in lambdas:
        a = lam
        g_phys = (a**2) * g_lat
        m_phys = m_lat / a
        r_phys = a * r_lat
        v_phys = av_lat / a
        vol4_phys = (a**4) * vol4_lat
        curv_phys = curv_lat / (a**2)
        lambda_phys = lambda_lat / (a**2)
        mg_phys = mg_lat / a

        phi = g_phys * m_phys / r_phys
        s_eh = (vol4_phys * curv_phys) / (16.0 * math.pi * g_phys)
        av = a * v_phys
        mg_ratio = (mg_phys**2) / lambda_phys
        gv2 = g_phys * (v_phys**2)

        phi_values.append(phi)
        action_values.append(s_eh)
        av_values.append(av)
        mg_ratio_values.append(mg_ratio)
        gv2_values.append(gv2)

        print(
            f"  {lam:>6.2f}  {phi:>12.8f}  {s_eh:>12.8f}  "
            f"{av:>8.3e}  {mg_ratio:>12.8f}  {gv2:>12.3e}"
        )

    tol = 1e-12
    p = check(
        "Newton potential GM/r is invariant along the scale ray",
        max(abs(x - phi_values[0]) for x in phi_values) < tol,
        "the weak-field dimensionless gravity observable does not pick lambda",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Einstein-Hilbert-style action is invariant along the scale ray",
        max(abs(x - action_values[0]) for x in action_values) < tol,
        "the coefficient 1/G and the measure-curvature factor cancel exactly under engineering scaling",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "hierarchy product a*v is invariant",
        max(abs(x - av_values[0]) for x in av_values) < 1e-28,
        "the hierarchy lane fixes only the product, not the absolute scale",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "graviton spectral-gap ratio m_g^2/Lambda is invariant",
        max(abs(x - mg_ratio_values[0]) for x in mg_ratio_values) < tol
        and abs(mg_ratio_values[0] - 2.0) < tol,
        "the retained compactness identity lives on the same scale ray",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "dimensionless cross-lane combination G v^2 is invariant",
        max(abs(x - gv2_values[0]) for x in gv2_values) < 1e-24,
        "gravity plus hierarchy still does not pick lambda",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THEOREM NOTE VERDICT")
    p = check(
        "note states that the current family fixes a scale ray, not an anchor",
        "fixes a scale ray, not an absolute scale anchor" in note
        and "no intrinsic absolute anchor for `a`" in note,
        "the note must state the no-go explicitly rather than hint at it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note requires a new non-homogeneous unit-bearing observable for progress",
        (
            "new non-homogeneous, unit-bearing same-surface observable" in note
            or "new non-homogeneous unit-bearing same-surface observable" in note
            or "unit-bearing same-surface theorem" in note
        ),
        "this is the sharpened next theorem target after the no-go",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Current admitted gravity/action package is homogeneous under one "
        "global unit-map rescaling. It fixes a SCALE RAY, not an absolute "
        "Planck anchor. Absolute a remains PINNED_OBSERVABLE until a new "
        "unit-bearing same-surface theorem lands."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
