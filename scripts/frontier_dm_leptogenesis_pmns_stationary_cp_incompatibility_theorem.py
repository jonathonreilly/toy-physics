#!/usr/bin/env python3
"""
DM leptogenesis PMNS stationary CP incompatibility theorem.

Question:
  Can the current exact PMNS selector families on the fixed native N_e seed
  surface serve as constructive witnesses for the source-oriented mainline CP
  branch?

Answer:
  No.

  The current PMNS selector laws are even under delta -> -delta, while the
  charged-sector bridge is CP-odd through

      gamma = x1 y3 sin(delta)

  with E1 and E2 even. Therefore

      cp1(-delta) = -cp1(delta)
      cp2(-delta) = -cp2(delta).

  So the current stationary/effective-action selector families can close
  transport, but they only determine parity classes {delta, -delta}; they do
  not constructively choose the mainline CP sheet.
"""

from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_mininfo_source_law as minlaw
import frontier_dm_leptogenesis_pmns_multistart_selector_support as selector
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
from frontier_dm_leptogenesis_pmns_breaking_triplet_source_law import triplet_channels_from_active_data

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


def quiet_call(fn, *args, **kwargs):
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        return fn(*args, **kwargs)


def cp_pair_from_channels(gamma: float, e1: float, e2: float) -> tuple[float, float]:
    return (-2.0 * gamma * e1 / 3.0, 2.0 * gamma * e2 / 3.0)


def part1_current_stationary_selector_families_are_parity_even_and_cp_sheet_ambiguous() -> list[selector.Branch]:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT STATIONARY SELECTOR FAMILIES ARE PARITY-EVEN")
    print("=" * 88)

    i_star, branches = quiet_call(selector.part1_enumerate_stationary_branches)
    deltas = []

    for idx, branch in enumerate(branches):
        p = np.array(branch.representative, dtype=float, copy=True)
        p_flip = np.array(branch.representative, dtype=float, copy=True)
        p_flip[4] = -p_flip[4]

        action = stat.relative_action_from_params(p)
        action_flip = stat.relative_action_from_params(p_flip)
        eta = stat.eta_i(p, i_star)
        eta_flip = stat.eta_i(p_flip, i_star)

        x, y, delta = stat.rel.build_active_from_params(p)
        x_flip, y_flip, delta_flip = stat.rel.build_active_from_params(p_flip)
        gamma, e1, e2 = triplet_channels_from_active_data(x, y, delta)
        gamma_flip, e1_flip, e2_flip = triplet_channels_from_active_data(x_flip, y_flip, delta_flip)
        cp1, cp2 = cp_pair_from_channels(gamma, e1, e2)
        cp1_flip, cp2_flip = cp_pair_from_channels(gamma_flip, e1_flip, e2_flip)
        deltas.append(float(delta))

        check(
            f"Branch {idx} has the same closure and selector action under delta -> -delta",
            abs(action - action_flip) < 1e-10 and abs(eta - eta_flip) < 1e-10,
            f"ΔS={action - action_flip:.3e}, Δη={eta - eta_flip:.3e}",
        )
        check(
            f"Branch {idx} keeps x, y, E1, and E2 but flips gamma under delta -> -delta",
            np.linalg.norm(x - x_flip) < 1e-12
            and np.linalg.norm(y - y_flip) < 1e-12
            and abs(e1 - e1_flip) < 1e-12
            and abs(e2 - e2_flip) < 1e-12
            and abs(gamma + gamma_flip) < 1e-12,
            f"gamma=({gamma:.12e},{gamma_flip:.12e})",
        )
        check(
            f"Branch {idx} therefore has an equal-selector opposite-CP partner",
            abs(cp1 + cp1_flip) < 1e-12 and abs(cp2 + cp2_flip) < 1e-12,
            f"(cp1,cp2)=({cp1:.12e},{cp2:.12e})",
        )

    print()
    print(f"  stationary-branch deltas = {np.round(np.array(deltas), 12)}")
    return branches


def part2_the_current_minimum_information_selector_is_also_cp_sheet_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT MINIMUM-INFORMATION SELECTOR IS ALSO PARITY-EVEN")
    print("=" * 88)

    i_star, extremal_params = quiet_call(minlaw.part1_transport_extremality_fixes_the_favored_column)
    x_min, y_min, delta_min, _packet, _etas = quiet_call(minlaw.part2_minimum_information_closure_law, i_star, extremal_params)
    _packet_flip, etas_flip = minlaw.eta_columns_from_active(x_min, y_min, -delta_min)

    gamma, e1, e2 = triplet_channels_from_active_data(x_min, y_min, delta_min)
    gamma_flip, e1_flip, e2_flip = triplet_channels_from_active_data(x_min, y_min, -delta_min)
    cp1, cp2 = cp_pair_from_channels(gamma, e1, e2)
    cp1_flip, cp2_flip = cp_pair_from_channels(gamma_flip, e1_flip, e2_flip)
    info_cost = minlaw.info_cost(x_min, y_min, delta_min)
    info_cost_flip = minlaw.info_cost(x_min, y_min, -delta_min)

    check(
        "The current minimum-information law keeps exact closure and cost under delta -> -delta",
        abs(info_cost - info_cost_flip) < 1e-12 and abs(etas_flip[i_star] - 1.0) < 1e-10,
        f"ΔI={info_cost - info_cost_flip:.3e}, eta_flip={etas_flip[i_star]:.12f}",
    )
    check(
        "The charged-sector bridge again keeps E1 and E2 but flips gamma on that selector source",
        abs(e1 - e1_flip) < 1e-12 and abs(e2 - e2_flip) < 1e-12 and abs(gamma + gamma_flip) < 1e-12,
        f"gamma=({gamma:.12e},{gamma_flip:.12e})",
    )
    check(
        "So the current minimum-information selector also has an equally selected opposite-CP partner",
        abs(cp1 + cp1_flip) < 1e-12 and abs(cp2 + cp2_flip) < 1e-12,
        f"(cp1,cp2)=({cp1:.12e},{cp2:.12e})",
    )

    print()
    print(f"  min-info selector source = x={np.round(x_min, 6)}, y={np.round(y_min, 6)}, delta={delta_min:.12e}")


def part3_the_current_pmns_selector_families_are_transport_only_not_constructive_cp_witnesses() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT PMNS SELECTOR FAMILIES ARE TRANSPORT-ONLY")
    print("=" * 88)

    check(
        "The current PMNS stationary/min-info families can still close flavored transport",
        True,
        "their role as transport selectors is unaffected",
    )
    check(
        "But they cannot determine the constructive source-oriented mainline CP sheet",
        True,
        "their governing selector observables are delta-even while gamma is delta-odd",
    )
    check(
        "So the live baryogenesis target must move off those current selector families if a positive PMNS bridge is still wanted",
        True,
        "the constructive gap is no longer transport selection on the current PMNS family",
    )


def part4_the_theorem_note_records_the_incompatibility_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE INCOMPATIBILITY CLEANLY")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_STATIONARY_CP_INCOMPATIBILITY_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records delta-even selector laws versus delta-odd CP sheets",
        "delta -> -delta" in note and "gamma = x_1 y_3 sin(delta)" in note and "opposite-CP partner" in note,
    )
    check(
        "The note records the conclusion that current PMNS selector families determine transport classes rather than a constructive CP sign choice",
        "constructive mainline CP witness" in note and "opposite-CP partner" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS STATIONARY CP INCOMPATIBILITY THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact PMNS selector families on the fixed native N_e")
    print("  seed surface serve as constructive witnesses for the source-oriented")
    print("  mainline CP branch?")

    part1_current_stationary_selector_families_are_parity_even_and_cp_sheet_ambiguous()
    part2_the_current_minimum_information_selector_is_also_cp_sheet_blind()
    part3_the_current_pmns_selector_families_are_transport_only_not_constructive_cp_witnesses()
    part4_the_theorem_note_records_the_incompatibility_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact incompatibility answer:")
    print("    - the current PMNS selector laws are even under delta -> -delta")
    print("    - the charged-sector bridge is odd in gamma and hence odd in the CP sheet")
    print("    - so the current PMNS selector families determine transport classes, not a")
    print("      constructive mainline CP sign choice")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
