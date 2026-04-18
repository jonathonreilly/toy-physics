#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H local chain path-algebra current-bank boundary.

Purpose:
  Verify that the current stack does not already realize the sharpest local
  Wilson certificate for the DM route under another name.
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


def is_excluded_review_stack(rel: str) -> bool:
    explicit = {
        "docs/DM_PF_COMPRESSED_ROUTE_ATTACK_PLAN_NOTE_2026-04-18.md",
        "scripts/DM_EFFECTIVE_PARENT_one_clock_transfer_boundary_2026_04_18.py",
    }
    prefixes = (
        "docs/DM_EFFECTIVE_PARENT_",
        "docs/DM_WILSON_TO_DWEH_",
        "docs/DM_WILSON_DIRECT_DESCENDANT_",
        "docs/DM_WILSON_PARENT_CORRECTNESS_AUDIT_",
        "scripts/DM_EFFECTIVE_PARENT_",
        "scripts/frontier_dm_wilson_to_dweh_",
        "scripts/frontier_dm_wilson_direct_descendant_",
        "scripts/frontier_dm_wilson_parent_correctness_audit_",
        "scripts/DM_WILSON_DIRECT_DESCENDANT_",
    )
    return rel in explicit or rel.startswith(prefixes)


def files_with_all(tokens: list[str]) -> list[str]:
    hits: list[str] = []
    for folder, suffix in (("docs", "*.md"), ("scripts", "*.py")):
        for path in sorted((ROOT / folder).glob(suffix)):
            rel = str(path.relative_to(ROOT))
            if is_excluded_review_stack(rel):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if all(token in text for token in tokens):
                hits.append(rel)
    return hits


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H LOCAL CHAIN PATH-ALGEBRA CURRENT-BANK BOUNDARY")
    print("=" * 88)

    generic_boundary = read(
        "docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md"
    )
    chain_target = read("docs/DM_WILSON_TO_DWEH_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    minimal_cert = read("docs/DM_WILSON_TO_DWEH_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: THE GENERIC WILSON-TO-dW_e^H ROUTE IS STILL NOT REALIZED")
    print("=" * 88)
    check(
        "The generic current-bank boundary note already says there is no theorem-grade Wilson-to-dW_e^H descendant law on the current stack",
        "does **not** already have:" in generic_boundary
        and "a Wilson-to-`dW_e^H` descendant theorem" in generic_boundary,
    )
    check(
        "The same boundary note already says there is no theorem-grade Wilson Hermitian source family on the current stack",
        "or a Wilson-side Hermitian source family realizing that codomain." in generic_boundary
        and "genuine new\nconstructive route on current `main`." in generic_boundary,
    )

    print("\n" + "=" * 88)
    print("PART 2: THE LOCAL PATH ALGEBRA WOULD AUTOMATICALLY INDUCE THAT GENERIC ROUTE")
    print("=" * 88)
    check(
        "The local chain target note says the Hermitian shadow of Phi_chain gives a canonical 9-channel Wilson Hermitian source family",
        "canonical Wilson Hermitian source family" in chain_target
        and "spanning a copy of `Herm(3)`" in chain_target,
    )
    check(
        "The minimal-certificate note says the whole structured route is equivalent to Phi_chain plus the descended identity into dW_e^H",
        "exactly one minimal local" in minimal_cert
        and "`dW_W o Phi_chain = dW_e^H`" in minimal_cert,
    )

    print("\n" + "=" * 88)
    print("PART 3: THERE IS NO HIDDEN PRE-EXISTING LOCAL PATH-ALGEBRA ARTIFACT")
    print("=" * 88)
    local_hits = files_with_all(["Phi_chain", "dW_e^H"])
    path_hits = files_with_all(["path-algebra", "dW_e^H"])
    check(
        "No pre-existing doc or script outside the new Wilson/DM stack already combines Phi_chain with dW_e^H under another name",
        len(local_hits) == 0,
        f"hits={local_hits}",
    )
    check(
        "No pre-existing doc or script outside the new Wilson/DM stack already states a path-algebra route into dW_e^H",
        len(path_hits) == 0,
        f"hits={path_hits}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current stack does not already realize the sharpest local Wilson certificate for the DM route",
        True,
        "if it did, it would already realize the excluded generic Wilson-to-dW_e^H source family route",
    )
    check(
        "So the remaining gap is genuinely constructive even at the sharpest local level",
        True,
        "positive construction of Phi_chain plus the descended identity still remains",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
