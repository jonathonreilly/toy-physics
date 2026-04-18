#!/usr/bin/env python3
"""
Proof-standard boundary for atlas and external-theory use on the PF lane.
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
    note = read("docs/PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md")
    all_paths = read("docs/PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md")
    selection = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")
    parent_boundary = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")
    step2 = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")
    global_closure = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    print("=" * 108)
    print("PERRON-FROBENIUS EXTERNAL-THEORY PROOF STANDARD")
    print("=" * 108)
    print()

    check(
        "Proof-standard note explicitly separates atlas indexing from proof content",
        "Atlas rows are index objects, not proof objects." in note
        and "row itself is never the proof" in note,
        bucket="SUPPORT",
    )
    check(
        "Proof-standard note explicitly separates external templates from in-repo theorem closure",
        "Published mathematics is a hypothesis template, not a plug-in closure." in note
        and "No conclusion may be imported at wider scope than the hypotheses matched" in note,
        bucket="SUPPORT",
    )
    check(
        "Attack-program note already uses outside mathematics at work-order scope rather than as imported closure",
        "do **not** close the repo by themselves" in all_paths
        and "template" in all_paths,
        bucket="SUPPORT",
    )
    check(
        "Current PF boundary already records that the global selector remains negative despite the external theory guidance",
        "positive global PF selector theorem" in global_closure
        and "not derivable yet" in global_closure
        and "missing Wilson-to-PMNS descendant / intertwiner theorem" in selection,
        bucket="SUPPORT",
    )

    check(
        "Atlas rows can be used legitimately as navigation because the underlying theorem rows are present locally",
        "Full taste-cube site-phase / cube-shift intertwiner" in atlas
        and "DM projected-source triplet sign theorem" in atlas
        and "PMNS nontrivial `C_3` current boundary" in atlas,
        detail="the atlas is admissible as an index because the exact local theorem notes exist",
    )
    check(
        "Luescher may guide step 1 but cannot be used as if it already proves the repo's global parent theorem",
        "10.1007/BF01614090" in note
        and "cannot be cited as if it already proves the repo’s global parent" in note,
        detail="external transfer-matrix positivity is a model for the step-1 target, not a repo proof by citation",
    )
    check(
        "Stinespring may guide step 2 but cannot be used as if it already supplies the missing Wilson-to-PMNS descendant law",
        "10.1090/S0002-9939-1955-0069403-4" in note
        and "cannot be cited as if it already gives the missing" in note
        and "Wilson-to-PMNS descendant law" in note,
        detail="compression/dilation is the right form, but the descendant law still has to be proved on repo objects",
    )
    check(
        "Evans-Hoegh-Krohn may guide step 3 but cannot be used before the descendant theorem exists",
        "10.1112/jlms/s2-17.2.345" in note
        and "cannot be cited as if it already gives common-state" in note
        and "compatibility before the descendant theorem exists" in note
        and "positive global PF selector theorem" in global_closure,
        detail="positive-map PF theory belongs only after parent and descendant hypotheses are matched",
    )
    check(
        "The branch already has the right negative guards in place: step 1 remains partial and step 2 remains open",
        "does **not** yet close step 1 globally" in parent_boundary
        and "cross-sector provenance" in step2
        and "not derivable yet" in global_closure,
        detail="the repo is already guarding against the exact hand-wave failure mode",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
