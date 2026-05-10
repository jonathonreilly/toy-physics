#!/usr/bin/env python3
"""Review-hygiene runner for the 2026-05-10 cross-PR campaign consistency survey.

Verifies the structural/textual properties of
docs/CAMPAIGN_CONSISTENCY_SURVEY_NOTE_2026-05-10_meta.md without
running any physics computation. The survey note is meta, survey-only;
this runner only confirms the cross-PR consistency assertions are
recorded as expected.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "docs" / "CAMPAIGN_CONSISTENCY_SURVEY_NOTE_2026-05-10_meta.md"


def fmt(name: str, ok: bool, detail: str = "") -> tuple[bool, str]:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    return ok, line


def check_present(text: str, *needles: str) -> bool:
    return all(n in text for n in needles)


def main() -> int:
    if not NOTE.exists():
        print(f"FAIL: missing survey note at {NOTE}")
        return 1

    text = NOTE.read_text(encoding="utf-8")

    results: list[tuple[bool, str]] = []

    # 1. Meta classification + survey-only framing.
    results.append(
        fmt(
            "meta classification + survey-only",
            check_present(
                text,
                "**Type:** meta",
                "**Claim type:** meta",
                "survey-only",
                "no theorem promotion",
            ),
        )
    )

    # 2. Survey result records no contradictions.
    results.append(
        fmt(
            "survey result: no contradictions detected",
            check_present(text, "**Survey result:**", "no contradictions"),
        )
    )

    # 3. Two-axiom surface preserved.
    results.append(
        fmt(
            "A1+A2 preserved",
            check_present(
                text,
                "MINIMAL_AXIOMS_2026-05-03",
                "**A1** Local algebra `Cl(3)`",
                "**A2** Spatial substrate `Z³`",
            ),
        )
    )

    # 4. Four foundational meta clarifications.
    for pr, label in [
        ("#725", "physical-lattice"),
        ("#728", "C_3-preserved"),
        ("#729", "conventions-unification"),
        ("#790", "BAE rename"),
    ]:
        results.append(
            fmt(
                f"foundational meta {pr} ({label})",
                pr in text,
            )
        )

    # 5. BAE 30-probe campaign cross-references.
    results.append(
        fmt(
            "BAE 30-probe terminal synthesis #836",
            check_present(
                text,
                "PR #836",
                "30-probe",
                "Probe 19",
                "Probe 24",
                "Probe 29",
            ),
        )
    )

    # 6. BAE + P admission count maintained.
    results.append(
        fmt(
            "BAE + P admissions correctly counted",
            check_present(
                text,
                "BAE",
                "radian-bridge",
                "2 admissions remaining",
            ),
        )
    )

    # 7. Substrate-to-carrier round (P1, P2, P3, P4).
    for pr, label in [
        ("#874", "P3"),
        ("#875", "P4"),
        ("#876", "P2"),
        ("#877", "P1"),
    ]:
        results.append(
            fmt(
                f"substrate-to-carrier {pr} ({label})",
                pr in text and label in text,
            )
        )

    # 8. G_Newton three named admissions B(a), B(b), B(c).
    results.append(
        fmt(
            "G_Newton three admissions named",
            check_present(text, "B(a)", "B(b)", "B(c)"),
        )
    )

    # 9. G_Newton companion sub-closures G1, G2, G3.
    for token in ["gnewtonG1", "gnewtonG2", "gnewtonG3"]:
        results.append(
            fmt(
                f"G_Newton companion {token}",
                token in text,
            )
        )

    # 10. Synthesis #882 with timing note.
    results.append(
        fmt(
            "synthesis #882 timing vs G1/G2/G3",
            check_present(
                text,
                "PR #882",
                "BEFORE G1/G2/G3",
                "09:49:07",
                "09:50:17",
            ),
        )
    )

    # 11. Bridge-lane / Lane 2 / C-iso landmarks.
    for pr, label in [
        ("#843", "bridge-lane"),
        ("#845", "ε_witness"),
        ("#857", "NLO/N5LO"),
    ]:
        results.append(
            fmt(
                f"engineering landmark {pr} ({label})",
                pr in text,
            )
        )

    # 12. Eleven cross-consistency checks recorded.
    for ck in range(1, 12):
        results.append(
            fmt(
                f"cross-consistency Check {ck} listed",
                f"### Check {ck}:" in text,
            )
        )

    # 13. Conditionality chains explicit.
    results.append(
        fmt(
            "conditionality chains enumerated",
            check_present(
                text,
                "Conditionality chains",
                "PROVIDED substep-4",
                "PROVIDED P1+P2+P3",
                "PROVIDED G1+G2+G3",
            ),
        )
    )

    # 14. No silent admission introduction recorded.
    results.append(
        fmt(
            "no silent admission introduction",
            "no silent admission introduction" in text.lower()
            or "no silent new admission" in text.lower()
            or "no silent admission" in text.lower(),
        )
    )

    # 15. No theorem promotion or retagging.
    results.append(
        fmt(
            "no theorem promotion / retagging",
            check_present(
                text,
                "no theorem promotion",
                "no retagging",
            ),
        )
    )

    # 16. Authority disclaimer present.
    results.append(
        fmt(
            "authority disclaimer present",
            "Authority disclaimer" in text,
        )
    )

    # 17. Items audit lane retains authority on.
    results.append(
        fmt(
            "audit lane authority items listed",
            "audit lane retains authority" in text,
        )
    )

    # 18. Cross-domain independence: Probe 25 vs G2, Probe 22 vs P1.
    # Match against the Check section headers and key phrases (whitespace-collapsed).
    text_collapsed = " ".join(text.split())
    results.append(
        fmt(
            "Probe 25 vs G2 cross-domain check",
            check_present(
                text_collapsed,
                "Probe 25 (F3 structural rejection) vs G2 (Born-as-source)",
                "No domain overlap",
            ),
        )
    )
    results.append(
        fmt(
            "Probe 22 vs P1 cross-domain check",
            check_present(
                text_collapsed,
                "Probe 22 (spectrum-cone pivot illusory) vs P1 (RP-induced selection)",
                "Different sectors",
            ),
        )
    )

    # 19. F3 finding consistency check (Probes 25 + 27 + 28 → F3).
    results.append(
        fmt(
            "F3 finding consistency Probes 25/27/28",
            check_present(text, "Probe 27", "Probe 28", "F3"),
        )
    )

    # 20. Substep-4 staggered-Dirac realization gate referenced.
    results.append(
        fmt(
            "substep-4 staggered-Dirac referenced",
            "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac" in text,
        )
    )

    # 21. C-iso engineering eliminated as dominant systematic.
    results.append(
        fmt(
            "C-iso eliminated as dominant systematic",
            "C-iso truncation eliminated" in text or "eliminated as dominant systematic" in text,
        )
    )

    # 22. Note explicitly does not adjudicate audit-lane items.
    results.append(
        fmt(
            "audit lane authority preserved (does NOT adjudicate)",
            check_present(
                text,
                "does NOT adjudicate",
                "Whether P1, P2, P3",
                "Whether G1, G2, G3",
            ),
        )
    )

    # 23. Inventory section lists landed retained-grade claims.
    results.append(
        fmt(
            "inventory section present",
            "Inventory — landed retained-grade claims surveyed" in text,
        )
    )

    # 24. Probe 29 partial-falsification candidate noted.
    results.append(
        fmt(
            "Probe 29 partial-falsification recorded",
            "partial-falsification candidate" in text and "κ=1" in text,
        )
    )

    # 25. Lane 2 STRUCTURAL OBSTRUCTION verdict.
    results.append(
        fmt(
            "Lane 2 STRUCTURAL OBSTRUCTION recorded",
            "STRUCTURAL OBSTRUCTION" in text,
        )
    )

    # 26. The companion paired runner is referenced (filesystem self-loop).
    results.append(
        fmt(
            "paired runner self-reference",
            "frontier_campaign_consistency_survey_2026_05_10_meta.py" in text,
        )
    )

    # 27. Cached output path referenced.
    results.append(
        fmt(
            "cached output path referenced",
            "frontier_campaign_consistency_survey_2026_05_10_meta.txt" in text,
        )
    )

    # Print results and tally.
    passes = sum(1 for ok, _ in results if ok)
    fails = len(results) - passes
    for _, line in results:
        print(line)
    print()
    print(f"=== TOTAL: PASS={passes}, FAIL={fails} ===")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
