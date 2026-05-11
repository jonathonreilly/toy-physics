#!/usr/bin/env python3
"""Check the radian-unit-convention reclassification meta note.

This runner is a review-hygiene check, not a physics proof. It verifies:
  - the note is classified as meta and does not declare pipeline status;
  - the reclassification of P as a unit convention is stated explicitly
    and cited to the Conventions Unification pattern (PR #729);
  - the framework's structural prediction (phi_dimensionless = 2/9 per
    Probe 24 Step 1) is correctly identified as retained;
  - the SI definitional fact ([rad] = L/L = 1) is stated as the
    definitional input, not derived from Cl(3)/Z^3;
  - the reclassification is stated as conditional / SHARPENED, not as
    strict closure;
  - the note does not promote any retained theorem or claim BAE is
    closed;
  - the note does not add a new mathematical axiom;
  - the note does not load PDG values as derivation input;
  - cross-references to the recently-landed companion notes are present;
  - the structural-feature limit (framework's natural scaling matching
    SI/radian convention is itself a structural consistency observation)
    is stated honestly.

Companion to:
  - CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md (PR #729)
  - PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md (PR #725)
  - KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md (PR #814)
  - KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md (PR #826)
  - KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md (PR #836)
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "RADIAN_UNIT_CONVENTION_RECLASSIFICATION_SHARPENED_NOTE_2026-05-10_radianconv.md"
CONVENTIONS_NOTE = ROOT / "docs" / "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md"
PHYSICAL_LATTICE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
PROBE24 = ROOT / "docs" / "KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md"
PROBE30 = ROOT / "docs" / "KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md"
SYNTHESIS = ROOT / "docs" / "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"

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
    for path, label in [
        (NOTE, "radian-unit-convention reclassification note"),
        (CONVENTIONS_NOTE, "conventions-unification companion note"),
        (PHYSICAL_LATTICE, "physical-lattice baseline note"),
        (PROBE24, "Probe 24 phi-from-Z_3-character note"),
        (PROBE30, "Probe 30 radian-from-dimensions note"),
        (SYNTHESIS, "30-probe campaign terminal synthesis note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
    ]:
        if not path.exists():
            print(f"missing {label}: {path}")
            return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Radian-unit-convention reclassification check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("source note is meta", "**Claim type:** meta" in note)
    effective_label = "Effective" + " status:"
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    # Note uses 'effective_status' field-name reference in passing (when
    # explaining what is preserved). What we forbid is DECLARING a value.
    check(
        "does not declare effective_status value",
        not re.search(r"effective_status\s*:\s*\w+", note),
    )
    check("does not declare audit-clean verdict token", audit_clean_token not in note)
    note_plain = " ".join(note.split())
    check(
        "does not add a new mathematical axiom",
        ("does not add a new" in note.lower())
        and (
            "physical `Cl(3)` local algebra plus `Z^3` spatial substrate baseline still suffice"
            in note_plain
            or "physical `Cl(3)` local algebra plus `Z^3` spatial substrate baseline still suffices"
            in note_plain
            or "A1+A2 still suffice" in note
        ),
    )

    # ---- core reclassification statement ----
    note_norm = " ".join(note.replace("*", "").split())
    check(
        "reclassification of P as unit convention stated explicitly",
        "P` reclassified as a unit convention" in note
        or "reclassified as a unit convention" in note,
    )
    check(
        "Conventions Unification pattern cited (PR #729)",
        "PR #729" in note and "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08" in note,
    )
    check(
        "P explicitly identified with radian-bridge primitive",
        "radian-bridge primitive" in note and "`P`" in note,
    )

    # ---- positive content (Probe 24 Step 1 retained) ----
    check(
        "Probe 24 Step 1 phi_dimensionless = 2/9 retained content cited",
        "n_eff / d² = 2/9" in note or "n_eff/d² = 2/9" in note,
    )
    check(
        "Probe 24 source-note cross-reference present",
        "KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24" in note,
    )
    check(
        "Probe 30 source-note cross-reference present",
        "KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30" in note,
    )

    # ---- SI definitional fact ----
    check(
        "SI definitional fact ([rad] = L/L = 1) stated",
        "[rad] = L / L = 1" in note or "[rad] = L/L = 1" in note,
    )
    check(
        "SI radian dimensionless explicitly stated",
        "SI radian is itself dimensionless" in note
        or "SI radian is dimensionless" in note
        or "radian is itself dimensionless" in note,
    )
    check(
        "explicit comparison with cycle convention",
        "period-1-rad" in note and "period-2π-rad" in note,
    )

    # ---- conventions unification analogues ----
    for analogue in ["meter", "second", "kilogram", "GeV"]:
        check(
            f"unit-convention analogue cited: {analogue}",
            analogue in note,
        )

    # ---- conditional / sharpened framing ----
    check(
        "reclassification stated conditionally",
        "conditional" in note.lower(),
    )
    check(
        "SHARPENED framing explicitly stated",
        "SHARPENED" in note,
    )
    check(
        "three honest framings present",
        "CLOSURE" in note and "STRUCTURAL OBSTRUCTION" in note and "SHARPENED" in note,
    )

    # ---- audit hygiene: no PDG numerical loading ----
    pdg_numeric_patterns = [
        r"m_e\s*=\s*0\.51",
        r"m_μ\s*=\s*105",
        r"m_τ\s*=\s*1\.77\d",
        r"m_e\s*=\s*0\.000511",
        r"m_τ\s*=\s*1\.7771",
    ]
    empirical_loading = False
    for pat in pdg_numeric_patterns:
        if re.search(pat, note, flags=re.IGNORECASE):
            empirical_loading = True
            break
    check(
        "no PDG numerical mass values inserted as derivation input",
        not empirical_loading,
    )
    check(
        "explicitly disclaims PDG-input use",
        "No PDG values consumed as derivation input" in note
        or "does not load PDG" in note.lower()
        or "PDG appears only as" in note,
    )

    # ---- forbidden promotions ----
    # We forbid affirmative promotions; negated phrasings ("does not promote",
    # "No retained theorem promoted", "not claim BAE is closed") are allowed
    # and indeed expected in the disclaimer sections.
    def has_affirmative_match(pattern: str, text: str) -> bool:
        """True iff there is at least one match NOT preceded (within ~50 chars)
        by a negation token."""
        for m in re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            head = text[max(0, m.start() - 50): m.start()].lower()
            negators = ("not ", "no ", "never", "without", "absent", "unaffected", "unchanged", "claim ")
            if any(neg in head for neg in negators):
                continue
            return True
        return False

    forbidden_promotions = [
        ("BAE closure by declaration", r"BAE\s+is\s+(now\s+)?closed"),
        ("BAE retained promotion", r"BAE\s+is\s+(now\s+)?retained"),
        ("specific theorem promoted to retained",
         r"theorem\s+(?:is\s+)?(?:now\s+)?promoted"),
        ("specific bridge-gap count claimed below 1",
         r"admission count\s+(?:is|=)\s*0"),
    ]
    for label, pattern in forbidden_promotions:
        check(
            f"forbidden promotion absent: {label}",
            not has_affirmative_match(pattern, note),
        )

    # ---- BAE remains bounded ----
    check(
        "BAE explicitly remains bounded",
        "BAE remains bounded" in note
        or "BAE remains independently bounded" in note,
    )
    check(
        "BAE 30-probe campaign synthesis cited",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09" in note,
    )

    # ---- structural-feature limit honestly stated ----
    check(
        "structural-feature limit honestly stated",
        "natural angular scaling" in note
        or "structural feature" in note.lower(),
    )
    check(
        "honest 'what this DOES NOT close' section",
        "What this DOES NOT close" in note,
    )

    # ---- admission count reduction ----
    check(
        "admission count reduction stated (2 -> 1)",
        ("2 → 1" in note) or ("2 -> 1" in note),
    )
    check(
        "admission count = 1 BAE-only stated",
        "1 (BAE only)" in note or "BAE only" in note,
    )

    # ---- review-loop rule present ----
    check(
        "review-loop rule present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )

    # ---- audit-lane authority preserved ----
    check(
        "audit-lane authority preserved",
        "audit lane" in note.lower() and "authority" in note.lower(),
    )

    # ---- cross-references ----
    cross_refs = [
        "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08",
        "KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24",
        "KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30",
        "KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24",
        "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09",
        "MINIMAL_AXIOMS_2026-05-03",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE",
    ]
    for ref in cross_refs:
        check(f"cross-references retained note: {ref}", ref in note)

    # ---- baseline alignment ----
    check(
        "minimal axioms note has physical Cl(3) A1",
        "the physical local algebra is `Cl(3)`" in minimal,
    )
    check(
        "minimal axioms note has physical Z^3 A2",
        "the physical spatial substrate is the cubic" in minimal,
    )

    # ---- bottom line present ----
    check(
        "bottom-line verdict present",
        "Bottom line" in note or "Verdict:" in note,
    )

    # ---- convention table present ----
    check(
        "comparison table to landed conventions present",
        "Length" in note and "Time" in note and "Mass" in note and "Angle" in note,
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Radian-unit-convention reclassification check passed: "
        "P reclassified as unit convention under Conventions Unification "
        "(PR #729) pattern, conditional / SHARPENED, no retained theorem "
        "promoted, no new axiom, no PDG input, BAE remains bounded."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
