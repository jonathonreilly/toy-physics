# Quark Bimodule NORM-Existence Theorem

**Date:** 2026-04-19  
**Lane:** Quark up-amplitude / bimodule LO closure  
**Status:** retained existence theorem on the current branch; this does not
yet select the physical law uniquely, but it resolves the binary residue
"does an LO split law exist on the bimodule?" with a clean **yes**  
**Primary runner:** `scripts/frontier_quark_bimodule_norm_existence_theorem.py`

---

## 0. Executive summary

Let

```text
I := R * Im(p)
```

be the one-real imaginary channel on the retained CKM projector ray
`p = cos_d + i sin_d`, with `|p|^2 = 1` and retained scalar claim

```text
a_d = rho = Re(r) = 1 / sqrt(42).
```

For this branch, call a real-linear ownership-response map on the normalized
channel `I` a **NORM law**.

The exact bridge family already on the branch,

```text
a_u(kappa) = Im(p) * (1 - rho * kappa),
kappa in [sqrt(6/7), 1],
```

lifts directly to actual complementary endomorphisms of `I`:

```text
D_kappa(x) = rho * kappa * x,
U_kappa(x) = (1 - rho * kappa) * x.
```

Here `D_kappa` is the down-sector share and `U_kappa` is the up-sector share.
They satisfy

```text
U_kappa + D_kappa = Id_I
```

for every retained `kappa`, and applying `U_kappa` to `Im(p)` reproduces the
exact quark bridge amplitudes.

So the open quark residue is no longer:

> "does any LO split law exist on the bimodule?"

It is now the sharper question:

> which NORM law on the bimodule is canonical, natural, or retained-physics
> selected?

---

## 1. Setup

Retained quark atoms:

```text
p = cos_d + i sin_d,      |p|^2 = 1,
r = rho + i eta = p / sqrt(7),
rho = 1 / sqrt(42),
sin_d = sqrt(5/6),
supp = 6/7,
delta_A1 = 1/42.
```

The same-day endpoint-obstruction theorem already proved that the quark packet
carries the exact one-parameter bridge family

```text
a_u(kappa) = sin_d * (1 - rho * kappa),
```

with three distinguished exact points:

```text
kappa_support = sqrt(6/7),
kappa_target  = 48/49,
kappa_BICAC   = 1.
```

The present note asks a different question: do those bridge amplitudes
correspond to actual bimodule split maps on the retained imaginary channel?

---

## 2. The theorem

Because `I = R * Im(p)` is one-real-dimensional, every real-linear
endomorphism of `I` is multiplication by a scalar.

For any retained `kappa in [sqrt(6/7), 1]`, define

```text
D_kappa := rho * kappa * Id_I,
U_kappa := (1 - rho * kappa) * Id_I.
```

Then:

1. `D_kappa, U_kappa in End_R(I)` are well-defined real-linear maps;
2. they are complementary:

   ```text
   U_kappa + D_kappa = Id_I;
   ```

3. they are positive contractions on the physical interval because
   `0 <= rho * kappa <= rho < 1`;
4. evaluating on `Im(p)` reproduces the exact bridge family:

   ```text
   U_kappa(Im(p)) = Im(p) * (1 - rho * kappa) = a_u(kappa).
   ```

### Formal statement

> **Theorem (NORM existence on the quark bimodule).** On the retained
> one-real imaginary channel `I = R * Im(p)` of the CKM `1 (+) 5` bimodule,
> every retained bridge factor `kappa in [sqrt(6/7), 1]` determines a real
> complementary split law
>
> ```text
> D_kappa(x) = rho * kappa * x,
> U_kappa(x) = (1 - rho * kappa) * x.
> ```
>
> In particular, the support, target, and BICAC points are all realized by
> actual LO bimodule split maps on `I`.

So the binary existence question has the answer **yes**.

---

## 3. Distinguished exact laws

### 3.1 Support law

At

```text
kappa_support = sqrt(supp) = sqrt(6/7),
```

the up map gives

```text
U_support(Im(p))
= sin_d * (1 - rho * sqrt(6/7))
= sin_d * (1 - 1/7)
= sin_d * 6/7
= sin_d * supp.
```

### 3.2 Retained target law

At

```text
kappa_target = 1 - supp * delta_A1 = 48/49,
```

the up map gives

```text
U_target(Im(p)) = sin_d * (1 - 48 rho / 49) = 0.7748865611...
```

which is the retained preferred target already present in the RPSR packet.

### 3.3 BICAC law

At

```text
kappa_BICAC = 1,
```

the split law becomes

```text
D_BICAC(x) = rho x,
U_BICAC(x) = (1-rho) x.
```

Evaluating on `Im(p)` gives

```text
a_u = sin_d * (1-rho),
```

hence

```text
a_u + rho * sin_d = sin_d,
```

which is exactly STRC-LO / BICAC.

---

## 4. Scientific consequence

This theorem does **not** yet choose the physical endpoint. The same-day
endpoint-obstruction theorem remains fully in force: the current retained
packet does not derive `kappa = 1`.

What changes is the shape of the residue.

Before this note, a fair question was:

> perhaps the quark packet does not even define a genuine LO split law on the
> bimodule.

After this note, that possibility is gone. The branch now knows that:

1. the retained bridge interval lifts to honest complementary bimodule maps on
   the one-real imaginary channel;
2. the three exact bridge points are not just scalar formulas, but actual
   endomorphism laws on `I`;
3. the remaining issue is **canonicalization**, not existence.

That is the precise role of this theorem.

---

## 5. Relation to what remains

The next same-day strengthening is the NORM-naturality theorem:

- `docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bimodule_norm_naturality_theorem.py`

That theorem shows that if one asks for a normalized affine extension of the
split law across the full ownership interval `a in [0,1]`, then BICAC is the
unique such extension.

So the open quark gap is now bracketed exactly:

- **NORM existence:** yes;
- **endpoint uniqueness from retained packet alone:** no;
- **unique normalized affine extension:** yes, but only after adding the
  naturality requirement.

---

## 6. Runner summary

The companion runner verifies:

- the retained interval is nonempty;
- support / target / BICAC all lie in it;
- each `D_kappa, U_kappa` is real-linear on `I`;
- complementarity `U_kappa + D_kappa = Id_I`;
- positivity / contractivity on the retained interval;
- exact recovery of the bridge amplitudes;
- exact support endpoint, exact target value, and exact BICAC closure.

Expected runner status:

```text
PASS=10
FAIL=0
```
