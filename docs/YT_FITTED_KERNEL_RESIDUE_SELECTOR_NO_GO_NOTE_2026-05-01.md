# PR #230 Fitted Scalar-Kernel Residue Selector No-Go

**Status:** exact negative boundary / fitted scalar-kernel residue selector
no-go

## Question

After unit taste projection, the finite scalar ladder has no pole at the
retained scout kernel strength.  A possible shortcut is to fit a constant
scalar-channel multiplier:

```text
g_eff * lambda_unit(0) = 1
```

and then treat the same finite row as the scalar pole for the FH/LSZ readout.

This is not a retained closure route.

## Calculation

For each finite crossing witness from the zero-mode-removed ladder search, the
unit taste projection gives:

```text
lambda_unit = lambda_raw / 16
g_eff = 1 / lambda_unit
```

The denominator derivative of the fitted pole is then:

```text
D'(p^2) = -g_eff d(lambda_unit)/dp^2
        = -(1/lambda_unit) (1/16) d(lambda_raw)/dp^2
```

So the fitted residue proxy becomes:

```text
1 / |D'| = lambda_raw / |d lambda_raw / dp^2|
```

The taste normalization factor cancels only because `g_eff` was fitted to the
finite pole.  The residue is still controlled by the finite derivative ratio,
and `g_eff` is an underived scalar-channel normalization.

## Result

The runner matches the four finite crossing rows and computes the fitted
residue proxy.  The current rows require:

```text
g_eff range: 2.26091440260 to 10.9336833038
fitted residue proxy spread: 2.00925585041
```

This spread is enough to show that the finite-row choice remains load-bearing.
More importantly, the fitted pole selector is not a theorem: it imports the
missing scalar kernel normalization instead of deriving the interacting
denominator and `K'(x_pole)`.

## Claim Boundary

This block does not claim scalar LSZ closure.  It proves only:

```text
fitted finite-pole selector != retained scalar denominator theorem
```

The remaining routes are unchanged:

- derive the momentum-dependent scalar kernel and `K'(x_pole)`;
- derive the finite-volume/taste/projector residue limit;
- or measure the same-source scalar pole derivative in production FH/LSZ data.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fitted_kernel_residue_selector_no_go.py
python3 scripts/frontier_yt_fitted_kernel_residue_selector_no_go.py
# SUMMARY: PASS=8 FAIL=0
```
