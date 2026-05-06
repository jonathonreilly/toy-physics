# DM Neutrino Weak Vector Theorem

**Status:** exact support theorem; re-audit target for the
representation-content scope only
**Date:** 2026-04-15  
**Branch:** `codex/dm-across-the-line`

---

## Status

**EXACT representation theorem; base normalization closed elsewhere**

The branch now closes one more exact part of the neutrino bridge:

> the direct local chiral bridge family  
> `Y_i = P_R Gamma_i P_L`  
> is an exact weak vector under the derived `SU(2)` bivectors.

This is real progress. It upgrades the bridge family from "an axis-picked
operator that seems plausible" to "a theorem-grade spin-1 weak multiplet."

At the stage of this theorem alone, it still did **not** close the neutrino
base coupling. The reason is sharp: the weak-vector covariance equations are
homogeneous, so they do not fix the overall coefficient. The later
bosonic-normalization theorem closes that base-normalization step separately.

---

## The Theorem

Let

- `B_a = -(i/4) sum_{m,n=1}^3 eps_{amn} Gamma_m Gamma_n` be the
  normalized derived weak bivectors, equivalently
  `B_1 = -(i/2) Gamma_2 Gamma_3` and cyclic permutations
- `gamma_5` be the `3+1` chirality operator on `C^16`
- `P_L = (1 + gamma_5)/2`, `P_R = (1 - gamma_5)/2`
- `Y_i = P_R Gamma_i P_L`

Then:

1. the bivectors `B_a` form exact `su(2)` on the taste space
2. the spatial `Gamma_i` family on `C^8` transforms as a vector:

   `[B_a, Gamma_b] = i eps_{abc} Gamma_c`

3. the same is true for the chiral bridge family on `C^16`:

   `[B_a, Y_b] = i eps_{abc} Y_c`

4. the adjoint Casimir on both families is exactly spin-1:

   `sum_a [B_a,[B_a, X_b]] = 2 X_b`

   for `X_b = Gamma_b` or `Y_b`

5. the bridge family is trace-orthogonal:

   `Tr(Y_i^dag Y_j) = 8 delta_ij`

So the direct post-EWSB bridge is now not only selected as `Gamma_1` after
axis choice; the full family `Y_i` is an exact weak-vector multiplet.

---

## Restricted-Packet Algebra

This note does not require an external authority for the load-bearing
commutator. The exact packet used by the runner is:

- `sigma_x = [[0,1],[1,0]]`
- `sigma_y = [[0,-i],[i,0]]`
- `sigma_z = [[1,0],[0,-1]]`

On `C^8`, the spatial taste generators are

- `Gamma_1 = sigma_x x I x I`
- `Gamma_2 = sigma_y x sigma_x x I`
- `Gamma_3 = sigma_y x sigma_y x sigma_x`

On `C^16`, the bridge packet uses

- `Gamma_0 = sigma_z x sigma_z x sigma_z x sigma_x`
- `Gamma_1 = sigma_x x I x I x I`
- `Gamma_2 = sigma_z x sigma_x x I x I`
- `Gamma_3 = sigma_z x sigma_z x sigma_x x I`
- `gamma_5 = Gamma_0 Gamma_1 Gamma_2 Gamma_3`
- `P_L = (I + gamma_5)/2`, `P_R = (I - gamma_5)/2`

These matrices obey the Clifford relations

`Gamma_i Gamma_j + Gamma_j Gamma_i = 2 delta_ij I`

for the spatial `Gamma_i`. The runner also checks that `gamma_5`
anticommutes with each spatial `Gamma_i` and that `P_L`, `P_R` are
complementary orthogonal projectors.

The commutator identity then follows directly. For any spatial Clifford
triple,

`[Gamma_m Gamma_n, Gamma_b] = 2 delta_{nb} Gamma_m - 2 delta_{mb} Gamma_n`.

Therefore

`[B_a, Gamma_b]`

`= -(i/4) sum_{m,n} eps_{amn} [Gamma_m Gamma_n, Gamma_b]`

`= i sum_c eps_{abc} Gamma_c`.

Because `gamma_5` anticommutes with each spatial `Gamma_i`, every even
product `Gamma_m Gamma_n` commutes with `gamma_5`. Hence
`[B_a, P_L] = [B_a, P_R] = 0`, and

`[B_a, Y_b] = [B_a, P_R Gamma_b P_L]`

`= P_R [B_a, Gamma_b] P_L`

`= i sum_c eps_{abc} P_R Gamma_c P_L`

`= i sum_c eps_{abc} Y_c`.

The spin-1 Casimir follows by applying the same commutator twice:

`sum_a [B_a,[B_a,Y_b]] = 2 Y_b`,

using `sum_{a,c} eps_{abc} eps_{acd} = -2 delta_bd`. Trace orthogonality is
the finite-matrix trace identity

`Tr(Y_i^dag Y_j) = Tr(P_L Gamma_i Gamma_j P_L) = 8 delta_ij`,

checked exactly by the paired runner on the explicit tensor-product matrices.

---

## What This Actually Buys

This theorem closes the representation content of the bridge family.

Before this pass, the branch had:

- an exact operator-selection theorem (`Gamma_1`, not `Xi_5`)
- an exact second-order cascade geometry
- an exact weak-matching obstruction to reusing the old `G5` route

Now it also has:

- an exact statement that the direct bridge family carries the correct weak
  spin-1 transformation law

That means the bridge family is no longer just "the thing picked by axis
selection." It is a canonically transforming weak object in the derived
operator algebra.

This matters because it removes one more possible harsh objection:

> "Maybe `Gamma_1` is just a basis artifact and not a genuine weak-sector
> operator family."

That objection is now dead.

---

## Why This Still Does Not Fix The Coefficient

The key obstruction is algebraic and exact:

if `Y_i` obeys

`[B_a, Y_b] = i eps_{abc} Y_c`

then for any scalar `lambda`,

`[B_a, lambda Y_b] = i eps_{abc} lambda Y_c`

as well.

Likewise the Casimir equation is homogeneous:

`sum_a [B_a,[B_a, lambda Y_b]] = 2 lambda Y_b`.

So the weak-vector theorem fixes the **representation law**, but not the
**absolute normalization**.

This is exactly why the theorem does **not** by itself promote any particular
base benchmark.

That equality would require an extra ingredient beyond covariance, for example:

- a new weak-sector Ward / Slavnov-Taylor-style identity for the direct bridge
- or a theorem-grade Higgs / bridge field-normalization principle
- or a stronger gauge-Higgs unification result than the branch currently has

At the stage of this note, none of those existed on this branch yet. The later
bosonic-normalization theorem supplies the field-normalization selector, but
not the second-order suppression law.

---

## Relation To Gauge Universality

This also clarifies the scope of the older gauge-universality theorem.

That theorem proves that the three hw=1 fermion species carry isomorphic gauge
representations. It is a representation-content result. It does **not** prove
coefficient sharing between different operator families.

The new weak-vector theorem is the same kind of result:

- it proves the direct bridge family is an exact weak vector
- it does **not** prove the coefficient multiplying that family in the physical
  neutrino Yukawa equals the weak gauge coupling

So the branch should not treat "exact weak representation" and
"exact coefficient sharing" as the same achievement. They are not.

---

## Updated Blocker

The denominator blocker is now even narrower:

> the branch has fixed the direct local bridge family and its exact weak
> representation content, but it still lacks the theorem that fixes the
> suppressed second-order coefficient below the now-selected base surface.

Equivalently:

> the remaining problem is no longer operator selection or weak covariance. It
> is the suppressed second-order coefficient on the exact `Gamma_1` return.

That is the right Nature-bar statement.

---

## Verification

Verified by:

- [`scripts/frontier_dm_neutrino_weak_vector_theorem.py`](../scripts/frontier_dm_neutrino_weak_vector_theorem.py)
- captured stdout:
  [`outputs/frontier_dm_neutrino_weak_vector_theorem_2026-05-06.txt`](../outputs/frontier_dm_neutrino_weak_vector_theorem_2026-05-06.txt)

Command:

`python3 scripts/frontier_dm_neutrino_weak_vector_theorem.py`

The runner checks:

- explicit `C^8` and `C^16` Clifford relations
- `gamma_5` chirality anticommutation and `P_L`, `P_R` projector algebra
- exact `su(2)` closure of the weak bivectors
- exact vector transformation of `Gamma_i`
- exact vector transformation of `Y_i = P_R Gamma_i P_L`
- exact spin-1 Casimir `2`
- trace orthogonality of the bridge family
- explicit rescaling invariance of the covariance equations

Latest captured result:

`RESULT: 18 PASS, 0 FAIL`
