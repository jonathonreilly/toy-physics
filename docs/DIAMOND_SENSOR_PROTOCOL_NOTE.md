# Diamond Sensor Protocol Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded lab-facing discriminator protocol, intentionally
bounded; **not** a closed NV prediction.
**Status authority:** independent audit lane only.
**Authority role:** records, but does not close, a bounded discriminator
protocol (lock-in `X`, `Y`, `phi`, widefield phase ramp; minimal control
stack; qualitative ordering table) for a diamond/NV collaborator,
conditional on cited upstream retarded-field / wavefield notes. Names
the missing NV ideal-detector forward-model bridge theorem as the
single open theorem target for a closed protocol.

## Purpose

This note turns the cited phase-sensitive / retarded / wavefield lane
into a concrete **discriminator protocol** a diamond/NV collaborator
could evaluate. It is **not** a closed protocol in the sense of a
calibrated lab signal budget; the ideal-detector forward model and
the NV-coupling map are still missing.

The repo does **not** yet support a defensible absolute gravity
amplitude for an NV experiment. So the claim surface stays narrow:

- phase-quadrature discriminator design: yes
- coherent spatial phase ramp design: yes
- absolute gravity detectability: not budgeted here

## Audit boundary

This note assembles a class-B experiment-facing protocol card by
importing upstream retarded-field / wavefield phase-ramp authorities
and naming the corresponding lock-in observables (`X`, `Y`,
`phi = atan2(Y, X)`, widefield phase profile). It is **not** a
derivation of those upstream phase-ramp results and **not** a closed
NV-coupling forward model.

**Cited authorities (one-hop deps; cited but not closed in this note):**

- [`docs/RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md`](RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`)
  — supplies the bounded retarded-field causality probe used as
  qualitative motivation for a finite-delay phase-lag signature.
- [`docs/RETARDED_FIELD_DELAY_PROXY_NOTE.md`](RETARDED_FIELD_DELAY_PROXY_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — supplies the bounded intermediate-layer phase-lag proxy. Cited as
  motivation for the qualitative ordering with drive frequency and
  separation; itself not retained-grade.
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — supplies the bounded exact-lattice wavefield escalation that motivates
  the spatial phase-ramp readout. Cited as proxy-level motivation; not a
  retained NV-coupling theorem.

**In-note class-B content (what survives at this scope):**

- a discriminator protocol naming the lock-in observables `X`, `Y`,
  `phi`, and the widefield spatial phase profile;
- a qualitative ordering table: standard quasi-static null gives
  `Y ~ 0`, `phi ~ 0`, flat phase, while a finite-delay / wave-like
  coupling gives `Y != 0`, `phi != 0`, and a coherent spatial phase
  ramp that strengthens with drive frequency and source-detector
  separation;
- a minimal control stack (drive off; source retracted; `pi`
  reference flip; static-source baseline) and a pre-experiment
  validation step (run the same lock-in pipeline on a known magnetic
  or strain source first);
- the same qualitative content reported by
  `scripts/diamond_sensor_protocol_probe.py`, which is a class-A
  consequence of the qualitative ordering (not a calibrated forward
  model).

These are class-B / class-A consequences of the cited upstream phase-
ramp authorities and qualitative-ordering reasoning; they are **not**
a derivation of the NV ideal-detector forward model and **not** a
calibrated signal budget.

**Admitted-context derivation gap (real, not import-redirect):**

The note **does not** derive any of:

1. an ideal-detector forward model mapping a driven source trajectory
   through an NV Hamiltonian to lock-in observables `X`, `Y`, `phi`,
   and a widefield spatial phase profile (perfect phase reference, no
   technical noise, no bandwidth or integration limits);
2. a validated mapping from the cited retained / conditional wavefield
   proxy to a real NV sensor coupling strength;
3. a calibrated absolute signal budget for a specific NV lab geometry
   that would convert the qualitative ordering table into a
   detectability claim.

The note explicitly labels (1) under "Requirement: ideal-detector
forward model first" and (2)-(3) under "Honest limitation". This is a
**real D-class derivation gap**, not a dependency-citation issue. No
retained, bounded, or proposed theorem on the current atlas closes
(1)-(3) for this row.

## What the lab should measure

Measure the lock-in channels:

- `X`: in-phase response
- `Y`: quadrature response
- `phi = atan2(Y, X)`: phase lag

If the setup is widefield, also record the spatial phase profile across the NV
image.

## Requirement: ideal-detector forward model first

Before any lab-specific protocol is treated as complete, build the
ideal-detector version of the measurement:

- same driven source history in every comparator
- perfect phase reference
- no noise floor
- no finite-bandwidth or spectral-leakage model
- direct output for `X`, `Y`, `phi`, and spatial phase profile

This is a required precondition, not an optional refinement.
It checks source fidelity first and keeps the physics prediction
separate from detector artefacts.

## Standard null

After calibration and static-background subtraction, the quasi-static /
instantaneous Newtonian baseline should give:

- `Y ≈ 0`
- `phi ≈ 0`
- no stable spatial phase ramp

## Discriminator-design expectation (scope-bounded)

Conditional on the cited upstream retarded-field / wavefield authorities
above and on a future ideal-detector forward model (still missing), the
discriminator-design expectation is:

- a nonzero quadrature channel `Y`
- a nonzero phase lag `phi`
- a coherent spatial phase ramp in widefield readout
- strengthening of the quadrature / phase signal with increasing drive
  frequency and increasing source-detector separation

This is the **qualitative ordering** the protocol card is built around.
It is **not** a calibrated NV detectability claim, since neither the
ideal-detector forward model nor the validated NV-coupling map is closed
in this note.

## Minimal control stack

Use the smallest control set that lets the collaborator tell signal from
instrument lag:

1. drive off
2. source retracted far enough that the coupling should be negligible
3. same drive with a `pi` reference flip, to verify the quadrature sign
4. static source / no modulation, to remove DC or slow drift backgrounds

If the lab wants an extra control, first run the same lock-in pipeline on a
known magnetic or strain source to validate the instrumentation.

## Suggested scan points

The repo cannot justify calibrated amplitude numbers yet, so the protocol is
expressed as an ordering table rather than a quantitative prediction table.

Suggested scan classes:

- drive frequency: low, mid, high
- source-detector separation: near, mid, far

| scan class | standard null expectation | discriminator-design expectation (under cited retarded / wavefield proxy) |
| --- | --- | --- |
| low drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | weakest signal candidate; likely small or marginal |
| low drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | weak phase lag if any |
| mid drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | detectable `Y` is more plausible |
| mid drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | stronger phase lag or quadrature than near separation |
| high drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | stronger phase-sensitive response than low drive |
| high drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | strongest candidate for a coherent `Y` and phase ramp |

The qualitative ordering is the key claim of the discriminator design:

- under the cited retarded / wavefield proxy (and conditional on a
  future ideal-detector forward model): `Y` and `phi` should grow with
  drive frequency and separation
- standard null: `Y` stays near zero after calibration

Absolute amplitudes are **not** budgeted by this table.

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the `pi` reference control
- the phase is not flat across the image in widefield mode
- the effect strengthens in the high-drive / far-separation direction

## What would count as a miss

- quadrature vanishes after calibration
- the phase is flat across the field of view
- the signal moves only because of instrument lag, heating, or trivial
  amplitude rescaling

## Honest limitation

This repo does not yet provide a calibrated gravity amplitude for NV sensors.

So the strongest defensible lab-facing artifact is a discriminator protocol:

- ideal-detector forward model first
- phase-sensitive lock-in readout
- standard quasi-static null
- sign-flip control
- optional spatial phase-ramp imaging

## Experimental framing (scope-bounded)

The cleanest phrasing for a lab contact is:

"Measure the lock-in quadrature and spatial phase profile for a driven
source near an NV sensor. The standard quasi-static baseline predicts
no stable quadrature after calibration; under the cited retarded /
wavefield phase-ramp proxy (and conditional on a future ideal-detector
forward model), the discriminator protocol names a nonzero phase-lag
signature that strengthens with drive frequency and source-detector
separation as the qualitative ordering signal. Absolute detectability
is not budgeted by this protocol."

## References

- NV dual-channel lock-in readout of time-dependent fields:
  [Phys. Rev. B 88, 220410](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.88.220410)
- widefield / per-pixel lock-in detection in diamond NV imaging:
  [Scientific Reports 2022](https://www.nature.com/articles/s41598-022-12609-3)
- NV strain sensitivity in diamond mechanical structures:
  [Scientific Reports 2020](https://www.nature.com/articles/s41598-020-65049-2)

## Final Verdict (scope-bounded)

**Bounded experiment-facing discriminator protocol only.**

Conditional on the cited upstream retarded-field / wavefield authorities
(`retained_bounded` causality probe, `audited_conditional` delay proxy
and wavefield escalation), this row records:

- a discriminator protocol naming `X`, `Y`, `phi`, and the spatial
  phase profile;
- a qualitative ordering table for drive frequency × separation under
  the same single-delay / wave-like proxy;
- a minimal control stack and a pre-experiment validation step.

It is **not** a closed lab protocol, **not** a calibrated NV detectability
claim, and **not** a derivation of the cited upstream authorities. The
ideal-detector forward model and validated NV-coupling map remain open
as the single D-class theorem target for this row.

## Repair target

Per audit verdict (`notes_for_re_audit_if_any`): provide the
ideal-detector forward-model theorem deriving `X`, `Y`, `phi`, the
spatial phase ramp, and the frequency / separation ordering from the
retained retarded / wavefield lane or an explicitly retained upstream
note. The current note exposes only the qualitative ordering and the
discriminator protocol; the bridge theorem from cited retarded /
wavefield proxies to calibrated NV lock-in observables is the open
target.

## Repo-canonical vocabulary

Terminology used in this note matches the repo-canonical vocabulary:
"diamond NV", "phase ramp", "signal budget", "prediction", "protocol",
"lock-in quadrature `Y`", "phase lag `phi`", "spatial phase profile".
No new tags, no new classes, no parent-framing cross-references
implying a class, no status promotion language.
