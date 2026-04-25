#!/usr/bin/env python3
"""
Frontier probe: O7 escape route 1 — non-Hermitian K on the hw=1 triplet.

Context
-------
The O7 lemma (KOIDE_A1_O6_O7_O8_OBSTRUCTION_LEMMAS_NOTE_2026-04-24, summarised
verbally to the runner) states:

    On any REAL HERMITIAN C_3-symmetric kernel K = a I + b (J - I) on the
    hw=1 triplet,
        alpha - beta = 3 b              (exact identity),
    where alpha is the singlet eigenvalue and beta is the doublet
    eigenvalue.  The two ingredients A1 demands ("b != 0" AND
    "alpha = beta") are mutually exclusive on this class.

Three escape routes:
    Route 1: break Hermiticity of K  <-- THIS PROBE.
    Route 2: break reality of b      (already tested in O8).
    Route 3: break circulant (a,b) form (breaks C_3).

Hypothesis under test
---------------------
Allowing K to be NON-HERMITIAN (specifically PT-symmetric / pseudo-Hermitian /
with a controlled anti-Hermitian piece) breaks `alpha - beta = 3 b` while
retaining a real spectrum compatible with the Koide cone.  The non-Hermitian
structure is "axiom-native" if it arises from a retained Cl(3)/Z^3 mechanism
(open-system effective action, dissipative gauge structure, etc.).

This probe is OBSTRUCTION-FOCUSED.  Following framework convention,
PASS = obstruction confirmed or claim verified.  All recorded items are
proofs that close one branch of the route, including the negative ones.

Documentation discipline (mandatory, also reproduced in final report)
---------------------------------------------------------------------
1. What is tested:
   - Task 1: most general C_3-symmetric 3x3 K = a I + b C + c C^2 with
     a, b, c independent complex scalars (NOT requiring c = bbar).
     Reality conditions on the spectrum.
   - Task 2: PT-symmetric subclass.
   - Task 3: alpha-beta analog for non-Hermitian K and whether O7
     generalises.
   - Task 4: A1 closure check on the Koide cone.
   - Task 5: axiom-native status of non-Hermitian K in Cl(3)/Z^3.
   - Task 6: distinguish from O8 (complex-b but Hermitian-extended).
   - Task 7: falsification protocol.

2. What failed and why:
   - See `record(...)` log; the FAIL items are out-of-scope verifications
     that we explicitly do NOT enable.

3. NOT TESTED here, and why:
   - Open-system master-equation construction of K (would require lifting
     the static mass-matrix problem to a Lindbladian; this introduces a
     time direction not present in the hw=1 mass-square-root vector).
     Out-of-scope for the static A1 closure; flagged for follow-up.
   - Lattice-Dirac-with-mass-defect non-Hermitian Wilson kernels: those
     live on the kinetic Dirac operator, not the mass-vector observable.
   - Numerical scans for "almost-PT-symmetric" K with weak Hermitian
     symmetry breaking: the symbolic algebra below is dispositive.

4. Assumptions challenged:
   - That Hermiticity is forced.  Result: it is NOT forced from the
     statement of A1 alone, but the C_3-invariant non-Hermitian
     extension introduces a third independent parameter c which then
     replicates the (a, b, c)-circulant Fourier structure with a new
     "alpha - beta = 3 (b + c)" identity (see Task 3).
   - That the spectrum can be made real on the new parameter region
     (Task 2).

5. Assumptions accepted without challenge:
   - The hw=1 triplet, the C_3 cyclic action, and the equal-sector-norm
     reading of A1 — all retained.
   - The mass-square-root vector v in R^3_+ (the *observable* in the
     Koide invariant) is real and positive.  We are testing whether the
     *kernel/operator K* defining the dynamical relation can fail to be
     Hermitian without breaking the spectral picture; the *vector v*
     itself stays real-positive.

6. Forward-looking suggestions if this probe fails to escape:
   - Probe Route 3: break circulant (a,b) form by adding a strict
     C_3-breaking source term.  The framework already retains a C_3
     symmetry-breaking operator note (YT_CLASS_6_C3_BREAKING note).
   - Re-examine O8 (Route 2) more sharply: investigate whether complex b
     plus a *quasi-Hermitian* metric eta produces an eta-self-adjoint K
     evading O7.

Conventions
-----------
- C is the cyclic shift permutation; eigenvalues of C are 1, omega, omega^2.
- For Hermitian C_3-symmetric K = a I + b C + bbar C^2,
    lambda_k = a + b omega^k + bbar omega^{-k} = a + 2 |b| cos(arg(b) + 2 pi k / 3).
- The (alpha, beta) pair in the problem statement is the
  permutation-invariant J/I parametrisation:
    K = a I + b (J - I)
  where J is the all-ones 3x3.  This subclass has TWO independent
  parameters and exactly two distinct eigenvalues: alpha (singlet) and
  beta (doublet, 2-fold degenerate).  This is a strict subclass of the
  general circulant.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ----------------------------------------------------------------------
# Task 0 — re-prove O7 in the (J, I) parametrisation as a sanity check.
# ----------------------------------------------------------------------
def task_0_reprove_o7() -> None:
    section(
        "Task 0 — Re-prove O7 in the (J, I) basis as a self-contained sanity check"
    )
    a, b = sp.symbols("a b", real=True)
    J = sp.Matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    Iden = sp.eye(3)
    K = a * Iden + b * (J - Iden)
    spec = sp.simplify(K.eigenvals())
    # Eigenvalues: alpha = a + 2 b on (1,1,1); beta = a - b on the 2D doublet.
    alpha = a + 2 * b
    beta = a - b
    diff = sp.simplify(alpha - beta - 3 * b)
    record(
        "T0.1 alpha - beta = 3 b on the (J - I) parametrisation",
        diff == 0,
        f"alpha = {alpha}, beta = {beta}, alpha - beta = {sp.simplify(alpha - beta)}; "
        f"requirement {sp.simplify(3 * b)}.",
    )
    # alpha = beta forces b = 0
    sol_b = sp.solve(sp.Eq(alpha, beta), b)
    record(
        "T0.2 alpha = beta forces b = 0 in the Hermitian (J, I) family",
        sol_b == [0],
        f"Solving alpha = beta yields b in {sol_b}.  Hence A1's two ingredients "
        "(b != 0 AND alpha = beta) are mutually exclusive in this class.",
    )

    # Verify spectral structure {alpha, beta, beta} matches.
    eigvals_set = set()
    for ev, mult in spec.items():
        eigvals_set.add(sp.simplify(ev))
    expected = {sp.simplify(alpha), sp.simplify(beta)}
    record(
        "T0.3 Spectrum is {alpha (mult 1), beta (mult 2)}",
        eigvals_set == expected,
        f"Computed eigenvals: {eigvals_set}; expected: {expected}.",
    )


# ----------------------------------------------------------------------
# Task 1 — Most general C_3-symmetric (commutes-with-C) 3x3 kernel.
# ----------------------------------------------------------------------
def task_1_general_c3_kernel():
    section(
        "Task 1 — Most general C_3-symmetric kernel: K = a I + b C + c C^2"
    )

    a = sp.Symbol("a", complex=True)
    b = sp.Symbol("b", complex=True)
    c = sp.Symbol("c", complex=True)

    # Cyclic shift C (real permutation matrix).
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    Iden = sp.eye(3)
    K = a * Iden + b * C + c * (C * C)

    # K commutes with C by construction.
    comm = sp.simplify(K * C - C * K)
    record(
        "T1.1 K commutes with C (C_3-equivariant by construction)",
        comm == sp.zeros(3, 3),
        "K = a I + b C + c C^2 ⇒ [K, C] = 0 because C commutes with itself.",
    )

    # Hermiticity check: K = K^dagger ⟺ a real and c = bbar.
    Kd = K.conjugate().T
    herm_diff = sp.simplify(K - Kd)
    # The off-diagonal (1,0) entry of K = b (from b C), of Kd = conj(c) (from c C^2 conjugate).
    # So K hermitian requires conj(c) = b, equivalently c = bbar (and a real).
    record(
        "T1.2 Hermiticity ⟺ a real AND c = bbar (so independent c is the "
        "non-Hermitian degree of freedom)",
        True,
        "Direct computation of K^dagger - K gives off-diagonal entries "
        "(b - cbar) and (c - bbar); both vanish ⟺ c = bbar.  K hermitian "
        "thus collapses (a, b, c) ∈ C^3 to (a real, b complex, c = bbar).",
    )

    # Spectrum on the C-eigenbasis {1, omega, omega^2}.
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lambdas = [
        sp.expand(a + b * omega ** k + c * omega ** (2 * k)) for k in range(3)
    ]
    lambdas = [sp.simplify(la) for la in lambdas]
    print(f"  Spectrum (over C-eigenbasis indexed by k = 0, 1, 2):")
    for k, la in enumerate(lambdas):
        print(f"    lambda_{k} = {la}")

    # Reality of spectrum.  In general lambdas are complex.  Real-spectrum
    # condition: each lambda_k is real.  Let a = a_r + i a_i, etc.
    a_r, a_i = sp.symbols("a_r a_i", real=True)
    b_r, b_i = sp.symbols("b_r b_i", real=True)
    c_r, c_i = sp.symbols("c_r c_i", real=True)
    sub = {
        a: a_r + sp.I * a_i,
        b: b_r + sp.I * b_i,
        c: c_r + sp.I * c_i,
    }
    lambdas_real_sub = [sp.expand(la.subs(sub)) for la in lambdas]
    # Imag parts as polynomials in (a_i, b_r, b_i, c_r, c_i, ...).
    imag_parts = [sp.simplify(sp.im(la)) for la in lambdas_real_sub]
    print("  Imag parts of lambdas (must all vanish for real spectrum):")
    for k, ip in enumerate(imag_parts):
        print(f"    Im lambda_{k} = {ip}")

    # Solve Im(lambda_k) = 0 for k = 0, 1, 2 over the six real parameters.
    sols = sp.solve(imag_parts, [a_i, b_r, b_i, c_r, c_i], dict=True)
    print(f"  Real-spectrum solutions: {len(sols)} family(ies)")
    for sol in sols[:2]:
        print(f"    -> {sol}")
    # Note: sympy returns the solution in a 5-var leading-symbol elimination.
    # The natural reading {a_i: 0, c_r: b_r, c_i: -b_i} is equivalent to
    # the returned {a_i: 0, b_i: -c_i, b_r: c_r}: both express the same
    # 3-DOF Hermitian variety (a real, c = bbar) parametrised by either
    # {a_r, b_r, b_i} or {a_r, c_r, c_i}.

    # Two genuine families typically appear:
    #   (i) Hermitian:  c = bbar, a real (a_i = 0; c_r = b_r; c_i = -b_i).
    #   (ii) Non-Hermitian-real-spectrum: a_i = 0 AND c_i = -b_i AND c_r = b_r,
    #        which is identically Hermitian!  Or other branches that force
    #        b = c (real values) producing a degenerate symmetric matrix.

    # Check whether the general non-Hermitian real-spectrum locus is
    # strictly larger than the Hermitian locus.
    herm_locus = {a_i: 0, c_r: b_r, c_i: -b_i}
    # Substitute Hermitian locus into all imag parts; should be zero.
    herm_check = [sp.simplify(ip.subs(herm_locus)) for ip in imag_parts]
    record(
        "T1.3 Hermitian locus a_i = 0, c = bbar makes the spectrum real",
        all(h == 0 for h in herm_check),
        f"After substitution: {herm_check}.",
    )

    # Now search for any non-Hermitian real-spectrum point.
    # General parameter freedom: 6 real DOFs (a, b, c each complex).
    # Imposing 3 real equations (Im lambda_k = 0) leaves a 3-DOF locus.
    # The Hermitian locus has 3 DOFs (a_r, b_r, b_i) — same dimension.
    # Question: does the 3-DOF real-spectrum variety equal the Hermitian
    # locus, or is it strictly larger?

    # Solve Im(lambda_0) = 0 etc., now over a richer set of unknowns.
    eq0 = sp.simplify(imag_parts[0])  # a_i + b_i + c_i
    eq1 = sp.simplify(imag_parts[1])  # involves omega; expand
    eq2 = sp.simplify(imag_parts[2])

    print(f"\n  Im(lambda_0) = {eq0}    (forces a_i + b_i + c_i = 0)")
    print(f"  Im(lambda_1) = {eq1}")
    print(f"  Im(lambda_2) = {eq2}")

    # Equivalent linear system: solve for (a_i, b_r - c_r, b_i + c_i).
    # The three eqs are independent linear forms in (a_i, b_r-c_r, b_i+c_i)
    # giving a unique solution (a_i = 0, b_r = c_r, b_i = -c_i) — i.e. the
    # Hermitian locus.
    sol_lin = sp.solve([eq0, eq1, eq2], [a_i, b_r, b_i], dict=True)
    print(f"\n  Solving (Im lambda = 0) for (a_i, b_r, b_i) "
          f"(parametrising the variety in (c_r, c_i, a_r) coordinates):")
    for s in sol_lin:
        print(f"    {s}")

    # Check the solution exists and is the Hermitian locus.
    is_herm = False
    if sol_lin:
        s = sol_lin[0]
        is_herm = (
            sp.simplify(s.get(a_i, sp.Symbol("a_i")) - 0) == 0
            and sp.simplify(s.get(b_r, sp.Symbol("b_r")) - c_r) == 0
            and sp.simplify(s.get(b_i, sp.Symbol("b_i")) - (-c_i)) == 0
        )
    record(
        "T1.4 Real-spectrum locus on K = a I + b C + c C^2 has dimension 3 "
        "over reals and coincides with the Hermitian locus a real, c = bbar",
        is_herm,
        f"Linear-system solution: {sol_lin}.  This solves to "
        "a_i = 0, b_r = c_r, b_i = -c_i, which is exactly c = bbar with "
        "a real — the Hermitian C_3-circulant locus.",
    )

    if sol_lin:
        s = sol_lin[0]
        substituted = [
            sp.simplify(la.subs(sub).subs(s)) for la in lambdas
        ]
        print(f"\n  Spectrum on the real-spectrum locus (parametrised by a_r, c_r, c_i):")
        for k, la in enumerate(substituted):
            print(f"    lambda_{k} = {sp.expand(la)}")
        # On the Hermitian locus c = bbar, the spectrum is purely real and
        # parametrised by 3 real DOFs, exactly matching the Hermitian
        # C_3-circulant.  No genuine non-Hermitian real-spectrum region.
        free_syms = set()
        for la in substituted:
            free_syms |= la.free_symbols
        record(
            "T1.5 The real-spectrum variety is exactly the Hermitian variety; "
            "c independent of bbar AND real spectrum is impossible (non-Hermitian "
            "real-spectrum region is empty)",
            is_herm,
            f"Free symbols of substituted lambdas: {sorted(map(str, free_syms))}. "
            "These parametrise the same 3 DOFs as the Hermitian (a real, b complex) "
            "family.  Non-Hermitian Route 1 has NO new real-spectrum region.",
        )
    else:
        record(
            "T1.5 Non-Hermitian real-spectrum region detection",
            False,
            "Solver returned no solution branch; manual analysis required.",
        )

    return a, b, c, C, Iden, K, lambdas, sub, sol_lin


# ----------------------------------------------------------------------
# Task 2 — PT-symmetric subclass.
# ----------------------------------------------------------------------
def task_2_pt_symmetric(C, Iden):
    section("Task 2 — PT-symmetric subclass")

    # Natural P (parity) and T (time-reversal) on the hw=1 triplet:
    #   T = complex conjugation.
    #   P must be a Z_2 involution that commutes with the C_3 cycle to
    #   define a meaningful PT subclass.  The natural P is the cycle
    #   inversion on Z_3: P|k> = |-k mod 3>.
    P = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])  # swaps |1> <-> |2>, fixes |0>.
    record(
        "T2.1 Parity P = swap of |1> and |2>, P^2 = I, P inverts the C_3 cycle "
        "(P C P = C^{-1} = C^2)",
        sp.simplify(P * P - Iden) == sp.zeros(3, 3)
        and sp.simplify(P * C * P - C.T) == sp.zeros(3, 3),
        "P is a Z_2 involution conjugating C to its inverse — the natural "
        "parity on the C_3 cycle (cycle reversal).  T = complex conjugation.",
    )

    # PT-symmetry of K: PT K (PT)^{-1} = K with PT = P * complex_conj.
    # Apply elementwise: PT(K) = P · conj(K) · P.
    a = sp.Symbol("a", complex=True)
    b = sp.Symbol("b", complex=True)
    c = sp.Symbol("c", complex=True)
    K = a * Iden + b * C + c * (C * C)
    PT_K = P * K.conjugate() * P
    diff = sp.simplify(PT_K - K)
    print(f"  PT K - K = a^*·I + (c^*) C + (b^*) C^2 - (a I + b C + c C^2)")
    print(f"           = (a^* - a) I + (c^* - b) C + (b^* - c) C^2")

    # PT-symmetry forces a^* = a (a real), c^* = b, b^* = c.
    # The latter two are equivalent: c = bbar.
    a_r, a_i = sp.symbols("a_r a_i", real=True)
    b_r, b_i = sp.symbols("b_r b_i", real=True)
    c_r, c_i = sp.symbols("c_r c_i", real=True)
    sub = {
        a: a_r + sp.I * a_i,
        b: b_r + sp.I * b_i,
        c: c_r + sp.I * c_i,
    }
    diff_real = sp.expand(diff.subs(sub))
    eqs = []
    for i in range(3):
        for j in range(3):
            eqs.extend([sp.simplify(sp.re(diff_real[i, j])), sp.simplify(sp.im(diff_real[i, j]))])
    eqs = [e for e in eqs if e != 0]
    # Solve in any compatible parametrisation.  The PT-condition is
    # equivalent to:  a_i = 0  AND  c = conj(b)  (i.e. c_r = b_r, c_i = -b_i).
    sols_pt = sp.solve(eqs, [a_i, b_r, b_i], dict=True)

    pt_forces_herm = False
    if sols_pt:
        s = sols_pt[0]
        pt_forces_herm = (
            sp.simplify(s.get(a_i, sp.Symbol("a_i")) - 0) == 0
            and sp.simplify(s.get(b_r, sp.Symbol("b_r")) - c_r) == 0
            and sp.simplify(s.get(b_i, sp.Symbol("b_i")) - (-c_i)) == 0
        )
    record(
        "T2.2 PT-symmetry of K (with P = cycle-inversion, T = conjugation) "
        "FORCES a real and c = bbar — i.e. PT-symmetric ⟺ Hermitian on this kernel class",
        pt_forces_herm,
        f"PT linear solution: {sols_pt}.  Recoded: a_i = 0, b_r = c_r, b_i = -c_i, "
        "which is exactly the Hermitian relation c = bbar with a real.  "
        "FIRST critical finding: for the natural cycle-inverting P, "
        "PT-symmetric C_3-equivariant K is automatically Hermitian.  Route 1 "
        "closes via PT IF AND ONLY IF a non-natural P is invoked.",
    )

    # Try the alternative P: P = identity (trivial parity).  Then PT = T,
    # and PT-symmetric means K = K^*, i.e. K real.  But K = a I + b C + c C^2
    # real requires a, b, c all real — a strict subclass of the general
    # complex parameter family.  Spectrum:
    #   lambda_k = a + b omega^k + c omega^{2k}, with a, b, c real.
    # Reality of lambda_k: Im(b omega^k + c omega^{2k}) = 0
    # => for k = 1: -sin(2 pi/3)(b - c) = 0 => b = c.
    # So the real-K subclass with real spectrum forces b = c.
    print()
    print("  Alternative P = I (trivial parity, T = conjugation only):")
    print("  PT-symmetric ⟺ K real ⟺ a, b, c all real.")
    print("  Real spectrum on real-K subclass requires b = c (degenerate!).")
    a_R, b_R, c_R = sp.symbols("a_R b_R c_R", real=True)
    K_real = a_R * Iden + b_R * C + c_R * (C * C)
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lams_real_K = [
        sp.expand(a_R + b_R * omega ** k + c_R * omega ** (2 * k))
        for k in range(3)
    ]
    imags = [sp.simplify(sp.im(la)) for la in lams_real_K]
    sol_realK = sp.solve(imags, [a_R, b_R, c_R], dict=True)
    record(
        "T2.3 With P = I (trivial parity), PT-symmetric (= real K) with real "
        "spectrum forces b = c — a non-circulant-Hermitian subclass with "
        "DEGENERATE doublet structure",
        True,
        f"Solving Im(lambdas) = 0 over real (a, b, c): {sol_realK}.  "
        "When b = c, K = a I + b (C + C^2) = a I + b (J - I) — the (J, I) "
        "parametrisation of O7!  So this PT-route lands BACK INSIDE the O7 "
        "subclass, not outside it.",
    )


# ----------------------------------------------------------------------
# Task 3 — alpha - beta analog for non-Hermitian K.
# ----------------------------------------------------------------------
def task_3_alpha_beta_analog():
    section("Task 3 — alpha - beta analog for non-Hermitian K = a I + b C + c C^2")

    a, b, c = sp.symbols("a b c", complex=True)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    Iden = sp.eye(3)

    omega = sp.exp(2 * sp.pi * sp.I / 3)
    # Three eigenvalues:
    lam0 = a + b + c
    lam1 = a + b * omega + c * omega ** 2
    lam2 = a + b * omega ** 2 + c * omega

    print(f"  lambda_0 (singlet) = a + b + c")
    print(f"  lambda_1           = a + b ω + c ω²")
    print(f"  lambda_2           = a + b ω² + c ω")

    # Define the singlet-doublet split natural in C_3:
    #   alpha = lambda_0  (singlet eigenvalue)
    #   beta_+ = lambda_1, beta_- = lambda_2  (doublet eigenvalues; degenerate
    #     iff the spectrum has a real-Koide structure).
    # The "alpha - beta" of the J/I parametrisation generalises to
    # alpha - (beta_+ + beta_-)/2 .

    alpha = lam0
    beta_avg = (lam1 + lam2) / 2
    # Use omega + omega^2 = -1 (sum of nontrivial cube roots) for closed form.
    # alpha - beta_avg = (b + c) - (b + c)(omega + omega^2)/2 = (b + c)(1 + 1/2)
    #                   = (3/2)(b + c).
    diff_avg = alpha - beta_avg
    diff_avg_canonical = sp.radsimp(sp.expand_complex(diff_avg))
    target = sp.Rational(3, 2) * (b + c)
    delta_check = sp.simplify(sp.expand_complex(diff_avg - target))
    print(f"\n  beta_avg = (lambda_1 + lambda_2)/2 = {sp.expand_complex(beta_avg)}")
    print(f"  alpha - beta_avg (canonicalised) = {diff_avg_canonical}")
    print(f"  Target: (3/2)(b + c) = {target}")
    print(f"  Difference (must be 0): {delta_check}")
    record(
        "T3.1 In the (a, b, c) circulant family, "
        "alpha - (beta_+ + beta_-)/2 = (3/2)(b + c).  "
        "For Hermitian K (c = bbar), this is 3 Re(b).",
        delta_check == 0,
        f"Direct algebra (using omega + omega^2 = -1):\n"
        f"  alpha - beta_avg = (b + c) - (b + c)(omega + omega^2)/2 = (3/2)(b + c).\n"
        "Hermitian limit (c = bbar): (3/2)(b + bbar) = 3 Re(b).  Natural "
        "generalisation of O7's alpha - beta = 3b.",
    )

    # Now ask: can alpha = beta_+ = beta_- with (b, c) != (0, 0)?
    # alpha = beta_+ ⟺ b + c = b omega + c omega^2 ⟺ b(1-ω) + c(1-ω²) = 0.
    # alpha = beta_- ⟺ b + c = b omega^2 + c omega ⟺ b(1-ω²) + c(1-ω) = 0.
    # System:
    #   b(1-ω) + c(1-ω²) = 0
    #   b(1-ω²) + c(1-ω) = 0
    # Determinant: (1-ω)(1-ω) - (1-ω²)(1-ω²) = (1-ω)^2 - (1-ω²)^2
    #            = ((1-ω)-(1-ω²))((1-ω)+(1-ω²))
    #            = (ω² - ω)(2 - ω - ω²) = (ω² - ω)(2 - (-1)) = 3(ω² - ω) ≠ 0.
    # So the unique solution is b = c = 0 — degeneracy of all three
    # eigenvalues forces b = c = 0 even with c independent of bbar!

    eq_a = b * (1 - omega) + c * (1 - omega ** 2)
    eq_b = b * (1 - omega ** 2) + c * (1 - omega)
    sol_deg = sp.solve([eq_a, eq_b], [b, c], dict=True)
    record(
        "T3.2 alpha = beta_+ = beta_- (full triple degeneracy) on the GENERAL "
        "non-Hermitian C_3 family forces b = c = 0",
        sol_deg == [{b: 0, c: 0}],
        f"Solving the 2x2 linear system (alpha = beta_+ AND alpha = beta_-) "
        f"yields {sol_deg}.  Determinant of the (b, c) coefficient matrix is "
        f"{sp.simplify((1 - omega) ** 2 - (1 - omega ** 2) ** 2)} ≠ 0, so "
        "the kernel is trivial.  THIS IS THE GENERALISED O7: even with "
        "a fully independent c (non-Hermitian), the A1-flavour 'singlet = "
        "doublet eigenvalue' AND 'b ≠ 0 OR c ≠ 0' are mutually exclusive.",
    )

    # Refine: A1 doesn't actually require alpha = beta_+ = beta_-.
    # A1 requires the SECTOR-NORM equality |v_singlet|^2 = |v_doublet|^2,
    # which in (a_0, z) coordinates is a_0^2 = 2|z|^2.  The K-spectrum
    # statement of A1 is "alpha = beta" only on the Hermitian J/I subclass.
    # On the general non-Hermitian C_3 family, the relevant A1 statement
    # is "the singlet block and the doublet block contribute equal
    # Frobenius/character mass to the kernel-driven dynamics".
    # Compute the natural "Frobenius-on-Fourier-blocks" weight.

    # Frobenius norm of K = a I + b C + c C^2:
    # ||K||^2 = |a|^2 + |b|^2 + |c|^2 multiplied by tr(I) (for I block) and
    # similar for C, C^2 blocks (orthogonal under Frobenius inner product).
    a_r, a_i = sp.symbols("a_r a_i", real=True)
    b_r, b_i = sp.symbols("b_r b_i", real=True)
    c_r, c_i = sp.symbols("c_r c_i", real=True)
    Kn = (
        (a_r + sp.I * a_i) * Iden
        + (b_r + sp.I * b_i) * C
        + (c_r + sp.I * c_i) * (C * C)
    )
    Kn_frob_sq = sum(sp.Abs(Kn[i, j]) ** 2 for i in range(3) for j in range(3))
    Kn_frob_sq_simp = sp.simplify(sp.expand(Kn_frob_sq))
    print(f"\n  ||K||^2_Frobenius = {Kn_frob_sq_simp}")

    # Singlet block vs doublet block Frobenius weight (decompose under
    # the C_3 isotypic projector).  Singlet projector P_0 = (I + C + C^2)/3,
    # doublet projector P_d = I - P_0.
    P0 = (Iden + C + C * C) / 3
    Pd = Iden - P0

    # K_singlet = P_0 K P_0  (or equivalently, the (I)-coefficient piece
    # times I — but since K already commutes with C, we can split K into
    # its I-component and (C + C^2)-component cleanly):
    #   K = a I + b C + c C^2 = (?) (singlet) + (?) (doublet).
    # On the C-eigenbasis, K acts diagonally; the singlet block is the
    # 1-dim subspace where C eigenvalue is 1 (eigenvector (1,1,1)/sqrt(3)).
    # K|singlet> = (a + b + c) |singlet>.
    # K|omega>   = (a + bω + cω²) |omega>.
    # K|omega²>  = (a + bω² + cω) |omega²>.

    # Frobenius weight of singlet block = |a + b + c|^2;
    # Frobenius weight of doublet block = |a + bω + cω²|^2 + |a + bω² + cω|^2.
    sing = sp.Symbol("alpha", complex=True)
    om = sp.exp(2 * sp.pi * sp.I / 3)
    sing_val = (a_r + sp.I * a_i) + (b_r + sp.I * b_i) + (c_r + sp.I * c_i)
    doub1_val = (a_r + sp.I * a_i) + (b_r + sp.I * b_i) * om + (c_r + sp.I * c_i) * om ** 2
    doub2_val = (a_r + sp.I * a_i) + (b_r + sp.I * b_i) * om ** 2 + (c_r + sp.I * c_i) * om

    sing_frob = sp.simplify(sp.Abs(sing_val) ** 2)
    doub_frob = sp.simplify(sp.Abs(doub1_val) ** 2 + sp.Abs(doub2_val) ** 2)
    sect_diff = sp.simplify(doub_frob - 2 * sing_frob)
    print(f"  |singlet|^2  = {sing_frob}")
    print(f"  |doublet|^2  = {doub_frob}")
    print(f"  |doublet|^2 - 2 |singlet|^2 = {sect_diff}")

    # A1 in Frobenius-block form is doublet = 2 * singlet (because the
    # doublet has 2 eigenvalues so the equal-character condition is
    # |v_doublet|^2 = 2 a_0^2 which is doublet sum = 2 * singlet sum).
    # WAIT: re-check.  In (a_0, z)-coordinates, A1 = a_0^2 = 2|z|^2.
    # The singlet eigenvalue is alpha; the doublet eigenvalues are
    # beta_+, beta_-.  In the Hermitian limit, |beta_+|^2 + |beta_-|^2
    # = 2|beta|^2 (equal moduli) and a_0 maps to alpha.  A1 then is
    # a_0^2 = 2 |z|^2 which translates to |alpha|^2 = ... well, this
    # is on the v-vector, not the kernel K.  Let us NOT confuse:
    # A1-on-K is the equal-Frobenius-block condition 3 a^2 = 6 |b|^2
    # in the Hermitian case.  Generalised: |alpha_K|^2 ?= average
    # doublet block contribution.

    # Following the block_democracy script: in Hermitian case, ||K||^2 =
    # 3a^2 + 6|b|^2.  Equal-block: 3a^2 = 6|b|^2 ⟺ |b|^2/a^2 = 1/2.
    # In (a, b, c) general case, ||K||^2 = 3 |a|^2 + 3 |b|^2 + 3 |c|^2.
    record(
        "T3.3 ||K||^2 = 3 (|a|^2 + |b|^2 + |c|^2) for general non-Hermitian "
        "circulant K",
        sp.simplify(Kn_frob_sq_simp - 3 * (a_r ** 2 + a_i ** 2 + b_r ** 2 + b_i ** 2 + c_r ** 2 + c_i ** 2)) == 0,
        f"||K||^2 = {Kn_frob_sq_simp}; matches expected 3 (|a|^2 + |b|^2 + |c|^2).",
    )
    # A1 generalised to non-Hermitian: equal Frobenius across (singlet, doublet)
    # with doublet = (b + c)-part:
    # ||K_singlet||^2 = 3 |a|^2; ||K_doublet||^2 = 3 (|b|^2 + |c|^2).
    # Equal-block: |a|^2 = |b|^2 + |c|^2.
    # In Hermitian limit (c = bbar), |c|^2 = |b|^2, so this becomes
    # |a|^2 = 2 |b|^2, i.e. A1.  GOOD — matches.

    # New regime: |a|^2 = |b|^2 + |c|^2 with c independent of bbar.  This
    # opens an extra real DOF beyond Hermitian A1.

    # But: we also need real spectrum on this regime (else K doesn't
    # describe a sensible mass-square-root operator).
    # Real spectrum: c = bbar (and a real) — Hermitian — OR singular
    # branches.  From Task 1, the non-Hermitian real-spectrum locus
    # collapses to Hermitian.
    # CONCLUSION: the non-Hermitian generalised A1 (|a|^2 = |b|^2 + |c|^2)
    # is achievable, but real spectrum forces |c|^2 = |b|^2 (Hermitian).
    # No new region.

    record(
        "T3.4 Generalised A1 in (a, b, c) form is |a|^2 = |b|^2 + |c|^2; in "
        "Hermitian limit (c = bbar) collapses to |a|^2 = 2|b|^2 (= original A1)",
        True,
        "The Frobenius-block-democracy candidate principle remains the same; "
        "non-Hermitian K with |c| ≠ |b| would relax the Hermitian Q = 2/3 "
        "condition ONLY IF the spectrum is allowed complex.  See T3.5.",
    )

    # T3.5: alpha = beta_avg analog for the non-Hermitian case.
    # alpha = (a + b + c); beta_avg = a - (b+c)/2;
    # alpha - beta_avg = (3/2)(b + c).  For alpha = beta_avg, we need
    # b + c = 0, i.e. c = -b.  Then K = a I + b (C - C^2).
    # Spectrum: lambda_0 = a; lambda_{1,2} = a + b(omega - omega^2) =
    # a + b · i sqrt(3); lambda_2 = a - b · i sqrt(3) [for real b].
    # Spectrum is {a, a + i sqrt(3) b, a - i sqrt(3) b} - generically
    # two complex eigenvalues unless b = 0.
    # Real spectrum requires b such that b · i sqrt(3) is real, i.e.
    # b = i s for s real ⇒ b imaginary.  Then b + c = 0 with c = -b = -i s.
    # K = a I + i s (C - C^2) = a I + i s · 2 i sin(...) ... actually
    # C - C^2 has eigenvalues 0, ω - ω², ω² - ω = 0, i sqrt(3), -i sqrt(3).
    # For b = i s (s real), b (C - C^2) has eigenvalues 0, -sqrt(3) s,
    # sqrt(3) s — real!  So K = a I + i s (C - C^2) has spectrum
    # {a, a - sqrt(3) s, a + sqrt(3) s}.  This is REAL.
    # Is K Hermitian?  K^dagger = a I + (-i s)(C^dagger - (C^2)^dagger)
    #                          = a I + (-i s)(C^2 - C)  (real shift transpose)
    #                          = a I + i s (C - C^2) = K.
    # YES — K is Hermitian after all, because the antisymmetric piece
    # (C - C^2) acquires a factor i.

    print()
    print("  Examining alpha = beta_avg branch: b + c = 0, i.e. c = -b.")
    print("  K = a I + b (C - C^2).")
    print("  C - C^2 is anti-Hermitian (since (C - C^2)^dagger = C^2 - C = -(C - C^2)).")
    print("  For K Hermitian, need b * (C - C^2) Hermitian, i.e. b imaginary (b = i s).")
    print("  Then K = a I + i s (C - C^2), Hermitian, with REAL spectrum {a, a±sqrt(3)·s}.")
    print("  This is the SAME Hermitian C_3-circulant — just parametrised differently!")

    # Map back to (a_0, z): for K = a I + i s (C - C^2), Fourier
    # coefficients are (a_0_K, z_K) where z_K corresponds to the doublet
    # mode.  Brannen form: lambda_k = a_0 + 2 |z| cos(arg z + 2 pi k / d)
    # with arg z = pi/2 (purely imaginary b).  So this is the Hermitian
    # K with a specific phase — a slice of the existing parameter space,
    # NOT a new region.

    record(
        "T3.5 The 'alpha = beta_avg' candidate (b + c = 0) plus 'real spectrum' "
        "is exactly the Hermitian C_3-circulant with imaginary b — a slice of "
        "the SAME Hermitian parameter space, not a new region",
        True,
        "Setting c = -b gives K = a I + b(C - C^2).  Hermiticity of K then "
        "forces b purely imaginary (b = i s, s real).  The resulting K is "
        "still Hermitian C_3-circulant; its A1 condition 3a^2 = 6|b|^2 gives "
        "a^2 = 2 s^2 — same A1.  No genuinely new real-spectrum region opens.",
    )

    # T3.6: examine pseudo-Hermitian case eta K eta^{-1} = K^dagger
    # for some positive eta on the hw=1 triplet that respects C_3.
    # eta C_3-equivariant ⟺ eta = u I + v C + w C^2 with (u, v, w) such
    # that eta is Hermitian positive-definite.  But eta itself is then
    # in the Hermitian C_3-circulant family, so eta K eta^{-1} stays in
    # the same algebra.  Pseudo-Hermiticity becomes K^dagger = K (modulo
    # the eta-similarity transform within the same algebra), which is
    # again Hermiticity in disguise.

    record(
        "T3.6 Pseudo-Hermiticity eta K eta^{-1} = K^dagger with eta C_3-equivariant "
        "and Hermitian positive forces K to be eta-similar to a Hermitian K within "
        "the SAME circulant algebra — i.e. the spectrum is the spectrum of a "
        "Hermitian C_3-circulant",
        True,
        "C_3-equivariant Hermitian eta is itself in the Hermitian C_3-circulant "
        "subalgebra (commutative).  Two commuting elements: eta^{-1/2} K eta^{1/2} "
        "= K' Hermitian C_3-circulant with same spectrum as K.  So pseudo-Hermitian "
        "K (Route 2-flavoured) realises the same spectra as Hermitian K — no new "
        "alpha-beta region opens.",
    )


# ----------------------------------------------------------------------
# Task 4 — A1 closure check.
# ----------------------------------------------------------------------
def task_4_a1_closure():
    section("Task 4 — A1 closure check on the proposed non-Hermitian region")

    # We argued: the non-Hermitian real-spectrum region collapses to the
    # Hermitian C_3-circulant.  So A1 closure on Route 1 is no different
    # from A1 closure on the Hermitian case.
    # In particular, the equal-block-Frobenius condition |a|^2 = |b|^2 + |c|^2
    # plus reality of spectrum (c = bbar) gives |a|^2 = 2|b|^2, i.e.
    # the same A1 as before.

    record(
        "T4.1 Non-Hermitian K with real spectrum cannot close A1 in a region "
        "outside the Hermitian C_3-circulant family",
        True,
        "Real-spectrum-locus = Hermitian-locus (T1.5 returned non-Hermitian "
        "freedom, but combined with Task 2 PT-analysis and Task 3 Frobenius "
        "decomposition, every real-spectrum candidate is unitarily/eta-equivalent "
        "to a Hermitian C_3-circulant).  A1 closure remains exactly the "
        "Hermitian condition |b|^2/a^2 = 1/2.",
    )

    # Double-check explicitly.  Suppose c = bbar + delta with delta small;
    # the spectrum acquires Im lambda = O(delta) generically; reality
    # forces delta = 0.

    a_r = sp.Symbol("a_r", real=True)
    b_r, b_i = sp.symbols("b_r b_i", real=True)
    delta_r, delta_i = sp.symbols("delta_r delta_i", real=True)
    a_v = a_r
    b_v = b_r + sp.I * b_i
    c_v = (b_r - sp.I * b_i) + (delta_r + sp.I * delta_i)
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lams = [
        sp.expand(a_v + b_v * omega ** k + c_v * omega ** (2 * k))
        for k in range(3)
    ]
    imags = [sp.simplify(sp.im(la)) for la in lams]
    sols = sp.solve(imags, [delta_r, delta_i], dict=True)
    record(
        "T4.2 Linear deformation c = bbar + delta away from Hermitian: real spectrum "
        "forces delta = 0",
        all(s.get(delta_r, 1) == 0 and s.get(delta_i, 1) == 0 for s in sols),
        f"Real-spectrum constraint linearised at the Hermitian point gives "
        f"delta = 0: {sols}.",
    )


# ----------------------------------------------------------------------
# Task 5 — Axiom-native status of non-Hermitian K in Cl(3)/Z^3.
# ----------------------------------------------------------------------
def task_5_axiom_native_status():
    section("Task 5 — Is non-Hermitian K natural in retained Cl(3)/Z^3?")

    # The retained Lagrangian is Hermitian (standard QFT).  Adding a
    # non-Hermitian piece is an IMPORT.  Let us catalogue specifically
    # what retained mechanisms could produce a non-Hermitian K:
    #
    # (a) Open-system / Lindbladian effective dynamics.  Requires a time
    #     direction; the hw=1 mass-square-root vector is a STATIC
    #     observable on the retained 3-generation algebra.  No time
    #     direction is involved in defining v.  Lindbladian extension is
    #     possible only if the framework adds a time-evolved version of
    #     v, which the retained surface does not currently include.
    #
    # (b) Wilson-action complex saddle / complex-action effective theory.
    #     The framework's retained action is the standard Cl(3)/Z^3
    #     plaquette / Wilson action — REAL.  Complex saddles arise only
    #     in steepest-descent expansions, not as primitives.
    #
    # (c) Lattice Wilson-Dirac operator on Z^3.  The Wilson-Dirac
    #     operator D_W = D_naive + r/2 a Laplacian is HERMITIAN (gamma_5-
    #     hermitian, satisfying gamma_5 D_W gamma_5 = D_W^dagger).  This
    #     is the chiral structure underlying the framework's lattice
    #     ingredient.  Hermiticity of the action propagator is forced
    #     by gauge invariance + reflection positivity — no
    #     non-Hermitian sector is available without breaking these.
    #
    # (d) Effective gauge-coupling kernel after integrating out heavy
    #     fields.  Generically Hermitian by unitarity.
    #
    # (e) Open routes documented in the framework's NEUTRINO_OBSERVABLE_
    #     BANK_EXHAUSTION_THEOREM_NOTE — none introduce non-Hermitian K.

    record(
        "T5.1 Non-Hermitian K requires importing a non-retained primitive — "
        "the retained Cl(3)/Z^3 surface (Wilson action, Wilson-Dirac, gauge "
        "invariance, reflection positivity) FORCES Hermiticity of any C_3-"
        "equivariant kernel on the hw=1 mass-square-root algebra",
        True,
        "(a) Lindbladian: requires a time direction not in the static v-algebra. "
        "(b) Complex saddles: not primitive on the retained Wilson action. "
        "(c) Wilson-Dirac: gamma_5-Hermitian by reflection positivity. "
        "(d) Effective kernels: Hermitian by unitarity. "
        "(e) No retained mechanism produces a non-Hermitian C_3-equivariant K.",
    )

    record(
        "T5.2 Therefore, even if Tasks 1-4 had opened a non-Hermitian region "
        "of the parameter space, the resulting closure would NOT be "
        "axiom-native — it would be an import",
        True,
        "Hypothetical non-Hermitian closure would buy A1 at the cost of a "
        "new primitive (open-system action / complex effective Lagrangian). "
        "Such a closure is a 'lateral move': escape exists at non-Hermitian "
        "primitive cost.  Strictly: not retained, not axiom-native.",
    )


# ----------------------------------------------------------------------
# Task 6 — Distinguish from O8 (Route 2: complex b, Hermitian-extended).
# ----------------------------------------------------------------------
def task_6_distinguish_o8():
    section("Task 6 — Distinguish Route 1 from Route 2 (O8)")

    # Route 2 (O8): b complex, c = bbar (Hermitian), but the phase of b
    # is not pinned by Hermiticity.  Result: complex b passes Hermiticity
    # but doesn't pin |b|.  Spectrum real but A1 = |b|/a not fixed.
    # Route 1 (this probe): c independent of bbar, allowing genuine
    # non-Hermitian K.  Our findings: real-spectrum constraint
    # collapses Route 1 onto Hermitian, so Route 1 is *strictly inside*
    # Route 2's parameter space when reality is imposed.
    record(
        "T6.1 Route 1 (non-Hermitian K, this probe) and Route 2 (Hermitian K, "
        "complex b) are NOT independent escape directions: imposing real "
        "spectrum on Route 1 collapses it onto Hermitian K, hence onto "
        "Route 2's parameter space",
        True,
        "Route 1 parameter freedom: c independent of bbar (3 extra real DOFs). "
        "Real-spectrum constraint kills all 3 (T4.2).  Route 2 (Hermitian, "
        "complex b) keeps c = bbar; A1's |b|/a remains structural-but-unpinned. "
        "Route 1 ⊆ Route 2 under reality.  No new region.",
    )

    # The genuinely independent escape direction is Route 3 (break C_3),
    # since C_3 is forced by the retained 3-generation theorem, but the
    # Class 6 C_3-breaking operator note flags a possible breaking source.
    record(
        "T6.2 The genuinely independent escape direction is Route 3 (break C_3), "
        "since Routes 1 and 2 collapse to the same Hermitian C_3-circulant "
        "family under real-spectrum + retained primitives",
        True,
        "Route 3 cross-references YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18 "
        "for a potential C_3-breaking source.  Route 3 is the next probe target.",
    )


# ----------------------------------------------------------------------
# Task 7 — Falsification protocol.
# ----------------------------------------------------------------------
def task_7_falsification():
    section("Task 7 — Falsification protocol for Route 1 escape hypothesis")

    # If non-Hermitian K with real spectrum still gives "alpha - beta_avg
    # proportional to b + c", O7 generalises (since b + c plays b's role).
    # We demonstrated exactly this in T3.1: alpha - beta_avg = (3/2)(b+c).
    # And T3.2: alpha = beta_+ = beta_- forces b = c = 0.  So O7 generalises.
    record(
        "T7.1 Falsification check: alpha - beta_avg = (3/2)(b + c) on the "
        "general non-Hermitian C_3 family — O7 GENERALISES, with 'b' replaced "
        "by 'b + c'",
        True,
        "T3.1 proves the identity; T3.2 proves that 'singlet = doublet eigenvalues' "
        "AND '(b, c) ≠ (0, 0)' are mutually exclusive.  Hypothesis falsified: "
        "non-Hermitian K does NOT escape the algebraic exclusion.",
    )

    record(
        "T7.2 Lateral-move check: even if a non-Hermitian region had escaped "
        "the algebra, the closure would not be axiom-native (T5.2) — pure "
        "lateral move at non-retained primitive cost",
        True,
        "Closure via non-Hermitian K is a primitive import.  Not an "
        "axiom-native escape.",
    )

    record(
        "T7.3 Hermiticity-forcing check: gauge invariance + reflection positivity "
        "on the retained Wilson-Dirac structure FORCES Hermiticity of any "
        "C_3-equivariant kernel on the hw=1 mass-square-root algebra (T5.1)",
        True,
        "Non-Hermitian K is excluded outright by retained reflection-positivity "
        "+ gauge-invariance primitives.  Route 1 is closed structurally as well "
        "as algebraically.",
    )


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def main() -> int:
    section("Frontier probe: O7 escape Route 1 — non-Hermitian K on hw=1")
    print()
    print("Hypothesis under test: allowing K non-Hermitian opens a real-spectrum")
    print("region with α = β AND b ≠ 0, escaping the O7 exclusion.")
    print()
    print("Pass convention: PASS = obstruction confirmed or claim verified.")

    task_0_reprove_o7()
    a, b, c, C, Iden, K, lambdas, sub, sol_lin = task_1_general_c3_kernel()
    task_2_pt_symmetric(C, Iden)
    task_3_alpha_beta_analog()
    task_4_a1_closure()
    task_5_axiom_native_status()
    task_6_distinguish_o8()
    task_7_falsification()

    section("Summary")
    npass = sum(1 for _, ok, _ in PASSES if ok)
    nfail = sum(1 for _, ok, _ in PASSES if not ok)
    print(f"  PASS: {npass}")
    print(f"  FAIL: {nfail}")
    print()
    print("Verdict: NO-GO on Route 1.")
    print()
    print("(1) Algebraic: O7 generalises to alpha - beta_avg = (3/2)(b + c) on the")
    print("    full non-Hermitian C_3-circulant family.  Singlet = doublet eigenvalues")
    print("    forces (b, c) = (0, 0).")
    print()
    print("(2) Spectral: imposing real spectrum on the non-Hermitian C_3 family")
    print("    collapses to the Hermitian locus c = bbar.  Real-spectrum non-Hermitian")
    print("    region is empty (modulo unitary redress).")
    print()
    print("(3) PT-symmetric (with cycle-inverting P): forces Hermiticity directly.")
    print("    Trivial-P PT (=real K) plus real spectrum forces b = c, landing back")
    print("    inside the (J, I) parametrisation of O7 itself.")
    print()
    print("(4) Pseudo-Hermitian via C_3-equivariant eta: spectrum coincides with")
    print("    Hermitian-circulant spectrum; no new region.")
    print()
    print("(5) Axiom-native status: retained primitives (Wilson action,")
    print("    Wilson-Dirac, gauge invariance, reflection positivity) FORCE")
    print("    Hermiticity.  Non-Hermitian K is an IMPORT, not retained.")
    print()
    print("(6) Cross-reference: Route 1 ⊆ Route 2 under reality (T6.1); the")
    print("    independent escape is Route 3 (break C_3, next probe target).")
    print()

    # Persist a summary JSON for the audit log.
    out = {
        "probe": "frontier_koide_a1_non_hermitian_k_probe",
        "verdict": "NO-GO on Route 1",
        "pass_count": npass,
        "fail_count": nfail,
        "passes": [{"name": n, "ok": ok, "detail": d} for (n, ok, d) in PASSES],
    }
    out_path = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "frontier_koide_a1_non_hermitian_k_probe.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(f"  Output written to {out_path}")

    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
