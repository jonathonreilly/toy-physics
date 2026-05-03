# PR #230 FH/LSZ Response-Window Acceptance Gate

**Status:** open / FH-LSZ response-window acceptance gate not passed
**Runner:** `scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py`
**Certificate:** `outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json`

## Purpose

The response-window forensics certificate found that the tau=1 target
diagnostic is stable while the fitted `dE/ds` surface remains unstable.  This
gate records what would be required before any response-window/readout switch
could become production evidence.

## Result

```text
python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0
```

The current chunks provide stable chunk-level symmetric source-shift
effective-mass slopes across tau windows 0-9:

```text
stable_tau_windows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
tau_window_mean_spread = 1.00497773596142
```

The acceptance gate still does not pass:

- per-configuration multi-tau covariance is absent;
- target serialization currently records tau=1 slopes only;
- the finite-source-linearity gate is not passed, so only one source radius is
  available;
- the fitted-slope response-stability gate remains open.

## Claim Boundary

This gate does not authorize a response readout switch, retained closure, or
`proposed_retained` wording.  It does not set `kappa_s = 1`, does not treat one
finite source radius as the zero-source FH derivative, and does not use
`H_unit`, Ward authority, observed target values, `alpha_LM`, plaquette, or
`u0` as proof inputs.

Even a future passing response-window gate would still require scalar-pole
derivative/model-class/FV/IR control and canonical-Higgs source-overlap
identity before physical `y_t` closure.

## Next Action

Extend target serialization to per-configuration multi-tau response rows and
run a multi-radius source-response calibration, or continue the non-source-only
canonical-Higgs identity routes.
