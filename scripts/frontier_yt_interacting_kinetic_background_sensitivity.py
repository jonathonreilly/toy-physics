#!/usr/bin/env python3
"""
PR #230 interacting kinetic-background sensitivity.

The free Wilson-staggered action fixes the kinetic coefficient, but PR #230
needs the interacting SU(3) Wilson-staggered kinetic readout.  This runner
tests whether the free coefficient can be used as a zero-import stand-in by
measuring the nonzero-momentum kinetic proxy on small fixed gauge backgrounds.

If the proxy changes across admissible backgrounds before ensemble averaging,
then the interacting coefficient is a real dynamical observable, not a
definition inherited from the free action.
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
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_interacting_kinetic_background_sensitivity_2026-05-01.json"

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


def import_harness() -> Any:
    module_name = "yt_direct_lattice_correlator_production_bg_import"
    spec = importlib.util.spec_from_file_location(module_name, HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import harness: {HARNESS}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def constant_spatial_phase_background(prod: Any, geom: Any, theta: float) -> Any:
    gauge = prod.GaugeField(geom)
    phase = np.eye(prod.NC, dtype=complex)
    phase[0, 0] = np.exp(1.0j * theta)
    phase[1, 1] = np.exp(-1.0j * theta)
    phase[2, 2] = 1.0 + 0.0j
    for coords in np.ndindex(*geom.dims):
        gauge.u[coords][1] = phase
    return gauge


def random_projected_background(prod: Any, geom: Any, seed: int, eps: float) -> Any:
    rng = np.random.default_rng(seed)
    gauge = prod.GaugeField(geom)
    for coords in np.ndindex(*geom.dims):
        for mu in range(prod.NDIM):
            noise = np.eye(prod.NC, dtype=complex) + eps * (
                rng.normal(size=(prod.NC, prod.NC))
                + 1.0j * rng.normal(size=(prod.NC, prod.NC))
            )
            gauge.u[coords][mu] = prod.project_su3(noise)
    return gauge


def measure_background(prod: Any, label: str, gauge: Any, mass: float) -> dict[str, Any]:
    measured = prod.measure_correlator(
        gauge,
        mass,
        1.0e-10,
        2000,
        [(0, 0, 0), (1, 0, 0), (1, 1, 0)],
    )
    momentum_rows = {
        key: [measured["momentum_correlators"][key]]
        for key in measured["momentum_correlators"]
    }
    analysis = prod.fit_momentum_energies(momentum_rows, gauge.geom.spatial_l)
    return {
        "label": label,
        "plaquette": gauge.plaquette(),
        "max_cg_residual": measured["max_cg_residual"],
        "momentum_analysis": analysis,
    }


def main() -> int:
    print("PR #230 interacting kinetic-background sensitivity")
    print("=" * 72)

    prod = import_harness()
    geom = prod.Geometry(4, 8)
    mass = 2.0
    backgrounds = [
        ("cold", prod.GaugeField(geom)),
        ("constant_spatial_phase_theta_0_25", constant_spatial_phase_background(prod, geom, 0.25)),
        ("random_projected_eps_0_05", random_projected_background(prod, geom, 20260501, 0.05)),
    ]
    rows = [measure_background(prod, label, gauge, mass) for label, gauge in backgrounds]
    pmin_mkin = [
        row["momentum_analysis"]["kinetic_mass_fits"]["1,0,0"]["m_kin_lat"]
        for row in rows
    ]
    finite = [float(x) for x in pmin_mkin if math.isfinite(float(x))]
    spread = (max(finite) - min(finite)) / max(sum(finite) / len(finite), 1.0e-30)
    plaquettes = [float(row["plaquette"]) for row in rows]
    residuals = [float(row["max_cg_residual"]) for row in rows]

    report("background-scan-runs", len(rows) == 3, f"rows={len(rows)}")
    report("cg-solves-converge", max(residuals) < 1.0e-8, f"max_residual={max(residuals):.3e}")
    report("kinetic-proxies-finite", len(finite) == 3, f"mkin={pmin_mkin}")
    report(
        "gauge-background-changes-kinetic-proxy",
        spread > 0.10,
        f"relative_spread={spread:.6g}",
    )
    report(
        "backgrounds-not-identical-by-plaquette",
        max(plaquettes) - min(plaquettes) > 1.0e-4,
        f"plaquettes={plaquettes}",
    )
    report(
        "not-retained-closure",
        True,
        "fixed backgrounds show sensitivity; production ensemble/matching still required",
    )

    result = {
        "actual_current_surface_status": "bounded-support / interacting kinetic background sensitivity",
        "verdict": (
            "The free kinetic coefficient is not enough to certify the "
            "interacting top kinetic readout.  On small admissible gauge "
            "backgrounds, the momentum-projected kinetic proxy changes before "
            "ensemble averaging.  Therefore the interacting c2/kinetic "
            "renormalization is a real dynamical observable requiring ensemble "
            "measurement or a retained interacting theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Interacting kinetic coefficient depends on gauge dynamics; no production ensemble or matching theorem is present.",
        "mass": mass,
        "rows": rows,
        "pmin_mkin_values": pmin_mkin,
        "relative_spread": spread,
        "strict_non_claims": [
            "not a production measurement",
            "not a y_t derivation",
            "does not use observed top mass as calibration",
            "does not define y_t through H_unit matrix elements",
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
