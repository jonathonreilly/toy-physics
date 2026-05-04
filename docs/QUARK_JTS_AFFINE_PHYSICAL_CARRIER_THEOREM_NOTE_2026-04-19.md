# Quark JTS Affine Physical-Carrier Theorem

**Date:** 2026-04-19
**Lane:** Quark up-amplitude / jet-to-section identification.
**Status:** **Derived theorem.** The perturbation cone on the physical
`1(+)5` reduced bimodule carrier is canonically the `1`-jet space of the
physical-route section functor inside the retained bimodule, i.e. of
deforming sections whose image stays on the exact affine physical carrier
through the projector ray.

**Primary runner:** `scripts/frontier_quark_issr1_bicac_forcing.py`

---

## 0.1 Bimodule provenance

The retained bimodule is

```text
B  =  Cl(3)/Z_3  ⊗  Cl_CKM(1 ⊕ 5)
```

with:

- `Cl(3)/Z_3`: the core flavor algebra, retained from
  `docs/CL3_SM_EMBEDDING_THEOREM.md` and `docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md`
  on main;
- `Cl_CKM(1 ⊕ 5)`: the CKM 1⊕5 Clifford carrier, retained from the CKM
  atlas closure (`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` on main), which
  fixes the unit projector ray `p = cos_d e_1 + sin_d e_5` with
  `cos_d = 1/√6`, `sin_d = √(5/6)`;
- the exact reduced physical carrier `H_(1+5) = span{e_1, e_5}`, retained
  from the same CKM atlas closure as the physical carrier plane through
  the projector ray;
- the retained atoms `a_d = ρ = 1/√42` (from
  `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`),
  `supp = 6/7` and `δ_{A1} = 1/42` (CKM atlas).

No new axiom cost is added by this theorem; the JTS identification follows
by elementary linear algebra on the retained bases (see §1 below).

---

## 0. Theorem

Let

```text
H_(1+5) = span{e_1, e_5}
```

be the exact physical reduced carrier, and let

```text
p = cos_d e_1 + sin_d e_5
```

be the retained unit projector ray on that carrier.

Define the perturbation cone

```text
Pert(p) := { psi = a_u e_5 + a_d p : (a_u, a_d) in R^2 }.
```

Define the affine physical carrier through `p`:

```text
A_p := p + H_(1+5).
```

Because `H_(1+5)` is the exact retained physical reduced carrier, this affine
plane is a canonical affine subspace of the bimodule:

```text
A_p ⊂ B.
```

Define the physical-route section functor at `p` by

```text
Sect_phys(B ; p)
  := { eps -> p_eps in B : p_0 = p,  p_eps - p in H_(1+5) for all eps }.
```

Equivalently, `Sect_phys(B ; p)` is the section functor of `A_p`.

Then:

1. `Pert(p) = H_(1+5)` as a real vector plane.
2. The map

   ```text
   psi -> j^1_0(eps -> p + eps psi)
   ```

   is a canonical bijection

   ```text
   Pert(p) ≅ J^1_p(Sect_phys(B ; p)) = J^1_p(A_p).
   ```

So the jet-to-section identification is derived from retained affine bimodule
geometry.

---

## 1. Proof

Because

```text
p = cos_d e_1 + sin_d e_5
```

with `cos_d = 1/sqrt(6) != 0`, one has

```text
e_1 = (p - sin_d e_5) / cos_d.
```

Hence `{p, e_5}` is a basis of `H_(1+5)`, so

```text
Pert(p) = span{p, e_5} = H_(1+5).
```

Now `A_p = p + H_(1+5)` is the canonical physical-route affine subspace of the
retained bimodule through `p`, with tangent space

```text
T_p A_p = H_(1+5).
```

For any `psi in Pert(p)`, the affine section

```text
gamma_psi(eps) = p + eps psi
```

lies in `A_p`, satisfies `gamma_psi(0)=p`, and has derivative

```text
gamma'_psi(0) = psi.
```

So

```text
J(psi) := j^1_0(gamma_psi)
```

defines a canonical map

```text
Pert(p) -> J^1_p(Sect_phys(B ; p)) = J^1_p(A_p).
```

Conversely, any `1`-jet `j^1_0(p_eps)` in `J^1_p(A_p)` has derivative vector

```text
d/d eps p_eps |_{eps=0} in T_p A_p = H_(1+5) = Pert(p).
```

Differentiation is inverse to `J`. Therefore `J` is a canonical bijection. QED.

---

## 2. Why this closes JTS

The older packet treated JTS as an extra category-theoretic primitive because
it had not isolated the exact physical deformation carrier. Once the exact
physical carrier `H_(1+5)` is retained, no further selector is needed:

- the perturbation cone is already the carrier plane;
- the affine physical carrier through `p` is the canonical physical-route
  subspace of `B`;
- jets of affine sections are canonically tangent vectors.

So the JTS identification is mathematically unavoidable on the retained
carrier.

---

## 3. Relation to the Route-2 readout family

The stricter Route-2 family

```text
Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*
```

still depends on the unresolved readout map and therefore remains a separate
realization problem.

That does not affect the present theorem: the JTS theorem is about the exact
affine physical carrier through `p`, not about one particular readout-coupled
spacetime realization.

---

## 4. Closure consequence

With JTS derived, the remaining physical equality

```text
Pi(psi_phys) = Pi(p)
```

is supplied independently by exact `1(+)5` channel completeness. So ISSR1 is
fully closed on the retained packet.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [cl3_sm_embedding_theorem](CL3_SM_EMBEDDING_THEOREM.md)
- [cl3_color_automorphism_theorem](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- [ckm_atlas_axiom_closure_note](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [quark_projector_parameter_audit_note_2026-04-19](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
