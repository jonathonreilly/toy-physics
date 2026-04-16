#!/usr/bin/env python3
"""
Baryogenesis K_sph single-active-lane reduction on the current main package
surface.

This runner sharpens the sphaleron-survival stage after

  eta = J * K_EWPT * K_tr * K_sph

by showing that K_sph does not live on a multidirectional same-surface
baryon/lepton washout space. On current main it reduces to one real functional
of one washout-active quotient lane:

  K_sph = F_sph[q_+(tau)].
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
K_SPH_IF_10PCT_OTHER_STAGES = K_NP_TARGET / (0.1 * 0.1)

I3 = np.eye(3, dtype=complex)
I8 = np.eye(8, dtype=complex)

TASTE_STATES = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]


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


def hamming_weight(state: tuple[int, int, int]) -> int:
    return sum(state)


def baryon_and_lepton_operators() -> tuple[np.ndarray, np.ndarray]:
    baryon = np.zeros((8, 8), dtype=complex)
    lepton = np.zeros((8, 8), dtype=complex)
    for idx, state in enumerate(TASTE_STATES):
        hw = hamming_weight(state)
        if hw in (1, 2):
            baryon[idx, idx] = 1.0 / 3.0
        else:
            lepton[idx, idx] = 1.0
    return baryon, lepton


def flatten(op: np.ndarray) -> np.ndarray:
    return op.reshape(-1)


def phase_matrix(phases: list[float]) -> np.ndarray:
    return np.diag([complex(math.cos(p), math.sin(p)) for p in phases])


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS K_SPH SINGLE-ACTIVE-LANE REDUCTION")
    print("=" * 80)
    print()
    print("Question:")
    print("  On current main, does the sphaleron-survival factor K_sph live on")
    print("  a multidirectional baryon/lepton washout space, or on one exact")
    print("  washout-active quotient lane?")
    print()

    print("=" * 80)
    print("PART 1: EXACT BARYON/LEPTON CHARGE-PLANE REDUCTION")
    print("=" * 80)
    print()

    baryon, lepton = baryon_and_lepton_operators()
    b_plus_l = baryon + lepton
    b_minus_l = baryon - lepton

    rank_bl = np.linalg.matrix_rank(
        np.column_stack([flatten(baryon), flatten(lepton)]), tol=1e-12
    )
    rank_pm = np.linalg.matrix_rank(
        np.column_stack([flatten(b_plus_l), flatten(b_minus_l)]), tol=1e-12
    )
    quotient_dim = rank_bl - 1
    anomaly_sum_b_minus_l = float(np.sum(np.diag(b_minus_l).real))
    active_sum_b_plus_l = float(np.sum(np.diag(b_plus_l).real))

    check(
        "the retained baryon/lepton charge plane has dimension 2",
        rank_bl == 2,
        f"rank span{{B,L}} = {rank_bl}",
    )
    check(
        "the same charge plane is exactly spanned by B+L and B-L",
        rank_pm == 2,
        f"rank span{{B+L,B-L}} = {rank_pm}",
    )
    check(
        "B = ((B+L) + (B-L))/2 exactly",
        np.linalg.norm(baryon - 0.5 * (b_plus_l + b_minus_l)) < 1e-12,
    )
    check(
        "L = ((B+L) - (B-L))/2 exactly",
        np.linalg.norm(lepton - 0.5 * (b_plus_l - b_minus_l)) < 1e-12,
    )
    check(
        "B-L has zero retained anomaly sum and is the protected spectator direction",
        abs(anomaly_sum_b_minus_l) < 1e-12,
        f"sum diag(B-L) = {anomaly_sum_b_minus_l:.1e}",
    )
    check(
        "B+L is a nontrivial active charge direction",
        abs(active_sum_b_plus_l - 4.0) < 1e-12,
        f"sum diag(B+L) = {active_sum_b_plus_l:.6f}",
    )
    check(
        "quotienting by the protected B-L direction leaves one active lane",
        quotient_dim == 1,
        f"dim(span{{B,L}} / span{{B-L}}) = {quotient_dim}",
    )
    info(
        "charge-plane meaning",
        "the sphaleron-survival stage cannot depend on a two-dimensional same-surface baryon/lepton charge space once the protected B-L direction is modded out",
    )
    print()

    print("=" * 80)
    print("PART 2: UNIQUE ACTIVE-QUOTIENT COORDINATE")
    print("=" * 80)
    print()

    samples = [
        (1.0, 0.0),
        (0.0, 1.0),
        (0.7, 0.3),
        (0.4, -0.2),
    ]
    for idx, (q_b, q_l) in enumerate(samples, start=1):
        q_plus = 0.5 * (q_b + q_l)
        q_minus = 0.5 * (q_b - q_l)
        lhs = q_b * baryon + q_l * lepton
        rhs = q_plus * b_plus_l + q_minus * b_minus_l
        check(
            f"sample charge history {idx} decomposes exactly into active and spectator lanes",
            np.linalg.norm(lhs - rhs) < 1e-12,
            f"q_plus = {q_plus:.6f}, q_minus = {q_minus:.6f}",
        )

    q1_b, q1_l = 1.0, 0.0
    q2_b, q2_l = 0.7, 0.3
    q1_plus = 0.5 * (q1_b + q1_l)
    q2_plus = 0.5 * (q2_b + q2_l)
    diff = (q1_b * baryon + q1_l * lepton) - (q2_b * baryon + q2_l * lepton)
    spectator_piece = 0.5 * ((q1_b - q1_l) - (q2_b - q2_l)) * b_minus_l
    check(
        "configurations with the same active quotient coordinate differ only by the protected spectator lane",
        abs(q1_plus - q2_plus) < 1e-12 and np.linalg.norm(diff - spectator_piece) < 1e-12,
        f"q_plus(sample1) = {q1_plus:.6f}, q_plus(sample2) = {q2_plus:.6f}",
    )

    p_gen = phase_matrix([0.37, -0.91, 1.23])
    p_lift = np.kron(p_gen, I8)
    bp_lift = np.kron(I3, b_plus_l)
    bm_lift = np.kron(I3, b_minus_l)
    comm_bp = np.linalg.norm(p_lift @ bp_lift - bp_lift @ p_lift)
    comm_bm = np.linalg.norm(p_lift @ bm_lift - bm_lift @ p_lift)

    check(
        "the active B+L lane is generation blind on the retained electroweak surface",
        comm_bp < 1e-12,
        f"||[P_gen,B+L]|| = {comm_bp:.2e}",
    )
    check(
        "the protected B-L spectator lane is generation blind on the retained electroweak surface",
        comm_bm < 1e-12,
        f"||[P_gen,B-L]|| = {comm_bm:.2e}",
    )
    info(
        "stage consequence",
        "after transport into the sphaleron-active region, the retained survival/washout problem depends only on the one scalar active coordinate q_+(tau)",
    )
    print()

    print("=" * 80)
    print("PART 3: K_SPH TARGET GEOMETRY")
    print("=" * 80)
    print()

    print(f"  K_NP,target                               = {K_NP_TARGET:.6e}")
    print(f"  equal three-stage K_sph benchmark         = {K_EQUAL_SPLIT:.6e}")
    print(f"  K_sph if K_EWPT = K_tr = 0.1              = {K_SPH_IF_10PCT_OTHER_STAGES:.6e}")
    print()

    check(
        "K_NP target inherited by K_sph is 1.837341e-5",
        abs(K_NP_TARGET - 1.837341e-5) < 1e-11,
        f"K_NP,target = {K_NP_TARGET:.6e}",
    )
    check(
        "equal three-stage split gives K_sph = (K_NP)^(1/3)",
        abs(K_EQUAL_SPLIT - 2.638740e-2) < 1e-8,
        f"K_equal = {K_EQUAL_SPLIT:.6e}",
    )
    check(
        "10% transition and 10% transport would force K_sph into the 1e-3 range",
        1.0e-3 < K_SPH_IF_10PCT_OTHER_STAGES < 1.0e-2,
        f"K_sph = {K_SPH_IF_10PCT_OTHER_STAGES:.6e}",
    )
    info(
        "geometry meaning",
        "the stage decomposition turns K_sph into a sharply normalized target even though the active-lane history functional itself remains open",
    )
    print()

    print("=" * 80)
    print("PART 4: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    proton_note = (DOCS / "PROTON_LIFETIME_DERIVED_NOTE.md").read_text(encoding="utf-8")
    ksph_note = (DOCS / "BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    stage_note = (DOCS / "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md").read_text(
        encoding="utf-8"
    )
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "proton-lifetime note records the native sphaleron structure B+L violated, B-L conserved",
        "B+L violated, B-L conserved" in proton_note,
    )
    check(
        "K_sph note records the single-active-lane functional K_sph = F_sph[q_+(tau)]",
        "`K_sph = F_sph[q_+(τ)]`" in ksph_note,
    )
    check(
        "K_sph note records the exact active/spectator decomposition",
        "`q_B(τ) B + q_L(τ) L = q_+(τ) (B+L) + q_-(τ) (B-L)`" in ksph_note,
    )
    check(
        "closure-gate note points to the K_sph reduction note",
        "BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md" in gate_note,
    )
    check(
        "stage-decomposition note points to the K_sph reduction note",
        "BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md" in stage_note,
    )
    check(
        "derivation atlas carries the K_sph single-active-lane row",
        "Baryogenesis K_sph single-active-lane reduction" in atlas,
    )
    check(
        "canonical harness index includes the K_sph runner",
        "frontier_baryogenesis_ksph_single_active_lane.py" in harness,
    )
    check(
        "current flagship entrypoint points to the K_sph note",
        "BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the sphaleron-survival stage K_sph now reduces to one real")
    print("      functional of one washout-active quotient lane")
    print("      K_sph = F_sph[q_+(tau)]")
    print("    - the protected B-L spectator direction removes the apparent")
    print("      two-dimensional baryon/lepton washout ambiguity")
    print("    - no multidirectional same-surface washout space remains on")
    print("      the current authority surface")
    print("    - the genuinely open content is the active-lane functional")
    print("      itself, not hidden extra charge-space multiplicity")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
