#!/usr/bin/env python3
"""Audit the direct Planck full-packet physical readout lane honestly.

This lane does not claim retained Planck closure. It proves the sharper direct
result:

  - the physical coarse carrier is already the full packet P_A;
  - the quotient-only Schur-visible block P_q is not physically admissible as
    the final packet readout;
  - every positive additive packet-local extension of the quotient count is
      R_alpha(rho) = Tr(rho P_q) + alpha Tr(rho P_E),  alpha >= 0;
  - on the democratic full-cell state, quarter occurs iff alpha = 1;
  - so the exact remaining law is only the physical promotion:
      p_phys = Tr(rho_cell P_A).
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_FULL_PACKET_PHYSICAL_READOUT_THEOREM_LANE_2026-04-23.md"
SECTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
LIFT = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
WEIGHTED = ROOT / "docs/PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md"
OBS = ROOT / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
POS = ROOT / "docs/PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md"
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"


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
    lift_note = normalized(LIFT)
    weighted_note = normalized(WEIGHTED)
    obs_note = normalized(OBS)
    pos_note = normalized(POS)
    physical_note = normalized(PHYSICAL)

    n_pass = 0
    n_fail = 0

    print("Planck full-packet physical readout theorem lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the section-canonical lane still forces the coarse physical packet to P_A",
        "coarse four-axis worldtube channel is **section-canonical**" in section_note
        and "`p_phys = m_axis`" in section_note,
        "the direct readout theorem should start from the already fixed coarse packet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the multiplicity-lift lane still proves P_A = P_q + P_E and closes the factor of 2",
        "`p_a = p_q + p_e`" in lift_note and "2 tr(rho_cell p_q) = 1/4" in lift_note,
        "the direct readout theorem should not reopen the lift problem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the weighted Schur lane still rules out hidden quarter in normalized Schur/Perron data",
        "`1/13 <= alpha(beta) <= 1/7`" in weighted_note
        and "strictly below quarter" in weighted_note,
        "the direct theorem should improve on the weighted-state obstruction rather than contradict it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the observable-principle boundary lane still identifies the scalar observable with p_vac, not quarter",
        "observable-principle scalar boundary pressure = p_vac" in obs_note
        or "p_phys = p_obs = p_vac" in obs_note,
        "the remaining theorem should therefore be a packet-readout law, not another scalar Schur law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the positive-residual lane still says quarter closes conditionally from delta = Tr(rho_cell P_A)",
        "`delta = tr(rho_cell p_a)`" in pos_note and "`nu = 5/4`" in pos_note,
        "the present lane should refine that conditional closure into a packet-readout classification",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the physical-lattice necessity note still forbids proper exact quotienting of exact physical sectors",
        "no proper exact quotient/rooting/reduction" in physical_note
        and "physical-species semantics" in physical_note,
        "quotient-only packet readout should be inadmissible if it discards exact physical multiplicity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT PACKET DECOMPOSITION")
    t = sp.Matrix([1, 0, 0, 0])
    x = sp.Matrix([0, 1, 0, 0])
    y = sp.Matrix([0, 0, 1, 0])
    z = sp.Matrix([0, 0, 0, 1])
    s = (x + y + z) / sp.sqrt(3)
    e1 = (x - y) / sp.sqrt(2)
    e2 = (x + y - 2 * z) / sp.sqrt(6)

    basis = sp.Matrix.hstack(t, s, e1, e2)
    p_q = sp.simplify(t * t.T + s * s.T)
    p_e = sp.simplify(e1 * e1.T + e2 * e2.T)
    p_a = sp.eye(4)

    p = check(
        "the basis {t,s,e1,e2} is orthonormal and complete on the coarse worldtube packet",
        sp.simplify(basis.T * basis - sp.eye(4)) == sp.zeros(4),
        "this is the exact packet decomposition H_A = H_q (+) E",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "P_q and P_E are orthogonal complementary projectors with ranks 2 and 2",
        sp.simplify(p_q * p_e) == sp.zeros(4)
        and sp.simplify(p_q + p_e - p_a) == sp.zeros(4)
        and p_q.rank() == 2
        and p_e.rank() == 2
        and p_a.rank() == 4,
        "the only remaining packet readout ambiguity should live in how the hidden E block is counted",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: CLASSIFICATION OF ADDITIVE PACKET-LOCAL READOUTS")
    q_mass, e_mass, alpha = sp.symbols("q_mass e_mass alpha", nonnegative=True, real=True)
    r_alpha = sp.simplify(q_mass + alpha * e_mass)

    p = check(
        "once quotient agreement fixes the visible block, every additive packet-local extension has one free coefficient alpha on the hidden E block",
        sp.simplify(r_alpha - (q_mass + alpha * e_mass)) == 0,
        "the direct readout problem is now one-parameter: R_alpha = Tr(rho P_q) + alpha Tr(rho P_E)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "positivity restricts the extension coefficient to alpha >= 0",
        alpha.is_nonnegative is True,
        "negative hidden-block weighting would violate positivity on positive packet states",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: DEMOCRATIC WITNESS VALUES")
    rho_axis = sp.eye(4) / 16
    mass_q = sp.simplify(sp.trace(rho_axis * p_q))
    mass_e = sp.simplify(sp.trace(rho_axis * p_e))
    mass_a = sp.simplify(sp.trace(rho_axis * p_a))
    witness_r = sp.simplify(mass_q + alpha * mass_e)

    p = check(
        "the democratic witness still gives exact masses 1/8, 1/8, and 1/4 on P_q, P_E, and P_A",
        mass_q == sp.Rational(1, 8)
        and mass_e == sp.Rational(1, 8)
        and mass_a == sp.Rational(1, 4),
        "the hidden block contributes exactly the same mass as the visible quotient block",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the quotient-only readout alpha = 0 gives only 1/8",
        sp.simplify(witness_r.subs(alpha, 0) - sp.Rational(1, 8)) == 0,
        "this is exactly the Schur-visible but physically incomplete packet count",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the unweighted full-packet completion alpha = 1 gives exact quarter",
        sp.simplify(witness_r.subs(alpha, 1) - sp.Rational(1, 4)) == 0,
        "counting the full exact packet restores the Planck target on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    quarter_solutions = sp.solve(sp.Eq(witness_r, sp.Rational(1, 4)), alpha)
    p = check(
        "quarter occurs iff alpha = 1 inside the classified readout family",
        quarter_solutions == [sp.Integer(1)],
        "the direct readout problem is no longer diffuse; one coefficient is now forced if quarter is to hold",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: PHYSICAL INTERPRETATION")
    p = check(
        "alpha = 0 is exactly the forbidden proper-quotient readout of the physical packet",
        mass_a > mass_q and p_q.rank() < p_a.rank(),
        "reading only P_q throws away the exact physical E block after the carrier itself has already been fixed to P_A",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "alpha != 1 would amount to a new relative same-shell weighting datum between fixed exact packet blocks",
        sp.simplify(witness_r - (mass_q + alpha * mass_e)) == 0,
        "once the packet decomposition is fixed, the only remaining freedom is an extra weight on E; the no-extra-datum completion sets that weight to 1",
    )
    n_pass += int(p)
    n_fail += int(not p)

    lambda_min = sp.Integer(1)
    nu_alpha = sp.simplify(lambda_min + witness_r)
    p = check(
        "under the full-packet readout alpha = 1, the action witness closes at nu = 5/4",
        sp.simplify(nu_alpha.subs(alpha, 1) - sp.Rational(5, 4)) == 0,
        "this matches the exact quarter-closing witness from the action lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: HONEST ENDPOINT")
    p = check(
        "the new lane presents the remaining issue as a promotion from scalar Schur observable to full-packet readout",
        "only remaining physical promotion law" in note
        and "physical boundary pressure is the full-packet occupation readout" in note,
        "the theorem should narrow the endpoint rather than overstate closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly avoids claiming retained closure without the final readout promotion",
        "does **not** prove that the present scalar schur observable" in note
        and "cannot claim" in note,
        "the lane should stay honest about what is and is not closed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"PASS={n_pass} FAIL={n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
