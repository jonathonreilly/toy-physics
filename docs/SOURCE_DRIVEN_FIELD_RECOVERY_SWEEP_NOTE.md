# Source-Driven Field Recovery Sweep

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical observation on a runner-defined exact 3D
lattice family (`h = 0.5`, `W = 6`, `L = 30`, source strengths
`s in {0.001, 0.002, 0.004, 0.008}`) with a runner-selected damped
telegraph-style local field rule (parameters `c_field = 0.45`,
`damp = 0.35`) and a calibration sweep over `target max |f_dyn|` in
`{0.001, 0.002, 0.005, 0.010, 0.020, 0.040, 0.080}`. Frozen on disk.
**Status authority:** independent audit lane only.
**Claim scope:** at the declared family the runner reproduces (i)
`4/4 TOWARD` sign on every target-max row, (ii) dynamic `F~M`
exponents that decrease monotonically from `0.997` at
`target = 0.001` to `0.642` at `target = 0.080`, (iii) a conservative
pocket replay at `c_field = 0.40`, `damp = 0.35`, `target = 0.010`
with exact zero-source reduction (`+0.000000e+00`), dynamic
`F~M = 0.96`, and mean `|dyn/inst|` ratio `1.304`. The claim is
explicitly bounded to this declared parameter envelope; the telegraph
rule, its parameters, and the calibration targets are runner-selected,
not derived from A_min primitives.

## Audit boundary (2026-05-10)

The independent audit verdict on this row's most recent active hash is
`audited_conditional` (codex-gpt-5.5, fresh_context, 2026-05-10) with
`chain_closes: false`. The audit's `chain_closure_explanation` named
two issues:

1. "the runner delegates the lattice, field construction, propagation,
   constants, and power fit to an unprovided imported module
   (`scripts.minimal_source_driven_field_probe`)"
2. "the note also relies on a conservative pocket replay whose runner
   source and stdout are named but absent" — partial improvement
   since audit. As of 2026-05-10 the conservative pocket runner
   `scripts/source_driven_field_recovery_pocket.py` is present in the
   working tree; the runner reproduces the conservative pocket table
   on demand. The pocket log path
   `logs/2026-04-05-source-driven-field-recovery-pocket.txt` is no
   longer the live cache path; the runner cache lives at
   `logs/runner-cache/source_driven_field_recovery_sweep.txt`.

The audit also recorded `runner_check_breakdown:
{A:0, B:0, C:0, D:0, total_pass:0}` — the runner prints values without
explicit threshold checks, so the audit packet cannot verify the
load-bearing observables against tolerances.

The audit's `notes_for_re_audit_if_any` recorded a
`runner_artifact_issue` repair class: "Provide the imported probe
module and the conservative pocket runner/stdout, then rerun the audit
against a fully supplied computation with explicit threshold checks."

This 2026-05-10 rigorize pass selects the audit's repair target by:

1. **Citing the upstream foundational authority chain explicitly**
   so the audit packet can route through
   `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE` (the source note for the
   imported `Lattice3D` / `propagate` / `K` /
   `_source_driven_field_layers_raw` helpers); this addresses the "no
   one-hop authorities supplied" surface flagged by the audit.
2. **Adding hard-bar threshold assertions to the runner** so the
   load-bearing values (TOWARD count per row, dynamic `F~M` exponents,
   monotonic drift) are verified against explicit tolerances rather
   than only printed; assertion failure exits non-zero.
3. **Disclosing the runner-selected modeling inputs** (telegraph rule
   form, `c_field` / `damp` parameters, calibration targets) as tuned
   support, not derived from A_min primitives.
4. **Disclosing the conservative pocket runner** as a sibling
   companion artifact that is present in the working tree.

PATH A (deriving the telegraph rule, its parameters, and the
calibration target choice from retained framework primitives) is
theorem-level work and is deferred to future work as a separate
retained promotion.

## Hand-selected modeling inputs (NOT derived in this packet)

The following modeling inputs are runner-selected; they are NOT
derived from A_min primitives in this note:

- **Damped telegraph-style local field rule** with parameters
  `c_field = 0.45`, `damp = 0.35` for the broad sweep, and
  `c_field = 0.40`, `damp = 0.35` for the conservative pocket replay.
  There is no derivation of this update rule or its parameter values
  from accepted framework primitives.
- **Calibration target ladder** `target max |f_dyn| in {0.001, ..., 0.080}`
  for the broad sweep and `target = 0.010` for the conservative
  pocket. The choice of targets is a runner sweep design, not a
  derived coupling.
- **Source-strength ladder** `s in {0.001, 0.002, 0.004, 0.008}`
  inherited from the imported foundational module; the source
  geometry is the foundational module's static mass source.

## Cited live authority chain (audit-disclosed)

The runner imports `Lattice3D`, `propagate`, `K`, `H`, `NL_PHYS`,
`PW`, `C_FIELD`, `DAMP`, `SOURCE_STRENGTHS`, `SOURCE_Z`,
`_centroid_z`, `_source_driven_field_layers_raw`, `_scale_field_layers`,
`_field_abs_max`, and `_fit_power` from
`scripts/minimal_source_driven_field_probe.py` (source note
[`MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`](MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md)).
The runner-imported lattice/propagation primitives constitute the
foundational implementation surface for this bounded sweep; this
note's load-bearing observables (TOWARD count, `F~M` exponents,
monotonic drift) are computed via that imported infrastructure.

The current ledger statuses of the foundational and sibling notes are:

- [`docs/MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`](MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md)
  — foundational `Lattice3D` / `propagate` / `K` /
  `_source_driven_field_layers_raw` source authority (current
  ledger: `audit_status: unaudited`).
- [`docs/SOURCE_DRIVEN_FIELD_RECOVERY_H025_POCKET_NOTE.md`](SOURCE_DRIVEN_FIELD_RECOVERY_H025_POCKET_NOTE.md)
  — companion `h = 0.25` recovery pocket on a smaller family (current
  ledger: `effective_status: retained_bounded`).

The bounded inheritance for this note's load-bearing claim is the
runner-imported foundational surface above. The `audited_conditional`
status is maintained until either the `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE`
foundational authority is independently retained, or the runner is
made fully self-contained.

## Companion conservative pocket runner

The conservative pocket replay reported below is produced by the
sibling runner `scripts/source_driven_field_recovery_pocket.py`,
which is present in the working tree on 2026-05-10 and reproduces the
table in this note via direct execution. The pocket runner re-exposes
the foundational module's defaults but overrides
`C_FIELD = 0.40`, `DAMP = 0.35`, `TARGET_MAX = 0.01` and is otherwise
a thin replay of the broad-sweep architecture at one calibration row.

## Hard-bar runner assertions (2026-05-10)

The broad-sweep runner now enforces the following thresholds;
assertion failure exits non-zero (see
`scripts/source_driven_field_recovery_sweep.py`):

| Bar | Threshold | Frozen value |
| --- | --- | --- |
| TOWARD sign on every target-max row | every row has `4/4 TOWARD` | `7/7` rows pass |
| Weak-field linear recovery | dynamic `F~M >= 0.95` at `target <= 0.005` | `0.997, 0.994, 0.985` |
| Strong-calibration drift | dynamic `F~M < 0.80` at `target = 0.080` | `0.642` |
| Monotonic drift | `F~M(target_i)` non-increasing in `target_i` | monotone |
| All-row alpha sanity | every row has `0 < F~M < 1.05` | all in `(0.6, 1.05)` |

These assertions verify the load-bearing observables on the declared
sweep. They do not assert anything about size transfer, continuum
limit, or self-consistent field dynamics.

## Artifact chain

- [`scripts/source_driven_field_recovery_sweep.py`](../scripts/source_driven_field_recovery_sweep.py)
  (broad sweep)
- [`scripts/source_driven_field_recovery_pocket.py`](../scripts/source_driven_field_recovery_pocket.py)
  (conservative pocket replay)
- [`logs/runner-cache/source_driven_field_recovery_sweep.txt`](../logs/runner-cache/source_driven_field_recovery_sweep.txt)
- imported infrastructure:
  [`scripts/minimal_source_driven_field_probe.py`](../scripts/minimal_source_driven_field_probe.py)
  (`Lattice3D`, `propagate`, `K`, `H`, `NL_PHYS`, `PW`, `C_FIELD`,
  `DAMP`, `SOURCE_STRENGTHS`, `_centroid_z`,
  `_source_driven_field_layers_raw`, `_scale_field_layers`,
  `_field_abs_max`, `_fit_power`).

## Question

Does the same minimal source-driven local-field architecture recover the weak-field
mass-scaling lane when the generated field is kept genuinely small, rather than
calibrated to the stronger `max |f_dyn| = 0.08` row used in the first probe?

## Frozen result

Broad sweep on the exact 3D lattice (`h = 0.5`, `W = 6`, `L = 30`):

| target `max |f_dyn|` | `TOWARD` | dynamic `F~M` | largest dynamic shift |
| ---: | ---: | ---: | ---: |
| `0.001` | `4/4` | `0.997` | `+3.180396e-03` |
| `0.002` | `4/4` | `0.994` | `+6.314115e-03` |
| `0.005` | `4/4` | `0.985` | `+1.543423e-02` |
| `0.010` | `4/4` | `0.968` | `+2.969381e-02` |
| `0.020` | `4/4` | `0.934` | `+5.468048e-02` |
| `0.040` | `4/4` | `0.855` | `+9.073752e-02` |
| `0.080` | `4/4` | `0.642` | `+1.105259e-01` |

Conservative pocket replay:

- `c_field = 0.40`, `damp = 0.35`, `target = 0.010`
- zero-source dynamic shift: `+0.000000e+00`
- dynamic `F~M = 0.96`
- `4/4` dynamic rows stay `TOWARD`
- mean `|dyn/inst|` ratio: `1.304`

Dynamic pocket shifts:

- `+3.601586e-03`
- `+7.129776e-03`
- `+1.396546e-02`
- `+2.675231e-02`

## Safe read

The strongest bounded numerical statement on the declared scope is:

- the runner-defined damped-telegraph architecture preserves
  `4/4 TOWARD` on every calibration row in the swept ladder
- in the small-field pocket (`target <= 0.005`), the dynamic `F~M`
  exponent stays at or above `0.985` (essentially linear)
- as `target` increases the dynamic `F~M` exponent monotonically
  decreases, dropping to `0.642` at `target = 0.080`
- the conservative pocket replay reproduces zero-source reduction
  exactly and preserves dynamic `F~M = 0.96` on a four-row mass ladder

## Honest limitation

This is a runner-defined bounded numerical observation on the
declared parameter envelope, not a derivation of a self-consistent
field theory from A_min primitives.

- the telegraph-style update rule and its parameters
  (`c_field = 0.45`, `damp = 0.35` for the broad sweep,
  `c_field = 0.40`, `damp = 0.35` for the pocket replay) are
  runner-selected, not derived from accepted framework primitives
- the calibration target ladder is runner-designed, not derived
- the foundational lattice/propagation infrastructure
  (`Lattice3D`, `propagate`, `K`, etc.) is imported from
  `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE`, whose ledger status is
  currently `unaudited`
- the strong-calibration drift (`F~M = 0.642` at `target = 0.080`)
  is itself recorded as a calibration-sensitivity finding, not a
  derived strong-field threshold

## Branch verdict

The runner-defined harness produces a **bounded numerical observation**
on the declared parameter envelope:

- the source-driven architecture has a real weak-field recovery
  pocket on the declared sweep
- in that pocket, `TOWARD` survives (`4/4`) and the dynamic mass
  exponent stays near linear (`>= 0.985`) at `target <= 0.005`
- the same architecture drifts away from linear mass scaling as the
  generated field grows, dropping to `F~M = 0.642` at `target = 0.080`

The broader "self-consistent field dynamics is calibration-sensitive
not dead" reading is recorded only as a cross-reference; the
telegraph rule and its parameters are runner-selected, the
foundational infrastructure import is currently `unaudited`, and the
bounded observation does not promote the source-driven channel to a
retained field-theoretic theorem. PATH A (deriving the telegraph
rule, its parameters, and the calibration ladder from retained
framework dynamics) is deferred to future work as a separate retained
promotion.
