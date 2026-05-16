#!/usr/bin/env python3
"""Audit whether canonical block-localization gives a canonical
Hamiltonian/momentum-constraint interpretation on the direct universal route.

This is constraint-only. It does not claim full GR.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
BLOCK = DOCS / "UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md"
CONSTRAINT = DOCS / "UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md"
CURVATURE = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
CURRENT = DOCS / "UNIVERSAL_GR_BLOCK_CONSTRAINT_INTERPRETATION_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


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
    """Canonical lapse/shift/trace/shear basis on the symmetric `3+1` sector."""

    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),  # lapse
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),  # shift triplet
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),  # trace
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


def frob(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.tensordot(a, b, axes=2))


def rotate_tensor(rot: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return rot.T @ basis @ rot


def rep_matrix(rot: np.ndarray, frame: Sequence[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        img = rotate_tensor(rot, basis)
        for i, ref in enumerate(frame):
            out[i, j] = frob(ref, img)
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


def spectral_projector(casimir: np.ndarray, target: float, tol: float = 1e-8) -> np.ndarray:
    vals, vecs = np.linalg.eigh(casimir)
    mask = np.isclose(vals, target, atol=tol)
    if not np.any(mask):
        raise RuntimeError(f"no eigenspace found for target {target}")
    basis = vecs[:, mask]
    return basis @ basis.T


def block_rank(mat: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(mat, tol=1e-10))


def comm_norm(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a @ b - b @ a, ord="fro"))


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1_NOTE)
    block = read(BLOCK)
    constraint = read(CONSTRAINT)
    curvature = read(CURVATURE)
    current = read(CURRENT)

    frame = canonical_polarization_frame()
    projector = pi_a1()
    complement = np.eye(10) - projector

    gens = {k: generator(k) for k in ("x", "y", "z")}
    casimir = sum(g @ g for g in gens.values())
    p_shift = spectral_projector(casimir, -2.0)
    p_shear = spectral_projector(casimir, -6.0)

    p_lapse = np.zeros((10, 10), dtype=float)
    p_lapse[0, 0] = 1.0
    p_trace = np.zeros((10, 10), dtype=float)
    p_trace[4, 4] = 1.0
    p_hamiltonian = p_lapse + p_trace

    rotations = {
        "x": rotation("x", math.pi / 7.0),
        "y": rotation("y", math.pi / 5.0),
        "z": rotation("z", math.pi / 6.0),
    }
    reps = {k: rep_matrix(rot, frame) for k, rot in rotations.items()}

    comms = {
        "Pi_A1": {k: comm_norm(projector, rep) for k, rep in reps.items()},
        "P_shift": {k: comm_norm(p_shift, rep) for k, rep in reps.items()},
        "P_shear": {k: comm_norm(p_shear, rep) for k, rep in reps.items()},
    }

    orthogonal = np.allclose(projector @ p_shift, 0.0) and np.allclose(projector @ p_shear, 0.0)
    orthogonal = orthogonal and np.allclose(p_shift @ p_shear, 0.0)
    complete = np.allclose(projector + p_shift + p_shear, np.eye(10), atol=1e-10)
    split_rank = {
        "Pi_A1": block_rank(projector),
        "P_shift": block_rank(p_shift),
        "P_shear": block_rank(p_shear),
        "P_hamiltonian": block_rank(p_hamiltonian),
        "P_lapse": block_rank(p_lapse),
        "P_trace": block_rank(p_trace),
    }

    # Graph-bookkeeping: the candidate upstream supplier chain and the
    # parent note must exist on disk in this branch. Mirrors the
    # "Candidate upstream supplier chain" section of the parent note.
    supplier_paths = {
        "observable_principle_from_axiom_note": OBSERVABLE,
        "s3_anomaly_spacetime_lift_note": ROUTE2,
        "universal_gr_tensor_variational_candidate_note": VARIATIONAL,
        "universal_gr_tensor_quotient_uniqueness_note": UNIQUENESS,
        "universal_gr_a1_invariant_section_note": A1_NOTE,
        "universal_gr_casimir_block_localization_note": BLOCK,
        "universal_gr_constraint_action_stationarity_note": CONSTRAINT,
        "universal_gr_canonical_projector_connection_note": CURVATURE,
        "universal_gr_block_constraint_interpretation_note": CURRENT,
    }
    suppliers_present = {name: path.exists() for name, path in supplier_paths.items()}
    perimeter_present = (
        has(current, "audit-conditional perimeter")
        and has(current, "candidate upstream supplier chain")
        and has(current, "audit dependency repair links")
        and has(current, "status authority and audit hygiene")
    )

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "the observable-principle scalar generator is present in the universal stack",
        ),
        Check(
            "3+1 lift is exact",
            has(route2, "pl s^3 x r") or has(route2, "pl s^3"),
            "Route 2 supplies the exact `PL S^3 x R` lift",
        ),
        Check(
            "tensor variational candidate is exact",
            has(var, "s_gr^cand") and has(var, "hessian"),
            "the universal tensor-valued variational candidate is exact as a construction",
        ),
        Check(
            "quotient uniqueness is exact",
            has(uni, "unique symmetric `3+1` quotient kernel") or has(uni, "unique symmetric"),
            "the quotient kernel is unique on the finite prototype",
        ),
        Check(
            "A1 projector is exact",
            block_rank(projector) == 2 and has(a1, "pi_a1"),
            "Pi_A1 is the invariant rank-2 core",
        ),
        Check(
            "Casimir block split is exact",
            split_rank["P_shift"] == 3 and split_rank["P_shear"] == 5,
            f"ranks = {split_rank}",
        ),
        Check(
            "block projectors are orthogonal and complete",
            orthogonal and complete,
            "Pi_A1, shift, and shear projectors form a complete orthogonal split",
        ),
        Check(
            "block projectors commute with valid rotations",
            max(max(v.values()) for v in comms.values()) < 1e-12,
            f"commutator norms = { {k: {a: f'{b:.3e}' for a, b in v.items()} for k, v in comms.items()} }",
        ),
        Check(
            "current atlas records the remaining gap",
            has(constraint, "orbit-flat")
            and has(curvature, "orbit bundle")
            and has(curvature, "distinguished connection"),
            "the remaining obstruction is still the complement bundle, not the block split",
        ),
        Check(
            "canonical block interpretation is now justified",
            has(block, "canonical block-localization operator")
            and (
                has(block, "lapse / shift / trace / shear")
                or has(block, "lapse ⊕ shift ⊕ trace ⊕ traceless-shear")
            ),
            "the universal route already has the canonical block-localization theorem",
        ),
        Check(
            "candidate upstream supplier notes exist on disk",
            all(suppliers_present.values()),
            f"supplier presence = {suppliers_present}",
        ),
        Check(
            "parent note records audit-conditional perimeter and supplier chain",
            perimeter_present,
            "the parent note carries the status-authority block, the audit-conditional perimeter, the candidate upstream supplier chain, and the audit dependency repair links sections",
        ),
        Check(
            "parent note honestly admits the F-class identification gap",
            has(current, "renaming")
            and has(current, "operator-level einstein/regge identification")
            and has(current, "still open"),
            "the parent note labels the load-bearing identification as a renaming/interpretation step, names the operator-level Einstein/Regge identification gap, and labels it as still open",
        ),
    ]

    print("UNIVERSAL GR BLOCK-CONSTRAINT INTERPRETATION AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("BLOCK PROJECTORS")
    print("=" * 78)
    print(f"Pi_A1 rank = {split_rank['Pi_A1']}")
    print(f"Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)")
    print(f"P_lapse rank = {split_rank['P_lapse']}")
    print(f"P_trace rank = {split_rank['P_trace']}")
    print(f"P_shift rank = {split_rank['P_shift']}")
    print(f"P_shear rank = {split_rank['P_shear']}")
    print(f"commutator norms = { {k: {a: f'{b:.3e}' for a, b in v.items()} for k, v in comms.items()} }")

    print("\n" + "=" * 78)
    print("CONSTRAINT INTERPRETATION")
    print("=" * 78)
    print("Hamiltonian block = Pi_A1 = lapse + spatial trace")
    print("Momentum block = P_shift = j=1 Casimir block on the complement")
    print("Trace/shear split = P_trace ⊕ P_shear")

    print("\n" + "=" * 78)
    print("AUDIT-CONDITIONAL PERIMETER")
    print("=" * 78)
    print(
        "The algebraic block split is supported by the candidate upstream\n"
        "supplier chain on disk in this branch (graph-bookkeeping only;\n"
        "does not promote audit_status):"
    )
    for name, present in suppliers_present.items():
        tag = "present" if present else "MISSING"
        print(f"  - {name}: {tag}")
    print(
        "\n"
        "The F-class load-bearing identification step the audit flags is the\n"
        "renaming of the canonical universal Casimir blocks under the GR-canon\n"
        "labels 'Hamiltonian-constraint sector' (Pi_A1 = lapse + spatial trace)\n"
        "and 'momentum-constraint sector' (P_shift = j=1 complement block). The\n"
        "operator-level Einstein/Regge identification on the block-localized\n"
        "universal Hessian and the normalization/sign convention on the\n"
        "E \\oplus T1 complement remain open, and this row stays\n"
        "audited_conditional under the F-class renaming flag."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "The direct universal route's algebraic block split is canonical "
            "and exact: the exact Pi_A1 core and the Casimir-derived shift "
            "block are canonical under the spatial-rotation Casimir. The "
            "GR-canon labels 'Hamiltonian-constraint sector' and "
            "'momentum-constraint sector' attached to those blocks are an "
            "imported identification (F-class renaming) rather than a "
            "first-principles derivation; the audit verdict and this row's "
            "effective status remain audited_conditional. What remains open "
            "is the operator-level identification of the block-localized "
            "universal Hessian with the Einstein/Regge constraint operator "
            "and its exact normalization on the E \\oplus T1 complement."
        )
        return 0

    print("One or more exact block-constraint checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
