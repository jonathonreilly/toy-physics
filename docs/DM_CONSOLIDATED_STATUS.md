# DM Relic Mapping: Consolidated Status

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Status:** BOUNDED (per review.md and Codex canonical claim ledger)
**Purpose:** Single-source consolidation of ALL DM lane work across the repository.

This document consolidates every file, script, number, and assessment related
to the DM relic mapping gate. It supersedes no individual note but serves as
the map to all of them.

---

## 1. The Full Derivation Chain (Every Step, Numbered)

The DM ratio R = Omega_DM / Omega_b = 5.48 is built from a 13-step chain
on Z^3 with Cl(3). Below is every step, its classification, the key number,
and the file that proves it.

| # | Step | Classification | Key Number | Proof File |
|---|------|---------------|------------|------------|
| 1 | Taste space C^8 = 1 + 3 + 3 + 1 | **EXACT** | 8 = 2^3 states | `DM_CLEAN_DERIVATION_NOTE.md` Step 1 |
| 2 | Visible sector T_1 + T_2 (6 gauge-charged states) | **EXACT** | 6 states | `DM_CLEAN_DERIVATION_NOTE.md` Step 2 |
| 3 | Dark sector S_0 + S_3 (2 gauge singlets) | **EXACT** | 2 states | `DM_CLEAN_DERIVATION_NOTE.md` Step 3 |
| 4 | Mass-squared ratio 3/5 from Hamming weights | **EXACT** | 9/15 = 3/5 | `DM_CLEAN_DERIVATION_NOTE.md` Step 4 |
| 5 | g_bare = 1 (Hamiltonian coefficient) | **BOUNDED** | g = 1.000 | `DM_CLEAN_DERIVATION_NOTE.md` Step 5; `DM_CLOSURE_CASE_NOTE.md` Argument 1 |
| 6 | alpha_s = 0.0923 from plaquette | **DERIVED** (inherits bounded from 5) | alpha_plaq = 0.0923 | `DM_CLEAN_DERIVATION_NOTE.md` Step 6 |
| 7 | Sommerfeld enhancement S_vis = 1.592 | **DERIVED** | S_vis = 1.592, S_dark = 1.000 | `DM_CLEAN_DERIVATION_NOTE.md` Step 7; `DM_RATIO_SOMMERFELD_NOTE.md` |
| 8 | Channel weighting f_vis/f_dark = 155/27 = 5.741 | **EXACT** | 155/27 | `DM_CLEAN_DERIVATION_NOTE.md` Step 8 |
| 9 | sigma_v = pi * alpha_s^2 / m^2 (lattice T-matrix) | **DERIVED** | C = pi (algebraically proved) | `DM_FINAL_GAPS_NOTE.md` (16/16 PASS); `DM_SIGMA_V_LATTICE_NOTE.md` |
| 10 | Boltzmann equation from lattice master equation | **DERIVED** | Stosszahlansatz error < 10^{-45000} | `DM_BOLTZMANN_THEOREM.md`; `DM_DIRECT_BOLTZMANN_NOTE.md` (21/21); `DM_STOSSZAHLANSATZ_THEOREM_NOTE.md` (14/14) |
| 11 | Freeze-out x_F ~ 25 | **DERIVED** | x_F = 25 (log-insensitive) | `DM_CLEAN_DERIVATION_NOTE.md` Step 11 |
| 12 | H(T) from Newtonian cosmology | **DERIVED** (k = 0 bounded) | H^2 = (8piG/3)rho | `DM_FRIEDMANN_FROM_NEWTON_NOTE.md` (13/13); `DM_CLOSURE_CASE_NOTE.md` Argument 2 |
| 13 | R = (3/5)(155/27)(1.592) = 5.48 | **BOUNDED** (inherits from 5, 12) | R = 5.483 | `DM_CLEAN_DERIVATION_NOTE.md` Step 13 |

**Count: 4 EXACT, 7 DERIVED, 2 BOUNDED.**

**Irreducible bounded inputs:**
1. g_bare = 1 -- Cl(3) normalization argument (whether constraint or convention)
2. k = 0 -- spatial flatness (observationally confirmed; numerically irrelevant at 10^{-47} per `DM_CLOSURE_CASE_NOTE.md`)

**Observational input:** eta = 6.12 x 10^{-10} (enters Omega_b only, not Omega_DM)

### Detailed provenance flow

```
Cl(3) bit strings -----> mass ratio 3/5 -----------\
                                                      \
SU(3) x SU(2) --------> Casimir channels 155/27 ---+--> R_base = 31/9 = 3.444
(lattice gauge group)    f_vis, f_dark              /
                                                   /
Plaquette action -------> alpha_plaq = 0.092 -----+
     |                        |                    |
[BOUNDED: g_bare=1]           |                    |
                              v                    |
Lattice Green's fn ----> Coulomb Sommerfeld -----> S_vis = 1.592
                              ^                    |
Taste spectrum --> g_*=106.75 |                    |
Heat kernel ----> n_eq        |                    |
Lattice master eq ----------> Boltzmann eq.        |
Poisson coupling -----------> Friedmann eq.        |
Spectral gap + 2nd law -----> H > 0               |
     |                        |                    |
     +-----> x_F = 25 -------+                    |
                                                   v
                                            R = R_base * S_vis = 5.48
```

### R values from different approaches

| Approach | R | Deviation from R_obs = 5.47 | File |
|----------|---|----------------------------|------|
| Main (x_F = 28.8, Coulomb Sommerfeld) | 5.66 | 3.4% | `frontier_dm_relic_mapping.py` |
| Wildcard (Perron spectral) | 5.32 | 2.8% | `frontier_dm_relic_mapping_wildcard.py` |
| **Synthesis (x_F = 25, Coulomb Sommerfeld)** | **5.48** | **0.2%** | `frontier_dm_relic_synthesis.py` |
| Gap-closure (thermodynamic limit) | 5.56 | 1.7% | `frontier_dm_relic_gap_closure.py` |
| Finite lattice graph-native | 5.66 | 3.4% | `frontier_dm_relic_mapping.py` |
| Observed (Planck 2018) | 5.47 | --- | --- |

### Sensitivity

| Parameter | Range | R range | dR/R |
|-----------|-------|---------|------|
| g_bare | [0.9, 1.1] | [4.99, 6.10] | 20% |
| g_bare | [0.95, 1.05] | [5.22, 5.78] | 10% |
| x_F | [15, 35] | [4.96, 5.92] | 17.5% |
| x_F | [20, 30] | [5.24, 5.71] | 8.7% |
| alpha_s | [0.08, 0.10] | [5.17, 5.68] | 9.3% |
| sigma_v coefficient | [0.5x, 2x] nominal | via x_F: ~1% | 1.0% |

---

## 2. The DM Numerator (Omega_DM)

The dark matter abundance Omega_DM is set by thermal freeze-out of the S_3
taste state (Hamming weight h = 3, gauge singlet). This is the STRONG part
of the derivation.

### 2.1 DM candidate identification

The 8 taste states of Cl(3) decompose under orbits classified by Hamming weight:
- h = 0: S_0 (scalar singlet, 1 state) -- massless, does not freeze out
- h = 1: T_1 (vector triplet, 3 states) -- SU(3) color-charged (visible)
- h = 2: T_2 (pseudovector triplet, 3 states) -- SU(2) weak-charged (visible)
- h = 3: S_3 (pseudoscalar singlet, 1 state) -- gauge singlet (DM candidate)

S_3 is the ONLY massive gauge singlet. Wilson mass: m_S3 = 3 * m_0.

**Status: EXACT.** Combinatorial identity on Z^3.

### 2.2 Annihilation cross-section

sigma_v = pi * alpha_s^2 / m^2

The coefficient C = pi is algebraically proved from:
1. 3D solid angle: 4pi from S^2 topology (topological invariant)
2. s-wave: Oh cubic symmetry guarantees l = 0
3. Phase space: |M|^2 / (phase space) = 32pi^2 alpha^2 / (32pi) = pi alpha^2
4. IR dispersion: E(k) = |k| + O(k^3) from lattice Taylor expansion
5. Density of states: E^2/(2pi^2) from Weyl's law (Moise 1952)

**Status: DERIVED (all 8 sub-tests PASS, 6 EXACT + 2 DERIVED).** File: `DM_FINAL_GAPS_NOTE.md`.

### 2.3 Boltzmann equation

The Boltzmann equation df/dt + v.grad(f) = C[f] is DERIVED from the lattice
master equation dP/dt = WP via:

1. **Master equation is lattice-native.** W_{ij} from Fermi golden rule on
   the staggered Hamiltonian. Not imported.
2. **Stosszahlansatz is a THEOREM.** Two independent proofs:
   - Spectral gap + Combes-Thomas + Wick: factorization error < 10^{-22000} (`DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`, 14/14)
   - Direct matrix inversion: factorization error < 10^{-45000} (`DM_DIRECT_BOLTZMANN_NOTE.md`, 21/21)
3. **Coarse-graining.** Partial trace + proved factorization gives the Boltzmann collision integral.
4. **H-theorem.** Entropy monotonically non-decreasing.

**Remaining caveat:** Proof is for the free (Gaussian) theory. Extension to
the interacting case requires spectral gap persistence under weak coupling.

The full lattice-Boltzmann reduction theorem is stated in `DM_BOLTZMANN_THEOREM.md`
but verified only on a small 1D toy interaction model per review.md.

**Status: DERIVED (bounded at the paper bar per Codex).**

### 2.4 Friedmann equation H(T)

The first Friedmann equation H^2 = (8piG/3)rho follows from Newtonian
cosmology (Milne 1934):
1. Newton's law from lattice Poisson equation (EXACT)
2. Shell theorem from Gauss's law on Z^3 (EXACT)
3. Energy conservation for E = 0 shell (k = 0, BOUNDED)

**Key insight** (from `DM_FINAL_GAPS_NOTE.md` and `DM_FLAGSHIP_CLOSURE_NOTE.md`):
Freeze-out uses only the FIRST Friedmann equation. The pressure term rho + 3p
enters only the SECOND equation (acceleration), which freeze-out never invokes.
Therefore Newtonian cosmology suffices.

**k = 0 irrelevance** (from `DM_CLOSURE_CASE_NOTE.md`): At freeze-out
(T_F ~ 10^{18} GeV), the curvature term |k/a^2| is suppressed by 10^{-47}
relative to the radiation term. The value of k does not matter.

**Status: DERIVED (k = 0 numerically irrelevant, not assumed).**

### 2.5 Freeze-out and relic abundance

x_F ~ 25 from the lattice Boltzmann equation with Gamma_ann = H condition.
Log-insensitive: changing sigma_v by 2x shifts x_F by ~2 units, R by ~1%.

Omega_DM h^2 = (1.07e9 GeV^{-1}) x_F / (sqrt(g_*) M_Pl sigma_v)

**Status: DERIVED.** The DM NUMERATOR is the strong part of the chain.

---

## 3. The DM Denominator (Omega_b -> eta)

The baryon abundance Omega_b = 3.65e7 * eta requires the baryon-to-photon
ratio eta = 6.12 x 10^{-10}. This is the WEAK part -- where the baryogenesis
chain lives.

### 3.1 The conversion eta -> Omega_b

This is pure kinematics (counting, not nuclear physics). See `BBN_FROM_FRAMEWORK_NOTE.md`:

    Omega_b = eta * n_gamma * m_p / rho_crit

No nuclear reaction rates, binding energies, or cross-sections needed. Nuclear
physics determines the helium fraction Y_p, not Omega_b. Setting Y_p = 0
shifts Omega_b by only 0.18%.

**Status: CLOSED (no nuclear physics needed).**

### 3.2 Where does eta come from?

Three Sakharov conditions are all present in the framework:

| Condition | Source | Score | File |
|-----------|--------|-------|------|
| B violation | SU(2) sphalerons from derived gauge structure | 0.90 | `BARYOGENESIS_NOTE.md` |
| CP violation | Z_3 cyclic permutation: delta = 2pi/3, J = 3.1e-5 | 0.75 | `BARYOGENESIS_NOTE.md` |
| Out-of-equilibrium | CW phase transition (taste scalars) | 0.40-0.85 | `EWPT_STRENGTH_NOTE.md`, `EWPT_LATTICE_MC_NOTE.md`, `EWPT_GAUGE_CLOSURE_NOTE.md` |

### 3.3 Every approach to computing eta

**Approach A: Parametric (original, `frontier_baryogenesis.py`)**
- Formula: n_B/s = (N_f/4)(Gamma_ws/T^4)(D_q*T/v_w) S_CP (v/T)/(L_w*T)
- Imported: v_w = 0.05, L_w*T = 15, D_q*T = 6
- Result: eta ~ 6e-10 IF v/T ~ 0.52
- Status: CONDITIONAL on v/T

**Approach B: Framework-seeded transport (`ETA_FROM_FRAMEWORK_NOTE.md`)**
- Framework-derived: J_Z3 = 3.1e-5, v/T = 0.56, Gamma_sph ~ alpha_w^5 T^4
- Imported: v_w, L_w*T, D_q*T (low sensitivity -- double-exponential washout)
- Result: eta depends exponentially on v/T, linearly on transport prefactor
- Key finding: transport 100x variation shifts v/T crossing by only 0.05
- Status: OPEN (transport imported)

**Approach C: Coupled transport at T_n (`DM_COUPLED_TRANSPORT_NOTE.md`)**
- Self-consistent solution at T_n = 180.6 GeV
- v_w = 0.062, L_w*T = 48.1, D_q*T = 6.07
- Result: eta_coupled = 2.31e-10 (factor 2.67 below observed)
- Status: BOUNDED (imports C_tr calibration from FHS 2006)

**Approach D: Taste-enhanced eta (`DM_TASTE_ENHANCED_ETA_NOTE.md`)**
- Applies 8/3 taste trace factor to eta_coupled
- eta_corrected = 2.31e-10 * 8/3 = 6.16e-10 (0.5% from observed)
- Status: BOUNDED (Codex says post-hoc multiplier is not closure)

**Approach E: Native eta without post-hoc (`DM_NATIVE_ETA_NOTE.md`)**
- Taste factor IN the source term, C_tr derived from diffusion network
- v(T_n)/T_n = 0.73 (from analytic daisy, not MC calibration)
- Result: eta = 5.22e-10 (85% of observed, ratio 0.85)
- Status: BOUNDED (15% shortfall, see Root Cause Analysis)

**Approach F: Taste-corrected EWPT chain (`frontier_dm_ewpt_taste_corrected.py`)**
- E_total/E_daisy = 2.0 EXACTLY (from `frontier_taste_sector_resolved.py`)
- Propagates E x 2 through full nonlinear chain
- Problem: ALL points go supersonic (detonation regime)
- Status: BOUNDED (detonation problem, see Section 7)

### 3.4 The factor 2.67 gap and the 8/3 taste enhancement

The gap between eta_coupled = 2.31e-10 and eta_obs = 6.12e-10 is exactly
the ratio 8/3 = 2.667, which comes from the taste trace:

- Standard transport equations: Tr[Y^dag Y] = 3 y_t^2 (3 generations)
- Lattice transport equations: Tr[Y^dag Y] = 8 y_t^2 (8 taste states)
- Enhancement: 8/3 = 2.667

The factor is protected against taste splitting (trace invariance: sum of
eigenvalues = 8 regardless of degeneracy breaking).

**Codex assessment** (review.md): The taste-enhanced eta is NOT closure
authority. It multiplies an already-bounded result by a post-hoc factor.
The transport equations need to be rebuilt with the explicit taste-enhanced
source.

### 3.5 The sphaleron coupling proof for 8/3

`frontier_taste_sphaleron_coupling.py` proves (4 independent layers):
1. **Layer A**: All 8 taste states are SU(2) doublets (Casimir = 3/4), zero singlets
2. **Layer B**: No chirality in d = 3 (Gamma_5 does not exist as a grading)
3. **Layer C**: 3D dimensionally-reduced theory treats all 8 states equivalently
4. **Layer D**: ABJ anomaly equation gives Delta_B = N_doublets = 8 per sphaleron

**Codex assessment**: Structural proof is correct. But it proves the FACTOR,
not the CHAIN. The factor 8/3 is necessary but not sufficient for closure.

---

## 4. The EWPT Surface

This is the single most internally contradictory part of the DM lane. Multiple
scripts give different v/T numbers from different methods, and there is no
reconciled surface.

### 4.1 All v/T numbers in the repository

| Method | v(T_c)/T_c | v(T_n)/T_n | File |
|--------|-----------|-----------|------|
| SM perturbative (no extras) | 0.015 | --- | `EWPT_STRENGTH_NOTE.md` |
| Perturbative 1-loop (m_S = 80 GeV) | 0.37-0.44 | --- | `EWPT_STRENGTH_NOTE.md` |
| Daisy-improved (lam_p = 0.3) | 1.21 | --- | `EWPT_STRENGTH_NOTE.md` |
| Full 1-loop (m_S = 80 GeV) | 0.37 | --- | `EWPT_STRENGTH_NOTE.md` |
| **Scalar-only MC (L -> inf)** | **0.49 +/- 0.02** | --- | `EWPT_LATTICE_MC_NOTE.md` |
| MC + gauge R = 1.5 (imported) | 0.73 +/- 0.03 | --- | `EWPT_LATTICE_MC_NOTE.md` |
| **Gauge-effective MC** | **0.56 +/- 0.05** | --- | `EWPT_GAUGE_CLOSURE_NOTE.md` |
| Analytic bound (monotonicity) | >= 0.49 | --- | `EWPT_GAUGE_CLOSURE_NOTE.md` |
| First-principles R derivation | 0.51 | --- | `EWPT_GAUGE_CLOSURE_NOTE.md` |
| Daisy-resummed (m_phys = 120 GeV, lam_p = 0.30) | 0.55 | --- | `DM_EWPT_NATIVE_NOTE.md` |
| **Daisy-resummed (m_phys = 200 GeV, lam_p = 0.30)** | **2.29** | --- | `DM_EWPT_NATIVE_NOTE.md` |
| MC-calibrated R_NP = 1.57 | 0.56 | 0.80 | `DM_NUCLEATION_TEMPERATURE_NOTE.md` |
| Analytic daisy R_NP = 1.68 | --- | 0.73 | `DM_NATIVE_ETA_NOTE.md` |
| Perturbative CW at T_c | 0.29 | --- | `DM_NATIVE_ETA_NOTE.md` |
| **E x 2 corrected (taste-resolved)** | **1.10** | **1.45** | `frontier_dm_ewpt_taste_corrected.py` |
| 2HDM lattice literature | 0.5-3.0 | --- | `EWPT_STRENGTH_NOTE.md` |

### 4.2 Which is most trustworthy?

**Gauge-effective MC (v/T = 0.56 +/- 0.05):** This is the single best
number. It runs a 3D scalar MC with gauge-corrected parameters computed
from first principles. Three independent attacks all converge. This is
what `EWPT_GAUGE_CLOSURE_NOTE.md` establishes.

**E x 2 corrected (v/T = 1.10 at T_c):** This incorporates the
taste-sector-resolved result that E_total/E_daisy = 2.0 EXACTLY. It
is structurally more complete. But it drives the transition so strongly
that nucleation produces detonation (Section 7).

### 4.3 Internal contradictions

1. **Older notes use v/T ~ 0.5 (partial washout).** `BARYOGENESIS_NOTE.md`
   says eta requires v/T ~ 0.52 in the partial-washout regime. But newer
   EWPT notes give v/T > 1.

2. **Which v/T matters for baryogenesis?** The review.md identifies this
   mismatch: "until one note states which of v(T_c)/T_c, v(T_n)/T_n, or
   wall-local v/T is the real baryogenesis input, the lane is not promotable."

3. **v/T = 0.56 vs v/T = 1.10 vs v/T = 2.29:** These come from different
   approximation levels. The 0.56 is from gauge-effective MC (most controlled).
   The 1.10 includes the E x 2 taste correction (structurally correct but
   produces detonation). The 2.29 is from daisy at m_phys = 200 GeV
   (strongly dependent on scalar mass).

4. **The Daisy-resummed numbers span 0.55 to 2.29** depending on m_phys
   and lambda_p. The taste scalar mass is NOT uniquely predicted by the
   framework.

### 4.4 Critical temperatures

| Source | T_c (GeV) | T_n (GeV) | T_n/T_c |
|--------|----------|----------|---------|
| Lattice MC | 182 | ~173 | ~0.95 |
| Nucleation (MC-calibrated) | 183.6 | 180.6 | 0.983 |
| Nucleation (Daisy E x 1) | --- | --- | 0.90 |
| Nucleation (E x 2 corrected) | 176.7 | 155-165 | 0.88-0.93 |
| Nucleation (Daisy, `frontier_dm_nucleation.py`) | 222.6 | 200.5 | 0.90 |

The different T_c values reflect different effective potential parameters.
The spread (176-223 GeV) is a genuine systematic uncertainty from the
approximation method.

---

## 5. The Transport Sector

### 5.1 D_q*T (quark diffusion coefficient)

| Script/Method | D_q*T | Status |
|---------------|-------|--------|
| AMY leading-log | 1.6 | Literature import |
| Coulomb-log formula (C_0 = 0.5) | 3.9 | Analytic + inserted C_0 |
| AMY NLO (Moore factor ~3) | 4.9 | Literature import |
| Full LO with Coulomb log | 6.5 | AMY + framework alpha_s |
| Lattice QCD (Ding+ 2011, quenched) | ~3-6 | Non-perturbative |
| Imported value (baryogenesis scripts) | 6.0 | Literature |
| Native lattice, static-screened (L=12) | 8.3 | Framework (overestimates) |
| **HTL-resummed lattice (L=16)** | **3.1** | **Framework (best)** |
| HTL-resummed (extrapolated) | ~3.0-3.2 | Framework |

**Evolution of D_q*T derivation:**
1. `DM_TRANSPORT_DERIVED_NOTE.md`: Plugged framework alpha_s into AMY/Moore formulas. Range [3.6, 7.2]. Codex rejected as "not first-principles."
2. `DM_TRANSPORT_GREENKUBO_NOTE.md`: Green-Kubo with lattice current-current correlator, but landed on analytic continuum-limit Coulomb-log formula with C_0 = 0.5. Result: 3.9.
3. `DM_DQT_NATIVE_NOTE.md`: Fully native lattice mode sum, no analytic formula. Result: 8.3. Too high because static Debye screening overscreens magnetic modes.
4. `DM_DQT_HTL_NOTE.md`: HTL-improved propagators with Landau damping for magnetic sector. Result: 3.1. Magnetic sector dominates (68% of scattering rate).

**Status: DERIVED (one-loop skeleton + HTL resummation). 30% uncertainty from loop order.**

### 5.2 v_w (bubble wall velocity)

| Script/Method | v_w | Status |
|---------------|-----|--------|
| Simple force balance (prev.) | 0.001-0.009 | Underestimates |
| Full bounce wall (prev.) | 0.01-0.10 | Wide range |
| **Boltzmann closure (T_n/T_c = 0.98)** | **0.014** | **Framework** |
| Boltzmann closure range | [0.006, 0.048] | T_n/T_c = [0.95, 0.99] |
| Coupled transport fixed point | 0.062 | Self-consistent |
| Imported value | 0.05 | Literature |
| E x 2 corrected | **DETONATION** | Supersonic! |

**Critical finding** (`DM_NUCLEATION_FINDING_NOTE.md`): At T_n/T_c = 0.90
(from Daisy-resummed potential), the driving pressure DeltaV/T^4 is too
large for Boltzmann friction to balance. The wall velocity enters the
detonation regime (v_w > c_s ~ 0.58). This kills the transport-mediated
baryogenesis mechanism.

**Status: BOUNDED.** The v_w determination requires either a different taste
scalar mass, full 3D lattice simulation, or non-linear friction computation.

### 5.3 L_w*T (bubble wall thickness)

| Method | L_w*T | File |
|--------|-------|------|
| Curvature / parametric | 13.8 | `DM_BOUNCE_WALL_NOTE.md` |
| Kink ODE (T/T_c = 0.99) | 16-18 | `DM_BOUNCE_WALL_NOTE.md` |
| Kink ODE (T/T_c = 0.95) | 8-10 | `DM_BOUNCE_WALL_NOTE.md` |
| Nucleation (MC-calibrated) | 47.6 at T_n | `DM_NUCLEATION_TEMPERATURE_NOTE.md` |
| Coupled transport | 48.1 | `DM_COUPLED_TRANSPORT_NOTE.md` |
| Imported | 15 | `BARYOGENESIS_NOTE.md` |
| Median of reliable methods | ~12 [8, 18] | `DM_BOUNCE_WALL_NOTE.md` |

Note the dramatic difference: at T_c the wall is thin (~14), but at T_n
(with more supercooling) it broadens to ~48.

**Status: DERIVED.** The CW bounce equation gives L_w*T from framework parameters.

### 5.4 C_tr (transport coefficient)

| Method | C_tr | File |
|--------|------|------|
| FHS (2006) calibration (imported) | 1.56e-6 | `DM_COUPLED_TRANSPORT_NOTE.md` |
| Framework diffusion network | 1.72e-6 | `DM_NATIVE_ETA_NOTE.md` |

The native C_tr differs from the imported value by 11%. Codex notes that
C_tr calibration is still an import.

**Status: BOUNDED.**

### 5.5 Combined transport sensitivity

From `DM_R_SENSITIVITY_NOTE.md`:

| Parameter | Range | Factor span | dR/R |
|-----------|-------|-------------|------|
| D_q*T | [2.17, 4.03] | 1.9x | 66% |
| v_w | [0.006, 0.048] | 8.0x | 300% |
| L_w*T | [10, 18] | 1.8x | 62% |
| **Combined** | --- | **26.7x** | **653%** |

**Key structural result:** R depends on eta LINEARLY (not logarithmically).
The transport prefactor P = D_q*T / (v_w * L_w*T) propagates directly into
eta and hence into R. There is no logarithmic suppression. The hypothesis
that transport precision doesn't matter is falsified.

However, the DM freeze-out sector (Omega_DM) is independent of transport.
The transport uncertainty enters ONLY through Omega_b via eta.

---

## 6. The Taste Enhancement (8/3)

### 6.1 The structural proof

`frontier_taste_sphaleron_coupling.py` proves all 8 taste states couple
to SU(2) sphalerons. Four independent layers:

**Layer A (Representation theory):** All 8 states of C^8 carry j = 1/2
under the derived SU(2). The SU(2) Casimir eigenvalue is 3/4 for all 8
states. There are ZERO singlets.

**Layer B (No chirality in d=3):** In 3 spatial dimensions, Gamma_5^2 = -I
(not +I), so there is no chirality grading. The 4D notion "only left-handed
doublets couple to sphalerons" does not apply. All 8 states participate.

**Layer C (Dimensional reduction):** The 3D effective theory at T_EW treats
all 8 states equivalently. The sphaleron is a 3D gauge configuration.

**Layer D (Anomaly equation):** The ABJ anomaly gives Delta_B = N_doublets = 8
per sphaleron transition.

### 6.2 The taste-sector-resolved computation

`frontier_taste_sector_resolved.py` decomposes observables by BZ corner
(Hamming weight sector):

| Sector | Dimension | EWPT E_s/E_total | Pi_s/Pi_total | R_s(overlap) |
|--------|-----------|-----------------|--------------|-------------|
| Singlet (h=0) | 1 | 0.25 | 0.125 | --- |
| Triplet (h=1) | 3 | 0.25 | 0.375 | --- |
| Anti-triplet (h=2) | 3 | 0.25 | 0.375 | --- |
| Pseudoscalar (h=3) | 1 | 0.25 | 0.125 | --- |

Key result: **E_total / E_daisy = 2.0000 EXACTLY.** The standard daisy
approximation counts only the singlet + triplet sectors (4 modes). All 8
modes contribute equally to the thermal cubic coefficient.

### 6.3 Why Codex says it's not closure

From review.md:

1. The 8/3 factor multiplies an already-bounded eta_coupled result post-hoc.
   It does not rebuild the transport equations with the explicit
   taste-enhanced source from the start.

2. The C_tr calibration from FHS (2006) is still imported. The native C_tr
   (1.72e-6 vs 1.56e-6) is different by 11%.

3. The non-perturbative v(T_n)/T_n calibration is untouched.

4. The native eta note (`DM_NATIVE_ETA_NOTE.md`) addresses objection 1
   (puts 8/3 in the source term) and objection 2 (derives C_tr natively).
   But it gets eta = 5.22e-10, which is 15% below observed. The 15%
   shortfall traces to the daisy v/T being 0.73 instead of 0.80.

**Bottom line:** The 8/3 is structurally proved. But it alone does not close
the baryogenesis chain because the transport framework it sits in is still bounded.

---

## 7. The Detonation Problem

### 7.1 What happens with E x 2

The taste-sector-resolved computation proves E_total/E_daisy = 2.0 exactly.
When this E x 2 correction propagates through the nonlinear EWPT chain
(`frontier_dm_ewpt_taste_corrected.py`):

1. v(T_c)/T_c increases from ~0.56 to ~1.10 (much stronger transition)
2. The barrier is taller and sharper
3. More supercooling is needed for nucleation (T_n/T_c ~ 0.88-0.93)
4. The driving pressure DeltaV(T_n)/T_n^4 becomes very large
5. **The Boltzmann friction CANNOT balance the driving pressure**
6. All solutions give v_w > c_s (speed of sound)
7. The wall enters the **detonation regime**

### 7.2 Why detonation kills baryogenesis

Baryogenesis via transport (the mechanism in all the eta computations above)
requires **deflagration** (subsonic walls):
- A compression wave propagates AHEAD of the wall
- CP-violating currents diffuse into the symmetric phase
- Sphalerons convert the asymmetry to baryon number

In detonation:
- A rarefaction wave propagates BEHIND the wall
- No perturbation ahead of the wall
- The transport mechanism does not operate

### 7.3 The finding from `DM_NUCLEATION_FINDING_NOTE.md`

At m_s = 120 GeV: T_n/T_c = 0.90, wall goes supersonic.
At m_s = 200 GeV: DeltaV is smaller, v_w ~ 0.01 (subsonic, deflagration survives).

**The framework does NOT uniquely predict m_s.** The taste scalar mass is
estimated at O(m_W) by naturalness, not derived.

### 7.4 Possible resolutions

1. **Taste scalar mass in the deflagration window:** If m_s ~ 200 GeV or
   larger, the transition is weaker and deflagration survives.

2. **High-T expansion breaks down:** The 1-loop Daisy at T_n/T_c = 0.90
   may overestimate the barrier. Full 3D lattice simulation needed.

3. **Non-linear friction:** At large v_w, particle-production backreaction
   can increase friction substantially. The linearized Boltzmann friction
   used here underestimates drag.

4. **Alternative baryogenesis mechanism:** Cold baryogenesis, bubble
   collisions, or other mechanisms that operate in the detonation regime.

5. **Adjust nucleation criterion:** S_3/T = 160 instead of 140 gives T_n
   closer to T_c, less supercooling.

---

## 8. What Works vs What Doesn't

### What WORKS (strong results)

1. **Taste decomposition 1+3+3+1:** EXACT combinatorial identity on Z^3.
   Zero controversy.

2. **Mass ratio 3/5:** EXACT from Hamming weights. Zero parameters.

3. **Channel ratio 155/27:** EXACT SU(3) x SU(2) group theory.

4. **R_base = 31/9 = 3.444:** Product of the above. EXACT and parameter-free.

5. **g_* = 106.75:** EXACT from taste spectrum counting.

6. **Sommerfeld S_vis = 1.592:** DERIVED from lattice Coulomb potential
   with SU(3) channel decomposition. Controlled at the percent level.

7. **Stosszahlansatz theorem:** PROVED with error < 10^{-45000}. Two
   independent derivations. Neither cites external theorems.

8. **sigma_v coefficient C = pi:** Algebraically proved from 3D kinematics.

9. **Boltzmann equation:** DERIVED from lattice master equation.

10. **H(T) from Newtonian cosmology:** DERIVED without GR.

11. **R = 5.48 at g_bare = 1:** The structural backbone gives the right
    answer with one bounded parameter. Sensitivity g in [0.95, 1.05]
    gives R in [5.22, 5.78].

12. **8/3 taste trace factor:** Structurally proved (4 independent layers).
    Protected by trace invariance.

13. **Three Sakharov conditions:** All present in the framework at the
    structural level.

14. **BBN chain:** Pure kinematics, no nuclear physics.

### What DOESN'T work (honest failures)

1. **g_bare = 1 is not derived dynamically.** It is a normalization/algebraic
   argument. Self-duality at beta = 6 does NOT provide an independent
   selection principle (honest negative, `G_BARE_SELF_DUALITY_NOTE.md`).
   No other lattice selection principle succeeds.

2. **eta is NOT derived.** The baryogenesis chain lands in the right
   ballpark (factor 2.67 from observed without 8/3, 0.85x with native
   derivation) but is not closed. Codex identifies multiple imports.

3. **The EWPT surface is internally contradictory.** Multiple v/T values
   (0.49 to 2.29) from different methods. No reconciled surface.

4. **The detonation problem.** With the structurally correct E x 2, all
   nucleation points go supersonic. This potentially kills the transport
   baryogenesis mechanism.

5. **Transport uncertainty dominates R.** dR/R = 653% from combined
   transport corners. v_w alone spans 8x.

6. **The Boltzmann theorem is verified only on a 1D toy model.** The
   thermodynamic limit and expansion steps lean on standard
   Riemann/Weyl/Newtonian structure.

7. **C_tr calibration is imported.** Even the native derivation gives
   11% different from FHS (2006).

8. **v(T_n)/T_n vs v(T_c)/T_c confusion.** The review.md explicitly
   flags this: "until one note states which v/T is the real baryogenesis
   input, the lane is not promotable."

### What is HONESTLY BOUNDED (could go either way)

1. **g_bare = 1:** 7/10 strength argument (compelling within framework,
   a skeptic who accepts A5 should accept g = 1).

2. **k = 0:** 9/10 (numerically irrelevant by 45 orders of magnitude).

3. **Thermodynamic limit:** Standard for lattice field theory, numerically
   verified to L = 20. Not a theorem for this specific graph family.

4. **Interacting Stosszahlansatz:** Proved for free theory, spectral gap
   persistence under weak coupling needed for interacting case.

---

## 9. Attack Vectors Still Open

### 9.1 What would close the DM gate for the paper

**The honest answer from review.md's "best attack" list:**

1. **Derive T_n from the bounce/effective-potential surface** using
   S_3(T_n)/T_n ~ 140. This IS done (`DM_NUCLEATION_TEMPERATURE_NOTE.md`,
   `frontier_dm_nucleation.py`) but different potential parameters give
   different T_n values (180-200 GeV), and the E x 2 correction pushes
   into detonation.

2. **Derive the wall-local CP source directly on the physical taste
   space.** Do not use a post-hoc 8/3 multiplier. The native eta note
   (`DM_NATIVE_ETA_NOTE.md`) does this but gets 5.22e-10 (15% low).

3. **Derive C_tr from the framework transport system** instead of FHS
   calibration. The native derivation gives 1.72e-6 vs imported 1.56e-6.
   Close but not yet reconciled.

4. **Rebuild v_w on the reconciled native surface** with no stale
   imported non-perturbative enhancement.

5. **Solve the coupled transport fixed point** instead of scanning
   parameters independently. Done in `DM_COUPLED_TRANSPORT_NOTE.md`
   but still imports C_tr.

6. **Resolve the detonation problem.** This is the key new blocker.
   Possible routes:
   - Show that taste scalar mass m_s ~ 200 GeV is the physical value
     (keeps deflagration)
   - Include non-linear friction (particle production at the wall)
   - Full 3D lattice simulation of the EWPT with taste scalars
   - Demonstrate an alternative baryogenesis mechanism in detonation

7. **Reconcile the v/T surface.** State definitively which v/T is the
   baryogenesis input and compute it consistently.

### 9.2 What would close the gate definitively (beyond the paper)

1. **Full non-perturbative lattice EWPT** with taste scalars. This
   simultaneously determines v/T, T_n, L_w, and the nature of the
   transition (deflagration vs detonation). This is the single
   computation that would resolve everything.

2. **Derive g_bare from a lattice self-consistency condition.** This
   would eliminate the last bounded input in the numerator chain.

3. **Compute eta from first principles** (close baryogenesis). This
   requires routes 1-7 above plus a reconciled transport framework.

4. **ADM (Asymmetric Dark Matter) route.** If the dark sector carries
   a conserved charge violated by SU(2) sphalerons, then R = (m_DM/m_p)
   * (charge ratio), bypassing baryogenesis entirely. Explored in
   `DM_ELEGANT_BRAINSTORM.md` Approach 2. Feasibility 5/10, very high
   payoff.

### 9.3 The root cause (`ROOT_CAUSE_ANALYSIS_THREE_GATES.md`)

All three remaining gates (DM eta, y_t, CKM) have residuals pointing
DOWNWARD. The common root is the taste activity fraction: in each case,
an approximation undercounts how many of the 8 taste states participate.

For DM: The daisy approximation counts 4 of 8 taste modes in the thermal
cubic E. The full taste-resolved computation gives E x 2. But E x 2
drives the transition so strongly that it creates the detonation problem.

The single computation that would close all three gates simultaneously:
a **taste-sector-resolved effective potential** on the Cl(3) lattice,
resolving E_s, Pi_s, and R_s for each sector (1, 3, 3*, 1'). This is
partially done in `frontier_taste_sector_resolved.py` but not yet at
full thermodynamic scale.

---

## Script Reference Index

### Core DM chain scripts

| Script | Key result | PASS/FAIL |
|--------|-----------|-----------|
| `frontier_dm_relic_mapping.py` | R = 5.66 (graph-native) | 9/10 (T^4 FAIL on finite lattice) |
| `frontier_dm_relic_mapping_wildcard.py` | R = 5.32 (Perron spectral) | --- |
| `frontier_dm_relic_synthesis.py` | R = 5.48 (synthesis) | 4/4 |
| `frontier_dm_relic_gap_closure.py` | R = 5.56, zero imports for R | 11/11 |
| `frontier_dm_relic_paper.py` | Honest provenance audit | --- |
| `frontier_dm_clean_derivation.py` | 13-step chain, 4 EXACT + 7 DERIVED + 2 BOUNDED | --- |
| `frontier_dm_final_gaps.py` | sigma_v C=pi proved, Boltzmann derived | 16/16 |
| `frontier_dm_theorem_application.py` | Full chain exhibition | 25/25 |

### Boltzmann/Stosszahlansatz scripts

| Script | Key result |
|--------|-----------|
| `frontier_dm_stosszahlansatz.py` | Factorization error < 10^{-22000} |
| `frontier_dm_stosszahlansatz_theorem.py` | Theorem statement and proof |
| `frontier_dm_direct_boltzmann.py` | Direct computation: error < 10^{-45000} |
| `frontier_dm_boltzmann_theorem.py` | Full Boltzmann reduction theorem |

### Sommerfeld and cross-section scripts

| Script | Key result |
|--------|-----------|
| `frontier_dm_ratio_sommerfeld.py` | Channel-weighted Sommerfeld S_vis = 1.592 |
| `frontier_dm_ratio_structural.py` | R_base = 31/9 structural |
| `frontier_dm_sigma_v_lattice.py` | sigma_v from lattice T-matrix |
| `frontier_dm_coulomb_from_lattice.py` | V(r) = -alpha/r from Green's function |

### Transport scripts

| Script | Key result |
|--------|-----------|
| `frontier_dm_transport_derived.py` | All 3 transport params from framework couplings |
| `frontier_dm_transport_greenkubo.py` | D_q*T = 3.9 from Green-Kubo |
| `frontier_dm_dqt_native.py` | D_q*T = 8.3 native lattice (static-screened) |
| `frontier_dm_dqt_htl.py` | D_q*T = 3.1 HTL-resummed |
| `frontier_dm_vw_derivation.py` | v_w = 0.014 from Boltzmann closure |
| `frontier_dm_bounce_wall.py` | L_w*T ~ 12 [8, 18] from CW bounce |
| `frontier_dm_coupled_transport.py` | Coupled fixed point: v_w = 0.062, eta = 2.31e-10 |

### EWPT scripts

| Script | Key result |
|--------|-----------|
| `frontier_ewpt_strength.py` | Perturbative v/T estimates |
| `frontier_ewpt_lattice_mc.py` | Scalar MC v/T = 0.49; + gauge = 0.73 |
| `frontier_ewpt_gauge_closure.py` | Gauge-effective MC v/T = 0.56 |
| `frontier_dm_ewpt_native.py` | Daisy-resummed v/T, CLOSED for R_NP |
| `frontier_dm_nucleation_temperature.py` | T_n = 180.6 GeV, v(T_n)/T_n = 0.80 |
| `frontier_dm_nucleation.py` | T_n = 200.5 GeV, DETONATION finding |
| `frontier_dm_ewpt_taste_corrected.py` | E x 2 chain, detonation at all points |

### Baryogenesis and eta scripts

| Script | Key result |
|--------|-----------|
| `frontier_baryogenesis.py` | Parametric eta ~ 6e-10 IF v/T ~ 0.52 |
| `frontier_eta_from_framework.py` | 3 derived + 3 imported inputs |
| `frontier_dm_taste_enhanced_eta.py` | eta = 6.16e-10 with 8/3 post-hoc |
| `frontier_dm_native_eta.py` | eta = 5.22e-10 (native, no post-hoc) |
| `frontier_dm_eta_derivation.py` | eta derivation chain |
| `frontier_bbn_from_framework.py` | BBN is pure kinematics |

### Taste enhancement and sector-resolved scripts

| Script | Key result |
|--------|-----------|
| `frontier_taste_sphaleron_coupling.py` | All 8 doublets, 4-layer proof |
| `frontier_taste_sector_resolved.py` | E_total/E_daisy = 2.0 EXACT |
| `frontier_taste_determinant_hierarchy.py` | Taste determinant hierarchy |
| `frontier_sphaleron_magnetic_derived.py` | kappa_sph = 21.3, c_mag = 0.369 |

### Sensitivity and diagnostic scripts

| Script | Key result |
|--------|-----------|
| `frontier_dm_r_sensitivity.py` | dR/R = 653% from transport |
| `frontier_dm_k_independence.py` | k irrelevance at 10^{-47} |
| `frontier_dm_invariant_bridge.py` | Invariant bridge construction |
| `frontier_dm_axiom_boundary.py` | All bounded items trace to A5 |
| `frontier_dm_g_bare_from_hamiltonian.py` | g_bare = 1 argument |
| `frontier_dm_graph_native.py` | Graph-native quantity definitions |
| `frontier_dm_friedmann_from_newton.py` | First Friedmann is Newtonian |
| `frontier_dm_thermodynamic_closure.py` | Thermodynamic vs continuum limit |

---

## Doc Reference Index

### Core derivation notes

| Doc | Content |
|-----|---------|
| `DM_CLEAN_DERIVATION_NOTE.md` | The 13-step chain (canonical) |
| `DM_FLAGSHIP_CLOSURE_NOTE.md` | Precise derived/bounded boundary, Codex objection map |
| `DM_RELIC_PAPER_NOTE.md` | Paper-safe framing, error budget |
| `DM_RELIC_BRIDGE_NOTE.md` | The bridge: sigma_v to R, eta is the missing piece |
| `DM_CLOSURE_CASE_NOTE.md` | Arguments for g_bare and k=0 closure |
| `DM_RELIC_SYNTHESIS_NOTE.md` | Synthesis of approaches, R = 5.48 |

### Structural proofs

| Doc | Content |
|-----|---------|
| `DM_BOLTZMANN_THEOREM.md` | Boltzmann reduction theorem |
| `DM_STOSSZAHLANSATZ_THEOREM_NOTE.md` | Stosszahlansatz as theorem |
| `DM_DIRECT_BOLTZMANN_NOTE.md` | Direct computation proof |
| `DM_FINAL_GAPS_NOTE.md` | sigma_v C=pi proved, Boltzmann derived |
| `DM_SIGMA_V_LATTICE_NOTE.md` | sigma_v from lattice T-matrix |
| `DM_COULOMB_FROM_LATTICE_NOTE.md` | Coulomb potential from Green's function |

### Transport and EWPT

| Doc | Content |
|-----|---------|
| `DM_TRANSPORT_DERIVED_NOTE.md` | All 3 transport params derived |
| `DM_TRANSPORT_GREENKUBO_NOTE.md` | D_q*T from Green-Kubo |
| `DM_DQT_NATIVE_NOTE.md` | D_q*T native lattice |
| `DM_DQT_HTL_NOTE.md` | D_q*T HTL-resummed (3.1) |
| `DM_VW_DERIVATION_NOTE.md` | v_w from Boltzmann closure |
| `DM_BOUNCE_WALL_NOTE.md` | L_w*T from CW bounce |
| `DM_EWPT_NATIVE_NOTE.md` | Daisy-resummed EWPT |
| `DM_NUCLEATION_TEMPERATURE_NOTE.md` | T_n from bounce action |
| `DM_NUCLEATION_FINDING_NOTE.md` | DETONATION finding |
| `DM_COUPLED_TRANSPORT_NOTE.md` | Coupled transport at T_n |
| `EWPT_STRENGTH_NOTE.md` | Perturbative EWPT estimates |
| `EWPT_LATTICE_MC_NOTE.md` | Scalar MC v/T = 0.49 |
| `EWPT_GAUGE_CLOSURE_NOTE.md` | Gauge-effective MC v/T = 0.56 |

### Baryogenesis and eta

| Doc | Content |
|-----|---------|
| `BARYOGENESIS_NOTE.md` | Three Sakharov conditions |
| `ETA_FROM_FRAMEWORK_NOTE.md` | Input classification for eta |
| `DM_TASTE_ENHANCED_ETA_NOTE.md` | 8/3 taste enhancement |
| `DM_NATIVE_ETA_NOTE.md` | Native eta = 5.22e-10 |
| `BBN_FROM_FRAMEWORK_NOTE.md` | BBN is kinematics |

### Strategy and diagnostics

| Doc | Content |
|-----|---------|
| `DM_ELEGANT_BRAINSTORM.md` | Five mathematical approaches to close gate |
| `DM_R_SENSITIVITY_NOTE.md` | Transport sensitivity (dR/R = 653%) |
| `DM_WILD_RATIO_NOTE.md` | Bypass baryogenesis? Sharp negative. |
| `DM_AXIOM_BOUNDARY_NOTE.md` | All bounded items trace to A5 |
| `ROOT_CAUSE_ANALYSIS_THREE_GATES.md` | Common root: taste activity fraction |

---

## Codex Assessment (from review.md)

Paper-safe read:

> Structural DM inputs are materially stronger. The BBN objection is mostly
> retired, L_w*T is substantially narrowed, and D_q*T now has a native
> one-loop lattice route. The full relic mapping still remains bounded because
> eta still depends on imported C_tr, imported non-perturbative v(T_n)/T_n,
> and transport closure that is not yet fully native at the paper bar.

The DM relic mapping gate remains **BOUNDED**. The strongest honest claim:

> R = 5.48 follows from a 13-step chain on Z^3 with Cl(3). The structural
> backbone (mass ratio 3/5, Casimir channels 155/27, Sommerfeld 1.59) is
> exact and parameter-free. Two items remain bounded: g_bare = 1 (Cl(3)
> normalization) and k = 0 (numerically irrelevant). The baryon abundance
> uses the observed eta = 6.1 x 10^{-10}. At g = 1, R matches R_obs to 0.25%.

---

## Files Consulted for This Consolidation

Every file listed in the script and doc reference indices above was read in
full to produce this document. The complete list of 47+ docs and 37+ scripts
spans the full DM lane from the Cl(3) axioms through to the cosmological
pie chart.
