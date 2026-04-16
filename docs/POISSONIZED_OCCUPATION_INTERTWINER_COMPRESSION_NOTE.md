# Exact Poissonized Occupation/Intertwiner Compression for the Plaquette Law

**Date:** 2026-04-16  
**Status:** exact resummed/state-compressed representation of the infinite-carrier law  
**Script:** `scripts/frontier_poissonized_occupation_intertwiner_compression.py`

## Question

After the exact character/intertwiner foam law and the exact no-go against any
small finite `B/X` low-carrier closure, is there still a useful exact
resummed/state-compressed representation of the plaquette law?

## Exact answer

Yes.

The exact finite-periodic-lattice plaquette law admits an exact **Poissonized
occupation/intertwiner compression**:

- each plaquette carries a countable local state `(m,n) in N^2`,
- the local state weights are explicit iid Poisson probabilities,
- the link Haar integrals are absorbed into occupation/intertwiner amplitudes,
- and truncating to `m+n <= K` gives a finite local alphabet with an explicit
  uniform tail bound on the normalized finite-lattice law.

So the honest endpoint is now sharper than before:

1. exact law: closed
2. exact finite small low-carrier closure: impossible
3. exact useful resummed/state-compressed representation: closed

What remains open, if desired, is only a faster evaluator or a tighter closed
recursion for that already compressed law.

`docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md` now sharpens that further:
for every truncation `K`, the exact local evaluator state space is finite not
only on plaquettes but also on links, via the finite invariant-channel
alphabets `Lambda_K`.

## Theorem 1: exact local Poissonization

Write

`a(U) = Tr(U) / 3`

so `|a(U)| <= 1` on compact `SU(3)`.

Let `M` and `N` be independent Poisson random variables with mean

`lambda = beta / 2`.

Then

`E[a(U)^M conj(a(U))^N]`
`= exp[lambda (a(U) - 1)] exp[lambda (conj(a(U)) - 1)]`
`= exp[(beta/6)(Tr U + Tr U^dag) - beta]`.

Therefore

`e^(-beta) w_beta(U) = E[a(U)^M conj(a(U))^N]`

and equivalently

`w_beta(U) = e^beta E[a(U)^M conj(a(U))^N]`.

This is an exact resummation of the one-plaquette Wilson weight.

At `beta = 6`, the local Poisson mean is

`lambda = 3`.

## Theorem 2: exact finite-lattice occupation/intertwiner law

Take a finite periodic lattice with `P` plaquettes and define the normalized
partition function and anchored plaquette numerator

`z_L(beta) = e^(-beta P) Z_L(beta)`

and

`n_{L,q}(beta) = e^(-beta P) N_{L,q}(beta)`.

Applying Theorem 1 on every plaquette gives

`z_L(beta) = E_{(M_p,N_p)}[ I_L({M_p,N_p}) ]`

and

`n_{L,q}(beta) = E_{(M_p,N_p)}[ J_{L,q}({M_p,N_p}) ]`

where:

- the plaquette states `(M_p,N_p)` are iid Poisson occupation pairs with mean
  `beta/2`,
- `I_L` is the finite product of link Haar integrals with plaquette factors
  `a(U_p)^(M_p) conj(a(U_p))^(N_p)`,
- `J_{L,q}` is the same anchored numerator amplitude with one extra factor
  `a(U_q)`.

Because `|a(U_p)| <= 1`, both occupation/intertwiner amplitudes satisfy

`|I_L| <= 1`, `|J_{L,q}| <= 1`.

So the exact plaquette law is now compressed from an infinite face-character
alphabet to a countable local occupation alphabet `N^2`.

## Theorem 3: exact finite local alphabet truncation

Define the finite local state space

`Omega_K = {(m,n) in N^2 : m+n <= K}`.

Its exact size is

`|Omega_K| = (K+1)(K+2)/2`.

Let

`q_K(beta) = P(Poisson(beta) > K)`

since `M+N` is Poisson with mean `beta`.

Now truncate the exact occupation law by discarding all global plaquette-state
configurations for which any plaquette has `M_p + N_p > K`.

Then the normalized partition function and normalized anchored numerator satisfy
the exact uniform bounds

`|z_L(beta) - z_{L,K}(beta)| <= epsilon_K(P)`

and

`|n_{L,q}(beta) - n_{L,q,K}(beta)| <= epsilon_K(P)`

with

`epsilon_K(P) = 1 - (1 - q_K(beta))^P`.

So finite local alphabets are now available with rigorous tail control.

This is the useful exact compression that survives the finite low-carrier no-go.

## Beta = 6 local truncation data

At `beta = 6`, `M+N ~ Poisson(6)`. The runner gives:

- `K = 12`: `|Omega_K| = 91`, `q_K = 0.008827483517898`
- `K = 14`: `|Omega_K| = 120`, `q_K = 0.001400353833362`
- `K = 16`: `|Omega_K| = 153`, `q_K = 0.000174877435413`
- `K = 18`: `|Omega_K| = 190`, `q_K = 0.000017597042094`
- `K = 20`: `|Omega_K| = 231`, `q_K = 0.000001455106990`

So a finite local alphabet of size `231` already leaves a per-plaquette tail of
about `1.46 x 10^-6` on the normalized local law.

## Relation to the earlier carrier theorems

This compression is consistent with the earlier exact local results:

- `m+n = 0` carries the trivial local sector
- `m+n = 1` is the first fundamental / anti-fundamental carrier level
- `m+n = 2` is where the first `6`, `6bar`, and `8` face characters appear
- the first explicit singular-link `X` and `B` sectors still sit inside the
  same exact occupation/intertwiner law

So this note does not replace the earlier low-carrier theorems.
It reorganizes them into an exact countable occupation law with a rigorous
finite-state truncation scheme.

## What this closes

This closes the remaining representation problem from the previous branch state.

The branch no longer ends at:

> exact law known, but no useful exact compression.

It now ends at:

> exact law known, exact finite small low-carrier closure impossible, and exact
> Poissonized occupation/intertwiner compression available with explicit finite
> local alphabets and explicit truncation tails.

The next note,

- `docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md`

then closes the exact local link-state side as well.

## Honest remaining scope

This note still does **not** by itself give:

- a direct closed form for `<P>(6)`,
- a fast transfer-matrix evaluator for the full finite lattice,
- or a tiny exact finite-state recursion.

But those are now acceleration questions, not missing-law questions and not
missing-compression questions in the basic exact sense.

## Paper-safe conclusion

The strongest clean statement is now:

> the plaquette is analytically derived exactly as a finite-periodic-lattice
> `SU(3)` character/intertwiner foam ratio, and that exact infinite-carrier law
> admits an exact Poissonized occupation/intertwiner compression with finite
> local alphabets `Omega_K` and explicit uniform truncation tails.

That is a real analytic compression, and it avoids the false claim of an exact
small finite `B/X` closure.

## Commands run

```bash
python3 scripts/frontier_poissonized_occupation_intertwiner_compression.py
```

Output summary:

- exact local Poissonized identity `e^(-beta) w_beta(U) = E[a(U)^M conj(a(U))^N]`
- exact finite-lattice normalized occupation/intertwiner law
- exact finite local alphabet `Omega_K`
- explicit tail `q_K = P(Poisson(beta) > K)` at `beta = 6`
- explicit uniform normalized-law truncation bound `epsilon_K(P)`
