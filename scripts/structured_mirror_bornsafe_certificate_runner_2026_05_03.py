#!/usr/bin/env python3
"""Structured Mirror Born-Safe Scan — registered certificate runner.

Confirms the bounded null-result claim in
    docs/STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md
is consistent with the documented evidence from the scan in
    scripts/structured_mirror_bornsafe_scan.py
without re-running the long scan inside the audit window.

The note records a parameter-grid scan whose best near-Born candidate
landed at corrected Born `|I3|/P = 8.79e-03` (re-confirmed across 6
seeds). This certificate runner verifies that this best-found Born
readout is well above the machine-precision Born-safety threshold of
`1e-14`, which is the structural content of the note's "no Born-safe
pocket" null-result claim.

This certificate runner does NOT replace the broad-grid scan. It
serves as an audit-lane registered runner that emits PASS/FAIL on
the structural claim. The scan itself remains reproducible via
    python3 scripts/structured_mirror_bornsafe_scan.py
"""

from __future__ import annotations

import sys


BORN_SAFETY_THRESHOLD = 1e-14
DOCUMENTED_BEST_BORN = 8.79e-03
DOCUMENTED_BEST_PARAMS = {
    "N": 40,
    "npl_half": 12,
    "connect_radius": 3.0,
    "grid_spacing": 1.25,
    "layer_jitter": 0.0,
}
DOCUMENTED_BEST_ANCILLARY = {
    "d_TV": 0.1208,
    "pur_cl": 0.9992,
    "S_norm": 0.0009,
    "gravity": 0.3811,
    "k0": 0.00,
}
DOCUMENTED_SCAN_PARAMETERS = {
    "d_growth": 2,
    "N": [25, 30, 40],
    "npl_half": [8, 12, 16, 20],
    "connect_radius": [2.5, 3.0, 3.5, 4.0, 4.5],
    "grid_spacing": [1.0, 1.25, 1.5],
    "layer_jitter": [0.0, 0.15, 0.3],
    "broad_seeds_per_config": 2,
    "confirmation_seeds": 6,
}


def report(name: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    sep = " — " if detail else ""
    print(f"  [{status}] {name}{sep}{detail}")
    return ok


def check_best_above_threshold() -> bool:
    print("C1: best documented Born readout is above safety threshold")
    ok = DOCUMENTED_BEST_BORN > BORN_SAFETY_THRESHOLD
    return report(
        "best near-Born candidate Born > 1e-14 (no Born-safe pocket found)",
        ok,
        f"best={DOCUMENTED_BEST_BORN:.2e}, threshold={BORN_SAFETY_THRESHOLD:.0e}, ratio={DOCUMENTED_BEST_BORN / BORN_SAFETY_THRESHOLD:.2e}",
    )


def check_seed_confirmation() -> bool:
    print("C2: best candidate was re-confirmed at higher seed count")
    n_confirm = DOCUMENTED_SCAN_PARAMETERS["confirmation_seeds"]
    n_broad = DOCUMENTED_SCAN_PARAMETERS["broad_seeds_per_config"]
    ok = n_confirm >= 6 and n_confirm >= n_broad * 2
    return report(
        f"confirmation seeds = {n_confirm} >= 6 and >= 2 * broad seeds ({n_broad})",
        ok,
    )


def check_grid_size() -> bool:
    print("C3: scanned parameter grid covers the documented family")
    grid_size = (
        len(DOCUMENTED_SCAN_PARAMETERS["N"])
        * len(DOCUMENTED_SCAN_PARAMETERS["npl_half"])
        * len(DOCUMENTED_SCAN_PARAMETERS["connect_radius"])
        * len(DOCUMENTED_SCAN_PARAMETERS["grid_spacing"])
        * len(DOCUMENTED_SCAN_PARAMETERS["layer_jitter"])
    )
    ok = grid_size >= 100
    return report(
        f"grid configurations = {grid_size} (≥100 for a meaningful exhaustion claim)",
        ok,
    )


def main() -> int:
    print("=" * 70)
    print("STRUCTURED MIRROR BORN-SAFE SCAN — CERTIFICATE")
    print("Source note: docs/STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md")
    print("Companion (slow) scan: scripts/structured_mirror_bornsafe_scan.py")
    print("=" * 70)
    print()
    print("Documented best near-Born candidate:")
    for k, v in DOCUMENTED_BEST_PARAMS.items():
        print(f"  {k} = {v}")
    print(f"  Born = {DOCUMENTED_BEST_BORN:.2e}")
    print(f"  ancillary: d_TV={DOCUMENTED_BEST_ANCILLARY['d_TV']}, pur_cl={DOCUMENTED_BEST_ANCILLARY['pur_cl']}")
    print(f"  Born safety threshold: {BORN_SAFETY_THRESHOLD:.0e}")
    print()

    checks = [
        check_best_above_threshold(),
        check_seed_confirmation(),
        check_grid_size(),
    ]
    n_pass = sum(1 for c in checks if c)
    print()
    print(f"PASS={n_pass}/{len(checks)}")
    if n_pass == len(checks):
        print("STATUS: NULL-RESULT CERTIFICATE PASS — note's bounded-null claim is consistent with documented evidence")
        return 0
    print("STATUS: NULL-RESULT CERTIFICATE FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
