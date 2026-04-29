#!/usr/bin/env python3
"""Route-2 R_conn center-ratio bridge obstruction.

This runner verifies a block-02 Lane 3 stretch attempt on the sharp Route-2
E-center residual:

    gamma_T(center) / gamma_E(center) = -8/9.

The tempting observation is that 8/9 is the retained SU(3) connected color
projection R_conn = (N_c^2 - 1) / N_c^2 at N_c = 3.  The runner proves the
conditional algebra and the import boundary: imposing c_TE = -R_conn gives the
target rho_E = 21/4, but the current restricted Route-2 carrier contains no
typed source-domain map from the SU(3) color projection to the E/T center
endpoint ratio.  Therefore R_conn is a conditional bridge target, not a
derivation of the up-type scalar law.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
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


def percent_gap(value: float, target: float) -> float:
    return abs(value / target - 1.0) * 100.0


def r_conn(n_c: int = 3) -> Fraction:
    return Fraction(n_c * n_c - 1, n_c * n_c)


def q_e_from_center_ratio(c_te: Fraction, q_t: Fraction = Fraction(5, 6), shell_te: Fraction = Fraction(-2, 1)) -> Fraction:
    return shell_te * q_t / c_te


def rho_e_from_center_ratio(c_te: Fraction) -> Fraction:
    q_e = q_e_from_center_ratio(c_te)
    return 6 * (q_e - 1)


def reduced_map(rho_e: Fraction) -> np.ndarray:
    rho = float(rho_e)
    return np.array(
        [
            [1.0, 0.0, rho, 0.0],
            [0.0, -2.0, 0.0, 2.0],
        ],
        dtype=float,
    )


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    note = DOCS / "QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md"
    rconn_note = DOCS / "RCONN_DERIVED_NOTE.md"
    readout_note = DOCS / "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md"
    naturality_note = DOCS / "QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md"
    bilinear_note = DOCS / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"

    print("=" * 88)
    print("LANE 3 ROUTE-2 R_CONN CENTER-RATIO BRIDGE OBSTRUCTION")
    print("=" * 88)

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (note, rconn_note, readout_note, naturality_note, bilinear_note):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    note_text = read(note)
    rconn_text = read(rconn_note)
    readout_text = read(readout_note)
    naturality_text = read(naturality_note)
    bilinear_text = read(bilinear_note)

    check("R_conn note carries the SU(3) 8/9 value", "R_conn = (N_c^2 - 1) / N_c^2" in rconn_text and "8/9" in rconn_text)
    check("readout note names -8/9 as the missing center ratio", "-8/9" in readout_text and "beta_E / alpha_E = 21/4" in readout_text)
    check("naturality note keeps -8/9 as an open E-center target", "derive gamma_T(center)/gamma_E(center) = -8/9" in naturality_text)
    check(
        "new note does not claim retained non-top quark masses",
        "does not claim\nretained `m_u` or `m_c`" in note_text
        or "does not claim retained `m_u` or `m_c`" in note_text,
    )

    print()
    print("B. Conditional exact bridge algebra")
    print("-" * 72)
    r = r_conn(3)
    center_target = -r
    q_e = q_e_from_center_ratio(center_target)
    rho_e = rho_e_from_center_ratio(center_target)
    check("N_c=3 gives R_conn=8/9 exactly", r == Fraction(8, 9), str(r))
    check("imposing c_TE=-R_conn gives q_E=15/8 exactly", q_e == Fraction(15, 8), str(q_e))
    check("imposing c_TE=-R_conn gives rho_E=21/4 exactly", rho_e == Fraction(21, 4), str(rho_e))
    check("rho_E=21/4 maps back to c_TE=-8/9 under granted T-side data", rho_e_from_center_ratio(Fraction(-8, 9)) == Fraction(21, 4))

    for n_c, expected in ((2, Fraction(22, 3)), (3, Fraction(21, 4)), (4, Fraction(14, 3))):
        rho = rho_e_from_center_ratio(-r_conn(n_c))
        check(f"general N_c={n_c} conditional rho_E is exact", rho == expected, f"rho_E={rho}")

    print()
    print("C. Live bounded comparator")
    print("-" * 72)
    data = restricted_readout_data()
    live_center_ratio = data.center_ratio_te
    live_rho = data.rho_e
    check("live center T/E ratio is close to -R_conn but not exact", percent_gap(live_center_ratio, float(center_target)) < 0.25 and abs(live_center_ratio - float(center_target)) > EXACT_TOL, f"live={live_center_ratio:.12f}, target={float(center_target):.12f}, gap={percent_gap(live_center_ratio, float(center_target)):.6f}%")
    check("live rho_E is close to 21/4 but not exact", percent_gap(live_rho, float(Fraction(21, 4))) < 0.2 and abs(live_rho - float(Fraction(21, 4))) > EXACT_TOL, f"live={live_rho:.12f}, target={float(Fraction(21, 4)):.12f}, gap={percent_gap(live_rho, float(Fraction(21, 4))):.6f}%")

    print()
    print("D. Import-boundary witness")
    print("-" * 72)
    e_shell = data.carrier_e_shell
    e_center = data.carrier_e_center
    t_shell = data.carrier_t_shell
    t_center = data.carrier_t_center
    p_zero = reduced_map(Fraction(0, 1))
    p_target = reduced_map(Fraction(21, 4))

    check("rho_E=0 and rho_E=21/4 agree on E-shell", np.max(np.abs(p_zero @ e_shell - p_target @ e_shell)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 agree on the granted T-side shell", np.max(np.abs(p_zero @ t_shell - p_target @ t_shell)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 agree on the granted T-side center", np.max(np.abs(p_zero @ t_center - p_target @ t_center)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 differ only at E-center", abs((p_zero @ e_center)[0] - (p_target @ e_center)[0]) > 0.5, f"{(p_zero @ e_center)[0]:.6f} vs {(p_target @ e_center)[0]:.6f}")

    route2_mentions_rconn = "R_conn" in readout_text or "R_conn" in naturality_text or "R_conn" in bilinear_text
    route2_mentions_color_trace = "color trace" in readout_text.lower() or "color trace" in naturality_text.lower() or "color trace" in bilinear_text.lower()
    rconn_mentions_route2 = "Route-2" in rconn_text or "Theta_R" in rconn_text or "E-center" in rconn_text
    check("current Route-2 readout surfaces do not type the R_conn bridge", not route2_mentions_rconn and not route2_mentions_color_trace)
    check("R_conn surface does not identify a Route-2 E/T endpoint ratio", not rconn_mentions_route2)

    proof_inputs = {
        "restricted_route2_carrier",
        "endpoint_algebra",
        "granted_t_side_candidates",
        "retained_rconn_value",
        "exact_rational_arithmetic",
    }
    forbidden = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "ckm_j_error_minimization",
        "nearest_live_endpoint_selector",
    }
    check("forbidden proof inputs are absent", proof_inputs.isdisjoint(forbidden), str(sorted(proof_inputs)))
    check("new note states the load-bearing missing bridge", "source-domain identification" in note_text and "not a derivation" in note_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: -R_conn is a sharp conditional bridge to rho_E=21/4,")
        print("but the source-domain identification is still missing.")
        return 0
    print("VERDICT: R_conn bridge obstruction verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
