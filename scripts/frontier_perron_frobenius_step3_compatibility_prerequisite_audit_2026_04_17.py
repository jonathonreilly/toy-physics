#!/usr/bin/env python3
"""
Prerequisite audit for the eventual step-3 PF compatibility theorem.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP3_COMPATIBILITY_PREREQUISITE_AUDIT_NOTE_2026-04-17.md")
    parent = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")
    step2 = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")
    global_closure = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")
    three_step = read("docs/PERRON_FROBENIUS_THREE_STEP_GLOBAL_PROGRAM_BOUNDARY_NOTE_2026-04-17.md")
    external = read("docs/PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md")
    all_paths = read("docs/PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md")

    readiness = {
        "global_parent_theorem": False,
        "pmns_descendant_law": False,
        "plaquette_fixed_pf_data": False,
        "matched_step3_positive_map_hypotheses": False,
    }

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-3 COMPATIBILITY PREREQUISITE AUDIT")
    print("=" * 108)
    print()
    print("Current readiness matrix")
    for name, ready in readiness.items():
        label = name.replace("_", " ")
        print(f"  - {label:<43} : {'ready' if ready else 'not ready'}")
    print()

    check(
        "Audit note explicitly types step 3 as a four-prerequisite problem",
        "four distinct prerequisites are closed" in note
        and "Common parent object." in note
        and "Sector descendant laws." in note
        and "Fixed sector PF states." in note
        and "Matched step-3 hypotheses." in note,
        bucket="SUPPORT",
    )
    check(
        "Sector-local PF exactness already exists and is correctly separated from global common-state compatibility",
        "sector-local PF / dominant-mode theorems already exist" in note
        and "sector-local PF selection: yes;" in global_closure
        and "global sole-axiom PF selector: no." in global_closure,
        bucket="SUPPORT",
    )

    check(
        "A genuine step-3 theorem still lacks a global parent object even though the Wilson gauge surface already has a real parent object",
        "step 1 is closed only on the Wilson gauge surface" in parent
        and "does **not** yet close step 1 globally" in parent
        and "item 1 is only partially closed" in note,
        detail="the parent object exists locally on the Wilson surface, but the global parent theorem is not yet in hand",
    )
    check(
        "The PMNS-side step-3 prerequisite is still missing because there is no Wilson-to-PMNS descendant/intertwiner theorem",
        "The missing theorem is specifically:" in step2
        and "Wilson-to-PMNS" in step2
        and "descendant / intertwiner theorem" in step2
        and "cannot honestly advance from step 2 to step" in step2
        and "item 2 is still open on the PMNS side" in note,
        detail="common-state comparison remains blocked by missing cross-sector provenance",
    )
    check(
        "The plaquette-side step-3 prerequisite is still missing because the framework-point beta-side PF data are not determined",
        "plaquette framework-point beta-side vector `v_6`" in global_closure
        and "is still not" in global_closure
        and "item 3 is still open on the plaquette side" in note
        and "operator-side / Perron data are not yet determined" in note
        and "operator-plus-projection" in global_closure,
        detail="without fixed plaquette framework-point data there is no single common-state object to compare",
    )
    check(
        "Positive-map PF theory is only a step-3 template after descendant laws are in hand and common-state comparison is well-posed",
        "step-3 template for PF-type spectral compatibility of positive maps" in external
        and "descendant laws are actually in hand" in external
        and "common-state comparison is mathematically well-posed" in all_paths
        and "item 4 therefore remains unavailable too" in note,
        detail="Evans-Hoegh-Krohn is a hypothesis template, not a plug-in closure for the current bank",
    )
    check(
        "Therefore step 3 is not merely unproved; it is not yet theorem-ready on exact common-state data",
        "finish step 2, not step 3." in three_step
        and "common parent PF state whose sector descendants can be compared" in three_step
        and "does **not** yet support an honest step-3 theorem" in note
        and "audit hypotheses, not pretend closure" in note,
        detail="the compatibility scout front should currently audit prerequisites rather than claim closure",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
