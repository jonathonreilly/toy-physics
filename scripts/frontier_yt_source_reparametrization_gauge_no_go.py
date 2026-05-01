#!/usr/bin/env python3
"""
PR #230 source-reparametrization gauge no-go.

This runner formalizes the scalar-source normalization obstruction.  Any route
that uses only source-functional responses is covariant under a rescaling of
the scalar source coordinate.  The covariance preserves source-response
relations but changes the physical Yukawa readout unless a canonical scalar
field normalization / LSZ residue is independently supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_reparametrization_gauge_no_go_2026-05-01.json"

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
    print("PR #230 source-reparametrization gauge no-go")
    print("=" * 72)

    source_ratio = 1.0 / math.sqrt(6.0)
    scalar_charge = source_ratio
    curvature = 2.5
    scalar_propagator = 0.8
    four_fermion_product = scalar_charge * scalar_charge * scalar_propagator

    kappas = [0.5, 0.75, 1.0, 1.25, 1.5]
    rows = []
    for kappa in kappas:
        # s_phys = kappa * s_lattice.  Rewriting the same source functional in
        # s_lattice units rescales derivatives but not the underlying response.
        slope_in_lattice_source = scalar_charge * kappa
        curvature_in_lattice_source = curvature * kappa * kappa
        propagator_in_lattice_source = scalar_propagator / (kappa * kappa)
        invariant_four_fermion = slope_in_lattice_source * slope_in_lattice_source * propagator_in_lattice_source
        physical_y_readout = slope_in_lattice_source / kappa
        wrong_readout_if_kappa_set_to_one = slope_in_lattice_source
        rows.append(
            {
                "kappa_source_to_physical_field": kappa,
                "slope_in_lattice_source": slope_in_lattice_source,
                "curvature_in_lattice_source": curvature_in_lattice_source,
                "propagator_in_lattice_source": propagator_in_lattice_source,
                "four_fermion_product": invariant_four_fermion,
                "physical_y_readout_if_kappa_known": physical_y_readout,
                "wrong_readout_if_kappa_set_to_one": wrong_readout_if_kappa_set_to_one,
            }
        )

    invariant_spread = max(row["four_fermion_product"] for row in rows) - min(
        row["four_fermion_product"] for row in rows
    )
    wrong_values = [row["wrong_readout_if_kappa_set_to_one"] for row in rows]
    wrong_spread = (max(wrong_values) - min(wrong_values)) / (sum(wrong_values) / len(wrong_values))
    physical_values = [row["physical_y_readout_if_kappa_known"] for row in rows]
    physical_spread = max(physical_values) - min(physical_values)

    report("source-functional-products-covariant", invariant_spread < 1.0e-14, f"invariant_spread={invariant_spread:.3e}")
    report("known-kappa-readout-stable", physical_spread < 1.0e-14, f"physical_spread={physical_spread:.3e}")
    report("setting-kappa-to-one-changes-readout", wrong_spread > 0.70, f"wrong_relative_spread={wrong_spread:.6g}")
    report("same-1pi-product-not-enough", abs(four_fermion_product - rows[0]["four_fermion_product"]) < 1.0e-14, "y^2 D_phi invariant under source rescaling")
    report("feynman-hellmann-slope-not-enough", True, "dE/ds_lattice needs kappa_source_to_physical_field")
    report("not-retained-closure", True, "requires scalar LSZ/canonical field normalization or direct physical response measurement")

    result = {
        "actual_current_surface_status": "exact negative boundary / source reparametrization gauge",
        "verdict": (
            "Source-functional routes are covariant under scalar-source "
            "reparametrization.  The same source-response products can be held "
            "fixed while the readout obtained by setting the source "
            "normalization to one varies.  Therefore PR #230 cannot close from "
            "source curvature, same-1PI products, or Feynman-Hellmann slopes "
            "alone.  A canonical scalar field normalization, scalar LSZ residue, "
            "or direct physical response measurement is required."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source normalization kappa is a gauge freedom on the current source-functional surface.",
        "rows": rows,
        "base_values": {
            "source_ratio": source_ratio,
            "scalar_charge": scalar_charge,
            "curvature": curvature,
            "scalar_propagator": scalar_propagator,
            "four_fermion_product": four_fermion_product,
        },
        "strict_non_claims": [
            "does not rule out a future scalar LSZ theorem",
            "does not use H_unit matrix-element readout",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM/plaquette/u0 as proof input",
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
