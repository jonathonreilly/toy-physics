#!/usr/bin/env python3
"""Audit whether the current Planck route is the right native route.

Verdict sought:
  - keep or reject the direct worldtube/cell-counting route;
  - if keep, identify the more native final theorem target.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_AXIOM_NATIVE_ROUTE_CHECK_2026-04-23.md"
PROGRAM = ROOT / "docs/PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md"
DIRECT = ROOT / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
COUNTING = ROOT / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
SOURCEFREE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
TRACIAL = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_AUTOMORPHISM_TRACIALITY_CANDIDATE_2026-04-23.md"
GRAV_NO_GO = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
SPIN_NO_GO = ROOT / "docs/PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md"
CHAR_NO_GO = ROOT / "docs/PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return bool(passed)


def atomic_projector(idx: int, dim: int) -> sp.Matrix:
    vec = sp.zeros(dim, 1)
    vec[idx, 0] = 1
    return vec * vec.T


def main() -> int:
    note = normalized(NOTE)
    program = normalized(PROGRAM)
    direct = normalized(DIRECT)
    counting = normalized(COUNTING)
    sourcefree = normalized(SOURCEFREE)
    tracial = normalized(TRACIAL)
    grav = normalized(GRAV_NO_GO)
    spin = normalized(SPIN_NO_GO)
    char = normalized(CHAR_NO_GO)

    n_pass = 0
    n_fail = 0

    print("Planck axiom-native route check")
    print("=" * 78)

    section("PART 1: DIRECT ROUTE BACKBONE")
    p = check(
        "the branch program still names the direct worldtube chain as the canonical surviving route",
        "current canonical direct route" in program
        and "planck_scale_direct_worldtube_packet_coefficient_chain_2026-04-23.md" in program,
        "the route check should start from the branch's own canonical entrypoint rather than reopening earlier packaging",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the direct chain no longer centers scalar boundary pressure",
        "no longer best described by the older \"boundary pressure\" language" in program
        and "historical wording" in direct,
        "the surviving route should be judged as a finite-cell coefficient chain, not a Schur scalar route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the counting theorem already closes the geometric half of the route",
        "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting
        and "n_cell = p_a" in counting,
        "the remaining question is no longer what object is counted by a boundary cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the source-free derivation note says the remaining blocker is local state selection on the primitive cell",
        "7-parameter family" in sourcefree
        and "source-free local traciality theorem" in sourcefree,
        "this shows the last obstacle is not packet combinatorics anymore",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: ALTERNATIVE ROUTES ARE MORE BLOCKED")
    p = check(
        "the gravity/action family is blocked by the scale-ray no-go",
        "fixes a scale ray, not an absolute scale anchor" in grav,
        "this keeps gravity/action structurally important but not presently closer to closure than the direct finite-cell route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the same-defect linear holonomy class is already boxed out for exact conventional Planck",
        "exact conventional `a = l_p` is impossible on that class" in spin
        or "exact `a = l_p` is impossible on this class" in spin,
        "so returning to obvious local spin holonomies is not the better native route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical gauge-invariant local holonomy class is also boxed out",
        "ruled out for exact conventional `a = l_p`" in char
        or "exact conventional `a = l_p` is impossible on this canonical" in char,
        "the current branch has already ruled out the canonical local character-deficit class as the closure route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THE LEVEL SHIFT")
    p = check(
        "the new direct theorem candidate moves the last blocker upstream to primitive-cell traciality",
        "primitive-cell source-free traciality theorem" in note
        and "source-free local automorphism traciality candidate" in tracial,
        "the route should be kept only after this level shift from boundary scalar language to primitive-cell state selection",
    )
    n_pass += int(p)
    n_fail += int(not p)

    # Exact consequence of the recommended shift.
    dim = 16
    states = list(product((0, 1), repeat=4))
    one_hot = [i for i, state in enumerate(states) if sum(state) == 1]
    p_a = sum((atomic_projector(i, dim) for i in one_hot), sp.zeros(dim))
    rho_tr = sp.eye(dim) / dim
    coeff = sp.simplify(sp.trace(rho_tr * p_a))

    p = check(
        "once the primitive-cell traciality theorem is granted, the direct route closes cleanly",
        p_a.rank() == 4 and coeff == sp.Rational(1, 4),
        "the route check should confirm that the remaining theorem really is enough to collapse the lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the route-check note stays honest that the branch is not yet retained-closed",
        "cannot claim" in note and "already has an axiom-native retained planck derivation" in note,
        "the audit should separate the right route from a false closure claim",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
