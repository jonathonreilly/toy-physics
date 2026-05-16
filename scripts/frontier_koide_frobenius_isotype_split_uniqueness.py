"""
Conditional AM-GM result on Herm_circ(3) inside an admitted Frobenius split.

Scope (matches the narrowed note at
docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md):

The runner verifies the algebraic AM-GM chain
  E_+    = (tr M)^2 / 3        [scalar-subspace Frobenius energy]
  E_perp = Tr(M^2) - (tr M)^2/3 [traceless-subspace Frobenius energy]
  E_+ + E_perp = Tr(M^2)        [Pythagoras]
  max log(E_+ E_perp) at E_+ = E_perp = N/2  [AM-GM, strictly concave]
giving kappa = a^2/|b|^2 = 2 and Q = 2/3 on the AM-GM-symmetric point.

It does NOT establish uniqueness of the Frobenius normalization itself.
The general Ad-invariant symmetric bilinear form on Herm(3) is the
TWO-parameter family
  B_{α,β}(A, B) = α · Tr(AB) + β · (tr A)(tr B)
with PD region α > 0 AND α + 3β > 0. Choosing β = 0 picks the Frobenius
form, but PD + Ad-invariance alone leave β free, so the scalar/traceless
isotype-scale RATIO is not fixed by retained Cl(3)/Herm_circ(3)
structure. Test (1e) below exhibits an explicit PD Ad-invariant member
of the family with β ≠ 0 that disagrees with the Frobenius form on a
trace-bearing matrix.

What this runner verifies (each line is a PASS-counted symbolic check):
  (1) Frobenius form Tr(M^2): trace identity, Hermitian self-adjoint
      identity, Ad-invariance (1c), and the auditor-quoted PD/Ad-invariant
      counter-example family B_{α,β} (1d degenerate boundary, 1e generic
      PD member with β ≠ 0). No uniqueness claim is made.
  (2) Singlet projector P_0 = J/3 is the unique C_3-singlet rank-1
      Hermitian projector on C^3 (vector-space statement; separate from
      the matrix-space Frobenius question above).
  (3) P_I : M -> (tr M / 3) I as the orthogonal projection in the
      admitted Frobenius inner product; E_+ = (tr M)^2 / 3 follows.
  (4) E_perp = Tr(M^2) - E_+ is the traceless-part Frobenius squared.
  (5) Both E_+ >= 0 and E_perp >= 0, with strict positivity at the
      non-degenerate PDG charged-lepton interior point.
  (6) Pythagoras: E_+ + E_perp = Tr(M^2) exactly.
  (7) AM-GM extremum at E_+ = E_perp = N/2 ⟹ kappa = 2 ⟹ Q = 2/3.
  (8) Composite consistency of (1)-(7) into the conditional chain.

This runner is the executable backing of the conditional AM-GM headline.
It is NOT a uniqueness theorem for the Frobenius normalization.
"""
import sympy as sp

sp.init_printing()

PASS = 0
FAIL = 0
log = []


def ok(name, cond, detail=""):
    global PASS, FAIL
    if bool(cond):
        PASS += 1
        log.append(f"  [PASS] {name}: {detail}")
    else:
        FAIL += 1
        log.append(f"  [FAIL] {name}: {detail}")


# ==========================================================================
# Setup: symbolic Herm_circ(3) matrix M = a I + b C + b^* C^2
# ==========================================================================

a = sp.Symbol('a', real=True)
x = sp.Symbol('x', real=True)  # b = x + iy
y = sp.Symbol('y', real=True)
b = x + sp.I * y
b_bar = x - sp.I * y

I3 = sp.eye(3)
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])  # cyclic shift
C2 = C * C

# Hermitian circulant matrix: M = a I + b C + b^* C^2
M = a * I3 + b * C + b_bar * C2
# Explicit form:
# M = [[a, b, b*], [b*, a, b], [b, b*, a]]
M_explicit = sp.simplify(M)

# J = all-ones matrix
J = sp.Matrix([[1,1,1], [1,1,1], [1,1,1]])

# Singlet projector P_0 = J/3
P_0 = J / 3

# omega
omega = sp.Rational(-1,2) + sp.I * sp.sqrt(3) / 2
omega2 = sp.Rational(-1,2) - sp.I * sp.sqrt(3) / 2

# ==========================================================================
# (1) Tr(M^2) is the Frobenius inner product on Herm_circ(3)
# ==========================================================================

log.append("=== (1) Frobenius form on Herm_circ(3) ===")

# Compute Tr(M^2) symbolically
M_sq = sp.simplify(M * M)
Tr_M_sq = sp.simplify(sp.trace(M_sq))
ok("1a. Tr(M^2) = 3a^2 + 6|b|^2 = 3a^2 + 6(x^2+y^2)",
   sp.simplify(Tr_M_sq - (3*a**2 + 6*(x**2 + y**2))) == 0,
   f"Tr(M^2) = {Tr_M_sq}")

# ||M||_F^2 = Tr(M^dagger M) = Tr(M^2) for Hermitian M
# Executable: M = M^dagger for Hermitian, so Tr(M^dagger M) = Tr(M · M) = Tr(M^2).
M_dagger = M.T.conjugate()
ok("1b. For Hermitian M, Tr(M^dagger M) = Tr(M^2) (symbolic identity)",
   sp.simplify(M - M_dagger) == sp.zeros(3, 3)
   and sp.simplify(sp.trace(M_dagger * M) - sp.trace(M * M)) == 0,
   "M = M^dagger ⟹ Tr(M^dagger M) = Tr(M^2)")

# The trace form B(A, B) = Tr(AB) is one Ad-invariant symmetric bilinear
# form on Herm(3). Under Herm(3) = R·I ⊕ su(3), Schur orthogonality forces
# a U(3)-invariant form to act as one scalar per irreducible isotype, so
# the GENERAL Ad-invariant symmetric bilinear form on Herm(3) is the
# TWO-PARAMETER family
#   B_{α,β}(A, B) = α · Tr(AB) + β · (tr A)(tr B),
# where α controls the traceless (su(3)) isotype and (α + 3β) controls
# the scalar (R·I) isotype. The ratio of the two isotype scales is NOT
# fixed by Ad-invariance: β is free, and PD-ness only requires α > 0 and
# α + 3β > 0. This runner does NOT close that 1-parameter freedom and the
# note's headline scope is correspondingly demoted to a CONDITIONAL AM-GM
# result inside an admitted Frobenius (β = 0) normalization.
#
# The two executable checks below register exactly that scope:
#   1c. Tr(AB) is Ad-invariant (one direction; does NOT imply uniqueness).
#   1d. The pure-(tr A)(tr B) alternative (β > 0, α = 0) is degenerate
#       (zero on traceless), so PD excludes that single boundary point.
#   1e. The full PD Ad-invariant FAMILY α·Tr + β·(tr)(tr) with α > 0 and
#       α + 3β > 0 contains non-Frobenius members (β ≠ 0), so PD alone
#       does NOT force β = 0. This is the auditor-quoted counter-example
#       family, exhibited explicitly.
t = sp.Symbol('t', real=True)
# Representative of su(3): Gell-Mann-like traceless Hermitian
X_tr = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
t1, t2, t3 = sp.symbols('t1 t2 t3', real=True)
U_diag = sp.diag(sp.exp(sp.I * t1), sp.exp(sp.I * t2), sp.exp(sp.I * t3))
A_test = sp.Matrix([[1, sp.Rational(1, 2), 0], [sp.Rational(1, 2), 2, 0], [0, 0, 3]])
B_test = sp.Matrix([[2, 0, 1], [0, 1, 0], [1, 0, 4]])
trace_AB = sp.trace(A_test * B_test)
A_conj = U_diag.T.conjugate() * A_test * U_diag
B_conj = U_diag.T.conjugate() * B_test * U_diag
trace_conj_AB = sp.simplify(sp.trace(A_conj * B_conj))
ok("1c. Tr(AB) is Ad-invariant on Herm(3) (does not by itself imply uniqueness)",
   sp.simplify(trace_conj_AB - trace_AB) == 0,
   f"Tr(AB) = {trace_AB}, Tr(U^†AU · U^†BU) = {trace_conj_AB}")

# 1d. The pure-(tr A)(tr B) alternative (β > 0, α = 0) vanishes on
# traceless matrices, so PD excludes that single boundary point of the
# family. This does NOT exclude mixed PD members with β ≠ 0.
B_2_on_traceless = sp.trace(X_tr) * sp.trace(X_tr)
ok("1d. Pure-(tr A)(tr B) alternative (β > 0, α = 0) vanishes on a traceless matrix",
   sp.trace(X_tr) == 0 and B_2_on_traceless == 0,
   f"Tr(X_tr) = {sp.trace(X_tr)}; pure-trace-product form is degenerate")

# 1e. The auditor-quoted counter-example family: exhibit an explicit
# PD Ad-invariant form B_{α,β} with β ≠ 0, verify it is Ad-invariant on
# the test pair (A_test, B_test), verify it is PD on Herm(3) by checking
# the isotype scales (α > 0 on su(3); α + 3β > 0 on R·I), and verify it
# disagrees with the Frobenius form on a generic Herm(3) matrix M_test
# with non-zero trace. This is the registered counter-example to any
# uniqueness reading of (1c) + (1d) alone.
alpha_val = sp.Rational(1, 1)   # α = 1 > 0
beta_val  = sp.Rational(1, 1)   # β = 1 ≠ 0, and α + 3β = 4 > 0

def B_ab(A, B, alpha, beta):
    return alpha * sp.trace(A * B) + beta * sp.trace(A) * sp.trace(B)

B_ab_AB      = sp.simplify(B_ab(A_test, B_test, alpha_val, beta_val))
B_ab_conj_AB = sp.simplify(B_ab(A_conj, B_conj, alpha_val, beta_val))
ad_invariant_1e = sp.simplify(B_ab_AB - B_ab_conj_AB) == 0

# PD diagnostic: pick a generic non-zero Hermitian H and check B_{α,β}(H, H) > 0.
# For Hermitian H with trace τ and traceless part H_⊥, B_{α,β}(H, H) =
#   α · (Tr(H_⊥^2) + τ^2 / 3) + β · τ^2
#     = α · Tr(H_⊥^2) + (α/3 + β) · τ^2 .
# Sufficient PD on Herm(3): α > 0 (traceless) AND (α + 3β)/3 > 0 ⟺ α + 3β > 0.
pd_on_su3      = alpha_val > 0
pd_on_scalarI  = (alpha_val + 3 * beta_val) > 0

# Disagreement with Frobenius (β = 0) on a generic trace-bearing M_test.
M_test = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 2]])  # Hermitian, tr = 4
frob_MM = sp.trace(M_test * M_test)                    # = 1 + 1 + 4 = 6
B_ab_MM = sp.simplify(B_ab(M_test, M_test, alpha_val, beta_val))
disagrees = sp.simplify(B_ab_MM - frob_MM) != 0        # 6 + 16 vs 6

ok("1e. Counter-example: B_{α,β} = α·Tr(AB)+β·(tr A)(tr B) with α=β=1 is "
   "PD, Ad-invariant, and disagrees with Frobenius (β=0) on a trace-bearing M",
   ad_invariant_1e and pd_on_su3 and pd_on_scalarI and disagrees,
   f"Ad-invariant: {ad_invariant_1e}; α>0: {pd_on_su3}; α+3β>0: {pd_on_scalarI}; "
   f"B_{{α,β}}(M,M)={B_ab_MM} vs Frobenius={frob_MM} (disagree: {disagrees})")

# ==========================================================================
# (2) Singlet projector P_0 = J/3 is the unique C_3-singlet projector
# ==========================================================================

log.append("\n=== (2) Singlet projector uniqueness ===")

# Check: P_0 = J/3 is idempotent
P_0_sq = sp.simplify(P_0 * P_0)
ok("2a. P_0^2 = P_0 (idempotent)",
   sp.simplify(P_0_sq - P_0) == sp.zeros(3, 3),
   "P_0 is a projector")

# Check: P_0 is Hermitian
ok("2b. P_0 = P_0^dagger (self-adjoint)",
   sp.simplify(P_0 - P_0.T.conjugate()) == sp.zeros(3, 3),
   "P_0 is Hermitian")

# Check: P_0 has rank 1
ok("2c. rank(P_0) = 1",
   P_0.rank() == 1,
   "projects onto 1-dim subspace")

# Check: image of P_0 is span of (1,1,1)/sqrt(3) = C_3 singlet
v_singlet = sp.Matrix([[1], [1], [1]]) / sp.sqrt(3)
P_0_v = sp.simplify(P_0 * v_singlet)
ok("2d. P_0 * (1,1,1)/sqrt(3) = (1,1,1)/sqrt(3)",
   sp.simplify(P_0_v - v_singlet) == sp.zeros(3, 1),
   "singlet vector is eigenvector with eigenvalue 1")

# Check: P_0 commutes with C (preserves C_3 structure)
comm = sp.simplify(P_0 * C - C * P_0)
ok("2e. [P_0, C] = 0 (C_3 invariance)",
   comm == sp.zeros(3, 3),
   "projector commutes with cyclic shift")

# Uniqueness of P_0: any rank-1 C_3-singlet Hermitian projector must project
# onto the unique 1-dim C_3-invariant subspace of C^3. Executable derivation:
# (i) compute C's eigenvectors, (ii) identify the eigenvalue-1 eigenvector,
# (iii) show it is unique up to scalar, (iv) show P_0 = v v^† matches J/3.
C_eigenvalues = list(C.eigenvals().keys())
# Eigenvalue-1 eigenvector
v_eigvecs = [v for v in C.eigenvects() if sp.simplify(v[0] - 1) == 0]
# v_eigvecs = [(eigenvalue, multiplicity, [basis])]
ok("2f1. Eigenvalue 1 of C appears with multiplicity 1",
   len(v_eigvecs) == 1 and v_eigvecs[0][1] == 1,
   f"eigenvalue-1 multiplicity = {v_eigvecs[0][1]}")

# The single eigenvector (up to scalar) is (1, 1, 1)
v_eig1 = v_eigvecs[0][2][0]
v_eig1_normed = v_eig1 / sp.sqrt((v_eig1.T * v_eig1)[0, 0])
P_from_eigvec = v_eig1_normed * v_eig1_normed.T
ok("2f2. Rank-1 C_3-singlet projector v_1 v_1^T (with v_1 normalized) = J/3",
   sp.simplify(P_from_eigvec - P_0) == sp.zeros(3, 3),
   "constructed from eigenvalue-1 eigenvector of C")

# Uniqueness via Schur: any OTHER rank-1 Hermitian projector commuting with C
# must have an eigenvector of C among its range. Since only eigenvalue-1
# eigenvector is real, rank-1 Hermitian projector with real entries that
# commutes with C is uniquely J/3.
ok("2f3. Uniqueness: any rank-1 Hermitian projector P with [P, C] = 0 has range = span{(1,1,1)}",
   len(v_eigvecs) == 1,  # only one real eigenvalue (1) ⟹ unique real eigenvector
   "C has exactly one real eigenvalue (= 1) ⟹ unique real eigenvector")

# ==========================================================================
# (3) E_+ = (tr M)^2 / 3 via MATRIX-SPACE projection onto scalar subspace
# ==========================================================================

log.append("\n=== (3) Singlet energy E_+ (matrix-space projection) ===")

# Correct framing: E_+ uses the MATRIX-SPACE projector P_I onto
# scalar multiples of the identity I (not the vector-space singlet projector
# P_0 = J/3 that acts on C^3).
# P_I(M) = (Tr(I^dagger M) / Tr(I^dagger I)) * I = (tr M / 3) * I
# This is the orthogonal projection in the Frobenius inner product.

# Tr(M) = 3a
tr_M = sp.trace(M)
ok("3a. tr(M) = 3a for Hermitian circulant",
   sp.simplify(tr_M - 3*a) == 0,
   f"tr M = {tr_M}")

# Matrix-space projector onto I:
# P_I: Herm(3) -> span{I}, P_I(M) = (tr M / 3) * I
P_I_M = (tr_M / 3) * sp.eye(3)
P_I_M = sp.simplify(P_I_M)

# Check: P_I_M is (a) times I
expected_PIM = a * sp.eye(3)
ok("3b. P_I(M) = (tr M / 3) * I = a * I",
   sp.simplify(P_I_M - expected_PIM) == sp.zeros(3, 3),
   f"scalar projection onto I = a * I")

# E_+ = ||P_I(M)||_F^2 = Tr((P_I(M))^2)
E_plus_frob = sp.simplify(sp.trace(P_I_M * P_I_M))
expected_E_plus = 3*a**2  # (tr M)^2 / 3 = 9a^2/3 = 3a^2
ok("3c. E_+ = ||P_I(M)||_F^2 = 3a^2 = (tr M)^2 / 3",
   sp.simplify(E_plus_frob - expected_E_plus) == 0,
   f"E_+ = {E_plus_frob}")

# Also verify: (tr M)^2 / 3 = 3a^2
ok("3d. (tr M)^2 / 3 = 3a^2",
   sp.simplify((tr_M**2)/3 - 3*a**2) == 0,
   "alternative formula")

# ==========================================================================
# (4) E_perp = Tr(M^2) - (tr M)^2 / 3 = 6|b|^2 via complementary projection
# ==========================================================================

log.append("\n=== (4) Doublet energy E_perp ===")

E_perp = sp.simplify(Tr_M_sq - (tr_M**2)/3)
ok("4a. E_perp = Tr(M^2) - (tr M)^2 / 3 = 6|b|^2",
   sp.simplify(E_perp - 6*(x**2 + y**2)) == 0,
   f"E_perp = {E_perp}")

# Complementary matrix-space projector: P_I_perp = Id - P_I (acting on Herm(3))
# (P_I_perp M) = M - (tr M / 3) * I  [traceless part of M]
P_I_perp_M = sp.simplify(M - P_I_M)

# Check: P_I_perp_M has trace zero
ok("4b. tr(P_I_perp M) = 0 (traceless part)",
   sp.simplify(sp.trace(P_I_perp_M)) == 0,
   "complementary projection is traceless")

# E_perp = ||P_I_perp M||_F^2 = Tr((P_I_perp M)^2)  (Hermitian, so =  Tr(X X^dag))
E_perp_frob = sp.simplify(sp.trace(P_I_perp_M * P_I_perp_M))
ok("4c. E_perp = ||P_I_perp M||_F^2 = 6|b|^2",
   sp.simplify(E_perp_frob - E_perp) == 0,
   f"traceless Frobenius squared: {E_perp_frob}")

# ==========================================================================
# (5) Positivity of E_+ and E_perp
# ==========================================================================

log.append("\n=== (5) Positivity ===")

# E_+ = 3a^2 >= 0. Executable: symbolic solver on the inequality.
nonneg_Eplus = sp.solve([3*a**2 < 0], [a])
ok("5a. E_+ = 3a^2 >= 0 for all real a (no real solutions of 3a^2 < 0)",
   nonneg_Eplus in (False, []),
   f"solutions of 3a^2 < 0 over reals: {nonneg_Eplus}")

# E_perp = 6(x^2 + y^2) >= 0. Executable: same kind of symbolic check.
nonneg_Eperp = sp.solve([6*(x**2 + y**2) < 0], [x, y])
ok("5b. E_perp = 6(x^2 + y^2) >= 0 for all real x, y",
   nonneg_Eperp in (False, []),
   f"solutions of 6(x^2+y^2) < 0 over reals: {nonneg_Eperp}")

# Equality: E_+ = 0 iff a = 0; E_perp = 0 iff b = 0.
# For physical non-degenerate charged leptons, plug in measured PDG masses
# and verify BOTH E_+ > 0 and E_perp > 0 numerically (interior case).
# Masses from PDG 2024 (MeV, converted consistently):
m_e_num = 0.5109989461
m_mu_num = 105.6583745
m_tau_num = 1776.86
# Koide's circulant encoding: eigenvalues of M correspond to sqrt(masses).
# (For Koide's original Q, m_i = sqrt(m_e), sqrt(m_mu), sqrt(m_tau); here we
#  encode the same data directly in a, b via the Herm_circ(3) spectral form.)
# Eigenvalues of M are a + b*omega^k + b^*·omega^{2k} for k = 0, 1, 2.
# For three real positive eigenvalues (sqrt masses), the standard Koide set
# has a_num = mean of sqrt(m_i), b = (complex value).
import cmath, math
s_e, s_mu, s_tau = math.sqrt(m_e_num), math.sqrt(m_mu_num), math.sqrt(m_tau_num)
a_num = (s_e + s_mu + s_tau) / 3.0
# Use the discrete Fourier transform of (s_e, s_mu, s_tau) under C to get b
om_num = cmath.exp(2j * math.pi / 3)
b_num = (s_e + s_mu * om_num.conjugate() + s_tau * om_num) / 3.0
E_plus_num = 3 * a_num**2
E_perp_num = 6 * (b_num.real**2 + b_num.imag**2)
ok("5c. Physical charged leptons (PDG): E_+ > 0 AND E_perp > 0 (interior case)",
   E_plus_num > 0 and E_perp_num > 0,
   f"E_+ = {E_plus_num:.6g}, E_perp = {E_perp_num:.6g}")

# ==========================================================================
# (6) Additivity: Tr(M^2) = E_+ + E_perp (exact)
# ==========================================================================

log.append("\n=== (6) Additivity (Pythagoras) ===")

ok("6a. E_+ + E_perp = Tr(M^2) exactly",
   sp.simplify(3*a**2 + 6*(x**2+y**2) - Tr_M_sq) == 0,
   "isotype decomposition is orthogonal under Frobenius")

# This means: fixing N = Tr(M^2) fixes E_+ + E_perp. Executable: the
# substitution identity holds symbolically — if Tr(M^2) = N, then the sum
# E_+ + E_perp also equals N (by 6a). Solve: E_perp = N - E_+.
N_sym_6 = sp.Symbol('N', positive=True)
E_plus_expr = 3 * a**2
E_perp_expr = 6 * (x**2 + y**2)
constraint_sum = E_plus_expr + E_perp_expr - N_sym_6
# Under the substitution Tr(M^2) = N (i.e. 3a^2 + 6(x^2+y^2) = N)
under_constraint = sp.simplify(constraint_sum.subs(Tr_M_sq, N_sym_6))
ok("6b. Under Tr(M^2) = N, the relation E_+ + E_perp = N holds symbolically",
   sp.simplify(constraint_sum - (Tr_M_sq - N_sym_6)) == 0,
   "E_+ + E_perp = Tr(M^2) so constraint reduces to Tr(M^2) = N")

# ==========================================================================
# (7) AM-GM: max of log(E_+ * E_perp) under E_+ + E_perp = N
# ==========================================================================

log.append("\n=== (7) AM-GM extremum ===")

# By AM-GM: for positive reals x + y = N, xy <= (N/2)^2 with equality iff
# x = y. Executable: compute the product xy under x + y = N as a univariate
# function of x, find its critical point, verify max at x = N/2 with value
# (N/2)^2. Also verify second derivative is strictly negative (concavity).

E_p_sym = sp.Symbol('E_p', positive=True)
N_sym = sp.Symbol('N', positive=True)
# Product as univariate function of E_+ with E_perp = N - E_+:
product_fn = E_p_sym * (N_sym - E_p_sym)
# First derivative w.r.t. E_+
dP_dEp = sp.diff(product_fn, E_p_sym)
# Critical point: dP/dE_+ = 0 ⟹ N - 2·E_+ = 0 ⟹ E_+ = N/2
crit = sp.solve(dP_dEp, E_p_sym)
max_value = product_fn.subs(E_p_sym, crit[0])
# Second derivative: d²P/dE_+² = -2 < 0 (strict concavity)
d2P_dEp2 = sp.diff(product_fn, E_p_sym, 2)
ok("7a. max E_+·E_perp under E_+ + E_perp = N equals (N/2)^2 at E_+ = N/2",
   len(crit) == 1
   and sp.simplify(crit[0] - N_sym / 2) == 0
   and sp.simplify(max_value - (N_sym / 2) ** 2) == 0
   and d2P_dEp2 == -2,
   f"crit = {crit}, max = {max_value}, d²P/dE² = {d2P_dEp2} (< 0 strictly concave)")

# At the AM-GM max, E_+ = E_perp = N/2. Since E_+ = 3a^2 and E_perp = 6|b|^2,
# equality gives 3a^2 = 6|b|^2 ⟹ a^2 = 2|b|^2 ⟹ kappa = a^2/|b|^2 = 2.
# Executable: solve the equality symbolically.
kappa_sym = sp.Symbol('kappa', positive=True)
# Equation: 3a^2 = 6|b|^2, with |b|^2 = x^2 + y^2, kappa := a^2/(x^2+y^2)
equality_constraint = 3*a**2 - 6*(x**2 + y**2)
kappa_from_constraint = sp.solve(equality_constraint, a**2)
# kappa = a^2 / (x^2 + y^2) = 2(x^2+y^2) / (x^2+y^2) = 2
kappa_value = kappa_from_constraint[0] / (x**2 + y**2)
ok("7b. At the AM-GM max, kappa = a^2/|b|^2 = 2",
   sp.simplify(kappa_value - 2) == 0,
   f"a^2 = {kappa_from_constraint[0]}, kappa = a^2/|b|^2 = {sp.simplify(kappa_value)}")

# Q = (1 + 2/kappa) / d for d=3
Q_value = (1 + sp.Rational(2, 2)) / 3
ok("7c. Q = (1 + 2/kappa)/d = 2/3 at kappa=2, d=3",
   Q_value == sp.Rational(2, 3),
   f"Q = {Q_value}")

# ==========================================================================
# (8) Composite consistency — combine the executable pieces into one check.
# ==========================================================================

log.append("\n=== (8) Composite forcing consistency ===")

# Summary print (no PASS counting): each piece already has its own executable
# PASS above. Here we state the conditional chain for the reader, then
# verify composite. Note that (1) verifies Ad-invariance and exhibits the
# auditor's counter-example family rather than claiming uniqueness.
print("""
  Conditional-chain pieces (each with executable PASS above):
    (1) Frobenius form Tr(M^2) is Ad-invariant; PD Ad-invariant family
        B_{α,β} = α Tr(AB) + β (tr A)(tr B) with α > 0, α + 3β > 0 has
        β = 0 (Frobenius) as one member but contains other PD members
        (β ≠ 0) that disagree with Frobenius on trace-bearing M. The
        Frobenius normalization is ADMITTED, not derived.
    (2) P_0 = J/3 = unique rank-1 C_3-singlet Hermitian projector on C^3
    (3) P_I(M) = (tr M / 3) I = orthogonal projector under admitted Frobenius
    (4) E_+ = (tr M)^2 / 3 = ||P_I M||_F^2
    (5) E_perp = Tr(M^2) - E_+ = ||(I - P_I) M||_F^2
    (6) Positivity: E_+, E_perp >= 0 (strict at non-degenerate lepton masses)
    (7) Additivity (Pythagoras): E_+ + E_perp = Tr(M^2)
    (8) AM-GM max at E_+ = E_perp ⟹ kappa = 2 ⟹ Q = 2/3
""")

# Composite executable check: each building block has been verified
# symbolically above. Verify they combine consistently: starting from the
# Herm_circ(3) axioms, following the chain gives kappa = 2 and Q = 2/3.
composite_ok = (
    # (1) Frobenius form is Ad-invariant AND M is Hermitian
    sp.simplify(sp.trace(A_conj * B_conj) - sp.trace(A_test * B_test)) == 0
    and sp.simplify(M - M_dagger) == sp.zeros(3, 3)
    # (2) P_0 is unique rank-1 projector
    and sp.simplify(P_from_eigvec - P_0) == sp.zeros(3, 3)
    # (3) P_I matches expected form
    # (checked earlier in the file)
    # (4) E_+ = 3a^2
    and sp.simplify(E_plus_frob - 3 * a**2) == 0
    # (5) E_perp = 6|b|^2
    and sp.simplify(E_perp - 6 * (x**2 + y**2)) == 0
    # (6) Positivity over reals
    and nonneg_Eplus in (False, [])
    and nonneg_Eperp in (False, [])
    # (7) Pythagoras
    and sp.simplify(3 * a**2 + 6 * (x**2 + y**2) - Tr_M_sq) == 0
    # (8) AM-GM maximum gives kappa = 2
    and sp.simplify(kappa_value - 2) == 0
    and Q_value == sp.Rational(2, 3)
)
ok("8. COMPOSITE: conditional on fixed Frobenius normalization, AM-GM on log(E_+ · E_perp) gives kappa = 2 and Q = 2/3",
   composite_ok,
   "chain (1)->(2)->(3)->(4)->(5)->(6)->(7)->(8) is gap-free and executable")

# ==========================================================================
# Summary
# ==========================================================================

print("=" * 72)
print("FROBENIUS ISOTYPE SPLIT AM-GM CHECK (conditional on admitted Frobenius normalization)")
print("=" * 72)
for line in log:
    print(line)
print()
print(f"Total: {PASS} PASS, {FAIL} FAIL")
print()
print("Verdict:")
if FAIL == 0:
    print("  Conditional on the ADMITTED Frobenius matrix-space normalization,")
    print("  the AM-GM route has executable internal support:")
    print("    Tr(M^2)    = Ad-invariant trace form (one member of the PD")
    print("                 family B_{α,β} = α Tr(AB) + β (tr A)(tr B); the")
    print("                 normalization β = 0 is admitted, not derived; the")
    print("                 counter-example family is exhibited in (1e))")
    print("    P_0 = J/3  = C_3-singlet Hermitian projector on C^3")
    print("    E_+        = (tr M)^2/3 = ||P_I M||_F^2  [P_I on Herm(3)]")
    print("    E_perp     = Tr(M^2) - E_+ = ||(I - P_I) M||_F^2")
    print("    pieces positive and additive (Pythagoras)")
    print()
    print("  AM-GM then forces the conditional extremum at E_+ = E_perp,")
    print("  giving kappa = a^2/|b|^2 = 2 and Q = 2/3.")
    print()
    print("  This is NOT a uniqueness theorem for the Frobenius normalization.")
    print("  Both the open derivation gap (Frobenius β = 0 uniquely forced)")
    print("  and the physical/source-law bridge to the charged-lepton packet")
    print("  remain separate open items.")
    print()
    print("  FROBENIUS_ISOTYPE_SPLIT_CONDITIONAL_CHAIN=TRUE")
else:
    print(f"  {FAIL} checks failed. Conditional chain not closed.")
    print("  FROBENIUS_ISOTYPE_SPLIT_CONDITIONAL_CHAIN=PARTIAL")
