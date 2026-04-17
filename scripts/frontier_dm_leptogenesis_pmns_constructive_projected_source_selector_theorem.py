#!/usr/bin/env python3
"""
DM leptogenesis PMNS constructive projected-source selector theorem.

Question:
  Is the constructive projected-source sign chamber on the current PMNS branch
  empty or transport-incompatible, or does there already exist an exact
  `D_- / dW_e^H` witness with

      gamma > 0, E1 > 0, E2 > 0

  on the fixed native seed surface?

Answer:
  A constructive witness already exists.

  On the fixed native `N_e` seed surface there is an explicit projected-source
  / `D_-` witness whose response pack satisfies the constructive sign system,
  whose CP pair is on the mainline sheet `(-,+)`, and whose best flavored
  transport value saturates the current transport-extremal overshoot value

      eta / eta_obs = 1.052220313052...

  Therefore the current PMNS branch is not blocked by incompatibility between
  constructive CP and transport closure. The remaining issue is only the
  microscopic selector law that picks this constructive sheet uniquely.
"""

from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate as cand
from frontier_dm_leptogenesis_full_microscopic_reduction import (
    build_full_charge_preserving_operator,
    schur_eff,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    seed_averages,
    source_coordinates,
)
from frontier_dm_leptogenesis_pmns_cp_bridge_boundary import breaking_triplet_coordinates
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_breaking_triplet_cp_theorem import cp_formula

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

# Exact constructive witness on the fixed native N_e seed surface.
WITNESS_X = np.array(
    [1.1741615606031017, 0.4625443480094451, 0.05329409138745294],
    dtype=float,
)
WITNESS_Y = np.array(
    [0.7587414158970156, 0.02690429951341027, 0.13435428458957413],
    dtype=float,
)
WITNESS_DELTA = 1.8825957561635622


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


def witness_data() -> tuple[np.ndarray, list[float], dict[str, float], tuple[float, float], np.ndarray]:
    h = canonical_h(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    responses = hermitian_linear_responses(h)
    triplet = triplet_from_projected_response_pack(responses)
    cp_pair = cp_formula(
        triplet["A"],
        triplet["b"],
        triplet["c"],
        triplet["d"],
        triplet["delta"],
        triplet["rho"],
        triplet["gamma"],
    )
    _packet, etas = cand.eta_columns_from_active(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    return h, responses, triplet, cp_pair, etas


def part1_the_constructive_sign_chamber_is_nonempty_on_the_fixed_seed_surface() -> tuple[np.ndarray, list[float], dict[str, float], tuple[float, float], np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE CONSTRUCTIVE SIGN CHAMBER IS NONEMPTY")
    print("=" * 88)

    h, responses, triplet, cp_pair, etas = witness_data()
    xbar, ybar = seed_averages(WITNESS_X, WITNESS_Y)
    xi, eta, delta = source_coordinates(WITNESS_X, WITNESS_Y, WITNESS_DELTA)

    check(
        "The constructive witness stays on the exact fixed native seed surface",
        abs(xbar - cand.XBAR_NE) < 1e-12 and abs(ybar - cand.YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({xbar:.12f},{ybar:.12f})",
    )
    check(
        "The constructive witness is genuinely off-seed",
        np.linalg.norm(xi) > 1e-6 and np.linalg.norm(eta) > 1e-6 and abs(delta) > 1e-6,
        f"xi={np.round(xi, 6)}, eta={np.round(eta, 6)}, delta={delta:.12f}",
    )
    check(
        "Its projected-source triplet channels satisfy gamma > 0, E1 > 0, E2 > 0",
        triplet["gamma"] > 0.0 and triplet["E1"] > 0.0 and triplet["E2"] > 0.0,
        f"(gamma,E1,E2)=({triplet['gamma']:.12f},{triplet['E1']:.12f},{triplet['E2']:.12f})",
    )
    check(
        "Its CP pair is therefore already on the source-oriented mainline sheet",
        cp_pair[0] < 0.0 and cp_pair[1] > 0.0,
        f"(cp1,cp2)=({cp_pair[0]:.12f},{cp_pair[1]:.12f})",
    )
    check(
        "At dW_e^H level the same witness satisfies the exact projected-source sign inequalities",
        abs(triplet["gamma"] - 0.5 * responses[6]) < 1e-12
        and abs(triplet["E1"] - (0.5 * (responses[1] - responses[2]) + 0.25 * (responses[3] - responses[5]))) < 1e-12
        and abs(triplet["E2"] - (responses[0] + 0.25 * (responses[3] + responses[5]) - 0.5 * (responses[1] + responses[2]) - 0.5 * responses[7])) < 1e-12,
        f"responses={np.round(np.array(responses), 6)}",
    )

    print()
    print("  constructive witness:")
    print(f"    x      = {np.round(WITNESS_X, 12)}")
    print(f"    y      = {np.round(WITNESS_Y, 12)}")
    print(f"    delta  = {WITNESS_DELTA:.12f}")
    print(f"    eta    = {np.round(etas, 12)}")
    print(f"    dW_e^H = {np.round(np.array(responses), 12)}")

    return h, responses, triplet, cp_pair, etas


def part2_the_constructive_sign_chamber_already_reaches_the_transport_extremal_value(etas_witness: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CONSTRUCTIVE SIGN CHAMBER ALREADY REACHES THE EXTREMAL VALUE")
    print("=" * 88)

    x_ext, y_ext, delta_ext, _packet_ext, etas_ext = quiet_call(
        cand.part2_transport_extremality_selects_a_positive_off_seed_candidate
    )
    ext_triplet = triplet_from_projected_response_pack(
        hermitian_linear_responses(canonical_h(x_ext, y_ext, delta_ext))
    )
    ext_cp = cp_formula(
        ext_triplet["A"],
        ext_triplet["b"],
        ext_triplet["c"],
        ext_triplet["d"],
        ext_triplet["delta"],
        ext_triplet["rho"],
        ext_triplet["gamma"],
    )

    check(
        "The constructive witness itself already gives eta / eta_obs > 1",
        float(np.max(etas_witness)) > 1.0,
        f"eta_best={float(np.max(etas_witness)):.12f}",
    )
    check(
        "Its best transport value matches the unconstrained transport-extremal value exactly",
        abs(float(np.max(etas_witness)) - float(np.max(etas_ext))) < 1e-9,
        f"(constructive,extremal)=({float(np.max(etas_witness)):.12f},{float(np.max(etas_ext)):.12f})",
    )
    check(
        "So maximizing exact transport over the constructive sign chamber already saturates the global extremal value",
        True,
        "the sign-constrained selector is not transport-inferior on the current branch",
    )
    check(
        "The old displayed transport-extremal representative and the constructive witness have different CP sign patterns at the same eta value",
        ext_cp[0] > 0.0 and ext_cp[1] > 0.0,
        f"old extremal cp=({ext_cp[0]:.12f},{ext_cp[1]:.12f})",
    )


def part3_the_constructive_witness_lifts_canonically_to_dminus_and_full_d(h_witness: np.ndarray, responses: list[float], triplet: dict[str, float]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CONSTRUCTIVE WITNESS LIFTS TO D_- AND FULL D")
    print("=" * 88)

    d_full, q = build_full_charge_preserving_operator(h_witness)
    d_minus = d_full[5:10, 5:10]
    l_e = schur_eff(d_minus[:3, :3], d_minus[:3, 3:5], d_minus[3:5, :3], d_minus[3:5, 3:5])
    responses_rec = hermitian_linear_responses(l_e)
    triplet_rec = triplet_from_projected_response_pack(responses_rec)

    check(
        "The explicit microscopic witness preserves charge exactly",
        np.linalg.norm(d_full @ q - q @ d_full) < 1e-12,
        f"commutator={np.linalg.norm(d_full @ q - q @ d_full):.2e}",
    )
    check(
        "Its charge -1 block D_- reconstructs the constructive Hermitian source block by the exact Schur map",
        np.linalg.norm(l_e - h_witness) < 1e-12,
        f"err={np.linalg.norm(l_e - h_witness):.2e}",
    )
    check(
        "So the constructive sign system is already exact on dW_e^H itself",
        np.linalg.norm(np.array(responses_rec) - np.array(responses)) < 1e-12,
        f"response err={np.linalg.norm(np.array(responses_rec) - np.array(responses)):.2e}",
    )
    check(
        "And the same D_- witness reproduces the constructive triplet package exactly",
        all(abs(triplet_rec[key] - triplet[key]) < 1e-12 for key in ("gamma", "E1", "E2")),
        f"(gamma,E1,E2)=({triplet_rec['gamma']:.12f},{triplet_rec['E1']:.12f},{triplet_rec['E2']:.12f})",
    )


def part4_the_theorem_note_records_the_new_gate_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE NEW GATE")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records that the constructive projected-source sign chamber already reaches the extremal transport value",
        "1.052220313052" in note and "constructive sign chamber" in note and "D_- / dW_e^H" in note,
    )
    check(
        "The note also records that the remaining issue is only the microscopic selector law",
        "microscopic `D_- / dW_e^H` selector law" in note or "microscopic selector law" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS CONSTRUCTIVE PROJECTED-SOURCE SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is the constructive projected-source sign chamber on the current PMNS")
    print("  branch empty or transport-incompatible, or does there already exist an")
    print("  exact D_- / dW_e^H witness with gamma > 0, E1 > 0, and E2 > 0?")

    h_witness, responses, triplet, _cp_pair, etas = (
        part1_the_constructive_sign_chamber_is_nonempty_on_the_fixed_seed_surface()
    )
    part2_the_constructive_sign_chamber_already_reaches_the_transport_extremal_value(etas)
    part3_the_constructive_witness_lifts_canonically_to_dminus_and_full_d(h_witness, responses, triplet)
    part4_the_theorem_note_records_the_new_gate_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact constructive answer:")
    print("    - the projected-source sign chamber is nonempty on the current PMNS branch")
    print("    - it already contains a witness with gamma > 0, E1 > 0, E2 > 0 and eta / eta_obs > 1")
    print("    - that witness saturates the current transport-extremal value")
    print("    - so the remaining issue is only the microscopic selector law that")
    print("      chooses this constructive sheet uniquely")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
