#!/usr/bin/env python3
"""Audit the strongest one-shot synthesis route for the direct Planck lane.

This runner checks the sharpest honest synthesis result now available:

  - there is a single theorem shape that would collapse both remaining
    blockers at once;
  - that theorem is the source-free elementary boundary event theorem on the
    exact primitive C^16 cell;
  - but the current branch does not yet derive it on the retained surface, so
    the route remains conditional/support rather than retained closure.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_WORLDTUBE_SYNTHESIS_RETAINED_CLOSE_AUDIT_2026-04-23.md"
)
DIRECT = ROOT / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
PROJECTOR = (
    ROOT / "docs/PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md"
)
NON_SCHUR = ROOT / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"
FULL_PACKET = (
    ROOT / "docs/PLANCK_SCALE_FULL_PACKET_PHYSICAL_READOUT_THEOREM_LANE_2026-04-23.md"
)
SECTION = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
VOCAB = ROOT / "docs/repo/CONTROLLED_VOCABULARY.md"
OLD_AUDIT = ROOT / "docs/PLANCK_SCALE_AXIOM_NATIVE_RETAINED_AUDIT_2026-04-23.md"


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


def xor_bits(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x ^ y) for x, y in zip(a, b))


def main() -> int:
    note = normalized(NOTE)
    direct = normalized(DIRECT)
    projector = normalized(PROJECTOR)
    non_schur = normalized(NON_SCHUR)
    full_packet = normalized(FULL_PACKET)
    section_note = normalized(SECTION)
    vocab = normalized(VOCAB)
    old_audit = normalized(OLD_AUDIT)

    n_pass = 0
    n_fail = 0

    print("Planck boundary worldtube synthesis retained-close audit")
    print("=" * 78)

    section("PART 1: UPSTREAM SCIENCE STATE")
    p = check(
        "the direct route still isolates one final bridge c_cell = c_wt",
        "c_cell = c_wt" in direct and "what is not yet closed" in direct,
        "the synthesis should start from the already-compressed direct route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the section-canonical lane still forces the full packet P_A",
        "section-canonical" in section_note and "p_a" in section_note,
        "the synthesis theorem must inherit a fixed packet rather than refit one",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the full-packet lane still rules out quotient-only physical readout",
        "quotient-only readout" in full_packet
        and "not physically admissible" in full_packet
        and "tr(rho p_a)" in full_packet,
        "the synthesis route must keep the full packet rather than the Schur-visible quotient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the projector lane still says quarter closes only on a new event grammar",
        "quarter closes exactly **if** physical boundary readout is the event observable" in projector
        or "quarter closes exactly **if** physical boundary pressure is the event readout" in projector,
        "the synthesis should not pretend the scalar Schur grammar already closes the route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur lane still says the democratic full-cell state is conditional on stronger flip invariance",
        "does **not** close planck unconditionally" in non_schur
        and "rho_cell = i_16 / 16" in non_schur
        and "flip-transitivity principle" in non_schur,
        "the synthesis should not silently promote the tracial state to retained status",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: ONE-SHOT THEOREM SHAPE")
    states = list(product((0, 1), repeat=4))
    dim = len(states)
    atoms = [atomic_projector(i, dim) for i in range(dim)]
    index = {state: i for i, state in enumerate(states)}
    one_hot = [state for state in states if sum(state) == 1]
    P_A = sum((atoms[index[state]] for state in one_hot), sp.zeros(dim))
    rho_cell = sp.eye(dim) / dim

    p = check(
        "the primitive cell has 16 atoms and the worldtube packet has 4 atoms",
        dim == 16 and len(one_hot) == 4 and sp.trace(P_A) == 4,
        "the direct coefficient route is rank counting on the exact four-bit cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    vars_p = sp.symbols("p0:16", real=True)
    equations = []
    for s in states:
        for g in generators:
            equations.append(sp.Eq(vars_p[index[s]], vars_p[index[xor_bits(s, g)]]))
    equations.append(sp.Eq(sum(vars_p), 1))
    solution = sp.linsolve([eq.lhs - eq.rhs for eq in equations], vars_p)
    tuple_solution = next(iter(solution))
    uniform = tuple(sp.Rational(1, 16) for _ in range(dim))

    p = check(
        "full local bit-flip invariance plus normalization uniquely gives the tracial state",
        tuple_solution == uniform,
        "this is the mathematical core of the source-free primitive-cell state candidate",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the tracial state gives the exact quarter packet coefficient",
        sp.simplify(sp.trace(rho_cell * P_A)) == sp.Rational(1, 4),
        "once the primitive state is tracial and the packet is fixed, the coefficient is forced",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "one theorem can collapse both blockers at once",
        tuple_solution == uniform and sp.simplify(sp.trace(rho_cell * P_A)) == sp.Rational(1, 4),
        "a single source-free primitive-cell event theorem would imply both rho_cell = I_16/16 and c_cell = Tr(rho_cell P_A)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: RETAINED-STATUS AUDIT")
    p = check(
        "the repo vocabulary still distinguishes retained from conditional/support",
        "| `conditional / support` | useful positive package whose load-bearing step is still conditional" in vocab
        and "| `open flagship gate` | still-open flagship closure target |" in vocab,
        "the synthesis verdict should use the repo's own claim-strength language",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the older retained audit still says Planck is not yet retained",
        "not yet a retained axiom-native planck derivation" in old_audit
        and "conditional / support" in old_audit,
        "the new synthesis audit must not silently overrule the prior honest status",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the new note states the route as one stronger theorem candidate rather than a finished retained close",
        "source-free elementary boundary event theorem" in note
        and "conditional / support" in note
        and "not retained closure" in note,
        "the writeup should record the one-shot reduction without overselling it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the new note records that both blockers collapse under the one-shot theorem",
        "collapse both remaining blockers at once" in note
        and "rho_cell = i_16 / 16" in note
        and "c_cell = tr(rho_cell p_a) = 1/4" in note,
        "the synthesis audit should make the exact reduction target explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the new note still says the theorem is not yet derived from the retained accepted stack",
        "does **not** yet derive that theorem from the retained accepted stack" in note,
        "the route is still conditional/support until that one theorem is actually earned",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    print(
        "Verdict: the direct Planck route admits a single one-shot reduction target, but that theorem is not yet retained; status remains conditional/support."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
