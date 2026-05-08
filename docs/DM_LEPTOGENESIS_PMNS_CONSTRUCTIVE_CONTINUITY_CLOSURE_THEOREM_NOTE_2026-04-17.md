# DM Leptogenesis PMNS Constructive Continuity Closure Theorem

**Date:** 2026-04-17  
**Status:** exact positive existence theorem on the open PMNS constructive gate  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem.py`

## Question

Does the constructive projected-source chamber on the fixed native `N_e` seed
surface contain only an overshooting witness, or does it already contain an
exact `eta/eta_obs = 1` point?

## Bottom line

It already contains an exact closure point.

Take the explicit interpolation family from the aligned native seed point to
the constructive projected-source witness:

- aligned native seed:
  - `x_seed = (XBAR_NE, XBAR_NE, XBAR_NE)`
  - `y_seed = (YBAR_NE, YBAR_NE, YBAR_NE)`
  - `delta_seed = 0`
- constructive witness:
  - `x_w = (1.174161560603, 0.462544348009, 0.053294091387)`
  - `y_w = (0.758741415897, 0.026904299513, 0.134354284590)`
  - `delta_w = 1.882595756164`

and define

`(x,y,delta)(lambda) = (1-lambda)(x_seed,y_seed,0) + lambda (x_w,y_w,delta_w)`.

Along this family:

- the exact native seed averages stay fixed
- the constructive witness column satisfies
  - `eta_1(0) < 1`
  - `eta_1(1) > 1`

Equivalently:

- `eta_1(0) < 1 < eta_1(1)`

so by continuity there exists `lambda_* in (0,1)` with

- `eta_1(lambda_*) = 1`.

At that same point the projected-source triplet still satisfies

- `gamma > 0`
- `E1 > 0`
- `E2 > 0`.

So the constructive PMNS chamber contains an exact `eta = eta_obs` point on
the current branch.

## Exact theorem content

### 1. The interpolation family stays on the fixed native seed surface

Both endpoints have the same exact native averages

- `xbar = XBAR_NE = 0.563333333333...`
- `ybar = YBAR_NE = 0.306666666667...`

and linear interpolation preserves those averages exactly. So every
`lambda in [0,1]` stays on the same fixed native `N_e` seed surface.

### 2. The constructive column crosses exact closure

On the aligned native seed point, the constructive witness column is still
below exact closure:

- `eta_1(0) = 0.719082664368...`

while on the constructive witness it overshoots:

- `eta_1(1) = 1.052220313052...`.

Therefore continuity gives an exact root

- `lambda_* in (0,1)`

with

- `eta_1(lambda_*) = 1`.

Numerically the branch witness is

- `lambda_* = 0.795532193595...`.

### 3. The root remains constructive

At that same root the projected-source triplet still lies on the constructive
mainline chamber:

- `gamma = 0.177466004463... > 0`
- `E1 = 0.247922610478... > 0`
- `E2 = 1.552085732579... > 0`

and the full flavored read is

- `eta/eta_obs = (1.039446..., 1.000000..., 0.858610...)`.

So this is not only an exact closure point. It is an exact closure point on
the constructive projected-source sheet.

## Consequence

This sharpens the PMNS side materially.

What was already known:

- the constructive sign chamber is nonempty
- it contains an overshooting witness

What is now stronger:

- it also contains an exact `eta = eta_obs` point

So the remaining PMNS issue is no longer existence of a constructive exact
closure point. It is only the selector law that would choose that point
uniquely.

## Scope

This note does **not** prove selector closure.

It proves exact constructive existence on the current branch:

- a constructive exact closure point exists on the fixed native `N_e` seed
  surface.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16](DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)
- [dm_leptogenesis_ne_projected_source_triplet_sign_theorem_note_2026-04-16](DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md)
- [dm_leptogenesis_pmns_constructive_projected_source_selector_theorem_note_2026-04-16](DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md)
- [dm_leptogenesis_pmns_projector_interface_note_2026-04-16](DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [dm_leptogenesis_pmns_transport_extremal_source_candidate_note_2026-04-16](DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
