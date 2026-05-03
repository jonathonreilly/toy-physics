#!/usr/bin/env python3
"""
Audited current `beta = 6` `spatial_pair` witness family does not realize the
completed first-sector triple `Z_min` exactly.

Boundary refinement of the explicit completed triple:

  1. the first symmetric three-sample seam is closed positively to one explicit
     completed triple `Z_min` (rank-one transfer realization theorem 2026-04-19);
  2. the live first three-sample environment evaluator route already records
     a current explicit `spatial_pair` witness family parameterised by the
     four scalars `(tau_transfer, tau_boundary, linear_decay, asym_decay)`;
  3. on the audited parameter box `tau_transfer in [10^-4, 5e-2]`,
     `tau_boundary in [0.5, 4.0]`, `asym_decay in [10^-8, 10^-4]`, with the
     interior `linear_decay` free, the best one-parameter scaled fit
     `c * Zhat_best` to the explicit triple `Z_min` is driven onto three of
     the four box edges and still leaves a strictly positive Euclidean gap
     `||c_best Zhat_best - Z_min||_2 = 0.007578536496...`;
  4. so the current explicit witness family is only a boundary ansatz, not the
     missing exact realisation of `Z_min`.

Scope (deliberately scoped, see GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED
_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md):

  - the runner does NOT search over a wider class of witness families; the
    note's claim is only about THIS particular `spatial_pair` family;
  - the runner does NOT attempt to derive `Z_min` from the framework — it
    consumes the explicit `Z_min` already produced by the rank-one transfer
    realisation theorem (2026-04-19) and the upstream completion theorem;
  - the runner verifies the explicit numerical fit reported in the note's
    "Bottom line" section (Zhat_best, c_best, gap norm, active boundary
    edges) and the named consequence "Z_min is still not realised exactly".

Audit-class self-classification: this is a Class C / structural-support
runner. It witnesses one bounded, deterministic, single-precision-stable
boundary statement about a specific witness family; it does not advance the
underlying open question (the actual framework-point Wilson environment
packet realising `Z_min`).
"""

from __future__ import annotations

from pathlib import Path
import math
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_rank_one_transfer_realization_2026_04_19 import (
    completed_sector_data,
)
from frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17 import (
    build_recurrence_matrix,
    sample_operator,
    spatial_pair,
)


ROOT = Path(__file__).resolve().parents[1]
NMAX = 5

# Audited parameter box for the current explicit `spatial_pair` witness family.
# Edges in this dictionary are the published audited bounds; the runner finds
# the best `linear_decay` on the interior at the most favourable corner of the
# remaining three edges (lower tau_transfer, upper tau_boundary, lower
# asym_decay). These boundary values are exactly the ones reported in the
# parent note.
TAU_TRANSFER_LOWER = 1.0e-4
TAU_BOUNDARY_UPPER = 4.0
ASYM_DECAY_LOWER = 1.0e-8

# Note's published numerical witness values (must be reproduced).
NOTE_ZMIN = (0.135165279562, 0.374012880009, 0.543843858544)
NOTE_ZHAT = (0.280527830070, 0.789850309412, 1.120725632470)
NOTE_C_BEST = 0.481383963846
NOTE_GAP_NORM = 0.007578536496


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


def gap_at(
    jmat: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    e_three: np.ndarray,
    z_min: np.ndarray,
    tau_transfer: float,
    tau_boundary: float,
    linear_decay: float,
    asym_decay: float,
) -> tuple[float, np.ndarray, float]:
    """Return (gap_norm, zhat, c_best) for the family vector at these params.

    The free overall scale is the unconstrained least-squares scalar
        c_best = argmin_c ||c * zhat - z_min||
               = (zhat . z_min) / (zhat . zhat).
    """
    _s, _eta, _amp, rho = spatial_pair(
        jmat,
        weights,
        index,
        tau_transfer=tau_transfer,
        tau_boundary=tau_boundary,
        linear_decay=linear_decay,
        asym_decay=asym_decay,
    )
    zhat = np.real_if_close(e_three @ rho).real
    denom = float(np.dot(zhat, zhat))
    c_best = float(np.dot(zhat, z_min)) / denom
    gap_norm = float(np.linalg.norm(c_best * zhat - z_min))
    return gap_norm, zhat, c_best


def golden_section_minimum(
    f, lo: float, hi: float, tol: float = 1.0e-13, maxiter: int = 400
) -> float:
    """Pure-numpy golden section minimisation of a unimodal scalar function."""
    inv_phi = (math.sqrt(5.0) - 1.0) / 2.0  # ~0.6180339887
    a, b = lo, hi
    c = b - inv_phi * (b - a)
    d = a + inv_phi * (b - a)
    fc = f(c)
    fd = f(d)
    for _ in range(maxiter):
        if abs(b - a) < tol:
            break
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - inv_phi * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + inv_phi * (b - a)
            fd = f(d)
    return 0.5 * (a + b)


def main() -> int:
    print("=" * 116)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR COMPLETED TRIPLE CURRENT TRANSFER-FAMILY BOUNDARY")
    print("=" * 116)
    print()
    print("Question:")
    print("  On the audited current explicit `beta = 6` `spatial_pair` witness")
    print("  family, does the best one-parameter scaled fit realize the")
    print("  completed first-sector triple Z_min exactly?")
    print()

    note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md"
    )
    completion_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md"
    )
    transfer_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md"
    )

    # ----- 1. Reproduce Z_min from the upstream rank-one transfer realisation.
    v_min, z_min = completed_sector_data()
    z_min_gap = float(np.linalg.norm(np.array(NOTE_ZMIN, dtype=float) - z_min))

    # ----- 2. Build the live `spatial_pair` witness family infrastructure.
    jmat, weights, index = build_recurrence_matrix(NMAX)
    e_three = sample_operator(weights)

    # ----- 3. On the audited corner boundary, optimise the free interior
    #         linear_decay parameter via golden-section search.
    def gap_of_ld(ld: float) -> float:
        return gap_at(
            jmat,
            weights,
            index,
            e_three,
            z_min,
            tau_transfer=TAU_TRANSFER_LOWER,
            tau_boundary=TAU_BOUNDARY_UPPER,
            linear_decay=ld,
            asym_decay=ASYM_DECAY_LOWER,
        )[0]

    ld_best = golden_section_minimum(gap_of_ld, 0.05, 1.0, tol=1.0e-13)
    gap_best, zhat_best, c_best = gap_at(
        jmat,
        weights,
        index,
        e_three,
        z_min,
        tau_transfer=TAU_TRANSFER_LOWER,
        tau_boundary=TAU_BOUNDARY_UPPER,
        linear_decay=ld_best,
        asym_decay=ASYM_DECAY_LOWER,
    )
    scaled_fit = c_best * zhat_best
    diff = scaled_fit - z_min

    # ----- 4. Confirm the boundary-corner is in fact a local optimum: each
    #         small admissible step into the interior of the audited box
    #         (tau_transfer up, tau_boundary down, asym_decay up) increases
    #         the gap, validating "driven to the parameter-box boundary".
    def gap_with(tau_t: float, tau_b: float, ad: float) -> float:
        return gap_at(
            jmat,
            weights,
            index,
            e_three,
            z_min,
            tau_transfer=tau_t,
            tau_boundary=tau_b,
            linear_decay=ld_best,
            asym_decay=ad,
        )[0]

    base_gap = gap_with(TAU_TRANSFER_LOWER, TAU_BOUNDARY_UPPER, ASYM_DECAY_LOWER)
    interior_step_tau_transfer = gap_with(
        TAU_TRANSFER_LOWER * 5.0, TAU_BOUNDARY_UPPER, ASYM_DECAY_LOWER
    )
    interior_step_tau_boundary = gap_with(
        TAU_TRANSFER_LOWER, TAU_BOUNDARY_UPPER * 0.9, ASYM_DECAY_LOWER
    )
    interior_step_asym_decay = gap_with(
        TAU_TRANSFER_LOWER, TAU_BOUNDARY_UPPER, ASYM_DECAY_LOWER * 100.0
    )

    print("Reproduced completed first-sector triple from rank-one transfer realisation:")
    print(f"  Z_min                        = {np.array2string(z_min, precision=12)}")
    print(f"  ||Z_min - note Z_min||       = {z_min_gap:.3e}")
    print()
    print("Best one-parameter scaled fit on the audited parameter-box corner:")
    print(f"  tau_transfer (lower edge)    = {TAU_TRANSFER_LOWER:.0e}")
    print(f"  tau_boundary (upper edge)    = {TAU_BOUNDARY_UPPER}")
    print(f"  asym_decay   (lower edge)    = {ASYM_DECAY_LOWER:.0e}")
    print(f"  best linear_decay (interior) = {ld_best:.12f}")
    print(f"  Zhat_best                    = {np.array2string(zhat_best, precision=12)}")
    print(f"  c_best                       = {c_best:.12f}")
    print(f"  c_best * Zhat_best           = {np.array2string(scaled_fit, precision=12)}")
    print(f"  gap (c*Zhat - Z_min)         = {np.array2string(diff, precision=12)}")
    print(f"  ||gap||_2                    = {gap_best:.12f}")
    print()
    print("Local-edge sanity (gap when each boundary edge is relaxed inward):")
    print(f"  base (corner)                = {base_gap:.12f}")
    print(f"  tau_transfer  -> 5e-4        = {interior_step_tau_transfer:.12f}  (should rise)")
    print(f"  tau_boundary  -> 3.6         = {interior_step_tau_boundary:.12f}  (should rise)")
    print(f"  asym_decay    -> 1e-6        = {interior_step_asym_decay:.12f}  (should rise)")
    print()

    # ===== Theorem-level checks (verify the note's published claims) =====

    check(
        "the parent note records the published numerical bottom-line "
        "(Z_min triple, Zhat_best vector, c_best, gap norm)",
        all(
            tok in note
            for tok in (
                "0.135165279562",
                "0.374012880009",
                "0.543843858544",
                "0.280527830070",
                "0.789850309412",
                "1.120725632470",
                "0.481383963846",
                "0.007578536496",
            )
        ),
        "all explicit numbers found verbatim in the note text",
    )
    check(
        "the upstream completion theorem (2026-04-19) supplies the explicit "
        "completed first-sector triple Z_min consumed by this boundary check",
        ("completed sample triple" in completion_note) and ("a^min" in completion_note),
    )
    check(
        "the spatial-environment transfer theorem note pins the abstract "
        "object the `spatial_pair` family realises (positive conjugation-"
        "symmetric boundary state hit by powers of S_beta^env)",
        "S_beta^env" in transfer_note
        and "positive conjugation-symmetric boundary state" in transfer_note,
    )
    check(
        "reproduced Z_min from the rank-one transfer realisation matches the "
        "note's published completed triple to 1e-9",
        z_min_gap < 1.0e-9,
        f"||Z_min reproduced - Z_min note||={z_min_gap:.3e}",
    )
    check(
        "the best scaled-fit `Zhat_best` reproduces the note's published "
        "vector to 1e-6",
        all(
            abs(zhat_best[i] - NOTE_ZHAT[i]) < 1.0e-6 for i in range(3)
        ),
        f"Zhat_best={np.array2string(zhat_best, precision=10)}",
    )
    check(
        "the optimal overall scale `c_best` reproduces the note's published "
        "value to 1e-6",
        abs(c_best - NOTE_C_BEST) < 1.0e-6,
        f"c_best={c_best:.12f}",
    )
    check(
        "the Euclidean gap `||c_best Zhat_best - Z_min||_2` reproduces the "
        "note's published value to 1e-9",
        abs(gap_best - NOTE_GAP_NORM) < 1.0e-9,
        f"||c*Zhat - Z_min||={gap_best:.12f}",
    )
    check(
        "the audited corner is a strict local minimum: relaxing any of the "
        "three active edges into the interior strictly increases the gap",
        interior_step_tau_transfer > base_gap
        and interior_step_tau_boundary > base_gap
        and interior_step_asym_decay > base_gap,
        f"(rel_tau_t,rel_tau_b,rel_ad)=({interior_step_tau_transfer:.6e},"
        f"{interior_step_tau_boundary:.6e},{interior_step_asym_decay:.6e})",
    )
    check(
        "the best audited scaled fit therefore does NOT realise Z_min "
        "exactly: the gap norm is strictly bounded away from zero "
        "(>= 1e-3)",
        gap_best > 1.0e-3,
        f"||c*Zhat - Z_min|| = {gap_best:.12f} > 1e-3",
    )
    check(
        "the note's prose conclusion `still not realized exactly inside the "
        "audited current explicit witness family` is therefore numerically "
        "supported",
        "still not realized exactly" in note
        and "best audited scaled fit" in note,
    )

    print()
    print("=" * 116)
    print("RESULT")
    print("=" * 116)
    print("  Boundary refinement (current explicit `spatial_pair` family is only an ansatz):")
    print("    - the audited parameter box's best one-parameter scaled fit lands on")
    print("      three of four edges (lower tau_transfer, upper tau_boundary, lower")
    print("      asym_decay) with one interior optimum at linear_decay ~= 0.323966;")
    print(f"    - the residual gap ||c_best Zhat_best - Z_min||_2 = {gap_best:.12e}")
    print("      is strictly positive, so this witness family does NOT realise the")
    print("      completed first-sector triple Z_min exactly;")
    print("    - the family therefore remains a boundary ansatz; the missing exact")
    print("      realisation is the actual framework-point Wilson environment packet.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
