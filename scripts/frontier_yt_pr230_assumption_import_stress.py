#!/usr/bin/env python3
"""
PR #230 assumption/import stress certificate.

This runner makes the physics-loop assumption exercise executable.  It checks
that the current PR #230 positive-closure routes still separate allowed
substrate inputs from forbidden proof imports, and that no route is allowed to
claim retained top-Yukawa closure while the scalar-LSZ or heavy-matching imports
remain open.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude" / "science" / "physics-loops" / "yt-pr230-ward-physical-readout-20260501"
ASSUMPTIONS = PACK / "ASSUMPTIONS_AND_IMPORTS.md"
OUTPUT = ROOT / "outputs" / "yt_pr230_assumption_import_stress_2026-05-01.json"

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


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 assumption/import stress certificate")
    print("=" * 72)

    text = ASSUMPTIONS.read_text(encoding="utf-8")
    certificates = {
        "campaign": load("outputs/yt_pr230_campaign_status_certificate_2026-05-01.json"),
        "kinetic_matching": load("outputs/yt_heavy_kinetic_matching_obstruction_2026-05-01.json"),
        "momentum_pilot": load("outputs/yt_momentum_pilot_scaling_certificate_2026-05-01.json"),
        "scalar_ir": load("outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json"),
        "projector_norm": load("outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json"),
        "scalar_renormalization_condition_overlap": load(
            "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json"
        ),
        "source_contact_term_scheme": load(
            "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json"
        ),
        "finite_source_shift_derivative_no_go": load(
            "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json"
        ),
    }

    required_terms = [
        "H_unit-to-top matrix-element definition",
        "yt_ward_identity as y_t authority",
        "observed top mass / observed y_t as proof selectors",
        "alpha_LM / plaquette / u0 as load-bearing normalization",
        "c2 = 1 unless derived",
        "Z_match = 1 unless derived",
        "kappa_s = 1 unless derived",
        "source operator overlap",
        "Source contact counterterms",
        "Single finite source-shift radius as a zero-source derivative",
        "Reduced cold-gauge momentum pilots",
    ]
    missing_terms = [term for term in required_terms if term not in text]
    proposal_allowed = [
        name for name, cert in certificates.items() if cert.get("proposal_allowed") is True
    ]

    report("assumption-ledger-present", ASSUMPTIONS.exists(), str(ASSUMPTIONS.relative_to(ROOT)))
    report("refreshed-kinetic-imports-present", "Heavy kinetic-action coefficient `c2`" in text and "Z_match" in text, "c2 and Z_match imports named")
    report("forbidden-imports-explicit", not missing_terms, f"missing={missing_terms}")
    report("all-loaded-certificates-no-fail", all(int(cert.get("fail_count", 0)) == 0 for cert in certificates.values()), f"count={len(certificates)}")
    report("no-route-authorizes-retained-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "kinetic-countermodel-load-bearing",
        "exact negative boundary" in str(certificates["kinetic_matching"].get("actual_current_surface_status")),
        certificates["kinetic_matching"].get("actual_current_surface_status"),
    )
    report(
        "reduced-pilot-not-strict-evidence",
        "bounded-support" in str(certificates["momentum_pilot"].get("actual_current_surface_status")),
        certificates["momentum_pilot"].get("actual_current_surface_status"),
    )
    report(
        "scalar-ladder-imports-remain-open",
        "zero-mode" in str(certificates["scalar_ir"].get("actual_current_surface_status"))
        and "projector" in str(certificates["projector_norm"].get("actual_current_surface_status")),
        "IR/zero-mode and projector normalization obstructions loaded",
    )
    report(
        "canonical-kinetic-normalization-not-source-overlap",
        "renormalization-condition source-overlap no-go"
        in str(certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status")),
        certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status"),
    )
    report(
        "source-contact-terms-not-pole-residue",
        "source contact-term scheme boundary"
        in str(certificates["source_contact_term_scheme"].get("actual_current_surface_status")),
        certificates["source_contact_term_scheme"].get("actual_current_surface_status"),
    )
    report(
        "single-finite-source-radius-not-zero-derivative",
        "finite source-shift slope not zero-source derivative certificate"
        in str(certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status")),
        certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status"),
    )

    result = {
        "actual_current_surface_status": "open / assumption-import stress complete",
        "verdict": (
            "The refreshed PR #230 assumption exercise is explicit: H_unit, "
            "yt_ward_identity, observed top/y_t, alpha_LM/plaquette/u0, "
            "reduced cold pilots, undetermined c2, undetermined Z_match, and "
            "kappa_s = 1 are forbidden as proof shortcuts unless the relevant "
            "normalization or matching theorem is derived.  Canonical Z_h=1 "
            "does not derive the source operator overlap <0|O_s|h>, and source "
            "contact-term schemes do not derive the isolated pole residue.  A "
            "single finite source-shift radius also does not derive the zero-source "
            "Feynman-Hellmann derivative.  No current route "
            "certificate authorizes retained proposal wording.  Positive "
            "closure still requires production evidence plus heavy matching, "
            "or an independent scalar pole/LSZ theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Open scalar-LSZ and heavy-matching imports remain after assumption stress.",
        "checked_certificates": {
            name: cert.get("actual_current_surface_status") for name, cert in certificates.items()
        },
        "missing_forbidden_terms": missing_terms,
        "strict_non_claims": [
            "not a y_t derivation",
            "not a production measurement",
            "does not use observed top mass as calibration",
            "does not define y_t through H_unit matrix elements",
            "does not use yt_ward_identity as y_t authority",
            "does not set kappa_s to one without scalar LSZ/canonical normalization",
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
