# DM Neutrino Base Normalization Audit

**Date:** 2026-04-15  
**Branch:** `codex/dm-across-the-line`  
**Script:** `scripts/frontier_dm_neutrino_base_coupling_theorem.py`
**Superseded by:** `DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`

---

## Status

**EXACT HISTORICAL AUDIT**

The direct local post-EWSB neutrino Dirac operator is now fixed as `Gamma_1`.
What is **not** fixed is the physical normalization of that bridge.

This audit was run to test whether the branch can already promote a statement
like

`y_nu^(0) / g_weak = 1 / sqrt(2)`

to theorem status.

It cannot.

---

## Exact Result

Let

- `Y = P_R Gamma_1 P_L` be the direct local chiral bridge on `C^16`
- `Gamma_1` be the corresponding unprojected weak-axis operator

Then the branch now proves three exact statements at once:

1. **Full-space Frobenius normalization**

   `Tr(Y^dag Y) / 16 = 1/2`

   while

   `Tr(Gamma_1^dag Gamma_1) / 16 = 1`

   so the **full `C^16` Frobenius ratio** is

   `sqrt( Tr(Y^dag Y) / Tr(Gamma_1^dag Gamma_1) ) = 1 / sqrt(2)`.

2. **Active chiral-subspace normalization**

   On the active source and target chiral halves,

   `Tr(Y^dag Y) / dim(P_L) = 1`

   and

   `Tr(P_L Gamma_1^dag Gamma_1) / dim(P_L) = 1`,

   so the **active-subspace Frobenius ratio** is exactly `1`.

3. **Operator norm**

   The nonzero singular values of `Y` are all `1`, exactly matching the
   singular values of `Gamma_1` on its active bridge. So the **operator-norm
   ratio** is also exactly `1`.

---

## What This Means

The direct local bridge is exact, but its normalization is not uniquely fixed
by the current branch.

There are at least two equally natural framework-native normalizations:

- **full-space normalization** -> `y_nu^(0) / g_weak = 1 / sqrt(2)`
- **active-subspace normalization** -> `y_nu^(0) / g_weak = 1`

So the branch does **not** yet have a theorem-grade base-coupling derivation.

The new weak-vector theorem does not remove this ambiguity. It proves the
bridge family `Y_i = P_R Gamma_i P_L` transforms exactly as a weak spin-1
multiplet, but that covariance is homogeneous under `Y_i -> lambda Y_i`, so it
still does not select the absolute normalization.

---

## What Remains Exact

The same audit confirms the generation-resolved return structure remains exact.

For any second-order channel kernel

`K = a P_{O_0} + b P_{T_2}`,

the induced return on `T_1` is exactly

`R(a,b) = diag(a,b,b) x I_time`.

So the only open coefficient freedom is:

- the overall physical normalization of the direct bridge
- the two channel coefficients `a` and `b`

There is **not** an arbitrary `3 x 3` Yukawa matrix hiding here.

---

## Updated Harsh Blocker

The denominator blocker is now sharper:

> derive a theorem-grade physical normalization principle for the direct
> `Gamma_1` neutrino bridge, and then derive the dynamical second-order
> channel coefficients `a` and `b`.

Until that happens, the second-order cascade remains a bounded mechanism, not
an axiom-level neutrino Yukawa derivation.
