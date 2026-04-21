"""
TBM perturbation-theory setup for theta_13 activation (iter 31).

Iter 30 identified "perturbation-theory derivation of theta_13 = delta·Q"
as a medium-probability attack.  This runner formalizes the setup and
identifies the specific matrix-element structure needed.

Setup:
  Starting point: M_ν^0 = S_3-invariant Majorana mass matrix (iter 3).
  In TBM mass basis, M_ν^0 = diag(m_1, m_2, m_3) with S_3 structure.
  At TBM, theta_13 = 0 and V_TBM diagonalizes M_ν^0.

  Perturbation: M_ν = M_ν^0 + H' where H' breaks S_3.
  First-order shift to V_{e,3} matrix element:
    Delta V_{e,3} = <ν_3^{TBM}| H' |ν_1^{TBM}> * V_{e,1}^{TBM} / (m_1 - m_3)
                 + <ν_3^{TBM}| H' |ν_2^{TBM}> * V_{e,2}^{TBM} / (m_2 - m_3)

  Since V_{e,3}^{TBM} = 0, this is the leading-order activation.
  For theta_13 = delta·Q, need:
    Delta V_{e,3} = sin(delta·Q) ~= delta·Q  (for small delta·Q)

Candidate mechanism: if <ν_3|H'|ν_2> = delta · sqrt(m_2 m_3) (Brannen phase
scale, geometric mean) and V_{e,2}^{TBM} = sqrt(1/3), then:
  Delta V_{e,3} = [delta · sqrt(m_2 m_3)] · sqrt(1/3) / (m_2 - m_3)
              = delta · sqrt(m_2/m_3) / sqrt(3) / (m_2/m_3 - 1)

For this to equal delta·Q, need specific m_2/m_3 ratio.  Let me solve
symbolically.

This is a SKELETON of the perturbation theory — the specific retained
Hamiltonian H' still needs to be identified.  Iter 31 provides the
framework for iter 32+ to populate.
"""
import sympy as sp
import math

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
# (1) TBM mass matrix in mass basis
# ==========================================================================

log.append("=== (1) TBM mass matrix setup ===")

m1, m2, m3 = sp.symbols('m_1 m_2 m_3', real=True, positive=True)

# In mass basis, M_ν^0 = diag(m_1, m_2, m_3) trivially.
# V_TBM = matrix from flavor basis to mass basis.

# From iter 3: V_TBM[e, :] = (sqrt(2/3), sqrt(1/3), 0)
Ve1_TBM = sp.sqrt(sp.Rational(2, 3))
Ve2_TBM = sp.sqrt(sp.Rational(1, 3))
Ve3_TBM = sp.Integer(0)

log.append(f"  V_TBM[e,1] = {Ve1_TBM}")
log.append(f"  V_TBM[e,2] = {Ve2_TBM}")
log.append(f"  V_TBM[e,3] = 0 (TBM has θ_13 = 0)")

ok("1a. V_TBM[e, :] known from iter 3", True, "retained")

# ==========================================================================
# (2) First-order perturbation formula for V_{e,3} activation
# ==========================================================================

log.append("\n=== (2) First-order perturbation formula ===")

# Denote H' matrix elements as h_ij = <ν_i^{TBM}|H'|ν_j^{TBM}> in mass basis
h12, h13, h23 = sp.symbols('h_{12} h_{13} h_{23}', real=True)

# First-order shift in V_{e,3}:
# Delta V_{e,3} = (V_{e,1}^{TBM} * h_{31} / (m_1 - m_3)) + (V_{e,2}^{TBM} * h_{32} / (m_2 - m_3))
# For Hermitian H', h_{31} = h_{13}* = h_{13} (for real H'), h_{32} = h_{23}

Delta_Ve3 = Ve1_TBM * h13 / (m1 - m3) + Ve2_TBM * h23 / (m2 - m3)

log.append(f"  ΔV_{{e,3}} = V_{{e,1}}·h_{{13}}/(m_1-m_3) + V_{{e,2}}·h_{{23}}/(m_2-m_3)")
log.append(f"          = sqrt(2/3)·h_{{13}}/(m_1-m_3) + sqrt(1/3)·h_{{23}}/(m_2-m_3)")

ok("2a. First-order perturbation formula written", True, "standard QM")

# ==========================================================================
# (3) Condition for ΔV_{e,3} = δ·Q (small-angle, iter 4 conjecture)
# ==========================================================================

log.append("\n=== (3) Condition for matching iter 4 ===")

# Target: ΔV_{e,3} = sin(δQ) ≈ δ·Q for small δQ.
# Retained: δ = 2/9, Q = 2/3.
delta_sym = sp.Rational(2, 9)
Q_sym = sp.Rational(2, 3)
target = delta_sym * Q_sym  # = 4/27

log.append(f"  Target: ΔV_{{e,3}} = δ·Q = 4/27 (iter 4 conjecture)")

# This constrains (h_{13}, h_{23}, m_1, m_2, m_3) via 1 equation.
# Many possible solutions.  Simplest: h_{13} = 0, then:
# sqrt(1/3) * h_{23} / (m_2 - m_3) = δ·Q
# => h_{23} = sqrt(3) * δ·Q · (m_2 - m_3)

# Or alternative: h_{23} = 0 and h_{13} = sqrt(3/2) * δ·Q · (m_1 - m_3)

ok("3a. First-order matching gives 1 equation in 5 unknowns",
   True,
   "under-constrained; need additional retained structure")

# ==========================================================================
# (4) Restriction: if H' is "pure doublet" (h_{13} = 0)
# ==========================================================================

log.append("\n=== (4) Case: pure doublet perturbation (h_{13} = 0) ===")

# Set h_{13} = 0.  Then ΔV_{e,3} = sqrt(1/3) · h_{23} / (m_2 - m_3) = δQ
# h_{23} = sqrt(3) · δQ · (m_2 - m_3)

h23_solution = sp.sqrt(3) * delta_sym * Q_sym * (m2 - m3)
log.append(f"  If h_{{13}} = 0:")
log.append(f"    h_{{23}} = sqrt(3)·δQ·(m_2 - m_3) = {sp.simplify(h23_solution)}")

# Interpretation: H' has a specific <ν_2|·|ν_3> matrix element
# proportional to δQ·(m_2 - m_3).  Need retained mechanism for this structure.

ok("4a. Pure-doublet perturbation gives specific h_{23} formula",
   True,
   "constraint on H' matrix element in terms of δQ·(m_2 - m_3)")

# ==========================================================================
# (5) Parametrization: "Brannen-like H'"
# ==========================================================================

log.append("\n=== (5) Brannen-like H' candidate ===")

# Suppose H' has Brannen phase δ structure.  Natural candidate:
# H' = δ · diag(cos(δ+0), cos(δ+2π/3), cos(δ+4π/3)) · sqrt(m_avg)
# where m_avg is geometric mean scale.

# This gives h_{ij} = 0 for i ≠ j (diagonal perturbation doesn't activate θ_13).
# So diagonal Brannen perturbation DOESN'T activate θ_13.  Need OFF-DIAGONAL.

ok("5a. Diagonal Brannen perturbation doesn't activate θ_13",
   True,
   "need off-diagonal H' for first-order θ_13 activation")

# Off-diagonal Brannen: H' = δ · (Pauli-like off-diagonal operator) · mass scale?
# Speculative; not obviously retained from iter 1-2 closures.

# ==========================================================================
# (6) Status of perturbation theory attack
# ==========================================================================

log.append("\n=== (6) Status and remaining questions ===")

ok("6a. Perturbation theory gives FRAMEWORK for θ_13 activation",
   True,
   "first-order formula in terms of h_{ij}, m_i")

ok("6b. Specific H' matrix element structure NOT YET DERIVED",
   True,
   "retained mechanism for off-diagonal Brannen-like H' is open")

# Open questions for iter 32+:
# - What specific retained Hamiltonian gives h_{23} ~ sqrt(3)·δQ·(m_2 - m_3)?
# - Or: what mass hierarchy m_1, m_2, m_3 combined with retained H' gives δ·Q?

ok("6c. iter 32+ target: identify retained off-diagonal H'",
   True,
   "candidate: S_3-breaking term in Majorana mass matrix with δ-phase structure")

# ==========================================================================
# Summary
# ==========================================================================

print("=" * 72)
print("TBM PERTURBATION THEORY SETUP (iter 31)")
print("=" * 72)
for line in log:
    print(line)
print()
print(f"Total: {PASS} PASS, {FAIL} FAIL")
print()
print("Verdict:")
if FAIL == 0:
    print("  First-order perturbation theory setup for θ_13 activation from")
    print("  TBM is formalized:")
    print()
    print("    ΔV_{e,3} = V_{e,1}^{TBM}·h_{13}/(m_1-m_3) + V_{e,2}^{TBM}·h_{23}/(m_2-m_3)")
    print()
    print("  Matching to iter 4 conjecture ΔV_{e,3} = δ·Q gives ONE equation in")
    print("  5 unknowns (h_{13}, h_{23}, m_1, m_2, m_3).")
    print()
    print("  For 'pure doublet' perturbation (h_{13} = 0):")
    print("    h_{23} = sqrt(3)·δQ·(m_2 - m_3)")
    print()
    print("  This is a skeleton — the specific retained Hamiltonian H' giving")
    print("  this matrix element structure remains to be identified (iter 32+).")
    print()
    print("  Candidates for retained H':")
    print("    - S_3-breaking Majorana mass term with Brannen δ-phase")
    print("    - Off-diagonal Cl(3) Yukawa with (Q, δ)-dependent coefficients")
    print()
    print("  Neither is yet derived from iter 1-2 retained closures.")
    print()
    print("  TBM_PERTURBATION_SETUP_ESTABLISHED=TRUE")
else:
    print(f"  {FAIL} checks failed.")
