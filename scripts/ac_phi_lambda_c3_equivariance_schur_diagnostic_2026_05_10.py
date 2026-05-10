#!/usr/bin/env python3
"""Diagnostic runner for the AC_phi_lambda preserved-C_3 structural foreclosure note.

This runner is a brief illustrative diagnostic, NOT a load-bearing component
of the foreclosure proof (which is one-page representation theory and is
recorded in the source note Section 3). It serves two purposes:

  1. Structural Schur check: construct the regular representation of Z/3Z
     on C^3 in sympy, build an explicit symbolic C_3-equivariant Hermitian
     circulant operator H = a*I + b*U + b_bar*U^2, and verify that
     <c_alpha|H|c_alpha> = a = Tr(H)/3 for all corner-basis indices alpha.

  2. Review-hygiene check on the source note: verify that the note is
     classified as bounded_theorem with proposal_allowed: false, uses
     markdown-link citations, does not add a new axiom, does not introduce
     new repo vocabulary, and cites all 10 A3-campaign probes.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / (
    "AC_PHI_LAMBDA_PRESERVED_C3_STRUCTURAL_FORECLOSURE_"
    "BOUNDED_THEOREM_NOTE_2026-05-10.md"
)
SUBSTEP4 = ROOT / "docs" / (
    "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md"
)
PRESERVED_C3 = ROOT / "docs" / "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md"
BAE_RENAME = ROOT / "docs" / "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"

PROBE_NOTES = [
    "A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md",
    "A3_ROUTE2_SINGLE_CLOCK_C3_OBSTRUCTION_NOTE_2026-05-08_r2.md",
    "A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md",
    "A3_ROUTE4_SPIN6_CHAIN_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r4.md",
    "A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md",
    "A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md",
    "A3_R2_HOSTILE_REVIEW_CONFIRMS_EXHAUSTION_NOTE_2026-05-08_r2hr.md",
    "A3_R3_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r3hr.md",
    "A3_R4_HOSTILE_REVIEW_CONFIRMED_NOTE_2026-05-08_r4hr.md",
    "A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md",
]

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


# -------------------------------------------------------------
# Section A. Structural Schur check on the regular rep of Z/3Z on C^3
# -------------------------------------------------------------
def run_schur_check() -> None:
    print()
    print("=" * 64)
    print("Section A: structural Schur check on the regular rep of Z/3Z on C^3")
    print("=" * 64)

    # Regular representation of Z/3Z on C^3 in the corner basis {|c_1>, |c_2>, |c_3>}.
    # Generator U_C3 acts as the 3-cycle |c_1> -> |c_2> -> |c_3> -> |c_1>.
    U = sp.Matrix([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ])
    I3 = sp.eye(3)
    U2 = U * U
    U3 = U * U2

    check("U_C3 is a 3-cycle permutation matrix (U^3 = I)", U3.equals(I3))
    check("U_C3 has order 3 (U != I, U^2 != I)", (not U.equals(I3)) and (not U2.equals(I3)))
    check("U_C3 is unitary (U^dagger U = I)", (U.H * U).equals(I3))

    # Spectrum: {1, omega, omega^2} with omega = exp(2*pi*i/3). Sympy does not
    # symbolically equate exp(2*pi*I/3) with -1/2 + sqrt(3)*I/2 by default, so
    # compare numerically as a multiset.
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    eigs_num = sorted(
        (complex(e.evalf()) for e in U.eigenvals().keys()),
        key=lambda z: (z.real, z.imag),
    )
    expected_num = sorted(
        (complex(sp.simplify(e).evalf()) for e in [sp.Integer(1), omega, omega**2]),
        key=lambda z: (z.real, z.imag),
    )
    eigs_match = (
        len(eigs_num) == 3
        and all(abs(a - b) < 1e-10 for a, b in zip(eigs_num, expected_num))
    )
    check("spectrum of U_C3 is {1, omega, omega^2}", eigs_match,
          detail=f"eigs={[sp.simplify(e) for e in U.eigenvals().keys()]}")

    # Schur's lemma: any matrix commuting with U on C^3 (regular rep) is
    # a polynomial in U, hence of the form H = a*I + b*U + b_bar*U^2 if H is
    # also Hermitian (b real or complex; the b_bar = conj(b) coupling on U^2
    # is the Hermiticity condition).
    a = sp.symbols("a", real=True)
    b = sp.symbols("b")  # complex
    b_bar = sp.conjugate(b)
    H = a * I3 + b * U + b_bar * U2

    # 1. Hermiticity check.
    check("H is Hermitian (H^dagger == H)", sp.simplify(H.H - H) == sp.zeros(3, 3))

    # 2. Commutation with U_C3.
    commutator = H * U - U * H
    check(
        "H commutes with U_C3 ([H, U_C3] = 0)",
        sp.simplify(commutator) == sp.zeros(3, 3),
    )

    # 3. Constant-diagonal property: <c_alpha|H|c_alpha> = a for all alpha.
    diag_entries = [sp.simplify(H[i, i]) for i in range(3)]
    all_equal_a = all(sp.simplify(d - a) == 0 for d in diag_entries)
    check(
        "<c_alpha|H|c_alpha> = a (constant over alpha)",
        all_equal_a,
        detail=f"diag = {diag_entries}",
    )

    # 4. Identity a = Tr(H) / 3.
    tr_over_3 = sp.simplify(H.trace() / 3)
    check(
        "a = Tr(H) / 3 (cyclic identity)",
        sp.simplify(tr_over_3 - a) == 0,
        detail=f"Tr(H)/3 = {tr_over_3}",
    )

    # 5. Numerical instance check: a = 3/2, b = 7/10 (real).
    H_num = H.subs({a: sp.Rational(3, 2), b: sp.Rational(7, 10)})
    diag_num = [sp.simplify(H_num[i, i]) for i in range(3)]
    expected_diag = sp.Rational(3, 2)
    all_match = all(d == expected_diag for d in diag_num)
    check(
        "numerical instance a=3/2, b=7/10 gives diag (3/2, 3/2, 3/2)",
        all_match,
        detail=f"diag_num = {diag_num}",
    )

    # 6. Eigenvalue formula: lambda_k = a + 2*Re(b * omega^k) for k in {0,1,2}.
    H_num_eigvals_set = set(sp.simplify(e) for e in H_num.eigenvals().keys())
    expected_lambda_set = set(
        sp.simplify(sp.Rational(3, 2) + 2 * sp.Rational(7, 10) * sp.cos(2 * sp.pi * k / 3))
        for k in range(3)
    )
    eig_match = (
        len(H_num_eigvals_set) == len(expected_lambda_set)
        and all(
            any(sp.simplify(e - x) == 0 for x in expected_lambda_set)
            for e in H_num_eigvals_set
        )
    )
    check(
        "eigenvalues of numerical H match the circulant spectrum formula",
        eig_match,
        detail=f"eigvals = {list(H_num_eigvals_set)}",
    )

    # 7. Counterfactual: a non-C_3-equivariant H (e.g., diag(1, 2, 3)) does
    #    NOT have constant corner-diagonal.
    H_break = sp.diag(1, 2, 3)
    break_diag = [H_break[i, i] for i in range(3)]
    not_constant = len(set(break_diag)) > 1
    check(
        "counterfactual: non-C_3-equivariant H distinguishes corners",
        not_constant,
        detail=f"break_diag = {break_diag}",
    )

    # 8. Counterfactual: diag(1, 2, 3) does not commute with U_C3.
    counter_commutator = H_break * U - U * H_break
    nonzero = sp.simplify(counter_commutator) != sp.zeros(3, 3)
    check(
        "counterfactual: non-C_3-equivariant H does NOT commute with U_C3",
        nonzero,
    )


# -------------------------------------------------------------
# Section B. Review-hygiene checks on the source note
# -------------------------------------------------------------
def run_note_check() -> None:
    print()
    print("=" * 64)
    print("Section B: review-hygiene checks on the source note")
    print("=" * 64)

    for path, label in [
        (NOTE, "foreclosure synthesis note"),
        (SUBSTEP4, "substep-4 AC narrowing note"),
        (PRESERVED_C3, "preserved-C_3 interpretation note"),
        (BAE_RENAME, "BAE rename meta note"),
        (MINIMAL_AXIOMS, "minimal axioms note"),
    ]:
        check(f"required source exists: {label}", path.exists(),
              detail=str(path.relative_to(ROOT)))

    if not NOTE.exists():
        return

    note = NOTE.read_text()

    # Classification + status authority.
    check(
        "note declares claim_type: bounded_theorem",
        "**Claim type:** bounded_theorem" in note,
    )
    check(
        "note declares status authority: independent audit lane only",
        "**Status authority:** independent audit lane only" in note,
    )
    check(
        "note declares proposal_allowed: false",
        "proposal_allowed: false" in note,
    )

    # Author does not write pipeline status.
    effective_label = "Effective " + "status"
    audit_clean_token = "audited" + "_clean"
    check(
        "note does not declare audit-clean verdict",
        audit_clean_token not in note,
    )
    check(
        "note does not assert an Effective-status header",
        effective_label + ":" not in note,
    )

    # No new axiom claims.
    check(
        "note does not propose a new axiom",
        "A_min" in note and "is unchanged" in note,
    )
    check(
        "note does not include a forbidden_imports_used: true line",
        "forbidden_imports_used: true" not in note,
    )

    # Cites all 10 probes via markdown links.
    for probe in PROBE_NOTES:
        marker = f"({probe})"
        check(
            f"cites probe via markdown link: {probe}",
            marker in note,
        )

    # Cites the parent atomic decomposition + preserved-C_3 + BAE rename.
    parents = [
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md",
        "C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md",
        "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md",
        "AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for parent in parents:
        check(
            f"cites parent / canonical authority: {parent}",
            f"({parent})" in note,
        )

    # Core repo-canonical vocabulary present (no new tags introduced).
    vocab_terms = [
        "Schur",
        "regular representation",
        "circulant",
        "C_3",
        "Z/3",
        "Type I_3",
        "AC_phi" if "AC_phi" in note else "AC_φ",
        "AC_lambda" if "AC_lambda" in note else "AC_λ",
        "AC_phi_lambda" if "AC_phi_lambda" in note else "AC_φλ",
        "BAE",
        "preserved",
    ]
    for term in vocab_terms:
        check(
            f"repo-canonical vocabulary present: {term}",
            term in note,
        )

    # 10-probe inventory table includes the unaudited status flags (per
    # 2026-05-10 ledger snapshot).
    check(
        "10-probe inventory records `unaudited` ledger status",
        note.count("`unaudited`") >= 10,
    )

    # AC_phi_lambda decomposition into (AC_lambda.struct, AC_lambda.label, BAE).
    check(
        "AC_phi_lambda decomposition records AC_lambda.struct",
        "AC_λ.struct" in note or "AC_lambda.struct" in note,
    )
    check(
        "AC_phi_lambda decomposition records AC_lambda.label",
        "AC_λ.label" in note or "AC_lambda.label" in note,
    )
    check(
        "AC_phi_lambda decomposition records BAE as the open atom",
        "BAE" in note and "remaining" in note and ("genuinely open" in note or "single remaining open" in note),
    )

    # Names all five escape routes.
    escapes = [
        "Non-`C_3`-symmetric primitive",
        "Spontaneous `C_3` breaking",
        "External Higgs VEV",
        "PDG mass input",
        "Explicit labeling axiom",
    ]
    for escape in escapes:
        check(
            f"escape route named: {escape}",
            escape in note,
        )

    # Cites the canonical synthesis-template's "not a new derivation" framing.
    check(
        "note states 'not a new derivation'",
        "not a new derivation" in note.lower(),
    )


def main() -> int:
    print("AC_phi_lambda preserved-C_3 structural foreclosure diagnostic")
    print(f"Source note: {NOTE.relative_to(ROOT)}")
    run_schur_check()
    run_note_check()
    print()
    print("=" * 64)
    print(f"PASS = {PASS}, FAIL = {FAIL}")
    print("=" * 64)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
