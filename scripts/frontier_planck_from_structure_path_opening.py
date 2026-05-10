#!/usr/bin/env python3
"""Check the Planck-from-structure path-opening synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis:
  - is classified as meta and does not declare pipeline status;
  - cross-references the four source-note proposals (#874-#877);
  - cross-references the prior-round wins (#845, #857, #790, #836, #729, #725);
  - states the "path-opening, not closure" framing explicitly;
  - enumerates the conditionalities explicitly (P1+P2+P3 audit, substep-4 ratchet,
    G_Newton's three admissions);
  - records the G_Newton three named admissions (B(a), B(b), B(c));
  - lists the strategic options without selecting among them;
  - does not promote any source theorem or audit row;
  - does not add a new repo-wide axiom;
  - does not load PDG values as derivation input;
  - cross-references foundational notes that exist on main.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md"
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
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1
    if not MINIMAL_AXIOMS.exists():
        print(f"missing minimal axioms note: {MINIMAL_AXIOMS}")
        return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Planck-from-structure path-opening synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta type", "**Type:** meta" in note)
    check("synthesis note is meta claim_type", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    check(
        "does not declare pipeline status",
        effective_token not in note and audit_clean_token not in note,
    )
    check(
        "authority disclaimer present",
        "Authority disclaimer" in note
        and "source-note proposal" in note
        and "audit lane" in note.lower(),
    )

    # ---- four source-note cross-references (this round) ----
    round_prs = [
        ("#877", "P1 substrate-to-carrier forcing"),
        ("#876", "P2 hidden-character delta=0"),
        ("#874", "P3 orientation principle"),
        ("#875", "P4 G_Newton self-consistency"),
    ]
    for pr, label in round_prs:
        check(f"this-round PR cross-reference: {pr} ({label})", pr in note)

    # ---- prior-round PRs combined into the path-opening ----
    prior_prs = [
        ("#845", "C-iso epsilon_witness closure"),
        ("#857", "SU(3) NNLO/N5LO closed-form rationals"),
        ("#790", "BAE rename"),
        ("#836", "30-probe BAE terminal synthesis"),
        ("#729", "conventions-unification companion"),
        ("#725", "physical-lattice foundational interpretation"),
    ]
    for pr, label in prior_prs:
        check(f"prior-round PR cross-reference: {pr} ({label})", pr in note)

    # ---- "path-opening, not closure" framing ----
    check(
        "path-opening framing stated explicitly",
        "path-opening" in note.lower(),
    )
    check(
        "path-opening contrasted with closure",
        "path-opening, not closure" in note.lower()
        or "path-opening" in note.lower()
        and "not closure" in note.lower(),
    )

    # ---- conditionalities enumerated ----
    check(
        "conditional on audit ratification of P1+P2+P3",
        "audit ratification" in note.lower()
        and ("P1+P2+P3" in note or ("P1" in note and "P2" in note and "P3" in note)),
    )
    check(
        "conditional on substep-4 ratchet",
        "substep-4" in note
        and ("ratchet" in note.lower() or "closure of the substep-4" in note.lower()),
    )
    check(
        "conditional on G_Newton three admissions",
        "three named admissions" in note.lower()
        or "three admissions" in note.lower(),
    )

    # ---- G_Newton three named admissions recorded ----
    check(
        "G_Newton admission B(a) skeleton-selection recorded",
        "B(a)" in note and "skeleton-selection" in note.lower(),
    )
    check(
        "G_Newton admission B(b) Born-as-source recorded",
        "B(b)" in note and "Born-as-source" in note,
    )
    check(
        "G_Newton admission B(c) valley-linear recorded",
        "B(c)" in note and "valley-linear" in note.lower(),
    )

    # ---- already-named admissions preserved ----
    check(
        "BAE admission preserved (unchanged by this round)",
        "BAE" in note and "bounded" in note.lower(),
    )
    check(
        "P (radian bridge) admission preserved",
        "radian bridge" in note.lower(),
    )

    # ---- strategic options listed without selection ----
    check(
        "strategic options listed (>=3 options)",
        "Attack the substep-4 ratchet" in note
        and ("Attack G_Newton" in note or "G_Newton" in note)
        and ("engineering-side" in note.lower() or "engineering frontier" in note.lower()),
    )
    check(
        "synthesis does not select option",
        "does not select" in note.lower()
        and ("audit lane has authority" in note.lower()
             or "audit-lane authority" in note.lower()),
    )

    # ---- audit-honest framing: what it did NOT do ----
    check(
        "explicit list of what round did NOT do",
        "What the round did NOT do" in note or "What this round did not do" in note,
    )
    check(
        "no theorem promotion stated",
        "Promote any source note" in note or "no theorem promotion" in note.lower()
        or "does not promote" in note.lower(),
    )
    check(
        "no repo-wide axiom added stated",
        "Add a new repo-wide axiom" in note
        or "no new repo-wide axiom" in note.lower()
        or "No new repo-wide axiom" in note,
    )
    check(
        "no admission count aggregation",
        "does not aggregate" in note.lower()
        or "single composite count" in note.lower()
        or "single number" in note.lower(),
    )

    # ---- forbidden-input boundary preserved ----
    check(
        "no PDG-as-input claim preserved",
        "No PDG observed values" in note
        or "PDG values" in note and "not load-bearing" in note,
    )
    check(
        "substep-4 AC narrowing rule preserved",
        "substep-4 AC narrowing" in note.lower()
        or "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE" in note,
    )

    # ---- the four PR-level proposed claim types ----
    check(
        "P1 (#877) proposed as bounded_theorem",
        "bounded_theorem" in note and "#877" in note,
    )
    check(
        "P2 (#876) proposed as positive_theorem",
        "positive_theorem" in note and "#876" in note,
    )
    check(
        "P3 (#874) proposed as bounded_theorem",
        "bounded_theorem" in note and "#874" in note,
    )
    check(
        "P4 (#875) proposed as bounded sharpening (not closure)",
        "bounded sharpening" in note.lower()
        and ("not full closure" in note.lower() or "not full" in note.lower()),
    )

    # ---- the import-surface table is present (path-opening claim) ----
    check(
        "pre-round import surface table present",
        "Pre-round count" in note or "pre-round count" in note.lower(),
    )
    check(
        "conditional post-round import surface table present",
        "Conditional post-round count" in note
        or "conditional post-round count" in note.lower(),
    )
    check(
        "conventional scale anchor row addressed",
        "conventional scale anchor" in note.lower()
        or "Conventional scale anchor" in note,
    )

    # ---- cross-references to foundational notes that exist on main ----
    foundational_refs = [
        "MINIMAL_AXIOMS_2026-05-03",
        "PHYSICAL_LATTICE_NECESSITY_NOTE",
        "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09",
        "CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08",
        "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09",
    ]
    for ref in foundational_refs:
        check(f"cross-references foundational note: {ref}", ref in note)

    # ---- baseline alignment with MINIMAL_AXIOMS_2026-05-03 ----
    check(
        "minimal axioms note records physical Cl(3) local algebra",
        "the physical local algebra is `Cl(3)`" in minimal,
    )
    check(
        "minimal axioms note records physical Z^3 spatial substrate",
        "the physical spatial substrate is the cubic" in minimal,
    )
    check(
        "synthesis honors the physical Cl(3)/Z^3 baseline",
        "physical `Cl(3)`" in note and "`Z^3`" in note
        and "No new repo-wide axiom" in note,
    )

    # ---- review-loop rule ----
    check(
        "review-loop rule for future branches present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )
    check(
        "review-loop rule notes synthesis is conditional",
        "remain conditional" in note.lower()
        or "remains conditional" in note.lower()
        or "if any of P1+P2+P3 is rejected" in note,
    )

    # ---- "What this note is NOT" boundary list ----
    check(
        "What this note is NOT section present",
        "What this note is NOT" in note,
    )
    check(
        "explicit no closure claim",
        "Not a claim that Planck-from-structure is closed" in note,
    )

    print()
    print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    if FAIL:
        return 1
    print(
        "Planck-from-structure path-opening synthesis check passed: "
        "all four this-round source proposals cross-referenced, prior-round wins "
        "cross-referenced, path-opening framing stated, conditionalities "
        "enumerated, G_Newton three admissions recorded, no theorem "
        "promotion, no repo-wide axiom added, strategic options listed without "
        "selection."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
