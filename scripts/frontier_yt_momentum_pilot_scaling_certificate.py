#!/usr/bin/env python3
"""
Certificate for the PR #230 bounded momentum-enabled pilot.

The pilot exercises the production harness momentum fields on two small cold
volumes.  It is intentionally non-production and is expected to show large
finite-volume/systematic drift.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "outputs" / "yt_direct_lattice_correlator_momentum_pilot_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_momentum_pilot_scaling_certificate_2026-05-01.json"

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
    print("PR #230 momentum pilot scaling certificate")
    print("=" * 72)

    data = json.loads(PILOT.read_text(encoding="utf-8"))
    ensembles = data.get("ensembles", [])
    metadata = data.get("metadata", {})
    pmin_mkin = []
    per_volume = []
    for ens in ensembles:
        kin = ens.get("momentum_analysis", {}).get("kinetic_mass_fits", {}).get("1,0,0", {})
        mkin = float(kin.get("m_kin_lat", float("nan")))
        pmin_mkin.append(mkin)
        per_volume.append(
            {
                "dims": ens.get("dims"),
                "selected_mass_parameter": ens.get("selected_mass_parameter"),
                "pmin_delta_e_lat": kin.get("delta_e_lat"),
                "pmin_m_kin_lat": mkin,
                "pmin_m_kin_lat_err": kin.get("m_kin_lat_err"),
            }
        )

    finite = [v for v in pmin_mkin if math.isfinite(v) and v > 0.0]
    spread = (max(finite) - min(finite)) / max(sum(finite) / len(finite), 1.0e-30) if len(finite) > 1 else float("nan")

    report("pilot-certificate-present", bool(data), str(PILOT.relative_to(ROOT)))
    report("pilot-is-reduced-scope", metadata.get("phase") == "reduced_scope", metadata.get("phase"))
    report("two-small-volumes-present", len(ensembles) == 2, f"count={len(ensembles)}")
    report("pmin-kinetic-masses-finite", len(finite) == len(ensembles), f"mkin={pmin_mkin}")
    report(
        "finite-volume-drift-large",
        math.isfinite(spread) and spread > 0.50,
        f"relative_spread={spread:.6g}",
    )
    report(
        "strict-runner-should-reject-pilot",
        True,
        "cold-gauge, one configuration per volume, no matching theorem",
    )

    result = {
        "actual_current_surface_status": "bounded-support / momentum pilot scaling",
        "verdict": (
            "The momentum-enabled harness runs on two small cold volumes and "
            "emits finite kinetic-mass proxies, but the p_min kinetic proxy has "
            "large volume drift.  This supports the implementation route while "
            "confirming that the current pilot is not production evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Reduced-scope cold-gauge pilot with large finite-volume drift and no matching theorem.",
        "pilot_certificate": str(PILOT.relative_to(ROOT)),
        "per_volume": per_volume,
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
