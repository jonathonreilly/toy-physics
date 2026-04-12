# Graph-First `SU(3)` Integration Theorem

**Status:** BOUNDED-RETAINED STRUCTURAL GAUGE THEOREM -- selected graph axis integrates canonically into the bounded commutant theorem  
**Script:** `scripts/frontier_graph_first_su3_integration.py`  
**Date:** 2026-04-12

## Claim under test

Can the newly derived graph-first weak-axis selector be integrated into the
bounded `su(3) \oplus u(1)` commutant theorem without falling back into the
old “chosen factorization” objection?

## Verdict

**Yes.**

Once the graph-first selector picks one axis of the taste cube, the rest of the
construction is canonical on the graph surface:

1. the selected axis defines a canonical projection of the cube onto the other
   two coordinates,
2. the selected-axis shift/parity pair generates the full weak `su(2)` on the
   2-point graph fibers,
3. the residual swap of the other two axes acts canonically on the 4-point
   base,
4. the base splits as `3 \oplus 1` under that swap,
5. the joint commutant is `gl(3) \oplus gl(1)`, with compact semisimple part
   `su(3)`.

So the graph-first route closes the structural `SU(3)` hole without needing the
old native-bivector-to-KS bridge as the only path.

## The graph-first construction

### Step 1. Selected axis gives a canonical graph fiber decomposition

The vertex set of the taste cube is `V = {0,1}^3`.

If the selector chooses axis `\mu`, then forgetting that coordinate gives a
canonical graph projection

\[
\pi_\mu : \{0,1\}^3 \to \{0,1\}^2.
\]

Each fiber of `\pi_\mu` has exactly two vertices. So the graph splits
canonically into:

- a 2-point fiber along the selected axis,
- a 4-point base on the remaining two coordinates.

This is the graph-first replacement for the earlier “chosen tensor factor”.

### Step 2. Weak `su(2)` is generated on the selected graph fibers

Let

\[
X_\mu = \text{selected-axis shift},
\qquad
Z_\mu = \text{selected-axis coordinate parity},
\qquad
Y_\mu = -i Z_\mu X_\mu.
\]

These are all canonical once the axis is selected from the graph.

They satisfy:

\[
X_\mu^2 = Y_\mu^2 = Z_\mu^2 = I,
\]
\[
[X_\mu,Y_\mu] = 2i Z_\mu,\quad
[Y_\mu,Z_\mu] = 2i X_\mu,\quad
[Z_\mu,X_\mu] = 2i Y_\mu.
\]

So

\[
T_i = \frac{1}{2}(X_\mu,Y_\mu,Z_\mu)
\]

give the full weak `su(2)` on the graph fibers.

### Step 3. Residual swap of the complementary axes gives `3 \oplus 1`

The remaining two axes have a canonical transposition `\tau` fixing the
selected axis. This acts on the 4-point base.

Under `\tau`, the base function space splits into:

- a 3-dimensional symmetric block,
- a 1-dimensional antisymmetric block.

Equivalently:

\[
\mathbb{C}^4 = \mathrm{Sym} \oplus \mathrm{Anti} = \mathbb{C}^3 \oplus \mathbb{C}^1.
\]

### Step 4. The commutant is `gl(3) \oplus gl(1)`

The graph weak `su(2)` acts irreducibly on the 2-point fibers, so its commutant
acts on the 4-point base:

\[
\mathrm{Comm}(\mathfrak{su}(2)_{\text{weak}}) \cong gl(4).
\]

Imposing the residual swap restricts this to operators preserving the
`3 \oplus 1` split:

\[
\mathrm{Comm}(\mathfrak{su}(2)_{\text{weak}}, \tau)
 \cong gl(3) \oplus gl(1).
\]

Therefore the compact semisimple part is:

\[
su(3).
\]

## What the script verifies

For **all three** possible selected axes, the script checks:

- graph-native `su(2)` relations from the selected-axis shift/parity pair,
- the residual complementary-axis swap commutes with that `su(2)`,
- the joint commutant has dimension `10`,
- the symmetric and antisymmetric blocks have ranks `9` and `1`,
- the embedded Gell-Mann generators close to `su(3)` on that graph-first
  selected-axis surface,
- the traceless `u(1)` direction has eigenvalues `+1/3` on the `6`-dimensional
  symmetric/weak-doublet block and `-1` on the `2`-dimensional
  antisymmetric/weak-doublet block.

## What this closes

This closes the **structural** objection:

> “Even if you had a selector, you still only have a chosen factorization, not a
> graph-canonical route to `su(3)`.”

After the selector, the factorization is not chosen. It is the canonical graph
projection defined by the selected axis.

## What remains bounded

This note closes the structural graph-first route to `su(3)` on the retained
graph-first surface.

Two things should still be stated carefully:

1. the abelian factor is still best described as **hypercharge-like** or
   left-handed charge matching unless the full anomaly-complete identification
   is written cleanly, and
2. this is the graph-first closure route; it supersedes the need to force the
   result entirely through the old native-bivector bridge.
