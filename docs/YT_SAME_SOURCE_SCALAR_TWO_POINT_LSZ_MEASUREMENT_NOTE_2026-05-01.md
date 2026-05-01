# Top-Yukawa Same-Source Scalar Two-Point LSZ Measurement

**Date:** 2026-05-01
**Status:** bounded-support / same-source scalar two-point LSZ measurement primitive
**Runner:** `scripts/frontier_yt_same_source_scalar_two_point_lsz_measurement.py`
**Certificate:** `outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support if a controlled scalar pole, inverse-propagator derivative, and canonical-Higgs normalization are later derived or measured
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "No isolated scalar pole, continuum/IR control, or canonical LSZ normalization is derived."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Measurement Object

For the same additive scalar source used by the Feynman-Hellmann response
route,

```text
D(s) = D + (m_bare + s),
```

the scalar source two-point object is:

```text
C_ss(q) = Tr[S V_q S V_-q]
Gamma_ss(q) = 1 / C_ss(q)
```

where `S = D^{-1}` and `V_q` is the diagonal scalar source vertex with
momentum `q`.

Validation:

```text
python3 scripts/frontier_yt_same_source_scalar_two_point_lsz_measurement.py
# SUMMARY: PASS=8 FAIL=0
```

## Result

The runner computes `C_ss(q)` exactly on a tiny cold Wilson-staggered lattice.
It verifies:

- the same-source scalar bubble is finite;
- no measured reduced-mode inverse curvature gives a controlled scalar pole;
- the finite residue proxy is strongly mass-dependent;
- source rescaling changes inverse curvature as expected;
- the object identifies the route for fixing `kappa_s`.

## Claim Boundary

This is not retained closure.  A physical scalar LSZ bridge still needs:

- production or theorem-grade `C_ss(q)` for the same source used in `dE_top/ds`;
- an isolated Higgs-channel pole in the controlled finite-volume/IR limit;
- `dGamma_ss/dp^2` at that pole;
- a match to the canonical Higgs kinetic normalization used by `v`.

Until then, `dE_top/ds` cannot be converted to physical `dE_top/dh`, and
`kappa_s = 1` remains forbidden.
