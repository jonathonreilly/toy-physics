# Wave-Retardation Continuum Limit — NEGATIVE (Comparator-Dominated, Not Retardation-Dominated)

**Date:** 2026-04-07
**Status:** proposed_retained negative — refining the lattice spacing H from 0.5 to 0.35 to 0.25 (with physical parameters held approximately constant; v/c drifts 3% at medium due to integer rounding) does NOT give a converged value for the retardation magnitude under any of **three** tested c=∞ comparators: cached static slices at NL_dyn (`dI`), equilibrated static slices at 3×NL_dyn (`dIeq`), or the corrected radial imposed-Newton field (`dN`). dM (retarded wave field) is fairly stable across the refinement (14% monotone drift) — the instability is in the comparator construction, not in the retarded field. After correcting the imposed-Newton comparator to include the transverse `y` term, `dN` no longer provides a cleaner magnitude story: `rel_MN` runs `25.60% → 1.26% → 31.24%`, while `rel_MIeq` runs `74.11% → 29.44% → 23.16%`. `dIeq` is the least unstable comparator on the last refinement step, but it still does **not** converge to `dN` (`rel_IeqN` runs `80.74% → 30.33% → 47.17%`) and does not itself converge. The "M ≠ I" existence is logically valid, but the magnitude does not survive lattice refinement under any tested comparator. The retarded field dM itself is continuum-stable and remains a well-defined physical quantity; the issue is the reference it's compared against.

## Artifact chain

- [`scripts/wave_retardation_continuum_limit.py`](../scripts/wave_retardation_continuum_limit.py)
- [`logs/2026-04-07-wave-retardation-continuum-limit.txt`](../logs/2026-04-07-wave-retardation-continuum-limit.txt)

## Question

The lab-card lane (`WAVE_RETARDATION_LAB_PREDICTION_NOTE.md`) showed
that the Lane 6 / Lane 8b 25-30% retardation gap is configuration-dependent
and does not have a clean v/c power law. This lane tests whether the
configuration dependence is a **finite-lattice-spacing artifact that
vanishes in the continuum limit**:

- Hold physical parameters approximately constant
- Refine H ∈ {0.5, 0.35, 0.25}
- See whether (M − I) / max(|M|, |I|) converges to a finite value
- If yes: there is a continuum prediction; the lab card can be unblocked
- If no: the Lane 6 result is fundamentally lattice-artifact-sensitive

## Setup

Physical parameters held **approximately** constant across refinements
(rounding to integer cell counts is unavoidable):

| Quantity | Target value | Meaning |
| --- | ---: | --- |
| `T_phys` | 15.0 | Total propagation "time" = NL × H |
| `iz_start_phys` | 3.0 | Source initial position (matches Lane 6 iz=6 at H=0.5) |
| `iz_end_phys` | 0.0 | Source final position |
| `D_phys` | 3.0 | Source displacement (matches Lane 6) |
| `PW_phys` | 6.0 | Transverse beam half-width |
| `k × H` | 2.5 | Phase per edge step (so k_phase = 2.5/H) |
| `S_phys` | 0.004 | Field source strength |
| `v/c` (target) | −0.30 | Source velocity (D_phys / (T_phys · (1−src_frac))) |

At each refinement, NL = round(T_phys / H), iz_range = round(D_phys / H),
k_phase = K_PER_H / H. The propagator and the (2+1)D wave equation are
re-implemented with explicit H (no module-level constants).

**Discretization caveat.** The realized v/c at each refinement is
NOT exactly the target. Because NL, src_layer = NL/3, n_active, and
iz_range are all integer-rounded, the actual velocity per layer drifts:

| H | NL | src_layer | n_active | iz_range | realized v/c |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.50 | 30 | 10 | 20 | 6 | **−0.3000** |
| 0.35 | 43 | 14 | 29 | 9 | **−0.3103** |
| 0.25 | 60 | 20 | 40 | 12 | **−0.3000** |

The medium step has v/c off by 3.4% from target. This is small
enough that it doesn't change the qualitative interpretation of the
results, but it means the sweep is only **approximately**
constant-velocity. A perfectly constant-velocity sweep would require
choosing T_phys so that all three (NL, src_layer, iz_range) divide
evenly at every H — which is not generally possible across an
arbitrary refinement schedule.

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

## Follow-on test: imposed-Newton comparator (added 2026-04-07)

After the cached-static-slice comparator was identified as the
unstable half, a third comparator was added to the harness as a
diagnostic baseline:

> **dN (imposed-Newton)**: at each layer t, build the field on the
> (iy, iz) cell grid as `field[iy, iz] = S / (dist + 0.1)` where
> `dist = √((layer·H − x_src)² + y² + ((iz − hw)·H − iz_of_t(t)·H)²)`.
> This is the analytic c=∞ Newtonian potential evaluated at the
> source's CURRENT physical position at every layer. No
> wave-equation evolution, no cache, no equilibration time.

The first shipped `dN` pass accidentally omitted the transverse `y`
term from the radial distance. The table below is the **corrected**
replay with the full `(x, y, z)` radial distance.

The same H ∈ {0.50, 0.35, 0.25} sweep with all three comparators:

| H | NL | dM | dI (cached static) | dN (imposed Newton) | rel_MI | rel_MN |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.50 | 30 | +0.00836 | +0.01175 | +0.01124 | **28.81%** | 25.60% |
| 0.35 | 43 | +0.00794 | +0.00878 | +0.00784 | 9.53% | 1.26% |
| 0.25 | 60 | +0.00721 | +0.01274 | +0.01049 | **43.40%** | 31.24% |

### Comparator stability across refinements

| Quantity | coarse → medium | medium → fine |
| --- | ---: | ---: |
| dM | −5.0% | −9.2% |
| **dI (cached static)** | **−25.3%** | **+45.2%** (oscillating) |
| **dN (imposed Newton)** | **−30.2%** | **+33.8%** |
| rel_MI | −66.9% | +355.6% |
| rel_MN | −95.1% | +2386.5% |

### What this tells us

**The retained negative does not depend on dN.** Even before bringing
in any Poisson-style baseline, the two wave-equation-side quantities
already show the problem:

- `dM` is fairly stable under refinement
- `dI` is not
- `rel_MI` is non-monotone and does not converge

That is enough to downgrade the quantitative Lane 6 / Lane 8b
retardation-magnitude claim.

**After fixing the radial-distance bug, dN does not rescue the lane.**
The corrected imposed-Newton comparator no longer supports the earlier
"large but cleaner" story. Instead:

- `rel_MN` is small at the medium refinement and then jumps back up at
  the fine refinement (`25.60% → 1.26% → 31.24%`)
- `dN` itself is still non-monotone (`+0.01124 → +0.00784 → +0.01049`)
- `rel_MN` is therefore also not a converged continuum quantity

So `dN` remains useful only as a diagnostic baseline, not as a stable
quantitative comparator.

### Why dN is still the wrong comparator

The imposed-Newton field `s / r` is the analytic solution to the
**Poisson equation** (`∇²f = source`), not the wave equation.

The wave equation is `(1/c²) ∂²f/∂t² − ∇²f = source`. Its **static
limit** (∂²/∂t² = 0) is also Poisson — but the wave equation in our
lattice harness has a different normalization than the imposed
potential because:

1. The wave-equation static field on the grown DAG depends on the
   lattice connectivity, the propagator weight `w h²/L²`, and the
   angular factor `exp(−β θ²)`. None of these match the imposed
   `1/r` profile in normalization.
2. The imposed-Newton field is evaluated at the cell midpoint
   without any path-sum weighting, so it has a different effective
   coupling to the beam than any wave-equation-derived field.

The right physical c=∞ analog of the wave equation is the
**exact discrete static solution of the same lattice operator** at the
current source position. The cached-static-slice comparators were
trying to approximate that object via time evolution, but the results
here show that simple late-time slicing does not pin it down cleanly
at these refinements.

So none of the tested comparators is fully satisfactory:

- **dI (cached static slice)**: right physical concept, lattice-unstable
  because the static slices aren't fully equilibrated at finite NL
- **dIeq (equilibrated static slice)**: closer to equilibrium and least
  unstable on the last step, but still not converged
- **dN (imposed Newton)**: physically apples-to-oranges and, after the
  radial fix, also not a numerically converged magnitude reference

### What this lane shows definitively

1. **dM (retarded wave field) is fairly continuum-stable** —
   monotone 14% drift across an 8× lattice density change. This is
   the cleanest result of the lane.
2. **The instability problem is in the comparator construction**,
   not in the retarded field itself. Three different comparators
   give three different non-converged magnitude stories, while the
   retarded field remains consistent.
3. **No comparator tested in this lane gives a clean continuum
   limit for the retardation magnitude.** `dIeq` is the least-bad
   current comparator, but it still does not converge.
4. **The next move is no longer simple slice equilibration.** The
   real bottleneck is defining the correct **discrete static
   comparator** for this lattice.

## Follow-on test #2: equilibrated-static-slice comparator

After imposed-Newton was shown to be a useful diagnostic baseline but
not a converged comparator, the next move was to test whether the
cached-static-slice comparator's instability is simply **incomplete
equilibration**. A fourth comparator was added:

> **dIeq (equilibrated static)**: same construction as dI, but each
> cached static problem is solved on `NL_eq = 3 × NL_dyn` layers
> instead of `NL_dyn`. The late-time slice is taken from the long
> solve, so the cached static field should be much closer to the
> true wave-equation static limit.

The hypothesis: if the dI instability is just incomplete
equilibration, dIeq should be more lattice-stable. At minimum, it
should give a smoother refinement story than dI and move in the same
general direction as the diagnostic dN branch.

### Result — the equilibrated comparator is NO BETTER

| Quantity | H=0.50 | H=0.35 | H=0.25 | drift |
| --- | ---: | ---: | ---: | --- |
| dM | +0.00836 | +0.00794 | +0.00721 | monotone, −14% |
| dI (cached static) | +0.01175 | +0.00878 | +0.01274 | oscillates, 35% |
| **dIeq (equilibrated, 3× NL)** | **+0.00217** | **+0.01126** | **+0.00554** | **oscillates, 420%** |
| dN (imposed Newton) | +0.01124 | +0.00784 | +0.01049 | −30% then +34% |

And the corresponding rel_gaps:

| Quantity | H=0.50 | H=0.35 | H=0.25 |
| --- | ---: | ---: | ---: |
| rel_MI (vs cached static) | 28.81% | 9.53% | 43.40% |
| **rel_MIeq (vs equilibrated)** | **74.11%** | **29.44%** | **23.16%** |
| rel_MN (vs imposed Newton) | 25.60% | 1.26% | 31.24% |
| **rel_IeqN (equilibrated vs Newton)** | **80.74%** | **30.33%** | **47.17%** |

### The decisive failure mode

The equilibrated static slice does **not** settle into a cleaner static
baseline as H refines. `rel_IeqN` runs 80.74% → 30.33% → 47.17%, so the
equilibrated branch still fails to line up cleanly with the diagnostic
Poisson-style baseline.

And `dIeq` itself oscillates **much more** than `dI`: +420% from
coarse to medium, −51% from medium to fine. Longer equilibration
time does not stabilize the cached slice — it adds a different
instability.

**The dI instability is NOT just incomplete equilibration.** The
discrete lattice wave-equation static problem has an H-dependent
normalization or boundary structure that longer equilibration does
not fix. Either the lattice wave operator's discrete Green's
function differs from the continuum one by O(1) factors (not O(H)
corrections), or there's a boundary / finite-domain effect that
interacts with the equilibration time in a non-trivial way.

### The one piece of good news: rel_MIeq has a smoother last step

| Quantity | Δ (medium → fine) |
| --- | ---: |
| rel_MI | 0.339 |
| **rel_MIeq** | **0.063** |
| rel_MN | 0.300 |

`rel_MIeq` changes by only 6% at the last refinement step — much
smaller than `rel_MI`'s 34% and `rel_MN`'s 30%. This is a **partial**
improvement: the equilibrated-static comparator gives a smoother
*relative gap* at the last refinement, even though the underlying
`dIeq` quantity itself oscillates. The stability is coming from `dM`
(which is stable) dominating the rel_gap when both dM and dIeq happen
to be small.

But this is not a clean convergence. `rel_MIeq` goes 74.11% →
29.44% → 23.16% — still drifting monotonically down by ~6% per
refinement. If that drift continued, it would need another 3-4
refinement steps to stabilize, which requires much finer H than we
can compute.

### Updated interpretation

After three comparators tested (dI, dIeq, dN):

- **dM (retarded wave field) is continuum-stable** — this is
  genuinely a real physical quantity that has a meaningful
  continuum limit. 14% drift across the refinement, monotone.
- **No c=∞ comparator is continuum-stable at these refinements**:
  - `dI` (cached static, NL_dyn) oscillates 35%
  - `dIeq` (equilibrated static, 3×NL_dyn) oscillates 420% then 51%
  - `dN` (imposed Newton, 1/r potential) is a useful diagnostic but
    still non-monotone and physically a different field equation
- **The wave-equation static limit on the grown DAG lattice does
  not cleanly equal the continuum Poisson solution** at H ≥ 0.25.
  The two differ by a lattice-normalization factor that changes
  with H.

The next move is no longer "equilibrate the cached slices." The
fundamental issue is that the **discrete wave-equation static
Green's function** on this lattice does not cleanly match the
continuum Poisson Green's function. To close the comparator
question, we need either:

1. **A much finer lattice** — tests whether the mismatch vanishes
   at H ≤ 0.1. Blocked by memory unless the harness is rewritten
   more efficiently (e.g., numpy-vectorized or with a sparse
   adjacency representation).
2. **An analytic derivation** of the discrete Green's function on
   the grown DAG lattice, with explicit H-dependent normalization,
   so we can compute the "correct" c=∞ comparator in closed form.
3. **A different observable entirely** — give up on the comparator
   question and characterize dM's behavior directly (how does
   it depend on v/c, on source-beam distance, on source strength)
   without reference to any c=∞ baseline.

Option 3 is the cheapest and most decisive for the flagship physics:
it asks "is the retarded wave field a well-defined physical quantity
with a clean continuum limit?" and answers yes (dM drifts only 14%
monotonically). The "retardation vs instantaneous" framing was the
issue, not the physics.

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
survives lattice refinement, the next step is **the exact discrete
static comparator** for the implemented field operator, not another
variant of stitched cached slices. The three serious options are:

1. **Direct discrete static solve**: solve the static fixed-point /
   Poisson problem on the same finite `(y, z)` grid and boundary
   conditions as the wave-equation field, then use that as the
   `c = infinity` comparator. This is now the preferred next move.
2. **Matrix-free finer-H refinement**: if the direct static solve
   still shows H-dependent normalization, push to finer H with a
   matrix-free implementation instead of the current Python adjacency
   route.
3. **Direct-`dM` flagship**: if no comparator yields a stable
   quantitative magnitude, stop centering the lane on `M - I` and
   treat the retarded field response `dM` itself as the flagship
   observable family.

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

> "Refining the lattice spacing H from 0.5 → 0.35 → 0.25 with
> physical parameters held approximately constant (modulo integer
> rounding of NL/src_layer/iz_range, which gives v/c drift of about
> 3% at the medium step) gives rel_MI values 28.81% → 9.53% → 43.40%
> — non-monotone, growing in change between successive refinements,
> no convergence. dM (retarded wave field) drifts only 14%
> monotonically and is fairly stable. dI (cached-static-slice
> comparator) oscillates 35% with no convergence pattern. That is
> already enough to show that the quantitative Lane 6 / Lane 8b
> retardation magnitude is comparator-dominated. After correcting the
> imposed-Newton comparator to use the full radial `(x, y, z)`
> distance, the `dN` branch also fails to converge:
> `rel_MN = 25.60% → 1.26% → 31.24%`. The equilibrated-static branch
> `dIeq` is the least unstable current comparator
> (`rel_MIeq = 74.11% → 29.44% → 23.16%`), but it still does not
> converge and does not approach the imposed-Newton baseline
> (`rel_IeqN = 80.74% → 30.33% → 47.17%`). The current bottleneck is
> the definition of the exact discrete static comparator for this
> lattice, not more cached-slice equilibration. The Lane 6 25%
> rel_gap is dominated by comparator construction artifacts, not by a
> stable retardation signal. The 'M ≠ I' existence is logically
> valid; the magnitude does not survive lattice refinement under any
> tested comparator. The flagship lanes that don't depend on a c=∞ comparator
> (Lanes 4, 5, 7, 8, and the lightcone half of Lane 8b) are
> unaffected. The retarded-vs-instantaneous magnitude claim of
> Lanes 6 and 8b is downgraded from 'quantitative prediction' to
> 'existence only at fixed H'."
