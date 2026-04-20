# Koide Scalar-Lane Observable-Radius Theorem

**Date:** 2026-04-20  
**Lane:** Charged-lepton Koide `\kappa` / MRU route  
**Status:** retained closure theorem for the 2026-04-20 open import `I6`. The
observable-principle side of the scalar charged-lepton lane does not retain an
ordered Cartesian frame on the real `C_3` doublet; it retains only the doublet
radius.  
**Primary runner:**
`scripts/frontier_koide_scalar_lane_observable_radius_theorem_2026_04_20.py`

---

## 0. Question

The remaining open-import register isolated one structural postulate on the MRU
route:

> why is the real doublet on the scalar charged-lepton lane quotiented by
> `SO(2)`, so that only its radius survives as scalar data?

This note derives that quotient directly from the retained observable-principle
stack.

## 1. Bottom line

The relevant object on the MRU lane is not an arbitrary function on the
doublet plane. It is the **local scalar jet** supplied by the observable
principle:

```text
W[J] = log|det(D + J)| - log|det D|.
```

By `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`, local scalar observables are the
source derivatives of `W`. On the retained `hw=1` cyclic bundle, the
non-trivial real isotype is the doublet

```text
V_perp = span_R{B_1, B_2}.
```

The `C_3` generator acts on `V_perp` as the 120-degree real rotation
`R_{2pi/3}`. Therefore any local scalar quadratic jet on the doublet is a
real symmetric bilinear form `S` satisfying

```text
R_{2pi/3}^T S R_{2pi/3} = S.
```

Solving this exactly gives

```text
S = lambda I_2.
```

So the observable-principle scalar jet on `V_perp` is forced to be

```text
lambda (r_1^2 + r_2^2),
```

not `lambda_1 r_1^2 + lambda_2 r_2^2`, not `r_1 r_2`, and not any
frame-sensitive Cartesian slot.

Equivalently, on the full singlet-plus-doublet carrier, the most general
retained quadratic local scalar is exactly

```text
Q(r_0, r_1, r_2) = alpha r_0^2 + beta (r_1^2 + r_2^2).
```

So the scalar charged-lepton lane factors through the exact quotient

```text
R ⊕ R^2 / SO(2),
```

with quotient coordinates

```text
rho_+^2    = E_+    = r_0^2 / 3,
rho_perp^2 = E_perp = (r_1^2 + r_2^2) / 6.
```

That is precisely the missing law needed by the MRU route.

## 2. Input stack

This theorem uses only retained ingredients already on branch:

1. `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
2. `KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
3. `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
4. `KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`

The load-bearing import is Theorem 2 of the observable-principle note:
**local scalar observables are source derivatives of the unique additive
CPT-even scalar generator**. On the MRU lane that means the relevant local
scalar data is a symmetric bilinear jet.

## 3. Theorem

**Theorem (observable-radius law on the scalar charged-lepton lane).** Let

```text
V = R B_0 ⊕ V_perp,
V_perp = span_R{B_1, B_2},
```

with `C_3` acting trivially on `B_0` and by the 120-degree rotation
`R_{2pi/3}` on `V_perp`. Then:

1. every local scalar quadratic jet supplied by the observable principle on
   `V_perp` is a real symmetric bilinear form `S` commuting with
   `R_{2pi/3}`;
2. the exact invariance equation
   `R_{2pi/3}^T S R_{2pi/3} = S` forces `S = lambda I_2`;
3. therefore the doublet contribution to any retained local scalar quadratic
   jet is exactly `lambda (r_1^2 + r_2^2)`;
4. on the full scalar lane, the general retained quadratic local scalar is
   exactly
   `Q = alpha r_0^2 + beta (r_1^2 + r_2^2)`;
5. consequently the MRU lane retains only the quotient coordinates
   `(rho_+, rho_perp)`, not an ordered Cartesian frame on `V_perp`.

### Proof

Write the `C_3` action on the doublet in the orthogonal basis `(B_1, B_2)` as

```text
R :=
[ cos(2pi/3)  -sin(2pi/3) ]
[ sin(2pi/3)   cos(2pi/3) ].
```

Let

```text
S =
[ a  b ]
[ b  c ]
```

be a real symmetric bilinear form on the doublet. Observable-principle local
scalar jets are scalar under the retained `C_3` action, so they satisfy

```text
R^T S R = S.
```

Direct solution gives

```text
b = 0,
c = a,
```

hence `S = a I_2`. Therefore for doublet coordinates `(r_1, r_2)`:

```text
Q_perp(r_1, r_2) = [r_1 r_2] S [r_1 r_2]^T = a (r_1^2 + r_2^2).
```

Now add the singlet coordinate `r_0`. A generic real symmetric quadratic form
on `(r_0, r_1, r_2)` has cross-terms

```text
r_0 r_1,  r_0 r_2,  r_1 r_2.
```

Imposing invariance under `diag(1, R)` kills the singlet-doublet cross terms
and again forces the doublet block to be scalar. So the full invariant
quadratic family is exactly

```text
Q(r_0, r_1, r_2) = alpha r_0^2 + beta (r_1^2 + r_2^2).
```

Finally, with the retained cyclic normalizations

```text
E_+    = r_0^2 / 3,
E_perp = (r_1^2 + r_2^2) / 6,
```

the scalar lane is exactly the two-slot quotient carrier

```text
(rho_+, rho_perp),   rho_+^2 = E_+,   rho_perp^2 = E_perp.
```

QED.

## 4. Consequence for MRU

The open import `I6` asked for a retained derivation of the `SO(2)` quotient
instead of treating it as a structural postulate. This theorem supplies that
derivation in exactly the scope the MRU route needs:

- the observable-principle local scalar jet sees the doublet only through
  `r_1^2 + r_2^2`;
- the reduced carrier `(rho_+, rho_perp)` is therefore retained;
- the reduced log-volume law of
  `KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` now sits on a
  retained carrier, not on a postulated quotient.

So the MRU route no longer needs the open `SO(2)`-quotient import.

## 5. Scope

What is proved:

- the local scalar-jet content of the observable principle on the MRU lane is
  exactly `SO(2)`-invariant on the doublet;
- the retained scalar lane factors through the doublet radius;
- `I6` is closed for the MRU route.

What is not claimed:

- this note does not classify arbitrary nonlocal or orientation-sensitive
  observables on the doublet plane;
- it does not derive `Q = 2/3` or `delta = 2/9`;
- it does not replace the separate spectrum/operator bridge route, which
  remains an independent closure route for `kappa = 2`.

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_scalar_lane_observable_radius_theorem_2026_04_20.py
```

Expected final line:

```text
PASS=13 FAIL=0
```
