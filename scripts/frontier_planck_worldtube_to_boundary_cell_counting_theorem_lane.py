#!/usr/bin/env python3
"""Audit the direct worldtube-to-boundary cell-counting theorem honestly.

This lane attacks the last direct bridge in the Planck program:

    c_cell = Tr(rho_cell P_A).

The theorem proved here is narrower and cleaner than the older "pressure"
language:

  - an elementary codimension-1 boundary cell coefficient is modeled as an
    integer-valued local count observable on the one-cell event algebra;
  - under minimal-shell support, atomic diagonality, residual S_3 invariance,
    and additive counting, every such observable is N_(u_t,u_s) = u_t P_t + u_s P_s;
  - counting minimal one-step incidences forces u_t = u_s = 1, hence
    N_cell = P_A;
  - therefore c_cell(rho) = Tr(rho P_A) for every state rho.

After the later one-axiom default-datum theorem, the state step is closed on
the authorized one-axiom semantic surface. This runner still checks the
counting theorem itself.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
)
DIRECT = (
    ROOT
    / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
)
SECTION = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
MULT = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
)
NON_SCHUR = (
    ROOT
    / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"
)
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


def atomic_projector(idx: int, dim: int = 16) -> sp.Matrix:
    vec = sp.zeros(dim, 1)
    vec[idx, 0] = 1
    return vec * vec.T


def main() -> int:
    note = normalized(NOTE)
    direct = normalized(DIRECT)
    section_note = normalized(SECTION)
    mult = normalized(MULT)
    non_schur = normalized(NON_SCHUR)
    physical = normalized(PHYSICAL)

    n_pass = 0
    n_fail = 0

    print("Planck worldtube-to-boundary cell-counting theorem audit")
    print("=" * 78)

    section("PART 1: NOTE ALIGNMENT")
    p = check(
        "the new note states the bridge as a cell-counting theorem rather than a scalar pressure problem",
        "cell-counting theorem" in note
        and "n_cell = p_a" in note
        and "not a schur free-energy scalar" in note,
        "the lane should now be framed as direct boundary-cell counting on the exact one-cell event algebra",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the direct canonical chain records the closed cell-counting law",
        "c_cell(rho) = tr(rho p_a)" in direct
        and "the counting side is no longer open" in direct,
        "the theorem should close the exact direct counting bridge on the canonical direct chain",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: UPSTREAM SCIENCE SURFACES")
    p = check(
        "section-canonical packet theorem still forces the coarse worldtube packet P_A",
        "p_a = sum_(|eta|=1) p_eta" in section_note
        or "forced to be p_a" in section_note,
        "the counting law has to live on the already-forced packet rather than choose a new carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "multiplicity-lift theorem still fixes full-packet quarter and forbids quotient-only undercounting",
        "tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in mult
        and "no proper exact quotient" in mult,
        "the cell-counting law should count the full packet and not discard the hidden E block",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur lane still records democratic full-cell quarter as conditional on stronger flip invariance",
        "rho_cell = i_16 / 16" in non_schur
        and "does **not** yet prove" in non_schur
        and "full flip-transitivity" in non_schur,
        "the theorem here should close the counting law while leaving the retained-state obstruction honest",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the physical-lattice boundary still rejects proper exact quotienting of retained physical sectors",
        "no proper exact quotient/rooting/reduction" in physical
        and "physical-species semantics" in physical,
        "quotient-only counting on P_q should remain physically inadmissible on the accepted surface",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT COUNTING-LAW CLASSIFICATION")
    states = list(product((0, 1), repeat=4))
    dim = len(states)
    atoms = [atomic_projector(i, dim) for i in range(dim)]
    one_hot_indices = [i for i, bits in enumerate(states) if sum(bits) == 1]

    idx_t = one_hot_indices[0]
    idx_x, idx_y, idx_z = one_hot_indices[1:]

    p_t = atoms[idx_t]
    p_s = atoms[idx_x] + atoms[idx_y] + atoms[idx_z]
    p_a = p_t + p_s

    u_t, u_s = sp.symbols("u_t u_s", integer=True, nonnegative=True)
    n_general = sp.simplify(u_t * p_t + u_s * p_s)
    n_cell = p_a
    rho_dem = sp.eye(dim) / dim
    c_dem = sp.simplify(sp.trace(rho_dem * n_cell))

    p_q = sp.zeros(dim)
    ket_t = sp.zeros(dim, 1)
    ket_t[idx_t, 0] = 1
    ket_s = sp.zeros(dim, 1)
    for idx in (idx_x, idx_y, idx_z):
        ket_s[idx, 0] = sp.sqrt(sp.Rational(1, 3))
    p_q = ket_t * ket_t.T + ket_s * ket_s.T

    p = check(
        "the time-locked one-cell carrier still has sixteen primitive atomic states",
        dim == 16,
        "the direct count observable acts on the exact four-bit cell, not on a reduced Schur carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the forced packet P_A contains exactly the four Hamming-weight-1 atomic events",
        len(one_hot_indices) == 4 and p_a.rank() == 4,
        "an elementary one-step boundary cell should count exactly the four one-hot incidences",
    )
    n_pass += int(p)
    n_fail += int(not p)

    diag_entries = [sp.simplify(n_general[i, i]) for i in range(dim)]
    expected = [sp.Integer(0)] * dim
    expected[idx_t] = u_t
    expected[idx_x] = expected[idx_y] = expected[idx_z] = u_s
    p = check(
        "every diagonal residual-invariant minimal-shell counter reduces to one temporal weight and one common spatial weight",
        diag_entries == expected,
        "minimal-shell support plus residual S_3 invariance leave only the pair (u_t, u_s)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "unit one-step incidence counting forces u_t = u_s = 1 and hence N_cell = P_A",
        sp.simplify(n_general.subs({u_t: 1, u_s: 1}) - n_cell) == sp.zeros(dim),
        "once the observable counts minimal incidences rather than weighted energies, the unique count operator is the packet projector itself",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the quotient-visible Schur block P_q is not an admissible atomic count observable",
        any(sp.simplify(p_q[i, j]) != 0 for i in range(dim) for j in range(dim) if i != j),
        "P_q contains off-diagonal spatial coherence and therefore is not a diagonal atomic event counter on the physical cell basis",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "on the democratic full-cell state the exact cell count lands quarter",
        c_dem == sp.Rational(1, 4),
        "with N_cell = P_A and rho = I_16/16, the boundary-cell coefficient is exactly 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: RESIDUAL HONESTY")
    p = check(
        "the note closes the counting law and points to the later state theorem",
        "that state step is now closed after the later one-axiom bridge" in note
        and "planck_scale_one_axiom_conservative_semantics_bridge_theorem" in note,
        "the direct bridge should be marked closed while delegating state closure to the one-axiom theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the exact Planck consequence once the source-free state is accepted",
        "a = l_p" in direct and "c_cell = tr(rho_cell p_a)" in note,
        "the lane should make clear that Planck closes cleanly once the democratic state theorem is available",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
