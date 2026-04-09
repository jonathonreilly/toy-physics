# dM Continuum Limit Across Multiple v/c — Downgraded (3-Refinement Negative)

**Date:** 2026-04-07 (revised with H=0.25 data)
**Status:** retained negative — earlier "weak positive" framing from a 2-refinement sweep is **downgraded**. At 3 refinements H ∈ {0.5, 0.35, 0.25} on 3 velocities, **none** of the dM values converge at the 5% threshold. Last-step drifts are 16.4% (v=−0.15), 9.3% (v=−0.25), 13.5% (v=−0.35). The monotone-in-v pattern seen at H=0.35 also breaks at H=0.25 — v=−0.25 becomes a local peak. What survives: dM values at H=0.25 sit in a narrow band [+0.0068, +0.0077] (12% spread across the v range), and each velocity individually shows monotone decrease with H, suggesting dM is approaching a smaller limit ~0.006 as H → 0 but has not reached it.

## Artifact chain

- [`scripts/dm_continuum_limit_velocity.py`](../scripts/dm_continuum_limit_velocity.py)
- [`logs/2026-04-07-dm-continuum-limit-velocity.txt`](../logs/2026-04-07-dm-continuum-limit-velocity.txt)

## History

This note was originally written as a **weak positive** based on a
2-refinement sweep {H=0.5, H=0.35} that showed 2 of 3 velocities
converging at the 5% drift threshold, with dM monotone decreasing in
|v|. Adding the third refinement at H=0.25 downgrades the claim —
see [History section](#history-of-the-downgrade) at the bottom for
the earlier numbers and why they gave a misleading picture.

## Question

The companion continuum lane
([`WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md`](WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md))
showed that `dM` (retarded wave field deflection) was the **least
unstable** dynamical quantity on Fam1 at v/c=0.30: it had 14% monotone
last-step drift across the refinement {0.5, 0.35, 0.25}, while all
c=∞ comparators tested were more unstable.

The natural follow-on: does `dM` stay the least unstable wave-field
observable at **other**
velocities? If yes, we have a functional `dM(v/c)` as a direct
continuum physical observable, independent of any c=∞ comparator.

## Setup

Physical parameters held approximately constant across refinements
(same as the companion continuum lane):

- T_phys = 15.0, PW_phys = 6.0, k*H = 2.5, S_phys = 0.004
- Source starts at IZ_START_PHYS = 3.0, moves linearly in z at
  velocity `v_target` cells/layer
- Source activates at NL/3, runs for NL − NL/3 layers
- Fam1 grown DAG (seed=0, drift=0.20, restore=0.70)

Velocity targets: v ∈ {−0.15, −0.25, −0.35}. Refinement:
H ∈ {0.5, 0.35, 0.25}.

## Result (3-refinement sweep)

### Refinement table

| v_target | H=0.5 | H=0.35 | H=0.25 | Δ last step | verdict |
| ---: | ---: | ---: | ---: | ---: | --- |
| −0.150 | +0.009408 | +0.008996 | **+0.007523** | **−16.4%** | NOT converged |
| −0.250 | +0.009130 | +0.008435 | **+0.007647** | **−9.3%** | marginal |
| −0.350 | +0.007922 | +0.007871 | **+0.006812** | **−13.5%** | marginal |

### What this tells us

**None converge at 5%.** The best is v=−0.25 at 9.3%, and the
worst is v=−0.15 at 16.4%. All three drifts are negative (monotone
decrease with H refinement), and all three are large.

**The monotone-in-v pattern breaks at H=0.25.** At H=0.35 the values
were (0.0090, 0.0084, 0.0079) — monotone decreasing in |v|. At
H=0.25 they are (0.00752, **0.00765**, 0.00681) — v=−0.25 is now a
local peak, not an intermediate. The monotone-in-v claim from the
2-refinement sweep was a coincidence of the particular lattice
resolutions.

### What survives

- **dM values are bounded across v.** At H=0.25 they occupy the
  narrow band [+0.00681, +0.00765], a **12% spread** across the
  2.3× range in |v|. This is a real feature — dM is not exploding
  or collapsing to zero anywhere in this velocity range.
- **Each velocity individually decreases monotonically with H.** The
  H=0.5 → H=0.35 → H=0.25 trajectory is monotone for all three
  velocities, and the drift sizes suggest dM is approaching a
  smaller limit (~0.006 to 0.007) as H → 0. We just haven't reached
  that limit with H=0.25.

### Interpretation

`dM(v, H)` shows two real features: (a) monotone decrease with
lattice refinement at each v, and (b) bounded in a narrow band
across v. What it does NOT show is convergence at the tested
refinement levels. The earlier "weak positive" framing confused a
coincidental smooth intermediate step (H=0.5 → H=0.35) with real
convergence.

The companion continuum lane's original result at v=−0.30 on Fam1
had the same structure: monotone decrease with H, 14% drift at the
last step. That was described as "fairly continuum-stable." The
Lane δ result here is consistent with that — ~10-16% last-step
drift across three velocities, bounded band of values. The "stable"
claim was really "bounded and monotone in H, but not yet
numerically converged at this resolution."

## What this does NOT establish

- Whether dM converges at finer H. The monotone-in-H trend is
  compatible with eventual convergence (to ~0.006), but the drift
  sizes (9–16%) are still large and we cannot extrapolate reliably.
- A functional form dM(v). Three points is not enough to fit
  anything, and the transverse structure (monotone vs non-monotone
  in v) is unstable under refinement.
- Family portability. This lane runs Fam1 only. Lane α++ showed
  Fam2 does NOT converge for kubo_true; a similar negative is
  plausible for dM(v) on Fam2.

## Frontier map adjustment (Update 12, revised)

| Row | 2-refinement framing (earlier) | 3-refinement framing (this update) |
| --- | --- | --- |
| dM(v) at multiple velocities | **weak positive**: monotone in v, 2/3 converged | **negative**: 0/3 converged at H=0.25, non-monotone in v at finest H |
| Functional-form prediction dM(v/c) | "narrow band" | **still bounded band**, but not nailed |
| Direct continuum prediction without comparator | partial | still partial — same status as companion lane's v=−0.30 result |

## Honest read

The Lane δ weak positive was premature. Running the 3rd refinement
(H=0.25) shows that what looked like "2/3 converged at 5%" was a
coincidence of the coarse→medium step being small at two of the
three velocities. The finest step (medium→fine) reveals 9-16%
drift at all three velocities and a broken monotone-in-v pattern.

What doesn't change:

- The companion continuum lane's v=−0.30 result is unaffected. It
  already reported 14% drift at the last step and called it
  "fairly continuum-stable" — consistent with these new numbers.
- dM values remain bounded in a narrow band across v.
- Each velocity's H-trajectory is monotone decreasing.

What does change:

- We can no longer claim dM has a clean converged value at any
  single velocity (only the qualitative "bounded and monotone in H"
  pattern holds).
- The "dM is monotone in v" claim is wrong at H=0.25 — it was an
  artifact of the coarser lattices.

## What to attack next

1. **Refine at H=0.20 on the same three velocities.** The monotone
   H-trajectory at all three velocities suggests the continuum limit
   is at smaller H. Adding one more refinement point per velocity
   would give a 4-point series to fit a power-law or extrapolate.
   This is the cheapest next move.
2. **Wait for Codex's exact discrete static comparator** — when it
   lands, rerun the wave-retardation continuum lane against the
   exact comparator. That's on the main retardation-magnitude path
   and is orthogonal to Lane δ.
3. **Do not re-run Fam2/Fam3 on dM(v)** — the Lane α++ negative
   suggests those families won't converge better, and the result
   would not meaningfully update the scorecard.

## History of the downgrade

The original note of this lane cited a 2-refinement sweep with
these numbers (H ∈ {0.5, 0.35} only):

| v_target | H=0.5 | H=0.35 | Δ last | verdict |
| ---: | ---: | ---: | ---: | --- |
| −0.15 | +0.00941 | +0.00900 | 4.4% | "converged" |
| −0.25 | +0.00913 | +0.00844 | 7.6% | marginal |
| −0.35 | +0.00792 | +0.00787 | 0.6% | "converged" |

The 2-refinement sweep gave 2 of 3 velocities apparent convergence.
It also gave a clean monotone-in-|v| pattern at H=0.35.

Adding H=0.25 broke both: all three velocities now show 9-16%
drift (none converged), and the v=−0.25 value is a local peak in
v-space. The original "weak positive" bottom line was premature.

This is honest science: the 2-refinement framing flagged
convergence candidates, and the 3-refinement data showed they
weren't actually converged. The downgrade is the correct move.

## Bottom line (revised)

> "At three source velocities v ∈ {−0.15, −0.25, −0.35} on Fam1
> with 3 refinements H ∈ {0.5, 0.35, 0.25}, none of the dM values
> converge at the 5% threshold. Last-step drifts are 16.4%, 9.3%,
> 13.5%. The earlier 2-refinement 'weak positive' framing is
> downgraded. What survives: dM values at H=0.25 sit in a narrow
> band [+0.0068, +0.0077] (12% spread), and each velocity
> individually shows monotone decrease with H, suggesting a
> continuum limit near ~0.006 that requires finer H to reach. The
> 'dM is monotone in v' pattern seen at H=0.35 breaks at H=0.25
> (v=−0.25 is now a local peak). This is consistent with the
> companion continuum lane's original v=−0.30 finding (14% drift,
> called 'fairly continuum-stable') — both lanes show dM is
> bounded and well-ordered but not numerically converged at this
> lattice resolution."
