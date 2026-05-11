# Koide BAE Probe 22 — Spectrum-Level Cone Localization Pivot Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure;
no new admission)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 22 of the Koide
Brannen Amplitude Equipartition (BAE) closure campaign. Tests the
**spectrum-level cone localization pivot** as a route distinct from
the parameter-level routes already enumerated by Probes 1-21. The
pivot asks: instead of deriving `(a, b)` such that `|b|²/a² = 1/2`
(BAE), derive directly that the eigenvalues
`{λ_0, λ_1, λ_2}` of the matter-sector circulant
`H = aI + bC + b̄C²` on `hw=1` lie on the Koide cone
`λ_0² + λ_1² + λ_2² = 4(λ_0λ_1 + λ_0λ_2 + λ_1λ_2)`, and close
`Q = 2/3 = BAE` via the retained polynomial identity
`KOIDE_CONE_THREE_FORM_EQUIVALENCE`.
**Status:** source-note proposal for a sharpened bounded obstruction.
The retained Koide-Circulant Character Bridge identity (positive_theorem)
makes the spectrum-level cone localization arithmetically identical to
the parameter-level BAE on `Herm_circ(3)`. The pivot does not provide
a derivation route distinct from the parameter-level routes already
enumerated; it provides the SAME equation in DIFFERENT variables. The
BAE admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probe-spectrum-cone-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_spectrum_cone_2026_05_09_probe22.py`](../scripts/cl3_koide_bae_probe_spectrum_cone_2026_05_09_probe22.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_spectrum_cone_2026_05_09_probe22.txt`](../logs/runner-cache/cl3_koide_bae_probe_spectrum_cone_2026_05_09_probe22.txt)

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
- **"BAE"** = Brannen Amplitude Equipartition, the amplitude-ratio
  constraint `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian
  circulant `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`. Per the
  2026-05-09 BAE rename meta note, legacy aliases
  ("A1-condition", "A1 admission", "Brannen-Rivero A1") remain
  acceptable when cross-referencing landed PRs.

These are distinct objects despite the historical shared label.

## Question

Probes 1-21 attacked closure at the **parameter level** — derive
`(a, b)` values such that `|b|²/a² = 1/2`. All 18 named probes
returned bounded structural obstruction; the campaign synthesis
([`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md))
+ Probes 12-13 + Probe 18 sharpened the missing primitive to
"the canonical (1,1)-multiplicity-weighted Frobenius pairing on
`M_3(ℂ)_Herm` under `C_3`-isotype decomposition" / equivalently
"the U(1)_b angular quotient on the non-trivial doublet of
`A^{C_3}`."

**This probe asks:** can the obstruction be circumvented by pivoting
to a spectrum-level framing? Specifically, can one derive directly
that the eigenvalues `{λ_0, λ_1, λ_2}` of the matter-sector
circulant `H = aI + bC + b̄C²` lie on the Koide cone
`λ_0² + λ_1² + λ_2² = 4(λ_0λ_1 + λ_0λ_2 + λ_1λ_2)`, with the
retained polynomial identity
[`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
closing `Q = 2/3` from cone-localization?

## Answer

**No.** The spectrum-level pivot does **not** escape the parameter-level
obstruction. The retained Koide-Circulant Character Bridge identity
(positive_theorem,
[`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md))
makes the spectrum-level cone localization equation
**arithmetically identical** to the parameter-level BAE on
`Herm_circ(3)`:

```text
3 (λ_0² + λ_1² + λ_2²) − 2 (λ_0 + λ_1 + λ_2)²  =  −9 (a² − 2|b|²).   (*)
```

The cone slack on the left and the BAE slack on the right (the
retained algebraic equivalence
`Q = 2/3 ⇔ a² = 2|b|² ⇔ BAE`,
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md))
are the **same equation up to a non-vanishing real prefactor of −9**.
Vanishing of one is vanishing of the other; both have the same zero
set on `(a, |b|)`-space. Therefore:

- "spectrum lies on the Koide cone" and
- "operator parameters satisfy BAE"

are not distinct mathematical statements on `Herm_circ(3)`. They are
the SAME equation in DIFFERENT variables.

**Verdict: SHARPENED bounded obstruction.** The spectrum-level pivot
is RULED OUT as a route to BAE closure distinct from the parameter-
level routes already enumerated by Probes 1-21. The campaign's
terminal residue applies at BOTH levels. The BAE admission count is
UNCHANGED.

## Setup

### Premises (A_min for probe 22)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant (R1) | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| Spectrum (R2) | `λ_k = a + bω^k + b̄ω^{−k} = a + 2\|b\|cos(arg(b) + 2πk/3)` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R2 |
| Bridge | `a₀ = √3 a`, `\|z\|² = 3\|b\|²`, `a₀² − 2\|z\|² = 3a² − 6\|b\|²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md) (positive_theorem) |
| ConeIdentity | Cone equation iff Q = 2/3 (polynomial T2 identity) | source dependency; see [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md) (positive_theorem) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Campaign | 18-probe terminal residue: `(1,1)`-weighted Frobenius / `U(1)_b` angular quotient | source dependency; see [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md) + Probes 12, 13, 14, 18 |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new admissions added by this probe (verdict: SHARPENED, no
  closure achieved without admission, and no admission proposed)
- NO new axioms (per user 2026-05-09 clarification: closure must come
  from already-cited source-stack content or from a derivation extending the
  retained library)

## Derivation

### Step 1 — Spectrum-level cone localization is the spectral form of BAE

Substitute the retained spectrum (R2) `λ_k = a + bω^k + b̄ω^{−k}`
into the elementary symmetric polynomials:

```text
e₁ ≡ λ₀ + λ₁ + λ₂  =  3a               (uses 1 + ω + ω² = 0)
e₂ ≡ Σ_{i<j} λ_i λ_j  =  3a² − 3|b|²
p₂ ≡ λ₀² + λ₁² + λ₂²  =  e₁² − 2 e₂  =  9a² − 6a² + 6|b|²
                                            =  3a² + 6|b|²
```

(Runner Section 3, T3.2, T4.2 verifies the explicit forms.)

The cone localization condition

```text
3 p₂  =  2 e₁²
```

(equivalent to `Q = 2/3` per retained
[`KOIDE_CONE_THREE_FORM_EQUIVALENCE`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
T2) becomes

```text
3 (3a² + 6|b|²)  =  2 (3a)²
9 a² + 18 |b|²  =  18 a²
9 |b|²  =  9 (a² − |b|²) ... (rearranged)
```

Equivalently, the **cone slack** is

```text
3 p₂ − 2 e₁²  =  9 a² + 18 |b|² − 18 a²
              =  − 9 (a² − 2 |b|²)                     (*)
```

The right-hand side is the **BAE slack** `(a² − 2|b|²)` multiplied
by the non-vanishing real constant `−9`. (Runner Section 3, T3.3
verifies this exactly.)

### Step 2 — Bridge identity is the algebraic content of (*)

The retained Koide-Circulant Character Bridge identity (T3 of
[`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md))
states:

```text
a₀² − 2 |z|²  =  3 a² − 6 |b|²                        (Bridge T3)
```

Combined with the eigenvalue-side Plancherel identity
`p₂ = a₀² + 2|z|²` (retained per
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
equation 1) and `e₁² = 3 a₀²` (equation 2), the cone slack rewrites:

```text
3 p₂ − 2 e₁²  =  3 (a₀² + 2|z|²) − 2 · 3 a₀²
              =  3 a₀² + 6 |z|² − 6 a₀²
              =  − 3 (a₀² − 2 |z|²)
              =  − 3 (3 a² − 6 |b|²)                   (by Bridge T3)
              =  − 9 (a² − 2 |b|²).
```

This recovers (*) algebraically. Runner Section 2 verifies T3
symbolically; Section 3 T3.3 verifies the chain to (*) symbolically.

### Step 3 — The two slack expressions have the same zero set

Equation (*) is an algebraic identity on `Herm_circ(3)`. The cone
slack `3 p₂ − 2 e₁²` and the BAE slack `(a² − 2 |b|²)` differ only
by the non-vanishing real constant `−9`. Therefore:

```text
{(a, b) ∈ ℝ × ℂ  :  cone slack = 0}
   =  {(a, b) ∈ ℝ × ℂ  :  BAE slack = 0}
   =  {(a, b)  :  a² = 2|b|²}                          (BAE locus)
```

Vanishing of either slack is the BAE condition `|b|²/a² = 1/2`
(when `a ≠ 0`). Runner Section 4 T4.4 verifies this on six concrete
sample points (three BAE-satisfying, three off-BAE) and Section 4
T4.6 verifies the prefactor `−9` is non-vanishing.

### Step 4 — Spectrum invariants on the matter-sector circulant
### are functions of `(a, |b|)` only for BAE purposes

The matter-sector circulant `H = aI + bC + b̄C²` has 4 real DOF:
`(a, b_re, b_im)` (3 real DOF) plus a free overall sign / scale.
The eigenvalue triple `(λ_0, λ_1, λ_2)` is parametrized by
`(a, |b|, arg(b))` via the Brannen/Rivero spectral form
`λ_k = a + 2|b|cos(arg(b) + 2πk/3)`.

The full set of spectrum invariants is `{e_1, e_2, e_3}` (or
equivalently `{p_1, p_2, p_3}`):

```text
e_1  =  3 a                        (delta-INDEPENDENT)
e_2  =  3 a² − 3 |b|²              (delta-INDEPENDENT)
e_3  =  a³ − 3 a |b|² + 2 |b|³ cos(3 δ)   (delta-DEPENDENT)
```

(where `δ = arg(b)`, runner Section 5 T5.3 verifies). Of the three
spectrum invariants, only `e_3` carries `δ`-dependence — through
`cos(3δ)`. **The BAE condition is `δ`-independent** (it's `a² = 2|b|²`,
which contains no `δ`). Therefore the BAE-relevant spectrum invariants
are exactly `e_1` and `e_2`, both of which are functions of `(a, |b|)`
only.

This means: any spectrum-level statement on the matter-sector
circulant that bears on the BAE condition reduces to a statement in
`(a, |b|)`. The spectrum-level pivot has **no extra coordinate**
beyond `(a, |b|)` to break the parameter-level obstruction with.

(Runner Section 5 T5.1.1, T5.1.2, T5.2.e_1, T5.2.e_2 verify
δ-independence of `e_1, e_2, p_1, p_2`. Section 5 T5.1.3, T5.2.e_3
verify `e_3, p_3` ARE δ-dependent. Section 5 T5.5 records that the
BAE condition is δ-independent and thus reduces to (a, |b|) only.)

### Step 5 — The closure step is correct, conditional on antecedent

If, hypothetically, the antecedent "spectrum on Koide cone" could be
derived from cited source-stack content for the matter-sector circulant, the
retained polynomial identity
[`KOIDE_CONE_THREE_FORM_EQUIVALENCE`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
T2 would correctly close `Q = 2/3`, and the retained algebraic
equivalence
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
would correctly close BAE. **The closure step is sound**; the
problem is the antecedent.

By Steps 1-3, "spectrum on cone" = BAE on the matter-sector circulant.
By Step 4, no spectrum-level coordinate provides additional leverage.
Therefore the antecedent has the **same derivation content** as BAE
itself, and the 18-probe campaign's bounded structural obstruction
applies.

(Runner Section 6 T6.1-T6.4 verifies the closure step on retained
polynomial-identity ground.)

## Theorem (Probe 22 sharpened bounded obstruction)

**Theorem.** On A_min = A1 + A2 + retained `C_3`-action on `hw=1` +
retained `M_3(ℂ)` on `hw=1` + retained Circulant R1 + retained
Spectrum R2 + retained Bridge T1-T3 + retained ConeIdentity T2 +
retained KoideAlg + retained 18-probe campaign synthesis:

```text
(a) Substituting R2 into the cone slack `3 p₂ − 2 e₁²` gives
    exactly `−9 (a² − 2|b|²)` — algebraically equal to the BAE
    slack up to the non-vanishing real prefactor −9.
    [Closes from retained R1+R2+ConeIdentity+Bridge; runner Sections
     2-3.]

(b) The cone-localization condition (vanishing of cone slack) and
    the BAE condition (vanishing of `a² − 2|b|²`) cut out the SAME
    locus in `(a, |b|)`-space:
        cone-locus  =  BAE-locus  =  {(a, b) : a² = 2|b|²}.
    [Closes from (a) and the prefactor non-vanishing; runner
     Sections 3-4.]

(c) The BAE-relevant spectrum invariants `e₁ = 3a`,
    `e₂ = 3a² − 3|b|²`, `p₁ = e₁`, `p₂ = e₁² − 2e₂ = 3a² + 6|b|²`
    are δ-INDEPENDENT (where `δ = arg(b)`). The δ-dependent
    invariant `e₃ = a³ − 3a|b|² + 2|b|³ cos(3δ)` does NOT enter the
    BAE condition (since BAE is δ-independent). Therefore the
    spectrum-level pivot has NO extra coordinate beyond `(a, |b|)`
    to break the parameter-level obstruction with.
    [Closes from R2 + symbolic differentiation; runner Section 5.]

(d) The retained polynomial identity
    `KOIDE_CONE_THREE_FORM_EQUIVALENCE` correctly closes
    `Q = 2/3` from cone-localization, and the retained algebraic
    equivalence closes BAE from `Q = 2/3`. The closure step is
    sound; the problem is the antecedent.
    [Closes from retained polynomial identity; runner Section 6.]

Therefore: the spectrum-level cone localization pivot does NOT
provide a route to BAE closure distinct from the parameter-level
routes already enumerated by Probes 1-21. The pivot provides the
SAME equation in DIFFERENT variables, and the 18-probe campaign's
bounded structural obstruction applies at both levels.

The BAE admission count is unchanged. No new admission is proposed
by this probe. The campaign's terminal residue acquires explicit
coverage of the spectrum-level reformulation:

  "the canonical (1,1)-multiplicity-weighted Frobenius pairing on
   M_3(C)_Herm under C_3-isotype decomposition / equivalently
   the U(1)_b angular quotient on the non-trivial doublet of A^{C_3}"

remains the single named primitive whose absence blocks closure at
BOTH the parameter level and the spectrum level.
```

**Proof.** (a) is the algebraic computation of Step 1, verified
symbolically in runner Sections 2-3. (b) follows from (a) and the
prefactor `−9` being non-vanishing, verified in Section 4. (c)
follows from R2 + Newton-Girard / symbolic differentiation, verified
in Section 5. (d) follows from retained polynomial identity T2 +
retained algebraic equivalence, verified in Section 6. ∎

## Convention-robustness check

The spectrum-level pivot is invariant under:

- **Scale invariance**: `H → cH` rescales `(a, b) → (ca, cb)` and
  `λ_k → c λ_k`. Both cone slack and BAE slack scale as `c²`, so the
  zero set `(a² = 2|b|²)` is preserved. ✓ (Runner Section 4 T4.4
  on three BAE-satisfying samples at three different scales
  `a ∈ {sqrt(2), 2sqrt(2), sqrt(2)/2}`.)
- **Basis change** `C → C^{-1} = C²`: preserves the `C_3`-action and
  isotype structure (swaps `ω ↔ ω̄`). The eigenvalue spectrum is
  unchanged (just relabels the cube roots). ✓ (Implicit in R1, R2.)
- **`arg(b)`-shift** `b → e^{iα} b`: the eigenvalue triple is
  permuted (the cube roots cycle); the cone equation, BAE equation,
  and `e_1, e_2` are all unchanged. ✓ (Runner Section 4 T4.5.)

The bimodule frame for the matter-sector circulant `H = aI + bC + b̄C²`
is canonically pinned by cited source-stack content (R1: any `C_3`-equivariant
Hermitian on `hw=1` is of this form). What is **not pinned** is
the `(1,1)`-weighting / `U(1)_b` quotient — which Probe 22 confirms
applies at the spectrum level as well as at the parameter level.

## Comparison to prior probes in the BAE campaign

| Probe | Closure path | Result | Spectrum-level relevance |
|---|---|---|---|
| Probes 1-7 (Routes A, D, E, F + Probes 1, 2, 3, 4, 5, 6, 7) | Parameter-level: derive `(a, b)` ratio | Bounded obstruction | Inherited at spectrum level by Probe 22 |
| Probe 12 (Plancherel) | `\hat{C_3}`-Plancherel-uniform state on `A^{C_3}` | Bounded obstruction (gives `(1,2)` not `(1,1)`) | Inherited at spectrum level by Probe 22 |
| Probe 13 (Real-structure) | Antilinear involution `K` for `(1,1)` ℝ-isotype | Sharpened obstruction (Z_2, not SO(2)) | Inherited at spectrum level by Probe 22 |
| Probe 14 (Retained-U(1) hunt) | Existing retained U(1) projecting to U(1)_b | No candidate succeeds | Inherited at spectrum level by Probe 22 |
| Probes 15-17 (continuum, Q-functional, route 17) | Various | Bounded obstructions | Inherited at spectrum level by Probe 22 |
| Probe 18 (F1 vs F2 vs F3 functional) | Discrete Q-functional choice | Sharpened obstruction with partial F2-closure | Inherited at spectrum level by Probe 22 |
| **Probe 22 (this note)** | **Spectrum-level cone localization** | **Sharpened obstruction; pivot is bridge-illusory** | **N/A — this IS the spectrum-level probe** |

This probe contributes:

1. **Confirmation** that the bridge identity makes spectrum-level and
   parameter-level frames arithmetically identical for the matter-
   sector circulant `H = aI + bC + b̄C²`.
2. **Closure of the spectrum-level pivot route** as a distinct attack
   vector. Probe 22 rules out the spectrum-level reframing as a
   strategy; it does not contradict the campaign synthesis but
   sharpens its scope.
3. **Explicit coverage** of the spectrum-level invariants `(e_1, e_2,
   e_3)` / `(p_1, p_2, p_3)`: confirmation that BAE-relevant
   invariants are δ-independent, reducing to `(a, |b|)` only.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction; no closure)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["BAE: |b|²/a² = 1/2"]` —
  the residual admission, with the Probe 22 sharpening:
  "the (1,1)-multiplicity-weighted Frobenius pairing on
   M_3(ℂ)_Herm under C_3-isotype decomposition / equivalently
   the U(1)_b angular quotient on the non-trivial doublet of A^{C_3}"
  applies at both the parameter level and the spectrum level.

**No new admissions added by this probe.**

### What this probe DOES

1. Verifies the retained R1 + R2 forms on a concrete circulant
   `H = aI + bC + b̄C²` (Section 1).
2. Verifies the retained Bridge identity (T1, T2, T3) symbolically
   (Section 2).
3. Verifies that the spectrum-level cone slack
   `3 p₂ − 2 e₁²` equals `−9 (a² − 2|b|²)` algebraically (Section 3).
4. Verifies that "spectrum on cone" and "operator BAE" cut out the
   same locus in `(a, |b|)`-space (Section 4).
5. Verifies that BAE-relevant spectrum invariants are δ-independent
   (Section 5).
6. Verifies that the retained polynomial closure step (cone ⇒ Q=2/3
   ⇒ BAE) is sound (Section 6).
7. Verifies the verdict: spectrum-level pivot is bridge-illusory
   for the matter-sector circulant (Section 7).

### What this probe DOES NOT do

1. Does NOT close BAE.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem (BZ, 3GenObs, Circulant R1,
   Spectrum R2, Bridge T1-T3, ConeIdentity T2, KoideAlg, Campaign,
   any prior Probe).
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   campaign synthesis (admit / derive / pivot).
7. Does NOT propose `U(1)_b` as a new primitive (per user 2026-05-09
   constraint: no new axioms, no external imports).

## Honest assessment

The brief allowed three honest outcomes:

1. **CLOSURE**: derive that matter-sector eigenvalues lie on Koide
   cone from cited source-stack content. → **NOT ACHIEVED.** The bridge identity
   makes "spectrum-on-cone" arithmetically identical to BAE; deriving
   it would require deriving BAE.

2. **STRUCTURAL OBSTRUCTION**: spectrum-localization on cone cannot
   be derived from cited source-stack content. → **ACHIEVED (sharpened).** The
   obstruction is identified as a BRIDGE-IDENTITY-INHERITED
   obstruction. The retained Bridge T3 + retained Spectrum R2 +
   retained ConeIdentity T2 collectively make spectrum-level
   localization equivalent to parameter-level BAE. Therefore the
   18-probe campaign's bounded obstruction at parameter level
   applies, unchanged, at spectrum level.

3. **SHARPENED**: progress without full closure. → **ACHIEVED
   (sharpened bounded obstruction).** The probe sharpens the campaign
   by ruling out the spectrum-level pivot as an attack vector,
   explicitly localizing the obstruction at BOTH levels.

The campaign's terminal residue is now confirmed to apply at the
spectrum level as well: any spectrum-level coordinate (eigenvalue
triple, power sums, elementary symmetric polynomials) that bears on
BAE reduces by R2 to a function on `(a, |b|)`-space, where the
parameter-level obstruction lives.

**The pivot is illusory** because the bridge identity is exact and
retained: spectrum-side coordinates `(a₀, z)` and operator-side
coordinates `(a, b)` are linearly related by `a₀ = √3 a`, `z = √3 b`,
and the cone equation in eigenvalues maps directly to the BAE
equation in operator parameters under R2. **There is no
spectrum-level escape hatch on the matter-sector circulant.**

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant R1 + Spectrum R2: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Bridge T1-T3 (positive_theorem): [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
- Cone polynomial identity (positive_theorem): [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
- Cone completing-root (positive_theorem): [`KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Spectrum-operator bridge: [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)

### Eleven-probe campaign + Probes 12-18

- Campaign synthesis: [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (Real-structure): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 14 (Retained-U(1) hunt): [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)

### BAE rename

- Rename note: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md) (PR #790, 2026-05-09).

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_spectrum_cone_2026_05_09_probe22.py
```

Expected: `=== TOTAL: PASS=35, FAIL=0 ===`

The runner verifies:

1. Section 1 (5 tests) — Retained inputs (R1, R2) realized on
   concrete `H = aI + bC + b̄C²`: `C³ = I`, `C` unitary, `C`
   eigenvalues `{1, ω, ω̄}`, `H` Hermitian, eigenvalues match
   Brannen/Rivero form.
2. Section 2 (3 tests) — Retained Bridge identity (T1, T2, T3)
   verified symbolically: `a₀ = √3 a`, `|z|² = 3|b|²`,
   `a₀² − 2|z|² = 3a² − 6|b|²`.
3. Section 3 (4 tests) — Spectrum-level cone reduces to BAE:
   `F_orbit = const · (a² − 2|b|²)` symbolically, sum identities,
   cone slack = `−9 (a² − 2|b|²)`, BAE iff cone-localization at
   concrete sample points.
4. Section 4 (6 tests) — Spectrum-level pivot is bridge-identical to
   parameter-level: Brannen/Rivero spectral form, δ-independence of
   `e₁, e₂`, Q = 2/3 ⇔ BAE, locus equality on six samples,
   δ-independence of cone localization at BAE, prefactor `−9`
   non-vanishing.
5. Section 5 (9 tests) — Spectrum invariants are functions of
   `(a, |b|)` only for BAE purposes: `e₁, e₂, p₁, p₂` δ-independent;
   `e₃, p₃` δ-dependent (carry the residual angular DOF); explicit
   forms; e₃ takes different values for different δ; spectrum pivot
   adds no BAE-relevant DOF beyond `(a, |b|)`.
6. Section 6 (4 tests) — Retained polynomial closure `cone ⇒ Q = 2/3`:
   `F_ratio' = −F_orbit_retained` (T2 identity), concrete cone-on
   triple (1, 1, 4 + 3√2), concrete off-cone triple (1, 1, 1),
   closure step soundness conditional on antecedent.
7. Section 7 (4 tests) — Verdict: SHARPENED bounded obstruction; BAE
   admission count unchanged; no PDG values consumed; no new axioms
   or imports.

No hard-coded True values. All PASSes are keyed to substantive
symbolic or numerical computations.

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of any prior probe. The spectrum-level pivot is
  a structurally distinct attack vector from the parameter-level
  routes of Probes 1-21.
- Identifies a NEW STRUCTURAL FINDING: the bridge identity makes
  the spectrum-level pivot **arithmetically identical** to the
  parameter-level BAE on `Herm_circ(3)`. This is a closure of the
  spectrum-level reframing as a distinct attack route, not a relabel.
- Sharpens the campaign synthesis by explicitly extending the
  18-probe terminal residue to cover the spectrum-level
  reformulation: the campaign's named primitive applies at BOTH
  levels.
- Provides explicit symbolic coverage of the spectrum invariants
  `(e_1, e_2, e_3)` / `(p_1, p_2, p_3)` and their δ-dependence
  structure — establishing that BAE-relevant invariants reduce to
  `(a, |b|)`-only.

The spectrum-level pivot is a substantively different framing
(eigenvalue-side vs operator-parameter-side); ruling it out via the
bridge identity is a substantive structural result.

## Empirical AC testability

| Component | Testability |
|---|---|
| Bridge identity T3 | Pure algebraic identity (positive_theorem); no empirical input. |
| Cone-slack = -9 BAE-slack | Pure algebraic identity; no empirical input. |
| BAE-relevant δ-independence | Pure symbolic computation; no empirical input. |
| BAE residual admission | Same as parameter-level: tests via lattice MC of `(1,1)`-weighted Frobenius vs `(1,2)`-weighted Frobenius response on `M_3(ℂ)_Herm` would be falsifiable, but no PDG comparison is loaded. |

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: the bridge
  identity is a retained polynomial-algebra fact, not a derivation
  of BAE. The probe is honest that "spectrum-on-cone" and BAE are
  the same equation.
- `feedback_hostile_review_semantics.md`: this probe stress-tests
  the action-level identification — does pivoting from
  parameter-side to spectrum-side change what the equation says
  about the matter-sector operator? Answer: no, because the bridge
  identity is exact and the eigenvalue triple is functionally a
  re-coordinatization of `(a, |b|, arg(b))`.
- `feedback_retained_tier_purity_and_package_wiring.md`: probe is
  a bounded source-note proposal; no automatic cross-tier promotion;
  audit lane decides. The probe respects cited source-stack content (R1, R2,
  Bridge, ConeIdentity, KoideAlg, Campaign) and does not propose any
  promotion.
- `feedback_physics_loop_corollary_churn.md`: the spectrum-level
  pivot is a structurally distinct attack vector. The bridge-identity
  closure of this pivot is substantive new content, not a relabel.
- `feedback_compute_speed_not_human_timelines.md`: closure paths are
  characterized in terms of WHAT additional content would be needed
  (the U(1)_b primitive identified by Probes 13-14), not in terms of
  human-time estimates.

## Status

```yaml
actual_current_surface_status: bounded_theorem (sharpened obstruction)
proposed_claim_type: bounded_theorem
audit_review_points: |
  Conditional on:
   (a) independent audit confirmation that the bridge identity
       T3 (KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE
       2026-05-09) is recognized as positive_theorem retained;
   (b) independent audit confirmation that the cone slack
       3 p₂ − 2 e₁² equals −9 (a² − 2|b|²) on Herm_circ(3) (verified
       symbolically by the runner);
   (c) independent audit confirmation that the BAE-relevant
       spectrum invariants `(e₁, e₂)` are δ-independent, reducing
       to `(a, |b|)` only;
   (d) the verdict "spectrum-level pivot is bridge-illusory" being
       recognized as a sharpening of the campaign synthesis without
       contradicting any cited source-stack content.
hypothetical_axiom_status: null
admitted_observation_status: |
  BAE residual = "the (1,1)-multiplicity-weighted Frobenius pairing
  on M_3(ℂ)_Herm under C_3-isotype decomposition / equivalently
  the U(1)_b angular quotient on the non-trivial doublet of A^{C_3}"
  applies at both the parameter level (Probes 1-21) and the
  spectrum level (Probe 22).
claim_type_reason: |
  This note rules out the spectrum-level cone localization pivot as
  a route to BAE closure distinct from the parameter-level routes
  enumerated by Probes 1-21. The retained Bridge identity makes the
  two levels arithmetically identical for the matter-sector circulant.
  The probe's verdict is SHARPENED bounded obstruction; the BAE
  admission count is UNCHANGED.
independent_audit_required_before_status_change: true
bare_retained_allowed: false
forbidden_imports_used: false
```
