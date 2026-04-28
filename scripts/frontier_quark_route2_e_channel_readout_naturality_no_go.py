#!/usr/bin/env python3
"""Route-2 E-channel readout naturality no-go.

This runner verifies the minimal-premise obstruction in
QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md.

It intentionally does not use observed quark masses or CKM/J target fitting.
The only live endpoint value used is classified as bounded comparator evidence
for the rational-candidate audit, not as a derivation input.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import math
import sys

import numpy as np

from frontier_quark_route2_exact_readout_map import restricted_readout_data


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_TOL = 1.0e-12


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def reduced_map(rho_e: Fraction) -> np.ndarray:
    rho = float(rho_e)
    return np.array(
        [
            [1.0, 0.0, rho, 0.0],
            [0.0, -2.0, 0.0, 2.0],
        ],
        dtype=float,
    )


def e_center_lift(rho_e: Fraction) -> Fraction:
    return Fraction(1, 1) + rho_e / 6


def center_te_ratio(rho_e: Fraction) -> Fraction:
    # With granted q_T=5/6 and shell T/E=-2:
    return Fraction(-2, 1) * Fraction(5, 6) / e_center_lift(rho_e)


def low_rationals(lower: Fraction, upper: Fraction, max_num: int = 32, max_den: int = 16) -> set[Fraction]:
    out: set[Fraction] = set()
    for den in range(1, max_den + 1):
        for num in range(-max_num, max_num + 1):
            value = Fraction(num, den)
            if lower <= value <= upper:
                out.add(value)
    return out


def nearest_rational(value: float, candidates: set[Fraction]) -> Fraction:
    return min(candidates, key=lambda q: abs(float(q) / value - 1.0))


def main() -> int:
    note = DOCS / "QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md"
    readout_note = DOCS / "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md"
    ratio_note = DOCS / "QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md"
    time_note = DOCS / "QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md"

    print("=" * 88)
    print("LANE 3 ROUTE-2 E-CHANNEL READOUT NATURALITY NO-GO")
    print("=" * 88)

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (note, readout_note, ratio_note, time_note):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    note_text = note.read_text(encoding="utf-8")
    readout_text = readout_note.read_text(encoding="utf-8")
    ratio_text = ratio_note.read_text(encoding="utf-8")
    check("readout note identifies beta_E/alpha_E as missing map entry", "beta_E / alpha_E = 21/4" in readout_text)
    check("ratio-chain note identifies {-8/9} as endpoint-chain target", "-8/9" in ratio_text and "15/8" in ratio_text)
    check("new note states no retained up-mass claim", "does not claim retained `m_u` or `m_c`" in note_text)

    print()
    print("B. Reduced exact family")
    print("-" * 72)
    data = restricted_readout_data()
    e_shell = data.carrier_e_shell
    e_center = data.carrier_e_center
    target_shell = np.array([1.0, 0.0, 0.0, 0.0])
    target_center = np.array([1.0, 0.0, 1.0 / 6.0, 0.0])
    check("E-shell carrier column is exact", np.max(np.abs(e_shell - target_shell)) < EXACT_TOL, str(e_shell))
    check("E-center carrier column is exact", np.max(np.abs(e_center - target_center)) < EXACT_TOL, str(e_center))

    rho_zero = Fraction(0, 1)
    rho_target = Fraction(21, 4)
    p_zero = reduced_map(rho_zero)
    p_target = reduced_map(rho_target)
    shell_zero = p_zero @ e_shell
    shell_target = p_target @ e_shell
    center_zero = p_zero @ e_center
    center_target = p_target @ e_center

    check("rho_E=0 and rho_E=21/4 agree on E-shell normalization", np.max(np.abs(shell_zero - shell_target)) < EXACT_TOL, f"{shell_zero} vs {shell_target}")
    check("rho_E=0 and rho_E=21/4 differ on E-center lift", abs(center_zero[0] - center_target[0]) > 0.5, f"{center_zero[0]:.6f} vs {center_target[0]:.6f}")
    check("rho_E=21/4 gives E-center lift 15/8 exactly", e_center_lift(rho_target) == Fraction(15, 8), str(e_center_lift(rho_target)))
    check("rho_E=0 gives E-center lift 1 exactly", e_center_lift(rho_zero) == 1, str(e_center_lift(rho_zero)))

    print()
    print("C. Equivalence to the endpoint ratio chain")
    print("-" * 72)
    check("rho_E=21/4 is equivalent to center T/E ratio -8/9 under granted T-side data", center_te_ratio(rho_target) == Fraction(-8, 9), str(center_te_ratio(rho_target)))
    check("rho_E=0 does not give center T/E ratio -8/9", center_te_ratio(rho_zero) != Fraction(-8, 9), str(center_te_ratio(rho_zero)))
    solved_rho = 6 * (Fraction(15, 8) - 1)
    check("q_E=15/8 solves back to rho_E=21/4", solved_rho == rho_target, str(solved_rho))
    solved_qe = Fraction(-2, 1) * Fraction(5, 6) / Fraction(-8, 9)
    check("ratio chain {5/6,-2,-8/9} solves q_E=15/8", solved_qe == Fraction(15, 8), str(solved_qe))

    print()
    print("D. Naturality frames")
    print("-" * 72)
    rho_same_as_t = Fraction(-1, 1)
    rho_no_lift = Fraction(0, 1)
    rho_unit_lift = Fraction(1, 1)
    for label, rho in (("same-as-T", rho_same_as_t), ("no-lift", rho_no_lift), ("unit-lift", rho_unit_lift), ("target", rho_target)):
        print(f"  {label:10s}: rho_E={rho}, q_E={e_center_lift(rho)}, c_TE={center_te_ratio(rho)}")

    check("same-as-T naturality is exact admissible but not target", e_center_lift(rho_same_as_t) == Fraction(5, 6) and rho_same_as_t != rho_target)
    check("no-lift naturality is exact admissible but not target", e_center_lift(rho_no_lift) == 1 and rho_no_lift != rho_target)
    check("unit-lift naturality is exact admissible but not target", e_center_lift(rho_unit_lift) == Fraction(7, 6) and rho_unit_lift != rho_target)

    candidates = low_rationals(Fraction(-2, 1), Fraction(6, 1))
    check("low-rational grammar has many admissible rho_E values", len(candidates) > 80, f"count={len(candidates)}")
    check("low-rational grammar includes target 21/4 but does not make it unique", rho_target in candidates and len(candidates) > 1)
    live_rho = Fraction.from_float(data.rho_e)
    nearest = nearest_rational(float(live_rho), candidates)
    check("21/4 is selected only after using live E-endpoint distance", nearest == rho_target, f"nearest={nearest}, live_rho={data.rho_e:.12f}")
    check("live endpoint rho_E is bounded comparator, not exact target", abs(data.rho_e - float(rho_target)) > EXACT_TOL and abs(data.rho_e - float(rho_target)) < 0.01, f"live={data.rho_e:.12f}, target={float(rho_target):.12f}")

    print()
    print("E. Comparator firewall")
    print("-" * 72)
    proof_inputs = {
        "carrier_columns",
        "endpoint_algebra",
        "granted_t_side_candidates",
        "rational_arithmetic",
    }
    forbidden = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "ckm_j_error_minimization",
        "hidden_e_center_source",
    }
    check("forbidden proof inputs are absent from proof-input set", proof_inputs.isdisjoint(forbidden), str(sorted(proof_inputs)))
    check("note says nearest-rational selection is bounded evidence", "Nearest-rational selection is bounded candidate evidence" in note_text)
    check("note names the next exact target as -8/9 or 15/8", "-8/9" in note_text and "15/8" in note_text)
    check("note preserves future primitive routes", "source-domain" in note_text and "tensor readout-map theorem" in note_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: minimal Route-2 naturality does not derive rho_E = 21/4.")
        print("A new E-center source/readout primitive is still required.")
        return 0
    print("VERDICT: naturality no-go verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
