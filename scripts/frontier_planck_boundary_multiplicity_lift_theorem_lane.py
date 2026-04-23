#!/usr/bin/env python3
"""Audit the boundary multiplicity-lift lane honestly.

This lane does not claim retained Planck closure. It proves the sharper
carrier-level statement:

  - the physical coarse worldtube selector is the full axis projector P_A;
  - the minimal Schur carrier only sees the quotient projector P_q;
  - the invisible complement is an exact rank-2 doublet block P_E;
  - no proper exact quotient on the retained observable sector is admissible;
  - under the democratic C^16 state, P_q and P_E carry equal mass 1/8;
  - therefore the full lifted worldtube mass is exactly
      Tr(rho P_A) = 2 Tr(rho P_q) = 1/4.

So the multiplicity/lift factor 2 is closed. The remaining open step is only
the scalar law identifying physical boundary pressure with the lifted mass.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
SECTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
INTERTWINER = ROOT / "docs/PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md"
BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
AXIS = ROOT / "docs/PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def main() -> int:
    note = normalized(NOTE)
    section_note = normalized(SECTION)
    intertwiner = normalized(INTERTWINER)
    bridge = normalized(BRIDGE)
    axis = normalized(AXIS)
    physical = normalized(PHYSICAL)

    n_pass = 0
    n_fail = 0

    print("Planck boundary multiplicity-lift lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "section-canonical lane still forces the physical coarse selector onto P_A",
        "coarse four-axis worldtube channel is **section-canonical**" in section_note
        and "forced onto the coarse `hw=1` four-axis worldtube channel" in section_note,
        "the multiplicity lift should start from the full physical coarse worldtube sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "intertwiner lane still says the minimal Schur carrier only sees the rank-2 quotient P_q",
        "canonical quotient projector is" in intertwiner
        and "tr(rho_cell p_q) = rank(p_q) / 16 = 2/16 = 1/8" in intertwiner,
        "the visible Schur block should still be the quotient mass 1/8",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "C^16 bridge/endpoint lanes still isolate the full axis mass as 1/4",
        "m_axis = tr(rho_cell p_a) = 1/4" in bridge
        and "m_axis = tr(rho_cell p_a) = 1/4" in axis,
        "the lift theorem should recover the existing quarter exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "physical-lattice note still forbids proper exact quotienting of retained observable sectors",
        "no proper exact quotient/rooting/reduction" in physical
        and "physical-species semantics" in physical,
        "the invisible doublet cannot be dismissed as gauge redundancy if the full sector is physical",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT AXIS-CARRIER DECOMPOSITION")
    t = sp.Matrix([1, 0, 0, 0])
    x = sp.Matrix([0, 1, 0, 0])
    y = sp.Matrix([0, 0, 1, 0])
    z = sp.Matrix([0, 0, 0, 1])
    s = (x + y + z) / sp.sqrt(3)
    e1 = (x - y) / sp.sqrt(2)
    e2 = (x + y - 2 * z) / sp.sqrt(6)

    basis = sp.Matrix.hstack(t, s, e1, e2)
    p_q = sp.simplify(t * t.T + s * s.T)
    p_e = sp.simplify(e1 * e1.T + e2 * e2.T)
    p_a = sp.eye(4)

    p = check(
        "the axis carrier basis {t,s,e1,e2} is orthonormal and complete",
        sp.simplify(basis.T * basis - sp.eye(4)) == sp.zeros(4),
        "the full four-axis carrier splits into the visible quotient block and the invisible doublet block",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "P_q is the exact rank-2 quotient projector",
        p_q.rank() == 2 and sp.simplify(p_q * p_q - p_q) == sp.zeros(4),
        "the quotient block is span{|t>,|s>}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "P_E is the exact rank-2 invisible doublet projector",
        p_e.rank() == 2 and sp.simplify(p_e * p_e - p_e) == sp.zeros(4),
        "the invisible block is the S_3 doublet complement inside the spatial triplet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "P_q and P_E are orthogonal complementary projectors",
        sp.simplify(p_q * p_e) == sp.zeros(4) and sp.simplify(p_q + p_e - p_a) == sp.zeros(4),
        "the full physical coarse sector is exactly the quotient block plus its invisible complement",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the full axis projector has rank 4 while each block has rank 2",
        p_a.rank() == 4 and p_q.rank() == 2 and p_e.rank() == 2,
        "the missing factor 2 is already visible at the level of exact block dimensions",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: REPRESENTATION-THEORETIC CONTENT")
    perm_xy = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    perm_yz = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )

    p = check(
        "the quotient block is permutation-blind",
        perm_xy * t == t
        and perm_yz * t == t
        and sp.simplify(perm_xy * s - s) == sp.zeros(4, 1)
        and sp.simplify(perm_yz * s - s) == sp.zeros(4, 1),
        "this is exactly the information visible to the minimal Schur carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the invisible block is a genuine nontrivial doublet, not zero",
        sp.simplify(perm_xy * e1 - e1) != sp.zeros(4, 1)
        and sp.simplify(perm_yz * e2 - e2) != sp.zeros(4, 1),
        "the hidden multiplicity is real representation content, not a null sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "discarding P_E would be a proper exact reduction of the full physical sector",
        p_e != sp.zeros(4) and p_q.rank() < p_a.rank(),
        "once P_A is the physical coarse selector, keeping only P_q really does drop exact sector content",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: DEMOCRATIC MASS LIFT")
    rho_axis = sp.eye(4) / 16
    mass_q = sp.simplify(sp.trace(rho_axis * p_q))
    mass_e = sp.simplify(sp.trace(rho_axis * p_e))
    mass_a = sp.simplify(sp.trace(rho_axis * p_a))

    p = check(
        "the quotient block carries exact democratic mass 1/8",
        mass_q == sp.Rational(1, 8),
        "this is the best canonical Schur-visible mass already isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the invisible doublet carries the same democratic mass 1/8",
        mass_e == sp.Rational(1, 8),
        "the hidden multiplicity contributes exactly as much mass as the visible quotient block",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the full lifted worldtube mass is exactly 1/4",
        mass_a == sp.Rational(1, 4),
        "lifting from P_q to the full section-canonical sector restores the quarter exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the multiplicity lift law is exactly m_lift = 2 * m_q",
        sp.simplify(mass_a - 2 * mass_q) == 0,
        "the missing factor of 2 is now a theorem, not a guessed normalization",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the factor of 2 is simultaneously the rank ratio rank(P_A)/rank(P_q)",
        p_a.rank() / p_q.rank() == 2,
        "the mass lift follows from exact equal-dimensional completion of the quotient block",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: HONEST SCIENTIFIC ENDPOINT")
    p = check(
        "this lane closes multiplicity but not the scalar pressure-identification law",
        "still open:" in note
        and "scalar identification" in note
        and "`p_phys = tr(rho_cell p_a)`" in note,
        "the remaining burden is only to identify physical boundary pressure with the lifted worldtube mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action-language restatement is still nu = lambda_min(L_sigma) + m_lift = 5/4",
        "nu = lambda_min(l_sigma) + m_lift = 5/4" in note,
        "the new theorem should reduce the action lane to the same final scalar law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass}/{n_pass + n_fail} PASS")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
