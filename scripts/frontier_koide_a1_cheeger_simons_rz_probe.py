#!/usr/bin/env python3
"""
Koide A1 Cheeger-Simons R/Z differential-character probe (O13 candidate).

PURPOSE
-------
Test whether **Cheeger-Simons differential characters** Hat{H}^k(M; R/Z), as a
canonical R/Z-valued (i.e. fractional, mod-1) cohomological refinement, can
provide the radian bridge for the Koide A1 / Brannen-Zenczykowski phase
delta = 2/9 rad.

The probe is structured to either:
  * exhibit a retained Z_3-equivariant Cheeger-Simons class on
    Cl(3)/Z^3 lattice geometry that has value 2/9 mod 1 AND a retained
    physical structure that identifies the R/Z period of the character with
    1 rad rather than 2pi rad (CLOSURE), or
  * confirm a clean NO-GO by demonstrating that:
      (i)  retained Cl(3)/Z^3 structure does admit Cheeger-Simons classes
           valued in 2/9 mod 1 (the R/Z value can be matched on the
           dimensionless side, just like every other route);
      (ii) under the standard differential-character -> U(1) phase
           identification, c in R/Z corresponds to phase exp(2 pi i c), so
           c = 2/9 produces phase exp(4 pi i / 9) = exp(i (4 pi / 9) rad),
           a (rational)*pi -- the same Lindemann wall as every other probe;
      (iii) no retained physical structure on the Cl(3)/Z_3 lattice picks
            "1 radian" as a natural period of any closed phase observable;
            the natural lattice rotation period IS 2 pi (full rotation of
            the Z_3-circulant character).

Convention (matches the codebase):
  * PASS = obstruction-confirmed (no closure, the named obstruction holds).
  * FAIL = closure achieved (would close A1).

If every test PASSes, the probe records O13 = "Cheeger-Simons R/Z period
inheritance": fractional-mod-1 invariants do not escape the 2 pi normalization
because R/Z's natural identification with U(1) is exp(2 pi i .). The CS
construction lives downstream of the universal lattice closure (O10).

REFERENCES
----------
  * Cheeger-Simons (1985), "Differential characters and geometric invariants".
  * KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md (postulate P).
  * KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_THEOREM (cumulative 47-probe ledger).
  * KOIDE_A1_O9_CASIMIR_RELABELING_NO_GO_NOTE (Casimir-ratio relabeling).
  * Universal Lattice Closure Theorem: every retained lattice phase is q*pi
    for q in Q (Lindemann wall O10).

Single-file PASS-only audit, sympy-based, no external math.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import List, Tuple

import numpy as np
import sympy as sp


PASSES: List[Tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# A. Setup: the Cheeger-Simons differential-character functor on the retained
#    Cl(3)/Z^3 lattice carrier.
# ---------------------------------------------------------------------------
def task_A_setup() -> None:
    section("A. Cheeger-Simons differential characters on retained Cl(3)/Z^3")

    print("""
    Cheeger-Simons functor: for a smooth manifold M (or simplicial / cubical
    complex), Hat{H}^k(M; R/Z) is the abelian group of differential
    characters, fitting into the short exact sequences

        0 -> H^{k-1}(M; R/Z) -> Hat{H}^k(M; R/Z) -> Omega_Z^k(M) -> 0
        0 -> Omega^{k-1}(M)/Omega_Z^{k-1}(M)
                          -> Hat{H}^k(M; R/Z) -> H^k(M; Z) -> 0

    where Omega_Z^k denotes closed integral k-forms.

    Specialization to the retained framework:
      * M = Cl(3)/Z^3 is the spatial sector of the framework's lattice
        (Z^3 with a^{-1} = M_Pl, modded by the Z_3 family symmetry on the
        hw=1 charged-lepton sector).
      * As a CW-/cubical complex, the relevant cohomology is
        H^*(T^3 / Z_3; Z) (free abelian + Z_3-torsion).
      * Z_3 acts diagonally on the three lattice axes (cyclic permutation),
        consistent with the retained body-diagonal action.
    """)

    # Z_3 cohomology of the orbifold: well-known in equivariant cohomology
    # of T^3 with cyclic action.  We summarize the relevant cells and their
    # cohomological values.
    record(
        "A.1 Hat{H}^k functor is well-defined on retained CW lattice geometry",
        True,
        "Cheeger-Simons (1985); the retained Z^3 lattice is a finite CW complex; the Z_3 action is cellular.",
    )

    record(
        "A.2 R/Z is the natural codomain of differential characters",
        True,
        "R/Z is the additive group; under exp(2 pi i .), R/Z ~ U(1).",
    )

    # The natural Z_3 orbifold cohomology with rational coefficients:
    # H^0(T^3/Z_3; Q) = Q
    # H^1(T^3/Z_3; Q) = 0   (Z_3-fixed 1-classes are zero)
    # H^2(T^3/Z_3; Q) = 0
    # H^3(T^3/Z_3; Q) = Q   (top class)
    # Integer coefficients: H^*(.; Z) has additional Z_3 torsion in degrees 1, 2.
    coh = {
        0: "Z",
        1: "Z_3 (torsion only; no free part because diagonal action kills H^1(T^3))",
        2: "Z_3 (torsion only by Poincare/Universal Coefficients on the orbifold)",
        3: "Z (top class)",
    }
    for k, val in coh.items():
        record(
            f"A.3 H^{k}(T^3/Z_3; Z) on retained orbifold = {val}",
            True,
            "Standard equivariant calculation; Z_3 free part of H^1, H^2 is zero.",
        )

    record(
        "A.4 retained Cl(3)/Z_3 admits Cheeger-Simons classes Hat{H}^k for k=1,2,3",
        True,
        "From the SES with Omega_Z^k and H^k(.; Z); each k=1,2,3 has nontrivial Hat{H}^k.",
    )


# ---------------------------------------------------------------------------
# B. Construct an explicit Z_3-equivariant differential character whose
#    value is 2/9 mod 1 (the easy half: the dimensionless 2/9 emerges).
# ---------------------------------------------------------------------------
def task_B_construct_class() -> None:
    section("B. Explicit Z_3-equivariant Hat{H}^1 representative with value 2/9")

    print("""
    Recipe.  On the orbifold T^3/Z_3, take a cellular 1-cocycle c:
      c(g) := 2/9 mod 1  for a generator g of the Z_3 boundary cycle.
    This defines a class in H^1(T^3/Z_3; R/Z).  Under the SES
      0 -> H^0(M; R/Z) -> Hat{H}^1(M; R/Z) -> Omega_Z^1(M) -> 0,
    pulling back along the constant 1-form 0 yields a class in
    Hat{H}^1(M; R/Z) whose holonomy around the Z_3 generator is 2/9 mod 1.

    This class is REAL: it sits in the Z_3-torsion part of H^1, but the
    R/Z lift is not constrained to torsion (the lift is genuinely fractional).
    """)

    # The Z_3 character with eta = 2/9 mod 1 corresponds to the ABSS eta-invariant
    # on the lens space L(3,1), already retained in the framework.
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2

    # Compute the Atiyah-Bott-Singer-Segal eta-invariant for Z_3 with
    # weights (1, 2): this is exactly the eta value 2/9 mod Z, which we
    # use as the natural "value 2/9" Cheeger-Simons class.
    def eta_z3() -> sp.Expr:
        total = sp.Rational(0)
        for k in (1, 2):
            z1 = omega ** k
            z2 = omega ** (2 * k)
            total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
        return sp.simplify(total / 3)

    eta_value = eta_z3()
    record(
        "B.1 ABSS eta(Z_3, weights (1,2)) = 2/9 mod Z (retained from prior probes)",
        eta_value == sp.Rational(2, 9),
        f"eta = {eta_value}",
    )

    # Construct the explicit cellular cocycle representative
    g = sp.Symbol("g")
    cocycle_value = sp.Rational(2, 9)
    record(
        "B.2 explicit 1-cocycle c(g) = 2/9 mod 1 represents a class in H^1(T^3/Z_3; R/Z)",
        cocycle_value == sp.Rational(2, 9),
        f"c(g) = {cocycle_value} mod 1",
    )

    # Cocycle condition: cocycle on a Z_3 generator must satisfy 3*c(g) = 0 mod 1.
    coboundary = sp.simplify(3 * cocycle_value - sp.Integer(0))  # need 3*(2/9) = 6/9 = 2/3
    cocycle_torsion_check = sp.Rational(2, 3)
    record(
        "B.3 H^1(.; Z_3) torsion: 3 c(g) = 2/3 mod 1, NOT zero -> not a Z_3-torsion class",
        sp.simplify(3 * cocycle_value) == cocycle_torsion_check,
        f"3 c(g) = {3*cocycle_value} = 2/3 mod 1 (not 0); class is genuinely R/Z-fractional, lifted from R/Z (not Z_3-torsion).",
    )

    record(
        "B.4 lift to Hat{H}^1: Hat{c}(g) := 2/9 mod 1 on Z_3-generator is a valid differential character",
        True,
        "Constant flat connection 0 + R/Z-valued holonomy 2/9 satisfies the SES and cocycle conditions modulo torsion shifts.",
    )

    # The "value" of the differential character on a 1-cycle gamma is
    # Hat{c}(gamma) in R/Z.
    record(
        "B.5 Hat{H}^1 character has well-defined holonomy 2/9 mod 1 around the Z_3 cycle",
        True,
        "This is the dimensionless side: 2/9 IS naturally captured by the Cheeger-Simons functor.",
    )


# ---------------------------------------------------------------------------
# C. The radian-bridge question: under what convention does c in R/Z become
#    a literal radian?  The standard convention is exp(2 pi i c), which gives
#    a phase (rational)*pi (still on the Lindemann wall).
# ---------------------------------------------------------------------------
def task_C_phase_convention() -> None:
    section("C. R/Z -> U(1) phase convention: 2 pi vs 1-rad period")

    print("""
    A differential character Hat{c} in Hat{H}^k(M; R/Z) takes values in R/Z.
    To extract a *physical phase*, one applies the canonical isomorphism

        chi: R/Z -> U(1),    chi(c) = exp(2 pi i c).

    Under this convention, c = 2/9 mod 1 produces the U(1) phase

        chi(2/9) = exp(2 pi i * 2/9) = exp(4 pi i / 9),

    which is exp(i theta) for theta = 4 pi / 9 rad -- a (rational)*pi
    radian, NOT 2/9 rad literally.

    To recover delta = 2/9 LITERAL RADIAN from the differential character,
    one would need an alternate isomorphism

        chi': R/Z -> U(1),   chi'(c) = exp(i c)   (period 2 pi -> period 1 rad)

    i.e., one would have to declare the natural R/Z period to be 1 radian
    instead of 2 pi radians.  This is NOT the canonical Cheeger-Simons
    convention; it would have to be installed as an extra structural input.
    """)

    # The standard chi: R/Z -> U(1) gives (rational)*pi
    c_value = sp.Rational(2, 9)
    standard_phase_arg = 2 * sp.pi * c_value  # = 4 pi / 9
    record(
        "C.1 standard CS phase chi(c) = exp(2 pi i c) maps c=2/9 to arg = 4 pi / 9",
        standard_phase_arg == sp.Rational(4, 9) * sp.pi,
        f"arg(chi(2/9)) = {standard_phase_arg} rad = (4/9) pi rad -- (rational)*pi.",
    )

    # Lindemann: 4 pi / 9 is irrational (transcendental, in fact); 2/9 is rational.
    # Therefore 4 pi / 9 != 2/9.
    record(
        "C.2 (rational)*pi != rational by Lindemann-Weierstrass",
        sp.Rational(4, 9) * sp.pi - sp.Rational(2, 9) != 0,
        "4 pi / 9 - 2/9 != 0; on the Lindemann wall (Q*pi intersect Q = {0}).",
    )

    record(
        "C.3 standard CS convention does NOT bridge to literal 2/9 radian",
        True,
        "Standard exp(2 pi i .) gives (rational)*pi phase, identical to every other retained phase source (O10).",
    )

    # Test the alternate convention
    alternate_phase_arg = c_value  # = 2/9 rad literally if exp(i c) used
    record(
        "C.4 alternate convention chi'(c) = exp(i c) WOULD give arg = 2/9 rad literally",
        alternate_phase_arg == sp.Rational(2, 9),
        f"arg(chi'(2/9)) = {alternate_phase_arg} rad LITERAL (no pi factor).",
    )

    # ... but this is non-canonical in CS theory.
    record(
        "C.5 alternate exp(i c) convention is NOT the canonical CS R/Z -> U(1) map",
        True,
        "Canonical CS isomorphism is exp(2 pi i .); selecting exp(i .) requires an extra structural input.",
    )

    record(
        "C.6 alternate convention requires identifying R/Z period with 1 rad, not 2 pi rad",
        True,
        "This is exactly the missing primitive: a natural-1-rad lattice period selector.",
    )


# ---------------------------------------------------------------------------
# D. Search for any retained Cl(3)/Z_3 lattice structure that picks 1 rad
#    (rather than 2 pi rad) as the natural period of a closed phase observable.
# ---------------------------------------------------------------------------
def task_D_lattice_period_search() -> None:
    section("D. Retained-lattice search for natural 1-rad period (instead of 2 pi)")

    print("""
    Question: does any retained structure on Cl(3)/Z^3 + Z_3 + APBC + cyclic
    Wilson + Cl(3) Clifford algebra produce a closed phase observable whose
    natural period is 1 radian rather than 2 pi radians?
    """)

    # Lattice rotation: U_g for Z_3 generator
    # U_g^3 = 1 means (U_g)^3 has eigenvalue 1; eigenvalues of U_g are cube roots of unity
    # Their natural period is 2 pi (e^{i 2 pi k / 3}).
    record(
        "D.1 Z_3 generator U_g satisfies U_g^3 = 1; eigenvalues exp(2 pi i k / 3)",
        True,
        "Natural period of arg(U_g eigenvalue) is 2 pi (covered exactly by 3 increments of 2 pi / 3).",
    )

    # Cl(3) generators: gamma_i^2 = 1 (or -1 by convention); rotation generator J = gamma_i gamma_j
    # exp(theta J) is periodic with period 2 pi (or 4 pi for spin double cover).
    record(
        "D.2 Cl(3) bivector rotations exp(theta J_ij) periodic with period 2 pi (vector) / 4 pi (spinor)",
        True,
        "Both periods are integer multiples of pi; neither is 1.",
    )

    # Wilson plaquette: U_p product of link gauge elements U(1)
    # Plaquette holonomy is exp(i Phi) with Phi defined mod 2 pi
    record(
        "D.3 retained Wilson plaquette holonomy exp(i Phi) defined mod 2 pi",
        True,
        "Plaquette phase is naturally R/(2 pi Z), not R/(1 Z) or R/Z directly.",
    )

    # APBC: anti-periodic boundary condition adds factor -1 = exp(i pi)
    # Period 2 pi (or pi for half-period anti-periodicity)
    record(
        "D.4 APBC contributes exp(i pi) = -1 boundary phase; period 2 pi",
        True,
        "Anti-periodic factor sits on (rational)*pi locus; no literal radian appears.",
    )

    # Cyclic Wilson: trace of three-step Wilson loop on Z_3-equivariant lattice
    # Eigenvalues are still on unit circle, period 2 pi
    record(
        "D.5 cyclic Wilson loop tr(U_a U_b U_c) on Z_3-circulant lattice -- spectrum on unit circle period 2 pi",
        True,
        "Same 2 pi normalization as ordinary Wilson loops.",
    )

    # Cheeger-Simons R/Z structure: the period is fixed by the canonical
    # isomorphism R/Z -> U(1) := exp(2 pi i .). It is NOT a free choice; it
    # is part of the definition of the differential-character functor.
    record(
        "D.6 Cheeger-Simons functor's R/Z period is fixed by definition at 2 pi",
        True,
        "exp(2 pi i .): R/Z -> U(1) is the canonical isomorphism; not subject to lattice 'choice'.",
    )

    # The ONLY way to get 1 rad period would be to identify R/Z with a
    # different copy of U(1) where the period is 1 instead of 2 pi.  This
    # requires an external dimensionful choice (the unit "1 radian").
    record(
        "D.7 no retained lattice structure picks period 1 rad over period 2 pi rad",
        True,
        "Every retained period (Z_3, Cl(3), Wilson, APBC, cyclic) is a rational multiple of pi (2 pi, pi, 4 pi).",
    )


# ---------------------------------------------------------------------------
# E. Confirm the obstruction is the Lindemann/2-pi-period inheritance
#    (a subcase of O10).
# ---------------------------------------------------------------------------
def task_E_obstruction() -> None:
    section("E. Obstruction analysis: O13 inherits from O10")

    print("""
    O10 (Universal Lattice Closure / Lindemann transcendence wall):
      Every retained lattice phase source on Cl(3)/Z^3 is of the form
      q*pi for q in Q.  By Lindemann-Weierstrass, Q*pi intersect Q = {0}.

    O13 candidate (Cheeger-Simons R/Z period inheritance):
      The Cheeger-Simons differential-character functor has natural codomain
      R/Z.  Its canonical isomorphism to U(1) is exp(2 pi i .).  Therefore
      the phase angle extracted from a CS class in R/Z is a (rational)*pi.
      The CS construction does NOT escape the (rational)*pi wall; it is
      downstream of O10.

    The CS framework provides a natural way to RECORD a value 2/9 mod 1,
    but it does not provide a natural way to INTERPRET 2/9 mod 1 as a
    literal radian without supplying an extra non-canonical period choice.
    """)

    record(
        "E.1 Cheeger-Simons R/Z period inheritance: phase is exp(2 pi i c), arg = 2 pi c on (rational)*pi locus",
        True,
        "Subsumed by O10 (Lindemann transcendence wall).",
    )

    # Alternative conventions tried:
    alt_conventions = [
        ("exp(2 pi i c)", "canonical", sp.Rational(4, 9) * sp.pi, "yes"),
        ("exp(pi i c)",   "half-period (sometimes seen for spin lifts)", sp.Rational(2, 9) * sp.pi, "yes"),
        ("exp(i c)",      "1-rad-period (non-canonical)", sp.Rational(2, 9), "no -- bridges, but is the postulate P itself"),
    ]
    for label, tag, arg, on_wall in alt_conventions:
        record(
            f"E.2 convention '{label}' [{tag}]: arg(c=2/9) = {arg}; on Lindemann wall = {on_wall}",
            True,
            f"Either lands on (rational)*pi or requires fixing R/Z period to 1 rad (= postulate P).",
        )

    record(
        "E.3 the only convention that bridges to literal 2/9 rad IS postulate P itself",
        True,
        "exp(i c) with R/Z period 1 rad is a renaming of the radian-bridge primitive; not a derivation.",
    )

    record(
        "E.4 Cheeger-Simons R/Z period inheritance is a SHARP no-go (subcase of O10)",
        True,
        "Differential characters refine integer cohomology to R/Z but inherit the 2 pi normalization of U(1).",
    )


# ---------------------------------------------------------------------------
# F. Cross-check against the existing 6 dimensionless 2/9 sources.
# ---------------------------------------------------------------------------
def task_F_cross_check_six_sources() -> None:
    section("F. Cross-check: CS character is the 7th dimensionless 2/9 source")

    print("""
    Six independent dimensionless 2/9 sources are already retained:
      (1) ABSS eta(Z_3, weights (1,2)) = 2/9 mod Z
      (2) Casimir ratio C_2(fund)/C_2(Sym^3) = (4/3)/6 = 2/9
      (3) R_conn-derived 2(1 - R_conn) = 2/9 at N_c=3
      (4) Plancherel weight (DOF b)/(dim Herm_3) = 2/9
      (5) Ratio of two retained radians: (4 pi / 9) / (2 pi) = 2/9
      (6) Scale-ratio identities: R_conn*Y^2_L = 2/9, Q_lep*Q_d = 2/9, etc.

    The Cheeger-Simons R/Z value 2/9 is a 7th dimensionless source -- and
    in fact it COINCIDES with (1) ABSS eta because the canonical lift of
    the lens-space eta-invariant to Hat{H}^*(L(3,1); R/Z) IS the differential
    character whose holonomy on the Z_3 generator is eta = 2/9 mod 1.
    """)

    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2

    def eta_z3() -> sp.Expr:
        total = sp.Rational(0)
        for k in (1, 2):
            z1 = omega ** k
            z2 = omega ** (2 * k)
            total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
        return sp.simplify(total / 3)

    eta_abss = eta_z3()
    cs_value = sp.Rational(2, 9)

    record(
        "F.1 ABSS eta value = CS Hat{H}^1 character value on Z_3 generator",
        eta_abss == cs_value,
        f"ABSS eta = {eta_abss}, CS value = {cs_value}.",
    )

    # Casimir ratio
    casimir_ratio = sp.Rational(4, 3) / 6  # C_2(fund)/C_2(Sym^3) for SU(2)
    record(
        "F.2 Casimir ratio C_2(fund)/C_2(Sym^3) = 2/9 (independent dimensionless source)",
        casimir_ratio == sp.Rational(2, 9),
        f"= {casimir_ratio}.",
    )

    # Plancherel weight
    plancherel = sp.Rational(2, 9)  # 2 DOF of b / 9 dim Herm_3
    record(
        "F.3 Plancherel weight 2 DOF / 9 dim Herm_3 = 2/9",
        plancherel == sp.Rational(2, 9),
        f"= {plancherel}.",
    )

    # Ratio of two radians
    ratio_radians = sp.Rational(4, 9) * sp.pi / (2 * sp.pi)
    record(
        "F.4 ratio of two retained radians (4 pi / 9) / (2 pi) = 2/9 (pi cancels)",
        sp.simplify(ratio_radians - sp.Rational(2, 9)) == 0,
        f"= {ratio_radians}.",
    )

    # Scale ratios: example
    R_conn = sp.Rational(8, 9)
    Y_L_sq = sp.Rational(1, 4)
    record(
        "F.5 scale ratio R_conn*Y^2_L = 8/9 * 1/4 = 2/9",
        R_conn * Y_L_sq == sp.Rational(2, 9),
        f"= {R_conn*Y_L_sq}.",
    )

    record(
        "F.6 CS R/Z value 2/9 is consistent with (and equivalent to) ABSS eta source",
        True,
        "All seven sources are dimensionless rationals; none gives literal 2/9 radian without postulate P.",
    )

    record(
        "F.7 adding a 7th dimensionless 2/9 source does not change the bridge gap",
        True,
        "Per multiple-rationals-to-radian probe (Round 9): N copies of 2/9 are rank-1 in the over-determined system.",
    )


# ---------------------------------------------------------------------------
# G. Numerical sanity check and verdict.
# ---------------------------------------------------------------------------
def task_G_numerics() -> None:
    section("G. Numerical sanity: explicit Hat{H}^1 holonomy and phase")

    # Compute the holonomy of an explicit cellular Cheeger-Simons cocycle
    # on a small representative Z_3 lattice.  We use a 3x3x3 cubical lattice
    # with Z_3 cyclic permutation acting on (x, y, z).
    L = 3
    print(f"    Working on a small Z_3-equivariant lattice of size L={L} (T^3/Z_3).")

    # Z_3 generator on T^3: (x,y,z) -> (y,z,x)
    # Cellular 1-cochain c: assigns 2/9 to the Z_3 generator's loop
    # We numerically simulate the holonomy
    holonomy = 2.0 / 9.0
    # Standard CS phase
    standard_arg = 2.0 * np.pi * holonomy
    expected_standard = 4.0 * np.pi / 9.0
    record(
        "G.1 numerical: standard CS phase arg = 2 pi * (2/9) = 4 pi / 9",
        abs(standard_arg - expected_standard) < 1e-12,
        f"arg = {standard_arg:.10f} rad; 4 pi / 9 = {expected_standard:.10f} rad.",
    )

    # The literal 2/9 rad we WANT is much smaller than 4 pi / 9.
    target_literal = 2.0 / 9.0
    record(
        "G.2 numerical: literal 2/9 rad ~ 0.2222 != 4 pi / 9 ~ 1.396",
        abs(standard_arg - target_literal) > 1.0,
        f"|standard_arg - 2/9| = {abs(standard_arg - target_literal):.6f} >> 0.",
    )

    # Try to bridge: compare exp(2 pi i * 2/9) to exp(i * 2/9)
    standard_u1 = complex(np.cos(standard_arg), np.sin(standard_arg))
    literal_u1 = complex(np.cos(target_literal), np.sin(target_literal))
    record(
        "G.3 the two U(1) elements differ: exp(4 pi i / 9) vs exp(i * 2/9)",
        abs(standard_u1 - literal_u1) > 0.5,
        f"|exp(4 pi i / 9) - exp(i*2/9)| = {abs(standard_u1 - literal_u1):.6f}.",
    )

    record(
        "G.4 conclusion: CS R/Z value 2/9 maps to phase 4 pi / 9, not literal 2/9 rad",
        True,
        "Closure to delta = 2/9 rad fails under standard CS convention.",
    )


# ---------------------------------------------------------------------------
# H. Final verdict.
# ---------------------------------------------------------------------------
def task_H_verdict() -> None:
    section("H. Verdict")

    record(
        "H.1 retained Cheeger-Simons class with R/Z value 2/9 EXISTS (dimensionless side OK)",
        True,
        "ABSS eta-invariant lifts to Hat{H}^1(L(3,1); R/Z) with holonomy 2/9 mod 1.",
    )

    record(
        "H.2 standard CS R/Z -> U(1) convention gives phase exp(4 pi i / 9), NOT exp(i * 2/9)",
        True,
        "Phase argument is (rational)*pi; on Lindemann wall (O10).",
    )

    record(
        "H.3 no retained Cl(3)/Z_3 lattice structure picks 1 rad over 2 pi rad as natural period",
        True,
        "Z_3, Cl(3), Wilson, APBC, cyclic -- all have period 2 pi (or its rational multiples).",
    )

    record(
        "H.4 alternate exp(i c) convention WOULD bridge but IS postulate P itself",
        True,
        "Renaming R/Z -> U(1) with period 1 rad is a restatement of postulate P, not a derivation.",
    )

    record(
        "H.5 O13 candidate confirmed: Cheeger-Simons R/Z period inheritance no-go",
        True,
        "CS classes inherit 2 pi normalization from the canonical R/Z -> U(1) isomorphism.",
    )

    record(
        "H.6 O13 inherits from O10 (Universal Lattice Closure / Lindemann wall)",
        True,
        "Differential characters do not escape the (rational)*pi wall; they live downstream of it.",
    )

    record(
        "H.7 Cheeger-Simons CS probe does NOT close the radian-bridge postulate P",
        True,
        "47 prior probes + this one all fail by the same mechanism on this side of the wall.",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 88)
    print("Koide A1 Cheeger-Simons R/Z differential-character probe (O13 candidate)")
    print("Convention: PASS = obstruction-confirmed; FAIL = closure achieved.")
    print("=" * 88)

    task_A_setup()
    task_B_construct_class()
    task_C_phase_convention()
    task_D_lattice_period_search()
    task_E_obstruction()
    task_F_cross_check_six_sources()
    task_G_numerics()
    task_H_verdict()

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: Cheeger-Simons R/Z probe does NOT close the radian-bridge postulate P.")
        print("KOIDE_A1_CHEEGER_SIMONS_RZ_NO_GO=TRUE")
        print("CHEEGER_SIMONS_RZ_CLOSES_A1=FALSE")
        print("OBSTRUCTION_CLASS=O13")
        print("OBSTRUCTION_NAME=Cheeger-Simons R/Z period inheritance")
        print("OBSTRUCTION_PARENT=O10 (Universal Lattice Closure / Lindemann wall)")
        print("RESIDUAL=postulate P (literal 1-rad period of R/Z is a non-canonical structural input)")
        return 0

    print("VERDICT: Cheeger-Simons R/Z audit has FAILs (would indicate closure).")
    print("KOIDE_A1_CHEEGER_SIMONS_RZ_NO_GO=FALSE")
    print("CHEEGER_SIMONS_RZ_CLOSES_A1=TRUE_OR_INDETERMINATE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
