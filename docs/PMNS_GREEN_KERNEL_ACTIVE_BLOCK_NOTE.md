# PMNS Green-Kernel Active-Block Interface

Question:
If an independently computed projected Green-kernel / resolvent on the `hw=1`
active triplet is supplied, what does it determine?

Answer:
Yes. On the active triplet, the projected resolvent

`G_λ = (I - λ ΔD_act)^(-1)`

recovers `ΔD_act` exactly. Once that active deformation is recovered, it
decomposes uniquely into:

`(xbar, ybar, xi_1, xi_2, eta_1, eta_2, delta)`

where:

- `(xbar, ybar)` is the active seed pair
- `(xi_1, xi_2, eta_1, eta_2, delta)` is the 5-real corner-breaking source

The weak-axis seed patch is exactly the vanishing locus of the 5-real source.
So this gives an exact interface for the active microscopic block.

Boundary:

- This note does not derive the projected Green kernel itself from lower-level
  `Cl(3)` on `Z^3` dynamics.
- The route is blind to passive monomial data.
- The route is blind to the sector-orientation bit.
- So it closes the active block, but not the full top-to-bottom neutrino lane
  by itself.

Verification:

- `python3 /Users/jonBridger/Toy Physics-neutrino-majorana/scripts/frontier_pmns_green_kernel_active_block.py`
