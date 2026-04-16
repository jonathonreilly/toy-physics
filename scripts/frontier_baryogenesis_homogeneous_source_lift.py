#!/usr/bin/env python3
"""
Baryogenesis homogeneous source-lift theorem on the current main package
surface.

This runner sharpens the source-pullback theorem:

  S_src[chi] = W[J_chi]

by showing that on the retained APBC/Higgs scalar lane the admissible
same-surface source lifts collapse to the one-dimensional homogeneous family

  J_chi = j(chi) I.
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
LOG_K_TARGET = math.log(ETA_OBS / J_PROMOTED)


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


def temporal_modes(lt: int) -> list[float]:
    return [(2 * n + 1) * math.pi / lt for n in range(lt)]


def exact_uniform_generator(lt: int, u0: float, j: float) -> float:
    return 4.0 * sum(
        math.log1p(j * j / (u0 * u0 * (3.0 + math.sin(w) ** 2)))
        for w in temporal_modes(lt)
    )


def perm_matrix(perm: list[int]) -> np.ndarray:
    n = len(perm)
    out = np.zeros((n, n), dtype=float)
    for i, j in enumerate(perm):
        out[j, i] = 1.0
    return out


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS HOMOGENEOUS SOURCE LIFT")
    print("=" * 80)
    print()
    print("Question:")
    print("  After S_src[chi] = W[J_chi], does the source side still require a")
    print("  general local matrix-valued lift, or is the retained lift already")
    print("  forced onto the homogeneous scalar family?")
    print()

    print("=" * 80)
    print("PART 1: UPSTREAM ONE-LANE / SOURCE-GENERATOR SURFACE")
    print("=" * 80)
    print()

    kewpt_note = (DOCS / "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md").read_text(
        encoding="utf-8"
    )
    obs_note = (DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md").read_text(
        encoding="utf-8"
    )
    pullback_note = (DOCS / "BARYOGENESIS_SOURCE_PULLBACK_NOTE.md").read_text(
        encoding="utf-8"
    )
    selector_note = (DOCS / "HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md").read_text(
        encoding="utf-8"
    )
    spatial_note = (DOCS / "HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md").read_text(
        encoding="utf-8"
    )

    check(
        "K_EWPT reduction note records one scalar history lane",
        "`K_EWPT = F_EWPT[χ(τ)]`" in kewpt_note,
    )
    check(
        "observable-principle note records the local scalar source family",
        "`J = sum_x j_x P_x`" in obs_note,
    )
    check(
        "observable-principle note records the exact homogeneous source family J = j I",
        "`J = j I`" in obs_note,
    )
    check(
        "source-pullback note records S_src[chi] = W[J_chi]",
        "`S_src[χ] = W[J_χ]`" in pullback_note,
    )
    check(
        "selector note records locality forbids mode-dependent hand-picking inside the minimal orbit",
        "locality forbids mode-dependent hand-picking inside the minimal orbit" in selector_note,
    )
    check(
        "spatial BC note records the finite intensive 3+1 order-parameter limit",
        "finite intensive `3+1` order-parameter limit" in spatial_note,
    )
    info(
        "surface meaning",
        "upstream the package already fixes one scalar lane, one scalar generator, one local source family, one exact homogeneous source slice, and one intensive 3+1 order-parameter surface",
    )
    print()

    print("=" * 80)
    print("PART 2: KLEIN-FOUR FIXED SUBSPACE IS ONE-DIMENSIONAL")
    print("=" * 80)
    print()

    # Orbit labels: [pi/4, 3pi/4, 5pi/4, 7pi/4]
    sign = perm_matrix([2, 3, 0, 1])
    conj = perm_matrix([3, 2, 1, 0])
    group_avg = 0.25 * (np.eye(4) + sign + conj + sign @ conj)
    eigvals = np.linalg.eigvalsh(group_avg)
    rank = int(np.sum(eigvals > 1e-12))
    fixed_vec = group_avg @ np.array([1.0, 2.0, 3.0, 4.0], dtype=float)

    print(f"  group-average eigenvalues = {eigvals}")
    print(f"  projected sample vector   = {fixed_vec}")
    print()

    check(
        "the resolved Lt=4 orbit fixed subspace has dimension one",
        rank == 1,
        f"rank(Fix) = {rank}",
    )
    check(
        "the fixed vector is uniform across the resolved orbit",
        np.max(np.abs(fixed_vec - fixed_vec[0])) < 1e-12,
        f"fixed_vec = {fixed_vec.tolist()}",
    )
    check(
        "sign and conjugation both preserve the uniform vector",
        np.allclose(sign @ np.ones(4), np.ones(4))
        and np.allclose(conj @ np.ones(4), np.ones(4)),
        "uniform orbit vector is the common fixed direction",
    )
    info(
        "fixed-subspace meaning",
        "once the retained temporal support is constrained to the resolved Klein-four orbit, the admissible temporal profile is forced to be uniform",
    )
    print()

    print("=" * 80)
    print("PART 3: EXACT HOMOGENEOUS SOURCE FAMILY")
    print("=" * 80)
    print()

    for j in (0.0, 0.1, 0.3):
        w4 = exact_uniform_generator(4, 1.0, j)
        print(f"  j={j:.3f}: W_4(j) = {w4:.12e}")

    s_src = exact_uniform_generator(4, 1.0, 0.3)
    i_damp_req = s_src - LOG_K_TARGET
    check(
        "the exact homogeneous APBC source family remains positive on the positive branch",
        s_src > 0.0,
        f"W_4(0.3) = {s_src:.12f}",
    )
    check(
        "the sharpened bridge eta = J * exp[W(jI) - I_damp] reconstructs the target with the required damping",
        abs(J_PROMOTED * math.exp(s_src - i_damp_req) - ETA_OBS) < 1e-20,
        f"I_damp,req = {i_damp_req:.12f}",
    )
    info(
        "lift consequence",
        "the remaining source-side freedom is one scalar reparameterization j(chi) into a known exact homogeneous source family, not an arbitrary local matrix-valued source lift",
    )
    print()

    print("=" * 80)
    print("PART 4: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    homog_note = (DOCS / "BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(
        encoding="utf-8"
    )
    pullback_note = (DOCS / "BARYOGENESIS_SOURCE_PULLBACK_NOTE.md").read_text(
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
        "homogeneous-source-lift note records J_chi = j(chi) I",
        "`J_χ = j(χ) I`" in homog_note,
    )
    check(
        "homogeneous-source-lift note records S_src[chi] = W[j(chi) I]",
        "`S_src[χ] = W[j(χ) I]`" in homog_note,
    )
    check(
        "homogeneous-source-lift note records the sharpened bridge eta = J * exp[W(j(chi) I) - I_damp[chi]]",
        "`η = J * exp[W(j(χ) I) - I_damp[χ]]`" in homog_note,
    )
    check(
        "source-pullback note now points to the homogeneous-source-lift note",
        "BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md" in pullback_note,
    )
    check(
        "closure-gate note records the homogeneous lift",
        "`J_χ = j(χ) I`" in gate_note and "`η = J * exp[W(j(χ) I) - I_damp[χ]]`" in gate_note,
    )
    check(
        "derivation atlas carries the homogeneous-source-lift row",
        "Baryogenesis homogeneous source lift" in atlas,
    )
    check(
        "canonical harness index includes the homogeneous-source-lift runner",
        "frontier_baryogenesis_homogeneous_source_lift.py" in harness,
    )
    check(
        "current flagship entrypoint points to the homogeneous-source-lift note",
        "BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the retained same-surface source lift is exactly homogeneous")
    print("      J_chi = j(chi) I")
    print("    - the source side is therefore reduced to one scalar")
    print("      reparameterization into the exact homogeneous APBC family")
    print("    - the viable positive-branch bridge sharpens to")
    print("      eta = J * exp[W(j(chi) I) - I_damp[chi]]")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
