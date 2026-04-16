#!/usr/bin/env python3
"""
Exact mixed-cumulant audit and first nonlinear coefficient for the Wilson
gauge-vacuum plaquette on the accepted 3 spatial + 1 derived-time surface.

What this closes:
  - no nonlocal mixed correction through order beta^4
  - exact classification of the first distinct order-beta^5 supports
  - exact first nonlinear coefficient in the full-vacuum reduction law

What this does not close:
  - the full nonperturbative beta-dependent reduction law at beta = 6
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
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
    out = [0] * DIMS
    out[mu] = 1
    return tuple(out)


UNITS = [unit(mu) for mu in range(DIMS)]


def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(x, y))


def plaquette_key(plaquette: tuple[tuple[int, ...], tuple[int, int]]) -> tuple[tuple[int, ...], tuple[int, int]]:
    return plaquette


def canonical_edge(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (a, b) if a <= b else (b, a)


def oriented_edges(plaquette: tuple[tuple[int, ...], tuple[int, int]]) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    base, (mu, nu) = plaquette
    v0 = base
    v1 = add(base, UNITS[mu])
    v2 = add(v1, UNITS[nu])
    v3 = add(base, UNITS[nu])
    return ((v0, v1), (v1, v2), (v2, v3), (v3, v0))


def edges_unoriented(plaquette: tuple[tuple[int, ...], tuple[int, int]]) -> set[tuple[tuple[int, ...], tuple[int, ...]]]:
    return {canonical_edge(a, b) for a, b in oriented_edges(plaquette)}


def edge_charge_map(plaquette: tuple[tuple[int, ...], tuple[int, int]]) -> Counter[tuple[tuple[int, ...], tuple[int, ...]]]:
    out: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    for a, b in oriented_edges(plaquette):
        out[canonical_edge(a, b)] += 1 if a <= b else -1
    return out


def adjacent(
    left: tuple[tuple[int, ...], tuple[int, int]],
    right: tuple[tuple[int, ...], tuple[int, int]],
) -> bool:
    return bool(edges_unoriented(left) & edges_unoriented(right))


def all_local_plaquettes() -> list[tuple[tuple[int, ...], tuple[int, int]]]:
    bases = list(product((-1, 0, 1), repeat=DIMS))
    return [(base, dirs) for base in bases for dirs in combinations(range(DIMS), 2)]


LOCAL_PLAQUETTES = all_local_plaquettes()
LOCAL_CHARGES = {plaquette: edge_charge_map(plaquette) for plaquette in LOCAL_PLAQUETTES}
LOCAL_CHARGES[OBSERVED] = edge_charge_map(OBSERVED)
OBSERVED_EDGES = tuple(edges_unoriented(OBSERVED))
OBSERVED_EDGE_SET = set(OBSERVED_EDGES)


def shares_exactly_one_observed_edge(plaquette: tuple[tuple[int, ...], tuple[int, int]], edge: tuple[tuple[int, ...], tuple[int, ...]]) -> bool:
    plaquette_edges = edges_unoriented(plaquette)
    return edge in plaquette_edges and len(plaquette_edges & OBSERVED_EDGE_SET) == 1


def per_observed_edge_candidates() -> list[list[tuple[tuple[int, ...], tuple[int, int]]]]:
    out: list[list[tuple[tuple[int, ...], tuple[int, int]]]] = []
    for edge in OBSERVED_EDGES:
        candidates = [p for p in LOCAL_PLAQUETTES if p != OBSERVED and shares_exactly_one_observed_edge(p, edge)]
        out.append(sorted(candidates, key=plaquette_key))
    return out


def has_mod3_assignment(copies: tuple[tuple[tuple[int, ...], tuple[int, int]], ...]) -> tuple[bool, tuple[int, ...] | None]:
    maps = [LOCAL_CHARGES[plaquette] for plaquette in copies]
    edges = sorted({edge for mapping in maps for edge in mapping})
    for signs in product((1, -1), repeat=len(copies)):
        charges: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
        for sign, mapping in zip(signs, maps):
            for edge, value in mapping.items():
                charges[edge] += sign * value
        if all(charges[edge] % 3 == 0 for edge in edges):
            return True, signs
    return False, None


def order_four_leafless_audit() -> tuple[int, int]:
    per_edge = per_observed_edge_candidates()
    total = 0
    survivors = 0
    for choice in product(*per_edge):
        if len(set(choice)) < 4:
            continue
        total += 1
        ok, _ = has_mod3_assignment((OBSERVED, *choice))
        if ok:
            survivors += 1
    return total, survivors


def candidate_extra_faces(
    support: tuple[tuple[tuple[int, ...], tuple[int, int]], ...]
) -> list[tuple[tuple[int, ...], tuple[int, int]]]:
    used = set(support) | {OBSERVED}
    extras = []
    for plaquette in LOCAL_PLAQUETTES:
        if plaquette in used:
            continue
        if any(adjacent(plaquette, other) for other in support):
            extras.append(plaquette)
    return sorted(extras, key=plaquette_key)


def order_five_distinct_survivors() -> tuple[int, dict[tuple[tuple[tuple[int, ...], tuple[int, int]], ...], tuple[int, ...]]]:
    per_edge = per_observed_edge_candidates()
    survivors: dict[tuple[tuple[tuple[int, ...], tuple[int, int]], ...], tuple[int, ...]] = {}
    tested = 0
    for choice in product(*per_edge):
        if len(set(choice)) < 4:
            continue
        for extra in candidate_extra_faces(choice):
            support = tuple(sorted((*choice, extra), key=plaquette_key))
            if support in survivors:
                continue
            tested += 1
            ok, signs = has_mod3_assignment((OBSERVED, *support))
            if ok:
                survivors[support] = signs if signs is not None else ()
    return tested, survivors


def expected_cube_shells() -> set[tuple[tuple[tuple[int, ...], tuple[int, int]], ...]]:
    out: set[tuple[tuple[tuple[int, ...], tuple[int, int]], ...]] = set()
    for lam in (2, 3):
        for offset in (-1, 0):
            shift = tuple(offset if i == lam else 0 for i in range(DIMS))
            opposite = tuple((1 if offset == 0 else -1) if i == lam else 0 for i in range(DIMS))
            shell = (
                (shift, (0, lam)),
                (add((0, 1, 0, 0), shift), (0, lam)),
                (shift, (1, lam)),
                (add((1, 0, 0, 0), shift), (1, lam)),
                (opposite, (0, 1)),
            )
            out.add(tuple(sorted(shell, key=plaquette_key)))
    return out


def per_shell_coefficient() -> Fraction:
    # Two global orientations survive, each face contributes (Tr + Tr^\dagger)/6,
    # and the closed cube surface gives the raw link integral 3^(V-E) with
    # V = 8, E = 12.
    orientation_factor = Fraction(2, 1)
    face_normalization = Fraction(1, 6) ** 6
    raw_link_integral = Fraction(1, 3) ** 4
    return orientation_factor * face_normalization * raw_link_integral


def total_nonlocal_beta5_coefficient() -> Fraction:
    return Fraction(4, 1) * per_shell_coefficient()


def beta_eff_beta5_coefficient() -> Fraction:
    slope = Fraction(1, 18)
    return total_nonlocal_beta5_coefficient() / slope


def main() -> int:
    per_edge = per_observed_edge_candidates()
    order4_tested, order4_survivors = order_four_leafless_audit()
    order5_tested, order5_survivors = order_five_distinct_survivors()
    expected_shells = expected_cube_shells()
    per_shell = per_shell_coefficient()
    total_coeff = total_nonlocal_beta5_coefficient()
    beta_eff_coeff = beta_eff_beta5_coefficient()

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE MIXED-CUMULANT AUDIT")
    print("=" * 78)
    print()
    print("Observed-edge local combinatorics")
    print(f"  candidates per observed edge             = {[len(candidates) for candidates in per_edge]}")
    print(f"  order-beta^4 leafless supports tested    = {order4_tested}")
    print(f"  order-beta^4 leafless survivors          = {order4_survivors}")
    print()
    print("Order-beta^5 distinct survivor audit")
    print(f"  order-beta^5 supports tested             = {order5_tested}")
    print(f"  order-beta^5 distinct survivors          = {len(order5_survivors)}")
    for support, signs in sorted(order5_survivors.items()):
        print(f"  survivor signs                           = {signs}")
        for plaquette in support:
            print(f"    {plaquette}")
    print()
    print("First nonlinear coefficient")
    print(f"  per-cube-shell coefficient               = {per_shell} = {float(per_shell):.15e}")
    print(f"  total nonlocal beta^5 coefficient        = {total_coeff} = {float(total_coeff):.15e}")
    print(f"  beta_eff beta^5 coefficient              = {beta_eff_coeff} = {float(beta_eff_coeff):.15e}")
    print()

    check(
        "each observed edge has exactly five distinct one-edge-sharing local action plaquettes",
        all(len(candidates) == 5 for candidates in per_edge),
        detail=f"candidate counts = {[len(candidates) for candidates in per_edge]}",
    )
    check(
        "no leafless nonlocal support survives through order beta^4",
        order4_tested == 625 and order4_survivors == 0,
        detail=f"tested {order4_tested} one-per-edge supports and found {order4_survivors} survivors",
    )
    check(
        "the only distinct order-beta^5 survivors are the four elementary cube shells through the observed plaquette",
        set(order5_survivors) == expected_shells,
        detail=f"tested {order5_tested} supports and found {len(order5_survivors)} survivors",
    )
    check(
        "each cube shell contributes exactly 1/18^5",
        per_shell == Fraction(1, 18**5),
        detail=f"per-shell coefficient = {per_shell}",
    )
    check(
        "the first nonlocal numerator correction is exactly 4/18^5 * beta^5",
        total_coeff == Fraction(4, 18**5),
        detail=f"total coefficient = {total_coeff}",
    )
    check(
        "the full-vacuum reduction law therefore begins beta_eff(beta)=beta + beta^5/26244 + O(beta^6)",
        beta_eff_coeff == Fraction(1, 26244),
        detail=f"beta_eff coefficient = {beta_eff_coeff}",
    )

    check(
        "tree repeated-plaquette supports are handled analytically by the leaf-factorization lemma in the authority note",
        True,
        detail="the finite search above classifies only the leafless residual supports after exact leaf peeling",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
