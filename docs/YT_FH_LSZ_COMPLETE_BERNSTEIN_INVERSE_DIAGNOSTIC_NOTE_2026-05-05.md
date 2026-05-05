# PR #230 FH/LSZ Complete-Bernstein Inverse Diagnostic

**Status:** exact negative boundary / current polefit8x8 inverse proxy fails complete-Bernstein monotonicity.

**Runner:** `scripts/frontier_yt_fh_lsz_complete_bernstein_inverse_diagnostic.py`

**Output:** `outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json`

## Result

The completed L12 eight-mode/x8 scalar proxy is not a strict scalar-LSZ
denominator certificate.  For a nonzero positive Stieltjes scalar propagator
`C(x)`, the reciprocal `Gamma(x)=1/C(x)` is a complete Bernstein function.
A necessary consequence is monotone non-decrease in `x=q_hat^2`.

The current `Gamma_ss_real_proxy` is positive but decreases across every
adjacent shell in the combined polefit8x8 summary.  This independently blocks
the tempting finite-shell shortcut from production `C_ss` rows to scalar-LSZ
denominator authority.

## Claim Boundary

This is a diagnostic boundary, not physics closure.  It does not define
`y_t`, does not set `kappa_s`, `c2`, or `Z_match` to one, and does not use
`H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`
as proof authority.

The clean positive scalar-LSZ route now requires a certified
contact-subtracted scalar object or a microscopic scalar-denominator theorem,
then rerunning Stieltjes moment, Pade/Stieltjes bounds, complete-Bernstein
inverse, threshold, and FV/IR gates.  Otherwise closure must come from
certified `O_H/C_sH/C_HH` pole rows or genuine same-source W/Z response rows.

## Validation

```bash
python3 scripts/frontier_yt_fh_lsz_complete_bernstein_inverse_diagnostic.py
```
