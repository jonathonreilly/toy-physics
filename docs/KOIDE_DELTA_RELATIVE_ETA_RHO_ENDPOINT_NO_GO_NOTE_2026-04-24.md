# Koide delta relative-eta/rho endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_relative_eta_rho_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use relative eta or rho invariants of the retained `Z_3` boundary to bridge
closed APS data to the selected open Berry endpoint:

```text
relative eta/rho invariant
  -> theta_end - theta0 = eta_APS
  -> delta_physical = 2/9.
```

## Executable theorem

The retained twisted eta values are:

```text
eta_0 =  2/9
eta_1 = -1/9
eta_2 = -1/9.
```

The relative eta/rho differences are only:

```text
rho in {-1/3, 0, 1/3}.
```

Thus `eta_APS = 2/9` is not itself a nonzero relative-rho value.

## Obstruction

To hit the APS endpoint from a nonzero rho value requires a new coefficient:

```text
c * (1/3) = 2/9
c = 2/3.
```

That coefficient is not fixed by the relative eta arithmetic.  It is exactly a
new normalization from a closed comparison invariant to an open selected-line
endpoint.

The open endpoint still transforms as:

```text
theta_end - theta0
  -> theta_end - theta0 + chi_end - chi0.
```

The runner verifies that endpoint trivialization can fit the APS value
independently of the rho invariant.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_NORMALIZATION = rho_to_open_endpoint_coefficient_not_retained
```

## Why this is not closure

Relative eta/rho invariants compare closed twisted sectors.  They do not supply
the physical endpoint sections or functor needed for the Brannen selected line.
Choosing the untwisted eta value as the open endpoint is still the residual
Berry/APS bridge.

## Falsifiers

- A retained theorem that maps relative eta normalization to the selected-line
  Berry endpoint with coefficient `2/3` before seeing the target value.
- A boundary functor whose endpoint sections make the open phase equal to
  untwisted APS eta for all admissible trivializations.
- A proof that the selected Brannen line is itself a closed rho comparison
  cycle rather than an open path.

## Boundaries

- Covers the three `Z_3` character twists of the retained weights `(1,2)` and
  their pairwise relative eta/rho differences.
- Does not refute a future physical endpoint-trivialization theorem.

## Hostile reviewer objections answered

- **"Rho is more physical than eta."**  It is still a closed comparison
  invariant and its values are `0` or `+-1/3`, not `2/9`.
- **"Scale rho by `2/3`."**  That is the missing normalization primitive.
- **"Use eta_0 directly."**  That returns to the closed APS support value and
  does not identify the open selected-line endpoint.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_relative_eta_rho_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_RELATIVE_ETA_RHO_ENDPOINT_NO_GO=TRUE
DELTA_RELATIVE_ETA_RHO_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_NORMALIZATION=rho_to_open_endpoint_coefficient_not_retained
```
