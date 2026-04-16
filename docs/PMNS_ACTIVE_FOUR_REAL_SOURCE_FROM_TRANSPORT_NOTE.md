# PMNS Active Four-Real Source From Transport

## Question
Once the active transport / response profile is derived at lower level, does the
remaining four-real active orbit-breaking source still need a separate theorem
object?

## Exact Result
No.

The non-averaged lower-level active transport / response profile determines the
active block exactly. From that active block:

- `xbar` is read from the `C3`-even diagonal mean
- `sigma` is read from the forward-cycle complex mean
- the residual active source is exactly the four-real vector

`(xi_1, xi_2, rho_1, rho_2)`

with:

- `xi_3 = -xi_1 - xi_2`
- `rho_3 = -rho_1 - rho_2`

So the active block rebuilds exactly from:

- `xbar`
- `sigma`
- `(xi_1, xi_2, rho_1, rho_2)`

Therefore the four-real source is no longer an extra unresolved object on the
lower-level active transport chain. It is just the centered non-averaged part
of the active transport profile.

## Boundary
This does not yet derive the lower-level active transport / response profile
itself from `Cl(3)` on `Z^3` alone. It only closes the residual four-real source
once that lower-level active profile is genuinely available.
