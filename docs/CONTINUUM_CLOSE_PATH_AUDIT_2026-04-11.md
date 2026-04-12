# Continuum Close Path Audit

**Date:** 2026-04-11  
**Scope:** continuum / derivation close path only  
**Status:** diagnostic note, not a new physics claim

## What is already on the table

The retained continuum material already supports a bounded weak-field bridge:

- [`docs/CONTINUUM_LIMIT_NOTE.md`](CONTINUUM_LIMIT_NOTE.md) retains the
  h^2-measure result
- weak-field deflection is converging between `h = 0.25` and `h = 0.125`
- the Wilson companion note retains a same-convention open-surface
  test-mass / continuum package
- [`docs/NEWTON_DERIVATION_NOTE.md`](NEWTON_DERIVATION_NOTE.md) is already
  framed at the correct family-level boundary: bounded, not architecture-
  independent, and explicitly open on the persistent-pattern mass step

So the remaining question is not whether there is *any* continuum signal.
The question is the shortest credible path to close the remaining gap without
overclaiming.

## What the current h = 0.0625 lane is telling us

The current lane is limited by two different effects:

1. **Compute cost**
   - fixed 3D volume means node count rises like `h^-3`
   - the propagation depth also grows as the lattice is refined
   - so the effective work scales closer to `h^-4` than to `h^-3`
   - halving `h` from `0.125` to `0.0625` is therefore about `8x` the nodes
     and `16x` the refinement work, even before numerical stability is
     considered

2. **Geometry leakage**
   - the current observable chain uses an open boundary
   - the retained note already shows `P_det` underflow and boundary leakage
   - the observable is therefore not stable enough to justify a brute-force
     `h -> 0` claim on `P_det` itself
   - finer `h` does not remove the leakage problem; it makes the accumulation
     more visible because there are more layers to leak through

So the current `h = 0.0625` lane is not just slow. It is also asking the wrong
observable to carry the continuum claim.

## What is actually missing

### Missing item 1: a boundary-robust observable

The retained weak-field story should be driven by a local quantity that
survives refinement:

- centroid / deflection in the weak-field regime
- source-mass response
- a per-node transfer normalization or open-boundary correction

`P_det` is useful as a diagnostic, but it is not the right quantity to close
the continuum gap.

### Missing item 2: a boundary-aware normalization

The note in [`docs/CONTINUUM_LIMIT_NOTE.md`](CONTINUUM_LIMIT_NOTE.md)
already points to the likely fix:

- per-node `T` normalization
- or an equivalent open-boundary correction

Without that correction, the fine-grid run keeps mixing continuum behavior with
boundary leakage.

### Missing item 3: a minimal Richardson-style sequence

The shortest credible sequence is not a brute-force single-point `h=0.0625`
run. It is:

- `h = 0.25`
- `h = 0.125`
- `h = 0.0625` only if the corrected observable remains stable

Then extrapolate the local observable with a low-order Richardson fit. That is
enough to test whether the continuum value is stable without pretending the
full 3D `P_det` channel is the theorem.

## What is optional

These are useful, but not required to close the remaining continuum gap:

- a new analytically derived transfer kernel
- a different lattice family
- a larger brute-force `h=0.0625` run on the current unstable observable
- further reframing of `NEWTON_DERIVATION_NOTE.md`

`NEWTON_DERIVATION_NOTE.md` does **not** need to be reframed further for the
current scope. It already sits at the correct family-level boundary:
test-particle / family-law yes, persistent-pattern / architecture-independence
no.

## Shortest credible close path

1. Keep the Newton derivation note as a bounded family theorem.
2. Replace `P_det` with a boundary-robust weak-field observable.
3. Add per-node `T` normalization or an equivalent open-boundary correction.
4. Run the smallest Richardson ladder that is still stable:
   `h = 0.25 -> 0.125 -> 0.0625`.
5. Promote only the continuum statement that is actually supported by the
   corrected observable.

## Bottom line

The current h=0.0625 lane is both compute-limited and geometry-limited, but
the geometry limitation is the decisive one. The shortest path is not more
brute force on the present observable. It is a corrected observable with a
boundary-aware normalization, followed by a small Richardson sequence.
