#!/usr/bin/env python3
"""
PR #230 mass-response bracket certificate.

Use the existing reduced 12^3 x 24 mass-bracket correlator run to extract a
bare scalar-source response dE/dm_bare.  This is a lightweight data-backed
Feynman-Hellmann scout.  It is not production evidence and not a physical
Yukawa readout because the bare mass/source normalization and matching remain
open.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_mass_response_bracket_certificate_2026-05-01.json"

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


def main() -> int:
    print("PR #230 mass-response bracket certificate")
    print("=" * 72)

    data = json.loads(INPUT.read_text(encoding="utf-8"))
    ensemble = data["ensembles"][0]
    phase = data.get("metadata", {}).get("phase")
    rows = sorted(ensemble["mass_parameter_scan"], key=lambda row: float(row["m_bare_lat"]))
    bare_masses = np.asarray([float(row["m_bare_lat"]) for row in rows], dtype=float)
    fitted_energies = np.asarray([float(row["m_fit_lat"]) for row in rows], dtype=float)
    fitted_errors = np.asarray([float(row.get("m_fit_lat_err", 0.0) or 0.0) for row in rows], dtype=float)

    local_slopes = np.diff(fitted_energies) / np.diff(bare_masses)
    selected_mass = float(ensemble.get("selected_mass_parameter", bare_masses[len(bare_masses) // 2]))
    central_index = int(np.argmin(np.abs(bare_masses - selected_mass)))
    if 0 < central_index < len(bare_masses) - 1:
        central_slope = (fitted_energies[central_index + 1] - fitted_energies[central_index - 1]) / (
            bare_masses[central_index + 1] - bare_masses[central_index - 1]
        )
    else:
        central_slope = local_slopes[min(central_index, len(local_slopes) - 1)]

    coeffs = np.polyfit(bare_masses, fitted_energies, deg=2)
    poly_derivative_at_selected = float(2.0 * coeffs[0] * selected_mass + coeffs[1])
    response_spread = float((np.max(local_slopes) - np.min(local_slopes)) / max(np.mean(local_slopes), 1.0e-30))

    report("mass-bracket-certificate-present", INPUT.exists(), str(INPUT.relative_to(ROOT)))
    report("mass-scan-has-at-least-three-points", len(rows) >= 3, f"points={len(rows)}")
    report("reduced-scope-not-production", phase == "pilot", f"phase={phase}")
    report("fitted-energy-monotone", bool(np.all(np.diff(fitted_energies) > 0.0)), f"energies={fitted_energies.tolist()}")
    report("bare-source-response-positive", bool(np.all(local_slopes > 0.0)), f"local_slopes={local_slopes.tolist()}")
    report("response-not-constant-across-bracket", response_spread > 0.5, f"relative_spread={response_spread:.6g}")
    report("not-physical-yukawa-readout", True, "bare mass/source response still needs scalar-source normalization and matching")

    result = {
        "actual_current_surface_status": "bounded-support / reduced mass-response bracket",
        "verdict": (
            "The existing reduced 12^3 x 24 mass-bracket run already contains "
            "a data-backed Feynman-Hellmann-style response dE/dm_bare.  The "
            "response is positive and monotone, so the observable is viable.  "
            "It is not a physical top Yukawa readout because the run is reduced "
            "scope and because dE/dm_bare is a bare-source response; scalar "
            "source-to-Higgs normalization and lattice-to-SM matching remain "
            "open imports."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Reduced-scope data and bare-source response do not authorize retained proposal wording.",
        "input_certificate": str(INPUT.relative_to(ROOT)),
        "phase": phase,
        "volume": f"{ensemble['spatial_L']}^3x{ensemble['time_L']}",
        "selected_mass_parameter": selected_mass,
        "mass_response": {
            "bare_masses": bare_masses.tolist(),
            "fitted_energies": fitted_energies.tolist(),
            "fitted_errors": fitted_errors.tolist(),
            "local_slopes_dE_dm_bare": local_slopes.tolist(),
            "central_slope_dE_dm_bare": float(central_slope),
            "quadratic_derivative_at_selected": poly_derivative_at_selected,
            "relative_local_slope_spread": response_spread,
        },
        "required_next_steps": [
            "repeat as production response measurement on gauge ensembles",
            "derive or measure scalar source-to-canonical-Higgs normalization",
            "derive lattice-to-SM matching for the response observable",
        ],
        "strict_non_claims": [
            "not production data",
            "not a physical y_t derivation",
            "does not use H_unit matrix-element readout",
            "does not use observed top mass or observed y_t",
            "does not set scalar-source normalization or Z_match to one",
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
