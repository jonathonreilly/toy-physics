# Freeze-Out from Lattice Thermodynamics -- why the relic step remains open

**Date:** 2026-04-12  
**Status:** bounded gap memo -- direct lattice inputs are useful, but the full freeze-out / relic-abundance step is not yet derived from the graph axioms alone

## Artifact chain

- [`scripts/frontier_freezeout_from_lattice.py`](../scripts/frontier_freezeout_from_lattice.py)
- Log: `logs/YYYY-MM-DD-freezeout_from_lattice.txt`

## Problem

The DM ratio `R = Omega_DM/Omega_b` was being presented as if the freeze-out
layer were fully structural. That is too strong. The current review state
supports three narrower statements:

1. the lattice contact-propagator lane gives a real enhancement observable
2. the standard freeze-out formula remains a thermodynamic / cosmological input
3. the exact relic-abundance ratio is still review-only until a native
   replacement for Boltzmann + Friedmann is derived

This note records the exact boundary instead of pretending the boundary is
closed.

## What the lattice does give

The direct lattice contact-propagator lane is meaningful:

- build `H_free` and `H_Coulomb` as finite radial Hamiltonians
- invert `(E - H)` directly
- read off the contact resolvent element `G(0,0;E)`
- compare the attractive Coulomb channel to the free channel on the same grid

That yields a genuine lattice observable: a contact enhancement relative to the
free case. It is an input to the DM analysis, not the relic-abundance closure.

## What remains imported

The freeze-out step still depends on the standard thermal relic machinery:

- the Boltzmann equation for number-density evolution
- the Hubble / Friedmann expansion term `3Hn`
- a decoupling criterion `Gamma_ann = H`
- thermal equilibrium / Maxwell-Boltzmann statistics
- a perturbative annihilation ansatz `sigma v ~ pi * alpha_s^2 / m^2`
- the standard freeze-out parameter `x_F ~ 25`

Those ingredients are not derived from the lattice axiom by the current code.
They are the exact imported machinery that still has to be removed if the
paper is to claim a fully native relic-abundance derivation.

## What is still conditional

The usual `g_* = 106.75` count can be reproduced as a consistency check once
the full SM field content is assumed. That does not by itself solve the relic
problem:

- the count depends on the full chiral matter assignment
- the freeze-out parameter still comes from the Boltzmann equation
- the ratio `R` still depends on the expansion history

So `g_*` is at best a conditional counting identity here, not the missing
relief valve that closes freeze-out.

## Honest conclusion

The freeze-out gap is still open.

The strongest safe statement is:

- direct finite-lattice contact enhancement is real
- the continuum Sommerfeld formula remains a matched continuum interpretation
- the full relic abundance still imports Boltzmann/Friedmann freeze-out
- `R = Omega_DM/Omega_b` is therefore still review-only

If the paper wants a native relic-abundance theorem, it still needs one of:

1. a graph-native master equation whose thermodynamic limit reproduces the relic
   abundance without importing the Boltzmann/Friedmann layer, or
2. a proof that the existing Boltzmann/Friedmann layer is a theorem of the
   lattice dynamics rather than an external cosmological assumption

