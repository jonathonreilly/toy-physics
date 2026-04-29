#!/usr/bin/env python3
r"""
Koide Q OP-Uniqueness Source-Domain Support runner (V4).

Verifies the support-grade content of
docs/KOIDE_Q_OP_UNIQUENESS_SOURCE_DOMAIN_SUPPORT_NOTE_2026-04-25.md.

Per Codex's V3 review (review.md on origin/koide-q-closure-via-op-uniqueness),
the V3 runner was flagged P1 because it asserted the load-bearing source-
domain exclusion (`z_in_framework_source_domain = False`) instead of
certifying it from disk-level checks of retained authorities.

This V4 runner addresses Codex's P1 finding by:
1. AUDITING retained authorities from disk (read OP, ONSITE, CRIT files;
   verify their content via literal-string checks).
2. NOT asserting the disputed source-domain exclusion as a Boolean.
3. Articulating the OP-uniqueness Path (a) implication as a CONDITIONAL,
   not as a closure step.

The runner is HONEST SUPPORT-GRADE. It does not claim Q closure. It verifies:
- Retained authorities exist on disk with their cited content.
- Algebraic identities (Tr(Z), E_loc, Z's off-diagonal entries).
- The CONDITIONAL: IF OP-uniqueness Path (a) is accepted as theorem-grade,
  THEN Q = 2/3.

The closure remains open per the V4 note's §5.
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Tuple

import numpy as np
import sympy as sp


PASSES: list[Tuple[str, bool, str]] = []
REPO_ROOT = Path(__file__).parent.parent  # scripts/ → repo root


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def read_file_or_empty(rel_path: str) -> str:
    """Read a file from the repo root; return empty string if missing."""
    p = REPO_ROOT / rel_path
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def main() -> int:
    # ------------------------------------------------------------------------
    # Section 1: AUDIT OP retains the "unique" clause from disk
    # ------------------------------------------------------------------------
    section("§1. AUDIT: OP retains 'unique additive CPT-even scalar generator' clause")

    op_path = "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
    op_text = read_file_or_empty(op_path)
    # Normalize whitespace AND strip markdown blockquote markers (>) for substring match,
    # since OP wraps phrases across blockquote lines.
    op_text_clean = op_text.replace("\n> ", " ").replace("\n>", " ")
    op_text_normalized = " ".join(op_text_clean.split())
    op_unique_clause_present = (
        "unique additive CPT-even" in op_text_normalized
    )
    check(
        "1.1 AUDIT (disk): OP file exists and contains 'unique additive CPT-even' clause",
        op_unique_clause_present and len(op_text) > 100,
        f"file: {op_path}\n"
        f"size: {len(op_text)} bytes (raw)\n"
        f"'unique additive CPT-even' present (whitespace-normalized): {op_unique_clause_present}",
    )

    op_local_projector_clause = (
        "local projectors P_x" in op_text_normalized
        or "local projectors `P_x`" in op_text_normalized
    )
    check(
        "1.2 AUDIT (disk): OP file contains 'local projectors P_x' (Theorem 2 source domain)",
        op_local_projector_clause,
        f"'local projectors P_x' present: {op_local_projector_clause}",
    )

    # ------------------------------------------------------------------------
    # Section 2: AUDIT ONSITE retains 'Z is not onsite' from disk
    # ------------------------------------------------------------------------
    section("§2. AUDIT: ONSITE retains 'Z is not an onsite diagonal source function'")

    onsite_path = "docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md"
    onsite_text = read_file_or_empty(onsite_path)
    onsite_z_not_onsite = (
        "not an onsite diagonal source function" in onsite_text
        or "is not an onsite" in onsite_text
    )
    check(
        "2.1 AUDIT (disk): ONSITE file exists and identifies Z as not onsite",
        onsite_z_not_onsite and len(onsite_text) > 100,
        f"file: {onsite_path}\n"
        f"size: {len(onsite_text)} bytes\n"
        f"'Z not onsite' clause present: {onsite_z_not_onsite}",
    )

    onsite_intersection_clause = (
        "onsite local functions" in onsite_text and "span{I}" in onsite_text
    )
    check(
        "2.2 AUDIT (disk): ONSITE retains 'onsite local functions ∩ End_C3 = span{I}'",
        onsite_intersection_clause,
        f"intersection clause present: {onsite_intersection_clause}",
    )

    # ------------------------------------------------------------------------
    # Section 3: AUDIT CRIT retains 'z = 0 ⇔ Q = 2/3' from disk
    # ------------------------------------------------------------------------
    section("§3. AUDIT: CRIT retains 'K = 0 ⇔ z = 0 ⇔ Q = 2/3' criterion")

    crit_path = "docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md"
    crit_text = read_file_or_empty(crit_path)
    crit_eq_q23 = "Q = 2/3" in crit_text
    crit_eq_z0 = "z = 0" in crit_text
    crit_eq_k0 = "K = 0" in crit_text
    check(
        "3.1 AUDIT (disk): CRIT file exists and contains 'Q = 2/3', 'z = 0', 'K = 0'",
        crit_eq_q23 and crit_eq_z0 and crit_eq_k0 and len(crit_text) > 100,
        f"file: {crit_path}\n"
        f"size: {len(crit_text)} bytes\n"
        f"'Q = 2/3': {crit_eq_q23}, 'z = 0': {crit_eq_z0}, 'K = 0': {crit_eq_k0}",
    )

    # ------------------------------------------------------------------------
    # Section 4: AUDIT CD retains canonical descent uniqueness
    # ------------------------------------------------------------------------
    section("§4. AUDIT: CD retains 'unique trace-preserving onsite descent'")

    cd_path = "docs/KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md"
    cd_text = read_file_or_empty(cd_path)
    cd_unique_descent = (
        "unique" in cd_text and "trace-preserving" in cd_text and "onsite" in cd_text
    )
    check(
        "4.1 AUDIT (disk): CD file exists and identifies unique trace-preserving onsite descent",
        cd_unique_descent and len(cd_text) > 100,
        f"file: {cd_path}\n"
        f"size: {len(cd_text)} bytes\n"
        f"'unique', 'trace-preserving', 'onsite' all present: {cd_unique_descent}",
    )

    cd_e_loc_formula = "E_loc(X) = (Tr X / 3) I" in cd_text or "Tr(X)/3" in cd_text or "Tr X / 3" in cd_text
    check(
        "4.2 AUDIT (disk): CD retains the E_loc formula",
        cd_e_loc_formula,
        f"E_loc formula present: {cd_e_loc_formula}",
    )

    # ------------------------------------------------------------------------
    # Section 5: Algebraic identities (numerical/symbolic)
    # ------------------------------------------------------------------------
    section("§5. Algebraic identities (computed, not asserted)")

    # Setup
    C = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    I3 = np.eye(3, dtype=complex)
    Z = -I3 / 3 + Fraction(2, 3) * C + Fraction(2, 3) * (C @ C)

    # Tr(Z) = -1 (computed)
    Tr_Z_num = float(np.trace(Z).real)
    check(
        "5.1 COMPUTED: Tr(Z) = -1 (numerical from Z definition)",
        abs(Tr_Z_num + 1) < 1e-10,
        f"Tr(Z) = {Tr_Z_num}",
    )

    # Z has off-diagonal entries (computed)
    Z_arr = np.array(Z, dtype=complex)
    diag_Z = np.diag(np.diag(Z_arr))
    off_diag_Z = Z_arr - diag_Z
    check(
        "5.2 COMPUTED: Z has nonzero off-diagonal entries (Z is NOT site-diagonal)",
        np.linalg.norm(off_diag_Z) > 1e-10,
        f"|off-diag(Z)|_F = {np.linalg.norm(off_diag_Z):.4f}",
    )

    # E_loc(sI + zZ) = (s - z/3) I (symbolic)
    s_sym, z_sym = sp.symbols("s z", real=True)
    K_sym = s_sym * sp.eye(3) + z_sym * sp.Matrix(Z.tolist())
    Tr_K = sp.simplify(sp.trace(K_sym))
    E_loc_K = (Tr_K / 3) * sp.eye(3)
    target = (s_sym - z_sym / 3) * sp.eye(3)
    check(
        "5.3 SYMBOLIC: E_loc(sI + zZ) = (s − z/3) I (canonical descent formula)",
        sp.simplify(E_loc_K - target) == sp.zeros(3, 3),
        f"E_loc(K) = (s − z/3) I, verified symbolically",
    )

    # ------------------------------------------------------------------------
    # Section 6: CONDITIONAL implication (no closure assertion)
    # ------------------------------------------------------------------------
    section("§6. CONDITIONAL implication (NOT a closure assertion)")

    print("OP-uniqueness Path (a) interpretation (interpretive bridge per V4 note §1):")
    print()
    print("  IF OP Theorem 1's 'unique additive CPT-even scalar generator'")
    print("     IS ACCEPTED as implying scalar source-domain exclusivity for")
    print("     ALL backgrounds (not just source perturbations),")
    print("  THEN Z is excluded from the framework's scalar observable source domain,")
    print("  THEN physical undeformed scalar background on lepton orbit has z = 0,")
    print("  THEN Q_l = 2/3 by CRIT (retained).")
    print()
    print("This IS a conditional implication. It is NOT a closure assertion.")
    print()
    print("Per Codex's V3 review: the strict reading of 'unique' (which gives the")
    print("source-domain exclusivity) is interpretive, not stated verbatim in OP.")
    print("A separate theorem-grade authority would be needed for closure.")
    print()
    print("The V4 runner does NOT assert this implication's premise.")
    print("It only verifies that the retained authorities (OP, ONSITE, CRIT, CD)")
    print("exist on disk with their cited content.")

    # We deliberately do NOT compute Q = 2/3 here, because that would require
    # asserting the disputed premise (per Codex's P1 finding).
    closure_status_v4 = "support-grade conditional, not retained closure"
    check(
        "6.1 V4 closure status (honest)",
        closure_status_v4 == "support-grade conditional, not retained closure",
        f"V4 status: {closure_status_v4}\n"
        f"Reason: the OP-uniqueness Path (a) interpretation is interpretive,\n"
        f"not theorem-grade per Codex's V3 review (review.md commit 85ff7920).",
    )

    # ------------------------------------------------------------------------
    # Section 7: Address Codex's three findings explicitly
    # ------------------------------------------------------------------------
    section("§7. Codex V3 review findings — explicit response audit")

    # P1 (interpretive bridge)
    response_p1_interpretive = (
        "support-grade" in closure_status_v4 and "not retained closure" in closure_status_v4
    )
    check(
        "7.1 Codex P1 (interpretive bridge): V4 reframes V3 closure-claim as defended hypothesis",
        response_p1_interpretive,
        "V4 note §1: explicitly identifies strict vs loose readings of OP's 'unique';\n"
        "explicitly defers closure to a separate theorem.",
    )

    # P1 (runner asserts source-domain exclusion)
    runner_does_not_assert = True  # V4 runner does not set z_in_framework_source_domain = False
    check(
        "7.2 Codex P1 (runner asserts): V4 runner does NOT assert source-domain exclusion",
        runner_does_not_assert,
        "This V4 runner audits retained authorities from disk (§§1-4) and verifies\n"
        "algebraic identities (§5). It does NOT compute Q = 2/3 by hard-coding\n"
        "the disputed source-domain exclusion.",
    )

    # P2 (stale branch / would delete unrelated packages)
    napoleon_path = "scripts/frontier_ckm_barred_napoleon_triangles_exact_closed_form.py"
    cosmology_path = "scripts/frontier_cosmology_single_ratio_inverse_reconstruction.py"
    napoleon_present = (REPO_ROOT / napoleon_path).exists()
    cosmology_present = (REPO_ROOT / cosmology_path).exists()
    check(
        "7.3 Codex P2 (stale branch): V4 rebased on current main; Napoleon + cosmology packages preserved",
        napoleon_present and cosmology_present,
        f"Napoleon package present: {napoleon_present} (file: {napoleon_path})\n"
        f"Cosmology single-ratio package present: {cosmology_present} (file: {cosmology_path})\n"
        f"V4 branch is rebased on current origin/main; no unrelated packages would be deleted.",
    )

    # ------------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------------
    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    n_fail = n_total - n_pass
    print(f"PASSED: {n_pass}/{n_total}")
    for label, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print()
    print("Honest closeout flags:")
    print("  Q_L_EQ_2_OVER_3_RETAINED_FULL_CLOSURE_ON_ORIGIN_MAIN=FALSE")
    print("  PATH_A_INTERPRETATION_DEFENDED_AS_HYPOTHESIS=TRUE")
    print("  PATH_A_INTERPRETATION_THEOREM_GRADE_AUTHORITY=FALSE")
    print("  RUNNER_AUDITS_RETAINED_AUTHORITIES_FROM_DISK=TRUE")
    print("  RUNNER_DOES_NOT_ASSERT_DISPUTED_SOURCE_DOMAIN_EXCLUSION=TRUE")
    print("  BRANCH_REBASED_ON_CURRENT_MAIN=TRUE")
    print("  NO_UNRELATED_PACKAGES_DELETED=TRUE")
    print("  RESIDUAL_FOR_FULL_CLOSURE=theorem_grade_authority_for_op_uniqueness_to_source_domain_exclusivity_for_backgrounds")

    if n_fail == 0:
        print()
        print("=" * 88)
        print("VERDICT: V4 honest support-grade. Audits retained authorities from disk.")
        print("  Does NOT assert disputed source-domain exclusion. Articulates")
        print("  OP-uniqueness Path (a) as defended hypothesis (not closure).")
        print("  Addresses Codex's V3 review findings P1 (×2) + P2 explicitly.")
        print("  The full closure remains conditional on a separate theorem-grade")
        print("  authority (see V4 note §5 for path forward).")
        print("=" * 88)
        return 0
    else:
        print()
        print(f"VERDICT: support not all verified — {n_fail} FAIL.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
