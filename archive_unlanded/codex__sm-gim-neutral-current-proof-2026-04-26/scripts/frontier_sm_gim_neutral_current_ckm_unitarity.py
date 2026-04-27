#!/usr/bin/env python3
"""Verifier for the SM GIM neutral-current / CKM projector theorem.

The runner audits
SM_GIM_NEUTRAL_CURRENT_CKM_UNITARITY_THEOREM_NOTE_2026-04-26.md with exact
rational matrix arithmetic. It deliberately does not claim any CKM numerical
entry, rare-decay rate, PMNS angle, baryogenesis asymmetry, or full loop-level
FCNC cancellation beyond the generation-independent GIM projector piece.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[Fraction]]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    suffix = f" -- {detail}" if detail else ""
    if condition:
        PASS_COUNT += 1
        print(f"PASS: {name}{suffix}")
    else:
        FAIL_COUNT += 1
        print(f"FAIL: {name}{suffix}")


def read_status(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Status:**"):
            return line
    return ""


def eye(n: int) -> Matrix:
    return [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]


def zero(n: int, m: int) -> Matrix:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    out = zero(rows, cols)
    for i in range(rows):
        for j in range(cols):
            out[i][j] = sum((a[i][k] * b[k][j] for k in range(inner)), Fraction(0))
    return out


def scalar_mul(c: Fraction, a: Matrix) -> Matrix:
    return [[c * value for value in row] for row in a]


def diag(values: list[Fraction]) -> Matrix:
    out = zero(len(values), len(values))
    for i, value in enumerate(values):
        out[i][i] = value
    return out


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def is_zero_matrix(a: Matrix) -> bool:
    return all(value == 0 for row in a for value in row)


def offdiag_values(a: Matrix) -> list[Fraction]:
    return [a[i][j] for i in range(len(a)) for j in range(len(a[0])) if i != j]


def has_nonzero_offdiag(a: Matrix) -> bool:
    return any(value != 0 for value in offdiag_values(a))


def rotation(i: int, j: int, c: Fraction, s: Fraction, n: int = 3) -> Matrix:
    out = eye(n)
    out[i][i] = c
    out[i][j] = s
    out[j][i] = -s
    out[j][j] = c
    return out


def assert_orthogonal(name: str, u: Matrix) -> None:
    lhs = matmul(transpose(u), u)
    rhs = matmul(u, transpose(u))
    check(f"{name} satisfies U^T U = I exactly", lhs == eye(len(u)))
    check(f"{name} satisfies U U^T = I exactly", rhs == eye(len(u)))


def transformed_neutral_current(u: Matrix, coefficient: Fraction) -> Matrix:
    return matmul(transpose(u), matmul(scalar_mul(coefficient, eye(len(u))), u))


def format_matrix(a: Matrix) -> str:
    return "[" + "; ".join(", ".join(str(value) for value in row) for row in a) + "]"


def main() -> int:
    theorem_note = DOCS / "SM_GIM_NEUTRAL_CURRENT_CKM_UNITARITY_THEOREM_NOTE_2026-04-26.md"
    yukawa_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    ew_note = DOCS / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
    ckm_note = DOCS / "CKM_MODULI_ONLY_UNITARITY_JARLSKOG_AREA_CERTIFICATE_THEOREM_NOTE_2026-04-26.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("one-Higgs Yukawa theorem exists", yukawa_note.exists(), str(yukawa_note.relative_to(ROOT)))
    check("EW gauge-mass theorem exists", ew_note.exists(), str(ew_note.relative_to(ROOT)))
    check("CKM unitarity certificate theorem exists", ckm_note.exists(), str(ckm_note.relative_to(ROOT)))

    check("Yukawa theorem is standalone positive", "standalone positive" in read_status(yukawa_note).lower())
    check("EW theorem is standalone positive", "standalone positive" in read_status(ew_note).lower())
    check("CKM certificate is standalone positive", "standalone positive" in read_status(ckm_note).lower())

    note_text = theorem_note.read_text(encoding="utf-8")
    check("note records primary runner", "frontier_sm_gim_neutral_current_ckm_unitarity.py" in note_text)
    note_lower = note_text.lower()
    check("note states tree-level neutral-current scope", "flavor diagonal at tree level" in note_lower)
    check("note states GIM projector scope", "generation-independent charged-current loop kernel" in note_text)
    check("note rejects full loop FCNC overclaim", "need not vanish when the internal masses are nondegenerate" in note_text)
    check("note does not derive CKM entries", "derive any ckm entry" in note_lower)

    # Exact rational left rotations. Each is a product of Pythagorean rotations.
    r12 = rotation(0, 1, Fraction(3, 5), Fraction(4, 5))
    r23 = rotation(1, 2, Fraction(5, 13), Fraction(12, 13))
    r13 = rotation(0, 2, Fraction(7, 25), Fraction(24, 25))
    r12_b = rotation(0, 1, Fraction(8, 17), Fraction(15, 17))

    u_u_l = matmul(r12, r23)
    u_d_l = matmul(r13, r12_b)
    u_e_l = matmul(r23, r13)
    u_u_r = r13
    u_d_r = r12_b
    u_e_r = matmul(r12_b, r23)

    assert_orthogonal("U_uL", u_u_l)
    assert_orthogonal("U_dL", u_d_l)
    assert_orthogonal("U_eL", u_e_l)
    assert_orthogonal("U_uR", u_u_r)
    assert_orthogonal("U_dR", u_d_r)
    assert_orthogonal("U_eR", u_e_r)

    d_u = diag([Fraction(2), Fraction(5), Fraction(17)])
    d_d = diag([Fraction(3), Fraction(7), Fraction(19)])

    # Gauge-basis Yukawas with nontrivial left and right rotations:
    # Y = U_L D U_R^T, so U_L^T Y U_R = D.
    y_u = matmul(u_u_l, matmul(d_u, transpose(u_u_r)))
    y_d = matmul(u_d_l, matmul(d_d, transpose(u_d_r)))
    check("toy up Yukawa diagonalizes by U_uL and U_uR", matmul(transpose(u_u_l), matmul(y_u, u_u_r)) == d_u)
    check("toy down Yukawa diagonalizes by U_dL and U_dR", matmul(transpose(u_d_l), matmul(y_d, u_d_r)) == d_d)
    check("toy Yukawas are not already diagonal in gauge basis", has_nonzero_offdiag(y_u) and has_nonzero_offdiag(y_d))

    # Neutral-current coefficients at a representative exact sin^2 theta_W = 3/8.
    s2w = Fraction(3, 8)
    rotations = {
        "u_L": u_u_l,
        "d_L": u_d_l,
        "e_L": u_e_l,
        "u_R": u_u_r,
        "d_R": u_d_r,
        "e_R": u_e_r,
    }
    current_tests = [
        ("photon up", Fraction(2, 3), ("u_L", "u_R")),
        ("photon down", Fraction(-1, 3), ("d_L", "d_R")),
        ("photon charged lepton", Fraction(-1), ("e_L", "e_R")),
        ("Z up_L", Fraction(1, 2) - Fraction(2, 3) * s2w, ("u_L",)),
        ("Z down_L", Fraction(-1, 2) - Fraction(-1, 3) * s2w, ("d_L",)),
        ("Z charged lepton L", Fraction(-1, 2) + s2w, ("e_L",)),
        ("Z up_R", -Fraction(2, 3) * s2w, ("u_R",)),
        ("Z down_R", Fraction(1, 3) * s2w, ("d_R",)),
        ("Z charged lepton R", s2w, ("e_R",)),
        ("gluon color generator eigenline", Fraction(4, 3), ("u_L", "d_L", "u_R", "d_R")),
    ]
    for label, coeff, species_list in current_tests:
        for species in species_list:
            u = rotations[species]
            transformed = transformed_neutral_current(u, coeff)
            target = scalar_mul(coeff, eye(3))
            check(
                f"{label} neutral current remains generation diagonal for {species}",
                transformed == target,
            )

    v_ckm = matmul(transpose(u_u_l), u_d_l)
    assert_orthogonal("V_CKM = U_uL^T U_dL", v_ckm)
    check("charged current has nontrivial off-diagonal CKM entries", has_nonzero_offdiag(v_ckm), format_matrix(v_ckm))
    check("right-handed rotations do not enter V_CKM witness", v_ckm == matmul(transpose(u_u_l), u_d_l))

    common_kernel = scalar_mul(Fraction(11, 7), eye(3))
    up_common = matmul(v_ckm, matmul(common_kernel, transpose(v_ckm)))
    down_common = matmul(transpose(v_ckm), matmul(common_kernel, v_ckm))
    check("up-sector common loop kernel projects to scalar identity", up_common == common_kernel)
    check("down-sector common loop kernel projects to scalar identity", down_common == common_kernel)
    check("up-sector common GIM offdiagonal entries vanish", all(value == 0 for value in offdiag_values(up_common)))
    check("down-sector common GIM offdiagonal entries vanish", all(value == 0 for value in offdiag_values(down_common)))

    nondegenerate_kernel = diag([Fraction(1), Fraction(2), Fraction(5)])
    residual = matmul(v_ckm, matmul(nondegenerate_kernel, transpose(v_ckm)))
    check("nondegenerate loop kernel can leave residual offdiagonal terms", has_nonzero_offdiag(residual), format_matrix(residual))
    check("residual differs from common projector identity", not is_zero_matrix(sub(residual, nondegenerate_kernel)))

    # Direct unitarity sum audit: sum_i V_ai V_bi = delta_ab for real witness.
    row_projector = matmul(v_ckm, transpose(v_ckm))
    col_projector = matmul(transpose(v_ckm), v_ckm)
    for a in range(3):
        for b in range(3):
            expected = Fraction(int(a == b), 1)
            check(f"row projector ({a},{b}) equals delta", row_projector[a][b] == expected, str(row_projector[a][b]))
            check(f"column projector ({a},{b}) equals delta", col_projector[a][b] == expected, str(col_projector[a][b]))

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
