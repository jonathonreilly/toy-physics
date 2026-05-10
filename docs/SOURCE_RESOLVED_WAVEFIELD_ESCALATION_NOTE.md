# Source-Resolved Wavefield Escalation

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical observation on a runner-defined larger exact
lattice family (`h = 0.25`, `W = 4`, `L = 8`, source cluster of 5
in-bounds nodes at `source_z = 2.5`, source strengths
`s in {0.001, 0.002, 0.004, 0.008}`) with a hand-selected finite-speed
wavefield update rule and tuned wavefield parameters. Frozen on disk.
**Status authority:** independent audit lane only.
**Claim scope:** at the declared family the runner reproduces (i) exact
zero-source reduction (`+0.000000e+00`), (ii) `4/4 TOWARD` sign on
the wavefield channel, (iii) wavefield `F~M` exponent `~ 0.98` (near-
linear), and (iv) a coherent detector-line phase ramp with mean `R²`
`~ 0.96` and multi-radian span. The claim is explicitly bounded to
this declared parameter envelope; the wavefield update rule and its
parameters are runner-selected, not derived from A_min primitives.

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`
with `chain_closes: false`. The audit's `chain_closure_explanation`
named three issues:

1. "the finite-speed wavefield rule and parameters are selected
   rather than derived" — real; explicitly disclosed below
2. "its compact-pocket parent is unaudited" — partial improvement
   since audit. As of 2026-05-10 the four cited upstream Green-pocket
   / source-driven probes are all `audited_clean` with effective
   `retained_bounded`; the bounded inheritance is now from
   `retained_bounded` parents, not unaudited parents
3. "the table's `wave/same` column is actually `wave/instantaneous`" —
   real; the source script computes
   `wave_ratio = abs(wave_delta / inst_delta)` (see line 297 of
   `scripts/source_resolved_wavefield_escalation.py`). The header
   label `wave/same` was a misprint; the displayed quantity is
   `|wave/instantaneous|`. The frozen-table column header below has
   been corrected accordingly.

This 2026-05-10 rigorize pass selects **PATH B**: scope the load-
bearing claim to the bounded numerical observation on the declared
parameter envelope, explicitly disclose the runner-selected wavefield
rule and parameters as tuned support (not derived from A_min
primitives), correct the `wave/same` column label to `wave/inst` to
match the underlying quantity, and disclose the upstream parent
statuses. PATH A (deriving the finite-speed wavefield rule and its
parameters from retained dynamics) is deferred to future work as a
separate retained promotion.

## Hand-selected modeling inputs (NOT derived in this packet)

The following modeling inputs are runner-selected; they are NOT
derived from A_min primitives in this note:

- **Finite-speed wavefield update rule** with parameters
  `wave_lag_blend = 0.72`, `wave_speed2 = 0.16`, `damp = 0.18`,
  `source_blend = 0.52`. There is no derivation of this update rule
  or its parameter values from accepted framework primitives. They
  are tuned to produce the exact zero-source reduction and the
  observed phase-ramp behavior on the declared family.
- **Same-site memory mix** `mix = 0.9` and **kernel** parameters
  `mu = 0.08`, `eps = 0.5` — likewise tuned, not derived.

## Upstream one-hop dependencies (audit-disclosed)

The four upstream rows cited by the audit are all currently
`audited_clean` with effective `retained_bounded`:

- [`docs/SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md)
  (`audit_status: audited_clean`, `effective_status: retained_bounded`).
- [`docs/SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`](SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md)
  (`audit_status: audited_clean`, `effective_status: retained_bounded`).
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`](SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md)
  (`audit_status: audited_clean`, `effective_status: retained_bounded`).
- [`docs/MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`](MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md)
  (`audit_status: audited_clean`, `effective_status: retained_bounded`).

The bounded numerical observation in this note inherits a `bounded`
grade from these `retained_bounded` parents and from the runner-
selected modeling inputs above; the `audited_conditional` status is
maintained until the wavefield rule and parameters are derived (PATH A).

## Artifact chain

- [`scripts/source_resolved_wavefield_escalation.py`](../scripts/source_resolved_wavefield_escalation.py)
- [`logs/2026-04-05-source-resolved-wavefield-escalation.txt`](../logs/2026-04-05-source-resolved-wavefield-escalation.txt)

## Question

Can the exact-lattice wavefield lane be pushed beyond the compact pocket by
moving to a larger exact family and using a cleaner wave-like observable than a
single phase lag?

This probe stays narrow:

- one larger exact lattice family at `h = 0.25`
- one exact zero-source reduction check
- one instantaneous `1/r` control
- one same-site-memory control
- one finite-speed wavefield candidate
- one weak-field sign / `F~M` gate
- one wave-like observable: detector-line phase-ramp slope and span relative
  to the same-site control

## Frozen result

The frozen larger exact family uses:

- `h = 0.25`
- `W = 4`
- `L = 8`
- source cluster with `5` in-bounds nodes
- `source_z = 2.5`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- same-site memory `mix = 0.9`
- wavefield update parameters:
  - `wave_lag_blend = 0.72`
  - `wave_speed2 = 0.16`
  - `damp = 0.18`
  - `source_blend = 0.52`

Reduction check:

- zero-source same-site shift: `+0.000000e+00`
- zero-source wavefield shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | same-site deflection | wavefield deflection | phase lag (rad) | ramp slope (rad / z) | ramp R² | `\|wave/inst\|` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.931018e-03` | `+3.658426e-03` | `+1.759245e-01` | `-0.740` | `-0.1215` | `0.959` | `60.022` |
| `0.0020` | `+5.873223e-03` | `+7.321503e-03` | `+3.559416e-01` | `-1.473` | `-0.2444` | `0.959` | `60.604` |
| `0.0040` | `+1.179000e-02` | `+1.466136e-02` | `+7.157359e-01` | `-2.880` | `-0.4925` | `0.960` | `60.707` |
| `0.0080` | `+2.374397e-02` | `+2.939408e-02` | `+1.326988e+00` | `+0.337` | `-1.0274` | `0.966` | `55.887` |

Fitted exponents:

- instantaneous `F~M`: `1.01`
- same-site-memory `F~M`: `1.00`
- wavefield `F~M`: `0.98`

## Safe read

The strongest bounded numerical statement on the declared scope is:

- exact zero-source reduction survives on the declared family
- the wavefield-channel sign stays `TOWARD` (`4/4`) at the chosen `s` values
- the runner-fitted mass-scaling exponents are `1.01` (instantaneous),
  `1.00` (same-site memory), and `0.98` (wavefield) on the declared `s` values
- the runner-computed detector-line phase ramp has mean `R²` `~ 0.96`
  and multi-radian span on the declared parameter envelope
- the displayed ratio in the rightmost column is `|wave/inst|` `~ 60`
  (corrected from the earlier "wave/same" misprint per audit)

## Honest limitation

This is a runner-defined bounded numerical observation on the
declared parameter envelope, not a derivation of a causal-field
theory or a continuum closure.

- the wavefield update rule and its parameters
  (`wave_lag_blend = 0.72`, `wave_speed2 = 0.16`, `damp = 0.18`,
  `source_blend = 0.52`, `mix = 0.9`, `mu = 0.08`, `eps = 0.5`)
  are runner-selected, not derived from A_min primitives
- the detector-line phase-ramp readout is a runner-defined proxy
  observable, not a derivation of a wave-equation observable from
  retained dynamics
- the result is an exact-lattice bounded observation, not a
  generated-geometry transfer or a continuum theorem

## Branch verdict

The runner-defined harness produces a **bounded numerical observation**
on the declared parameter envelope:

- exact zero-source reduction survives on the declared family
- the wavefield-channel sign stays `TOWARD` (`4/4`) at the chosen `s` values
- the wavefield `F~M` exponent remains near `1.00` (specifically `0.98`)
- the detector-line phase-ramp readout has mean `R²` `~ 0.96` and
  multi-radian span on the declared scope
- the displayed `|wave/inst|` ratio is `~ 60`, not a "wave/same"
  comparison (corrected per audit)

The broader "exact-lattice wavefield step" reading is recorded only as
a cross-reference; the wavefield rule and its parameters are runner-
selected and not derived from A_min primitives, so the bounded
observation does not promote the wavefield channel to a retained
field-theoretic theorem. PATH A (deriving the wavefield rule and
parameters from retained dynamics) is deferred to future work as a
separate retained promotion.
