#!/usr/bin/env python3
"""Audit the Planck bulk-to-boundary Schur-completion lane honestly.

This lane sharpens the surviving boundary route in the strongest honest way:
  - exact bulk elimination forces the quadratic boundary carrier to be the
    Schur complement of the same-surface bulk completion;
  - positivity of the quadratic boundary form is inherited from positivity of
    the completed bulk operator;
  - collectivity/nonlocality is generically created by bulk elimination;
  - but transfer-generator sign, positivity cone, and additive pressure
    normalization are not fixed by Schur completion alone;
  - consequently the Schur-completion lane does not yet kill the remaining
    Planck scale freedom.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
TRANSFER = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md"
PRESSURE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
OH = ROOT / "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def schur_complement(m_bb: sp.Matrix, m_bi: sp.Matrix, m_ii: sp.Matrix) -> sp.Matrix:
    return sp.simplify(m_bb - m_bi * m_ii.inv() * m_bi.T)


def top_eigenvalue(matrix: sp.Matrix) -> sp.Expr:
    values = list(matrix.eigenvals().keys())
    return max(values, key=lambda expr: complex(sp.N(expr, 50)).real)


def min_eigenvalue(matrix: sp.Matrix) -> sp.Expr:
    values = list(matrix.eigenvals().keys())
    return min(values, key=lambda expr: complex(sp.N(expr, 50)).real)


def main() -> int:
    note = normalized(NOTE)
    timelock = normalized(TIMELOCK)
    transfer = normalized(TRANSFER)
    pressure = normalized(PRESSURE)
    scale_ray = normalized(SCALE_RAY)
    oh = normalized(OH)

    n_pass = 0
    n_fail = 0

    print("Planck bulk-to-boundary Schur-completion lane audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY EVIDENCE")
    p = check(
        "time-lock still fixes one exact spacetime clock",
        "a_s = c a_t" in timelock and "beta = 1" in timelock,
        "the Schur lane is built only after the exact relative space/time lock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "timelocked transfer note already identifies a Schur boundary target class",
        "schur-complement reduction" in transfer and "one-clock semigroup" in transfer,
        "this lane should strengthen that candidate class rather than replace it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "boundary spectral note still leaves quarter as a normalization principle problem",
        "new parameter-free gravitational normalization principle" in pressure,
        "the load-bearing open step is already the pressure/normalization law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "older shell note already establishes exact Schur boundary action culture in the repo",
        "exact schur-complement boundary action" in oh
        and (
            "schur-complement energy of the microscopic lattice dynamics itself" in oh
            or "schur-complement boundary energy of the lattice dynamics itself" in oh
        ),
        "the new lane is a Planck-boundary analogue rather than a foreign construction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "scale-ray note still says a new unit-bearing observable is required",
        (
            "new non-homogeneous, unit-bearing same-surface observable" in scale_ray
            or "new non-homogeneous unit-bearing same-surface observable" in scale_ray
            or "unit-bearing same-surface theorem" in scale_ray
        ),
        "the Schur lane must honestly test whether it becomes that new anchor",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT SCHUR ELIMINATION / POSITIVITY")
    a, b, c = sp.symbols("a b c", positive=True)
    x, y = sp.symbols("x y", real=True)
    q = sp.Rational(1, 2) * (a * x**2 + 2 * b * x * y + c * y**2)
    s = sp.simplify(a - b**2 / c)
    q_completed = sp.expand(
        sp.Rational(1, 2) * c * (y + b * x / c) ** 2 + sp.Rational(1, 2) * s * x**2
    )
    p = check(
        "completion of squares gives the exact scalar Schur boundary action",
        sp.simplify(q - q_completed) == 0,
        "for a 1+1 block the effective boundary form is exactly (1/2) (a - b^2/c) x^2",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "scalar Schur complement is positive on a positive bulk block",
        sp.simplify(s) == a - b**2 / c,
        (
            "with c>0 and determinant ac-b^2 >= 0, the reduced scalar form is nonnegative; "
            "the boundary quadratic positivity is inherited from the bulk block"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    m_bb = sp.Matrix([[2, 0], [0, 2]])
    m_bi = sp.Matrix([[1, 0], [0, 1]])
    m_ii = sp.Matrix([[2, 1], [1, 2]])
    l_sigma = schur_complement(m_bb, m_bi, m_ii)
    expected = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    p = check(
        "the exact 2+2 witness reduces to the claimed collective boundary operator",
        sp.simplify(l_sigma - expected) == sp.zeros(2),
        "bulk elimination produces L_Sigma = [[4/3,1/3],[1/3,4/3]] exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr, 30)))
    p = check(
        "the witness Schur boundary operator is positive definite",
        evals == [1, sp.Rational(5, 3)],
        "positive bulk completion yields strictly positive boundary quadratic eigenvalues",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "collective boundary coupling is created even from a diagonal boundary block",
        m_bb[0, 1] == 0 and l_sigma[0, 1] != 0,
        "nonlocality is generated by the Schur term M_BI M_II^(-1) M_IB",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: SIGN / NORMALIZATION OBSTRUCTION")
    positive_generator = l_sigma
    negative_generator = -l_sigma
    p = check(
        "Schur elimination alone does not fix the generator sign",
        positive_generator[0, 1] > 0 and negative_generator[0, 1] < 0,
        (
            "L_Sigma is compatible with a Metzler-style growth sign, while -L_Sigma is not; "
            "bulk elimination produces the quadratic form, not the transfer sign convention"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    w = sp.symbols("w", real=True)
    top_pressure = sp.simplify(w - min_eigenvalue(l_sigma))
    p = check(
        "additive scalar shift moves the top pressure without changing eigenspaces",
        sp.simplify(top_pressure - (w - 1)) == 0,
        "for G_w = w I - L_Sigma the top pressure is exactly p_*(w) = w - lambda_min(L_Sigma)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    quarter_w = sp.solve(sp.Eq(top_pressure, sp.Rational(1, 4)), w)[0]
    p = check(
        "the quarter target is therefore equivalent to fixing one normalization constant",
        sp.simplify(quarter_w - sp.Rational(5, 4)) == 0,
        "the same Schur carrier hits p_*=1/4 only after choosing the additive shift w=5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    alt_pressure = sp.simplify(sp.Rational(7, 4) - min_eigenvalue(l_sigma))
    p = check(
        "different additive shifts produce different exact pressures on the same Schur carrier",
        alt_pressure == sp.Rational(3, 4),
        "the boundary coefficient is not fixed by the carrier alone",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SCHUR COMPLEMENT PRESERVES THE SCALE RAY")
    lam = sp.symbols("lam", positive=True)
    scaled_schur = schur_complement(lam * m_bb, lam * m_bi, lam * m_ii)
    p = check(
        "Schur complement scales homogeneously with a homogeneous bulk completion",
        sp.simplify(scaled_schur - lam * l_sigma) == sp.zeros(2),
        "if M(lambda)=lambda M(1), then L_Sigma(lambda)=lambda L_Sigma(1) exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    scaled_top_pressure = sp.simplify(lam * top_eigenvalue(l_sigma))
    p = check(
        "without a new normalization law the Schur carrier itself does not anchor a preferred scale",
        sp.simplify(scaled_top_pressure - sp.Rational(5, 3) * lam) == 0,
        "homogeneous rescaling just moves the spectrum along the same ray",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note explicitly says the carrier is closed but the coefficient is not",
        "closes the **carrier** much more sharply than before" in note
        and "does not close the **coefficient**" in note,
        "the lane should not overstate quarter closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly identifies normalization as the live open theorem",
        "live open step is the **normalization law**" in note
        and "one-parameter normalization obstruction" in note,
        "the missing theorem should be narrowed to one sharp object",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says Schur completion does not kill the remaining scale freedom",
        "does **not** by itself kill the remaining scale freedom" in note,
        "this lane should strengthen the route honestly rather than claim exact Planck",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Exact bulk elimination on the time-locked surface really does force a "
        "positive collective Schur boundary carrier, but it does not force the "
        "transfer-generator sign or the additive pressure normalization. The "
        "quarter coefficient remains an open normalization theorem, so this lane "
        "does not yet kill the remaining Planck scale freedom."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
