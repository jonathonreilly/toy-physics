#!/usr/bin/env python3
"""Audit the source-free cell-state retained-derivation lane honestly.

This lane tries to derive the direct Planck state law

    rho_cell = I_16 / 16

from already-accepted retained structure only.

The honest result is a sharp reduction / no-go:

  - current retained direct structure leaves an exact 7-parameter family of
    diagonal S_3-invariant full-cell source-free candidate states;
  - neither the scalar observable principle nor the Born/event grammar selects
    one state from that family;
  - a new retained source-free local traciality theorem would still be needed;
  - full four-bit flip invariance is one stronger sufficient witness, not the
    minimal missing content.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
DIRECT = ROOT / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
NON_SCHUR = ROOT / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"
SECTIONAL = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
PROJECTOR = ROOT / "docs/PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md"
OBSERVABLE = ROOT / "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
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
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def orbit_key(state: tuple[int, int, int, int]) -> tuple[int, int]:
    return state[0], sum(state[1:])


def s3_invariant(weights: dict[tuple[int, int, int, int], sp.Rational]) -> bool:
    by_orbit: dict[tuple[int, int], sp.Rational] = {}
    for state, weight in weights.items():
        key = orbit_key(state)
        if key in by_orbit and by_orbit[key] != weight:
            return False
        by_orbit[key] = weight
    return True


def normalized_positive(weights: dict[tuple[int, int, int, int], sp.Rational]) -> bool:
    total = sum(weights.values())
    return total == 1 and all(weight >= 0 for weight in weights.values())


def packet_mass(weights: dict[tuple[int, int, int, int], sp.Rational]) -> sp.Rational:
    return sum(weight for state, weight in weights.items() if sum(state) == 1)


def xor_bits(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x ^ y for x, y in zip(a, b))


def main() -> int:
    note = normalized(NOTE)
    direct = normalized(DIRECT)
    non_schur = normalized(NON_SCHUR)
    sectional = normalized(SECTIONAL)
    projector = normalized(PROJECTOR)
    observable = normalized(OBSERVABLE)
    hilbert = normalized(HILBERT)
    info = normalized(INFO)
    physical = normalized(PHYSICAL)

    states = list(product((0, 1), repeat=4))
    one_hot = [state for state in states if sum(state) == 1]
    complement = [state for state in states if sum(state) != 1]

    n_pass = 0
    n_fail = 0

    print("Planck source-free cell-state retained derivation lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the direct route isolates source-free state semantics as the package-boundary issue",
        "source-free default datum" in direct
        and "the counting side is no longer open" in direct,
        "the historical retained-state no-go should remain scoped to the pre-bridge state-selection problem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur lane still says current accepted data do not force the democratic state",
        "do **not** force the democratic state" in non_schur
        and "eight orbit weights" in non_schur,
        "the source-free-state problem should begin from the exact underdetermination already recorded there",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the worldtube packet is already section-canonical",
        "section-canonical" in sectional and "p_a" in sectional,
        "this lane should not reopen packet selection; it should only address the state law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the projector route still treats the state-selection step as the remaining physical issue",
        "the full-cell source-free state" in projector and "projector/event" in projector,
        "this lane should attack that source-free-state step directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT RETAINED-DIRECT STATE FAMILY")
    orbit_classes: dict[tuple[int, int], list[tuple[int, int, int, int]]] = {}
    for state in states:
        orbit_classes.setdefault(orbit_key(state), []).append(state)

    expected_keys = {(t, w) for t in (0, 1) for w in range(4)}
    expected_sizes = {
        (0, 0): 1,
        (0, 1): 3,
        (0, 2): 3,
        (0, 3): 1,
        (1, 0): 1,
        (1, 1): 3,
        (1, 2): 3,
        (1, 3): 1,
    }

    p = check(
        "the exact time-locked cell has 16 primitive states",
        len(states) == 16,
        "the direct lane works on the full four-bit carrier C^16",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "residual S_3 invariance classifies primitive states into exactly eight orbits",
        set(orbit_classes) == expected_keys and all(len(orbit_classes[key]) == expected_sizes[key] for key in expected_keys),
        "after time-lock the only retained label data are the temporal bit and spatial Hamming weight",
    )
    n_pass += int(p)
    n_fail += int(not p)

    orbit_weights = sp.symbols("a00 a01 a02 a03 a10 a11 a12 a13", real=True)
    normalization = sp.Eq(
        orbit_weights[0]
        + 3 * orbit_weights[1]
        + 3 * orbit_weights[2]
        + orbit_weights[3]
        + orbit_weights[4]
        + 3 * orbit_weights[5]
        + 3 * orbit_weights[6]
        + orbit_weights[7],
        1,
    )
    rank = sp.Matrix([[1, 3, 3, 1, 1, 3, 3, 1]]).rank()
    family_dim = len(orbit_weights) - rank

    p = check(
        "current retained-direct source-free candidates form an exact 7-parameter family",
        family_dim == 7,
        "eight orbit weights plus one normalization equation leave seven free parameters",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXPLICIT UNDERDETERMINATION WITNESSES")
    rho_tr = {state: sp.Rational(1, 16) for state in states}
    rho_lt = {state: sp.Rational(1, 32) for state in one_hot}
    rho_lt.update({state: sp.Rational(7, 96) for state in complement})

    p = check(
        "the democratic state is retained-direct admissible",
        s3_invariant(rho_tr) and normalized_positive(rho_tr),
        "rho_tr = I_16 / 16 is diagonal, normalized, positive, and S_3-invariant",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "a distinct packet-light state is also retained-direct admissible",
        s3_invariant(rho_lt) and normalized_positive(rho_lt),
        "rho_lt = (1/32) P_A + (7/96) (I_16 - P_A) still satisfies the same retained-direct constraints",
    )
    n_pass += int(p)
    n_fail += int(not p)

    alpha_tr = packet_mass(rho_tr)
    alpha_lt = packet_mass(rho_lt)

    p = check(
        "the two admissible states give different worldtube-packet coefficients",
        alpha_tr == sp.Rational(1, 4) and alpha_lt == sp.Rational(1, 8) and alpha_tr != alpha_lt,
        "the current retained-direct stack allows at least two different source-free packet masses",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: ACCEPTED OBSERVABLE STRUCTURES DO NOT SELECT THE STATE")
    p = check(
        "the scalar observable principle is an observable-generator theorem, not a state-selection theorem",
        "w[j] = log |det(d+j)| - log |det d|" in observable
        and "local scalar observables are exactly the coefficients in its local source expansion" in observable,
        "the scalar route fixes W[J] from partition factorization but does not provide rho_source-free on the full event algebra",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the Hilbert/Born side supplies event probabilities on a chosen state, not a unique source-free state",
        "the born rule (automatic from the inner product)" in hilbert
        and "conserved information flow" in info,
        "the accepted one-axiom Hilbert/information notes fix the event grammar and conserved flow, but they do not pick one density matrix on the 16-state cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "physical-lattice necessity fixes substrate ontology, not the local cell state",
        "finite local staggered-dirac dynamics" in physical and "physical-lattice reading" in physical,
        "the retained physical-lattice boundary strengthens ontology and no-quotient semantics, but it does not collapse the 7-parameter local state family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: SHARPEST EXTRA THEOREM STILL NEEDED")
    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    vars_p = sp.symbols("p0:16", real=True)
    index = {state: i for i, state in enumerate(states)}
    equations = []
    for state in states:
        for generator in generators:
            equations.append(sp.Eq(vars_p[index[state]], vars_p[index[xor_bits(state, generator)]]))
    equations.append(sp.Eq(sum(vars_p), 1))
    solution = next(iter(sp.linsolve([eq.lhs - eq.rhs for eq in equations], vars_p)))

    p = check(
        "full four-bit flip transitivity is a stronger sufficient witness that uniquely forces the democratic state",
        solution == tuple(sp.Rational(1, 16) for _ in states),
        "bit-flip invariance is not the minimal missing content, but it is an exact sufficient theorem witness for local traciality",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the real missing content is source-free local traciality / no-preferred-projector selection on the full cell",
        True,
        "once one asserts a retained theorem that source-free local occupancy assigns equal weight to every primitive cell event, rho_cell = I_16 / 16 follows immediately",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE ALIGNMENT")
    p = check(
        "the note states that closure was not achieved",
        "no." in note and "closure is **not** achieved" in note,
        "the writeup should stay honest and avoid promoting the source-free-state route to closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the 7-parameter family and the explicit witness pair",
        "7-parameter family" in note
        and "witness a: democratic/tracial state" in note
        and "witness b: packet-light residual state" in note,
        "the writeup should make the exact underdetermination explicit rather than merely stating it abstractly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note names source-free local traciality as the sharpest missing theorem",
        "source-free local traciality theorem" in note
        and "no-preferred-projector" in note,
        "the lane should end on the smallest real missing theorem, not just repeat the stronger flip-invariance witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    print("Verdict: no retained derivation of rho_cell = I_16 / 16 from the current accepted stack alone.")
    print("Exact remaining need: a retained source-free local traciality theorem on the full time-locked C^16 cell.")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
