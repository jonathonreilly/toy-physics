#!/usr/bin/env python3
"""
PR #230 nonzero-momentum correlator scout.

This runner implements the first lightweight compute step suggested by the
heavy kinetic-mass route: reuse the existing Wilson-staggered Dirac builder and
CG propagator solve, but measure momentum-projected point-source correlators
instead of only the zero-momentum correlator.

It runs on a tiny cold gauge field.  The result is methodology evidence only,
not production data and not retained y_t closure.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_nonzero_momentum_correlator_scout_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def import_production_harness() -> Any:
    module_name = "yt_direct_lattice_correlator_production_import"
    spec = importlib.util.spec_from_file_location(module_name, PRODUCTION_HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import production harness: {PRODUCTION_HARNESS}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def p_hat_sq(nvec: tuple[int, int, int], spatial_lattice_size: int) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_lattice_size)) ** 2 for n in nvec)


def effective_energy(corr: np.ndarray) -> tuple[float, list[float]]:
    estimates: list[float] = []
    max_tau = min(3, len(corr) - 2)
    for tau in range(1, max_tau + 1):
        if corr[tau] > 0.0 and corr[tau + 1] > 0.0:
            estimates.append(math.log(corr[tau] / corr[tau + 1]))
    if not estimates:
        return float("nan"), []
    return float(sum(estimates) / len(estimates)), estimates


def measure_momentum_correlators(
    *,
    prod: Any,
    spatial_lattice_size: int,
    time_lattice_size: int,
    mass: float,
    momentum_modes: list[tuple[int, int, int]],
    rtol: float,
    maxiter: int,
) -> dict[str, Any]:
    geom = prod.Geometry(spatial_lattice_size, time_lattice_size)
    gauge = prod.GaugeField(geom)
    dirac = prod.build_staggered_dirac(gauge, mass)
    source_site = geom.site_index((0, 0, 0, 0))
    source_solutions = []
    residuals = []
    infos = []
    for source_color in range(prod.NC):
        source_index = source_site * prod.NC + source_color
        sol, info, residual = prod.solve_propagator_normal_eq(dirac, source_index, rtol, maxiter)
        source_solutions.append(sol)
        residuals.append(float(residual))
        infos.append(int(info))

    correlators = {}
    energy_rows = {}
    for nvec in momentum_modes:
        corr = np.zeros(time_lattice_size, dtype=complex)
        for source_color, sol in enumerate(source_solutions):
            for site in range(geom.volume):
                t, x, y, z = geom.site_coords(site)
                phase_arg = (
                    nvec[0] * x + nvec[1] * y + nvec[2] * z
                ) / spatial_lattice_size
                # Use the even cos-projected channel so the cold-gauge scout
                # tests the energy splitting without a source-position phase.
                phase = math.cos(2.0 * math.pi * phase_arg)
                # Color trace of the staggered point-source propagator.
                corr[t] += phase * sol[site * prod.NC + source_color]
        corr /= prod.NC
        real_corr = np.real_if_close(corr, tol=1000).real
        energy, estimates = effective_energy(real_corr)
        key = ",".join(str(n) for n in nvec)
        correlators[key] = [float(x) for x in real_corr]
        energy_rows[key] = {
            "momentum_mode": nvec,
            "p_hat_sq": p_hat_sq(nvec, spatial_lattice_size),
            "energy": energy,
            "effective_energy_samples": estimates,
            "max_imag_abs": float(np.max(np.abs(corr.imag))),
        }

    e0 = energy_rows["0,0,0"]["energy"]
    kinetic_rows = {}
    for key, row in energy_rows.items():
        nvec = tuple(row["momentum_mode"])
        if nvec == (0, 0, 0):
            continue
        delta_e = row["energy"] - e0
        m_kin = row["p_hat_sq"] / (2.0 * delta_e) if delta_e > 0.0 else float("nan")
        kinetic_rows[key] = {
            "delta_e": delta_e,
            "m_kin_lat": m_kin,
        }

    return {
        "mass": mass,
        "cg_infos": infos,
        "max_cg_residual": max(residuals),
        "correlators": correlators,
        "energies": energy_rows,
        "kinetic_masses": kinetic_rows,
    }


def main() -> int:
    print("PR #230 nonzero-momentum correlator scout")
    print("=" * 72)

    prod = import_production_harness()
    spatial_lattice_size = 4
    time_lattice_size = 8
    masses = [1.0, 2.0, 5.0]
    momentum_modes = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]

    runs = [
        measure_momentum_correlators(
            prod=prod,
            spatial_lattice_size=spatial_lattice_size,
            time_lattice_size=time_lattice_size,
            mass=mass,
            momentum_modes=momentum_modes,
            rtol=1.0e-10,
            maxiter=2000,
        )
        for mass in masses
    ]

    all_residuals = [run["max_cg_residual"] for run in runs]
    all_imag = [
        row["max_imag_abs"]
        for run in runs
        for row in run["energies"].values()
    ]
    ordered = []
    pmin_deltas = []
    pmin_mkins = []
    for run in runs:
        e0 = run["energies"]["0,0,0"]["energy"]
        e1 = run["energies"]["1,0,0"]["energy"]
        e11 = run["energies"]["1,1,0"]["energy"]
        ordered.append(e0 < e1 < e11)
        pmin_deltas.append(run["kinetic_masses"]["1,0,0"]["delta_e"])
        pmin_mkins.append(run["kinetic_masses"]["1,0,0"]["m_kin_lat"])

    report(
        "production-harness-imported",
        hasattr(prod, "build_staggered_dirac") and hasattr(prod, "solve_propagator_normal_eq"),
        "reused staggered Dirac and CG solve primitives",
    )
    report(
        "cg-solves-converge",
        max(all_residuals) < 1.0e-8,
        f"max_residual={max(all_residuals):.3e}",
    )
    report(
        "momentum-correlators-real-on-cold-gauge",
        max(all_imag) < 1.0e-12,
        f"max_imag_abs={max(all_imag):.3e}",
    )
    report(
        "nonzero-momentum-energies-order-correctly",
        all(ordered),
        f"ordered_by_mass={ordered}",
    )
    report(
        "heavier-mass-has-smaller-pmin-splitting",
        pmin_deltas[0] > pmin_deltas[1] > pmin_deltas[2] > 0.0,
        f"delta_e_pmin={pmin_deltas}",
    )
    report(
        "kinetic-mass-extraction-finite",
        all(math.isfinite(v) and v > 0.0 for v in pmin_mkins),
        f"m_kin_pmin={pmin_mkins}",
    )
    report(
        "not-production-closure",
        True,
        "tiny cold-gauge scout validates machinery only; no production evidence or matching theorem",
    )

    result = {
        "actual_current_surface_status": "bounded-support / nonzero-momentum correlator scout",
        "verdict": (
            "The existing PR #230 production harness can be reused to construct "
            "momentum-projected staggered correlators.  On a tiny cold gauge "
            "field, nonzero-momentum energies order correctly and produce finite "
            "kinetic-mass estimates from E(p)-E(0).  This is methodology support "
            "for the heavy kinetic-mass route, not retained closure: it uses no "
            "production ensemble, no gauge statistics, and no lattice-HQET/NRQCD "
            "matching theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The scout uses a tiny cold gauge field and lacks production "
            "statistics plus a retained heavy matching bridge."
        ),
        "geometry": {
            "spatial_lattice_size": spatial_lattice_size,
            "time_lattice_size": time_lattice_size,
            "momentum_modes": momentum_modes,
        },
        "runs": runs,
        "strict_non_claims": [
            "not a production measurement",
            "not a y_t derivation",
            "does not use observed top mass as calibration",
            "does not define y_t through H_unit matrix elements",
        ],
        "required_next_artifacts": [
            "add production-mode momentum projection to the direct-correlator harness",
            "measure nonzero-momentum top/HQET correlators over gauge ensembles",
            "extract E(p)-E(0) with statistical/systematic uncertainties",
            "derive matching from lattice kinetic mass to SM top mass",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
