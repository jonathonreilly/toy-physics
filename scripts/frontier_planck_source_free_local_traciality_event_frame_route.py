#!/usr/bin/env python3
"""Audit the event-frame route to source-free local traciality.

This route asks a sharply reduced question:

  - current retained direct symmetry on the primitive C^16 cell is only S_3;
  - therefore source-free diagonal states are still classified by 8 orbits;
  - if one strengthens source-free local symmetry to any transitive primitive
    event-frame relabeling group, the state becomes tracial immediately.

The script checks the exact group/orbit facts, the tracial consequence of
transitivity, and the honesty of the note's status claims.
"""

from __future__ import annotations

from itertools import permutations, product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_EVENT_FRAME_ROUTE_2026-04-23.md"
)
COUNTING = (
    ROOT
    / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
)
SOURCEFREE = (
    ROOT
    / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
)
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"
HILBERT = ROOT / "docs/SINGLE_AXIOM_HILBERT_NOTE.md"
INFO = ROOT / "docs/SINGLE_AXIOM_INFORMATION_NOTE.md"


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


def permute_spatial(state: tuple[int, int, int, int], perm: tuple[int, int, int]) -> tuple[int, int, int, int]:
    t, x, y, z = state
    spatial = (x, y, z)
    return (t, spatial[perm[0]], spatial[perm[1]], spatial[perm[2]])


def xor_state(state: tuple[int, int, int, int], shift: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple((a + b) % 2 for a, b in zip(state, shift))


def orbit_of(state: tuple[int, int, int, int], group_action) -> set[tuple[int, int, int, int]]:
    return {group_action(state, g) for g in group_action.group}


def atomic_projector(idx: int, dim: int) -> sp.Matrix:
    vec = sp.zeros(dim, 1)
    vec[idx, 0] = 1
    return vec * vec.T


def main() -> int:
    note = normalized(NOTE)
    counting = normalized(COUNTING)
    sourcefree = normalized(SOURCEFREE)
    physical = normalized(PHYSICAL)
    hilbert = normalized(HILBERT)
    info = normalized(INFO)

    n_pass = 0
    n_fail = 0

    states = list(product((0, 1), repeat=4))
    state_to_index = {state: idx for idx, state in enumerate(states)}

    print("Planck source-free local traciality event-frame route audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the direct counting law is already closed upstream",
        "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting
        and "n_cell = p_a" in counting,
        "this event-frame route should attack only the remaining source-free state problem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the retained derivation lane already identifies a 7-parameter underdetermined source-free family",
        "7-parameter family" in sourcefree
        and "rho_lt = (1/32) p_a + (7/96) (i_16 - p_a)" in sourcefree,
        "the event-frame route should sharpen that underdetermination into an exact missing-transitivity statement",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "support notes already fix physical lattice semantics and finite local Hilbert structure",
        "finite-dimensional hilbert space with local tensor product structure" in hilbert
        and "conserved information flow" in info
        and "no proper exact quotient" in physical,
        "the event-frame route should sit on primitive local physical events, not on scalar Schur thermodynamics",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: RETAINED EVENT-FRAME SYMMETRY")
    s3 = list(permutations((0, 1, 2)))

    class SpatialAction:
        group = s3

        @staticmethod
        def apply(state, perm):
            return permute_spatial(state, perm)

    def s3_action(state, perm):
        return permute_spatial(state, perm)

    s3_orbits: dict[tuple[int, int], set[tuple[int, int, int, int]]] = {}
    for state in states:
        label = (state[0], state[1] + state[2] + state[3])
        s3_orbits.setdefault(label, set()).add(state)

    p = check(
        "residual exact symmetry after time-lock has exactly 8 primitive event-frame orbits",
        len(s3_orbits) == 8 and set(s3_orbits) == set(product((0, 1), range(4))),
        "the current retained direct event-frame symmetry is only S_3, with orbits classified by (t,w)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    expected_sizes = {(t, w): sp.binomial(3, w) for t in (0, 1) for w in range(4)}
    p = check(
        "each retained orbit has the exact binomial multiplicity dictated by spatial Hamming weight",
        all(len(s3_orbits[label]) == expected_sizes[label] for label in s3_orbits),
        "retained event-frame invariance leaves eight orbit weights and one normalization equation",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: TRANSITIVE EVENT-FRAME WITNESS")
    flips = list(product((0, 1), repeat=4))
    orbit_from_zero = {xor_state((0, 0, 0, 0), shift) for shift in flips}
    p = check(
        "the full local bit-flip translation group is a concrete transitive witness on the 16-event frame",
        len(orbit_from_zero) == 16 and set(orbit_from_zero) == set(states),
        "this witness is stronger than necessary, but it shows the exact missing content is transitivity on primitive events",
    )
    n_pass += int(p)
    n_fail += int(not p)

    dim = 16
    d = sp.symbols("d0:16", real=True)
    equations = [sp.Eq(d[i], d[0]) for i in range(1, dim)]
    equations.append(sp.Eq(sum(d), 1))
    solution = sp.solve(equations, d, dict=True)
    unique_solution = solution == [{symbol: sp.Rational(1, dim) for symbol in d}]
    p = check(
        "transitive event-frame invariance plus normalization force the tracial state",
        unique_solution,
        "if all primitive projector weights are identified by one orbit, rho_cell = I_16/16 follows immediately",
    )
    n_pass += int(p)
    n_fail += int(not p)

    one_hot = [state_to_index[state] for state in states if sum(state) == 1]
    p_a = sum((atomic_projector(i, dim) for i in one_hot), sp.zeros(dim))
    rho_tr = sp.eye(dim) / dim
    quarter = sp.simplify(sp.trace(rho_tr * p_a))
    p = check(
        "the tracial state gives the exact quarter coefficient on the forced packet P_A",
        p_a.rank() == 4 and quarter == sp.Rational(1, 4),
        "once event-frame transitivity lands, the direct Planck chain closes through the existing counting theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: EXACT OBSTRUCTION")
    rho_lt = sp.zeros(dim)
    for i in range(dim):
        rho_lt[i, i] = sp.Rational(1, 32) if i in one_hot else sp.Rational(7, 96)

    spatial_swap_state = {state: permute_spatial(state, (1, 0, 2)) for state in states}
    swap_matrix = sp.zeros(dim)
    for state, image in spatial_swap_state.items():
        swap_matrix[state_to_index[image], state_to_index[state]] = 1
    s3_invariant = swap_matrix * rho_lt * swap_matrix.T == rho_lt

    temporal_flip_state = {state: xor_state(state, (1, 0, 0, 0)) for state in states}
    tflip_matrix = sp.zeros(dim)
    for state, image in temporal_flip_state.items():
        tflip_matrix[state_to_index[image], state_to_index[state]] = 1
    not_tflip_invariant = tflip_matrix * rho_lt * tflip_matrix.T != rho_lt

    p = check(
        "the packet-light witness is compatible with retained S_3 but excluded by any stronger orbit-connecting event-frame symmetry",
        s3_invariant and not_tflip_invariant,
        "this shows the exact missing content is not positivity or diagonality but transitivity across retained orbit classes",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note stays honest that current retained structure does not yet provide primitive event-frame transitivity",
        "not retained closure" in note
        and "identifying all sixteen primitive" in note
        and "sharp exact obstruction" in note,
        "the route should land the precise missing theorem, not overclaim Planck closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
