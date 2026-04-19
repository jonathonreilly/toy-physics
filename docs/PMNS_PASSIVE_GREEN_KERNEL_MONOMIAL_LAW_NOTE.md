# PMNS Passive Green-Kernel Monomial Law

## Question

If the passive projected Green-kernel is supplied through lower-level passive
source-response columns, what does it determine?

## Exact Result

The lower-level passive response columns determine the passive projected kernel
exactly. That projected kernel determines the passive monomial block exactly,
and the derived passive block determines:

- the offset `q` through the native support-moment law
- the passive coefficient triple through conjugation by `P_q^dag`

So the passive monomial data are exactly closed on the lower-level response
chain by:

- passive response columns
- passive projected kernel
- native support-moment selector for `q`

## Boundary

This note does not derive the passive response columns themselves from
`Cl(3)` on `Z^3` alone. It is blind to the active microscopic block and to the
sector orientation bit. It closes the passive monomial data only on the
lower-level response chain.
