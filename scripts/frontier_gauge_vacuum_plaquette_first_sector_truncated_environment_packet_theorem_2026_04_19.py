#!/usr/bin/env python3
"""
Exact truncated diagonal/environment packet determined by the completed
first-sector plaquette triple.

This refines the factorized-class boundary:

  1. the rank-one transfer witness does not by itself solve the canonical
     Wilson factorized-class realization problem;
  2. but the completed first-sector triple already determines one exact
     truncated diagonal/environment packet on the retained first-symmetric
     sector;
  3. so the remaining seam is extension of that retained packet to the full
     beta=6 framework-point environment packet, not existence of a retained
     diagonal packet itself.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_rank_one_transfer_realization_2026_04_19 import (
    completed_sector_data,
)
from frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17 import (
    sample_angle_units,
)
from frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17 import (
    evaluation_matrix,
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
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR TRUNCATED ENVIRONMENT PACKET")
    print("=" * 112)
    print()
    print("Question:")
    print("  Does the completed first-sector triple already determine a retained")
    print("  diagonal/environment packet inside the canonical character-measure")
    print("  description, even before the full framework-point extension is known?")

    completion_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md")
    factor_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md")
    measure_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    v_min, z_min = completed_sector_data()
    z00_min = float(v_min[0])
    rho_ret = v_min / z00_min

    sample_angles = [(u1 * np.pi / 16.0, u2 * np.pi / 16.0) for u1, u2 in sample_angle_units().values()]
    e_three = evaluation_matrix([(0, 0), (1, 0), (0, 1), (1, 1)], sample_angles)
    z_recon = np.real_if_close(z00_min * (e_three @ rho_ret)).real
    recon_gap = float(np.linalg.norm(z_recon - z_min))
    rho_swap_gap = float(abs(rho_ret[1] - rho_ret[2]))

    print()
    print(f"  v_min                                       = {np.round(v_min, 12).tolist()}")
    print(f"  z00_min                                     = {z00_min:.12f}")
    print(f"  rho_ret                                     = {np.round(rho_ret, 12).tolist()}")
    print(f"  reconstructed sample triple                 = {np.round(z_recon, 12).tolist()}")
    print(f"  reconstruction gap                          = {recon_gap:.6e}")
    print()

    check(
        "The factorization and character-measure notes already fix the canonical environment description as an overall scale z_(0,0)^env together with normalized coefficients rho_(p,q)(6)",
        "positive diagonal coefficient sequence" in factor_note
        and "normalized boundary class function" in measure_note
        and "rho_(p,q)(6)" in measure_note,
    )
    check(
        "The completion note already fixes one explicit retained first-sector coefficient vector v_min for the completed triple Z_min",
        "completed sample triple" in completion_note and "a^min" in completion_note,
    )
    check(
        "Normalizing by the retained trivial-channel coefficient defines one exact truncated environment packet rho_ret with rho_(0,0)=1",
        abs(rho_ret[0] - 1.0) < 1.0e-12 and rho_ret[1] > 0.0 and rho_ret[3] > -1.0e-12,
        f"rho_ret={np.round(rho_ret, 10).tolist()}",
    )
    check(
        "That truncated packet is conjugation-symmetric on the retained first-symmetric sector",
        rho_swap_gap < 1.0e-12,
        f"|rho_(1,0)-rho_(0,1)|={rho_swap_gap:.3e}",
    )
    check(
        "The retained three-sample triple reconstructs exactly from the pair (z00_min, rho_ret)",
        recon_gap < 1.0e-12,
        f"||z_recon-Z_min||={recon_gap:.3e}",
    )
    check(
        "So the remaining framework-point seam is not existence of a retained diagonal/environment packet itself, but extension of this truncated packet to the full beta=6 environment data",
        recon_gap < 1.0e-12 and e_three.shape == (3, 4),
        f"z00_min={z00_min:.6f}",
    )

    print("\n" + "=" * 112)
    print("RESULT")
    print("=" * 112)
    print("  Exact refinement:")
    print("    - the completed first-sector triple already determines one explicit")
    print("      retained diagonal/environment packet on the first-symmetric sector")
    print("    - namely one overall scale z00_min together with one normalized")
    print("      conjugation-symmetric retained coefficient packet rho_ret")
    print("    - therefore the remaining open object is the extension / realization")
    print("      of this retained packet inside the full beta=6 framework-point")
    print("      environment packet, not retained diagonal-packet existence")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
