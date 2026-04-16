# Exact Link-Channel Compression for the Poissonized Plaquette Law

**Date:** 2026-04-16  
**Status:** exact finite local link-channel alphabet for every `Omega_K` truncation  
**Script:** `scripts/frontier_poissonized_link_channel_compression.py`

## Question

After Poissonizing the infinite-carrier plaquette law into finite plaquette
occupation alphabets `Omega_K`, what is the exact remaining local state space
needed by an evaluator?

More concretely:

- once each plaquette is truncated to `(m,n)` with `m+n <= K`,
- what does a link have to remember exactly,
- and where do the previously identified `regular`, `X`, and `B` sectors sit
  inside that exact compressed evaluator?

## Exact answer

The exact remaining local link data are finite **invariant-channel states**.

For a `K`-truncated plaquette law:

1. each plaquette carries a finite state `(m,n) in Omega_K`,
2. each link sees induced counts `(r,s)` of fundamental and anti-fundamental
   legs with `r+s <= 4K`,
3. the exact local link tensor lives on the finite invariant space

`Inv(3^(⊗r) ⊗ 3bar^(⊗s))`.

So every `K` gives an exact finite tensor-network evaluator state space:

- plaquette alphabet `Omega_K`,
- link channel alphabet

`Lambda_K = {(r,s,alpha): r,s >= 0, r+s <= 4K, 1 <= alpha <= dim Inv(r,s)}`.

This is the exact finite-state evaluator behind the Poissonized compression.

## Theorem 1: exact link-channel dimensions from SU(3) tensor recursion

Let `(a,b)` denote the `SU(3)` irrep with Dynkin labels `(a,b)`.

Tensoring with the fundamental and anti-fundamental obeys the exact branching
rules

`(a,b) ⊗ 3 = (a+1,b) ⊕ (a-1,b+1) ⊕ (a,b-1)`

and

`(a,b) ⊗ 3bar = (a,b+1) ⊕ (a+1,b-1) ⊕ (a-1,b)`

with the obvious nonnegativity restrictions on labels.

Starting from the trivial irrep `(0,0)` and iterating these exact rules gives
the full tensor-product decomposition of

`3^(⊗r) ⊗ 3bar^(⊗s)`.

Therefore

`dim Inv(r,s) = mult((0,0) in 3^(⊗r) ⊗ 3bar^(⊗s))`

is exact and computable by finite recursion.

## Theorem 2: exact first special channels

The first local channels are exactly:

- regular projector:
  - `dim Inv(1,1) = 1`
- crossing `X` sector:
  - `dim Inv(2,2) = 2`
- baryon `B` sector:
  - `dim Inv(3,0) = dim Inv(0,3) = 1`

So the earlier `regular`, `X`, and `B` link tensors are literally the first
exact link channels in the compressed occupation evaluator.

The next richer channels already appear immediately after:

- `dim Inv(4,1) = 3`
- `dim Inv(4,4) = 23`

So the evaluator is finite for fixed `K`, but not tiny.

## Theorem 3: exact finite link-channel alphabet at truncation `K`

For `Omega_K = {(m,n): m+n <= K}`, a link sees at most four incident plaquettes,
so the induced local counts obey

`r+s <= 4K`.

The exact finite link-channel alphabet is therefore

`Lambda_K = {(r,s,alpha): r+s <= 4K, 1 <= alpha <= dim Inv(r,s)}`.

The runner computes two exact sizes:

1. the coarse nonzero support size:
   - number of count pairs `(r,s)` with `dim Inv(r,s) > 0`
2. the full channel count:
   - `Xi_K = sum_{r+s <= 4K} dim Inv(r,s)`

At `beta = 6`, using the previously useful plaquette truncation levels:

- `K = 8`:
  - `|Omega_K| = 45`
  - nonzero `(r,s)` support = `187`
  - full link channels `Xi_K = 959852570241`
- `K = 12`:
  - `|Omega_K| = 91`
  - nonzero `(r,s)` support = `409`
  - full link channels `Xi_K = 13762130392745662853`
- `K = 16`:
  - `|Omega_K| = 153`
  - nonzero `(r,s)` support = `715`
  - full link channels
    `Xi_K = 251668333351922437336472385`
- `K = 20`:
  - `|Omega_K| = 231`
  - nonzero `(r,s)` support = `1107`
  - full link channels
    `Xi_K = 5751651283997210283708144343174357`

So the exact local evaluator is finite, but a naive invariant-basis expansion is
already enormous.

## Corollary: exact local finiteness is closed

This closes a real evaluator question.

The branch no longer has to say merely:

> the law has a countable local occupation compression.

It can now say:

> for every truncation `K`, the exact evaluator is a finite tensor network with
> explicit finite plaquette states `Omega_K` and explicit finite link-channel
> states `Lambda_K`.

That is a theorem-grade finite-state compression.

## What remains open

The remaining gap is no longer whether the local state space is finite.

That is done.

The remaining gap is now sharper:

> compress or contract the exact invariant-channel basis efficiently.

In other words:

- finite-state existence: closed
- exact local channel identification: closed
- efficient contraction / basis compression: still open

## Paper-safe conclusion

The strongest clean statement is now:

> the exact Poissonized plaquette occupation law admits a further exact finite
> local compression to link-channel spaces `Inv(3^(⊗r) ⊗ 3bar^(⊗s))`; the
> earlier `regular`, `X`, and `B` sectors are the first explicit channels in
> that exact evaluator. The remaining difficulty is algorithmic contraction of
> the finite but rapidly growing channel basis, not missing local state data.

## Commands run

```bash
python3 scripts/frontier_poissonized_link_channel_compression.py
```

Output summary:

- exact `dim Inv(r,s)` recursion
- exact first special channels `regular`, `X`, `B`
- exact finite link-channel alphabets for `K = 8, 12, 16, 20`
- exact separation between finite-state existence and remaining contraction
  complexity
