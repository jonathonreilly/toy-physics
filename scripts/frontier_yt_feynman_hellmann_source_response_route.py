#!/usr/bin/env python3
"""
PR #230 Feynman-Hellmann scalar-response route.

This runner tests a route distinct from absolute top-mass extraction:
measure the response of a top correlator energy to a uniform scalar source.
The route can remove additive rest-mass ambiguity, but it still needs the
scalar source normalization / Higgs-field matching before it can be a physical
Yukawa readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_feynman_hellmann_source_response_route_2026-05-01.json"

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


def log_correlator(
    t: np.ndarray, *, additive_mass: float, residual_energy: float, scalar_charge: float, source: float
) -> np.ndarray:
    amplitude = 1.0 + 0.07 * source + 0.01 * source * source
    energy = additive_mass + residual_energy + scalar_charge * source + 0.15 * source * source
    return math.log(amplitude) - energy * t


def effective_energy(log_c: np.ndarray) -> np.ndarray:
    return log_c[:-1] - log_c[1:]


def fit_energy_slope(sources: np.ndarray, energies: np.ndarray) -> float:
    coeffs = np.polyfit(sources, energies, deg=1)
    return float(coeffs[0])


def main() -> int:
    print("PR #230 Feynman-Hellmann scalar-response route")
    print("=" * 72)

    t = np.arange(2.0, 9.0)
    sources = np.asarray([-0.002, 0.0, 0.002], dtype=float)
    true_scalar_charge = 1.0 / math.sqrt(6.0)
    residual_energy = 0.35
    additive_masses = [5.0, 50.0, 500.0]

    rows = []
    for additive_mass in additive_masses:
        energies = []
        subtracted_energies = []
        for source in sources:
            log_c = log_correlator(
                t,
                additive_mass=additive_mass,
                residual_energy=residual_energy,
                scalar_charge=true_scalar_charge,
                source=source,
            )
            e_eff = float(np.mean(effective_energy(log_c)[1:]))
            energies.append(e_eff)
            subtracted_energies.append(e_eff - additive_mass)
        slope = fit_energy_slope(sources, np.asarray(energies))
        subtracted_slope = fit_energy_slope(sources, np.asarray(subtracted_energies))
        rows.append(
            {
                "additive_mass": additive_mass,
                "slope": slope,
                "subtracted_slope": subtracted_slope,
                "slope_error": abs(slope - true_scalar_charge),
                "subtracted_slope_error": abs(subtracted_slope - true_scalar_charge),
            }
        )

    source_rescalings = [0.75, 1.0, 1.25]
    rescaled_readouts = []
    for kappa_source in source_rescalings:
        # If the physical source is h = kappa_source * s, then dE/dh differs
        # from the lattice-source slope by the inverse source normalization.
        rescaled_readouts.append(
            {
                "kappa_source": kappa_source,
                "same_lattice_slope": true_scalar_charge,
                "physical_slope_if_h_equals_kappa_s": true_scalar_charge / kappa_source,
            }
        )

    max_slope_error = max(row["slope_error"] for row in rows)
    max_subtracted_error = max(row["subtracted_slope_error"] for row in rows)
    physical_slopes = [row["physical_slope_if_h_equals_kappa_s"] for row in rescaled_readouts]
    physical_spread = (max(physical_slopes) - min(physical_slopes)) / (sum(physical_slopes) / len(physical_slopes))

    report("fh-energy-slope-recovers-source-charge", max_slope_error < 5.0e-4, f"max_slope_error={max_slope_error:.3e}")
    report("additive-mass-cancels-in-response", max_subtracted_error < 5.0e-4, f"max_subtracted_error={max_subtracted_error:.3e}")
    report("source-rescaling-changes-physical-readout", physical_spread > 0.35, f"relative_spread={physical_spread:.6g}")
    report("does-not-use-observed-targets", True, "synthetic response stress test only")
    report("does-not-use-h-unit", True, "route is correlator response, not matrix-element definition")
    report("not-retained-closure", True, "needs scalar-source-to-Higgs normalization and production correlators")

    result = {
        "actual_current_surface_status": "bounded-support / Feynman-Hellmann source-response route",
        "verdict": (
            "A Feynman-Hellmann scalar-source response is a viable alternate "
            "observable route because an energy slope dE/ds can be extracted "
            "without relying on the absolute additive rest mass.  However, the "
            "slope is with respect to the chosen lattice scalar source.  A "
            "rescaling of that source changes the physical dE/dh Yukawa readout "
            "unless the source-to-Higgs normalization or scalar LSZ residue is "
            "derived.  The route is therefore bounded support, not PR #230 "
            "retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Scalar source normalization and production response data remain open imports.",
        "true_scalar_charge_in_synthetic_test": true_scalar_charge,
        "additive_mass_rows": rows,
        "source_rescaling_rows": rescaled_readouts,
        "required_next_theorem_or_evidence": [
            "derive the scalar source-to-canonical-Higgs normalization",
            "or measure the scalar LSZ residue directly on production ensembles",
            "and measure the Feynman-Hellmann top response on gauge ensembles",
        ],
        "strict_non_claims": [
            "not a production measurement",
            "not a y_t derivation",
            "does not define y_t via H_unit",
            "does not import observed top mass or observed y_t",
            "does not set Z_match or scalar-source normalization to one",
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
