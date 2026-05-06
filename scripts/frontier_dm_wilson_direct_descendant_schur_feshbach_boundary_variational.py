#!/usr/bin/env python3
"""
DM Wilson direct-descendant Schur-Feshbach boundary variational theorem.

This verifier audits the object-level block algebra in the paired note:

  * the Schur block L_e is the boundary Green compression inverse;
  * Feshbach elimination gives D_- [u; v_*(u)] = [L_e u; 0];
  * for positive Hermitian D_-, L_e is the Dirichlet boundary minimum;
  * Loewner bounds on positive microscopic blocks descend to Schur bounds.

It deliberately does not evaluate the microscopic charged block D_-, select the
charged support split, or close the final DM selector/relic lane.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy
import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]
NOTE_NAME = "DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md"
NOTE_PATH = ROOT / "docs" / NOTE_NAME
SCRIPT_NAME = Path(__file__).name


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def banner(title: str) -> None:
    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_zero_matrix(mat: sp.Matrix) -> bool:
    return all(sympy.simplify(entry) == 0 for entry in mat)


def principal_minors(mat: sp.Matrix) -> list[sp.Expr]:
    indices = range(mat.rows)
    out: list[sp.Expr] = []
    for size in range(1, mat.rows + 1):
        for combo in combinations(indices, size):
            out.append(sympy.factor(mat.extract(combo, combo).det()))
    return out


def leading_principal_minors(mat: sp.Matrix) -> list[sp.Expr]:
    return [sympy.factor(mat[:idx, :idx].det()) for idx in range(1, mat.rows + 1)]


def all_positive(values: list[sp.Expr]) -> bool:
    return all(bool(sp.N(value) > 0) for value in values)


def all_nonnegative(values: list[sp.Expr]) -> bool:
    return all(bool(sp.N(value) >= 0) for value in values)


def block2(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, d: sp.Matrix) -> sp.Matrix:
    return a.row_join(b).col_join(c.row_join(d))


def sample_blocks() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    a = sp.Matrix([[8, 1, 0], [1, 7, 1], [0, 1, 6]])
    f = sp.Matrix([[4, 1], [1, 3]])
    b = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    c = b.T
    d_minus = block2(a, b, c, f)
    l_e = a - b * f.inv() * c
    return a, b, c, f, d_minus, l_e


def package_file(relpath: str) -> Path:
    return ROOT / relpath


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT SCHUR-FESHBACH BOUNDARY VARIATIONAL THEOREM")
    print("=" * 88)

    _a, b, c, f, d_minus, l_e = sample_blocks()
    e_dim = 3
    r_dim = 2
    i_e = sp.eye(e_dim).col_join(sp.zeros(r_dim, e_dim))
    z = sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 3, 4]])
    j_z = block2(z, sp.zeros(e_dim, r_dim), sp.zeros(r_dim, e_dim), sp.zeros(r_dim, r_dim))

    banner("PART 1: NOTE SCOPE AND AUTHORITY HYGIENE")
    note = read_text(NOTE_PATH)
    check("The theorem note exists on the package surface", NOTE_PATH.exists(), NOTE_NAME)
    check("The theorem note points to this object-level verifier", SCRIPT_NAME in note, SCRIPT_NAME)
    for phrase in [
        "does not evaluate `D_-`",
        "does not by itself select",
        "The positive variational assumption is explicit",
        "Finite-dimensional closure certificate",
        "**Claim type:** `positive_theorem`",
        "fitted selector",
        "not a hidden Wilson-native construction",
    ]:
        check(f"Scope phrase present: {phrase}", phrase in note)
    normalized_note = " ".join(note.split())
    check(
        "Scope phrase present: does not claim Wilson-native parent closure",
        "does not claim Wilson-native parent closure" in normalized_note,
    )
    check(
        "Scope phrase present: does not independently close the DM flagship lane",
        "does not independently close the DM flagship lane" in normalized_note,
    )

    banner("PART 2: SCHUR FACTORIZATION, INVERTIBILITY, AND BOUNDARY GREEN COMPRESSION")
    upper = block2(sp.eye(e_dim), b * f.inv(), sp.zeros(r_dim, e_dim), sp.eye(r_dim))
    middle = block2(l_e, sp.zeros(e_dim, r_dim), sp.zeros(r_dim, e_dim), f)
    lower = block2(sp.eye(e_dim), sp.zeros(e_dim, r_dim), f.inv() * c, sp.eye(r_dim))
    expected_inv = block2(
        l_e.inv(),
        -l_e.inv() * b * f.inv(),
        -f.inv() * c * l_e.inv(),
        f.inv() + f.inv() * c * l_e.inv() * b * f.inv(),
    )
    compression = i_e.T * d_minus.inv() * i_e

    check("Interior block F is invertible", f.det() != 0, f"det(F)={sympy.factor(f.det())}")
    check("Schur block L_e is invertible", l_e.det() != 0, f"det(L_e)={sympy.factor(l_e.det())}")
    check(
        "Block determinant identity det(D_-) = det(F) det(L_e)",
        sympy.factor(d_minus.det() - f.det() * l_e.det()) == 0,
        f"det(D_-)={sympy.factor(d_minus.det())}",
    )
    check("Exact Schur factorization reconstructs D_-", is_zero_matrix(upper * middle * lower - d_minus))
    check("Exact block inverse formula matches D_-^{-1}", is_zero_matrix(d_minus.inv() - expected_inv))
    check("Boundary Green compression equals L_e^{-1}", is_zero_matrix(compression - l_e.inv()))
    check("Equivalent inverse-compression law recovers L_e", is_zero_matrix(compression.inv() - l_e))

    banner("PART 3: DETERMINANT RESPONSE AND DESCENDED HERMITIAN LAW")
    t = sp.symbols("t")
    full_ratio = sympy.factor((d_minus + t * j_z).det() / d_minus.det())
    schur_ratio = sympy.factor((l_e + t * z).det() / l_e.det())
    first_variation = sp.diff(schur_ratio, t).subs(t, 0)
    trace_response = sp.trace(l_e.inv() * z)
    green_response = sp.trace(compression * z)

    check("Normalized determinant response reduces exactly to the Schur block", sympy.simplify(full_ratio - schur_ratio) == 0)
    check("First variation is Tr(L_e^{-1} X)", sympy.simplify(first_variation - trace_response) == 0)
    check("Green-compression response equals the Schur response", sympy.simplify(green_response - trace_response) == 0)

    banner("PART 4: FESHBACH ELIMINATION")
    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    u = sp.Matrix([u1, u2, u3])
    v_star = -f.inv() * c * u
    eliminated = d_minus * u.col_join(v_star)
    expected_eliminated = (l_e * u).col_join(sp.zeros(r_dim, 1))
    check("The eliminated interior field is v_*(u) = -F^{-1} C u", v_star == -f.inv() * c * u)
    check("D_- [u; v_*(u)] = [L_e u; 0] exactly", is_zero_matrix(eliminated - expected_eliminated))

    banner("PART 5: POSITIVE DIRICHLET VARIATIONAL PRINCIPLE")
    d_minors = leading_principal_minors(d_minus)
    f_minors = leading_principal_minors(f)
    l_minors = leading_principal_minors(l_e)
    v1, v2 = sp.symbols("v1 v2", real=True)
    v = sp.Matrix([v1, v2])
    trial = u.col_join(v)
    q_uv = sympy.expand((trial.T * d_minus * trial)[0])
    boundary_q = sympy.expand((u.T * l_e * u)[0])
    square_vec = v + f.inv() * c * u
    square_q = sympy.expand((square_vec.T * f * square_vec)[0])
    grad_q = sp.Matrix([sp.diff(q_uv, v1), sp.diff(q_uv, v2)])
    grad_at_star = grad_q.subs({v1: v_star[0], v2: v_star[1]})

    check("Sample D_- is Hermitian positive definite", all_positive(d_minors), f"leading minors={d_minors}")
    check("Interior F is positive definite", all_positive(f_minors), f"leading minors={f_minors}")
    check("Schur block L_e is positive definite", all_positive(l_minors), f"leading minors={l_minors}")
    check("Quadratic form completes the square exactly", sympy.simplify(q_uv - boundary_q - square_q) == 0)
    check("The Feshbach field is the stationary point of Q_u(v)", is_zero_matrix(grad_at_star))
    check("The Hessian in interior variables is 2F > 0", all_positive(leading_principal_minors(2 * f)))
    check("The minimum value is u^T L_e u", sympy.simplify(q_uv.subs({v1: v_star[0], v2: v_star[1]}) - boundary_q) == 0)

    banner("PART 6: TRIAL-INTERIOR UPPER CERTIFICATES")
    r_zero = sp.zeros(r_dim, e_dim)
    r_sharp = -f.inv() * c
    embed_zero = sp.eye(e_dim).col_join(r_zero)
    embed_sharp = sp.eye(e_dim).col_join(r_sharp)
    k_zero = embed_zero.T * d_minus * embed_zero
    k_sharp = embed_sharp.T * d_minus * embed_sharp
    zero_gap = sympy.simplify(k_zero - l_e)
    sharp_gap = sympy.simplify(k_sharp - l_e)
    completion_gap = sympy.simplify((r_zero - r_sharp).T * f * (r_zero - r_sharp))

    check("Zero trial map gives a Loewner upper certificate", all_nonnegative(principal_minors(zero_gap)), f"principal minors={principal_minors(zero_gap)}")
    check("Trial gap equals the completed-square matrix", is_zero_matrix(zero_gap - completion_gap))
    check("Sharp Feshbach trial map has zero gap", is_zero_matrix(sharp_gap))

    banner("PART 7: MICROSCOPIC LOEWNER MONOTONICITY DESCENDS TO BOUNDARY LAW")
    p = sp.diag(1, 2, 3, 4, 5)
    d_high = d_minus + p
    f_high = d_high[e_dim:, e_dim:]
    l_high = d_high[:e_dim, :e_dim] - d_high[:e_dim, e_dim:] * f_high.inv() * d_high[e_dim:, :e_dim]
    gap = sympy.simplify(l_high - l_e)
    check("The microscopic perturbation D_high - D_low is positive definite", all_positive(leading_principal_minors(p)))
    check("The high microscopic block remains positive definite", all_positive(leading_principal_minors(d_high)))
    check("The descended Schur law is monotone: L_high - L_low >= 0", all_nonnegative(principal_minors(gap)), f"principal minors={principal_minors(gap)}")

    banner("PART 8: PACKAGE WIRING AND NEGATIVE-CLOSURE FLAGS")
    for relpath in [
        "docs/CANONICAL_HARNESS_INDEX.md",
        "docs/publication/ci3_z3/PUBLICATION_MATRIX.md",
        "docs/publication/ci3_z3/CLAIMS_TABLE.md",
        "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md",
        "docs/publication/ci3_z3/DERIVATION_ATLAS.md",
        "docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md",
        "docs/publication/ci3_z3/RESULTS_INDEX.md",
        "docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md",
        "docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md",
    ]:
        body = read_text(package_file(relpath))
        check(f"{relpath} links the boundary theorem note", NOTE_NAME in body)

    forbidden_true_flags = [
        ("DM_MICROSCOPIC_D_MINUS_EVALUATED", "TRUE"),
        ("DM_FINAL_SELECTOR_CLOSED", "TRUE"),
        ("DM_FLAGSHIP_LANE_CLOSED", "TRUE"),
        ("WILSON_NATIVE_PARENT_CLOSURE", "TRUE"),
    ]
    check(
        "No forbidden final-closure flag is asserted by this packet",
        not any(f"{name}={value}" in note for name, value in forbidden_true_flags),
    )

    print("\n" + "=" * 88)
    print("SUMMARY")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print(f"FAILED: {FAIL_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print("DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL=TRUE")
    print("DM_BOUNDARY_RESOLVENT_CERTIFICATE=TRUE")
    print("DM_POSITIVE_DIRICHLET_CERTIFICATE=TRUE")
    print("DM_MICROSCOPIC_D_MINUS_EVALUATED_BY_THIS_THEOREM=FALSE")
    print("DM_FINAL_SELECTOR_CLOSED_BY_THIS_THEOREM=FALSE")
    print("DM_FLAGSHIP_LANE_CLOSED_BY_THIS_THEOREM=FALSE")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
