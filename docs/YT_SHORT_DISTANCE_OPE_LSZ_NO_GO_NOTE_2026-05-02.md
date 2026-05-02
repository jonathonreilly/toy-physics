# PR #230 Short-Distance/OPE LSZ Shortcut No-Go

**Status:** exact negative boundary / short-distance OPE not scalar LSZ closure  
**Runner:** `scripts/frontier_yt_short_distance_ope_lsz_no_go.py`  
**Certificate:** `outputs/yt_short_distance_ope_lsz_no_go_2026-05-02.json`

## Claim Tested

This block tests whether the PR #230 scalar source-to-Higgs blocker can be
closed from UV source normalization, short-distance operator matching, or a
finite set of OPE coefficients of the same-source scalar two-point function.

It cannot.  Finite OPE data determine finitely many large-momentum spectral
moments.  They do not determine the isolated IR pole residue
`<0|O_s|h>^2`, the inverse-propagator derivative `D'_ss(pole)`, or the
identity between the source-created scalar pole and the canonical Higgs radial
mode used by `v`.

## Executable Witness

The runner constructs positive pole-plus-continuum models

```text
C_ss(Q^2) = Z_p / (Q^2 + m_p^2) + sum_i w_i / (Q^2 + M_i^2)
```

and fixes the first four large-`Q` coefficients

```text
C_ss(Q^2) ~ a_0/Q^2 - a_1/Q^4 + a_2/Q^6 - a_3/Q^8.
```

For several different values of the pole residue `Z_p`, a positive continuum
weight vector reproduces the same finite OPE coefficients.  The high-`Q`
correlators agree asymptotically, but the IR pole residue changes by a factor
of ten and the corresponding fixed-`dE/ds` Yukawa proxy changes by more than a
factor of three.

## Result

Short-distance/OPE information is useful support for source/operator
bookkeeping, but it is not the missing scalar LSZ theorem.  The current route
still needs one of the following:

- a microscopic scalar denominator and pole-saturation/threshold theorem;
- production same-source pole data accepted by model-class/FV/IR gates;
- a source-pole-to-canonical-Higgs identity certificate.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It does
not set `kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use
`H_unit`, `yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`,
plaquette, or `u0` as proof authority.

## Next Action

Continue seed-controlled FH/LSZ production chunks, and in the foreground attack
the genuinely IR scalar-denominator/threshold or source-pole-to-canonical-Higgs
identity theorem.  Do not use UV operator normalization or finite OPE
coefficients as `kappa_s`.
