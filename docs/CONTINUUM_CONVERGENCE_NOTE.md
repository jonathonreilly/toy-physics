# Continuum Convergence Note

**Date:** 2026-04-04  
**Status:** bounded - bounded or caveated result note

This note collects the current dimension-dependent-kernel results on the
ordered-lattice family. It is intentionally narrower than the branch-history
headlines that produced it.

The safe read today is:

- the original 3D dense spent-delay `1/L` gravity signal does **not** survive
  refinement
- a new ordered-lattice propagator fork using `1/L^(d-1)` is a **strong
  empirical persistence candidate** across the tested 2D / 3D / 4D lattice
  families
- that kernel family is still **not** a derived theorem, and it is still
  **not** a promoted top-level canonical lane

This is frontier work on `main`, not a replacement for the flagship mirror
story.

## What is on firm ground

### 1. 2D ordered lattice with `1/L`

The 2D lattice refinement signal is real and strong.

- TOWARD gravity survives and strengthens under refinement
- Born remains machine-clean
- MI / decoherence / `d_TV` converge in the retained window
- the 2D tail fit is consistent with a `1/b`-like law on the tested window

### 2. 3D dense spent-delay with `1/L`

The old attractive 3D dense spent-delay read was a fixed-scale artifact.

- at `h = 1.0`, the retained window is attractive
- at `h = 0.5`, that same family collapses toward away/depletion
- so the older “3D 10/10 card” does **not** survive refinement on the original
  `1/L` transport

### 3. 3D ordered lattice with `1/L^2`

This is the most important new exploratory branch.

On the tested ordered-lattice family:

- TOWARD gravity survives from `h = 0.5` through the current `h = 0.125` run
- the branch remains Born-clean at machine precision on the retained checks
- the barrier card stays nontrivial on MI / decoherence / `d_TV`
- a frozen `h = 0.25` eight-property card now exists on `main`
- the no-barrier post-peak tail fit improves when the `h = 0.25` lattice is
  widened:
  - earlier retained read: `b^(-0.53)`
  - wider retained read: `b^(-0.70)`, `R^2 = 0.955`

Primary branch artifacts:

- [`scripts/lattice_3d_l2_fast.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_fast.py)
- [`scripts/lattice_3d_l2_canonical_card.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_canonical_card.py)
- [`scripts/lattice_3d_inverse_square_kernel.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_inverse_square_kernel.py)
- [`scripts/lattice_3d_l2_tail_stats.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_tail_stats.py)
- [`docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md)

### 4. 4D ordered lattice with `1/L^3`

The 4D result is useful, but it is still bounded.

Current branch evidence supports:

- short 4D lattices are not discriminative
- on the longer tested 4D windows, `1/L^3` looks stronger than lower powers
  on persistence-with-length
- Born remains machine-clean on the tested 4D branch

Current branch evidence does **not** yet support:

- a unique-selection theorem
- a finished asymptotic `1/r^3` or force-law closure
- a promoted continuum theorem

## What remains unresolved

### Transfer norm is still under reconciliation

There are currently two different transfer-style reads on `main`:

1. the bounded local probe:
   - [`docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md)
   - this local measure-corrected discriminator leaned closer to `p = 1.5`
     than `p = 2.0` in 3D
2. the imported branch transfer story:
   - [`scripts/transfer_norm_and_born.py`](/Users/jonreilly/Projects/Physics/scripts/transfer_norm_and_born.py)
   - this is a different observable and should not be read as already
     superseding the bounded local probe

So the review-safe wording is:

- `p = d - 1` is the **strongest empirical persistence candidate**
- transfer-norm selection is still **under reconciliation**
- the branch is **not yet** “derived from axioms” or “uniquely selected”

### RG control is promising, not fully closed

The branch has a real RG-style stabilization story for gravity magnitude, but
the current safe separation is:

- sign persistence under refinement (RETAINED)
- post-peak tail steepening: **CORRECTED** — at same width (W=10), the
  tail from z>=5 is -0.82 at h=0.5 and -0.63 at h=0.25 (shallower, not
  steeper). The tail from peak onward is -0.82 (h=0.5, peak z=5) vs
  -0.52 (h=0.25, peak z=4). The exponent gets SHALLOWER with finer h.
  The earlier “-0.35 → -0.53 steepening” compared different lattice widths.
- finite-magnitude RG control (RETAINED)

Those are related, but they are not the same claim and should not be collapsed
into one blanket “continuum solved” statement. The distance law direction is
currently AWAY from Newtonian, not toward it.

### O5-style tail prediction was refuted as stated

The earlier prediction that the `h = 0.125` tail exponent should fall in a
specific numerical band was refuted. The useful lesson is boundary/peak
motion:

- the peak shifts outward as `h` decreases
- measuring the far tail at finer `h` requires a wider lattice
- a failed prediction here is evidence that the falsification framework is
  working, not that the branch is automatically dead

## Clean interpretation

The current best summary is:

- the ordered lattice has a genuine refinement bridge in 2D
- the original 3D `1/L` gravity signal fails under refinement
- a new `1/L^(d-1)` propagator fork is the strongest current empirical
  candidate for persistent gravity on the ordered-lattice family
- that branch is stronger than it was this morning, but still bounded and
  still under active review

## What this note should not be used to claim

- “kernel = `1/L^(d-1)` is derived from the axioms”
- “transfer norm uniquely selects `p = d - 1`”
- “Newtonian gravity is now established”
- “the continuum theorem is complete”

Those claims still outrun the retained artifact chain.
