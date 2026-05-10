# Primitive P-BAE — M1 Trace State Degeneracy Correction Note

**Date:** 2026-05-10
**Status:** source-only correction stanza for candidate primitive M1.
**Target note:** [`PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md`](PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md)
(file lives on open PR #1039 branch `primitive/p-bae-multiplicity-counting-2026-05-10`).
**Catching PR:** [#1049](https://github.com/jonathonreilly/Physics/pull/1049) —
*primitive P-BAE — M1/M2 duality is BOUNDED (saddle-equivalent,
fluctuation-distinct)*.
**Authority role:** correction stanza (source-only). Does NOT modify
the targeted proposal note. Records the M1 content reclassification so
downstream audits cite the corrected definition.

---

## 0. Context

PR #1039 proposes three candidate derived primitives (M1, M2, M3)
that close the framework's Brannen Amplitude Equation (BAE)
algebraically. The proposed M1 statement uses a **linear trace
functional** on the C_3-isotype decomposition of `Herm_circ(3)`:

> **P-BAE-M1 (as stated in PR #1039 § "Candidate M1").**
> Define a derived trace functional `τ_M : Herm_circ(3) → ℝ` by
> `τ_M(X) := Tr(π_+(X)) + Tr(π_⊥(X))`, where `π_+ : Herm_circ(3) → ℝ⟨I⟩`
> is the trivial-isotype projector and `π_⊥ : Herm_circ(3) → ℝ⟨C+C²⟩ ⊕
> ℝ⟨i(C-C²)⟩` is the doublet projector.

PR #1049 (M1/M2 duality analysis) performed a literal-content audit
of this definition and found that **`τ_M` collapses to the ordinary
trace `Tr` on every Hermitian circulant matrix**. Therefore the
LINEAR-TRACE form of M1 is degenerate and cannot serve as the
BAE-closing primitive.

This correction stanza:

1. records the degeneracy proof,
2. names the actual non-linear functional that closes BAE,
3. classifies the M1-content correction as **STRUCTURAL** (the
   surrogate non-linear functional is canonically determined by the
   block-Frobenius structure that the linear trace was meant to
   encode),
4. stays inside the "source-only" review-loop discipline by adding a
   companion document rather than editing the open proposal note.

## 1. Degeneracy proof (cited from PR #1049 §2)

Let `H = aI + bC + b̄C²` with `a ∈ ℝ` and `b ∈ ℂ` be the canonical
Hermitian circulant parametrization on the 3 × 3 lattice. The C_3
isotype decomposition gives:

- Trivial component: `π_+(H) = aI`, so `Tr(π_+(H)) = 3a`.
- Doublet component: `π_⊥(H) = bC + b̄C²`, so
  `Tr(π_⊥(H)) = b · Tr(C) + b̄ · Tr(C²) = 0 + 0 = 0`
  because `C` and `C²` are **traceless** (eigenvalues are the three
  cube roots of unity, summing to 0).

Therefore:

```
τ_M(H) = Tr(π_+(H)) + Tr(π_⊥(H))
       = 3a + 0
       = 3a
       = Tr(H)              (since Tr(H) = 3a + b·Tr(C) + b̄·Tr(C²) = 3a).
```

The linear trace form `τ_M` is identical to the ordinary trace `Tr`
on `Herm_circ(3)`. It cannot distinguish the (1, 1) R-irreducible-block
weighting from the (1, 2) real-dimension weighting that M1's
extremization argument requires. As a linear trace state, M1 cannot
load-bear the BAE derivation.

## 2. Corrected M1 content (block-Frobenius log-functional)

The actual content that closes BAE under the (1, 1) weighting is a
**non-linear log-functional** on the isotype Frobenius block norms:

```
L_M1(H) := log ‖π_+(H)‖²_F + log ‖π_⊥(H)‖²_F
        = log E_+(H)       + log E_⊥(H)
        = log(3 a²)         + log(6 |b|²)
```

where `E_+(H) = ‖π_+(H)‖²_F = 3 a²` and `E_⊥(H) = ‖π_⊥(H)‖²_F = 6 |b|²`
are the Frobenius energies of the two isotype blocks. The (1, 1)
weighting is the **equal log-weight on the two block energies** — not
a linear trace assignment.

Extremization of `L_M1` under the normalization constraint
`E_+ + E_⊥ = N` reproduces the BAE saddle (PR #1039 §"Derivation of
BAE"):

```
d/dE_+ [log E_+ + log(N − E_+)] = 0
⇒ E_+ = E_⊥ = N/2
⇒ 3 a² = 6 |b|² ⇒ |b|²/a² = 1/2 = BAE.   ∎
```

This is the **isotype-block Frobenius log-functional** form of M1.
It is properly non-linear in `H`, and its (1, 1) weighting is on the
two log-summands, not on the trace coefficients.

## 3. Classification of the correction

Per the hostile-review tier brief (see PR #1049 §"Verdict") and the
saddle-vs-fluctuation distinction made for the M1/M2 duality:

| Item | Tier |
|------|------|
| Linear-trace M1 (PR #1039 literal definition) | **DEGENERATE** (collapses to `Tr`) |
| Block-Frobenius log-functional M1 (this note) | **STRUCTURAL** (canonical surrogate) |
| M1 / M2 saddle equivalence | **POSITIVE** (PR #1049 §6 Bridge theorem) |
| M1 / M2 Hessian / fluctuation distinction | **BOUNDED** (factor-2 Jacobian-class ambiguity) |

The reclassification is **content-level, not status-level**: the
candidate primitive is still STRUCTURAL for closing BAE at the saddle,
provided the non-linear log-functional form is adopted in place of
the linear trace form.

## 4. Where the correction must propagate

Downstream notes and audits that cite "P-BAE-M1" must reference the
**block-Frobenius log-functional** `L_M1`, not the linear trace `τ_M`,
when they need:

- the algebraic derivation of BAE from M1,
- distinction between (1, 1) and (1, 2) weightings on the C_3 isotype
  decomposition,
- the bridge to M2's measure-quotient form (PR #1049 establishes the
  Laplace duality `dμ_M1 = exp(L_M1) · δ(constraint) dH` ↔
  `dμ_M2 = exp(-S_M2) dν`).

Notes that cite M1 only at the saddle-equivalence level (i.e., for
the BAE value `|b|²/a² = 1/2`) require no further change — the saddle
is unchanged by this correction.

## 5. Source-only review-loop compliance

- Only a SOURCE NOTE is added; no synthesis / no output packet.
- The targeted proposal note (PR #1039) is NOT edited from this PR.
- The catching audit (PR #1049) is cited; this correction stanza
  records the M1 reclassification so it propagates independent of
  PR #1039's merge state.
- A paired runner [`scripts/cl3_t1_corrections_v2_2026_05_10.py`](../scripts/cl3_t1_corrections_v2_2026_05_10.py)
  verifies the degeneracy and the non-linear form numerically.
- Cached output: [`logs/runner-cache/cl3_t1_corrections_v2_2026_05_10.txt`](../logs/runner-cache/cl3_t1_corrections_v2_2026_05_10.txt).

## 6. Authority disclaimer

This is a source-only correction stanza. Audit verdict and downstream
status (retention, tier promotion) are set only by the independent
audit lane.
