# EW Current Matching Rule No-Go Closure Note

**Date:** 2026-05-03
**Type:** no_go
**Status:** proposed_retained no-go closure of the former open gate. The
retained Fierz/channel-count theorem fixes the exact adjoint fraction
`F_adj = (N_c^2 - 1) / N_c^2 = 8/9` at `N_c = 3`, but the current retained
framework primitives do not fix the physical EW readout functional that
weights the singlet/disconnected current after CMT factorization.
**Primary runner:** `scripts/frontier_ew_current_matching_rule_no_go.py`

## Cited Authority

- [EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  derives the exact representation-theoretic ratio
  `(N_c^2 - 1) / N_c^2` and explicitly separates it from the physical
  matching rule.

Plain-text bounded context, not load-bearing dependencies of this no-go:
`docs/EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md` and
`docs/RCONN_DERIVED_NOTE.md`. They provide the existing bounded/OZI route,
but neither supplies an exact disconnected-current coefficient.

## Claim

**No-go theorem (matching-rule underdetermination).** On the current retained
packet consisting of:

1. `N_c = 3` and the exact SU(`N_c`) Fierz decomposition
   `q qbar = 1 + adj`;
2. the exact channel fraction
   `F_adj = dim(adj) / dim(q qbar) = (N_c^2 - 1) / N_c^2`;
3. the CMT mean-field factorization `U -> u_0 V`, which multiplies both
   singlet and adjoint two-link EW-current channel contributions by the same
   `u_0^2`; and
4. the bounded OZI statement that disconnected current contributions are
   suppressed as `O(1/N_c^2)` but not assigned an exact coefficient,

the package-level EW matching factor is not determined. In particular, the
connected-trace selector

```text
kappa_EW = 0
```

is an extra matching premise, not a consequence of the retained primitives.

## Coefficient Parametrization

Normalize the post-CMT channel sum to

```text
T = C + S = 1,
```

where

```text
C = F_adj = (N_c^2 - 1) / N_c^2,
S = 1 - F_adj = 1 / N_c^2.
```

Let `kappa_EW` be the physical disconnected-current readout coefficient:

```text
Pi_EW^phys(kappa_EW) = C + kappa_EW S.
```

The CMT/lattice normalization reads the total channel sum `T`. Therefore the
EW alpha-level matching factor is

```text
K_EW(kappa_EW)
  = T / Pi_EW^phys(kappa_EW)
  = 1 / (F_adj + kappa_EW (1 - F_adj)).                  (1)
```

Equivalently, `K_EW(kappa_EW) = 1 / (F_adj + kappa_EW (1 - F_adj))`.

At `N_c = 3`, equation (1) becomes

```text
K_EW(kappa_EW) = 1 / (8/9 + kappa_EW/9).
```

The package-level `9/8` factor is the special case

```text
K_EW(0) = 9/8,
```

which is exactly the connected-trace selector. The full-trace readout is also
compatible with the retained Fierz/CMT algebra:

```text
K_EW(1) = 1.
```

Thus the retained packet admits at least two completions with identical
Fierz arithmetic, identical CMT scaling, and identical `O(1/N_c^2)`
disconnected-channel size, but different EW matching factors.

## Proof

### 1. Fierz fixes channel dimensions, not the readout functional

The Fierz/channel-count theorem fixes only the decomposition

```text
q qbar = 1 + adj,
dim(1) = 1,
dim(adj) = N_c^2 - 1.
```

It therefore fixes

```text
C / T = (N_c^2 - 1) / N_c^2,
S / T = 1 / N_c^2.
```

No equation in that theorem assigns the physical EW current to `C` rather
than to `C + kappa_EW S`. The value of `kappa_EW` is a statement about the
lattice-to-continuum current readout, not about representation dimension.

### 2. CMT is color-blind at the relevant two-link level

The CMT substitution `U -> u_0 V` gives the same two-link factor to every
EW-current channel:

```text
C(U) = u_0^2 C(V),
S(U) = u_0^2 S(V),
T(U) = u_0^2 T(V).
```

Consequently equation (1) is invariant under CMT scaling:

```text
T(U) / (C(U) + kappa_EW S(U))
  = T(V) / (C(V) + kappa_EW S(V)).
```

CMT can neither select `kappa_EW = 0` nor exclude `kappa_EW = 1`, because it
treats both channels uniformly.

### 3. Bounded OZI suppression does not fix the coefficient

For bounded `kappa_EW = O(1)`, the disconnected readout contribution relative
to the connected channel is

```text
kappa_EW S / C
  = kappa_EW / (N_c^2 - 1)
  = O(1/N_c^2).
```

This includes `kappa_EW = 0`, `kappa_EW = 1`, and any finite intermediate
coefficient. The OZI route therefore supplies a suppression class, not the
exact coefficient needed to make `K_EW = 9/8`.

### 4. Independence witness

Construct two admissible completions of the retained packet:

```text
Completion A: kappa_EW = 0,  K_EW = 9/8.
Completion B: kappa_EW = 1,  K_EW = 1.
```

Both completions satisfy the exact Fierz ratio `C/T = 8/9`, both satisfy
the same color-blind CMT scaling law, and both keep the disconnected channel
at `O(1/N_c^2)` relative size. Since they agree on all retained premises but
disagree on the package-level EW matching factor, the matching rule is
underdetermined by those premises.

Therefore the connected-trace EW readout cannot be derived from the current
retained primitives alone. A future positive theorem would need to add an
actual lattice-current selector argument that fixes `kappa_EW = 0`, or an
exact disconnected-current computation that fixes the same value.

## Consequences

The former open gate is closed negatively:

- exact Fierz/channel-count arithmetic remains retained-bounded support for
  `F_adj = 8/9`;
- the package-level EW coefficient must be written as
  `K_EW(kappa_EW)`, not as an unconditional retained `9/8`;
- any numerical use of `sqrt(9/8)` for `g_1(v)` or `g_2(v)` is the conditional
  specialization `kappa_EW = 0`;
- empirical agreement after choosing `kappa_EW = 0` is not a derivation and
  must not be used to fit or ratify the coefficient.

Safe downstream wording:

> The EW normalization lane is bounded by a named matching coefficient
> `kappa_EW`: `K_EW(kappa_EW) = 1 / (8/9 + kappa_EW/9)`. The familiar
> `9/8` alpha-level correction is the connected-trace specialization
> `kappa_EW = 0`, not an unconditional retained theorem.

Unsafe downstream wording:

> The framework derives the exact `9/8` EW color-projection correction.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_current_matching_rule_no_go.py
```

The runner verifies the exact rational arithmetic, the CMT invariance of the
free coefficient, the OZI boundedness class, the two-completion independence
witness, and the direct downstream wording guardrails.
