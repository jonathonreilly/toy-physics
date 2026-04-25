# Koide delta Callan-Harvey degree-functor no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_callan_harvey_degree_functor_no_go.py`  
**Status:** no-go; anomaly inflow fixes the closed scalar, not the selected-line readout degree

## Theorem Attempt

Use Callan-Harvey anomaly inflow to remove the endpoint-functor residual.  The
strongest version asks whether inflow current normalization forces:

```text
delta_open = eta_APS.
```

## Result

Negative.  The retained arithmetic fixes:

```text
A_CH = eta_APS = 2/9.
```

The selected-line readout can still carry open variables:

```text
delta_open = n N_desc eta_APS + c.
```

The retained APS/anomaly equations have zero rank in `(n, N_desc, c)`.

## Exact Residual

With `c = 0`, closure is equivalent to:

```text
n N_desc = 1.
```

With an arbitrary endpoint basepoint:

```text
delta_open / eta_APS - 1 = n N_desc - 1 + c / eta_APS.
```

Thus the remaining theorem is a unit-current selected-line law plus endpoint
basepoint law.

## Countermodels

The same closed anomaly support permits:

```text
n = 1, N_desc = 1/2, c = 0  -> delta_open = 1/9
n = 2, N_desc = 1,   c = 0  -> delta_open = 4/9
n = 1, N_desc = 1,   c = 1/9 -> delta_open = 1/3
```

These are excluded only by the missing selected-line unit-current theorem.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_CURRENT_NORMALIZATION = selected_line_unit_current_degree_not_forced
RESIDUAL_SCALAR = n_times_N_desc_minus_one_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem identifying the selected Brannen line as the unique unit
  Callan-Harvey inflow channel.
- A retained theorem excluding higher or fractional open-readout degree.
- A retained endpoint basepoint theorem deriving `c = 0`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_callan_harvey_degree_functor_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_NO_GO=TRUE
DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_CURRENT_NORMALIZATION=selected_line_unit_current_degree_not_forced
RESIDUAL_SCALAR=n_times_N_desc_minus_one_plus_c_over_eta_APS
```
