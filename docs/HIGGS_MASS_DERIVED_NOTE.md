# Higgs Mass: Canonical Authority Boundary

## Question

After implementing the full 3-loop Higgs runner directly, what still keeps the
Higgs lane from being fully unbounded?

## Final reviewer answer

The canonical Higgs posture is now **derived quantitative lane with inherited
YT residuals**, and that inherited caveat is no longer a separate Higgs-native
systematic.

The framework now supports all of the following:

| Result | Status |
|---|---|
| taste condensate acts as the Higgs field | DERIVED |
| lattice Coleman-Weinberg electroweak symmetry breaking occurs naturally | DERIVED |
| the hierarchy problem is removed because the cutoff is physical (`pi/a`) | DERIVED |
| the boundary condition `lambda(M_Pl) = 0` is framework-native | DERIVED |
| a direct framework-side full 3-loop Higgs computation exists | DERIVED |
| Buttazzo-style calibrated-fit dependence is required | NO |

What is **not** yet unbounded is the exact numerical Higgs claim by itself,
because the Higgs lane still inherits the explicit `y_t(v)` systematic.

## Canonical retained claim

The paper-safe Higgs claim is now:

- the framework derives the Higgs mechanism itself
- the framework derives the natural high-scale boundary `lambda(M_Pl) = 0`
- the current package now contains a direct full 3-loop Higgs runner with no
  Buttazzo-style parametric fit
- for the current accepted central input `y_t(v) = 0.9176`, that runner gives
  `m_H ~= 125.1 GeV`
- the exact Higgs lane is derived and inherits the current YT-lane precision
  caveat rather than a separate Higgs-only closure gap

## What changed

The old Higgs limitation had two distinct pieces:

1. the package lacked a complete direct 3-loop Higgs implementation
2. the accepted `y_t(v)` route still carried the load-bearing precision caveat

The new runner
[scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
removes blocker (1). It computes the Higgs mass directly from the framework
boundary condition `lambda(M_Pl) = 0` using the full 3-loop SM RGE system and
current framework-side low-energy inputs.

So the remaining Higgs caveat is no longer “missing Higgs machinery.”
It is inherited from the accepted `y_t` lane.

## Taste-scalar support theorem

The current Higgs support stack also contains one exact taste-block theorem:
[TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](./TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md).

That theorem shows that the one-loop fermion Coleman-Weinberg Hessian on the
retained taste block is isotropic at the axis-aligned electroweak minimum, so
the fermion-CW sector alone cannot split the Higgs direction from the two
orthogonal taste directions.

On the current bounded gauge-only split model this gives a near-degenerate
taste-scalar pair at

- `m_taste = 124.91 GeV`

with a scalar-only thermal-cubic estimate `v_c/T_c = 0.3079`.

This is useful support for Higgs/taste bookkeeping and downstream EWPT work,
but it does not change the canonical Higgs claim itself. The promoted Higgs row
remains `m_H = 125.1 GeV`, with inherited YT-lane precision caveat.

## Current numerical posture

For the current central input `y_t(v) = 0.9176`, the full 3-loop Higgs runner
gives:

- `m_H ~= 125.1 GeV` with no parametric fit
- an inherited Higgs band of roughly `121.1-129.2 GeV` on the old
  bridge-path cross-check budget

That means the honest Higgs read is:

- **mechanism:** derived
- **3-loop computation:** implemented
- **central Higgs value:** framework-side and direct
- **remaining bound:** inherited from `y_t`, not from missing Higgs code

## Why exact Higgs closure is still systematic-limited

Only two scientific cautions remain.

1. The accepted `y_t(v)` route still carries the lane’s live precision caveat.
2. Vacuum stability inherits that same Yukawa-route precision caveat.

So the correct current claim is not “Higgs still lacks a real computation.”
It is “Higgs is conditionally closed at 3-loop on the accepted YT route.”

## Current route inventory

### Canonical authority

- [scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
  is now the primary quantitative authority runner for the Higgs lane.
  Its job is to show that the Higgs-specific 3-loop blocker is gone.
- [scripts/frontier_higgs_mass_derived.py](../scripts/frontier_higgs_mass_derived.py)
  remains a useful mechanism / boundary companion, but it is no longer the
  only honest Higgs-boundary runner.

### Supporting Higgs surfaces

These are downstream support notes (each consumes this note as authority,
direction is *support → this note*; they are referenced by name rather
than markdown link to avoid creating parent-cites-child citation graph
edges and length-2 cycles):

- `HIGGS_MECHANISM_NOTE.md` — mechanism-level support
- `HIGGS_FROM_LATTICE_NOTE.md` — bounded / historical quantitative support
- [HIGGS_MASS_NOTE.md](./HIGGS_MASS_NOTE.md) — historical numerical CW support
  (kept as markdown link since it is upstream / does not cite back)

These notes remain useful context, but they should not outrank this note when
a reader asks what the Higgs lane currently claims.

## Paper-safe framing

**Can claim**

- the Higgs mechanism emerges naturally from the lattice
- the hierarchy problem is solved structurally
- `lambda(M_Pl) = 0` is a framework-native Higgs boundary condition
- the repo now contains a direct full 3-loop Higgs computation with no
  Buttazzo-style calibrated-fit dependence
- the remaining Higgs precision caveat is inherited from the accepted `y_t`
  lane

**Cannot claim**

- the Higgs lane is unbounded independently of `y_t`
- vacuum stability is unbounded while `y_t` still carries a live precision
  caveat
- older lattice-CW or partial-Higgs notes as if they were the live authority
