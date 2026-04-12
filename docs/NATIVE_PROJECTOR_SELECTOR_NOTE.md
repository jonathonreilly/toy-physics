# Native Projector Selector on the `Cl(3)` / `C^8` Surface

**Status:** BLOCKED -- projector-valued order parameters on the current native surface do not canonically select a weak axis  
**Script:** `scripts/frontier_native_projector_selector.py`  
**Date:** 2026-04-12

## Claim under test

Can the missing `S_3 -> Z_2` weak-axis selector be realized as a
projector-valued order parameter intrinsic to the native `Cl(3)` / `C^8`
surface?

The projector route is the most natural remaining same-surface attack:

1. search for canonical projectors built from native operators,
2. search for commutant projectors on the axis orbit module,
3. search for spectral projectors of the natural native triplets, and
4. test whether any of those families can produce an intrinsic
   three-vacuum axis structure with residual `Z_2`.

## Verdict

**No canonical weak-axis selector was found on the low-degree native
surface.**

The script finds three useful facts:

1. the axis orbit module has only the singlet-plus-standard projector
   structure (`1 \oplus 2`);
2. the low-degree native Clifford surface contains only rank-4 spectral
   projectors of single involutions, not rank-1 or rank-3 axis selectors;
3. the natural native triplets are spectrally isotropic, so their
   projector families remain sign- or axis-parametrized rather than
   canonically selecting a vacuum.

## What the script checks

### 1. Axis-module commutant projectors

On the three-axis permutation module:

- the `S_3` commutant is 2-dimensional,
- the only nontrivial invariant projectors are the symmetric singlet
  `P_sym = J/3` and the complementary standard projector
  `P_std = I - P_sym`,
- every coordinate-axis projector fails `S_3` invariance.

So the orbit-module route gives `1 \oplus 2`, not a canonical axis.

### 2. Native low-degree projector search

On the native `C^8` surface, the script exhaustively searches the low-degree
Hermitian span

\[
\mathrm{span}_{\mathbb{R}}\{I,\Gamma_5,\Gamma_1,\Gamma_2,\Gamma_3,A_1,A_2,A_3\},
\]

using a rational coefficient grid. The only projectors found are:

- the identity,
- the obvious spectral projectors `(I \pm B)/2` for the basis involutions
  `B \in {Gamma_5, Gamma_1, Gamma_2, Gamma_3, A_1, A_2, A_3}`.

Every nontrivial projector in that search has rank `4`, i.e. a `4+4` split.
No rank-1, rank-2, rank-3, rank-5, rank-6, or rank-7 projector appears on
that low-degree native surface.

### 3. Spectral projectors of the natural native triplets

For either natural axis-labelled triplet

- `Phi_i = Gamma_i`, or
- `Phi_i = A_i = -i Gamma_j Gamma_k`,

the source

\[
H(\phi) = \sum_i \phi_i \Phi_i
\]

satisfies `H(\phi)^2 = |\phi|^2 I`, so its spectral projectors are always
rank `4`. The corresponding trace invariants are isotropic (`Tr H^3 = 0`,
`Tr H^4 = 8|\phi|^4`), so the projector family cannot distinguish axis,
planar, or fully symmetric directions.

## Meaning for the full paper

This is **not** a no-go for the full paper. It is a no-go for the
projector-valued selector route on the low-degree native surface.

The correct publication reading is:

1. the native `Cl(3)` surface does contain natural projector families,
2. but they collapse to singlet/standard or rank-4 spectral projectors,
3. therefore they do **not** canonically produce a three-vacuum weak-axis
   selector with residual `Z_2`.

## What would be needed to close the gap

To upgrade this route, the review branch would need a larger same-surface
operator or a genuinely dynamical construction, for example:

- a higher-degree native operator,
- a bilocal / nonlocal projector family,
- or a derived potential on a larger native operator surface that produces
  three axis vacua with residual `Z_2`.

Absent that, the projector route is blocked on the current retained surface.
