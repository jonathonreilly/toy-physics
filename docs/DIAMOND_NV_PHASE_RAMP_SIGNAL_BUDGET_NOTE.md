# Diamond / NV Phase-Ramp Signal Budget Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** narrow experiment-facing **discriminator** card for the
phase-sensitive lane; **not** a closed signal budget.
**Status authority:** independent audit lane only.
**Authority role:** records, but does not close, a bounded discriminator
card naming the lock-in observables (`X`, `Y`, `phi`, widefield phase
ramp), the qualitative ordering with drive frequency / separation, and
the minimal control stack, conditional on cited upstream retarded /
wavefield notes and the sibling diamond protocol / prediction notes.
The "signal budget" terminology here refers to the **qualitative
ordering structure**, not to a calibrated absolute amplitude budget.
Names the missing NV ideal-detector forward-model bridge theorem as
the single open theorem target for a closed signal budget.

## One-line read

The best current diamond-facing **discriminator design** is not an
absolute gravity measurement.
It is a lock-in quadrature and spatial phase-ramp null test, conditional
on the cited upstream phase-sensitive lane and on a future NV ideal-
detector forward model (still missing).

## Audit boundary

This note assembles a class-B experiment-facing discriminator card by
importing upstream retarded / wavefield phase-ramp authorities, the two
sibling diamond protocol / prediction notes, the propagator-family
unification meta note, and the complex-action carryover / grown
companion notes. It is **not** a derivation of those upstream phase-
ramp results and **not** a closed NV-coupling forward model.

**Cited authorities (one-hop deps; cited but not closed in this note):**

- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)
  (`claim_type: positive_theorem`, `effective_status: unaudited`) —
  supplies the proposed wavefield mechanism. Cited as proxy-level
  motivation for the spatial phase-ramp readout; itself not retained-
  grade and currently unaudited.
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — supplies the bounded exact-lattice wavefield escalation. Cited as
  proxy-level motivation; not a retained NV-coupling theorem.
- [`docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`)
  — supplies the complex-action carryover used as motivation for a
  scalar-coupling phase / absorption crossover.
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
  (`claim_type: positive_theorem`, `effective_status: audited_conditional`)
  — sibling complex-action grown-companion note, cited as proxy-level
  motivation.
- [`docs/PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`](PROPAGATOR_FAMILY_UNIFICATION_NOTE.md)
  (`claim_type: meta`, `effective_status: audited_conditional`) —
  meta-level propagator-family note; keeps the claim surface narrow
  ("same transport skeleton, different scalar coupling"). Itself meta,
  not a closure.
- [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](DIAMOND_SENSOR_PROTOCOL_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — sibling discriminator protocol; itself bounded and not a closed
  NV prediction (see this PR's narrowed Audit boundary block in that
  note).
- [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](DIAMOND_SENSOR_PREDICTION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — sibling discriminator prediction; itself bounded and not a closed
  NV prediction (see this PR's narrowed Audit boundary block in that
  note).

**In-note class-B content (what survives at this scope):**

- a discriminator card naming the lock-in observables `X`, `Y`,
  `phi = atan2(Y, X)`, and the widefield spatial phase profile;
- a qualitative ordering: standard quasi-static null gives `Y ~ 0`,
  `phi ~ 0`, flat phase, while a finite-delay / wave-like coupling
  gives `Y != 0`, `phi != 0`, and a coherent spatial phase ramp that
  strengthens with drive frequency and source-detector separation;
- a minimal control stack (drive off; source retracted; `pi`
  reference flip; static-source baseline) and a pre-experiment
  validation step (run the same lock-in pipeline on a known magnetic
  or strain source first);
- a narrow narrative reading of the cited authorities: the wavefield
  lane gives the phase-ramp motivation; the complex-action lanes show
  that a scalar coupling can deform the same propagator into a phase /
  absorption crossover; the propagator-family note keeps the claim
  surface narrow at "same transport skeleton, different scalar
  coupling"; the sibling diamond protocol / prediction notes already
  map that structure onto an NV lock-in readout.

These are class-B / class-A consequences of the cited upstream phase-
ramp / complex-action authorities; they are **not** a derivation of
the NV ideal-detector forward model and **not** a calibrated absolute
amplitude budget.

**Admitted-context derivation gap (real, not import-redirect):**

The note **does not** derive any of:

1. an ideal-detector forward model mapping a driven source trajectory
   through an NV Hamiltonian to lock-in observables `X`, `Y`, `phi`,
   and a widefield spatial phase profile;
2. a validated mapping from the cited retained / conditional wavefield
   proxy to a real NV sensor coupling strength;
3. a calibrated absolute signal budget for a specific NV lab geometry
   that would convert the qualitative ordering into a detectability
   claim;
4. a source geometry that is already tied to a specific lab setup;
5. a lab-specific noise-floor estimate.

The note explicitly labels (1)-(5) under "What remains unknown" and
"What this is not". This is a **real D-class derivation gap**, not a
dependency-citation issue. No retained, bounded, or proposed theorem
on the current atlas closes (1)-(5) for this row. The "signal budget"
in the note title refers to the **qualitative ordering structure**
(drive band × separation, and ordering of `Y`, `phi`, ramp slope), not
to a calibrated absolute amplitude budget.

## What should be measured

Measure the standard lock-in channels:

- `X`: in-phase response
- `Y`: quadrature response
- `phi = atan2(Y, X)`: phase lag

If the setup is widefield, also measure the spatial phase profile across the
NV image.

## Standard null

After calibration and static-background subtraction, the quasi-static /
instantaneous baseline should give:

- `Y ≈ 0`
- `phi ≈ 0`
- no stable spatial phase ramp

That is the null the protocol is built around.

## Discriminator-design expectation (scope-bounded)

Conditional on the cited upstream phase-sensitive / retarded /
wavefield authorities above and on a future ideal-detector forward
model (still missing), the discriminator-design expectation is:

- a nonzero quadrature channel `Y`
- a nonzero phase lag `phi`
- in widefield readout, a coherent spatial phase ramp
- stronger phase-sensitive response as source-detector separation increases
  and as the drive moves away from the quasi-static limit

This is the **qualitative ordering** the discriminator card is built
around. It is **not** a calibrated NV detectability claim; the
ideal-detector forward model and the validated NV-coupling map are not
closed in this note.

## Minimal control stack

Use the smallest control set that distinguishes signal from instrument lag:

1. drive off
2. source retracted far enough that coupling should be negligible
3. same drive with a `pi` reference flip, to verify the quadrature sign
4. static source / no modulation, to remove DC or slow drift backgrounds

If the lab wants one extra validation step, run the same lock-in pipeline on a
known magnetic or strain source first.

## What in-repo evidence motivates this discriminator card

This note is motivated by the cited upstream evidence (status disclosed
in the Audit boundary block above), not by lab-budgeted amplitude
estimates:

- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- [`docs/PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`](PROPAGATOR_FAMILY_UNIFICATION_NOTE.md)
- [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](DIAMOND_SENSOR_PROTOCOL_NOTE.md)
- [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](DIAMOND_SENSOR_PREDICTION_NOTE.md)

The narrative reading of the cited evidence (qualitative motivation,
not a closed bridge):

- the wavefield lane gives the phase-ramp motivation
- the complex-action lanes show that a scalar coupling can deform the same
  propagator into a phase / absorption crossover
- the propagator-family note keeps the claim surface narrow: same transport
  skeleton, different scalar coupling
- the sibling diamond protocol / prediction notes already map that
  structure onto an NV lock-in readout

This narrative is **not** a derivation. The bridge from the cited
proxy-level phase-ramp evidence to NV lock-in observables remains the
open D-class theorem target.

## What remains unknown

Before contacting a lab, the repo still does **not** provide:

- a calibrated absolute signal budget
- a source geometry that is already tied to a specific lab setup
- a lab-specific noise-floor estimate
- a validated mapping from the retained wavefield proxy to a real NV sensor
  coupling strength

So the claim surface stays narrow:

- phase-quadrature discriminator: yes
- coherent spatial phase ramp: yes
- absolute gravity detectability: not yet budgeted here

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the reference `pi` control
- a widefield image shows a stable nonzero phase gradient
- the phase signal strengthens in the expected causal direction with
  separation / drive changes

## What would count as a miss

- the quadrature vanishes after calibration
- the phase is flat across the image
- the signal is explained entirely by instrument lag, heating, or a trivial
  amplitude rescaling

## Final verdict (scope-bounded)

**Bounded experiment-facing discriminator card; not a closed signal
budget.**

Conditional on the cited upstream phase-sensitive / retarded /
wavefield / complex-action authorities and on the sibling diamond
protocol / prediction notes (all narrowed in this PR), this row records:

- a discriminator card naming `X`, `Y`, `phi`, and the spatial phase
  profile;
- a qualitative ordering with drive frequency / separation and a
  minimal control stack;
- a narrative reading of the cited evidence at the proxy / structural
  level only.

It is **not** a closed lab signal budget, **not** a calibrated NV
detectability claim, and **not** a derivation of the cited upstream
authorities. The "signal budget" terminology refers to the qualitative
ordering structure, not to a calibrated absolute amplitude budget. The
ideal-detector forward model and validated NV-coupling map remain open
as the single D-class theorem target for this row.

## Repair target

Per audit verdict (`notes_for_re_audit_if_any`): provide an
ideal-detector forward-model theorem plus a validated mapping from the
retained wavefield proxy to NV lock-in observables `X`, `Y`, `phi`,
and the spatial phase profile before re-auditing. The current note
exposes only the qualitative ordering and the discriminator card; the
bridge theorem from cited retarded / wavefield proxies to calibrated
NV lock-in observables is the open target.

## Repo-canonical vocabulary

Terminology used in this note matches the repo-canonical vocabulary:
"diamond NV", "phase ramp", "signal budget", "prediction", "protocol",
"lock-in quadrature `Y`", "phase lag `phi`", "spatial phase profile".
No new tags, no new classes, no parent-framing cross-references
implying a class, no status promotion language.
