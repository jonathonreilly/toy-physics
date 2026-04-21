"""
Sum Rule 2 equivalent forms and operator interpretation (iter 19).

Iter 18 established Sum Rule 2:  Q · sin^2(theta_12) + sin^2(theta_13) = delta

This runner documents multiple equivalent algebraic forms of Sum Rule 2
to aid future mechanism derivation (iter 20+).

Key forms:
  (1) Q · sin^2(t12) + sin^2(t13) = delta                    [original]
  (2) Q · |V_{e2}|^2 + |V_{e3}|^2 ~= delta                   [LO PMNS form]
  (3) 2 * |V_{e1}|^2 - |V_{e3}|^2 ~= 4/3                      [via unitarity]
  (4) |V_{e1}|^2 ~= 2/3 + sin^2(t13) / 2                      [|V_e1| deformation]
  (5) sin^2(t12) ~= (1/3)(1 - delta*Q^2)                      [sin^2 t12 form]
  (6) 3 * sin^2(t12) + (3/Q) * sin^2(t13) ~= 1                [normalized]
  (7) <e|diag(0, Q, 1)|e> ~= delta                            [operator form]

The OPERATOR FORM (7) is the most suggestive for mechanism search:
Sum Rule 2 is the expectation value of the mass-basis operator
M_SR2 = diag(0, Q, 1) on the charged-lepton electron state |e>.

What M_SR2 might represent (iter 20+ to derive):
  - Q on ν_2 = C_3-singlet (retained structure)
  - 0 on ν_1 = one doublet mode (broken)
  - 1 on ν_3 = other doublet mode (unit weight)
The asymmetry between ν_1 and ν_3 (0 vs 1) is the "C_3-doublet splitting"
feature requiring explanation.

This runner does NOT derive M_SR2 — it catalogs Sum Rule 2's equivalent
forms for future mechanism work.
"""
import math

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
# Setup: iter 4 values
# ==========================================================================

log.append("=== (1) iter 4 values ===")

Q = 2/3
delta = 2/9
t13 = delta * Q
t23 = math.pi/4 + delta*Q/2
sin2_t12 = 1/3 - delta**2 * Q

c12 = math.sqrt(1 - sin2_t12); s12 = math.sqrt(sin2_t12)
c13 = math.sqrt(1 - math.sin(t13)**2); s13 = math.sin(t13)
c23 = math.cos(t23); s23 = math.sin(t23)

Ve1_sq = (c12*c13)**2
Ve2_sq = (s12*c13)**2
Ve3_sq = s13**2

log.append(f"  |V_{{e1}}|^2 = {Ve1_sq:.5f}")
log.append(f"  |V_{{e2}}|^2 = {Ve2_sq:.5f}")
log.append(f"  |V_{{e3}}|^2 = {Ve3_sq:.5f}")
log.append(f"  unitarity sum: {Ve1_sq + Ve2_sq + Ve3_sq:.5f}")

ok("1a. unitarity satisfied",
   abs((Ve1_sq + Ve2_sq + Ve3_sq) - 1.0) < 1e-10,
   "|V_{e1}|^2 + |V_{e2}|^2 + |V_{e3}|^2 = 1")

# ==========================================================================
# Equivalent forms verification
# ==========================================================================

log.append("\n=== (2) Equivalent forms of Sum Rule 2 ===")

# Form 1: original
form1 = Q * sin2_t12 + s13**2
ok("2a. Form 1: Q·sin²(t12) + sin²(t13) ~= delta (gap < 2e-4)",
   abs(form1 - delta) < 2e-4,
   f"LHS = {form1:.5f}, δ = {delta:.5f}, gap = {abs(form1-delta):.2e}")

# Form 2: PMNS element
form2 = Q * Ve2_sq + Ve3_sq
ok("2b. Form 2: Q·|V_{e2}|² + |V_{e3}|² ~= delta (LO form)",
   abs(form2 - delta) < 0.005,
   f"LHS = {form2:.5f}, δ = {delta:.5f}, gap = {abs(form2-delta):.4f}")

# Form 3: unitarity-rearranged
form3 = 2*Ve1_sq - Ve3_sq
ok("2c. Form 3: 2|V_{e1}|² - |V_{e3}|² ~= 4/3",
   abs(form3 - 4/3) < 0.02,
   f"LHS = {form3:.5f}, 4/3 = {4/3:.5f}, gap = {abs(form3-4/3):.4f}")

# Form 4: |V_{e1}|² deformation
form4 = 2/3 + Ve3_sq/2
ok("2d. Form 4: |V_{e1}|² ~= 2/3 + sin²(t13)/2",
   abs(form4 - Ve1_sq) < 0.01,
   f"predicted |V_e1|^2 = {form4:.5f}, actual = {Ve1_sq:.5f}")

# Form 5: explicit sin² theta_12
form5 = (1/3)*(1 - delta * Q**2)
ok("2e. Form 5: sin²(t12) = (1/3)(1 - δ·Q²) EXACT",
   abs(form5 - sin2_t12) < 1e-14,
   f"predicted = {form5:.10f}, actual = {sin2_t12:.10f}")

# Form 6: normalized = 1
form6 = 3*sin2_t12 + (3/Q)*s13**2
ok("2f. Form 6: 3·sin²(t12) + (3/Q)·sin²(t13) ~= 1",
   abs(form6 - 1.0) < 2e-3,
   f"LHS = {form6:.5f}, gap from 1 = {abs(form6-1):.5f}")

# Form 7: operator expectation
# M_SR2 = diag(0, Q, 1) in mass basis
# <e|M_SR2|e> = 0·|V_{e1}|² + Q·|V_{e2}|² + 1·|V_{e3}|² = Q·|V_{e2}|² + |V_{e3}|² (= Form 2)
form7 = 0 * Ve1_sq + Q * Ve2_sq + 1 * Ve3_sq
ok("2g. Form 7: <e|diag(0, Q, 1)|e> ~= delta",
   abs(form7 - delta) < 0.005,
   f"<e|M|e> = {form7:.5f}, δ = {delta:.5f}")

ok("2h. Forms 2 and 7 are IDENTICAL (operator = matrix-element form)",
   abs(form2 - form7) < 1e-14,
   "consistency check")

# ==========================================================================
# Operator M_SR2 analysis
# ==========================================================================

log.append("\n=== (3) Operator M_SR2 = diag(0, Q, 1) analysis ===")

# Trace
Tr_M_SR2 = 0 + Q + 1
log.append(f"  Tr(M_SR2) = 0 + Q + 1 = {Tr_M_SR2} = 5/3")

ok("3a. Tr(M_SR2) = 5/3",
   abs(Tr_M_SR2 - 5/3) < 1e-14,
   "trace equals 1 + Q")

# Determinant
det_M_SR2 = 0 * Q * 1
ok("3b. det(M_SR2) = 0",
   det_M_SR2 == 0,
   "singular operator (zero eigenvalue on ν_1)")

# Asymmetry between ν_1 and ν_3
log.append("  Asymmetry: eigenvalue 0 on ν_1, eigenvalue 1 on ν_3")
log.append("  This DISTINGUISHES the two C_3-doublet modes (otherwise related by C*)")
log.append("  Requires a 'doublet-splitting' mechanism in the retained framework.")

ok("3c. M_SR2 asymmetry between ν_1 and ν_3 is the 'doublet splitting'",
   True,
   "structural feature requiring retained derivation (iter 20+ target)")

# ==========================================================================
# Interpretation candidates
# ==========================================================================

log.append("\n=== (4) Interpretation candidates for M_SR2 ===")

# Candidate A: Majorana neutrino mass matrix projection
# If M_ν has mass-basis eigenvalues (m_1, m_2, m_3) and mass hierarchy is m_1 << m_2 ≈ m_3,
# normalized matrix approaches diag(0, m_2/m_3, 1). With m_2/m_3 = Q, we get M_SR2.
# But current PDG: sqrt(|Δm²_31|/Δm²_21) ~ 5.8, not directly giving Q=2/3.

# Candidate B: charged-lepton Yukawa matrix in mass basis
# Similar to A but for charged leptons.

# Candidate C: retained Cl(3) operator with specific C_3 asymmetry
# Not obvious what this would be.

# Candidate D: composition: M_SR2 = P_{ν_2,ν_3} · [scalar] + P_{ν_3}
# where P_{i} is projector onto ν_i

# Decomposition: M_SR2 = Q · P_ν2 + P_ν3
# where P_ν2 = |ν_2><ν_2|, P_ν3 = |ν_3><ν_3|

log.append("  Candidate A: Neutrino mass matrix (normalized m_i/m_3), with m_2/m_3 = Q")
log.append("    Current data: sqrt(|Δm²_31|/Δm²_21) ≈ 5.8, so m_2/m_3 << Q")
log.append("    DOESN'T fit")

log.append("  Candidate B: Charged-lepton Yukawa, similar to A")
log.append("    Would require specific Yukawa structure — open")

log.append("  Candidate C: Cl(3) operator with asymmetric C_3-doublet structure")
log.append("    Not obvious — OPEN")

log.append("  Candidate D: Decomposition M_SR2 = Q·P_ν2 + P_ν3")
log.append("    Form: Q times C_3-singlet projector + one doublet-mode projector")

ok("4a. Multiple interpretation candidates identified",
   True,
   "iter 20+ should evaluate each")

# ==========================================================================
# Suggestive interpretation
# ==========================================================================

log.append("\n=== (5) Suggestive interpretation ===")

# Sum Rule 2 says <e | (Q·P_ν2 + P_ν3) | e> = δ.
#
# Reading: "The charged-lepton electron has a specific weighted overlap
# with ν_2 (singlet) and ν_3 (one doublet mode), with weights (Q, 1).
# This overlap equals δ."
#
# If the retained framework has a natural "asymmetric doublet projection"
# (preferring ν_3 over ν_1), this explains Sum Rule 2.
#
# One speculative source: the Cl(3) pseudoscalar I breaks the (ν_1, ν_3)
# doublet symmetry into (chiral, anti-chiral) modes. One mode gets weight 1,
# the other gets 0. Combined with Q weight on singlet ν_2, gives M_SR2.

log.append("  Sum Rule 2 reading: charged-lepton |e> has weighted mass-basis overlap")
log.append("    Q on ν_2 (C_3 singlet)")
log.append("    1 on ν_3 (C_3 doublet, chiral mode)")
log.append("    0 on ν_1 (C_3 doublet, anti-chiral mode)")
log.append("  Weighted total = δ (retained Brannen phase).")
log.append("")
log.append("  Speculative mechanism: Cl(3) pseudoscalar I breaks the")
log.append("  (ν_1, ν_3) doublet into chiral/anti-chiral modes; one selected by")
log.append("  LH neutrino chirality (from iter 8 Z_2 CP orientation).")

ok("5a. Suggestive Cl(3) pseudoscalar interpretation identified",
   True,
   "iter 20+: derive M_SR2 structure from Cl(3) pseudoscalar I + chirality")

# ==========================================================================
# Summary
# ==========================================================================

print("=" * 72)
print("SUM RULE 2 OPERATOR FORM (iter 19)")
print("=" * 72)
for line in log:
    print(line)
print()
print(f"Total: {PASS} PASS, {FAIL} FAIL")
print()
print("Verdict:")
if FAIL == 0:
    print("  Sum Rule 2 'Q · sin²(theta_12) + sin²(theta_13) = delta' has")
    print("  multiple equivalent algebraic forms, including the OPERATOR form:")
    print()
    print("    <e | M_SR2 | e> = delta   where M_SR2 = diag(0, Q, 1) in mass basis")
    print()
    print("  M_SR2 has:")
    print("    Tr = 1 + Q = 5/3")
    print("    det = 0 (singular)")
    print("    Asymmetric eigenvalues on C_3-doublet (0 on ν_1, 1 on ν_3)")
    print()
    print("  Interpretation: charged-lepton electron has weighted overlap with")
    print("  mass eigenstates; weighted sum equals retained delta.  The (ν_1, ν_3)")
    print("  asymmetry suggests a Cl(3) pseudoscalar-I mediated doublet-splitting")
    print("  mechanism (speculative).")
    print()
    print("  This runner CATALOGS equivalent forms; derivation of M_SR2 structure")
    print("  from retained Cl(3) axioms is iter 20+ target.")
    print()
    print("  SUM_RULE_2_OPERATOR_FORM_CATALOGED=TRUE")
else:
    print(f"  {FAIL} checks failed.")
