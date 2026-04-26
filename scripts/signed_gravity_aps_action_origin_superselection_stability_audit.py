#!/usr/bin/env python3
"""Origin, superselection, and stability audit for the APS-locked action.

The proposed APS-locked source action is

    S_int = - chi_eta(Y) M_phys <rho, Phi>.

This audit asks three narrower questions:

  1. Can that term be obtained from the retained separable APS/Wald/Gauss
     ingredients without adding the chi*rho*Phi cross term?
  2. Is chi_eta superselected, or only conditionally stable while the APS
     boundary gap is protected?
  3. Does the locked positive-inertial-mass sign law avoid the negative-mass
     runaway control, and what energy-stability gap remains?

This is not a physical signed-gravity claim.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
    hermitian_part,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    status = "PASS" if passed else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


def source_basis_residual(include_cross_term: bool) -> tuple[float, np.ndarray]:
    """Least-squares residual for target [J_+, J_-] = [M, -M]."""

    target = np.array([1.0, -1.0])
    columns = [
        np.array([1.0, 1.0]),  # retained positive Born/Gauss source
        np.array([0.0, 0.0]),  # APS eta spectator term
        np.array([0.0, 0.0]),  # positive Wald area term, Phi-independent
    ]
    if include_cross_term:
        columns.append(np.array([1.0, -1.0]))  # proposed chi*rho*Phi source term
    mat = np.column_stack(columns)
    coeffs, *_ = np.linalg.lstsq(mat, target, rcond=None)
    residual = float(np.linalg.norm(mat @ coeffs - target))
    return residual, coeffs


def chi_of(matrix: np.ndarray) -> int:
    eta, zero, _, _ = eta_delta(matrix)
    return chi_from_eta(eta, zero)


def eta_superselection_rows(samples: int = 200) -> tuple[bool, float, list[int]]:
    rng = np.random.default_rng(20260425)
    d0 = boundary_model(+1, gap=0.4)
    vals = np.linalg.eigvalsh(d0)
    gap = float(np.min(np.abs(vals)))

    stable = True
    min_gap = math.inf
    for _ in range(samples):
        raw = hermitian_part(rng.normal(size=d0.shape) + 1j * rng.normal(size=d0.shape))
        norm = float(np.linalg.norm(raw, ord=2))
        perturb = raw * (0.20 * gap / norm)
        d = d0 + perturb
        stable = stable and chi_of(d) == +1
        min_gap = min(min_gap, float(np.min(np.abs(np.linalg.eigvalsh(d)))))

    path = []
    for t in np.linspace(1.0, -1.0, 9):
        d = d0.copy()
        d[0, 0] = gap * t
        path.append(chi_of(d))
    return stable and min_gap > 0.5 * gap, min_gap, path


def pair_force_residual(mode: str, chi_a: int, chi_b: int) -> tuple[float, int, int]:
    if mode == "locked":
        source_a, response_a = chi_a, chi_a
        source_b, response_b = chi_b, chi_b
    elif mode == "source_only":
        source_a, response_a = chi_a, +1
        source_b, response_b = chi_b, +1
    elif mode == "response_only":
        source_a, response_a = +1, chi_a
        source_b, response_b = +1, chi_b
    else:
        raise ValueError(mode)

    force_a = response_a * source_b
    force_b = -response_b * source_a
    residual = abs(force_a + force_b) / max(abs(force_a), abs(force_b), 1.0e-30)
    return float(residual), force_a, force_b


def potential_energy(chi_a: int, chi_b: int, mass_a: float, mass_b: float, r: float, core: float) -> float:
    """Locked-sign Newtonian pair energy with a finite core softening."""

    return -chi_a * chi_b * mass_a * mass_b / math.sqrt(r * r + core * core)


def energy_rows() -> dict[str, float]:
    mass = 1.0
    rs = np.linspace(0.05, 10.0, 500)
    core = 1.0
    same_totals = np.array([2 * mass + potential_energy(+1, +1, mass, mass, float(r), core) for r in rs])
    opp_totals = np.array([2 * mass + potential_energy(+1, -1, mass, mass, float(r), core) for r in rs])

    small_core = 0.25
    same_small_core = np.array(
        [2 * mass + potential_energy(+1, +1, mass, mass, float(r), small_core) for r in rs]
    )
    return {
        "same_min_core_1": float(np.min(same_totals)),
        "opp_min_core_1": float(np.min(opp_totals)),
        "same_min_core_0p25": float(np.min(same_small_core)),
        "opp_pair_creation_infimum": 2.0 * mass,
    }


def main() -> int:
    print("=" * 100)
    print("APS-LOCKED ACTION: ORIGIN / SUPERSELECTION / STABILITY AUDIT")
    print("  no physical signed-gravity claim")
    print("=" * 100)
    print()

    print("ORIGIN AUDIT")
    retained_residual, retained_coeffs = source_basis_residual(include_cross_term=False)
    extended_residual, extended_coeffs = source_basis_residual(include_cross_term=True)
    check(
        "retained separable APS/Wald/Gauss terms cannot produce signed source",
        retained_residual > 1.0,
        f"least-squares residual={retained_residual:.3e}, coeffs={np.round(retained_coeffs, 3)}",
    )
    check(
        "adding the chi*rho*Phi cross term exactly produces signed source",
        extended_residual < TOL and abs(extended_coeffs[-1] - 1.0) < TOL,
        f"residual={extended_residual:.3e}, coeffs={np.round(extended_coeffs, 3)}",
    )
    print("  read: the proposed action is a genuine new cross term, not a consequence")
    print("        of positive Born source + APS spectator + positive Wald area.")
    print()

    print("ETA SUPERSELECTION AUDIT")
    stable, min_gap, path = eta_superselection_rows()
    check(
        "eta sign is stable under sampled gap-preserving perturbations",
        stable,
        f"min_gap_after={min_gap:.3f}",
    )
    check(
        "eta sign changes through explicit zero-crossing defect if gap is not protected",
        path[:4] == [+1, +1, +1, +1] and path[4] == 0 and path[-4:] == [-1, -1, -1, -1],
        f"chi_path={path}",
    )
    print("  read: superselection is conditional on a protected APS boundary gap.")
    print("        The retained stack has not yet derived that protection.")
    print()

    print("ACTION-REACTION / RUNAWAY CONTROLS")
    locked_residuals = [pair_force_residual("locked", a, b)[0] for a, b in ((+1, +1), (+1, -1), (-1, +1), (-1, -1))]
    source_residuals = [pair_force_residual("source_only", a, b)[0] for a, b in ((+1, +1), (+1, -1), (-1, +1), (-1, -1))]
    response_residuals = [pair_force_residual("response_only", a, b)[0] for a, b in ((+1, +1), (+1, -1), (-1, +1), (-1, -1))]
    check("locked signs have exact two-body force balance", max(locked_residuals) < TOL)
    check("source-only control fails mixed-pair balance", max(source_residuals) > 1.0)
    check("response-only control fails mixed-pair balance", max(response_residuals) > 1.0)

    residual, force_a, force_b = pair_force_residual("locked", +1, -1)
    check(
        "opposite locked signs do not produce negative-mass runaway acceleration",
        residual < TOL and force_a == -1 and force_b == +1,
        f"F_A={force_a:+d}, F_B={force_b:+d}",
    )

    energies = energy_rows()
    check(
        "opposite-sign pair creation has positive rest-energy infimum",
        energies["opp_pair_creation_infimum"] > 0.0 and energies["opp_min_core_1"] > 0.0,
        f"E_opp,min(core=1)={energies['opp_min_core_1']:.3f}",
    )
    ordinary_collapse_seen = energies["same_min_core_0p25"] < 0.0
    check(
        "ordinary same-sector Newtonian collapse remains a UV/core issue",
        ordinary_collapse_seen and energies["same_min_core_1"] > 0.0,
        f"E_same,min(core=1)={energies['same_min_core_1']:.3f}, "
        f"E_same,min(core=0.25)={energies['same_min_core_0p25']:.3f}",
    )
    print("  read: the locked positive-inertial-mass sign law avoids the classic")
    print("        negative-mass runaway control. Full boundedness still requires")
    print("        the same kind of UV/core or constraint input ordinary gravity needs.")
    print()

    print("VERDICT")
    print("  Origin: no-go within retained separable APS/Wald/Gauss terms.")
    print("  Superselection: conditional on a protected boundary spectral gap.")
    print("  Stability: no negative-inertial-mass runaway in the locked table;")
    print("    ordinary attractive collapse/UV boundedness remains open.")
    final_tag = "APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED"
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"FINAL_TAG: {final_tag}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
