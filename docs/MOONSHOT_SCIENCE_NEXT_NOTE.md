# Moonshot Science Next Note

**Date:** 2026-04-05  
**Status:** ranked shortlist of the next true moonshot science directions

## Purpose

This note is not a testability map.

It is the next-science shortlist after the latest retained results, with the
ranking set by one question:

- what has the best chance of unifying the wavefield, trapping/frontier, and
  self-gravity threads without breaking the weak-field lane?

The testable-platform work is now better separated elsewhere.
Here we keep the science-first ranking narrow and opinionated.

## Current retained anchors

The shortlist is grounded in the retained basis now on `main`:

- exact-lattice wavefield discriminator with a coherent detector-line phase
  ramp
- retained grown trapping/frontier transport with an outward frontier shift
- exact-lattice Poisson-like backreaction control with exact `epsilon = 0`
  reduction, but only a bounded control effect
- exact-lattice and grown-geometry weak-field laws that stay review-safe as
  long as the reduction checks are enforced

The crucial constraint is:

- do not lose the weak-field lane in order to gain a stronger field story

## Ranking

### 1. Self-Consistent Propagating Field on Retained Grown Geometry

This is still the best moonshot.

Why it ranks first:

- it is the cleanest route to a genuine causal-field mechanism
- it is the most plausible way to tie wavefield, trapping/frontier, and
  self-gravity into one architecture
- it is the one lane that could turn `gamma` from a chosen knob into an
  emergent response variable

Minimal observable:

- detector-line phase-ramp slope and span under a causal update rule, plus a
  matched-control signed detector moment

Exact reduction / falsifier:

- zero feedback must reproduce the retained grown baseline exactly at every
  iteration
- matched-null topology update with zero source must also be exact
- if the causal observable is flat after those checks, the lane is a no-go

Why it could raise the interest map:

- it would be a genuine architecture jump, not another parameter tweak
- it could unify the phase-sensitive wavefield story with the trapping/frontier
  and backreaction threads
- it would answer the strongest remaining criticism: that the current lanes are
  fragmented into separate proxies

Why it could fail:

- the update may remain effectively smoothing, with no stable causal observable
- the end-to-end weak-field law may collapse once the field feeds back
- the loop may only produce topology-induced attenuation rather than true
  self-gravity

### 2. Wavefield-Plus-Frontier Unification

This is the best bridge if the full self-consistent field is too strong a jump.

Why it ranks second:

- the exact-lattice wavefield lane is already the strongest retained phase
  discriminator
- the grown trapping/frontier lane already has a reviewable structural moment
- combining them could yield a single detector-side observable that carries
  both phase and frontier structure

Minimal observable:

- a phase-ramp observable paired with a frontier-shell radial moment shift

Exact reduction / falsifier:

- zero source or zero trapping coupling must recover the retained baseline
- if adding frontier structure destroys the phase-ramp coherence, the
  unification fails

Why it could raise the interest map:

- it would connect two retained positives into one higher-level observable
- it is closer to a real mechanism than either lane alone
- it gives a sharper story than “phase here, trapping there”

Why it could fail:

- the two effects may stay separable and refuse to cohere into one architecture
- the frontier observable may remain transport-only while the wavefield stays
  exact-lattice-only

### 3. Exact-Lattice Self-Gravity With Per-Step Born Protection

This is the cleanest self-gravity moonshot that still respects the audit bar.

Why it ranks third:

- the exact-lattice Poisson loop already gives the strictest control setup
- it is the most honest place to ask whether a self-generated field can exist
  without destroying the loop-level Born audit
- it is also the place where the current story most clearly separates step
  locality from end-to-end nonlinearity

Minimal observable:

- matched-control signed detector moment, not raw escape

Exact reduction / falsifier:

- `epsilon = 0` must be the identity loop at every iteration
- step-local Born must stay machine-clean
- if the end-to-end loop remains non-Born-clean or the weak-field law breaks,
  the lane is only a control

Why it could raise the interest map:

- it would show the model can generate a self-field without immediately losing
  the baseline physics
- it would give the paper a stronger “emergent backreaction” axis

Why it could fail:

- the loop may remain too weak to matter physically
- the end-to-end Born drift may prove that the nonlinear evolution is not a
  viable self-gravity sector

### 4. Geometry-Transfer Unification

This is the portability question, not the mechanism question.

Why it ranks fourth:

- the compact generated-family bridge is still closed
- the split-shell reopening is real but not yet a closure
- that makes geometry transfer worth pushing, but not as the top moonshot

Minimal observable:

- maintain the weak-field law while widening detector support on a genuinely
  different family

Exact reduction / falsifier:

- zero-source reduction must stay exact
- if the improved geometry only rescues support but not the law, the transfer
  remains bounded

Why it could raise the interest map:

- a real transfer to a new family weakens the “exact-lattice only” objection
- it would make the retained theory look more portable and less hand-tuned

Why it could fail:

- the family may still be geometry-limited
- support may widen without recovering the weak-field law

### 5. Strong-Field Frontier Without Losing Weak-Field Control

This is the long-shot horizon branch.

Why it ranks fifth:

- the grown trapping/frontier result is promising but still bounded
- the stronger propagating-field variants already failed
- so any stronger horizon story has to prove it is more than amplitude loss

Minimal observable:

- a no-return or frontier-shift observable that is stronger than plain escape

Exact reduction / falsifier:

- zero trapping or zero feedback must reproduce the retained baseline exactly
- if the observable collapses into monotone attenuation, the branch is only a
  transport proxy

Why it could raise the interest map:

- it would be the most obvious strong-field analogue in the current program
- it could tie into the self-gravity and causal-field stories later

Why it could fail:

- the signal may remain a transport artifact
- it may never become a causal field mechanism

## What Not To Overprioritize

- more diamond/platform planning
- more branch-side distance-law rhetoric without a stronger mechanism
- more small propagating-field tweaks that already failed the reduction bar
- more readout tuning on families where the weak-field law already collapsed

## Bottom Line

The best moonshot science direction is still:

1. self-consistent propagating field on retained grown geometry

The best fallback is:

2. wavefield-plus-frontier unification

The best self-gravity check is:

3. exact-lattice self-gravity with per-step Born protection

If one of those lands, the rest of the program becomes easier to unify.
If none of them lands, that is also valuable because it tells us the weak-field
lanes are more robust than the strong-field ones.
