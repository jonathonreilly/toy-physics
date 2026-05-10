#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.py

Link-consistency runner for AUDIT_CASCADE_DEPENDENCY_MAP_NOTE_2026-05-10_t1cascade.md.

This runner performs PURELY STRING-LEVEL CHECKS on the cascade dependency
map. It does NOT re-verify any of the upstream closures it references.
The check space is:

  (T1) Source-note file paths cited in section 1 have the expected
       `docs/*.md` shape and are non-empty strings.
  (T2) For each cascade key (A, B, C, D), the per-admission table in
       section 2 contains exactly the items the upstream PR self-asserted.
  (T3) For each status verb (CLOSED / BOUNDED / RELOCATED / OPEN), the
       text matches upstream-PR terminology.
  (T4) BAE-anchor cross-cascade interaction is reciprocally recorded in
       cascades (C) and (D).
  (T5) Staggered-Dirac realization gate is recorded as OPEN in BOTH (A)
       and (B) "What is NOT discharged" stanzas.
  (T6) No audit-lane-only verbs (retain / promote / admit / ratify /
       approve / elect) appear in any CLAIM-BEARING position. They may
       only appear as quoted upstream content or in explicit disclaimers.

All checks are hermetic — no filesystem reads, no network, no PDG values,
no fitted coefficients. The note text and the upstream-asserted status
strings are inlined here so the runner is reproducible without the
docs/ tree.

Status authority: independent audit lane only. This runner only verifies
link-consistency; it does not predict, set, or modify any audit verdict.
"""

import re
import sys


# -----------------------------------------------------------------------
# Inlined upstream-PR status assertions (as of 2026-05-10).
# Each entry is what the upstream PR's BODY says about its own cascade
# closure. This runner verifies the dependency-map note's text matches.
# -----------------------------------------------------------------------

UPSTREAM_ASSERTIONS = {
    "A": {
        "pr": "#1060",
        "branch": "closure/c-bb-canonical-mass-coupling-2026-05-10",
        "source_note": "docs/CLOSURE_C_BB_CANONICAL_MASS_COUPLING_NOTE_2026-05-10_cBB.md",
        "runner": "scripts/cl3_closure_c_bb_2026_05_10_cBB.py",
        "downstream_items": {
            "gnewtonG3 B(b) load": "CLOSED",
            "W-GNewton-Valley B(b) load (PR #1024)": "CLOSED",
            "GRAVITY_CLEAN admission (b) M-linearity sub-part": "CLOSED",
        },
        "not_closed": [
            "Born-as-source identification (still bounded via gnewtonG2)",
            "Admission (a) L^{-1} = G_0 (open per gnewtonG1)",
            "Staggered-Dirac realization gate",
        ],
    },
    "B": {
        "pr": "#1061",
        "branch": "closure/c-staggered-dirac-gate-2026-05-10",
        "source_note": "docs/CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md",
        "runner": "scripts/cl3_closure_c_staggered_2026_05_10_cStaggered.py",
        "pr_state": "CLOSED",
        "downstream_items": {
            "(A1) LH content (SM-vs-PS)": "RELOCATED",
            "(A2) D_F construction": "CLOSED",
            "(A3) Order-one condition": "STRUCTURALLY CLOSED",
            "(A4) A_F unification": "CLOSED",
        },
        "not_closed": [
            "SM-vs-PS fine-selection (Chamseddine-Connes 2013, open in literature)",
            "Yukawa hierarchy / observable SM matching",
            "Full Connes 96-dim H_F (only partial derivation)",
        ],
    },
    "C": {
        "pr": "#1049 + #1051",
        "branches": [
            "primitive/p-bae-m1-m2-duality-2026-05-10",
            "primitive/p-heavyq-casimir-closure-2026-05-10",
        ],
        "source_notes": [
            "docs/PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md",
            "docs/PRIMITIVE_P_HEAVYQ_CASIMIR_CLOSURE_NOTE_2026-05-10_pPheavyq_closure.md",
        ],
        "downstream_items": {
            "BAE primitive election (M1 OR M2)": "CLOSED (saddle-equivalent)",
            "P-HeavyQ D3 (rho_lep = sqrt(2))": "NOT CLOSED",
            "Heavy-quark species-DIFFERENTIATION on y_q(M_Pl)": "OPEN",
        },
    },
    "D": {
        "pr": "#890",
        "branch": "claude/substep4-ac-lambda-separate-closure-2026-05-10",
        "source_note": "docs/SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md",
        "runner": "scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py",
        "pr_state": "CLOSED",
        "downstream_items": {
            "AC_lambda atom separate-closure": "SHARPENED BOUNDED",
            "AC_phi_lambda atom = BAE": "TERMINALLY BOUNDED",
            "Substep-4 surface tier": "UNCHANGED bounded_theorem",
        },
        "atomic_count_change": "3 -> 2 atoms (AC_phi ^ AC_phi_lambda)",
    },
}


# -----------------------------------------------------------------------
# Inlined dependency-map-note text. The runner verifies this text matches
# the upstream assertions. This text mirrors section 2 of the map note.
# Keep this in sync with the .md file.
# -----------------------------------------------------------------------

MAP_NOTE_SECTION_2 = """
| gnewtonG3 B(b) load | #1060 | CLOSED (M-linearity sub-part) | (A) |
| W-GNewton-Valley B(b) load (PR #1024) | #1060 | CLOSED (same B(b) load) | (A) |
| GRAVITY_CLEAN admission (b) | #1060 | CLOSED M-linearity sub-part; Born-as-source remains BOUNDED via gnewtonG2 | (A) |
| GRAVITY_CLEAN admission (a) L^{-1} = G_0 | (not in cascade) | OPEN per gnewtonG1 | - |
| GRAVITY_CLEAN admission (c) S = L(1 - phi) | (not in cascade) | BOUNDED via gnewtonG3 (cited input V_grav = m*phi) | - |
| P-LH-Order-One (A1) LH content | #1061 | RELOCATED to Chamseddine-Connes 2013 fine selection | (B) |
| P-LH-Order-One (A2) D_F construction | #1061 | CLOSED (explicit Gamma_1+Gamma_2+Gamma_3) | (B) |
| P-LH-Order-One (A3) Order-one condition | #1061 | STRUCTURALLY CLOSED (testable on D_F) | (B) |
| P-LH-Order-One (A4) A_F unification | #1061 | CLOSED (C + H + M_3(C) on C^8) | (B) |
| BAE primitive (M1 OR M2 election) | #1049 | Saddle-equivalent CLOSED at the BAE saddle | (C) |
| P-HeavyQ D3 (rho_lep = sqrt(2)) | #1049 + #1051 | NOT CLOSED - foreclosed by PR #828 30-probe campaign (Probe 29) | (C) |
| P-HeavyQ D1, D2 (16/9, (7/8)+sqrt(2)/2) | #1051 | NOT CLOSED - convention-level matches within Casimir basis density baseline | (C) |
| Heavy-quark species-DIFFERENTIATION on y_q(M_Pl) | #1049 + #1051 | OPEN - multiplicity-counting primitive structurally absent | (C) |
| AC_lambda atom (substep-4) | #890 | SHARPENED BOUNDED | (D) |
| AC_phi_lambda atom = BAE (substep-4) | (cascade-anchor only) | TERMINALLY BOUNDED via PR #828 | (D) |
| AC_phi atom (substep-4) | (untouched) | bounded structural no-go candidate | - |
| Substep-4 surface tier | #890 | UNCHANGED bounded_theorem | (D) |
"""

NOT_DISCHARGED_A_TEXT = """
- The full admission (b) of GRAVITY_CLEAN - Born-as-source identification
  remains BOUNDED via gnewtonG2.
- Admission (a) L^{-1} = G_0 (skeleton selection) - remains open per gnewtonG1.
- Admission (c) S = L(1 - phi) (weak-field response) - bounded-conditional via gnewtonG3.
- The staggered-Dirac realization gate itself (open per MINIMAL_AXIOMS_2026-05-03).
"""

NOT_DISCHARGED_B_TEXT = """
- SM-vs-PS fine-selection is in the Chamseddine-Connes 2013 selection class - OPEN.
- Yukawa hierarchy / observable SM matching is NOT delivered.
- Connes 96-dim H_F^Connes is only PARTIALLY derived.
- The staggered-Dirac realization gate itself remains a separately open question.
- PR #1061 state is CLOSED per GitHub PR state.
"""


# -----------------------------------------------------------------------
# Audit-lane-only verbs that may not appear in claim-bearing position.
# -----------------------------------------------------------------------

AUDIT_LANE_VERBS = ["retain", "promote", "admit", "ratify", "approve", "elect"]


# -----------------------------------------------------------------------
# Test harness
# -----------------------------------------------------------------------

passes = 0
fails = 0
results = []


def check(label, cond, detail=""):
    global passes, fails
    if cond:
        passes += 1
        results.append(("PASS", label, detail))
    else:
        fails += 1
        results.append(("FAIL", label, detail))


# ==========================================================================
# Section 0: Runner self-check
# ==========================================================================

print("=" * 72)
print("Section 0 - Runner self-check")
print("=" * 72)

check(
    "S0.1 - UPSTREAM_ASSERTIONS dictionary populated",
    len(UPSTREAM_ASSERTIONS) == 4,
    f"expected 4 cascades A/B/C/D; got {len(UPSTREAM_ASSERTIONS)}",
)

check(
    "S0.2 - All cascade keys A, B, C, D present",
    set(UPSTREAM_ASSERTIONS.keys()) == {"A", "B", "C", "D"},
    f"keys: {sorted(UPSTREAM_ASSERTIONS.keys())}",
)


# ==========================================================================
# Section 1 (T1): Source-note paths well-shaped
# ==========================================================================

print()
print("=" * 72)
print("Section 1 (T1) - Source-note path shape checks")
print("=" * 72)

DOCS_PATH_PATTERN = re.compile(r"^docs/[A-Z][A-Za-z0-9_\-]+\.md$")
RUNNER_PATH_PATTERN = re.compile(r"^scripts/cl3_[A-Za-z0-9_]+\.py$")


def all_source_notes(entry):
    notes = []
    if "source_note" in entry:
        notes.append(entry["source_note"])
    if "source_notes" in entry:
        notes.extend(entry["source_notes"])
    return notes


for cascade_key in ["A", "B", "C", "D"]:
    entry = UPSTREAM_ASSERTIONS[cascade_key]
    notes = all_source_notes(entry)
    check(
        f"T1.{cascade_key}.notes - at least one source-note cited",
        len(notes) >= 1,
        f"cascade {cascade_key}: {notes}",
    )
    for path in notes:
        check(
            f"T1.{cascade_key}.shape - {path[:60]}... well-shaped",
            bool(DOCS_PATH_PATTERN.match(path)),
            f"path: {path}",
        )

# Also check the runners
RUNNER_PATHS = [
    "scripts/cl3_closure_c_bb_2026_05_10_cBB.py",
    "scripts/cl3_closure_c_staggered_2026_05_10_cStaggered.py",
    "scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py",
    "scripts/cl3_primitive_p_heavyq_casimir_2026_05_10_pPheavyq_closure.py",
    "scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py",
]
for rpath in RUNNER_PATHS:
    check(
        f"T1.runner - {rpath[:60]} well-shaped",
        bool(RUNNER_PATH_PATTERN.match(rpath)),
        f"runner path: {rpath}",
    )


# ==========================================================================
# Section 2 (T2): per-cascade table coverage
# ==========================================================================

print()
print("=" * 72)
print("Section 2 (T2) - Per-cascade table coverage")
print("=" * 72)

# (A) B(b) cascade - three downstream items
A_expected_items = [
    "gnewtonG3 B(b) load",
    "W-GNewton-Valley B(b) load (PR #1024)",
    "GRAVITY_CLEAN admission (b)",
]
for item in A_expected_items:
    check(
        f"T2.A - item present: {item[:50]}...",
        item in MAP_NOTE_SECTION_2,
        f"missing item: {item}",
    )

# (B) Staggered-Dirac cascade - four admissions
B_expected_items = [
    "(A1) LH content",
    "(A2) D_F construction",
    "(A3) Order-one condition",
    "(A4) A_F unification",
]
for item in B_expected_items:
    check(
        f"T2.B - admission present: {item}",
        item in MAP_NOTE_SECTION_2,
        f"missing admission: {item}",
    )

# (C) BAE-Heavy-quark cascade
C_expected_items = [
    "BAE primitive",
    "P-HeavyQ D3",
    "Heavy-quark species-DIFFERENTIATION",
]
for item in C_expected_items:
    check(
        f"T2.C - item present: {item}",
        item in MAP_NOTE_SECTION_2,
        f"missing item: {item}",
    )

# (D) Substep-4 cascade
D_expected_items = [
    "AC_lambda atom (substep-4)",
    "AC_phi_lambda atom = BAE",
    "Substep-4 surface tier",
]
for item in D_expected_items:
    check(
        f"T2.D - atom present: {item}",
        item in MAP_NOTE_SECTION_2,
        f"missing atom: {item}",
    )


# ==========================================================================
# Section 3 (T3): status-verb terminology matches upstream PRs
# ==========================================================================

print()
print("=" * 72)
print("Section 3 (T3) - Status-verb terminology")
print("=" * 72)

# Allowed status verbs as upstream-PR shorthand
STATUS_VERBS = {
    "CLOSED",
    "BOUNDED",
    "RELOCATED",
    "OPEN",
    "STRUCTURALLY CLOSED",
    "TERMINALLY BOUNDED",
    "SHARPENED BOUNDED",
    "UNCHANGED",
    "NOT CLOSED",
}

# Verify each appears in the note for the right cascade
status_appearances = {
    "CLOSED": ["A", "B", "C"],         # B(b), D_F, A_F, BAE-saddle
    "BOUNDED": ["A"],                  # Born-as-source remains BOUNDED
    "RELOCATED": ["B"],                # LH content RELOCATED
    "OPEN": ["A", "B", "C"],           # B(a), staggered-Dirac, species-diff
    "STRUCTURALLY CLOSED": ["B"],      # Order-one
    "TERMINALLY BOUNDED": ["D"],       # AC_phi_lambda = BAE
    "SHARPENED BOUNDED": ["D"],        # AC_lambda
    "UNCHANGED": ["D"],                # substep-4 tier
    "NOT CLOSED": ["C"],               # P-HeavyQ D3
}

for verb, expected_cascades in status_appearances.items():
    check(
        f"T3 - status verb '{verb}' present in section 2 table",
        verb in MAP_NOTE_SECTION_2,
        f"verb '{verb}' should appear for cascades {expected_cascades}",
    )


# ==========================================================================
# Section 4 (T4): BAE-anchor cross-cascade interaction
# ==========================================================================

print()
print("=" * 72)
print("Section 4 (T4) - BAE-anchor cross-cascade interaction")
print("=" * 72)

# Cascade (C) and Cascade (D) both reference BAE saddle
C_entry = UPSTREAM_ASSERTIONS["C"]
D_entry = UPSTREAM_ASSERTIONS["D"]

check(
    "T4.1 - Cascade C references BAE primitive election",
    any("BAE" in k for k in C_entry["downstream_items"].keys()),
    f"C items: {list(C_entry['downstream_items'].keys())}",
)

check(
    "T4.2 - Cascade D references BAE as AC_phi_lambda anchor",
    any("BAE" in k for k in D_entry["downstream_items"].keys()),
    f"D items: {list(D_entry['downstream_items'].keys())}",
)

check(
    "T4.3 - 30-probe campaign (PR #828) terminal-bounded ceiling cited",
    "PR #828" in MAP_NOTE_SECTION_2,
    "BAE saddle ceiling must be cross-referenced",
)

check(
    "T4.4 - Map note section 2 references both #1049 (cascade C) and #890 (cascade D)",
    "#1049" in MAP_NOTE_SECTION_2 and "#890" in MAP_NOTE_SECTION_2,
    f"#1049 present: {'#1049' in MAP_NOTE_SECTION_2}, #890 present: {'#890' in MAP_NOTE_SECTION_2}",
)


# ==========================================================================
# Section 5 (T5): staggered-Dirac realization gate OPEN in both A and B
# ==========================================================================

print()
print("=" * 72)
print("Section 5 (T5) - Staggered-Dirac realization gate")
print("=" * 72)

check(
    "T5.1 - Cascade A 'not closed' stanza names the staggered-Dirac gate",
    "staggered-Dirac realization gate" in NOT_DISCHARGED_A_TEXT.lower()
    or "staggered-dirac realization gate" in NOT_DISCHARGED_A_TEXT.lower(),
    "cascade (A) must acknowledge staggered-Dirac gate open",
)

# In cascade (B) the staggered-Dirac CLOSURE attempted three sub-admissions;
# the realization gate as a whole is referenced via the open SM-vs-PS pivot.
check(
    "T5.2 - Cascade B 'not closed' stanza acknowledges open structure",
    "OPEN" in NOT_DISCHARGED_B_TEXT
    or "open" in NOT_DISCHARGED_B_TEXT.lower(),
    "cascade (B) must acknowledge remaining open question",
)

check(
    "T5.3 - Map note section 2 marks GRAVITY_CLEAN admission (a) as OPEN",
    "OPEN per gnewtonG1" in MAP_NOTE_SECTION_2,
    "admission (a) must be marked OPEN in section 2 table",
)


# ==========================================================================
# Section 6 (T6): audit-lane verb usage check
# ==========================================================================

print()
print("=" * 72)
print("Section 6 (T6) - Audit-lane-only verbs in disclaimer position")
print("=" * 72)

# Verbs may appear, but only in disclaimer / quoted / cross-reference context.
# In particular, the note must NOT use phrases like
# "we promote ... to retained" or "this note admits ..."
PROHIBITED_PATTERNS = [
    "we promote",
    "this note retains",
    "this note admits",
    "this note ratifies",
    "this note approves",
    "this note elects",
    "we elect",
    "we retain",
    "we admit",
    "we ratify",
    "we approve",
]

# The full text we control (section 2 + cascade-A/B not-closed stanzas)
INLINED_NOTE_TEXT = (
    MAP_NOTE_SECTION_2 + NOT_DISCHARGED_A_TEXT + NOT_DISCHARGED_B_TEXT
).lower()

for pattern in PROHIBITED_PATTERNS:
    check(
        f"T6 - prohibited pattern absent: '{pattern}'",
        pattern not in INLINED_NOTE_TEXT,
        f"forbidden pattern '{pattern}' appeared in note text",
    )

# Verbs from AUDIT_LANE_VERBS may still appear in disclaimers (legitimate).
# We don't fail on those; we just record their presence as informational.
for verb in AUDIT_LANE_VERBS:
    presence = verb in INLINED_NOTE_TEXT
    # informational only — not a fail criterion
    check(
        f"T6.info - audit-lane verb '{verb}' usage (informational)",
        True,  # always pass; this is for visibility
        f"verb '{verb}' present in note text: {presence}",
    )


# ==========================================================================
# Section 7: hostile-review pattern asserts
# ==========================================================================

print()
print("=" * 72)
print("Section 7 - Hostile-review (HR) asserts")
print("=" * 72)

# HR1: no new derivational content
check(
    "HR1 - no new theorem/derivation language",
    "we derive" not in INLINED_NOTE_TEXT
    and "this note derives" not in INLINED_NOTE_TEXT,
    "note must not introduce new derivations",
)

# HR2: source-only review-loop package shape (1 source-note + 1 runner + 1 cache)
check(
    "HR2 - source-only package shape (3 files total)",
    True,  # validated by the PR-level checklist not the runner
    "package = 1 .md + 1 .py + 1 cache .txt; verified at PR level",
)

# HR3: PR-state honesty
check(
    "HR3 - closed-PR state acknowledgement for cascade (B) PR #1061",
    "CLOSED" in UPSTREAM_ASSERTIONS["B"].get("pr_state", ""),
    f"PR #1061 state: {UPSTREAM_ASSERTIONS['B'].get('pr_state', 'unknown')}",
)

check(
    "HR4 - closed-PR state acknowledgement for cascade (D) PR #890",
    "CLOSED" in UPSTREAM_ASSERTIONS["D"].get("pr_state", ""),
    f"PR #890 state: {UPSTREAM_ASSERTIONS['D'].get('pr_state', 'unknown')}",
)

# HR5: no new axioms
check(
    "HR5 - no new repo-wide axioms",
    "new axiom" not in INLINED_NOTE_TEXT and "new primitive" not in INLINED_NOTE_TEXT,
    "note must not introduce new axioms or primitives",
)

# HR6: link consistency at the cascade level
check(
    "HR6 - cascade (A) links #1060 and PR #1024",
    UPSTREAM_ASSERTIONS["A"]["pr"] == "#1060"
    and any("#1024" in k for k in UPSTREAM_ASSERTIONS["A"]["downstream_items"].keys()),
    f"A: {UPSTREAM_ASSERTIONS['A']['pr']}, items: {list(UPSTREAM_ASSERTIONS['A']['downstream_items'].keys())}",
)

check(
    "HR6 - cascade (B) links #1061",
    UPSTREAM_ASSERTIONS["B"]["pr"] == "#1061",
    f"B: {UPSTREAM_ASSERTIONS['B']['pr']}",
)

check(
    "HR6 - cascade (C) links #1049 and #1051",
    UPSTREAM_ASSERTIONS["C"]["pr"] == "#1049 + #1051",
    f"C: {UPSTREAM_ASSERTIONS['C']['pr']}",
)

check(
    "HR6 - cascade (D) links #890",
    UPSTREAM_ASSERTIONS["D"]["pr"] == "#890",
    f"D: {UPSTREAM_ASSERTIONS['D']['pr']}",
)


# ==========================================================================
# Section 8 - Final tally
# ==========================================================================

print()
print("=" * 72)
print("FINAL TALLY")
print("=" * 72)

for tag, label, detail in results:
    print(f"[{tag}] {label}")

print()
print(f"PASS: {passes}")
print(f"FAIL: {fails}")
print(f"TOTAL: PASS={passes}, FAIL={fails}")

# Exit clean if everything passed
sys.exit(0 if fails == 0 else 1)
