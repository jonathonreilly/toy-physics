#!/usr/bin/env python3
"""Exact Schur-boundary audit for the conditional Majorana/seesaw lane.

This runner verifies the algebra in
docs/NEUTRINO_MAJORANA_SEESAW_SCHUR_BOUNDARY_THEOREM_NOTE_2026-04-25.md.

Scope:
  * proves the downstream boundary map after a Dirac block D and invertible
    right-handed Majorana block M_R are supplied;
  * verifies determinant, Green-compression, rank, scale, and singular-value
    certificates on exact rational witnesses;
  * checks that the note is wired as conditional support, not as a positive
    Majorana primitive, mu, Y_nu, or neutrino-spectrum closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0
REPO_ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read_text(rel_path: str) -> str:
    path = REPO_ROOT / rel_path
    return path.read_text() if path.exists() else ""


def status_line(content: str) -> str:
    for line in content.splitlines()[:30]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**") or stripped.lower().startswith("status:"):
            return stripped.split(":", 1)[1].strip().strip("*").strip()
    return ""


def audit_authorities() -> None:
    banner("Authority and boundary audit")

    authorities = (
        (
            "docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md",
            ("exact retained-stack reduction", "Majorana / seesaw closure needs a new charge-`2` primitive", "Y_nu"),
        ),
        (
            "docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md",
            ("exact current-stack theorem", "mu_current = 0", "charge-`2` primitive"),
        ),
        (
            "docs/NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md",
            ("exact frontier reduction", "new charge-`2` microscopic primitive", "does **not** prove"),
        ),
        (
            "docs/NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md",
            ("outside the flagship paper core", "positive retained Majorana realization", "Dirac Yukawa"),
        ),
    )

    for rel_path, required_tokens in authorities:
        content = read_text(rel_path)
        print(f"  {rel_path}")
        print(f"    Status: {status_line(content) or 'NO STATUS LINE'}")
        check(f"authority exists: {rel_path}", bool(content))
        for token in required_tokens:
            check(f"authority token in {rel_path}: {token}", token in content)


def witness_blocks() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    D = sp.Matrix(
        [
            [1, 2, 0],
            [0, 1, 1],
            [2, 0, 1],
        ]
    )
    M_R = sp.Matrix(
        [
            [5, 1, 0],
            [1, 4, 2],
            [0, 2, 3],
        ]
    )
    zero = sp.zeros(3)
    K = sp.Matrix.vstack(sp.Matrix.hstack(zero, D), sp.Matrix.hstack(D.T, M_R))
    M_light = -D * M_R.inv() * D.T
    return D, M_R, K, sp.simplify(M_light)


def audit_schur_elimination(D: sp.Matrix, M_R: sp.Matrix, K: sp.Matrix, M_light: sp.Matrix) -> None:
    banner("Feshbach-Schur elimination")

    x1, x2, x3 = sp.symbols("x1 x2 x3")
    ell = sp.Matrix([x1, x2, x3])
    r_star = -M_R.inv() * D.T * ell
    reduced = sp.simplify(K * sp.Matrix.vstack(ell, r_star))
    expected = sp.Matrix.vstack(M_light * ell, sp.zeros(3, 1))

    print(f"  det(D)   = {D.det()}")
    print(f"  det(M_R) = {M_R.det()}")
    print(f"  M_light  = {M_light}")
    check("D witness is invertible", D.det() != 0)
    check("M_R witness is invertible", M_R.det() != 0)
    check("K [ell; -M_R^-1 D^T ell] = [M_light ell; 0]", sp.simplify(reduced - expected) == sp.zeros(6, 1))
    check("M_light is symmetric", sp.simplify(M_light - M_light.T) == sp.zeros(3))


def audit_determinant_and_green(D: sp.Matrix, M_R: sp.Matrix, K: sp.Matrix, M_light: sp.Matrix) -> None:
    banner("Determinant factorization and inverse Green compression")

    det_k = sp.factor(K.det())
    det_factor = sp.factor(M_R.det() * M_light.det())
    print(f"  det(K)                         = {det_k}")
    print(f"  det(M_R) det(M_light)          = {det_factor}")
    check("det K = det(M_R) det(M_light)", sp.simplify(det_k - det_factor) == 0)
    check("K is invertible iff M_light is invertible on this witness", K.det() != 0 and M_light.det() != 0)

    light_green = K.inv()[:3, :3]
    diff = sp.simplify(light_green - M_light.inv())
    check("light-light block of K^-1 equals M_light^-1", diff == sp.zeros(3))

    # Cross-check by solving a source response directly.
    y1, y2, y3 = sp.symbols("y1 y2 y3")
    src = sp.Matrix([y1, y2, y3])
    full_response = K.inv() * sp.Matrix.vstack(src, sp.zeros(3, 1))
    check("compressed full Green response equals Schur response",
          sp.simplify(full_response[:3, :] - M_light.inv() * src) == sp.zeros(3, 1))


def audit_rank_and_kernel(M_R: sp.Matrix) -> None:
    banner("Rank and kernel criteria")

    D_full = sp.Matrix([[1, 2, 0], [0, 1, 1], [2, 0, 1]])
    M_full = -D_full * M_R.inv() * D_full.T
    check("full-rank D gives full-rank M_light", D_full.rank() == 3 and M_full.rank() == 3)
    check("rank(M_light) <= rank(D) for full-rank witness", M_full.rank() <= D_full.rank())

    D_sing = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    M_sing = -D_sing * M_R.inv() * D_sing.T
    ell = sp.Matrix([0, 0, 1])
    print(f"  rank(D_sing)      = {D_sing.rank()}")
    print(f"  rank(M_light)     = {M_sing.rank()}")
    check("rank(M_light) <= rank(D) for singular witness", M_sing.rank() <= D_sing.rank())
    check("left-kernel vector D^T ell = 0", D_sing.T * ell == sp.zeros(3, 1))
    check("left-kernel vector remains massless: M_light ell = 0", M_sing * ell == sp.zeros(3, 1))


def audit_scale_covariance(D: sp.Matrix, M_R: sp.Matrix, M_light: sp.Matrix) -> None:
    banner("Scale covariance")

    a = sp.Rational(7, 3)
    b = sp.Rational(5, 2)
    scaled = -(a * D) * (b * M_R).inv() * (a * D).T
    expected = sp.simplify((a ** 2 / b) * M_light)
    check("D -> aD and M_R -> bM_R gives M_light -> (a^2/b)M_light",
          sp.simplify(scaled - expected) == sp.zeros(3))

    mu = sp.symbols("mu", positive=True)
    M0 = M_R
    M_mu = -D * (mu * M0).inv() * D.T
    check("M_R = mu M0 gives M_light(mu) = mu^-1 M_light(1)",
          sp.simplify(M_mu - (1 / mu) * M_light) == sp.zeros(3))


def singular_values(mat: sp.Matrix) -> np.ndarray:
    arr = np.array(mat.evalf(), dtype=float)
    return np.linalg.svd(arr, compute_uv=False)


def audit_singular_value_certificates(D: sp.Matrix, M_R: sp.Matrix, M_light: sp.Matrix) -> None:
    banner("Singular-value certificates")

    s_D = singular_values(D)
    s_R = singular_values(M_R)
    s_L = singular_values(M_light)

    smax_D = float(s_D[0])
    smin_D = float(s_D[-1])
    smax_R = float(s_R[0])
    smin_R = float(s_R[-1])
    smax_L = float(s_L[0])
    smin_L = float(s_L[-1])

    upper = smax_D ** 2 / smin_R
    lower = smin_D ** 2 / smax_R
    print(f"  s_max(D)^2 / s_min(M_R) = {upper:.12f}")
    print(f"  s_max(M_light)          = {smax_L:.12f}")
    print(f"  s_min(D)^2 / s_max(M_R) = {lower:.12f}")
    print(f"  s_min(M_light)          = {smin_L:.12f}")
    check("upper certificate: s_max(M_light) <= s_max(D)^2 / s_min(M_R)", smax_L <= upper + 1e-12)
    check("lower certificate for invertible D: s_min(M_light) >= s_min(D)^2 / s_max(M_R)", smin_L + 1e-12 >= lower)


def audit_note_boundary() -> None:
    banner("Note boundary and public package wiring")

    note = "NEUTRINO_MAJORANA_SEESAW_SCHUR_BOUNDARY_THEOREM_NOTE_2026-04-25.md"
    runner = "frontier_neutrino_majorana_seesaw_schur_boundary.py"
    note_text = read_text(f"docs/{note}")

    required_note_boundaries = (
        "does not derive `Y_nu`",
        "does not derive the Majorana amplitude `mu`",
        "does not choose Dirac versus Majorana nature",
        "does not close the neutrino mass spectrum",
        "The theorem does not supply those inputs.",
    )
    for token in required_note_boundaries:
        check(f"note keeps boundary: {token}", token in note_text)

    package_surfaces = (
        ("docs/CANONICAL_HARNESS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/CLAIMS_TABLE.md", (note,)),
        ("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md", (note, runner)),
        ("docs/publication/ci3_z3/DERIVATION_ATLAS.md", (note, runner)),
        ("docs/publication/ci3_z3/RESULTS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/PUBLICATION_MATRIX.md", (note, runner)),
        ("docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md", (note, "conditional exact")),
        ("docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md", (note, "does not derive")),
        ("docs/NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md", (note, "conditional")),
        ("docs/NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md", (note, "Schur")),
    )
    for rel_path, tokens in package_surfaces:
        content = read_text(rel_path)
        ok = bool(content) and all(token in content for token in tokens)
        print(f"  {rel_path}: {'OK' if ok else 'MISSING'}")
        check(f"package surface wired: {rel_path}", ok)


def main() -> int:
    print("=" * 88)
    print("Neutrino Majorana/seesaw Schur-boundary audit")
    print("See docs/NEUTRINO_MAJORANA_SEESAW_SCHUR_BOUNDARY_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_authorities()
    D, M_R, K, M_light = witness_blocks()
    audit_schur_elimination(D, M_R, K, M_light)
    audit_determinant_and_green(D, M_R, K, M_light)
    audit_rank_and_kernel(M_R)
    audit_scale_covariance(D, M_R, M_light)
    audit_singular_value_certificates(D, M_R, M_light)
    audit_note_boundary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
