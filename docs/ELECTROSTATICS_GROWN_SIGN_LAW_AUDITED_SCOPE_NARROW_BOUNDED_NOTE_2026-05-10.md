# Electrostatics Grown Sign-Law Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_electrostatics_grown_sign_law_audited_scope_pass_thresholds.py`](../scripts/frontier_electrostatics_grown_sign_law_audited_scope_pass_thresholds.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md`](ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
returned `audited_conditional` with the explicit verdict:

> The runner source performs a real numerical propagation and
> reproduces the note's printed signs, cancellation, and linearity
> checks, but it imports the grown geometry generator
> `scripts.gate_b_grown_joint_package.grow` whose implementation and
> retained-grade basis are not included in the restricted packet. The
> missing step is closure of the retained grown row/geometry
> generator and its boundary conditions from the stated axiom or
> provided evidence.

with re-audit guidance:

> missing_dependency_edge: include the `grow` implementation and a
> registered deterministic runner artifact with explicit PASS
> thresholds for sign, neutral cancellation, dipole partial
> cancellation, and +1/+2 linearity.

The parent note's `Audit boundary (2026-04-28)` section already records
the same conditional verdict and Path A future-work list. This
companion note narrows the parent's audited within-scope content into
an explicit PASS-threshold gate set on a registered companion runner.
It does not extend the parent's scope and does not close the upstream
`grow`-generator dependency.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_conditional`
- `audit_date: 2026-05-05`
- `chain_closes: false`
- `claim_scope` (audited): "Fixed grown geometry row drift=0.2,
  restore=0.7, seeds=[0,1], fixed-field/no graph update, one source
  layer, final-layer centroid readout, with the provided runner output
  and source code."

## Narrow within-scope content (what the audited row does close)

Inside the audited fixed-row scope, this companion runner gates the
following propositions with explicit PASS thresholds against the
parent's already-frozen numerical output:

| Audited content | PASS threshold | Status |
|---|---|---|
| Single +1 source produces AWAY motion (`delta_z < -1e-5`) | sign and resolution gate | PASS |
| Single -1 source produces TOWARD motion (`delta_z > +1e-5`) | sign and resolution gate | PASS |
| Sign antisymmetry: `\|delta(+1) + delta(-1)\| / \|delta(+1)\| < 1e-3` | relative-tolerance gate | PASS |
| Neutral same-point +/- pair: `\|delta_z\| < 1e-12` | machine-precision guardrail | PASS |
| Like-pair (+1, +1) produces AWAY motion | sign gate | PASS |
| Dipole (+1, -1) produces TOWARD partial cancellation | sign gate | PASS |
| Double +2 source produces AWAY motion | sign gate | PASS |
| Charge linearity: `\|delta(+2)/delta(+1) - 2.0\| < 5e-3` | linearity gate | PASS |
| Audited scope guardrail: single grown row, not geometry-generic | scope-statement guardrail | PASS |

The companion runner imports the same `grow` generator and the same
propagation/centroid routines as the parent runner, so the underlying
numerical behaviour is identical. The new content is the explicit
deterministic PASS-threshold gating around that behaviour, addressing
the audit verdict's "missing_dependency_edge" repair item for the
runner-artifact half of the gap.

## What the narrow scope does **not** close

The audit verdict's other repair items remain open and are **not**
addressed by this companion:

- closure of the retained grown row / `grow` geometry generator and
  its boundary conditions from the stated axiom (the `scripts/gate_b_grown_joint_package.py`
  open-dependency edge in the audit ledger);
- coverage beyond the single grown row `(drift=0.2, restore=0.7)`;
- any geometry-generic sign-law theorem;
- coverage of graph-update cases or alternative source-layer / detector
  configurations;
- any extension to full electromagnetism, Maxwell, or radiation
  derivations.

The parent note's `What this note does NOT claim` and `What would
close this lane (Path A future work)` sections record the same
boundaries.

## What would close the open dependencies (Path A future work)

Promoting the parent row from `audited_conditional` to retained would
require, per the audit verdict's repair targets:

1. closure of the `gate_b_grown_joint_package.grow` implementation
   from the stated axiom or other registered evidence (the
   open-dependency edge in the audit ledger);
2. extension of the runner gates to a family of grown geometries with
   hard PASS thresholds (or explicit retention of the single-row
   scope, which is the current stance and is what this companion
   gates).

Until (1) is supplied, the row remains a bounded conditional
sign-law-transfer support note at the audited single-row scope.

## Dependencies

- [`ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md`](ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
  for the parent audited support note.

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_conditional`;
- close the upstream `grow`-generator dependency;
- extend the audited scope beyond the single grown row;
- claim a geometry-generic sign-law theorem;
- extend to full electromagnetism, Maxwell, or radiation.

## Verification

Run:

```bash
PYTHONPATH=. python3 scripts/frontier_electrostatics_grown_sign_law_audited_scope_pass_thresholds.py
```

Expected:

```text
TOTAL: PASS=9, FAIL=0
VERDICT: bounded grown sign-law audited-scope checks pass with explicit PASS thresholds
         on the single grown row drift=0.2, restore=0.7. This is bounded support, not
         a geometry-generic electrostatics theorem and not full EM.
```

```yaml
claim_id: electrostatics_grown_sign_law_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/ELECTROSTATICS_GROWN_SIGN_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_electrostatics_grown_sign_law_audited_scope_pass_thresholds.py
proposed_claim_type: bounded_theorem
deps:
  - electrostatics_grown_sign_law_note
audit_authority: independent audit lane only
```
