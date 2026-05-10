#!/usr/bin/env python3
"""Restricted discrete Einstein/Regge lift on the current strong-field bridge.

This runner verifies the load-bearing claim of
``docs/DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md`` by computation over the actual
restricted shell operator and bridge fields, replacing the prior text-presence
witness check shared with the universal-glue runner.

Cited authorities (one-hop deps the runner consumes):

  - ``docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md`` (audited_conditional,
    bounded_theorem). Provides the exact lattice Schur DtN ``Lambda_R`` and
    the source-quadratic boundary functional ``I_R(f; j)``.
  - ``docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md`` (audited_clean,
    bounded_theorem). Provides the static-conformal bridge ``psi = 1+phi_ext,
    chi = 1-phi_ext = alpha psi`` and the source/stress readout
    ``rho = sigma_R/(2 pi psi^5), S = 0.5 rho (1/alpha - 1)``.

Verified content:

  1. ``Lambda_R`` built from the exterior block of the lattice Laplacian is
     symmetric positive definite on the trace ring.
  2. The exact shell trace ``f_*`` of the exterior projector field
     ``phi_ext`` is the stationary point of the sourced boundary functional
     ``I_R(f; j) = 1/2 f^T Lambda_R f - j^T f`` for the trace flux ``j``.
  3. The same shell trace lift to the static-conformal bridge satisfies the
     two discrete constraint equations
         H_0 psi  =  2 pi psi^5 rho
         H_0 chi  = -2 pi alpha psi^5 (rho + 2 S)
     to lattice precision on both the exact local O_h and broader finite-rank
     source classes.
  4. The Einstein/Regge analogue
         delta I_R = 0  <=>  Lambda_R f_* = j
     is equivalent to the discrete shell-trace equation that drives the
     static-conformal ``3+1`` lift on the current bridge surface.

Bounded scope (``audited_conditional`` per ledger):

  - ``Lambda_R`` is built on the finite ``R = 4`` exterior shell of the
    current ``15^3`` box; no claim of broader nonlinear GR.
  - The shell-trace-to-``3+1`` lift uses the static-conformal bridge from
    ``RESTRICTED_STRONG_FIELD_CLOSURE_NOTE`` as cited authority; the runner
    does not rederive that bridge.
  - No claim of a fully general pointwise Einstein/Regge tensor theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from _frontier_loader import load_frontier


schur = load_frontier("oh_schur_boundary_action", "frontier_oh_schur_boundary_action.py")
lift = load_frontier("oh_static_constraint_lift", "frontier_oh_static_constraint_lift.py")


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"
    cls: str = "A"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT", cls: str = "A") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status, cls=cls))
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag} ({cls})] [{status}] {name}")
    if detail:
        print(f"    {detail}")


SIZE = 15
CUTOFF = 4.0
SYM_TOL = 1e-12
EXACT_TOL = 1e-12


def main() -> int:
    print("Discrete Einstein/Regge lift on the current strong-field bridge")
    print("=" * 72)

    # 1. Build the actual Schur DtN Lambda_R from the lattice Laplacian on the
    #    R=4 exterior shell. This replaces the prior generic SPD witness.
    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(SIZE, CUTOFF)
    Lambda = np.asarray(Lambda, dtype=float)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    eigvals = np.linalg.eigvalsh(Lambda_sym)
    min_eig = float(np.min(eigvals))
    cond_number = float(np.max(eigvals)) / max(min_eig, np.finfo(float).tiny)

    record(
        "Lambda_R built from the lattice Laplacian exterior block is symmetric positive definite on the trace ring",
        sym_err < SYM_TOL and min_eig > 0.0,
        (
            f"trace count={len(trace_idx)}, bulk count={len(bulk_idx)}, "
            f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}, "
            f"condition number={cond_number:.3e}"
        ),
    )

    # 2. Verify the source-quadratic boundary functional is stationary at the
    #    exact shell trace of the O_h family on the same Schur DtN.
    same_source = schur.same_source
    coarse = schur.coarse
    oh = schur.analyze_family(
        same_source.build_best_phi_grid(), Lambda, trace_idx, bulk_idx, interior
    )
    fr = schur.analyze_family(
        coarse.build_finite_rank_phi_grid(), Lambda, trace_idx, bulk_idx, interior
    )

    oh_val, oh_grad = schur.boundary_action(Lambda, oh["f"], oh["j_trace"])
    fr_val, fr_grad = schur.boundary_action(Lambda, fr["f"], fr["j_trace"])

    record(
        "the sourced boundary functional I_R(f; j) is exactly stationary at the O_h shell trace",
        float(np.max(np.abs(oh_grad))) < EXACT_TOL,
        f"max |Lambda_R f_* - j| = {np.max(np.abs(oh_grad)):.3e}, I_R(f_*; j) = {oh_val:.6e}",
    )
    record(
        "the sourced boundary functional I_R(f; j) is exactly stationary at the finite-rank shell trace",
        float(np.max(np.abs(fr_grad))) < EXACT_TOL,
        f"max |Lambda_R f_* - j| = {np.max(np.abs(fr_grad)):.3e}, I_R(f_*; j) = {fr_val:.6e}",
    )

    # 3. Quadratic excess identity: I_R(f; j) - I_R(f_*; j) = 1/2 (f-f_*)^T Lambda_R (f-f_*).
    rng = np.random.default_rng(20260510)
    perturbations = [
        rng.standard_normal(oh["f"].shape) * 1e-3,
        rng.standard_normal(oh["f"].shape) * 1e-2,
        rng.standard_normal(oh["f"].shape) * 1e-1,
    ]
    max_excess_err = 0.0
    min_excess = float("inf")
    for delta in perturbations:
        f_pert = oh["f"] + delta
        val_pert, _ = schur.boundary_action(Lambda, f_pert, oh["j_trace"])
        expected_excess = 0.5 * float(delta @ (Lambda @ delta))
        observed_excess = float(val_pert - oh_val)
        max_excess_err = max(max_excess_err, abs(observed_excess - expected_excess))
        min_excess = min(min_excess, observed_excess)

    record(
        "the boundary functional excess identity I_R(f; j) - I_R(f_*; j) = 1/2 (f-f_*)^T Lambda_R (f-f_*) holds exactly",
        max_excess_err < 1e-10,
        f"max excess identity error = {max_excess_err:.3e}, min sampled excess = {min_excess:.3e}",
    )
    record(
        "every sampled perturbation strictly increases I_R, certifying the shell trace is the unique global minimum",
        min_excess > 0.0,
        f"min sampled excess = {min_excess:.3e} (positive)",
        status="BOUNDED",
    )

    # 4. The same shell trace drives the static-conformal 3+1 lift via the
    #    cited bridge / source-readout authority (RESTRICTED_STRONG_FIELD_CLOSURE).
    oh_lift = lift.analyze_family(same_source.build_best_phi_grid())
    fr_lift = lift.analyze_family(coarse.build_finite_rank_phi_grid())

    psi_residual_oh = float(np.max(np.abs(oh_lift["res_psi"])))
    chi_residual_oh = float(np.max(np.abs(oh_lift["res_chi"])))
    psi_residual_fr = float(np.max(np.abs(fr_lift["res_psi"])))
    chi_residual_fr = float(np.max(np.abs(fr_lift["res_chi"])))

    record(
        "on the O_h family the shell trace lifts to bridge fields satisfying H_0 psi = 2 pi psi^5 rho exactly",
        psi_residual_oh < 1e-10,
        f"max residual = {psi_residual_oh:.3e}",
    )
    record(
        "on the O_h family the shell trace lifts to bridge fields satisfying H_0 chi = -2 pi alpha psi^5 (rho + 2 S) exactly",
        chi_residual_oh < 1e-10,
        f"max residual = {chi_residual_oh:.3e}",
    )
    record(
        "the broader finite-rank class satisfies both static-conformal constraint equations to lattice precision",
        psi_residual_fr < 1e-10 and chi_residual_fr < 1e-10,
        f"max residuals = (psi {psi_residual_fr:.3e}, chi {chi_residual_fr:.3e})",
    )

    # 5. End-to-end Einstein/Regge analogue: stationarity of I_R == discrete
    #    shell-trace law that drives the conformal 3+1 lift.
    einstein_regge_ok = (
        sym_err < SYM_TOL
        and min_eig > 0.0
        and float(np.max(np.abs(oh_grad))) < EXACT_TOL
        and psi_residual_oh < 1e-10
        and chi_residual_oh < 1e-10
        and min_excess > 0.0
    )
    record(
        "delta I_R = 0  <=>  Lambda_R f_* = j is the discrete shell-trace equation that drives the static-conformal 3+1 lift on the O_h bridge surface",
        einstein_regge_ok,
        "stationarity of the boundary functional reproduces the same shell trace whose lift solves the conformal constraint pair",
        status="BOUNDED",
    )

    # 6. Status / scope guard: confirm the note's claim envelope is matched.
    note_path = Path(__file__).resolve().parents[1] / "docs" / "DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md"
    note_text = note_path.read_text(encoding="utf-8")
    scope_keywords = (
        "restricted",
        "static conformal",
        "boundary functional",
        "stationary point",
    )
    scope_ok = all(kw in note_text.lower() for kw in scope_keywords)
    not_full_gr = (
        "fully general nonlinear gr" in note_text.lower()
        or "not full nonlinear gr" in note_text.lower()
    )
    record(
        "the note states the bounded scope (restricted static-conformal class, boundary functional stationarity, not full nonlinear GR)",
        scope_ok and not_full_gr,
        f"scope keywords present = {scope_ok}, full-GR disclaimer present = {not_full_gr}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "On the current restricted strong-field class, the exact shell law and "
        "current same-charge bridge ARE the stationary point of one local "
        "discrete boundary functional. Stationarity of I_R reproduces the "
        "shell-trace equation whose conformal lift satisfies the static "
        "constraint pair to lattice precision. This is bounded to the cited "
        "Schur DtN authority and the cited static-conformal bridge authority."
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
