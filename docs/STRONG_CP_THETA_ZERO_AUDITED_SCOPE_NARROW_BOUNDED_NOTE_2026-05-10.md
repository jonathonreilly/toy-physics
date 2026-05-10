# Strong CP / θ = 0 Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_strong_cp_theta_zero.py`](../scripts/frontier_strong_cp_theta_zero.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md)
returned `audited_conditional` with the explicit verdict:

> The runner genuinely computes several retained-surface consistency
> checks, including determinant positivity, axial-grid behavior,
> effective-action reality, and sampled θ-sum positivity. However,
> the load-bearing θ_eff = 0 step uses the θ-free action-class
> definition and an explicit positive real mass surface as premises
> rather than deriving them from the provided axiom packet. The note
> itself correctly narrows the claim to a bounded conditional
> action-surface closure, so the appropriate verdict is conditional
> rather than failed or clean.

with re-audit guidance:

> missing_bridge_theorem: add a retained operator-basis/action-surface
> theorem deriving no admissible F̃F term and a registered positive
> real quark-mass orientation theorem, then update the runner to
> construct and reject the forbidden slots.

The parent note's `Audit boundary (2026-04-28)`,
`What this note does NOT claim`, and `What would close this lane
(Path A future work)` sections already record the same conditional
verdict and Path A repair list. This companion note isolates the
within-scope content that the audit verdict explicitly accepts as
internally-consistent on the selected θ-free Wilson-plus-staggered
scalar-mass surface, separated from the two open bridge dependencies.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_conditional`
- `audit_date: 2026-05-05`
- `chain_closes: false`
- `claim_scope` (audited): "Audited only the explicitly θ-free
  Wilson-plus-staggered scalar-mass retained action surface and its
  internal determinant, axial, effective-action, and positive-weight
  checks."

## Narrow within-scope content (what the audited row does close)

Inside the audited explicitly-θ-free Wilson-plus-staggered scalar-
mass action-surface scope, the parent runner verifies the following
internal consistency checks. Each is independent of the two open
bridge dependencies:

| Audited content | Bucket | Status |
|---|---|---|
| Free-field and gauged `Z^3` staggered determinant positivity | RETAINED-SURFACE COMPUTE | PASS |
| `3+1` APBC determinant positivity on sampled retained `SU(3)` configurations | RETAINED-SURFACE COMPUTE | PASS |
| Sampled nontrivial topological charge without determinant phase generation | RETAINED-SURFACE COMPUTE | PASS |
| `epsilon D + D epsilon = 0` on the retained `3+1` APBC surface | RETAINED-SURFACE COMPUTE | PASS |
| Sampled exact `±λ` pairing of `i D` | RETAINED-SURFACE COMPUTE | PASS |
| Sampled `Im Γ_f = 0` | RETAINED-SURFACE COMPUTE | PASS |
| Sampled spectral-phase / determinant-phase agreement | RETAINED-SURFACE COMPUTE | PASS |
| Axial-grid audit consistent with "only `α ∈ π Z` preserves a real mass operator" | RETAINED-SURFACE COMPUTE | PASS |
| Explicit nontrivial axial rotation exits the retained scalar-mass action class | RETAINED-SURFACE COMPUTE | PASS |
| Admissible retained-surface axial endpoints keep zero determinant phase | RETAINED-SURFACE COMPUTE | PASS |
| Explicit positive-mass quark-surface audit gives `arg det(M_u M_d) = 0` | RETAINED-SURFACE COMPUTE | PASS |
| Sampled retained effective action is real | RETAINED-SURFACE COMPUTE | PASS |
| Linkwise complex conjugation preserves the full retained effective action | RETAINED-SURFACE COMPUTE | PASS |
| Sampled retained positive-weight `Q`-weighted family obeys `\|Z(θ)\| ≤ Z(0)` | RETAINED-SURFACE COMPUTE | PASS |
| Sampled retained free energy minimized at `θ = 0` | RETAINED-SURFACE COMPUTE | PASS |
| Selected-axis weak `su(2)` closes exactly | THEOREM | PASS |
| Joint commutant dimension `10 = gl(3) ⊕ gl(1)` | THEOREM | PASS |
| `Z_3` discrete cube-root eigenvalues; does not commute with selected-axis `SU(2)` | THEOREM | PASS |
| `\|det V_CKM\| = 1` | THEOREM | PASS |
| Algebraic `epsilon^2 = I`, unitarity of `U_α = exp(i α epsilon / 2)`, kinetic invariance `U_α D U_α = D`, and mass rotation algebra | THEOREM | PASS |

Inside this audited scope, the parent runner reports
`THEOREM PASS=13 FAIL=0` and `RETAINED-SURFACE COMPUTE PASS=30 FAIL=0`,
all of which are accepted by the audit verdict as internal consistency
checks on the selected action surface.

## What the narrow scope does **not** close

The audit verdict and the parent's own scope-qualifier sections
already flag these explicitly. This companion note records them in
one place for re-audit traceability:

- a derivation that the physical `Cl(3)/Z^3` action **forbids** the
  CP-odd `F̃F` term (the action-surface "no bare θ slot" premise is
  taken as part of the retained action-class definition, not derived);
- a derivation of the positive real quark-mass orientation
  (`arg det(M_u M_d) = 0`) from framework primitives (the parent
  runner uses an explicit positive-mass surface);
- a dynamical selection of `θ = 0` rather than an evaluation of a
  θ-free surface (the runner finds no generated phase on the θ-free
  surface but does not derive the surface's exclusion of CP-odd
  terms).

These are exactly the two bridge dependencies the audit verdict's
re-audit guidance asks for.

## What would close the open dependencies (Path A future work)

Promoting the parent row from `audited_conditional` to retained would
require, per the audit verdict's repair targets:

1. a retained operator-basis / action-surface theorem deriving from
   `Cl(3)/Z^3` primitives and canonical normalization that no
   gauge-invariant CP-odd θ term is an admissible action slot;
2. a registered positive real quark-mass orientation /
   `arg det(M_u M_d) = 0` theorem as a dependency;
3. an updated runner that constructs the allowed action basis and
   **fails** if an `F̃F` term or complex mass phase is admitted
   (rather than evaluating on the θ-free surface).

Until at least (1) is supplied, the row remains a bounded conditional
action-surface θ_eff = 0 closure note at the audited scope.

## Dependencies

- [`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md)
  for the parent audited support note.

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the action-surface `F̃F`-exclusion theorem from framework
  primitives;
- derive the positive real quark-mass orientation from framework
  primitives;
- claim a dynamical `θ = 0` selection;
- claim an unrestricted all-formulations strong-CP solution;
- claim axion-model exclusion beyond the retained action surface;
- alter observable neutron-EDM matrix-element claims, which continue
  to live in the separate CKM-only neutron-EDM lane.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_strong_cp_theta_zero.py
```

Expected (unchanged from parent):

```text
THEOREM PASS=13  FAIL=0
RETAINED-SURFACE COMPUTE PASS=30  FAIL=0
SUPPORT=4
```

The runner is the same one cited by the parent note. This narrowing
companion does not introduce a new runner because the audited
within-scope action-surface checks are already exercised. The new
content is the explicit scope-narrowing recording of which checks the
audit verdict accepts as internal consistency on the θ-free
Wilson-plus-staggered scalar-mass surface versus which remain open as
bridge dependencies.

```yaml
claim_id: strong_cp_theta_zero_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/STRONG_CP_THETA_ZERO_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_strong_cp_theta_zero.py
proposed_claim_type: bounded_theorem
deps:
  - strong_cp_theta_zero_note
audit_authority: independent audit lane only
```
