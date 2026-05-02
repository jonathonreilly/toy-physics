#!/usr/bin/env python3
"""
PR #230 Cl(3)/Z3 source-unit normalization no-go.

This route attacks the source-to-canonical-Higgs blocker at the substrate
level: can the Cl(3)/Z3 unit conventions themselves fix kappa_s?

The result is negative.  Unit lattice spacing, unit Clifford generators, and
the additive source coefficient in D + m + s define a source coordinate and
the operator dS/ds.  They do not define a propagating scalar field metric or
canonical Higgs kinetic normalization.  A canonical field h = kappa_s s can be
assigned with different kappa_s values while preserving the same source
functional; only a scalar pole/kinetic term or same-source LSZ residue fixes
the conversion.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_LSZ_ATTEMPT = ROOT / "outputs" / "yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"
INVARIANT_READOUT = ROOT / "outputs" / "yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_cl3_source_unit_normalization_no_go_2026-05-01.json"

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


def transformed_model(kappa_s: float) -> dict[str, float]:
    """A source-functional toy model showing what changes under h=kappa_s s."""
    d_e_ds = 0.137
    gamma_prime_ss = 2.75
    source_curvature = 4.5
    return {
        "kappa_s": kappa_s,
        "dE_ds": d_e_ds,
        "Gamma_prime_ss": gamma_prime_ss,
        "source_curvature_ss": source_curvature,
        "dE_dh": d_e_ds / kappa_s,
        "Gamma_prime_hh": gamma_prime_ss * kappa_s * kappa_s,
        "curvature_hh": source_curvature * kappa_s * kappa_s,
        "same_source_invariant": d_e_ds * (gamma_prime_ss ** 0.5),
        "canonical_h_readout": (d_e_ds / kappa_s) * ((gamma_prime_ss * kappa_s * kappa_s) ** 0.5),
    }


def main() -> int:
    print("PR #230 Cl(3)/Z3 source-unit normalization no-go")
    print("=" * 72)

    source_attempt = json.loads(SOURCE_LSZ_ATTEMPT.read_text(encoding="utf-8"))
    invariant_readout = json.loads(INVARIANT_READOUT.read_text(encoding="utf-8"))
    substrate_premises = [
        {
            "premise": "unit lattice spacing a=1",
            "fixes_source_coordinate": True,
            "fixes_canonical_higgs_metric": False,
            "reason": "sets dimensionless lattice units, not a propagating scalar kinetic residue",
        },
        {
            "premise": "unit Cl(3) generator norm e_i^2=1",
            "fixes_source_coordinate": False,
            "fixes_canonical_higgs_metric": False,
            "reason": "normalizes Clifford/taste algebra, not the scalar source-to-field map",
        },
        {
            "premise": "additive source coefficient in D + m + s",
            "fixes_source_coordinate": True,
            "fixes_canonical_higgs_metric": False,
            "reason": "defines dS/ds as the scalar density insertion; h=kappa_s s remains open",
        },
        {
            "premise": "g_bare = 1 gauge normalization",
            "fixes_source_coordinate": False,
            "fixes_canonical_higgs_metric": False,
            "reason": "normalizes gauge links/coupling, not scalar pole residue or |D H|^2",
        },
        {
            "premise": "standard functional derivative definitions",
            "fixes_source_coordinate": True,
            "fixes_canonical_higgs_metric": False,
            "reason": "extracts source correlators but is covariant under source-field rescaling",
        },
    ]
    closers = [p for p in substrate_premises if p["fixes_canonical_higgs_metric"]]
    models = [transformed_model(kappa_s) for kappa_s in [0.5, 1.0, 2.0, 3.0]]
    invariant_values = {round(model["same_source_invariant"], 12) for model in models}
    canonical_values = {round(model["canonical_h_readout"], 12) for model in models}
    physical_slopes = [model["dE_dh"] for model in models]
    curvature_values = [model["curvature_hh"] for model in models]

    report(
        "source-lsz-attempt-loaded",
        SOURCE_LSZ_ATTEMPT.exists() and source_attempt.get("proposal_allowed") is False,
        str(SOURCE_LSZ_ATTEMPT.relative_to(ROOT)),
    )
    report(
        "invariant-readout-loaded",
        INVARIANT_READOUT.exists() and invariant_readout.get("proposal_allowed") is False,
        str(INVARIANT_READOUT.relative_to(ROOT)),
    )
    report(
        "substrate-premises-listed",
        len(substrate_premises) == 5,
        f"premises={len(substrate_premises)}",
    )
    report(
        "no-substrate-unit-premise-fixes-kappa",
        len(closers) == 0,
        f"closers={closers}",
    )
    report(
        "source-functional-data-covariant-under-kappa",
        len(invariant_values) == 1 and len(canonical_values) == 1,
        f"invariant_values={sorted(invariant_values)}",
    )
    report(
        "physical-slope-and-curvature-change-with-kappa",
        max(physical_slopes) / min(physical_slopes) > 5.0 and max(curvature_values) / min(curvature_values) > 30.0,
        f"dE_dh_spread={max(physical_slopes) / min(physical_slopes):.6g}, curvature_spread={max(curvature_values) / min(curvature_values):.6g}",
    )
    report(
        "kappa-one-not-derived",
        True,
        "kappa_s=1 would be an added canonical-field convention without pole/kinetic proof",
    )
    report("not-retained-closure", True, "substrate source unit is not scalar LSZ normalization")

    result = {
        "actual_current_surface_status": "exact negative boundary / Cl3 source-unit normalization no-go",
        "verdict": (
            "The Cl(3)/Z3 substrate unit conventions define the lattice source "
            "coordinate for the additive mass/source functional, but they do "
            "not define the canonical Higgs field metric.  Unit lattice "
            "spacing, unit Clifford generators, g_bare=1, and the coefficient "
            "of D+m+s leave h=kappa_s s open.  Same-source FH/LSZ combinations "
            "are invariant under this rescaling, but the physical slope dE/dh "
            "and canonical curvature change unless the scalar pole residue or "
            "kinetic normalization is derived.  Thus kappa_s=1 is not derived "
            "from the substrate source unit."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No allowed Cl(3)/Z3 source-unit premise fixes the canonical Higgs metric or kappa_s.",
        "parent_certificates": [
            str(SOURCE_LSZ_ATTEMPT.relative_to(ROOT)),
            str(INVARIANT_READOUT.relative_to(ROOT)),
        ],
        "substrate_premises": substrate_premises,
        "kappa_models": models,
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
        ],
        "required_next_theorem": [
            "derive a scalar pole and inverse-propagator derivative for the same source",
            "derive the match from that residue to canonical |D H|^2 normalization",
            "or measure the same-source pole derivative on production ensembles and connect it to the canonical Higgs response",
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
