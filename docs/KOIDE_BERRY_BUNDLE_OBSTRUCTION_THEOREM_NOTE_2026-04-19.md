# Koide Berry Bundle Obstruction / Uniqueness Theorem

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide Berry route.
**Status:** support - structural or confirmatory support note
Koide cone. This sharpens the Berry lane by proving that the remaining
bundle/Chern choice is not just underived on the actual base: it is
topologically obstructed there. The old monopole picture can only live on an
auxiliary enlarged surface, not on the true projectivized Koide locus.
**Primary runner:** `scripts/frontier_koide_berry_bundle_obstruction_theorem.py`
(`PASS=30 FAIL=0`).

---

## 0. Executive summary

Let

```text
v = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)) in R^3_{>0}
```

and write `e_+ = (1,1,1)/sqrt(3)`. By the retained algebraic Koide theorem,

```text
Q = 2/3  <=>  sigma := |v_parallel|^2 / |v|^2 = 1/2,
```

so after normalization `|v| = 1` the Koide locus is

```text
K_norm = { s in S^2 : (s . e_+)^2 = 1/2 }.
```

That is a fixed-latitude set, hence one-dimensional:

- the sign-relaxed normalized locus is two circles;
- the physical positive locus is a union of three open arcs on the upper
  circle;
- the `C_3` cyclic permutation acts freely and permutes those three arcs;
- the physical quotient `K_norm^+ / C_3` is therefore an open interval.

This kills the old monopole/Chern packaging on the actual projectivized Koide
cone:

1. every complex `C_3`-equivariant line bundle on `K_norm^+` descends to a
   line bundle on an interval, hence is equivariantly trivial;
2. every equivariant `U(1)` connection on that quotient interval is
   gauge-trivial;
3. therefore there is no nonzero first Chern class and no gauge-invariant
   Berry holonomy on the actual positive projectivized Koide cone.

If one relaxes positivity and works on the sign-relaxed projective conic, the
base becomes `S^1`, but `H^2(S^1; Z) = 0` still forces topological triviality.
So the missing datum is not an integer monopole charge `n`; the only surviving
holonomy datum there is a free flat-connection parameter, and `2/9` remains
unforced there as well.

---

## 1. Retained setup

From
`docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`,
Koide `Q = 2/3` is equivalent to

```text
sigma = |v_parallel|^2 / |v|^2 = 1/2
```

for the `C_3` singlet/doublet split. So on the unit sphere the normalized
sqrt-mass vector satisfies

```text
s . e_+ = +/- 1/sqrt(2),   e_+ := (1,1,1)/sqrt(3).
```

Choose an orthonormal doublet basis

```text
u_1 := (1,-1,0)/sqrt(2),
u_2 := (1,1,-2)/sqrt(6).
```

Then every normalized Koide point has the form

```text
s_+(phi) =  e_+/sqrt(2) + (cos phi u_1 + sin phi u_2)/sqrt(2),
s_-(phi) = -e_+/sqrt(2) + (cos phi u_1 + sin phi u_2)/sqrt(2).
```

The cyclic permutation matrix `C` fixes `e_+` and rotates the doublet plane by
`2 pi / 3`:

```text
C u_1 = -(1/2) u_1 + (sqrt(3)/2) u_2,
C u_2 = -(sqrt(3)/2) u_1 - (1/2) u_2,
```

so

```text
C s_pm(phi) = s_pm(phi + 2 pi / 3).
```

---

## 2. Geometry theorem

> **Theorem 1 (actual projectivized Koide geometry).**
> Let `K_norm` be the normalized Koide locus in `S^2` and let
> `K_norm^+ := K_norm cap R^3_{>0}`.
>
> 1. `K_norm` is one-dimensional: explicitly
>    `K_norm = S^1_+ sqcup S^1_-`, the two latitude circles
>    `s . e_+ = +/- 1/sqrt(2)`.
> 2. `K_norm^+` is a union of three open arcs in `S^1_+`, cyclically permuted
>    by `C_3`.
> 3. The quotient `K_norm^+ / C_3` is an open interval.

**Proof sketch.**

Item 1 is immediate from the explicit parameterization above. For item 2,
positivity is an open condition on the circle coordinates, so `K_norm^+` is an
open subset of `S^1_+`; direct evaluation of the three coordinate functions
shows that it consists of three `C_3`-related arcs. Because the `C_3` action is
free and transitively permutes those arcs, the quotient is a single open arc,
homeomorphic to an interval. The runner verifies all of this numerically and
symbolically on the retained basis. `square`

**Consequence.** The actual positive projectivized Koide cone is not a
2-sphere, and not even a circle after quotienting by the physical `C_3`
symmetry. It is an interval.

---

## 3. Bundle obstruction theorem

> **Theorem 2 (equivariant bundle triviality on the physical Koide base).**
> Every complex `C_3`-equivariant line bundle on `K_norm^+` is equivariantly
> trivial. In particular:
>
> - the only possible first Chern class on the physical base is `c_1 = 0`;
> - there is no monopole bundle with flux `n != 0` on `K_norm^+`;
> - there is no topological route from the actual projectivized Koide cone to
>   `c_1 = 2`.

**Proof.** The `C_3` action on `K_norm^+` is free, so equivariant complex line
bundles on `K_norm^+` are equivalent to complex line bundles on the quotient
`K_norm^+ / C_3`. By Theorem 1 that quotient is an interval, hence
contractible. Complex line bundles over a contractible base are trivial. `square`

---

## 4. Berry holonomy obstruction

> **Corollary 3 (no gauge-invariant Berry phase on the actual positive base).**
> Let `L` be any complex `C_3`-equivariant line bundle over `K_norm^+` and let
> `A` be any equivariant unitary connection on `L`. Then, after descending to
> the quotient interval `K_norm^+ / C_3`, the connection is gauge-equivalent to
> `A = 0`. Therefore the physical positive projectivized Koide cone carries no
> gauge-invariant Berry holonomy.

**Reason.** After Theorem 2, descend to the trivial bundle over an interval.
Every `U(1)` connection on an interval has the form `A = i a(t) dt`; since the
base is simply connected with no closed loop, `A` is pure gauge and has no
gauge-invariant loop phase. `square`

So the phase `2/9` cannot be forced by topology, Chern class, or quotient-loop
holonomy on the actual positive projectivized Koide cone.

---

## 5. Sign-relaxed variant

The strongest obstruction above uses the physical positive base. If one instead
relaxes positivity and projectivizes the full real Koide cone by all nonzero
real scales, the base is a circle `S^1`. Even there:

- `H^2(S^1; Z) = 0`, so every complex line bundle is still topologically
  trivial;
- there is still no nonzero Chern class;
- the only remaining connection datum is a flat holonomy parameter on `S^1`.

So the sign-relaxed route is not topologically quantized either. A constant flat
connection on the quotient circle can realize `delta = 2/9`, but nearby flat
connections realize nearby phases as well. This is non-uniqueness, not forcing.

### 5.1 What the missing datum really is

On this sign-relaxed auxiliary circle, retained route data determine only a
holonomy family

```text
Hol_t = exp(i 2 pi t),
delta(t) = t / 3,
```

with `t in R / Z` on the quotient circle. The old monopole integer `n` is not
the missing datum on the actual projectivized Koide base because there is no
nontrivial `c_1` there to carry it. If one wants `delta = 2/9`, one may choose
`t = 2/3`, but that is a geometric postulate on an auxiliary circle, not a
topological theorem on the physical Koide projectivization.

---

## 6. Formal consequence for the Berry lane

The retained Berry route now has a sharp honest status:

1. On the actual positive projectivized Koide cone, the bundle choice is unique
   and trivial; no `c_1 != 0` packaging is available.
2. On the sign-relaxed projective conic, the bundle is still trivial and the
   phase is an arbitrary flat-holonomy choice.
3. Therefore any successful Berry-type derivation of the charged-lepton phase
   must add one of the following:
   - a genuinely enlarged 2D base, together with a derivation that the physical
     phase is read there;
   - or an extra endpoint-identification / connection law not present in the
     retained route data.

This is a real theorem, not a placeholder critique: it proves that the old
`S^2_Koide` / monopole-`c_1 = 2` packaging cannot be the theorem on the actual
projectivized Koide base.

---

## 7. Runner summary

`scripts/frontier_koide_berry_bundle_obstruction_theorem.py` verifies:

- the corrected normalized Koide geometry (`sigma = 1/2`, not `2/3`);
- explicit circle parameterization of the normalized locus;
- exact `C_3` action as a `2 pi / 3` rotation on the doublet plane;
- physical positivity locus = three open arcs;
- quotient topology: interval on the physical positive base, circle on the
  sign-relaxed projective conic;
- vanishing `beta_2` on both relevant bases;
- continuous non-uniqueness of flat holonomy on the sign-relaxed quotient.

Verified result: `PASS=30 FAIL=0`.

---

## 8. Cross-references

- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`
- `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
- `docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md`

---

## 9. Honest statement

This note does not derive the charged-lepton phase. It proves something
different and sharper: on the actual positive projectivized Koide cone there is
no nontrivial topological bundle available from which such a phase could be
forced by Chern arithmetic. That turns the old Berry route from "candidate
forcing theorem with one missing bundle choice" into a precise obstruction and
uniqueness theorem for the remaining bundle choice itself.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
