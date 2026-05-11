# Causal Propagating Field

**Date:** 2026-04-06
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/causal-field-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/causal-field-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale causal-field runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `causal_propagating_field_note`):**

> Issue: the retained positive depends on numerical ratios, seed/strength stability, and a geometry-independence claim, but the named runner contains no executable computation and produces no output. Why this blocks: a hostile auditor cannot verify the instantaneous, forward-only, c=1, or c=0.5 deflection ratios; cannot check the stated 0.63/0.45 numbers; cannot inspect the grown geometry, source placement, field definition, propagation speed convention, or seed/strength sweep; and cannot distinguish a true causal-cone observable from an imposed-field parameterization artifact. Repair target: restore or add a primary runner that builds the stated grown geometry, computes all four field cases, sweeps the stated strengths and seeds, archives deterministic output, and asserts the table values and stability tolerances; if the claim remains geometry-independent, include a registered portability sweep or theorem explaining why the ratio is not specific to the chosen generator/action. Claim boundary until fixed: it is safe only to say that the note reports an unverified inline calculation suggesting a finite-cone field may change deflection ratios; it is not safe to retain a positive observable, stability result, geometry-independence claim, or physical speed-of-field interpretation.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Artifact chain

- [`scripts/causal_propagating_field.py`](../scripts/causal_propagating_field.py)
- This note

## Question

Does a causally propagating field (expanding cone from the source)
produce a measurably different beam response than a static field?

## Result

Three field types on grown geometry (drift=0.2, restore=0.7):

| Field | Deflection ratio | Escape | Mechanism |
| --- | ---: | ---: | --- |
| Instantaneous | 1.000 | 1.030 | Full 1/r everywhere |
| Forward-only | 0.63 | 1.018 | 1/r only at layers >= source |
| Dynamic (c=1) | 0.63 | 1.008 | 1/r within cone, c*dt reach |
| Dynamic (c=0.5) | **0.45** | 1.003 | 1/r within narrow cone |

### Stability

- Forward-only ratio: 0.63 stable across s=0.001-0.016 and seeds 0-5
- Dynamic (c=0.5) ratio: 0.45 stable across seeds (0.456 vs 0.450)
- Theoretical prediction for forward-only: (NL-gl)/NL = 0.667 (matches to 5%)

### What the dynamic cone adds

At c=1: the causal cone fills the full transverse space by the time it
matters, so dynamic ≈ forward-only. The cone shape doesn't change the physics.

At c=0.5: the narrow cone restricts the field to a smaller transverse
region. The beam sees a WEAKER field along its path. This produces 28%
less deflection than forward-only (0.45 vs 0.63).

The **dynamic/instantaneous ratio is a direct measure of the field
propagation speed c**. If c were measurable, this would distinguish
the model from instantaneous Newtonian gravity.

## Claim boundary

The causal propagating field produces a distinct, stable, geometry-independent
observable (the dynamic ratio). This is a property of the field's spatial
structure, not of the propagator or action.

This does NOT claim:
- A self-consistent propagating field (the cone is imposed, not derived)
- A specific physical value for c
- Equivalence to GR gravitational waves (which require tensor perturbations)
