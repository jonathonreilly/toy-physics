# PR230 Common-Window Response Support Intake

**Status:** bounded support / common-window response stability support accepted; physical readout switch remains blocked

**Runners:**

- `scripts/frontier_yt_fh_lsz_common_window_response_gate.py`
- `scripts/frontier_yt_same_source_pole_data_sufficiency_gate.py`

**Certificates:**

- `outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json`
- `outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json`

```yaml
actual_current_surface_status: bounded-support / common-window response support accepted; physical readout switch remains blocked
conditional_surface_status: conditional-support only if scalar pole/model-class/FV/IR authority and canonical-Higgs pole identity are supplied
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Purpose

Block51 correctly retired the stale L12 incompleteness boundary, but it still
left "response stability" as too broad a blocker.  The repo already contains a
more precise support result: the mixed raw fitted-slope instability is
explained by inconsistent source-shift fit windows, and a predeclared
`tau=10..12` common-window response gate passes as bounded support across the
full `63/63` L12 set.

This block wires that support into the same-source pole-data sufficiency gate
without promoting it to a physical top-Yukawa readout.

## Result

The common-window response gate reports:

- mean common-window slope `1.4254094730430789`;
- chunk-level relative standard deviation `0.00561579672777511`;
- pooled relative standard error `0.0007075238835801541`;
- replacement response-stability support passed;
- `readout_switch_authorized=false`.

The updated same-source sufficiency gate now distinguishes:

- complete L12 same-source support: passed;
- response-side stability support: passed through the common-window gate;
- physical response readout switch: not authorized;
- scalar pole/model-class/FV/IR authority: absent;
- canonical-Higgs pole identity: absent.

Therefore response-side stability support is no longer the right next blocker.
The remaining response-side issue is physical readout authorization, which is
the same scalar-LSZ and canonical-Higgs identity bridge already blocking the
route.

## Boundary

This block does not choose the common-window response as a physical `dE/dh`
observable.  It only says the response data have a stable support diagnostic
when read through the predeclared common window.  Physical use still requires
the source pole, pole derivative, finite-volume/IR/model-class authority, and
the identity of that pole with canonical Higgs radial `O_H`.

## Non-Claims

This note does not claim retained or `proposed_retained` PR230 closure.  It
does not set `kappa_s = 1`, does not authorize a common-window physical
readout switch, does not identify the scalar source with canonical `O_H`, does
not use `H_unit`, `yt_ward_identity`, observed top mass, observed `y_t`,
`alpha_LM`, plaquette, or `u0`, and does not relabel source-only rows as strict
`C_sH/C_HH` source-Higgs pole rows.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_same_source_pole_data_sufficiency_gate.py
python3 scripts/frontier_yt_fh_lsz_common_window_response_gate.py
# SUMMARY: PASS=14 FAIL=0
python3 scripts/frontier_yt_same_source_pole_data_sufficiency_gate.py
# SUMMARY: PASS=13 FAIL=0
```
