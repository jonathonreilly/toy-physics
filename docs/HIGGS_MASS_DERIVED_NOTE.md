# Higgs Mass: Canonical Authority Boundary

## Question

After implementing the full 3-loop Higgs runner directly, what still keeps the
Higgs lane bounded?

## Final reviewer answer

The canonical Higgs posture remains `BOUNDED`, but the bound is now much
narrower than before.

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
because the Higgs lane still inherits the bounded `y_t(v)` route.

## Canonical retained claim

The paper-safe Higgs claim is now:

- the framework derives the Higgs mechanism itself
- the framework derives the natural high-scale boundary `lambda(M_Pl) = 0`
- the branch now contains a direct full 3-loop Higgs runner with no
  Buttazzo-style parametric fit
- for the current accepted central input `y_t(v) = 0.918`, that runner gives
  `m_H ~= 125.3 GeV`
- the exact Higgs lane is still `BOUNDED` only because the accepted `y_t`
  route carries an inherited `~3%` QFP / backward-Ward systematic

## What changed

The old Higgs bound had two distinct pieces:

1. the branch lacked a complete direct 3-loop Higgs implementation
2. the accepted `y_t(v)` route was still bounded

The new runner
[scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
removes blocker (1). It computes the Higgs mass directly from the framework
boundary condition `lambda(M_Pl) = 0` using the full 3-loop SM RGE system and
current framework-side low-energy inputs.

So the remaining Higgs boundedness is no longer “missing Higgs machinery.”
It is inherited from the still-bounded `y_t` lane.

## Current numerical posture

For the current central input `y_t(v) = 0.918`, the full 3-loop Higgs runner
gives:

- `m_H ~= 125.3 GeV` with no parametric fit
- an inherited Higgs band of roughly `115.2-135.3 GeV` if the `y_t` route is
  varied by the current `~3%` QFP systematic

That means the honest Higgs read is:

- **mechanism:** derived
- **3-loop computation:** implemented
- **central Higgs value:** framework-side and direct
- **remaining bound:** inherited from `y_t`, not from missing Higgs code

## Why exact Higgs closure is still bounded

Only two scientific cautions remain.

1. The accepted `y_t(v)` route is still bounded.
   The backward-Ward / QFP bridge remains the limiting step for the Higgs lane.
2. Vacuum stability inherits the same bound.
   If `y_t` carries a bounded systematic, then the statement `lambda(mu) > 0`
   for all scales inherits that same systematic.

So the correct current claim is not “Higgs still lacks a real computation.”
It is “Higgs is conditionally closed at 3-loop on the accepted bounded `y_t`
route.”

## Current route inventory

### Canonical authority

- [scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py)
  is now the primary quantitative authority runner for the Higgs lane.
  Its job is to show that the Higgs-specific 3-loop blocker is gone.
- [scripts/frontier_higgs_mass_derived.py](../scripts/frontier_higgs_mass_derived.py)
  remains a useful mechanism / boundary companion, but it is no longer the
  only honest Higgs-boundary runner.

### Supporting Higgs surfaces

- [HIGGS_MECHANISM_NOTE.md](./HIGGS_MECHANISM_NOTE.md)
  mechanism-level support
- [HIGGS_FROM_LATTICE_NOTE.md](./HIGGS_FROM_LATTICE_NOTE.md)
  bounded / historical quantitative support
- [HIGGS_MASS_NOTE.md](./HIGGS_MASS_NOTE.md)
  historical numerical CW support

These notes remain useful context, but they should not outrank this note when
a reader asks what the Higgs lane currently claims.

## Paper-safe framing

**Can claim**

- the Higgs mechanism emerges naturally from the lattice
- the hierarchy problem is solved structurally
- `lambda(M_Pl) = 0` is a framework-native Higgs boundary condition
- the repo now contains a direct full 3-loop Higgs computation with no
  Buttazzo-style calibrated-fit dependence
- the remaining Higgs bound is inherited from the bounded `y_t` lane

**Cannot claim**

- the Higgs lane is unbounded independently of `y_t`
- vacuum stability is unbounded while `y_t` still carries the QFP bound
- older lattice-CW or partial-Higgs notes as if they were the live authority
