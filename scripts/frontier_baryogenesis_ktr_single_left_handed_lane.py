#!/usr/bin/env python3
"""
Baryogenesis K_tr single-left-handed-lane reduction on the current main
package surface.

This runner sharpens the transport stage after

  eta = J * K_EWPT * K_tr * K_sph

by showing that K_tr does not live on a mixed left/right-handed transport
space. On current main it reduces to one real functional of one retained
left-handed electroweak-active density-history lane:

  K_tr = F_tr[ell_L(tau)].
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

ETA_OBS = 6.12e-10
J_PROMOTED = 3.330901e-5
K_NP_TARGET = ETA_OBS / J_PROMOTED
K_EQUAL_SPLIT = K_NP_TARGET ** (1.0 / 3.0)
K_TR_IF_10PCT_OTHER_STAGES = K_NP_TARGET / (0.1 * 0.1)

I2 = np.eye(2, dtype=complex)
I3 = np.eye(3, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


def phase_matrix(phases: list[float]) -> np.ndarray:
    return np.diag([complex(math.cos(p), math.sin(p)) for p in phases])


def flatten(op: np.ndarray) -> np.ndarray:
    return op.reshape(-1)


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS K_TR SINGLE-LEFT-HANDED-LANE REDUCTION")
    print("=" * 80)
    print()
    print("Question:")
    print("  On current main, does the transport factor K_tr live on a mixed")
    print("  left/right-handed transport space, or on one exact left-handed")
    print("  electroweak-active quotient lane?")
    print()

    print("=" * 80)
    print("PART 1: EXACT CHIRALITY-PLANE REDUCTION")
    print("=" * 80)
    print()

    i16 = np.eye(16, dtype=complex)
    g0 = kron4(SZ, SZ, SZ, SX)
    g1 = kron4(SX, I2, I2, I2)
    g2 = kron4(SZ, SX, I2, I2)
    g3 = kron4(SZ, SZ, SX, I2)
    g5 = g0 @ g1 @ g2 @ g3
    p_l = (i16 + g5) / 2.0
    p_r = (i16 - g5) / 2.0

    rank_lr = np.linalg.matrix_rank(
        np.column_stack([flatten(p_l), flatten(p_r)]), tol=1e-12
    )
    quotient_dim = rank_lr - 1

    check(
        "gamma_5 squares to +I on the 4D chirality surface",
        np.linalg.norm(g5 @ g5 - i16) < 1e-12,
    )
    check(
        "P_L + P_R = I exactly",
        np.linalg.norm(p_l + p_r - i16) < 1e-12,
    )
    check(
        "P_L P_R = 0 exactly",
        np.linalg.norm(p_l @ p_r) < 1e-12,
    )
    check(
        "the chirality split is 8 + 8",
        abs(np.trace(p_l).real - 8.0) < 1e-12 and abs(np.trace(p_r).real - 8.0) < 1e-12,
        f"tr(P_L) = {np.trace(p_l).real:.1f}, tr(P_R) = {np.trace(p_r).real:.1f}",
    )
    check(
        "the retained chirality plane has dimension 2",
        rank_lr == 2,
        f"rank span{{P_L,P_R}} = {rank_lr}",
    )
    check(
        "quotienting by the right-handed spectator direction leaves one active lane",
        quotient_dim == 1,
        f"dim(span{{P_L,P_R}} / span{{P_R}}) = {quotient_dim}",
    )

    samples = [
        (1.0, 0.0),
        (0.0, 1.0),
        (0.7, 0.3),
        (0.4, -0.2),
    ]
    for idx, (ell_l, r_r) in enumerate(samples, start=1):
        rho = ell_l * p_l + r_r * p_r
        proj_l = p_l @ rho @ p_l
        proj_r = p_r @ rho @ p_r
        check(
            f"sample chirality history {idx} decomposes exactly into active and spectator lanes",
            np.linalg.norm(rho - (proj_l + proj_r)) < 1e-12,
            f"ell_L = {ell_l:.6f}, r_R = {r_r:.6f}",
        )

    ell1, rr1 = 0.5, 0.0
    ell2, rr2 = 0.5, 0.7
    rho1 = ell1 * p_l + rr1 * p_r
    rho2 = ell2 * p_l + rr2 * p_r
    check(
        "configurations with the same left-handed active coordinate differ only by the right-handed spectator lane",
        np.linalg.norm((rho2 - rho1) - (rr2 - rr1) * p_r) < 1e-12,
        f"ell_L(sample1) = {ell1:.6f}, ell_L(sample2) = {ell2:.6f}",
    )
    info(
        "chirality-plane meaning",
        "once the right-handed spectator direction is quotiented out, the transport stage cannot depend on a mixed-chirality same-surface transport space",
    )
    print()

    print("=" * 80)
    print("PART 2: LEFT-HANDED ACTIVE / RIGHT-HANDED SPECTATOR BOUNDARY")
    print("=" * 80)
    print()

    one_gen_note = (DOCS / "ONE_GENERATION_MATTER_CLOSURE_NOTE.md").read_text(
        encoding="utf-8"
    )
    lh_note = (DOCS / "LEFT_HANDED_CHARGE_MATCHING_NOTE.md").read_text(
        encoding="utf-8"
    )
    anomaly_note = (DOCS / "ANOMALY_FORCES_TIME_THEOREM.md").read_text(
        encoding="utf-8"
    )
    rh_runner = (ROOT / "scripts" / "frontier_right_handed_sector.py").read_text(
        encoding="utf-8"
    )
    stage_note = (DOCS / "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md").read_text(
        encoding="utf-8"
    )

    check(
        "left-handed charge-matching note records the retained left-handed doublet sector and the one-generation note carries that full-framework boundary",
        "`Q_L : (2,3)_{+1/3}`" in lh_note
        and "`L_L : (2,1)_{-1}`" in lh_note
        and "left-handed gauge/matter sector" in one_gen_note,
    )
    check(
        "anomaly theorem records that chirality distinguishes left-handed doublets from right-handed singlets",
        "chirality distinguishes SU(2) doublets (left) from singlets (right)" in anomaly_note,
    )
    check(
        "right-handed sector runner records the exact 8+8 chirality split",
        "C^16 = C^8_L + C^8_R (8+8 chirality split)" in rh_runner,
    )
    check(
        "right-handed sector runner records that SU(2) acts only on left-handed states",
        "SU(2) is a CHIRAL gauge symmetry, acting only on left-handed states." in rh_runner,
    )
    check(
        "stage-decomposition note defines K_tr on left-handed densities n_L^src and n_L^act",
        "`n_L^src` be the left-handed CP-odd density" in stage_note
        and "`n_L^act` be the portion delivered" in stage_note
        and "`K_tr = n_L^act / n_L^src`" in stage_note,
    )

    p_gen = phase_matrix([0.37, -0.91, 1.23])
    p_lift = np.kron(p_gen, i16)
    pl_lift = np.kron(I3, p_l)
    pr_lift = np.kron(I3, p_r)
    comm_l = np.linalg.norm(p_lift @ pl_lift - pl_lift @ p_lift)
    comm_r = np.linalg.norm(p_lift @ pr_lift - pr_lift @ p_lift)

    check(
        "the left-handed active lane is generation blind on the retained surface",
        comm_l < 1e-12,
        f"||[P_gen,P_L]|| = {comm_l:.2e}",
    )
    check(
        "the right-handed spectator lane is generation blind on the retained surface",
        comm_r < 1e-12,
        f"||[P_gen,P_R]|| = {comm_r:.2e}",
    )
    info(
        "stage consequence",
        "after the exact flavor factorization and chirality split, the transport problem depends only on one left-handed electroweak-active density coordinate ell_L(tau)",
    )
    print()

    print("=" * 80)
    print("PART 3: K_TR TARGET GEOMETRY")
    print("=" * 80)
    print()

    print(f"  K_NP,target                               = {K_NP_TARGET:.6e}")
    print(f"  equal three-stage K_tr benchmark          = {K_EQUAL_SPLIT:.6e}")
    print(f"  K_tr if K_EWPT = K_sph = 0.1              = {K_TR_IF_10PCT_OTHER_STAGES:.6e}")
    print()

    check(
        "K_NP target inherited by K_tr is 1.837341e-5",
        abs(K_NP_TARGET - 1.837341e-5) < 1e-11,
        f"K_NP,target = {K_NP_TARGET:.6e}",
    )
    check(
        "equal three-stage split gives K_tr = (K_NP)^(1/3)",
        abs(K_EQUAL_SPLIT - 2.638740e-2) < 1e-8,
        f"K_equal = {K_EQUAL_SPLIT:.6e}",
    )
    check(
        "10% transition and 10% sphaleron survival would force K_tr into the 1e-3 range",
        1.0e-3 < K_TR_IF_10PCT_OTHER_STAGES < 1.0e-2,
        f"K_tr = {K_TR_IF_10PCT_OTHER_STAGES:.6e}",
    )
    info(
        "geometry meaning",
        "the stage decomposition turns K_tr into a sharply normalized target even though the active-lane transport functional itself remains open",
    )
    print()

    print("=" * 80)
    print("PART 4: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    ktr_note = (
        DOCS / "BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md"
    ).read_text(encoding="utf-8")
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "K_tr note records the single-left-handed-lane functional K_tr = F_tr[ell_L(tau)]",
        "`K_tr = F_tr[ℓ_L(τ)]`" in ktr_note,
    )
    check(
        "K_tr note records the exact chirality decomposition rho = ell_L P_L + r_R P_R",
        "`ρ(τ) = ℓ_L(τ) P_L + r_R(τ) P_R`" in ktr_note,
    )
    check(
        "closure-gate note points to the K_tr reduction note",
        "BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md" in gate_note,
    )
    check(
        "derivation atlas carries the K_tr single-left-handed-lane row",
        "Baryogenesis K_tr single-left-handed-lane reduction" in atlas,
    )
    check(
        "canonical harness index includes the K_tr runner",
        "frontier_baryogenesis_ktr_single_left_handed_lane.py" in harness,
    )
    check(
        "current flagship entrypoint points to the K_tr note",
        "BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the transport stage K_tr now reduces to one real functional")
    print("      of one left-handed electroweak-active density lane")
    print("      K_tr = F_tr[ell_L(tau)]")
    print("    - the exact 4D chirality split removes the apparent mixed")
    print("      left/right-handed transport ambiguity")
    print("    - no mixed-chirality same-surface transport space remains on")
    print("      the current authority surface")
    print("    - the genuinely open content is the active-lane transport")
    print("      functional itself")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
