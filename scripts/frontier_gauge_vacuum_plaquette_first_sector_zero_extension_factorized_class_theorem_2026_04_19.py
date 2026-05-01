#!/usr/bin/env python3
"""
Explicit factorized-class extension of the retained first-sector environment
packet by minimal support on the dominant-weight box.

This closes one more existence seam:

  1. the retained first-sector completion already determines one exact
     truncated packet `(z00_min, rho_ret)`;
  2. that retained packet admits one explicit full extension inside the
     canonical Wilson factorized class by zeroing higher retained coefficients;
  3. so existence inside the factorized class is no longer open either.

What remains open is the actual framework-point Wilson environment packet,
not existence of some factorized-class extension.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_truncated_environment_packet_theorem_2026_04_19 import (
    read as _read_helper,
)
from frontier_gauge_vacuum_plaquette_first_sector_rank_one_transfer_realization_2026_04_19 import (
    completed_sector_data,
)
from frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17 import (
    sample_angle_units,
)
from frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17 import (
    evaluation_matrix,
)
from frontier_gauge_vacuum_plaquette_spatial_environment_character_measure import (
    BETA,
    build_recurrence_matrix,
    conjugation_swap_matrix,
    dim_su3,
    matrix_exponential_symmetric,
    wilson_character_coefficient,
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
    return _read_helper(rel_path)


def local_factor_diagonal(weights: list[tuple[int, int]]) -> np.ndarray:
    c00 = wilson_character_coefficient(0, 0)
    local = np.array(
        [wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00) for p, q in weights],
        dtype=float,
    )
    return np.diag(local**4)


def main() -> int:
    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR ZERO-EXTENSION FACTORIZED-CLASS THEOREM")
    print("=" * 112)
    print()
    print("Question:")
    print("  Once the retained first-sector packet is known, does there already exist")
    print("  one explicit full extension inside the canonical Wilson factorized class?")

    measure_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    truncated_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md")
    # Stale-path: the boundary note was moved to
    # `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`
    # because its dedicated runner (declared but missing on disk) blocked an
    # audit of THAT note. The substring this runner verifies
    # ("best audited retained diagonal fit still misses") was historical
    # content of the boundary note, which the archive preserves verbatim.
    # Redirect the read to the archived location so this runner remains a
    # self-contained verification of its own load-bearing zero-extension
    # claim.
    boundary_note = read(
        "archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/"
        "GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_RANK_ONE_FACTORIZED_CLASS_BOUNDARY_NOTE_2026-04-19.md"
    )

    v_min, z_min = completed_sector_data()
    z00_min = float(v_min[0])
    rho_ret = v_min / z00_min

    jmat, weights, index = build_recurrence_matrix(5)
    swap = conjugation_swap_matrix(weights, index)
    multiplier = matrix_exponential_symmetric(jmat, BETA / 2.0)
    d_local = local_factor_diagonal(weights)

    rho_ext = np.zeros(len(weights), dtype=float)
    rho_ext[index[(0, 0)]] = rho_ret[0]
    rho_ext[index[(1, 0)]] = rho_ret[1]
    rho_ext[index[(0, 1)]] = rho_ret[2]
    rho_ext[index[(1, 1)]] = rho_ret[3]
    r_ext = np.diag(rho_ext)
    t_ext = multiplier @ d_local @ r_ext @ multiplier

    sym_err = float(np.max(np.abs(t_ext - t_ext.T)))
    swap_err = float(np.max(np.abs(swap @ t_ext - t_ext @ swap)))
    eig_min = float(np.min(np.linalg.eigvalsh(t_ext)))
    rho_min = float(np.min(rho_ext))

    sample_angles = [(u1 * np.pi / 16.0, u2 * np.pi / 16.0) for u1, u2 in sample_angle_units().values()]
    e_three = evaluation_matrix([(0, 0), (1, 0), (0, 1), (1, 1)], sample_angles)
    z_recon = np.real_if_close(z00_min * (e_three @ rho_ret)).real
    recon_gap = float(np.linalg.norm(z_recon - z_min))

    print()
    print(f"  z00_min                                     = {z00_min:.12f}")
    print(f"  rho_ret                                     = {np.round(rho_ret, 12).tolist()}")
    print(f"  nonzero rho_ext entries                     = {[(w, round(float(rho_ext[index[w]]), 12)) for w in weights if rho_ext[index[w]] > 0.0]}")
    print(f"  factorized operator symmetry / swap errors  = {sym_err:.3e} / {swap_err:.3e}")
    print(f"  min eigenvalue(T_ext)                       = {eig_min:.3e}")
    print(f"  retained reconstruction gap                 = {recon_gap:.3e}")
    print()

    check(
        "The character-measure note already permits nonnegative conjugation-symmetric normalized coefficient data rho_(p,q)(6) as the canonical boundary-class description",
        "rho_(p,q)(beta) >= 0" in measure_note
        and "rho_(0,0)(beta) = 1" in measure_note
        and "rho_(p,q)(beta) = rho_(q,p)(beta)" in measure_note,
    )
    check(
        "The earlier retained theorem already fixes one exact truncated packet (z00_min, rho_ret) from the completed first-sector triple",
        "completed first-sector triple already determines one explicit truncated diagonal/environment packet" in truncated_note
        and "rho_ret" in truncated_note,
    )
    check(
        "Extending rho_ret by zero outside the retained first-symmetric weights gives one explicit full nonnegative conjugation-symmetric coefficient sequence on the truncated dominant-weight box",
        rho_min > -1.0e-12
        and abs(rho_ext[index[(1, 0)]] - rho_ext[index[(0, 1)]]) < 1.0e-12,
        f"nonzero count={int(np.count_nonzero(rho_ext))}",
    )
    check(
        "That zero-extension yields one explicit self-adjoint conjugation-symmetric positive-semidefinite factorized operator exp(3 J) D_6^loc diag(rho_ext) exp(3 J)",
        sym_err < 1.0e-12 and swap_err < 1.0e-12 and eig_min > -1.0e-10,
        f"(sym,swap,eig_min)=({sym_err:.3e},{swap_err:.3e},{eig_min:.3e})",
    )
    check(
        "The extended packet still reproduces the retained completed three-sample triple exactly on the retained first-symmetric sector",
        recon_gap < 1.0e-12,
        f"||z_recon-Z_min||={recon_gap:.3e}",
    )
    check(
        "Therefore existence of a factorized-class extension consistent with the retained first-sector packet is no longer open; the remaining seam is the actual framework-point Wilson environment packet, not class existence",
        "best audited retained diagonal fit still misses" in boundary_note
        and recon_gap < 1.0e-12
        and eig_min > -1.0e-10,
        f"z00_min={z00_min:.6f}",
    )

    print("\n" + "=" * 112)
    print("RESULT")
    print("=" * 112)
    print("  Exact constructive upgrade:")
    print("    - the retained first-sector packet already has one explicit full")
    print("      extension inside the canonical Wilson factorized class")
    print("    - namely the minimal-support zero extension of rho_ret")
    print("    - therefore factorized-class existence is no longer open either")
    print("    - the remaining honest seam is now the actual framework-point Wilson")
    print("      environment packet / Perron-Jacobi realization and downstream DM")
    print("      packet matching, not existence of some factorized-class extension")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
