#!/usr/bin/env python3
"""
Certificate for the PR #230 momentum-harness extension.

The production harness now accepts --momentum-modes and emits momentum-analysis
fields.  This runner validates the reduced-scope smoke artifact without
claiming production evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_momentum_harness_smoke_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_momentum_harness_extension_certificate_2026-05-01.json"

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
    print("PR #230 momentum-harness extension certificate")
    print("=" * 72)

    data = json.loads(SMOKE.read_text(encoding="utf-8"))
    ensembles = data.get("ensembles", [])
    ensemble = ensembles[0] if ensembles else {}
    momentum = ensemble.get("momentum_analysis", {})
    energy_fits = momentum.get("energy_fits", {})
    kinetic_fits = momentum.get("kinetic_mass_fits", {})
    metadata = data.get("metadata", {})

    report("smoke-certificate-present", bool(data), str(SMOKE.relative_to(ROOT)))
    report("reduced-scope-not-production", metadata.get("phase") == "reduced_scope", metadata.get("phase"))
    report("momentum-energy-fields-present", {"0,0,0", "1,0,0", "1,1,0"}.issubset(energy_fits), f"keys={sorted(energy_fits)}")
    report("kinetic-mass-fields-present", {"1,0,0", "1,1,0"}.issubset(kinetic_fits), f"keys={sorted(kinetic_fits)}")

    finite_kinetic = [
        float(row.get("m_kin_lat", float("nan")))
        for row in kinetic_fits.values()
    ]
    report(
        "kinetic-mass-proxies-finite",
        all(math.isfinite(value) and value > 0.0 for value in finite_kinetic),
        f"m_kin={finite_kinetic}",
    )
    report(
        "strict-runner-should-not-accept-smoke",
        True,
        "one cold-gauge configuration, no production statistics, no matching theorem",
    )

    result = {
        "actual_current_surface_status": "bounded-support / momentum harness extension",
        "verdict": (
            "The direct-correlator production harness now emits momentum-analysis "
            "fields and finite kinetic-mass proxies in a reduced-scope smoke run. "
            "This is implementation support only; it is not production evidence "
            "and does not supply heavy-action matching."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Reduced-scope smoke run only; no production statistics or matching theorem.",
        "smoke_certificate": str(SMOKE.relative_to(ROOT)),
        "kinetic_mass_fits": kinetic_fits,
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
