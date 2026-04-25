# Koide delta higher Cl(3) boundary source-grammar no-go

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py`
**Status:** no-go; local `Cl(3)/Z3` boundary source grammar does not force the selected endpoint identity

## Theorem Attempt

Exhaust the retained local `Cl(3)/Z3` boundary source grammar coupled to the
selected Brannen endpoint.  The hoped-for result was:

```text
spectator_channel = 0
c = 0
```

which would remove the reduced delta condition.

## Result

Negative.  The `C3`-fixed `Cl(3)` word space is four-dimensional, with fixed
generators:

```text
1
vector orbit
bivector orbit
pseudoscalar
```

So retained cyclic Clifford symmetry does not collapse all boundary sources to
a unique scalar word.

On the endpoint channel algebra, let:

```text
Z = P_selected - P_spectator.
```

Then `Z^2 = I`, so every higher local channel source collapses to:

```text
A_even I + A_odd Z.
```

Endpoint-exact source words independently collapse to:

```text
B_even I + B_odd Z.
```

## Unified Residual

After total anomaly normalization:

```text
selected_channel = (A_even + A_odd) / (2 A_even)
spectator_channel = (A_even - A_odd) / (2 A_even)
c = B_even + B_odd
```

The selected endpoint residual is:

```text
delta_open / eta_APS - 1 =
  -spectator_channel + c / eta_APS.
```

Closure requires the two independent coefficient conditions:

```text
A_odd = A_even
B_odd = -B_even
```

These are the selected-line projector law and endpoint zero-basepoint law.
They are not consequences of the retained grammar.

## Countermodels

The same retained grammar and total anomaly normalization permit:

```text
selected unit channel
spectator unit channel
half-selected half-spectator channel
selected unit channel with endpoint shift
```

Only the first closes.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_CHANNEL = selected_line_projector_source_not_forced
RESIDUAL_TRIVIALIZATION = selected_endpoint_exact_counterterm_not_forced_zero
RESIDUAL_SCALAR = minus_spectator_channel_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem proving the selected boundary projector is the only
  admissible anomaly channel.
- A retained theorem excluding spectator boundary idempotents.
- A retained theorem proving the selected endpoint exact counterterm vanishes.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_NO_GO=TRUE
DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_CHANNEL=selected_line_projector_source_not_forced
RESIDUAL_TRIVIALIZATION=selected_endpoint_exact_counterterm_not_forced_zero
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
```
