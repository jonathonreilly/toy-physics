# Wilson Two-Body Open-Lattice Note

**Date:** 2026-04-11  
**Status:** bounded-retained candidate on frontier; not yet promoted  
**Scripts:**  
- `frontier_wilson_two_body.py`  
- `frontier_wilson_two_body_open.py`  
- `frontier_wilson_two_body_laws.py`

## Question

Does the Wilson-fermion two-orbital Hartree lane produce a genuine mutual
attraction signal once the staggered parity oscillation is removed, and if so,
how much of a Newton-like law can actually be retained?

## Periodic Wilson Result

`frontier_wilson_two_body.py` gives a real narrow clean window:

- `G=5`
- `d=3,4`
- both `mu^2 = 0` and `mu^2 = 0.22`
- early-time mutual acceleration is clean and attractive with `SNR ~ 4-5`

But it also fails immediately beyond that window:

- `d=5,6` flips sign on the same `side=9` periodic lattice
- all larger `G` become noisy

So the periodic Wilson result is **not** Newton-law closure. It is a clean
short-range window on a small periodic box.

## Open-Boundary Wilson Result

`frontier_wilson_two_body_open.py` removes the periodic-image contamination and
tests the same lane on open 3D Wilson lattices.

Audited surface:

- `side = 11, 13`
- `G = 5`
- `mu^2 = 0.22`
- separations `d = 3,4,5,6`

Result:

- `8/8` configurations attractive
- `8/8` configurations clean (`SNR > 2`)

Representative rows:

- `side=11, d=3`: `a_mut = -0.566674 ± 0.058502` (`SNR=9.69`)
- `side=11, d=6`: `a_mut = -0.056988 ± 0.006457` (`SNR=8.83`)
- `side=13, d=3`: `a_mut = -0.567354 ± 0.058224` (`SNR=9.74`)
- `side=13, d=6`: `a_mut = -0.056692 ± 0.006955` (`SNR=8.15`)

The controls are also much cleaner than in the periodic box:

- `FREE` drift is tiny on the larger open surfaces
- `SELF_ONLY` stays near flat or weakly outward
- `SHARED` closes inward strongly

So the Wilson mutual-attraction signal is real on the open surface.

## Law Sweeps

`frontier_wilson_two_body_laws.py` extends the open-lattice result.

### Distance falloff

Surface:

- `side = 11, 13, 15`
- `G = 5`
- `mu^2 = 0.22`
- clean attractive rows only

Fits:

- global clean fit: `|a_mut| ~ d^-3.406` (`R^2 = 0.9935`)
- `side=11`: `d^-3.139` (`R^2 = 0.9968`)
- `side=13`: `d^-3.313` (`R^2 = 0.9960`)
- `side=15`: `d^-3.500` (`R^2 = 0.9939`)

This is a very clean power law, but it is **not** Newtonian `1/r^2`.

### Partner-source scaling

At `side=13`, `d=4`:

- `mB = 0.5`: `a_mut = -0.206150`
- `mB = 1.0`: `a_mut = -0.246222`
- `mB = 1.5`: `a_mut = -0.314107`
- `mB = 2.0`: `a_mut = -0.346657`
- `mB = 3.0`: `a_mut = -0.503814`

Fit:

- `|a_mut| ~ mB^0.483` (`R^2 = 0.9363`)

So the partner-source dependence is monotone and real, but clearly sublinear
on that screened surface.

## Both-Masses Audit

`frontier_newton_both_masses.py` checks the newer open-surface,
weak-screening surface with `mu^2 = 0.001`, but it still does **not** close a
full `M_A M_B` law.

What the runner actually varies:

- `source_A`, `source_B` in the Poisson source
- two unit-normalized orbitals with the **same** Wilson Hamiltonian mass term

So it measures source-linearity slices, not a full inertial-times-source law.

Direct rerun on that surface:

- anchor slice `a_on_A` vs `source_B` at `source_A = 1.0`: `R^2 = 0.9956`
- anchor slice `a_on_B` vs `source_A` at `source_B = 1.0`: `R^2 = 1.0000`
- full-grid normalized response `a_on_A / source_B`: `CV = 62.9%`
- equal-and-opposite acceleration proxy `a_A / a_B`: fails strongly on the full grid

So the honest read is:

- the open Wilson lane supports a real distance-law calibration
- it also supports slice-wise source linearity
- it still does **not** support retained full Newton closure

## Honest Interpretation

The Wilson lane has improved substantially over the staggered two-body lane:

- mutual attraction survives when tested with a genuine two-orbital control
- the open-lattice surface removes the small-box periodic sign flip
- the signal is clean enough to fit

But the law that emerges is:

- **real**
- **clean**
- **non-Newtonian**

Current best statement:

> Open-boundary Wilson two-orbital Hartree dynamics produces a robust mutual
> attraction channel on the audited `G=5`, `mu^2=0.22` surface, with a clean
> screened distance falloff `|a_mut| ~ d^-3.4` and sublinear partner-source
> scaling `|a_mut| ~ m_B^0.48`.

That is scientifically meaningful, but it is not the Nature-threshold
“emergent Newton law” claim.

## Screening-Mass Addendum

The later `mu^2` sweep narrows the interpretation further:

- `mu^2 = 0.22` gives `alpha = -3.315`
- `mu^2 = 0.05` gives `alpha = -2.392`
- `mu^2 = 0.01` gives `alpha = -1.992`
- `mu^2 = 0.005` gives `alpha = -1.927`
- `mu^2 = 0.001` gives `alpha = -1.871`

So the steep exponent is not a fixed law of the open surface. It is strongly
screening-controlled and softens toward Newton-compatible scaling as `mu^2` is reduced.

## Important Guardrail

`frontier_wilson_newton_law.py` should **not** be treated as the clean next
test in its current form. Despite its header, it still uses a periodic cubic
lattice and circular-mean separation, so it does not actually remove the image
artifact that the open-lattice harness was built to avoid.

## What This Supports

This Wilson result is strongest as:

- a bounded-retained mutual-attraction result
- a counterexample to “the two-body lane is pure artifact”
- a launch point for understanding why the discrete mutual channel follows a
  steeper-than-Newton falloff

It does **not** yet support:

- retained full `F ∝ M_1 M_2 / r^2`
- a valid action-reaction law on the both-masses grid
- a promoted Nature-level Newton-law claim

## Exact Next Observable

The next decisive observable is no longer another source-weight-only sweep.

It is:

- separate inertial masses in `H_A(M_A, Phi)` and `H_B(M_B, Phi)`
- the early-time mutual momentum-transfer residual on the same open surface
  - `P_A^mut = M_A * a_A^(shared-self_only)`
  - `P_B^mut = M_B * a_B^(shared-self_only)`
- then test:
  - `P_A^mut ∝ M_B`
  - `P_B^mut ∝ M_A`
  - `P_A^mut = -P_B^mut`
