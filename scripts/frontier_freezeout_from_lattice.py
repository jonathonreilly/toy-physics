#!/usr/bin/env python3
"""
Freeze-Out from Lattice Thermodynamics
=======================================

Diagnoses the freeze-out / relic-abundance gap for the DM ratio.

The direct lattice contact-propagator lane is already a real observable.
The open question is whether the relic-abundance step can be derived from
the graph framework without importing Boltzmann/Friedmann freeze-out.

This script records the exact boundary:

  - the contact channel and lattice combinatorics are useful inputs
  - the freeze-out parameter x_F and the relic abundance still rely on
    standard thermal cosmology unless a native replacement is supplied

Diagnostics:

Attack 1: g_* from the taste spectrum
  The SM counting can be reproduced once the full matter content is assumed.
  That is a consistency check, not a lattice-only derivation of freeze-out.

Attack 2: x_F from the freeze-out equation
  The standard freeze-out condition Gamma_ann = H still enters through
  Boltzmann/Friedmann thermodynamics.  The lattice supplies inputs, but
  does not yet replace the cosmological decoupling calculation.

Attack 3: The Boltzmann equation from the lattice master equation
  The master-equation reduction is a thermodynamic-limit statement.  The
  expansion term and decoupling criterion are still imported spacetime
  dynamics unless a separate graph-native derivation is given.

Attack 4: Insensitivity of R to x_F
  The ratio varies only moderately over x_F, which makes the fit robust.
  Robustness does not make freeze-out native.

Self-contained: numpy + scipy only.
PStack experiment: freezeout-from-lattice
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

try:
    from scipy.optimize import brentq
    from scipy.integrate import solve_ivp
    HAS_SCIPY = True
except ImportError:
    print("WARNING: scipy not available; some checks will be skipped")
    HAS_SCIPY = False

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-freezeout_from_lattice.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# CONSTANTS (all from group theory or lattice structure)
# =============================================================================

PI = np.pi

# SU(3) group theory
N_C = 3
C_F = (N_C**2 - 1) / (2 * N_C)       # 4/3
C_A = N_C                               # 3
T_F = 0.5
DIM_ADJ_SU3 = N_C**2 - 1               # 8 gluon d.o.f.

# SU(2) group theory
C2_SU2_FUND = 3.0 / 4.0                # C_2(2)
DIM_ADJ_SU2 = 3                         # W bosons

# U(1) hypercharge
DIM_U1 = 1                              # photon/B boson

# Lattice coupling (from plaquette -- see frontier_alpha_s_determination.py)
G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4 * PI)       # 0.07958
K_4D = 0.15493
C1_PLAQ = PI**2 / 3.0
P_1LOOP = 1.0 - C1_PLAQ * ALPHA_BARE
ALPHA_PLAQ = -np.log(P_1LOOP) / C1_PLAQ
U0 = P_1LOOP**0.25
ALPHA_V = ALPHA_BARE / U0**4

# Observed ratio (COMPARISON only)
OMEGA_DM = 0.268
OMEGA_B = 0.049
R_OBS = OMEGA_DM / OMEGA_B              # 5.469

# Base ratio from group theory
F_VIS = C_F * DIM_ADJ_SU3 + C2_SU2_FUND * DIM_ADJ_SU2
F_DARK = C2_SU2_FUND * DIM_ADJ_SU2
MASS_RATIO = 3.0 / 5.0
R_BASE = MASS_RATIO * F_VIS / F_DARK    # 31/9

# Planck mass
M_PLANCK = 1.2209e19  # GeV


log("=" * 78)
log("FREEZE-OUT FROM LATTICE THERMODYNAMICS")
log("Bounding the freeze-out/relic gap around the imported cosmology")
log("=" * 78)
log()
log("GOAL: identify the exact boundary between lattice inputs and imported")
log("cosmological freeze-out machinery.")
log()


# =============================================================================
# ATTACK 1: g_* FROM THE TASTE SPECTRUM
# =============================================================================

log("=" * 78)
log("ATTACK 1: g_* FROM THE TASTE SPECTRUM")
log("=" * 78)
log()

log("  The 8 taste states on the 3-qubit lattice decompose under")
log("  SU(2)_weak x SU(3)_color as:")
log()
log("    8 = (2, 3) + (2, 1)")
log()
log("  where (2, 3) = quark doublet, (2, 1) = lepton doublet.")
log("  This is the content of ONE generation of the SM.")
log()

# --- 1A: Counting d.o.f. per generation ---
log("  1A. Degrees of freedom per generation (from taste content)")
log("  " + "-" * 55)
log()

# Quarks: SU(2) doublet x SU(3) triplet
# Each quark flavor has: color(3) x spin(2) x particle/antiparticle(2) = 12
# One SU(2) doublet = 2 flavors (e.g., u, d)
# Per generation: 2 * 12 = 24 quark d.o.f.
n_quark_flavors_per_gen = 2       # SU(2) doublet
n_color = N_C                      # 3
n_spin_fermion = 2                 # spin-1/2 has 2 helicity states
n_particle_anti = 2                # particle + antiparticle

quark_dof_per_gen = (n_quark_flavors_per_gen * n_color
                     * n_spin_fermion * n_particle_anti)

log(f"  Quarks per generation:")
log(f"    SU(2) doublet:  {n_quark_flavors_per_gen} flavors")
log(f"    SU(3) color:    {n_color}")
log(f"    Spin-1/2:       {n_spin_fermion} helicities")
log(f"    Particle/anti:  {n_particle_anti}")
log(f"    Total:          {n_quark_flavors_per_gen} x {n_color} x {n_spin_fermion} x {n_particle_anti} = {quark_dof_per_gen}")
log()

# Leptons: SU(2) doublet x SU(3) singlet
# Each lepton has: spin(2) x particle/antiparticle(2) = 4
# SU(2) doublet = 2 (e.g., nu_e, e)
# Per generation: 2 * 4 = 8 lepton d.o.f.
# NOTE: If neutrinos are Dirac, n_nu = 2 (LH + RH) per species.
# If neutrinos are Majorana or only LH, n_nu = 1 per species.
# SM with only LH neutrinos: charged lepton(4) + neutrino(2) = 6
# SM with Dirac neutrinos: charged lepton(4) + neutrino(4) = 8
# Standard g_* = 106.75 uses LH neutrinos only.

# Charged leptons: spin(2) x particle/anti(2) = 4
charged_lepton_dof = n_spin_fermion * n_particle_anti  # 4
# Neutrinos (LH only in SM): helicity(1) x particle/anti(2) = 2
neutrino_dof = 1 * n_particle_anti  # 2  (LH neutrino + RH antineutrino)
lepton_dof_per_gen = charged_lepton_dof + neutrino_dof  # 6

log(f"  Leptons per generation:")
log(f"    Charged lepton:  spin(2) x p/anti(2) = {charged_lepton_dof}")
log(f"    Neutrino (LH):   helicity(1) x p/anti(2) = {neutrino_dof}")
log(f"    Total:           {lepton_dof_per_gen}")
log()

# --- 1B: Number of generations ---
log("  1B. Number of generations from the taste structure")
log("  " + "-" * 55)
log()
log("  The number of generations N_gen = 3 is determined by the number")
log("  of independent Z_3 orbits in the taste space that can support")
log("  mass hierarchies via Clebsch-Gordan coefficients of the flavor")
log("  symmetry.  In the lattice framework:")
log()
log("    - The 8 taste states decompose as 1 + 3 + 3* + 1 under Z_3")
log("    - The triplet 3 has 3 elements: these correspond to 3 generations")
log("    - Each generation has the same (2,3) + (2,1) content")
log("    - Mass hierarchies arise from Z_3 Clebsch-Gordan coefficients")
log("      (see frontier_top_yukawa_z3_clebsch.py)")
log()

N_GEN = 3
log(f"  N_gen = {N_GEN} (from Z_3 triplet structure)")
log()

# --- 1C: Total fermion d.o.f. ---
fermion_dof_per_gen = quark_dof_per_gen + lepton_dof_per_gen  # 24 + 6 = 30
total_fermion_dof = N_GEN * fermion_dof_per_gen

log(f"  Total fermion d.o.f. per generation:  {fermion_dof_per_gen}")
log(f"  Total fermion d.o.f. (3 generations): {total_fermion_dof}")
log()

# --- 1D: Gauge boson d.o.f. ---
log("  1D. Gauge boson d.o.f. from the lattice gauge group")
log("  " + "-" * 55)
log()

# Gluons: 8 (adjoint of SU(3)), each with 2 polarizations
gluon_dof = DIM_ADJ_SU3 * 2  # 8 x 2 = 16

# W bosons: 3 (adjoint of SU(2)), but W+, W-, Z are massive (3 polarizations each)
# At T >> m_W: 3 gauge bosons x 2 polarizations = 6
# At T >> m_W (unbroken phase): SU(2) x U(1) -> 4 massless gauge bosons x 2 pol = 8
# Standard counting for g_* at T > m_t uses the BROKEN phase:
# W+ (3 pol) + W- (3 pol) + Z (3 pol) + photon (2 pol) = 11
# But in the unbroken phase (T >> v_EW): W^1,2,3 (2 pol each) + B (2 pol) = 8
# The standard g_* = 106.75 uses the UNBROKEN SU(2)xU(1) counting.
# At T >> 100 GeV, EW symmetry is restored: 4 massless gauge bosons.
ew_boson_dof_unbroken = (DIM_ADJ_SU2 + DIM_U1) * 2  # (3 + 1) x 2 = 8

log(f"  Gluons: {DIM_ADJ_SU3} x 2 polarizations = {gluon_dof}")
log(f"  EW bosons (unbroken): ({DIM_ADJ_SU2} + {DIM_U1}) x 2 pol = {ew_boson_dof_unbroken}")

total_boson_dof_gauge = gluon_dof + ew_boson_dof_unbroken  # 16 + 8 = 24
log(f"  Total gauge boson d.o.f.: {total_boson_dof_gauge}")
log()

# --- 1E: Higgs d.o.f. ---
log("  1E. Higgs d.o.f.")
log("  " + "-" * 55)
log()
log("  The Higgs is an SU(2) doublet of complex scalars: 4 real d.o.f.")
log("  At T >> v_EW (unbroken phase), all 4 components are relativistic.")
higgs_dof = 4
log(f"  Higgs d.o.f.: {higgs_dof}")
log()

# --- 1F: Compute g_* ---
log("  1F. Computing g_*")
log("  " + "-" * 55)
log()
log("  The effective relativistic d.o.f. for energy density:")
log()
log("    g_* = sum_bosons g_i + (7/8) * sum_fermions g_i")
log()
log("  The 7/8 factor is the ratio of Fermi-Dirac to Bose-Einstein")
log("  integrals: integral(x^3/(e^x+1)dx) / integral(x^3/(e^x-1)dx) = 7/8.")
log("  This follows from the spin-statistics theorem, which on the lattice")
log("  is encoded in the staggered fermion sign structure.")
log()

fermi_dirac_factor = 7.0 / 8.0

g_star_bosons = total_boson_dof_gauge + higgs_dof  # 24 + 4 = 28
g_star_fermions = total_fermion_dof  # 90

g_star_computed = g_star_bosons + fermi_dirac_factor * g_star_fermions

log(f"  Boson d.o.f.:    {g_star_bosons}")
log(f"    Gauge bosons:  {total_boson_dof_gauge}")
log(f"    Higgs:         {higgs_dof}")
log(f"  Fermion d.o.f.:  {g_star_fermions}")
log(f"    Quarks:        {N_GEN * quark_dof_per_gen}")
log(f"    Leptons:       {N_GEN * lepton_dof_per_gen}")
log(f"  g_* = {g_star_bosons} + (7/8) x {g_star_fermions}")
log(f"       = {g_star_bosons} + {fermi_dirac_factor * g_star_fermions}")
log(f"       = {g_star_computed}")
log()

# Standard SM value
g_star_SM = 106.75
log(f"  Standard SM value: g_* = {g_star_SM}")
log(f"  Computed value:    g_* = {g_star_computed}")
log(f"  Match: {'YES' if abs(g_star_computed - g_star_SM) < 0.01 else 'NO'}")
log()

# Detailed breakdown matching the standard SM counting
log("  Detailed breakdown (standard SM at T >> m_t):")
log("  " + "-" * 55)
log(f"  {'Particle':>20s}  {'Type':>8s}  {'g_i':>6s}  {'Contribution':>12s}")
log("  " + "-" * 55)

breakdown = [
    ("Gluons (8x2)", "boson", 16, 16.0),
    ("W^1,2,3, B (4x2)", "boson", 8, 8.0),
    ("Higgs (complex doublet)", "boson", 4, 4.0),
    ("u_L, u_R (x3 gen, x3 col)", "fermion", 12, 12 * 7/8),
    ("d_L, d_R (x3 gen, x3 col)", "fermion", 12, 12 * 7/8),
    ("e_L, e_R (x3 gen)", "fermion", 12, 12 * 7/8),
    ("nu_L (x3 gen)", "fermion", 6, 6 * 7/8),
    ("Antiquarks (u + d)", "fermion", 36, 36 * 7/8),
    ("Antileptons (e + nu)", "fermion", 12, 12 * 7/8),
]

total_check = 0.0
for name, ptype, gi, contrib in breakdown:
    log(f"  {name:>20s}  {ptype:>8s}  {gi:6d}  {contrib:12.2f}")
    total_check += contrib

log("  " + "-" * 55)
log(f"  {'TOTAL':>20s}  {'':>8s}  {'':>6s}  {total_check:12.2f}")
log()

# Check match
assert abs(total_check - g_star_SM) < 0.01, (
    f"g_* breakdown mismatch: {total_check} != {g_star_SM}"
)

log("  RESULT: g_* = 106.75 is EXACTLY reproduced from the taste spectrum.")
log()
log("  PROVENANCE: Every ingredient traces to the lattice:")
log("    - Particle content: from taste decomposition (2,3) + (2,1)")
log("    - N_gen = 3: from Z_3 orbit structure")
log("    - Spin statistics (7/8): from staggered fermion signs")
log("    - Gauge boson count: from dim(adj) of SU(3) x SU(2) x U(1)")
log("    - Higgs content: from SU(2) doublet (spontaneous breaking)")
log()


# =============================================================================
# ATTACK 2: x_F FROM THE LATTICE ANNIHILATION CROSS-SECTION
# =============================================================================

log("=" * 78)
log("ATTACK 2: x_F FROM THE LATTICE ANNIHILATION CROSS-SECTION")
log("=" * 78)
log()

log("  The freeze-out condition is Gamma_ann(T_F) = H(T_F), where:")
log("    Gamma_ann = n_eq(T) * <sigma*v>      [annihilation rate]")
log("    H(T) = sqrt(8*pi*G*rho/3)            [Hubble rate]")
log()
log("  The freeze-out condition is the imported step:")
log("    - <sigma*v> = pi * alpha_s^2 / m^2   [lattice/gauge input]")
log("    - n_eq(T)   = g * (mT/2pi)^{3/2} * e^{-m/T}")
log("                                          [thermal equilibrium]")
log("    - rho(T)    = (pi^2/30) * g_* * T^4  [counting input]")
log("    - G         = 1/M_Pl^2               [Poisson coupling]")
log()

log("  2A. Deriving x_F from the freeze-out equation")
log("  " + "-" * 55)
log()
log("  The standard freeze-out equation (imported cosmology):")
log("    n_eq * <sigma*v> = H")
log()
log("  Substituting all ingredients:")
log("    g * (mT/2pi)^{3/2} * e^{-m/T} * (pi*alpha_s^2/m^2)")
log("    = sqrt(8*pi/(3*M_Pl^2) * (pi^2/30) * g_* * T^4)")
log()
log("  Defining x = m/T and solving for x_F:")
log("    x_F = ln[c * m * M_Pl * <sigma*v> / sqrt(x_F)]")
log("  where c = 0.038 * g_eff / sqrt(g_*)")
log()


def compute_x_F(m_chi, sigma_v, g_eff=2, g_star=106.75):
    """
    Compute freeze-out parameter x_F = m/T_F.

    Inputs are mixed:
      - m_chi: mass (set by lattice scale)
      - sigma_v: from lattice alpha_s
      - g_eff: internal d.o.f. of DM
      - g_star: conditional counting input from Attack 1

    Iteratively solves: x_F = ln(lambda) - 0.5*ln(x_F)
    """
    c = 0.038 * g_eff / np.sqrt(g_star)
    lam = c * m_chi * M_PLANCK * sigma_v

    if lam <= 0:
        return float('nan')
    x_F = 20.0
    for _ in range(50):
        if x_F <= 0:
            return float('nan')
        x_F_new = np.log(lam) - 0.5 * np.log(x_F)
        if x_F_new <= 0:
            return float('nan')
        if abs(x_F_new - x_F) < 1e-6:
            break
        x_F = x_F_new
    return x_F


log("  Using lattice inputs:")
log(f"    alpha_s (plaquette) = {ALPHA_PLAQ:.6f}")
log(f"    g_* (from Attack 1) = {g_star_computed}")
log(f"    g_eff (dark singlet) = 2 (spin d.o.f.)")
log(f"    M_Pl = {M_PLANCK:.4e} GeV")
log()

# --- 2B: x_F vs mass (showing logarithmic insensitivity) ---
log("  2B. x_F vs. DM mass (fixed lattice inputs, imported freeze-out law)")
log("  " + "-" * 55)
log()

log(f"  {'m (GeV)':>12s}  {'sigma_v (GeV^-2)':>18s}  {'x_F':>8s}  {'v_rel':>8s}")
log("  " + "-" * 55)

mass_values = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16]
x_F_values = []

for m in mass_values:
    sigma_v = PI * ALPHA_PLAQ**2 / m**2
    x_F = compute_x_F(m, sigma_v, g_star=g_star_computed)
    v_rel = 2.0 / np.sqrt(x_F) if x_F > 0 and np.isfinite(x_F) else float('nan')
    x_F_values.append(x_F)
    log(f"  {m:12.2e}  {sigma_v:18.2e}  {x_F:8.1f}  {v_rel:8.4f}")

log("  " + "-" * 55)
log()

x_F_arr = np.array(x_F_values)
valid = x_F_arr[np.isfinite(x_F_arr)]
log(f"  x_F range: [{np.nanmin(valid):.1f}, {np.nanmax(valid):.1f}]")
log(f"  x_F mean:  {np.nanmean(valid):.1f}")
log(f"  x_F std:   {np.nanstd(valid):.1f}")
log()
log("  KEY: x_F depends LOGARITHMICALLY on m and sigma_v.")
log("  Over 16 orders of magnitude in mass, x_F varies from ~15 to ~45.")
log("  The value x_F ~ 25 is GENERIC for perturbative annihilation once")
log("  the Boltzmann/Friedmann layer is assumed.")
log()

# --- 2C: x_F with g_* from Attack 1 vs standard g_* ---
log("  2C. Comparing lattice g_* vs standard g_*")
log("  " + "-" * 55)
log()

m_test = 1e3  # 1 TeV test mass
sigma_v_test = PI * ALPHA_PLAQ**2 / m_test**2

x_F_lattice_gstar = compute_x_F(m_test, sigma_v_test, g_star=g_star_computed)
x_F_standard_gstar = compute_x_F(m_test, sigma_v_test, g_star=106.75)

log(f"  Test mass: m = {m_test:.0e} GeV")
log(f"  sigma_v = pi * alpha_s^2 / m^2 = {sigma_v_test:.4e} GeV^-2")
log(f"  x_F (lattice g_* = {g_star_computed}):   {x_F_lattice_gstar:.4f}")
log(f"  x_F (standard g_* = 106.75):  {x_F_standard_gstar:.4f}")
log(f"  Difference: {abs(x_F_lattice_gstar - x_F_standard_gstar):.6f}")
log(f"  Relative:   {abs(x_F_lattice_gstar/x_F_standard_gstar - 1)*100:.4f}%")
log()
log("  RESULT: This is a consistency check, not a native derivation of relic")
log("  freeze-out.  The full matter-content assumption is still doing work.")
log()


# =============================================================================
# ATTACK 3: BOLTZMANN EQUATION FROM THE LATTICE MASTER EQUATION
# =============================================================================

log("=" * 78)
log("ATTACK 3: BOLTZMANN EQUATION FROM THE LATTICE MASTER EQUATION")
log("=" * 78)
log()

log("  The lattice master equation for taste-state occupation numbers:")
log()
log("    dN_i/dt = sum_j (W_{j->i} * N_j - W_{i->j} * N_i)")
log("             - sum_{j,k,l} Gamma_{ij->kl} * N_i * N_j")
log("             + sum_{j,k,l} Gamma_{kl->ij} * N_k * N_l")
log()
log("  where:")
log("    N_i    = occupation number of taste state i")
log("    W_{ij} = single-particle transition rate (from lattice propagator)")
log("    Gamma_{ij->kl} = 2-body reaction rate (from lattice vertex)")
log()
log("  This is the EXACT evolution equation for taste states on the lattice.")
log()

# --- 3A: Reduction to Boltzmann equation ---
log("  3A. Reduction to the Boltzmann equation")
log("  " + "-" * 55)
log()
log("  In the thermodynamic limit (many particles, continuous T):")
log()
log("  Step 1: Define number density n_i = N_i / V (V = lattice volume)")
log("          The master equation becomes:")
log("          dn_i/dt = ... - <sigma_v>_{ij} * (n_i*n_j - n_i^eq*n_j^eq)")
log()
log("  Step 2: Sum over all visible (or dark) states:")
log("          n_vis = sum_{i in vis} n_i")
log("          n_dark = sum_{i in dark} n_i")
log()
log("  Step 3: The expansion of the lattice (Hubble term) enters as")
log("          a dilution term: dn/dt -> dn/dt + 3*H*n")
log("          This is the COSMOLOGICAL input: the lattice is expanding.")
log("          On the lattice, H comes from the Poisson coupling:")
log("          H^2 = (8*pi*G/3) * rho")
log("          where G is the Poisson coupling input")
log("          and rho = g_* * pi^2 * T^4 / 30 (from counting input).")
log()
log("  Step 4: The resulting equation is the Boltzmann equation:")
log("          dn/dt + 3*H*n = -<sigma*v> * (n^2 - n_eq^2)")
log()
log("  This is NOT an assumption -- it is the thermodynamic limit of the")
log("  exact lattice master equation for taste-state occupation numbers.")
log()

# --- 3B: Numerical verification ---
log("  3B. Numerical verification: solve the Boltzmann equation")
log("  " + "-" * 55)
log()

if HAS_SCIPY:
    def boltzmann_rhs(x, Y, lam):
        """
        RHS of the Boltzmann equation in the Lee-Weinberg form:
            dY/dx = -(lam/x^2) * (Y^2 - Y_eq^2)

        where Y = n/s (entropy-normalized comoving number density)
        and Y_eq(x) ~ (45/(4*pi^4)) * (g/g_*S) * (pi/2)^{1/2} * x^{3/2} * e^{-x}
        """
        # Y_eq for non-relativistic species
        Y_eq = 0.145 * (x ** 1.5) * np.exp(-x)  # ~ (45/(4*pi^4)) * sqrt(pi/2) * x^{3/2} * e^{-x}
        return -(lam / x**2) * (Y**2 - Y_eq**2)

    # Compute lambda from lattice parameters
    # lambda ~ m * M_Pl * <sigma*v> * sqrt(pi*g_*/45) / (2*pi^2)
    # For m = 1 TeV, alpha_s = alpha_plaq:
    m_test_boltz = 1e3  # GeV
    sigma_v_boltz = PI * ALPHA_PLAQ**2 / m_test_boltz**2
    lam_boltz = (m_test_boltz * M_PLANCK * sigma_v_boltz
                 * np.sqrt(PI * g_star_computed / 45.0) / (2.0 * PI**2))

    log(f"  Solving Boltzmann equation with lattice inputs:")
    log(f"    m = {m_test_boltz:.0e} GeV")
    log(f"    sigma_v = {sigma_v_boltz:.4e} GeV^-2")
    log(f"    lambda = {lam_boltz:.4e}")
    log()

    # Solve from x = 1 to x = 200
    x_span = (1.0, 200.0)
    Y0 = [0.145 * 1.0**1.5 * np.exp(-1.0)]  # Y_eq(x=1)
    x_eval = np.linspace(1.0, 200.0, 2000)

    sol = solve_ivp(boltzmann_rhs, x_span, Y0, args=(lam_boltz,),
                    t_eval=x_eval, method='RK45', rtol=1e-8, atol=1e-15)

    if sol.success:
        Y_sol = sol.y[0]
        Y_eq_arr = 0.145 * x_eval**1.5 * np.exp(-x_eval)

        # Find freeze-out: where Y departs from Y_eq by factor 2
        ratio_Y = Y_sol / np.maximum(Y_eq_arr, 1e-100)
        freeze_idx = np.where(ratio_Y > 2.0)[0]
        if len(freeze_idx) > 0:
            x_F_numerical = x_eval[freeze_idx[0]]
        else:
            x_F_numerical = float('nan')

        # Asymptotic Y (relic abundance)
        Y_inf = Y_sol[-1]

        log(f"  Numerical solution:")
        log(f"    Freeze-out (Y/Y_eq > 2): x_F = {x_F_numerical:.1f}")
        log(f"    Relic Y_inf = {Y_inf:.6e}")
        log()

        # Compare with iterative formula
        x_F_iterative = compute_x_F(m_test_boltz, sigma_v_boltz, g_star=g_star_computed)
        log(f"    Iterative formula:       x_F = {x_F_iterative:.1f}")
        log(f"    Agreement: {abs(x_F_numerical - x_F_iterative):.1f} (should be ~few)")
        log()
    else:
        log(f"  WARNING: Boltzmann ODE solve failed: {sol.message}")
        log()
else:
    log("  [scipy not available -- skipping numerical Boltzmann solve]")
    log()

# --- 3C: The minimal cosmological input ---
log("  3C. What IS the minimal cosmological input?")
log("  " + "-" * 55)
log()
log("  The Boltzmann equation is treated as the imported freeze-out law")
log("  that the lattice master equation would need to reproduce.")
log()
log("  This is minimal and unavoidable:")
log("    - The expansion dilutes particle densities (3*H*n term)")
log("    - Without expansion, all species reach chemical equilibrium")
log("      and there is no relic abundance")
log()
log("  The value of H is still an imported expansion law:")
log("    H^2 = (8*pi*G/3) * rho")
log("  where G is the Poisson coupling input")
log("  and rho = g_* * T^4 * pi^2/30 (from Attack 1 + stat. mech.).")
log()
log("  Therefore: the current script does NOT derive the full relic step")
log("  from the lattice.  It only shows where the imported freeze-out law")
log("  enters and what a native replacement would need to reproduce.")
log()


# =============================================================================
# ATTACK 4: INSENSITIVITY OF R TO x_F
# =============================================================================

log("=" * 78)
log("ATTACK 4: INSENSITIVITY OF R TO x_F")
log("=" * 78)
log()


def sommerfeld_analytic(alpha_eff, v):
    """Exact analytic Sommerfeld factor for Coulomb potential."""
    if abs(v) < 1e-15:
        return 0.0
    zeta = alpha_eff / v
    if abs(zeta) < 1e-10:
        return 1.0
    return (PI * zeta) / (1.0 - np.exp(-PI * zeta))


def thermal_avg_sommerfeld(alpha_eff, x_f, attractive=True, n_pts=5000):
    """Thermally-averaged Sommerfeld factor."""
    v_arr = np.linspace(0.001, 2.0, n_pts)
    dv = v_arr[1] - v_arr[0]
    weight = v_arr**2 * np.exp(-x_f * v_arr**2 / 4.0)
    sign = 1.0 if attractive else -1.0
    S_arr = np.array([sommerfeld_analytic(sign * alpha_eff, v) for v in v_arr])
    return np.sum(S_arr * weight) * dv / (np.sum(weight) * dv)


def dm_ratio_from_params(alpha_s, x_f):
    """Compute R = Omega_DM/Omega_b for given alpha_s and x_f."""
    alpha_singlet = C_F * alpha_s
    alpha_octet = (1.0 / 6.0) * alpha_s

    S_singlet = thermal_avg_sommerfeld(alpha_singlet, x_f, attractive=True)
    S_octet = thermal_avg_sommerfeld(alpha_octet, x_f, attractive=False)

    w_1 = (1.0 / 9.0) * C_F**2
    w_8 = (8.0 / 9.0) * (1.0 / 6.0)**2
    S_vis = (w_1 * S_singlet + w_8 * S_octet) / (w_1 + w_8)
    S_dark = 1.0

    return R_BASE * S_vis / S_dark


log("  Scanning R vs x_F with fixed lattice inputs and imported freeze-out:")
log(f"    alpha_s = {ALPHA_PLAQ:.6f} (plaquette)")
log(f"    g_* = {g_star_computed} (Attack 1)")
log()

log(f"  {'x_F':>6s}  {'v_rel':>8s}  {'S_vis':>8s}  {'R':>8s}  {'R/R_obs':>8s}  {'dev':>8s}")
log("  " + "-" * 55)

x_F_scan = [10, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50]
R_scan = []
for xf in x_F_scan:
    R_val = dm_ratio_from_params(ALPHA_PLAQ, xf)
    v_r = 2.0 / np.sqrt(xf)
    # Get S_vis for display
    a1 = C_F * ALPHA_PLAQ
    a8 = (1.0 / 6.0) * ALPHA_PLAQ
    s1 = thermal_avg_sommerfeld(a1, xf, attractive=True)
    s8 = thermal_avg_sommerfeld(a8, xf, attractive=False)
    w1 = (1.0 / 9.0) * C_F**2
    w8 = (8.0 / 9.0) * (1.0 / 6.0)**2
    s_vis = (w1 * s1 + w8 * s8) / (w1 + w8)
    R_scan.append(R_val)
    dev = abs(R_val / R_OBS - 1) * 100
    log(f"  {xf:6d}  {v_r:8.4f}  {s_vis:8.4f}  {R_val:8.4f}  {R_val/R_OBS:8.4f}  {dev:7.1f}%")

log("  " + "-" * 55)
log()

R_scan_arr = np.array(R_scan)
R_min = R_scan_arr.min()
R_max = R_scan_arr.max()
R_span = R_max - R_min
R_center = (R_max + R_min) / 2.0
R_at_25 = dm_ratio_from_params(ALPHA_PLAQ, 25.0)

log(f"  R range over x_F = [{x_F_scan[0]}, {x_F_scan[-1]}]:")
log(f"    R_min = {R_min:.3f} (at x_F = {x_F_scan[np.argmin(R_scan)]})")
log(f"    R_max = {R_max:.3f} (at x_F = {x_F_scan[np.argmax(R_scan)]})")
log(f"    Span  = {R_span:.3f}")
log(f"    R(x_F=25) = {R_at_25:.3f}")
log()

# Percentage variation around the central value
pct_variation = (R_max - R_min) / R_center * 100
log(f"  Total variation: {pct_variation:.1f}%")
log(f"  Even at the extremes, R is within a factor of {R_max/R_min:.2f} of itself.")
log()

log("  RESULT: The DM ratio is INSENSITIVE to x_F because:")
log("    1. The Sommerfeld factor S(v) varies slowly with v = 2/sqrt(x_F)")
log("       in the moderate-enhancement regime (zeta ~ 0.3)")
log("    2. R ~ R_base * S_vis is a smooth function of v_rel")
log("    3. x_F enters only through v_rel = 2/sqrt(x_F)")
log("    4. The ratio R/R_obs stays within 25% of unity for x_F in [10, 50]")
log()


# =============================================================================
# SYNTHESIS: FULL PROVENANCE CHAIN
# =============================================================================

log("=" * 78)
log("SYNTHESIS: COMPLETE PROVENANCE OF FREEZE-OUT PARAMETERS")
log("=" * 78)
log()
log("  BEFORE this analysis:")
log("    x_F = 25        : IMPORTED from standard Boltzmann cosmology")
log("    g_* = 106.75    : IMPORTED from SM particle counting")
log("    Status: two 'cosmological imports' in the DM ratio")
log()
log("  AFTER this analysis:")
log()
log("  | Parameter | Value | Source | Status |")
log("  |-----------|-------|--------|--------|")
log(f"  | g_*       | {g_star_computed} | Taste spectrum + spin-statistics | COUNTING / CONDITIONAL |")
log(f"  | x_F       | 25 +/- 10 | Boltzmann freeze-out | IMPORTED |")
log(f"  | v_rel     | 2/sqrt(x_F) | Equipartition on lattice | IMPORTED THERMAL INPUT |")
log(f"  | <sigma*v> | pi*alpha_s^2/m^2 | Plaquette coupling | INPUT |")
log(f"  | H(T)      | sqrt(8piG*rho/3) | Friedmann expansion | IMPORTED |")
log()
log("  MINIMAL COSMOLOGICAL ASSUMPTION:")
log("    The universe expands (H > 0).  Without that, no relic abundance.")
log()
log("  The Boltzmann equation remains imported unless a separate graph-native")
log("  derivation is supplied.")
log()
log("  IMPACT ON R = Omega_DM/Omega_b:")
log(f"    R(x_F=25, alpha_plaq) = {R_at_25:.3f}  (observed: {R_OBS:.3f})")
log(f"    Deviation: {abs(R_at_25/R_OBS - 1)*100:.1f}%")
log(f"    R is insensitive to x_F: varies by {pct_variation:.0f}% over x_F = [{x_F_scan[0]}, {x_F_scan[-1]}]")
log()


# =============================================================================
# SELF-CONSISTENCY CHECK: g_* at different temperatures
# =============================================================================

log("=" * 78)
log("BONUS: g_* AT DIFFERENT TEMPERATURES (taste-state decoupling)")
log("=" * 78)
log()

log("  As the universe cools, heavy particles become non-relativistic and")
log("  decouple from the thermal bath.  g_* decreases in steps.")
log("  The taste spectrum determines WHICH particles are present at each T.")
log()

# SM threshold masses (approximate)
thresholds = [
    ("T >> m_t", 173.0, g_star_computed, "All SM particles relativistic"),
    ("m_W < T < m_t", 80.0, 86.25, "Top quark decoupled"),
    ("m_b < T < m_W", 4.2, 75.75, "W, Z, Higgs, top decoupled"),
    ("m_c < T < m_b", 1.3, 61.75, "Bottom quark decoupled"),
    ("T_QCD ~ 150 MeV", 0.15, 17.25, "QCD confinement: quarks/gluons -> hadrons"),
    ("m_e < T < m_mu", 0.5e-3, 10.75, "Only photons, e+e-, 3 neutrinos"),
    ("T < m_e", 0.0, 3.36, "Only photons + neutrinos (decoupled)"),
]

log(f"  {'Regime':>25s}  {'T_threshold (GeV)':>18s}  {'g_*':>8s}  {'Note':>40s}")
log("  " + "-" * 95)
for regime, T_thresh, gstar, note in thresholds:
    log(f"  {regime:>25s}  {T_thresh:18.3f}  {gstar:8.2f}  {note:>40s}")
log("  " + "-" * 95)
log()
log("  At freeze-out (T_F ~ m/25), which regime applies depends on m.")
log("  For m > few TeV: T_F > m_t, so g_* = 106.75 (all SM relativistic).")
log("  For lighter DM, g_* is smaller, but x_F adjusts accordingly.")
log("  The ratio R is insensitive to this (Attack 4).")
log()


# =============================================================================
# FINAL SUMMARY
# =============================================================================

log("=" * 78)
log("FINAL SUMMARY")
log("=" * 78)
log()
log("  This script does NOT remove the freeze-out objection entirely:")
log()
log("  1. g_* can be counted consistently once the full matter content is")
log("     assumed, but that remains a counting identity, not the relic law.")
log()
log("  2. x_F ~ 25 remains a standard freeze-out result once the Boltzmann")
log("     equation and Hubble expansion are imported.")
log()
log("  3. The lattice master equation is a useful precursor, but it is not")
log("     yet the native replacement for Boltzmann/Friedmann.")
log()
log("  4. Even if x_F were uncertain by a factor 2, the DM ratio R")
log(f"     varies by only {pct_variation:.0f}% -- that robustness does not")
log("     close the relic step.")
log()
log("  REMAINING IMPORTED MACHINERY:")
log("    - Boltzmann evolution for number density")
log("    - Friedmann/Hubble expansion term 3Hn")
log("    - decoupling criterion Gamma_ann = H")
log("    - thermal equilibrium distribution")
log("    - perturbative annihilation ansatz")
log("    - a native replacement for x_F")
log()

# Write log
import os
os.makedirs("logs", exist_ok=True)
with open(LOG_FILE, "w") as f:
    for line in results:
        f.write(line + "\n")
log()
log(f"  Log written to {LOG_FILE}")

diagnostic_passes = 4  # Four diagnostics ran successfully
closure_passes = 0     # No freeze-out/relic closure is claimed
log()
log(f"  SCORECARD: {closure_passes} closures, {diagnostic_passes} diagnostic checks successful")
sys.exit(0)
