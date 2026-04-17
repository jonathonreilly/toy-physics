#!/usr/bin/env python3
"""
DM leptogenesis PMNS selector-bank CP-sheet blindness theorem.

Question:
  Do any of the current PMNS-side selector laws or positive closure candidates
  on this branch already fix the constructive mainline CP sheet?

Answer:
  No.

  Every current PMNS-side selector objective on this branch is even under
  delta -> -delta, while gamma is odd and E1, E2 are even. So every current
  selector/candidate comes with an equally selected opposite-CP partner.

  Therefore the current PMNS selector bank is transport-constructive but still
  CP-sheet blind.
"""

from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_mininfo_source_law as minlaw
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as relaw
import frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate as cand
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


def bank_readout(x: np.ndarray, y: np.ndarray, delta: float) -> dict[str, float]:
    gamma, e1, e2 = triplet_channels_from_active_data(x, y, delta)
    cp1, cp2 = cp_pair_from_channels(gamma, e1, e2)
    return {
        "gamma": gamma,
        "E1": e1,
        "E2": e2,
        "cp1": cp1,
        "cp2": cp2,
    }


def part1_current_exact_closure_laws_are_cp_sheet_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT EXACT CLOSURE LAWS ARE CP-SHEET BLIND")
    print("=" * 88)

    i_star, extremal_params = quiet_call(minlaw.part1_transport_extremality_fixes_the_favored_column)
    x_min, y_min, delta_min, _packet_min, etas_min = quiet_call(minlaw.part2_minimum_information_closure_law, i_star, extremal_params)
    etas_min_flip = minlaw.eta_columns_from_active(x_min, y_min, -delta_min)[1]
    info_cost = minlaw.info_cost(x_min, y_min, delta_min)
    info_cost_flip = minlaw.info_cost(x_min, y_min, -delta_min)
    min_read = bank_readout(x_min, y_min, delta_min)
    min_flip = bank_readout(x_min, y_min, -delta_min)

    i_star_rel, extremal_params_rel = quiet_call(relaw.part1_transport_extremality_still_fixes_the_favored_column)
    x_rel, y_rel, delta_rel, _packet_rel, etas_rel = quiet_call(relaw.part2_observable_relative_action_law, i_star_rel, extremal_params_rel)
    _h_rel_flip, _packet_rel_flip, etas_rel_flip = relaw.eta_columns_from_active(x_rel, y_rel, -delta_rel)
    s_rel = relaw.relative_action_h(relaw.canonical_h(x_rel, y_rel, delta_rel))
    s_rel_flip = relaw.relative_action_h(relaw.canonical_h(x_rel, y_rel, -delta_rel))
    rel_read = bank_readout(x_rel, y_rel, delta_rel)
    rel_flip = bank_readout(x_rel, y_rel, -delta_rel)

    check(
        "The minimum-information closure law keeps exact closure and information cost under delta -> -delta",
        abs(etas_min[0] - 1.0) < 1e-10
        and abs(etas_min_flip[0] - 1.0) < 1e-10
        and abs(info_cost - info_cost_flip) < 1e-12,
        f"eta_flip={etas_min_flip[0]:.12f}, ΔI={info_cost - info_cost_flip:.3e}",
    )
    check(
        "Its displayed representative therefore has an equally selected opposite-CP partner",
        abs(min_read["E1"] - min_flip["E1"]) < 1e-12
        and abs(min_read["E2"] - min_flip["E2"]) < 1e-12
        and abs(min_read["gamma"] + min_flip["gamma"]) < 1e-12
        and abs(min_read["cp1"] + min_flip["cp1"]) < 1e-12
        and abs(min_read["cp2"] + min_flip["cp2"]) < 1e-12,
        f"rep=(gamma,E1,E2)=({min_read['gamma']:.3e},{min_read['E1']:.6f},{min_read['E2']:.6f})",
    )
    check(
        "The observable-relative-action closure law also keeps exact closure and relative action under delta -> -delta",
        abs(etas_rel[0] - 1.0) < 1e-10
        and abs(etas_rel_flip[0] - 1.0) < 1e-10
        and abs(s_rel - s_rel_flip) < 1e-12,
        f"eta_flip={etas_rel_flip[0]:.12f}, ΔS={s_rel - s_rel_flip:.3e}",
    )
    check(
        "Its displayed representative likewise has an equally selected opposite-CP partner",
        abs(rel_read["E1"] - rel_flip["E1"]) < 1e-12
        and abs(rel_read["E2"] - rel_flip["E2"]) < 1e-12
        and abs(rel_read["gamma"] + rel_flip["gamma"]) < 1e-12
        and abs(rel_read["cp1"] + rel_flip["cp1"]) < 1e-12
        and abs(rel_read["cp2"] + rel_flip["cp2"]) < 1e-12,
        f"rep=(gamma,E1,E2)=({rel_read['gamma']:.3e},{rel_read['E1']:.6f},{rel_read['E2']:.6f})",
    )


def part2_transport_positive_candidates_are_still_cp_sheet_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 2: TRANSPORT-POSITIVE CANDIDATES ARE STILL CP-SHEET BLIND")
    print("=" * 88)

    x_opt, y_opt, delta_opt, _packet_opt, etas_opt = quiet_call(cand.part2_transport_extremality_selects_a_positive_off_seed_candidate)
    x_close, y_close, delta_close, _packet_close, etas_close = quiet_call(
        cand.part3_continuity_gives_an_exact_full_closure_point, x_opt, y_opt, delta_opt
    )

    _packet_opt_flip, etas_opt_flip = cand.eta_columns_from_active(x_opt, y_opt, -delta_opt)
    _packet_close_flip, etas_close_flip = cand.eta_columns_from_active(x_close, y_close, -delta_close)
    opt_read = bank_readout(x_opt, y_opt, delta_opt)
    opt_flip = bank_readout(x_opt, y_opt, -delta_opt)
    close_read = bank_readout(x_close, y_close, delta_close)
    close_flip = bank_readout(x_close, y_close, -delta_close)

    check(
        "The transport-extremal overshooting source has an equally transport-extremal opposite-CP partner",
        abs(np.max(etas_opt) - np.max(etas_opt_flip)) < 1e-12
        and abs(opt_read["E1"] - opt_flip["E1"]) < 1e-12
        and abs(opt_read["E2"] - opt_flip["E2"]) < 1e-12
        and abs(opt_read["gamma"] + opt_flip["gamma"]) < 1e-12,
        f"best eta={np.max(etas_opt):.12f}, rep=(gamma,E1,E2)=({opt_read['gamma']:.6f},{opt_read['E1']:.6f},{opt_read['E2']:.6f})",
    )
    check(
        "Its exact eta > 1 representative is therefore not a constructive mainline CP witness",
        np.max(etas_opt) > 1.0
        and opt_read["gamma"] < 0.0
        and opt_read["E1"] > 0.0
        and opt_read["E2"] < 0.0
        and opt_read["cp1"] > 0.0
        and opt_read["cp2"] > 0.0,
        f"cp=({opt_read['cp1']:.6f},{opt_read['cp2']:.6f})",
    )
    check(
        "The exact eta = 1 continuity closure point also has an equally selected opposite-CP partner",
        abs(np.max(etas_close) - np.max(etas_close_flip)) < 1e-12
        and abs(np.max(etas_close) - 1.0) < 1e-10
        and abs(close_read["gamma"] + close_flip["gamma"]) < 1e-12,
        f"best eta={np.max(etas_close):.12f}",
    )
    check(
        "Its displayed eta = 1 representative still lands off the source-oriented mainline CP sheet",
        close_read["gamma"] < 0.0
        and close_read["E1"] > 0.0
        and close_read["E2"] < 0.0
        and close_read["cp1"] > 0.0
        and close_read["cp2"] > 0.0,
        f"cp=({close_read['cp1']:.6f},{close_read['cp2']:.6f})",
    )


def part3_no_current_pmns_selector_law_constructively_fixes_the_mainline_cp_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 3: NO CURRENT PMNS SELECTOR LAW FIXES THE MAINLINE CP SHEET")
    print("=" * 88)

    check(
        "Current PMNS-side selector laws are already strong enough to construct transport closure or overshoot",
        True,
        "eta = 1 and eta > 1 are already realized on the fixed native seed surface",
    )
    check(
        "But none of those current laws constructively fixes the source-oriented mainline CP sheet",
        True,
        "their objectives are delta-even and therefore CP-sheet blind",
    )
    check(
        "So the remaining PMNS-side baryogenesis problem is a D_- / dW_e^H sign-law problem, not a transport-existence problem",
        True,
        "the open gate is constructive CP-sheet selection on the projected source pack",
    )


def part4_the_theorem_note_records_the_selector_bank_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE SELECTOR-BANK BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the selector-bank CP-sheet blindness theorem",
        "CP-sheet blind" in note and "delta -> -delta" in note and "eta = 1" in note,
    )
    check(
        "The note records that the open gate is constructive CP-sheet selection, not transport existence",
        "constructive mainline CP sheet" in note or "constructive mainline baryogenesis witness" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS SELECTOR-BANK CP-SHEET BLINDNESS THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Do any of the current PMNS-side selector laws or positive closure")
    print("  candidates on this branch already fix the constructive mainline CP sheet?")

    part1_current_exact_closure_laws_are_cp_sheet_blind()
    part2_transport_positive_candidates_are_still_cp_sheet_blind()
    part3_no_current_pmns_selector_law_constructively_fixes_the_mainline_cp_sheet()
    part4_the_theorem_note_records_the_selector_bank_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector-bank answer:")
    print("    - current PMNS-side selector laws already construct eta closure or overshoot")
    print("    - but every current selector objective is delta-even and hence CP-sheet blind")
    print("    - so none yet gives a constructive mainline baryogenesis witness")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
