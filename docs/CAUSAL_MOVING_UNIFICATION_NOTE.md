# Causal vs Moving-Source Unification Note

**Date:** 2026-04-06  
**Status:** narrow classification note: shared causal-delay core, but genuinely separate observables

## Artifact Chain

- [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)
- [`docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md)
- [`docs/MOVING_SOURCE_CROSS_FAMILY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MOVING_SOURCE_CROSS_FAMILY_NOTE.md)
- [`docs/MOVING_SOURCE_CROSS_FAMILY_REPLAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MOVING_SOURCE_CROSS_FAMILY_REPLAY_NOTE.md)

## Question

Do the retained causal propagating-field observable and the retained
moving-source directional observable belong to the same portable mechanism
family, or do they only share a weaker causal-delay core?

## Comparison

### Retained causal propagating-field observable

The causal-field lane measures how the beam response changes when the field
itself is restricted to a causal cone.

Key retained facts:

- the exact-null control survives
- the dynamic cone ratio is stable on the center family
- the `c = 0.5` cone gives a distinct ratio from the instantaneous control
- the same dynamic ratio transfers across the three portable families only
  partially; [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)
  freezes that lane as a family boundary rather than a clean portability law

So the causal-field observable is best read as a field-scheduling / causal-cone
observable.

### Retained moving-source directional observable

The moving-source lane measures whether a source moving with signed `v` leaves
a signed centroid bias and small phase lag on a portable grown row.

Key retained facts:

- the exact zero baseline survives
- the matched static control stays flat at `v = 0`
- the centroid bias flips sign with `v`
- the effect survives on two portable grown families
- the phase lag is present but secondary to the directional centroid bias

So the moving-source observable is best read as a source-trajectory / retarded
source proxy.

## Classification

The cleanest review-safe classification is:

- **not the same portable mechanism family**
- **not fully independent either**
- **they share a common causal-delay core**
- **but they split into different observables**

The shared core is:

- causal ordering
- delayed access to the source
- direction-sensitive response to when the field becomes available

The split is:

- the causal-field observable is about the propagation of the field itself
- the moving-source observable is about the motion of the source inside an
  otherwise fixed causal response kernel

## Safe Read

What survives across both lanes:

- exact-null controls stay exact
- directional responses remain sign-sensitive
- retarded/causal structure matters in both cases

What does not survive as a single family:

- a single cross-family ratio law
- a single portable observable with the same normalization
- a clean claim that moving-source and causal-cone propagation are one and the
  same effect

## Final Verdict

**shared causal-delay core, but genuinely separate observables: the causal
propagating-field lane is a field-propagation proxy, while the moving-source
lane is a retarded-source proxy**
