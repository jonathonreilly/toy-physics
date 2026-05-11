# Source-Resolved Exact Green Pocket

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical observation on a runner-defined small exact
lattice family (`h = 0.5`, `W = 3`, `L = 20`, boundary-clipped cross5
source cluster with 4 in-bounds nodes, source strengths
`s in {0.001, 0.002, 0.004, 0.008}`) with a hand-selected Green-like
kernel `exp(-mu r)/(r + eps)` at `mu = 0.08`, `eps = 0.5`, and an
explicitly calibrated gain `2.131774e+00`. Frozen on disk.
**Status authority:** independent audit lane only.
**Claim scope:** at the declared family the runner reproduces (i) exact
zero-source reduction (`+0.000000e+00`), (ii) `4/4 TOWARD` sign on the
Green-kernel channel, (iii) Green-kernel `F~M` exponent `1.00`
(near-linear), and (iv) mean `|green/inst|` ratio `1.235`. The claim
is explicitly bounded to this declared parameter envelope; the
Green-kernel choice and the calibration gain are runner-selected, not
derived from the physical `Cl(3)` local algebra / `Z^3` spatial
substrate baseline.

## Audit boundary (2026-05-10)

The independent audit verdict on this row's prior active hash was
`audited_conditional` (codex-gpt-5.5, fresh_context, 2026-05-10) with
`chain_closes: false`. The audit's `chain_closure_explanation` named
two issues:

1. "the runner delegates the exact-lattice construction, propagation
   rule, centroid readout, K, source constants, and instantaneous
   comparator to `scripts.minimal_source_driven_field_probe`, whose
   source is not included and is not a cited authority. With no
   one-hop authorities supplied, those load-bearing definitions are
   outside the restricted packet."
2. The `runner_check_breakdown` was `{A:0, B:0, C:0, D:0, total_pass:0}`
   — the runner prints values without explicit threshold checks, so
   the audit packet cannot verify the load-bearing observables against
   tolerances.

The audit's `notes_for_re_audit_if_any` recorded a
`runner_artifact_issue` repair class with the cheapest next action:
"Include `scripts/minimal_source_driven_field_probe.py` or a
self-contained reduced runner exposing `Lattice3D`, `propagate`, `K`,
source constants, centroid readout, and instantaneous comparator,
then rerun and re-audit the bounded pocket."

This 2026-05-10 rigorize pass selects the audit's repair target by:

1. **Citing the upstream foundational authority chain explicitly** so
   the audit packet can route through `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE`
   (the source note for the imported `Lattice3D` / `propagate` / `K`
   helpers); this addresses the "no one-hop authorities supplied"
   surface flagged by the audit.
2. **Adding hard-bar threshold assertions to the runner** so the
   load-bearing values (zero-source reduction, TOWARD sign, `F~M`
   exponent, mean ratio) are verified against explicit tolerances
   rather than only printed; assertion failure exits non-zero.
3. **Disclosing the runner-selected modeling inputs** (Green kernel
   form and parameters, calibration gain) as tuned support, not
   derived from the repo baseline.

PATH A (deriving the Green-kernel form and calibration gain from
retained repo dynamics) is theorem-level work and is deferred
to future work as a separate retained promotion.

## Hand-selected modeling inputs (NOT derived in this packet)

The following modeling inputs are runner-selected; they are NOT
derived from the physical `Cl(3)` local algebra / `Z^3` spatial
substrate baseline in this note:

- **Green-like kernel form** `exp(-mu r) / (r + eps)` with parameters
  `mu = 0.08`, `eps = 0.5`. There is no derivation of this kernel
  shape or its parameter values from accepted framework primitives.
- **Calibration gain** `gain = FIELD_TARGET_MAX / max|f_ref|`
  evaluating to `2.131774e+00` on this family, which sets the absolute
  amplitude of the Green-kernel field. The gain is a runner-tuned
  normalization, not a derived coupling. The strong observables that
  survive the gain choice are dimensionless (sign, `F~M` exponent,
  ratio class), but the absolute deflection magnitudes do not.
- **Source cluster geometry** — the boundary-clipped cross5 cluster
  is a runner-selected discrete source pattern, not a derived
  symmetric mass distribution.

## Cited live authority chain (audit-disclosed)

The runner imports `Lattice3D`, `propagate`, `K`, `SOURCE_Z`,
`SOURCE_STRENGTHS`, `_centroid_z`, `_instantaneous_field_layers`, and
`_fit_power` from `scripts/minimal_source_driven_field_probe.py`
(source note [`MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`](MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md)).
The runner-imported lattice/propagation primitives constitute the
foundational implementation surface for this bounded pocket; this
note's load-bearing observables (zero-source reduction, TOWARD sign,
`F~M` exponent) are computed via that imported infrastructure.

The current ledger statuses of the foundational and sibling notes are:

- [`docs/MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`](MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md)
  — foundational `Lattice3D` / `propagate` / `K` source authority
  (current ledger: `audit_status: unaudited`).
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_H025_POCKET_NOTE.md`](SOURCE_RESOLVED_EXACT_GREEN_H025_POCKET_NOTE.md)
  — companion `h = 0.25` Green pocket on a smaller family (current
  ledger: `audit_status: unaudited`).
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md`](SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md)
  — companion scaling note (current ledger: `audit_status: unaudited`).
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`](SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md)
  — downstream self-consistent extension (current ledger:
  `effective_status: retained_bounded`).
- [`docs/SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`](SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md)
  — downstream propagating-Green sibling (current ledger:
  `audit_status: unaudited`).

The bounded inheritance for this note's load-bearing claim is the
runner-imported foundational surface above. This landing adds hard-bar
runner assertions and explicit one-hop authority links, but it does not
mark the claim clean; the row should remain queued for independent
re-audit until either `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE` is
independently retained or the runner is made fully self-contained.

## Hard-bar runner assertions (2026-05-10)

The runner now enforces the following thresholds; assertion failure
exits non-zero (see `scripts/source_resolved_exact_green_pocket.py`):

| Bar | Threshold | Frozen value |
| --- | --- | --- |
| zero-source reduction | `\|zero_delta\| <= 1e-12` | `+0.000000e+00` |
| TOWARD sign | `4/4` rows have `green_delta > 0` | `4/4` |
| Green `F~M` exponent | `0.95 <= alpha_green <= 1.05` | `1.00` |
| Mean `|green/inst|` ratio | `1.10 <= mean_ratio <= 1.40` | `1.235` |
| Calibration gain finiteness | `0 < gain < 100` | `2.131774e+00` |

These assertions verify the load-bearing observables on the declared
family. They do not assert anything about size transfer, continuum
limit, or self-consistent field dynamics.

## Artifact chain

- [`scripts/source_resolved_exact_green_pocket.py`](../scripts/source_resolved_exact_green_pocket.py)
- [`logs/runner-cache/source_resolved_exact_green_pocket.txt`](../logs/runner-cache/source_resolved_exact_green_pocket.txt)
- imported infrastructure:
  [`scripts/minimal_source_driven_field_probe.py`](../scripts/minimal_source_driven_field_probe.py)
  (`Lattice3D`, `propagate`, `K`, `SOURCE_Z`, `SOURCE_STRENGTHS`,
  `_centroid_z`, `_instantaneous_field_layers`, `_fit_power`).

## Question

Can a source-resolved Green-like field on an exact lattice, built from a
fixed source cluster rather than a telegraph recurrence or edge-carried
transport, preserve the weak-field gravity lane on the retained source
strength ladder?

This note is intentionally narrow:

- one exact lattice family, kept small enough for a fast feasibility check
- one source-resolved Green-like kernel
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source must recover free propagation exactly

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.5`, `W = 3`, `L = 20`
- fixed cross5 source cluster clipped at the boundary, leaving 4 in-bounds source nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- calibration gain `2.131774e+00`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | Green-kernel deflection | ratio | max `|f|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.713544e-03` | `+2.139974e-03` | `1.249` | `2.5e-03` |
| `0.0020` | `+3.440703e-03` | `+4.279368e-03` | `1.244` | `5.0e-03` |
| `0.0040` | `+6.936763e-03` | `+8.557987e-03` | `1.234` | `1.0e-02` |
| `0.0080` | `+1.410179e-02` | `+1.712572e-02` | `1.214` | `2.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `1.01`
- Green-kernel `F~M`: `1.00`

## Safe read

The strongest bounded numerical statement on the declared scope is:

- exact zero-source reduction holds (`+0.000000e+00`, machine-precision)
- the Green-kernel field keeps the `TOWARD` sign on `4/4` rows of the
  retained source ladder
- the Green-kernel mass-scaling exponent is `1.00` (essentially linear
  on the four-row ladder)
- the dynamic field remains nontrivial, with mean `|green/inst| = 1.235`

## Honest limitation

This is a runner-defined bounded numerical observation on the declared
parameter envelope, not a derivation of a Green-field theorem from
the repo baseline.

- the exact lattice here is intentionally small (`h = 0.5`, `W = 3`,
  `L = 20`); no size-transfer or continuum claim is made
- the architecture is source-resolved and linear; this is not a
  self-consistent dynamical field equation
- the source cluster is boundary-clipped (4 in-bounds of cross5
  template) rather than fully symmetric, so this is a bounded pocket
  control, not a clean geometric refinement proof
- the Green kernel form `exp(-mu r) / (r + eps)` and parameters
  `mu = 0.08`, `eps = 0.5` are runner-selected, not derived
- the calibration gain `2.131774e+00` is runner-tuned to a chosen
  `FIELD_TARGET_MAX = 0.02`, not a derived coupling
- the foundational lattice/propagation infrastructure
  (`Lattice3D`, `propagate`, `K`, etc.) is imported from
  `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE` whose ledger status is
  currently `unaudited`

## Branch verdict

The runner-defined harness produces a **bounded numerical observation**
on the declared parameter envelope:

- exact zero-source reduction survives on the declared family
- the Green-kernel sign stays `TOWARD` (`4/4`) at the chosen `s` values
- the Green-kernel `F~M` exponent stays at `1.00` on the four-row ladder
- the mean `|green/inst|` ratio is `1.235` on the declared scope

The broader "exact-lattice self-generated field candidate" reading is
recorded only as a cross-reference; the Green kernel and the
calibration gain are runner-selected, the foundational infrastructure
import is currently `unaudited`, and the bounded observation does not
promote the source-resolved Green channel to a retained field-theoretic
theorem. PATH A (deriving the Green-kernel form, parameters, and
calibration gain from retained framework dynamics) is deferred to
future work as a separate retained promotion.
