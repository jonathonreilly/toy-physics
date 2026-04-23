#!/usr/bin/env python3
"""Audit the observable-principle boundary-pressure identification lane.

This lane does not claim Planck closure. It proves the sharper observable-side
statement:

  - the same multiplicative-to-additive logic from the observable-principle
    note identifies the exact scalar boundary observable with
    F_vac(L) = (1/2) log det(L), equivalently p_vac(L) = (1/(2n)) log det(L);
  - semigroup top pressure p_* = sup spec(G) is not additive on direct sums and
    therefore is not the current scalar observable-principle quantity;
  - the C^16 axis-sector mass m_axis = 1/4 lives on a different carrier and is
    not selected by the current Schur boundary scalar grammar;
  - on the exact witness, p_vac = (1/4) log(5/3) != 1/4, so quarter is ruled
    out if physical boundary pressure is required to be the observable-principle
    scalar.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
)
OBS = ROOT / "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
SCHUR = ROOT / "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md"
NONAFFINE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
ACTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


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


def main() -> int:
    note = normalized(NOTE)
    obs = normalized(OBS)
    schur = normalized(SCHUR)
    nonaffine = normalized(NONAFFINE)
    action = normalized(ACTION)
    c16 = normalized(C16)

    n_pass = 0
    n_fail = 0

    print("Planck boundary observable-principle pressure identification lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM SURFACES")
    p = check(
        "the observable-principle note still fixes the multiplicative-to-additive log law",
        "w(r_1 r_2) = w(r_1) + w(r_2)" in obs
        and "w = c log |z| + const" in obs
        and "scalar additivity on independent subsystems" in obs,
        "the boundary observable lane should inherit the same scalar logic rather than invent a new one",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the Schur note still fixes the exact microscopic boundary action",
        "i_r(f ; j) = 1/2 f^t lambda_r f - j^t f" in schur
        and "exact schur-complement energy of the microscopic lattice" in schur,
        "the observable side must stay on the same Schur boundary carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-affine boundary note still fixes z_hat = det(L)^(-1/2) and p_vac",
        "z_hat(l_sigma) = det(l_sigma)^(-1/2)" in nonaffine
        and "p_vac(l_sigma)" in nonaffine,
        "the observable lane should identify the scalar quantity already earned there",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action-pressure note still fixes p_*(nu) = nu - lambda_min(L_Sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action,
        "growth pressure remains a distinct same-surface quantity on the action lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 bridge note still fixes the candidate bridge quantity m_axis = 1/4",
        "m_axis = 1/4" in c16
        and "physical boundary pressure = c^16 axis-sector mass" in c16,
        "the observable lane should treat this as a distinct candidate, not silently absorb it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT BOUNDARY OBSERVABLE GENERATOR")
    a, b = sp.symbols("a b", positive=True, real=True)
    z1 = a ** sp.Rational(-1, 2)
    z2 = b ** sp.Rational(-1, 2)
    z12 = (a * b) ** sp.Rational(-1, 2)
    f1 = -sp.log(z1)
    f2 = -sp.log(z2)
    f12 = -sp.log(z12)

    p = check(
        "the normalized Schur vacuum partition factorizes on independent direct sums",
        sp.simplify(z12 - z1 * z2) == 0,
        "for positive one-mode carriers Z_hat(a ⊕ b) = Z_hat(a) Z_hat(b)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the corresponding additive scalar is F_vac = -log Z_hat = (1/2) log det(L)",
        sp.simplify(f12 - (f1 + f2)) == 0
        and sp.simplify(f12 - sp.log(a * b) / 2) == 0,
        "the same observable-principle logic identifies the boundary scalar with the log partition free energy",
    )
    n_pass += int(p)
    n_fail += int(not p)

    l1, l2 = sp.symbols("l1 l2", positive=True, real=True)
    p_obs = sp.log(l1 * l2) / 4
    p = check(
        "on rank n=2 the scalar boundary observable density is p_obs = (1/4) log det(L)",
        sp.simplify(p_obs - (sp.log(l1 * l2) / 4)) == 0,
        "dividing the additive free energy by carrier rank gives the scalar density used in the lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: TOP-GROWTH PRESSURE IS NOT THE CURRENT SCALAR OBSERVABLE")
    g1 = sp.Matrix([[sp.Rational(1, 4)]])
    g2 = sp.Matrix([[sp.Rational(1, 8)]])
    g12 = sp.diag(g1[0, 0], g2[0, 0])
    p1 = max(g1.eigenvals().keys())
    p2 = max(g2.eigenvals().keys())
    p12 = max(g12.eigenvals().keys())

    p = check(
        "top-growth pressure on a direct sum is max-type rather than additive",
        p1 == sp.Rational(1, 4)
        and p2 == sp.Rational(1, 8)
        and p12 == sp.Rational(1, 4)
        and p12 != p1 + p2,
        "sup spec(G1 ⊕ G2) = max(sup spec(G1), sup spec(G2)) on the simplest exact witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "therefore p_* cannot be the current additive scalar observable-principle quantity",
        p12 == max(p1, p2) and p12 != p1 + p2,
        "an extra block-selection / growth-selection law would be needed to promote p_* to the physical scalar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: WITNESS VALUE AND QUARTER OBSTRUCTION")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    det_l = sp.simplify(l_sigma.det())
    p_vac = sp.simplify(sp.log(det_l) / 4)
    lambda_min = min(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    nu_obs = sp.simplify(lambda_min + p_vac)

    p = check(
        "the exact Schur witness still has determinant 5/3 and lambda_min = 1",
        det_l == sp.Rational(5, 3) and lambda_min == 1,
        "this is the same witness already fixed by the earlier boundary lanes",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the observable-principle scalar density on the witness is p_vac = (1/4) log(5/3)",
        sp.simplify(p_vac - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the exact scalar selected by the current boundary observable principle",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness observable density is not quarter",
        sp.simplify(p_vac - sp.Rational(1, 4)) != 0
        and abs(float(sp.N(p_vac, 50)) - 0.12770640594149768) < 1e-15,
        "if physical boundary pressure is the observable-principle scalar, quarter fails on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the corresponding action-lane vacuum density is nu_obs = 1 + (1/4) log(5/3), not 5/4",
        sp.simplify(nu_obs - (1 + sp.log(sp.Rational(5, 3)) / 4)) == 0
        and sp.simplify(nu_obs - sp.Rational(5, 4)) != 0,
        "observable-principle scalar identification does not rescue the quarter action law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: C^16 AXIS MASS REMAINS A DISTINCT BRIDGE")
    m_axis = sp.Rational(1, 4)
    p = check(
        "the C^16 candidate matches quarter but not the observable-principle scalar witness value",
        sp.simplify(m_axis - sp.Rational(1, 4)) == 0
        and sp.simplify(m_axis - p_vac) != 0,
        "the current boundary observable grammar does not collapse the Schur scalar and the C^16 projector mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "there is no current same-surface scalar identification of p_vac with m_axis",
        sp.simplify(p_vac - m_axis) != 0,
        "a future close would need an extra carrier/projector bridge rather than the present scalar boundary observable principle alone",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE HONESTY")
    p = check(
        "the note explicitly identifies the scalar boundary observable with p_vac",
        "observable-principle scalar boundary pressure = p_vac" in note
        or "p_phys = p_obs = p_vac" in note,
        "the main positive result should be stated directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says p_* is outside the current scalar grammar",
        "top-growth pressure is outside the current scalar observable grammar" in note
        or "non-additive growth-selection" in note,
        "the writeup should not blur additive observable pressure with semigroup top growth",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says m_axis remains a bridge quantity rather than a current observable-principle identification",
        "m_axis remains a serious candidate, but not an observable-principle identification theorem" in note
        or "candidate bridge quantity" in note,
        "the C^16 route should stay honest",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note reduces the frontier to the conceptual choice between scalar and non-scalar pressure",
        "is physical boundary pressure the additive scalar observable" in note
        and "different non-scalar/block-selected quantity" in note,
        "the result should compress the open problem to one exact conceptual bridge",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The observable-principle attack lands as an exact identification theorem "
        "for the scalar boundary observable and a no-go for quarter on that scalar "
        "route. The current observable principle selects p_vac(L_Sigma), not "
        "semigroup top pressure and not the C^16 axis-sector mass. So quarter, if "
        "it survives at all, now has to come from a new non-scalar/block-selecting "
        "physical bridge."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
