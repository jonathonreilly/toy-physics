#!/usr/bin/env python3
"""Check the conventions-unification companion note.

This runner is a review-hygiene check, not a physics proof. It verifies:
  - the note is classified as meta and does not declare pipeline status;
  - the unification of labeling and unit conventions is stated explicitly
    and cited to standard physics analogues;
  - the Planck-from-structure escape is stated conditionally, not as a
    closure claim;
  - the note does not load PDG values as derivation input;
  - the note does not promote any specific Option C parameter target to
    retained status;
  - the note does not claim the bridge-gap admission count drops to a
    specific number;
  - cross-references to the recently-landed companion notes are present;
  - the note does not add a new mathematical axiom.

Companion to:
  - PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md
  - C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
PHYSICAL_LATTICE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
C3_PRESERVED = ROOT / "docs" / "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md"

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
        (NOTE, "conventions-unification companion note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
        (PHYSICAL_LATTICE, "physical-lattice baseline note"),
        (C3_PRESERVED, "preserved-C_3 companion note"),
    ]:
        if not path.exists():
            print(f"missing {label}: {path}")
            return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Conventions-unification companion check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("source note is meta", "**Claim type:** meta" in note)
    effective_label = "Effective" + " status:"
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    check(
        "does not declare pipeline status",
        effective_label not in note and effective_token not in note and "effective_status" not in note,
    )
    check("does not declare audit-clean verdict token", audit_clean_token not in note)
    check(
        "does not add a new mathematical axiom",
        "does not add a new" in note.lower() and "A1+A2 still suffice" in note,
    )

    # ---- the unification stated ----
    # Normalize whitespace + strip markdown emphasis markers for substring search
    note_norm = " ".join(note.replace("*", "").split())
    check(
        "unification of labeling+unit conventions stated explicitly",
        "labeling conventions and unit conventions are the same kind" in note_norm,
    )
    check(
        "labeling layer present (mass ordering)",
        "Mass-ordering" in note and "{electron, muon, tau}" in note,
    )
    check(
        "unit-conversion layer present",
        "Unit conversion" in note
        and "meters" in note
        and "seconds" in note
        and "kilograms" in note,
    )
    # quark labels: any of these representations is fine
    quark_label_present = (
        "u`, `d`, `s`, `c`, `b`, `t`" in note
        or "{u, d, s, c, b, t}" in note
        or "{u, c, t}" in note
        or "u`/`c`/`t`" in note
    )
    check("labeling-convention analogue cited (quark names)", quark_label_present)
    for analogue in ["ν_1", "K_S"]:
        check(f"labeling-convention analogue cited: {analogue}", analogue in note)

    # ---- Planck escape stated conditionally ----
    check(
        "Planck-from-structure escape mentioned",
        "Planck length" in note or "Planck length" in note.replace("\n", " "),
    )
    check(
        "Planck escape stated conditionally",
        "is itself a research target" in note
        or "conditional" in note.lower()
        and "research target" in note.lower(),
    )
    check(
        "Planck-derivation explicitly NOT claimed retained",
        "is not retained on main" in note or "not retained" in note,
    )
    check(
        "EW-Planck hierarchy retained-derivation cited (no opining)",
        "v_EW = M_Pl" in note and "COMPLETE_PREDICTION_CHAIN_2026_04_15" in note,
    )

    # ---- audit hygiene: no PDG numerical loading ----
    pdg_numeric_patterns = [
        r"m_e\s*=\s*0\.51",
        r"m_μ\s*=\s*105",
        r"m_τ\s*=\s*1\.77",
        r"m_e\s*=\s*0\.000511",
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
        "explicitly references substep-4 AC narrowing",
        "substep-4 AC narrowing" in note,
    )
    check(
        "explicitly disclaims PDG-input use",
        "PDG values are still not\nload-bearing" in note
        or "not load-bearing as derivation input" in note
        or "PDG values are still not" in note,
    )

    # ---- forbidden promotions ----
    forbidden_promotions = [
        ("AC closure by declaration", "AC" + "_" + r"[a-zA-Zφλ]+\s+is\s+closed"),
        ("specific param promoted to retained",
         r"A1\s+is\s+(now\s+)?retained|P1\s+is\s+(now\s+)?retained"),
        ("specific bridge-gap count claimed",
         r"bridge-gap admission count\s+(?:is|=)\s*\d"),
    ]
    for label, pattern in forbidden_promotions:
        check(
            f"forbidden promotion absent: {label}",
            re.search(pattern, note, flags=re.IGNORECASE | re.DOTALL) is None,
        )

    # ---- conditional language is honest ----
    check(
        "Planck-derivation result is open, not closed",
        "open" in note.lower() and "research target" in note.lower(),
    )
    check(
        "Option C parameter targets remain bounded",
        "remain bounded" in note or "remain open" in note,
    )

    # ---- cross-references ----
    for ref in [
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE",
        "MINIMAL_AXIOMS_2026-05-03",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE",
        "A3_OPTION_C_BRANNEN_RIVERO",
        "KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE",
    ]:
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

    # ---- review-loop rule present ----
    check(
        "review-loop rule present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Conventions-unification check passed: "
        "labeling and unit conventions tracked together, Planck escape "
        "stated conditionally, no Option C target promoted, no new axiom."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
