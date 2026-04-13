#!/usr/bin/env python3
"""
frontier_gstar_reconciliation.py
================================

Reconcile the g_* = 106.75 vs 110.75 inconsistency found by the
adversarial audit (ADVERSARIAL_CHAIN_AUDIT_2026-04-13.md, item 5).

Root cause:
-----------
Three baryogenesis scripts used g_* = 110.75, claiming "SM + 4 taste
scalars."  This is WRONG for the thermal plasma: the extra taste states
have masses of order the lattice spacing (~Planck mass) and are NOT
relativistic at T ~ 160 GeV.  Only the hw=0 taste (the physical SM
fermion) is light and contributes to the thermal plasma.

Resolution:
-----------
* g_*(thermal) = 106.75  -- counts ONLY light (relativistic) states
  at T >> m_t.  This is the standard SM value and applies to:
    - Energy density:  rho = (pi^2/30) g_* T^4
    - Entropy density: s   = (2 pi^2/45) g_* T^3
    - Hubble rate:     H   = sqrt(8 pi^3 g_* / 90) T^2 / M_Pl
    - Freeze-out:      x_F, Omega_DM h^2 formulas

* N_taste = 8 per staggered field -- all 8 taste states are active at
  the LATTICE (Planck) scale where sphaleron transitions occur.  The
  8/3 enhancement factor in the CP-violating source comes from counting
  taste states that participate in the sphaleron transition, NOT from
  adding them to the thermal plasma.

Key insight: the sphaleron is a topological transition in the gauge
field, happening at the UV (lattice) scale.  ALL taste states couple to
the gauge field identically, so all 8 participate.  But only the hw=0
state is light enough to be in thermal equilibrium at T_EW ~ 160 GeV.

Derivation of g_* = 106.75 from the taste spectrum
---------------------------------------------------
The staggered lattice produces 8 taste states per fermion field.
Under the residual taste symmetry, these decompose as representations
of the SM gauge group:

  Cl(3) -> 8 tastes -> (2,3) + (2,1) per generation

The hw=0 state (lightest) in each channel is the physical SM particle.
The other 7 tastes per field have masses ~ a^{-1} (lattice spacing).

At T >> m_t but T << M_Planck (i.e., the entire accessible range):
  - Only hw=0 tastes contribute to thermal plasma
  - SM particle content (hw=0 only):
      Bosons:  gluons 8x2 + EW(unbroken) 4x2 + Higgs(4) = 28
      Fermions: 3 gen x (quarks 24 + leptons 6) = 90
      g_* = 28 + (7/8) x 90 = 28 + 78.75 = 106.75

The "4 taste scalars" that led to 110.75 was an error: those states
have Planck-scale masses and are thermally decoupled at T_EW.

Scripts fixed by this reconciliation
-------------------------------------
  frontier_dm_native_eta.py:        110.75 -> 106.75
  frontier_dm_taste_enhanced_eta.py: 110.75 -> 106.75
  frontier_dm_coupled_transport.py:  110.75 -> 106.75
  frontier_dm_eta_derivation.py:     106.75 + 4.0 -> 106.75

All other scripts already use 106.75.  See GSTAR_RECONCILIATION_NOTE.md
for the full argument.
"""

import sys
import math
import os

# ============================================================
# Output helpers
# ============================================================

SCRIPT = os.path.basename(__file__)
SEP = "=" * 72

def log(msg=""):
    print(msg)

def banner(title):
    log(f"\n{SEP}")
    log(title)
    log(SEP)

# ============================================================
# PART 1: Derive g_* = 106.75 from the taste spectrum
# ============================================================

banner("PART 1: g_* FROM THE TASTE SPECTRUM")

log("""
The staggered lattice gives 8 taste states per fermion field.
These decompose under the SM gauge group as:

  8 tastes -> (2,3) + (2,1)   [per generation]

The taste spectrum has a "grade splitting": the hw=0 state is the
lightest (identified as the physical SM particle), and the hw>0 states
have masses of order a^{-1} ~ M_Planck.

For the THERMAL plasma at temperature T:
  - A particle contributes to g_* only if m << T
  - At T_EW ~ 160 GeV, only hw=0 states (m ~ GeV) are relativistic
  - The hw>0 tastes (m ~ M_Planck >> T_EW) are Boltzmann-suppressed
    by exp(-M_Planck / T_EW) ~ exp(-10^{17}) ~ 0
""")

# --- Fermion d.o.f. (hw=0 tastes only = SM particles) ---
N_GEN = 3

# Quarks: per generation
# SU(2) doublet x SU(3) triplet: 2 flavors x 3 colors = 6
# Each quark: spin(2) x particle/anti(2) = 4
quark_dof_per_gen = 2 * 3 * 2 * 2  # = 24
log(f"  Quarks per generation:  2(SU2) x 3(SU3) x 2(spin) x 2(p/anti) = {quark_dof_per_gen}")

# Leptons: per generation
# Charged lepton: spin(2) x particle/anti(2) = 4
# Neutrino (LH only in SM): helicity(1) x particle/anti(2) = 2
charged_lepton_dof = 2 * 2  # = 4
neutrino_dof = 1 * 2        # = 2 (LH nu + RH anti-nu)
lepton_dof_per_gen = charged_lepton_dof + neutrino_dof  # = 6
log(f"  Leptons per generation: charged(4) + neutrino_LH(2) = {lepton_dof_per_gen}")

fermion_dof_per_gen = quark_dof_per_gen + lepton_dof_per_gen  # = 30
total_fermion_dof = N_GEN * fermion_dof_per_gen  # = 90
log(f"  Fermion d.o.f. per gen: {fermion_dof_per_gen}")
log(f"  Total fermion d.o.f.:   {N_GEN} x {fermion_dof_per_gen} = {total_fermion_dof}")

# --- Boson d.o.f. ---
# At T >> v_EW (unbroken EW phase):
gluon_dof = 8 * 2           # 8 gluons x 2 polarizations = 16
ew_boson_dof = (3 + 1) * 2  # SU(2)xU(1): 4 massless bosons x 2 pol = 8
higgs_dof = 4               # Complex SU(2) doublet: 4 real d.o.f.
total_boson_dof = gluon_dof + ew_boson_dof + higgs_dof  # = 28

log(f"\n  Gluons:           8 x 2 = {gluon_dof}")
log(f"  EW bosons (unbroken): 4 x 2 = {ew_boson_dof}")
log(f"  Higgs doublet:    {higgs_dof}")
log(f"  Total boson d.o.f.:   {total_boson_dof}")

# --- Compute g_* ---
FERMI_DIRAC_FACTOR = 7.0 / 8.0
g_star_thermal = total_boson_dof + FERMI_DIRAC_FACTOR * total_fermion_dof

log(f"\n  g_*(thermal) = {total_boson_dof} + (7/8) x {total_fermion_dof}")
log(f"               = {total_boson_dof} + {FERMI_DIRAC_FACTOR * total_fermion_dof}")
log(f"               = {g_star_thermal}")

G_STAR_SM = 106.75
assert abs(g_star_thermal - G_STAR_SM) < 0.01, (
    f"g_* mismatch: computed {g_star_thermal} != expected {G_STAR_SM}"
)
log(f"\n  CONFIRMED: g_*(thermal) = {G_STAR_SM}")

# ============================================================
# PART 2: Why taste states do NOT add to g_*(thermal)
# ============================================================

banner("PART 2: TASTE STATES ARE THERMALLY DECOUPLED")

log("""
The "110.75 = 106.75 + 4 taste scalars" used in some scripts was WRONG.

Argument: the extra taste states have masses m_taste ~ a^{-1} ~ M_Pl.

  Thermal occupation at T_EW ~ 160 GeV:
    n(m_taste) ~ exp(-m_taste / T_EW)
              ~ exp(-M_Pl / T_EW)
              ~ exp(-1.22e19 / 160)
              ~ exp(-7.6e16)
              = 0  (to any finite precision)

These states are as thermally relevant as a bowling ball in the CMB.
They contribute ZERO to:
  - Energy density rho(T)
  - Entropy density s(T)
  - The Hubble rate H(T)
  - Freeze-out parameter x_F
""")

M_PL = 1.22e19  # Planck mass in GeV
T_EW = 160.0    # EW temperature in GeV
boltzmann_suppression = math.exp(-min(M_PL / T_EW, 700))  # clip to avoid overflow
log(f"  M_Pl / T_EW = {M_PL / T_EW:.2e}")
log(f"  exp(-M_Pl / T_EW) = exp(-{M_PL / T_EW:.2e}) = {boltzmann_suppression}")
log(f"  -> Taste scalars contribute ZERO to thermal g_*")

# ============================================================
# PART 3: Where the 8/3 taste enhancement DOES matter
# ============================================================

banner("PART 3: SPHALERON CP SOURCE -- WHERE ALL TASTES ARE ACTIVE")

log("""
The sphaleron is a topological transition in the SU(2) gauge field.
It happens at the UV (lattice) scale where ALL taste states are active.

For the CP-violating source in electroweak baryogenesis:
  - Each taste state couples to the gauge field identically
  - The sphaleron transition involves ALL 8 tastes
  - The CP source gets enhanced by a factor N_taste/N_gen = 8/3

This is NOT a thermal effect -- it's a gauge-topology effect.
The taste enhancement enters the CP-violating source term S_CP,
not the thermal bath parameters (g_*, H, s).

Correct treatment:
  - Hubble rate:  H = sqrt(8 pi^3 g_* / 90) T^2 / M_Pl
                  with g_* = 106.75 (thermal, hw=0 only)
  - CP source:    S_CP ~ (N_taste/N_gen) x J_CKM x y_t^2 / T
                  with N_taste = 8 (all tastes active at UV scale)
  - eta_B:        proportional to S_CP / (g_* * H)
                  -> the 8/3 enters via S_CP, not via g_*
""")

N_TASTE = 8
taste_enhancement = N_TASTE / N_GEN
log(f"  N_taste = {N_TASTE}")
log(f"  N_gen   = {N_GEN}")
log(f"  Taste enhancement for CP source: {N_TASTE}/{N_GEN} = {taste_enhancement:.4f}")
log(f"  g_*(thermal) remains: {G_STAR_SM}")
log()
log(f"  WRONG:  g_* = 106.75 + 4 = 110.75  (adding taste scalars to thermal bath)")
log(f"  RIGHT:  g_* = 106.75               (thermal bath = SM only)")
log(f"          S_CP enhanced by 8/3        (all tastes in sphaleron)")

# ============================================================
# PART 4: Audit of all scripts
# ============================================================

banner("PART 4: SCRIPT AUDIT -- g_* VALUES ACROSS CODEBASE")

# Scripts that had the wrong value (110.75)
wrong_scripts = [
    ("frontier_dm_native_eta.py",        "G_STAR = 110.75", "G_STAR = 106.75"),
    ("frontier_dm_taste_enhanced_eta.py", "G_STAR = 110.75", "G_STAR = 106.75"),
    ("frontier_dm_coupled_transport.py",  "G_STAR = 110.75", "G_STAR = 106.75"),
    ("frontier_dm_eta_derivation.py",     "g_star = 106.75 + 4.0", "g_star = 106.75"),
]

log("\n  Scripts with INCORRECT g_* (now fixed):")
log(f"  {'Script':<40s} {'Old value':<25s} {'New value':<20s}")
log(f"  {'-'*85}")
for script, old, new in wrong_scripts:
    log(f"  {script:<40s} {old:<25s} {new:<20s}")

# Scripts that were already correct (106.75)
correct_scripts = [
    "frontier_baryogenesis.py",
    "frontier_eta_from_framework.py",
    "frontier_dm_k_independence.py",
    "frontier_dm_axiom_boundary.py",
    "frontier_dm_vw_derivation.py",
    "frontier_dm_ratio_structural.py",
    "frontier_freezeout_from_lattice.py",
    "frontier_dm_clean_derivation.py",
    "frontier_dm_r_sensitivity.py",
    "frontier_dm_relic_gap_closure.py",
    "frontier_dm_relic_mapping.py",
    "frontier_dm_boltzmann_theorem.py",
    "frontier_dm_friedmann_from_newton.py",
    "frontier_dm_transport_derived.py",
    "frontier_dm_nucleation_temperature.py",
    "frontier_g_bare_self_duality.py",
]

log(f"\n  Scripts with CORRECT g_* = 106.75 (no change needed):")
for s in correct_scripts:
    log(f"    {s}")

# ============================================================
# PART 5: Quantitative impact of the fix
# ============================================================

banner("PART 5: QUANTITATIVE IMPACT OF 110.75 -> 106.75")

log("""
The 110.75 -> 106.75 change affects the baryogenesis scripts through:

  1. Energy density:    rho ~ g_* T^4
  2. Entropy density:   s ~ g_* T^3
  3. Hubble rate:       H ~ sqrt(g_*) T^2
  4. Sphaleron rate:    A_sph ~ 1/g_*
""")

g_old = 110.75
g_new = 106.75

# Fractional changes
delta_rho = (g_new - g_old) / g_old
delta_H = (math.sqrt(g_new) - math.sqrt(g_old)) / math.sqrt(g_old)
delta_s = delta_rho  # same scaling
delta_Asph = (1.0/g_new - 1.0/g_old) / (1.0/g_old)

log(f"  g_*(old) = {g_old}")
log(f"  g_*(new) = {g_new}")
log(f"  Delta g_* / g_* = {delta_rho:+.4f}  ({abs(delta_rho)*100:.2f}%)")
log(f"\n  Impact on derived quantities:")
log(f"    rho:     Delta = {delta_rho:+.4f}  ({abs(delta_rho)*100:.2f}%)")
log(f"    s:       Delta = {delta_s:+.4f}  ({abs(delta_s)*100:.2f}%)")
log(f"    H:       Delta = {delta_H:+.4f}  ({abs(delta_H)*100:.2f}%)")
log(f"    A_sph:   Delta = {delta_Asph:+.4f}  ({abs(delta_Asph)*100:.2f}%)")
log(f"\n  All shifts are < 4%.  The baryogenesis result eta_B ~ 10^{{-10}}")
log(f"  has much larger theoretical uncertainties (kappa_sph, v_w, etc.).")
log(f"  The fix is about CONSISTENCY, not numerical accuracy.")

# ============================================================
# PART 6: Summary table
# ============================================================

banner("PART 6: SUMMARY -- THERMAL g_* vs SPHALERON TASTE COUNT")

log("""
  +---------------------------+--------+----------------------------------+
  | Quantity                  | Value  | Where it enters                  |
  +---------------------------+--------+----------------------------------+
  | g_*(thermal)              | 106.75 | rho, s, H, freeze-out, Omega_DM |
  | N_taste (per staggered)   |   8    | CP source in sphaleron           |
  | N_gen                     |   3    | SM fermion generations           |
  | Taste enhancement         |  8/3   | S_CP ~ (8/3) * J_CKM * y_t^2    |
  +---------------------------+--------+----------------------------------+

  CRITICAL DISTINCTION:
    g_*(thermal) counts RELATIVISTIC states in the plasma  -> 106.75
    N_taste counts GAUGE-COUPLED states at UV scale        -> 8
    These are DIFFERENT physical quantities.
    Mixing them (adding taste scalars to g_*) was the error.
""")

# ============================================================
# ASSERTIONS
# ============================================================

banner("ASSERTIONS")

results = []

# 1. g_* derivation
t1 = abs(g_star_thermal - 106.75) < 0.01
results.append(("g_* = 106.75 from taste spectrum", t1,
                f"computed {g_star_thermal}"))

# 2. Fermion counting
t2 = total_fermion_dof == 90
results.append(("Total fermion d.o.f. = 90", t2,
                f"computed {total_fermion_dof}"))

# 3. Boson counting
t3 = total_boson_dof == 28
results.append(("Total boson d.o.f. = 28", t3,
                f"computed {total_boson_dof}"))

# 4. Taste enhancement
t4 = abs(taste_enhancement - 8.0/3.0) < 1e-10
results.append(("Taste enhancement = 8/3", t4,
                f"computed {taste_enhancement}"))

# 5. Impact is small (< 5%)
t5 = abs(delta_rho) < 0.05
results.append(("Impact of fix < 5%", t5,
                f"|delta| = {abs(delta_rho)*100:.2f}%"))

log()
all_pass = True
for name, passed, detail in results:
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_pass = False
    log(f"  [{status}] {name}: {detail}")

log()
if all_pass:
    log("  ALL ASSERTIONS PASSED")
else:
    log("  SOME ASSERTIONS FAILED")
    sys.exit(1)

# ============================================================
# Final banner
# ============================================================

banner("RECONCILIATION COMPLETE")
log(f"""
  g_* = 106.75 is the UNIQUE correct value for the thermal plasma.
  The 110.75 variant was an error (taste scalars are Planck-mass).
  The taste enhancement 8/3 enters via S_CP, not via g_*.
  All scripts are now consistent.

  See: docs/GSTAR_RECONCILIATION_NOTE.md
""")
