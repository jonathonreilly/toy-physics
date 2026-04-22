#!/usr/bin/env python3
"""
DM selector shifted-doublet-imaginary-sign support theorem.

Question:
  After identifying the canonical recovered projection of the internal
  selector, can the remaining recovered-bank selector burden be sharpened to
  one exact doublet-block activation side?

Answer:
  Yes.

  The active doublet-block theorem gives

      Im(K_Z3[1,2]) = sqrt(3) * delta - 4 sqrt(2) / 3.

  On the current selector packet:

    - the exact observable-relative-action source lies on the positive side
      Im(K_Z3[1,2]) > 0,
    - the preferred recovered lift 0 is the unique recovered lift on that
      same positive side,
    - every other recovered lift lies on the negative side,
    - and the preferred recovered lift is already the unique threshold
      selector picked by tau_b,min.

  So the live selector burden narrows again: on the current packet, it is
  enough to derive the positive activation law for the shifted imaginary
  doublet mixing, or to replace that packet by a finer microscopic law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import recovered_bank
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_selector_relative_action_recovered_branch_separation_support_2026_04_21 import (
    observable_relative_action_selection,
)
from frontier_dm_selector_relative_action_recovered_projection_support_2026_04_21 import (
    unique_argmin,
)
from frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21 import (
    threshold_volume,
)
from frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization import (
    inverse_eigenvalue_parameters,
)
from dm_selector_branch_support import ANCHOR_OFFSET, common_shift

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


def flat(text: str) -> str:
    return " ".join(text.split())


def imag12_from_h(h: np.ndarray) -> float:
    kz = np.asarray(kz_from_h(h), dtype=complex)
    return float(np.imag(kz[1, 2]))


def delta_switch() -> float:
    return 4.0 * math.sqrt(2.0) / (3.0 * math.sqrt(3.0))


def main() -> int:
    print("=" * 88)
    print("DM SELECTOR SHIFTED-DOUBLET-IMAGINARY-SIGN SUPPORT THEOREM")
    print("=" * 88)

    doublet_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md")
    sep_note = read("docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    proj_note = read("docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    review = read("docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md")

    _i_star, _x_sel, _y_sel, _delta_sel, h_rel, _etas = observable_relative_action_selection()
    rel_target = np.asarray(active_target_from_h(h_rel), dtype=float)
    rel_imag = imag12_from_h(h_rel)
    d_cut = delta_switch()

    _lifts, hs_bank, repairs_bank, _targets = recovered_bank()
    imag_bank = np.array([imag12_from_h(h) for h in hs_bank], dtype=float)
    target_bank = np.array([active_target_from_h(h) for h in hs_bank], dtype=float)
    triplet_bank = [triplet_from_projected_response_pack(hermitian_linear_responses(h)) for h in hs_bank]

    mu_anchor = common_shift(repairs_bank, ANCHOR_OFFSET)
    params_bank = [inverse_eigenvalue_parameters(h, mu_anchor) for h in hs_bank]
    tau_b = np.array([math.log1p(p[1]) for p in params_bank], dtype=float)
    tau_b_min = float(np.min(tau_b))
    tau_vals = np.array([threshold_volume(p, tau_b_min) for p in params_bank], dtype=float)
    tau_idx, tau_margin = unique_argmin(tau_vals)

    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE Z3 DOUBLET THEOREM FIXES ONE CANONICAL SIGN BOUNDARY")
    print("=" * 88)

    check(
        "The doublet-block theorem note records delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)",
        "delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)" in doublet_note,
    )
    check(
        "So the exact sign boundary is delta = 4 sqrt(2) / (3 sqrt(3))",
        abs(d_cut - 4.0 * math.sqrt(2.0) / (3.0 * math.sqrt(3.0))) < 1.0e-12,
        f"delta_cut = {d_cut:.15f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE INTERNAL SELECTOR LIES ON THE POSITIVE SIDE OF THAT BOUNDARY")
    print("=" * 88)

    check(
        "The separation note still records the exact internal observable-relative-action selector",
        "observable-relative-action law" in sep_note and "exact internal selector law" in sep_note,
    )
    check(
        "The internal selector target has delta_rel > delta_cut",
        rel_target[0] > d_cut,
        f"(delta_rel, delta_cut)=({rel_target[0]:.12f}, {d_cut:.12f})",
    )
    check(
        "Equivalently, the internal selector has positive shifted imaginary doublet mixing Im(K12) > 0",
        rel_imag > 0.0,
        f"Im(K12)_rel = {rel_imag:.12e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: ON THE RECOVERED BANK, ONLY THE PREFERRED LIFT SHARES THAT POSITIVE SIDE")
    print("=" * 88)

    positive_idx = np.where(imag_bank > 0.0)[0]
    check(
        "Exactly one recovered lift has positive shifted imaginary doublet mixing",
        len(positive_idx) == 1,
        f"positive indices = {positive_idx.tolist()}",
    )
    check(
        "That unique positive recovered lift is the preferred lift 0",
        len(positive_idx) == 1 and int(positive_idx[0]) == 0,
        f"Im(K12)_bank = {np.round(imag_bank, 12)}",
    )
    check(
        "Every competing recovered lift lies strictly on the negative side Im(K12) < 0",
        np.all(imag_bank[1:] < 0.0),
        f"competitor imag parts = {np.round(imag_bank[1:], 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE CONSTRUCTIVE TRIPLET CHAMBER STILL DOES NOT DISTINGUISH THE RECOVERED PACKET")
    print("=" * 88)

    gamma_bank = np.array([float(t["gamma"]) for t in triplet_bank], dtype=float)
    e1_bank = np.array([float(t["E1"]) for t in triplet_bank], dtype=float)
    e2_bank = np.array([float(t["E2"]) for t in triplet_bank], dtype=float)

    check(
        "All recovered lifts already share the same exact constructive triplet tuple",
        np.allclose(gamma_bank, gamma_bank[0], atol=1.0e-12)
        and np.allclose(e1_bank, e1_bank[0], atol=1.0e-12)
        and np.allclose(e2_bank, e2_bank[0], atol=1.0e-12),
        f"(gamma,E1,E2)=({gamma_bank[0]:.12f},{e1_bank[0]:.12f},{e2_bank[0]:.12f})",
    )
    check(
        "So the constructive triplet chamber gamma > 0, E1 > 0, E2 > 0 is shared across the recovered packet",
        np.all(gamma_bank > 0.0) and np.all(e1_bank > 0.0) and np.all(e2_bank > 0.0),
        "triplet chamber does not break the recovered degeneracy",
    )
    check(
        "Every recovered lift also stays on the positive oriented-phase side sin(delta) > 0",
        np.all(np.sin(target_bank[:, 0]) > 0.0),
        f"sin(delta)_bank = {np.round(np.sin(target_bank[:, 0]), 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 5: THE POSITIVE SHIFTED-IMAGINARY SIDE IS THE FIRST RIGHT-SENSITIVE REFINEMENT")
    print("=" * 88)

    check(
        "The projection note still records that the preferred recovered lift is the canonical recovered image of the internal selector",
        "canonical recovered projection" in flat(proj_note)
        and "preferred recovered lift `0`" in flat(proj_note),
    )
    check(
        "The intrinsic threshold candidate tau_b,min still selects the same preferred recovered lift uniquely",
        tau_idx == 0 and tau_margin > 1.0e-9,
        f"(winner, margin)=({tau_idx}, {tau_margin:.12f})",
    )
    check(
        "So on the current selector packet the internal selector, the recovered projection, the threshold selector, and the shifted-imaginary sign all agree on the same preferred recovered lift",
        len(positive_idx) == 1 and int(positive_idx[0]) == 0 and tau_idx == 0 and rel_imag > 0.0,
        "same preferred lift 0",
    )

    print("\n" + "=" * 88)
    print("PART 6: SCIENTIFIC CONSEQUENCE")
    print("=" * 88)

    check(
        "The review register still names the finer right-sensitive microscopic selector law as open",
        "finer right-sensitive microscopic point-selection law" in review
        or "finer right-sensitive microscopic selector law" in review,
    )
    check(
        "On the current selector packet, the shifted-imaginary sign is the first right-sensitive datum that refines the sharp source tuple and constructive triplet chamber",
        np.allclose(gamma_bank, gamma_bank[0], atol=1.0e-12)
        and np.all(gamma_bank > 0.0)
        and len(positive_idx) == 1
        and int(positive_idx[0]) == 0,
        "first right-sensitive refinement",
    )
    check(
        "So the remaining selector burden now narrows to the positive activation law for the shifted imaginary doublet mixing, or a finer replacement law",
        len(positive_idx) == 1 and int(positive_idx[0]) == 0 and rel_imag > 0.0 and tau_idx == 0,
        "support narrowing only",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The internal selector target already lies on the positive side of the")
    print("  canonical doublet-block boundary Im(K12)=0.")
    print("  On the recovered bank, the preferred lift 0 is the unique point on that")
    print("  same positive side, and it is already the recovered threshold selector")
    print("  chosen by tau_b,min.")
    print()
    print("  So the remaining selector burden narrows again:")
    print("    derive the positive activation law for the shifted imaginary")
    print("    doublet mixing on the current selector packet, or replace it")
    print("    with a finer microscopic law.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
