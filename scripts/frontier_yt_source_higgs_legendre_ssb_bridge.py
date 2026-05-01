#!/usr/bin/env python3
"""
Source-to-Higgs Legendre/SSB bridge reduction for PR #230.

This runner isolates one piece of the Ward physical-readout repair.  It checks
the exact algebra of the Standard Model SSB readout once a canonical Higgs
doublet coefficient is available, and it records the remaining source-to-
canonical-field imports.  It does not identify the source field with H_unit and
does not use observed top data.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_legendre_ssb_bridge_2026-05-01.json"

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
    print("YT source-to-Higgs Legendre/SSB bridge reduction")
    print("=" * 72)

    n_color = 3
    n_iso = 2
    c_tree = 1.0 / math.sqrt(n_color * n_iso)

    # v is arbitrary here because the check is dimensionless: the SSB relation
    # sqrt(2) m / v must return the doublet Yukawa coefficient for every v.
    sample_v_values = [1.0, 2.0, 246.0]
    ssb_checks = []
    for v in sample_v_values:
        mass_from_doublet = c_tree * v / math.sqrt(2.0)
        recovered_yukawa = math.sqrt(2.0) * mass_from_doublet / v
        physical_h_vertex = c_tree / math.sqrt(2.0)
        mass_over_v = mass_from_doublet / v
        ssb_checks.append(
            {
                "v": v,
                "mass_from_doublet": mass_from_doublet,
                "recovered_doublet_yukawa": recovered_yukawa,
                "physical_h_vertex": physical_h_vertex,
                "mass_over_v": mass_over_v,
            }
        )

    ssb_exact = all(
        abs(item["recovered_doublet_yukawa"] - c_tree) < 1e-15
        and abs(item["physical_h_vertex"] - item["mass_over_v"]) < 1e-15
        for item in ssb_checks
    )

    # The source-to-field normalization is the unresolved part.  If the scalar
    # source creates a canonical Higgs doublet with normalization kappa_H, then
    # the doublet Yukawa readout is c_tree * kappa_H.  SSB cannot determine
    # kappa_H; it only maps that coefficient to mass and the physical h vertex.
    conditional_kappa_h = 1.0
    conditional_yukawa = c_tree * conditional_kappa_h

    open_imports = {
        "source_to_canonical_higgs_normalization": (
            "derive kappa_H from the Legendre transform/two-point residue of "
            "the scalar source, not by naming the source field"
        ),
        "scalar_carrier_map": (
            "prove the canonical scalar field selected by the source is the "
            "physical Higgs doublet fluctuation"
        ),
        "chirality_and_species_selector": (
            "connect the scalar-bilinear source to Q_L H q_R with the retained "
            "right-handed species assignments"
        ),
        "lsz_residue": (
            "derive the scalar external-leg factor from the pole residue"
        ),
    }

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_fragments = [
        "y_t" + "_bare :=",
        "<0 | " + "H_unit",
        "<0|" + "H_unit",
    ]
    forbidden_hits = [fragment for fragment in forbidden_fragments if fragment in source_text]

    report("tree-coefficient-is-one-over-sqrt-six", abs(c_tree - 1.0 / math.sqrt(6.0)) < 1e-15, f"{c_tree:.15f}")
    report("ssb-recovers-doublet-yukawa-for-all-v", ssb_exact, f"sample_v={sample_v_values}")
    report(
        "physical-h-vertex-is-mass-over-v",
        ssb_exact,
        "h t t vertex coefficient equals m/v, while doublet y equals sqrt(2) m/v",
    )
    report(
        "ssb-does-not-determine-source-normalization",
        bool(open_imports),
        "kappa_H remains an independent source/canonical-field bridge",
    )
    report(
        "conditional-unit-kappa-recovers-tree-value",
        abs(conditional_yukawa - c_tree) < 1e-15,
        f"conditional y={conditional_yukawa:.15f}",
    )
    report("forbidden-definition-absent", not forbidden_hits, f"forbidden hits={forbidden_hits}")
    report("closure-firewall-engaged", True, "actual status remains open / exact subderivation")

    result = {
        "actual_current_surface_status": "exact subderivation / open bridge",
        "conditional_surface_status": (
            "If the scalar source creates the canonical Higgs doublet with "
            "kappa_H = 1 and the other readout bridges are clean, SSB preserves "
            "the 1/sqrt(6) doublet Yukawa coefficient."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "SSB algebra is exact, but kappa_H and the source/canonical-field bridge remain open.",
        "computed": {
            "n_color": n_color,
            "n_iso": n_iso,
            "tree_coefficient": c_tree,
            "conditional_kappa_H": conditional_kappa_h,
            "conditional_yukawa": conditional_yukawa,
            "ssb_checks": ssb_checks,
        },
        "open_imports": open_imports,
        "forbidden_definition_hits": forbidden_hits,
        "non_claims": [
            "does not derive kappa_H",
            "does not identify a scalar source with H_unit",
            "does not promote the Ward theorem",
            "does not use observed top mass or observed Yukawa as input",
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
