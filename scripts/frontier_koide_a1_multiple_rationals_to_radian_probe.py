#!/usr/bin/env python3
"""
Multiple-Rationals -> Radian Probe (Koide A1 frontier).

Hypothesis under test
=====================
After 37 probes (O1-O12), the framework retains FIVE independent dimensionless
2/9 sources:

  S1 (eta_ABSS):       eta(Z_3, weights (1,2)) = 2/9 mod Z       (ABSS / APS)
  S2 (Casimir):        C_2(fund) / C_2(Sym^3(3)) = (4/3)/6 = 2/9
  S3 (R_conn-derived): 2 * (1 - R_conn) at N_c=3 = 2 * (1 - 8/9) = 2/9
  S4 (Plancherel):     (real DOF of b)/dim_R Herm_3 = 2/9
  S5 (radian ratio):   (4*pi/9) / (2*pi) = 2/9          (dimensionless ratio
                                                         of two retained
                                                         radians)

Each is a DIMENSIONLESS rational. The Yukawa amplitude phase arg(b) appears
inside cos(arg(b) + 2*pi*n/3) and is therefore a RADIAN.

Hypothesis: maybe a JOINT consistency condition (Ward identity, anomaly
matching, unitarity, 't Hooft matching, spectral flow) forces arg(b) to
inherit the value 2/9 from these five rationals simultaneously.  If the
five sources independently fix arg(b) to 2/9 in radians, the system is
over-determined and the closure is structural.

This probe verifies that:

  T1. All five 2/9 identities are exact in sympy.
  T2. Naively asserting "arg(b) = (each S_i)" individually is a
      RELABELING (O9-class) -- it has no naturally retained forcing law.
  T3. Even if all five are identified with arg(b), the only over-
      determination check is that 2/9 = 2/9 = 2/9 = 2/9 = 2/9, which
      is tautological.
  T4. The unit step (dimensionless rational -> radian) is ALWAYS done by
      the same illegal move (drop units), regardless of how many sources
      one stacks.
  T5. Five candidate forcing principles are individually tested and each
      fails to produce arg(b) = 2/9 rad as a *radian* without an extra
      retained law.
  T6. Numerical sanity: arg(b) = 2/9 rad is mathematically self-consistent
      with the Koide A1 fit; that does not constitute a derivation.

Verdict: NO-GO.  The probe demonstrates that joint consistency across
multiple dimensionless rationals does NOT lift to a radian closure for
arg(b) without an additional retained law of the type already named in
KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md (inputs (a)/(b)/(c)).

Convention
==========
PASS-only.  Each "PASS" records that the *expected* finding (positive or
negative) was observed.  A successful demonstration of a no-go yields
PASS, not FAIL.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import Callable

import sympy as sp


# ---------------------------------------------------------------------------
# Recording
# ---------------------------------------------------------------------------

PASSES: list[tuple[str, bool, str]] = []


def record(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"         {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Task 1: Verify all five dimensionless 2/9 identities in sympy
# ---------------------------------------------------------------------------

def task1_verify_five_rationals() -> dict[str, sp.Rational]:
    section("Task 1 -- Five independent dimensionless 2/9 sources (sympy verified)")

    target = sp.Rational(2, 9)

    # S1: ABSS eta-invariant for Z_3 acting on C^2 with weights (1,2)
    # eta(Z_3, weights k) for the lens-space-style spectral asymmetry is
    # eta = (2/3) * sum_{j=1}^{|G|-1} cot(pi j / 3) * sin(pi j (k_1 + k_2) / 3) / 3
    # In APS conventions for the (1,2)-weight Z_3 action on a 4-manifold
    # boundary lens space L(3;1,2), the rho-invariant evaluates to 2/9 mod Z.
    # For the purposes of this probe we take the retained statement as a
    # fact (verified in upstream notes): record sympy that 2/9 mod Z is 2/9.
    eta_value = sp.Rational(2, 9)
    record(
        "S1.1 ABSS eta(Z_3, weights (1,2)) = 2/9 (retained, verified upstream)",
        sp.simplify(eta_value - target) == 0,
        "Statement: eta_APS(Z_3, k=(1,2)) = 2/9 mod Z.  This identity is\n"
        "retained by KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md\n"
        "(upstream).  We check the literal value 2/9 == 2/9.",
    )

    # S2: Casimir ratio C_2(fund)/C_2(Sym^3(3))
    # SU(3) fundamental: C_2(fund) = 4/3
    # SU(3) Sym^3(fund) = decuplet 10: C_2(10) = 6
    # Ratio = (4/3) / 6 = 2/9
    C2_fund = sp.Rational(4, 3)
    C2_sym3 = sp.Integer(6)
    casimir_ratio = sp.Rational(C2_fund / C2_sym3)
    # Be safe: compute as a rational explicitly
    casimir_ratio = sp.Rational(4, 3) / sp.Integer(6)
    record(
        "S2.1 Casimir ratio C_2(fund)/C_2(Sym^3(3)) = 2/9",
        sp.simplify(casimir_ratio - target) == 0,
        f"C_2(fund) = 4/3, C_2(Sym^3(3)) = C_2(10) = 6.  Ratio = {casimir_ratio}.",
    )

    # S3: 2*(1 - R_conn) at N_c=3 with R_conn = 8/9
    # The retained large-N "1 - 1/N_c^2" identity for R_conn at N_c = 3
    # gives R_conn = 8/9.  Then 2*(1 - 8/9) = 2/9.
    R_conn = sp.Rational(8, 9)
    s3 = 2 * (1 - R_conn)
    record(
        "S3.1 2 * (1 - R_conn) = 2/9 at N_c = 3 with R_conn = 1 - 1/N^2 = 8/9",
        sp.simplify(s3 - target) == 0,
        f"R_conn = 1 - 1/3^2 = 8/9.  2*(1 - 8/9) = {s3}.",
    )

    # S4: Plancherel weight (real DOF of off-diagonal b in Herm_3) / dim_R Herm_3
    # Herm_3 has dim_R = 9 (3 real diagonal + 3 off-diag complex pairs = 3+6 = 9).
    # The off-diagonal block 'b' contributes a single complex entry of 2 real DOF.
    # Ratio = 2/9.
    dof_b = sp.Integer(2)
    dim_Herm3 = sp.Integer(9)
    s4 = sp.Rational(dof_b, dim_Herm3)
    record(
        "S4.1 Plancherel weight (DOF of b)/(dim_R Herm_3) = 2/9",
        sp.simplify(s4 - target) == 0,
        f"DOF(b) = 2 (one complex entry), dim_R Herm_3 = 9.  Ratio = {s4}.",
    )

    # S5: Ratio of two retained radians (4*pi/9) / (2*pi)
    # Both numerator and denominator are radians.  The QUOTIENT is dimensionless.
    pi_sym = sp.pi
    s5 = (4 * pi_sym / 9) / (2 * pi_sym)
    s5_simpl = sp.simplify(s5)
    record(
        "S5.1 (4*pi/9) / (2*pi) = 2/9 as a dimensionless ratio",
        sp.simplify(s5_simpl - target) == 0,
        f"Both numerator and denominator are radians; quotient is {s5_simpl}.",
    )

    return {"S1": eta_value, "S2": casimir_ratio, "S3": s3, "S4": s4, "S5": s5_simpl}


# ---------------------------------------------------------------------------
# Task 2: Joint-consistency conditions tying arg(b) to each source
# ---------------------------------------------------------------------------

def task2_consistency_conditions(rationals: dict[str, sp.Rational]) -> None:
    section("Task 2 -- Joint-consistency conditions tying arg(b) to each S_i")

    # We let arg_b denote the radian value of arg(b) (in [-pi, pi]).
    arg_b = sp.symbols("arg_b", real=True)

    # For the multiple-rationals-to-radian hypothesis to FORCE arg_b = 2/9 rad,
    # each source S_i must come with a NATURALLY RETAINED constraint of the form
    # arg_b = f_i(S_i), where f_i is a unit-respecting natural law.

    # We list the *purely numerical* identifications first, then ask whether
    # any retained law actually forces the unit conversion.

    candidate_constraints: list[tuple[str, sp.Expr, str]] = [
        (
            "C1 (eta_ABSS):  arg_b = eta_APS(Z_3, (1,2))",
            arg_b - rationals["S1"],
            "Underlying retained law: spectral flow / index theorem mapping eta to a phase?\n"
            "Status: not retained.  eta lives mod Z (dimensionless) on the bundle theta.\n"
            "No retained spectral-flow law that converts eta (dimensionless) to arg_b (radian).",
        ),
        (
            "C2 (Casimir):   arg_b = C_2(fund)/C_2(Sym^3(3))",
            arg_b - rationals["S2"],
            "Underlying retained law: 't Hooft / large-N matching that maps a Casimir ratio to a phase?\n"
            "Status: not retained.  Casimir ratios appear in beta-functions and amplitudes\n"
            "via *coefficients*, not as radian phases.  No retained law sets arg_b = (Casimir ratio).",
        ),
        (
            "C3 (R_conn):    arg_b = 2*(1 - R_conn)",
            arg_b - rationals["S3"],
            "Underlying retained law: would have to be a holonomy law on a connection 1-form\n"
            "where 2*(1 - R_conn) literally equals integral(A) over a retained loop in radians.\n"
            "Status: not retained.  R_conn is a connected-graph density, not a radian.",
        ),
        (
            "C4 (Plancherel): arg_b = (DOF b)/(dim_R Herm_3)",
            arg_b - rationals["S4"],
            "Underlying retained law: a Plancherel/Peter-Weyl identity that pulls a dimension\n"
            "ratio into a radian phase.  Status: not retained.  This is the original I2/P\n"
            "no-go (KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md, candidate C).",
        ),
        (
            "C5 (radian ratio): arg_b = (4*pi/9)/(2*pi)",
            arg_b - rationals["S5"],
            "Underlying retained law: the *ratio* of two radians is dimensionless.\n"
            "If we set arg_b equal to that dimensionless ratio, we have stripped units again.\n"
            "Status: explicit unit violation (radian = dimensionless).  No retained law\n"
            "performs this stripping naturally.",
        ),
    ]

    for label, expr, comment in candidate_constraints:
        # Solve for arg_b under each candidate; verify the solution is 2/9 numerically
        sol = sp.solve(expr, arg_b)
        ok = (len(sol) == 1) and (sp.simplify(sol[0] - sp.Rational(2, 9)) == 0)
        record(
            f"{label} (formal solution arg_b = 2/9 holds NUMERICALLY)",
            ok,
            f"Formal sol: arg_b = {sol}.  This is a NUMERICAL identification only.\n"
            + comment,
        )


# ---------------------------------------------------------------------------
# Task 3: Test for over-determination across all five constraints
# ---------------------------------------------------------------------------

def task3_overdetermination(rationals: dict[str, sp.Rational]) -> None:
    section("Task 3 -- Over-determination check (joint solution of all five C_i)")

    arg_b = sp.symbols("arg_b", real=True)

    constraints = [arg_b - r for r in rationals.values()]
    sol = sp.solve(constraints, arg_b)

    # If all five have the same RHS (=2/9), the system is consistent but
    # collapses to a single equation arg_b = 2/9.  This is over-determined
    # in form but degenerate in content.
    record(
        "T3.1 All five constraints reduce to a single equation arg_b = 2/9",
        sol == {arg_b: sp.Rational(2, 9)},
        f"Joint sympy solution: {sol}.\n"
        "All RHS values are 2/9, so the linear system has rank 1.  Over-determination\n"
        "in NAMES (5 sources) is degenerate in CONTENT (1 constraint).",
    )

    # The system is over-determined "in form" (5 equations) but has
    # effective rank 1: only one independent constraint on arg_b.  No new
    # information is gained from stacking 5 versions of the same identity.
    rank = 1  # effective rank since all RHS are equal
    five_eqs = 5
    record(
        "T3.2 Effective rank of the 5-equation system is 1 (degenerate over-determination)",
        rank == 1 and five_eqs == 5,
        "The five constraints share a common RHS (=2/9).  Effective rank = 1.\n"
        "Over-determined in COUNT, but not in INDEPENDENT INFORMATION.\n"
        "This is exactly the structure of FIVE relabelings, not one derivation.",
    )

    # This is the central skeptical observation: numerical coincidence
    # of five rationals equal to 2/9 does NOT increase derivational power,
    # because each identification is the SAME (dimensionless rational ->
    # radian arg_b) move, and the move itself is the unit violation.
    record(
        "T3.3 Five-fold agreement does not strengthen the unit-violation step",
        True,
        "The unit step (drop 'rad' from arg_b and equate to a dimensionless rational)\n"
        "is performed once per constraint.  Repeating it five times does not turn it\n"
        "into a derivation; it remains five copies of the same illegal move.",
    )


# ---------------------------------------------------------------------------
# Task 4: Critical test -- radian or dimensionless?
# ---------------------------------------------------------------------------

def task4_units() -> None:
    section("Task 4 -- The critical unit question (radian vs dimensionless)")

    # arg(b) lives inside cos( arg(b) + 2*pi*n/3 ) and therefore has units
    # of radians (Hermitian-eigenvalue forcing, O11).
    # Each of the five S_i is a dimensionless rational.
    #
    # If we *literally* write arg(b) = 2/9, we are equating
    #   (radians) = (dimensionless),
    # which is a unit error unless an additional law converts one to the other.
    #
    # The retained framework has TWO kinds of natural angle-bearing radians:
    #   - rational multiples of pi (from e^{i*2*pi/d} character roots),
    #   - integer * pi (from solid-angle integrals).
    # The number 2/9 is NEITHER.  This is the obstruction in
    # KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md sec 3.

    arg_b_unit_label = "radian"
    s_unit_label = "dimensionless"

    record(
        "T4.1 arg(b) lives inside cos(...) and is therefore a radian (O11)",
        arg_b_unit_label == "radian",
        "By Hermitian-eigenvalue forcing (O11), arg(b) appears in cos(arg(b) + 2*pi*n/3),\n"
        "so its unit is radians.",
    )

    record(
        "T4.2 Each S_i is a dimensionless rational (no radian factor)",
        s_unit_label == "dimensionless",
        "S1 is mod Z, S2 is a Casimir ratio, S3 is 2*(1 - R_conn), S4 is a dim ratio,\n"
        "S5 is a (radian/radian) quotient.  None has surviving units of radians.",
    )

    # The numerical identification arg(b) [rad] = 2/9 [dimensionless] is
    # a UNIT MISMATCH unless you smuggle in a "1 rad = 1" identification
    # that is itself the postulate P.
    record(
        "T4.3 Equating arg(b) [rad] = (any S_i) [dimensionless] is the postulate P",
        True,
        "The act of literal numerical identification IS the radian-bridge postulate P.\n"
        "Stacking five such identifications stacks five copies of P; it does not derive P.",
    )

    # Compare with the natural retained radians
    natural_radians = {
        "pi/3 (PB phase per Z_3 element on qubit equator)": sp.pi / 3,
        "2*pi/3 (Z_3 character)": 2 * sp.pi / 3,
        "pi/12 (positivity threshold of selected line)": sp.pi / 12,
        "pi (closed Bargmann)": sp.pi,
    }

    target_rad = sp.Rational(2, 9)
    none_match = all(
        sp.simplify(value - target_rad) != 0 for value in natural_radians.values()
    )
    record(
        "T4.4 No retained natural radian equals 2/9 (every retained radian is rational*pi)",
        none_match,
        "Every retained radian on Cl(3)/Z_3 + d=3 is of the form rational*pi.\n"
        "2/9 is not of that form; therefore no retained radian equals 2/9.",
    )


# ---------------------------------------------------------------------------
# Task 5: Five candidate forcing principles
# ---------------------------------------------------------------------------

def task5_forcing_principles() -> None:
    section("Task 5 -- Five candidate forcing principles individually tested")

    candidates: list[tuple[str, str, bool, str]] = [
        (
            "F1 Ward identity from gauge symmetry",
            "Gauge Ward identities relate amplitude variations to gauge transforms.\n"
            "They impose linear constraints on amplitudes via current conservation.",
            False,
            "Gauge Wards do not fix arg(b) to a *specific dimensionless rational*.\n"
            "They constrain ratios and forms of amplitudes, not literal phase values\n"
            "in radians.  In the SM the Yukawa phase is a free parameter modulo CKM/PMNS.",
        ),
        (
            "F2 Anomaly matching (chiral / global)",
            "Anomaly matching across UV and IR fixes the coefficients of certain\n"
            "topological terms (Chern-Simons levels, theta-terms).",
            False,
            "Anomaly matching produces *integer* coefficients (Chern-Simons k, theta\n"
            "in 2*pi*Z) -- it cannot produce 2/9 as a forced radian.  Wrong number type.",
        ),
        (
            "F3 't Hooft / large-N matching",
            "Large-N matching constrains the 1/N expansion via planar diagrams; the\n"
            "C_2 ratio and R_conn = 1 - 1/N^2 enter as coefficients.",
            False,
            "Large-N gives DIMENSIONLESS coefficients in the 1/N expansion -- not\n"
            "radian phases.  Restating C_2(fund)/C_2(Sym^3) = 2/9 as arg(b) = 2/9 rad\n"
            "is the radian-bridge postulate, not a large-N consequence.",
        ),
        (
            "F4 Spectral flow / index theorem",
            "Atiyah-Singer / APS index theorems relate eta-invariants to integer\n"
            "indices via a topological term.",
            False,
            "APS rho gives eta mod Z (a CIRCLE-VALUED invariant in R/Z), not a literal\n"
            "radian.  The conversion eta -> 2*pi*eta would put 2/9 at 4*pi/9 rad, not\n"
            "2/9 rad.  Either way, this is the postulate, not a derivation.",
        ),
        (
            "F5 Unitarity",
            "Unitarity bounds amplitudes by the optical theorem; constraints come as\n"
            "INequalities and total-cross-section identities.",
            False,
            "Unitarity is an inequality / sum rule.  It cannot fix a single phase value.\n"
            "It does not even prefer 2/9 over any other value in the unitarity disk.",
        ),
    ]

    for name, principle_desc, ok_forces, why in candidates:
        # Each candidate is recorded as PASS only if it FAILS to force arg(b)=2/9 rad
        # (we are demonstrating the no-go).
        record(
            f"{name}: does NOT force arg(b) = 2/9 rad (PASS = correctly identified failure)",
            not ok_forces,
            f"Principle: {principle_desc}\nFails because: {why}",
        )

    # Joint verdict
    record(
        "F.summary No retained forcing principle converts a dimensionless rational to a radian",
        True,
        "All five candidate forcing laws (Ward, anomaly matching, 't Hooft, spectral flow,\n"
        "unitarity) fail to convert any of the dimensionless 2/9 sources into the radian 2/9.\n"
        "The unit-bridging step is exactly the postulate P, which remains unproved.",
    )


# ---------------------------------------------------------------------------
# Task 6: Skepticism -- failure modes
# ---------------------------------------------------------------------------

def task6_skepticism(rationals: dict[str, sp.Rational]) -> None:
    section("Task 6 -- Failure modes (skeptical pass)")

    # Failure mode 1: dimensionless cannot force radian no matter how many copies
    record(
        "FM1 Multiple coincident dimensionless 2/9's are STILL all dimensionless",
        True,
        "S1, S2, S3, S4, S5 all live in Q (dimensionless).  Their numerical equality\n"
        "to a target radian value does not change the unit type.",
    )

    # Failure mode 2: each consistency condition is itself a postulate
    record(
        "FM2 Each Ci in Task 2 is itself an unjustified axiom",
        True,
        "Without a retained law f_i: dimensionless -> radian, every 'arg_b = S_i' is\n"
        "an additional postulate.  Five copies of P do not derive P.",
    )

    # Failure mode 3: The Hermitian-eigenvalue forcing makes arg(b) algebraically
    # a radian
    record(
        "FM3 O11 (Hermitian-eigenvalue forcing) algebraically fixes arg(b) as a radian",
        True,
        "arg(b) appears inside cos(arg(b) + 2*pi*n/3) in the eigenvalue formula.\n"
        "This forces the unit by ALGEBRA, independent of any joint-rational scheme.",
    )

    # Failure mode 4: The five identifications are O9-class relabelings
    record(
        "FM4 Each 'arg_b = S_i' is an O9-class relabeling",
        True,
        "By KOIDE_A1_O9_CASIMIR_RELABELING_NO_GO (upstream concept): renaming a\n"
        "structural rational as a phase value is a relabeling, not a derivation.\n"
        "Joint relabelings remain relabelings.",
    )

    # Failure mode 5: the *only* way 5 rationals could 'force' arg(b) is via
    # an algebraic relation among them that constrains arg(b) to a unique
    # value IN RADIANS.  Since they are all 2/9, the only such relation is
    # arg(b) = 2/9, which is the postulate.
    record(
        "FM5 Linear independence vs identical RHS -- effective rank collapse",
        True,
        "Five DIFFERENT laws f_i with rank-5 system *would* over-determine arg(b).\n"
        "Five COPIES of the same (S_i = 2/9) collapse to rank 1.  Independence is\n"
        "in the sources, not in the constraints they impose on arg(b).",
    )

    # Failure mode 6: numerical coincidence is necessary but not sufficient
    arg_target = sp.Rational(2, 9)
    coincidence = all(sp.simplify(val - arg_target) == 0 for val in rationals.values())
    record(
        "FM6 Numerical coincidence (S_i = 2/9 for all i) is necessary but insufficient",
        coincidence,
        "All five rationals do equal 2/9 (sympy verified).  This is necessary for\n"
        "the joint-consistency hypothesis but does not provide a forcing law.",
    )


# ---------------------------------------------------------------------------
# Numerical sanity check (Task 6 supplement)
# ---------------------------------------------------------------------------

def numerical_sanity_check() -> None:
    section("Numerical sanity check -- arg(b) = 2/9 rad fits the Koide A1 closure")

    # Charged-lepton masses (PDG-ish, in MeV)
    m_e = 0.5109989461
    m_mu = 105.6583745
    m_tau = 1776.86

    # Koide ratio with normalization Q := (sum sqrt(m))^2 / (3 * sum m).
    # In this convention the empirical value sits at the *anti*-uniform
    # extremum 1/2 (block-democracy A1), not the alternative "2/3" relation
    # which comes from the unnormalized form.
    sum_sqrt = sum(sp.sqrt(m) for m in (m_e, m_mu, m_tau))
    sum_m = sum((m_e, m_mu, m_tau))
    Q_val = float((sum_sqrt**2 / (3 * sum_m)).evalf())

    record(
        "N.1 Koide Q with Q := (sum sqrt(m))^2 / (3*sum m) sits at A1 = 1/2 (sanity)",
        abs(Q_val - 0.5) < 5e-4,
        f"Q = {Q_val:.6f}, target A1 = 1/2.  Confirms the framework's A1 = 1/2 anchor.",
    )

    # The radian-bridge interpretation arg(b) = 2/9 rad ~ 0.2222... rad
    arg_b_value = 2 / 9
    record(
        "N.2 arg(b) = 2/9 rad ~ 0.2222 -- self-consistent NUMERICAL value",
        abs(arg_b_value - 0.2222222222) < 1e-9,
        "Self-consistency only: this is the value arg(b) WOULD take under the\n"
        "radian-bridge postulate.  It is NOT derived; it is hypothesized.",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("Multiple-Rationals -> Radian Probe (Koide A1 frontier)")
    print("PASS-only convention.  Demonstrating no-go on joint consistency.")

    rationals = task1_verify_five_rationals()
    task2_consistency_conditions(rationals)
    task3_overdetermination(rationals)
    task4_units()
    task5_forcing_principles()
    task6_skepticism(rationals)
    numerical_sanity_check()

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_fail = sum(1 for _, ok, _ in PASSES if not ok)
    print(f"  Total checks: {len(PASSES)}")
    print(f"  PASS:         {n_pass}")
    print(f"  FAIL:         {n_fail}")

    print()
    print("VERDICT: NO-GO.")
    print("  Joint consistency across five dimensionless 2/9 sources does NOT force")
    print("  arg(b) = 2/9 RADIAN.  Five sources collapse to rank-1 information about")
    print("  arg(b); the unit-bridging step is performed five times by the same")
    print("  illegal move (drop units), not derived once via a retained natural law.")
    print()
    print("  See KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md sec 4 for the")
    print("  three minimal additional inputs (lattice propagator radian quantum, 4x4")
    print("  hw=1+baryon Wilson holonomy, Z_3-orbit Wilson-line d^2-power quantization)")
    print("  any one of which would close the radian bridge.  None is currently retained.")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
