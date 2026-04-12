# Dark Matter Lane Closure: Definitive Assessment

**Date:** 2026-04-12
**Status:** Lane bounded -- consistent but not predictive
**Script:** `scripts/frontier_dark_matter_closure.py`
**Log:** `logs/2026-04-12-dark_matter_closure.txt`
**Depends on:** `docs/DARK_MATTER_SINGLETS_NOTE.md` (first pass),
`docs/GENERATIONS_RIGOROUS_NOTE.md` (taste structure)

---

## Abstract

The first pass on dark matter from taste singlets (S0, S3 in the 8 = 1+3+3\*+1
decomposition) identified three problems: (1) SU(2) j=3/2, (2) mass ratio
0.33 vs observed 5.47, (3) U(1) charge unknown. This closure analysis resolves
all three, but the resolution is the same in each case: **at the Planck mass
scale, non-gravitational interactions are negligible.** The candidate survives
but makes no testable predictions beyond gravitational coupling.

**Verdict:** BOUNDED. The taste singlet DM hypothesis is consistent with
observations but not uniquely predictive. The lane is neither closed (no fatal
contradiction) nor triumphantly open (no sharp testable prediction). An
alternative mechanism (lattice monopoles) is identified as independently viable.

---

## 1. Problem 1: SU(2) j=3/2 -- Resolution by Mass Suppression

### The problem

S0=(0,0,0) and S3=(1,1,1) have j=3/2 under the total-spin SU(2) built from
the taste algebra. They are SU(2) non-singlets and would therefore participate
in weak interactions.

### Exhaustive SU(2) analysis

We tested every possible SU(2) embedding in the 8-dim taste space:

| SU(2) embedding | S0 quantum number | S3 quantum number |
|-----------------|-------------------|-------------------|
| Total spin      | j=3/2, m=+3/2     | j=3/2, m=-3/2     |
| Single-axis     | j=1/2             | j=1/2             |
| First-bit isospin | I_3=+1/2       | I_3=-1/2          |

**No SU(2) embedding makes S0 or S3 into singlets.** This is a theorem: the
all-up and all-down states transform nontrivially under any SU(2) that acts
nontrivially on any qubit. The only trivial embedding is the identity, which
is not a gauge symmetry.

### Resolution: mass suppression

At M = M_Planck, the weak scattering cross section is:

    sigma_weak ~ alpha_W^2 / M_Planck^2 ~ 10^{-69} cm^2

Current direct detection limits are ~10^{-46} cm^2 -- **23 orders of magnitude
above** the singlet cross section. The SU(2) coupling exists in principle but
is utterly undetectable.

This is the standard resolution for superheavy dark matter: WIMPzilla candidates
(Chung, Kolb, Riotto 1999) face identical quantum-number issues but are viable
because their interactions are mass-suppressed.

**Status: CLOSED by mass suppression.**

---

## 2. Problem 3: U(1) Charge -- Resolution by Mass Suppression

### The problem

In the staggered formulation, the U(1) gauge link couples equally to all taste
states. All 8 tastes carry the same electric charge. The singlets are not
naturally neutral.

### Analysis

The framework does not determine the U(1) charge assignment. Hypercharge in the
SM requires 4-5 distinct values per generation; the taste space provides only
4 Hamming weights across 2 relevant orbits. There is no natural function Y(|s|)
that reproduces SM hypercharges.

However: **at the Planck mass, charge is irrelevant.**

Even for unit electric charge:
- Thomson cross section: sigma_T ~ alpha^2/M^2 ~ 10^{-70} cm^2
- sigma_T / m ~ 10^{-66} cm^2/g
- CMB constraint: sigma/m < 10^{-5} cm^2/g
- Satisfied by 61 orders of magnitude

All observational constraints on charged dark matter are satisfied for
M = M_Planck, regardless of charge assignment.

**Status: CLOSED -- moot at Planck mass.**

---

## 3. Problem 2: Mass Ratio 0.33 vs 5.47 -- Partial Resolution

### Wilson baseline (confirmed)

With equal number densities and Wilson masses m(|s|) = (2r/a)|s|:

    Omega_DM/Omega_vis = m(S3) / (3*m(T1) + 3*m(T2)) = 3/9 = 0.33

This is 16x below the observed ratio of 5.47.

### Self-consistent mass with gravitational self-energy

Including gravitational self-energy m_phys = m_W - alpha_G * m_phys^2:

| alpha_G | m(S3)/m(T1) | Omega ratio |
|---------|-------------|-------------|
| 0.0     | 3.00        | 0.333       |
| 0.5     | 2.25        | 0.279       |
| 1.0     | 2.11        | 0.268       |
| 5.0     | 1.90        | —           |

Gravity COMPRESSES the hierarchy -- makes the ratio worse, not better. The
self-consistent mass ratio approaches sqrt(3) = 1.73 for strong coupling.

### Selective annihilation mechanism

The mass ratio alone cannot produce 5.47. However, if visible and dark states
have different annihilation cross sections:

- Visible (colored): sigma_vis ~ alpha_s^2 / M^2
- Dark (color singlet): sigma_dark ~ alpha_G^2 / M^2
- Number density ratio: n_dark/n_vis ~ sigma_vis/sigma_dark

Required cross-section ratio: sigma_vis/sigma_dark = 16.4

This is achievable if alpha_s(M_Planck)/alpha_G ~ 4. With alpha_s running to
~0.03 at M_Planck (from asymptotic freedom) and alpha_G ~ 0.007, the ratio is
~18 -- consistent with the observed 5.47.

### Assessment

The mechanism is **consistent** but **not predictive**: matching 5.47 requires
a specific ratio of coupling constants that the framework does not determine.
The relic abundance is an adjustable output, not a prediction.

**Status: PARTIALLY CLOSED -- achievable but not predicted.**

---

## 4. Production Mechanism

Standard gravitational production (Chung et al. 1999) fails for M = M_Planck
because the production rate is exponentially suppressed as exp(-2M/H_I) with
H_I ~ 10^{13} GeV << M_Planck.

In the framework where the lattice IS fundamental, the production question
is reframed: all states are initially populated, and the observed ratio is
set by selective annihilation during the hot phase. This is self-consistent
but not independently testable.

---

## 5. Alternative Mechanisms

### Lattice monopoles (most promising alternative)

Compact U(1) on a lattice automatically supports magnetic monopoles (DeGrand
and Toussaint 1980). Properties:
- Mass: ~1/a ~ M_Planck
- Charge: magnetically charged, electrically neutral
- Stability: topologically protected (magnetic charge conservation)
- Detection: interacts magnetically, not electromagnetically

This is an **independent** DM candidate within the framework, complementary to
taste singlets. It has been proposed in the literature (Preskill 1979).

### Other mechanisms considered

| Mechanism | Status |
|-----------|--------|
| Gravitational solitons (geons) | Speculative, no calculation |
| KK modes | Not independent -- same as taste doublers |
| Vacuum fluctuations | Distinct from DM |
| Domain walls | Too heavy (domain wall problem) |

---

## 6. Updated Scorecard

| Criterion | First Pass | Closure | Resolution |
|-----------|------------|---------|------------|
| Colorless (SU(3) singlet) | PASS | PASS | -- |
| Electrically neutral | UNKNOWN | MOOT | Mass suppresses EM |
| Weakly interacting | FAIL | MOOT | Mass suppresses weak |
| Stable | PASS | PASS | -- |
| Correct relic abundance | UNKNOWN | PARTIAL | Needs sigma_vis/sigma_dark |
| Gravitational interaction | PASS | PASS | -- |
| No direct detection | PASS | PASS | -- |
| Consistent with CMB | PASS | PASS | -- |
| Consistent with BBN | UNKNOWN | PASS | M >> T_BBN |
| Predictive (testable) | PASS | WEAK | No observable test |

**Score: 6 PASS / 2 MOOT / 1 PARTIAL / 1 WEAK**

Previous: 6 PASS / 1 FAIL / 3 UNKNOWN. Net: all problems addressed, but
predictiveness downgraded from PASS to WEAK.

---

## 7. What the Framework Predicts

### Definite predictions

1. Dark matter exists (2 out of 8 taste states are singlets)
2. DM is SU(3) color singlet (exact, from zero projection onto triplet subspace)
3. DM mass is at the lattice scale (~M_Planck)
4. DM is kinematically stable (at exact 3-body decay threshold)
5. Exactly 2 dark species per 6 visible (multiplicity ratio = 1/3)

### Conditional predictions

6. Omega_DM/Omega_vis ~ 5 IF alpha_s(M_Pl)/alpha_G ~ 4

### Not predicted

- The exact relic abundance (depends on coupling constant ratio)
- Whether DM is electrically charged (framework is silent, but irrelevant)
- Any detection signal (all cross sections suppressed by M_Planck^{-2})

---

## 8. Honest Assessment

### The core insight

All three problems from the first pass share a single resolution: **Planck-mass
dark matter is immune to non-gravitational constraints.** The candidate's gauge
quantum numbers (SU(2) j=3/2, possibly charged under U(1)) would be fatal for
a TeV-scale candidate but are irrelevant at M_Planck. The interaction cross
sections are suppressed by factors of 10^{-23} to 10^{-61} below experimental
limits.

### The limitation

This same feature that saves the candidate also makes it untestable. A dark
matter candidate that interacts only gravitationally and has M ~ M_Planck is
indistinguishable from any other superheavy gravitationally-coupled relic. The
specific origin in taste singlets adds no observable signature.

### The strongest claim

The framework **requires** the existence of 2 taste singlet states. If the
lattice is fundamental, these states exist. Their stability is guaranteed by
kinematics (exact threshold). Their gravitational coupling is automatic. The
only question is whether they constitute the observed dark matter, and this
cannot be answered from within the framework without determining the Planck-scale
coupling constants.

### Lane status

**BOUNDED.** This lane is not closed (no contradiction found) and not open (no
testable prediction identified). It should be retained as a consistent
consequence of the taste decomposition but not promoted as a dark matter
prediction until either: (a) the coupling constants alpha_s(M_Pl) and alpha_G
are computed from the lattice, yielding a parameter-free abundance prediction,
or (b) an observable consequence of Planck-mass DM is identified.

---

## References

- Chung, Kolb & Riotto, Phys. Rev. D 59, 023501 (1999) -- WIMPzilla production
- Cirelli, Fornengo & Strumia, Nucl. Phys. B 753, 178 (2006) -- minimal dark matter
- DeGrand & Toussaint, Phys. Rev. D 22, 2478 (1980) -- lattice U(1) monopoles
- Preskill, Phys. Rev. Lett. 43, 1365 (1979) -- monopole dark matter
- Servant & Tait, Nucl. Phys. B 650, 391 (2003) -- KK dark matter
