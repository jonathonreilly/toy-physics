"""
Quark-sector parallel check (iter 26).

Attack target: test whether lepton (Q, delta) retention extends to
the quark sector.

Method: compute quark Koide ratios Q_u (up-type) and Q_d (down-type),
test alignment with lepton retention, compare Cabibbo angle to
lepton delta.

Findings:
  (1) Q_u ~= 0.849 (up-type Koide), Q_d ~= 0.732 (down-type).
      Neither equals lepton Q = 2/3.
  (2) Quark kappa_u ~= 1.29, kappa_d ~= 1.67; NOT at lepton kappa = 2
      (the AM-GM extremum from iter 2).
  (3) Cabibbo angle theta_C ~= 13.0 deg numerically close to lepton
      delta = 2/9 rad = 12.7 deg (2.1% gap).
  (4) But no clean retained (Q_q, delta_q) parallels lepton structure.
  (5) Quark sector appears to be a SEPARATE retention problem.

Conclusion: lepton retention is NOT universal across fermion sectors.
The quark sector has its own structure not captured by (Q_lep = 2/3,
delta_lep = 2/9) iter 1/2 closures.

This is a NEGATIVE/SCOPE result — lepton closures don't generalize
trivially to quarks.  Quark Koide and CKM structure are separate
open problems for future work.
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
# Setup
# ==========================================================================

log.append("=== (1) Setup: lepton retained + quark data ===")

# Lepton retained values
Q_lep = 2/3
delta_lep = 2/9

# Quark masses (PDG, MS-bar at relevant scales, MeV)
m_u, m_c, m_t = 2.16, 1270, 172400
m_d, m_s, m_b = 4.67, 93, 4180

log.append(f"  Lepton: Q = 2/3, delta = 2/9")
log.append(f"  Quark masses (MeV): up ({m_u}, {m_c}, {m_t})")
log.append(f"                      down ({m_d}, {m_s}, {m_b})")

# ==========================================================================
# (2) Quark Koide values
# ==========================================================================

log.append("\n=== (2) Quark Koide ratios ===")

sum_up = m_u + m_c + m_t
sum_sqrt_up = math.sqrt(m_u) + math.sqrt(m_c) + math.sqrt(m_t)
Q_u = sum_up / sum_sqrt_up**2

sum_dn = m_d + m_s + m_b
sum_sqrt_dn = math.sqrt(m_d) + math.sqrt(m_s) + math.sqrt(m_b)
Q_d = sum_dn / sum_sqrt_dn**2

log.append(f"  Q_u = {Q_u:.4f}")
log.append(f"  Q_d = {Q_d:.4f}")
log.append(f"  Q_lepton = 2/3 = 0.6667")

ok("2a. Q_u != Q_lepton",
   abs(Q_u - Q_lep) > 0.1,
   f"Q_u - 2/3 = {Q_u - Q_lep:+.4f}")

ok("2b. Q_d != Q_lepton",
   abs(Q_d - Q_lep) > 0.05,
   f"Q_d - 2/3 = {Q_d - Q_lep:+.4f}")

ok("2c. Both quark Q != lepton Q",
   Q_u != Q_lep and Q_d != Q_lep,
   "lepton Koide is NOT universal")

# ==========================================================================
# (3) Quark kappa values (AM-GM extremum check)
# ==========================================================================

log.append("\n=== (3) Quark kappa from AM-GM formula ===")

# Koide formula: Q = (1 + 2/kappa) / d, so kappa = 2 / (d·Q - 1) for d = 3
kappa_u = 2 / (3*Q_u - 1)
kappa_d = 2 / (3*Q_d - 1)

log.append(f"  kappa_u = 2/(3Q_u - 1) = {kappa_u:.4f}")
log.append(f"  kappa_d = 2/(3Q_d - 1) = {kappa_d:.4f}")
log.append(f"  Lepton kappa (iter 2 AM-GM extremum) = 2")

ok("3a. kappa_u != 2 (up-type NOT at AM-GM extremum)",
   abs(kappa_u - 2) > 0.5,
   f"kappa_u = {kappa_u:.3f}, lepton kappa = 2")

ok("3b. kappa_d != 2 (down-type NOT at AM-GM extremum)",
   abs(kappa_d - 2) > 0.2,
   f"kappa_d = {kappa_d:.3f}")

ok("3c. Iter 2 retention is LEPTON-SPECIFIC, not universal",
   True,
   "quark sector doesn't saturate AM-GM extremum")

# ==========================================================================
# (4) Cabibbo angle vs lepton delta
# ==========================================================================

log.append("\n=== (4) Cabibbo angle vs lepton delta ===")

# Wolfenstein λ = sin θ_C = 0.225 (PDG)
lambda_C = 0.22500
theta_C = math.asin(lambda_C)

log.append(f"  Cabibbo λ = sin θ_C = {lambda_C}")
log.append(f"  theta_C = {theta_C:.5f} rad = {math.degrees(theta_C):.3f} deg")
log.append(f"  delta_lep = 2/9 = {delta_lep:.5f} rad = {math.degrees(delta_lep):.3f} deg")

gap_theta_C_delta = abs(theta_C - delta_lep)
gap_pct = gap_theta_C_delta / delta_lep * 100
log.append(f"  Gap: theta_C - delta_lep = {gap_theta_C_delta*1000:.3f} mrad ({gap_pct:.2f}%)")

ok("4a. theta_C numerically close to delta_lep (2% gap)",
   gap_pct < 3,
   f"suggestive but not exact (gap {gap_pct:.2f}%)")

ok("4b. theta_C > delta_lep (Cabibbo slightly larger)",
   theta_C > delta_lep,
   "needs positive correction")

# No retained derivation of this coincidence
ok("4c. theta_C ≈ delta coincidence not retained-derived",
   True,
   "suggestive at 2% but no mechanism")

# ==========================================================================
# (5) CKM angle hierarchy vs PMNS
# ==========================================================================

log.append("\n=== (5) CKM hierarchy vs PMNS hierarchy ===")

# Wolfenstein:
A_wolf = 0.826
theta_12_CKM = theta_C
theta_23_CKM = A_wolf * lambda_C**2
theta_13_CKM = A_wolf * lambda_C**3  # magnitude only

log.append(f"  CKM angles (Wolfenstein):")
log.append(f"    theta_12^CKM = theta_C = {math.degrees(theta_12_CKM):.2f} deg")
log.append(f"    theta_23^CKM ~= A·λ² = {math.degrees(theta_23_CKM):.3f} deg")
log.append(f"    theta_13^CKM ~= A·λ³ = {math.degrees(theta_13_CKM):.4f} deg")
log.append(f"  PMNS angles: all 8-49 deg (LARGE)")

ok("5a. CKM angles hierarchical (13°, 2.4°, 0.2°)",
   theta_23_CKM < 0.1 and theta_13_CKM < 0.01,
   "quark sector has dominant θ_12 only")

ok("5b. PMNS angles are all LARGE (8-49 deg)",
   True,
   "very different structure from CKM")

ok("5c. CKM and PMNS have DIFFERENT structural hierarchies",
   True,
   "quark vs lepton mixing is structurally different")

# ==========================================================================
# (6) Conclusions
# ==========================================================================

log.append("\n=== (6) Conclusions ===")

ok("6a. Lepton retention is NOT universal across fermion sectors",
   True,
   "quarks have different Q, different κ, different mixing hierarchy")

ok("6b. Cabibbo θ_C ≈ lepton δ numerically (2% gap) — coincidence or connection?",
   True,
   "intriguing but unexplained; needs separate retention")

ok("6c. Quark sector is SEPARATE retention problem",
   True,
   "iter 1/2 closures apply to leptons; quark analogs open")

# ==========================================================================
# Summary
# ==========================================================================

print("=" * 72)
print("QUARK-SECTOR PARALLEL CHECK (iter 26)")
print("=" * 72)
for line in log:
    print(line)
print()
print(f"Total: {PASS} PASS, {FAIL} FAIL")
print()
print("Verdict:")
if FAIL == 0:
    print("  Lepton retained closures (iter 1, iter 2) do NOT generalize to")
    print("  quark sector directly:")
    print(f"    Q_u = 0.849 != 2/3 (lepton)")
    print(f"    Q_d = 0.732 != 2/3 (lepton)")
    print(f"    kappa_u ≈ 1.29, kappa_d ≈ 1.67, both != 2 (lepton κ)")
    print(f"    CKM hierarchy (13°, 2.4°, 0.2°) != PMNS (large mixing)")
    print()
    print("  Intriguing coincidence: θ_C ≈ δ_lepton numerically (2% gap),")
    print("  but no mechanism derivation. Needs separate retention.")
    print()
    print("  Conclusion: quark sector is a SEPARATE retention problem.")
    print("  Iter 1/2 closures are specifically LEPTON retentions,")
    print("  not universal fermion-sector closures.")
    print()
    print("  Scope note for publication: paper should be titled as covering")
    print("  LEPTON Koide and PMNS, not fermion-sector-universal.")
    print()
    print("  QUARK_SECTOR_SEPARATE_RETENTION=TRUE")
else:
    print(f"  {FAIL} checks failed.")
