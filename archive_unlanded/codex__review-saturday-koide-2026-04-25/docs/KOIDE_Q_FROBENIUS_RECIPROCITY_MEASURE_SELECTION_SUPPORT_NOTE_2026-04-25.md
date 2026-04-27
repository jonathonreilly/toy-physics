# Koide Q Frobenius-Reciprocity Measure-Selection Support Note

**Date:** 2026-04-25
**Lane:** charged-lepton Koide / dimensionless Q support
**Status:** exact support / criterion theorem only; not retained native Koide
closure
**Primary runner:**
`scripts/frontier_koide_q_frobenius_reciprocity_measure_selection_support.py`

---

## 1. Purpose

This note lands the useful science from the `saturday-koide` branch without
promoting charged-lepton Koide to retained closure.

The branch's valid contribution is the representation-theoretic sharpening of
the measure-selection side of the Koide `Q` support lane:

```text
Frobenius reciprocity counts isotype multiplicities.
Herm_circ(3) has one trivial real isotype and one non-trivial real doublet.
Therefore the Frobenius-reciprocity multiplicity measure is (1, 1).
```

That is the block-total Frobenius measure already identified by
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`.
If the physical charged-lepton extremal convention is this
Frobenius-reciprocity multiplicity measure, the internal AM-GM chain gives
`kappa = 2` and hence `Q = 2/3`.

The conditional is load-bearing. The current retained package still has not
derived that the physical charged-lepton observable must select this
source-free Frobenius block-total carrier rather than another retained support
carrier or source law.

---

## 2. Inputs on current main

| tag | retained/support input | authority |
|---|---|---|
| KAPPA | block-total Frobenius energies `E_+ = 3a^2`, `E_perp = 6|b|^2`; the `(1,1)` weights are identified as Frobenius-reciprocity multiplicity count | `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md` |
| FROB SPLIT | Frobenius trace inner product and Frobenius-orthogonal scalar/traceless split are canonical inside the admitted route | `KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md` |
| CRIT | on the admitted normalized reduced carrier, `K=0 <=> z=0 <=> Q=2/3`; this is a criterion, not retained native closure | `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md` |

The new contribution here is not a new numerical value. It is a clean audit of
which measure is selected by Frobenius reciprocity and what remains physical
rather than algebraic.

---

## 3. Frobenius-reciprocity measure statement

For `C_3`, the Hermitian circulant carrier decomposes as

```text
Herm_circ(3) = R I  +  { b C + bbar C^2 : b in C }.
```

The two summands are orthogonal real isotypes:

```text
trivial isotype:       R I                         multiplicity 1
real doublet isotype:  { b C + bbar C^2 : b in C } multiplicity 1
```

Schur orthogonality / Frobenius reciprocity counts irreducible multiplicities,
not real dimensions. Therefore the representation-ring measure on this
decomposition is

```text
(trivial, doublet) = (1, 1).
```

The determinant/rank log-law instead reads the doublet by its real dimension
or projector rank and therefore gives a `(1,2)` weighting. That is a different
measure. It is mathematically coherent, but it is not the Frobenius-reciprocity
multiplicity count.

This sharpens the available support claim:

```text
Frobenius reciprocity selects the block-total multiplicity measure (1,1).
It does not by itself prove that charged-lepton physics must use that measure
as the physical source law.
```

---

## 4. Conditional Koide consequence

For

```text
H = a I + b C + bbar C^2,
```

the block-total Frobenius energies are

```text
E_+    = ||a I||_F^2              = 3a^2
E_perp = ||b C + bbar C^2||_F^2   = 6|b|^2.
```

The equal-weight Frobenius-reciprocity log-law is

```text
S_FR = log E_+ + log E_perp.
```

At fixed `E_+ + E_perp = N`, the AM-GM extremum is

```text
E_+ = E_perp.
```

Therefore

```text
3a^2 = 6|b|^2
=> a^2 = 2|b|^2
=> kappa := a^2/|b|^2 = 2.
```

On the Brannen square-root carrier,

```text
c^2 = 4|b|^2/a^2 = 4/kappa,
Q = (c^2 + 2)/6.
```

At `kappa = 2`,

```text
c^2 = 2,
Q = 2/3.
```

By contrast, the determinant/rank weighting `(1,2)` gives

```text
kappa = 2 * (1/2) = 1,
Q = 1,
```

so the measure distinction is not cosmetic. The Frobenius-reciprocity choice is
exactly the choice that lands at the Koide value.

---

## 5. What this note closes

This note closes the following support-level statements:

1. Frobenius reciprocity selects `(1,1)` multiplicity weighting on the
   `Herm_circ(3)` trivial-plus-doublet split.
2. The determinant/rank log-law's `(1,2)` weighting is not that
   multiplicity measure.
3. Conditional on selecting the Frobenius-reciprocity block-total measure as
   the physical charged-lepton extremal convention, the admitted AM-GM chain
   gives `kappa = 2` and `Q = 2/3`.
4. The remaining Koide `Q` problem is not the internal Frobenius algebra. It is
   the physical source-domain/source-free carrier-selection theorem.

---

## 6. What this note does not close

This note does **not** prove:

1. retained charged-lepton Koide `Q = 2/3`;
2. that the physical charged-lepton observable must use the
   Frobenius-reciprocity block-total measure rather than another retained
   support carrier or source law;
3. that the normalized reduced carrier is the physical carrier;
4. that the physical reduced source is source-free (`K=0`);
5. the selected-line boundary-source / based-endpoint bridge behind
   `delta = 2/9`;
6. the Type-B rational-to-radian observable law for the Brannen phase;
7. the overall charged-lepton scale.

Those remain open package boundaries.

---

## 7. Closeout flags

```text
KOIDE_Q_FROBENIUS_RECIPROCITY_MEASURE_SELECTION_SUPPORT=TRUE
FROBENIUS_RECIPROCITY_SELECTS_BLOCK_TOTAL_1_1_MEASURE=TRUE
DET_LOG_LAW_IS_DIMENSIONAL_1_2_NOT_FR_MULTIPLICITY=TRUE
CONDITIONAL_Q_EQ_2_OVER_3_IF_FR_BLOCK_TOTAL_PHYSICAL=TRUE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE
RESIDUAL_Q=derive_physical_source_domain_and_source_free_reduced_carrier_selection
RESIDUAL_DELTA=derive_selected_line_boundary_source_based_endpoint_and_Type_B_radian_readout
```

