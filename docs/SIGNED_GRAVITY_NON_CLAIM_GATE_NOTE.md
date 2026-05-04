# Signed Gravity Non-Claim Gate Note

**Date:** 2026-04-25
**Status:** mandatory non-claim gate for signed gravitational response wording
**Primary runner:** [`scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py) (chi-product sign-flip diagnostic, 1/8 TOWARD at chi_product=+1, 5/8 AWAY at chi_product=-1)
**Companion:** [`SIGNED_GRAVITY_MECHANISM_SEPARATION_NOTE.md`](SIGNED_GRAVITY_MECHANISM_SEPARATION_NOTE.md)

This note defines the wording and promotion gate for the signed gravitational
response lane.

## Hard Boundary

The signed-response lane currently supports only this narrow statement:

> If a native or naturally hosted locked branch label `chi_g = +/-1` is later
> supplied, the consequence harness has a coherent same-sector attraction /
> opposite-sector repulsion table with positive inertial mass and two-body
> action-reaction closure.

It does not currently support:

- negative gravitational mass
- gravitational shielding
- propulsion
- reactionless force
- switchable gravity
- physical antigravity
- a full tensor-gravity claim

Use "AWAY", "opposite-sector repulsive-looking", or "signed-response
consequence" when the mechanism bucket is clear. Do not use "antigravity" as a
claim term.

## Current Gate State

The current P0 state is blocked at the derivation level:

| gate | current tag | consequence |
|---|---|---|
| local/taste-cell selector | `NO_GO_STRICT_SELECTOR` | no audited local `Q_chi` both conserves the retained massive scalar surface and pins scalar source sign |
| local source primitive | `SOURCE_PRIMITIVE_BLOCKED_LOCAL` | parity scalar density is signed but not branch-stable, conserved, or smooth-monopole stable |
| locked action-reaction algebra | pass for locked signs | consequence control only while selector/source gates are blocked |
| source-only / response-only controls | fail mixed-pair balance | no-go controls |
| lensing AWAY rows | phase-window dependent | interference only |
| complex-action AWAY rows | absorptive path selection | not conservative repulsive gravity |

The lane is therefore blocked from physical signed-gravity promotion until a
new selector/source construction changes the first two rows.

## Allowed Wording

Allowed before selector/source closure:

- "coherent locked-sign consequence harness"
- "repulsive-looking opposite-sector row in the locked algebraic control"
- "lensing phase flip"
- "complex absorptive AWAY"
- "boundary/proxy row"
- "inserted control/no-go"
- "not a physical signed-gravity claim"

Allowed conditional wording:

> A signed-response candidate would require a native selector, a branch-stable
> signed source, source/response locking by one label, positive inertial mass,
> and two-body action-reaction closure.

## Forbidden Wording

Do not write:

- "the framework predicts antigravity"
- "negative mass exists"
- "gravity is shielded"
- "gravity can be switched"
- "this enables propulsion"
- "lensing AWAY proves repulsive gravity"
- "complex-action AWAY proves repulsive gravity"
- "Born-clean AWAY proves a physical sector"
- "inserted `chi_g` source is derived"

These phrases are blocked unless a future theorem supplies the missing
selector/source derivation and the claim is rewritten with the actual mechanism.

## Citation Gate

The following artifacts may not be cited as positive `chi_g` evidence by
themselves:

- [`LENSING_K_SWEEP_NOTE.md`](LENSING_K_SWEEP_NOTE.md)
- [`../scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py)
- [`COMPLEX_ACTION_NOTE.md`](COMPLEX_ACTION_NOTE.md)
- [`COMPLEX_SELECTIVITY_COMPARE_NOTE.md`](COMPLEX_SELECTIVITY_COMPARE_NOTE.md)
- [`COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`](COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md)
- inserted-source normalization or electrostatics signed-charge controls

They can be cited only as mechanism separation, quarantine, or control
evidence.

## Promotion Checklist

Before any future text calls an AWAY row a signed gravitational response
candidate, it must show:

1. mechanism bucket is `locked_chi_response`
2. selector gate passes
3. source gate passes
4. the same `chi_g` locks source and response
5. two-body action-reaction passes
6. inertial mass remains positive
7. source-only and response-only controls are rejected
8. lensing phase and complex absorptive explanations are not the active
   mechanism
9. boundary/proxy readouts are replayed on a conservative two-body gate

If any item is missing, the row must remain `CLAIM_SURFACE_BLOCKED`,
`LENSING_PHASE_ONLY`, `COMPLEX_ABSORPTIVE_ONLY`, `BOUNDARY_PROXY_ONLY`, or
`CONTROL_NO_GO`.

## Current Verdict

The present signed gravitational response lane is a useful consequence and
no-go control lane. It is not a physical antigravity lane.
