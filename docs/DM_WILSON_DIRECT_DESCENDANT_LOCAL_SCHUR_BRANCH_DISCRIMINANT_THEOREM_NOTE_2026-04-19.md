# DM Wilson Direct-Descendant Local Schur Branch-Discriminant Theorem

**Date:** 2026-04-19
**Status:** exact source-side reduction theorem on the open DM gate. The
current positive-branch discriminator is local to the descended charged Schur
block `L_e = Schur_{E_e}(D_-)`: once `L_e` is fixed, the descended Hermitian
law reconstructs `H_e` exactly, and the explicit branch scalar is
`Delta_src(dW_e^H) = det(H_e(L_e))`. This is not yet a derivation of the
physical sign law from `Cl(3)` on `Z^3`; it is an exact reduction of the live
branch-choice object to the local descended block.
**Primary runner:**
`scripts/frontier_dm_wilson_direct_descendant_local_schur_branch_discriminant_theorem_2026_04_19.py`
(`PASS=10 FAIL=0`).

## Question

After the exact projected-source branch-discriminant theorem
(`Delta_src(dW_e^H) = det(H_e)`) and the exact local Schur reduction theorem
(`dW_e^H` depends only on `L_e = Schur_{E_e}(D_-)`), does the current DM
source-side branch-choice rule still depend on ambient Wilson completion data?

Or can the live positive-branch object already be stated exactly as a local
sign law on the descended charged block?

## Bottom line

It can already be stated locally.

Once the charged Schur block `L_e` is fixed, the descended first-variation law

`X -> Re Tr(L_e^(-1) X) = Tr(H_e X)`

reconstructs the full Hermitian block

`H_e = (L_e^(-1) + (L_e^(-1))^*) / 2`

exactly from the standard `9` Hermitian probe responses.

The explicit projected-source branch scalar

`Delta_src`

then equals

`det(H_e(L_e))`

exactly. Therefore the current positive-branch rule

`Delta_src > 0`

is already a **local sign law on `L_e`**. Changing the ambient completion of
`D_-` while keeping `L_e` fixed cannot change that scalar.

This is the exact source-side reduction that the reviewed DM packet still
needed:

- the branch discriminator is no longer only an external statement about the
  baseline-connected component of `det(H) != 0`;
- it is an explicit local scalar of the descended microscopic block.

What remains open is narrower:

- derive the actual microscopic right-sensitive law for `L_e`,
- and derive why the physical solution must satisfy the positive sign.

## The theorem

Assume only the exact local Schur setting already isolated on the reviewed
Wilson direct-descendant route:

1. an invertible charge-preserving microscopic operator
   `D = D_0 (+) D_- (+) D_+`;
2. a charged support split `E_- = E_e (+) E_r` with `dim E_e = 3`;
3. the local Schur block `L_e = Schur_{E_e}(D_-)`.

Let

`H_e(L_e) := (L_e^(-1) + (L_e^(-1))^*) / 2`.

Let `dW_e^H` denote the descended Hermitian first-variation law on `Herm(3)`,
and let `Delta_src(dW_e^H)` be the explicit cubic projected-source scalar from
the branch-discriminant theorem.

> **Theorem.** Once `L_e` is fixed:
>
> 1. the `9` descended Hermitian responses reconstruct `H_e(L_e)` exactly;
> 2. `Delta_src(dW_e^H) = det(H_e(L_e))` exactly;
> 3. therefore the current positive-branch discriminator is local to `L_e`;
> 4. any two ambient completions with the same `L_e` induce the same
>    `Delta_src` and the same branch sign.

So the live branch-choice object has already reduced to one scalar sign law on
the local descended block.

## Why this matters

This closes a real source-side ambiguity.

Before this note, the branch packet contained two exact ingredients:

- the branch scalar `Delta_src` on `dW_e^H`;
- the local-Schur fact that `dW_e^H` depends only on `L_e`.

But the combined consequence had not been stated explicitly:

> the branch sign is already a local invariant of `L_e`.

That matters because it removes one fake remaining gap. The live DM route is
not waiting on additional ambient Wilson completion data once `L_e` is fixed.
It is waiting on the finer right-sensitive microscopic law for `L_e` itself.

## Relation to the frozen triplet

The theorem also sharpens the role of the exact projected-source triplet
channels `(gamma, E1, E2)`.

On the live basin set:

- Basin 1,
- Basin 2,
- Basin X,

all carry the same exact triplet

- `gamma = 1/2`,
- `E1 = sqrt(8/3)`,
- `E2 = sqrt(8)/3`,

while `Delta_src` changes sign:

- Basin 1: positive,
- Basin 2: negative,
- Basin X: negative.

So the current positive-branch rule cannot factor only through the frozen
triplet channels. The missing source-side selector is strictly finer and
right-sensitive, exactly as the reviewed transport-status note claimed.

## What this closes

- the ambiguity over whether the branch scalar still depends on ambient
  completion data once `L_e` is fixed;
- the gap between the local-Schur reduction and the projected-source branch
  discriminant;
- the idea that the frozen triplet channels might already encode the live
  branch sign.

## What this does not close

- the actual microscopic law for `L_e`;
- a derivation of the positive sign from `Cl(3)` on `Z^3`;
- the final DM flagship lane.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_SOURCE_FAMILY_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_FLAGSHIP_FRONTIER_COLLAPSE_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_local_schur_branch_discriminant_theorem_2026_04_19.py
```

Expected:

- `PASS=10 FAIL=0`
