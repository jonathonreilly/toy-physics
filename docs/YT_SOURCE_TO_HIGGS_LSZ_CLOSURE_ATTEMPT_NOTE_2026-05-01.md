# Top-Yukawa Source-to-Higgs / LSZ Closure Attempt

**Date:** 2026-05-01  
**Status:** open / source-to-Higgs LSZ closure attempt blocked  
**Runner:** `scripts/frontier_yt_source_to_higgs_lsz_closure_attempt.py`  
**Certificate:** `outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json`

```yaml
actual_current_surface_status: open
conditional_surface_status: conditional-support if a future scalar LSZ/source-normalization theorem is added
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The source-to-canonical-Higgs / scalar LSZ theorem remains open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Attempt

This is the explicit closure attempt against the narrowed PR #230 blocker:
find any allowed current-surface premise that fixes the scalar source
normalization `kappa_s`.

The runner checks:

- logdet additive scalar generator;
- SSB identity `m = y v / sqrt(2)`;
- EW Higgs gauge-mass diagonalization;
- SM one-Higgs gauge selection;
- same-1PI / four-fermion product;
- Feynman-Hellmann `dE/ds` response;
- `R_conn` / color projection;
- forbidden `H_unit` and observed-target shortcuts.

## Result

```text
python3 scripts/frontier_yt_source_to_higgs_lsz_closure_attempt.py
# SUMMARY: PASS=7 FAIL=0
```

No allowed current-surface premise fixes `kappa_s`.  The allowed premises are
useful, but they remain source-reparametrization covariant.  The premises that
would appear to close the gap are either forbidden, conditional, or start after
canonical Higgs normalization has already been supplied.

## Required New Theorem

A genuine closure theorem must prove all of:

- the scalar source creates an isolated physical Higgs-channel pole;
- the pole residue / inverse-propagator derivative fixes `kappa_s`;
- the source field matches the canonical kinetic normalization used by `v`;
- the proof does not use `H_unit`, observed top/`y_t`, `alpha_LM`,
  plaquette/`u0`, or reduced pilot data.

## Non-Claims

- This note does not claim retained closure.
- This note does not demote the direct production route.
- This note does not use `H_unit` matrix-element readout.
- This note does not use observed top mass or observed `y_t`.
