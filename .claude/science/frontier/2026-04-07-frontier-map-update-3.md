# Frontier Map Update #3 — 2026-04-07 (off-scaffold negative)

## What just happened

The free_coh coherence program had three partial revivals on
scaffolded cross-generators:

- Batch 1 (9 families, scaffolded): 7/9 = 77.8%
- Batch 2 (12 families, scaffolded): 10/12 = 83.3%
- Combined scaffolded: 17/21 = 81.0%, vs old rule 12/21 = 57.1%, +24 points

The last remaining caveat on all three was that the held-out generators
shared the `(layer, iy, iz)` grid scaffold. This update closes that
caveat with the off-scaffold held-out lane:

> On 9 continuous-position generators (uniform, Gaussian, clustered,
> rotated, Halton, radial, stretched), the frozen rule
> `free_coh ≥ 7.96e-04` achieves **5/9 = 55.6%**, exactly matching
> the old node-level rule. The +24 point advantage is **scaffold-specific**.

## Scorecard reversal (again)

| Row | Update 2 (post-first-negative) | Coherence lane (post-revival) | This update (post-off-scaffold) |
| --- | --- | --- | --- |
| Strength against harshest critique | reverted | modest restoration (+24 scaffolded) | **reverted**; 0 advantage off-scaffold |
| Compact underlying principle | reverted | modest restoration (single global metric) | **reverted**; no scalar metric generalizes off-scaffold |
| Theory compression | sharper target | partial answer (free_coh) | **new target**: direct path-sum argument, not metric |
| Matter / inertial closure | open | open | **now highest-priority next move** |

## What this tells us

1. **The simple-classifier lane is now closed across four distinct
   metric families** (2-prop node-level, local_z_asym, free_coh,
   off-scaffold free_coh). Four attempts, one surviving positive
   (scaffolded batch 1), three negatives.

2. **Structural intuition beats every classifier tried.** The
   pre-committed pass/fail predictions in the off-scaffold lane hit
   8/9 = 88.9%. The same kind of structural reasoning would have
   hit similar rates on the earlier batches. The classifier-search
   approach consistently underperforms human pattern matching on
   this problem.

3. **The physics is knowable.** The 88.9% baseline says the pass/fail
   boundary is determined by properties that can be read off the
   generator spec: density, symmetry, uniformity, Z2 balance in the
   measurement axis. What fails is every attempt to encode those
   properties as a SINGLE scalar metric.

4. **The right next move is not another metric search.** It is either:
   - **Matter / inertial closure** (different scorecard column, fresh
     ground, the scalar field + beam program has enough wave-equation
     infrastructure to support a persistent-object test now)
   - **Direct analytic derivation** from path-sum + S = L(1−f),
     targeting the structural features (density + symmetry) that
     explain the 88.9% baseline

## What is NOT changed by this update

- The wave-equation lanes (Lane 4–8b) remain fully retained and
  unaffected. The (3+1)D radiation, the retarded gravity, and the
  Poisson static gravity are all derived from one local PDE and are
  not scaffold-dependent in the problematic sense — they use a grid
  for the field but the *physics* (lightcone, F~M, Born, retardation)
  is substrate-natural.
- The dynamic Lane 6 condition is still a genuinely informative
  addition to the static battery.
- Only the **classifier program** is closed. The physics program is
  not.

## Bottom line

After four classifier lanes the honest summary is:

> "The simple-classifier attack on the weak-field package is exhausted.
> No single scalar metric (2-prop node, local_z_asym, free_coh,
> off-scaffold free_coh) generalizes to a genuinely cross-generator
> off-scaffold held-out set. Structural intuition remains at ~89% on
> the same generators, so the physics is predictable — but not via
> metric search. The next leverage is in matter/inertial closure or
> direct analytic derivation from the path-sum + S = L(1−f), not in
> another metric lane."
