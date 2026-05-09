#!/usr/bin/env python3
"""Check the 30-probe BAE campaign terminal synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis:
  - is classified as meta and does not declare pipeline status;
  - cites all 30 probes with their PR numbers;
  - records the 2 positive derivations (m_τ Wilson chain, φ_dimensionless=2/9);
  - records the partial-falsification finding (Probe 29: κ=1 vs κ=2);
  - records the structural impossibility theorems (14, 17, 25+27+28);
  - records the 2 remaining admissions (BAE + P);
  - does not promote any audit row;
  - cross-references retained foundational notes;
  - establishes review-loop rule for future BAE-related branches.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
RENAME_NOTE = ROOT / "docs" / "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1
    if not MINIMAL_AXIOMS.exists():
        print(f"missing minimal axioms note: {MINIMAL_AXIOMS}")
        return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("30-probe BAE campaign terminal synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    check(
        "does not declare pipeline status",
        effective_token not in note and audit_clean_token not in note,
    )

    # ---- 30 probes cited with PRs ----
    expected_prs = [
        "#727", "#730", "#731", "#732",  # Routes F/E/A/D
        "#735", "#733", "#736", "#734",  # Probes 1-4
        "#738", "#737", "#740",          # Probes 5-7
        "#751",                          # 11-probe synthesis
        "#755", "#763", "#784",          # Probes 12-14
        "#788", "#789", "#787",          # Probes 15-17
        "#790",                          # rename
        "#792",                          # Probe 18
        "#799", "#798", "#800", "#801",  # Probes 19-22
        "#813", "#814", "#820", "#818",  # Probes 23-26
        "#824", "#827", "#825", "#826",  # Probes 27-30
    ]
    for pr in expected_prs:
        check(f"PR cross-reference: {pr}", pr in note)

    # ---- 2 positive derivations recorded ----
    check(
        "Probe 19 m_τ Wilson chain recorded",
        "m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}" in note
        and "0.017%" in note,
    )
    check(
        "Probe 24 Step 1 φ_dimensionless = 2/9 recorded",
        "φ_dimensionless = n_eff / d² = 2/9" in note
        or "n_eff / d² = 2/9" in note,
    )

    # ---- structural impossibility theorems recorded ----
    check(
        "Probe 14 impossibility (no retained U(1) projects to U(1)_b) recorded",
        "no retained continuous U(1) projects to U(1)_b" in note
        or "no retained continuous U(1)" in note,
    )
    check(
        "Probe 17 impossibility (U(1)_b spectrum-non-preserving) recorded",
        "U(1)_b is spectrum-non-preserving" in note
        and "ANY unitary similarity" in note,
    )
    check(
        "Probes 25+27+28 (F1 structurally absent) recorded",
        "F1 (multiplicity (1,1)) is structurally absent" in note
        or "F1 is structurally absent" in note,
    )

    # ---- partial-falsification finding (Probe 29) recorded ----
    check(
        "Probe 29 partial falsification recorded",
        "PARTIAL FALSIFICATION" in note
        or "partial falsification" in note.lower(),
    )
    check(
        "κ=1 vs κ=2 disagreement recorded",
        ("κ = 1" in note and "κ = 2" in note) or
        ("κ=1" in note and "κ=2" in note),
    )
    check(
        "factor-of-2 disagreement quantified",
        "factor of 2 in κ" in note or "factor 2 in κ" in note,
    )

    # ---- 2 remaining admissions correctly counted ----
    check(
        "BAE remaining admission named",
        "BAE" in note and "bounded" in note.lower(),
    )
    check(
        "P (radian bridge) remaining admission named",
        "radian bridge" in note.lower() or ("P" in note and "radian" in note),
    )
    check(
        "admission count is 2 (not 3)",
        "Total | **2**" in note or "**2** (Probe 24 ruled out third)" in note
        or "Total | 2" in note,
    )

    # ---- no theorem promotion ----
    check(
        "no theorem promotion",
        "does not promote" in note,
    )
    check(
        "no axiom added",
        "no new axiom" in note.lower() or "No new axiom" in note,
    )

    # ---- strategic options listed but not selected ----
    check(
        "strategic options listed (3 options)",
        "Accept partial falsification" in note
        and ("Build new retained physics" in note or "Build new" in note)
        and ("Pivot" in note or "pivot" in note),
    )
    check(
        "synthesis does not select option",
        "does not select" in note.lower(),
    )

    # ---- cross-references to retained foundational notes ----
    foundational_refs = [
        "MINIMAL_AXIOMS_2026-05-03",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08",
        "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09",
        "KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08",
    ]
    for ref in foundational_refs:
        check(f"cross-references retained note: {ref}", ref in note)

    # ---- baseline alignment ----
    check(
        "minimal axioms note has Cl(3) A1",
        "the physical local algebra is `Cl(3)`" in minimal,
    )
    check(
        "minimal axioms note has Z³ A2",
        "the physical spatial substrate is the cubic" in minimal,
    )

    # ---- naming-collision warning preserved ----
    check(
        "naming-collision warning present",
        "framework axiom A1" in note and "BAE" in note,
    )

    # ---- review-loop rule ----
    check(
        "review-loop rule for future branches present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )
    check(
        "review-loop rule notes campaign is terminal",
        "campaign on BAE is **terminal**" in note
        or "campaign is **terminal**" in note,
    )

    # ---- 4 rounds across 30 probes ----
    rounds_present = sum(1 for r in ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "Round 6", "Round 7", "Round 8", "Round 9"] if r in note)
    check(
        "campaign rounds enumerated (≥7 distinct rounds)",
        rounds_present >= 7,
        f"rounds counted: {rounds_present}/9",
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "30-probe BAE campaign terminal synthesis check passed: "
        "all 30 probes cited, 2 positive derivations recorded, "
        "structural impossibility theorems recorded, "
        "partial-falsification finding recorded, "
        "2 remaining admissions correctly counted, "
        "no theorem promotion, no axiom added, "
        "strategic options listed without selection."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
