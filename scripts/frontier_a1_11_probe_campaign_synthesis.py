#!/usr/bin/env python3
"""Check the Koide A1 eleven-probe campaign synthesis meta note.

This runner is a review-hygiene check, not a physics proof. It verifies
that the synthesis note:

  - is classified as meta and does not declare pipeline status;
  - cross-references the retained foundational notes (MINIMAL_AXIOMS,
    PHYSICAL_LATTICE_FOUNDATIONAL, C3_SYMMETRY_PRESERVED,
    STAGGERED_DIRAC_SUBSTEP4_AC_NARROW);
  - cross-references each of the eleven probe source notes by filename;
  - cites all eleven PR numbers (#727, #730, #731, #732, #733, #734,
    #735, #736, #737, #738, #740);
  - names the missing primitive consistently with the canonical phrase
    "(1,1)-multiplicity-weighted Frobenius pairing on M_3(C)_Herm under
    C_3-isotype decomposition";
  - states the 3:6 structural-locus argument;
  - does not claim A1-condition closure or add a new axiom;
  - does not promote any downstream theorem or write an audit verdict;
  - does not load-bear PDG numerical mass values as derivation input.

It is the paired runner for the synthesis meta note and follows the
reviewer's salvaged-runner pattern (frontier_c3_symmetry_preserved_*,
frontier_physical_lattice_foundational_*).
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
PHYSICAL_LATTICE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
C3_PRESERVED = ROOT / "docs" / "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md"
SUBSTEP4 = ROOT / "docs" / "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"

# Probe source-note filenames that are on main as of campaign close.
ON_MAIN_PROBE_NOTES = [
    "KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md",
    "KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md",
    "KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md",
    "KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md",
    "KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md",
    "KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md",
    "KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md",
    "KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md",
    "KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md",
    "KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md",
]

# Probe 7 source-note filename — open PR (#740), on a separate branch.
PROBE7_NOTE = "KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md"

# All eleven PR numbers cited.
ELEVEN_PR_NUMBERS = ["#727", "#730", "#731", "#732", "#733", "#734",
                     "#735", "#736", "#737", "#738", "#740"]

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
        (NOTE, "eleven-probe campaign synthesis note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
        (PHYSICAL_LATTICE, "physical-lattice baseline note"),
        (C3_PRESERVED, "preserved-C_3 interpretation note"),
        (SUBSTEP4, "substep-4 AC narrowing note"),
    ]:
        if not path.exists():
            print(f"missing {label}: {path}")
            return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Koide A1 eleven-probe campaign synthesis check")
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

    # ---- foundational cross-references ----
    for ref in [
        "MINIMAL_AXIOMS_2026-05-03",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac",
    ]:
        check(f"cross-references retained foundational note: {ref}", ref in note)

    # ---- C_3 / circulant retained provenance ----
    for ref in [
        "STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07",
        "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18",
        "CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE",
    ]:
        check(f"cross-references retained provenance: {ref}", ref in note)

    # ---- per-probe cross-references (10 on-main notes by filename) ----
    for probe_note in ON_MAIN_PROBE_NOTES:
        check(f"cross-references probe note: {probe_note}", probe_note in note)
        # Also confirm the file exists on this branch (sanity check).
        check(
            f"probe note file exists on this branch: {probe_note}",
            (ROOT / "docs" / probe_note).exists(),
        )

    # ---- Probe 7 cross-reference (file is on its own branch; only filename cited) ----
    check(f"cross-references probe-7 note (open PR): {PROBE7_NOTE}", PROBE7_NOTE in note)

    # ---- eleven PR numbers cited ----
    for pr in ELEVEN_PR_NUMBERS:
        check(f"cites PR {pr}", pr in note)
    check(
        "cites exactly the eleven distinct PR numbers",
        len({pr for pr in ELEVEN_PR_NUMBERS if pr in note}) == 11,
    )

    # ---- missing-primitive named consistently ----
    primitive_phrase = (
        "(1,1)`-multiplicity-weighted Frobenius pairing on\n"
        "> `M_3(ℂ)_Herm` under `C_3`-isotype decomposition"
    )
    check(
        "missing primitive named precisely (canonical phrase)",
        primitive_phrase in note,
    )
    check(
        "missing primitive language uses 'multiplicity-weighted Frobenius pairing'",
        "multiplicity-weighted Frobenius pairing" in note,
    )
    check(
        "missing primitive references C_3-isotype decomposition",
        "C_3`-isotype decomposition" in note,
    )
    check(
        "missing primitive references M_3(C)_Herm",
        "M_3(ℂ)_Herm" in note,
    )

    # ---- 3:6 structural-locus argument ----
    check(
        "states 3:6 multiplicity ratio structural locus",
        "3 : 6" in note or "3:6" in note,
    )
    check(
        "states algebraic equivalence 3a^2 = 6|b|^2",
        "3 · a²  =  6 · |b|²" in note or "3a² = 6|b|²" in note,
    )
    check(
        "isotype decomposition stated explicitly",
        "trivial-character isotype" in note and "non-trivial-character" in note,
    )
    check(
        "Probe 7 §8 corroboration cited",
        "Probe 7 §8" in note,
    )
    check(
        "Route D weight-class corroboration cited",
        "Route D" in note and "weight-class" in note,
    )
    check(
        "Probe 1 Frobenius reduction-map corroboration cited",
        "Probe 1" in note and ("Frobenius" in note),
    )

    # ---- audit-honest options ----
    check(
        "Option (a) admit-as-axiom enumerated",
        "Option (a)" in note and "admit" in note,
    )
    check(
        "Option (b) further-probe enumerated",
        "Option (b)" in note and ("derive the primitive" in note or "research target" in note),
    )
    check(
        "Option (c) pivot-to-other-bridge enumerated",
        "Option (c)" in note and "pivot" in note.lower(),
    )
    check(
        "no option selected by this note",
        "NOT TAKEN" in note and "OPEN" in note and "NEUTRAL" in note,
    )

    # ---- forbidden promotions / closure claims ----
    forbidden_promotions = [
        ("AC closure by declaration", "AC" + "_" + r".*is\s+closed"),
        ("A1 condition closed", r"A1[- ]condition\s+is\s+(now\s+)?closed"),
        ("missing primitive admitted", r"missing primitive\s+is\s+(now\s+)?admitted"),
        # Match positive declarations only (e.g. "we add a new axiom"); skip
        # negated policy lines like "No new axiom is added."
        ("new axiom added", r"(?<!no\s)(?<!not\s)\bwe\s+add\s+a\s+new\s+axiom\b"),
        ("bridge-gap admission count zero", r"bridge-gap admission count\s*(?:is|=|moves)\s*0"),
    ]
    for label, pattern in forbidden_promotions:
        check(
            f"forbidden promotion absent: {label}",
            re.search(pattern, note, flags=re.IGNORECASE | re.DOTALL) is None,
        )

    # ---- explicit "does NOT do" guarantees ----
    check(
        "explicit: does not admit primitive as axiom",
        "Admit the primitive as a new axiom" in note or "no mathematical axiom is" in note.lower() or "No mathematical axiom is\n   added" in note,
    )
    check(
        "explicit: does not derive A1-condition",
        "Derive the A1-condition" in note,
    )
    check(
        "explicit: does not modify any retained theorem",
        "Modify any retained theorem" in note,
    )
    check(
        "explicit: A1+A2 still suffice",
        "A1+A2 still suffice" in note,
    )
    check(
        "explicit: no PDG values as derivation input",
        "PDG" in note and "not load-bear" in note.lower() or "does not load-bear PDG" in note.lower(),
    )

    # ---- audit hygiene: no PDG numerical mass values inserted ----
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

    # ---- naming-collision warning present ----
    check("naming-collision warning present (framework axiom A1 vs A1-condition)",
          "framework axiom A1" in note and "A1-condition" in note)

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

    # ---- terminal-state language ----
    check(
        "campaign declared terminal / converged",
        "converged" in note and "terminal" in note,
    )
    check(
        "structural obstruction language",
        "STRUCTURAL OBSTRUCTION" in note or "structural obstruction" in note.lower(),
    )

    print()
    print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    if FAIL:
        return 1
    print(
        "Eleven-probe campaign synthesis check passed: terminal state recorded, "
        "missing primitive named precisely (canonical (1,1)-multiplicity-weighted "
        "Frobenius pairing on M_3(C)_Herm under C_3-isotype decomposition), "
        "no closure claimed, no axiom added, no theorem promoted."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
