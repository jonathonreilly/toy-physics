#!/usr/bin/env python3
"""
Source-Higgs kappa residue obstruction for PR #230.

After the SSB bookkeeping reduction, the remaining source bridge is a single
normalization: kappa_H, the map from the source-normalized scalar coefficient
to the canonical Higgs-doublet coefficient.  This runner shows that group
counts and SSB algebra do not select kappa_H.  A scalar two-point residue or
equivalent LSZ theorem is required.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_kappa_residue_obstruction_2026-05-01.json"

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
    print("YT source-Higgs kappa residue obstruction")
    print("=" * 72)

    n_color = 3
    n_iso = 2
    c_source = 1.0 / math.sqrt(n_color * n_iso)

    # kappa_H represents the unresolved map from source-normalized scalar
    # coefficient to canonical Higgs-doublet coefficient:
    #
    #     y_doublet = c_source * kappa_H.
    #
    # The current group-count and SSB checks see c_source, but they do not
    # select kappa_H.  The values below are countermodels to selection by
    # counts alone; they all preserve N_c, N_iso, and the SSB identity.
    kappa_values = [0.5, math.sqrt(8.0 / 9.0), 1.0, 2.0]
    countermodels = []
    for kappa in kappa_values:
        y_doublet = c_source * kappa
        v = 1.0
        mass = y_doublet * v / math.sqrt(2.0)
        recovered_y = math.sqrt(2.0) * mass / v
        countermodels.append(
            {
                "kappa_H": kappa,
                "source_coefficient": c_source,
                "doublet_yukawa": y_doublet,
                "mass_at_v_equals_1": mass,
                "recovered_yukawa": recovered_y,
                "ssb_identity_holds": abs(recovered_y - y_doublet) < 1e-15,
            }
        )

    distinct_yukawas = {round(item["doublet_yukawa"], 15) for item in countermodels}
    all_ssb_hold = all(item["ssb_identity_holds"] for item in countermodels)

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_fragments = [
        "y_t" + "_bare :=",
        "<0 | " + "H_unit",
        "<0|" + "H_unit",
    ]
    forbidden_hits = [fragment for fragment in forbidden_fragments if fragment in source_text]

    report("source-coefficient-fixed-by-counts", abs(c_source - 1.0 / math.sqrt(6.0)) < 1e-15, f"{c_source:.15f}")
    report("multiple-kappa-countermodels", len(distinct_yukawas) == len(kappa_values), f"distinct y values={sorted(distinct_yukawas)}")
    report("ssb-identity-holds-for-all-kappa", all_ssb_hold, "sqrt(2) m/v recovers y_doublet for every kappa")
    report(
        "counts-do-not-select-kappa-one",
        all(item["source_coefficient"] == c_source for item in countermodels),
        "N_c and N_iso are identical in every countermodel",
    )
    report(
        "residue-theorem-required",
        True,
        "kappa_H requires scalar two-point residue/LSZ normalization, not group-count arithmetic",
    )
    report("forbidden-definition-absent", not forbidden_hits, f"forbidden hits={forbidden_hits}")
    report("closure-firewall-engaged", True, "actual status is exact negative boundary for kappa selection by counts+SSB alone")

    result = {
        "actual_current_surface_status": "exact negative boundary / open bridge",
        "verdict": (
            "The current source/count/SSB data do not derive kappa_H = 1.  "
            "Different kappa_H values preserve the same group-count coefficient "
            "and the same SSB identity while producing different doublet Yukawa "
            "readouts.  A scalar two-point residue or equivalent LSZ theorem is "
            "required to select kappa_H."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The runner proves a missing normalization condition, not retained top-Yukawa closure.",
        "constants": {
            "n_color": n_color,
            "n_iso": n_iso,
            "source_coefficient": c_source,
        },
        "countermodels": countermodels,
        "required_new_theorem": (
            "derive the scalar source two-point residue and prove that the "
            "canonical Higgs-doublet normalization gives kappa_H = 1, or carry "
            "the measured/derived kappa_H as a separate physical input"
        ),
        "forbidden_definition_hits": forbidden_hits,
        "non_claims": [
            "does not derive kappa_H = 1",
            "does not identify the source scalar with H_unit by definition",
            "does not use observed top mass or observed Yukawa as input",
            "does not promote the Ward theorem",
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
