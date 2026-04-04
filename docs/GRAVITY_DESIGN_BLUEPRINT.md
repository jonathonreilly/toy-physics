# Gravity Design Blueprint

Date: 2026-04-02

## Purpose

This note defines the next science frontier after the current review-hardening
cycle.

The repo now has three locked quantitative results:

1. Gravity exists in a statistically real sense on the retained setup.
2. Linear-path-sum decoherence capacity decays approximately as `1 / N`.
3. Gravity and decoherence coexist over a broad bounded parameter window on the
   same propagator / same graph family class.

The missing piece is no longer “does anything happen?” It is:

- can the gravity side be upgraded from bounded deflection to a more law-like
  structure, and
- can any mechanism beat the linear `1 / N` overlap ceiling without breaking
  the rest of the package?

## Locked Constraints

Any new design program is judged against these constraints:

- `k = 0 -> 0` sanity must stay clean
- Born / linearity companions must stay clean unless the whole point is a
  controlled Born-breaking experiment
- fixed-position controls remain mandatory for mass scaling
- centroid shift is no longer the only gravity-side observable
- channel / bundle observables must be tracked alongside centroid

## Program A: Gravity Completion

### Goal

Close the gravity story on the retained family by testing whether the observed
deflection has a stable mass law and by measuring gravity in the right
observable space.

### Why this is next

- distance scaling is now quantitative
- same-graph gravity exists
- source-aware seams and guarded dense-prune both suggest that channel-space
  structure is more informative than centroid alone

### Questions

1. Does the retained gravity response scale with source mass in a controlled,
   non-saturating window?
2. Does the response look stronger / cleaner in channel-space observables than
   in centroid shift?
3. Is the current `1 / b^2`-like detector displacement a geometry/beam effect,
   a readout effect, or the actual law of the current substrate?

### Required observables

- centroid shift
- bundle bias
- cancellation
- effective detector channel count (`eff_ch`)

### Success criteria

- a stable positive mass law on fixed-position controls
- at least one gravity observable with cleaner scaling than centroid
- explicit separation between true law, readout artifact, and saturation

### Falsifier

- if mass scaling remains noisy or saturating across clean windows and all
  channel-space observables are equally fragile, then the current gravity story
  is bounded but not law-like

## Program B: Ceiling Breaker

### Goal

Test whether the linear `1 / N` decoherence ceiling can be beaten by a mild,
review-safe nonlinear propagator.

### Why this is next

- the asymptotic obstacle is now quantitative:
  - `(1 - pur_min) ~ N^-1.01`
  - `(1 - overlap) ~ N^-0.84`
- soft graph-side tricks help only in bounded windows because they are fighting
  that ceiling

### Design principle

Only nonlinearities that explicitly target overlap homogenization are worth
testing. Generic amplitude tricks are not.

### Preferred pilot classes

1. overlap-sensitive layer normalization
2. bundle-sensitive gain/suppression
3. local competition that preserves phase information while resisting
   concentration homogenization

### Required controls

- compare exponent, not just prefactor
- Born / linearity companion on matched small controls
- no hidden moving-window or normalization artifacts

### Success criteria

- measured decay exponent for `1 - pur_min` becomes meaningfully slower than
  `1 / N`
- or a stable non-decaying floor appears on bounded windows without trivial
  collapse

### Falsifier

- if the nonlinearity only changes prefactor, breaks Born cleanly, or produces
  trivial renormalization artifacts, the lane is closed

## Program C: Hard Geometry / Nucleation

### Goal

Create hard channel geometry directly instead of trying to repair random-like
 graphs after CLT-style homogenization has already set in.

### Why this is still live

- guarded pruning works by preserving channel support
- source-aware seams survive most clearly in the retained modular family
- the strongest structural clue in the repo is still that geometry/channel
  organization matters more than weak local perturbations

### Design target

- births should add capacity to under-supported shell / channel sectors
- deaths should remove nodes that homogenize the detector pattern
- rule should preserve mass-coupled detector channels, not merely total reach

### Success criteria

- generated geometry that resists the `1 / N` ceiling better than unstructured
  graphs
- gravity-side observables survive without requiring a narrow seed pocket

### Falsifier

- if generated geometry still washes into the same `1 / N` ceiling or only
  recreates a brittle selected corner, the lane is not enough

## Priority Order

1. Program A: complete the retained gravity story with mass scaling plus
   channel-space observables
2. Program B: test one mild overlap-sensitive nonlinear propagator against the
   `1 / N` ceiling
3. Program C: develop one hard-geometry / nucleation pilot

## What We Stop Doing

- centroid-only gravity claims
- broad generic sweeps with no theory target
- more soft-pruning score variants
- more local-continuation tuning
- more source-projected promotion without seed-scaling

## Immediate Worker Tasks

1. fixed-position mass-scaling completion on the retained gravity setup
2. channel-observable scaling on the retained source-aware seam
3. one overlap-sensitive nonlinear pilot against the `1 / N` ceiling
4. one hard-geometry / nucleation pilot that targets channel support directly

## Repo-Safe Summary

The next frontier is not another cleanup sweep. It is a design program:

- finish the gravity story on the retained substrate
- attack the `1 / N` ceiling directly
- and only then decide whether the model has a real route to an emergent
  gravity law rather than a bounded interference phenomenon
