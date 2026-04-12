# Graph-Native Freeze-Out and the Relic Gap

**Date:** 2026-04-12  
**Status:** bounded graph-native freeze-out theorem; full relic abundance remains open

## What This Lane Attacks

The old DM-relic objection was that the lane still imported the standard
Boltzmann/Friedmann freeze-out law. The direct lattice contact-propagator
result is now real, but the full relic-abundance calculation still needed an
internal master equation and a native dilution law.

This note records the strongest result that can be derived from the graph
framework itself:

1. the exact graph-volume dilution identity,
2. the homogeneous graph-native master equation for pair annihilation,
3. the native decoupling criterion `Gamma_ann ~ Gamma_dil`,
4. the exact point where physical cosmology still enters.

## Derived Result

Let `N(t)` be the total occupation and `V(t)` the graph volume. Define

`Y(t) = N(t) / V(t)`.

Then the quotient rule gives the exact identity

`dY/dt + (d ln V / dt) Y = (1/V) dN/dt`.

If the graph master equation is pair annihilation with contact enhancement,

`dN/dt = -lambda_eff * V * (Y^2 - Y_eq^2)`,

then the density obeys

`dY/dt + Gamma_dil * Y = -lambda_eff * (Y^2 - Y_eq^2)`,

with `Gamma_dil = d ln V / dt` and `lambda_eff = lambda_0 * S_contact`.

This is the strongest non-imported freeze-out theorem in the lane.

## What Is Now Native

- The dilution term is graph-native and exact.
- The annihilation kernel can carry the bounded contact enhancement from the
  lattice Green's-function lane.
- The freeze-out threshold is native:

  `Y_crit = Gamma_dil / lambda_eff`

  so decoupling begins when `Gamma_ann ~ Gamma_dil`.

- A graph-clock decoupling time can be solved without reference to physical
  cosmology once a graph equilibrium profile is chosen.

## Exact Obstruction

The physical relic-abundance step still requires two identifications that are
not derived here:

- `Gamma_dil -> 3H(t)`
- graph equilibrium `Y_eq` -> thermal equilibrium `n_eq(T)`

Those are the remaining cosmological inputs. Until they are derived, the
current result is a graph-native freeze-out law, not the full
`Omega_DM / Omega_b` prediction.

## Status

- `Solved`: graph-native master equation, exact dilution law, native
  decoupling criterion, graph-clock freeze-out threshold.
- `Open`: mapping to physical Hubble expansion, mapping to temperature, full
  relic-abundance law.

## Paper Use

This note should be cited as the strongest framework-side result in the DM
lane. It narrows the relic obstruction to one explicit step: the map from
graph growth to the physical thermal history.
