# Native Nonlocal Selector Note

**Date:** 2026-04-12  
**Status:** CANDIDATE FOUND ON THE TESTED NONLOCAL SURFACE  
**Script:** `scripts/frontier_native_nonlocal_selector.py`

## Claim under test

Can the missing weak-axis selector be built on the native `Cl(3)` / graph-taste
surface using graph shifts, two-step paths, bilocal kernels, or other
path-summed native data, without importing the KS factorization?

This is the right graph-first question for the expansive paper. The earlier
low-degree Clifford triplets were too isotropic and gave a hard no-go. The
remaining question is whether a larger same-surface operator surface can
produce a genuine `S_3 -> Z_2` selector.

## Verdict

**Yes, on the tested graph-shift / bilocal surface.**

The harness finds a concrete candidate family built from native cube graph
shifts and their two-step path kernels:

\[
K_i(\lambda) = S_i + \lambda B_i,\qquad B_i = S_j S_k,\quad \{i,j,k\} = \{1,2,3\}.
\]

The purely graph-native shift triplet `S_i` already produces an axis-selective
quartic invariant, and the strictly bilocal two-step family `B_i` behaves the
same way. The mixed family `S_i + \lambda B_i` preserves the selector over the
scanned values of `\lambda`.

## What the script proves

### 1. The low-degree native Clifford triplets remain a no-go

The native low-degree Hermitian surface

\[
\mathrm{span}_{\mathbb{R}}\{I,\Gamma_5,\Gamma_1,\Gamma_2,\Gamma_3,A_1,A_2,A_3\}
\]

still behaves exactly as before:

- `Gamma_i` and `A_i = -i Gamma_j Gamma_k` are Hermitian triplets,
- `H(\phi)^2 = |\phi|^2 I`,
- `Tr H^4 / Tr H^2^2` is constant on the sphere.

So the simplest native Clifford triplets do **not** select a weak axis.

### 2. The graph-shift triplet is axis-selective

On the 3-cube taste graph, the one-step axis shifts `S_i` are involutive
Hermitian graph operators. The corresponding quartic ratio

\[
R_4(\phi) = \frac{\mathrm{Tr}\,H(\phi)^4}{\mathrm{Tr}\,H(\phi)^2{}^2}
\]

is not isotropic. The harness finds:

- axis directions have the smallest `R_4`,
- planar directions are higher,
- fully symmetric directions are higher still.

That is exactly the signature of an axis-selecting quartic Landau surface.

### 3. The bilocal two-step path triplet also works

The bilocal family

\[
B_i = S_j S_k
\]

is strictly two-step / nonlocal on the cube graph. It produces the same
axis-selective quartic pattern as `S_i`.

### 4. The mixed graph-shift / bilocal family is robust

The scanned mixed family

\[
K_i(\lambda) = S_i + \lambda B_i
\]

keeps the axis minima for every scanned `\lambda` in the harness.

## Safe paper reading

The correct interpretation is:

1. the low-degree native Clifford triplets are too isotropic,
2. the graph-shift and two-step path operators on the 3-cube do provide a
   concrete same-surface selector candidate,
3. that candidate has the expected three axis vacua with residual `Z_2`
   stabilizer on the axis labels,
4. the result is still a harness-level candidate, not yet a dynamical theorem.

## What this does and does not close

This **does** give the full-paper effort a viable same-surface selector
candidate that is genuinely graph-first and not KS-factorized.

This **does not yet** prove that the selector is forced by the underlying
dynamics. The next theorem would need to derive the graph-shift / bilocal
surface itself, or show that the same-surface potential is unavoidable.

