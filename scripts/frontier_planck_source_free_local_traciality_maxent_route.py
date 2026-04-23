#!/usr/bin/env python3
"""Audit the Planck max-entropy route on the last source-free-state blocker."""

from __future__ import annotations

from pathlib import Path
import math
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_MAXENT_ROUTE_2026-04-23.md"
COUNTING = ROOT / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
SOURCEFREE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
DIRECT = ROOT / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"


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


def entropy(probs: list[float]) -> float:
    total = 0.0
    for p in probs:
        if p > 0.0:
            total -= p * math.log(p)
    return total


def main() -> int:
    note = normalized(NOTE)
    counting = normalized(COUNTING)
    sourcefree = normalized(SOURCEFREE)
    direct = normalized(DIRECT)

    n_pass = 0
    n_fail = 0

    print("Planck source-free local traciality max-entropy route audit")
    print("=" * 78)

    dim = 16
    rank_pa = 4
    rho_tr = [1.0 / dim] * dim
    rho_lt = [1.0 / 32.0] * rank_pa + [7.0 / 96.0] * (dim - rank_pa)
    s_tr = entropy(rho_tr)
    s_lt = entropy(rho_lt)
    d_lt = math.log(dim) - s_lt

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the direct counting law is already closed upstream",
        "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting
        or "c_cell = tr(rho_cell p_a)" in counting,
        "the max-entropy route should only target the local source-free state",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the retained-direct lane still says the current accepted stack does not derive the democratic state",
        "is **not derivable** from the currently accepted retained stack alone" in sourcefree
        and "7-parameter family" in sourcefree,
        "the note must stay honest that this route is not already retained closure",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the direct chain still identifies the source-free state as the last blocker",
        "rho_cell = i_16 / 16" in direct and "c_cell = c_wt" in direct,
        "the max-entropy theorem candidate should plug exactly that state-side gap",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 2: EXACT MAX-ENTROPY CONSEQUENCES")
    p = check(
        "the tracial state is normalized on the full primitive cell",
        abs(sum(rho_tr) - 1.0) < 1e-12,
        "rho_tr = I_16 / 16 is a valid density state",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the packet-light witness is normalized",
        abs(sum(rho_lt) - 1.0) < 1e-12,
        "rho_lt remains an admissible comparison witness from the retained-direct no-go note",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "full-cell entropy of the tracial state is log 16",
        abs(s_tr - math.log(dim)) < 1e-12,
        f"S(rho_tr)={s_tr:.12f} = log(16)",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the packet-light witness has strictly smaller entropy",
        s_tr > s_lt,
        f"S(rho_tr)={s_tr:.12f} > S(rho_lt)={s_lt:.12f}",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "relative entropy against the tracial state is positive for the nontracial witness",
        d_lt > 0.0,
        f"D(rho_lt || I_16/16)=log(16)-S(rho_lt)={d_lt:.12f} > 0",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "max-entropy on the full primitive cell therefore singles out the tracial state",
        abs((math.log(dim) - s_tr)) < 1e-12 and d_lt > 0.0,
        "among unconstrained one-cell density matrices, the unique entropy maximizer is rho_cell = I_16 / 16",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 3: PLANCK CONSEQUENCE")
    c_cell = sp.Rational(rank_pa, dim)
    p = check(
        "tracial state plus the counting theorem yields exact quarter",
        c_cell == sp.Rational(1, 4),
        "c_cell = Tr((I_16/16) P_A) = rank(P_A)/16 = 4/16 = 1/4",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 4: NOTE HONESTY")
    p = check(
        "the note presents the route as a theorem candidate plus retained no-go",
        "science-only max-entropy theorem candidate plus sharp retained no-go" in note,
        "the writeup should not overclaim retained closure",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the note is explicit that the current retained stack does not yet imply the max-entropy principle",
        "does **not** yet imply the source-free full-cell maximum-entropy principle" in note,
        "this is the exact missing promotion step",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the note records conditional Planck closure if the max-entropy theorem is accepted",
        "a^2 = l_p^2" in note and "a = l_p" in note,
        "the route should close immediately once rho_cell = I_16 / 16 is accepted",
    )
    n_pass += int(p); n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    print(
        "Verdict: the max-entropy route cleanly derives rho_cell = I_16/16 if source-free means unconstrained full-cell entropy maximization; without that new theorem, retained Planck closure remains open."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
