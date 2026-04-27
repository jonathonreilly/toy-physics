# Propagator Family Unification Note

**Date:** 2026-04-05  
**Status:** narrow review-safe unification note for the proposed_retained wavefield,
complex-action, and electrostatics scalar-sign-law lanes

## Artifact chain

This note is a synthesis of retained `main` results only:

- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- [`docs/ELECTROSTATICS_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ELECTROSTATICS_CARD_NOTE.md)
- [`docs/ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md)

## One-line read

The common retained structure is a fixed propagator on a causal graph, with a
scalar coupling that changes how edges contribute without changing the basic
path-sum form.

That is the narrow unification claim here.

## Common propagator skeleton

Across the retained lanes, the shared shape is:

- a graph or ordered-lattice family
- a path-sum or stepwise transport rule
- a baseline propagation kernel that remains the same family-to-family
- a scalar coupling that modifies the edge contribution in a controlled way
- a zero-coupling or null-control reduction that must recover the baseline

In symbolic form, the retained lanes all look like a variant of:

```text
amplitude(edge) = baseline_propagator(edge) × scalar_coupling(edge)
```

The exact details differ by lane, but the review-safe common point is that the
coupling is scalar and multiplicative at the edge level, not a change to the
overall transport architecture.

## What each retained lane contributes

### Wavefield lane

The wavefield mechanism keeps the baseline propagator fixed and promotes a
phase-sensitive detector-line observable.

Retained behavior:

- exact zero-source reduction survives
- the detector-line phase ramp is coherent
- the ramp coefficient depends on source depth and source strength
- weak-field `F~M` stays near unity on the exact family

Interpretation:

- the scalar coupling here acts as a phase-sensitive transport control
- the important observable is not raw attenuation, but a stable phase ramp

### Complex-action lane

The complex-action carryover keeps the same ordered transport family and adds
a scalar action deformation:

```text
S = L(1 - f) + iγLf
```

Retained behavior:

- exact `gamma = 0` reduction survives
- Born stays machine-clean on the frozen exact field and the grown-row companion
- increasing `gamma` drives a `TOWARD -> AWAY` crossover
- detector escape falls sharply as the scalar coupling grows

Interpretation:

- the scalar coupling acts like a phase / absorption deformation of the same
  fixed propagator
- the narrow retained claim is structural crossover, not geometry-independence

### Electrostatics scalar-sign lane

The electrostatics card keeps the same ordered-lattice transport family but
changes the source polarity.

Retained behavior:

- sign antisymmetry is clean
- opposite-sign superposition cancels to printed precision
- dipole orientation flips the sign of the response
- the charge response is linear on the tested range
- screening strongly attenuates the response

Interpretation:

- the scalar coupling acts like a sign selector on the same transport skeleton
- the retained claim is electrostatics-like sign structure, not full Maxwell
  theory

## What is actually unified

The narrow unification is:

- same underlying path-sum / transport scaffold
- same requirement for a null or zero-coupling reduction
- same use of a scalar coupling to alter edge-level transport
- same review discipline: the promoted observable must survive the baseline
  check

That is enough to say the project has a **propagator family**, not merely a set
of unrelated cards.

## What is not unified yet

This note does **not** claim:

- geometry-generic transfer from exact lattices to all generated families
- a derivation of the scalar couplings from one principle
- full electromagnetism
- continuum closure
- self-gravity as a retained mechanism
- QNM / BMV / horizon thermodynamics as retained claims
- a single flagship theorem that forces belief on its own

The missing step is still a stronger bridge between families, not a new
taxonomy of existing results.

## Safe conclusion

The narrow review-safe statement is:

- the retained wavefield, complex-action, and electrostatics results all share
  a common propagator skeleton
- the difference between them is the scalar coupling attached to the same
  transport architecture
- the project is therefore better described as a family of fixed-field
  coupling laws than as a pile of disconnected numerics

That is the strongest unification claim currently supported on `main`.

