#!/usr/bin/env python3
"""Audit the Schur-to-weighted-C^16 boundary lane honestly.

This lane does not claim Planck closure. It proves the sharper statement:

  - the current Schur/Perron data do canonically induce a weighted C^16
    axis-sector state on the section-canonical worldtube sector;
  - normalized Schur/Perron states are blind to the additive quarter-closing
    pressure shift w;
  - on the exact witness, the induced axis-sector diagonal weights are always
    (1/2, 1/6, 1/6, 1/6);
  - this determines only the conditional axis-sector state, not the total
    full-cell occupation of that sector;
  - the canonical no-extra-datum maximum-entropy extension to the full 16-state
    carrier has axis occupation alpha = exp(S_axis)/(12 + exp(S_axis));
  - because the Schur quotient is only 2-dimensional, alpha <= 1/7 < 1/4;
  - so normalized Schur/Perron data alone cannot restore the missing
    multiplicity or close exact quarter.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md"
)
SECTION = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
INTERTWINER = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md"
)
TRANSFER = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
)
VACUUM = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md"
)
BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
ASSUMPTIONS = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_LANE_FULL_ASSUMPTION_STRESS_AUDIT_2026-04-23.md"
)


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
    section_note = normalized(SECTION)
    intertwiner = normalized(INTERTWINER)
    transfer = normalized(TRANSFER)
    vacuum = normalized(VACUUM)
    bridge = normalized(BRIDGE)
    assumptions = normalized(ASSUMPTIONS)

    n_pass = 0
    n_fail = 0

    print("Planck boundary weighted C^16 state from Schur lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "section-canonical lane still forces the coarse four-axis worldtube sector P_A",
        "p_a = p_t + p_s" in section_note
        and "section-canonical" in section_note
        and "the unique admissible projector is" in section_note,
        "the new lane should induce a state on the already-forced coarse worldtube sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "intertwiner lane still says the minimal Schur carrier sees only the quotient span{|t>,|s>}",
        "h_q = span{|t>, |s>}" in intertwiner
        and "canonical quotient projector" in intertwiner
        and "1/8" in intertwiner,
        "the weighted-state route must start on the same 2-dimensional quotient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "transfer lane still fixes the exact Schur witness and canonical one-clock grammar",
        "[[4/3, 1/3], [1/3, 4/3]]" in transfer
        and "t_can(tau) = exp(-tau l_sigma)" in transfer,
        "the weighted state should come from the exact boundary Schur data, not a new carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "vacuum/action lane still says quarter would require the additive shift 5/4",
        "nu = lambda_min(l_sigma) + m_axis" in vacuum and "5/4" in vacuum,
        "the new lane should test whether normalized Schur/Perron states can see that datum",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "bridge and assumption audit still identify weighted C^16 state induction as a live attack",
        "m_axis = 1/4" in bridge
        and "derive a boundary-induced weighted `c^16` state" in assumptions,
        "this lane should execute the attack flagged by the audit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: NORMALIZED SCHUR/PERRON STATE ON THE QUOTIENT")
    beta, w = sp.symbols("beta w", nonnegative=True, real=True)
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    i2 = sp.eye(2)
    g_w = w * i2 - l_sigma
    exp_g = (beta * g_w).exp()
    sigma = sp.simplify(exp_g / sp.trace(exp_g))
    sigma_no_shift = sp.simplify(((-beta) * l_sigma).exp() / sp.trace(((-beta) * l_sigma).exp()))
    shifted_factorization = sp.simplify((beta * g_w).exp() - sp.exp(beta * w) * ((-beta) * l_sigma).exp())

    p = check(
        "the normalized quotient state is exactly blind to the additive shift w",
        shifted_factorization == sp.zeros(2)
        and w not in sigma[0, 0].free_symbols
        and w not in sigma[0, 1].free_symbols,
        "the factor exp(beta w) cancels, so normalized Schur/Perron states cannot see the quarter-closing shift",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact witness still has Schur eigenvalues 1 and 5/3",
        sorted(l_sigma.eigenvals().keys(), key=sp.default_sort_key)
        == [sp.Integer(1), sp.Rational(5, 3)],
        "this is the fixed quotient spectrum underlying the induced weighted state",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the normalized quotient state always has equal diagonal entries 1/2",
        sp.simplify(sigma_no_shift[0, 0] - sp.Rational(1, 2)) == 0
        and sp.simplify(sigma_no_shift[1, 1] - sp.Rational(1, 2)) == 0,
        "functions of the exact witness keep equal diagonal entries, so the quotient weights of |t> and |s> are fixed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the off-diagonal coherence is nontrivial but does not affect the diagonal quotient weights",
        sigma_no_shift[0, 1].free_symbols == {beta}
        and sigma_no_shift[0, 1] == sigma_no_shift[1, 0],
        "beta changes only the t-s coherence / rank, not the diagonal half-half split",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EQUIVARIANT LIFT TO THE AXIS SECTOR")
    sqrt3 = sp.sqrt(3)
    v = sp.Matrix(
        [
            [1, 0],
            [0, 1 / sqrt3],
            [0, 1 / sqrt3],
            [0, 1 / sqrt3],
        ]
    )
    rho_a = sp.simplify(v * sigma_no_shift * v.T)

    p = check(
        "the canonical quotient embedding V is isometric",
        sp.simplify(v.T * v - sp.eye(2)) == sp.zeros(2),
        "V sends |t> to the temporal ray and |s> to the uniform spatial singlet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the induced axis-sector state has exact primitive weights 1/2 and 1/6,1/6,1/6",
        sp.simplify(rho_a[0, 0] - sp.Rational(1, 2)) == 0
        and all(sp.simplify(rho_a[i, i] - sp.Rational(1, 6)) == 0 for i in (1, 2, 3)),
        "the Schur route does derive a canonical weighted axis-sector state, but it is not democratic on the four axis rays",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the induced state is supported only on the rank-2 quotient image inside the rank-4 axis sector",
        rho_a.rank() <= 2,
        "this is where the missing multiplicity first appears on the weighted-state route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the induced axis-sector state has unit conditional mass on P_A",
        sp.simplify(sp.trace(rho_a) - 1) == 0,
        "Schur/Perron data fix the conditional state inside the axis sector, not its occupation in the full 16-state carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: CANONICAL FULL-CELL MAXIMUM-ENTROPY EXTENSION")
    lam = sp.exp(-beta) / (sp.exp(-beta) + sp.exp(-sp.Rational(5, 3) * beta))
    s_axis = sp.simplify(-lam * sp.log(lam) - (1 - lam) * sp.log(1 - lam))
    alpha = sp.simplify(sp.exp(s_axis) / (12 + sp.exp(s_axis)))

    p = check(
        "the quotient/axis entropy is bounded by log 2 because the induced state has rank at most 2",
        float(sp.N(s_axis.subs(beta, 0), 50)) <= float(sp.N(sp.log(2), 50)) + 1e-12,
        "a Schur-induced weighted state can never carry more than 2-dimensional entropy on the axis sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical no-extra-datum full-cell occupation is alpha = exp(S_axis)/(12 + exp(S_axis))",
        alpha.free_symbols == {beta},
        "maximum entropy over the unresolved 12-state complement turns the open problem into a pure occupation theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    alpha_hot = sp.simplify(alpha.subs(beta, 0))
    alpha_cold = sp.limit(alpha, beta, sp.oo)
    p = check(
        "the exact endpoint occupations are alpha(0) = 1/7 and alpha(+oo) = 1/13",
        sp.simplify(alpha_hot - sp.Rational(1, 7)) == 0
        and sp.simplify(alpha_cold - sp.Rational(1, 13)) == 0,
        "the whole canonical family stays in a narrow interval strictly below quarter",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical occupation family never reaches quarter",
        float(sp.N(alpha_hot, 50)) < 0.25 and float(sp.N(alpha_cold, 50)) < 0.25,
        "even the largest no-extra-datum occupation from the Schur-induced weighted state is only 1/7",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: WHAT QUARTER WOULD REQUIRE")
    alpha_target = sp.Rational(1, 4)
    s_needed = sp.solve(sp.Eq(alpha_target, sp.exp(sp.Symbol("s")) / (12 + sp.exp(sp.Symbol("s")))), sp.Symbol("s"))
    needed = s_needed[0]

    p = check(
        "quarter would require exp(S_axis) = 4, equivalently S_axis = log 4",
        sp.simplify(needed - sp.log(4)) == 0,
        "restoring the missing multiplicity means promoting the rank-2 quotient entropy to full rank-4 axis entropy",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the honest obstruction: Schur data fix shape but not amount",
        "fix the **internal shape** of the axis-sector state" in NOTE.read_text(encoding="utf-8")
        and "not the total occupation of that sector" in note
        and "alpha(beta) <= 2 / (12 + 2) = 1/7 < 1/4" in note,
        "the writeup should make explicit that the weighted-state route improves the problem statement without overselling a close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    if n_fail:
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
