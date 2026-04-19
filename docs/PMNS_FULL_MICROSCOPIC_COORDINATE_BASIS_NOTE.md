# PMNS Full Microscopic Coordinate Basis

**Status:** exact structural theorem on the PMNS-relevant microscopic quotient  
**Script:** [`frontier_pmns_full_microscopic_coordinate_basis.py`](../scripts/frontier_pmns_full_microscopic_coordinate_basis.py)

## Question

Once the fixed lepton supports are in hand, what are the exact PMNS-relevant
coordinates of the full microscopic operator?

## Answer

Modulo spectator completion inside the charge sectors, the exact PMNS-relevant
microscopic coordinates are

`(tau, q, a_1, a_2, a_3, xbar, ybar, xi_1, xi_2, eta_1, eta_2, delta)`.

Here

- `tau` is the sector-orientation bit
- `(q, a_i)` are the passive monomial data
- `(xbar, ybar)` are the active seed-pair data
- `(xi_1, xi_2, eta_1, eta_2, delta)` are the active `5`-real corner source

The exact microscopic chain is therefore

`D -> (D_0^trip, D_-^trip) -> (tau, q, a_i, xbar, ybar, xi, eta, delta)`.

## Theorem

**Theorem (PMNS full microscopic coordinate basis).**

On the one-sided minimal PMNS classes:

1. the full microscopic operator reduces exactly to its charge-sector Schur
   triplet pair `(D_0^trip, D_-^trip)`,
2. that triplet pair decomposes exactly into
   - sector orientation,
   - passive monomial law,
   - active seed pair,
   - active corner-breaking source,
3. those coordinates reconstruct the triplet pair exactly,
4. the residual sheet bit is downstream of the active operator and is not an
   independent microscopic basis coordinate.

## Structural Content

The decomposition is not phenomenological bookkeeping. It is an exact
coordinate basis for the PMNS-relevant microscopic quotient:

- the passive lane is exactly monomial,
- the active lane is exactly canonical `I + C` support plus its seed/breaking
  split,
- the sheet bit is readable from the active operator through the existing
  closure stack and does not enlarge the microscopic basis.

So once the full microscopic operator `D` is reduced to its charge-sector Schur
pair, there is no further hidden PMNS-side object.

## Boundary

This theorem fixes the **carrier** of the PMNS-relevant microscopic data. It
does **not** yet fix the values of those coordinates from `Cl(3)` on `Z^3`.

That is the point at which the lane was later reduced to the sole-axiom
question:

- does `Cl(3)` on `Z^3` by itself force the coordinate values,
- or does it fix only the carrier?

## Verified Outputs

The runner verifies:

- exact reduction of the full microscopic operator to the Schur triplet pair
- exact extraction of `tau`
- exact extraction of passive offset `q`
- exact extraction of passive coefficients `a_i`
- exact extraction of the active seed pair `(xbar, ybar)`
- exact extraction of the active `5`-real corner source
- exact reconstruction of the triplet pair from those coordinates

## Conclusion

The PMNS-relevant microscopic quotient has a complete exact coordinate basis.
What remains after this theorem is not another hidden PMNS object, but only the
value law for those coordinates from `Cl(3)` on `Z^3`.
