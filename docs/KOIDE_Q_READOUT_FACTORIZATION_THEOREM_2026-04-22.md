# Koide Q Readout Factorization Theorem

**Date:** 2026-04-22
**Claim type:** bounded_theorem
**Status:** exact support theorem on the admitted first-live second-order
readout grammar; not a closure theorem
**Purpose:** replace the weakest remaining phrase in the second-order `Q` route

> the selector should live on the second-order returned operator

with the strongest exact quotient statement currently available on the retained
`Γ_1 / T_1` grammar.

**Primary runner:** `scripts/frontier_koide_q_readout_factorization_theorem.py`

---

## Audit scope

This note has been narrowed in response to an auditor verdict
(`audit_status=audited_conditional`, `claim_type=positive_theorem`,
`scope_too_broad`).

**Auditor's repair target (verbatim):**

> scope_too_broad: split out the exact rank/kernel quotient as the clean
> bounded theorem, or add a theorem and runner check proving that local
> bosonic first-live species-resolving C3-covariant admissibility forces
> constancy on span(e_z).

**Resolution chosen:** split. The bounded theorem retained in this note is the
exact rank/kernel quotient of the linear map `L : R^4 -> Diag_3(R)` defined
below (Sections 1-2). The broader claim that the full admissibility class
(local, bosonic in `Γ_1`, first-live on `T_1`, species-resolving,
`C_3`-covariant) forces every admissible selector to be constant on
`span(e_z)` is **not** carried as a theorem in this note. It is preserved
below as an explicitly-labeled `## Conditional extension`, contingent on a
future theorem-and-runner check of that admissibility-implies-constancy step.

No prior math has been removed; only the scope-of-claim labeling has changed.

---

## 1. Exact map

On the retained charged-lepton readout grammar, define the second-order map

```text
L(W) = P_{T_1} Γ_1 W Γ_1 P_{T_1}
```

on the four reachable/intermediate-state weight slots

```text
W = u P_{O_0} + v P_{(1,1,0)} + w P_{(1,0,1)} + z P_{(0,1,1)}.
```

The exact single-slot images are

```text
P_{T_1} Γ_1 P_{O_0} Γ_1 P_{T_1}     = diag(1,0,0)
P_{T_1} Γ_1 P_{(1,1,0)} Γ_1 P_{T_1} = diag(0,1,0)
P_{T_1} Γ_1 P_{(1,0,1)} Γ_1 P_{T_1} = diag(0,0,1)
P_{T_1} Γ_1 P_{(0,1,1)} Γ_1 P_{T_1} = 0.
```

So the readout map is exactly

```text
L(u,v,w,z) = diag(u,v,w).
```

---

## 2. Quotient theorem (bounded)

The map `L : R^4 -> Diag_3(R)` has:

- rank `3`,
- kernel `span{(0,0,0,1)}`,
- image equal to the full diagonal species space.

Therefore

```text
R^4 / span(e_unreach)  ≅  Diag_3(R),
```

and two weight packages have the same first-live returned operator if and only
if they differ only in the unreachable slot `z`.

This is the clean bounded theorem of the note: the exact rank/kernel quotient
of the linear readout map `L` on the retained `Γ_1 / T_1` grammar. It is a
purely linear-algebraic statement about `L`, independent of any selector
admissibility hypothesis.

---

## 3. Conditional extension

> **Status:** conditional. The statement of this section is **not** carried as
> a theorem of this note. It is the broader claim flagged by the auditor as
> requiring its own theorem-and-runner check, namely that local bosonic
> first-live species-resolving `C_3`-covariant admissibility forces constancy
> on `span(e_z)`. Until that step is proved separately, the content below is
> recorded only as a conditional extension of the bounded theorem above.
> The companion runner mirrors this scope split: sections A-C verify the
> bounded theorem, and section D explicitly records that the
> admissibility-implies-kernel-invariance step is **not** verified by the
> runner.

Within the retained scope:

- local,
- bosonic/even in `Γ_1`,
- first-live on `T_1`,
- species-resolving,
- `C_3`-covariant,

the conditional reading is that every admissible selector depends on the
weight package only through the returned operator

```text
R_{Γ_1}(W) = diag(u,v,w).
```

Conditional on that admissibility-implies-constancy step, the exact species
Fourier transport then sends that returned operator to the Koide carrier
`H_cyc`, and the cyclic quadratic scalar sector reduces to the same two-slot
carrier `(E_+, E_perp)`.

So, conditionally, this note would upgrade the old identification language
inside the admitted first-live second-order class:

```text
admitted first-live selector = scalar on the exact second-order returned
operator
```

from a plausible carrier choice to an exact statement on the first-live
readout grammar. Without the separate admissibility-implies-constancy
theorem-and-runner check, this section remains an extension target rather
than a proved consequence of the bounded theorem in Section 2.

---

## 4. Honest scope

### What this note claims (bounded theorem)

1. on the first-live second-order readout grammar, the linear readout map
   `L : R^4 -> Diag_3(R)` has rank `3`, kernel `span{e_z}`, and image equal
   to the full diagonal species space;
2. equivalently, the unreachable slot `z` is the entire kernel of `L`, and
   `R^4 / span(e_z) ≅ Diag_3(R)`.

### What this note does not claim

1. it does not claim that local bosonic first-live species-resolving
   `C_3`-covariant admissibility, by itself, forces every admissible selector
   to be constant on `span(e_z)`; that step is recorded only as a conditional
   extension (Section 3) and would require its own theorem-and-runner check;
2. it does not claim a universal statement about all possible higher-order or
   nonlocal carriers;
3. it does not touch the separate `delta` bridge;
4. it does not rewrite authority surfaces;
5. it does not by itself prove that the physical charged-lepton selector must
   belong to this admitted class.

---

## 5. Bottom line

The strongest clean **bounded** statement for review is:

> on the retained `Γ_1 / T_1` grammar, the exact second-order readout map
> `L : R^4 -> Diag_3(R)` has rank `3` and kernel `span{e_z}`, so
> `R^4 / span(e_z) ≅ Diag_3(R)`.

That is a purely linear-algebraic rank/kernel quotient. The further reading
that every admissible first-live selector factors uniquely through the
returned operator is held as a conditional extension (Section 3), pending a
separate theorem-and-runner check that admissibility forces constancy on
`span(e_z)`. The remaining open issue beyond either statement is still the
physical identification of the second-order `Q` route.
