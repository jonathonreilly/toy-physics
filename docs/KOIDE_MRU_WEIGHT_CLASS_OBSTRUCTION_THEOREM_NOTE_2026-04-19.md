# Koide MRU Weight-Class Obstruction Theorem

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide / MRU
**Status:** exact obstruction theorem on the unreduced carrier, now paired with
its branch-local resolution. The theorem itself is unchanged: the unreduced
`3 x 3` determinant carrier counts weights `(1,2)` and therefore cannot force
MRU by itself. What has changed is that the exact missing object is now
derived: the scalar charged-lepton lane reduces canonically to the two-slot
real-isotype carrier `(+ , perp)` before the log-volume / extremal law is
applied.
**Primary runner:** `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`

---

## 0. Executive summary

On the `d = 3` cyclic carrier,

```text
E_+    = r_0^2 / 3   = 3 a^2,
E_perp = (r_1^2 + r_2^2) / 6 = 6 |b|^2.
```

For the weighted block-log-volume family

```text
S_{mu,nu} = mu log(E_+) + nu log(E_perp)
```

at fixed `E_tot = E_+ + E_perp`, every interior stationary leaf is

```text
kappa := a^2 / |b|^2 = 2 mu / nu.
```

So:

- MRU is the equal-weight leaf `(mu, nu) = (1,1)`;
- the unreduced determinant carrier

  ```text
  det(alpha P_+ + beta P_perp) = alpha beta^2
  ```

  carries weights `(1,2)` and lands at `kappa = 1`.

That obstruction remains exact.

The branch-local resolution is not to dispute that calculation. It is to
derive the carrier reduction the theorem said was missing:

```text
(r_0, r_1, r_2)  ->  (rho_+, rho_perp)
```

with

```text
rho_+^2    = E_+,
rho_perp^2 = E_perp,
```

because the scalar lane quotients the internal `SO(2)` frame of the real
doublet. On that reduced carrier,

```text
det diag(rho_+, rho_perp) = rho_+ rho_perp,
```

so the same log-volume law is equal-weight automatically and lands at MRU.

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

Writing

```text
H = (r_0/3) B_0 + (r_1/6) B_1 + (r_2/6) B_2,
```

the real-trace norms give

```text
||B_0||^2 = 3,
||B_1||^2 = ||B_2||^2 = 6,
```

and therefore

```text
E_+    = r_0^2 / 3 = 3 a^2,
E_perp = (r_1^2 + r_2^2) / 6 = 6 |b|^2.
```

Hence

```text
E_+ = E_perp
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

---

## 2. Weighted block-log-volume classification

Define

```text
S_{mu,nu}(H) := mu log(E_+) + nu log(E_perp),
```

with `mu, nu > 0`, under fixed total block power

```text
E_+ + E_perp = E_tot.
```

The Lagrange equations give the unique interior stationary point

```text
E_+^*    = mu / (mu + nu) * E_tot,
E_perp^* = nu / (mu + nu) * E_tot.
```

So

```text
E_+^* / E_perp^* = mu / nu,
```

and therefore

```text
kappa = 2 mu / nu.
```

This theorem is exact and unchanged.

---

## 3. The unreduced determinant obstruction

Let `P_+` and `P_perp` be the `C_3` singlet and doublet projectors on the
unreduced `3 x 3` carrier, with ranks `1` and `2`.

Any positive operator that is scalar on these two isotypic blocks has the form

```text
D = alpha P_+ + beta P_perp.
```

Because the non-trivial block has multiplicity `2`,

```text
det(D) = alpha beta^2,
log|det D| = log alpha + 2 log beta.
```

So the unreduced determinant law carries weight pair `(1,2)` and therefore
selects

```text
kappa = 2 * 1 / 2 = 1.
```

That is the exact obstruction:

> no log-volume law applied on the unreduced `3 x 3` isotypic-scalar carrier
> can force MRU.

---

## 4. The exact missing object, now derived

The missing object identified above was:

```text
a retained 1:1 real-isotype measure, or an equivalent canonical reduction to a
two-slot (+, perp) carrier before applying the log-volume / extremal law.
```

The branch now derives it.

The non-trivial real doublet

```text
V_perp = span_R{B_1, B_2}
```

has an internal orthonormal frame freedom

```text
(B_1, B_2) -> (B_1', B_2') = (B_1, B_2) R(theta),
```

under which

```text
(r_1, r_2) -> R(theta) (r_1, r_2)
```

but

```text
r_1^2 + r_2^2
```

is invariant. So the scalar lane does not retain the ordered Cartesian pair
inside the doublet plane. It retains only the doublet radius.

Therefore the exact scalar reduction is

```text
(r_0, r_1, r_2)  ->  (rho_+, rho_perp),
```

with

```text
rho_+    = |r_0| / sqrt(3),
rho_perp = sqrt(r_1^2 + r_2^2) / sqrt(6).
```

Equivalently,

```text
rho_+^2    = E_+,
rho_perp^2 = E_perp.
```

This is the exact retained two-slot real-isotype carrier the earlier theorem
said would be sufficient.

---

## 5. Resolution on the reduced carrier

Apply the same log-volume / extremal law on the reduced carrier

```text
D_red = diag(rho_+, rho_perp).
```

Then

```text
det(D_red) = rho_+ rho_perp,
log|det D_red| = log rho_+ + log rho_perp.
```

At fixed reduced total power

```text
rho_+^2 + rho_perp^2 = E_tot,
```

the unique positive stationary point is

```text
rho_+^2 = rho_perp^2 = E_tot / 2.
```

So

```text
E_+ = E_perp
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

In other words:

> the obstruction remains exact on the unreduced carrier, but it no longer
> blocks the lane because the branch has now derived the carrier reduction it
> said was missing.

---

## 6. Scientific consequence

The theorem should now be read in two layers:

1. **negative layer:** unreduced determinant multiplicities alone do not force
   MRU;
2. **positive layer:** the scalar charged-lepton lane does not live on that
   unreduced carrier. It lives on the real-isotype quotient, where there are
   only two slots and the log-volume law is exactly the MRU leaf.

So the weight-class obstruction has been converted from a blocker into the
load-bearing explanation of why the quotient step was necessary.

---

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_mru_weight_class_obstruction_theorem.py
```

The runner now certifies both:

1. the old obstruction on the unreduced `3 x 3` carrier, and
2. the exact real-isotype quotient reduction that resolves it on this branch.
