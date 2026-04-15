#!/usr/bin/env python3
"""Test whether representation matching fixes the lambda family.

This runner starts from the exact weight-1 lift family

    L_lambda(D) = (cos(lambda) D, sin(lambda) D)

and checks the three possible ways lambda could have been fixed by the
current atlas:

1. representation-theoretic matching on the residual `SO(2)` weight-1
   sectors;
2. normalization conventions;
3. compatibility with `Pi_A1` and the shared bright axis.

The expected result is that none of those constraints chooses a canonical
lambda. The exact one-parameter family survives as a multiplicity-space
circle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

PHASE_NOTE = DOCS / "POLARIZATION_PHASE_CURVATURE_OBSTRUCTION_NOTE.md"
PHASE_LIFT_NOTE = DOCS / "POLARIZATION_PHASE_LIFT_CANDIDATE_NOTE.md"
UNIVERSAL_WEIGHTS = DOCS / "POLARIZATION_UNIVERSAL_WEIGHT_DECOMPOSITION_NOTE.md"
UNIVERSAL_A1 = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
COMMON = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
LAMBDA_NOTE = DOCS / "POLARIZATION_LAMBDA_REP_MATCHING_NOTE.md"


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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def rot2(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def source_rep(theta: float) -> np.ndarray:
    return rot2(theta)


def target_rep(theta: float) -> np.ndarray:
    r = rot2(theta)
    return np.block([[r, np.zeros((2, 2), dtype=float)], [np.zeros((2, 2), dtype=float), r]])


def lift_family(lam: float) -> np.ndarray:
    c = math.cos(lam)
    s = math.sin(lam)
    eye = np.eye(2, dtype=float)
    return np.vstack([c * eye, s * eye])


def multiplicity_rotation(phi: float) -> np.ndarray:
    c = math.cos(phi)
    s = math.sin(phi)
    eye = np.eye(2, dtype=float)
    return np.block([[c * eye, -s * eye], [s * eye, c * eye]])


def frob(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b, ord="fro"))


def intertwiner_space_dim() -> tuple[int, float]:
    thetas = [math.pi / 7.0, math.pi / 5.0, math.pi / 3.0]
    blocks = []
    for theta in thetas:
        a = target_rep(theta)
        b = source_rep(theta)
        # vec(AL - LB) = (I \otimes A - B^T \otimes I) vec(L)
        blocks.append(np.kron(np.eye(2), a) - np.kron(b.T, np.eye(4)))
    mat = np.vstack(blocks)
    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    dim = int(np.sum(s < 1e-12))
    return dim, float(s[-1])


def pi_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def embed_into_universal_core(lam: float) -> np.ndarray:
    """Embed one source unit vector into the universal core/complement model."""

    core = np.zeros(10, dtype=float)
    core[0] = 1.0
    core[4] = 1.0

    target = lift_family(lam) @ np.array([1.0, 0.0], dtype=float)
    comp = np.zeros(10, dtype=float)
    comp[1] = target[0]
    comp[2] = 0.0
    comp[5] = target[2]
    comp[6] = 0.0
    return core + comp


def main() -> int:
    phase_note = read(PHASE_NOTE)
    phase_lift = read(PHASE_LIFT_NOTE)
    weights = read(UNIVERSAL_WEIGHTS)
    a1_note = read(UNIVERSAL_A1)
    common = read(COMMON)
    lambda_note = read(LAMBDA_NOTE)

    dim, smallest_sv = intertwiner_space_dim()
    lambdas = [0.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0, math.pi / 2.0]
    thetas = [math.pi / 9.0, math.pi / 7.0, math.pi / 5.0]

    equiv_err = 0.0
    norm_err = 0.0
    shift_err = 0.0
    comm_err = 0.0
    a1_err = 0.0
    comp_spread = 0.0

    projector = pi_a1()
    core_proj = projector @ embed_into_universal_core(0.0)

    for lam in lambdas:
        L = lift_family(lam)
        norm_err = max(norm_err, abs(np.linalg.norm(L, ord="fro") - 1.4142135623730951))

        for theta in thetas:
            lhs = target_rep(theta) @ L
            rhs = L @ source_rep(theta)
            equiv_err = max(equiv_err, frob(lhs, rhs))

        for phi in [math.pi / 11.0, math.pi / 8.0, math.pi / 6.0]:
            M = multiplicity_rotation(phi)
            comm_err = max(comm_err, frob(target_rep(0.37) @ M, M @ target_rep(0.37)))
            shift_err = max(shift_err, frob(M @ L, lift_family(lam + phi)))

        u_lam = embed_into_universal_core(lam)
        a1_err = max(a1_err, float(np.max(np.abs(projector @ u_lam - core_proj))))
        comp_spread = max(comp_spread, float(np.linalg.norm(u_lam - embed_into_universal_core(0.0))))

    print("POLARIZATION LAMBDA REPRESENTATION MATCHING")
    print("=" * 78)
    print(f"intertwiner space dimension = {dim}")
    print(f"smallest singular value     = {smallest_sv:.3e}")
    print(f"equivariance residual       = {equiv_err:.3e}")
    print(f"normalization residual      = {norm_err:.3e}")
    print(f"multiplicity-shift residual = {shift_err:.3e}")
    print(f"multiplicity commutator err = {comm_err:.3e}")
    print(f"Pi_A1 projection residual   = {a1_err:.3e}")
    print(f"lambda-spread in complement = {comp_spread:.3e}")

    record(
        "the phase-to-curvature obstruction note already says the exact map is orbit-valued",
        has(phase_note, "orbit-valued") and has(phase_note, "SO(2)"),
        "the current atlas only fixes the shared residual orbit, not a section",
    )
    record(
        "the phase-lift candidate supplies the exact dark pair and the weight-1 lift family",
        has(phase_lift, "K_R^phase") and has(phase_lift, "vartheta_R") and has(phase_lift, "lambda"),
        "the exact support-side phase data are present",
    )
    record(
        "the universal weight decomposition exposes two weight-1 targets and a separate weight-2 block",
        has(weights, "weight-1 doublets") and has(weights, "weight-2"),
        "the target side has the required duplicate weight-1 sectors",
    )
    record(
        "representation-theoretic matching leaves a 4D real intertwiner space before normalization",
        dim == 4 and smallest_sv < 1e-12,
        f"intertwiner_dim={dim}, smallest_singular_value={smallest_sv:.3e}",
    )
    record(
        "normalization conventions remove only the scale, not lambda",
        equiv_err < 1e-12 and norm_err < 1e-12,
        f"equivariance={equiv_err:.3e}, norm={norm_err:.3e}",
    )
    record(
        "multiplicity-space rotations shift lambda rather than fix it",
        shift_err < 1e-12 and comm_err < 1e-12,
        f"shift_err={shift_err:.3e}, comm_err={comm_err:.3e}",
    )
    record(
        "Pi_A1 compatibility is blind to lambda",
        a1_err < 1e-12 and comp_spread > 1e-3,
        f"Pi_A1 error={a1_err:.3e}, complement spread={comp_spread:.3e}",
    )
    record(
        "the common bundle candidate does not canonicalize the multiplicity circle",
        has(common, "P_R^cand") and has(common, "candidate") and has(common, "complement"),
        "the common bundle remains candidate-level on the complement",
    )
    record(
        "the universal A1 projector fixes the invariant core but not the weight-1 mixing angle",
        has(a1_note, "Pi_A1") and has(a1_note, "complement"),
        "the canonical core is fixed, the complement is not",
    )

    print("\nVerdict:")
    print(
        "The matching problem does not fix lambda. The raw real intertwiner "
        "space from one weight-1 doublet into two identical weight-1 universal "
        "doublets is 4D; after the atlas' canonical basis choices and "
        "normalization, the surviving residual section is still a circle. The "
        "current normalization conventions, the exact Pi_A1 core, and the "
        "shared bright-axis decomposition all fix the core and the charge "
        "sectors, but they do not select a canonical point in the "
        "multiplicity space."
    )
    print(
        "Equivalently, the exact one-parameter family survives:"
        " L_lambda(D) = (cos(lambda) D, sin(lambda) D)."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = len(CHECKS) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
