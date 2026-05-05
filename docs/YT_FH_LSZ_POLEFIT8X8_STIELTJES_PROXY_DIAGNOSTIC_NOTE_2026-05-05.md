# PR #230 Polefit8x8 Stieltjes Proxy Diagnostic

**Status:** exact negative boundary / current polefit8x8 `C_ss` proxy fails Stieltjes monotonicity
**Runner:** `scripts/frontier_yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic.py`
**Certificate:** `outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json`

## Claim

The current eight-mode/x8 finite-shell `C_ss(q^2)` proxy cannot be promoted
into the strict scalar-LSZ Stieltjes moment certificate.

For a positive Stieltjes scalar two-point object

```text
C(x) = int dmu(s) / (x + s),        dmu(s) >= 0,        x = q_hat^2,
```

one has

```text
C(x2) - C(x1) = -(x2 - x1) int dmu(s) / ((x2+s)(x1+s)) <= 0
```

whenever `x2 > x1`.  Monotonic non-increase is therefore a necessary
precondition before Hankel moment positivity can become load-bearing.

The current polefit8x8 combined rows are positive, but their `C_ss` proxy
increases across every adjacent shell.  The smallest adjacent increase is
more than `5 sigma` relative to the row-level standard errors recorded by the
combiner.  This blocks the shortcut from finite-shell polefit8x8 rows to a
strict positive Stieltjes scalar-LSZ certificate.

## Boundary

This does not prove that a properly contact-subtracted or denominator-derived
scalar two-point object cannot be Stieltjes.  It proves only that the current
finite-shell proxy is not the object required by the strict certificate gate.

No retained or proposed-retained top-Yukawa closure is authorized.  The future
positive route still needs a certified scalar two-point object with Stieltjes
moments, threshold-gap control, FV/IR control, and scalar-denominator or
analytic-continuation authority; or a different physical-response/source-overlap
route.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic.py
python3 scripts/frontier_yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic.py
# SUMMARY: PASS=9 FAIL=0
```
