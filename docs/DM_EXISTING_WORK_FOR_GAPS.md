# DM Lane: Existing Work Relevant to Remaining Gaps

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Purpose:** Inventory of existing derivations that bear on the two remaining DM lane gaps:
  1. **sigma_v coefficient rigor** -- proving C = pi algebraically from the lattice
  2. **Boltzmann derivation from lattice** -- deriving the Boltzmann equation from lattice dynamics

---

## Gap 1: sigma_v Coefficient C = pi

### What is needed

An algebraic (not numerical) proof that the dimensionless coefficient in
sigma_v = C * alpha_s^2 / m^2 is exactly pi for s-wave fermion-antifermion
annihilation, derived from lattice quantities.

### Existing work

#### 1. `scripts/frontier_dm_sigma_v_lattice.py` (Approach 4, sections 4A-4B)

**Status: PARTIALLY addresses the gap.**

- **4A** extracts C numerically from the lattice Born calculation on a small
  (L=8) 3D lattice. C is shown to be approximately constant across coupling
  values, but the extracted value is displaced from pi by finite-lattice-size
  effects. There is no algebraic derivation of C = pi.
- **4B** shows that the lattice density of states converges to the continuum
  DOS (which contains the 1/pi^2 factor producing C = pi) as L grows. The
  convergence is numerical, not algebraic.
- The script's own synthesis (lines 893-924) states honestly: "The EXACT
  COEFFICIENT pi is only recovered in the continuum limit. On a finite
  lattice, C(L) differs from pi by O(1/L^2) corrections."

**Verdict:** Demonstrates C -> pi numerically via lattice DOS convergence.
Does NOT contain an algebraic proof that C = pi.

#### 2. `docs/DM_THERMODYNAMIC_CLOSURE_NOTE.md`

**Status: RESOLVES the limit identification, not the coefficient itself.**

- Proves that "continuum limit" was a misnomer -- the convergence C(L) -> pi
  is actually the thermodynamic limit (N -> infinity at fixed a = l_Planck),
  not the forbidden continuum limit (a -> 0).
- Invokes Weyl's law on PL manifolds to guarantee eigenvalue counting
  converges. The finite-size correction at physical N ~ 10^185 is O(10^{-96}).
- Does NOT algebraically derive that the limiting value is exactly pi.

**Verdict:** Closes the "which limit" question. Does not close the
"why exactly pi" question.

#### 3. `scripts/frontier_sommerfeld_analytic_proof.py`

**Status: DOES NOT address sigma_v coefficient.**

- Proves that the lattice Green's function ratio G_Coulomb/G_free converges
  to the Sommerfeld factor S = pi*zeta/(1 - exp(-pi*zeta)) via five steps:
  resolvent convergence, Gamow factor identity, LDOS ratio, continued
  fraction, and finite-size scaling.
- This proves the Sommerfeld enhancement is lattice-native, but the Sommerfeld
  factor is the ENHANCEMENT of sigma_v, not the base sigma_v itself.
- No derivation of the s-wave annihilation cross-section coefficient.

**Verdict:** Irrelevant to the C = pi gap. Addresses a different (already
closed) sub-problem.

#### 4. `scripts/frontier_sommerfeld_lattice_greens.py`

**Status: DOES NOT address sigma_v coefficient.**

- Computes the Sommerfeld enhancement S from the lattice Hamiltonian via
  Numerov integration and Green's function (resolvent) methods.
- No scattering amplitude or cross-section computation.

**Verdict:** Irrelevant to the C = pi gap.

#### 5. `scripts/frontier_annihilation_ratio.py`

**Status: USES but does not DERIVE the cross-section formula.**

- Computes Omega_DM/Omega_visible = 5.4 from group-theoretic channel
  counting, Casimir invariants, and freeze-out thermodynamics.
- Takes sigma ~ pi * alpha^2 * C_2(R) / m^2 as INPUT (line 155) and uses
  it throughout to compute annihilation rates for visible vs dark states.
- No derivation of why the coefficient is pi.

**Verdict:** Irrelevant to the C = pi gap. Downstream consumer of the formula.

#### 6. `scripts/frontier_dm_sigma_v_lattice.py` (Approaches 1-2: Optical theorem + Lippmann-Schwinger)

**Status: DERIVES the functional form, not the coefficient.**

- **Approach 1** (optical theorem): Proves sigma*v = Im[<k|T(E+i*eps)|k>] is
  an EXACT lattice identity following from unitarity (S^dag S = 1). This is
  verified numerically on 1D lattices.
- **Approach 2** (Lippmann-Schwinger T-matrix): Computes T = V(1 - G_0 V)^{-1}
  on finite lattices. Verifies agreement with the optical theorem.
- **1B** extracts the alpha^2 power law from the lattice Born calculation
  on a 3D lattice (best-fit exponent checked against 2.0).
- None of these extract the coefficient pi algebraically. They show
  sigma_v ~ alpha^2/m^2 from the lattice, with a numerical coefficient
  that approaches pi only in the large-L limit.

**Verdict:** Strongest existing result for sigma_v derivation. Proves the
FUNCTIONAL FORM is lattice-native. The exact coefficient remains numerical.

### Summary for Gap 1

| Script/Doc | Functional form | C = pi algebraically | C -> pi numerically |
|------------|:-:|:-:|:-:|
| `frontier_dm_sigma_v_lattice.py` (1-2) | YES | NO | -- |
| `frontier_dm_sigma_v_lattice.py` (4A-4B) | -- | NO | YES (L -> inf) |
| `DM_THERMODYNAMIC_CLOSURE_NOTE.md` | -- | NO | YES (Weyl's law) |
| `frontier_sommerfeld_analytic_proof.py` | -- | NO | -- |
| `frontier_sommerfeld_lattice_greens.py` | -- | NO | -- |
| `frontier_annihilation_ratio.py` | -- | NO | -- |

**Bottom line:** The functional form sigma_v = C * alpha^2 / m^2 is DERIVED
from the lattice. The coefficient C -> pi is shown numerically via lattice DOS
convergence and justified via Weyl's law, but there is no closed-form algebraic
proof that C = pi from lattice quantities alone. The thermodynamic closure note
correctly identifies this as a thermodynamic limit (not continuum limit) with
negligible finite-size corrections at physical N.

---

## Gap 2: Boltzmann Equation from Lattice

### What is needed

A derivation of the Boltzmann equation dn/dt + 3Hn = -<sigma*v>(n^2 - n_eq^2)
from lattice dynamics, without importing it from textbook cosmology.

### Existing work

#### 1. `scripts/frontier_freezeout_from_lattice.py` (Attack 3)

**Status: SUBSTANTIALLY addresses the gap.**

- Writes down the lattice master equation for taste-state occupation numbers:
  dN_i/dt = (transition terms) - (annihilation terms) + (creation terms).
- Shows the reduction to the Boltzmann equation in four steps:
  (1) define number densities n_i = N_i/V, (2) sum over visible/dark states,
  (3) add the Hubble dilution 3Hn from lattice expansion, (4) obtain the
  standard Boltzmann equation.
- States that the sole physical assumption is H > 0 (the universe expands).
- Verifies the freeze-out condition Gamma_ann = H numerically, confirming
  x_F ~ 25 for lattice inputs.

**Limitation:** The derivation in Attack 3 is SCHEMATIC. It describes the
steps in log/print statements but does not carry out the mathematical
reduction explicitly (no line-by-line algebra from master equation to
Boltzmann equation). The thermodynamic limit (many particles, continuous T)
is invoked but not rigorously controlled.

**Verdict:** Provides the correct FRAMEWORK for the derivation and identifies
the sole external assumption (H > 0). The mathematical reduction itself is
described but not executed as a rigorous proof.

#### 2. `docs/FREEZEOUT_FROM_LATTICE_NOTE.md`

**Status: Documents Attack 3 findings.**

- Reproduces the four-step reduction described in the script.
- States: "The Boltzmann equation is the continuum limit of the lattice
  master equation, not an imported equation."
- The note uses "continuum limit" here to mean the thermodynamic limit
  (many-particle limit), which is the correct identification per the
  thermodynamic closure note.
- Provides the updated provenance table showing all freeze-out parameters
  as STRUCTURAL.

**Verdict:** Documents the claim clearly but inherits the same limitation --
the reduction is described, not proved line-by-line.

#### 3. `scripts/frontier_freezeout_from_lattice.py` (Attack 1)

**Status: CLOSES g_* sub-gap completely.**

- Derives g_* = 106.75 exactly from the taste spectrum decomposition
  8 = (2,3) + (2,1) under SU(2) x SU(3), with N_gen = 3 from Z_3 orbits.
- The counting is fully structural: particle content from taste decomposition,
  spin statistics from staggered fermion signs, gauge boson count from
  dim(adj) of the gauge groups.

**Verdict:** g_* = 106.75 is fully derived. No gap remains here.

#### 4. `scripts/frontier_freezeout_from_lattice.py` (Attacks 2, 4)

**Status: CLOSES x_F sub-gap substantially.**

- Attack 2 derives x_F from the freeze-out condition using all lattice
  inputs. Shows x_F ~ 15-45 over 16 orders of magnitude in mass, centered
  at x_F ~ 25. The logarithmic insensitivity is the key structural feature.
- Attack 4 demonstrates R varies by only 33% over x_F = [10, 50], showing
  the prediction is robust against freeze-out details.

**Verdict:** x_F ~ 25 is derived from structural inputs. The robustness
to x_F variation further reduces this sub-gap's importance.

#### 5. `docs/DM_THERMODYNAMIC_CLOSURE_NOTE.md`

**Status: Supports the Boltzmann derivation framework.**

- Proves that the rho ~ T^4 (Stefan-Boltzmann) input to the Boltzmann
  equation follows from the thermodynamic limit on the lattice.
- Proves the lattice energy density converges to the BZ integral, which
  matches Stefan-Boltzmann at T << E_Planck.

**Verdict:** Closes the thermodynamic inputs to the Boltzmann equation.
Does not address the Boltzmann equation derivation itself.

### Summary for Gap 2

| Script/Doc | Master eq. framework | Line-by-line reduction | g_* derived | x_F derived | rho ~ T^4 |
|------------|:-:|:-:|:-:|:-:|:-:|
| `frontier_freezeout_from_lattice.py` (Atk 3) | YES | NO (schematic) | -- | -- | -- |
| `frontier_freezeout_from_lattice.py` (Atk 1) | -- | -- | YES | -- | -- |
| `frontier_freezeout_from_lattice.py` (Atk 2,4) | -- | -- | -- | YES | -- |
| `FREEZEOUT_FROM_LATTICE_NOTE.md` | YES (doc) | NO (schematic) | YES | YES | -- |
| `DM_THERMODYNAMIC_CLOSURE_NOTE.md` | -- | -- | -- | -- | YES |

**Bottom line:** The framework is in place: the lattice master equation for
taste states is identified, the reduction steps are enumerated, and all
subsidiary inputs (g_*, x_F, rho ~ T^4) are derived. What is missing is a
rigorous line-by-line mathematical reduction from the master equation to the
Boltzmann equation, controlling the thermodynamic limit explicitly.

---

## Overall Assessment

### What is already closed

1. **sigma_v functional form** (alpha^2/m^2): DERIVED from optical theorem + lattice Born.
2. **Sommerfeld enhancement**: DERIVED from lattice Green's function ratio.
3. **g_* = 106.75**: DERIVED from taste spectrum.
4. **x_F ~ 25**: DERIVED from structural freeze-out condition.
5. **rho ~ T^4**: DERIVED via thermodynamic limit (Weyl's law).
6. **"Continuum limit" misidentification**: RESOLVED (it is the thermodynamic limit).

### What remains open

1. **C = pi algebraic proof**: No existing script contains this. The numerical
   evidence is strong (lattice DOS convergence + Weyl's law guarantee), but a
   closed-form algebraic derivation linking the lattice phase-space integral
   to exactly pi has not been written. This could potentially be closed by
   computing the BZ integral of the Born T-matrix in closed form.

2. **Boltzmann equation rigorous derivation**: The lattice master equation
   framework is identified but the reduction is schematic. A rigorous
   derivation would need to: (a) write the master equation for a gas of
   lattice taste-states, (b) take the Stosszahlansatz (molecular chaos)
   limit, (c) show the annihilation kernel reduces to <sigma*v>, and
   (d) derive the 3Hn dilution term from the lattice expansion.

### Recommended next steps

1. For C = pi: Evaluate the Born-level lattice phase-space integral
   (integral of |V_tilde(q)|^2 over the on-shell surface in the BZ) in
   closed form. In the thermodynamic limit this integral is known to give
   pi from the solid-angle factor. The algebraic step is connecting the
   lattice BZ integral to the continuum result via Weyl's law.

2. For Boltzmann: Write a script that implements the master equation for N
   particles in 8 taste states on a finite lattice, evolves it numerically,
   and shows convergence to the Boltzmann equation solution as N grows.
   This would upgrade the derivation from "schematic" to "numerically
   verified with controlled convergence."
