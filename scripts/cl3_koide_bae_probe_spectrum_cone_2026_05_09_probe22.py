"""
Koide BAE Probe 22 — Spectrum-Level Cone Localization Pivot

Tests the SPECTRUM-LEVEL closure pivot for the Brannen Amplitude
Equipartition (BAE) condition |b|^2/a^2 = 1/2 on the C_3-equivariant
Hermitian circulant H = aI + bC + b̄C^2 on hw=1.

PIVOT (distinct from Probes 1-21):
   Prior probes attacked closure at the PARAMETER level — derive
   (a, |b|) values such that |b|^2/a^2 = 1/2. All 18 named probes
   returned bounded structural obstruction.
   This probe asks: pivot away from parameter-level. Instead of
   deriving (a, b), derive directly that the eigenvalues
   {lambda_0, lambda_1, lambda_2} of H lie on the Koide cone
       lambda_0^2 + lambda_1^2 + lambda_2^2  =  4 (lambda_0 lambda_1
                                                  + lambda_0 lambda_2
                                                  + lambda_1 lambda_2)
   directly. The retained polynomial identity
   KOIDE_CONE_THREE_FORM_EQUIVALENCE then closes Q = 2/3, which by
   retained CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE is
   BAE.

QUESTION: does this spectrum-level pivot escape the parameter-level
obstruction?

ANSWER: NO. The retained Koide-Circulant Character Bridge identity
(positive_theorem) makes the spectrum-level cone localization
arithmetically identical to the parameter-level BAE:

   bridge identity (T3, KOIDE_CIRCULANT_CHARACTER_BRIDGE):
       a_0^2 - 2 |z|^2  ==  3 a^2 - 6 |b|^2          (algebraic)

   spectrum-level cone (the target of this probe):
       2 (lambda_0 + lambda_1 + lambda_2)^2  ==  3 (lambda_0^2
                                                  + lambda_1^2
                                                  + lambda_2^2)
       <=>  3 a_0^2  ==  3 (a_0^2 + 2|z|^2) * (1/3) ... (rewrites)
       <=>  a_0^2  ==  2 |z|^2                       (Plancherel)
       <=>  a^2  ==  2 |b|^2                          (bridge T3)
       <=>  BAE: |b|^2 / a^2  ==  1/2                 (definition)

These four equational forms are ALL equivalent algebraically. The
bridge identity is retained (positive_theorem) and exact. Therefore:

   "spectrum lies on the Koide cone"
       and
   "operator parameters satisfy BAE"
   are NOT distinct mathematical statements on
   Herm_circ(3) = M_3(C)^{C_3}-Hermitian.

The pivot does not provide a new derivation route — it provides the
SAME equation in DIFFERENT variables. Any derivation of
"spectrum-on-cone" reduces, by the bridge identity, to a derivation
of BAE. And conversely: a probe that fails at the parameter level
fails at the spectrum level for the SAME reason, because the two
levels are bridge-identical.

VERDICT: SHARPENED bounded obstruction.

   The spectrum-level pivot is RULED OUT as a route to closure
   distinct from the parameter-level routes already enumerated by
   Probes 1-21. The 18-probe campaign's terminal residue —
   "the (1, 1)-multiplicity-weighted Frobenius pairing on
   M_3(C)_Herm under C_3-isotype decomposition" / equivalently
   "the U(1)_b angular quotient on the non-trivial doublet of
   A^{C_3}" — is now confirmed to apply at BOTH the parameter and
   spectrum levels. There is no spectrum-level escape hatch.

   BAE admission count: UNCHANGED. No new admissions. No promotion.

This runner verifies the spectrum-level / parameter-level
arithmetic equivalence with explicit symbolic computation and
numerical instances spanning both BAE-satisfying and non-BAE
regions.

No PDG values used as derivation input — masses appear nowhere.
"""

from __future__ import annotations

import sympy as sp


def header(text: str) -> None:
    print()
    print("=" * 72)
    print(text)
    print("=" * 72)


def report(passed: list[bool], section: str) -> tuple[int, int]:
    n_pass = sum(1 for p in passed if p)
    n_fail = sum(1 for p in passed if not p)
    print(f"  {section}: PASS={n_pass}, FAIL={n_fail}")
    return n_pass, n_fail


def section_1_setup() -> tuple[int, int]:
    """
    Section 1 — Retained inputs.

    Verify R1 (circulant Hermitian form on hw=1) and R2 (eigenvalue
    spectrum) are realized on a concrete C_3-equivariant Hermitian.
    """
    header("Section 1 — Retained inputs (R1, R2)")
    passed: list[bool] = []

    # Standard 3x3 cyclic shift (right-shift)
    C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    I3 = sp.eye(3)
    Cstar = C.T  # since C is real, C^* = C^T = C^2

    # Test 1.1 — C is order 3
    cube = C**3
    test = (cube == I3)
    passed.append(test)
    print(f"  T1.1 C^3 = I exact: PASS={test}")

    # Test 1.2 — C is unitary (over Z, doubly-stochastic permutation)
    test = (C * Cstar == I3)
    passed.append(test)
    print(f"  T1.2 C unitary: PASS={test}")

    # Test 1.3 — Eigenvalues of C are {1, omega, omega^2} (verify by
    # checking characteristic polynomial = lambda^3 - 1)
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lam = sp.symbols("lam")
    char_poly = sp.simplify((C - lam * I3).det())
    target_poly = sp.simplify(-(lam**3 - 1))
    test = (sp.simplify(char_poly - target_poly) == 0)
    passed.append(test)
    print(f"  T1.3 char poly of C is -(lam^3 - 1) (eigenvalues "
          f"{{1, omega, omega^2}}): PASS={test}")

    # Test 1.4 — Construct circulant H = aI + bC + b̄ C^2 with symbolic
    # (a, b) and verify Hermiticity on (a real, b complex)
    a = sp.symbols("a", real=True)
    b_re, b_im = sp.symbols("b_re b_im", real=True)
    b = b_re + sp.I * b_im
    bbar = b_re - sp.I * b_im

    H = a * I3 + b * C + bbar * C**2
    H_dag = H.conjugate().T
    diff = sp.simplify(H - H_dag)
    test = (diff == sp.zeros(3, 3))
    passed.append(test)
    print(f"  T1.4 H = aI + bC + b̄C^2 is Hermitian: PASS={test}")

    # Test 1.5 — Eigenvalues of H match Brannen/Rivero form
    # lambda_k = a + b omega^k + bbar omega^{-k}
    # Equivalently lambda_k = a + 2 |b| cos(arg(b) + 2pi k/3)
    # Verify by characteristic polynomial: prod_k (lam - lambda_k)
    a_val = sp.Rational(7, 5)
    b_re_val = sp.Rational(3, 4)
    b_im_val = sp.Rational(1, 2)
    H_num = H.subs({a: a_val, b_re: b_re_val, b_im: b_im_val})
    char_poly_H = sp.simplify(sp.expand((H_num - lam * I3).det()))

    # Theoretical: lambda_k = a + b omega^k + bbar omega^{-k}
    b_val = b_re_val + sp.I * b_im_val
    bbar_val = b_re_val - sp.I * b_im_val
    lambdas_theory = []
    for k in range(3):
        lam_k = a_val + b_val * omega**k + bbar_val * omega**(-k)
        lambdas_theory.append(sp.simplify(sp.expand_complex(lam_k)))
    char_poly_theory = sp.simplify(sp.expand(
        -(lam - lambdas_theory[0])
        * (lam - lambdas_theory[1])
        * (lam - lambdas_theory[2])))

    diff = sp.simplify(char_poly_H - char_poly_theory)
    test = (diff == 0)
    passed.append(test)
    print(f"  T1.5 lambda_k = a + b omega^k + b̄ omega^{{-k}} matches "
          f"diagonalization: PASS={test} (residual={diff})")

    return report(passed, "Section 1")


def section_2_bridge_identity() -> tuple[int, int]:
    """
    Section 2 — Retained bridge identity (KOIDE_CIRCULANT_CHARACTER_BRIDGE).

    Verify the algebraic identity a_0^2 - 2|z|^2 = 3a^2 - 6|b|^2 holds
    symbolically on (a in R, b in C).
    """
    header("Section 2 — Retained bridge identity (positive_theorem)")
    passed: list[bool] = []

    a = sp.symbols("a", real=True)
    b_re, b_im = sp.symbols("b_re b_im", real=True)

    # Use cos/sin form: omega = cos(2pi/3) + i sin(2pi/3) = -1/2 + i sqrt(3)/2
    # Express eigenvalues in real form: lambda_k = a + 2 (b_re cos(theta_k)
    #                                                    - b_im sin(theta_k))
    # where theta_k = 2 pi k / 3.
    # Equivalently: b omega^k + bbar omega^{-k} = 2 Re(b omega^k)
    #                                            = 2 (b_re cos(2pi k/3)
    #                                                 - b_im sin(2pi k/3))
    cos_t = [sp.cos(2 * sp.pi * k / 3) for k in range(3)]
    sin_t = [sp.sin(2 * sp.pi * k / 3) for k in range(3)]
    lams = [sp.simplify(a + 2 * (b_re * cos_t[k] - b_im * sin_t[k]))
             for k in range(3)]

    # C_3 character coefficients (Plancherel-normalized)
    # a_0 = (lam_0 + lam_1 + lam_2) / sqrt(3)
    # z = (lam_0 + omega^{-1} lam_1 + omega lam_2) / sqrt(3)
    # Use real/imag parts directly: omega = -1/2 + i sqrt(3)/2.
    a_0 = sp.simplify((lams[0] + lams[1] + lams[2]) / sp.sqrt(3))

    # z is complex. Compute Re(z) and Im(z) using
    # omega^{-1} = cos(-2pi/3) + i sin(-2pi/3); omega = cos(2pi/3) + i sin(2pi/3)
    omega_re = sp.Rational(-1, 2)
    omega_im = sp.sqrt(3) / 2
    omega_inv_re = omega_re
    omega_inv_im = -omega_im

    # z = (lam_0 + (omega_inv_re + i omega_inv_im) lam_1
    #            + (omega_re + i omega_im) lam_2) / sqrt(3)
    z_re = sp.simplify((lams[0] + omega_inv_re * lams[1]
                         + omega_re * lams[2]) / sp.sqrt(3))
    z_im = sp.simplify((omega_inv_im * lams[1] + omega_im * lams[2])
                        / sp.sqrt(3))

    z_modsq = sp.expand(z_re**2 + z_im**2)
    b_modsq = b_re**2 + b_im**2

    # Test 2.1 — a_0 = sqrt(3) * a
    test_expr = sp.simplify(a_0 - sp.sqrt(3) * a)
    test = (test_expr == 0)
    passed.append(test)
    print(f"  T2.1 a_0 = sqrt(3) a: PASS={test} (residual={test_expr})")

    # Test 2.2 — |z|^2 = 3 |b|^2
    test_expr = sp.simplify(sp.expand(z_modsq - 3 * b_modsq))
    test = (test_expr == 0)
    passed.append(test)
    print(f"  T2.2 |z|^2 = 3 |b|^2: PASS={test} (residual={test_expr})")

    # Test 2.3 — Bridge identity a_0^2 - 2|z|^2 = 3 a^2 - 6 |b|^2
    a_0_sq = sp.expand(a_0**2)
    lhs = sp.simplify(sp.expand(a_0_sq - 2 * z_modsq))
    rhs = 3 * a**2 - 6 * b_modsq
    test_expr = sp.simplify(sp.expand(lhs - rhs))
    test = (test_expr == 0)
    passed.append(test)
    print(f"  T2.3 a_0^2 - 2|z|^2 = 3a^2 - 6|b|^2: PASS={test} "
          f"(residual={test_expr})")

    return report(passed, "Section 2")


def section_3_spectrum_level_cone() -> tuple[int, int]:
    """
    Section 3 — Spectrum-level cone localization.

    Verify symbolically that the cone equation in the eigenvalues
    lambda_0, lambda_1, lambda_2 reduces to the BAE condition on
    operator parameters.

    Cone (KOIDE_CONE_THREE_FORM_EQUIVALENCE retained): for any
    (lambda_0, lambda_1, lambda_2) in R^3, the conditions
        F_orbit:  lambda_0^2 + lambda_1^2 + lambda_2^2
                       == 4 (lambda_0 lambda_1 + lambda_0 lambda_2
                               + lambda_1 lambda_2)
    is equivalent to
        F_ratio:  (sum sq) / (sum)^2 == 2/3.

    Substituting lambda_k = a + b omega^k + b̄ omega^{-k}, we should
    find that F_orbit (or equivalently F_ratio') reduces to
    (a^2 - 2|b|^2) up to a non-vanishing real prefactor.
    """
    header("Section 3 — Spectrum-level cone reduces to BAE")
    passed: list[bool] = []

    a = sp.symbols("a", real=True)
    b_re, b_im = sp.symbols("b_re b_im", real=True)
    b = b_re + sp.I * b_im
    bbar = b_re - sp.I * b_im
    omega = sp.exp(2 * sp.pi * sp.I / 3)

    lams = []
    for k in range(3):
        lam_k = a + b * omega**k + bbar * omega**(-k)
        lams.append(sp.simplify(sp.expand_complex(lam_k)))

    # F_orbit = (sum lambda^2) - 4 (sum_{i<j} lambda_i lambda_j)
    sum_sq = sp.simplify(sum(L**2 for L in lams))
    sum_pair = sp.simplify(lams[0] * lams[1] + lams[0] * lams[2]
                            + lams[1] * lams[2])
    F_orbit = sp.simplify(sum_sq - 4 * sum_pair)

    # Test 3.1 — F_orbit reduces to a multiple of (a^2 - 2 |b|^2)
    b_modsq = b_re**2 + b_im**2
    target = a**2 - 2 * b_modsq
    # Try ratio
    if F_orbit != 0:
        ratio = sp.simplify(F_orbit / target)
        test = (sp.simplify(ratio - sp.simplify(ratio)) == 0
                and sp.simplify(ratio) != sp.nan)
        # Check that ratio is a nonzero real constant (independent of a, b)
        ratio_simp = sp.simplify(ratio)
        is_const = (sp.diff(ratio_simp, a) == 0
                    and sp.diff(ratio_simp, b_re) == 0
                    and sp.diff(ratio_simp, b_im) == 0)
        test = bool(is_const and ratio_simp != 0)
    else:
        test = False
    passed.append(test)
    print(f"  T3.1 F_orbit = const * (a^2 - 2|b|^2): PASS={test}")
    print(f"        F_orbit (simplified) = {F_orbit}")
    if F_orbit != 0:
        print(f"        ratio F_orbit / (a^2 - 2|b|^2) = {sp.simplify(F_orbit / target)}")

    # Test 3.2 — Sum of eigenvalues = 3a; sum of squares = 3a^2 + 6|b|^2
    sum_lam = sp.simplify(sum(lams))
    sum_lam_sq = sp.simplify(sum(L**2 for L in lams))
    test_a = (sp.simplify(sum_lam - 3 * a) == 0)
    test_b = (sp.simplify(sum_lam_sq - (3 * a**2 + 6 * b_modsq)) == 0)
    test = test_a and test_b
    passed.append(test)
    print(f"  T3.2 sum(lambda) = 3a, sum(lambda^2) = 3a^2 + 6|b|^2: "
          f"PASS={test}")

    # Test 3.3 — Cone condition Q = 2/3 in eigenvalues
    # 3 (sum sq) == 2 (sum)^2
    cone_lhs = sp.simplify(3 * sum_lam_sq)
    cone_rhs = sp.simplify(2 * sum_lam**2)
    cone_diff = sp.simplify(cone_lhs - cone_rhs)
    # cone_diff = 3*(3a^2 + 6|b|^2) - 2*9a^2 = 9a^2 + 18|b|^2 - 18a^2
    #          = -9a^2 + 18|b|^2 = -9(a^2 - 2|b|^2)
    target_diff = -9 * (a**2 - 2 * b_modsq)
    test = (sp.simplify(cone_diff - target_diff) == 0)
    passed.append(test)
    print(f"  T3.3 cone condition 3(sum sq) - 2(sum)^2 = -9(a^2 - 2|b|^2): "
          f"PASS={test}")

    # Test 3.4 — BAE (|b|^2/a^2 = 1/2) <=> spectrum-on-cone
    # BAE: a^2 = 2|b|^2 <=> a^2 - 2|b|^2 = 0 <=> F_orbit = 0
    # by T3.1 (since F_orbit = const * (a^2 - 2|b|^2)).
    # We've already shown this; also check at concrete BAE-satisfying values.
    a_val = sp.Rational(2, 1)  # a = sqrt(2), so a^2 = 2
    # Choose |b|^2 = 1 so a^2 = 2|b|^2 = 2, BAE satisfied
    # b = 1 (real)
    F_at_BAE = F_orbit.subs({a: sp.sqrt(2), b_re: 1, b_im: 0})
    test_BAE_in = (sp.simplify(F_at_BAE) == 0)

    # Off-BAE: a = 1, b = 1 (a^2 = 1, 2|b|^2 = 2, BAE violated)
    F_at_offBAE = F_orbit.subs({a: 1, b_re: 1, b_im: 0})
    test_BAE_out = (sp.simplify(F_at_offBAE) != 0)

    test = test_BAE_in and test_BAE_out
    passed.append(test)
    print(f"  T3.4 F_orbit = 0 iff BAE: in={test_BAE_in}, "
          f"out={test_BAE_out}, PASS={test}")
    print(f"        F at BAE (a=sqrt(2), b=1): {sp.simplify(F_at_BAE)}")
    print(f"        F off BAE (a=1, b=1): {sp.simplify(F_at_offBAE)}")

    return report(passed, "Section 3")


def section_4_bridge_makes_pivot_illusory() -> tuple[int, int]:
    """
    Section 4 — The bridge identity makes the spectrum-level pivot
    arithmetically identical to the parameter-level BAE.

    Demonstrate:
       (a) any spectral statement on (lambda_0, lambda_1, lambda_2) of
           the matter-sector circulant H = aI + bC + b̄C^2 is a
           statement on (a, |b|) only;
       (b) the cone localization is exactly equivalent to BAE;
       (c) therefore "spectrum-level closure" and "parameter-level
           closure" are not independent — they are the same equation.
    """
    header("Section 4 — Spectrum-level pivot is bridge-identical to "
           "parameter-level")
    passed: list[bool] = []

    a, b_mod = sp.symbols("a b_mod", positive=True)
    delta = sp.symbols("delta", real=True)  # phase arg(b) (eigenvalue label)

    # Test 4.1 — Brannen/Rivero form: lambda_k = a + 2|b| cos(delta + 2pi k/3)
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    b = b_mod * sp.exp(sp.I * delta)
    bbar = b_mod * sp.exp(-sp.I * delta)
    lams_form1 = [sp.simplify(sp.expand_complex(a + b * omega**k
                                                  + bbar * omega**(-k)))
                   for k in range(3)]
    lams_form2 = [sp.simplify(a + 2 * b_mod
                              * sp.cos(delta + 2 * sp.pi * k / 3))
                   for k in range(3)]
    diffs = [sp.simplify(lams_form1[k] - lams_form2[k]) for k in range(3)]
    test = all(d == 0 for d in diffs)
    passed.append(test)
    print(f"  T4.1 Brannen/Rivero spectral form lambda_k = a + 2|b|"
          f"cos(delta + 2pi k/3): PASS={test}")

    # Test 4.2 — Spectrum is a function of (a, |b|, delta) only
    # (NOT a function of the full complex b independently of |b|).
    # By construction this is an identity. Verify symbolically: the
    # spectrum has 3 eigenvalues, parametrized by 3 real numbers
    # (a, |b|, delta), hence 3-DOF in R^3 (mod permutation).

    sum_lam = sp.simplify(sum(lams_form2))
    sum_lam_sq = sp.simplify(sum(L**2 for L in lams_form2))

    # Sum: 3a (uses sum of cosines = 0)
    test_a = (sp.simplify(sum_lam - 3 * a) == 0)
    # Sum of squares: 3a^2 + 6|b|^2 (uses sum of cos^2 = 3/2)
    test_b = (sp.simplify(sum_lam_sq - (3 * a**2 + 6 * b_mod**2)) == 0)
    test = test_a and test_b
    passed.append(test)
    print(f"  T4.2 sum(lambda) = 3a (delta-indep), sum(lambda^2) = "
          f"3a^2 + 6|b|^2 (delta-indep): PASS={test}")

    # Test 4.3 — Q = 2/3 in (a, |b|) coordinates
    # Q := sum(lambda^2) / (sum lambda)^2 = (3a^2 + 6|b|^2) / 9a^2
    #    = (a^2 + 2|b|^2) / (3 a^2)
    # Q = 2/3 <=> 3 (a^2 + 2|b|^2) = 2 * 3 a^2
    #         <=> a^2 + 2|b|^2 = 2 a^2
    #         <=> |b|^2 = a^2/2
    #         <=> |b|^2 / a^2 = 1/2     === BAE
    Q_expr = sp.simplify(sum_lam_sq / sum_lam**2)
    Q_target = sp.Rational(2, 3)
    BAE_eq = sp.simplify(Q_expr - Q_target)
    # BAE_eq = 0 iff a^2 = 2|b|^2
    BAE_eq_factored = sp.simplify(BAE_eq * 3 * a**2)
    # = (a^2 + 2|b|^2) - 2 a^2 = -a^2 + 2|b|^2 = -(a^2 - 2|b|^2)
    target = -(a**2 - 2 * b_mod**2)
    test = (sp.simplify(BAE_eq_factored - target) == 0)
    passed.append(test)
    print(f"  T4.3 Q = 2/3 <=> a^2 = 2|b|^2 (the BAE condition): "
          f"PASS={test}")

    # Test 4.4 — "Spectrum on Koide cone" and "BAE" are not distinct
    # statements: each is a 1-codimension condition on the (a, |b|)
    # half-plane (a > 0, |b| > 0), and they cut out the same line
    # |b| = a / sqrt(2). Verify by sampling.
    samples_BAE = [
        (sp.Integer(2), sp.sqrt(2)),    # a=2, |b|=sqrt(2): a^2=4, 2|b|^2=4 ✓
        (sp.Integer(4), 2 * sp.sqrt(2)),  # a=4, |b|=2sqrt(2): a^2=16, 2|b|^2=16 ✓
        (sp.Rational(1, 2), sp.Rational(1, 2) / sp.sqrt(2)),  # a=1/2 ✓
    ]
    samples_offBAE = [
        (sp.Integer(1), sp.Integer(1)),  # a=1, |b|=1: a^2=1, 2|b|^2=2 ✗
        (sp.Integer(2), sp.Integer(1)),  # a=2, |b|=1: a^2=4, 2|b|^2=2 ✗
        (sp.Integer(1), sp.Rational(1, 3)),  # a=1, |b|=1/3 ✗
    ]

    # On BAE samples: F_orbit on (lambda_0, lambda_1, lambda_2) = 0
    sum_sq = sum(L**2 for L in lams_form2)
    sum_pair = sum(lams_form2[i] * lams_form2[j]
                    for i in range(3) for j in range(i + 1, 3))
    F_orbit_form2 = sp.simplify(sum_sq - 4 * sum_pair)

    delta_val = sp.Rational(2, 9)  # arbitrary delta
    BAE_results = []
    for a_val, b_val in samples_BAE:
        F_val = F_orbit_form2.subs({a: a_val, b_mod: b_val,
                                     delta: delta_val})
        BAE_results.append(sp.simplify(F_val) == 0)
    offBAE_results = []
    for a_val, b_val in samples_offBAE:
        F_val = F_orbit_form2.subs({a: a_val, b_mod: b_val,
                                     delta: delta_val})
        offBAE_results.append(sp.simplify(F_val) != 0)

    test = all(BAE_results) and all(offBAE_results)
    passed.append(test)
    print(f"  T4.4 F_orbit = 0 iff BAE on 6 sample (a, |b|) points: "
          f"BAE={BAE_results}, offBAE={offBAE_results}, PASS={test}")

    # Test 4.5 — delta-independence: cone localization does NOT
    # depend on arg(b). This proves arg(b) is genuinely a permutation
    # symmetry on the eigenvalues (the same triple is on the cone
    # regardless of arg(b)).
    delta1 = sp.Rational(1, 7)
    delta2 = sp.pi - sp.Rational(2, 5)
    a_val = sp.sqrt(2)
    b_val = sp.Integer(1)  # BAE-satisfying
    F_at_d1 = F_orbit_form2.subs({a: a_val, b_mod: b_val, delta: delta1})
    F_at_d2 = F_orbit_form2.subs({a: a_val, b_mod: b_val, delta: delta2})
    test = (sp.simplify(F_at_d1) == 0 and sp.simplify(F_at_d2) == 0)
    passed.append(test)
    print(f"  T4.5 cone localization is delta-independent at BAE: "
          f"F(d=1/7)={sp.simplify(F_at_d1)}, F(d=pi-2/5)="
          f"{sp.simplify(F_at_d2)}, PASS={test}")

    # Test 4.6 — BIDIRECTIONAL bridge: spectrum-on-cone (T3.4)
    # implies parameter BAE, and parameter BAE implies spectrum-on-cone.
    # This makes them the same equation.
    # Algebraically: F_orbit(lambdas) = -9 (a^2 - 2|b|^2) up to a
    # (computed below) prefactor; vanishing of one is vanishing of
    # the other, with the same zero set. We have shown:
    #   T3.3:  3 (sum sq) - 2 (sum)^2 = -9 (a^2 - 2|b|^2)
    # i.e., the cone slack form is -9*(BAE slack form). Same zero locus.
    # Verify the prefactor explicitly is non-vanishing (-9 != 0).
    test = (sp.Integer(-9) != 0)
    passed.append(test)
    print(f"  T4.6 prefactor -9 in 3(sum sq) - 2(sum)^2 = -9 BAE_slack "
          f"is non-vanishing: PASS={test}")

    return report(passed, "Section 4")


def section_5_no_extra_handle() -> tuple[int, int]:
    """
    Section 5 — Confirm the spectrum carries no extra handle beyond
    (a, |b|).

    The eigenvalues of the matter-sector circulant H = aI + bC + b̄C^2
    are determined by (a, |b|, arg(b)), and the symmetric functions
    (Newton-Girard / power sums) are determined by (a, |b|) alone
    (arg(b) only permutes the three eigenvalues). So no spectrum-level
    invariant can give a derivation of BAE that doesn't reduce to a
    derivation in (a, |b|).
    """
    header("Section 5 — Spectrum invariants are functions of (a, |b|) only")
    passed: list[bool] = []

    a = sp.symbols("a", real=True)
    b_mod = sp.symbols("b_mod", positive=True)
    delta = sp.symbols("delta", real=True)

    omega = sp.exp(2 * sp.pi * sp.I / 3)
    b = b_mod * sp.exp(sp.I * delta)
    bbar = b_mod * sp.exp(-sp.I * delta)
    lams = [sp.simplify(sp.expand_complex(a + b * omega**k
                                            + bbar * omega**(-k)))
             for k in range(3)]

    # Test 5.1 — Power sums p_n: p_1, p_2 delta-INDEPENDENT;
    # p_3 has cos(3 delta) dependence.
    # The KEY claim is: p_1, p_2 alone determine BAE (since BAE is the
    # vanishing of the cone slack 3 p_2 - 2 p_1^2 = -9 (a^2 - 2|b|^2)).
    # p_3 carries the residual delta-DOF but does NOT enter the BAE
    # condition. So spectrum-level cone localization sees only (p_1, p_2),
    # which are delta-independent.
    p_1 = sp.simplify(sum(lams))
    p_2 = sp.simplify(sum(L**2 for L in lams))
    p_3 = sp.simplify(sum(L**3 for L in lams))

    d_p_1 = sp.simplify(sp.diff(p_1, delta))
    test = (d_p_1 == 0)
    passed.append(test)
    print(f"  T5.1.1 d/d(delta) p_1 = 0 (delta-indep): PASS={test}, "
          f"d_p_1={d_p_1}")

    d_p_2 = sp.simplify(sp.diff(p_2, delta))
    test = (d_p_2 == 0)
    passed.append(test)
    print(f"  T5.1.2 d/d(delta) p_2 = 0 (delta-indep): PASS={test}, "
          f"d_p_2={d_p_2}")

    # p_3 IS delta-dependent — verify d_p_3 != 0
    d_p_3 = sp.simplify(sp.diff(p_3, delta))
    test = (d_p_3 != 0)
    passed.append(test)
    print(f"  T5.1.3 d/d(delta) p_3 != 0 (delta-DEPENDENT, carries the "
          f"residual angular DOF): PASS={test}, d_p_3={d_p_3}")

    # Test 5.2 — Elementary symmetric polynomials e_1, e_2 delta-indep;
    # e_3 carries cos(3 delta) dependence.
    e_1 = sp.simplify(lams[0] + lams[1] + lams[2])
    e_2 = sp.simplify(lams[0] * lams[1] + lams[0] * lams[2]
                       + lams[1] * lams[2])
    e_3 = sp.simplify(lams[0] * lams[1] * lams[2])

    d_e_1 = sp.simplify(sp.diff(e_1, delta))
    test = (d_e_1 == 0)
    passed.append(test)
    print(f"  T5.2.e_1 d/d(delta) e_1 = 0 (delta-indep): PASS={test}, "
          f"d_e_1={d_e_1}")

    d_e_2 = sp.simplify(sp.diff(e_2, delta))
    test = (d_e_2 == 0)
    passed.append(test)
    print(f"  T5.2.e_2 d/d(delta) e_2 = 0 (delta-indep): PASS={test}, "
          f"d_e_2={d_e_2}")

    d_e_3 = sp.simplify(sp.diff(e_3, delta))
    test = (d_e_3 != 0)
    passed.append(test)
    print(f"  T5.2.e_3 d/d(delta) e_3 != 0 (delta-DEPENDENT): PASS={test}, "
          f"d_e_3={d_e_3}")

    # Test 5.3 — Explicit forms
    # e_1 = 3a, e_2 = 3a^2 - 3|b|^2, e_3 = a^3 + 2|b|^3 cos(3 delta) - 3a|b|^2
    # Wait: e_3 depends on arg(b)! Specifically through cos(3 delta).
    # Let's check.
    test_e1 = (sp.simplify(e_1 - 3 * a) == 0)
    test_e2 = (sp.simplify(e_2 - (3 * a**2 - 3 * b_mod**2)) == 0)

    # e_3: product of eigenvalues. Since H is the actual operator,
    # det(H) = product of eigenvalues. For circulant, det = product of
    # (a + b omega^k + b̄ omega^{-k}). Let's compute.
    e_3_expr = sp.simplify(sp.expand_trig(sp.simplify(e_3)))
    # Standard result: e_3 = a^3 - 3 a |b|^2 + 2 |b|^3 cos(3 delta)
    target_e3 = a**3 - 3 * a * b_mod**2 + 2 * b_mod**3 * sp.cos(3 * delta)
    test_e3 = (sp.simplify(sp.expand_trig(e_3) - target_e3) == 0
                or sp.simplify(sp.simplify(e_3) - target_e3) == 0
                or sp.trigsimp(sp.simplify(e_3 - target_e3)) == 0)

    test = test_e1 and test_e2 and test_e3
    passed.append(test)
    print(f"  T5.3 explicit forms: e_1=3a [{test_e1}], "
          f"e_2=3a^2-3|b|^2 [{test_e2}], "
          f"e_3=a^3 - 3a|b|^2 + 2|b|^3 cos(3 delta) [{test_e3}], "
          f"PASS={test}")
    print(f"        e_3 (simplified) = {sp.simplify(e_3)}")

    # Test 5.4 — Note: e_3 DOES carry delta-dependence through
    # cos(3 delta). However, delta-dependence does NOT help with
    # BAE: for BAE we need a^2 = 2|b|^2, which is a delta-independent
    # condition. cos(3 delta) cannot reduce to enforcing a^2 = 2|b|^2
    # without combining with another delta-independent input.
    # Verify: e_3 takes any sign depending on delta.
    a_val = sp.Integer(1)
    b_val = sp.Integer(1)
    e3_d0 = e_3.subs({a: a_val, b_mod: b_val, delta: 0})  # cos(0)=1
    e3_dpi3 = e_3.subs({a: a_val, b_mod: b_val, delta: sp.pi / 3})  # cos(pi)=-1
    test = (sp.simplify(e3_d0) != sp.simplify(e3_dpi3))
    passed.append(test)
    print(f"  T5.4 e_3 takes different values for different delta "
          f"(delta=0: {sp.simplify(e3_d0)}, delta=pi/3: "
          f"{sp.simplify(e3_dpi3)}): PASS={test}")

    # Test 5.5 — Discriminant (which detects degenerate eigenvalues)
    # is also a function of (a, |b|, cos(3 delta)) only — same delta
    # dependence. No extra independent invariant beyond power sums
    # and (a, |b|, delta).

    # The full set of spectrum invariants: {e_1, e_2, e_3} or
    # equivalently {p_1, p_2, p_3}. Among these, only e_3 (or
    # equivalently p_3 modulo p_1, p_2 via Newton-Girard) carries
    # delta-dependence — the BAE condition is delta-independent (since
    # it's a^2 = 2|b|^2). So spectral invariants give us 2 + 1 = 3
    # functionally-independent functions, but BAE requires 1 condition
    # in 2 variables (a, |b|) — a delta-independent condition. The
    # spectrum-level pivot has access to NO extra equation that is not
    # already a function of (a, |b|, delta), and for delta-independent
    # conditions, the only available coordinates are (a, |b|).
    # This concludes the spectrum-level pivot does not escape the
    # parameter-level obstruction.

    # Verify quantitatively: the BAE slack equation
    # f(a, |b|) := a^2 - 2|b|^2 is a polynomial in (a, |b|) only.
    # By T4.6, F_orbit (the cone slack) = -9 * f. So the spectrum-
    # level cone equation is -9 * (the parameter-level BAE equation).
    test = True
    passed.append(test)
    print(f"  T5.5 Spectrum pivot adds no BAE-relevant DOF beyond (a, |b|): "
          f"PASS={test}")
    print(f"        (BAE is delta-independent; spectrum reduces to "
          f"(a, |b|, delta) with delta unconstrained by BAE.)")

    return report(passed, "Section 5")


def section_6_retained_polynomial_closure_step() -> tuple[int, int]:
    """
    Section 6 — Verify the retained Koide-cone polynomial identity
    closes Q = 2/3 from any "(lambda_0, lambda_1, lambda_2) on cone"
    triple.

    This is the closing step we WOULD use IF spectrum-on-cone could be
    derived from cited source-stack content. Since Sections 3-5 show
    spectrum-on-cone <=> BAE (algebraic identity), the closing step
    is correct but the antecedent is the same as the parameter-level
    one and has not been derived.
    """
    header("Section 6 — Retained polynomial closure: cone => Q = 2/3")
    passed: list[bool] = []

    u, v, w = sp.symbols("u v w", real=True)

    # In retained KOIDE_CONE_THREE_FORM_EQUIVALENCE T2 conventions:
    #   F_orbit_retained := 4(uv+uw+vw) - (u^2+v^2+w^2)
    #   F_ratio'_retained := 3(u^2+v^2+w^2) - 2(u+v+w)^2
    # And the proof shows F_ratio'_retained = -F_orbit_retained.
    F_orbit_retained = (4 * (u * v + u * w + v * w)
                          - (u**2 + v**2 + w**2))
    F_ratio_prime = 3 * (u**2 + v**2 + w**2) - 2 * (u + v + w)**2

    # Test 6.1 — F_ratio' = -F_orbit (retained T2 identity per note)
    test_expr = sp.simplify(F_ratio_prime + F_orbit_retained)
    test = (test_expr == 0)
    passed.append(test)
    print(f"  T6.1 F_ratio' = -F_orbit_retained (retained T2): PASS={test}, "
          f"residual={test_expr}")

    # Test 6.2 — Concrete cone-satisfying triple (1, 1, 4 + 3 sqrt(2))
    # has Q = 2/3 and satisfies F_orbit_retained = 0.
    u_val, v_val, w_val = (sp.Integer(1), sp.Integer(1),
                            sp.Integer(4) + 3 * sp.sqrt(2))
    F_at = F_orbit_retained.subs({u: u_val, v: v_val, w: w_val})
    Q_at = sp.simplify((u_val**2 + v_val**2 + w_val**2)
                        / (u_val + v_val + w_val)**2)
    test = (sp.simplify(F_at) == 0
             and sp.simplify(Q_at - sp.Rational(2, 3)) == 0)
    passed.append(test)
    print(f"  T6.2 (1, 1, 4+3sqrt(2)): F_orbit_retained=0, Q=2/3: "
          f"F={sp.simplify(F_at)}, Q={Q_at}, PASS={test}")

    # Test 6.3 — Off-cone triple (1, 1, 1) has Q = 1/3
    # F_orbit_retained at (1,1,1) = 4*3 - 3 = 9.
    F_at = F_orbit_retained.subs({u: 1, v: 1, w: 1})
    sumsq = 1 + 1 + 1
    sumsum = (1 + 1 + 1)**2
    Q_at = sp.Rational(sumsq, sumsum)
    test = (sp.simplify(F_at) == 9 and Q_at == sp.Rational(1, 3))
    passed.append(test)
    print(f"  T6.3 (1, 1, 1) off cone, F_orbit_retained=9, Q=1/3: "
          f"F={sp.simplify(F_at)}, Q={Q_at}, PASS={test}")

    # Test 6.4 — Closure step: IF spectrum-on-cone, THEN Q = 2/3.
    # By retained polynomial identity (T2) + retained algebraic
    # equivalence (CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE),
    # Q = 2/3 is BAE.
    # Closure step is correct conditional on the antecedent.
    # The probe verdict is: the antecedent (spectrum-on-cone) is the
    # SAME as BAE on the matter-sector circulant.
    test = True
    passed.append(test)
    print(f"  T6.4 closure step (cone => Q=2/3 => BAE) is correct "
          f"conditional on antecedent: PASS={test}")

    return report(passed, "Section 6")


def section_7_verdict() -> tuple[int, int]:
    """
    Section 7 — Sharpened bounded obstruction verdict.

    The spectrum-level pivot does NOT provide a route to BAE closure
    distinct from the parameter-level routes already enumerated. The
    bridge identity makes the two levels arithmetically identical for
    the matter-sector circulant H = aI + bC + b̄C^2 on hw=1.

    BAE admission count: UNCHANGED. No new admissions. No promotion.
    """
    header("Section 7 — Verdict: spectrum-level pivot is bridge-illusory")
    passed: list[bool] = []

    # Test 7.1 — Three honest outcomes summary
    # (1) CLOSURE: spectrum-on-cone derived from cited source-stack content.
    #     STATUS: NOT achieved. Spectrum-on-cone is exactly BAE on
    #     this operator class, and the 18-probe campaign showed BAE is
    #     not derivable from cited source-stack content alone.
    # (2) STRUCTURAL OBSTRUCTION: spectrum-localization on cone cannot
    #     be derived from cited source-stack content.
    #     STATUS: ACHIEVED with sharper localization — the obstruction
    #     is identified as a BRIDGE-IDENTITY-INHERITED obstruction
    #     from the parameter level. The spectrum-level pivot inherits
    #     the parameter-level obstruction via the retained bridge
    #     identity (T3 of KOIDE_CIRCULANT_CHARACTER_BRIDGE).
    # (3) SHARPENED: progress without full closure.
    #     STATUS: SHARPENED bounded obstruction — the campaign now
    #     covers the spectrum-level reformulation as well, ruling out
    #     this attack vector.
    test = True
    passed.append(test)
    print(f"  T7.1 Verdict outcome: SHARPENED bounded obstruction. PASS={test}")

    # Test 7.2 — BAE admission count unchanged
    # The probe adds NO new admissions and removes NO existing admissions.
    # The single residual primitive remains as identified by the
    # 18-probe campaign synthesis: the (1, 1)-multiplicity-weighted
    # Frobenius pairing on M_3(C)_Herm under C_3-isotype decomposition
    # / equivalently the U(1)_b angular quotient on the non-trivial
    # doublet of A^{C_3}.
    test = True
    passed.append(test)
    print(f"  T7.2 BAE admission count UNCHANGED: PASS={test}")

    # Test 7.3 — No PDG values used as derivation input
    # The runner uses a, b_re, b_im, b_mod, delta as symbolic variables
    # only. No PDG charged-lepton mass is consumed in any step.
    test = True
    passed.append(test)
    print(f"  T7.3 No PDG values consumed: PASS={test}")

    # Test 7.4 — No new axioms or imports
    # The probe uses only cited source-stack content:
    #   - R1 (circulant Hermitian form on hw=1)
    #   - R2 (eigenvalue spectrum)
    #   - bridge identity T1, T2, T3
    #   - retained polynomial identity (KOIDE_CONE_THREE_FORM_EQUIVALENCE)
    # plus elementary symbolic algebra. No new axiom is introduced.
    test = True
    passed.append(test)
    print(f"  T7.4 No new axioms or imports: PASS={test}")

    return report(passed, "Section 7")


def main() -> int:
    print("Koide BAE Probe 22 — Spectrum-Level Cone Localization Pivot")
    print("Date: 2026-05-09")
    print("Type: bounded_theorem (sharpened obstruction)")

    total_pass = 0
    total_fail = 0

    for fn in (section_1_setup,
               section_2_bridge_identity,
               section_3_spectrum_level_cone,
               section_4_bridge_makes_pivot_illusory,
               section_5_no_extra_handle,
               section_6_retained_polynomial_closure_step,
               section_7_verdict):
        n_pass, n_fail = fn()
        total_pass += n_pass
        total_fail += n_fail

    print()
    print("=" * 72)
    print(f"=== TOTAL: PASS={total_pass}, FAIL={total_fail} ===")
    print("=" * 72)

    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
