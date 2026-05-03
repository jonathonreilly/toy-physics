# Handoff

## Outcome

Positive EW current matching closure was not reached on the current primitives.
The precise blocker is now sharper:

```text
Tr_internal(Q_EW)=0 removes Wick-disconnected current loops,
but kappa_EW multiplies the color Fierz singlet S in the connected
two-current contraction, where the internal factor is Tr_internal(Q_EW^2).
```

The exact counterexample is `N_c=3`, `Q_EW=T3`, `M=I_color`: the
Wick-disconnected factor is zero while the color-singlet same-line contribution
is `3/2`.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_current_traceless_generator_selector_no_go.py
PYTHONPATH=scripts python3 scripts/frontier_ew_current_matching_rule_no_go.py
python3 -m py_compile scripts/frontier_ew_current_traceless_generator_selector_no_go.py
```

Observed:

- `frontier_ew_current_traceless_generator_selector_no_go.py`: `PASS=29 FAIL=0`
- `frontier_ew_current_matching_rule_no_go.py`: `PASS=44 FAIL=0`

## Exact Next Action

Do not retry trace-based routes. The next productive positive attempt must
either:

1. define a framework-native EW current Wilson-line primitive whose two-current
   contraction is explicitly color-adjoint; or
2. compute the color Fierz singlet/disconnected coefficient exactly and show
   the physical readout coefficient is zero.
