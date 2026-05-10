#!/usr/bin/env python3
"""C-B(b) Born-as-source open-gate propagation runner.

This runner supports
`docs/CLOSURE_C_BB_F2_1_CORRECTION_NOTE_2026-05-10_cBB_correction.md`.
It checks a narrow source-note boundary:

* the conventions-unification companion does not contain Born-rule
  operationalism;
* the landed gnewtonG2 note does cite that companion for Born-rule
  operationalism;
* the landed T2 G_Newton hostile-review note records the same citation
  defect and names the downstream C-B(b) load;
* the downstream correction is an open-gate bookkeeping result, not an
  audit verdict, parent promotion, foundational-premise addition, or new
  physics derivation.

All checks are deterministic direct file inspections or structural
bookkeeping. No fitted, PDG, or observational values are used.
"""

from __future__ import annotations

from pathlib import Path

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def log_check(name: str, passed: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def read_doc(filename: str) -> str:
    path = ROOT / "docs" / filename
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def contains_all(text: str, needles: list[str]) -> bool:
    return all(needle in text for needle in needles)


def test_t1_conventions_has_no_born_operationalism() -> None:
    print("=" * 76)
    print("T1: CONVENTIONS-UNIFICATION CITATION CONTENT")
    print("=" * 76)

    filename = "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md"
    content = read_doc(filename)
    lower = content.lower()
    line_count = len(content.splitlines())

    log_check(
        "T1.a: conventions-unification companion exists",
        True,
        f"{filename}, lines={line_count}",
    )
    log_check(
        "T1.b: cited companion has no case-insensitive Born content",
        "born" not in lower,
        f"case-insensitive born count={lower.count('born')}",
    )
    log_check(
        "T1.c: cited companion is actually convention bookkeeping",
        ("label" in lower or "labeling" in lower) and "unit" in lower,
        "label/labeling and unit terms present",
    )
    print()


def test_t2_gnewton_source_carries_dead_citation() -> None:
    print("=" * 76)
    print("T2: LANDED GNEWTONG2 BORN-AS-SOURCE CITATION")
    print("=" * 76)

    filename = "G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md"
    content = read_doc(filename)
    lower = content.lower()

    log_check(
        "T2.a: gnewtonG2 source note exists",
        True,
        filename,
    )
    log_check(
        "T2.b: gnewtonG2 uses the conventions-unification companion for BornOp",
        contains_all(
            content,
            [
                "BornOp",
                "Born-rule operationalism",
                "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08",
            ],
        ),
        "BornOp row and companion citation found",
    )
    log_check(
        "T2.c: gnewtonG2 makes a Born-as-source claim surface",
        "born-as-source" in lower and "rho" in lower,
        "Born-as-source wording and density notation present",
    )
    print()


def test_t3_landed_hostile_review_records_defect() -> None:
    print("=" * 76)
    print("T3: LANDED T2 GNEWTON HOSTILE-REVIEW DEFECT RECORD")
    print("=" * 76)

    filename = "CLOSURE_T2_GNEWTON_REAUDIT_NOTE_2026-05-10_t2gnewton.md"
    content = read_doc(filename)
    lower = content.lower()

    log_check(
        "T3.a: T2 G_Newton hostile-review note exists",
        True,
        filename,
    )
    log_check(
        "T3.b: F2.1 citation defect is explicitly recorded",
        "f2.1" in lower and "citation defect" in lower and "zero matches" in lower,
        "F2.1, citation defect, and zero-match evidence present",
    )
    log_check(
        "T3.c: downstream C-B(b) load is named without acting as a verdict",
        "downstream c-b(b)" in lower and "canonical mass-coupling" in lower,
        "downstream C-B(b) mass-coupling chain is named",
    )
    print()


def test_t4_open_gate_boundary() -> None:
    print("=" * 76)
    print("T4: OPEN-GATE BOUNDARY FOR DOWNSTREAM C-B(b)")
    print("=" * 76)

    t2 = read_doc("CLOSURE_T2_GNEWTON_REAUDIT_NOTE_2026-05-10_t2gnewton.md")
    g2 = read_doc("G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md")
    hardening = read_doc("SELF_GRAVITY_BORN_HARDENING_NOTE.md")
    card = read_doc("STAGGERED_FERMION_CARD_2026-04-11.md")
    born_analysis = read_doc("BORN_RULE_ANALYSIS_2026-04-11.md")

    combined = "\n".join([t2, g2, hardening, card, born_analysis]).lower()

    log_check(
        "T4.a: Born-as-source remains an explicit named premise/open gate",
        "born-as-source" in combined and "admission" in combined,
        "Born-as-source admission wording present in landed sources",
    )
    log_check(
        "T4.b: Born+gravity hardening source exists and is bounded/no-go",
        "bounded no-go" in hardening.lower() or "no-go" in hardening.lower(),
        "hardening note names a bounded no-go boundary",
    )
    log_check(
        "T4.c: staggered fermion card imports rho = |psi|^2 as H2",
        "rho = |psi|^2" in card or "ρ = |ψ|^2" in card,
        "H2 position-density input is imported/admitted, not derived here",
    )
    log_check(
        "T4.d: no direct retained-grade Born derivation is asserted by this runner",
        "retained born-as-source derivation from the framework baseline" not in combined,
        "runner checks an open gate, not a retained promotion",
    )
    print()


def test_t5_note_policy_surface() -> None:
    print("=" * 76)
    print("T5: SOURCE-NOTE POLICY SURFACE")
    print("=" * 76)

    filename = "CLOSURE_C_BB_F2_1_CORRECTION_NOTE_2026-05-10_cBB_correction.md"
    content = read_doc(filename)
    lower = content.lower()

    banned = [
        "claim type:** " + "correction_" + "stanza",
        "target_" + "status",
        "audited_" + "clean",
        "effective_status = " + "retained",
        "audit_" + "status = " + "audited_" + "clean",
        "branch " + "`",
        "loop:",
        "cycle:",
        "pr #",
    ]

    log_check(
        "T5.a: source note declares canonical open_gate claim type",
        "**Claim type:** open_gate" in content,
        "claim_type surface is canonical for audit parsing",
    )
    log_check(
        "T5.b: source note avoids branch-local and audit-verdict authority",
        not any(term in lower for term in banned),
        "no PR-number authority, branch-local state, or audit verdicts",
    )
    log_check(
        "T5.c: source note names physical Cl(3) and Z^3 explicitly",
        "physical local algebra `cl(3)`" in lower and "physical `z^3` spatial substrate" in lower,
        "repo baseline is named without bare shorthand labels",
    )
    log_check(
        "T5.d: source note preserves the narrow salvage boundary",
        "does not modify or promote the downstream c-b(b)" in lower
        and "born-as-source open gate" in lower,
        "downstream chain is not promoted or retagged by review-loop",
    )
    print()


def main() -> int:
    print("# C-B(b) Born-as-source open-gate propagation runner")
    print("# Source note: docs/CLOSURE_C_BB_F2_1_CORRECTION_NOTE_2026-05-10_cBB_correction.md")
    print()

    test_t1_conventions_has_no_born_operationalism()
    test_t2_gnewton_source_carries_dead_citation()
    test_t3_landed_hostile_review_records_defect()
    test_t4_open_gate_boundary()
    test_t5_note_policy_surface()

    print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
