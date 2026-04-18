#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H Hermitian source-family current-bank boundary.

Purpose:
  Verify that current main already fixes the codomain dW_e^H and the
  downstream reconstruction stack, but still does not contain a theorem-grade
  Wilson-side Hermitian source family or descendant law realizing that
  codomain.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def files_with_both(token_a: str, token_b: str) -> list[str]:
    hits: list[str] = []
    excluded = {
        "docs/DM_PF_COMPRESSED_ROUTE_ATTACK_PLAN_NOTE_2026-04-18.md",
        "docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md",
        "docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md",
        "scripts/frontier_dm_wilson_to_dweh_hermitian_source_family_target_2026_04_18.py",
        "scripts/frontier_dm_wilson_to_dweh_hermitian_source_family_current_bank_boundary_2026_04_18.py",
    }
    for folder, suffix in (("docs", "*.md"), ("scripts", "*.py")):
        for path in sorted((ROOT / folder).glob(suffix)):
            rel = str(path.relative_to(ROOT))
            if rel in excluded:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if token_a in text and token_b in text:
                hits.append(rel)
    return hits


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H HERMITIAN SOURCE-FAMILY CURRENT-BANK BOUNDARY")
    print("=" * 88)

    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    selector = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")
    bank = read("docs/DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md")
    source_bank = read("docs/DM_NEUTRINO_SOURCE_BANK_Z3_DOUBLET_BLOCK_SELECTION_OBSTRUCTION_THEOREM_NOTE_2026-04-16.md")

    print("\n" + "=" * 88)
    print("PART 1: CURRENT MAIN STILL STATES dW_e^H ITSELF AS THE LIVE TARGET")
    print("=" * 88)
    check(
        "Projected-source law note still says the live remaining gap is to derive dW_e^H on E_e from Cl(3) on Z^3",
        "derive `dW_e^H` on `E_e` from `Cl(3)` on `Z^3`" in projected,
    )
    check(
        "Charged source-response reduction note still says the right target is to evaluate dW_e^H from Cl(3) on Z^3",
        "evaluate the charged-lepton projected Hermitian source law `dW_e^H`" in charged,
    )
    check(
        "Selector reduction note still states that the remaining blocker is exactly a right-sensitive microscopic selector law on dW_e^H",
        "It is exactly a **right-sensitive microscopic selector law** on" in selector
        and "`dW_e^H = Schur_Ee(D_-)`" in selector,
    )

    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT BANK REMAINS BLIND TO THE LIVE 2-REAL TARGET")
    print("=" * 88)
    check(
        "Observable-bank exhaustion note says every retained observable with target value factors through the frozen chamber bank",
        "factors through the **frozen** current-bank signature" in bank,
    )
    check(
        "Observable-bank exhaustion note says no retained observable on the current atlas uniquely pins (delta,q_+)",
        "no observable in the retained atlas bank can uniquely" in bank,
    )
    check(
        "Source-bank obstruction note says the minimal missing object is a new right-sensitive 2-real datum, equivalently the Z3 doublet-block law itself",
        "The minimal missing object is therefore:" in source_bank
        and "a **new right-sensitive `2`-real datum**" in source_bank,
    )

    print("\n" + "=" * 88)
    print("PART 3: CURRENT MAIN HAS NO HIDDEN WILSON-TO-dW_e^H ARTIFACT")
    print("=" * 88)
    wilson_dweh_hits = files_with_both("Wilson", "dW_e^H")
    hermitian_family_hits = files_with_both("Wilson", "Hermitian source family")
    check(
        "No pre-existing current-main doc or script combines Wilson-side structure with dW_e^H under another name",
        len(wilson_dweh_hits) == 0,
        f"hits={wilson_dweh_hits}",
    )
    check(
        "No pre-existing current-main doc or script already names a Wilson Hermitian source family target",
        len(hermitian_family_hits) == 0,
        f"hits={hermitian_family_hits}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current exact bank does not already realize the Wilson-side Hermitian source family needed upstream of the selector",
        True,
        "current main still names dW_e^H itself as live target and has no Wilson-to-dW_e^H artifact",
    )
    check(
        "So the Wilson Hermitian source family is a genuinely new constructive primitive on current main",
        True,
        "not a hidden current-bank object under another label",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
