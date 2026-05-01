# Top-Yukawa Mass-Response Bracket Certificate

**Date:** 2026-05-01  
**Status:** bounded-support / reduced mass-response bracket  
**Runner:** `scripts/frontier_yt_mass_response_bracket_certificate.py`  
**Certificate:** `outputs/yt_mass_response_bracket_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for a future production Feynman-Hellmann response measurement
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Reduced-scope data and bare-source response do not authorize retained proposal wording."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This note extracts the lightweight Feynman-Hellmann-style information already
present in the reduced `12^3 x 24` mass-bracket correlator run:

```text
dE_top / dm_bare
```

This is a bare-source response from a correlator measurement.  It is not the
old `H_unit` readout and it does not use observed top data.

## Result

```text
python3 scripts/frontier_yt_mass_response_bracket_certificate.py
# SUMMARY: PASS=7 FAIL=0
```

The fitted correlator energy is monotone in the bare mass, with positive local
slopes:

```text
[0.8858019822, 0.5730600072, 0.3261798736, 0.1704644512]
```

This confirms that the response observable is viable as a lightweight first
pass.  It also shows the response varies across the broad mass bracket, so a
production response campaign would need a controlled physical-point bracket and
matching.

## Boundary

The output is not a physical `y_t` readout.  It is reduced-scope pilot data and
measures `dE/dm_bare`, not `dE/dh` for a canonically normalized Higgs
fluctuation.  Closure still needs:

- production response measurement on gauge ensembles;
- scalar source-to-canonical-Higgs normalization or scalar LSZ residue;
- lattice-to-SM matching for the response observable.

## Non-Claims

- This note is not production data.
- This note is not a physical `y_t` derivation.
- This note does not use `H_unit` matrix-element readout.
- This note does not use observed top mass or observed `y_t`.
- This note does not set scalar-source normalization or `Z_match` to one.
