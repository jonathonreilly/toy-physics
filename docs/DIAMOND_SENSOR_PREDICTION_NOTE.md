# Diamond Sensor Prediction Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded experiment-facing discriminator design, intentionally
bounded; **not** a closed lab prediction.
**Status authority:** independent audit lane only.
**Authority role:** records, but does not close, a bounded discriminator
design (lock-in `X`, `Y`, `phi`, widefield phase ramp) for a diamond/NV
setup, conditional on cited upstream retarded-field / wavefield notes.
Names the missing NV ideal-detector forward-model bridge theorem as the
single open theorem target for a closed prediction.

## Purpose

This note turns the cited phase-sensitive / retarded / wavefield lane
notes into one lab-facing **discriminator design** for a diamond/NV
sensor setup.

The goal is **not** a generic force claim and **not** a closed
quantitative prediction.
The goal is one observable that a diamond lock-in microscope can in
principle measure, one standard-physics null, and one minimal control
set, with the explicit limitation that the NV ideal-detector forward
model and absolute amplitude budget are still missing.

## Audit boundary

This note assembles a class-B experiment-facing discriminator card by
importing upstream retarded-field / wavefield phase-ramp authorities
and naming the corresponding lock-in observables (`X`, `Y`,
`phi = atan2(Y, X)`, `R`, widefield phase profile). It is **not** a
derivation of those upstream phase-ramp results and **not** a closed
NV-coupling forward model.

**Cited authorities (one-hop deps; cited but not closed in this note):**

- [`docs/RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md`](RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`)
  — supplies the bounded retarded-field causality probe used as the
  qualitative motivation for a finite-delay phase-lag signature.
- [`docs/RETARDED_FIELD_DELAY_PROXY_NOTE.md`](RETARDED_FIELD_DELAY_PROXY_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — supplies the bounded intermediate-layer phase-lag proxy (`mix`
  parameter, single phase-lag observable). Cited as motivation for the
  toy `phi = atan(omega*tau)` scaling; itself not retained-grade.
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: audited_conditional`)
  — supplies the bounded exact-lattice wavefield escalation that motivates
  the spatial phase-ramp readout. Cited as proxy-level motivation; not a
  retained NV-coupling theorem.

**In-note class-B content (what survives at this scope):**

- a discriminator design naming the lock-in observables `X`, `Y`,
  `phi`, `R`, and the widefield spatial phase profile;
- a qualitative ordering: standard quasi-static null gives `Y ~ 0`,
  `phi ~ 0`, flat phase, while a finite-delay / wave-like coupling
  gives `Y != 0`, `phi != 0`, and a coherent spatial phase ramp that
  strengthens with drive frequency and source-detector separation;
- the toy scaling law `Y/X ~ omega*tau`, `phi = atan(omega*tau)`
  reported by `scripts/diamond_sensor_prediction_probe.py`, which is a
  class-A consequence of treating a fixed effective delay `tau` as the
  single retarded-coupling parameter (not derived from an NV
  Hamiltonian);
- a minimal control list (drive off; source retracted; `pi` reference
  flip; static-source baseline) and a pre-experiment validation step
  (run the same lock-in pipeline on a known magnetic or strain source
  first).

These are class-B / class-A consequences of the cited upstream phase-
ramp authorities and a single-delay toy model; they are **not** a
derivation of the NV ideal-detector forward model and **not** a
calibrated signal budget.

**Admitted-context derivation gap (real, not import-redirect):**

The note **does not** derive any of:

1. an ideal-detector forward model mapping a driven source trajectory
   through an NV Hamiltonian to lock-in observables `X`, `Y`, `phi`,
   `R`, and a widefield spatial phase profile (perfect phase reference,
   no technical noise, no bandwidth or integration limits);
2. a validated mapping from the cited retained / conditional wavefield
   proxy to a real NV sensor coupling strength;
3. a calibrated absolute signal budget for a specific NV lab geometry
   that would convert the qualitative ordering into a detectability
   claim.

The note explicitly labels (1) as "Requirement: ideal detector first"
and (2)-(3) as "Honest limitation". This is a **real D-class derivation
gap**, not a dependency-citation issue. No retained, bounded, or
proposed theorem on the current atlas closes (1)-(3) for this row.

## Why a lock-in interface is the right scope (not an absolute claim)

The NV literature already supports the relevant readout style:

- phase-sensitive lock-in readout of time-dependent fields in diamond NV
  magnetometry
- widefield / pixel-wise lock-in detection
- NV sensitivity to strain in diamond mechanical structures

That makes a lock-in quadrature or phase-ramp **discriminator design** a
better lab-facing scope than an absolute gravitational-force claim,
which is **not** budgeted by this repo.

The cited phase-sensitive infrastructure (status disclosed above):

- [`docs/RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md`](RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md)
- [`docs/RETARDED_FIELD_DELAY_PROXY_NOTE.md`](RETARDED_FIELD_DELAY_PROXY_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)

## Concrete discriminator design (scope-bounded; not a closed prediction)

Conditional on the cited upstream retarded-field / wavefield notes
above, the smallest defensible experiment-facing **discriminator design**
is:

- a driven-source NV lock-in readout should show a nonzero quadrature channel
  `Y` or a nonzero phase lag `phi = atan2(Y, X)` if the coupling is genuinely
  retarded / wave-like
- the same readout should remain phase-null after calibration in the
  standard instantaneous / quasi-static baseline
- in a widefield geometry, the phase should not just shift globally; it
  should form a coherent spatial phase ramp across the NV image if the
  wavefield lane is the right effective description

The direct null is:

- after phase calibration and static-background subtraction, standard
  Newtonian / quasi-static coupling predicts `Y ≈ 0` and no stable spatial
  phase ramp

The discriminator-design expectation, conditional on the cited retarded /
wavefield authorities above and on a future ideal-detector forward
model (still missing), is:

- finite propagation or wave-scheduling should produce a measurable
  phase-lag / quadrature component
- that quadrature should strengthen as the drive frequency rises and as the
  source-detector separation increases
- in an imaging readout, the phase slope across the field of view should be
  the cleanest discriminator, not raw amplitude

This is the **qualitative ordering** the discriminator card is built
around. It is **not** a calibrated NV detectability claim, since neither
the ideal-detector forward model nor the validated NV-coupling map is
closed in this note.

## Requirement: ideal detector first

Before adding any NV-specific sensitivity, noise floor, spectral artefact,
or lock-in implementation detail, the card must include an
**ideal-detector forward model**:

- perfect phase reference
- no technical noise
- no bandwidth or integration limits
- direct predicted outputs for `X`, `Y`, `R`, and `phi`

The source-fidelity check comes before detector realism:

- verify that the simulated source trajectory is the intended one
- verify that retarded and instantaneous comparators use the same source history
- only then add instrument-specific filtering or noise

This keeps the experiment card honest: physics prediction first,
instrument model second.

## Minimal control set

The smallest useful control set is:

1. drive off
2. same drive with the source removed or retracted far enough that the
   coupling should be negligible
3. same drive with a `pi` phase flip in the reference channel, to check that
   the extracted quadrature really changes sign
4. static source / no modulation, to remove any DC or slow drift background

If the lab wants a stronger control, the same protocol can be run first on a
known magnetic or strain source to verify the lock-in pipeline before trying
the weaker gravity-facing interpretation.

## Honest limitation

This repo does **not** yet give a defensible absolute gravity amplitude for an
NV lab.

So the claim surface should stay narrow:

- phase-quadrature discriminator: yes
- coherent spatial phase ramp: yes
- absolute gravity detectability: not yet budgeted here
- ideal-detector forward model: required before any lab-specific noise claim

That is the smallest prediction still worth taking to a diamond lab.

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the reference `pi` control
- a widefield sensor image shows a stable nonzero phase gradient
- the effect strengthens with frequency / separation in the expected causal
  direction

## What would count as a miss

- quadrature vanishes after calibration
- the phase is flat across the image
- the signal moves only because of instrument lag, heating, or a trivial
  amplitude rescaling

## Experimental framing (scope-bounded)

If this discriminator design is sent to a diamond/NV lab, the cleanest
phrasing is:

"Measure the lock-in quadrature and spatial phase ramp for a driven
source near an NV sensor. The standard quasi-static baseline predicts
no stable quadrature after calibration; under the cited retarded /
wavefield phase-ramp proxy (and conditional on a future ideal-detector
forward model), the discriminator design names a nonzero phase-lag
signature as the qualitative ordering signal. Absolute detectability
is not budgeted by this note."

## References that motivate the readout choice

- NV dual-channel lock-in readout of time-dependent fields:
  [Phys. Rev. B 88, 220410](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.88.220410)
- widefield / per-pixel lock-in detection in diamond NV imaging:
  [Scientific Reports 2022](https://www.nature.com/articles/s41598-022-12609-3)
- NV strain sensitivity in diamond mechanical structures:
  [Scientific Reports 2020](https://www.nature.com/articles/s41598-020-65049-2)

## Final Verdict (scope-bounded)

**Bounded experiment-facing discriminator design only.**

Conditional on the cited upstream retarded-field / wavefield authorities
(`retained_bounded` causality probe, `audited_conditional` delay proxy
and wavefield escalation), this row records:

- a discriminator design naming `X`, `Y`, `phi`, `R`, and the spatial
  phase profile;
- a qualitative `phi = atan(omega*tau)` toy scaling under a single-delay
  proxy (class-A consequence; not derived from an NV Hamiltonian);
- a minimal control list and a pre-experiment validation step.

It is **not** a closed lab prediction, **not** a calibrated NV detectability
claim, and **not** a derivation of the cited upstream authorities. The
ideal-detector forward model and validated NV-coupling map remain open
as the single D-class theorem target for this row.

## Repair target

Per audit verdict (`notes_for_re_audit_if_any`): retain or repair the
delay-proxy and wavefield dependencies, then add the cheapest explicit
ideal-detector forward-model theorem mapping a driven source trajectory
to `X`, `Y`, `R`, and `phi` for the NV readout geometry. The current
note exposes only the qualitative ordering and the discriminator
design; the bridge theorem from cited retarded / wavefield proxies to
calibrated NV lock-in observables is the open target.

## Repo-canonical vocabulary

Terminology used in this note matches the repo-canonical vocabulary:
"diamond NV", "phase ramp", "signal budget", "prediction", "protocol",
"lock-in quadrature `Y`", "phase lag `phi`", "spatial phase profile".
No new tags, no new classes, no parent-framing cross-references
implying a class, no status promotion language.
