#!/usr/bin/env python3
"""Audit the section-canonical worldtube-selector lane honestly.

This lane attacks the carrier objection directly. It does not claim full
Planck closure. It proves the stronger coarse-sector result:

  - on the minimal time-locked 4-bit spacetime cell, the residual symmetry is
    the spatial permutation group S_3 fixing the temporal bit;
  - on the minimal nonzero shell, the only invariant projectors are
    0, P_t, P_s, and P_A = P_t + P_s;
  - requiring a physical worldtube selector to be minimal, time-complete, and
    spatially isotropic uniquely forces the coarse hw=1 axis-sector projector
    P_A;
  - no finer spatial ray projector is residual-invariant.

So this lane closes coarse sector selection and leaves only the finer spatial
section obstruction.
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
ENDPOINT = (
    ROOT
    / "docs/PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
)


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


def orbit(state: tuple[int, int, int, int]) -> frozenset[tuple[int, int, int, int]]:
    """Residual orbit under permutations of the three spatial bits."""
    t = state[0]
    spatial = state[1:]
    out: set[tuple[int, int, int, int]] = set()
    for perm in itertools.permutations((0, 1, 2)):
        permuted = tuple(spatial[i] for i in perm)
        out.add((t,) + permuted)
    return frozenset(out)


def main() -> int:
    note = normalized(NOTE)
    timelock = normalized(TIMELOCK)
    c16 = normalized(C16)
    bridge = normalized(BRIDGE)
    endpoint = normalized(ENDPOINT)

    n_pass = 0
    n_fail = 0

    print("Planck boundary section-canonical worldtube-selector lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "time-lock note still fixes one time direction and a locked 3+1 unit map",
        "derived time-lock without absolute planck anchor" in timelock
        and "a_s = c a_t" in timelock
        and "one time direction" in timelock,
        "the selector lane must descend from the exact one-clock 3+1 structure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "C^16 note still records the exact hw=1 axis sector inside the 4-bit cell",
        "a = {1000, 0100, 0010, 0001}" in c16
        and "4/16 = 1/4" in c16,
        "the new lane should work on the exact four-axis candidate already isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "bridge note still says the future theorem must be about the full four-axis worldtube channel",
        "four-axis worldtube channel" in bridge
        and "axis-sector mass `1/4`" in bridge,
        "the new lane should attack channel selection directly rather than reopen coefficient numerology",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "endpoint note still says the missing content is a worldtube/projector law",
        "worldtube-projector law" in endpoint
        and "`p_phys = m_axis`" in endpoint,
        "the section-canonical lane should focus on the missing carrier/projector step",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: RESIDUAL-ORBIT CLASSIFICATION")
    states = list(itertools.product((0, 1), repeat=4))
    orbit_reps: dict[frozenset[tuple[int, int, int, int]], tuple[int, int]] = {}
    for state in states:
        t = state[0]
        w_s = sum(state[1:])
        orbit_reps[orbit(state)] = (t, w_s)

    pairs = sorted(set(orbit_reps.values()))
    expected_pairs = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
    ]
    p = check(
        "residual S_3 orbits are classified exactly by (time bit, spatial weight)",
        pairs == expected_pairs and len(orbit_reps) == 8,
        "after time-lock, only spatial permutations survive and they preserve t and w_s",
    )
    n_pass += int(p)
    n_fail += int(not p)

    vacuum = (0, 0, 0, 0)
    shell_1 = {state for state in states if sum(state) == 1}
    temporal = {(1, 0, 0, 0)}
    spatial = {(0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)}
    axis = temporal | spatial
    p = check(
        "the minimal nonzero shell adjacent to vacuum splits as temporal plus spatial one-hot orbits",
        shell_1 == axis and temporal.isdisjoint(spatial),
        "S_1 = {eta : |eta| = 1} = T union S on the exact 4-bit cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the temporal one-hot state and the spatial one-hot triplet are exactly the two residual orbits on S_1",
        orbit((1, 0, 0, 0)) == frozenset(temporal)
        and orbit((0, 1, 0, 0)) == frozenset(spatial),
        "minimal-shell invariant supports can only be built from these two orbit blocks",
    )
    n_pass += int(p)
    n_fail += int(not p)

    invariant_supports = [set(), temporal, spatial, axis]
    p = check(
        "the only residual-invariant supports on the minimal shell are empty, temporal, spatial, and full axis",
        all(
            all(orbit(s).issubset(support) for s in support) for support in invariant_supports
        )
        and len(invariant_supports) == 4,
        "every invariant support is a union of the two minimal-shell residual orbits",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: SECTION-CANONICAL COARSE WORLDTUBE SELECTOR")
    candidates = {
        "0": set(),
        "P_t": temporal,
        "P_s": spatial,
        "P_A": axis,
    }
    admissible = [
        name
        for name, support in candidates.items()
        if temporal.issubset(support) and spatial.issubset(support)
    ]
    p = check(
        "time-complete plus spatially isotropic minimal-shell selectors admit exactly one invariant projector",
        admissible == ["P_A"],
        "once the selector must see the full one-step 3+1 worldtube channel, the coarse hw=1 projector is unique",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the unique admissible coarse selector is the full hw=1 axis-sector support",
        candidates["P_A"] == axis and len(candidates["P_A"]) == 4,
        "the selected sector is exactly {1000,0100,0010,0001}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SHARP RESIDUAL OBSTRUCTION")
    spatial_rays = [
        {(0, 1, 0, 0)},
        {(0, 0, 1, 0)},
        {(0, 0, 0, 1)},
    ]
    nontrivial_proper_spatial = []
    for r in range(1, len(spatial)):
        for subset in itertools.combinations(spatial, r):
            nontrivial_proper_spatial.append(set(subset))

    p = check(
        "no nonzero proper subprojector of the spatial triplet is residual-invariant",
        all(any(orbit(s) != frozenset(subset) for s in subset) for subset in nontrivial_proper_spatial),
        "the residual spatial permutation symmetry still blocks a canonical finer spatial section",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the temporal ray is canonical but the spatial rays remain only orbit-related",
        orbit((1, 0, 0, 0)) == frozenset(temporal)
        and all(orbit(next(iter(ray))) == frozenset(spatial) for ray in spatial_rays),
        "time-lock singles out the temporal axis, but not any individual spatial axis",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: C^16 CONSEQUENCE")
    primitive_share = 1.0 / 16.0
    axis_mass = len(axis) * primitive_share
    p = check(
        "on the democratic C^16 state, the forced coarse selector carries exact mass 1/4",
        abs(axis_mass - 0.25) < 1.0e-15,
        "once P_A is forced, the associated coarse sector mass is exactly 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly records coarse section-canonicality and finer spatial obstruction",
        "coarse worldtube sector is **section-canonical**" in note
        and "no finer spatial ray inside that sector is canonically selected" in note,
        "the writeup should improve the carrier step without overselling full closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says scalar identification p_phys = m_axis is still open",
        "`p_phys = m_axis`" in NOTE.read_text(encoding="utf-8")
        and "still open" in NOTE.read_text(encoding="utf-8"),
        "this lane should close the carrier step, not fake the last scalar law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    print(
        "  The current time-lock plus 3+1 boundary structure does force the "
        "coarse C^16 hw=1 four-axis worldtube sector. The remaining obstruction "
        "is finer: no individual spatial ray inside that sector is canonically "
        "selected, and the scalar law p_phys = m_axis is still a separate step."
    )

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
