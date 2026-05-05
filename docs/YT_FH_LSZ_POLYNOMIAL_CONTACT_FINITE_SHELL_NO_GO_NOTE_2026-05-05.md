# PR #230 FH/LSZ Polynomial-Contact Finite-Shell No-Go

**Status:** exact negative boundary / finite-shell polynomial contact
non-identifiability no-go
**Runner:**
`scripts/frontier_yt_fh_lsz_polynomial_contact_finite_shell_no_go.py`
**Certificate:**
`outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json`

## Claim

The current finite polefit8x8 shell rows cannot be promoted into scalar-LSZ
authority by allowing an arbitrary higher-degree local polynomial contact
subtraction.

For `n` distinct shell points `x_i` and measured rows `C_i`, any chosen finite
residual values `S_i` can be represented as

```text
C_i - P(x_i) = S_i
```

for a unique polynomial `P` of degree at most `n-1`.  Therefore finite-shell
Stieltjes checks after an unconstrained polynomial contact subtraction do not
identify the physical scalar two-point object, pole residue, or `kappa_s`.

## Executable Witness

The runner loads the current combined polefit8x8 artifact and constructs two
strict positive one-pole Stieltjes residuals,

```text
S(x) = residue / (x + mass_sq),
```

using the same zero-momentum row but different `mass_sq` choices.  For each
residual it interpolates the degree-7 polynomial contact term that makes the
residual reproduce the measured eight-shell `C_ss` rows.

Both witnesses:

- reconstruct the current rows with max error below `1e-10`;
- pass all finite complete-monotonicity divided-difference checks;
- assign different pole locations and residues.

The two witness residues differ by a factor of `5.000`, and the pole locations
are separated by `1.800` in the shell variable.  That difference is not a
statistical fluctuation; it is contact-scheme freedom left open by admitting
an unconstrained polynomial contact term.

## Boundary

This is not a statement that either polynomial contact term is the physical
microscopic contact term.  It is the opposite: finite rows plus arbitrary
polynomial contact interpolation are too permissive.  A future positive route
must supply at least one of:

- a same-surface microscopic contact/denominator theorem;
- a strict polynomial-contact certificate with independent normalization and
  degree/order authority;
- a physical-response route that bypasses scalar-source normalization.

## Validation

```text
python3 scripts/frontier_yt_fh_lsz_polynomial_contact_finite_shell_no_go.py
# SUMMARY: PASS=11 FAIL=0
```

No retained or `proposed_retained` top-Yukawa closure is authorized.  This
artifact does not use `H_unit`, Ward authority, observed targets, `alpha_LM`,
plaquette/u0, `c2=1`, `Z_match=1`, or `kappa_s=1`.
