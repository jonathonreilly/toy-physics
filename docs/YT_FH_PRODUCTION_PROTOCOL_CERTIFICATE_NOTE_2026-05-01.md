# Top-Yukawa Feynman-Hellmann Production Protocol Certificate

**Date:** 2026-05-01
**Status:** bounded-support / Feynman-Hellmann production protocol
**Runner:** `scripts/frontier_yt_fh_production_protocol_certificate.py`
**Certificate:** `outputs/yt_fh_production_protocol_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support if production response data, scalar LSZ/canonical normalization, and response matching are later supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Protocol lacks production response data and scalar LSZ/canonical normalization kappa_s."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Protocol

The production-grade Feynman-Hellmann observable is:

```text
dE_top/ds
```

where `s` is the uniform additive lattice scalar source entering the Dirac
operator as `m_bare + s`.  The direct-correlator harness now supports this
with `--scalar-source-shifts`.

The production protocol is:

- use the same strict volumes as the PR #230 production lane:
  `12^3x24`, `16^3x32`, `24^3x48`;
- measure symmetric source shifts, for example `s = -0.01, 0, +0.01`;
- measure all shifts on the same saved gauge configurations for correlated
  slope fits;
- fit `E_top(s)` per volume and then jointly fit `dE_top/ds` with finite-volume
  and source-window systematics;
- keep reduced or cold-gauge runs as scouts only.

Validation:

```text
python3 scripts/frontier_yt_fh_production_protocol_certificate.py
# SUMMARY: PASS=9 FAIL=0
```

## What Fixes `kappa_s`

The protocol still does not produce physical `dE_top/dh`:

```text
dE_top/dh = (dE_top/ds) / kappa_s
```

The missing measurement/theorem is the scalar source two-point LSZ bridge for
the same source:

- derive an isolated Higgs-channel pole;
- compute the inverse-propagator derivative / canonical residue;
- match that residue to the canonical kinetic normalization used by `v`.

Forbidden shortcuts remain forbidden: `H_unit`, `yt_ward_identity`, observed
top or observed `y_t`, `alpha_LM` / plaquette / `u0`, `kappa_s = 1`, and
`Z_match = 1` unless the relevant theorem is derived.

## Non-Claims

- This note does not claim retained closure.
- This note does not supply production response data.
- This note does not convert `dE/ds` to physical `dE/dh`.
- This note does not set `kappa_s` or `Z_match` to one.
