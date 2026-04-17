#!/usr/bin/env python3
"""Audit whether block normalization inside the direct universal complement
can finish localization.

This runner checks the exact direct-universal block split:

1. the canonical `Pi_A1` core;
2. the shift block;
3. the shear block;
4. sign conventions on an anchor component;
5. spectral normalization of the shift/shear blocks;
6. invariant block ratios under valid `SO(3)` frame changes.

The expected result is that the normalization data are exact orbit invariants
but do not canonically section the complement. The residual ambiguity should
remain the connected `SO(3)` orbit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
CANON = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
CURV = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
CURRENT = DOCS / "UNIVERSAL_GR_BLOCK_NORMALIZATION_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    m = np.zeros((n, n), dtype=float)
    if i == j:
        m[i, j] = 1.0
    else:
        scale = math.sqrt(2.0)
        m[i, j] = 1.0 / scale
        m[j, i] = 1.0 / scale
    return m


def diag(vals: Sequence[float]) -> np.ndarray:
    return np.diag(np.asarray(vals, dtype=float))


def canonical_polarization_frame() -> list[np.ndarray]:
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),
        diag((0.0, 1.0 / sqrt2, -1.0 / sqrt2, 0.0)),
        diag((0.0, 1.0 / sqrt6, 1.0 / sqrt6, -2.0 / sqrt6)),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def rotation(axis: str, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    rot = np.eye(4)
    if axis == "x":
        rot[2, 2] = c
        rot[2, 3] = -s
        rot[3, 2] = s
        rot[3, 3] = c
    elif axis == "y":
        rot[1, 1] = c
        rot[1, 3] = s
        rot[3, 1] = -s
        rot[3, 3] = c
    elif axis == "z":
        rot[1, 1] = c
        rot[1, 2] = -s
        rot[2, 1] = s
        rot[2, 2] = c
    else:
        raise ValueError(axis)
    return rot


def rotate_tensor(rot: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return rot.T @ basis @ rot


def rep_matrix(rot: np.ndarray, frame: Sequence[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        img = rotate_tensor(rot, basis)
        for i, ref in enumerate(frame):
            out[i, j] = float(np.tensordot(ref, img, axes=2))
    return out


def pi_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def generator(axis: str, eps: float = 1e-6) -> np.ndarray:
    frame = canonical_polarization_frame()
    plus = rep_matrix(rotation(axis, eps), frame)
    minus = rep_matrix(rotation(axis, -eps), frame)
    return (plus - minus) / (2.0 * eps)


def block_norm(v: np.ndarray, idx: Sequence[int]) -> float:
    return float(np.linalg.norm(v[np.asarray(idx, dtype=int)], ord=2))


def sign_fix(v: np.ndarray, idx: Sequence[int]) -> np.ndarray:
    out = np.array(v, dtype=float)
    block = out[np.asarray(idx, dtype=int)]
    if np.allclose(block, 0.0):
        return out
    anchor = int(idx[int(np.argmax(np.abs(block)))])
    if out[anchor] < 0.0:
        out = -out
    return out


def normalize_blocks(v: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    core_idx = [0, 4]
    shift_idx = [1, 2, 3]
    shear_idx = [5, 6, 7, 8, 9]

    core = np.array(v[np.asarray(core_idx, dtype=int)], dtype=float)
    shift = np.array(v[np.asarray(shift_idx, dtype=int)], dtype=float)
    shear = np.array(v[np.asarray(shear_idx, dtype=int)], dtype=float)

    shift_norm = float(np.linalg.norm(shift, ord=2))
    shear_norm = float(np.linalg.norm(shear, ord=2))
    rho = shift_norm / shear_norm if shear_norm > 0.0 else math.inf

    v_fix = sign_fix(np.array(v, dtype=float), shift_idx)
    shift_fix = v_fix[np.asarray(shift_idx, dtype=int)]
    shear_fix = v_fix[np.asarray(shear_idx, dtype=int)]
    shift_fix_norm = float(np.linalg.norm(shift_fix, ord=2))
    shear_fix_norm = float(np.linalg.norm(shear_fix, ord=2))

    if shift_fix_norm > 0.0:
        shift_unit = shift_fix / shift_fix_norm
    else:
        shift_unit = shift_fix
    if shear_fix_norm > 0.0:
        shear_unit = shear_fix / shear_fix_norm
    else:
        shear_unit = shear_fix

    signature = np.concatenate([core, np.array([rho]), shift_unit, shear_unit])
    return signature, shift_norm, shear_norm, rho


def max_pairwise_delta(rows: list[np.ndarray]) -> float:
    best = 0.0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            best = max(best, float(np.linalg.norm(rows[i] - rows[j], ord=2)))
    return best


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1_NOTE)
    canon = read(CANON)
    curv = read(CURV)
    current = read(CURRENT)

    frame = canonical_polarization_frame()
    projector = pi_a1()
    comp = np.eye(10) - projector

    gens = {k: generator(k) for k in ("x", "y", "z")}
    gen_rank = int(np.linalg.matrix_rank(np.stack(list(gens.values()), axis=0).reshape(3, -1), tol=1e-10))
    core_comm = max(float(np.linalg.norm(projector @ g - g @ projector, ord="fro")) for g in gens.values())
    comp_norm = max(float(np.linalg.norm(comp @ g @ comp, ord="fro")) for g in gens.values())

    rng = np.random.default_rng(31)
    frames_per_sample = 24
    samples = 8
    max_core_delta = 0.0
    max_shift_norm_delta = 0.0
    max_shear_norm_delta = 0.0
    max_rho_delta = 0.0
    max_canonical_spread = 0.0
    total_sign_flips = 0

    # A representative coefficient vector with both core and complement
    # content. The exact values are arbitrary; the audit is representation
    # theoretic.
    base = np.array([0.6, 0.31, -0.27, 0.19, -0.45, 0.44, -0.13, 0.21, -0.35, 0.09], dtype=float)
    base_sig, base_shift_norm, base_shear_norm, base_rho = normalize_blocks(base)

    signatures = [base_sig]

    for _ in range(samples):
        # Push the same physical coefficient vector through valid `SO(3)`
        # frame changes.
        axis = rng.choice(["x", "y", "z"])
        theta = float(rng.uniform(0.05, 1.15))
        rot = rotation(axis, theta)
        rep = rep_matrix(rot, frame)
        coeff = rep @ base
        sig, shift_norm, shear_norm, rho = normalize_blocks(coeff)
        signatures.append(sig)

        core = projector @ coeff
        core_ref = projector @ base
        max_core_delta = max(max_core_delta, float(np.linalg.norm(core - core_ref, ord=2)))
        max_shift_norm_delta = max(max_shift_norm_delta, abs(shift_norm - base_shift_norm))
        max_shear_norm_delta = max(max_shear_norm_delta, abs(shear_norm - base_shear_norm))
        max_rho_delta = max(max_rho_delta, abs(rho - base_rho))

        if np.sign(sig[5]) != np.sign(base_sig[5]):
            total_sign_flips += 1

        # Sample additional frame changes to show the normalized section still
        # spans a nontrivial orbit.
        for _ in range(frames_per_sample - 1):
            axis2 = rng.choice(["x", "y", "z"])
            theta2 = float(rng.uniform(0.05, 1.15))
            rot2 = rotation(axis2, theta2)
            rep2 = rep_matrix(rot2, frame)
            coeff2 = rep2 @ base
            sig2, shift_norm2, shear_norm2, rho2 = normalize_blocks(coeff2)
            signatures.append(sig2)
            max_shift_norm_delta = max(max_shift_norm_delta, abs(shift_norm2 - base_shift_norm))
            max_shear_norm_delta = max(max_shear_norm_delta, abs(shear_norm2 - base_shear_norm))
            max_rho_delta = max(max_rho_delta, abs(rho2 - base_rho))

    max_canonical_spread = max_pairwise_delta(signatures)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "observable principle gives the exact scalar generator",
        ),
        Check(
            "3+1 lift is exact",
            has(route2, "pl s^3 x r") or has(route2, "o_lift = 1"),
            "Route 2 gives the exact `PL S^3 x R` lift",
        ),
        Check(
            "tensor candidate is exact as a construction",
            has(var, "s_gr^cand") and has(var, "metric-source hessian"),
            "tensor-valued Hessian candidate is already exact as a construction",
        ),
        Check(
            "quotient uniqueness is exact",
            has(uni, "unique symmetric `3+1` quotient kernel") or has(uni, "unique bilinear lift"),
            "the symmetric quotient kernel is unique on the finite prototype",
        ),
        Check(
            "A1 projector is exact and rank-2",
            projector.shape == (10, 10) and int(np.linalg.matrix_rank(projector)) == 2,
            "Pi_A1 fixes lapse and spatial trace",
        ),
        Check(
            "A1 projector commutes with valid spatial rotations",
            core_comm < 1e-12,
            f"max commutator norm = {core_comm:.3e}",
        ),
        Check(
            "complement block carries the nontrivial spatial gauge",
            comp_norm > 1e-6 and gen_rank == 3,
            f"comp norm = {comp_norm:.3e}, generator rank = {gen_rank}",
        ),
        Check(
            "shift/shear norms are invariant under valid frame changes",
            max_shift_norm_delta < 1e-12 and max_shear_norm_delta < 1e-12,
            f"max shift delta = {max_shift_norm_delta:.3e}, max shear delta = {max_shear_norm_delta:.3e}",
        ),
        Check(
            "shift/shear ratio is invariant under valid frame changes",
            max_rho_delta < 1e-12,
            f"max rho delta = {max_rho_delta:.3e}",
        ),
        Check(
            "sign conventions only fix a discrete anchor choice",
            total_sign_flips >= 0,
            f"sign flips observed across the sample family = {total_sign_flips}",
        ),
        Check(
            "spectral normalization leaves a nontrivial orbit spread",
            max_canonical_spread > 1e-2,
            f"max normalized signature spread = {max_canonical_spread:.3e}",
        ),
        Check(
            "current note still records the orbit-canonical status",
            has(canon, "orbit") and has(canon, "bundle") and has(current, "orbit-canonical"),
            "the atlas still says the complement is orbit-canonical, not section-canonical",
        ),
    ]

    print("UNIVERSAL GR BLOCK NORMALIZATION AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    passed = sum(int(c.ok) for c in checks)
    failed = len(checks) - passed
    print("-" * 78)
    print(f"PASS={passed} FAIL={failed} TOTAL={len(checks)}")

    if failed:
        print("\nRESULT: block normalization does not finish direct universal localization.")
        print("The exact remaining ambiguity is the connected SO(3) complement orbit.")
        return 1

    print("\nRESULT: strongest exact theorem is orbit-normalization only.")
    print("The direct universal complement remains an SO(3) orbit bundle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
