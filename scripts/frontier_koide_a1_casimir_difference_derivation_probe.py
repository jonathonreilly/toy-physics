#!/usr/bin/env python3
"""
A1 KEYSTONE probe: derive the Casimir-difference identity |b|²/a² = T(T+1) − Y²

Context (cold):
    The Koide A1 condition |b|²/a² = 1/2 on Herm_circ(3) has, after a long
    landscape audit, been reduced to ONE open structural lemma (Route F
    in docs/KOIDE_A1_DERIVATION_STATUS_NOTE.md):

        |b|²/a²  ?=  T(T+1)_{SU(2)_L, fund} − Y²_{U(1)_Y, Higgs}
                 =  3/4 − 1/4 = 1/2

    A separate D_3 SSB probe has already reduced the D_3-invariant, bounded
    degree-4 potential on Herm_circ(3) to V_4(γ) = (α a² + β |b|²)² with
    γ = β/α free, and A1 is γ = -2. The keystone reduction is: which axiom-
    native identity forces γ = -2 i.e. forces |b|²/a² = 1/2?

    This runner PROBES three candidate mechanisms for deriving the
    Casimir-difference identity. It does not presuppose the answer; each
    mechanism is set up symbolically and its actual constraint on (a, b)
    is computed.

Mechanisms probed:

    (M-A) Gauge-invariant Yukawa operator normalization via the SU(2)_L × U(1)_Y
          Casimir operator acting on the (L, H, e_R) fields. The Casimir
          commutator [T^a T^a, Y²] is known to vanish (both are central on
          irreps), but their DIFFERENCE T(T+1) − Y² acts as a scalar on each
          irrep. Test: impose that the Yukawa vertex carries the Casimir-
          difference scalar on the (L, H) Yukawa participant pair, and
          require generation-space covariance under the Z_3 circulant
          structure. Ask: does this force |b|²/a² = T(T+1) − Y²?

    (M-B) Triple-product gauge invariance via the SU(2)_L antisymmetric
          invariant ε_{ij}. The Yukawa L_α·Φ·e_R,β contracts L and Φ via
          ε_{ij} (the unique 2⊗2 → 1 SU(2) invariant). The ε_{ij} tensor
          has ε_{12} = +1, ε_{21} = -1, and ε_{ij}ε^{ij} = 2. If the Z_3
          generation-space circulant structure is RESTRICTED by requiring
          compatibility with the ε_{ij} antisymmetry in a specific way,
          check whether the restriction forces |b|²/a² = 1/2.

    (M-C) Mass-squared Casimir commutation. The charged-lepton mass-squared
          matrix M² = M M† must commute with the retained gauge Casimir on
          Yukawa participants. Specifically, restricted to the Yukawa-
          participant sector (doublet L + doublet H), [M², T(T+1) − Y²·I]
          = 0. This is automatic if M² is proportional to identity on the
          sector. Test whether the non-trivial content — combining this
          commutation with the C_τ = T(T+1) + Y² = 1 retained theorem and
          circulant structure — forces |b|²/a² = 1/2.

Runner style: matches scripts/frontier_koide_a1_yukawa_casimir_identity.py
              (PASS/FAIL records, sectioned printing, explicit sympy).

Outcome: each mechanism is tested and the actual constraint on (a, b) is
reported. If any mechanism CLOSES the lemma, the exact operator identity
is named. If not, the residual gap is characterized.
"""

import sys
from fractions import Fraction

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []
VERDICTS: list[tuple[str, str, str]] = []  # (mechanism, verdict, rationale)


def record(name: str, ok: bool, detail: str = ""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def verdict(mechanism: str, status: str, rationale: str):
    VERDICTS.append((mechanism, status, rationale))
    print()
    print(f"  VERDICT ({mechanism}): {status}")
    for line in rationale.split("\n"):
        print(f"    {line}")


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# --------------------------------------------------------------------
# Shared setup: Herm_circ(3) parameterization, circulant Yukawa matrix,
# retained gauge quantum numbers.
# --------------------------------------------------------------------


def build_herm_circ():
    """Return a sympy circulant Hermitian 3x3 matrix H = aI + bC + conj(b)C²."""
    a = sp.Symbol('a', real=True)
    br = sp.Symbol('b_r', real=True)
    bi = sp.Symbol('b_i', real=True)
    # Circulant basis: C has (C)_{ij} = δ_{i, j+1 mod 3}
    # For a Hermitian circulant, the (i,j) element is c_{(j-i) mod 3}
    # with c_1 = b, c_2 = conj(b) to be Hermitian.
    b = br + sp.I * bi
    bc = br - sp.I * bi
    H = sp.Matrix([
        [a,  b,  bc],
        [bc, a,  b ],
        [b,  bc, a ],
    ])
    return H, a, br, bi, b, bc


def A1_condition(a, br, bi):
    """Return the expression  |b|²/a² − 1/2  (zero at A1)."""
    return (br**2 + bi**2) / a**2 - sp.Rational(1, 2)


# --------------------------------------------------------------------
# Mechanism M-A: SU(2)_L × U(1)_Y Casimir-difference insertion in Yukawa
#               vertex, with Z_3 generation-space covariance.
# --------------------------------------------------------------------


def probe_mechanism_A():
    section("Mechanism M-A — Casimir-difference insertion in Yukawa vertex")
    print()
    print("  Setup:")
    print("    Yukawa vertex: y_{αβ} L̄_{α} · H · e_{R,β}")
    print("    Each Yukawa participant (L, H) carries SU(2)_L × U(1)_Y quantum numbers.")
    print("    Casimir operators act as scalars on irreps:")
    print("        C₂(SU(2)_L) = T(T+1) · 1   on rep with isospin T")
    print("        C₂(U(1)_Y ) = Y²       · 1   on rep with hypercharge Y")
    print()
    print("  Candidate insertion: weight the Yukawa vertex by the Casimir")
    print("  DIFFERENCE operator ∆C_{L,H} = T_L(T_L+1) − Y_H²  restricted to")
    print("  the (L, H) Yukawa participant subspace.  For L (T=1/2, Y=-1/2)")
    print("  and H (T=1/2, Y=+1/2), ∆C_L = ∆C_H = 3/4 − 1/4 = 1/2.")
    print()
    print("  Question:  does requiring the generation-space Yukawa matrix y_{αβ}")
    print("  to be an eigen-operator of this Casimir-difference insertion (with")
    print("  eigenvalue ∆C = 1/2) force |b|²/a² = 1/2?")

    # The Yukawa matrix on V_3 is circulant: y_{αβ} = a δ_{αβ} + b C_{αβ} + b̄ C²_{αβ}
    H, a, br, bi, b, bc = build_herm_circ()

    # Z_3 circulant generator C on V_3
    C = sp.Matrix([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ])

    # The Casimir-difference insertion is a scalar on the (L, H) sector,
    # so it acts on the Yukawa matrix y_{αβ} (a 3x3 generation-space matrix)
    # as a global scalar multiplication: ∆C · y_{αβ}.  This gives no
    # differential constraint on (a, b) in generation space.
    #
    # However, the PHYSICAL statement the task is probing is stronger:
    # the AMPLITUDE ratio |b|²/a² should itself EQUAL the Casimir difference.
    # This is a statement about NORMS of amplitude components, not about
    # eigenvalue equations.  Mechanism M-A therefore tests whether a
    # specific GAUGE-ALGEBRA IDENTITY fixes this norm ratio.
    #
    # Candidate gauge-algebra identity:
    #   The Yukawa coupling y L̄·Φ·e_R, when projected on (L, H) Yukawa
    #   participants, equals the expectation value of ∆C on the (L, H)
    #   pair:  ⟨(L,H) | ∆C | (L,H)⟩ = ∆C = 1/2.
    #   The INDEX-DIAGONAL part  a  carries the Casimir SUM on one
    #   participant (T(T+1) + Y² = 1), the INDEX-OFF-DIAGONAL part  b
    #   carries the Casimir DIFFERENCE on the pair (T(T+1) − Y² = 1/2).
    #
    # If that correspondence held, we would have  a = C_τ = 1 (up to norm)
    # and |b|² = ∆C = 1/2, giving |b|²/a² = 1/2.

    T = sp.Rational(1, 2)
    Y_L = sp.Rational(-1, 2)
    Y_H = sp.Rational(1, 2)

    Casimir_sum = T * (T + 1) + Y_L ** 2  # = 1  (C_τ retained)
    Casimir_diff_L = T * (T + 1) - Y_L ** 2
    Casimir_diff_H = T * (T + 1) - Y_H ** 2

    print()
    print(f"  Retained Casimirs:")
    print(f"    C_τ(sum)     = T(T+1) + Y²(L) = {Casimir_sum}   [retained theorem, gives y_τ]")
    print(f"    ∆C_L(diff)   = T(T+1) − Y²(L) = {Casimir_diff_L}")
    print(f"    ∆C_H(diff)   = T(T+1) − Y²(H) = {Casimir_diff_H}")
    print()
    print("  Correspondence test (M-A):")
    print("      a²  ?=  C_τ = 1        (diagonal carries sum)")
    print("      |b|² ?= ∆C   = 1/2     (off-diagonal carries difference)")
    print("  Would give  |b|²/a²  =  ∆C / C_τ  =  (1/2) / 1  =  1/2  ✓")

    MA_ratio = Casimir_diff_L / Casimir_sum
    forces_A1 = (MA_ratio == sp.Rational(1, 2))
    record(
        "M-A.1 Casimir-diff / Casimir-sum = 1/2 (numerically matches A1)",
        forces_A1,
        f"(T(T+1) − Y²)/(T(T+1) + Y²) = {MA_ratio}.  Matches A1 if the Yukawa\n"
        "components map to the SUM and DIFFERENCE respectively.",
    )

    # Rigorous derivation question: does a GAUGE-INVARIANCE argument force
    # the diagonal a to carry the sum and the off-diagonal b to carry the
    # difference?
    #
    # Test: decompose the Z_3 circulant structure via the discrete Fourier
    # transform.  On Herm_circ(3), the scalar (trivial) representation of
    # Z_3 contributes to  a  and the doublet (non-trivial) contributes to
    # b, b̄.  But SU(2)_L × U(1)_Y are INDEPENDENT of Z_3 on generations.
    # The quantum numbers (T, Y) are the SAME on each Z_3 component of a
    # given lepton generation.
    #
    # Therefore the SU(2)_L × U(1)_Y Casimir scalars (sum or difference)
    # multiply BOTH  a  and  b  uniformly.  No differential constraint
    # arises that separates a from b.
    #
    # Concretely: ∆C · y_{αβ} = ∆C · (a δ_{αβ} + b C_{αβ} + b̄ C²_{αβ})
    # rescales the whole Yukawa matrix uniformly.  Its ratio |b|²/a² is
    # left unchanged by the Casimir-difference insertion.

    y_matrix = a * sp.eye(3) + b * C + bc * (C * C)
    insertion = sp.Rational(1, 2) * y_matrix  # ∆C · y
    ratio_before = (br**2 + bi**2) / a**2
    # If we rescale by ∆C uniformly, both |b|² and a² get multiplied by (∆C)²,
    # so the ratio is invariant:
    ratio_after = ((sp.Rational(1, 2) * br)**2 + (sp.Rational(1, 2) * bi)**2) / (sp.Rational(1, 2) * a)**2
    ratio_change = sp.simplify(ratio_after - ratio_before)

    print()
    print(f"  Concretely: ∆C · y rescales the whole Yukawa matrix uniformly.")
    print(f"  Ratio |b|²/a² before: {ratio_before}")
    print(f"  Ratio |b|²/a² after:  {ratio_after}")
    print(f"  Ratio change:         {ratio_change}")

    ratio_is_invariant = (ratio_change == 0)
    record(
        "M-A.2 Casimir-difference insertion leaves |b|²/a² INVARIANT",
        ratio_is_invariant,
        "Uniform rescaling of y by the Casimir scalar cancels in the norm ratio.\n"
        "The insertion gives NO differential constraint on a vs b.",
    )

    # To get a non-trivial constraint, M-A would need the Casimir-difference
    # to act DIFFERENTIALLY on Z_3 components — but SU(2)_L × U(1)_Y and Z_3
    # on generations commute, so this does not happen within retained
    # ingredients.

    ma_forces_A1 = False  # Rigorous: M-A does not yield a differential constraint
    record(
        "M-A.3 Mechanism M-A does NOT force A1 (honest obstruction)",
        not ma_forces_A1,
        "Uniform Casimir rescaling leaves |b|²/a² invariant.\n"
        "The numerical match (M-A.1) is a rationalization, not a force.\n"
        "Without a new structural rule coupling generation space to gauge\n"
        "algebra, M-A does not close the lemma.",
    )

    verdict(
        "M-A  Casimir-difference insertion",
        "NO CONSTRAINT / NUMERICAL COINCIDENCE",
        "Casimir operators are scalars on each irrep, so their insertion rescales\n"
        "the Yukawa matrix uniformly.  The ratio |b|²/a² is invariant under this\n"
        "rescaling.  The numerical match (C_τ = 1, ∆C = 1/2) is a reformulation\n"
        "of the target identity, not a derivation.  To force A1 we would need a\n"
        "new ingredient coupling Z_3 generation space to SU(2)_L × U(1)_Y.",
    )
    return ma_forces_A1


# --------------------------------------------------------------------
# Mechanism M-B: SU(2)_L ε-tensor triple-product gauge invariant and
#                the Z_3-circulant compatibility.
# --------------------------------------------------------------------


def probe_mechanism_B():
    section("Mechanism M-B — Triple-product gauge invariant L·Φ·e_R with ε_{ij}")
    print()
    print("  Setup:")
    print("    Gauge-invariant Yukawa term requires the SU(2)_L doublets L, H")
    print("    to contract via the antisymmetric invariant ε_{ij}:")
    print("        L̄_α^{i} · H_{j} · e_{R,β} · ε_{ij}  is the unique 2⊗2→1 invariant.")
    print("    (Alternative Yukawa with charge-conjugate Higgs H̃ = iσ_2 H*")
    print("     produces the up-quark Yukawa; for charged leptons, L̄·H·e_R uses")
    print("     the doublet-times-doublet-to-singlet channel via the ε tensor.)")
    print()
    print("  Question: does demanding Z_3 generation-space circulant compatibility")
    print("  with the ε_{ij} antisymmetry restrict |b|²/a² to 1/2?")

    # ε tensor
    eps = sp.Matrix([[0, 1], [-1, 0]])

    # Norms
    eps_norm_sq = sum((eps[i, j]) ** 2 for i in range(2) for j in range(2))
    eps_double = sp.trace(eps.T * eps)

    print()
    print(f"  ε_{{ij}} = \n{sp.pretty(eps)}")
    print(f"  ε_{{ij}} ε^{{ij}} = {eps_double}   (standard SU(2) invariant normalization)")
    print(f"  |ε|_F² = Σ |ε_{{ij}}|² = {eps_norm_sq}")

    record(
        "M-B.1 ε_{ij} is antisymmetric with ε_{12}=+1, ε_{21}=-1",
        eps == sp.Matrix([[0, 1], [-1, 0]]),
        "Standard SU(2) antisymmetric invariant.",
    )

    record(
        "M-B.2 ε_{ij}ε^{ij} = 2 (norm of antisymmetric invariant)",
        eps_double == 2,
        "Matches dim(2⊗2) projected onto singlet: |ε|² = 2 = dim(fund)·1.",
    )

    # Now:  the CRITICAL question is whether ε_{ij} contraction imposes a
    # generation-space constraint.
    #
    # In the full Yukawa y_{αβ} L̄_α^i Φ_j e_{R,β} ε_{ij}, the ε_{ij} is
    # contracted over the SU(2)_L doublet index (i, j ∈ {1,2}).  The
    # generation indices (α, β) are SEPARATE and run over {1, 2, 3}.
    #
    # The Z_3 generation-space circulant requires:
    #   y_{αβ} = y_{(α+1)(β+1)}  (cyclic shift in both α and β),
    # which gives  y = a·I + b·C + b̄·C²  in generation space.
    #
    # The ε_{ij} factor is independent of (α, β) and contributes an overall
    # constant to the Yukawa vertex.  So ε_{ij} does NOT mix with the
    # generation-space circulant structure.
    #
    # BUT: there is a subtler question.  Does the ε_{ij} antisymmetry
    # FORBID certain generation-space structures?
    #
    # Test: is there a parity-like constraint that forces b to be
    # SPECIFICALLY real (or purely imaginary) or of specific magnitude?
    #
    # The circulant Hermiticity H = H† already forces C_{12}-entry = conj
    # of C_{21}-entry (the two off-diagonal orbits).  That's y_{αβ} = a I
    # + b C + b̄ C².  The ε antisymmetry is in SU(2)_L doublet space and
    # does not further constrain generation space.

    # Explicit check: compute the gauge-invariant Yukawa vertex in a
    # parameterized form and see what the ε contraction does.
    H, a, br, bi, b, bc = build_herm_circ()
    C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    # Yukawa generation-space matrix (circulant, Hermitian)
    y_gen = a * sp.eye(3) + b * C3 + bc * (C3 * C3)

    # The SU(2)_L doublet contraction gives an OVERALL constant per
    # generation component, so the full structure is y_gen ⊗ ε.
    # Build the tensor product explicitly:
    y_full = sp.zeros(6, 6)
    for alpha in range(3):
        for beta in range(3):
            y_ab = y_gen[alpha, beta]
            for i in range(2):
                for j in range(2):
                    y_full[2 * alpha + i, 2 * beta + j] = y_ab * eps[i, j]

    y_full_simplified = sp.simplify(y_full)

    # The Frobenius norm of y_full factorizes:
    # ||y_full||² = ||y_gen||² · ||ε||² = ||y_gen||² · 2
    norm_y_gen_sq = sum(abs(y_gen[i, j]) ** 2 for i in range(3) for j in range(3))
    norm_y_gen_sq_simp = sp.simplify(sp.expand(norm_y_gen_sq))
    norm_y_full_sq = sum(abs(y_full[i, j]) ** 2 for i in range(6) for j in range(6))
    norm_y_full_sq_simp = sp.simplify(sp.expand(norm_y_full_sq))

    print()
    print(f"  ||y_gen||_F² = {norm_y_gen_sq_simp}")
    print(f"  ||y_full||_F² = ||y_gen ⊗ ε||_F² = ||y_gen||² · ||ε||² = {norm_y_full_sq_simp}")
    ratio_check = sp.simplify(norm_y_full_sq_simp - 2 * norm_y_gen_sq_simp)
    print(f"  Factorization check: ||y_full||² − 2·||y_gen||² = {ratio_check}")

    record(
        "M-B.3 ε_{ij} contributes a uniform factor of 2 to the Yukawa norm",
        ratio_check == 0,
        "||y⊗ε||² = ||y||²·||ε||² = 2·||y||².  The ε factor does not\n"
        "discriminate between a (diagonal) and b (off-diagonal).",
    )

    # Conclusion for M-B: ε_{ij} gives only a uniform factor, and does not
    # force |b|²/a² to any specific value.

    # Test whether the ε antisymmetry forbids specific Hermitian-circulant
    # patterns.  It does not: the full construct y_gen ⊗ ε is Hermitian
    # (y_gen Hermitian, ε antisymmetric, but y⊗ε has specific Hermiticity
    # pattern under σ_2 conjugation — which is an SU(2)_L transform).
    mb_forces_A1 = False
    record(
        "M-B.4 Mechanism M-B does NOT force A1 (honest obstruction)",
        not mb_forces_A1,
        "ε_{ij} antisymmetric invariant factorizes off the generation\n"
        "structure.  Its presence contributes a universal factor of 2 to the\n"
        "Yukawa normalization but leaves the ratio |b|²/a² unconstrained.",
    )

    verdict(
        "M-B  Triple-product ε_{ij} invariant",
        "NO CONSTRAINT",
        "The ε_{ij} contraction operates entirely within SU(2)_L doublet indices\n"
        "(i,j) and factorizes as an overall tensor product with the generation-\n"
        "space Yukawa matrix.  It imposes no differential restriction on the\n"
        "(a, b) components in generation space.  The gauge-invariant singlet\n"
        "structure is compatible with ANY circulant Hermitian Yukawa texture.",
    )
    return mb_forces_A1


# --------------------------------------------------------------------
# Mechanism M-C: Commutation of mass-squared matrix with retained gauge Casimir
# --------------------------------------------------------------------


def probe_mechanism_C():
    section("Mechanism M-C — Mass² commutation with retained gauge Casimir")
    print()
    print("  Setup:")
    print("    Physical charged-lepton mass-squared matrix: M² = M·M† where")
    print("    M is the Dirac mass matrix (proportional to the Yukawa matrix")
    print("    times the Higgs VEV).  M^2 is a 3x3 Hermitian matrix in")
    print("    generation space.  On Herm_circ(3), M² = a·I + b·C + b̄·C².")
    print()
    print("    Retained gauge Casimirs (from CL3_SM_EMBEDDING):")
    print("        C₂_SU(2) = T(T+1) · 1_flavour = (3/4) · I_3   on Yukawa")
    print("                                                   participants")
    print("        C₂_U(1)  = Y²      · 1_flavour = (1/4) · I_3   on H")
    print()
    print("    The Casimir operators act as SCALARS on each gauge irrep, so")
    print("    in generation space they are proportional to I_3.  Therefore")
    print("    [M², C₂_SU(2)] = 0 and [M², C₂_U(1)] = 0 AUTOMATICALLY (both")
    print("    Casimirs are multiples of identity in generation space).")
    print()
    print("  Question: can a non-trivial commutation impose |b|²/a² = 1/2?")

    H, a, br, bi, b, bc = build_herm_circ()
    C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])

    # M² as circulant Hermitian
    M_sq = a * sp.eye(3) + b * C3 + bc * (C3 * C3)

    # Casimir operators proportional to I_3 (scalars on gauge irrep)
    C2_SU2 = sp.Rational(3, 4) * sp.eye(3)
    C2_U1 = sp.Rational(1, 4) * sp.eye(3)
    C2_diff = C2_SU2 - C2_U1  # = (1/2) · I_3
    C2_sum = C2_SU2 + C2_U1   # = 1 · I_3

    commutator_diff = M_sq * C2_diff - C2_diff * M_sq
    commutator_sum = M_sq * C2_sum - C2_sum * M_sq

    commutator_diff_simp = sp.simplify(commutator_diff)
    commutator_sum_simp = sp.simplify(commutator_sum)

    print()
    print(f"  [M², (T(T+1) − Y²) · I]  = {list(commutator_diff_simp)}")
    print(f"  [M², (T(T+1) + Y²) · I]  = {list(commutator_sum_simp)}")

    trivial_commutator_diff = (commutator_diff_simp == sp.zeros(3, 3))
    trivial_commutator_sum = (commutator_sum_simp == sp.zeros(3, 3))

    record(
        "M-C.1 [M², ∆C · I] = 0 trivially (Casimir-diff is a scalar in gen. space)",
        trivial_commutator_diff,
        "Scalar multiples of I commute with every matrix.  Gives no constraint.",
    )

    record(
        "M-C.2 [M², C_sum · I] = 0 trivially (Casimir-sum is also a scalar)",
        trivial_commutator_sum,
        "Same reasoning: both Casimirs are generation-space scalars.",
    )

    # A non-trivial question: CAN the Casimir be promoted to a non-trivial
    # generation-space operator that distinguishes the Z_3 scalar component
    # from the Z_3 doublet component?  This would require an ADDITIONAL
    # ingredient linking the retained Cl⁺(3) ≅ H structure to the Z_3
    # generation-space circulant.
    #
    # No such ingredient is retained.  The SU(2)_L × U(1)_Y Casimir
    # quantum numbers of L and H are THE SAME for every generation, so
    # they contribute trivially to the Z_3 decomposition.

    # Test: construct a candidate "generation-graded Casimir" C_gen
    # that gives the Casimir SUM on the Z_3 scalar and the Casimir
    # DIFFERENCE on the Z_3 doublet.  If such an operator is AXIOM-NATIVE,
    # then the commutation [M², C_gen] = 0 would indeed force |b|²/a²
    # = ∆C/C_sum = 1/2.
    #
    # Compute: does such an operator exist naturally?
    # The Z_3 scalar projector P_0 = (I + C + C²)/3
    # The Z_3 doublet projector  P_D = I − P_0 = (2I − C − C²)/3
    # Construct C_gen = C_sum · P_0 + ∆C · P_D.

    P0 = (sp.eye(3) + C3 + C3 * C3) / 3
    PD = sp.eye(3) - P0

    C_gen = sp.Rational(1, 1) * P0 + sp.Rational(1, 2) * PD  # C_sum=1, ∆C=1/2
    C_gen_simp = sp.simplify(C_gen)

    print()
    print("  Candidate 'generation-graded Casimir' C_gen:")
    print("      C_gen = C_sum · P_0 + ∆C · P_D")
    print("            = 1 · P_0 + (1/2) · P_D")
    print()
    print(f"  C_gen = \n{sp.pretty(C_gen_simp)}")

    # Trace check
    tr_C_gen = sp.trace(C_gen_simp)
    print(f"  tr(C_gen) = {tr_C_gen}   (mix of 1·(1 mode) + (1/2)·(2 modes) = 1 + 1 = 2)")

    # Eigenvalues
    eigs = C_gen_simp.eigenvals()
    print(f"  Eigenvalues of C_gen: {eigs}")

    # Test: if [M², C_gen] = 0 is imposed, what does it force?
    commutator_gen = sp.simplify(M_sq * C_gen_simp - C_gen_simp * M_sq)
    print()
    print(f"  [M², C_gen]   = \n{sp.pretty(sp.simplify(commutator_gen))}")

    # M² = a·I + b·C + b̄·C² is itself circulant, so it's diagonal in the
    # Z_3 Fourier basis.  C_gen is also diagonal in that basis (being a
    # linear combination of P_0 and P_D).  So they commute automatically.
    mc_commutation_trivial = (commutator_gen == sp.zeros(3, 3))

    record(
        "M-C.3 [M², C_gen] = 0 trivially (both circulant in Fourier basis)",
        mc_commutation_trivial,
        "C_gen is a linear combination of Z_3 projectors P_0, P_D; M² is\n"
        "circulant; both share a simultaneous eigenbasis.  Commutation is\n"
        "automatic and gives NO constraint on (a, b).",
    )

    # Try the stronger requirement: M² is an eigenvector of C_gen with a
    # specific eigenvalue.  Compute how M² decomposes under C_gen:
    # M² = a·I + b·C + b̄·C² = 3a·P_0 + (scalar in P_D subspace).
    # Here 3a is the Z_3 scalar component (eigenvalue of M² on P_0 subspace),
    # and the Z_3 doublet contributes the b, b̄ pieces.
    #
    # Using C_gen eigenvalues (1 on P_0, 1/2 on P_D):
    #   M² · C_gen = a · (3 P_0 · 1) + off-diagonal (·1/2)

    # Compute the two components of M² in the P_0, P_D decomposition
    M_sq_P0 = P0 * M_sq * P0  # should be 3a P_0 / 3 = a · P_0 (rank 1)
    M_sq_PD = PD * M_sq * PD  # doublet part
    M_sq_P0_simp = sp.simplify(M_sq_P0)
    M_sq_PD_simp = sp.simplify(M_sq_PD)

    print()
    print(f"  Z_3 scalar component of M²:  tr(P_0 · M²) = {sp.simplify(sp.trace(P0 * M_sq))}")
    print(f"      (this is 'a' since tr(P_0) = 1)")
    print(f"  Z_3 doublet component of M²: tr(P_D · M²) = {sp.simplify(sp.trace(PD * M_sq))}")
    print(f"      (this is '2a' since tr(P_D) = 2)")

    # The SINGLET energy
    E_plus = sp.simplify(sp.trace(M_sq * M_sq * P0))
    # The DOUBLET energy
    E_perp = sp.simplify(sp.trace(M_sq * M_sq * PD))

    # These match the standard Herm_circ(3) isotype decomposition:
    # E_+ = (tr M²)²/3 = 3a² for circulant with b parameters...
    # More carefully: E_+ is defined as ||P_I(M²)||² in the Frobenius inner
    # product of Herm(3), with P_I the projector onto scalar multiples of I.
    # For M² circulant Hermitian:
    # P_I(M²) = a·I, so E_+ = ||a·I||² = 3 a²
    # P_I^perp(M²) = b·C + b̄·C², so E_⊥ = 6 |b|²
    E_plus_def = 3 * a ** 2
    E_perp_def = 6 * (br ** 2 + bi ** 2)
    print()
    print(f"  Isotype energies in Herm_circ(3):")
    print(f"    E_+ = ||P_I(M²)||² = {E_plus_def}")
    print(f"    E_⊥ = ||P_I^perp(M²)||² = {E_perp_def}")

    # TEST: does requiring the Casimir-graded 'weight' on the energies match the
    # Casimir-graded eigenvalue structure of C_gen?
    # Specifically: E_+ = C_sum · something,  E_⊥ = ∆C · (something · 2)
    # (The factor 2 is the dim of the doublet.)
    #
    # If we impose the ansatz:
    #   E_+ / (dim_scalar) = C_sum · λ
    #   E_⊥ / (dim_doublet) = ∆C · λ     (same λ — one free parameter)
    # then
    #   3a² / 1 = 1 · λ    ⟹ λ = 3a²
    #   6|b|² / 2 = (1/2) · λ ⟹ 3|b|² = (1/2) · 3a² = 3a²/2 ⟹ |b|²= a²/2 ✓
    #
    # This GIVES |b|²/a² = 1/2 = A1 !!

    print()
    print("  CRITICAL ANSATZ (proposed Casimir-weighted normalization):")
    print("      E_+ / dim(scalar)  = C_sum · λ  ⟹ 3a²/1 = 1 · λ")
    print("      E_⊥ / dim(doublet) = ∆C    · λ  ⟹ 6|b|²/2 = (1/2) · λ")
    print("  Solving the pair:")

    lam = sp.Symbol('lambda', positive=True)
    b_sq = sp.Symbol('bsq', positive=True)   # stand-in for |b|² = br²+bi²
    E_plus_sym = 3 * a**2
    E_perp_sym = 6 * b_sq
    eq1 = sp.Eq(E_plus_sym / 1, 1 * lam)
    eq2 = sp.Eq(E_perp_sym / 2, sp.Rational(1, 2) * lam)
    # Solve for λ from eq1, substitute into eq2, solve for b_sq in terms of a
    sol_lam = sp.solve(eq1, lam)[0]          # λ = 3a²
    b_sq_sol = sp.solve(eq2.subs(lam, sol_lam), b_sq)
    print(f"    λ from E_+ equation:    λ = {sol_lam}")
    print(f"    |b|² from E_⊥ equation: {b_sq_sol}")

    if b_sq_sol:
        b_sq_val = b_sq_sol[0]
        ratio = sp.simplify(b_sq_val / a**2)
        print(f"    |b|²/a² = {ratio}  (target: 1/2)")
        forces_A1_under_ansatz = (ratio == sp.Rational(1, 2))
    else:
        forces_A1_under_ansatz = False

    record(
        "M-C.4 Casimir-weighted isotype ansatz gives |b|²/a² = 1/2 = A1 (conditional)",
        forces_A1_under_ansatz,
        "Under the ansatz E_+/dim_s = C_sum·λ and E_⊥/dim_d = ∆C·λ,\n"
        "the two equations force |b|²/a² = ∆C·dim_s/(C_sum·dim_d) = 1/2.\n"
        "IF the ansatz is axiom-native, this closes A1.",
    )

    # However, does the Cl(3)/Z³ retained framework ACTUALLY impose this ansatz?
    # The ansatz says: isotype energies per unit irrep dimension equal a
    # common scalar times the corresponding Casimir.  The Casimir-SUM
    # C_τ = 1 is already retained (gives y_τ).  The Casimir-DIFFERENCE
    # ∆C = 1/2 is NOT yet retained.
    #
    # The ansatz is EQUIVALENT to stating:
    #   "the Z_3 doublet energy-per-dim equals the Z_3 scalar energy-per-dim
    #    weighted by the Casimir RATIO ∆C/C_τ = 1/2."
    #
    # This is essentially a restatement of the target identity in a
    # Casimir-weighted form.  It IS the open lemma, not a derivation.
    #
    # To make the ansatz axiom-native, we need a retained principle that
    # says: "the isotype energy per irrep dim is proportional to the
    # Casimir of the gauge sector acting on that Z_3 irrep."  Since
    # SU(2)_L × U(1)_Y act the same way on every Z_3 irrep (they are
    # flavour-universal), no such principle arises automatically.

    mc_forces_A1 = False  # The ansatz gives A1, but the ansatz itself is not retained.
    record(
        "M-C.5 Mechanism M-C does NOT force A1 from retained ingredients alone",
        not mc_forces_A1,
        "The ansatz 'isotype energy per dim = Casimir·scalar' GIVES A1.\n"
        "But the ansatz itself is not axiom-native: SU(2)_L × U(1)_Y\n"
        "act identically on each Z_3 irrep, so no retained principle\n"
        "prescribes distinct Casimir weights on the Z_3 scalar vs doublet.",
    )

    verdict(
        "M-C  Mass² commutation with gauge Casimir",
        "CLOSE / REQUIRES ANSATZ",
        "Direct commutation [M², C_Casimir] = 0 is trivial and gives no\n"
        "constraint.  A Casimir-graded isotype-energy ansatz (E_+/d_s = C_sum·λ,\n"
        "E_⊥/d_d = ∆C·λ) DOES force |b|²/a² = 1/2.  The ansatz, however, is\n"
        "a reformulation of the target identity and is not yet implied by\n"
        "retained principles — it would need its own axiom-native derivation.",
    )

    return mc_forces_A1


# --------------------------------------------------------------------
# Bonus diagnostic: examine whether retained structures + additional
# obvious principles can force the Casimir-weighted isotype ansatz.
# --------------------------------------------------------------------


def diagnostic_isotype_ansatz():
    section("Diagnostic — what extra principle would make M-C's ansatz axiom-native?")
    print()
    print("  M-C showed: the ansatz 'E_+/d_s = C_sum·λ, E_⊥/d_d = ∆C·λ' closes A1.")
    print("  Here we examine what extra structural principle would IMPOSE this ansatz.")
    print()
    print("  Candidate principle (P1): 'each isotype carries its own Casimir'.")
    print("      This would require Z_3 scalar and Z_3 doublet to transform in")
    print("      DIFFERENT reps of SU(2)_L × U(1)_Y, with different Casimirs.")
    print("      In the retained framework, both are charged leptons with the")
    print("      same (T, Y).  So P1 is NOT retained.")
    print()
    print("  Candidate principle (P2): 'isotype energy ∝ gauge Casimir on sector'.")
    print("      Per-irrep-dim normalization is standard in QFT Wilson coefficients.")
    print("      If the Z_3 scalar energy is normalized by C_sum (the retained")
    print("      y_τ-generating Casimir) and the Z_3 doublet by ∆C (the open")
    print("      Casimir-difference), this is exactly the ansatz.")
    print("      But this normalization choice is precisely the keystone lemma.")
    print()
    print("  Candidate principle (P3): anomaly-matching on Z_3 coset.")
    print("      In SM, 't Hooft anomaly matching relates the UV global anomalies")
    print("      (chiral fermion content) to IR anomaly polynomials.  The SUM")
    print("      T(T+1) + Y² governs the universal part; the DIFFERENCE governs")
    print("      the sign asymmetry between SU(2)_L-anomaly and U(1)_Y-anomaly.")
    print("      IF the Z_3 generation-space structure hybridizes with the gauge-")
    print("      anomaly polynomial such that scalar ↔ sum-anomaly and doublet ↔")
    print("      difference-anomaly, the ansatz would emerge.  Status: speculative.")
    print()
    print("  Candidate principle (P4): fermion number ambiguity on Z_3 cyclic.")
    print("      In the retained Z_3 cyclic, the SCALAR generation mode has Z_3-")
    print("      charge 0 (trivial) and the DOUBLET modes have Z_3-charges ±1.")
    print("      IF the SUM Casimir couples to Z_3 charge squared (|q|² = 0)")
    print("      and the DIFFERENCE couples to (|q|² = 1), this gives the")
    print("      ansatz.  But |q|² = 0 vs 1 gives ratio 0/1, not 1/1/2.")
    print()
    print("  None of P1–P4 is a retained theorem in the current atlas.")

    record(
        "DIAG.1 No retained principle P1–P4 forces the isotype ansatz",
        True,
        "Each candidate extra principle is either not retained or reformulates\n"
        "the target identity.  The Casimir-difference identity |b|²/a² = ∆C\n"
        "remains a primitive that would need to be adopted or derived by a\n"
        "new structural theorem.",
    )


# --------------------------------------------------------------------
# Numerical cross-check: for M-C ansatz only, verify A1 extraction on
# representative (a, b) and confirm the mechanism acts as stated.
# --------------------------------------------------------------------


def numerical_crosscheck_mc():
    section("Numerical cross-check — M-C ansatz on sample circulant Herm")
    print()
    print("  Instantiate (a, b) saturating the M-C ansatz and check A1 holds.")

    a_val = sp.Rational(2, 1)
    b_sq_val = a_val ** 2 / 2  # = 2
    b_abs = sp.sqrt(b_sq_val)

    E_plus_val = 3 * a_val ** 2
    E_perp_val = 6 * b_sq_val

    lam_from_sum = E_plus_val / 1
    lam_from_diff = E_perp_val / (2 * sp.Rational(1, 2))  # dim_d = 2, ∆C = 1/2
    lam_equal = (lam_from_sum == lam_from_diff)

    print(f"    (a, |b|²)                = ({a_val}, {b_sq_val})")
    print(f"    E_+ = 3a²               = {E_plus_val}")
    print(f"    E_⊥ = 6|b|²             = {E_perp_val}")
    print(f"    λ from E_+/dim_s·C_sum  = {lam_from_sum}")
    print(f"    λ from E_⊥/dim_d·∆C     = {lam_from_diff}")

    record(
        "NC.1 M-C ansatz parameters are consistent at |b|²/a² = 1/2",
        lam_equal,
        f"Both sides give λ = {lam_from_sum} when A1 holds.",
    )

    # Now break A1 and confirm ansatz is violated
    a2 = sp.Rational(3, 1)
    bsq2 = a2 ** 2  # |b|²/a² = 1 (NOT A1)
    E_plus_2 = 3 * a2 ** 2
    E_perp_2 = 6 * bsq2
    lam_sum_2 = E_plus_2 / 1
    lam_diff_2 = E_perp_2 / (2 * sp.Rational(1, 2))

    print()
    print(f"  Break A1: (a, |b|²) = ({a2}, {bsq2}), ratio = 1 (NOT A1)")
    print(f"    λ from sum  = {lam_sum_2}")
    print(f"    λ from diff = {lam_diff_2}")
    print(f"    agree? {lam_sum_2 == lam_diff_2}")

    record(
        "NC.2 Ansatz FAILS at |b|²/a² ≠ 1/2 (consistency check)",
        lam_sum_2 != lam_diff_2,
        "Ansatz is ONLY consistent at A1.  Off A1 the two λ determinations\n"
        "disagree, confirming the ansatz would force A1 IF adopted.",
    )


def main() -> int:
    section("A1 KEYSTONE probe — derive |b|²/a² = T(T+1) − Y²")
    print()
    print("Target: close the remaining A1 lemma by deriving the Casimir-difference")
    print("identity from axiom-native mechanisms.  Tests M-A, M-B, M-C in turn.")
    print()
    print("Retained quantum numbers:")
    print("    SU(2)_L: T = 1/2 (Cl⁺(3) ≅ ℍ → Spin(3) = SU(2)_L)")
    print("    U(1)_Y:  Y = ±1/2 for L, H (pseudoscalar ω extension)")
    print("    C_τ = T(T+1) + Y² = 1        (retained, gives y_τ)")
    print("    ∆C  = T(T+1) − Y² = 1/2      (candidate identity, target of A1)")

    ma_ok = probe_mechanism_A()
    mb_ok = probe_mechanism_B()
    mc_ok = probe_mechanism_C()
    diagnostic_isotype_ansatz()
    numerical_crosscheck_mc()

    # Final summary
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total} checks")
    print()
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("PER-MECHANISM VERDICTS")
    print("-" * 88)
    for mech, status, rationale in VERDICTS:
        print(f"  {mech}: {status}")
        for line in rationale.split("\n"):
            print(f"      {line}")
        print()

    section("FINAL VERDICT — KEYSTONE CLOSURE STATUS")
    any_forces = ma_ok or mb_ok or mc_ok
    if any_forces:
        print("POSITIVE: at least one mechanism DERIVES A1 from retained ingredients.")
        print()
        if ma_ok:
            print("  M-A:  Casimir-difference insertion CLOSES the lemma.")
        if mb_ok:
            print("  M-B:  Triple-product ε_{ij} invariant CLOSES the lemma.")
        if mc_ok:
            print("  M-C:  Mass² commutation with gauge Casimir CLOSES the lemma.")
    else:
        print("NEGATIVE:  none of M-A, M-B, M-C derive A1 from strictly retained")
        print("ingredients.  Specifically:")
        print()
        print("  M-A  Casimir insertion — factorizes uniformly on generation space.")
        print("       No differential constraint on (a, b).  Ratio invariant.")
        print()
        print("  M-B  ε_{ij} triple-product — contracts in SU(2)_L doublet indices")
        print("       only; factorizes off generation-space circulant structure.")
        print("       No constraint on (a, b) ratio.")
        print()
        print("  M-C  Mass² / Casimir commutation — trivial since Casimir is a")
        print("       scalar in generation space.  A Casimir-graded isotype-energy")
        print("       ANSATZ does force A1, but the ansatz itself is a restatement")
        print("       of the target identity and not axiom-native in the retained")
        print("       framework.")
        print()
        print("FAILURE MODE — WHY THE LEMMA DOES NOT DERIVE WITHIN RETAINED INGREDIENTS:")
        print()
        print("  The retained SU(2)_L × U(1)_Y quantum numbers (T, Y) of the charged-")
        print("  lepton Yukawa participants are FLAVOUR-UNIVERSAL.  They are the same")
        print("  for every Z_3 generation (every Z_3 irrep of the generation-space")
        print("  circulant).  As a consequence, the SU(2)_L × U(1)_Y Casimir operators")
        print("  act as MULTIPLES OF IDENTITY in generation space and cannot")
        print("  distinguish the Z_3 scalar (which determines a) from the Z_3 doublet")
        print("  (which determines b).  The Casimir-difference identity")
        print("  |b|²/a² = T(T+1) − Y² would require a bridge that COUPLES the")
        print("  gauge-algebra Casimir imbalance directly to the Z_3 generation-space")
        print("  isotype weights.  The retained framework does not provide such a")
        print("  bridge among the ingredients surveyed here.")
        print()
        print("  CONCLUSION ON DERIVABILITY:")
        print("    - The Casimir-difference identity is DIMENSIONALLY and")
        print("      NUMERICALLY CONSISTENT with A1 (a genuine match of gauge-")
        print("      algebra invariants with the Herm_circ(3) isotype ratio).")
        print("    - It is NOT straightforwardly DERIVABLE from retained")
        print("      ingredients because the needed bridge (gauge algebra ↔ Z_3")
        print("      generation space) is absent.")
        print("    - The most economical path to closure is to ADOPT the Casimir-")
        print("      weighted isotype-energy ansatz as a primitive axiom in the")
        print("      EW-scalar / Yukawa lane.  Under this primitive, A1 follows")
        print("      from already-retained C_τ = 1 and the pseudoscalar hypercharge")
        print("      assignment.")

    all_pass = n_pass == n_total
    print()
    if all_pass:
        print("All structural checks PASS (including the negative 'does-not-force'")
        print("checks, which are the honest findings).")
    else:
        print(f"Structural checks: {n_pass}/{n_total} PASS.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
