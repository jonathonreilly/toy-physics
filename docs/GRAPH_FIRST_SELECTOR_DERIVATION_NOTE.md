# Graph-First Weak-Axis Selector Derivation

**Status:** STRONG NEW ROUTE -- the weak-axis selector is derived on the canonical graph-shift surface  
**Script:** `scripts/frontier_graph_first_selector_derivation.py`  
**Date:** 2026-04-12

## Claim under test

Do we actually need to close the old native-bivector `SU(2) -> SU(3)` bridge
in order to derive the color lane, or can the selector be derived directly
from the graph/taste axiom itself?

This note answers that question on a graph-first surface.

## Verdict

**Yes, the selector can be derived directly from the canonical graph-shift
surface.**

The taste cube carries three canonical one-step axis shifts `S_i`. These are
determined entirely by the graph structure of the `2^3` hypercube corners.
For

\[
H(\phi) = \sum_{i=1}^3 \phi_i S_i,
\]

the first nontrivial even invariant is

\[
V_{\mathrm{sel}}(\phi)
= \mathrm{Tr}\,H(\phi)^4 - \frac{1}{8}\big(\mathrm{Tr}\,H(\phi)^2\big)^2
= 32 \sum_{i<j} \phi_i^2 \phi_j^2.
\]

After normalization

\[
p_i = \frac{\phi_i^2}{\sum_j \phi_j^2},
\]

this becomes exactly the purity-deficit / pairwise-overlap potential

\[
F(p) = \sum_{i<j} p_i p_j
     = \frac{1}{2}\left(1 - \sum_i p_i^2\right),
\]

whose minima are precisely the three axis vertices

\[
(1,0,0),\quad (0,1,0),\quad (0,0,1),
\]

each with residual `Z_2` stabilizer.

So the missing weak-axis selector is not merely a phenomenological ansatz on
the tested graph-shift surface. It is the first nontrivial even invariant of
the canonical axis-shift triplet.

## Why this matters

This changes the structure of the `SU(3)` problem.

Before:
- derive native bivector `su(2)`,
- then somehow bridge it canonically to the KS factor `su(2)`,
- then apply the bounded commutant theorem.

Now there is a second, graph-first route:
- canonical graph shifts `S_i`,
- derived selector potential with three axis vacua and residual `Z_2`,
- distinguished axis becomes graph-canonical,
- then apply the bounded commutant theorem relative to that selected axis.

This means the full paper does **not** necessarily stand or fall on the old
native-bivector bridge alone.

## What the script proves

### 1. The graph-shift triplet is canonical

On the taste cube:

\[
S_1 = \sigma_x \otimes I \otimes I,\quad
S_2 = I \otimes \sigma_x \otimes I,\quad
S_3 = I \otimes I \otimes \sigma_x.
\]

These are:

- Hermitian,
- involutive (`S_i^2 = I`),
- pairwise commuting,
- and they transform as an `S_3` triplet under axis permutations.

### 2. The selector is derived, not inserted

For the source `H(\phi) = \sum_i \phi_i S_i`:

\[
\mathrm{Tr}\,H^2 = 8 |\phi|^2,
\]

and

\[
\mathrm{Tr}\,H^4 = 8\left(|\phi|^4 + 4\sum_{i<j}\phi_i^2\phi_j^2\right).
\]

Subtracting the purely isotropic quadratic piece gives the unique quartic
selector on this surface:

\[
V_{\mathrm{sel}}(\phi)
= \mathrm{Tr}\,H^4 - \frac{1}{8}(\mathrm{Tr}\,H^2)^2
= 32 \sum_{i<j}\phi_i^2\phi_j^2.
\]

### 3. The selector has exactly the right vacuum structure

On the normalized simplex `p_i = φ_i^2 / ∑ φ_j^2`, the potential is

\[
F(p) = \sum_{i<j} p_i p_j.
\]

This has:

- exactly three minima,
- each minimum is an axis,
- each axis has residual `Z_2` stabilizer from swapping the other two axes.

So the graph itself provides the `S_3 -> Z_2` selector on the tested surface.

## What this does not yet prove

This note does **not** yet finish the full gauge theorem by itself.

The remaining step is:

- integrate the graph-selected axis into the bounded `su(3) \oplus u(1)`
  commutant theorem cleanly and canonically, without slipping back into the
  old “chosen factorization” language.

But it does remove the most damaging form of the old objection:

> “There is no derived weak-axis selector on the same graph surface.”

On the canonical graph-shift surface, there now is one.
