# Koide MRU Weight-Class Obstruction Theorem

**Date:** 2026-04-19  
**Lane:** Charged-lepton Koide / MRU  
**Status:** exact obstruction theorem on the current branch; this does not
derive MRU from retained charged-lepton structure, but it identifies the exact
missing law/object with current-branch precision  
**Primary runner:** `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`
(expected `PASS=26 FAIL=0`)

---

## 0. Executive summary

The MRU note already proved that on the `d = 3` cyclic carrier,

```text
MRU  <=>  E_+ = E_perp  <=>  kappa := a^2 / |b|^2 = 2,
```

where

```text
E_+    = r_0^2 / 3   = 3 a^2,
E_perp = (r_1^2 + r_2^2) / 6 = 6 |b|^2.
```

This note goes one step further. It classifies the whole block-log-volume
selector family on the same carrier and shows:

1. every weighted block law is one scalar leaf `kappa = 2 mu / nu`;
2. MRU is exactly the equal-weight leaf `mu = nu`;
3. the retained `log|det|` / observable-principle carrier on the unreduced
   `3 x 3` circulant block necessarily carries weights `(mu, nu) = (1, 2)`,
   because `det(alpha P_+ + beta P_perp) = alpha beta^2`;
4. therefore the current branch cannot derive MRU from that determinant law
   alone;
5. the exact missing object is a retained law or carrier reduction that counts
   the non-trivial **real** doublet once rather than twice.

So the remaining gap is no longer just "derive `kappa = 2` somehow." It is:

> **produce a retained `1:1` real-isotype measure on the charged-lepton cyclic
> carrier, or an equivalent canonical reduction to a two-slot `(+ , perp)`
> carrier before applying a log-volume / extremal law.**

---

## 1. Setup

On the retained `hw=1` cyclic compression,

```text
H = a I + b C + b^bar C^2,
```

with canonical real cyclic basis

```text
B_0 = I,
B_1 = C + C^2,
B_2 = i (C - C^2).
```

The real-trace / Frobenius norms are

```text
||B_0||^2 = 3,
||B_1||^2 = ||B_2||^2 = 6.
```

Writing

```text
H = (r_0/3) B_0 + (r_1/6) B_1 + (r_2/6) B_2,
```

the canonical singlet and real-doublet block powers are

```text
E_+    := ||(r_0/3) B_0||^2      = r_0^2 / 3 = 3 a^2,
E_perp := ||(r_1/6) B_1 + (r_2/6) B_2||^2
        = (r_1^2 + r_2^2) / 6
        = 6 |b|^2.
```

Hence

```text
E_+ = E_perp  <=>  3 a^2 = 6 |b|^2  <=>  kappa = 2.
```

This is exactly the MRU equality from
`docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.

---

## 2. The weighted block-log-volume classification

Define the full two-parameter family

```text
S_{mu,nu}(H) := mu log(E_+) + nu log(E_perp),
```

with `mu, nu > 0`, under fixed total block power

```text
E_tot := E_+ + E_perp.
```

Using one Lagrange multiplier,

```text
L = mu log(E_+) + nu log(E_perp) - lambda (E_+ + E_perp - E_tot),
```

the unique interior stationary point is

```text
E_+^*    = mu / (mu + nu) * E_tot,
E_perp^* = nu / (mu + nu) * E_tot.
```

Therefore

```text
E_+^* / E_perp^* = mu / nu.
```

Translated back to cyclic responses,

```text
nu * (r_0^2 / 3) = mu * (r_1^2 + r_2^2) / 6
<=> 2 nu r_0^2 = mu (r_1^2 + r_2^2).
```

Translated to circulant coordinates,

```text
nu * 3 a^2 = mu * 6 |b|^2
<=> nu a^2 = 2 mu |b|^2
<=> kappa := a^2 / |b|^2 = 2 mu / nu.
```

### Formal theorem

> **Theorem (MRU weight-class classification).** On the charged-lepton
> `d = 3` cyclic carrier, every weighted block-log-volume law
> `S_{mu,nu} = mu log(E_+) + nu log(E_perp)` at fixed total block power selects
> exactly one leaf
>
> ```text
> kappa = 2 mu / nu.
> ```
>
> In particular, MRU is exactly the equal-weight leaf
>
> ```text
> mu = nu  <=>  E_+ = E_perp  <=>  kappa = 2.
> ```

This is stronger than the earlier equivalence statements because it identifies
the whole selector family and pinpoints MRU as one specific weight choice.

---

## 3. Retained observable-principle obstruction

Let `P_+` and `P_perp` be the `C_3` singlet and doublet projectors on the
retained `3 x 3` circulant carrier. They have ranks `1` and `2`.

Any circulant kernel diagonal in this split has the form

```text
D = alpha P_+ + beta P_perp.
```

Because the non-trivial block has multiplicity `2`,

```text
det(D) = alpha beta^2.
```

So the retained determinant law is

```text
log|det D| = log(alpha) + 2 log(beta),
```

which is the weight pair `(mu, nu) = (1, 2)`, not `(1, 1)`.

Feeding `(1, 2)` into the classification theorem gives

```text
kappa = 2 mu / nu = 1.
```

So the determinant-native stationary leaf is

```text
E_+ : E_perp = 1 : 2,
```

not the MRU leaf

```text
E_+ : E_perp = 1 : 1.
```

### Consequence

> **Corollary (unreduced determinant obstruction).** No extremal law that
> depends only on the unreduced `3 x 3` circulant determinant multiplicities
> can force MRU. The multiplicity pattern itself fixes the wrong weight ratio.

This makes the obstruction precise: the branch does not merely lack "some
selector." It specifically lacks a retained law that counts the whole
non-trivial real doublet as **one** block.

---

## 4. The exact missing object

The theorem identifies the exact missing structure:

### Option A: a retained real-isotype measure

A retained extremal law that assigns one unit of measure to each **real**
isotype block,

```text
(+)  and  (perp),
```

would give

```text
S_real = log(E_+) + log(E_perp),
```

hence MRU immediately.

### Option B: a canonical carrier reduction

Equivalently, if the branch could justify a canonical reduction from the full
unreduced `3 x 3` circulant carrier to a two-slot real-isotype carrier

```text
D_red = diag(alpha, beta),
```

then

```text
det(D_red) = alpha beta,
log|det D_red| = log(alpha) + log(beta),
```

which is exactly the equal-weight law.

### Honest status

That `1:1` real-isotype measure / reduction is **not** presently retained in
the branch. The note therefore does not derive MRU. It proves that this is now
the exact missing object.

---

## 5. Why this narrows the gap beyond equivalence

Before this note, the sharp honest statement was:

```text
MRU  <=>  kappa = 2,
```

but not why the physical carrier should satisfy MRU.

After this note, the sharper statement is:

```text
all block-log-volume laws on the cyclic carrier are classified by (mu, nu),
the retained determinant law forces (1, 2),
MRU is exactly (1, 1).
```

So the remaining charged-lepton task is no longer a vague selector search. It
is the single concrete problem:

> derive a retained `1:1` real-isotype weighting law, or derive the canonical
> reduction that makes that weighting lawful.

That is the strongest precise obstruction I can land today using only the
current branch.

---

## 6. Cross-checks and scope

### Established here

1. the entire weighted block-log-volume family on the charged-lepton cyclic
   carrier is classified exactly by `kappa = 2 mu / nu`;
2. MRU is the equal-weight leaf `mu = nu`;
3. the retained `log|det|` multiplicity on the unreduced `3 x 3` carrier is
   forced to `(1, 2)`;
4. therefore the exact missing object is a retained real-isotype measure or
   canonical reduction.

### Not established here

- no derivation that the physical charged-lepton carrier actually admits the
  required `1:1` reduction;
- no promotion of the charged-lepton Koide lane to a retained theorem;
- no claim about quarks, neutrinos, or the phase selector.

---

## 7. Reproduction

```bash
python3 scripts/frontier_koide_mru_weight_class_obstruction_theorem.py
```

Expected final line:

```text
PASS=26 FAIL=0
```

---

## 8. Citations

- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
- `docs/KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`
- `docs/KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md`
- `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
- `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
- `docs/KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md`
