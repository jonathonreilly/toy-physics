# PMNS Microscopic D Seven-Real Last Mile

## Question
After the current native selector, transport/moment, and passive phase-reduction
laws, how much of the PMNS-relevant microscopic operator `D` is still not fixed?

## Exact Result
On the retained one-sided minimal PMNS classes:

- `tau` is already fixed natively by moment-support cardinality
- `q` is already fixed natively by directional support moments
- `xbar` is already fixed natively by the `C3`-even active moment
- `sigma = (c_1 + c_2 + c_3)/3` on the forward cycle is already fixed natively
  by the `C3`-forward active moment
- passive monomial phases are removable, so passive data reduce to three real
  moduli `(|a_1|, |a_2|, |a_3|)`

The only remaining active data are four real orbit-breaking coordinates:

- `xi_1, xi_2` on the diagonal channel
- `rho_1, rho_2` on the cycle channel relative to the derived complex mean `sigma`

Therefore the unreduced PMNS-relevant `D` law is not a generic matrix law. It
is exactly a seven-real last mile:

`(|a_1|, |a_2|, |a_3|, xi_1, xi_2, rho_1, rho_2)`

together with the already derived native data `(tau, q, xbar, sigma)`.

## Boundary
This is still a reduction theorem, not full sole-axiom closure. It does not yet
derive those seven real values from `Cl(3)` on `Z^3`.
