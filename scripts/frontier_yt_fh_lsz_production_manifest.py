#!/usr/bin/env python3
"""
PR #230 joint Feynman-Hellmann / scalar-LSZ production manifest.

This is not a production run and not evidence.  It converts the existing
FH/LSZ protocol and resource projection into a resumable command manifest so
the production route has an exact launch surface without pretending the
multi-day/single-worker compute has been completed.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "outputs" / "yt_fh_production_protocol_certificate_2026-05-01.json"
RESOURCE = ROOT / "outputs" / "yt_fh_lsz_joint_resource_projection_2026-05-01.json"
HARNESS = ROOT / "outputs" / "yt_fh_lsz_joint_harness_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_production_manifest_2026-05-01.json"

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


def shell_join(parts: list[str]) -> str:
    return " ".join(parts)


def main() -> int:
    print("PR #230 joint FH/LSZ production manifest")
    print("=" * 72)

    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
    harness = json.loads(HARNESS.read_text(encoding="utf-8"))

    volumes = [
        {"label": "L12_T24", "volume": "12x24", "seed": 2026050101},
        {"label": "L16_T32", "volume": "16x32", "seed": 2026050102},
        {"label": "L24_T48", "volume": "24x48", "seed": 2026050103},
    ]
    masses = "0.45,0.75,1.05"
    source_shifts = "-0.01,0.0,0.01"
    scalar_two_point_modes = "0,0,0;1,0,0;0,1,0;0,0,1"
    scalar_two_point_noises = 16
    therm = 1000
    measurements = 1000
    separation = 20
    engine = "numba"

    commands = []
    for row in volumes:
        output = f"outputs/yt_pr230_fh_lsz_production_{row['label']}_2026-05-01.json"
        command = shell_join(
            [
                "python3",
                "scripts/yt_direct_lattice_correlator_production.py",
                "--volumes",
                row["volume"],
                "--masses",
                masses,
                "--therm",
                str(therm),
                "--measurements",
                str(measurements),
                "--separation",
                str(separation),
                "--engine",
                engine,
                "--scalar-source-shifts",
                source_shifts,
                "--scalar-two-point-modes",
                f"'{scalar_two_point_modes}'",
                "--scalar-two-point-noises",
                str(scalar_two_point_noises),
                "--seed",
                str(row["seed"]),
                "--output",
                output,
            ]
        )
        commands.append(
            {
                "label": row["label"],
                "volume": row["volume"],
                "seed": row["seed"],
                "output": output,
                "command": command,
                "expected_certificate_status": "production evidence only after successful run, fit, pole/LSZ analysis, and audit",
            }
        )

    postprocess_requirements = [
        "verify every production certificate has no reduced-scope/cold-pilot phase flag",
        "fit E_top(s) with common-ensemble correlated finite differences",
        "fit same-source Gamma_ss(q) and derive dGamma_ss/dp^2 at an isolated pole",
        "apply finite-volume, IR, and zero-mode limiting theorem or include it in the production analysis",
        "only then run a retained-proposal certificate; do not update CLAIMS_TABLE directly",
    ]
    projected_hours = float(resource["projection"]["joint_mass_scaled_hours"])

    report("protocol-loaded", PROTOCOL.exists() and protocol.get("proposal_allowed") is False, str(PROTOCOL.relative_to(ROOT)))
    report("resource-loaded", RESOURCE.exists() and resource.get("proposal_allowed") is False, str(RESOURCE.relative_to(ROOT)))
    report("harness-loaded", HARNESS.exists() and harness.get("proposal_allowed") is False, str(HARNESS.relative_to(ROOT)))
    report("three-volume-manifest", len(commands) == 3, f"commands={len(commands)}")
    report(
        "commands-include-fh-and-lsz-observables",
        all("--scalar-source-shifts" in item["command"] and "--scalar-two-point-modes" in item["command"] for item in commands),
        "all commands include source shifts and same-source scalar two-point modes",
    )
    report("production-cost-not-foreground", projected_hours > 1000.0, f"joint_mass_scaled_hours={projected_hours:.2f}")
    report("postprocess-gates-present", len(postprocess_requirements) == 5, f"gates={len(postprocess_requirements)}")
    report("not-retained-closure", True, "manifest is launch planning, not production data")

    result = {
        "actual_current_surface_status": "bounded-support / joint FH-LSZ production manifest",
        "verdict": (
            "The joint FH/LSZ production route now has exact launch commands "
            "for the three strict volumes, including common-ensemble scalar "
            "source shifts and same-source scalar two-point modes.  This is a "
            "resumable production manifest only.  It supplies no measurements, "
            "no pole derivative, and no retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A command manifest is not production evidence and does not derive kappa_s.",
        "parent_certificates": [
            str(PROTOCOL.relative_to(ROOT)),
            str(RESOURCE.relative_to(ROOT)),
            str(HARNESS.relative_to(ROOT)),
        ],
        "manifest_only": True,
        "production_parameters": {
            "masses": masses,
            "scalar_source_shifts": source_shifts,
            "scalar_two_point_modes": scalar_two_point_modes,
            "scalar_two_point_noises": scalar_two_point_noises,
            "thermalization_sweeps": therm,
            "saved_configurations": measurements,
            "measurement_separation_sweeps": separation,
            "engine": engine,
            "projected_joint_mass_scaled_hours": projected_hours,
        },
        "commands": commands,
        "postprocess_requirements": postprocess_requirements,
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
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
