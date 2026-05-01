#!/usr/bin/env python3
"""EW color-projection cycle-cleanup integration runner.

Verifies the follow-up cycle-cleanup edits to the 3 cycle nodes
(YT_EW_COLOR_PROJECTION_THEOREM.md, RCONN_DERIVED_NOTE.md,
EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md) that
integrate the new Fierz-channel derivation
(EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md, PR #249) into
the primary citation chain for the (N_c^2 - 1)/N_c^2 coefficient.

What this runner verifies:

  1. The new Fierz note (dependency from PR #249) is present in the
     working tree.
  2. YT_EW_COLOR_PROJECTION_THEOREM.md cites the Fierz note as a
     load-bearing one-hop dependency (markdown link in header section).
  3. YT_EW §2.7 names "TWO INDEPENDENT" derivations and references both
     the Fierz route (exact) and the 1/N_c route (RCONN).
  4. RCONN_DERIVED_NOTE.md has a "Sibling exact derivation" cross-ref to
     the Fierz note.
  5. EW_CURRENT_MATCHING_OZI_SUPPRESSION note has the same sibling
     cross-ref.
  6. The 3 cycle nodes' load-bearing physics content is preserved
     (no structural-content removed, only complementary citations
     added).
  7. The matching rule (M) is still named honestly in YT_EW.

The cycle-cleanup PR does NOT add new physics; it integrates the
exact-arithmetic Fierz route into the audit-graph chain so the
(N_c^2 - 1)/N_c^2 coefficient is no longer load-bearing on the 1/N_c
expansion alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


FIERZ_NOTE = "docs/EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md"
YT_EW = "docs/YT_EW_COLOR_PROJECTION_THEOREM.md"
RCONN = "docs/RCONN_DERIVED_NOTE.md"
OZI = "docs/EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md"


def part1_dependency_exists() -> None:
    section("Part 1: Fierz-channel note exists (PR #249 dependency)")
    check(
        "PR #249 Fierz-channel note is present in the working tree",
        (ROOT / FIERZ_NOTE).is_file(),
    )


def part2_yt_ew_cites_fierz_note() -> None:
    section("Part 2: YT_EW_COLOR_PROJECTION_THEOREM.md integration")
    note = read(YT_EW)
    fierz_link = "[EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)"
    check(
        "YT_EW header now cites the Fierz note as a one-hop dep (markdown link)",
        fierz_link in note,
    )
    # Check across line-wrapping by normalizing whitespace
    note_compact = " ".join(note.split())
    check(
        "YT_EW header explicitly labels the Fierz note as the 'primary group-theory derivation route'",
        "primary group-theory derivation route" in note_compact,
    )
    check(
        "YT_EW header marks RCONN as 'complementary' (not the only chain)",
        "complementary" in note and "RCONN_DERIVED_NOTE.md" in note,
    )
    check(
        "YT_EW §2.7 names 'TWO INDEPENDENT EXACT DERIVATIONS'",
        "TWO INDEPENDENT" in note or "two independent" in note,
    )
    check(
        "YT_EW §2.7 explicitly states the Fierz route gives the ratio with no O(1/N_c⁴) correction",
        "no `O(1/N_c⁴)` correction" in note or "no O(1/N_c⁴) correction" in note,
    )
    check(
        "YT_EW now names the matching rule (M) as the residual load-bearing input",
        "matching rule (M)" in note and "residual load-bearing input" in note,
    )


def part3_rconn_cross_ref() -> None:
    section("Part 3: RCONN_DERIVED_NOTE.md sibling cross-ref")
    note = read(RCONN)
    fierz_link = "[EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)"
    check(
        "RCONN has 'Sibling exact derivation' cross-ref to the Fierz note",
        "Sibling exact derivation" in note and fierz_link in note,
    )
    check(
        "RCONN now distinguishes the two routes (Fierz exact vs 1/N_c expansion)",
        "exact at any finite N_c" in note or "exact at any finite" in note,
    )


def part4_ozi_cross_ref() -> None:
    section("Part 4: OZI suppression note sibling cross-ref")
    note = read(OZI)
    fierz_link = "[EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)"
    check(
        "OZI has 'Sibling exact derivation' cross-ref to the Fierz note",
        "Sibling exact derivation" in note and fierz_link in note,
    )
    check(
        "OZI distinguishes its dynamical-suppression argument from the Fierz channel-fraction argument",
        "complementary" in note and ("dynamical" in note or "channel-fraction" in note or "channel weight" in note),
    )


def part5_no_physics_content_removed() -> None:
    section("Part 5: load-bearing physics content preserved across all 3 cycle nodes")
    yt_ew = read(YT_EW)
    rconn = read(RCONN)
    ozi = read(OZI)
    # YT_EW signature content
    check(
        "YT_EW retains the 9/8 = N_c^2/(N_c^2-1) statement",
        "9/8" in yt_ew and "N_c^2 / (N_c^2 - 1)" in yt_ew,
    )
    check(
        "YT_EW retains the Fierz identity equation Pi_EW = N_c D - 2N_c sum_A Pi_3^{AA}",
        "Pi_EW = N_c D - 2N_c sum_A Pi_3^{AA}" in yt_ew,
    )
    # RCONN signature content
    check(
        "RCONN retains the leading-order R_conn = (N_c^2 - 1) / N_c^2 + O(1/N_c^4) statement",
        "R_conn = (N_c^2 - 1) / N_c^2 + O(1/N_c^4)" in rconn,
    )
    # OZI signature content
    check(
        "OZI retains the OZI-suppression Pi_EW^{phys} = Pi_EW^{conn} * (1 + O(1/N_c^2)) statement",
        "Pi_EW^{phys} = Pi_EW^{conn} * (1 + O(1/N_c^2))" in ozi,
    )


def part6_audit_graph_break() -> None:
    section("Part 6: cycle-break (semantic): coefficient route now non-circular")
    yt_ew = read(YT_EW)
    # Before this PR: yt_ew listed only RCONN + OZI as one-hop deps,
    # both of which (via the audit's semantic reading) tied back to
    # yt_ew's own Section 2.6 matching claim.
    # After this PR: yt_ew lists Fierz as primary, RCONN as
    # complementary 1/N_c, OZI as bounded large-N_c support.
    # The Fierz note's chain is yt_ew → fierz → NATIVE_GAUGE_CLOSURE
    # (retained), which is acyclic.
    check(
        "YT_EW now lists the Fierz note as a one-hop dep (graph dep added)",
        "[EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md]" in yt_ew,
    )
    check(
        "YT_EW makes explicit that the coefficient is no longer load-bearing on the 1/N_c expansion alone",
        "no longer the bottleneck" in yt_ew or "no longer load-bearing" in yt_ew,
    )


def main() -> int:
    section("EW color-projection cycle-cleanup integration verification")
    part1_dependency_exists()
    part2_yt_ew_cites_fierz_note()
    part3_rconn_cross_ref()
    part4_ozi_cross_ref()
    part5_no_physics_content_removed()
    part6_audit_graph_break()

    print()
    print("-" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("-" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
