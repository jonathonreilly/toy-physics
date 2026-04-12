# DM Ratio Structural Note

## Summary

The dark matter ratio `R = Omega_DM / Omega_b = 5.48` is still a mixed object.
One ingredient is now genuinely stronger than before:

- the direct finite-lattice contact-propagator enhancement in the attractive
  Coulomb channel is a real lattice observable

The remaining relic-abundance step is not yet structural:

- the freeze-out parameter `x_F`
- the Boltzmann equation
- the Friedmann / Hubble expansion term
- the perturbative annihilation ansatz

Those remain imported machinery unless a native replacement is derived.

## What is actually established

The DM analysis can currently be separated into two layers:

1. `S_vis` or contact enhancement is a lattice observable on the discrete
   Hamiltonian
2. `Omega_DM/Omega_b` requires the freeze-out relic calculation, which still
   uses standard cosmology

So the bounded result is the contact enhancement itself, not the full relic
ratio.

## Direct lattice contact-propagator input

The new direct lattice computation gives:

- `H_free` and `H_Coulomb` as finite radial Hamiltonians
- `(E - H)^{-1}` at contact
- a finite enhancement in the attractive channel relative to the free case

This is valuable input for the DM story. It is not the missing relic-abundance
derivation.

## What remains imported

The current freeze-out chain still imports:

- Boltzmann number-density evolution
- `H(T) = sqrt(8 pi G rho / 3)`
- thermal equilibrium and equipartition
- a perturbative `sigma v` model
- the decoupling criterion `Gamma_ann = H`

Without replacing that machinery, the full `Omega_DM/Omega_b` result is still
review-only.

## Honest status

The safest paper-facing statement is now:

- bounded direct lattice contact-propagator observable: yes
- continuum Sommerfeld equality: supported by the analytic proof plus the
  direct lattice computation, but still separate from the relic-abundance step
- full freeze-out / relic-abundance closure: open

That is the clean boundary to use in the manuscript and review docs.
