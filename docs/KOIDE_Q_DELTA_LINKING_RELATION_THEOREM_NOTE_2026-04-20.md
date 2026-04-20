# Koide `Q`-`delta` Linking Relation Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide `Q` / Brannen phase `delta`  
**Status:** exact structural linking theorem. This note does **not** claim a
new retained derivation of the physical Koide value or of the physical phase in
radians. It isolates the exact shared arithmetic behind them and shows that,
once the one-singlet-plus-one-doublet leaf is fixed at retained `d = 3`, the
two target numbers are the same `Z_3` doublet count scaled by `d` and `d^2`.
The remaining open Berry-side object is therefore a **unit bridge**, not a new
numerical fit.

**Primary runner:** `scripts/frontier_koide_q_delta_linking_relation.py`
(`PASS=13 FAIL=0`).

---

## 0. Executive summary

The retained `C_3` Plancherel split on the charged-lepton Koide lane is

```text
R^3 = 1 (+) 2,
```

that is, one real singlet plus one real doublet. On a normalized `d`-slot
state, let

```text
sigma = |parallel to singlet|^2 / |state|^2.
```

Then the Koide invariant is

```text
Q = 1 / (d sigma).
```

So on the equal singlet/doublet norm leaf `sigma = 1/2`,

```text
Q_struct = 2 / d.
```

Independently, one complex doublet coordinate `b` contributes exactly `2` real
degrees of freedom inside the full `d x d` Hermitian algebra of real dimension
`d^2`. So the structural phase ratio is

```text
delta_struct = 2 / d^2.
```

Therefore

```text
delta_struct = Q_struct / d.
```

At retained `d = 3`,

```text
Q_struct = 2/3,
delta_struct = 2/9,
delta_struct = (2/3)/3.
```

This is the exact new content. It means the two charged-lepton numbers are not
arithmetically independent. The remaining open issue is whether the
dimensionless structural value `2/9` is **forced to be the physical phase in
radians**.

---

## 1. Structural `Q` arithmetic on the `1 (+) 2` split

Let `u = (1, ..., 1) / sqrt(d)` and let `v` be a normalized positive amplitude
state. Write

```text
v = v_parallel + v_perp,
sigma = |v_parallel|^2.
```

Then

```text
sum_i v_i = sqrt(d) <u, v>,
Q = |v|^2 / (sum_i v_i)^2 = 1 / (d sigma).
```

So on the leaf where the singlet and the single real doublet carry equal total
norm,

```text
sigma = 1/2  ->  Q = 2/d.
```

At `d = 3`, this gives the charged-lepton Koide value `Q = 2/3`.

This is not a new derivation of the leaf itself. The theorem's point is
different: it isolates the exact arithmetic once the leaf is fixed.

---

## 2. Structural `delta` arithmetic from doublet counting

On the circulant character side, one complex doublet coordinate

```text
b = |b| e^{i delta}
```

carries exactly two real degrees of freedom: `Re b` and `Im b`. The full
Hermitian `d x d` algebra has real dimension `d^2`. So the canonical
dimensionless ratio attached to one doublet channel is

```text
delta_struct = 2 / d^2.
```

At `d = 3`, this is exactly

```text
delta_struct = 2 / 9.
```

This is the same dimensional-ratio identity already buried in Appendix A.2 of
the April 18 circulant-character note, but here it is stated as the headline
arithmetic theorem and tied directly to the Koide leaf.

---

## 3. The linking relation

Combining the previous two identities gives

```text
Q_struct = 2 / d,
delta_struct = 2 / d^2,
delta_struct = Q_struct / d.
```

So at retained `d = 3`,

```text
delta_struct = Q_struct / 3.
```

This is the important scientific reduction:

- the charged-lepton Koide number and the Brannen phase number are the same
  unique-doublet count read against two different ambient sizes;
- they are not two numerically unrelated imports;
- any future retained derivation of the Koide leaf automatically fixes the
  structural phase ratio as `Q / 3`.

The runner also checks that this is the correct single-doublet continuation of
the arithmetic. Away from `d = 3`, it differs from the old ambient
`(d - 1) / d^2` wedge arithmetic. The two formulas agree at `d = 3` only by
accident.

---

## 4. Why `d = 3` matters

The same runner verifies the small-d real-irrep pattern:

- `d = 2`: one sign irrep, no real doublet;
- `d = 3`: exactly one real doublet and no sign irrep;
- `d >= 4`: either an extra sign irrep appears or more than one real doublet
  appears.

So among the low dimensions, `d = 3` is uniquely the

```text
one singlet + one real doublet
```

case. That is exactly the clean charged-lepton arithmetic used here.

---

## 5. Honest remaining gap

This theorem does **not** identify the dimensionless structural `2/9` with the
physical Berry phase measured in radians. That step is the remaining open
Berry-side bridge.

So the honest state after this theorem is:

- the arithmetic collapse is exact;
- the remaining open object is a **unit bridge** or equivalent physical-base
  quantization law;
- the live question is no longer "why these two unrelated numbers?" but
  "why does the structural `2/9` become the physical phase in radians?"

---

## 6. Runner summary

`scripts/frontier_koide_q_delta_linking_relation.py` verifies:

- `Q = 1 / (d sigma)` on the singlet/doublet split;
- `Q_struct = 2/d` on the equal-norm leaf;
- `delta_struct = 2/d^2` from one complex doublet inside `Herm_d`;
- the exact linking relation `delta_struct = Q_struct / d`;
- the `d = 3` specializations `Q = 2/3` and `delta_struct = 2/9`;
- `d = 3` uniqueness of the one-singlet-plus-one-doublet pattern among small
  dimensions;
- mismatch of the old ambient `(d-1)/d^2` continuation away from `d = 3`.
