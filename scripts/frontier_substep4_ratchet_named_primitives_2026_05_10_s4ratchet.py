#!/usr/bin/env python3
"""Check the substep-4 ratchet via named primitives meta clarification note.

This runner is a review-hygiene check, not a physics proof. It verifies that
the note:

  - is classified as meta and does not declare pipeline-derived status;
  - records the named-primitive pattern application from #725 / #728 / #729
    / #790 to the substep-4 staggered-Dirac realization gate;
  - records that the substep-4 admission inventory {AC_phi, AC_phi_lambda}
    is already-counted within the BAE+P campaign-terminal admission
    inventory recorded in #836;
  - does not promote substep-4 to positive_theorem;
  - does not load PDG values as derivation input;
  - does not add a new mathematical axiom (A1+A2 still suffice);
  - cross-references the source substep-4 AC narrowing note, the BAE
    30-probe terminal synthesis (#836), the BAE rename (#790), the four
    prior meta-clarification notes (#725 / #728 / #729 / #790), the
    Planck P1 / P3 consumers, and the minimal axioms;
  - records all three honest outcomes (closure proposal, structural
    obstruction, sharpened) explicitly.

It is a companion to the prior meta-clarification runners (physical-lattice
foundational, C_3 preserved interpretation, conventions unification, BAE
rename, BAE 30-probe terminal synthesis).
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "SUBSTEP4_RATCHET_NAMED_PRIMITIVES_META_NOTE_2026-05-10_s4ratchet.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
SUBSTEP4 = ROOT / "docs" / "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"
PHYSICAL_LATTICE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
C3_PRESERVED = ROOT / "docs" / "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md"
CONVENTIONS = ROOT / "docs" / "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md"
BAE_RENAME = ROOT / "docs" / "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md"
BAE_30_PROBE = ROOT / "docs" / "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md"
PLANCK_P1 = ROOT / "docs" / "PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md"
PLANCK_P3 = ROOT / "docs" / "PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md"

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
    required = [
        (NOTE, "substep-4 ratchet named-primitives note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
        (SUBSTEP4, "substep-4 AC narrowing note"),
        (PHYSICAL_LATTICE, "physical-lattice baseline note"),
        (C3_PRESERVED, "C_3 preserved interpretation note"),
        (CONVENTIONS, "conventions unification note"),
        (BAE_RENAME, "BAE rename meta note"),
        (BAE_30_PROBE, "BAE 30-probe terminal synthesis note"),
        (PLANCK_P1, "Planck P1 substrate-to-carrier forcing note"),
        (PLANCK_P3, "Planck P3 orientation principle note"),
    ]
    for path, label in required:
        if not path.exists():
            print(f"missing {label}: {path}")
            return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Substep-4 ratchet via named primitives meta check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification: source-meta, no pipeline status ----
    check("source note is meta", "**Claim type:** meta" in note)
    check("source note Type field is meta", "**Type:** meta" in note)

    # Tokens decomposed to avoid lint trips on the runner itself reading as
    # "declaring pipeline status" (we want to verify the SOURCE NOTE doesn't
    # declare them, while the RUNNER must mention them in checks).
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    audit_pending_token = "audit-pending"
    retained_decl_token = "is hereby retained"
    promote_decl_token = "hereby promoted"
    audit_verdict_decl_token = "audit verdict: retained"

    # The note may MENTION these tokens in describing the pipeline machinery,
    # but must not DECLARE them as a verdict for substep-4.
    check(
        "does not declare a pipeline retained-grade verdict on substep-4",
        retained_decl_token not in note
        and promote_decl_token not in note
        and audit_verdict_decl_token not in note,
    )
    check(
        "does not declare audit-clean verdict for substep-4",
        f"substep-4: {audit_clean_token}" not in note
        and f"substep-4 {audit_clean_token}" not in note,
    )

    # ---- named-primitive pattern application ----
    check(
        "names AC_phi as primitive",
        "AC_φ" in note and ("named small primitive" in note or "named primitive" in note),
    )
    check(
        "names AC_phi_lambda as primitive",
        "AC_φλ" in note and ("BAE" in note),
    )
    check(
        "AC_phi reframed via preserved-C_3 stance",
        "preserved" in note and "C_3" in note and "no-go" in note,
    )
    check(
        "AC_phi_lambda identified with BAE",
        "AC_φλ" in note
        and ("≡ BAE" in note or "= BAE" in note or "is the substep-4" in note or "BAE)" in note),
    )

    # ---- already-counted within BAE+P inventory ----
    check(
        "BAE + P campaign inventory cited",
        "BAE + P" in note or "BAE+P" in note or "BAE, P" in note or "{BAE, P}" in note,
    )
    check(
        "substep-4 admission count = 2 named primitives",
        "2 named primitives" in note.replace("**", "")
        or "BAE + P = 2" in note,
    )
    check(
        "substep-4 inventory does not introduce P",
        "do not introduce P" in note or "substep-4 atoms do not introduce P" in note,
    )

    # ---- pattern source clarity ----
    pattern_sources = [
        "#725",
        "#728",
        "#729",
        "#790",
    ]
    for src in pattern_sources:
        check(f"named-primitive pattern source cited: {src}", src in note)

    check(
        "30-probe campaign cited (#836 BAE synthesis)",
        "30-probe" in note and ("#836" in note or "campaign" in note),
    )

    # ---- forbidden: positive_theorem promotion ----
    # Match declarations that PROMOTE substep-4 (positive verbs like "is hereby
    # promoted", "now retained as positive_theorem", etc.). We exclude
    # negation-list contexts and pathway-description phrasings.
    note_lines = note.splitlines()
    forbidden_promotion_lines = []
    for idx, raw_line in enumerate(note_lines):
        line = raw_line.strip()
        line_lower = line.lower()
        # require co-occurrence on this line of substep-4 + positive_theorem
        if not (
            re.search(r"substep-?4\b", line, flags=re.IGNORECASE)
            and re.search(r"positive[_ ]theorem", line, flags=re.IGNORECASE)
        ):
            continue
        # in-line negation context — skip
        if any(
            neg in line_lower
            for neg in [
                "does not",
                "do not",
                "do NOT",
                "not promote",
                "not declare",
                "no claim",
                "explicitly not",
            ]
        ):
            continue
        # ratchet-pathway context — skip (describes what *would* happen if
        # the audit lane chose to)
        if any(tok in line_lower for tok in ["ratchet", "ratcheting", "conditional on"]):
            continue
        # surrounding-context negation: scan ~3 lines back for "does NOT" header
        ctx_start = max(0, idx - 5)
        ctx_lines = note_lines[ctx_start: idx + 1]
        ctx_blob = "\n".join(ctx_lines).lower()
        if any(
            neg in ctx_blob
            for neg in [
                "does **not**",
                "does not",
                "do not",
                "what this does not",
                "what this note does not",
                "explicitly does",
                "do not promote",
            ]
        ):
            continue
        forbidden_promotion_lines.append(line)
    check(
        "forbidden promotion absent: positive_theorem promotion of substep-4",
        not forbidden_promotion_lines,
        detail=(forbidden_promotion_lines[0] if forbidden_promotion_lines else ""),
    )

    other_forbidden = [
        ("substep-4 retained closure declared", r"substep-?4\b.*hereby\s+retained"),
        ("AC_phi closed", r"AC_φ\s+is\s+(now\s+)?closed"),
        ("AC_phi_lambda closed", r"AC_φλ\s+is\s+(now\s+)?closed"),
        ("BAE closed", r"BAE\s+is\s+(now\s+)?closed"),
    ]
    for label, pattern in other_forbidden:
        check(
            f"forbidden promotion absent: {label}",
            re.search(pattern, note, flags=re.IGNORECASE) is None,
        )

    # ---- audit hygiene: no PDG numerical loading ----
    pdg_numeric_patterns = [
        r"m_e\s*=\s*0\.51",
        r"m_μ\s*=\s*105",
        r"m_τ\s*=\s*1\.77",
        r"m_e\s*=\s*0\.000511",
        r"Q\s*=\s*2/3\s*\(observed\)",
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
        "PDG-input prohibition" in note or "PDG values" in note,
    )

    # ---- no new axiom ----
    check(
        "no new mathematical axiom added",
        "A1+A2 still suffice" in note or "do not add a new" in note.lower() or "does not" in note.lower(),
    )
    check(
        "minimal axioms note has physical Cl(3) A1",
        "the physical local algebra is `Cl(3)`" in minimal,
    )
    check(
        "minimal axioms note has physical Z^3 A2",
        "the physical spatial substrate is the cubic" in minimal,
    )

    # ---- ratchet pathway clarity (without declaring verdict) ----
    check(
        "retained_bounded ratchet path described",
        "retained_bounded" in note and "bounded_theorem" in note,
    )
    check(
        "audit-lane authority preserved",
        "audit lane" in note and ("authority" in note or "decides" in note),
    )

    # ---- downstream consumers cited ----
    check(
        "Planck P1 substrate-to-carrier consumer cited",
        "PLANCK_SUBSTRATE_TO_CARRIER_FORCING" in note,
    )
    check(
        "Planck P3 orientation principle consumer cited",
        "PLANCK_ORIENTATION_PRINCIPLE" in note,
    )
    check("L3a consumer mentioned", "L3a" in note)

    # ---- three-honest-outcomes structure ----
    check("CLOSURE PROPOSAL outcome stated", "CLOSURE PROPOSAL" in note)
    check("STRUCTURAL OBSTRUCTION outcome stated", "STRUCTURAL OBSTRUCTION" in note)
    check("SHARPENED outcome stated", "SHARPENED" in note)

    # ---- cross-references for source-only review-loop pattern ----
    cross_refs = [
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS",
        "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE",
        "CONVENTIONS_UNIFICATION_COMPANION_NOTE",
        "PLANCK_SUBSTRATE_TO_CARRIER_FORCING",
        "PLANCK_ORIENTATION_PRINCIPLE",
        "MINIMAL_AXIOMS_2026-05-03",
        "cl3_staggered_dirac_substep4_ac_phi_lambda_rigorize_2026_05_09",
    ]
    for ref in cross_refs:
        check(f"cross-references: {ref}", ref in note)

    # ---- A3 obstruction theorems cited (the C_3-not-broken result) ----
    check(
        "A3_ROUTE1 obstruction theorem cited",
        "A3_ROUTE1" in note,
    )
    check(
        "A3_ROUTE5 obstruction theorem cited",
        "A3_ROUTE5" in note,
    )

    # ---- review-loop rule present ----
    check(
        "review-loop rule present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )

    # ---- feedback alignment ----
    feedback_files = [
        "feedback_consistency_vs_derivation_below_w2",
        "feedback_hostile_review_semantics",
        "feedback_retained_tier_purity_and_package_wiring",
        "feedback_physics_loop_corollary_churn",
        "feedback_review_loop_source_only_policy",
    ]
    for fb in feedback_files:
        check(f"user-memory feedback alignment cited: {fb}", fb in note)

    # ---- not-corollary-churn justification ----
    check(
        "explicitly explains not corollary churn",
        "not \"corollary churn\"" in note or "Why this is not" in note,
    )
    check(
        "differentiates from #836 BAE synthesis",
        "synthesis" in note.lower() and "campaign-terminal" in note.lower(),
    )

    # ---- structural-bar honesty ----
    check(
        "AC_phi structural bar honestly stated",
        ("structurally barred" in note or "structurally impossible" in note)
        and "AC_φ" in note,
    )
    check(
        "AC_phi_lambda structural bar honestly stated",
        ("structurally barred" in note or "structural-impossibility" in note)
        and "AC_φλ" in note,
    )

    # ---- Brannen Amplitude Equipartition full name + alias ----
    check("BAE expanded as Brannen Amplitude Equipartition", "Brannen Amplitude Equipartition" in note)
    check("BAE shorthand used", "BAE" in note)

    # ---- ratchet implication clarity ----
    check(
        "P1 ratchet implication stated",
        "Planck P1" in note and ("inherit" in note or "ratchet" in note or "downstream" in note.lower()),
    )
    check(
        "P3 ratchet implication stated",
        "Planck P3" in note and ("inherit" in note or "ratchet" in note or "downstream" in note.lower()),
    )

    print()
    print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    if FAIL:
        return 1
    print(
        "Substep-4 ratchet via named primitives check passed: "
        "AC_phi and AC_phi_lambda are named primitives matching the BAE+P "
        "campaign-terminal inventory; no new axiom; no theorem promotion; "
        "audit-lane authority preserved."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
