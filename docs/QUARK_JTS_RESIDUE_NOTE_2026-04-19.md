# Quark JTS Residue

**Date:** 2026-04-19
**Lane:** Quark up-amplitude.
**Status:** support - structural or confirmatory support note
identification is now derived from retained bimodule geometry:

```text
Pert(p) = H_(1+5) ≅ J^1_p(A_p),   A_p = p + H_(1+5).
```

The older Route-2 readout-conditioned section family remains a separate,
stricter realization problem, but it is no longer load-bearing for ISSR1.

**Companion forcing theorem:**
`docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`

**Companion JTS theorem:**
`docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`

---

## 0. Executive summary

The original ISSR1 packet reduced the lane to a named residue:

```text
Pert(p)  ?=  J^1_p(Sect(B)).
```

That residue is now closed on retained geometry.

The key retained object is the exact physical reduced carrier

```text
H_(1+5) = span{e_1, e_5},
```

with physical projector ray

```text
p = cos_d e_1 + sin_d e_5.
```

The perturbation cone used by ISSR1 is

```text
Pert(p) = { psi = a_u e_5 + a_d p : (a_u, a_d) in R^2 }.
```

Since `{p, e_5}` is a basis of `H_(1+5)`, this cone is exactly the physical
carrier plane. The canonical affine physical carrier

```text
A_p := p + H_(1+5)
```

is the canonical physical-route affine subspace of the retained bimodule
through `p`. Equivalently, the retained packet fixes the physical-route section
functor

```text
Sect_phys(B ; p)
  := { eps -> p_eps in B : p_0 = p, p_eps - p in H_(1+5) }.
```

therefore has tangent plane

```text
T_p A_p = H_(1+5) = Pert(p),
```

and hence

```text
Pert(p) ≅ J^1_p(Sect_phys(B ; p)) = J^1_p(A_p)
```

canonically by the affine section law

```text
psi <-> j^1_0(eps -> p + eps psi).
```

So JTS is derived. The earlier Route-2 readout ambiguity survives only as a
different realization problem and does not block ISSR1.

---

## 1. Statement of JTS

> **JTS (Jet-To-Section identification).** Let
> `B = Cl(3)/Z_3 ⊗ Cl_CKM(1⊕5)` with unit ray
> `p = cos_d v_1 + i sin_d v_5`. Then the bimodule perturbation cone
>
> ```text
> Pert(p) := { psi = a_u (i v_5) + a_d p : (a_u, a_d) in R^2 }
> ```
>
> is canonically the `1`-jet space at `p` of deforming sections on the exact
> physical-route carrier through `p`.

On the retained physical carrier we write `e_5 = i v_5`, so the cone is

```text
Pert(p) = { a_u e_5 + a_d p }.
```

---

## 2. The exact carrier geometry

The same-day exact `1(+)5` theorem fixes the canonical reduced carrier

```text
H_(1+5) = span{e_1, e_5}.
```

Because

```text
p = cos_d e_1 + sin_d e_5,
cos_d != 0,
```

one has

```text
e_1 = (p - sin_d e_5) / cos_d.
```

So `{p, e_5}` is a basis of `H_(1+5)`, and therefore

```text
Pert(p) = H_(1+5)
```

as a real vector plane.

This is the geometric step the old packet was missing.

---

## 3. Canonical jet identification

Define the affine physical carrier

```text
A_p := p + H_(1+5).
```

Because `A_p ⊂ B`, this is equivalently the canonical physical-route section
functor

```text
Sect_phys(B ; p)
  := { eps -> p_eps in B : p_0 = p, p_eps - p in H_(1+5) for all eps }.
```

A deforming section of `A_p` over the `eps`-line is a smooth curve

```text
eps -> p_eps in A_p
```

with `p_0 = p`.

For every `psi in Pert(p)`, the affine section

```text
gamma_psi(eps) = p + eps psi
```

is canonical and has `1`-jet

```text
j^1_0(gamma_psi).
```

Differentiation at `eps = 0` recovers `psi`, so

```text
Pert(p) -> J^1_p(Sect_phys(B ; p)) = J^1_p(A_p),
psi -> j^1_0(gamma_psi)
```

is a canonical bijection.

This is JTS.

---

## 4. Why the old Route-2 obstruction no longer blocks JTS

The exact conditional family

```text
Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*
```

still depends on the unresolved readout map `P_R`. So it does not define one
unique exact Route-2 realization.

But that family is stricter than what JTS needs. JTS requires only the
canonical physical-route section functor inside `B`, and that is now provided
by the exact affine carrier `A_p`.

So the Route-2 readout ambiguity remains real, but it is no longer the JTS
residue.

---

## 5. Role in ISSR1 closure

With JTS resolved, the remaining decisive equality

```text
Pi(psi_phys) = Pi(p)
```

is supplied independently by exact `1(+)5` channel completeness:

```text
Pi_5 p = T_p(a_d e_1) + a_u e_5
=> a_u + a_d sin_d = sin_d.
```

So the closure packet now has two independent pieces:

1. JTS from affine physical carrier geometry.
2. Physical pinning from exact carrier completeness.

Together they close ISSR1.

---

## 6. What remains open

The remaining open point is narrower than the original residue:

- a fully unique Route-2 readout-conditioned spacetime realization is still not
  derived.

That is no longer the JTS problem and no longer load-bearing for quark LO
closure.

---

## 7. Cross-references

- `docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`
  — load-bearing JTS theorem.
- `docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`
  — updated closure note.
- `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
  — exact `1(+)5` physical pinning identity.
- `docs/QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`
  — narrower unresolved Route-2 realization issue.
- `docs/QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md`
  — readout-conditioned family `Xi_P`.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [quark_jts_affine_physical_carrier_theorem_note_2026-04-19](QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md)
- `QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)
- [strc_lo_collinearity_theorem_note_2026-04-19](STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md)
- [quark_route2_exact_readout_map_note_2026-04-19](QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md)
- [quark_route2_exact_time_coupling_note_2026-04-19](QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md)
