#!/usr/bin/env python3
"""
PR #230 gauge-VEV source-overlap no-go.

This runner attacks the tempting shortcut that the canonical electroweak VEV
or gauge-boson mass normalization fixes the Cl(3)/Z3 scalar source coordinate.
It does not.  Gauge masses fix the canonical Higgs-field metric after a Higgs
doublet is already identified; they do not fix the overlap between the additive
lattice scalar source s and that canonical field h.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_IMPORT = ROOT / "outputs" / "yt_canonical_scalar_normalization_import_audit_2026-05-01.json"
SOURCE_TO_HIGGS = ROOT / "outputs" / "yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"
CL3_SOURCE_UNIT = ROOT / "outputs" / "yt_cl3_source_unit_normalization_no_go_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_gauge_vev_source_overlap_no_go_2026-05-01.json"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def countermodel(kappa_s: float) -> dict[str, float]:
    v_canonical = 1.0
    g_ew = 1.0
    y_h = 0.8
    m_w = 0.5 * g_ew * v_canonical
    m_top = y_h * v_canonical / math.sqrt(2.0)
    d_e_dh = y_h / math.sqrt(2.0)
    d_e_ds = kappa_s * d_e_dh
    inferred_d_e_dh_if_kappa_set_to_one = d_e_ds
    return {
        "kappa_s": kappa_s,
        "v_canonical": v_canonical,
        "g_ew": g_ew,
        "m_w": m_w,
        "canonical_y_h": y_h,
        "m_top_from_canonical_h": m_top,
        "dE_dh": d_e_dh,
        "dE_ds": d_e_ds,
        "wrong_dE_dh_if_kappa_s_set_to_one": inferred_d_e_dh_if_kappa_set_to_one,
    }


def main() -> int:
    print("PR #230 gauge-VEV source-overlap no-go")
    print("=" * 72)

    canonical_import = load_json(CANONICAL_IMPORT)
    source_to_higgs = load_json(SOURCE_TO_HIGGS)
    cl3_source_unit = load_json(CL3_SOURCE_UNIT)
    models = [countermodel(0.5), countermodel(1.0), countermodel(2.0)]
    same_gauge_sector = len({row["m_w"] for row in models}) == 1 and len({row["v_canonical"] for row in models}) == 1
    different_source_response = len({round(row["dE_ds"], 12) for row in models}) == len(models)
    wrong_readouts = [
        abs(row["wrong_dE_dh_if_kappa_s_set_to_one"] - row["dE_dh"]) for row in models
    ]

    report("canonical-import-audit-loaded", bool(canonical_import), str(CANONICAL_IMPORT.relative_to(ROOT)))
    report("source-to-higgs-closure-loaded", bool(source_to_higgs), str(SOURCE_TO_HIGGS.relative_to(ROOT)))
    report("cl3-source-unit-loaded", bool(cl3_source_unit), str(CL3_SOURCE_UNIT.relative_to(ROOT)))
    report(
        "existing-audits-do-not-close-kappa",
        canonical_import.get("proposal_allowed") is False
        and source_to_higgs.get("proposal_allowed") is False
        and cl3_source_unit.get("proposal_allowed") is False,
        "all parent certificates keep proposal_allowed=false",
    )
    report(
        "countermodels-share-gauge-vev-sector",
        same_gauge_sector,
        f"m_w_values={sorted({row['m_w'] for row in models})}",
    )
    report(
        "countermodels-change-source-response",
        different_source_response,
        f"dE_ds_values={[row['dE_ds'] for row in models]}",
    )
    report(
        "kappa-one-shortcut-would-change-readout",
        max(wrong_readouts) > 0.25,
        f"max_wrong_shift={max(wrong_readouts):.6g}",
    )
    report("not-retained-closure", True, "gauge VEV normalization does not provide source overlap")

    result = {
        "actual_current_surface_status": "exact negative boundary / gauge-VEV source-overlap no-go",
        "verdict": (
            "The canonical electroweak VEV and gauge-boson mass normalization "
            "fix the metric of an already-identified canonical Higgs field h.  "
            "They do not fix the overlap h = kappa_s s between that field and "
            "the additive Cl(3)/Z3 scalar source s.  Countermodels with the same "
            "v, gauge coupling, and m_W but different kappa_s give different "
            "dE/ds and would produce different physical dE/dh if kappa_s were "
            "set to one.  Therefore the VEV/gauge-mass surface cannot replace "
            "a scalar LSZ residue or same-source production pole measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Gauge-sector canonical normalization does not derive the source-to-Higgs overlap kappa_s.",
        "parent_certificates": {
            "canonical_scalar_import": str(CANONICAL_IMPORT.relative_to(ROOT)),
            "source_to_higgs_lsz": str(SOURCE_TO_HIGGS.relative_to(ROOT)),
            "cl3_source_unit": str(CL3_SOURCE_UNIT.relative_to(ROOT)),
        },
        "countermodels": models,
        "strict_non_claims": [
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not set c2 or Z_match to one",
        ],
        "exact_next_action": (
            "Use a same-source scalar pole residue measurement/theorem to fix "
            "kappa_s, or continue the production FH/LSZ route; do not identify "
            "the substrate source with the canonical Higgs field from v alone."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
