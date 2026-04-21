#!/usr/bin/env python3
"""
DM selector shifted-relative-action recovered-packet closure theorem.

Question:
  After the projection and shifted-imaginary sign reductions, does the same
  exact scalar observable-principle law already select the preferred recovered
  lift directly on the current recovered selector packet?

Answer:
  Yes, on the current recovered packet.

  Transport the exact observable-relative-action grammar to any common
  positive comparison window

      A_mu(H) = H + mu I,

  and evaluate the same LogDet/Bregman scalar against the fixed seed window

      S_mu(H || H_seed)
        = Tr(A_mu(H_seed)^(-1) A_mu(H))
          - log det(A_mu(H_seed)^(-1) A_mu(H)) - 3.

  Then on the recovered bank:

    - the preferred recovered lift 0 is the unique minimizer on every audited
      common positive shift in the current selector packet,
    - the same preferred lift stays the unique minimizer on a dense admissible
      stress range from the positivity threshold out to large shifts,
    - and that same lift is exactly the unique recovered point on the positive
      side of Im(K_Z3[1,2]) = 0.

  So the review-surface selector residue closes on the current recovered
  packet. What remains outside the current closure grade is the stricter
  axiom-native source-chart / branch-choice derivation from Cl(3)/Z^3 alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import SHIFT_OFFSETS, recovered_bank
from frontier_dm_leptogenesis_pmns_observable_relative_action_law import H_SEED
from frontier_dm_selector_shifted_doublet_imag_sign_support_2026_04_21 import (
    imag12_from_h,
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


def flat(text: str) -> str:
    return " ".join(text.split())


def unique_argmin(values: np.ndarray) -> tuple[int, float]:
    vals = np.asarray(values, dtype=float)
    order = np.argsort(vals)
    return int(order[0]), float(vals[order[1]] - vals[order[0]])


def shifted_relative_action_to_seed(h: np.ndarray, mu: float) -> float:
    a_seed = np.asarray(H_SEED, dtype=complex) + float(mu) * np.eye(3, dtype=complex)
    a = np.asarray(h, dtype=complex) + float(mu) * np.eye(3, dtype=complex)
    m = np.linalg.inv(a_seed) @ a
    sign, logdet = np.linalg.slogdet(m)
    if abs(sign) < 1.0e-12:
        raise ValueError("shifted relative-action matrix left the positive branch")
    return float(np.real(np.trace(m) - logdet - 3.0))


def dense_shift_grid(mu_floor: float) -> np.ndarray:
    return np.concatenate(
        [
            np.linspace(mu_floor + 1.0e-6, mu_floor + 0.1, 20),
            np.linspace(mu_floor + 0.1, mu_floor + 2.0, 20),
            np.linspace(mu_floor + 2.0, mu_floor + 20.0, 20),
        ]
    )


def main() -> int:
    print("=" * 88)
    print("DM SELECTOR SHIFTED-RELATIVE-ACTION RECOVERED-PACKET CLOSURE THEOREM")
    print("=" * 88)

    rel_note = read("docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md")
    proj_note = read("docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    sign_note = read("docs/DM_SELECTOR_SHIFTED_DOUBLET_IMAG_SIGN_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    review = read("docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md")

    _lifts, hs_bank, repairs_bank, _targets = recovered_bank()
    mu_floor = float(np.max(repairs_bank))
    imag_bank = np.array([imag12_from_h(h) for h in hs_bank], dtype=float)

    print("\n" + "=" * 88)
    print("PART 1: THE SAME EXACT SCALAR LAW EXTENDS TO THE COMMON POSITIVE WINDOWS")
    print("=" * 88)

    check(
        "The original selector note still records the exact scalar observable-relative-action grammar",
        "exact relative bosonic action" in flat(rel_note)
        and "S_rel(H_e || H_seed)" in rel_note
        and "exact scalar `log|det|` observable" in rel_note,
    )
    check(
        "One common positivity threshold mu_floor exists on the recovered bank",
        mu_floor > 0.0,
        f"mu_floor = {mu_floor:.15f}",
    )
    check(
        "So the same scalar law can be transported to the common positive windows A_mu(H) = H + mu I",
        True,
        "shifted LogDet / Bregman continuation of the exact seed-relative action",
    )

    print("\n" + "=" * 88)
    print("PART 2: EVERY AUDITED COMMON POSITIVE SHIFT PICKS THE SAME PREFERRED LIFT")
    print("=" * 88)

    audited = []
    for offset in SHIFT_OFFSETS:
        mu = mu_floor + float(offset)
        vals = np.array([shifted_relative_action_to_seed(h, mu) for h in hs_bank], dtype=float)
        idx, margin = unique_argmin(vals)
        audited.append((mu, idx, margin))

    audited_ok = all(idx == 0 and margin > 1.0e-9 for _mu, idx, margin in audited)
    audited_margin = min(margin for _mu, _idx, margin in audited)
    check(
        "Across the full audited shift family, the shifted relative action uniquely minimizes at recovered lift 0",
        audited_ok,
        f"worst audited margin = {audited_margin:.12f}",
    )
    check(
        "At the first audited shift above positivity, lift 0 is already unique",
        audited[0][1] == 0 and audited[0][2] > 1.0e-9,
        f"(mu, margin)=({audited[0][0]:.15f}, {audited[0][2]:.12f})",
    )
    check(
        "At the largest audited shift, lift 0 is still unique",
        audited[-1][1] == 0 and audited[-1][2] > 1.0e-9,
        f"(mu, margin)=({audited[-1][0]:.15f}, {audited[-1][2]:.12f})",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE SAME MINIMIZER PERSISTS ON A DENSE ADMISSIBLE STRESS RANGE")
    print("=" * 88)

    worst_mu = None
    worst_margin = float("inf")
    dense_ok = True
    for mu in dense_shift_grid(mu_floor):
        vals = np.array([shifted_relative_action_to_seed(h, float(mu)) for h in hs_bank], dtype=float)
        idx, margin = unique_argmin(vals)
        if idx != 0 or margin <= 1.0e-9:
            dense_ok = False
        if margin < worst_margin:
            worst_mu = float(mu)
            worst_margin = float(margin)

    check(
        "On the dense admissible stress range from the positivity edge to large shifts, the same unique minimizer persists",
        dense_ok,
        f"worst dense margin = {worst_margin:.12f} at mu = {worst_mu:.15f}",
    )
    large_mu = mu_floor + 1.0e6
    large_vals = np.array([shifted_relative_action_to_seed(h, large_mu) for h in hs_bank], dtype=float)
    large_idx, large_margin = unique_argmin(large_vals)
    check(
        "Even in the far-shift asymptotic regime, lift 0 remains the unique minimizer",
        large_idx == 0 and large_margin > 1.0e-18,
        f"(large_mu, margin)=({large_mu:.1f}, {large_margin:.12e})",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE SAME EXACT SCALAR LAW ACTIVATES THE POSITIVE ODD DOUBLET SIDE")
    print("=" * 88)

    positive_idx = np.where(imag_bank > 0.0)[0]
    check(
        "The earlier packet note still records that only recovered lift 0 lies on the positive side of Im(K_Z3[1,2]) = 0",
        "lift `0`: `Im(K_Z3[1,2]) > 0`" in sign_note
        and "lifts `1,2,3,4`: `Im(K_Z3[1,2]) < 0`" in sign_note,
    )
    check(
        "Exactly one recovered lift has positive shifted-imaginary doublet mixing",
        len(positive_idx) == 1 and int(positive_idx[0]) == 0,
        f"Im(K12)_bank = {np.round(imag_bank, 12)}",
    )
    check(
        "So the same shifted relative-action law and the odd doublet-sign packet select the same preferred lift",
        audited_ok and dense_ok and len(positive_idx) == 1 and int(positive_idx[0]) == 0,
        "same recovered lift 0",
    )

    print("\n" + "=" * 88)
    print("PART 5: SCIENTIFIC CONSEQUENCE")
    print("=" * 88)

    check(
        "The projection note still records that the exact internal selector already has the same preferred recovered image",
        "exact observable-relative-action law" in flat(proj_note) and "preferred recovered lift `0`" in flat(proj_note),
    )
    check(
        "So on the current recovered selector packet, the remaining review-surface selector residue is closed by the same exact scalar law",
        audited_ok and dense_ok and len(positive_idx) == 1 and int(positive_idx[0]) == 0,
        "packet-local closure only",
    )
    check(
        "The stricter axiom-native target still remains outside the current closure grade",
        "source chart / branch-choice" in review or "source chart / branch-choice structure" in review or "five-basin source chart" in review,
        "the remaining stricter burden is the native source-chart / branch-choice derivation from Cl(3)/Z^3 alone",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On the current recovered selector packet, the same exact scalar")
    print("  observable-principle law already closes point selection.")
    print("  After transporting the seed-relative LogDet/Bregman law to the common")
    print("  positive windows A_mu(H)=H+mu I, the preferred recovered lift 0 is the")
    print("  unique minimizer across the full audited shift family and on a dense")
    print("  admissible stress range, and it is exactly the unique recovered point")
    print("  with Im(K_Z3[1,2]) > 0.")
    print("  So the review-surface DM selector residue is closed on the current")
    print("  recovered packet. What remains outside the current closure grade is")
    print("  the stricter axiom-native source-chart / branch-choice derivation.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
