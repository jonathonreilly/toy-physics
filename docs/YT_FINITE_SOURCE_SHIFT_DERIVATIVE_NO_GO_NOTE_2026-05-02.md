# PR #230 Finite Source-Shift Derivative No-Go

**Status:** exact negative boundary / finite source-shift slope not zero-source derivative certificate  
**Runner:** `scripts/frontier_yt_finite_source_shift_derivative_no_go.py`  
**Certificate:** `outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json`

## Claim Tested

The current FH/LSZ production chunks use one symmetric scalar-source radius:

```text
s in {-0.01, 0, +0.01}.
```

This block tests whether that three-point finite-difference slope certifies the
zero-source Feynman-Hellmann derivative `dE/ds|_0`.

It does not.

## Witness

For

```text
E(s) = E0 + a s + c s^3
```

the measured symmetric finite-difference slope at radius `delta` is

```text
[E(+delta) - E(-delta)] / (2 delta) = a + c delta^2.
```

Holding `a + c delta^2` fixed keeps `E(-delta)`, `E(0)`, `E(+delta)`, and the
finite symmetric slope fixed while changing the true derivative `a = dE/ds|_0`.

## Result

Single-radius source-response slopes are useful diagnostics, but they are not
load-bearing physical FH derivatives until a finite-source-linearity acceptance
gate exists.  A retained-grade future postprocess needs at least one of:

- multiple source-shift radii showing the zero-radius limit;
- a retained analyticity/response-bound theorem excluding cubic contamination;
- a production acceptance gate that makes the finite-source derivative stable.

This remains in addition to the scalar LSZ pole residue, FV/IR/zero-mode, and
canonical-Higgs identity gates.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It does
not treat finite source-shift slopes as physical `dE/dh`; it does not set
`kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use `H_unit`,
`yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`, plaquette,
or `u0` as proof authority.

## Next Action

Add a finite-source-linearity acceptance gate with at least two source radii,
or derive a retained response-bound theorem.  Until then, single-radius
`dE/ds` slopes remain diagnostics even when production chunks complete.
