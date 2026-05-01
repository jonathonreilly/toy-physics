#!/usr/bin/env python3
"""
PR #230 source-to-Higgs / LSZ closure attempt.

This is the explicit attempt to close the narrowed PR #230 blocker.  It checks
whether any allowed current-surface premise fixes the scalar source
normalization kappa_s after the source-reparametrization no-go and EW/Higgs
import audit.  The result is an exact blocker map, not retained closure.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"

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
    print("PR #230 source-to-Higgs / LSZ closure attempt")
    print("=" * 72)

    candidates = [
        {
            "premise": "logdet additive scalar generator",
            "allowed": True,
            "fixes_kappa_s": False,
            "reason": "fixes source-response functional form but remains covariant under source coordinate rescaling",
        },
        {
            "premise": "SSB relation m = y v / sqrt(2)",
            "allowed": True,
            "fixes_kappa_s": False,
            "reason": "valid after canonical Higgs field is supplied; does not map lattice source s to h",
        },
        {
            "premise": "EW Higgs gauge-mass diagonalization",
            "allowed": False,
            "fixes_kappa_s": False,
            "reason": "structural note assumes canonical |D H|^2 and is proposed/unaudited; no source bridge",
        },
        {
            "premise": "SM one-Higgs gauge selection",
            "allowed": False,
            "fixes_kappa_s": False,
            "reason": "selects monomial pattern but explicitly leaves Yukawa matrices free",
        },
        {
            "premise": "same-1PI / four-fermion product",
            "allowed": True,
            "fixes_kappa_s": False,
            "reason": "fixes y^2 D_phi only; invariant under y -> kappa y, D_phi -> D_phi/kappa^2",
        },
        {
            "premise": "Feynman-Hellmann dE/ds response",
            "allowed": True,
            "fixes_kappa_s": False,
            "reason": "observable slope is with respect to the lattice source coordinate s",
        },
        {
            "premise": "R_conn / color projection",
            "allowed": False,
            "fixes_kappa_s": False,
            "reason": "audited conditional and not a scalar source-to-Higgs normalization theorem",
        },
        {
            "premise": "H_unit matrix element",
            "allowed": False,
            "fixes_kappa_s": False,
            "reason": "forbidden audited-renaming route",
        },
        {
            "premise": "observed top mass or observed y_t",
            "allowed": False,
            "fixes_kappa_s": False,
            "reason": "external comparator cannot be proof selector",
        },
    ]

    allowed_candidates = [c for c in candidates if c["allowed"]]
    allowed_closers = [c for c in allowed_candidates if c["fixes_kappa_s"]]
    forbidden_closers = [c for c in candidates if not c["allowed"] and c["fixes_kappa_s"]]
    open_required_theorem = {
        "name": "source-to-canonical-Higgs LSZ theorem",
        "must_prove": [
            "the scalar source creates an isolated physical Higgs-channel pole",
            "the pole residue / inverse-propagator derivative fixes kappa_s",
            "the source field matches the canonical kinetic normalization used by v",
            "the proof does not use H_unit, observed top/y_t, alpha_LM, plaquette/u0, or reduced pilot data",
        ],
    }

    report("allowed-premise-list-nonempty", len(allowed_candidates) >= 4, f"allowed={len(allowed_candidates)}")
    report("no-allowed-premise-fixes-kappa", len(allowed_closers) == 0, f"allowed_closers={allowed_closers}")
    report("forbidden-shortcuts-listed", any(not c["allowed"] for c in candidates), "forbidden routes are explicit")
    report("h-unit-forbidden", any(c["premise"] == "H_unit matrix element" and not c["allowed"] for c in candidates), "H_unit route remains blocked")
    report("observed-values-forbidden", any(c["premise"] == "observed top mass or observed y_t" and not c["allowed"] for c in candidates), "observed targets remain comparators only")
    report("required-theorem-named", len(open_required_theorem["must_prove"]) == 4, open_required_theorem["name"])
    report("not-retained-closure", True, "closure attempt exposes open LSZ/source-normalization theorem")

    result = {
        "actual_current_surface_status": "open / source-to-Higgs LSZ closure attempt blocked",
        "verdict": (
            "No allowed current-surface premise fixes the scalar source "
            "normalization kappa_s.  The logdet source generator, SSB identity, "
            "same-1PI product, and Feynman-Hellmann response are all useful but "
            "source-reparametrization covariant.  Existing EW/Higgs structural "
            "notes, R_conn/color projection, H_unit, and observed targets cannot "
            "be used as clean proof inputs for this bridge.  PR #230 retained "
            "closure still requires the named source-to-canonical-Higgs LSZ "
            "theorem or direct production physical-response evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source-to-canonical-Higgs / scalar LSZ theorem remains open.",
        "candidates": candidates,
        "allowed_closers": allowed_closers,
        "forbidden_closers": forbidden_closers,
        "required_open_theorem": open_required_theorem,
        "strict_non_claims": [
            "does not claim retained closure",
            "does not demote direct production route",
            "does not use H_unit matrix-element readout",
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
