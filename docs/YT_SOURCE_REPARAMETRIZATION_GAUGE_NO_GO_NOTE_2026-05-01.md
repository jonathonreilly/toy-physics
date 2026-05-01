# Top-Yukawa Source-Reparametrization Gauge No-Go

**Date:** 2026-05-01  
**Status:** exact negative boundary / source reparametrization gauge  
**Runner:** `scripts/frontier_yt_source_reparametrization_gauge_no_go.py`  
**Certificate:** `outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future scalar LSZ or canonical-field theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The source normalization kappa is a gauge freedom on the current source-functional surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Claim

Source-functional routes are covariant under a scalar-source reparametrization.
If the physical scalar fluctuation is `h = kappa s`, then derivatives with
respect to the lattice source `s` are not physical derivatives with respect to
`h` until `kappa` is fixed.

This applies to:

- source curvature;
- same-1PI products `y^2 D_phi`;
- Feynman-Hellmann slopes `dE/ds`;
- scalar source response ratios.

## Result

```text
python3 scripts/frontier_yt_source_reparametrization_gauge_no_go.py
# SUMMARY: PASS=6 FAIL=0
```

The runner verifies that source-functional products can remain invariant while
the readout obtained by setting `kappa = 1` varies by order one.  If `kappa` is
known, the physical readout is stable.  The problem is not algebraic
bookkeeping; it is the absence of a retained canonical scalar normalization or
scalar LSZ residue on the current PR #230 surface.

## Consequence

No source-only analytic route should be promoted to top-Yukawa closure unless it
supplies one of the following:

- a scalar LSZ residue theorem;
- a canonical scalar kinetic/field normalization theorem;
- direct physical response measurement with matching;
- production correlator evidence plus an independently derived
  source-to-Higgs bridge.

## Non-Claims

- This note does not rule out a future scalar LSZ theorem.
- This note does not use `H_unit` matrix-element readout.
- This note does not use observed top mass or observed `y_t`.
- This note does not use `alpha_LM`, plaquette, or `u0` as proof input.
