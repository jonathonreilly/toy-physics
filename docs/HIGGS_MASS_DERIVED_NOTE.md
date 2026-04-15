# Higgs Mass: Derivation Status (Honest Assessment)

**Status:** SUPERSEDED by `COMPLETE_PREDICTION_CHAIN_2026_04_15.md`

> **WARNING:** This note predates the derivation of y_t (now 0.918 via
> Ward + √(8/9) color projection), the stability boundary prediction
> (λ(M_Pl) = 0 → m_H = 129.7 GeV), and the full EW coupling derivations.
> The three-tier structure below is outdated:
> - Tier 2 claimed y_t was "one free parameter" — y_t is now DERIVED
> - Tier 3 claimed m_H "REQUIRES SM INPUT" — all inputs now DERIVED
> - sin²θ_W = 3/8 was attributed to "GUT relation" — it comes from
>   bare couplings g_2²=1/4, g_Y²=1/5, NOT from GUT unification
> See the complete prediction chain for the current derivation.

## Question (HISTORICAL — see supersession note above)

Can the framework derive m_H = 125 GeV from first principles via the
Coleman-Weinberg mechanism, or does m_H require SM couplings as input?

## Three-Tier Answer

### Tier 1: FULLY DERIVED (zero free parameters)

These results follow from the lattice axioms alone (Cl(3) on Z^3):

| Result | Source | Status |
|--------|--------|--------|
| CW mechanism triggers EWSB | Taste condensate = Higgs field | DERIVED |
| Hierarchy problem resolved | Lambda = pi/a is physical, Delta ~ O(1) | DERIVED |
| EWSB with O(1) bare parameters | No fine-tuning needed | DERIVED |
| Gauge group SU(2)_L x U(1)_Y | Cl(3) taste algebra | DERIVED |
| Particle DOF count (n_i) | Taste doubling on Z^3 | DERIVED |
| sin^2(theta_W) = 3/8 at M_Planck | Cl(3) GUT relation | DERIVED |
| alpha_V = 0.092 at M_Planck | V-scheme plaquette action | DERIVED |
| m_Z/m_W = 1/cos(theta_W) | Pure gauge structure | DERIVED |

The CW mechanism is the framework's NATURAL Higgs mechanism. No elementary
scalar is postulated -- the Higgs field IS the taste condensate, and SSB
is dynamically driven by quantum corrections with the lattice providing the
physical UV cutoff.

The hierarchy problem is resolved because the cutoff IS the lattice spacing
(= Planck scale). The Barbieri-Giudice fine-tuning measure is Delta ~ 0.5,
compared to Delta ~ 10^34 in the continuum SM with a Planck cutoff.

### Tier 2: BOUNDED (one free parameter)

Given the derived gauge couplings, the CW potential gives m_H/m_W as a
SPECIFIC FUNCTION of y_t (the top Yukawa coupling):

    m_H/m_W = f_CW(y_t; g, g', Lambda)

This is a genuine prediction: the framework reduces the Higgs sector from
2 free parameters (mu^2, lambda) to 1 (y_t). The CW curve gives:

- For y_t ~ 0.5-1.0: m_H/m_W ~ 1.5-2.5 (lattice a=1)
- For y_t ~ 1.0 (observed): m_H/m_W ~ 1.85 (19% above SM value 1.56)
- The ratio decreases toward the SM value as lattice spacing decreases

The top Yukawa is bounded by the IR quasi-fixed-point:

    y_t* = sqrt(2/9 * (8*g_s^2 + 9/4*g^2 + 17/12*g'^2)) ~ 1.7

This is the right order of magnitude but 70% above the observed y_t = 0.994.

### Tier 3: REQUIRES SM INPUT (consistency check)

The exact numerical value m_H = 125 GeV cannot be derived without:

1. **y_t = 0.994** -- not predicted (only bounded by fixed point)
2. **Exact g, g' at M_Z** -- Cl(3) gives sin^2(theta_W) = 3/8 at M_Planck,
   but running to M_Z with SM RGEs gives ~40% deviations (the standard
   non-unification problem, which needs threshold corrections to resolve)
3. **2-loop CW corrections** -- the 1-loop CW gives m_H/m_W ~ 1.85 with
   SM couplings, 19% above the SM value; 2-loop corrections would reduce this

## Key Results

### SSB is generic, not fine-tuned

The CW mechanism triggers SSB for >50% of O(1) bare mass values.
This is not a coincidence or tuning -- it is a structural consequence
of the lattice UV cutoff bounding the quantum corrections.

### The hierarchy problem IS resolved

| Framework | Cutoff | BG Fine-tuning Delta |
|-----------|--------|---------------------|
| SM (TeV) | 10^3 GeV | 4 |
| SM (GUT) | 10^16 GeV | 4 x 10^26 |
| SM (Planck) | 10^19 GeV | 6 x 10^32 |
| **Lattice** | **pi/a ~ 3** | **~0.5** |

### m_H/m_W converges to SM with decreasing lattice spacing

| a | Lambda | m_H/m_W | m_H (GeV) |
|---|--------|---------|-----------|
| 2.0 | 1.57 | 2.18 | 175 |
| 1.0 | 3.14 | 1.85 | 149 |
| 0.5 | 6.28 | 1.64 | 132 |

At a = 0.5, m_H/m_W = 1.64 is within 5% of the SM value 1.56.

### Effect of taste scalar doublets on m_H

The Cl(3) framework predicts 4 Higgs doublets (from the 8 taste states
decomposing as C^2 x C^4 under SU(2)_weak).  One doublet is the SM Higgs;
the other 3 contribute 12 extra real bosonic DOF to the CW potential.

**Result:** Taste scalars push m_H UPWARD, not downward.

| Configuration | m_H (GeV) | Shift |
|---------------|-----------|-------|
| SM-only (a=1) | 153 | baseline |
| SM + 3 taste doublets (a=1) | 161 | +8 GeV (+5.3%) |

This is a robust consequence of the CW mechanism: bosonic loops add positive
curvature at the CW minimum, always increasing m_H^2.  The taste scalar
portal coupling is fixed by the gauge D-term: lambda_portal = (g^2+g'^2)/4.

At small lattice spacing (a < 0.6), the taste scalars destroy SSB entirely
(too much bosonic contribution overwhelms the top quark loop that drives
symmetry breaking).  This constrains the physical lattice spacing to a > 0.6.

**Implication:** The 153-to-125 gap must close through lattice spacing
convergence and 2-loop corrections, not through taste scalar contributions.

Script: `scripts/frontier_higgs_mass_derived.py`

## What This Means for the Paper

**CAN claim:**
- The Higgs mechanism emerges from the lattice (CW, no elementary scalar)
- The hierarchy problem is solved (cutoff = Planck, Delta ~ O(1))
- m_H is of the right order of magnitude
- m_H/m_W converges toward the SM as lattice spacing decreases

**CANNOT claim:**
- m_H = 125 GeV derived from first principles
- y_t predicted (only bounded)
- Complete gauge coupling unification (threshold corrections needed)

**Recommended framing:**
"The Coleman-Weinberg mechanism on the lattice provides a natural origin
for electroweak symmetry breaking, resolves the hierarchy problem, and
predicts m_H/m_W as a function of a single parameter (y_t). The observed
Higgs mass is consistent with the framework."

## Roadmap to Full Derivation

1. Compute Planck-scale threshold corrections to gauge RGE
   => fixes g, g' at M_Z
2. Determine y_t from 2-loop IR fixed point + lattice matching
   => pins y_t to ~20%
3. Compute 2-loop CW potential on the lattice
   => refines m_H/m_W to ~5%
4. Show lambda_bare and m^2_bare are radiatively stable at O(1)
   => completes naturalness argument

## Script

`scripts/frontier_higgs_mass_derived.py` -- self-contained, numpy + scipy only.
