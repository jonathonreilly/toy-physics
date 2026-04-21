#!/usr/bin/env python3
"""
DM selector relative-action / recovered projection support theorem.

Question:
  Once the observable-relative-action source and the recovered threshold branch
  are known to be distinct exact selector objects, is there nevertheless a
  canonical recovered projection of the internal selector onto that branch?

Answer:
  Yes.

  The relative-action source still stays off the recovered bank, but the
  preferred recovered lift is the unique nearest recovered point across a
  nontrivial audited intrinsic metric family:

    - Frobenius distance on H,
    - Euclidean distance on the active target (delta, q_+),
    - threshold-profile distance on the exact witness-volume family,
    - affine-invariant Riemannian distance on the common positive windows
      A_mu(H),
    - dual LogDet divergences on A_mu(H),
    - and inverse-eigenvalue parameter distance on the same windows.

  The same preferred recovered lift is already the unique point selected by
  the intrinsic threshold breakpoint tau_b,min.

  So the selector-side burden narrows again: it is no longer to discover a
  disconnected target on the recovered bank, but to justify the projection
  principle from the exact internal selector to that already-identified
  recovered point, or to replace both by a finer microscopic law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import ANCHOR_OFFSET, SHIFT_OFFSETS, common_shift, recovered_bank
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
)
from frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization import (
    inverse_eigenvalue_parameters,
    witness_volume_from_atomic_field,
)
from frontier_dm_selector_relative_action_recovered_branch_separation_support_2026_04_21 import (
    observable_relative_action_selection,
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


def unique_argmin(values: np.ndarray) -> tuple[int, float]:
    vals = np.asarray(values, dtype=float)
    order = np.argsort(vals)
    return int(order[0]), float(vals[order[1]] - vals[order[0]])


def affine_invariant_distance(a: np.ndarray, b: np.ndarray) -> float:
    wa, ua = np.linalg.eigh(np.asarray(a, dtype=complex))
    a_inv_half = ua @ np.diag(1.0 / np.sqrt(wa)) @ ua.conj().T
    c = a_inv_half @ np.asarray(b, dtype=complex) @ a_inv_half
    wc, _uc = np.linalg.eigh(c)
    return float(np.linalg.norm(np.log(wc)))


def logdet_divergence(a: np.ndarray, b: np.ndarray) -> float:
    x = np.asarray(a, dtype=complex) @ np.linalg.inv(np.asarray(b, dtype=complex))
    sign, logdet = np.linalg.slogdet(x)
    if abs(sign) < 1.0e-12:
        return float("inf")
    return float(np.real(np.trace(x) - logdet - x.shape[0]))


def threshold_profile_distance(
    params_a: tuple[float, float, float],
    params_b: tuple[float, float, float],
    tau_max: float,
    n: int = 201,
) -> float:
    taus = np.linspace(0.0, float(tau_max), int(n))
    va = np.array([witness_volume_from_atomic_field(params_a, float(t)) for t in taus], dtype=float)
    vb = np.array([witness_volume_from_atomic_field(params_b, float(t)) for t in taus], dtype=float)
    return float(np.linalg.norm(va - vb))


def main() -> int:
    print("=" * 88)
    print("DM SELECTOR RELATIVE-ACTION / RECOVERED PROJECTION SUPPORT THEOREM")
    print("=" * 88)

    thresh_note = read("docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md")
    sep_note = read("docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    review = read("docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md")

    _i_star, _x_sel, _y_sel, _delta_sel, h_rel, _etas_sel = observable_relative_action_selection()
    _lifts, hs_bank, repairs_bank, _targets = recovered_bank()
    target_rel = np.asarray(active_target_from_h(h_rel), dtype=float)

    mu_anchor = common_shift(repairs_bank, ANCHOR_OFFSET)
    params_anchor = [inverse_eigenvalue_parameters(h, mu_anchor) for h in hs_bank]
    tau_b = np.array([math.log1p(p[1]) for p in params_anchor], dtype=float)
    tau_b_min = float(np.min(tau_b))
    tau_b_argmin = int(np.argmin(tau_b))

    h_dists = np.array([np.linalg.norm(np.asarray(h_rel, dtype=complex) - np.asarray(h, dtype=complex)) for h in hs_bank], dtype=float)
    target_dists = np.array([np.linalg.norm(target_rel - np.asarray(active_target_from_h(h), dtype=float)) for h in hs_bank], dtype=float)

    params_rel_anchor = inverse_eigenvalue_parameters(h_rel, mu_anchor)
    tau_zero_rel = math.log1p(params_rel_anchor[0])
    tau_zero_bank_next = float(np.min([math.log1p(p[0]) for p in params_anchor]))
    tau_profile_max = min(0.25, tau_zero_rel - 1.0e-6, tau_zero_bank_next - 1.0e-6)
    profile_dists = np.array(
        [threshold_profile_distance(params_rel_anchor, p, tau_profile_max) for p in params_anchor],
        dtype=float,
    )

    shift_results: dict[str, list[tuple[int, float]]] = {
        "airm": [],
        "logdet_forward": [],
        "logdet_reverse": [],
        "inverse_params": [],
    }
    for offset in SHIFT_OFFSETS:
        mu = common_shift(repairs_bank, float(offset))
        a_rel = np.asarray(h_rel, dtype=complex) + mu * np.eye(3, dtype=complex)
        params_rel = np.asarray(inverse_eigenvalue_parameters(h_rel, mu), dtype=float)

        vals_airm = []
        vals_fwd = []
        vals_rev = []
        vals_param = []
        for h in hs_bank:
            a = np.asarray(h, dtype=complex) + mu * np.eye(3, dtype=complex)
            vals_airm.append(affine_invariant_distance(a_rel, a))
            vals_fwd.append(logdet_divergence(a_rel, a))
            vals_rev.append(logdet_divergence(a, a_rel))
            vals_param.append(np.linalg.norm(params_rel - np.asarray(inverse_eigenvalue_parameters(h, mu), dtype=float)))

        shift_results["airm"].append(unique_argmin(np.asarray(vals_airm, dtype=float)))
        shift_results["logdet_forward"].append(unique_argmin(np.asarray(vals_fwd, dtype=float)))
        shift_results["logdet_reverse"].append(unique_argmin(np.asarray(vals_rev, dtype=float)))
        shift_results["inverse_params"].append(unique_argmin(np.asarray(vals_param, dtype=float)))

    print("\n" + "=" * 88)
    print("PART 1: THE SAME RECOVERED LIFT IS ALREADY SINGLED OUT BY THE THRESHOLD FAMILY")
    print("=" * 88)

    check(
        "The recovered-bank threshold note still records the canonical breakpoint tau_b,min",
        "tau_b,min" in thresh_note and "earliest middle-branch" in thresh_note,
    )
    check(
        "The separation note still records that the internal selector and recovered branch are distinct exact selector objects",
        "distinct exact selector objects" in sep_note and "tau_b,rel" in sep_note,
    )
    check(
        "The intrinsic threshold breakpoint tau_b,min already selects recovered lift 0 uniquely",
        tau_b_argmin == 0 and tau_b[0] + 1.0e-12 < np.min(tau_b[1:]),
        f"(tau_b_min,next)=({tau_b[0]:.15f},{np.min(tau_b[1:]):.15f})",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE INTERNAL SELECTOR HAS A UNIQUE SHIFT-INDEPENDENT NEAREST RECOVERED POINT")
    print("=" * 88)

    h_idx, h_margin = unique_argmin(h_dists)
    tgt_idx, tgt_margin = unique_argmin(target_dists)
    prof_idx, prof_margin = unique_argmin(profile_dists)

    check(
        "In Frobenius distance on H, the relative-action source is uniquely nearest to recovered lift 0",
        h_idx == 0 and h_margin > 1.0e-6,
        f"(nearest, margin)=({h_idx}, {h_margin:.12f})",
    )
    check(
        "In Euclidean distance on the active target (delta, q_+), the relative-action source is uniquely nearest to recovered lift 0",
        tgt_idx == 0 and tgt_margin > 1.0e-6,
        f"(nearest, margin)=({tgt_idx}, {tgt_margin:.12f})",
    )
    check(
        "At the anchor positive window, the exact witness-volume threshold profile is also uniquely nearest to recovered lift 0",
        prof_idx == 0 and prof_margin > 1.0e-6,
        f"(nearest, margin)=({prof_idx}, {prof_margin:.12f}) on [0,{tau_profile_max:.6f}]",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE SAME PREFERRED LIFT PERSISTS ACROSS THE AUDITED POSITIVE-WINDOW GEOMETRIES")
    print("=" * 88)

    airm_ok = all(idx == 0 and margin > 1.0e-9 for idx, margin in shift_results["airm"])
    airm_margin = min(margin for _idx, margin in shift_results["airm"])
    fwd_ok = all(idx == 0 and margin > 1.0e-9 for idx, margin in shift_results["logdet_forward"])
    fwd_margin = min(margin for _idx, margin in shift_results["logdet_forward"])
    rev_ok = all(idx == 0 and margin > 1.0e-9 for idx, margin in shift_results["logdet_reverse"])
    rev_margin = min(margin for _idx, margin in shift_results["logdet_reverse"])
    par_ok = all(idx == 0 and margin > 1.0e-9 for idx, margin in shift_results["inverse_params"])
    par_margin = min(margin for _idx, margin in shift_results["inverse_params"])

    check(
        "Across all audited common positive shifts, the affine-invariant Riemannian distance picks recovered lift 0 uniquely",
        airm_ok,
        f"min audited margin = {airm_margin:.12f}",
    )
    check(
        "Across all audited common positive shifts, the forward LogDet divergence D(A_rel || A_i) picks recovered lift 0 uniquely",
        fwd_ok,
        f"min audited margin = {fwd_margin:.12f}",
    )
    check(
        "Across all audited common positive shifts, the reverse LogDet divergence D(A_i || A_rel) picks recovered lift 0 uniquely",
        rev_ok,
        f"min audited margin = {rev_margin:.12f}",
    )
    check(
        "Across all audited common positive shifts, inverse-eigenvalue parameter distance also picks recovered lift 0 uniquely",
        par_ok,
        f"min audited margin = {par_margin:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 4: SCIENTIFIC CONSEQUENCE")
    print("=" * 88)

    check(
        "The open-import register still names the finer right-sensitive microscopic selector law as the live DM blocker",
        "finer right-sensitive microscopic point-selection law" in review
        or "finer right-sensitive microscopic selector law" in review,
    )
    check(
        "The internal selector and recovered threshold branch are no longer disconnected by the current exact branch science",
        h_idx == 0 and tgt_idx == 0 and prof_idx == 0 and airm_ok and fwd_ok and rev_ok and par_ok and tau_b_argmin == 0,
        "the same preferred recovered lift is selected by the threshold family and by the audited projection metrics from the internal selector",
    )
    check(
        "So the remaining selector-side burden narrows to justifying the projection principle, or replacing both selector objects by a finer microscopic law",
        h_idx == 0 and tgt_idx == 0 and prof_idx == 0 and airm_ok and fwd_ok and rev_ok and par_ok and tau_b_argmin == 0,
        "support narrowing only",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The relative-action source still stays off the recovered selector branch,")
    print("  but it now has a canonical recovered projection packet.")
    print("  Across Frobenius, target, threshold-profile, affine-invariant, dual")
    print("  LogDet, and inverse-eigenvalue metrics, the unique nearest recovered")
    print("  point is always the preferred lift 0.")
    print("  That same lift is already selected by the intrinsic breakpoint tau_b,min.")
    print()
    print("  So the selector-side burden narrows again:")
    print("    justify the projection from the exact internal selector to that")
    print("    preferred recovered lift, or replace both by a finer microscopic law.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
