# Koide A1 Probe 12 — Plancherel / Peter-Weyl Bimodule Weighting Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 12 of the Koide
A1-condition closure campaign. Tests the Plancherel / Peter-Weyl
bimodule weighting mechanism identified by both Survey 3 (NCG /
algebraic) and Survey 4 (info-theoretic / RMT) as the most-converged
candidate route to derive the canonical `(1,1)`-multiplicity-weighted
Frobenius pairing on `M_3(ℂ)_Herm` under `C_3`-isotype decomposition.
**Status:** source-note proposal for a **sharpened** bounded
obstruction. The two named sub-derivations
(a) `C_3` acts on `M_3(ℂ)` by `*`-automorphisms via `Z³ → C_3` quotient
(b) the relevant bimodule is a Hilbert C*-module over the `C_3`-fixed
subalgebra
both **CLOSE** from retained content. The closure step from canonical
bimodule structure to the `(1,1)`-multiplicity weighting **FAILS** at
the same convention-trap that blocked Probe 1 (RP/GNS reduction-map
ambiguity), Route D (weight-class `(1,1)` vs `(1,2)` ambiguity), and
Probe 7 (linear-`Z_2` cannot single out a quadratic surface). The A1
admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-plancherel-peter-weyl-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_plancherel_peter_weyl_2026_05_09_probe12.py`](../scripts/cl3_koide_a1_probe_plancherel_peter_weyl_2026_05_09_probe12.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_plancherel_peter_weyl_2026_05_09_probe12.txt`](../logs/runner-cache/cl3_koide_a1_probe_plancherel_peter_weyl_2026_05_09_probe12.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"A1-condition"** = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian circulant
  `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`.

These are distinct objects despite the shared label. This probe
concerns the A1-condition only; framework axiom A1 is retained and
untouched.

## Question

The eleven-probe campaign synthesis
([`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md))
named the precisely-localized missing primitive:

> The canonical `(1,1)`-multiplicity-weighted Frobenius pairing on
> `M_3(ℂ)_Herm` under `C_3`-isotype decomposition.

External Surveys 3 (NCG / algebraic) and Survey 4 (info-theoretic /
RMT) independently identified the **Plancherel / Peter-Weyl bimodule
weighting mechanism** as the most-converged candidate to derive this
primitive from group-theoretic content.

The proposed mechanism: for a finite group `G` acting on a
finite-dimensional `*`-algebra `A` by `*`-automorphisms, the regular-
representation decomposition `A = ⊕_π V_π ⊗ V_π*` gives a canonical
`G`-invariant Haar pairing. Restricted to `M_3(ℂ)_Herm` under
`C_3`-conjugation, isotype-dimension weighting (`3` trivial : `6`
non-trivial real isotype) follows from dimension counting alone.
Watatani-index reformulation: `index = dim(M_3) / dim(fixed) = 9/3 = 3`,
sharp uniqueness theorem.

This converts the `(1,1)`-multiplicity-weighted Frobenius from a
*choice* into a *theorem* — IF two sub-derivations close from retained
content:

- **(a)** `C_3` acts on `M_3(ℂ)` by `*`-automorphisms via `Z³ → C_3`
  quotient
- **(b)** the relevant bimodule is a Hilbert C*-module over the
  `C_3`-fixed subalgebra (the circulants `aI + bC + b̄C²`)

**Question:** Do (a) and (b) close from retained content, and if so
does the Plancherel/Peter-Weyl mechanism then force the
`(1,1)`-multiplicity weighting (and hence A1 `|b|²/a² = 1/2`)?

## Answer

**Mixed.** Sub-derivations (a) and (b) **CLOSE from retained content**.
The closure step from canonical bimodule structure to the `(1,1)`
weighting **FAILS** because:

> Plancherel measure on `Ĉ_3` is **uniform** (`μ(χ) = 1/3` for each
> of the three characters `{1, ω, ω̄}`), not `(1,1)` on **real**
> isotypes. To extract a scalar from the `A^{C_3}`-valued pairing
> `E(X^*Y) ∈ A^{C_3} ≅ ℂ³` one must choose a state on `A^{C_3}`; the
> canonical (Plancherel-uniform) state gives the **`(1,2)` weighting**
> (`κ = 1`, NOT A1), not the `(1,1)` weighting (`κ = 2` = A1).
>
> The `(1,1)` weighting on real isotypes would require a NON-uniform
> state on `A^{C_3}` that combines `ω` and `ω̄` characters into a
> single doublet slot — i.e., applying Frobenius reciprocity over
> `ℝ` (which counts real isotypes, gives `(1,1)`) instead of over
> `ℂ` (which counts complex characters, gives `(1,2)`).
>
> Plancherel/Peter-Weyl operates over `ℂ`. It does NOT canonically
> distinguish `ω` from `ω̄`, so it does NOT canonically pick `(1,1)`.

**Verdict: SHARPENED bounded obstruction (bounded_theorem with
named admission).** The convention-trap surfaces at the same locus as
Probe 1 (vacuum-state freedom on the reduction map), Route D
(`(1,1)` vs `(1,2)` weight-class ambiguity), and the retained
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM`'s remaining
log-functional residue. The A1 admission count is UNCHANGED; this
probe sharpens the residue rather than closing it.

The convention-trap localizes precisely:

```
The retained-content principle that selects R-isotype counting
(gives (1,1) → κ = 2 = A1) over C-character counting (gives (1,2)
→ κ = 1 ≠ A1) is NOT supplied by Plancherel / Peter-Weyl alone.
```

This is a **sharper** restatement of Probe 1 §B4's reduction-map
ambiguity: the reduction map IS the choice of state on the fixed
subalgebra, and Plancherel does not pick a non-uniform state.

## Setup

### Premises (A_min for probe 12)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | retained per [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | retained per [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | retained per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Probe1 | RP/GNS does not force `(1,1)` Frobenius from retained content | retained per [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md) |
| Probe7 | The `1/2` in A1 is the `C_3`-multiplicity ratio `3:6` on `M_3(ℂ)_Herm` | retained per Probe 7 §8 (PR #740) |
| Campaign | Eleven-probe campaign synthesis identifies the missing primitive | retained per [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms — this probe's purpose is to derive the missing
  primitive from retained content, not admit it

## The Plancherel / Peter-Weyl mechanism

For a finite group `G` and a finite-dimensional `*`-algebra `A` on
which `G` acts by `*`-automorphisms, the **canonical structure** is:

1. **Regular representation decomposition**: `A = ⊕_π V_π ⊗ V_π*` as
   a `G × G`-bimodule, with `V_π` the irreducible representations.
2. **Plancherel measure** on the dual `Ĝ`: `μ(π) = (dim π)² / |G|`.
3. **Watatani index** for the inclusion `A^G ⊂ A`:
   `[A : A^G] = dim(A) / dim(A^G)` (for `|G| < ∞`).
4. **Conditional expectation** `E: A → A^G` defined by
   `E(X) = (1/|G|) Σ_g g · X`.
5. **Hilbert C*-module structure**: `A` is a right-Hilbert-C*-module
   over `A^G` via the inner product `⟨X, Y⟩_E = E(X^* Y) ∈ A^G`.

For `G = C_3` acting on `A = M_3(ℂ)` by conjugation `g · X = U_g X U_g^*`:

- All irreps of `C_3` are 1-dim; Plancherel measure is **uniform**:
  `μ(1) = μ(ω) = μ(ω̄) = 1/3`.
- `A^G` = circulants `{aI + bC + b̄C² : a ∈ ℝ, b ∈ ℂ}`.
- Watatani index: `[A : A^G] = 9/3 = 3`.
- Conditional expectation: `E(X) = (1/3)(X + CXC^* + C²XC^{*2})`.

The proposal is that this canonical structure forces the `(1,1)`
multiplicity-weighted Frobenius pairing.

## Sub-derivation (a): `C_3` acts on `M_3(ℂ)` by `*`-automorphisms

**Status: CLOSES from retained content.**

### Statement

There is a canonical action of `C_3` on `M_3(ℂ)` by `*`-automorphisms,
extending uniquely (up to inner automorphism) the retained `C_3[111]`
action on hw=1.

### Proof

Per BZ-corner forcing (BZ retained), `C_3[111]` acts on hw=1 ≅ ℂ³ by
the cyclic shift `U_C = C` (the standard 3×3 cyclic permutation
matrix). This action lifts to `M_3(ℂ)` by **conjugation**:

```
α_g : M_3(ℂ) → M_3(ℂ),   α_g(X) := U_g X U_g^*,   U_g := C^g.
```

This is automatically a `*`-automorphism:
- **Multiplication-preserving**: `α_g(XY) = U_g XY U_g^* = (U_g X U_g^*)(U_g Y U_g^*) = α_g(X) α_g(Y)`. (Verified by runner T2.2.)
- **`*`-preserving**: `α_g(X^*) = U_g X^* U_g^* = (U_g X U_g^*)^* = α_g(X)^*`. (Verified by runner T2.1.)
- **Identity-preserving**: `α_g(I) = U_g U_g^* = I`. (Verified by runner T2.3.)
- **Fixed-point algebra is the circulants**: `α_g(X) = X` for all `g` iff `[U_C, X] = 0` iff `X` is circulant. (Verified by runner T2.4a/b.)

**Uniqueness (Wigner-style argument).** Any `*`-automorphism of
`M_3(ℂ)` is **inner** (this is a standard theorem: every automorphism
of a finite simple matrix algebra is conjugation by a unitary, unique
up to overall phase). The retained `C_3[111]` on hw=1 specifies the
unitary `U_C` up to overall phase. The resulting conjugation action
is the unique lift to `M_3(ℂ)`.

**Conclusion.** The C_3-action by `*`-automorphisms is **canonical**
and follows from retained content (BZ + 3GenObs + standard
`*`-automorphism uniqueness). No new axiom is needed. ∎

## Sub-derivation (b): Hilbert C*-module structure over `A^{C_3}`

**Status: CLOSES from retained content.**

### Statement

`M_3(ℂ)` carries a canonical Hilbert C*-module structure over the
`C_3`-fixed subalgebra `A^{C_3}` (the circulants), with `A^{C_3}`-valued
inner product `⟨X, Y⟩_E = E(X^* Y)`.

### Proof

Define the conditional expectation
```
E(X) := (1/3)(X + α_1(X) + α_2(X)) = (1/3)(X + CXC^* + C²XC^{*2}).
```

The runner verifies (Section 3):
- **E is linear** (T3.1).
- **E is idempotent** (E² = E, T3.2).
- **E maps onto circulants** (T3.3, T3.4).
- **E is C_3-equivariant**: `E(α_g(X)) = E(X)` (T3.5).
- **E is positive** (`E(X^*X)` is PSD, T3.6).
- **E is faithful**: `E(X^*X) ≠ 0` for `X ≠ 0` (T3.7 witness).
- **E is a conditional expectation**: `E(aXb) = a E(X) b` for
  `a, b ∈ A^{C_3}`. (Standard property of Haar averaging.)

These are the defining properties of a faithful unital C*-conditional
expectation. The `A^{C_3}`-valued pairing
```
⟨X, Y⟩_E := E(X^* Y) ∈ A^{C_3}
```
satisfies:
- `⟨X, Y⟩_E^* = ⟨Y, X⟩_E`,
- `⟨X, X⟩_E ≥ 0`, with equality iff `X = 0` (faithfulness),
- `⟨X, Yb⟩_E = ⟨X, Y⟩_E b` for `b ∈ A^{C_3}` (right `A^{C_3}`-linearity),

making `M_3(ℂ)` a right Hilbert C*-module over `A^{C_3}` (T3.8).

**Conclusion.** The Hilbert C*-module structure is **canonical** and
follows from retained content (the `*`-automorphism action from (a)
plus standard Haar-averaging conditional expectation theory). No new
axiom is needed. ∎

## The closure step: Plancherel weighting → `(1,1)` ?

**Status: FAILS at the convention-trap.**

### What needs to happen

To force the `(1,1)`-multiplicity weighting, we need to extract a
**scalar** trace from the `A^{C_3}`-valued pairing `⟨X, Y⟩_E`. This
requires a **state** on `A^{C_3}`:
```
ω : A^{C_3} → ℂ,   ω(1) = 1,   ω(c^*c) ≥ 0.
```

Composition gives a scalar trace `(X, Y) := ω(⟨X, Y⟩_E) = ω(E(X^*Y))`.

The question is: does Plancherel/Peter-Weyl pin a canonical state `ω`
on `A^{C_3}`?

### What Plancherel/Peter-Weyl gives

`A^{C_3}` is the algebra of circulants on `ℂ³`. Via Fourier transform
on `C_3`, `A^{C_3} ≅ ℂ³` (commutative algebra of three characters
`{1, ω, ω̄}`).

The **canonical Plancherel measure** on `Ĉ_3` is `μ(χ) = 1/3` for each
of the three characters (since all irreps are 1-dim and `|C_3| = 3`):

```
μ(1) = μ(ω) = μ(ω̄) = 1/3.
```

This **uniform** measure defines the canonical Plancherel state on
`A^{C_3}`. Applying it to the pairing gives:
```
ω_{Plancherel}(E(X^*X)) = (1/3) Σ_χ E_χ(X^*X)
```
where `E_χ` is the projection onto the χ-character isotype.

### What this gives for circulant H = aI + bC + b̄C²

The eigenvalues of `H` on the three characters are:
```
λ_1 = a + 2 Re(b)
λ_ω = a + 2 Re(b ω)
λ_ω̄ = a + 2 Re(b ω̄)
```

The eigenvalues of `H^*H` are `|λ_χ|²`. Applied to the Plancherel
state:

```
ω_{Plancherel}(H^*H) = (1/3)(|λ_1|² + |λ_ω|² + |λ_ω̄|²)
                    = (1/3) Tr(H^*H)
                    = (1/3)(3a² + 6|b|²)
                    = a² + 2|b|²
```

This is the **`(1,2)` weighting** — `κ = 1`, **NOT** A1.

(Verified by runner T7.1: at H = 1.7·I + 0.6·C + 0.6·C², Plancherel-uniform scalar trace = `1.7² + 2·0.6² = 3.61` ✓.)

### Why this fails to give `(1,1)`

The `(1,1)` weighting requires combining `ω` and `ω̄` characters into
a **single real isotype** (the doublet), then weighting that doublet
*equally* with the trivial isotype. This is **Frobenius reciprocity
over `ℝ`** (which counts real isotypes: 1 trivial + 1 doublet = `(1,1)`).

Plancherel measure operates over `ℂ` and treats each of the three
characters as a separate slot, giving `(1, 1, 1)` over the three
characters, which on the real form becomes `(1, 2)` over real isotypes
(since the doublet absorbs both `ω` and `ω̄`).

**The convention-trap:**
```
ℂ-character counting (Plancherel)        →  (1, 1, 1) ↦ (1, 2)  →  κ = 1
ℝ-isotype counting (block-total Frobenius) →  (1, 1)              →  κ = 2 = A1
```

(Verified by runner T7.1, T8.4, T8.5, T9.1, T9.2.)

### Counterexample: alternative states give different answers

The runner constructs alternative positive normalized states on
`A^{C_3}`:
- Plancherel-uniform `(1/3, 1/3, 1/3)` → gives `a² + 2|b|²` = (1,2)
- Real-isotype `(1/2, 1/4, 1/4)` → gives a different combination
- "Anti-real" `(1/4, 3/8, 3/8)` → gives yet another combination

Each is a valid state on `A^{C_3}` (positive, normalized). None is
*algebraically* preferred. Plancherel-uniform is the **canonical**
choice from group theory; it gives `(1,2)`, not `(1,1)`. (Verified
T9.1, T9.2.)

## Theorem (Probe 12 sharpened bounded obstruction)

**Theorem.** On A1+A2 + retained C_3-action on hw=1 + retained
M_3(ℂ) on hw=1 + retained Frobenius block-total + standard Hilbert
C*-module / Plancherel theory:

```
(a) C_3 acts on M_3(ℂ) by *-automorphisms via the Z³ → C_3 quotient.
    [Closes from retained content; runner Section 2.]
(b) M_3(ℂ) carries a canonical Hilbert C*-module structure over the
    C_3-fixed subalgebra A^{C_3} = circulants, via the conditional
    expectation E(X) = (1/3)(X + CXC^* + C²XC^{*2}).
    [Closes from retained content; runner Section 3.]
(c) The canonical Plancherel state on A^{C_3} is uniform on Ĉ_3:
    μ(1) = μ(ω) = μ(ω̄) = 1/3, and gives the (1,2) weighting on
    M_3(ℂ)_Herm under the real isotype decomposition.
    [Closes; runner Sections 5-7.]
(d) The (1,1) weighting (which would force κ = 2 = A1) requires a
    NON-Plancherel state on A^{C_3} that combines ω and ω̄ characters
    into a single real-isotype slot. This non-uniform state is NOT
    forced by Plancherel/Peter-Weyl alone.
    [Failure mode; runner Sections 8-9.]

Therefore: the Plancherel/Peter-Weyl mechanism does NOT force the
canonical (1,1)-multiplicity-weighted Frobenius pairing. The
A1-condition closure attempt via this route returns SHARPENED
bounded obstruction. The remaining residue is named precisely:

  "the retained-content principle that selects R-isotype counting
   (gives (1,1) → κ = 2 = A1) over C-character counting (gives (1,2)
   → κ = 1)."

The A1 admission count is unchanged.
```

**Proof.** Sub-derivations (a) and (b) are explicit constructions
verified algebraically by the runner. The closure step (c-d) computes
the canonical Plancherel state explicitly and shows that it gives
`(1,2)` not `(1,1)`. ∎

## Convention-robustness check

Survey 3's exact warning was:
> "Every candidate admits an overall scalar normalization. The `1/2`
> ratio is convention-free *only because* the `(1,1)` ratio cancels
> overall normalization — any framework that gives independent
> normalizations to trivial vs non-trivial isotypes will fail."

The runner verifies (Section 10):

- **Scale-invariance of the ratio** `E_+ / E_⊥` is preserved under
  `H → cH` rescalings (T10.1). ✓
- **But** the choice between `(1,1)` and `(1,2)` weighting is also
  scale-invariant. So scale-invariance does not pin the choice (T10.2).
- **Basis change** `C → C^{-1}` preserves the C_3-action (T10.3). ✓

The bimodule frame is **canonically pinned** in the sense that the
inner product `⟨X, Y⟩_E = E(X^*Y)` is fixed by retained content
(via sub-derivations (a) and (b)). What is **not pinned** is the
**state** on the fixed subalgebra used to extract a scalar. This is
the surviving convention-trap.

## Attack-vector enumeration

Per the eleven-probe campaign synthesis, this probe is the twelfth
attack vector. It localizes to:

| # | Attack vector | Outcome |
|---|---|---|
| 12 | Plancherel / Peter-Weyl bimodule weighting | sharpened obstruction; sub-derivations (a),(b) close, closure step fails at the C-vs-R counting trap |

This refines the pre-existing residue surfaced by:
- **Probe 1 §B4** (reduction-map ambiguity): the reduction map IS the
  state choice on `A^{C_3}`. Probe 12 sharpens this to "Plancherel-
  canonical state gives `(1,2)`, not `(1,1)`."
- **Route D** (`(1,1)` vs `(1,2)` weight-class ambiguity): Probe 12
  identifies this as the C-character vs R-isotype counting choice,
  not just an arbitrary weight-class freedom.
- **Probe 7 §8** (`3:6` multiplicity ratio): Probe 12 shows that the
  `3:6` ratio is **literally** present in dimension counting, but
  Plancherel-uniform on Ĉ_3 still does not lift it to `(1,1)`.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction)
- `effective_status`: `retained_bounded` (after audit review)
- `admitted_context_inputs`: `["A1-condition: |b|²/a² = 1/2"]` —
  the residual admission, named precisely as "the retained-content
  principle that selects R-isotype counting over C-character
  counting on `M_3(ℂ)_Herm` under `C_3`-isotype decomposition"

### What this probe DOES

1. Closes sub-derivation (a): `C_3` acts on `M_3(ℂ)` by
   `*`-automorphisms canonically.
2. Closes sub-derivation (b): Hilbert C*-module structure over
   `A^{C_3}` is canonical.
3. Sharpens the residue: the `(1,1)` weighting is NOT supplied by
   Plancherel-canonical state on `A^{C_3}`. The trap is precisely
   the C-character vs R-isotype counting choice.

### What this probe DOES NOT do

1. Does NOT close the A1-condition.
2. Does NOT add a new axiom.
3. Does NOT modify any retained theorem (BZ, 3GenObs, Circulant,
   BlockTotalFrob, MRU, KoideAlg, Probe1, Probe7, Campaign).
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis (admit/derive/pivot).
7. Does NOT promote Survey 3 or Survey 4 to retained authority.
   Both remain external scoping context.

## Honest assessment

The Plancherel/Peter-Weyl approach was the most-converged candidate
mechanism identified by independent surveys. Its critical failure
mode was correctly anticipated by Survey 3's convention-trap warning:
"any framework that gives independent normalizations to trivial vs
non-trivial isotypes will fail."

What this probe contributes to the campaign is:

1. **Two new positive theorems**: sub-derivations (a) and (b) close
   from retained content. These are constructive and could
   potentially be packaged separately as positive support theorems
   in a future audit pass.

2. **Sharper residue characterization**: the convention-trap is
   precisely the **C-character vs R-isotype counting choice**, not
   a generic normalization ambiguity. This is a **smaller** named
   primitive than "canonical Frobenius pairing."

3. **Confirmation of the campaign's terminal state**: a twelfth
   independent attack returns the same structural obstruction,
   strengthening the campaign synthesis's conclusion that the
   missing primitive cannot be derived from generic group-theoretic
   content alone.

The residue is now: **a single named principle for selecting `R`-
isotype counting over `ℂ`-character counting on `M_3(ℂ)_Herm`**.
This is more precisely localized than the prior "canonical (1,1)
Frobenius pairing" phrasing, and could plausibly be the target of a
future Probe 13 if such a principle is identifiable from a yet-to-
be-tried mechanism (e.g., real-structure / antilinear involutions on
`M_3(ℂ)`, or a real-form Schur-orthogonality argument).

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Physical-lattice baseline interpretation: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Preserved-`C_3` interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Eleven-probe campaign

- Synthesis (terminal state): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Route D (Newton-Girard): [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)
- Probe 7 (Z_2×C_3 pairing; PR #740, off-main): see Campaign synthesis cross-ref

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_plancherel_peter_weyl_2026_05_09_probe12.py
```

Expected: `=== TOTAL: PASS=52, FAIL=0 ===`

The runner verifies:

1. Retained inputs (Section 1): C is unitary, order 3, eigenvalues
   `{1, ω, ω̄}`; H = aI + bC + b̄C² is Hermitian and circulant; (a,b)
   round-trip works.
2. Sub-derivation (a) (Section 2): conjugation action is
   `*`-preserving, multiplication-preserving, identity-preserving;
   fixed-point algebra is the circulants.
3. Sub-derivation (b) (Section 3): conditional expectation E is
   linear, idempotent, projects onto circulants, C_3-equivariant,
   positive, faithful; A^{C_3}-valued pairing.
4. Frobenius pairing baseline (Section 4): `||π_+(H)||² = 3a²`,
   `||π_⊥(H)||² = 6|b|²`, equipartition at A1.
5. Plancherel measure on Ĉ_3 (Section 5): uniform, `1/3` per
   character.
6. Character vs real-isotype dimensions (Section 6): `3+3+3` over
   ℂ, `3+6` over ℝ.
7. Plancherel-uniform scalar trace gives `(1,2)` weighting
   (Section 7): `a² + 2|b|²`, with NO selection of `(1,1)`.
8. Convention-trap (Section 8): block-total log (1,1) maximized at
   A1 vs det-carrier log (1,2) maximized at κ=1; both are valid
   choices.
9. Counterexample (Section 9): alternative non-Plancherel states
   give different scalar traces; (1,1) requires non-uniform state
   that is NOT Plancherel-canonical.
10. Convention robustness (Section 10): scale-invariance is shared
    by both weightings, so does not pin the choice; basis change
    `C → C^{-1}` preserves isotype structure.
11. Verdict (Section 11): sub-derivations (a),(b) close; closure
    step fails at convention-trap; sharpened bounded obstruction.
