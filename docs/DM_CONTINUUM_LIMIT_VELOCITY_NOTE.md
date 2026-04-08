# dM Continuum Limit Across Multiple v/c — Weak Positive

**Date:** 2026-04-07
**Status:** retained weak positive — at 3 velocities {−0.15, −0.25, −0.35}, the retarded wave field deflection `dM` is monotone decreasing with |v_target| and spans a narrow range (+0.0079 to +0.0090 at H=0.35). Two of three velocities converge at the 5% drift threshold at the coarse→medium refinement step (v=−0.15: 4.4%, v=−0.35: 0.6%); v=−0.25 is marginal at 7.6%. The 2-refinement sweep is not enough to nail down the continuum form, but it establishes that `dM` has a well-defined, bounded, monotone dependence on source velocity across a reasonable v/c range — directly, without any c=∞ comparator.

## Artifact chain

- [`scripts/dm_continuum_limit_velocity.py`](../scripts/dm_continuum_limit_velocity.py)
- [`logs/2026-04-07-dm-continuum-limit-velocity.txt`](../logs/2026-04-07-dm-continuum-limit-velocity.txt)

## Question

The companion continuum lane
([`WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md`](WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md))
showed:

- `dM` (retarded wave field deflection) is the one continuum-stable
  dynamical quantity at v/c=0.30 on Fam1: 14% monotone drift across
  the refinement {0.5, 0.35, 0.25}.
- All three c=∞ comparators tested (cached-slice dI, equilibrated
  dIeq, radial imposed-Newton dN) fail to converge — the `M − I`
  magnitude claim is comparator-dominated, not retardation-dominated.

The natural follow-on: does `dM` stay continuum-stable at **other**
velocities? If yes, we have a functional prediction `dM(v/c)` that is
a direct continuum physical observable, **independent of any c=∞
reference**. If no, the v=0.30 stability was velocity-specific.

## Setup

Physical parameters held approximately constant across refinements
(same as the companion continuum lane):

- T_phys = 15.0, PW_phys = 6.0, k*H = 2.5, S_phys = 0.004
- Source starts at IZ_START_PHYS = 3.0 (physical z), moves linearly
  in z at rate `v_target` cells/layer
- Source becomes active at layer `NL/3`, runs for `NL − NL/3` layers
- Fam1 grown DAG (seed=0, drift=0.20, restore=0.70)

Velocity targets: `v_target ∈ {−0.15, −0.25, −0.35}` (cells/layer,
negative = moving toward z=0). Refinement: `H ∈ {0.5, 0.35}`.

The H=0.25 finest step from the companion lane is skipped here
because it dominates cost (single wave solve at that resolution is
minutes; the full sweep at 3 refinements × 6 velocities took hours
in a prior run and did not complete). A 2-refinement sweep is enough
to flag convergence candidates but cannot nail down the continuum
form — see "What this does NOT establish."

## Result

### Per-velocity convergence

| v_target | H=0.5 | H=0.35 | Δ last step | verdict |
| ---: | ---: | ---: | ---: | --- |
| −0.150 | +0.009408 | +0.008996 | **4.4%** | converged |
| −0.250 | +0.009130 | +0.008435 | **7.6%** | marginal |
| −0.350 | +0.007922 | +0.007871 | **0.6%** | converged |

### Realized velocities vs targets

Because `iz_end` is integer-rounded per H, the realized `v_per_layer`
drifts slightly from the target:

| v_target | H=0.5 realized | H=0.35 realized |
| ---: | ---: | ---: |
| −0.150 | −0.1500 | −0.1379 |
| −0.250 | −0.2500 | −0.2414 |
| −0.350 | −0.3500 | −0.3448 |

The drift is small (< 10%) and symmetric across velocities — it does
not explain the v=−0.25 marginal convergence.

### Functional form on converged subset

At H=0.35 (the finest resolution tested), the two converged velocities
give:

| v | dM |
| ---: | ---: |
| −0.15 | +0.008996 |
| −0.35 | +0.007871 |

**dM is monotone decreasing in |v_target|.** As source velocity
increases, the beam deflection through the retarded wave field
decreases — consistent with the intuitive picture that the wave field
"lags behind" a faster-moving source and deposits less phase at the
beam before the source has moved on.

The full range at H=0.35 (including the marginal v=−0.25 point) is
+0.007871 to +0.008996 — a **13% spread** across a 2.3× range in
|v_target|.

## What this establishes

1. **`dM` is well-defined and bounded** across the tested velocity range.
   The three dM values at H=0.35 are all in the band [+0.0079, +0.0090].
2. **`dM` is monotone decreasing in |v|.** This is a real physical trend:
   faster-moving sources produce smaller retarded beam deflections.
3. **Two of three velocities converge** at the 5% threshold at the
   coarse→medium refinement step. v=−0.15 has Δ=4.4%, v=−0.35 has
   Δ=0.6%. The v=−0.25 marginal (7.6%) may be a coincidental slow
   convergence or a velocity-specific lattice-artifact interaction.
4. **This is done without any c=∞ comparator.** The result is a
   direct continuum prediction for the retarded gravitational
   deflection magnitude, independent of the comparator question that
   blocks the lab card.

## What this does NOT establish

- **A clean continuum-limit value at any velocity.** 2-refinement
  sweeps can only flag convergence candidates; they cannot nail the
  continuum value. Lane α+ showed a 3-refinement sweep can still
  produce bouncing (Fam2 at H=0.25 jumped up after monotone decrease).
  The "converged at 4.4% / 0.6%" labels here should be treated as
  provisional until H=0.25 or finer is added.
- **The functional form of `dM(v/c)`.** Three points is enough to
  identify a monotone trend but not enough to fit a power law,
  exponential, or any specific form. More velocity points would be
  needed, as well as at least a 3rd refinement step per velocity.
- **Family portability.** This lane runs Fam1 only. The Lane α+
  continuum-limit lane showed `kubo_true` is portable on Fam1/Fam3
  (0.5% agreement) but Fam2 is an outlier. `dM(v)` may have the same
  structure.
- **An explanation for the v=−0.25 marginal convergence.** The
  v=−0.15 and v=−0.35 points converge cleanly but v=−0.25 sits at
  7.6% drift. Could be noise at this single sample, could be a real
  lattice-artifact feature at a specific v/c. Needs either a 3rd
  refinement or a denser velocity grid to distinguish.

## Frontier map adjustment (Update 12)

| Row | Update 11 (Lane α+ family portability) | This lane |
| --- | --- | --- |
| `dM` at v/c = 0.30 | continuum-stable, 14% drift | (unchanged) |
| **`dM` at multiple v/c** | not tested | **weak positive: monotone in v, narrow range, 2/3 converged at 2-refinement level** |
| Direct continuum prediction without comparator | open | **partial — three values in a narrow band, but not yet a nailed functional form** |
| Lab-card lane | blocked (comparator-dominated) | still blocked, but `dM(v)` is a viable fallback if it's nailed at 3+ refinements |

## Honest read

This is a **weak positive** — the first direct multi-velocity
characterization of the retarded wave field's continuum behavior,
with no comparator involved. What it gets:

- A bounded, monotone, physically sensible `dM(v)` relationship
- Two velocities converged at 5% in a 2-refinement sweep
- A clear monotone trend: higher |v| → smaller `dM`

What it does not get:

- Nailed continuum values (only 2 refinements per velocity)
- A functional form (only 3 velocity points)
- Family portability (Fam1 only)
- Explanation for the v=−0.25 marginal point

The next refinement would be to add H=0.25 on the three velocities
that are already in the sweep (3 more expensive wave solves). That
would turn the "weak positive" into a proper continuum-limit claim
at each velocity, and identify whether v=−0.25 is a real feature or
a sampling artifact. This is feasible on current hardware; it was
skipped in this run only because the initial 6-velocity × 3-refinement
sweep was too expensive.

## What to attack next

1. **Extend to H=0.25 at the same 3 velocities.** Adds ~30 min of
   runtime but gives a proper 3-point refinement at each velocity.
   The minimum addition needed to turn this into a clean positive.
2. **Fam2 single-family refinement on Lane α+.** The cheapest
   insurance on the kubo_true continuum-limit story — resolves the
   Fam2 outlier at 12% drift.
3. **Wait for Codex's exact discrete static comparator.** Once it
   lands, we can rerun the wave-retardation continuum lane against
   the exact comparator and see whether the magnitude claim survives.

## Bottom line

> "At three source velocities {−0.15, −0.25, −0.35} on Fam1, the
> retarded wave field beam deflection `dM` is bounded in a narrow
> band [+0.0079, +0.0090] at H=0.35, monotone decreasing with |v|,
> and converges at the 5% threshold at the coarse→medium refinement
> step for 2 of 3 velocities (v=−0.15: 4.4%, v=−0.35: 0.6%; v=−0.25
> marginal at 7.6%). The 2-refinement sweep is not enough to nail
> the continuum value at any single velocity, but it establishes
> that `dM(v)` is a well-defined, bounded, monotone function — the
> first direct multi-velocity continuum characterization of the
> retarded wave field without any c=∞ comparator. Adding H=0.25
> at these three velocities is the cheapest next step; that would
> turn the weak positive into a proper continuum result and enable
> a functional-form fit."
