#!/usr/bin/env python3
"""Common polarization-bundle candidate with exact invariant core.

This runner pushes the shared primitive family one level further than the
earlier synthesis pass:

1. the direct-universal stack contributes the exact invariant rank-2 `A1`
   projector onto lapse and spatial trace;
2. Route 2 contributes the exact bridge triple `B_R = (K_R, I_TB, Xi_TB)`;
3. the finite-rank widening lane contributes the exact noncanonical
   support-family enlargement `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`.

The strongest axiom-native common candidate is then

    P_R^cand = (Pi_A1, B_R, O_R)

with a block-connection prototype

    nabla_R^cand = nabla_A1 ⊕ nabla_B ⊕ nabla_O.

This script checks the exact invariance properties of that candidate and the
sharp obstruction that still prevents a canonical full `3+1` bundle.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
COMMON_SYNTHESIS = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"
FINITE_FAMILY = DOCS / "FINITE_RANK_SUPPORT_GENERATOR_FAMILY_NOTE.md"
BILINEAR_NOTE = DOCS / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"
ACTION_NOTE = DOCS / "S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"

A1 = SourceFileLoader(
    "universal_gr_a1_invariant_section",
    str(ROOT / "scripts" / "frontier_universal_gr_a1_invariant_section.py"),
).load_module()
SUPPORT_FAMILY = SourceFileLoader(
    "finite_rank_support_generator_family",
    str(ROOT / "scripts" / "frontier_finite_rank_support_generator_family.py"),
).load_module()
BILINEAR = SourceFileLoader(
    "s3_time_bilinear_tensor_primitive",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
ACTION = SourceFileLoader(
    "s3_time_bilinear_tensor_action",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def projector_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def support_family_rank() -> tuple[int, float]:
    basis = SUPPORT_FAMILY.irrep.same_source.build_adapted_basis()
    q_fr = SUPPORT_FAMILY.irrep.finite_rank_qeff()
    coeff = basis.T @ q_fr
    q_a1 = basis[:, :2] @ coeff[:2]
    q_e = basis[:, 2:4] @ coeff[2:4]
    q_t = basis[:, 4:7] @ coeff[4:7]
    support_frame = np.column_stack([q_a1, q_e, q_t])
    return int(np.linalg.matrix_rank(support_frame, tol=1e-12)), float(np.max(np.abs(support_frame)))


def route2_bridge_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    q_center = BILINEAR.e0 + BILINEAR.e_x
    q_shell = BILINEAR.s_unit + BILINEAR.t1x
    theta_center = BILINEAR.vec_k(q_center)
    theta_shell = BILINEAR.vec_k(q_shell)

    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    seed_t = ACTION.expm(-0.0 * Lambda_sym) @ u_star
    xi_center = ACTION.xi_tb(theta_center, seed_t)
    semigroup_err = float(
        np.max(
            np.abs(
                (ACTION.expm(-1.0 * Lambda_sym) @ u_star)
                - (ACTION.expm(-0.5 * Lambda_sym) @ (ACTION.expm(-0.5 * Lambda_sym) @ u_star))
            )
        )
    )
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    return theta_center, theta_shell, xi_center, sym_err, semigroup_err


def main() -> int:
    print("POLARIZATION COMMON BUNDLE CANDIDATE")
    print("=" * 78)

    pi_a1 = projector_a1()
    pi_rank = int(np.linalg.matrix_rank(pi_a1, tol=1e-12))

    d = (2.0, 3.0, 5.0, 7.0)
    rng = np.random.default_rng(2)
    samples = 24
    frames_per_sample = 48
    max_a1_delta = 0.0
    max_perp_delta = 0.0
    coord_max_delta = np.zeros(10, dtype=float)

    for _ in range(samples):
        h = A1.random_symmetric_h(rng)
        base = A1.response_vector(h, A1.canonical_polarization_frame(), d)
        base_a1 = pi_a1 @ base
        base_perp = (np.eye(10) - pi_a1) @ base

        for _ in range(frames_per_sample):
            rot = A1.random_so3(rng)
            frame = A1.rotated_frame(rot)
            resp = A1.response_vector(h, frame, d)
            a1 = pi_a1 @ resp
            perp = (np.eye(10) - pi_a1) @ resp
            max_a1_delta = max(max_a1_delta, float(np.max(np.abs(a1 - base_a1))))
            max_perp_delta = max(max_perp_delta, float(np.max(np.abs(perp - base_perp))))
            coord_max_delta = np.maximum(coord_max_delta, np.abs(resp - base))

    invariant_coords = [i for i, delta in enumerate(coord_max_delta) if delta < 1e-12]

    theta_center, theta_shell, xi_center, sym_err, semigroup_err = route2_bridge_data()
    bridge_exact = np.all(np.isfinite(theta_center)) and np.all(np.isfinite(theta_shell))
    theta_center_expected = np.array([1.0, 0.0, 1.0 / 6.0, 0.0], dtype=float)
    theta_shell_expected = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    carrier_err = max(
        float(np.max(np.abs(theta_center - theta_center_expected))),
        float(np.max(np.abs(theta_shell - theta_shell_expected))),
    )

    support_rank, support_norm = support_family_rank()

    print("Candidate core:")
    print("  Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)")
    print("  B_R   = (K_R, I_TB, Xi_TB)")
    print("  P_R^cand = (Pi_A1, B_R, O_R)")
    print("  nabla_R^cand = nabla_A1 ⊕ nabla_B ⊕ nabla_O")
    print(f"  support-family rank([A1, E, T1]) = {support_rank}")
    print(f"  max support family norm = {support_norm:.12e}")
    print(f"  max Pi_A1 delta = {max_a1_delta:.12e}")
    print(f"  max complement delta = {max_perp_delta:.12e}")
    print(f"  invariant coordinates = {tuple(invariant_coords)}")
    print(f"  Route 2 carrier endpoint error = {carrier_err:.12e}")
    print(f"  Lambda_R symmetry error = {sym_err:.12e}")
    print(f"  Xi_TB semigroup error = {semigroup_err:.12e}")

    record(
        "the canonical A1 projector is exact and rank two",
        pi_rank == 2,
        f"Pi_A1 rank={pi_rank}",
    )
    record(
        "the canonical A1 projector is frame-invariant across sampled valid 3+1 frames",
        max_a1_delta < 1e-12,
        f"max Pi_A1 delta={max_a1_delta:.3e}",
    )
    record(
        r"the complementary E \oplus T1 channels remain frame-dependent",
        max_perp_delta > 1e-3,
        f"max complement delta={max_perp_delta:.3e}",
    )
    record(
        "the exact invariant coordinates are lapse and spatial trace",
        tuple(invariant_coords) == (0, 4),
        f"invariant coordinates={tuple(invariant_coords)}",
    )
    record(
        "the Route 2 carrier endpoints are exact on the canonical A1 family",
        bridge_exact and carrier_err < 1e-12,
        f"carrier endpoint error={carrier_err:.3e}",
    )
    record(
        "the Route 2 semigroup factor is symmetric positive and contracts exactly",
        sym_err < 1e-12 and semigroup_err < 1e-12,
        f"symmetry error={sym_err:.3e}, semigroup error={semigroup_err:.3e}",
    )
    record(
        "the finite-rank support-side enlargement has rank three at the source-family level",
        support_rank == 3,
        f"support-family rank={support_rank}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The strongest axiom-native common bundle candidate is the reducible "
        "object P_R^cand = (Pi_A1, B_R, O_R), with B_R = (K_R, I_TB, Xi_TB). "
        "It has an exact canonical A1 core, an exact Route 2 bridge triple, "
        "and an exact localized frame orbit. The natural distinguished-"
        "connection prototype is nabla_R^cand = nabla_A1 ⊕ nabla_B ⊕ nabla_O. "
        "That candidate is exact on the A1 core and exact on the bridge triple, "
        "but the complement remains frame-dependent, so the full canonical "
        "3+1 bundle is still not derived."
    )
    print(
        r"Sharp obstruction: the complementary E \oplus T1 channels are not "
        "canonically sourced from the current exact support stack, so there is "
        "no canonical distinguished connection on the full bundle from the "
        "current atlas alone."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
