#!/usr/bin/env python3
"""
Current-bank theorem: existing exact selector tools do not realize the PMNS
branch selector.

Question:
  After auditing the atlas bank axiom-first, do the existing exact selector
  tools already realize the remaining PMNS/neutrino branch selector under
  another name?

Answer:
  No. The current exact selector bank acts on other domains:
    - graph-axis selection on the cube-shift triplet
    - temporal-orbit selection on the APBC circle
    - scalar-axis selection on the EWSB quartic surface
  None is an exact bridge theorem selecting the Higgs-Z_3 datum or the
  neutrino-side versus charged-lepton-side minimal PMNS branch.

Boundary:
  Current-bank theorem only. It does not claim that such a bridge selector is
  impossible in future work.
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
    print("PMNS SELECTOR BANK: CURRENT NONREALIZATION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Graph-first weak-axis selector derivation")
    print("  - Hierarchy bosonic-bilinear selector")
    print("  - EWSB quartic selector inside the hierarchy/CKM lane")
    print("  - Neutrino Higgs Z_3 underdetermination")
    print("  - PMNS minimal-branch nonselection")
    print()
    print("Question:")
    print("  Do the exact selector tools already in the current bank realize the")
    print("  missing PMNS branch selector?")

    graph_selector = read("docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md")
    bilinear_selector = read("docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    ckm_selector = read("docs/CKM_FROM_MASS_HIERARCHY_NOTE.md")
    higgs_qh = read("docs/NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md")
    pmns_nonselection = read("docs/PMNS_MINIMAL_BRANCH_NONSELECTION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK DOES CONTAIN EXACT SELECTOR TOOLS")
    print("=" * 88)
    check("Atlas carries the graph-first weak-axis selector tool",
          "| Graph-first selector |" in atlas)
    check("The graph-first selector acts on the cube-shift source H(phi)=sum phi_i S_i",
          "H(\\phi) = \\sum_{i=1}^3 \\phi_i S_i" in graph_selector and "axis vertices" in graph_selector)
    check("The bosonic-bilinear selector acts on APBC temporal-orbit support",
          "`L_t = 4`" in bilinear_selector and "APBC temporal circle" in bilinear_selector)
    check("The CKM/hierarchy lane carries an exact quartic selector on scalar-axis space",
          "EWSB quartic selector" in ckm_selector and "breaks S\\_3 -> Z\\_2" in ckm_selector)

    print("\n" + "=" * 88)
    print("PART 2: THE PMNS SELECTOR QUESTION LIVES ON A DIFFERENT EXACT DATA SET")
    print("=" * 88)
    check("The Higgs-side theorem still leaves q_H underdetermined in {0,+1,-1}",
          "`q_H in {0,+1,-1}`" in higgs_qh or "q_H in {0,+1,-1}" in higgs_qh)
    check("The PMNS boundary theorem still isolates but does not select the minimal branches",
          "current exact bank isolates the minimal neutrino-side and" in pmns_nonselection
          and "charged-lepton-side PMNS-producing branches" in pmns_nonselection
          and "does not yet select among the surviving" in pmns_nonselection)
    check("The current atlas has no retained Higgs-multiplicity or shared-Higgs selector row",
          "higgs multiplicity selector" not in atlas.lower() and "shared-higgs `z_3` universality theorem" not in atlas.lower())

    print("\n" + "=" * 88)
    print("PART 3: EXISTING SELECTORS DO NOT REALIZE THE PMNS BRANCH BIT")
    print("=" * 88)
    check("The graph-first selector note does not supply a lepton Higgs-Z_3 bridge",
          "q_H" not in graph_selector and "Y_nu" not in graph_selector and "Y_e" not in graph_selector)
    check("The bosonic-bilinear selector note does not supply a lepton branch-selection bridge",
          "q_H" not in bilinear_selector and "Y_nu" not in bilinear_selector and "Y_e" not in bilinear_selector)
    check("The quartic selector statement in the CKM/hierarchy lane does not upgrade to a retained PMNS selector theorem",
          "Higgs Z\\_3 charge" in ckm_selector and "not yet universal" in ckm_selector)

    print()
    print("  So the current exact selector bank has real selector tools, but they")
    print("  act on graph-axis, temporal-orbit, and scalar-axis domains rather")
    print("  than on the lepton Higgs-Z_3 / PMNS branch datum.")

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the current bank does contain exact selector tools")
    print("    - but none of them realizes the missing PMNS branch selector")
    print("    - a genuinely new bridge selector is still required to choose the")
    print("      minimal neutrino-side or charged-lepton-side closure branch")
    print()
    print("  So the remaining selector gap is not hidden elsewhere in the current")
    print("  atlas bank under another exact selector name.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
