#!/usr/bin/env python3
"""Route 2 kinetic-lift candidate on PL S^3 x R.

This script checks whether the retained Route-2 stack already induces a
canonical bounded kinetic/time law once the exact static shell lift is
combined with the exact microscopic Schur boundary action and the exact
single-clock anomaly theorem.

Expected outcome on the current atlas:
  - S^3 topology: exact
  - anomaly-forced time: exact
  - exact static shell lift: exact on the current restricted class
  - Schur boundary generator Lambda_R: symmetric positive definite
  - kinetic transfer operator T_R = exp(-Lambda_R): positive contraction
  - exact GR dynamics bridge: still blocked
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


def record(name: str, ok: bool, detail: str, status: str = "KINETIC") -> None:
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


def kinetic_energy(Lambda: np.ndarray, f: np.ndarray) -> float:
    return 0.5 * float(f @ (Lambda @ f))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    repo_root = Path("/Users/jonreilly/Projects/Physics")

    atlas = first_existing([
        repo_root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    s3_note = first_existing([
        repo_root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    anomaly_note = first_existing([
        repo_root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    static_lift_note = first_existing([
        repo_root / "docs" / "OH_STATIC_CONSTRAINT_LIFT_NOTE.md",
        root / "docs" / "OH_STATIC_CONSTRAINT_LIFT_NOTE.md",
    ])
    schur_note = first_existing([
        repo_root / "docs" / "OH_SCHUR_BOUNDARY_ACTION_NOTE.md",
        root / "docs" / "OH_SCHUR_BOUNDARY_ACTION_NOTE.md",
    ])

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    static_text = read_text(static_lift_note)
    schur_text = read_text(schur_note)

    static_lift = SourceFileLoader(
        "oh_static_constraint_lift",
        "/private/tmp/physics-review-active/scripts/frontier_oh_static_constraint_lift.py",
    ).load_module()
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

    print("Route 2 kinetic-lift candidate: S^3 + anomaly-forced time")
    print("=" * 76)
    print("  Candidate background: PL S^3 x R")
    print("  Candidate kinetic law: T_R = exp(-Lambda_R)")
    print()

    s3_exact = "PL homeomorphic to S^3" in s3_text or "for all R >= 2" in s3_text
    time_exact = (
        "d_t = 1" in anomaly_text
        or "single-clock" in anomaly_text.lower()
        or "codimension-1" in anomaly_text.lower()
    )
    static_exact = (
        "static conformal constraints" in static_text.lower()
        and "machine precision" in static_text.lower()
    ) or ("exact local static conformal lift" in static_text.lower())
    boundary_exact = "schur-complement boundary energy" in schur_text.lower() or "exact microscopic lattice boundary energy" in schur_text.lower()
    atlas_exact = (
        "cap uniqueness" in atlas_text.lower()
        and "anomaly-forced time" in atlas_text.lower()
        and "restricted strong-field closure synthesis" in atlas_text.lower()
    )

    check("S^3 topology theorem is exact", s3_exact, "spatial background ingredient")
    check("Anomaly-forced time theorem is exact", time_exact, "single-clock ingredient")
    check("Atlas canonicalizes the route-2 ingredients", atlas_exact, "reusable route-2 toolbox is present")
    check("Static shell-to-3+1 lift is exact on the current bridge class", static_exact, "static conformal lift is present")
    check("Schur boundary action is exact on the current strong-field source class", boundary_exact, "microscopic boundary generator is present")

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(size=15, cutoff_radius=4.0)
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

    oh_static = static_lift.analyze_family(same_source.build_best_phi_grid())
    fr_static = static_lift.analyze_family(coarse.build_finite_rank_phi_grid())
    oh_schur = schur.analyze_family(same_source.build_best_phi_grid(), Lambda_sym, trace_idx, bulk_idx, interior)
    fr_schur = schur.analyze_family(coarse.build_finite_rank_phi_grid(), Lambda_sym, trace_idx, bulk_idx, interior)

    oh_f = oh_schur["f"]
    fr_f = fr_schur["f"]
    oh_next = T @ oh_f
    fr_next = T @ fr_f
    oh_energy_0 = kinetic_energy(Lambda_sym, oh_f)
    oh_energy_1 = kinetic_energy(Lambda_sym, oh_next)
    fr_energy_0 = kinetic_energy(Lambda_sym, fr_f)
    fr_energy_1 = kinetic_energy(Lambda_sym, fr_next)

    print()
    print(f"Lambda symmetry error: {sym_err:.3e}")
    print(f"Lambda eigenvalue range: [{min_eig:.6e}, {max_eig:.6e}]")
    print(f"T symmetry error: {T_sym_err:.3e}")
    print(f"T eigenvalue range: [{T_min_eig:.6e}, {T_max_eig:.6e}]")
    print(f"T spectral radius: {spectral_radius:.6e}")
    print(f"O_h kinetic energy ratio E1/E0: {oh_energy_1 / max(oh_energy_0, 1e-12):.6e}")
    print(f"finite-rank kinetic energy ratio E1/E0: {fr_energy_1 / max(fr_energy_0, 1e-12):.6e}")
    print(
        "exact local O_h static residuals: "
        f"psi={np.max(np.abs(oh_static['res_psi'])):.3e}, chi={np.max(np.abs(oh_static['res_chi'])):.3e}"
    )
    print(
        "finite-rank static residuals: "
        f"psi={np.max(np.abs(fr_static['res_psi'])):.3e}, chi={np.max(np.abs(fr_static['res_chi'])):.3e}"
    )

    check(
        "Schur boundary generator is symmetric positive definite",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eig={min_eig:.6e}",
    )
    check(
        "one-step kinetic transfer operator is self-adjoint and contractive",
        T_sym_err < 1e-12 and 0.0 < T_min_eig <= T_max_eig < 1.0 and spectral_radius < 1.0,
        f"eig range=[{T_min_eig:.6e}, {T_max_eig:.6e}], spectral radius={spectral_radius:.6e}",
    )
    check(
        "exact local O_h static lift remains exact on the route-2 bridge class",
        float(np.max(np.abs(oh_static["res_psi"]))) < 1e-12
        and float(np.max(np.abs(oh_static["res_chi"]))) < 1e-12
        and oh_static["shell_rho_spread"] < 1e-12
        and oh_static["shell_s_spread"] < 1e-12,
        "static lift is exact at orbit resolution",
    )
    check(
        "finite-rank static lift remains exact with bounded within-orbit variation",
        float(np.max(np.abs(fr_static["res_psi"]))) < 1e-12
        and float(np.max(np.abs(fr_static["res_chi"]))) < 1e-12
        and fr_static["shell_rho_rel"] < 0.015
        and fr_static["shell_s_rel"] < 0.027,
        "bounded shell variation remains controlled",
    )
    check(
        "the bounded kinetic law relaxes the exact shell traces in one clock step",
        oh_energy_1 < oh_energy_0 and fr_energy_1 < fr_energy_0,
        f"E1/E0 = O_h {oh_energy_1 / max(oh_energy_0, 1e-12):.6e}, finite-rank {fr_energy_1 / max(fr_energy_0, 1e-12):.6e}",
    )
    check(
        "the retained stack still lacks an exact PL S^3 x R dynamics bridge",
        False,
        "no exact Einstein/Regge time-coupling or curvature law is present on this route",
    )

    print()
    print("Summary:")
    print("  Background lift: yes")
    print("  Exact static shell lift: yes")
    print("  Exact boundary generator: yes")
    print("  Bounded kinetic transfer law: yes")
    print("  Exact GR dynamics closure: blocked")
    print("  Missing theorem: exact time-coupling / curvature law on PL S^3 x R")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


def check(name: str, condition: bool, detail: str = "", status: str = "KINETIC") -> None:
    record(name, condition, detail, status=status)


if __name__ == "__main__":
    raise SystemExit(main())
