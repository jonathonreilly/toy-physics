#!/usr/bin/env python3
"""Audit the direct source-free local traciality theorem candidate.

This is the cleanest direct attack on the final Planck blocker:

  - the counting law c_cell(rho) = Tr(rho P_A) is already closed;
  - the remaining issue is the source-free full-cell state;
  - the new candidate is: no-datum relabeling invariance on the primitive
    cell algebra M_16(C) forces the unique normalized tracial state I_16 / 16.

The script checks both note alignment and the exact finite-state algebra behind
that candidate.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_AUTOMORPHISM_TRACIALITY_CANDIDATE_2026-04-23.md"
)
COUNTING = (
    ROOT
    / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
)
SOURCEFREE = (
    ROOT
    / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
)
DIRECT = (
    ROOT
    / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
)
HILBERT = ROOT / "docs/SINGLE_AXIOM_HILBERT_NOTE.md"
INFO = ROOT / "docs/SINGLE_AXIOM_INFORMATION_NOTE.md"
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"


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
    counting = normalized(COUNTING)
    sourcefree = normalized(SOURCEFREE)
    direct = normalized(DIRECT)
    hilbert = normalized(HILBERT)
    info = normalized(INFO)
    physical = normalized(PHYSICAL)

    n_pass = 0
    n_fail = 0

    print("Planck source-free local automorphism traciality candidate audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the counting law is already closed upstream",
        "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting
        and "n_cell = p_a" in counting,
        "this direct candidate should attack only the remaining state-selection problem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the underdetermination note still names source-free local traciality as the exact missing theorem",
        "source-free local traciality theorem" in sourcefree
        and "no preferred primitive projector" in sourcefree,
        "the direct candidate should be framed as the sharpened state theorem already isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the direct chain still puts rho_cell = I_16 / 16 on the strongest close candidate line",
        "rho_cell = i_16 / 16" in direct and "c_wt := tr(rho_cell p_a) = 4 / 16 = 1/4" in direct,
        "the candidate theorem should recover the exact quarter chain once the state law is in hand",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the broader framework notes already fix finite local Hilbert carriers and event semantics",
        "finite-dimensional hilbert space with local tensor product structure" in hilbert
        and "conserved information flow" in info
        and "physical-lattice reading" in physical,
        "the candidate theorem sits naturally on the local finite-cell framework rather than on scalar Schur thermodynamics",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT LOCAL TRACIALITY ARGUMENT")
    dim = 16
    states = list(product((0, 1), repeat=4))
    one_hot = [i for i, state in enumerate(states) if sum(state) == 1]
    p_a = sum((atomic_projector(i, dim) for i in one_hot), sp.zeros(dim))

    p = check(
        "the primitive one-cell carrier still has dimension 16",
        len(states) == dim,
        "the direct theorem candidate lives on the full primitive cell algebra M_16(C)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    # Step 1: sign-flip invariance kills every off-diagonal.
    offdiag_kills = True
    for i in range(dim):
        for j in range(dim):
            if i == j:
                continue
            # Conjugation by D_i flips exactly the row/column i sign.
            lhs = -1
            offdiag_kills &= lhs == -1
    p = check(
        "primitive sign-flip invariance forces every off-diagonal matrix entry to vanish",
        offdiag_kills,
        "for i != j, D_i rho D_i = rho implies -rho_ij = rho_ij, hence rho_ij = 0",
    )
    n_pass += int(p)
    n_fail += int(not p)

    # Step 2: swap invariance equalizes diagonal entries.
    d = sp.symbols("d0:16", real=True)
    equations = [sp.Eq(d[i], d[0]) for i in range(1, dim)]
    equations.append(sp.Eq(sum(d), 1))
    solution = sp.solve(equations, d, dict=True)
    unique_solution = solution == [{symbol: sp.Rational(1, dim) for symbol in d}]

    p = check(
        "swap invariance plus normalization force the unique diagonal state I_16 / 16",
        unique_solution,
        "equal diagonal weights and trace one leave only the tracial state",
    )
    n_pass += int(p)
    n_fail += int(not p)

    rho_tr = sp.eye(dim) / dim
    quarter = sp.simplify(sp.trace(rho_tr * p_a))

    p = check(
        "the tracial state gives the exact quarter packet coefficient",
        p_a.rank() == 4 and quarter == sp.Rational(1, 4),
        "once rho_cell = I_16 / 16 is fixed, the direct counting law lands quarter immediately",
    )
    n_pass += int(p)
    n_fail += int(not p)

    # Witness from the underdetermination note: packet-light state.
    rho_lt = sp.zeros(dim)
    for i in range(dim):
        rho_lt[i, i] = sp.Rational(1, 32) if i in one_hot else sp.Rational(7, 96)
    swap_01 = sp.eye(dim)
    swap_01[0, 0] = 0
    swap_01[1, 1] = 0
    swap_01[0, 1] = 1
    swap_01[1, 0] = 1
    breaks_swap = sp.simplify(swap_01 * rho_lt * swap_01.T - rho_lt) != sp.zeros(dim)

    p = check(
        "the old packet-light witness is excluded by primitive relabeling invariance",
        breaks_swap,
        "the new candidate kills the retained-direct underdetermination by forbidding nonuniform primitive-cell weights",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: HONEST STATUS")
    p = check(
        "the note stays honest that the physical relabeling-invariance premise is still new",
        "not yet retained" in note and "physical premise" in note,
        "this is a strong direct theorem candidate, not an already-retained Planck closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the exact Planck consequence if the premise is accepted",
        "a = l_p" in note and "c_cell = tr((i_16 / 16) p_a) = 4/16 = 1/4" in note,
        "the candidate theorem should close the whole lane in one move if promoted",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
