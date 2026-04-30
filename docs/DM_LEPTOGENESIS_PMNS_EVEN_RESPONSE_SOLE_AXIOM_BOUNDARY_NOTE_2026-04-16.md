# DM Leptogenesis PMNS Even-Response Sole-Axiom Boundary

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_leptogenesis_pmns_even_response_sole_axiom_boundary.py`

## Question

After the residual PMNS sheet selector has been reduced to

- `sign(sin(delta))`

on the fixed native `N_e` seed surface, does the current sole-axiom bank
already fix the remaining constructive data?

## Bottom line

No.

On the same exact native `N_e` seed surface, and with the same positive odd
selector bit `sin(delta) > 0`, the canonical near-closing sample and the
constructive projected-source witness still carry opposite even-response
pairs:

- `canonical:     E1 < 0, E2 < 0`
- `constructive:  E1 > 0, E2 > 0`

So after the odd selector is fixed, the exact remaining PMNS sole-axiom object
is the even-response law for

- `(E1, E2)`

equivalently the carrier-side pair

- `(delta + rho, sigma sin(2v))`.

## Exact content

### 1. Same native seed surface, same positive odd selector bit

The canonical near-closing `N_e` sample and the constructive projected-source
witness already share the same exact native seed pair:

- `xbar = 0.563333333333...`
- `ybar = 0.306666666667...`

They also already agree on the current odd selector data:

- `sin(delta) > 0`
- equivalently `gamma > 0`
- equivalently `A13 > 0`

So the odd sheet orientation is not the remaining freedom between those two
samples.

### 2. The even-response pair still varies on that same odd sheet

Despite sharing the same seed surface and positive odd selector bit, the two
samples land on opposite even-response chambers:

- canonical near-closing sample:
  - `E1 = -0.678203236088...`
  - `E2 = -0.974296763912...`
- constructive projected-source witness:
  - `E1 = 0.296562850784...`
  - `E2 = 1.986407435174...`

So the current sole axiom does not yet fix the constructive PMNS sheet once
the odd bit is known.

### 3. Equivalent carrier-side statement

On the active charged-sector family,

- `E1 = delta + rho`
- `E2 = 3 sqrt(2) sigma sin(2v) / 4`

with

- `sigma = -Lambda_+ + Lambda_odd + u`

on the carrier

- `B_H,min = (Lambda_+, Lambda_odd, u, v, delta, rho, gamma)`.

So the same remaining PMNS sole-axiom object can be stated equivalently as the
carrier-side even-response pair:

- `delta + rho`
- `sigma sin(2v)`

rather than as another odd-sheet selector.

## Consequence

The odd PMNS sheet selector is already theorem-grade and closed:

- `sign(sin(delta))`

But that is not yet the full sole-axiom-native constructive law.

The remaining honest PMNS comparator object is now:

- the even-response law for `(E1, E2)`
- equivalently the carrier-side pair `(delta + rho, sigma sin(2v))`

So the next native theorem on the PMNS side is an even-response value law or
an even-response no-go, not another odd-slot selector theorem.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_pmns_even_response_sole_axiom_boundary.py
```
