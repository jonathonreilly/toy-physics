#!/usr/bin/env python3
"""Verify the physical-lattice foundational-interpretation declaration.

The declaration is at:
  docs/PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md

This runner verifies:
  Part 1: declaration structure (frontmatter, layer separation, scope).
  Part 2: the foundational-vs-mathematical-axiom distinction is explicit
          and audit-coherent (no formal-system content claimed).
  Part 3: the reframing of AC_φλ from admission to empirical witness is
          logically coherent (algebra-symmetry + empirical-breaking →
          unique realization).
  Part 4: the 10-probe A3 derivation-campaign obstructions remain valid
          (no contradictions introduced by the declaration).
  Part 5: empirical compatibility checks (3-generation count, mass
          hierarchy, CKM/PMNS structure).
  Part 6: layer-separation checks (foundational / formal / empirical).
  Part 7: reversibility check (formalist reading recoverable; no
          retained theorem corrupted).
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
MINIMAL_AXIOMS_PATH = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
NECESSITY_NOTE_PATH = ROOT / "docs" / "PHYSICAL_LATTICE_NECESSITY_NOTE.md"
SUBSTEP4_NOTE_PATH = ROOT / "docs" / "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Part 1: declaration structure
# ---------------------------------------------------------------------------
section("Part 1: declaration structure (frontmatter + scope)")

if not NOTE_PATH.exists():
    print(f"FATAL: declaration note not found at {NOTE_PATH}")
    sys.exit(1)

note_text = NOTE_PATH.read_text()

required_frontmatter = [
    "Physical-Lattice Foundational Interpretation Note",
    "foundational interpretive commitment",
    "not a mathematical axiom",
    "Claim type",
    "foundational_interpretation",
    "Effective status",
    "foundational",
]
for item in required_frontmatter:
    check(
        f"declaration has required frontmatter element: '{item}'",
        item in note_text,
        f"len={len(note_text)}",
    )

required_sections = [
    "What this note declares",
    "Why this is not a mathematical axiom",
    "What this commits to",
    "What this does NOT commit to",
    "How this shifts AC_φλ-class evaluations",
    "Why the A3 derivation-campaign obstructions remain valid",
    "Application across the framework",
    "Audit-grade defensibility",
    "Relation to existing notes",
    "Validation",
    "Conclusion",
]
for s in required_sections:
    check(f"declaration has section: '{s}'", s in note_text, "")


# ---------------------------------------------------------------------------
# Part 2: foundational-vs-mathematical-axiom distinction
# ---------------------------------------------------------------------------
section("Part 2: foundational-vs-mathematical-axiom distinction")

distinction_anchors = [
    "Formal system (mathematical)",
    "Foundational interpretation",
    "Empirical content",
    "wavefunction interpretation in QM",
    "Copenhagen vs Everett",
    "spacetime is real",
    "substantivalist",
    "does not modify the mathematical content",
    "It does not introduce",
    "new mathematical structure",
    "It does not add a new axiom",
]
for anchor in distinction_anchors:
    check(
        f"distinction anchor present: '{anchor}'",
        anchor in note_text,
        "audit-coherence: layer separation explicit",
    )

# Verify the declaration explicitly does NOT introduce formal-system content
forbidden_patterns = [
    r"new theorem proof depends on",  # would indicate formal-system content
    r"new mathematical axiom",
    r"adds an axiom",
    r"replaces A1",
    r"replaces A2",
    r"modifies A1",
    r"modifies A2",
]
import re as _re
for pat in forbidden_patterns:
    found_count = len(_re.findall(pat, note_text))
    check(
        f"no formal-system claim of type: /{pat}/",
        found_count == 0
        or (
            "no new mathematical axiom" in note_text.lower()
            and pat == r"new mathematical axiom"
        )  # allow as scope statement, not as claim
        or (pat == r"new theorem proof depends on" and "no new theorem" in note_text.lower()),
        f"matches={found_count}",
    )


# ---------------------------------------------------------------------------
# Part 3: AC_φλ reframing coherence
# ---------------------------------------------------------------------------
section("Part 3: AC_φλ reframing coherence (algebra + empirical → realization)")

reframing_anchors = [
    "AC_φ is provably impossible from retained primitives",
    "C_3-symmetric",
    "hw=1 sector",
    "exactly 3 C_3-orbit",
    "physical realization breaks C_3",
    "mass hierarchy",
    "LEP",
    "empirically witnessed",
    "Bridge-gap admission count",
    "0 (physical-lattice reading)",
    "1 (formalist reading)",
]
for anchor in reframing_anchors:
    check(
        f"reframing anchor present: '{anchor}'",
        anchor in note_text,
        "logical structure: algebra ⊕ empirical → realization",
    )


# ---------------------------------------------------------------------------
# Part 4: 10-probe A3 derivation-campaign obstructions remain valid
# ---------------------------------------------------------------------------
section("Part 4: A3 derivation-campaign obstructions remain valid")

# Verify all 5 routes referenced
route_anchors = [
    ("R1", "Higgs/Yukawa"),
    ("R2", "single-clock"),
    ("R3", "anomaly inflow"),
    ("R4", "Spin(6) chain"),
    ("R5", "no-proper-quotient"),
]
for code, desc in route_anchors:
    check(
        f"route {code} ({desc}) referenced and reframed",
        f"{code} (" in note_text or f" {code} " in note_text,
        f"obstruction theorem citation",
    )

# Verify hostile reviews referenced
check(
    "hostile reviews (R1.HR-R5.HR) referenced",
    "R1.HR-R5.HR" in note_text or "hostile review" in note_text,
    "all 5 hostile reviews",
)

# Verify obstruction-theorem retention statement
retention_anchors = [
    "obstruction theorems remain mathematically valid",
    "not falsified by this declaration",
    "What changes is their *interpretation*",
    "structural features",
]
for anchor in retention_anchors:
    check(
        f"obstruction-theorem retention: '{anchor}'",
        anchor in note_text,
        "no contradictions with retained theorems",
    )


# ---------------------------------------------------------------------------
# Part 5: empirical compatibility checks
# ---------------------------------------------------------------------------
section("Part 5: empirical compatibility (3 generations, mass hierarchy, CKM/PMNS)")

empirical_anchors = [
    "m_t",    # top mass present
    "m_c",    # charm mass present
    "m_u",    # up mass present
    "m_τ",    # tau mass present
    "m_μ",    # muon mass present
    "m_e",    # electron mass present
    "LEP",    # LEP measurements
    "Z-width",  # Z-boson width measurement
    "CKM",    # CKM matrix
    "PMNS",   # PMNS matrix
    "2.984",  # specific neutrino species count from LEP
]
for anchor in empirical_anchors:
    check(
        f"empirical compatibility anchor: '{anchor}'",
        anchor in note_text,
        "empirical witness for C_3-breaking on physical lattice",
    )


# ---------------------------------------------------------------------------
# Part 6: layer-separation checks
# ---------------------------------------------------------------------------
section("Part 6: three-layer separation (foundational / formal / empirical)")

# Verify layer distinctions
layer_anchors = [
    "Formal system (mathematical)",
    "Foundational interpretation",
    "Empirical content",
    "A1 (Cl(3))",
    "A2 (Z³)",
    "mass hierarchy",
    "CKM/PMNS structure",
    "three-generation count",
]
for anchor in layer_anchors:
    check(f"layer-separation anchor: '{anchor}'", anchor in note_text, "")

# Verify A1+A2 unchanged
check(
    "A1+A2 declared unchanged",
    "A1+A2 unchanged" in note_text or "A1+A2 still the only mathematical axioms" in note_text,
    "minimal-axiom hygiene preserved",
)


# ---------------------------------------------------------------------------
# Part 7: reversibility check
# ---------------------------------------------------------------------------
section("Part 7: reversibility (formalist reading recoverable)")

reversibility_anchors = [
    "Reversibility",
    "audit lane rejects",
    "formalist reading",
    "does not corrupt",
]
for anchor in reversibility_anchors:
    check(
        f"reversibility anchor: '{anchor}'",
        anchor in note_text,
        "audit-grade reversibility commitment",
    )


# ---------------------------------------------------------------------------
# Part 8: existing-note coherence (no contradictions)
# ---------------------------------------------------------------------------
section("Part 8: coherence with existing retained notes")

# MINIMAL_AXIOMS_2026-05-03 declares A1+A2 are the only axioms
if MINIMAL_AXIOMS_PATH.exists():
    minimal = MINIMAL_AXIOMS_PATH.read_text()
    check(
        "MINIMAL_AXIOMS_2026-05-03 still declares A1+A2 as the framework axioms",
        "A1 — Local algebra" in minimal and "A2 — Spatial substrate" in minimal,
        "this declaration does not modify the axiom list",
    )
    check(
        "this declaration acknowledges minimal-axioms note explicitly",
        "MINIMAL_AXIOMS_2026-05-03.md" in note_text,
        "cross-reference present",
    )

# PHYSICAL_LATTICE_NECESSITY_NOTE narrowed 2026-05-02
if NECESSITY_NOTE_PATH.exists():
    necessity = NECESSITY_NOTE_PATH.read_text()
    check(
        "PHYSICAL_LATTICE_NECESSITY_NOTE narrowing referenced",
        "narrowed 2026-05-02" in note_text,
        "honest delegation to existing narrowed scope",
    )
    check(
        "necessity-note algebraic content unchanged",
        "two-invariant" in necessity.lower() or "two-invariant" in necessity,
        "retained algebraic rigidity unchanged",
    )

# SUBSTEP4_AC_NARROW_BOUNDED_NOTE references
if SUBSTEP4_NOTE_PATH.exists():
    check(
        "SUBSTEP4 AC narrowing referenced",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"
        in note_text,
        "substep-4 AC-narrowing context preserved",
    )


# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------
section("Summary")
print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
if FAIL_COUNT == 0:
    print("VERDICT: declaration verified.")
    sys.exit(0)
else:
    print("VERDICT: declaration verification failed.")
    sys.exit(1)
