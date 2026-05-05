# PR230 Scalar-LSZ Carleman/Tauberian Determinacy Attempt

**Status:** exact negative boundary / Carleman/Tauberian scalar-LSZ
determinacy not derivable from current finite PR230 rows
**Runner:** `scripts/frontier_yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt.py`
**Certificate:** `outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json`

## Purpose

This block tests a stricter outside-math scalar-LSZ route: can
Carleman/Stieltjes moment determinacy or Tauberian threshold machinery replace
the missing scalar pole-residue authority?

## Result

The attempt does not close.  The runner constructs two positive finite atomic
Stieltjes measures whose moments agree through the checked finite prefix but
whose isolated pole weights differ.  That is enough to block any route that
treats finite FH/LSZ shell rows or finite moment rows as a unique scalar pole
residue.

Carleman determinacy is an infinite-tail statement:

```text
sum_n m_{2n}^{-1/(2n)} = infinity
```

A finite prefix can produce only a finite partial sum.  Tauberian threshold
reconstruction likewise needs same-surface large-order/asymptotic or threshold
density control, plus contact subtraction and FV/IR limiting order.  Current
PR230 rows supply neither infinite-tail nor asymptotic authority.

## Future Positive Contract

A positive scalar-LSZ moment certificate must provide:

- same-surface subtracted scalar correlator and source scheme;
- infinite moment sequence or rigorous same-surface tail/asymptotic bounds;
- Carleman or equivalent Stieltjes determinacy certificate;
- Tauberian threshold/gap authority;
- finite-volume/IR/zero-mode limiting-order certificate;
- isolated scalar pole and positive tight residue interval;
- firewall rejecting finite-prefix selectors, PSLQ/value recognition,
  observed targets, `H_unit`/Ward authority, `alpha_LM`/plaquette/`u0`, and
  unit `kappa_s/c2/Z_match` shortcuts.

## Boundary

No retained or `proposed_retained` PR230 closure is claimed.  This block does
not write an infinite-moment, Carleman/Tauberian, contact, threshold, or FV/IR
certificate.  It does not set `kappa_s`, `c2`, or `Z_match` to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt.py
# SUMMARY: PASS=14 FAIL=0
```
