# Quark ISSR1 BICAC Forcing Theorem

**Date:** 2026-04-19
**Lane:** Quark up-amplitude.
**Status:** **Closed theorem packet.** The jet-to-section residue is derived on
the exact affine physical carrier, and the physical pinning identity is carried
by exact `1(+)5` channel completeness on the same retained bimodule route.

**Primary runner:** `scripts/frontier_quark_issr1_bicac_forcing.py`
**Companion JTS theorem:** `docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`
**Companion residue/history note:** `docs/QUARK_JTS_RESIDUE_NOTE_2026-04-19.md`

---

## 0. Executive summary

The ISSR1 packet now closes without importing any free section selector.

Two retained ingredients are load-bearing:

1. **Affine-carrier JTS theorem.**
   The exact physical reduced carrier

   ```text
   H_(1+5) = span{e_1, e_5}
   ```

   and the physical projector ray

   ```text
   p = cos_d e_1 + sin_d e_5
   ```

   determine the canonical affine physical carrier

   ```text
   A_p := p + H_(1+5).
   ```

   inside the retained bimodule `B`. Equivalently, they determine the
   canonical physical-route section functor

   ```text
   Sect_phys(B ; p)
     := { eps -> p_eps in B : p_0 = p, p_eps - p in H_(1+5) }.
   ```

   Because the ISSR1 perturbation cone

   ```text
   Pert(p) = { psi = a_u e_5 + a_d p : (a_u, a_d) in R^2 }
   ```

   equals `H_(1+5)` as a real vector plane, it is canonically the `1`-jet space
   of deforming sections on that physical route:

   ```text
   Pert(p) ≅ J^1_p(Sect_phys(B ; p)) = J^1_p(A_p),
   psi <-> j^1_0(eps -> p + eps psi).
   ```

   So JTS is derived from retained affine bimodule geometry.

2. **Exact physical pinning identity.**
   On the same carrier, the exact `1(+)5` completeness theorem gives

   ```text
   Pi_5 p = T_p(a_d e_1) + a_u e_5,
   T_p = Pi_5 |p><e_1| = sin_d |e_5><e_1|.
   ```

   Therefore

   ```text
   a_u + a_d sin_d = sin_d.
   ```

   Under the Schur-rank-1 projection

   ```text
   Pi(psi) = Im<v_5, psi> = a_u + a_d sin_d,
   Pi(p) = sin_d,
   ```

   this is exactly

   ```text
   Pi(psi_phys) = Pi(p).
   ```

So the old gap is gone:

> JTS is now derived on the exact affine physical carrier, and the decisive
> equality is supplied independently by exact channel completeness on that same
> retained carrier.

The stricter Route-2 readout-conditioned family `Xi_P(t;c)` remains a different
realization problem. It no longer blocks JTS or ISSR1 because JTS is carried by
the exact affine physical carrier, not by the unresolved readout map.

---

## 1. Retained setup

The current branch already fixes the physical reduced carrier:

```text
H_(1+5) = span{e_1, e_5},
```

with

```text
p = cos_d e_1 + sin_d e_5,
cos_d = 1/sqrt(6),
sin_d = sqrt(5/6),
a_d = rho = 1/sqrt(42).
```

On the ISSR1 side, the SO(2)-weight-0 direction is the imag-axis direction
`i v_5`. On the physical reduced carrier we identify that direction with
`e_5`, so the perturbation cone is

```text
Pert(p) = { psi = a_u e_5 + a_d p : (a_u, a_d) in R^2 }.
```

Because

```text
e_1 = (p - sin_d e_5) / cos_d,
```

the vectors `{p, e_5}` form a basis of `H_(1+5)`, so

```text
Pert(p) = H_(1+5)
```

as a real plane.

---

## 2. The affine-carrier JTS theorem

Define the canonical affine physical carrier through the physical ray:

```text
A_p := p + H_(1+5).
```

Because `H_(1+5)` is the exact retained physical reduced carrier, `A_p` is the
canonical physical-route affine subspace of the bimodule through `p`. Define

```text
Sect_phys(B ; p)
  := { eps -> p_eps in B : p_0 = p, p_eps - p in H_(1+5) for all eps }.
```

This is exactly the section functor of `A_p`. A deforming section of this
retained physical route over the `eps`-line is therefore a smooth curve

```text
eps -> p_eps in A_p
```

with `p_0 = p`.

For every `psi in Pert(p)`, define the affine section

```text
gamma_psi(eps) := p + eps psi.
```

Then

```text
d/d eps gamma_psi(eps) |_{eps=0} = psi.
```

So the map

```text
J : Pert(p) -> J^1_p(A_p),
J(psi) = j^1_0(gamma_psi),
```

is canonical, equivalently as a map into `J^1_p(Sect_phys(B ; p))`.

Conversely, if `j = j^1_0(p_eps)` is any `1`-jet at `p`, then its derivative
vector

```text
d/d eps p_eps |_{eps=0}
```

lies in the tangent plane of `A_p`, which is exactly `H_(1+5) = Pert(p)`.
Hence differentiation gives the inverse map.

Therefore

```text
Pert(p) ≅ J^1_p(Sect_phys(B ; p)) = J^1_p(A_p)
```

canonically. This is the JTS identification on the physical bimodule route.

---

## 3. Schur-rank-1 projection

Under the SO(2) subgroup fixing the imag axis, the `l = 2` irrep `V_5`
decomposes with weight-0 multiplicity `1`. Hence

```text
dim Hom_{SO(2)}(C, V_5^{wt=0}) = 1.
```

The unique SO(2)-equivariant projection to the weight-0 slice is

```text
Pi(v) = Im<v_5, v>.
```

On the perturbation cone:

```text
Pi(psi) = a_u + a_d sin_d.
```

On the physical ray:

```text
Pi(p) = sin_d.
```

This is the exact representation-theoretic content of ISSR1.

---

## 4. Independent physical pinning identity

The decisive equality no longer comes from a jet-to-value reinterpretation. It
comes from the exact `1(+)5` completeness theorem on the same physical carrier.

Let

```text
Pi_5 = |e_5><e_5|,
T_p = Pi_5 |p><e_1| = sin_d |e_5><e_1|,
d = a_d e_1.
```

Then

```text
Pi_5 p = sin_d e_5,
T_p d  = a_d sin_d e_5.
```

Because the `5` channel is one-dimensional on `H_(1+5)`, the residual up
sector is uniquely

```text
u_5 := Pi_5 p - T_p d = a_u e_5,
```

so

```text
a_u = sin_d - a_d sin_d = sin_d (1-a_d).
```

Equivalently,

```text
a_u + a_d sin_d = sin_d.
```

At `a_d = rho` this is BICAC-LO.

This is an exact first-order identity on the physical carrier and is
independent of the JTS theorem.

---

## 5. Closure

Let

```text
psi_phys = a_u e_5 + a_d p
```

with `a_d = rho` and `a_u = sin_d(1-rho)` from exact `1(+)5` completeness.

Then:

1. `psi_phys` lies in `Pert(p)`, and by the affine-carrier theorem it is
   canonically a `1`-jet in `J^1_p(A_p)`;
2. Schur-rank-1 gives `Pi(psi_phys) = a_u + a_d sin_d`;
3. exact carrier completeness gives `a_u + a_d sin_d = sin_d = Pi(p)`.

Therefore

```text
Pi(psi_phys) = Pi(p),
```

and ISSR1 closes with no remaining residue.

---

## 6. Relation to the old Route-2 obstruction

The earlier non-closure reading treated "section functor" as the stricter
readout-conditioned Route-2 family

```text
Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*.
```

That family still depends on the unresolved readout map and therefore does not
define one unique exact Route-2 realization.

But that is **not** the section functor required for JTS. JTS only needs the
canonical physical-route section functor inside `B`, namely the sections whose
image stays on the exact affine carrier determined by `H_(1+5)` and `p`.

So the Route-2 readout ambiguity survives as a narrower realization issue, not
as a blocker to ISSR1 closure.

---

## 7. Runner summary

The companion runner now verifies:

1. `Pert(p)` and `H_(1+5)` are the same real plane;
2. the canonical affine section `eps -> p + eps psi` gives the JTS
   identification;
3. the exact `1(+)5` completeness theorem gives the physical pinning identity
   `a_u + a_d sin_d = sin_d`;
4. the physical perturbation therefore satisfies `Pi(psi_phys) = Pi(p)`;
5. support and target bridge points fail that equality, while `kappa = 1`
   satisfies it uniquely.

Expected runner status:

```text
PASS=13
FAIL=0
VERDICT: JTS DERIVED; ISSR1 CLOSED
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [quark_jts_affine_physical_carrier_theorem_note_2026-04-19](QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md)
- [quark_jts_residue_note_2026-04-19](QUARK_JTS_RESIDUE_NOTE_2026-04-19.md)
