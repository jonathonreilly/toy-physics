# Matter / Inertial Closure — NEGATIVE (Equivalence Principle Fails)

**Date:** 2026-04-07
**Status:** proposed_retained negative — Gaussian persistent packets on the grown-DAG propagator under a uniform linear force give Newton-linear delta_z per packet (R² > 0.96) but equivalence-principle slopes differ by **123%** across packets. The "fields but no matter" critique stands: the model does not exhibit generator-invariant inertial mass at the persistent-object level.

## Artifact chain

- [`scripts/matter_inertial_closure.py`](../scripts/matter_inertial_closure.py)
- [`logs/2026-04-07-matter-inertial-closure.txt`](../logs/2026-04-07-matter-inertial-closure.txt)

## Question

The classifier lane is closed (Update 3). The remaining gap on the
harshest-critique row is **"fields but no matter"** — the program has
wave equations, retardation, and radiation, but no persistent
localized objects with inertial response.

This lane attempts the closure directly with a minimal Newton test:

1. **Persistent object** = Gaussian amplitude packet at layer 1
2. **Uniform force** = linear field `f(y, z) = -g * z`
3. **Newton**: delta_z(g) - delta_z(0) should be linear in g
4. **Equivalence**: the linear slope should be **generator-invariant**
   — same across packets with different widths
5. **Family portability**: slopes should agree across Fam1/2/3

PASS requires all five (persistence, Newton linear, equivalence,
null, family portability).

## Result

| Test | Pass/Fail | Detail |
| --- | :---: | --- |
| Null (g=0 → delta_z=0) | **OK** | exact zero for all packets |
| Newton linearity per packet | **Partial** | narrow R²=1.0000, medium R²=0.9636, wide R²=0.9847 |
| Equivalence principle (slopes) | **FAIL (123%)** | narrow −73.5, medium −7.05, wide −18.3 |
| Persistence (σ_det/σ_0 < 4) | **FAIL** | narrow spreads 4.68× (to 2.34), medium 1.63×, wide 1.08× |
| Family portability (Fam1/2/3) | **Partial** | slopes −7.05, −5.94, −6.07 — rel dev 10.98% |

## The decisive finding

Three Gaussian packets of different initial widths, under the **same**
uniform force field, give response slopes differing by a factor of 10:

| Packet | σ_0 | σ_det | slope | R² |
| --- | ---: | ---: | ---: | ---: |
| narrow | 0.50 | 2.34 | **−73.45** | 1.0000 |
| medium | 1.00 | 1.63 | **−7.05** | 0.9636 |
| wide | 1.50 | 1.62 | **−18.28** | 0.9847 |

If the model had inertial mass in the Newton/equivalence sense, these
slopes would be approximately equal (all falling at the same rate).
Instead they span more than an order of magnitude.

## Physical interpretation of the failure

The narrow packet's large slope is **not** "larger inertial response"
— it is **wave-mechanical dispersion combined with field-gradient
coupling**. The narrow packet spreads rapidly (σ: 0.50 → 2.34, a 4.68×
expansion) as it propagates freely, becoming delocalized across a
wide z-range. Under the linear field `f = −g·z`, the delocalized
packet samples a large span of the z-gradient, accumulating more
net phase variation than a packet that stays localized.

In other words: the slope is **dispersion-dependent**, not
**mass-dependent**. The narrow packet responds more because it has
spread over more z, not because it has smaller "mass."

The medium and wide packets start already delocalized and do not
spread as much relative to their initial extent. Their slopes (−7.05
and −18.28) are of the same order but still differ by 2.6×. Even
among the "well-behaved" packets, the equivalence principle fails
at the 2–3× level.

## Why this is a real negative, not a setup artifact

Three potential confounds, all ruled out:

1. **Baseline centroid bias.** The narrow packet has a nonzero free
   centroid (cz(g=0) = +0.187) due to seed-specific drift asymmetry,
   but `delta_z = cz(g) − cz(0)` cancels this. The reported slopes
   are difference-based.

2. **Field coupling normalization.** The linear field `f = −g·z`
   couples identically to every node in every packet. Different
   slopes reflect different spatial extents of the amplitude
   distribution at the field locations, not different coupling
   strengths.

3. **Propagator nonlinearity.** The propagator is linear in the
   sources, so packet responses should add. The Gaussian packet is
   a linear combination of point sources — each point source feels
   the local field at its location. If equivalence held, the centroid
   of the sum would equal the sum of centroids weighted by source
   amplitudes, which for a symmetric Gaussian at origin gives a
   slope independent of σ. The slopes are NOT equal, so equivalence
   fails in the actual propagator behaviour, not in the measurement.

The failure is a genuine wave-mechanical feature: **the centroid of
a packet that spreads differently will accumulate differently under
a spatial field gradient**, regardless of whether the sources are
weighted uniformly or as a Gaussian. Without a mechanism that makes
the spreading **identical** across packets, the equivalence principle
cannot hold.

## What this closes

The critique that the program has "fields but no matter" stands
after this attempted closure:

- The program has persistent wave packets that approximately survive
  propagation (medium and wide)
- It has Newton-linear response to a uniform force per packet
- It has an exact null
- It has approximate family portability (11%, barely over 10%)

But it does **not** have:

- Generator-invariant inertial mass
- Equivalence principle at the persistent-object level
- A concept of "matter" that responds identically to a force
  regardless of its internal structure

A classical Gaussian packet is the natural first try for a persistent
object, and it fails this test. Getting matter to emerge in this
model would require either:

1. A **different persistent-object definition** — e.g., soliton-like
   structures whose width is stabilized by a nonlinearity
2. A **modified action** that includes a mass term directly
3. A **different kind of coupling** to the field that is geometry-independent

All three are structural changes, not tuning. This lane does not
explore them; it documents the negative for the specific
attempted-closure route (Gaussian packet + uniform linear field +
grown-DAG propagator + S = L(1−f)).

## Frontier map adjustment (Update 4)

| Row | Previous | This lane |
| --- | --- | --- |
| Matter / inertial closure | open, highest priority next move | **NEGATIVE** via Gaussian-packet attempt; open for other closure routes |
| Compact underlying principle | classifier lane closed | unchanged |
| Theory compression | direct path-sum argument needed | **sharper target**: derive why packet width determines slope |
| Strength against harshest critique | reverted | **"fields but no matter" critique stands** after both classifier and matter closure attempts |

## Honest read

The matter closure **attempt** failed. This does not prove matter
cannot emerge in the model; it shows the most natural minimal test
(Gaussian persistent packet under uniform force) does not give
equivalence. After:

- 4 classifier lanes (3 negatives, 1 partial-then-reverted)
- 1 matter closure attempt (this lane, negative)

The program's scorecard on the harshest-critique row is not
materially stronger than it was before Update 3. The wave-equation
physics program (Lanes 4–8b) is unaffected and remains the strongest
retained result set.

The remaining targets:

1. **Alternative persistent-object definitions** (solitons,
   coherent states, topological defects) — structural changes,
   not tuning
2. **Analytic derivation** of why packet width determines the force
   response — gives a sharper understanding of why equivalence fails
3. **Modified action with a mass term** — a different program
   altogether, not a closure of the current one

## Bottom line

> "The matter closure attempt with Gaussian packets of three different
> initial widths (σ=0.5, 1.0, 1.5) under a uniform linear force
> field `f = −g·z` gives Newton-linear delta_z(g) per packet
> (R² > 0.96) but slopes differing by 123% across packets
> (−73.5 / −7.05 / −18.28). The equivalence principle fails at the
> persistent-object level on the grown-DAG propagator. The narrow
> packet's amplified response is wave-mechanical spreading, not
> inertial mass. The 'fields but no matter' critique stands after
> this attempted closure; the remaining paths are alternative
> persistent-object definitions, analytic derivation of why
> spreading determines response, or a modified action with a mass
> term — all structural changes to the model, not parameter tuning."
