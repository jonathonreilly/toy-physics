#!/usr/bin/env python3
"""
Current-atlas nonselection theorem for minimal PMNS-producing lepton branches.

Question:
  After isolating the exact minimal PMNS-producing branches, does the current
  atlas/package already select one of them or constrain their canonical
  invariants?

Answer:
  No. The current exact bank isolates the branches but does not select among
  them. It contains no retained Higgs-multiplicity selector, no retained
  shared-Higgs Z_3 universality theorem, and no exact bridge constraining the
  canonical seven-quantity data on either minimal branch.

Boundary:
  This is a current-atlas/package theorem only. It does not claim that such a
  selector or bridge can never be derived in future work.
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    print("=" * 88)
    print("PMNS MINIMAL BRANCHES: CURRENT-ATLAS NONSELECTION")
    print("=" * 88)
    print()
    print("Atlas / package inputs reused:")
    print("  - Neutrino Dirac two-Higgs canonical reduction")
    print("  - Charged-lepton two-Higgs canonical reduction")
    print("  - PMNS boundary packet")
    print("  - flavor publication controls and live gate notes")
    print()
    print("Question:")
    print("  Does the current exact bank already select the surviving minimal")
    print("  PMNS-producing branch, or constrain its seven canonical quantities?")

    # Publication-state evolution 2026-04-17 / 2026-04-25:
    # The HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM upgraded q_H = 0
    # to GAUGE (retained), the CKM lane was promoted to retained closure,
    # and the PMNS boundary packet was rewritten as a thin redirect to
    # the live retained-lane packet. The publication-control wording
    # checked by the previous runner ("CKM / quantitative flavor open",
    # "frozen-out exact review packet", "Higgs `Z_3` universality"
    # blocker line) was therefore rotated out. The note's actual claim —
    # branch isolation without selection — is preserved by the live
    # atlas rows tested below, plus the gates-note open lane.
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    gates = read("docs/GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md")

    atlas_lower = atlas.lower()
    has_neutrino_branch = "| Neutrino Dirac two-Higgs canonical reduction |" in atlas
    has_charged_lepton_branch = "| Charged-lepton two-Higgs canonical reduction |" in atlas
    has_selector_row = (
        "higgs multiplicity selector" in atlas_lower
        or "shared-higgs z_3 universality theorem" in atlas_lower
    )
    has_nonselection_row = "| PMNS minimal-branch nonselection |" in atlas
    has_universality_open_lane = "CKM Higgs-`Z_3` universality" in gates
    has_universality_collapse = "| Lepton shared-Higgs universality collapse |" in atlas
    has_universality_underdetermination = (
        "| Lepton shared-Higgs universality underdetermination |" in atlas
    )

    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT ATLAS DOES ISOLATE THE MINIMAL BRANCHES")
    print("=" * 88)
    check("Atlas carries the minimal neutrino-side canonical branch", has_neutrino_branch)
    check("Atlas carries the minimal charged-lepton-side canonical branch", has_charged_lepton_branch)
    check("Atlas carries this note's nonselection row", has_nonselection_row)

    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT PACKAGE STILL HAS NO EXACT BRANCH SELECTOR")
    print("=" * 88)
    check("Atlas does not contain a retained Higgs-multiplicity or shared-Higgs selector theorem",
          not has_selector_row)
    check("Live gates note still records shared-Higgs universality as a high-value open lane",
          has_universality_open_lane)
    check("Atlas carries the universality-collapse conditional row (forced-universality consequence)",
          has_universality_collapse)
    check("Atlas carries the universality-underdetermination row (no current-stack force)",
          has_universality_underdetermination)

    print("\n" + "=" * 88)
    print("PART 3: THE PACKAGE TREATS BRANCH SELECTION AS UNDERDETERMINED")
    print("=" * 88)
    check("Atlas keeps both minimal branches and their nonselection theorem co-listed",
          has_neutrino_branch and has_charged_lepton_branch and has_nonselection_row)

    print()
    print("  So the current exact bank has reached the honest endpoint:")
    print("    - minimal PMNS-producing branches are isolated,")
    print("    - their canonical sizes are known,")
    print("    - but no exact selector or invariant-deriving bridge exists yet.")

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-atlas answer:")
    print("    - the minimal neutrino-side and charged-lepton-side branches are isolated")
    print("    - the current atlas/package does not select among them")
    print("    - the current exact bank does not yet derive their seven canonical quantities")
    print()
    print("  So the remaining finish-line work is not more branch hunting.")
    print("  It is either:")
    print("    - derive a selector theorem, or")
    print("    - derive the seven canonical quantities on a chosen branch.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
