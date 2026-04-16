# DM Neutrino Weak Matching Obstruction

**Date:** 2026-04-15  
**Branch:** `codex/dm-across-the-line`  
**Script:** `scripts/frontier_dm_neutrino_weak_matching_obstruction.py`

---

## Status

**EXACT OBSTRUCTION**

This note should now be read as a **historical obstruction** to the old
active-space matching route. The later bosonic-normalization theorem selects
the full-space `g_weak/sqrt(2)` benchmark as the physical base surface.

The branch now has a precise answer to the next denominator question:

> can the exact top-Yukawa protection route be reused to derive a theorem-grade
> weak matching `y_nu^(0) = g_weak` for the direct local `Gamma_1` bridge?

No.

---

## What Survives

Three pieces remain intact:

1. The direct local post-EWSB neutrino Dirac operator is fixed as `Gamma_1`.
2. On the active chiral bridge, `P_R Gamma_1 P_L` has unit operator norm.
3. The Higgs doublet mass relation still uses the exact group-theory factor
   `m = y v / sqrt(2)`.

So if a weak-sector matching theorem existed, the natural active-space
benchmark would indeed be

`y_nu^(0) = g_weak`.

---

## Exact Obstruction

The top-Yukawa protection chain works because `G5` is central in `Cl(3)`:

`[G5, X] = 0` for all relevant taste / gauge operators `X`.

That centrality is what allows the non-perturbative factorization step

`D[G5] = G5 D[I]`,

which then feeds the Slavnov-Taylor completion.

For the neutrino bridge, the relevant operator is `Gamma_1`, not `G5`.
The new runner proves:

1. `Gamma_1` is **not** central in `Cl(3)`.
   In particular:
   - `[Gamma_1, Gamma_2] != 0`
   - `[Gamma_1, Gamma_3] != 0`
   - `[Gamma_1, B_2] != 0`
   - `[Gamma_1, B_3] != 0`

2. `Gamma_1` fails propagator factorization:

   `S(k) Gamma_1 != Gamma_1 S(k)`

   for generic lattice momentum.

3. `Gamma_1` also fails generic gauge-chain factorization:

   `(B_2 S B_3) Gamma_1 != Gamma_1 (B_2 S B_3)`.

So the exact `G5`-based non-renormalization / matching route cannot simply be
ported over to the neutrino lane.

This also means the newer `g_bare` rigidity theorem does **not** close the
problem by itself. That theorem removes an extra scalar coefficient only after
the physical operator family is already fixed. Here the live gap is exactly the
missing coefficient-sharing theorem between the weak gauge vertex and the
direct `Gamma_1` fermion bridge.

---

## Consequence

The open theorem is no longer vague. It is now:

> derive a genuinely new weak-sector Ward / Slavnov-Taylor-style identity for
> the direct `Gamma_1` bridge, strong enough to force coefficient sharing
> between the weak gauge vertex and the direct local neutrino Yukawa bridge.

Without that new identity, the old active-space `y_nu^(0) = g_weak` route
remains only a bounded historical comparator, not a theorem.

---

## Updated Harsh Blocker

The denominator blocker is now maximally sharp:

1. The direct local operator is fixed: `Gamma_1`.
2. The old top-Yukawa matching machinery is proven not to transfer.
3. Therefore the remaining missing ingredient is a new weak-sector matching
   theorem for `Gamma_1` itself.

The later bosonic-normalization theorem changes the forward path:
the physical base surface is no longer the active-space benchmark at all.
What remains open is the suppressed second-order coefficient below the now
selected `g_weak/sqrt(2)` base surface.

If it does not, then the neutrino base coupling stays bounded and the DM
denominator remains bounded with `k_B = 8` as the best structural candidate,
not a derivation.
