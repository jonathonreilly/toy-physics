# Wave-Retardation Lab Prediction — NEGATIVE (No Clean v/c Scaling)

**Date:** 2026-04-07
**Status:** proposed_retained negative — two sweeps on the wave-retardation lane (varying v/c with trajectory-range coupled, then with trajectory-range fixed) show that the M − I gap is **configuration-dependent and non-monotonic in v/c**, not a clean power law. The original Lane 6 / Lane 8b 25-30% gap was a single-point result that does not extrapolate to lab v/c via any simple scaling. The lab prediction card is **blocked** until the configuration dependence is disentangled. The flagship wave-equation physics (Lanes 4–8b) is unaffected; only the lab translation is blocked.

## Artifact chain

- [`scripts/wave_retardation_velocity_sweep.py`](../scripts/wave_retardation_velocity_sweep.py)
- [`logs/2026-04-07-wave-retardation-velocity-sweep.txt`](../logs/2026-04-07-wave-retardation-velocity-sweep.txt)

## Question

The Lane 6 / Lane 8b retardation result was a single point: at
v/c = 0.30 (source moving in z over 20 active layers), the retarded
field M and the instantaneous comparator I differ in beam deflection
by 25% on Fam1 (and 26-31% on (3+1)D promotion across three families).

For an experimental prediction card, the obvious question is: how
does (M − I) scale with v/c? The candidate scalings are:

- (v/c)^1 → first-order post-Newtonian retardation
- (v/c)^2 → second-order relativistic corrections
- (v/c)^0 → saturated, geometry-dominated effect

This lane runs two sweeps:

1. **First sweep**: v varied over {0.05, 0.10, 0.15, 0.20, 0.25,
   0.30, 0.40} with n_active fixed at 20 layers. The trajectory
   range varies with v.
2. **Second sweep**: trajectory range fixed at iz: 6 → 0 (always
   6 cells), velocity varied by varying n_active over {60, 30, 20,
   15, 12, 10, 8}. The trajectory range is now constant; only the
   velocity changes.

If the first sweep gives a power law and the second sweep gives
the same power law, the scaling is genuine. If they diverge, the
"scaling" was a confound between velocity and trajectory geometry.

## First sweep result (range-coupled)

| v/c | iz_end | dM | dI | rel gap |
| ---: | ---: | ---: | ---: | ---: |
| 0.05 | 5 | +0.0082 | +0.0164 | **50.1%** |
| 0.10 | 4 | +0.0085 | +0.0157 | 45.8% |
| 0.15 | 3 | +0.0088 | +0.0148 | 40.9% |
| 0.20 | 2 | +0.0089 | +0.0139 | 36.0% |
| 0.25 | 1 | +0.0089 | +0.0128 | 30.8% |
| 0.30 | 0 | +0.0085 | +0.0112 | 24.8% |
| 0.40 | −2 | +0.0076 | +0.0076 | **0.00%** |

The gap **decreases** with v/c, hitting zero at v/c = 0.40. The
log-log fit gives slope ≈ −2.79, but this is **meaningless**: at
v/c = 0.40, the source overshoots from iz=6 to iz=−2, an 8-cell
trajectory that crosses the lattice symmetry point z = 2. M and I
both give the same averaged response because the trajectory is
symmetric about the lattice center, **not because of a velocity
effect**.

This sweep conflated v/c with trajectory range. Its slope is not
a velocity scaling.

## Second sweep result (trajectory-fixed)

| n_active | v/c | dM | dI | M − I | rel |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 60 | 0.10 | +0.0058 | **−0.0030** | +0.0088 | **151.5%** (sign flip) |
| 30 | 0.20 | +0.0126 | +0.0139 | −0.0013 | 9.4% |
| 20 | 0.30 | +0.0106 | +0.0114 | −0.0008 | 7.1% |
| 15 | 0.40 | +0.0074 | +0.0077 | −0.0003 | **3.8% (minimum)** |
| 12 | 0.50 | +0.0058 | +0.0052 | +0.0006 | 10.3% |
| 10 | 0.60 | +0.0050 | +0.0039 | +0.0011 | 21.1% |
| 8 | 0.75 | +0.0036 | +0.0012 | +0.0024 | 66.6% |

The gap is **non-monotonic** in v/c: it has a minimum near v/c ≈ 0.4
(3.8%), grows on both sides, and even **flips sign** at very low
velocity (n_active = 60, where the instantaneous comparator gives a
sign-flipped dI of −0.003).

The log-log fit gives slope ≈ −0.51, but this is also **meaningless**
because the relationship is not a power law.

## Three findings that block the lab card

### 1. The Lane 6 25% number is configuration-specific

At v/c = 0.30 the original Lane 6 reported `M − I = 25%`. The
trajectory-fixed sweep at v/c = 0.30 gives **7.1%**, three times
smaller. The original lane had a specific combination of `(NL=30,
n_active=20, src_layer=10, iz_start=6, iz_end=0)`. Other
parameterizations of the same v/c give different gaps.

The 25% gap is real but it is **a point measurement**, not a robust
prediction of "wave-retardation gives a 25% deviation from
instantaneous Newton at v/c = 0.30."

### 2. There is no clean v/c power law

Both sweeps give numerically meaningful slopes (−2.79 and −0.51)
but neither is a true scaling exponent — the first is dominated by
trajectory-range effects, the second is non-monotonic. Lab
extrapolation by power law is invalid.

### 3. The simulation-length and source-onset confound the gap

The trajectory-fixed sweep varies NL = src_layer + n_active + buffer.
That means the total beam propagation length and the source onset
time both change with v/c. The gap is sensitive to all three —
v/c, n_active, and total NL — and the harness as written cannot
disentangle them in a single 1D sweep.

A clean velocity scaling would require fixing NL, n_active,
source onset, AND trajectory range, while varying only v. That is
**not possible in a single parameter sweep** because n_active = (range / v),
so v and n_active are inversely related when range is fixed.

## Why a naïve lab card is meaningless

Both sweeps' "lab extrapolation" tables predict absurd numbers
(rel_gap ≈ 10²¹ at cold-atom scales, etc.) because they assume a
power law that doesn't exist. The honest lab translation is:

- The model has a (3+1)D wave equation with finite c
- The model has retarded gravitational interaction at the lattice scale
- The dimensionless ratio (M − I) / max(|M|, |I|) at the lattice
  scale is **configuration-dependent**, ranging from ~4% to >150%
  across the swept parameter set
- **No simple scaling translates the lattice prediction to lab v/c**
- A clean lab card requires either:
  - A continuum-limit analysis (H → 0, NL → ∞) where lattice
    artifacts vanish and a genuine v/c dependence emerges
  - A redesigned harness with independent controls for v, NL,
    n_active, and trajectory range
  - A direct identification of which dimensionless lattice ratio
    maps to which lab observable, with the mapping validated
    against a known physical limit

None of these are short lanes. Each is a substantial new piece of
work.

## What this does NOT undermine

The flagship wave-equation physics is **completely unaffected**:

- **Lane 4** (Poisson 3D static gravity, F~M = 0.9999): static, no v/c
- **Lane 5** (lightcone): strict `first_dt = r`, independent of v/c
- **Lane 6** (retarded ≠ instantaneous, single point): *exists* at the
  Fam1/2/3 v/c = 0.30 configuration; the existence is not in question
- **Lane 7** ((2+1)D radiation slope −0.47): independent of source motion
- **Lane 8** ((3+1)D radiation slope −1.14): independent of source motion
- **Lane 8b** ((3+1)D lightcone + retarded ≠ instantaneous): the
  retardation existence at v/c = 0.23 is also not in question

What is in question is **only the lab translation** of the Lane 6 /
Lane 8b retardation result. The lane shows the wave equation
qualitatively has retarded gravity (M ≠ I in some regime), but the
quantitative claim "the gap is X% at v/c = Y" is not robust enough
to extrapolate to lab values without further work.

## Frontier map adjustment (Update 8)

| Row | Update 7 (post second-order Kubo) | This lane |
| --- | --- | --- |
| Strength against harshest critique | first-order Kubo on linearity regime | unchanged |
| Compact underlying principle | bounded at 15/41 by Taylor approach | unchanged |
| Theory compression | second-order does NOT extend | unchanged |
| **Experimental prediction card** | open | **NEGATIVE — lab card blocked by configuration dependence; not a v/c scaling** |
| Wave-retardation flagship physics | retained (Lanes 6, 8b) | **unchanged** (existence holds, only lab translation blocked) |

## What to attack next

This lane closes the "easy lab card" path. Three remaining moves:

1. **Continuum-limit analysis of the wave-retardation gap** — take
   H → 0, NL → ∞ at fixed physical parameters, see whether a clean
   v/c scaling emerges in the limit. Substantial new lane.
2. **Non-perturbative full path-sum / resummation** for the
   classifier-failing families — the user's named "right next
   theory move." Independent of the lab card.
3. **Born preservation derivation** — small one-line proof that
   adds a third battery condition to the derivation column.

The continuum-limit analysis (1) is the natural follow-on to this
negative because it directly addresses the configuration dependence
that blocks the lab card. The non-perturbative path-sum (2) and the
Born derivation (3) are orthogonal — they advance the theory column
but not the experimental column.

## Honest read

The experimental prediction card is **blocked**. The wave-retardation
result exists at the lattice scale but its v/c dependence is
configuration-dependent and non-monotonic, so simple extrapolation
to lab v/c values is invalid. Both sweeps in this lane gave
numerically clean fits that turned out to be artifacts of the
sweep parameterization.

This is the **right kind of negative** to retain: it stops the
program from writing an over-claiming lab card, identifies exactly
why the simple translation fails, and points to the specific
follow-on (continuum limit) that would unblock it.

## Bottom line

> "Two velocity sweeps on the wave-retardation lane (range-coupled
> and trajectory-fixed) show that the M − I gap is configuration-
> dependent and non-monotonic in v/c. The first sweep's apparent
> scaling exponent of −2.79 conflated velocity with trajectory range.
> The trajectory-fixed sweep gives a non-monotonic gap with a
> minimum near v/c ≈ 0.4 (3.8%) and sign flips at extreme parameters.
> The original Lane 6 25% gap is a point measurement specific to its
> (NL, n_active, src_layer) configuration; the trajectory-fixed
> sweep at the same v/c = 0.30 gives 7.1%, three times smaller.
> No simple v/c power law extrapolates the lattice result to lab
> velocities. The experimental prediction card is blocked until a
> continuum-limit analysis or a redesigned harness with independent
> controls for v, n_active, and total NL is built. The flagship
> wave-equation physics (Lanes 4–8b) is unaffected; only the lab
> translation is blocked."
