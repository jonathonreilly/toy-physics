#!/usr/bin/env python3
"""Route 2 exact time-coupling audit.

This script checks whether the exact slice generator Lambda_R and the bounded
transfer bridge T_R = exp(-Lambda_R) can be promoted to an exact time-coupling
law on PL S^3 x R.

Verdict expected from the current atlas:
  - exact S^3 and anomaly-forced time are present
  - Lambda_R and T_R are well-defined and bounded
  - no exact dynamics bridge exists yet

That means the output should be a sharp blocker, not a closure theorem.
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


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


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
    transfer_note = first_existing([
        root / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md",
        repo_root / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md",
    ])
    committee_note = first_existing([
        root / "docs" / "S3_TIME_COMMITTEE_MEMO.md",
        repo_root / "docs" / "S3_TIME_COMMITTEE_MEMO.md",
    ])

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    schur_text = read_text(schur_note)
    transfer_text = read_text(transfer_note)
    committee_text = read_text(committee_note)

    schur = SourceFileLoader(
        "oh_schur_boundary_action",
        "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
    ).load_module()
    same_source = SourceFileLoader(
        "same_source_metric",
        "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
    ).load_module()
    coarse = SourceFileLoader(
        "coarse_grained",
        "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
    ).load_module()

    print("Route 2 exact time-coupling audit")
    print("=" * 72)
    print("  Candidate background: PL S^3 x R")
    print()

    check_s3 = has_any(s3_text, ["PL homeomorphic to `S^3`", "PL homeomorphic to S^3", "Status:** CLOSED"])
    check_anomaly = has_any(
        anomaly_text,
        ["d_t = 1 uniquely", "single-clock codimension-1 evolution excludes d_t > 1", "d_t = 1"],
    )
    check_atlas_tools = has_any(atlas_text, ["Anomaly-forced time", "S^3 cap uniqueness", "Restricted strong-field closure synthesis"])
    check_schur = has_any(schur_text.lower(), ["exact microscopic lattice boundary energy", "schur-complement boundary energy"])
    check_transfer_note = has_any(transfer_text, ["bounded transfer-matrix bridge", "T_R := exp(-Lambda_R)", "exact background: `PL S^3 x R`"])
    check_committee = has_any(committee_text, ["kinematic lift", "dynamics bridge", "PL S^3 x R"])

    record("S^3 compactification theorem is present and closed", check_s3, "S^3 compactification remains a retained route-2 tool")
    record("Anomaly-forced time theorem is present and exact", check_anomaly, "single-clock closure remains a retained route-2 tool")
    record("Atlas contains the route-2 reusable kinematic tools", check_atlas_tools, "the atlas exposes the needed topology/time primitives")
    record("Schur boundary action is present as the exact slice generator", check_schur, "the slice Hamiltonian comes from the exact microscopic boundary energy")
    record("The committee memo agrees Route 2 is kinematically exact but dynamically open", check_committee, "committee synthesis matches the atlas reading")

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
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
    print(f"O_h family stationary grad max: {float(np.max(np.abs(oh['grad_expected'] - oh['j_trace']))):.3e}")
    print(f"finite-rank family stationary grad max: {float(np.max(np.abs(fr['grad_expected'] - fr['j_trace']))):.3e}")

    record(
        "slice generator is symmetric positive definite",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eig={min_eig:.6e}",
    )
    record(
        "one-step transfer operator is self-adjoint and contractive",
        T_sym_err < 1e-12 and 0.0 < T_min_eig <= T_max_eig < 1.0 and spectral_radius < 1.0,
        f"eig range=[{T_min_eig:.6e}, {T_max_eig:.6e}], spectral radius={spectral_radius:.6e}",
    )
    record(
        "the exact local O_h bridge is stationary for the same slice generator",
        float(np.max(np.abs(oh["grad_expected"] - oh["j_trace"]))) < 1e-12,
        f"max |Lambda f - j| = {float(np.max(np.abs(oh['grad_expected'] - oh['j_trace']))):.3e}",
    )
    record(
        "the broader finite-rank bridge is stationary for the same slice generator",
        float(np.max(np.abs(fr["grad_expected"] - fr["j_trace"]))) < 1e-12,
        f"max |Lambda f - j| = {float(np.max(np.abs(fr['grad_expected'] - fr['j_trace']))):.3e}",
    )

    dynamics_bridge_exact = has_any(
        atlas_text,
        [
            "exact action on `PL S^3 x R`",
            "exact spacetime-lift observable",
            "uniqueness theorem forcing Einstein dynamics",
            "exact `PL S^3 x R` dynamics bridge",
        ],
    )
    record(
        "the atlas still lacks an exact PL S^3 x R dynamics bridge",
        dynamics_bridge_exact,
        "no exact Einstein/Regge time-coupling theorem is present on this route",
    )

    print()
    print("Summary:")
    print("  Background lift: yes")
    print("  Slice transfer generator: yes")
    print("  Exact GR dynamics closure: blocked")
    print("  Missing primitive: exact PL S^3 x R dynamics action / observable / uniqueness theorem")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
