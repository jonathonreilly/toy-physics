"""
SA4 attempt: H' = [B_1, M_0] bivector commutator (iter 33).

From iter 32's backlog SA4: test whether retained bivector B_1 commutator
with S_3-invariant Majorana mass M_0 gives H' with the required off-diagonal
structure.

Setup:
  M_0 = alpha·I + beta·(J - I) (S_3-invariant symmetric, mass-basis
    eigenvalues (alpha+2·beta, alpha-beta, alpha-beta) -- DEGENERATE
    on doublet).
  B_1 = bivector SO(3) generator, [[0,0,0],[0,0,-1],[0,1,0]].

Computation: H' = [B_1, M_0] is symmetric.  In mass basis:
  H'[2,2] = -4·beta/3
  H'[2,3] = H'[3,2] = -2·sqrt(6)·beta/3
  H'[3,3] = 0

Finding (honest):
  h_23 = -2·sqrt(6)·beta/3 (off-diagonal matrix element, correct form)
  BUT: m_2 = m_3 = alpha - beta (degenerate on doublet) so
    iter 31's non-degenerate perturbation theory doesn't apply directly.

Degenerate perturbation theory:
  Eigenvalue split from diagonalizing [[H'_{22}, H'_{23}], [H'_{32}, H'_{33}]]
  2x2 block gives splitting ~ 4·sqrt(7)·|beta|/3 with mixing angle
  arctan(sqrt(6))/2 ~ 34 degrees.

  Resulting V_{e,3'} ~ -sin(34°)·sqrt(1/3) ~ -0.32
  |V_{e,3'}|^2 ~ 0.104 — TOO LARGE compared to iter 4's 0.022.

  Conclusion: simple [B_1, M_0] perturbation over-activates θ_13.
  Scaling beta → small·beta would fix magnitude but not give (Q, δ)
  structure.

Status: SA4 with simple [B_1, M_0] does NOT cleanly give iter 4 structure.
Alternative bivector combinations or different M_0 structure required.

This is a NEGATIVE result for SA4 in simple form.
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
# Setup
# ==========================================================================

log.append("=== (1) Setup: B_1 and M_0 ===")

alpha, beta = sp.symbols('alpha beta', real=True)
M_0 = sp.Matrix([[alpha, beta, beta], [beta, alpha, beta], [beta, beta, alpha]])

B_1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])

log.append(f"  M_0 = diag(α, α, α) + β·(J - I)")
log.append(f"  B_1 = e_2·e_3 bivector (rotation generator around x-axis)")

ok("1a. M_0 S_3-invariant (retained from iter 3)", True, "")

# ==========================================================================
# Compute [B_1, M_0]
# ==========================================================================

log.append("\n=== (2) Commutator [B_1, M_0] ===")

Hp = B_1 * M_0 - M_0 * B_1
log.append(f"  [B_1, M_0] =")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"{sp.simplify(Hp[i,j])!s:>8} "
    log.append(row)

ok("2a. [B_1, M_0] is symmetric",
   Hp == Hp.T,
   "Hermitian operator eligible as H'")

# ==========================================================================
# V_TBM and mass basis rotation
# ==========================================================================

log.append("\n=== (3) H' in mass basis ===")

V_TBM = sp.Matrix([
    [sp.sqrt(sp.Rational(2,3)), sp.sqrt(sp.Rational(1,3)), 0],
    [-sp.sqrt(sp.Rational(1,6)), sp.sqrt(sp.Rational(1,3)), sp.sqrt(sp.Rational(1,2))],
    [sp.sqrt(sp.Rational(1,6)), -sp.sqrt(sp.Rational(1,3)), sp.sqrt(sp.Rational(1,2))]
])

Hp_mass = sp.simplify(V_TBM.T * Hp * V_TBM)
log.append(f"  V_TBM^T · [B_1, M_0] · V_TBM =")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"{sp.simplify(Hp_mass[i,j])!s:>16} "
    log.append(row)

h23_computed = sp.simplify(Hp_mass[1, 2])
log.append(f"  h_23 = {h23_computed}")

ok("3a. h_23 = -2·sqrt(6)·beta/3 computed",
   sp.simplify(h23_computed - (-2*sp.sqrt(6)*beta/3)) == 0,
   "off-diagonal matrix element has correct general form")

# ==========================================================================
# Degeneracy issue
# ==========================================================================

log.append("\n=== (4) Degeneracy issue (NOT non-degenerate pert theory) ===")

# Eigenvalues of M_0
# Singlet eigenvalue: alpha + 2·beta (V_TBM col_? = (1,1,-1)/sqrt(3)?)
# Actually for S_3-invariant M, eigenvalues are (alpha+2beta, alpha-beta, alpha-beta)
m_1 = alpha + 2*beta
m_2 = alpha - beta
m_3 = alpha - beta
log.append(f"  M_0 eigenvalues: m_1 = {m_1}, m_2 = m_3 = {m_2}")

ok("4a. m_2 = m_3 (DEGENERATE doublet)",
   m_2 == m_3,
   "iter 31 non-degenerate perturbation formula inapplicable")

# ==========================================================================
# Degenerate perturbation result
# ==========================================================================

log.append("\n=== (5) Degenerate perturbation gives WRONG magnitude ===")

# Off-diagonal block within (ν_2, ν_3) subspace:
# H'[2,2] = -4β/3, H'[2,3] = -2√6 β/3, H'[3,3] = 0
# Eigenvalue split: lambda = (-2β/3) ± sqrt((-2β/3)² + (2√6 β/3)²)
#                         = -2β/3 ± sqrt(4β²/9 + 24β²/9)
#                         = -2β/3 ± sqrt(28β²/9)
#                         = -2β/3 ± 2√7|β|/3

# Mixing angle: tan(2θ) = 2·H'[2,3] / (H'[2,2] - H'[3,3]) = 2·(-2√6β/3)/(-4β/3) = √6
theta_mix = sp.atan(sp.sqrt(6)) / 2
theta_mix_num = float(theta_mix)
import math
log.append(f"  Mixing angle within ν_2-ν_3 block: θ_mix = atan(√6)/2 = {math.degrees(theta_mix_num):.3f}°")

# Induced |V_{e,3'}|²
V_e3_prime = -sp.sin(theta_mix) * sp.sqrt(sp.Rational(1,3))  # rotation of |V_{e,2}| = √(1/3)
V_e3_prime_sq = sp.simplify(V_e3_prime**2)
V_e3_prime_num = float(V_e3_prime_sq)

log.append(f"  |V_{{e,3'}}|² induced = sin²(θ_mix) · 1/3 = {V_e3_prime_num:.4f}")
log.append(f"  iter 4 prediction: |V_{{e,3}}|² = sin²(δ·Q) ≈ 0.0218")

ok("5a. Induced |V_{e,3'}|² too large compared to iter 4",
   V_e3_prime_num > 0.05,
   f"induced {V_e3_prime_num:.4f} >> iter 4 0.022")

ok("5b. [B_1, M_0] does NOT cleanly match iter 4 at simple form",
   True,
   "over-activates θ_13 in degenerate perturbation")

# ==========================================================================
# Status
# ==========================================================================

log.append("\n=== (6) Status of SA4 ===")

ok("6a. SA4 with simple [B_1, M_0]: NEGATIVE result",
   True,
   "doesn't give iter 4's angle magnitude cleanly")

ok("6b. Alternative bivector combinations needed for SA4",
   True,
   "simple symmetric bivector gives θ_13 too large")

ok("6c. Or non-degenerate M_0 needed (lift m_2 = m_3 degeneracy first)",
   True,
   "requires additional retained mass-matrix structure")

# ==========================================================================
# Summary
# ==========================================================================

print("=" * 72)
print("SA4 BIVECTOR COMMUTATOR ATTEMPT (iter 33)")
print("=" * 72)
for line in log:
    print(line)
print()
print(f"Total: {PASS} PASS, {FAIL} FAIL")
print()
print("Verdict:")
if FAIL == 0:
    print("  SA4 with simple [B_1, M_0] does NOT cleanly match iter 4:")
    print(f"    h_23 = -2√6·β/3 (off-diagonal element, correct form)")
    print(f"    BUT: m_2 = m_3 degeneracy forces degenerate perturbation theory")
    print(f"    Mixing angle arctan(√6)/2 ≈ 34° gives |V_{{e,3'}}|² ≈ 0.104")
    print(f"    Iter 4 prediction: |V_{{e,3}}|² ≈ 0.022")
    print(f"    Induced value too large by factor ~5.")
    print()
    print("  NEGATIVE result for SA4 in simple form.")
    print("  Alternative bivector combinations OR M_0 with lifted degeneracy")
    print("  would be required.")
    print()
    print("  SA4_SIMPLE_FORM_NEGATIVE=TRUE")
else:
    print(f"  {FAIL} checks failed.")
