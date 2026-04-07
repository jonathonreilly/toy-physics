# Wave-Retardation Continuum Limit — NEGATIVE (Comparator-Dominated, Not Retardation-Dominated)

**Date:** 2026-04-07
**Status:** retained negative — refining the lattice spacing H from 0.5 to 0.35 to 0.25 (with all physical parameters held constant) does NOT give a converged value for the M − I rel_gap. The gap oscillates 28.81% → 9.53% → 43.40%. However, the failure structure is informative: dM (retarded wave field) drifts only 14% across the refinement (monotone, plausibly converging to ~0.007), while dI (cached-static-slice instantaneous comparator) oscillates 9% → 35% → 45%. The Lane 6 25% gap is dominated by the dI construction's lattice artifacts, NOT by a stable retardation signal. The "M ≠ I" existence is logically valid, but the magnitude does not have a clean continuum limit at these refinement levels.

## Artifact chain

- [`scripts/wave_retardation_continuum_limit.py`](../scripts/wave_retardation_continuum_limit.py)
- [`logs/2026-04-07-wave-retardation-continuum-limit.txt`](../logs/2026-04-07-wave-retardation-continuum-limit.txt)

## Question

The lab-card lane (`WAVE_RETARDATION_LAB_PREDICTION_NOTE.md`) showed
that the Lane 6 / Lane 8b 25-30% retardation gap is configuration-dependent
and does not have a clean v/c power law. This lane tests whether the
configuration dependence is a **finite-lattice-spacing artifact that
vanishes in the continuum limit**:

- Hold all physical parameters constant
- Refine H ∈ {0.5, 0.35, 0.25}
- See whether (M − I) / max(|M|, |I|) converges to a finite value
- If yes: there is a continuum prediction; the lab card can be unblocked
- If no: the Lane 6 result is fundamentally lattice-artifact-sensitive

## Setup

Physical parameters held constant across refinements:

| Quantity | Value | Meaning |
| --- | ---: | --- |
| `T_phys` | 15.0 | Total propagation "time" = NL × H |
| `iz_start_phys` | 3.0 | Source initial position (matches Lane 6 iz=6 at H=0.5) |
| `iz_end_phys` | 0.0 | Source final position |
| `D_phys` | 3.0 | Source displacement (matches Lane 6) |
| `PW_phys` | 6.0 | Transverse beam half-width |
| `k × H` | 2.5 | Phase per edge step (so k_phase = 2.5/H) |
| `S_phys` | 0.004 | Field source strength |
| `v/c` | −0.30 | Source velocity (D_phys / (T_phys · (1−src_frac))) |

At each refinement, NL = round(T_phys / H), iz_range = round(D_phys / H),
k_phase = K_PER_H / H. The propagator and the (2+1)D wave equation are
re-implemented with explicit H (no module-level constants).

(2+1)D was used instead of (3+1)D because the (3+1)D field cube at
H = 0.125 (97³ = 912k cells × 120 layers ≈ 110M cells) ran out of
memory in a first attempt.

## Result

| H | NL | n_nodes | dM (retarded) | dI (instant.) | M − I | rel_gap |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **0.50** | 30 | 18,126 | +0.00836 | +0.01175 | −0.00339 | **28.81%** |
| **0.35** | 43 | 51,451 | +0.00794 | +0.00878 | −0.00084 | **9.53%** |
| **0.25** | 60 | 141,660 | +0.00721 | +0.01274 | −0.00553 | **43.40%** |

### The H=0.5 reproduction

The H=0.5 row reproduces the original Lane 6 setup essentially exactly:
dM = +0.00836, dI = +0.01175, rel_gap = 28.81%, very close to Lane 6's
reported (dM, dI, gap) = (+0.00846, +0.01124, 24.77%). The new harness
is consistent with the original at the reference resolution.

### Convergence

| Step | Δ rel_gap | relative change |
| --- | ---: | ---: |
| coarse (0.50) → medium (0.35) | 0.193 | 66.9% |
| medium (0.35) → fine (0.25) | 0.339 | 355.6% |

The change does **not** shrink as the lattice is refined. It actually
**grows** between the second and third refinements. This is the
opposite of converging behavior.

**The rel_gap does not have a continuum limit at these refinement levels.**

### dM and dI separately

Looking at the two halves of the comparison separately:

| Quantity | H=0.5 | H=0.35 | H=0.25 | total drift |
| --- | ---: | ---: | ---: | ---: |
| **dM** (retarded wave field) | +0.00836 | +0.00794 | +0.00721 | **−14% (monotone)** |
| **dI** (cached static slice) | +0.01175 | +0.00878 | +0.01274 | **35% oscillation** |

- **dM is fairly stable**: monotone decrease by 14% across the refinement.
  Plausibly converging to ~0.007 in the H → 0 limit.
- **dI oscillates wildly**: 0.01175 → 0.00878 (down 25%) → 0.01274 (up 45%).
  No convergence pattern visible.

**The 25% rel_gap is dominated by the dI instability, not by a stable
retardation signal.** The retarded wave field's beam deflection
behaves like a real physical quantity that converges. The cached
static-slice instantaneous comparator does not.

## Why dI is the unstable half

The instantaneous comparator is constructed by:

1. For each visited source position `iz_of_t(t)`, solve a static
   wave-equation problem with the source frozen at that position.
2. Cache the LATE-TIME slice of that static solve (i.e., the
   wave-equation field after `NL` layers of equilibration).
3. At each layer `t` of the actual evolution, use the cached slice
   for the source's current position as the field at layer `t`.

This construction has **two lattice-spacing dependencies** that don't
cancel out:

1. The set of distinct visited source positions changes with H. At
   H=0.5 the source moves through {6, 5, 4, 3, 2, 1, 0} (7 positions).
   At H=0.25 it moves through {12, 11, 10, ..., 0} (13 positions).
   Each is a different cache key with its own static solve.
2. The "late-time slice" of each static solve is itself H-dependent
   because the wave-equation static problem hasn't fully equilibrated
   in `NL` layers — the slices encode transient behavior that varies
   with H.

The retarded field dM has neither problem: it's a single direct
evolution of the wave equation with a moving source, no caching, no
slice-stitching. That's why dM converges and dI doesn't.

## What this changes about the flagship physics

The Lane 6 / Lane 8b "M ≠ I" claim is:

- **Logically valid**: M and I are well-defined at any single H, and
  they differ at every H tested
- **Magnitude not robust**: the rel_gap is configuration- and
  H-dependent in ways that don't reduce to a clean continuum limit
- **Comparator-dominated**: the gap is mostly driven by the dI
  construction's lattice artifacts, not by a stable retardation effect
- **Existence-only retardation**: the retarded wave field does
  evolve consistently with finite c (Lane 5 lightcone is unaffected),
  but the quantitative comparison to a c=∞ analogue is not
  continuum-clean

This downgrades the Lane 6 / Lane 8b claim from "wave equation gives
retarded gravity that differs from instantaneous Newton by 25-30%"
to "wave equation has retarded field evolution; the existence of
M ≠ I against a stitched-static-slice comparator is real but the
magnitude does not have a clean continuum limit."

The flagship lanes that **are not affected** by this:

- **Lane 4** (Poisson 3D static gravity, F~M=0.9999) — pure static, no dI construction, and Poisson 3D has its own much better-behaved continuum properties
- **Lane 5** (lightcone, `first_dt = r` exactly) — independent of any comparator
- **Lane 7** ((2+1)D radiation slope −0.47) — independent of source motion comparators
- **Lane 8** ((3+1)D radiation slope −1.14) — same
- The **lightcone half** of Lane 8b (delta-pulse `first_dt = r` to r=8 in (3+1)D) — independent of dI

What is downgraded:

- **The retarded-vs-instantaneous half of Lane 6 / Lane 8b**: the
  *existence* holds but the *magnitude* is not continuum-stable

## What to attack next

This negative narrows the wave-retardation lane to "existence only"
at the magnitude level. To make a quantitative retardation claim that
survives lattice refinement, the next step is **a better c=∞
comparator** that does not depend on stitched static slices. Three
candidates:

1. **Imposed-Newton comparator**: use the imposed `s/(r+0.1)` field
   directly (the same field used in the static battery), evaluated
   at the current source position at each layer. This is the literal
   c=∞ Newtonian potential, with no wave-equation slices. It's a
   different theoretical framework (Newton vs wave equation), but
   it's the clean continuum reference.
2. **Equilibrated static slices**: solve each static wave-equation
   problem to genuine equilibrium (much larger NL than the dynamic
   evolution) instead of using the late-time slice from a finite NL.
   This would test whether the dI instability is just incomplete
   equilibration.
3. **Closed-form static field**: derive the analytic static
   wave-equation Green's function on the lattice and use it as the
   comparator. Removes all numerical equilibration questions.

(1) is the cheapest. (2) is medium cost. (3) is the highest leverage
but requires symbolic work.

Independent of the comparator question, the **non-perturbative
full-path-sum lane** (your originally named "right next theory move")
is also still open and orthogonal to this negative.

## Frontier map adjustment (Update 9)

| Row | Update 8 | This lane |
| --- | --- | --- |
| Wave-retardation magnitude claim | exists at lattice scale; lab card blocked | **downgraded**: existence holds, magnitude does not survive H refinement |
| Wave-retardation existence (M ≠ I at fixed H) | retained | retained — unaffected by this negative |
| Lane 5 lightcone, Lane 4 static, Lane 7/8 radiation | retained | unchanged |
| Experimental prediction card | blocked | **further blocked** — even without the v/c sweep, the underlying gap is not continuum-stable |
| Compact underlying principle | first-order Kubo on linearity regime (Update 7) | unchanged |

## Honest read

This is a **clean retained negative** for the magnitude side of the
wave-retardation flagship. The first-time-in-this-session lattice
refinement on a physics lane reveals that one of the more striking
results (the 25-30% retardation gap on three families) is dominated
by the comparator construction's lattice artifacts, not by a stable
physical effect.

The retarded wave field itself is fairly stable (dM drifts only 14%
across an 8× change in lattice density). It's the c=∞ comparator
that doesn't behave well in the continuum limit. So the *physics*
of the wave equation having retarded gravity is unaffected; what is
affected is the quantitative claim about how much it differs from
"instantaneous Newton."

The honest reframing: Lane 6 / Lane 8b show that the wave equation
has retarded field evolution (Lane 5 already proved finite c via
lightcone), and that this retarded evolution gives a different beam
deflection than a particular cached-static-slice approximation to
instantaneous gravity — at fixed lattice spacing. The magnitude of
that difference is not a robust physical number.

## Bottom line

> "Refining the lattice spacing H from 0.5 → 0.35 → 0.25 with all
> physical parameters held constant gives rel_gap values 28.81% →
> 9.53% → 43.40% — non-monotone, growing in change between successive
> refinements, no convergence. dM (retarded wave field) drifts only
> 14% monotonically across the refinement and plausibly converges to
> ~0.007. dI (cached-static-slice instantaneous comparator) oscillates
> 35% with no convergence pattern. The Lane 6 25% rel_gap is dominated
> by the dI construction's lattice artifacts, not by a stable
> retardation signal. The 'M ≠ I' existence is logically valid; the
> magnitude does not survive lattice refinement. The flagship lanes
> that don't depend on the dI construction (Lanes 4, 5, 7, 8, and
> the lightcone half of Lane 8b) are unaffected. The retarded-vs-
> instantaneous magnitude claim of Lanes 6 and 8b is downgraded from
> 'quantitative prediction' to 'existence only at fixed H'."
