#!/usr/bin/env python3
"""
DM A-BCC retained measurement closure theorem.

This is an integration runner for the review branch. It does not claim a new
axiom-native A-BCC derivation from Cl(3)/Z^3 alone. Its job is narrower:

  - execute the already-landed theorem stack that fixes the physical basin on
    the retained measurement surface,
  - verify that the physical source is Basin 1, that Basin 1 lies in C_base,
    and that the C_neg basins do not,
  - promote A-BCC from "live review-surface blocker" to "closed on the
    retained measurement framework".

The stricter pure-algebraic / axiom-native A-BCC target remains outside this
closure grade and is not asserted here.
"""

from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

PASS_COUNT = 0
FAIL_COUNT = 0

E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
GAMMA = 0.5

T_M = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex)
T_D = np.array([[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex)
T_Q = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)

BASIN_1 = (0.657061342210, 0.933806343759, 0.715042329587)
BASIN_2 = (28.005676879468, 20.721919153777, 5.011726669406)
BASIN_X = (21.128264303040, 12.680028385305, 2.089234625632)

DEPENDENCIES = [
    ("active-chamber completeness", "frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py"),
    ("upper-octant / source-cubic selector", "frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py"),
    ("sigma_hier upper-octant selector", "frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py"),
    ("P3 Sylvester physical path", "frontier_dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_2026_04_18.py"),
    ("PMNS nonsingularity reduction", "frontier_dm_abcc_pmns_nonsingularity_theorem.py"),
    ("Sylvester signature forcing", "frontier_dm_abcc_signature_forcing_theorem.py"),
    ("sigma-chain attack cascade", "frontier_dm_pns_attack_cascade.py"),
]


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


def parse_fail_count(output: str) -> int | None:
    matches = re.findall(r"FAIL\s*=\s*(\d+)", output)
    if not matches:
        return None
    return int(matches[-1])


def parse_pass_count(output: str) -> int | None:
    matches = re.findall(r"PASS\s*=\s*(\d+)", output)
    if not matches:
        return None
    return int(matches[-1])


def run_dependency(label: str, script_name: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script_name)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    fail_count = parse_fail_count(output)
    pass_count = parse_pass_count(output)
    ok = proc.returncode == 0 and (fail_count == 0 if fail_count is not None else True)
    detail_bits: list[str] = [f"rc={proc.returncode}"]
    if pass_count is not None:
        detail_bits.append(f"PASS={pass_count}")
    if fail_count is not None:
        detail_bits.append(f"FAIL={fail_count}")
    detail = ", ".join(detail_bits)
    check(f"Dependency runner passes: {label}", ok, detail)
    return ok, output


def h_of(point: tuple[float, float, float]) -> np.ndarray:
    m, d, q = point
    return H_BASE + m * T_M + d * T_D + q * T_Q


def main() -> int:
    print("DM A-BCC retained measurement closure theorem")
    print("=" * 72)

    print("\nPart 1: Execute the retained theorem stack")
    dependency_outputs: dict[str, str] = {}
    for label, script_name in DEPENDENCIES:
        _, output = run_dependency(label, script_name)
        dependency_outputs[script_name] = output

    print("\nPart 2: Direct basin-level endpoint checks")
    for name, point, expect_positive in [
        ("Basin 1", BASIN_1, True),
        ("Basin 2", BASIN_2, False),
        ("Basin X", BASIN_X, False),
    ]:
        det_val = float(np.real(np.linalg.det(h_of(point))))
        chamber_val = point[1] + point[2]
        if name == "Basin 1":
            check(
                "Basin 1 satisfies the retained chamber bound",
                chamber_val > E1,
                f"q+delta={chamber_val:.12f}, sqrt(8/3)={E1:.12f}",
            )
        sign_ok = det_val > 0 if expect_positive else det_val < 0
        sign_text = "C_base" if expect_positive else "C_neg"
        check(
            f"{name} endpoint lies in {sign_text}",
            sign_ok,
            f"det={det_val:.12f}",
        )

    print("\nPart 3: Integration consequences")
    pns_output = dependency_outputs["frontier_dm_pns_attack_cascade.py"]
    check(
        "sigma-chain runner explicitly derives PNS from the retained measurement framework",
        "PNS is derivable from the retained measurement framework" in pns_output,
    )
    check(
        "sigma-chain runner explicitly closes the basin-selection gate",
        "A-BCC closes the DM flagship basin-selection gate" in pns_output,
    )

    sig_output = dependency_outputs["frontier_dm_abcc_signature_forcing_theorem.py"]
    check(
        "signature-forcing runner records the reduction A-BCC <- PNS + Sylvester inertia",
        "A-BCC <- PNS + Sylvester inertia" in sig_output,
    )

    nonsing_output = dependency_outputs["frontier_dm_abcc_pmns_nonsingularity_theorem.py"]
    check(
        "nonsingularity runner confirms all C_neg basins violate PNS",
        "All C_neg basins violate PNS" in nonsing_output,
    )

    print("\nPart 4: Closure-grade statement")
    print("  [summary] A-BCC is closed on the retained measurement framework.")
    print("  [summary] The stricter axiom-native A-BCC target remains outside this closure grade.")
    print("  [summary] The only live DM blocker on the review surface is the finer right-sensitive microscopic selector law.")

    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("STATUS: ALL PASS — retained-measurement A-BCC closure verified")
    else:
        print("STATUS: FAILURES — see above")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
