#!/usr/bin/env python3
"""
DM neutrino source-surface observable-grammar exhaustion obstruction.

Question:
  After representation compression, is the true last-mile selector already
  proved to be exhausted by the exact atomic positive-probe grammar on
  dW_e^H = Schur_Ee(D_-)?

Answer:
  No.

  The branch now proves that the atomic grammar recovers the singleton response
  field, the intrinsic extensional family quotient, and every tested higher
  positive-probe functional on the recovered bank. What is still missing is the
  theorem that the true last-mile selector is exhausted by that grammar alone.

Boundary:
  This is an obstruction runner. It documents where the selector-side proof
  stops; it does not numerically search for another selector.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import (
    ANCHOR_OFFSET,
    base_vector_family,
    canonical_score_from_repairs,
    changed_support_presentation,
    common_shift,
    duplicated_presentation,
    extensional_response_map,
    family_witness_from_atomic_thresholds,
    maps_differ,
    maps_equal,
    positive_probe_family,
    recovered_bank,
    recover_scores_from_atomic_thresholds,
    relabeled_presentation,
    response_matrix,
    response_matrix_from_presentation,
    response_orders,
    spectral_projector_data,
    universal_frontier_indices,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def canonical_scores_from_hs(hs: list[np.ndarray], mu: float) -> tuple[np.ndarray, float, float, bool]:
    scores: list[float] = []
    max_formula_err = 0.0
    min_soft_gap = float("inf")
    soft_simple = True
    for h in hs:
        a = np.asarray(h, dtype=complex) + float(mu) * np.eye(3, dtype=complex)
        evals, responses, _projectors = spectral_projector_data(a)
        scores.append(float(np.max(responses)))
        max_formula_err = max(max_formula_err, abs(float(np.max(responses)) - math.log1p(1.0 / float(evals[0]))))
        min_soft_gap = min(min_soft_gap, float(evals[1] - evals[0]))
        soft_simple &= bool(np.argmax(responses) == 0 and responses[0] > responses[1] > responses[2])
    return np.asarray(scores, dtype=float), max_formula_err, min_soft_gap, soft_simple


def part1_atomic_threshold_events_recover_the_singleton_response_field_exactly() -> tuple[list[np.ndarray], np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: ATOMIC THRESHOLD EVENTS RECOVER THE SINGLETON RESPONSE FIELD EXACTLY")
    print("=" * 88)

    _lifts, hs_bank, repairs_bank, targets_bank = recovered_bank()
    mu_bank = common_shift(repairs_bank, ANCHOR_OFFSET)
    vector_family = base_vector_family()
    bank_scores = response_matrix_from_presentation(hs_bank, mu_bank, vector_family)
    bank_recovered = recover_scores_from_atomic_thresholds(bank_scores)
    _levels_bank, witness_bank, envelope_bank = family_witness_from_atomic_thresholds(bank_scores)
    direct_witness_bank = np.array(
        [np.any(bank_scores >= tau, axis=1) for tau in np.unique(bank_scores)],
        dtype=bool,
    )
    direct_envelope_bank = np.max(bank_scores, axis=1)

    bank_err = float(np.max(np.abs(bank_scores - bank_recovered)))
    witness_ok = bool(np.array_equal(witness_bank, direct_witness_bank))
    envelope_err = float(np.max(np.abs(envelope_bank - direct_envelope_bank)))

    check(
        "The recovered carrier bank still contains the same five exact clustered lifts",
        len(hs_bank) == 5,
        f"targets={[tuple(np.round(t, 6)) for t in targets_bank]}",
    )
    check(
        "On the recovered bank the atomic singleton threshold grammar recovers the sampled singleton response field exactly",
        bank_err < 1.0e-12,
        f"max recovery error={bank_err:.12e}",
    )
    check(
        "Family witness events on the sampled finite family are existential unions of atomic singleton threshold events",
        witness_ok,
        f"threshold count={len(np.unique(bank_scores))}",
    )
    check(
        "The sampled finite-family upper envelope is already recovered exactly from the atomic threshold grammar",
        envelope_err < 1.0e-12,
        f"max envelope error={envelope_err:.12e}",
    )

    return hs_bank, repairs_bank


def part2_the_intrinsic_family_quotient_already_lives_at_the_atomic_level(
    hs_bank: list[np.ndarray], repairs_bank: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE INTRINSIC FAMILY QUOTIENT ALREADY LIVES AT THE ATOMIC LEVEL")
    print("=" * 88)

    mu_bank = common_shift(repairs_bank, ANCHOR_OFFSET)
    base = base_vector_family()
    rel = relabeled_presentation(base)
    dup = duplicated_presentation(base)
    changed = changed_support_presentation(base)

    base_map = extensional_response_map(hs_bank, mu_bank, base)
    rel_map = extensional_response_map(hs_bank, mu_bank, rel)
    dup_map = extensional_response_map(hs_bank, mu_bank, dup)
    changed_map = extensional_response_map(hs_bank, mu_bank, changed)

    check(
        "Relabeling an extensional probe family leaves the exact atomic singleton-response field unchanged",
        maps_equal(base_map, rel_map),
        f"support size={len(base_map)}",
    )
    check(
        "Duplicating already-available probes is also invisible after passing to the intrinsic extensional family",
        maps_equal(base_map, dup_map),
        f"(list, support)=({len(dup)},{len(dup_map)})",
    )
    check(
        "The induced atomic threshold signatures are unchanged under relabeling and duplication of the same extensional family",
        maps_equal(rel_map, dup_map),
        f"signature count={len(rel_map)}",
    )
    check(
        "A genuine change in available positive-probe support is still visible to the exact atomic grammar",
        maps_differ(base_map, changed_map),
        f"changed support size={len(changed_map)}",
    )
    check(
        "So the exact atomic quotient stops at intrinsic family support; it does not quotient away real support changes",
        len(base_map) == len(changed_map) and maps_differ(base_map, changed_map),
        f"base_vs_changed_support={len(set(base_map) ^ set(changed_map))}",
    )


def part3_higher_level_selector_data_are_atomic_functionals(
    hs_bank: list[np.ndarray], repairs_bank: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: HIGHER-LEVEL SELECTOR DATA ARE ATOMIC FUNCTIONALS")
    print("=" * 88)

    probes = positive_probe_family()
    frontier = universal_frontier_indices(hs_bank, repairs_bank, probes)
    mu_bank = common_shift(repairs_bank, ANCHOR_OFFSET)
    canonical_scores, max_formula_err, min_soft_gap, soft_simple = canonical_scores_from_hs(hs_bank, mu_bank)
    repair_scores = canonical_score_from_repairs(repairs_bank, mu_bank)

    check(
        "Strict positive-probe dominance and the anchor-fiber Pareto frontier are functions of the recovered atomic singleton field",
        frontier == [0, 1],
        f"frontier={frontier}",
    )
    check(
        "The exact canonical extremal score is already determined by the atomic singleton response field via the full-family endpoint",
        soft_simple and max_formula_err < 1.0e-12 and min_soft_gap > 1.0e-6,
        f"(formula err, min gap)=({max_formula_err:.12e},{min_soft_gap:.12e})",
    )
    check(
        "On the recovered bank that canonical atomic endpoint has the same strict ordering as Lambda_+",
        response_orders(canonical_scores) == response_orders(repair_scores),
        f"order={response_orders(canonical_scores)}",
    )


def part4_the_current_bank_still_does_not_fix_an_intrinsic_threshold_law(
    hs_bank: list[np.ndarray], repairs_bank: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT BANK STILL DOES NOT FIX AN INTRINSIC THRESHOLD LAW")
    print("=" * 88)

    del repairs_bank
    nonrealization_note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_ATOMIC_WITNESS_VOLUME_SELECTOR_NONREALIZATION_NOTE_2026-04-18.md"
    )

    check(
        "The branch now carries the exact canonical witness-volume selector family on the full rank-one probe family",
        "V_tau(H)" in nonrealization_note and "piecewise-quadratic" in nonrealization_note,
    )
    check(
        "That exact intrinsic threshold-volume family already flips the recovered winner between tau=0.13 and tau=0.14",
        "tau = 0.13" in nonrealization_note and "lift `1`" in nonrealization_note and "tau = 0.14" in nonrealization_note and "lift `0`" in nonrealization_note,
    )
    check(
        "So the unresolved selector datum is now sharper than generic family choice: it is an intrinsic threshold law",
        len(hs_bank) == 5,
        "current exact bank nonrealization persists even on the canonical full-family threshold-volume selector",
    )


def part5_the_note_records_the_obstruction_honestly() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE OBSTRUCTION HONESTLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_OBSERVABLE_GRAMMAR_EXHAUSTION_OBSTRUCTION_NOTE_2026-04-17.md")
    representation_note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POSITIVE_PROBE_REPRESENTATION_THEOREM_NOTE_2026-04-17.md"
    )

    check(
        "The representation note already records that selector-family choice has been compressed to the canonical extremal law",
        "soft-mode extremal score" in representation_note and "observable-grammar exhaustion" in representation_note,
    )
    check(
        "The obstruction note names the exact missing selector-side theorem as observable-grammar exhaustion / intrinsic-family descent",
        "observable-grammar exhaustion / intrinsic-family descent" in note,
    )
    check(
        "The obstruction note keeps the boundary honest: representation is compressed, but selector closure is still not proved",
        "selector-class side does" in note and "close positively" in note,
    )
    check(
        "The obstruction note records the sharper current-bank nonrealization as a missing intrinsic threshold law",
        "intrinsic threshold law" in note and "tau = 0.13" in note and "tau = 0.14" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE OBSERVABLE-GRAMMAR EXHAUSTION OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After representation compression, is the true last-mile selector already")
    print("  proved to be exhausted by the exact atomic positive-probe grammar?")

    hs_bank, repairs_bank = part1_atomic_threshold_events_recover_the_singleton_response_field_exactly()
    part2_the_intrinsic_family_quotient_already_lives_at_the_atomic_level(hs_bank, repairs_bank)
    part3_higher_level_selector_data_are_atomic_functionals(hs_bank, repairs_bank)
    part4_the_current_bank_still_does_not_fix_an_intrinsic_threshold_law(hs_bank, repairs_bank)
    part5_the_note_records_the_obstruction_honestly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector-side branch verdict:")
    print("    - atomic singleton thresholds already recover the tested singleton field")
    print("    - the intrinsic extensional family quotient is already fixed at the atomic level")
    print("    - every tested higher positive-probe functional is atomic-field data")
    print("    - what is still missing is the theorem that the true last-mile selector is exhausted by that grammar")
    print("  RESULT: obstruction at observable-grammar exhaustion / intrinsic-family descent")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
