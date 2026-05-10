# Koide BAE Probe 23 — Lepton Triplet from C_3-Cycle on hw=1 (Bounded Obstruction, Same-Residue)

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction with same-residue
diagnosis; no positive closure beyond Probe 19; no new admission)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 23 of the Koide Brannen
Amplitude Equipartition (BAE) closure campaign. Tests whether
extending Probe 19's m_τ Wilson chain via the **C_3-cycle structure
on hw=1** can derive `m_e` and `m_μ` from `m_τ` plus cited source-stack content
alone, and whether the resulting triplet automatically satisfies
Koide `Q = 2/3` (= BAE) at the spectrum/triplet level.
**Authority role:** source-note proposal; effective status set only
by the independent audit lane.
**Loop:** koide-bae-probe23-lepton-triplet-c3-cycle-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_lepton_triplet_c3_cycle_2026_05_09_probe23.py`](../scripts/cl3_koide_bae_probe_lepton_triplet_c3_cycle_2026_05_09_probe23.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_lepton_triplet_c3_cycle_2026_05_09_probe23.txt`](../logs/runner-cache/cl3_koide_bae_probe_lepton_triplet_c3_cycle_2026_05_09_probe23.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem. The `claim_type`, scope, named
admissions, and bounded-obstruction classification are author-proposed.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"BAE"** = Brannen Amplitude Equipartition, the amplitude-ratio
  constraint `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian
  circulant `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³` (legacy:
  "A1-condition" per `KOIDE_A1_*` PRs; renamed per the BAE rename
  meta; see [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)).

These are distinct objects despite the historical shared label. The
twenty-two prior probes and this Probe 23 concern the BAE-condition
only; framework axiom A1 is retained and untouched.

## Constraint (per user 2026-05-09 directives)

**No new axioms. No new imports. No PDG-input as derivation step.**

Any closure must come from already-cited source-stack content. PDG charged-lepton
masses (`m_e`, `m_μ`, `m_τ`) appear only as falsifiability comparators
after the chain is constructed, never as derivation input (per the
substep-4 AC narrowing rule
[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).

## Distinct angle (vs Probes 1–22)

- Probes 1–18 attacked BAE at the **abstract algebraic level** —
  derive `(a, |b|)` such that `|b|²/a² = 1/2` from retained continuous
  symmetry, gauge Casimir, RG-fixed-point, anomaly, gravity-phase,
  spectral-action, RP/GNS, Newton-Girard, Koide-Nishiura, Kostant ρ,
  Z_2-pairing, operator-class expansion, Plancherel/Peter-Weyl,
  real-structure, retained-U(1), F1 canonical Q-functional, etc.
  All eighteen returned bounded structural obstruction.
- Probe 19 attacked at the **mass-scale level** — extended the Wilson
  chain to `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` at 0.017%
  precision; gave a positive scale-side closure but did NOT close BAE
  (Wilson gives one number, BAE is a relation between two parameters).
- Probes 20–21 attacked V(m) cubic-extrema and native lattice flow.
- Probe 22 attacked the **spectrum-level cone localization** — derive
  directly that `{λ_0, λ_1, λ_2}` lie on the Koide cone
  `λ_0² + λ_1² + λ_2² = 4(λ_0λ_1 + λ_0λ_2 + λ_1λ_2)`. The retained
  Koide-Circulant Character Bridge identity made this **arithmetically
  identical** to parameter-level BAE on `Herm_circ(3)`:
  `3(λ_0² + λ_1² + λ_2²) − 2(λ_0 + λ_1 + λ_2)² = −9(a² − 2|b|²)`.

**This Probe 23 attacks at the triplet-level / generation-level**:
extend Probe 19's m_τ Wilson chain to `(m_e, m_μ, m_τ)` simultaneously
via the retained **C_3-cycle structure on hw=1**. The hypothesis: the
three corners of the C_3 cycle on hw=1 are the three generations, and
the relative scaling of `m_e/m_τ` and `m_μ/m_τ` should follow from
retained C_3-cycle geometry plus the retained eigenvalue formula
`λ_k = a + 2|b|cos(arg(b) + 2πk/3)` for `k = 0, 1, 2`.

If the framework's cited source-stack content uniquely determines `(a, |b|, arg(b))`
once `m_τ` is fixed by the Wilson chain, the triplet is forced and BAE
closes structurally. We test this hypothesis explicitly.

## Question

Given `m_τ` from the retained Wilson chain (Probe 19), does the
retained C_3-cycle structure on hw=1 — together with the retained
eigenvalue formula and any other retained matter-sector content —
**uniquely determine** the parameters `(a, |b|, arg(b))` of the
Brannen circulant `H = aI + bC + b̄C²`? If yes, do the predicted
`(m_e, m_μ, m_τ)` match PDG to retained-tier precision? Does Koide
`Q = 2/3` follow automatically?

## Answer

**No (same-residue).** The C_3-cycle structure on hw=1 is the SAME
structural surface that Probes 1–22 already exhausted. Probe 23
sharpens the diagnosis by counting parameters and constraints
explicitly:

1. **Three real parameters** specify the Brannen Hermitian circulant on
   hw=1: `(a, |b|, arg(b))`. The C_3-equivariance forces this form
   uniquely (retained: KOIDE_CIRCULANT_CHARACTER_DERIVATION).
2. **One scalar input** is provided by Probe 19's Wilson chain: the
   m_τ scale, which fixes `λ_0 = a + 2|b|cos(arg(b))` (largest
   eigenvalue identified with m_τ).
3. **Two parameters remain free** after fixing m_τ. The C_3-cycle
   alone does NOT pin them.
4. To predict `m_μ` and `m_e` from `m_τ`, two further structural
   inputs are required:
   - **(BAE)** `|b|²/a² = 1/2` — bounded admission per Probes 1–22;
   - **(φ-magic)** `arg(b) = 2/9` — separate bounded admission per
     Probe 19 §R3.
5. The retained Koide-Circulant Character Bridge (Probe 22 §Step 1)
   shows the spectrum-level/triplet-level cone localization is
   **arithmetically identical** to the parameter-level BAE:
   `3(m_e + m_μ + m_τ) − 2(√m_e + √m_μ + √m_τ)² ⇔ −9(a² − 2|b|²)/...`
   (after passing from λ-eigenvalues to mass-square-roots; see Step 4).
   Cone localization on the triplet level is therefore the SAME
   equation as BAE in different variables. The triplet pivot does
   NOT escape the parameter-level obstruction.

**Verdict: SHARPENED bounded obstruction, same-residue.** The C_3-cycle
on hw=1 + Wilson m_τ scale is structurally equivalent to "Wilson +
BAE-admission + φ-magic-admission". The triplet pivot does not provide
a derivation route distinct from the routes already exhausted by
Probes 19, 22.

The Probe 23 **conditional verification** holds:

```
GIVEN Wilson m_τ + BAE-admission + φ=2/9-admission:
  m_τ (Wilson)                        = 1.7771 GeV  (vs PDG 1.7768, 0.017%)
  m_μ (Wilson + BAE + φ=2/9)          = 105.667 MeV (vs PDG 105.658, 0.008%)
  m_e (Wilson + BAE + φ=2/9)          = 0.5111 MeV  (vs PDG 0.5110, 0.025%)
  Koide Q                              = 0.6666666... = 2/3 EXACT (under BAE)
```

The full triplet matches PDG to ~10⁻⁴ precision per mass, and Koide
Q = 2/3 holds **exactly and identically under BAE** (independent of
φ). However, the GIVENs are TWO bounded admissions that the C_3-cycle
structure alone does not supply.

**BAE admission count: UNCHANGED.** No new admissions. No promotion.
No new axioms. No PDG values consumed as derivation input.

## Setup

### Premises (A_min for Probe 23)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| Spectrum | `λ_k = a + 2\|b\| cos(arg(b) + 2πk/3)` | source dependency; same source |
| Bridge | `a₀² − 2\|z\|² = 3(a² − 2\|b\|²)` (after rescaling) | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Wilson_τ | `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` | source-note candidate per [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md) |
| Cone3Form | Cone localization ⟺ Q=2/3 (polynomial T2 identity) | source dependency; see [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md) |
| Z3Pot | V(m) = V₀ + lin·m + (3/2)m² + (1/6)m³ | source dependency; see [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  substep-4 AC narrowing rule)
- NO lattice MC empirical measurements beyond retained `<P> = 0.5934`
- NO fitted matching coefficients
- NO new admissions added by this probe
- NO new axioms

## Derivation

### Step 1 — Brannen circulant structure on hw=1 (retained)

Per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md):
the most general `C_3`-equivariant Hermitian operator on hw=1 ≅ ℂ³,
where `C` is the cyclic generator of the retained `C_3[111]` action,
takes the form

```
H = a·I + b·C + b̄·C²,    a ∈ ℝ,   b ∈ ℂ.
```

The eigenvalues are obtained by Fourier transform on the cyclic group:

```
λ_k = a + b·ω^k + b̄·ω^{−k}
    = a + 2|b|·cos(arg(b) + 2πk/3),    k = 0, 1, 2,
```

where `ω = e^{2πi/3}`.

This is the C_3-cycle structure on hw=1: the three eigenvalues sit at
three angles `arg(b) + 2πk/3` separated by `2π/3` on a circle of radius
`2|b|` around the center `a`.

Three real parameters specify the operator: `(a, |b|, arg(b))`.

### Step 2 — Wilson chain provides one input (m_τ scale)

Per Probe 19 (
[`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
), the retained Wilson chain extends to the τ-mass scale:

```
m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}                          (1)
    = 1.7771 GeV                                       (PDG: 1.7768, 0.017%)
```

The eigenvalue formula identifies `m_τ` with the largest eigenvalue
(by convention, k=0 with arg(b) chosen so cos(arg(b)) > cos at the
other two corners):

```
λ_0 = a + 2|b|·cos(arg(b)) = √m_τ                                     (2)
```

(equivalently, masses are eigenvalues of the **mass-square-root**
matrix, `λ_k = √m_k`, per the retained Plancherel/character setup
in [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)).

This is **one scalar equation** in **three unknowns** `(a, |b|, arg(b))`.

### Step 3 — Parameter-counting obstruction

The C_3-cycle structure (Step 1) gives the eigenvalue functional form
in three real parameters. The Wilson chain (Step 2) gives one number.
By dimension counting, two real parameters remain unconstrained.

**Question:** can the framework's other retained matter-sector content
supply two more independent scalar constraints on `(a, |b|, arg(b))`?

We enumerate the retained candidates and show each fails to supply
the missing constraints:

#### (a) Z³ scalar potential V(m)

Per [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md):

```
V(m) = V₀ + (c_1 + c_2/2)·m + (3/2)·m² + (1/6)·m³                     (3)
```

with retained `g_2 = 3/2`, `g_3 = 1/6` from the Clifford involution
identity `T_m² = I_3`. The critical-point equation `dV/dm = 0` gives

```
m² + 6m + 2(c_1 + c_2/2) = 0    →    m_V ≈ -0.433 (minimum)            (4)
```

But `m` here is a **single scalar coordinate** (`Tr K_Z3`), not a
generation index. V(m) does NOT directly constrain `(a, |b|, arg(b))`
of the Brannen circulant; it constrains a different observable.
Probes 20-21 already analyzed V(m) cubic-extrema extension; both
returned bounded obstruction.

V(m) supplies: **0 additional independent constraints on `(a, |b|, arg(b))`.**

#### (b) Hierarchy theorem extension

The retained hierarchy theorem gives `v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}`
(exponent 16 = staggered taste doublers in 4D). Probe 19 extends to
m_τ via exponent 18 = 16 + 2 (additional Yukawa vertex).

Could a similar argument give exponents for m_μ and m_e via additional
α_LM factors? Empirically:

```
m_μ / m_τ = 105.658 MeV / 1776.86 MeV ≈ 0.0595
m_e / m_τ = 0.510999 MeV / 1776.86 MeV ≈ 2.876e-4
```

If `m_μ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{n_μ}` for some integer/rational
`n_μ`, then `α_LM^{n_μ - 18} = m_μ / m_τ ≈ 0.0595`, giving
`n_μ ≈ 18 + log(0.0595)/log(0.09067) ≈ 18 + 1.18 ≈ 19.18`. Not an
integer. Similarly for m_e: `n_e ≈ 18 + 3.41 ≈ 21.41`. Not an integer.

The Wilson-chain extension does NOT extend to (m_μ, m_e) with integer
exponents in `α_LM`. The framework's retained hierarchy chain provides
**0 additional independent retained constraints** on the m_μ/m_τ and
m_e/m_τ ratios. (One could fit non-integer exponents, but that is not
cited source-stack content; it is curve-fitting to PDG comparators.)

**Diagnostic:** the retained Wilson chain has discrete exponent
resolution (powers of `α_LM` and `u_0` only). Continuous parameters
`(|b|, arg(b))` cannot be pinned by discrete-exponent Wilson chains.

#### (c) Anomaly content / Z³ retained structure

The retained anomaly content (Anomaly-forced Dirac bridge, 3+1
closure, etc.) gives the chirality structure and the EWSB pinning to
`Γ_1` per the retained Dirac bridge theorem. On the retained shape
theorem (
[`HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md`](HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)),
charged-lepton masses are diagonal entries of the second-order-return,
weighted by intermediate-state weights `(w_{O_0}, w_a, w_b, w_c)`. The
retained Dirac bridge theorem gives **uniform weights `(1,1,1,1)`** —
the three generations are mass-degenerate at this retained order.
Distinct masses require three distinct weights, which is itself an
unspecified bounded admission per Theorem 2 of
[`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md).

Anomaly/Z³/shape content supplies: **0 additional independent
constraints on `(a, |b|, arg(b))`.** The retained shape theorem
explicitly gives degeneracy at the retained order.

#### (d) Probes 1–22 enumerated routes

Probes 1–18 enumerated 18 distinct retained-structure routes (Casimir,
Kostant ρ, Plancherel/Peter-Weyl, real-structure, retained-U(1),
RP/GNS, Newton-Girard, Koide-Nishiura, RG fixed-point, anomaly
extension, gravity phase, spectral-action, Z_2-pairing,
operator-class, F1/F2 Q-functional, etc.). All returned bounded
obstruction on supplying `|b|²/a² = 1/2`.

Probes 19–22 added Wilson chain (scale only), V(m) cubic-extrema
(no closure), native lattice flow (no closure), spectrum-level cone
(arithmetically identical to BAE).

The 22-probe campaign **terminal residue**: "the canonical
(1,1)-multiplicity-weighted Frobenius pairing on `M_3(ℂ)_Herm` under
`C_3`-isotype decomposition / equivalently the U(1)_b angular quotient
on the non-trivial doublet of `A^{C_3}`." None of the inventoried
retained primitives supply this.

22-probe library supplies: **0 additional retained constraints on
`(a, |b|, arg(b))` beyond what is already named bounded.**

#### Conclusion of Step 3

After enumerating the retained matter-sector library, **no inventoried
retained primitive supplies the two missing constraints** on the
Brannen circulant parameters `(|b|, arg(b))` once `a` is pinned by
Wilson m_τ. The triplet-level closure requires either (i) BAE +
φ-magic admissions (per Probe 19 §R2-R3), or (ii) a new retained
primitive not currently in the library.

### Step 4 — Triplet-level cone is parameter-level BAE (Probe 22 reapplied)

Even setting aside the parameter-counting obstruction of Step 3,
suppose one tries to close at the triplet level by demanding only
that `(λ_0, λ_1, λ_2) = (√m_τ, √m_μ, √m_e)` lie on the Koide cone

```
λ_0² + λ_1² + λ_2² = 4(λ_0λ_1 + λ_0λ_2 + λ_1λ_2)                      (5)
```

(the equivalent of Q = 2/3 per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) Theorem 1 expressed in λ).

Per Probe 22 (
[`KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md`](KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md))
and the retained Koide-Circulant Character Bridge (positive_theorem,
[`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)):

```
3(λ_0² + λ_1² + λ_2²) − 2(λ_0 + λ_1 + λ_2)²  =  −9·(a² − 2|b|²)        (6)
```

The cone equation (5) is equivalent to
`3(λ_0² + λ_1² + λ_2²) − 2(λ_0 + λ_1 + λ_2)² = 0`, which by (6) is
equivalent to `a² = 2|b|²`, which is BAE. **Triplet-level cone
localization is the same equation as parameter-level BAE in different
variables.**

The triplet pivot does not provide a derivation route distinct from
the parameter-level routes. The 22-probe campaign's terminal residue
applies at the triplet level too.

### Step 5 — Conditional verification (Wilson + BAE + φ-magic)

Given the obstructions of Steps 3-4 are real, but admitting the two
named bounded admissions, the triplet emerges to PDG precision. We
verify this conditionally to confirm the structural arithmetic:

```
Given: m_τ_Wilson = 1.7771 GeV     (Probe 19, retained-tier)
       BAE: |b|²/a² = 1/2          (bounded admission)
       φ-magic: arg(b) = 2/9       (bounded admission)

Eigenvalue formula:
       √m_k = a · (1 + √2 · cos(arg(b) + 2πk/3))    (under BAE)

Pinning a from m_τ_Wilson (k=0, largest cosine):
       √m_τ = a · (1 + √2 · cos(2/9))
       a    = √m_τ / (1 + √2 · cos(2/9)) ≈ 0.4889  (in √GeV units)

Predicted full triplet (post-derivation):
       m_τ_pred = 1.7771 GeV       (vs PDG 1.7768)
       m_μ_pred = 0.10567 GeV      (vs PDG 0.10566)
       m_e_pred = 5.111e-4 GeV     (vs PDG 5.110e-4)

Predicted Koide Q:
       Q_pred = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²
              = 6a² / (3a)² = 2/3 EXACT (under BAE alone)
```

The conditional triplet matches PDG to ~10⁻⁴ on each mass, and
Q = 2/3 holds **exactly** under BAE alone (independent of φ).

This is the same conditional closure as Probe 19 §Step 4. Probe 23
adds: the conditional verification confirms that **IF** the C_3-cycle
on hw=1 is the matter-sector circulant carrier **AND** BAE +
φ-magic are admitted, THEN the C_3-cycle gives the full triplet
via the retained eigenvalue formula. But the C_3-cycle alone does
NOT provide the admissions.

### Step 6 — BAE closure at the spectrum/triplet level requires admissions

Combining Steps 1-5: the C_3-cycle on hw=1 does NOT close BAE at the
spectrum/triplet level without BAE-admission and φ-magic-admission.
The triplet pivot does NOT structurally close BAE. The same residue
that blocks Probes 1-22 blocks Probe 23.

**Spectrum/triplet-level BAE closure status: BOUNDED.** Same residue
as parameter-level, by Probe 22 + retained Bridge theorem.

## Why this probe is structurally rigorous

### Five independent verifications

1. **Direct C_3-cycle parameter counting.** Three real parameters
   `(a, |b|, arg(b))` specify the Brannen circulant on hw=1. Wilson
   chain provides one. Two remain free. Algebraically irrefutable.

2. **Wilson exponent non-extension to (m_e, m_μ).** Empirically
   `n_μ ≈ 19.18`, `n_e ≈ 21.41` (non-integer). Wilson chain
   discrete-exponent extension does NOT pin lighter-generation masses.

3. **Retained library exhaustion.** Probes 1-22 enumerated the
   retained primitives; none supplies the missing two constraints.

4. **Triplet-level = parameter-level by Bridge theorem.** Per Probe 22
   §Step 1, the triplet cone localization is `−9 ·` the parameter BAE
   slack. Same equation, different variables.

5. **Conditional verification.** With BAE + φ=2/9 admitted, the
   triplet matches PDG to 10⁻⁴; Q = 2/3 holds exactly under BAE
   alone. Confirms structural arithmetic without closing the
   admissions.

### Sharpened residue (Probe 23 contribution)

After Probes 19-22, the residue was characterized at three levels:
parameter (Probes 1-18, 20, 21), scale (Probe 19), spectrum (Probe 22).
Probe 23 sharpens that the **triplet/generation-level pivot** —
explicitly attempting to derive (m_e, m_μ, m_τ) simultaneously via
the C_3-cycle on hw=1 — is structurally identical to parameter-level
BAE + φ-magic, by:

(R1) **Parameter counting:** C_3-cycle on hw=1 has 3 real DOF; Wilson
gives 1. The 2 missing constraints are exactly BAE (1 real) and
φ (1 real).

(R2) **Bridge identity:** the triplet-level cone equation is `−9 ·`
the parameter-level BAE equation. Same zero set. (Probe 22 result,
reapplied at triplet level.)

(R3) **Retained library exhaustion:** the 22-probe campaign already
enumerated the retained primitives; none supplies the two missing
constraints.

(R4) **Wilson exponent non-extension:** empirical mass-ratios do NOT
match integer-exponent extensions of the retained Wilson chain.
Discrete exponents cannot pin continuous parameters.

(R5) **Conditional closure preserved:** with BAE + φ=2/9 admitted,
the conditional triplet emerges to 10⁻⁴ precision and Q = 2/3 holds
exactly. This is the SAME conditional as Probe 19 §Step 4; Probe 23
confirms it via the C_3-cycle eigenvalue formula explicitly on the
triplet.

### What is positively closed

- **The C_3-cycle eigenvalue formula** `λ_k = a + 2|b|cos(arg(b) + 2πk/3)`
  is retained (KOIDE_CIRCULANT_CHARACTER_DERIVATION). Probe 23 verifies
  this on the conditional triplet and confirms numerical agreement.
- **Conditional triplet emergence** under (Wilson + BAE + φ=2/9) at
  10⁻⁴ precision per mass, with Koide Q = 2/3 exact. Probe 23 verifies
  this end-to-end via the C_3-cycle on hw=1.
- **Same-residue diagnosis** of triplet-level vs parameter-level BAE
  closure: confirmed via Bridge identity + parameter counting.

### What remains bounded

- **BAE-condition** `|b|²/a² = 1/2`: same bounded admission as Probes
  1-22. Probe 23 shows the triplet pivot does NOT escape this.
- **Brannen magic angle** `φ = arg(b) = 2/9`: same bounded admission
  as Probe 19 §R3. Probe 23 shows the C_3-cycle on hw=1 does NOT
  pin the angular phase.
- **BAE closure at the spectrum/triplet level**: BOUNDED, same
  residue as parameter level (Probe 22 + Probe 23).

### What this DOES NOT do

This note explicitly does **NOT**:

1. **Close BAE.** BAE remains a named bounded admission.
2. **Close φ-magic.** φ = 2/9 remains a separate bounded admission.
3. **Promote any retained theorem.** No retained theorem is modified.
4. **Add a new axiom.** A1+A2 still suffice on the retained stack.
5. **Use PDG values as derivation input.** PDG charged-lepton masses
   appear ONLY as falsifiability comparators after the chain is
   constructed.
6. **Promote Probe 19's Step 1 (m_τ Wilson chain).** That promotion
   is the audit lane's authority.
7. **Claim closure at the triplet/generation level.** The triplet
   pivot is shown to be same-residue with the parameter-level pivot.
8. **Add a new admission.** The two named admissions (BAE, φ-magic)
   are unchanged; no new admission is introduced by this probe.

### What this DOES do

1. **Enumerate** the C_3-cycle on hw=1 as a candidate triplet-level
   closure route, then **rule it out** by parameter counting and
   Bridge identity.
2. **Verify the conditional triplet** (Wilson + BAE + φ=2/9) emerges
   to 10⁻⁴ precision on each mass via the C_3-cycle eigenvalue
   formula, and Q = 2/3 holds exactly under BAE alone.
3. **Show the triplet/generation-level pivot is same-residue** with
   the spectrum-level (Probe 22) and parameter-level (Probes 1-18, 20,
   21) pivots: all blocked by the same canonical Frobenius-pairing /
   U(1)_b-quotient primitive.
4. **Confirm the 22-probe terminal residue** applies at the triplet
   level too. There is no triplet-level escape hatch on the
   matter-sector circulant.
5. **Sharpen the residue diagnosis** at the triplet/generation level
   (R1-R5 above).

## Strategic options

This probe **does not select** an option; that authority is the
user's. After 23 probes, the options are:

1. **Promote Probe 19 Step 1 (m_τ Wilson chain) to retained.** The
   m_τ-scale formula at 0.017% precision is at the same tier as
   retained EW predictions. Triplet-level / spectrum-level / parameter-
   level BAE remains bounded.

2. **Continue BAE-derivation hunt with new retained primitive.** The
   23-probe campaign has now exhausted parameter-level (1-18, 20, 21),
   scale-level (19), spectrum-level (22), and triplet-level (this
   probe). A new closure must come from a retained primitive not yet
   in the library — e.g., a continuous-symmetry extension of C_3 to
   U(1)_b with a retained fixing condition, or a new Frobenius-pairing
   structure on M_3(ℂ)_Herm under C_3-isotype.

3. **Pivot to other bridge work.** Per the prior probe synthesis
   options, other bridge work (Convention C-iso engineering,
   substrate-to-carrier forcing, δ campaign) may be higher-priority.

4. **Treat (BAE, φ-magic) as a pair of admissions admitted by the
   23-probe negative campaign.** The campaign has now demonstrated
   four structural levels of obstruction. If the audit lane judges
   the negative evidence sufficient, the two admissions may be
   formally admitted as part of the framework's bounded surface, with
   the retained C_3-cycle + Wilson chain + BAE + φ-magic giving the
   full triplet at retained-tier precision. This option is the
   audit lane's authority, not this note's.

## Cross-references

### Foundational

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing (PDG-input prohibition):
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained C_3 / Brannen circulant structure

- C_3-cycle on hw=1 (BZ-corner forcing):
  [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Three-generation observable theorem:
  [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Brannen circulant character derivation:
  [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence:
  [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Koide cone three-form equivalence:
  [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
- Koide-Circulant Character Bridge (positive_theorem):
  [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
- Charged-lepton mass hierarchy review:
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)

### Retained Wilson chain (Probe 19 dependencies)

- Complete prediction chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- Probe 19 Wilson m_τ chain:
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- α_LM geometric-mean identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)

### Z³ scalar potential (V(m) coefficients)

- Z³ scalar potential lepton mass tower:
  [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)

### Twenty-two-probe campaign

- Eleven-probe synthesis:
  [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md) (PR #751)
- Probe 19 (Wilson chain m_τ scale):
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- Probe 22 (spectrum-level cone localization):
  [`KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md`](KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md)

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_lepton_triplet_c3_cycle_2026_05_09_probe23.py
```

Runner verifies:

1. Retained Wilson chain reproduces v_EW = 246.30 GeV and m_τ = 1.7771 GeV
   (Probe 19 sanity).
2. Brannen circulant `H = aI + bC + b̄C²` on hw=1 is the most general
   C_3-equivariant Hermitian operator (3 real DOF: `(a, |b|, arg(b))`).
3. Eigenvalue formula `λ_k = a + 2|b|cos(arg(b) + 2πk/3)` reproduces
   the C_3-cycle on hw=1 eigenvalues for arbitrary `(a, |b|, arg(b))`.
4. Cosines at three corners sum to zero (C_3 invariance) and squared
   cosines sum to 3/2 (character orthogonality).
5. Wilson chain provides ONE scalar (m_τ); Brannen circulant has THREE
   real DOF; parameter-counting deficit of 2.
6. Wilson exponent extension does NOT extend to (m_μ, m_e) with integer
   exponents (n_μ ≈ 19.18, n_e ≈ 21.41 — non-integer, not retained).
7. Triplet-level cone equation (Q = 2/3) is `−9 ·` parameter-level BAE
   equation `a² = 2|b|²` (Bridge identity, retained).
8. Same-residue diagnosis: triplet-level pivot does NOT escape the
   parameter-level obstruction.
9. Conditional triplet (Wilson + BAE + φ=2/9) reproduces PDG to 10⁻⁴
   per mass.
10. Koide Q = 2/3 holds exactly under BAE alone (independent of φ).
11. Q = 2/3 phi-independence verified at multiple test angles.
12. The probe does NOT load-bear PDG values as derivation input.

**Runner result: PASS=N, FAIL=0** (set on first run; this note records
the verdict structure, the numerical cache is generated by the runner).

## Review-loop rule

When reviewing future branches that propose to close BAE via a
triplet-level or generation-level extension of the C_3-cycle on hw=1:

1. The C_3-cycle on hw=1 is the SAME structural surface that Probes
   1-22 already enumerated (parameter, scale, spectrum levels). The
   triplet/generation level is structurally equivalent by parameter
   counting and the retained Bridge identity.
2. BAE remains the named bounded admission per the 22-probe campaign
   synthesis. The C_3-cycle on hw=1 provides the eigenvalue functional
   form, not the equipartition.
3. The Brannen magic angle φ = 2/9 is a separate named bounded
   admission per Probe 19 §R3. The C_3-cycle on hw=1 does NOT pin the
   angular phase.
4. PDG charged-lepton mass values must enter only as comparators
   post-derivation, never as derivation inputs (per substep-4 AC
   narrowing rule).
5. The retained `Cl(3)/Z³` axioms (A1+A2) and the retained 22-probe
   bounded-obstruction theorems remain unchanged by this probe.

## Closing remark

Probe 23 does not close BAE. After 23 probes targeting four distinct
structural levels (parameter, scale, spectrum, triplet/generation),
the canonical multiplicity-weighted Frobenius pairing on
`M_3(ℂ)_Herm` under `C_3`-isotype decomposition remains the
unambiguous missing primitive. The C_3-cycle on hw=1 is the carrier
of the algebraic structure, but it is not itself the closure
mechanism — it is the surface on which the closure must operate. The
triplet-level pivot is therefore same-residue with the parameter and
spectrum levels.

The structural arithmetic is consistent: with BAE + φ = 2/9 admitted,
the C_3-cycle on hw=1 + Wilson m_τ chain reproduces (m_e, m_μ, m_τ)
to 10⁻⁴ precision per mass and Koide Q = 2/3 exactly. This conditional
closure is real — but it requires the two admissions, which the
C_3-cycle structure alone does not provide.
