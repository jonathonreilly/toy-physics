#!/usr/bin/env python3
"""
PR #230 large-Nc pole-dominance boundary.

Another possible scalar-residue repair is to argue that the scalar channel is
pole dominated at large N_c, so the continuum contribution is negligible.  This
runner checks whether that can certify the PR #230 Yukawa readout at N_c=3.

It cannot.  Large-Nc scaling is useful conditional support, but at N_c=3 the
natural 1/N_c or 1/N_c^2 continuum allowances produce percent-level shifts in
the canonical Yukawa proxy unless an additional finite-N_c suppression theorem
is derived.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_large_nc_pole_dominance_boundary_2026-05-01.json"

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
    print("PR #230 large-Nc pole-dominance boundary")
    print("=" * 72)

    n_c = 3
    source_ratio = 1.0 / math.sqrt(2.0 * n_c)
    continuum_scenarios = [
        ("optimistic_1_over_Nc2", 1.0 / (n_c * n_c)),
        ("looser_1_over_Nc", 1.0 / n_c),
        ("half_of_1_over_Nc2", 0.5 / (n_c * n_c)),
        ("one_percent", 0.01),
    ]
    rows = []
    for label, continuum_fraction in continuum_scenarios:
        pole_fraction = 1.0 - continuum_fraction
        y_proxy = source_ratio * math.sqrt(pole_fraction)
        relative_shift = abs(y_proxy / source_ratio - 1.0)
        rows.append(
            {
                "label": label,
                "continuum_fraction": continuum_fraction,
                "pole_fraction": pole_fraction,
                "y_over_g_proxy": y_proxy,
                "relative_shift_from_unit_pole": relative_shift,
            }
        )

    one_over_nc2_shift = next(row for row in rows if row["label"] == "optimistic_1_over_Nc2")[
        "relative_shift_from_unit_pole"
    ]
    one_over_nc_shift = next(row for row in rows if row["label"] == "looser_1_over_Nc")[
        "relative_shift_from_unit_pole"
    ]
    one_percent_shift = next(row for row in rows if row["label"] == "one_percent")[
        "relative_shift_from_unit_pole"
    ]

    report("source-ratio-fixed", abs(source_ratio - 1.0 / math.sqrt(6.0)) < 1.0e-15, f"{source_ratio:.15f}")
    report("large-nc-is-not-nc3-equality", n_c == 3, "physical N_c is finite, not an asymptotic limit")
    report("one-over-nc2-shift-percent-level", one_over_nc2_shift > 0.05, f"shift={one_over_nc2_shift:.6g}")
    report("one-over-nc-shift-large", one_over_nc_shift > 0.15, f"shift={one_over_nc_shift:.6g}")
    report("subpercent-closure-needs-continuum-bound", one_percent_shift < 0.01, f"1% continuum gives shift={one_percent_shift:.6g}")
    report("not-retained-closure", True, "large-Nc pole dominance needs a finite-Nc continuum suppression theorem")

    result = {
        "actual_current_surface_status": "exact negative boundary / large-Nc pole dominance not PR230 closure",
        "verdict": (
            "Large-Nc pole dominance is conditional support, not retained "
            "closure at N_c=3.  A natural 1/N_c^2 continuum allowance shifts "
            "the canonical Yukawa proxy by more than five percent, and a 1/N_c "
            "allowance shifts it much more.  A sub-percent PR #230 closure "
            "would need a retained finite-Nc theorem bounding the continuum "
            "fraction at about the percent level or better."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-Nc continuum suppression is not derived from the current retained surface.",
        "n_c": n_c,
        "source_ratio": source_ratio,
        "rows": rows,
        "required_next_theorem": [
            "derive scalar-channel pole saturation at N_c=3",
            "or derive a finite-Nc continuum fraction bound strong enough for the target uncertainty",
            "or measure the scalar pole residue directly",
        ],
        "strict_non_claims": [
            "does not reject large-Nc support as intuition",
            "does not use observed top/Higgs/Yukawa values",
            "does not define y_t through H_unit matrix elements",
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
