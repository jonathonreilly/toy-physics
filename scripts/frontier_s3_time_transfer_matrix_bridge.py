#!/usr/bin/env python3
"""Route 2 transfer-matrix bridge candidate for S^3 + anomaly-forced time.

This script checks whether the retained route-2 ingredients support a clean
bounded transfer-matrix bridge on the background PL S^3 x R:

  1. S^3 topology is exact.
  2. anomaly-forced time is exact (single clock, d_t = 1).
  3. the exact Schur boundary action on the current strong-field class gives a
     symmetric positive definite slice generator Lambda_R.
  4. the induced one-step transfer operator T_R = exp(-Lambda_R) is a
     positive self-adjoint contraction.

The bridge is bounded because the atlas still lacks an exact theorem that turns
this slice generator into a full Einstein/Regge metric dynamics law.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
from scipy.linalg import expm


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    repo_root = Path("/Users/jonreilly/Projects/Physics")
    docs = root / "docs"

    atlas = first_existing([
        repo_root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        docs / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    s3_note = first_existing([
        repo_root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        docs / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    anomaly_note = first_existing([
        repo_root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        docs / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    schur_note = first_existing([
        repo_root / "docs" / "OH_SCHUR_BOUNDARY_ACTION_NOTE.md",
        docs / "OH_SCHUR_BOUNDARY_ACTION_NOTE.md",
    ])
    bridge_note = first_existing([
        repo_root / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md",
        docs / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md",
    ])

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    schur_text = read_text(schur_note)
    bridge_text = read_text(bridge_note)

    schur = SourceFileLoader(
        "oh_schur_boundary_action",
        "/Users/jonreilly/Projects/Physics/scripts/frontier_oh_schur_boundary_action.py",
    ).load_module()
    same_source = SourceFileLoader(
        "same_source_metric",
        "/Users/jonreilly/Projects/Physics/scripts/frontier_same_source_metric_ansatz_scan.py",
    ).load_module()
    coarse = SourceFileLoader(
        "coarse_grained",
        "/Users/jonreilly/Projects/Physics/scripts/frontier_coarse_grained_exterior_law.py",
    ).load_module()

    print("Route 2: S^3 + anomaly-forced time transfer-matrix bridge")
    print("=" * 72)
    print("  Candidate background: PL S^3 x R")
    print()

    check_s3 = "PL homeomorphic to S^3" in s3_text or "Status:** CLOSED" in s3_text
    check_anomaly = "d_t = 1 uniquely" in anomaly_text or "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_text
    check_atlas = "`S^3` cap uniqueness" in atlas_text and "Anomaly-forced time" in atlas_text
    check_schur = "exact microscopic lattice boundary energy" in schur_text.lower() and "Schur-complement boundary energy" in schur_text

    check("S^3 topology theorem is present and closed", check_s3, "S^3 compactification is a retained route-2 tool")
    check("Anomaly-forced time theorem is present and exact", check_anomaly, "single-clock closure is a retained route-2 tool")
    check("Atlas contains both route-2 ingredients as reusable tools", check_atlas, "the atlas exposes the required topology/time primitives")
    check("Schur boundary action is present as the exact slice generator", check_schur, "the slice Hamiltonian comes from the exact microscopic boundary energy")

    size = 15
    cutoff_radius = 4.0
    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(size, cutoff_radius)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(Lambda_sym)
    min_eig = float(np.min(eigvals))
    max_eig = float(np.max(eigvals))

    T = expm(-Lambda_sym)
    T_sym_err = float(np.max(np.abs(T - T.T)))
    T_eigs = np.linalg.eigvalsh(0.5 * (T + T.T))
    T_min_eig = float(np.min(T_eigs))
    T_max_eig = float(np.max(T_eigs))
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(T))))

    oh = schur.analyze_family(same_source.build_best_phi_grid(), Lambda_sym, trace_idx, bulk_idx, interior)
    fr = schur.analyze_family(coarse.build_finite_rank_phi_grid(), Lambda_sym, trace_idx, bulk_idx, interior)

    print()
    print(f"slice trace nodes: {len(trace_idx)}")
    print(f"bulk nodes: {len(bulk_idx)}")
    print(f"Lambda symmetry error: {sym_err:.3e}")
    print(f"Lambda eigenvalue range: [{min_eig:.6e}, {max_eig:.6e}]")
    print(f"T symmetry error: {T_sym_err:.3e}")
    print(f"T eigenvalue range: [{T_min_eig:.6e}, {T_max_eig:.6e}]")
    print(f"T spectral radius: {spectral_radius:.6e}")
    print(
        f"O_h family stationary grad max: {float(np.max(np.abs(oh['grad_expected'] - oh['j_trace']))):.3e}"
    )
    print(
        f"finite-rank family stationary grad max: {float(np.max(np.abs(fr['grad_expected'] - fr['j_trace']))):.3e}"
    )

    check(
        "slice generator is symmetric positive definite",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eig={min_eig:.6e}",
    )
    check(
        "one-step transfer operator is self-adjoint and contractive",
        T_sym_err < 1e-12 and 0.0 < T_min_eig <= T_max_eig < 1.0 and spectral_radius < 1.0,
        f"eig range=[{T_min_eig:.6e}, {T_max_eig:.6e}], spectral radius={spectral_radius:.6e}",
    )
    check(
        "the exact local O_h bridge is stationary for the same slice generator",
        float(np.max(np.abs(oh["grad_expected"] - oh["j_trace"]))) < 1e-12,
        f"max |Lambda f - j| = {float(np.max(np.abs(oh['grad_expected'] - oh['j_trace']))):.3e}",
    )
    check(
        "the broader finite-rank bridge is stationary for the same slice generator",
        float(np.max(np.abs(fr["grad_expected"] - fr["j_trace"]))) < 1e-12,
        f"max |Lambda f - j| = {float(np.max(np.abs(fr['grad_expected'] - fr['j_trace']))):.3e}",
    )
    check(
        "the atlas still lacks an exact PL S^3 x R dynamics bridge",
        "the atlas still lacks an exact theorem" in bridge_text.lower()
        or "atlas still does not contain an exact gr dynamics bridge" in bridge_text.lower(),
        "no exact Einstein/Regge time-coupling theorem is present on this route; gap is documented in the bridge note",
        status="BLOCKED",
    )

    print()
    print("Summary:")
    print("  Background lift: yes")
    print("  Slice transfer generator: yes")
    print("  Exact GR dynamics closure: blocked")
    print("  Missing theorem: exact time-coupling / curvature law on PL S^3 x R")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


def check(name: str, condition: bool, detail: str = "", status: str = "BOUNDED") -> None:
    record(name, condition, detail, status=status)


if __name__ == "__main__":
    raise SystemExit(main())
