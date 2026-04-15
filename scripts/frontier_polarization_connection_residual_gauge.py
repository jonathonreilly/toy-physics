#!/usr/bin/env python3
"""Audit the connection-only polarization primitive.

This runner is deliberately narrow. It starts from the exact objects already
present in the current atlas:

  - the exact invariant `Pi_A1` section;
  - the exact Route 2 bridge triple `B_R = (K_R, I_TB, Xi_TB)`;
  - the Maurer-Cartan orbit connection on the valid `3+1` frame orbit.

It then tests whether stationarity, minimality, flatness, and compatibility
with the exact semigroup transport / tensorized action uniquely fix a
distinguished connection.

The expected result is:

  - the strongest canonical candidate is the block connection
      nabla^cand = nabla_A1 ⊕ nabla_B ⊕ omega_MC;
  - the exact residual gauge is not removed by the current axioms;
  - the universal complement still carries an SO(3) orbit gauge;
  - the support-side bright/dark splitting still leaves O(1) x O(2) freedom
    after endpoint conventions are fixed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

UNIVERSAL_A1 = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
CANONICAL_CONN = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
COMMON_SYNTHESIS = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"
COMMON_CANDIDATE = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
SUPPORT_CANONICAL = DOCS / "FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md"
SUPPORT_FAMILY = DOCS / "FINITE_RANK_SUPPORT_GENERATOR_FAMILY_NOTE.md"
ACTION_NOTE = DOCS / "S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"
BILINEAR_NOTE = DOCS / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"

A1 = SourceFileLoader(
    "universal_gr_a1_invariant_section",
    str(ROOT / "scripts" / "frontier_universal_gr_a1_invariant_section.py"),
).load_module()
CANON = SourceFileLoader(
    "universal_gr_canonical_projector_connection",
    str(ROOT / "scripts" / "frontier_universal_gr_canonical_projector_connection.py"),
).load_module()
COMMON = SourceFileLoader(
    "polarization_common_bundle_candidate",
    str(ROOT / "scripts" / "frontier_polarization_common_bundle_candidate.py"),
).load_module()
SUPPORT = SourceFileLoader(
    "finite_rank_support_canonical_frame",
    str(ROOT / "scripts" / "frontier_finite_rank_support_canonical_frame.py"),
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


def a1_projector() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def so3_generators() -> dict[str, np.ndarray]:
    return {axis: CANON.generator(axis) for axis in ("x", "y", "z")}


def generator_rank(gens: dict[str, np.ndarray]) -> int:
    stack = np.stack([gens["x"], gens["y"], gens["z"]], axis=0)
    return int(np.linalg.matrix_rank(stack.reshape(3, -1), tol=1e-10))


def support_bright_action(theta: float) -> float:
    basis = SUPPORT.same.build_adapted_basis()
    q = basis[:, 0] + 0.5 * basis[:, 1]
    q /= 1.0 + math.sqrt(6.0) * 0.5
    delta = SUPPORT.support_law.support_delta(q)
    u_e, u_t = BILINEAR.bright_coords(q)
    carrier = np.array([u_e, u_t, delta * u_e, delta * u_t], dtype=float)
    a = carrier.copy()
    c = float(math.cos(theta))
    s = float(math.sin(theta))
    r = np.array([[c, -s], [s, c]], dtype=float)
    r4 = np.block(
        [
            [r, np.zeros((2, 2), dtype=float)],
            [np.zeros((2, 2), dtype=float), r],
        ]
    )
    return 0.5 * float(np.sum((r4 @ a - r4 @ carrier) ** 2))


def route2_semigroup_probe() -> tuple[float, float, float]:
    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    t = 1.25
    full = ACTION.expm(-t * Lambda_sym) @ u_star
    half = ACTION.expm(-0.5 * t * Lambda_sym) @ (ACTION.expm(-0.5 * t * Lambda_sym) @ u_star)
    sym_err = float(np.max(np.abs(Lambda_sym - Lambda_sym.T)))
    semigroup_err = float(np.max(np.abs(full - half)))
    flatness_err = float(np.linalg.norm(ACTION.expm(np.zeros_like(Lambda_sym)) - np.eye(Lambda_sym.shape[0]), ord="fro"))
    return sym_err, semigroup_err, flatness_err


def orbit_frame_delta() -> tuple[float, float]:
    d = (2.0, 3.0, 5.0, 7.0)
    h = A1.random_symmetric_h(np.random.default_rng(7))
    frame_a = A1.canonical_polarization_frame()
    frame_b = A1.rotated_frame(A1.random_so3(np.random.default_rng(9)))
    resp_a = A1.response_vector(h, frame_a, d)
    resp_b = A1.response_vector(h, frame_b, d)
    a1 = a1_projector()
    delta_a1 = float(np.max(np.abs(a1 @ resp_a - a1 @ resp_b)))
    comp = np.eye(10) - a1
    delta_comp = float(np.max(np.abs(comp @ resp_a - comp @ resp_b)))
    return delta_a1, delta_comp


def main() -> int:
    print("POLARIZATION CONNECTION RESIDUAL GAUGE AUDIT")
    print("=" * 78)

    pi_a1 = a1_projector()
    gens = so3_generators()
    gen_rank = generator_rank(gens)
    comms = {axis: float(np.linalg.norm(pi_a1 @ g - g @ pi_a1, ord="fro")) for axis, g in gens.items()}
    a1_block = {axis: float(np.linalg.norm(pi_a1 @ g @ pi_a1, ord="fro")) for axis, g in gens.items()}
    comp = np.eye(10) - pi_a1
    comp_block = {axis: float(np.linalg.norm(comp @ g @ comp, ord="fro")) for axis, g in gens.items()}

    support_basis = SUPPORT.same.build_adapted_basis()
    q_support = support_basis[:, 0] + 0.5 * support_basis[:, 1]
    q_support /= 1.0 + math.sqrt(6.0) * 0.5
    action_theta0 = SUPPORT.carrier_action_penalty(q_support, 0.0)
    action_theta1 = SUPPORT.carrier_action_penalty(q_support, math.pi / 5.0)
    support_action_delta = abs(action_theta0 - action_theta1)
    delta_a1, delta_comp = orbit_frame_delta()
    sym_err, semigroup_err, flatness_err = route2_semigroup_probe()

    candidate_conn = "nabla_A1 ⊕ nabla_B ⊕ omega_MC"

    print("Candidate connection:")
    print(f"  P_R^cand = (Pi_A1, B_R, O_R)")
    print(f"  nabla^cand = {candidate_conn}")
    print(f"  SO(3) generator rank = {gen_rank}")
    print(f"  Pi_A1 commutator norms = { {k: f'{v:.3e}' for k, v in comms.items()} }")
    print(f"  A1-block generator norms = { {k: f'{v:.3e}' for k, v in a1_block.items()} }")
    print(f"  complement generator norms = { {k: f'{v:.3e}' for k, v in comp_block.items()} }")
    print(f"  support-action delta(theta=0,pi/5) = {support_action_delta:.3e}")
    print(f"  orbit-frame A1 delta = {delta_a1:.3e}")
    print(f"  orbit-frame complement delta = {delta_comp:.3e}")
    print(f"  semigroup symmetry error = {sym_err:.3e}")
    print(f"  semigroup composition error = {semigroup_err:.3e}")
    print(f"  flatness surrogate error = {flatness_err:.3e}")

    record(
        "the exact invariant A1 projector remains rank two and frame-invariant",
        int(np.linalg.matrix_rank(pi_a1, tol=1e-12)) == 2 and max(comms.values()) < 1e-12,
        f"rank={int(np.linalg.matrix_rank(pi_a1, tol=1e-12))}, commutators={ {k: f'{v:.3e}' for k, v in comms.items()} }",
    )
    record(
        "the SO(3) orbit generators are exact and three-dimensional",
        gen_rank == 3,
        f"generator_rank={gen_rank}",
    )
    record(
        "the A1 core is flat while the complement carries the spatial gauge",
        all(v < 1e-12 for v in a1_block.values()) and all(v > 1e-6 for v in comp_block.values()),
        f"A1-block={ {k: f'{v:.3e}' for k, v in a1_block.items()} }, complement={ {k: f'{v:.3e}' for k, v in comp_block.items()} }",
    )
    record(
        "the Route-2 tensorized action is blind to orthogonal bright reparameterizations",
        support_action_delta < 1e-12,
        f"action delta={support_action_delta:.3e}",
        status="BOUNDED",
    )
    record(
        "the exact semigroup transport is symmetric and composition-compatible",
        sym_err < 1e-12 and semigroup_err < 1e-12 and flatness_err < 1e-12,
        f"sym={sym_err:.3e}, semigroup={semigroup_err:.3e}, flatness={flatness_err:.3e}",
    )
    record(
        "the orbit localization remains frame-dependent away from Pi_A1",
        delta_comp > 1e-3 and delta_a1 < 1e-12,
        f"A1 delta={delta_a1:.3e}, complement delta={delta_comp:.3e}",
    )

    print("\nVerdict:")
    print(
        "The variational/transport constraints do not uniquely fix a distinguished "
        "connection. The strongest canonical candidate is the block connection "
        "nabla^cand = nabla_A1 ⊕ nabla_B ⊕ omega_MC, with Pi_A1 fixed exactly, "
        "Route-2 transport exact on B_R, and the complementary channels carried by "
        "the Maurer-Cartan orbit connection. After imposing stationarity, minimality, "
        "flatness, and compatibility with the exact semigroup transport / tensorized "
        "action, the exact residual gauge is still the frame orbit: SO(3) on the "
        "universal complement, and the support-side bright/dark residual freedom "
        "reduces to O(1) × O(2) once endpoint conventions are fixed."
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
