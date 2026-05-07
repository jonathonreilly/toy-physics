# Newton Derivation Top4 Bridge Note (Principle 3 conditional bridge)

**Date:** 2026-05-07
**Status:** support / bounded conditional bridge note. This note does not promote `newton_derivation_note` and does not assert a new persistent-pattern equivalence-principle theorem. It only registers the bridge that the audit-clean `persistent_object_top4_multistage_transfer_sweep` floor *operationally satisfies the Principle-3 extensivity premise* of the Newton-derivation conditional theorem on its own bounded multistage-compact-object scope.

## Purpose

The open gate `newton_derivation_note` carries the conditional theorem:

> on the retained ordered-lattice family, if the propagator is linear,
> the action creates a phase valley, the inertial quantity is extensive
> under the same composition law as the field-source parameter `s`,
> and momentum is conserved, then `p = 1` is selected and the
> Newtonian mass-scaling law follows on that family.

The auditor's load-bearing step is Principle 3:

> If the inertial quantity of a persistent pattern is an extensive
> quantity attached to the same composition law as the field-source
> parameter `s`, then `m proportional to s`.

Until 2026-04-16 the live machinery only exercised this premise on
test-particle / free-packet families. Two intervening artifacts now
exist that change the local picture:

- `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16`
  (audit-clean, retained_bounded) registered an exact-lattice multistage
  compact object floor that survives 11/13 widened-pocket cases under
  fixed admissibility gates including overlap, F~M alpha band, and
  kappa drift.
- `matter_inertial_closure_note` (audit-clean, retained_no_go) registered
  the negative result that free Gaussian packets do *not* satisfy a
  generator-invariant inertial mass, so the equivalence-principle reading
  remains blocked for that object family.

This bridge note records the precise observation that closes the
*Principle-3 sub-step* of the Newton-derivation conditional theorem on
the multistage compact-object family without claiming the persistent-pattern
equivalence-principle theorem itself.

## Conditional bridge claim

On the audit-clean `top4` multistage compact-object family
(`h = 0.25`, `blend = 0.25`, `top_keep = 4`, three updates per segment,
three chained segments), the Principle-3 extensivity premise of the
Newton-derivation chain is *operationally satisfied* by the same machinery
that already produced the audit-clean transfer-sweep floor:

1. **Persistence.** The persistent compact pattern survives the chained
   multistage updates with `stage_mean_overlap >= 0.90` (e.g. baseline
   row reports `[0.956, 0.956, 0.956]`).

2. **Extensivity in `s`.** The response exponent across SOURCE_STRENGTHS
   ` = [0.001, 0.002, 0.004, 0.008]` reads `stage_alpha in [0.95, 1.05]`
   on every admissible widened-pocket case. On the baseline row this is
   `[1.03, 1.03, 1.03]`. Reading the chain in the Newton-derivation
   direction, this is exactly the statement that `delta proportional to s`
   on a persistent pattern, i.e. that the response is linear in the
   single source-strength parameter `s` that also drives the field.

3. **Stage-to-stage stability of the response coefficient.** The
   maximum stage-to-stage drift of `kappa = delta / s` is
   `max_kappa_drift = 0.000%` on the baseline row. The same `s` that
   indexes the source strength continues to index the response across
   the chained multistage segments; there is no second scalar parameter.

The Principle-3 premise of the Newton-derivation chain is

> the inertial quantity of a persistent pattern is an extensive
> quantity attached to the same composition law as the field-source
> parameter `s`.

Operationally, on the multistage compact-object family this means:

> the same scalar `s` controls (i) the source-driven field, (ii) the
> linear response of the persistent pattern with stable coefficient,
> and (iii) the persistence of the pattern itself across chained
> stages.

All three are read directly off the audit-clean `top4` floor with no
additional inputs. The bridge therefore satisfies the Newton-derivation
conditional's Principle-3 premise *as a definitional identification*
on that family: the parameter `s` is the unique scalar whose extensivity
controls the field, the response, and the persistence simultaneously,
and this is exactly the role of "one-parameter mass" in the chain.

## What this bridge does NOT close

This bridge note is intentionally narrow. It explicitly does not assert:

- A persistent-pattern equivalence-principle theorem. The matter_inertial_closure
  no-go for free Gaussian packets shows that "generator-invariant inertial
  mass" remains blocked on a different object family.
- That the multistage compact object *responds* to an *external* field
  (i.e. a field sourced by a separate compact object) with the same
  generator-invariance. The probe used here is the same self-sourcing
  multistage compact object as in the audit-clean transfer sweep.
- Two-body momentum conservation between two different multistage compact
  objects. The current Principle-3 sub-step does not require this.
- Closure of the open gate `newton_derivation_note` itself. The gate's
  source note continues to flag a persistent-pattern theorem as the open
  step. This bridge only narrows the residual to the equivalence-principle
  / two-body extension.

Thus the open gate moves from "Principle 3 is unsupported on persistent
patterns" to "Principle 3 is operationally satisfied on the audit-clean
top4 multistage compact-object family; the residual gap is the
equivalence-principle / two-body extension to a different persistent
compact object."

## Artifact chain

- Primary runner: [`scripts/newton_derivation_top4_bridge_runner.py`](../scripts/newton_derivation_top4_bridge_runner.py)
  - re-extracts the Principle-3 measurements from the audit-clean
    `_run_case` admissibility helper at `top_keep = 4` on the baseline
    case `(W=3, L=6, source_z=2.0)`
  - prints `stage_mean_overlap`, `stage_alpha`, `stage_kappa`, and
    `max_kappa_drift`, then PASS/FAIL on the three Principle-3 gates
  - reuses the existing audit-clean machinery rather than introducing
    new dynamics

## Authorities cited

The bridge claim is built only from already-existing audit rows that
are themselves clean within their declared scopes:

- [persistent_object_top4_multistage_transfer_sweep_note_2026-04-16](PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md)
  — supplies the audit-clean retained-bounded statement that the
  multistage `top4` floor admits 11/13 widened-pocket cases under
  fixed overlap, alpha band, kappa drift, and stage-carry gates.
- [persistent_object_compact_inertial_probe_note_2026-04-16](PERSISTENT_OBJECT_COMPACT_INERTIAL_PROBE_NOTE_2026-04-16.md)
  — supplies the audit-clean retained-bounded statement that the
  `top3` compact object carries a stable weak-field response on its
  declared four nearby cases under broad/adaptive readouts and
  registers `KAPPA_DRIFT_THRESHOLD = 0.10`.
- [equivalence_principle_harness_note](EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md)
  — supplies the audit-clean retained-bounded statement that global
  amplitude scaling cancels in the centroid ratio and that normalized
  packet shape changes the response on the test-particle harness.
- [matter_inertial_closure_note](MATTER_INERTIAL_CLOSURE_NOTE.md)
  — supplies the audit-clean retained no-go statement that Gaussian
  packets do *not* satisfy a generator-invariant inertial mass, fixing
  the residual gap that this bridge does not close.
- [newton_derivation_note](NEWTON_DERIVATION_NOTE.md)
  — supplies the open-gate conditional theorem whose Principle-3
  premise this bridge note operationally satisfies on the multistage
  compact-object family.

## Best next move

The remaining gap on `newton_derivation_note` is now narrow and concrete:

> Does the same audit-clean multistage compact-object family also
> exhibit a generator-invariant response to an *external* field
> (i.e. a field sourced by a *different* compact object), or does
> the equivalence-principle no-go from `matter_inertial_closure_note`
> recur on the multistage object as well?

A future closure attempt should run an external-field response probe
on the `top4` multistage object family (varying object width in
`{top3, top4, top5}`) to test whether the response slope is shape-invariant
*on the persistent compact-object family* rather than on free Gaussian
packets. That experiment is outside the scope of this bridge note.
