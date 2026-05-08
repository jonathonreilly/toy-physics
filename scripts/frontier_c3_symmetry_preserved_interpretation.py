#!/usr/bin/env python3
"""Check the C_3 symmetry preserved interpretation note.

This runner is a review-hygiene check, not a physics proof. It verifies
that the note:
  - is classified as meta and does not declare pipeline status;
  - does not load-bear PDG/empirical mass values as derivation input;
  - states the preserved-C_3 interpretation in the standard preserved-
    symmetry idiom (QCD color, isospin, CPT analogues);
  - treats mass-ordering labels {electron, muon, tau} as conventions
    while preserving the separate species/readout bridge boundary;
  - does not promote specific Option C parameter targets to retained
    status;
  - cross-references the retained provenance of the C_3 structure on
    hw=1;
  - does not add a new mathematical axiom.

It is a companion to the physical-lattice baseline interpretation runner.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
PHYSICAL_LATTICE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
SUBSTEP4 = ROOT / "docs" / "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"

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
        (NOTE, "C_3 preserved interpretation note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
        (PHYSICAL_LATTICE, "physical-lattice baseline note"),
        (SUBSTEP4, "substep-4 AC narrowing note"),
    ]:
        if not path.exists():
            print(f"missing {label}: {path}")
            return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("C_3 symmetry preserved interpretation check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("source note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    effective_label = "Effective" + " status"
    check(
        "does not declare pipeline status",
        effective_label not in note and effective_token not in note and "effective_status" not in note,
    )
    check("does not declare audit-clean verdict token", audit_clean_token not in note)
    check("does not add a new mathematical axiom", "does not add a new axiom" in note or "A1+A2 still suffice" in note)

    # ---- preserved-C_3 stance ----
    check("preserved-C_3 stance stated", "preserved" in note and "fundamental" in note)
    check(
        "explicit 'embrace, not break' framing",
        "embrace" in note.lower() or "is not a problem to be broken" in note,
    )
    check(
        "10-probe campaign result re-read constructively",
        "Cannot be broken" in note or "cannot be broken" in note,
    )

    # ---- preserved-symmetry analogues ----
    for analogue in ["QCD", "color", "Isospin", "CPT", "K_S"]:
        check(f"preserved-symmetry analogue cited: {analogue}", analogue in note)

    # ---- structural prediction vs labeling convention ----
    check(
        "structural predictions section present",
        "Structural predictions" in note or "structural prediction" in note.lower(),
    )
    check(
        "labeling conventions section present",
        "Labeling conventions" in note or "labeling convention" in note.lower(),
    )
    check(
        "mass-ordering labels are conventions",
        "mass-ordering" in note.lower() and "convention" in note.lower(),
    )
    for analogue_label in ["u`/`c`/`t`", "ν_1", "K_S"]:
        check(
            f"labeling-convention analogue cited: {analogue_label}",
            analogue_label in note,
        )

    # ---- Option C reclassification ----
    check("A1 amplitude ratio reclassified", "A1" in note and "amplitude ratio" in note)
    check("P1 eigenvalue->mass map reclassified", "P1" in note and ("eigenvalue" in note or "mass map" in note))
    check("delta phase reclassified", ("δ" in note or "delta" in note.lower()) and "phase" in note)
    check("v_0 scale reclassified", "v_0" in note and "scale" in note)
    check(
        "reclassified as parameter/readout targets",
        "parameter/readout" in note and "C_3` must be broken" in note,
    )

    # ---- audit hygiene: no empirical loading ----
    # We only flag *explicit numerical mass values* used as derivation input.
    # Disclaimers like "forbids using PDG values" are expected and welcome.
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
        "explicitly disclaims PDG-input use",
        "does not load-bear PDG" in note or "not derivation input" in note,
    )

    # ---- forbidden promotions ----
    forbidden_promotions = [
        ("AC closure by declaration", "AC" + "_" + r".*is\s+closed"),
        ("bridge-gap count zero", r"bridge-gap admission count\s*(?:is|=|moves)\s*0"),
        ("specific param promoted to retained", r"A1\s+is\s+(now\s+)?retained"),
    ]
    for label, pattern in forbidden_promotions:
        check(
            f"forbidden promotion absent: {label}",
            re.search(pattern, note, flags=re.IGNORECASE | re.DOTALL) is None,
        )
    check(
        "species/readout bridge remains explicit",
        "species/readout" in note and "readout bridge" in note,
    )
    check(
        "three-state carrier not species closure",
        "three-state carrier" in note and "completed species/readout" in note,
    )

    # ---- retained provenance cross-references ----
    for ref in [
        "STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM",
        "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE",
        "MINIMAL_AXIOMS_2026-05-03",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE",
    ]:
        check(f"cross-references retained note: {ref}", ref in note)

    for route_ref in ["A3_ROUTE1", "A3_ROUTE2", "A3_ROUTE3", "A3_ROUTE4", "A3_ROUTE5"]:
        check(f"cross-references A3 obstruction: {route_ref}", route_ref in note)

    check("cross-references Option C decomposition", "A3_OPTION_C_BRANNEN_RIVERO" in note)

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
    check("review-loop rule present", "Review-loop rule" in note or "review-loop rule" in note.lower())

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Preserved-C_3 interpretation check passed: "
        "C_3 on hw=1 is preserved, mass-ordering labels are conventions, "
        "Option C parameter/readout targets remain bounded, no new axiom."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
