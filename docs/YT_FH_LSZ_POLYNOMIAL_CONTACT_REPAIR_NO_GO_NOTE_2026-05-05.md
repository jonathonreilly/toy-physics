# PR #230 FH/LSZ Polynomial-Contact Repair No-Go

**Status:** exact negative boundary / polynomial contact repair not
scalar-LSZ authority
**Runner:** `scripts/frontier_yt_fh_lsz_polynomial_contact_repair_no_go.py`
**Certificate:** `outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json`

## Claim

Finite polynomial contact fitting cannot turn the current polefit8x8
finite-shell `C_ss` proxy into a scalar-LSZ Stieltjes certificate.

For a polynomial contact subtraction of degree `d`, divided differences of
orders greater than `d` are invariant.  The current finite rows have robust
complete-monotonicity sign violations through higher orders, so degree
`0..5` contact families cannot repair the current proxy.

The opposite regime is also not a certificate.  With eight finite shell rows,
a polynomial of degree at most seven can interpolate the difference between
the raw rows and many different positive Stieltjes-looking target rows.  The
runner constructs two such residual families with different finite residue
normalizations.  Both pass finite complete-monotonicity prechecks, but they
are fitted contacts, not a same-surface contact-subtraction theorem.

## Boundary

This closes the finite polynomial-contact repair shortcut.  It does not rule
out a future same-surface contact certificate, microscopic scalar-denominator
theorem, strict moment-threshold-FV/IR certificate, or a physical-response
route that bypasses scalar-source LSZ.

No retained or proposed-retained top-Yukawa closure is authorized.  The runner
does not determine scalar pole residue, `K'(pole)`, `kappa_s`, `c2`, or
`Z_match`, and it does not use `H_unit`, Ward authority, observed targets,
`alpha_LM`, plaquette, `u0`, `y_t_bare`, or bare-coupling algebra.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_polynomial_contact_repair_no_go.py
python3 scripts/frontier_yt_fh_lsz_polynomial_contact_repair_no_go.py
# SUMMARY: PASS=13 FAIL=0
```
