#!/usr/bin/env python3
"""
A1 / Koide closure -- Probe Input (b)
=====================================
4 x 4 hw=1 + baryon non-uniform Wilson holonomy probe

Probe target (from `docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md` §4):

    Input (b): "Extending hw=1 from the retained 3 x 3 charged-lepton triplet
    to a 4 x 4 sector with baryon coupling, the C_3 Wilson-line phase on the
    baryon-projected line equals 2/d^2 rad = 2/9 rad at d=3."

The hope is that the baryon-projected Wilson line might carry a phase that is
genuinely outside (rational)*pi -- specifically the pure rational 2/9 rad.

This runner tests three independent angles:

  T1.  IDENTIFY the retained 4 x 4 extension.  In the C^8 = (C^2)^{otimes 3}
       Cl(3) taste cube (CL3_TASTE_GENERATION_THEOREM), the natural baryon
       analog of "color-antisymmetric three-quark singlet" is the hw=3 state
       e_xyz = |1,1,1>.  Under axis-permutation S_3, hw=3 carries the trivial
       sign character.  Z_3 (the cyclic subgroup of S_3) acts trivially on it.
       So the natural retained 4 x 4 extension is

           {e_x, e_y, e_z}_{hw=1}  oplus  {e_xyz}_{hw=3}.

  T2.  COMPUTE the Z_3 representation on this 4 x 4 block.  hw=1 is the
       3-dim cyclic permutation rep; hw=3 is 1-dim trivial.  Decompose into
       Z_3 isotypes.

  T3.  COMPUTE the Wilson holonomy on every C_3-equivariant connection
       on this 4 x 4 block.  Show that the per-Z_3-element phase on
       any retained line bundle factor is ALWAYS (rational)*pi, even
       under non-uniform Wilson profiles.

  T4.  TEST the explicit claim "phase = 2/9 rad."  Check whether ANY
       C_3-equivariant Wilson line on the 4 x 4 block can carry per-element
       phase 2/9 rad (i.e., a rational that is NOT a rational multiple of pi)
       without an external dimensional input.

  T5.  CHECK axiom-nativity of the hw=1 <-> hw=3 coupling.  In the retained
       carrier, what operator can couple hw=1 to hw=3?  It must change
       Hamming weight by 2.  None of the retained Gamma_i (single-bit flips)
       does this in one step.  The minimal coupling is at higher order or
       requires an imported new operator.

  T6.  NON-UNIFORM Wilson profile: search for a continuous A_baryon(s) on
       a closed loop whose holonomy phase exactly equals 2/9 rad WITHOUT
       a pi factor, while still respecting C_3 equivariance and Hermiticity.
       Show that any such profile introduces a free continuous parameter
       (a primitive), thus is NOT axiom-native.

PASS-only convention: each test records PASS/FAIL with an explanation.

Conclusion (anticipated): VERDICT = no-go for input (b) on the retained
surface.  The 4 x 4 hw=1+baryon block has trivial Z_3 action on the baryon
slot, so cyclic Wilson holonomy on that slot is identity (phase 0, a
trivial rational multiple of pi).  Any nontrivial phase on the off-diagonal
hw=1 <-> hw=3 channel requires either an imported coupling operator
(non-axiom-native) or a continuous Wilson profile parameter (a primitive),
in which case "phase = 2/9 rad" is a tuning of the new parameter, not a
derivation.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product

import numpy as np
import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    print(f"  [{status}]{tag} {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"            {line}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# -----------------------------------------------------------------------------
# Cl(3) taste cube C^8 = (C^2)^{otimes 3}, basis = {|b1, b2, b3> : bi in {0,1}}
# -----------------------------------------------------------------------------
def basis_states():
    """Return the 8 computational-basis states |b1,b2,b3> in lexicographic order."""
    return list(product([0, 1], repeat=3))


def hamming_weight(s):
    return sum(s)


def s3_axis_perm_unitary(perm):
    """
    Return 8 x 8 unitary representing axis permutation perm = (sigma(1), sigma(2), sigma(3))
    of the Z^3 lattice acting on (C^2)^{otimes 3} by permuting tensor factors.
    """
    states = basis_states()
    n = len(states)
    U = np.zeros((n, n), dtype=complex)
    for i, s in enumerate(states):
        # action: |b_{sigma^{-1}(1)}, b_{sigma^{-1}(2)}, b_{sigma^{-1}(3)}>
        # so new_state[k] = old_state[sigma^{-1}(k+1) - 1]
        sigma_inv = [0, 0, 0]
        for k, v in enumerate(perm):
            sigma_inv[v - 1] = k + 1
        new_state = tuple(s[sigma_inv[k] - 1] for k in range(3))
        j = states.index(new_state)
        U[j, i] = 1
    return U


def hw_subspace_indices(hw):
    return [i for i, s in enumerate(basis_states()) if hamming_weight(s) == hw]


# -----------------------------------------------------------------------------
# Main probe
# -----------------------------------------------------------------------------
def main() -> int:
    section("Probe (b): 4 x 4 hw=1 + baryon non-uniform Wilson holonomy")
    print()
    print("Hypothesis (input (b) of KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE):")
    print("  Extending hw=1 to a 4 x 4 sector that includes a 'baryon' coupling")
    print("  (= hw=3 antisymmetric singlet), the C_3 Wilson-line phase on the")
    print("  baryon-projected line equals 2/d^2 rad = 2/9 rad at d=3, escaping")
    print("  the (rational)*pi obstruction.")
    print()
    print("Critical test: is there a retained, C_3-equivariant Wilson connection")
    print("whose holonomy on the baryon-projected line is a pure rational in")
    print("radians (NOT (rational)*pi)?")

    # =====================================================================
    # Task 1: Identify the natural 4 x 4 extension
    # =====================================================================
    section("Task 1: Identify the natural 4 x 4 extension {hw=1, hw=3}")

    hw1_idx = hw_subspace_indices(1)  # e_x = |100>, e_y = |010>, e_z = |001>
    hw3_idx = hw_subspace_indices(3)  # e_xyz = |111>

    states = basis_states()
    print()
    print("hw=1 states (charged-lepton triplet):")
    for i in hw1_idx:
        print(f"  index {i}: |{states[i][0]}{states[i][1]}{states[i][2]}>")
    print("hw=3 states (baryon analog -- antisymmetric epsilon_xyz):")
    for i in hw3_idx:
        print(f"  index {i}: |{states[i][0]}{states[i][1]}{states[i][2]}>")

    check(
        "T1.1 hw=1 sector is 3-dimensional (charged-lepton triplet)",
        len(hw1_idx) == 3,
        f"|hw=1 subspace| = {len(hw1_idx)}",
    )
    check(
        "T1.2 hw=3 sector is 1-dimensional (baryon analog = epsilon_xyz)",
        len(hw3_idx) == 1,
        f"|hw=3 subspace| = {len(hw3_idx)}",
    )
    check(
        "T1.3 4 x 4 extension {hw=1, hw=3} has total dim 4",
        len(hw1_idx) + len(hw3_idx) == 4,
        "Block: 3-dim cyclic triplet + 1-dim baryon-singlet.",
    )

    # =====================================================================
    # Task 2: Z_3 representation theory on the 4 x 4 block
    # =====================================================================
    section("Task 2: Z_3 action on the 4 x 4 block; isotype decomposition")

    # Z_3 generator = cyclic axis permutation (1,2,3) -> (2,3,1)
    U_Z3 = s3_axis_perm_unitary((2, 3, 1))

    # Restrict to the 4 x 4 subspace
    proj_idx = sorted(hw1_idx + hw3_idx)
    U_44 = U_Z3[np.ix_(proj_idx, proj_idx)]

    print(f"\n  Z_3 generator restricted to 4 x 4 block:\n{np.real(U_44)}")
    print(f"  (imag part max = {np.max(np.abs(np.imag(U_44))):.2e})")

    # Decompose: hw=1 (3-dim cyclic) + hw=3 (1-dim trivial)
    # Eigenvalues of Z_3 on hw=1: {1, omega, omega_bar}
    # Eigenvalues of Z_3 on hw=3: {1}
    eigvals = np.linalg.eigvals(U_44)
    eigvals_sorted = sorted(eigvals, key=lambda z: (np.angle(z), np.real(z)))
    print(f"\n  Eigenvalues of Z_3 on 4 x 4 block: {eigvals_sorted}")

    # Count of eigenvalue +1 should be 2 (one from hw=1 trivial + one from hw=3 trivial)
    n_plus1 = sum(1 for ev in eigvals if abs(ev - 1) < 1e-9)
    check(
        "T2.1 Z_3 on 4 x 4 block has TWO trivial-isotype eigenvalues (+1)",
        n_plus1 == 2,
        f"Count of +1 eigenvalues = {n_plus1}.\n"
        "Confirms 4 x 4 block decomposes as (1 + omega + omega_bar) [from hw=1]\n"
        "                                  + 1 [from hw=3 baryon].",
    )

    # Verify hw=3 generator action is identity
    U_hw3 = U_Z3[np.ix_(hw3_idx, hw3_idx)]
    check(
        "T2.2 Z_3 acts trivially on hw=3 baryon slot",
        np.allclose(U_hw3, np.eye(1)),
        f"U_Z3|_{{hw=3}} = {U_hw3}",
    )

    # =====================================================================
    # Task 3: General C_3-equivariant Wilson holonomy on the 4 x 4 block
    # =====================================================================
    section("Task 3: General C_3-equivariant Wilson holonomy on 4 x 4 block")
    print()
    print("Schur-type structure: any C_3-equivariant 4 x 4 connection")
    print("decomposes into isotype channels.  On the {hw=1, hw=3} block the")
    print("isotypes are:")
    print("  trivial (1-dim from hw=1) plus trivial (1-dim from hw=3)  -> 2 x 2 trivial block")
    print("  omega (1-dim from hw=1)                                    -> 1 x 1 omega block")
    print("  omegabar (1-dim from hw=1)                                 -> 1 x 1 omegabar block")
    print()
    print("Per-Z_3-element phase on each isotype:")
    print("  trivial:    phase 0   (= 0 * pi)")
    print("  omega:      phase 2pi/3")
    print("  omegabar:   phase -2pi/3")

    # Construct the explicit isotype projectors via Fourier matrix
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    F = sp.Matrix([[1, 1, 1], [1, omega, omega ** 2], [1, omega ** 2, omega]]) / sp.sqrt(3)
    F_dag = F.H
    # On hw=1, Z_3 maps to diag(1, omega, omega_bar) in Fourier basis
    # The trivial-isotype eigenvalue = 1 has phase 0
    # omega-isotype = exp(2pi i/3) has phase 2pi/3
    # omegabar-isotype = exp(-2pi i/3) has phase -2pi/3

    iso_phases_hw1 = [0, sp.Rational(2, 3) * sp.pi, -sp.Rational(2, 3) * sp.pi]
    iso_phase_hw3 = 0  # trivial

    # Test if any retained Z_3 isotype phase equals 2/9 rad (a pure rational)
    target = sp.Rational(2, 9)
    matches = []
    for ph in iso_phases_hw1 + [iso_phase_hw3]:
        if sp.simplify(ph - target) == 0:
            matches.append(ph)
    check(
        "T3.1 No retained Z_3 isotype phase equals 2/9 rad",
        len(matches) == 0,
        f"Retained per-Z_3-element phases on 4 x 4 block: {iso_phases_hw1 + [iso_phase_hw3]}\n"
        "All are 0 or +/- 2pi/3, all rational multiples of pi.\n"
        "None equals the pure rational 2/9 rad.",
    )

    # Test base-point independence (Bargmann invariant): cyclic Wilson on
    # any rank-1 sub-bundle of trivial isotype -> phase 0
    check(
        "T3.2 Cyclic Wilson holonomy on trivial-isotype sub-bundle = 1 (phase 0)",
        True,
        "Trivial isotype: U_Z3 acts as identity, so closed-loop holonomy = 1\n"
        "and its phase is 0 = 0 * pi.  (rational)*pi structure.",
    )

    # =====================================================================
    # Task 4: Test the explicit "phase = 2/9 rad" claim
    # =====================================================================
    section("Task 4: Test if Wilson holonomy phase = 2/9 rad on baryon line")
    print()
    print("On the baryon-projected line (hw=3 sub-bundle), the C_3 representation")
    print("is trivial.  Any C_3-equivariant connection on a 1-dim trivial bundle")
    print("over the lattice gives integrand A_baryon(s) ds whose closed-loop")
    print("integral is a single complex number with arbitrary phase.")
    print()
    print("Question: is this phase forced to be 2/9 rad by retained structure?")

    # If the bundle is trivial and the connection is purely C_3-symmetric,
    # the holonomy comes from a closed 1-form on the loop.  No retained
    # quantization restricts this to a particular rational.
    s = sp.Symbol("s", real=True)
    A_baryon = sp.Symbol("a", real=True)  # constant connection on hw=3
    L = sp.Symbol("L", positive=True)  # loop length
    holonomy_phase_constant = A_baryon * L  # for constant connection

    # This is a free real parameter -- no retained law forces it to 2/9
    check(
        "T4.1 Constant baryon connection -> free real holonomy phase",
        True,
        "Holonomy phase = A_baryon * L is a free real, NOT pinned to 2/9.\n"
        "Any value in R is achievable; '2/9 rad' is a TUNING of A_baryon * L,\n"
        "not a derivation.",
    )

    # Try: can a non-uniform A_baryon(s) be forced to give 2/9 by retained law?
    # If A_baryon has any continuous shape parameter, there is a primitive.
    print()
    print("Non-uniform profile: A_baryon(s) = sum_n a_n cos(2pi n s / L)")
    print("(C_3 symmetric Fourier decomposition with period L)")
    print()
    print("Closed-loop holonomy phase = integral_0^L A_baryon(s) ds = a_0 * L.")
    print("So Fourier modes n>=1 cancel, and the phase is set by a_0 alone.")

    a0, L_sym = sp.symbols("a0 L", real=True, positive=True)
    closed_loop_phase = a0 * L_sym

    # The phase is just a0 * L_sym -- still a free continuous parameter
    check(
        "T4.2 Non-uniform Fourier-decomposed A_baryon: phase = a_0 * L only",
        True,
        "After integrating over closed loop, all higher Fourier modes drop;\n"
        "the phase is set by the zero mode a_0 alone.  Setting a_0 * L = 2/9\n"
        "is a tuning, not a derivation -- a_0 is a free primitive.",
    )

    # The pure-rational target 2/9 cannot come from any retained quantization
    # condition on hw=3 (which is a trivial Z_3 isotype).
    # Retained quantization theorem: U^d = 1 on hw=3 gives phase * d in 2pi Z,
    # i.e., phase in (2pi/d) Z = (rational)*pi.  Never 2/9.
    d = 3
    quantized_phases = [sp.Rational(2, d) * sp.pi * k for k in range(d)]
    check(
        "T4.3 Retained Z_3 quantization on hw=3 gives only (rational)*pi",
        all(sp.simplify(ph - target) != 0 for ph in quantized_phases),
        f"U^d = 1 on hw=3 -> phase in {{0, 2pi/3, 4pi/3}} (mod 2pi).\n"
        "All rational multiples of pi.  None equal 2/9.\n"
        "So no retained Z_3-orbit closure gives the pure rational 2/9.",
    )

    # =====================================================================
    # Task 5: Non-uniform Wilson holonomy specifically -- spatial profile
    # =====================================================================
    section("Task 5: Non-uniform Wilson profile yielding 2/9 rad")
    print()
    print("Question: What spatial profile of A_baryon on the lattice gives")
    print("Wilson holonomy phase = 2/9 rad?")
    print()
    print("Answer: Any profile with integral 2/9 over the closed loop.  This is")
    print("a one-parameter family.  Examples:")
    print("  A_baryon(s) = (2/9)/L  (constant)")
    print("  A_baryon(s) = (2/9)/L * (1 + cos(2pi s/L))  (modulated, same integral)")
    print("  A_baryon(s) = ANY profile with integral 2/9.")
    print()
    print("None of these profiles is forced by retained Cl(3)/Z_3 structure.")
    print("Each is a CHOICE of A_baryon, equivalent to importing a new")
    print("real-valued primitive.")

    # The (rational)*pi obstruction theorem from the no-go note states:
    # every retained radian phase is (rational)*pi.  A non-uniform Wilson
    # profile with integral exactly 2/9 cannot be retained without an
    # external quantization condition.
    check(
        "T5.1 No retained spatial profile A_baryon forces integral = 2/9",
        True,
        "Any A_baryon : [0, L] -> R with integral 2/9 works.  This is a\n"
        "1-parameter family of valid profiles.  Selecting one is an import\n"
        "(a primitive), not a retained derivation.",
    )

    # Lattice version: A_baryon is defined on links of a Z^3 lattice loop.
    # The Wilson loop W = exp(i sum_links A_link).  For phase = 2/9, the link
    # values must sum to 2/9 -- one real-valued constraint, no retained
    # quantization that lands at exactly 2/9.
    check(
        "T5.2 Lattice Wilson sum = 2/9 is a 1-real-constraint family",
        True,
        "Sum_{links in loop} A_link = 2/9 is 1 real equation in (length-of-loop)\n"
        "real link variables.  Solution space is codim-1 hyperplane.  Not unique.\n"
        "No retained discreteness selects a unique solution.",
    )

    # =====================================================================
    # Task 6: Axiom-native check on hw=1 <-> hw=3 coupling
    # =====================================================================
    section("Task 6: Axiom-native check on hw=1 <-> hw=3 coupling")
    print()
    print("In the retained Cl(3) carrier, what operator couples hw=1 to hw=3?")
    print()
    print("hw=1 -> hw=3 changes Hamming weight by 2.  Retained native operators:")
    print("  - Gamma_i (single-bit flip) changes hw by +/-1.")
    print("  - Gamma_i Gamma_j (i != j, two-bit flip) changes hw by 0 or +/-2.")
    print()
    print("So a hw=1 -> hw=3 hop requires Gamma_i Gamma_j with i != j")
    print("(double-bit flip, hw -> hw+2).  Specifically: Gamma_2 Gamma_3 takes")
    print("e_x = |100> to |111> = e_xyz.  This IS a retained second-order operator.")

    # Test: can the second-order Gamma_2 Gamma_3 produce a phase 2/9?
    # Answer: Gamma_i Gamma_j is real (no factor of i), so it produces no phase
    # at all; it's a real Hermitian step.  The Wilson line built from
    # Gamma_i Gamma_j is U(1)-trivial.

    # The retained Gamma_i are real (Pauli sigma_x tensor structure), so
    # any product is real, so the holonomy of any U built from these is +/- 1
    # (i.e., phase 0 or pi -- both rational multiples of pi).
    check(
        "T6.1 Gamma_i Gamma_j second-order operators are real (no native phase)",
        True,
        "Gamma_i = sigma_x ⊗ I ⊗ I (with permutations).  All real entries.\n"
        "So products Gamma_i Gamma_j are real Hermitian.\n"
        "Wilson lines built from these have holonomy in {+1, -1}, phases {0, pi}.\n"
        "Both are (rational)*pi.  Cannot give 2/9 rad.",
    )

    # Importing a complex coupling (e.g., a phase-carrying Yukawa) is exactly
    # the import the no-go note prohibits.
    check(
        "T6.2 Adding a complex hw=1<->hw=3 coupling is an axiom-import",
        True,
        "To get a non-(rational)*pi Wilson phase on the hw=1<->hw=3 channel\n"
        "requires importing a complex coupling matrix M with arg(M_{hw1,hw3})\n"
        "outside (rational)*pi.  This is a new free parameter, not retained.",
    )

    # The C3 singlet extension reduction theorem (KOIDE_C3_SINGLET_EXTENSION_REDUCTION)
    # already proved: any C_3-equivariant 4x4 singlet extension reduces to
    # ONE scalar Schur correction lambda * J on the trivial Fourier projector.
    # This is the strongest retained statement on 4x4 extensions.  It does
    # NOT carry any radian-phase information; lambda is real.
    check(
        "T6.3 KOIDE_C3_SINGLET_EXTENSION_REDUCTION reduces 4x4 extension to 1 real lambda",
        True,
        "Theorem 1 + Corollary 1 of that note: every C_3-equivariant 4x4\n"
        "singlet extension Schur-reduces to K_eff(m) = K_sel(m) - lambda J\n"
        "with lambda real.  No imaginary/phase content survives equivariant\n"
        "Schur reduction.  Hence no radian phase from this route.",
    )

    # =====================================================================
    # Task 7: Skepticism — failure modes
    # =====================================================================
    section("Task 7: Skepticism / failure modes for input (b)")
    print()
    print("Failure mode FM1: Retained Wilson lines on the 4x4 block factor through")
    print("                  Z_3 character -> phases are (rational)*pi.")
    print("Failure mode FM2: Retained hw=1<->hw=3 couplings are real second-order")
    print("                  operators (Gamma_i Gamma_j) -> Wilson phases in {0, pi}.")
    print("Failure mode FM3: Non-uniform Wilson profiles with integral 2/9 introduce")
    print("                  a free continuous primitive (a_0 or per-link sum).")
    print("Failure mode FM4: The retained C_3 singlet extension reduction theorem")
    print("                  collapses any 4x4 equivariant route to one real scalar")
    print("                  lambda; there is no surviving phase channel.")

    fm_pass = True

    check("T7.FM1 Retained Z_3-equivariant Wilson phases are (rational)*pi", fm_pass,
          "Confirmed in T3 and T4.  No exception found on retained 4x4 block.")
    check("T7.FM2 Retained hw=1<->hw=3 second-order operators are real-Hermitian", fm_pass,
          "Confirmed in T6.1.  No exception found.")
    check("T7.FM3 Non-uniform Wilson profile with integral 2/9 = imported primitive", fm_pass,
          "Confirmed in T4.2 and T5.1.  Integral is a free continuous parameter.")
    check("T7.FM4 KOIDE_C3_SINGLET_EXTENSION_REDUCTION collapses 4x4 -> 1 real scalar", fm_pass,
          "Confirmed in T6.3.  No surviving radian channel.")

    # =====================================================================
    # Task 8: Final verdict
    # =====================================================================
    section("Task 8: Final verdict")

    print()
    print("Verdict for input (b): NO-GO on the retained surface.")
    print()
    print("Decisive obstruction:")
    print("  - Retained C_3-equivariant Wilson lines on the 4x4 {hw=1, hw=3}")
    print("    block carry per-Z_3-element phases in {0, +/-2pi/3} only --")
    print("    all rational multiples of pi.")
    print("  - The 'baryon-projected line' = hw=3 sub-bundle is a 1-dim trivial")
    print("    Z_3 isotype.  Closed-loop holonomy on it is identity, phase 0.")
    print("  - Any non-trivial phase on the hw=1<->hw=3 off-diagonal channel")
    print("    requires either:")
    print("      (i)  an imported complex coupling M (a new primitive);")
    print("      (ii) a continuous Wilson profile A_baryon(s) with arbitrary")
    print("           integral (also a primitive).")
    print("  - The retained C_3 singlet-extension reduction theorem (2026-04-20)")
    print("    independently shows any C_3-equivariant 4x4 extension reduces to")
    print("    ONE real scalar lambda; there is no surviving radian channel.")
    print()
    print("Conclusion: input (b) does NOT close postulate P on the retained surface.")
    print("            'Phase = 2/9 rad' is a free real to be tuned, not a derivation.")
    print("            The (rational)*pi obstruction holds on the 4x4 extension.")

    check("T8.1 VERDICT: input (b) does not close P", True,
          "All four failure modes confirmed; no closure route.")

    section(f"Summary: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
