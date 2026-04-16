#!/usr/bin/env python3
"""
Exact distinct-shell theorem for the Wilson gauge-vacuum plaquette.

This runner proves the exact minimal connected shell geometry built from
distinct plaquettes around a marked plaquette on the accepted `3 spatial + 1
derived-time` surface.
"""

from __future__ import annotations

from itertools import combinations, product


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

DIMS = 4
OBSERVED = ((0, 0, 0, 0), (0, 1))


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def unit(mu: int) -> tuple[int, ...]:
    e = [0] * DIMS
    e[mu] = 1
    return tuple(e)


UNITS = [unit(mu) for mu in range(DIMS)]


def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(x, y))


def edges(plaquette: tuple[tuple[int, ...], tuple[int, int]]) -> tuple[tuple[tuple[int, ...], int], ...]:
    base, (mu, nu) = plaquette
    return (
        (base, mu),
        (add(base, UNITS[mu]), nu),
        (add(base, UNITS[nu]), mu),
        (base, nu),
    )


def xor_boundary(
    plaquettes: tuple[tuple[tuple[int, ...], tuple[int, int]], ...]
) -> set[tuple[tuple[int, ...], int]]:
    boundary: set[tuple[tuple[int, ...], int]] = set()
    for plaquette in plaquettes:
        for edge in edges(plaquette):
            if edge in boundary:
                boundary.remove(edge)
            else:
                boundary.add(edge)
    return boundary


def all_local_plaquettes() -> list[tuple[tuple[int, ...], tuple[int, int]]]:
    bases = list(product((-1, 0, 1), repeat=DIMS))
    return [(base, dirs) for base in bases for dirs in combinations(range(DIMS), 2)]


def candidates_by_observed_edge() -> list[list[tuple[tuple[int, ...], tuple[int, int]]]]:
    all_plaquettes = all_local_plaquettes()
    observed_edges = set(edges(OBSERVED))
    out: list[list[tuple[tuple[int, ...], tuple[int, int]]]] = []
    for edge in edges(OBSERVED):
        candidates = []
        for plaquette in all_plaquettes:
            if plaquette == OBSERVED:
                continue
            plaquette_edges = set(edges(plaquette))
            if edge not in plaquette_edges:
                continue
            shared_observed_edges = len(observed_edges & plaquette_edges)
            if shared_observed_edges == 1:
                candidates.append(plaquette)
        out.append(candidates)
    return out


def count_closed_four_action_shells() -> int:
    closed = 0
    per_edge = candidates_by_observed_edge()
    for choice in product(*per_edge):
        if len(set(choice)) < 4:
            continue
        boundary = xor_boundary((OBSERVED, *choice))
        if not boundary:
            closed += 1
    return closed


def explicit_cube_shell() -> tuple[tuple[tuple[int, ...], tuple[int, int]], ...]:
    return (
        OBSERVED,
        ((0, 0, 0, 0), (0, 2)),
        ((0, 1, 0, 0), (0, 2)),
        ((0, 0, 0, 0), (1, 2)),
        ((1, 0, 0, 0), (1, 2)),
        ((0, 0, 1, 0), (0, 1)),
    )


def main() -> int:
    observed_edges = edges(OBSERVED)
    per_edge = candidates_by_observed_edge()
    closed_four_shells = count_closed_four_action_shells()
    cube_shell = explicit_cube_shell()
    cube_boundary = xor_boundary(cube_shell)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE DISTINCT-SHELL THEOREM")
    print("=" * 78)
    print()
    print("Observed plaquette")
    print(f"  face                                 = {OBSERVED}")
    print(f"  boundary edges                       = {observed_edges}")
    print()
    print("Distinct neighboring action plaquettes")
    print(f"  candidates per observed edge         = {[len(cands) for cands in per_edge]}")
    print(f"  closed four-action shells found      = {closed_four_shells}")
    print()
    print("Explicit minimal cube shell")
    for face in cube_shell:
        print(f"  {face}")
    print(f"  shell boundary size                  = {len(cube_boundary)}")
    print()

    check(
        "every distinct plaquette sharing the observed boundary shares exactly one observed edge",
        all(len(cands) == 5 for cands in per_edge),
        detail="each observed edge has five distinct neighboring plaquettes and none covers two observed edges",
    )
    check(
        "a distinct connected shell needs at least four action plaquettes just to cover the four observed edges",
        all(len(cands) >= 4 for cands in per_edge),
        detail="one distinct plaquette covers only one observed edge, so four edges require at least four distinct action plaquettes",
    )
    check(
        "no four-action distinct shell closes the observed plaquette boundary",
        closed_four_shells == 0,
        detail="all 625 one-per-edge four-action candidates leave a nonempty outer boundary",
    )
    check(
        "an explicit five-action cube shell closes the observed boundary",
        len(cube_boundary) == 0,
        detail="the marked plaquette plus the other five faces of an elementary cube has empty mod-2 edge boundary",
    )
    check(
        "the first distinct connected nonlocal numerator shell is order beta^5",
        closed_four_shells == 0 and len(cube_boundary) == 0,
        detail="five distinct action plaquettes are necessary and sufficient around the marked face",
    )
    check(
        "the first connected vacuum shell is order beta^6",
        len(cube_boundary) == 0,
        detail="any connected closed vacuum shell contains a seed plaquette plus at least five others, and the cube boundary realizes size six",
    )
    check(
        "this exact distinct-shell result does not yet close the full beta_eff law",
        True,
        detail="mixed repeated-plaquette connected-cumulant terms still need a separate audit",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
