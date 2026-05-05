# PR #230 FH/LSZ Contact-Subtraction Identifiability Boundary

**Status:** exact negative boundary / contact-subtraction identifiability obstruction
**Runner:** `scripts/frontier_yt_fh_lsz_contact_subtraction_identifiability.py`
**Certificate:** `outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json`

## Claim

The current finite polefit8x8 rows do not select a contact subtraction.

After the current `C_ss(q_hat^2)` proxy failed the unsubtracted Stieltjes
monotonicity test, a tempting repair is to subtract a local contact term and
then retest the residual.  The finite rows do not fix that local term.  For an
affine local ambiguity

```text
C_sub(x) = C_raw(x) - a x,        x = q_hat^2,
```

any slope `a` above the largest adjacent raw slope makes the finite residual
non-increasing, while any slope below `min_i C_raw(x_i)/x_i` keeps it positive
on the measured shells.  On the current rows that interval is nonempty.  Two
different slopes in the interval both pass the necessary positive
non-increasing precheck, but they change the high-momentum residual by many
row standard errors.

Therefore monotonicity-restoration alone cannot define the scalar LSZ object,
the pole residue, or `kappa_s`.  A same-surface contact-subtraction certificate
or microscopic scalar-denominator theorem is still required before applying
Stieltjes moment tests to a subtracted object.

## Boundary

This is not a no-go for a properly derived contact-subtracted scalar two-point
function.  It blocks only the shortcut where a contact term is chosen from the
finite rows or from the desire to restore Stieltjes monotonicity.

No retained or proposed-retained top-Yukawa closure is authorized.  This note
does not set `kappa_s=1`, `c2=1`, or `Z_match=1`, and it does not use H-unit,
Ward authority, observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_contact_subtraction_identifiability.py
python3 scripts/frontier_yt_fh_lsz_contact_subtraction_identifiability.py
# SUMMARY: PASS=10 FAIL=0
```
