# PMNS Passive Green-Kernel Monomial Interface

## Question

If an independently computed projected Green-kernel on the passive `hw=1`
monomial block is supplied, what does it determine?

## Exact Result

Yes.

For the passive triplet block

`D_pass = diag(a_1,a_2,a_3) P_q`

the projected resolvent

`G_λ^pass = (I - λ D_pass)^(-1)`

recovers `D_pass` exactly, since

`D_pass = (I - (G_λ^pass)^(-1)) / λ`.

The already native support-moment law fixes the offset `q`, and conjugation by
`P_q^dag` then fixes the passive coefficient triple:

`diag(a_1,a_2,a_3) = D_pass P_q^dag`.

So the passive monomial value interface is exactly closed by the passive
projected Green kernel together with the native support-moment selector for
`q`.

## Boundary

This note does not derive the passive projected kernel itself from lower-level
`Cl(3)` on `Z^3` dynamics. It is blind to the active microscopic block and to
the sector orientation bit. It closes the passive monomial data only.
