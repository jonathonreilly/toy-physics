#!/usr/bin/env python3
"""Flux-fixed lattice matching decomposition for the strong-field exterior.

Exact content:
  1. Any exact lattice exterior field with finite enclosed source charge admits
     a unique point-Green representative Q * G_0, where Q is fixed by the
     enclosed discrete charge.
  2. The remainder h = phi - Q * G_0 has zero monopole charge and is harmonic
     outside the joint source support.

Bounded content:
  3. For the exact local O_h source class and the broader exact finite-rank
     source class already on codex/review-active, the flux-fixed point-Green
     representative captures the lattice shell data strongly in the same
     exterior regime where the coarse-grained radial law becomes vacuum-close.
  4. The remaining mismatch is therefore not monopole charge, but the
     anisotropic zero-monopole remainder already identified as the cubic l=4
     sector.

This is not full nonlinear GR. It replaces the ad hoc continuum fit a/r by an
exact lattice decomposition: conserved monopole charge plus a zero-monopole
harmonic remainder.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np
from scipy.sparse.linalg import spsolve


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name, ok, detail, status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


same_source = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
finite_rank = load_frontier("finite_rank_metric", "frontier_finite_rank_gravity_residual.py")
coarse = load_frontier("coarse_grained", "frontier_coarse_grained_exterior_law.py")


def build_point_green_grid(size: int) -> np.ndarray:
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    center = interior // 2
    src = finite_rank.flat_idx(center, center, center, interior)
    rhs = np.zeros(H0.shape[0])
    rhs[src] = 1.0
    col = spsolve(H0, rhs)
    grid = np.zeros((size, size, size))
    grid[1:-1, 1:-1, 1:-1] = col.reshape((interior, interior, interior))
    return grid


def full_neg_laplacian(field: np.ndarray) -> np.ndarray:
    lap = np.zeros_like(field)
    lap[1:-1, 1:-1, 1:-1] = (
        6.0 * field[1:-1, 1:-1, 1:-1]
        - field[2:, 1:-1, 1:-1]
        - field[:-2, 1:-1, 1:-1]
        - field[1:-1, 2:, 1:-1]
        - field[1:-1, :-2, 1:-1]
        - field[1:-1, 1:-1, 2:]
        - field[1:-1, 1:-1, :-2]
    )
    return lap


def enclosed_charge(field: np.ndarray, radius: int) -> float:
    lap = full_neg_laplacian(field)
    center = field.shape[0] // 2
    sl = slice(center - radius, center + radius + 1)
    return float(np.sum(lap[sl, sl, sl]))


def charge_stability_rows(field: np.ndarray):
    return [(radius, enclosed_charge(field, radius)) for radius in [2, 3, 4, 5]]


def shell_relative_errors(phi_grid: np.ndarray, rep_grid: np.ndarray, r_match: float):
    usable, radii, _ = coarse.shell_data(phi_grid)
    d2s = [d2 for d2 in usable if radii[d2] >= r_match]
    rels = []
    size = phi_grid.shape[0]
    center = (size - 1) / 2.0
    for d2 in d2s:
        vals = []
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                for k in range(1, size - 1):
                    dx = i - center
                    dy = j - center
                    dz = k - center
                    if int(dx * dx + dy * dy + dz * dz) == d2:
                        exact = float(phi_grid[i, j, k])
                        rep = float(rep_grid[i, j, k])
                        vals.append(abs(exact - rep) / max(abs(exact), 1e-12))
        rels.append((radii[d2], float(max(vals))))
    return rels


def analyze_family(name: str, phi_grid: np.ndarray):
    size = phi_grid.shape[0]
    point_green = build_point_green_grid(size)

    charge_rows = charge_stability_rows(phi_grid)
    q_vals = np.array([row[1] for row in charge_rows], dtype=float)
    q_mean = float(np.mean(q_vals))
    rep_grid = q_mean * point_green

    rep_charge_rows = charge_stability_rows(rep_grid)
    rem_rows = charge_stability_rows(phi_grid - rep_grid)

    print(f"\n{name}:")
    for radius, q in charge_rows:
        print(f"  enclosed charge at R={radius}: {q:.8f}")
    for radius, q in rem_rows:
        print(f"  remainder charge at R={radius}: {q:.3e}")

    matching_rows = []
    for r_match in [3.0, 3.5, 4.0, 4.5, 5.0]:
        rels = shell_relative_errors(phi_grid, rep_grid, r_match)
        max_rel = max(rel for _, rel in rels)
        rms_rel = float(np.sqrt(np.mean([rel * rel for _, rel in rels])))
        matching_rows.append((r_match, max_rel, rms_rel))
        print(f"  R_match={r_match:.1f}  rep_max_rel={max_rel:.4f}  rep_rms_rel={rms_rel:.4f}")

    return charge_rows, rep_charge_rows, rem_rows, matching_rows, q_mean


def first_window(rows, rel_thresh: float):
    for row in rows:
        if row[1] < rel_thresh:
            return row
    return None


def main() -> None:
    print("Flux-fixed lattice matching decomposition")
    print("=" * 72)

    phi_oh = same_source.build_best_phi_grid()
    oh_charge_rows, oh_rep_charge_rows, oh_rem_rows, oh_rows, oh_q = analyze_family(
        "exact local O_h family", phi_oh
    )

    phi_fr = coarse.build_finite_rank_phi_grid()
    fr_charge_rows, fr_rep_charge_rows, fr_rem_rows, fr_rows, fr_q = analyze_family(
        "exact finite-rank family", phi_fr
    )

    oh_q_spread = max(abs(q - oh_q) for _, q in oh_charge_rows)
    fr_q_spread = max(abs(q - fr_q) for _, q in fr_charge_rows)
    oh_rep_spread = max(abs(q - oh_q) for _, q in oh_rep_charge_rows)
    fr_rep_spread = max(abs(q - fr_q) for _, q in fr_rep_charge_rows)
    oh_rem_spread = max(abs(q) for _, q in oh_rem_rows)
    fr_rem_spread = max(abs(q) for _, q in fr_rem_rows)

    record(
        "exact local O_h field has radius-independent enclosed charge",
        oh_q_spread < 1e-10 and oh_rep_spread < 1e-10,
        f"exact spread={oh_q_spread:.3e}, representative spread={oh_rep_spread:.3e}",
    )
    record(
        "exact finite-rank field has radius-independent enclosed charge",
        fr_q_spread < 1e-10 and fr_rep_spread < 1e-10,
        f"exact spread={fr_q_spread:.3e}, representative spread={fr_rep_spread:.3e}",
    )
    record(
        "the local O_h remainder after subtracting Q*G_0 carries zero monopole charge",
        oh_rem_spread < 1e-10,
        f"max enclosed remainder charge={oh_rem_spread:.3e}",
    )
    record(
        "the finite-rank remainder after subtracting Q*G_0 carries zero monopole charge",
        fr_rem_spread < 1e-10,
        f"max enclosed remainder charge={fr_rem_spread:.3e}",
    )

    w_oh = first_window(oh_rows, rel_thresh=1e-10)
    w_fr = first_window(fr_rows, rel_thresh=0.015)

    record(
        "flux-fixed lattice Green representative matches the local O_h shell data exactly outside the source",
        w_oh is not None,
        (
            f"first exact shell window at R_match={w_oh[0]:.1f}: max_rel={w_oh[1]:.3e}"
            if w_oh is not None
            else "no exact shell window found"
        ),
        status="BOUNDED",
    )
    record(
        "flux-fixed lattice Green representative captures the finite-rank shell data at the percent level",
        w_fr is not None,
        (
            f"first shell window at R_match={w_fr[0]:.1f}: max_rel={w_fr[1]:.4f}, rms_rel={w_fr[2]:.4f}"
            if w_fr is not None
            else "no percent-level shell window found"
        ),
        status="BOUNDED",
    )
    record(
        "the shell-level matching regime starts in the same exterior band",
        w_oh is not None and w_fr is not None and abs(w_oh[0] - w_fr[0]) <= 1.5,
        (
            f"O_h shell window={w_oh[0]:.1f}, finite-rank shell window={w_fr[0]:.1f}"
            if w_oh is not None and w_fr is not None
            else "window comparison unavailable"
        ),
        status="BOUNDED",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
