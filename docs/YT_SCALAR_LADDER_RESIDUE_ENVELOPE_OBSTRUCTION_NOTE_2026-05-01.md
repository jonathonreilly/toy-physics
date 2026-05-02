# Top-Yukawa Scalar Ladder Residue-Envelope Obstruction

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar ladder residue-envelope obstruction
**Runner:** `scripts/frontier_yt_scalar_ladder_residue_envelope_obstruction.py`
**Certificate:** `outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary / scalar ladder residue-envelope obstruction
conditional_surface_status: conditional-support if a retained finite-volume/IR/zero-mode residue theorem is derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The pole-tuned residue proxy is not single-valued across allowed current-surface prescriptions."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

The scalar ladder determinant and eigen-derivative blocks separated two facts:

```text
lambda_max(pole) = 1                 # pole location
d lambda_max / d p^2 at the pole     # LSZ residue input
```

This block asks whether finite ladder data can already bound the second
quantity once the first is normalized away.  For each finite ladder surface,
the runner tunes the scalar-channel coupling to its own pole and computes the
pole-tuned residue proxy:

```text
g = 1 / lambda_max(0)
residue_proxy = |1 / d(1 - g lambda_max)/dp_hat^2|
              = |lambda_max(0) / lambda'_max(0)|
```

## Result

The pole-tuned residue proxy remains prescription dependent.

Validation:

```text
python3 scripts/frontier_yt_scalar_ladder_residue_envelope_obstruction.py
# SUMMARY: PASS=9 FAIL=0
```

Witnesses from the certificate:

- the full pole-tuned proxy envelope has spread greater than `5x`;
- at `N=5`, fixed `mu_IR^2=0.05`, local-source zero-mode removal changes the
  proxy by more than `5x` relative to zero-mode inclusion;
- at the same point, the removed-zero-mode local and normalized point-split
  projectors differ by more than `2x`;
- the removed-zero-mode finite-volume sequence is nonmonotone across
  `N=3,4,5`;
- naive `1/N` fits already show that the small finite-volume data are not a
  retained continuum prescription.

Therefore the finite Bethe-Salpeter ladder route still cannot supply
`kappa_s`, a scalar LSZ residue, or the same-source FH/LSZ readout.  The
retained route needs the zero-mode prescription, finite-volume and IR limiting
order, source/projector normalization, and a finite-`N_c=3` continuum bound, or
direct production pole-derivative data.

## Claim Boundary

This block does not claim retained or proposed-retained top-Yukawa closure.  It
does not set `kappa_s = 1`, does not use `H_unit` or `yt_ward_identity`, and
does not use observed target values, alpha/plaquette/u0, or reduced pilots as
proof inputs.
