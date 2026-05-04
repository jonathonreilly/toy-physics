# Hydrogen / Helium Atomic Companion Note

**Date:** 2026-04-18
**Status:** bounded work-history companion; preserved from branch review, not a
**Primary runner:** [`scripts/frontier_atomic_helium_hartree_companion.py`](../../../scripts/frontier_atomic_helium_hartree_companion.py) (lattice Hartree companion; bounded result, full CI not attempted)
flagship authority surface
**Source branch reviewed:** `origin/frontier/hydrogen-helium-review`

## What Was Kept

This salvage keeps only the branch material that remained scientifically useful
after review:

1. a hydrogen lattice-spectrum companion on the retained `Cl(3)` / `Z^3`
   kinetic-plus-Coulomb surface
2. a helium Hartree upper-bound companion on the same lattice surface
3. a one-parameter helium Jastrow/VMC companion showing partial correlation
   recovery beyond the product-state ansatz

Preserved scripts:

- [frontier_atomic_hydrogen_lattice_companion.py](../../../scripts/frontier_atomic_hydrogen_lattice_companion.py)
- [frontier_atomic_helium_hartree_companion.py](../../../scripts/frontier_atomic_helium_hartree_companion.py)
- [frontier_atomic_helium_jastrow_companion.py](../../../scripts/frontier_atomic_helium_jastrow_companion.py)

## What Was Not Kept

Two branch components were rejected rather than promoted:

1. the branch-local `alpha_EM` authority packet
2. the fixed-grid helium isoelectronic-series promotion

Reasons:

- current `main` already carries the retained EW normalization lane
  (`g_1(v)`, `g_2(v)`, `sin^2(theta_W)`, `1/alpha_EM(M_Z)`), so the branch did
  not add a needed new EW authority surface
- the branch-local `alpha_EM` runner explicitly imported `M_Z`, `m_t`, `m_b`,
  and `m_c`, so its “zero SM imports” wording was not acceptable as written
- the isoelectronic sweep’s own outputs degraded strongly with increasing `Z`
  on a fixed grid and therefore did not support the stronger asymptotic story
  stated in that branch packet

## Upstream Surfaces Used Here

These companions sit on already-live upstream surfaces:

- retained lattice kinetic operator / graph Hamiltonian route
- retained or accepted Coulomb-kernel route on `Z^3`
- retained EW normalization lane on `main` for the electromagnetic coupling
  side; this salvage itself stays in dimensionless or coupling-relative units

## Hydrogen Companion

The hydrogen script solves the finite-box lattice spectral problem for

`H_g = -Δ_Z^3 - g / |r|`

and preserves the bounded companion readouts:

- `E_2 / E_1 = 0.25857` vs `0.25000` at `N = 60`, `g = 1`
- `E_3 / E_1 = 0.11132` vs `0.11111`
- `E_5 / E_1 = 0.03857` vs `0.04000`
- emergent length `r_0 = 2 / g` measured numerically as `2.00` at `g = 1`

Interpretation:

- worth keeping as a numerical companion showing the expected Rydberg-style
  pattern on the retained lattice Hamiltonian surface
- not promoted as a new theorem, continuum-limit closure, or absolute eV
  prediction

## Helium Companions

The Hartree script keeps the bounded product-state upper-bound route for the
two-electron Hamiltonian on the same kernel. At `N = 30`, `g_EM = 0.5`,
`g_nuc = 1.0`, it gives:

- `E(He^+) / E_0 = -3.7908` vs continuum `-4`
- `|E(He)| / |E(He^+)| = 1.3424`
- `IE_1 / IE_2 = 0.3424`

The Jastrow/VMC companion then improves the helium ratio from the Hartree
baseline toward the known continuum / FCI checkpoint:

- Hartree baseline at `N = 20`: `|E(He)| / |E(He^+)| = 1.3978`
- one-parameter Jastrow optimum: `1.4357`
- historical full-CI / experiment checkpoint: `1.452`

Interpretation:

- worth keeping as bounded atomic numerics on the same lattice surface
- still not a closure of the exact helium problem
- still not enough for a general multi-electron or periodic-table promotion

## Why This Lives In Work History

This salvage is real and replayable, but it does not define a new live package
claim surface. The surviving material is best read as:

- bounded atomic sanity checks on the current lattice Hamiltonian surface
- route history for any future atomic closure program
- evidence that the branch was not empty, while also avoiding overpromotion of
  its rejected EW / isoelectronic claims

## Future Reopen Path

This salvage is also the correct starting point for any future atomic lane on
`main`. The next honest steps are:

- hydrogen continuum / volume control beyond the current finite-box companion
- helium beyond Hartree plus one-parameter Jastrow, without overstating exact
  closure
- a cleaner multi-electron extension that does not lean on fixed-grid
  isoelectronic overclaims

Two things are intentionally *not* part of this atomic reopen path:

- the branch-local `alpha_EM` authority attempt, which stays rejected in favor
  of the already-live EW normalization lane on `main`
- the charged-lepton / `m_e` closure problem, which belongs under the existing
  charged-lepton hierarchy / Koide program rather than the atomic companion
  lane itself
