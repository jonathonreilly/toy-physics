# PMNS Corner Transport Active Block

**Date:** 2026-04-16  
**Status:** bounded - bounded or caveated result note
**Script:** `scripts/frontier_pmns_corner_transport_active_block.py`

## Question

What does direct `hw=1` corner-to-corner transport on the active microscopic
block determine?

## Bottom line

The direct corner-transport route gives a genuine native law on the active
microscopic block:

- the orbit-average even transport mode recovers the weak-axis seed pair
  `(xbar, ybar)`
- the C3-odd transport asymmetry recovers the branch bit
- the weak-axis seed patch is the vanishing locus of the breaking carrier

But orbit-averaged corner transport is still blind to the active 5-real
corner-breaking source. So the route is dynamical and native, but not a full
microscopic closure theorem.

## Exact transport law

For the active hw=1 triplet, the direct corner-to-corner transport matrix is

`T_act = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C`.

Its C3 orbit moments are:

`t_even = tr(T_act) / 3`

`t_fwd = (T_12 + T_23 + T_31) / 3`

`t_bwd = (T_13 + T_32 + T_21) / 3`

The native outputs are:

- `xbar = Re(t_even)`  (exact for any δ; t_even = xbar)
- `ybar = Re(t_fwd)`   (exact on the aligned weak-axis patch δ = 0)
- branch bit = `0` if `Im(t_fwd) >= Im(t_bwd)`, else `1`

The branch bit is read from the **C3-odd, CP-odd imaginary** asymmetry of the
forward vs backward cycle amplitude. With T_act = diag(x) + diag(y_eff) C and
y_eff = (y_1, y_2, y_3 e^{iδ}), the only nonzero off-diagonal entries lie on
the forward cycle, so t_bwd = 0 and Im(t_fwd) = y_3 sin(δ) / 3. This
quantity flips sign under δ → −δ — the operational definition of branch
orientation. The corresponding real-part comparison Re(t_fwd) vs Re(t_bwd)
does **not** flip under δ → −δ (cos is even) and is therefore not a branch
selector. Earlier drafts of this note used the Re comparison; the runner has
always used the Im comparison and the runner is the authoritative
implementation. The note now matches the runner.

So the transport route fixes the seed pair (in the aligned patch) and the
branch orientation exactly on the active microscopic block.

## Boundary

The same transport averaging is blind to the five real corner-breaking
coordinates

`(xi_1, xi_2, eta_1, eta_2, delta)`.

Two distinct off-seed active operators can share the same orbit-averaged
transport moments while carrying different breaking data. So the route does not
close the full microscopic value law by itself.

## Meaning for the lane

This is a positive native result, and it is dynamic rather than purely static.
It gives the active block a transport law, but the full `Cl(3)` on `Z^3`
closure still needs an additional value law for the 5-real corner source.

## Verification

```bash
python3 scripts/frontier_pmns_corner_transport_active_block.py
```
