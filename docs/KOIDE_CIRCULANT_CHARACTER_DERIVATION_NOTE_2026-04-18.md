# Koide Q = 2/3 as a C_3[111] Character-Theoretic Derivation — Candidate Extension Note

**Date:** 2026-04-18
**Status:** candidate extension note — exact circulant/character bridge on the
retained `C_3[111]` orbit, but no retained Koide derivation on the current
surface
**Relates to:** `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`,
`docs/HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`,
`docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`,
`docs/KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md`,
`docs/KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`,
`docs/KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`,
`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`

## Summary

The charged-lepton Koide relation
```
Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3
```
admits a new **operator-space reformulation** on the retained `Cl(3)` on `Z^3`
surface. On the retained `hw=1` triplet, every Hermitian operator commuting with
the `C_3[111]` action is circulant, and its eigenvalue triple has exactly the
Brannen/Rivero cosine form. If one further assumes the matrix-space
equipartition condition `A1` and the phenomenological identification `P1`, then
Koide `Q = 2/3` follows algebraically.

This does **not** change the current retained charged-lepton status. The
authoritative April 17 review still stands: on the present retained surface the
charged-lepton sector is bounded observational-pin only. The contribution of
this note is to isolate the exact retained backbone `(R1, R2)` and sharpen the
candidate extension route beyond it.

The three charged-lepton masses reduce to a **one-parameter family** (plus
overall scale) given Koide:
```
√m_k = v_0 (1 + √2 cos(δ + 2πk/3))        [Brannen/Rivero 2006, hep-ph/0505220]
```
with `δ ≈ 2/9 rad` for charged leptons. The Koide prediction is independent of
δ; the three individual masses depend on δ through the cosine structure.

## Retained inputs (strict Cl(3)/Z³ consequences)

### R1. Circulant Hermitian form on a C_3[111] orbit (axiom-clean)

On the retained hw=1 triplet `T_1 = span{X_1, X_2, X_3}`, the cyclic permutation
`C_3[111] : X_i → X_{i+1 mod 3}` acts by conjugation on `M_3(ℂ)`. Any Hermitian
operator that commutes with this action has the **circulant matrix form**:
```
H = a·I + b·C + b̄·C²          a ∈ ℝ,  b ∈ ℂ
```
where `C` is the cyclic shift matrix. This is **pure character theory**: it
follows directly from `C_3` representation theory applied to the 9-dimensional
Hermitian algebra `M_3(ℂ)_Herm`, which decomposes under C_3 conjugation as
`3·trivial ⊕ 3·ω ⊕ 3·ω̄`. The trivial-isotypic Hermitian subalgebra is exactly
the circulants.

**Axiom status:** strict consequence of Cl(3)/Z³ + C_3[111] retained cyclic structure.

### R2. Circulant eigenvalue spectrum (axiom-clean)

The eigenvalues of `H = a·I + b·C + b̄·C²`, obtained by diagonalization in the
Fourier basis:
```
λ_k = a + 2|b| cos(arg(b) + 2πk/3)          k ∈ {0, 1, 2}
```
This is the Brannen/Rivero spectral form with the identifications
```
v_0 = a,       arg(b) = δ,       2|b| = (coefficient of cosine)
```

**Axiom status:** strict consequence of R1 via standard diagonalization.

## One structural assumption

### A1. Frobenius-norm equipartition of trivial : nontrivial sectors (3 : 6)

In the 9-dim `M_3(ℂ)_Herm`, the circulant matrix `H` has Frobenius norm
```
‖H‖² = 3a² + 6|b|²
```
counting the 3 diagonal entries (each contributing `a²`) and 6 off-diagonal
entries (each contributing `|b|²`).

**Assumption:** these two sectors contribute equally:
```
3a² = 6|b|²    ⟹    |b| = a/√2    ⟹    2|b| = √2 · a
```

This fixes the **√2 coefficient** in the Brannen/Rivero form:
```
λ_k = a (1 + √2 cos(δ + 2πk/3))
```

**Justification candidates (none fully axiom-derived):**
- Random-matrix measure with uniform entry distribution
- Gaussian ensemble equipartitioning energy between matrix modes
- Second-order phase-transition critical-point equipartition (analogous to
  classical equipartition per degree of freedom)
- Schur orthogonality between irrep sectors of C_3 on `M_3(ℂ)`

**This assumption is the one load-bearing non-axiom step.** It is the
magnitude-squared selection step of this candidate lane. It is NOT retained as a
theorem on the current surface.

## Exact bridge to the April 17 Koide package

Let `λ = (λ_0, λ_1, λ_2)` be the eigenvalue triple of the circulant Hermitian
```
H = a·I + b·C + b̄·C²,
```
and let `ω = e^{2πi/3}`. Then
```
λ_k = a + b ω^k + b̄ ω^{-k}.
```
Taking the `C_3` character decomposition of the triple `λ` itself gives
```
a_0 = (λ_0 + λ_1 + λ_2) / √3 = √3 · a,
z   = (λ_0 + ω̄ λ_1 + ω λ_2) / √3 = √3 · b.
```
Therefore
```
a_0² = 2 |z|²    ⟺    3a² = 6|b|².
```

So `A1` is **not** a new independent primitive relative to the April 17 Koide
package. It is the operator-space lift of the same equal-character-weight
condition already isolated in Theorem 1 of
`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`, now applied to the
circulant eigenvalue triple. The genuine open question is the **selection
principle** for this equality, not the algebraic bridge itself. On the current
science stack, the sharpest named candidate selection principle remains the
real-irrep-block-democracy lane of `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`.
Written in operator-space block energies
`E_+ = 3a²`, `E_⊥ = 6|b|²`, `A1` is exactly the same candidate principle in a
different coordinate system.

## One open identification problem

### P1. Spectral eigenvalues correspond to √m, not m

The circulant form gives eigenvalues `λ_k`. Identifying these with the
**square-roots of charged-lepton masses**:
```
λ_k = √m_k
```
reproduces observed charged-lepton masses to sub-percent precision at
`δ = 2/9 rad` (see §"Verification"). An alternative identification `λ_k = m_k`
would NOT give Koide `Q = 2/3`.

**Status:** This identification is outside audit-ratified tier today, but it is no longer a
free phenomenological guess. The new
`KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md` narrows it to a concrete
internal route: derive a positive quadratic parent operator `M` on the Koide
lane whose principal square root `M^(1/2)` is the circulant amplitude operator.
Then `eig(M^(1/2)) = √eig(M)` gives `λ_k = √m_k` automatically. The new
obstruction note sharpens the remaining gap: a nontrivial positive
`C_3[111]` parent lives in the eigenvalue/Fourier channel, while the current
retained charged-lepton readout is axis-diagonal (`U_e = I_3`). So the live
problem is now the parent **plus** the readout primitive, not the square-root
functional calculus itself.
Possible structural routes:
- Dirac spinor normalization (fermion wave functions have `√m` character)
- LSZ-style one-leg amplitude readout from a positive quadratic parent
- principal positive square root of a `C_3[111]`-covariant parent mass operator
- second-order return theorem: hw=1 intermediate-space matrix elements are
  quadratic, so physical linear amplitudes naturally arise on the square-root
  branch

## Koide Q = 2/3 as algebraic consequence

Given R1 + R2 + A1 + P1, and using the standard cosine identities for
third-roots-of-unity:

```
Σ_k cos(δ + 2πk/3) = 0                    (zero-sum of 3rd roots of unity)
Σ_k cos²(δ + 2πk/3) = 3/2                  (standard identity)
```

Then:
```
Σ_k √m_k = Σ_k v_0 (1 + √2 cos(θ_k))
        = 3 v_0 + √2 · 0
        = 3 v_0

Σ_k m_k = v_0² Σ_k (1 + √2 cos(θ_k))²
       = v_0² [3 + 2√2 Σ cos + 2 Σ cos²]
       = v_0² [3 + 0 + 2 · 3/2]
       = 6 v_0²

Q = (Σ m_k) / (Σ √m_k)² = 6 v_0² / 9 v_0² = 2/3
```

**Q = 2/3 is an exact algebraic consequence, independent of δ.**

## Numerical verification against PDG (2024)

**Input:** PDG pole masses
- `m_e = 0.5109989 MeV`
- `m_μ = 105.6583745 MeV`
- `m_τ = 1776.86 MeV`

**Compute:**
- `√m_e = 0.71484 √MeV`
- `√m_μ = 10.27903 √MeV`
- `√m_τ = 42.15282 √MeV`
- `v_0 = (√m_e + √m_μ + √m_τ) / 3 = 17.71556 √MeV`

**Predict from Brannen/Rivero at δ = 2/9:**

| k | `δ + 2πk/3` (rad) | `cos(·)` | `1 + √2 cos(·)` | `v_0 × (·)` (√MeV) | Assign to |
|---|---|---|---|---|---|
| 0 | 0.22222 | +0.97541 | 2.37937 | 42.1531 | τ |
| 1 | 2.31662 | −0.67858 | 0.04038 | 0.7154 | e |
| 2 | 4.41101 | −0.29684 | 0.58022 | 10.2770 | μ |

**Residuals against PDG √m:**
- τ: +0.001% (42.1531 vs 42.15282)
- e: +0.08%  (0.7154 vs 0.71484) — *agent prior residual estimate 0.003% was tight; recomputation here gives 0.08%, still sub-percent*
- μ: −0.02% (10.2770 vs 10.27903)

**Koide Q from these predictions:** exact 2/3 by construction (independent of δ).

**Best-fit δ from PDG:** 0.22227 rad (vs 2/9 = 0.22222). Difference 5×10⁻⁵ rad.

## What remains OPEN

### O1. Derivation of δ = 2/9 rad

No axiom-level mechanism for the specific value `δ ≈ 2/9 rad` has been
identified. Candidate derivations tested:
- `2/dim(M_3(ℂ)_Herm) = 2/9` — dimensional ratio, but interpreting as radians
  requires justification
- `2 arctan(1/9) = 0.22131` — 0.41% from 2/9, no framework provenance
- `π/14 = 0.22440` — 0.98% off, no framework provenance
- Temporal phase (APBC, Matsubara, winding) — all give π or 2π/n phases, not 2/9
- `δ = π/12 (critical angle)` — gives massless electron; observed δ = 2/9 sits
  just below this by 0.04 rad

### O2. Scale v_0

The overall scale `v_0 = 17.72 √MeV` determines absolute masses given the
ratios. No retained derivation of this scale is currently known on the charged-
lepton lane. The hierarchy theorem retains
`v = M_Pl × (7/8)^(1/4) × α_LM^{16}`, but that does **not** by itself supply an
independent lepton-sector first-power `(7/8)` factor, and reusing `(7/8)` in
that way would risk double-counting. So the present `v_0` story is still a
heuristic near-match problem, not a framework-correct closure.

### O3. Selection principle for the equal-character-weight / A1 condition

The exact bridge above shows that `A1` is the matrix-space form of the
equal-character-weight condition `a_0² = 2|z|²`. What remains open is not the
algebraic equivalence, but the charged-lepton-specific mechanism that selects
it. Candidates listed above remain non-retained. The current sharpest named
selection principle is still the April 17 real-irrep-block-democracy primitive.

### O4. Derive the positive parent behind the `√m` amplitude readout

The square-root map itself is now structurally narrowed: the repo already uses
it when passing from quadratic parents to one-leg amplitudes. The live question
is which positive `C_3[111]`-covariant parent operator `M` on the charged-lepton
lane has principal square root `M^(1/2)` equal to the candidate circulant
amplitude operator, **and** what retained readout makes that nontrivial
eigenvalue channel physical despite the current `U_e = I_3` axis readout.

The constructive target is now smaller than a generic `Herm(3)` reconstruction:
the Koide lane needs only the `3`-real `C_3[111]`-covariant Hermitian family
`a I + b C + b* C²`, and Koide itself cuts that to a `2`-real scale-plus-phase
subfamily. So the next positive attack is not "derive an arbitrary charged
Hermitian block", but "derive the microscopic source law for the cyclic
`3`-response Wilson descendant, then the single selector equation landing it on
the Koide cone." See
[KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md)
and
[KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md).
For the ranked positive-path map, with fresh axiom-only routes placed ahead of
transplant routes, see
`KOIDE_POSITIVE_PATHS_FIRST_PRINCIPLES_NOTE_2026-04-18.md` (positive-paths
hub aggregator; backticked to avoid 5+ length-N cycles through the koide
cluster — citation graph direction is *positive_paths_hub →
this_circulant_character* as a downstream reference, not vice versa).

## Relation to the current retained charged-lepton status

The current authoritative retained statement remains the April 17 charged-lepton
review:

- on the present retained surface, Koide is **structurally compatible** with the
  retained `hw=1` algebra;
- the framework does **not** yet derive Koide as a sole-axiom theorem output;
- charged-lepton closure remains a **bounded observational-pin package**.

This note does not supersede that result. It contributes a new exact
operator-space interpretation of the Brannen/Rivero ansatz and a cleaner
candidate extension route:

- `R1` and `R2` are exact retained statements;
- `A1` is the operator-space form of the same equal-character-weight condition
  already isolated in the April 17 package;
- `P1` is narrowed to the positive-parent / one-leg-amplitude construction;
- the scale / phase questions remain open.

So the science stack is:

- **retained now:** April 17 bounded charged-lepton package;
- **new here:** exact circulant/character bridge and sharper candidate extension
  language;
- **not retained yet:** any upgrade from bounded to derived.

## Proposed status classification

**CANDIDATE EXTENSION ROUTE — SCIENCE-CLEAN BUT NOT RETAINED**

This is a reduction of the charged-lepton mass-hierarchy problem, not a full
closure. The circulant form (R1, R2) is axiom-clean; the equipartition (A1)
and √m identification (P1) are structural assumptions requiring either
derivation or formal acceptance as retained primitives. Koide Q = 2/3 holds
exactly given R1+R2+A1+P1.

This is a proposal for a future retained extension route, not a correction to
the present charged-lepton framework state.

If a future retained extension supplies:
- a charged-lepton-specific selection principle for `A1`, and
- either a retained derivation or explicit primitive for `P1`,

then the current bounded status can be revisited on a clean science surface.

If the equipartition (A1) or √m identification (P1) are rejected:
- Koide remains a coincidence-class observation
- No change to bounded-package status

## Connection to Brannen/Rivero phenomenology

This derivation aligns with the Brannen (2006) + Rivero phenomenological
parametrization of charged-lepton masses (Gsponer/Rivero, hep-ph/0505220 and
subsequent work). Their circulant ansatz has been shown to fit PDG masses to
sub-10⁻⁵ precision at δ = 2/9 rad. This note provides a **character-theoretic
interpretation** of that ansatz as the natural Hermitian operator structure on
the retained C_3[111] orbit, and reduces Koide Q = 2/3 to an algebraic identity
of the cosine structure.

The Sumino (2009) family-gauge-symmetry derivation of Koide
(arXiv:0812.2090) provides a radiative-cancellation mechanism operating at
pole-mass vs running-mass scale. Our derivation is complementary: it's a
structural (not radiative) origin for Koide, valid at whichever scale the
circulant identification is made. Whether this is pole-mass scale (as in Sumino)
or hierarchy-theorem scale is a downstream question.

## Testable predictions / sharp questions

1. **Quark Koide extension.** Does the quark sector carry an analogous circulant
   structure under C_3[111] with a different δ? Literature notes (c,b,t) give
   `Q ≈ 0.67` at ~5% level. A framework-native prediction of the quark δ would
   be a sharp test.

2. **Neutrino Koide extension.** Brannen's neutrino conjecture uses `δ = 2/9 +
   π/12` in the circulant form and predicts neutrino mass ordering consistent
   with current oscillation data. Framework derivation of this complementary
   phase would further validate the structure.

3. **δ = 2/9 origin.** Any specific framework mechanism selecting this phase
   would close the remaining gap.

## File references

- Current retained-status authority: `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`
- Algebraic Koide cone equivalence: `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`
- Higher-order closure / real-irrep-block democracy: `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`
- Circulant/character bridge companion: `KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md`
- Generation-space theorem: `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- C_3[111] retained surface: `HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md`
- Literature: Brannen 2006 (unpublished notes); Rivero/Gsponer hep-ph/0505220;
  Koide 1981 PLB 120:161; Sumino arXiv:0812.2090 & 0903.3640;
  Xing/Zhang hep-ph/0602134 (running-vs-pole analysis);
  Kartavtsev arXiv:1111.0480 (multi-sector extensions).

---

# Appendix A: Follow-up agent verification (2026-04-18)

Four follow-up agents investigated the four open items (O1-O4). Arithmetic
verified independently. Results summarized below.

## A.1  v_0 scale HEURISTIC NEAR-MATCH (updates O2)

Using retained `v = 246.283 GeV` and `α_LM = 0.0907`, plus a **heuristic**
first-power reuse of the hierarchy APBC datum `(7/8)` as a lepton-sector
multiplier, the following identifications match observed values to <1%
precision:

```
m_τ       ≈ v × α_LM² × (7/8)              = 1.7729 GeV   vs 1.77686 GeV   (0.22% off)
Σ m_ℓ     ≈ v × α_LM² × √(7/8)             = 1.8953 GeV   vs 1.88303 GeV   (0.65% off)
v_0       ≈ √[v × α_LM² × (7/8)] / (1+√2 cos(2/9))  = 17.696 √MeV   vs 17.716 √MeV   (0.11% off)
```

**Step-by-step arithmetic (unit-labeled):**
- `α_LM² = 0.0907² = 0.008226` (dimensionless)
- `v × α_LM² = 246.283 GeV × 0.008226 = 2.0262 GeV`
- `v × α_LM² × (7/8) = 2.0262 × 0.875 = 1.7729 GeV` ✓
- Observed `m_τ = 1.77686 GeV`, residual `(1.7729 - 1.77686)/1.77686 = -0.22%` ✓

**Structural remark.** This appendix entry does **not** use only retained
framework constants in the strict sense. The cascade `v × α_LM² × (7/8)` uses
α_LM raised to integer power 2 (two additional cascade steps below the EW
hierarchy's `α_LM^{16}`), together with the APBC datum `(7/8)` raised to
integer power 1 (vs `(7/8)^{1/4}` in the EW hierarchy). This is **not**
currently a retained derivation: the hierarchy theorem retains
`(7/8)^(1/4)` for `v`, not an independent first-power `(7/8)` lepton-sector
factor, and
`docs/HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`
already warns that naïve first-power reuse is a double-count risk. The result
should therefore be read as a numerical clue only, not a framework-correct
closure. The sharpened structural question is whether there exists a
**non-double-counted** lepton-sector selector whose canonical value happens to
be `(7/8)^1`.

## A.2  δ = 2/9 rad — dimensional-ratio structural identity (updates O1)

Exhaustive search over geometric, topological, character-algebra,
temporal, and extremization candidates. Findings:

- **Berry phase on circulant moduli = 0** (eigenvectors δ-independent)
- **tr(H^n) extremization gives δ ∈ {0, π/3, 2π/3}**, NOT 2/9
- **APBC L_t=4 Matsubara phases mod 2π/3** give {π/4, π/12}, never 2/9
- **Character-algebra 2π/27** (= (2π/3)/9) gives 0.2327 rad — 4.7% off
- **π/12 critical angle** gives massless electron (wrong)
- **All other geometric/temporal candidates miss by ≥0.8%**

**The one surviving identity (exact):**
```
δ = 2/9 = (real DOF of b in b = |b| e^{iδ}) / (dim_ℝ M_3(ℂ)_Herm)
       = 2 / 9
       = 2 / |C_3|²
```
Numerically exact. Interpretation: δ is the ratio of the complex-phase
degree of freedom (2 real DOFs in b ∈ ℂ) to the total 9-dim Hermitian
algebra. **Required bridge:** a canonical identification of this
dimensionless ratio with radians. This unit bridge is not supplied by the
retained axiom set.

**Sector-universal structure suggestion.** Brannen's neutrino conjecture
uses `δ_ν = 2/9 + π/12`. If 2/9 is a universal structural ratio (common
to all fermion sectors via dim-ratio) and `π/12` is a sector offset
(interpretable as `(2π/3)/8` where 8 = dim Cl(3)), the burden reframes
to: derive 2/9 as common + π/12 as lepton-vs-neutrino offset. π/12 is
Cl(3)-native; 2/9 is the dim-ratio identity. Both pieces have structural
origins; the unit-bridge for δ still needs a derivation.

## A.3  Quark sector — NOT extensible with same ρ

Verified numerically:
```
Up-type: √m_t / v_0_up = 13.14 / 4.77 = 2.754
         Required cos θ = (2.754 - 1) / √2 = 1.240  → |cos| > 1, IMPOSSIBLE
Charged lepton: √m_τ / v_0_lep = 42.15 / 17.72 = 2.379
                Just below 1 + √2 = 2.414 envelope (98.5% of ceiling)
```

**The √2 equipartition (ρ = 2|b|/a = √2) caps eigenvalue ratio at 1 + √2 ≈
2.414**. Top quark overshoots (2.754); bottom quark overshoots (2.536);
charged-lepton tau JUST fits (2.379, at 98.5% of the ceiling).

**Implication:** Koide Q = 2/3 is SECTOR-SPECIFIC, not universal.
Relaxing A1 (allowing sector-dependent ρ) gives:
- ρ_lep = √2 ≈ 1.414 (charged leptons near equipartition-critical)
- ρ_up ≈ 1.754 (up-type, color-modified)
- ρ_down ≈ 1.536 (down-type, color-modified)

The circulant eigenvalue structure (R1, R2) still holds for quarks, but
the equipartition assumption A1 is charged-lepton-specific. Literature's
"quark Koide at 5%" is partial cancellation near ρ=√2 for (c,b,t), not a
fundamental identity.

**This strengthens the charged-lepton story.** Tau sitting at 98.5% of
the equipartition envelope (nearly maximal) is a non-trivial structural
observation. The electron being just below the critical angle π/12
(small but nonzero mass) is the complementary boundary feature. Charged
leptons specifically fit between these two extremal structures — a
near-critical arrangement.

## A.4  √m vs m identification — narrowed to the positive-parent route (O4)

Systematic search of axiom-level operator interpretations found:

1. Natural Cl(3) operators (`Γ_i Γ_i = I`, `M(φ)² = |φ|² I`, the
   second-order return `Σ`) give **dimensionless or mass-1 eigenvalues**,
   not [mass]^{1/2}.
2. The Hermitian circulant `H = a·I + b·C + b̄·C²` has dimensionless
   eigenvalues unless `a, b` are imported with dimensions. The retained
   hierarchy theorem gives `v` in mass units, not `√mass`, so a parent
   operator is still needed.
3. The repo now supports a sharper internal route: if there exists a positive
   quadratic parent `M`, then the one-leg amplitude operator `M^(1/2)` carries
   eigenvalues `√m` exactly; this matches both the charged-lepton convention-B
   square-root readout and the LSZ square-root rule.
4. What is still missing is the charged-lepton-specific parent `M` itself, plus
   the retained readout primitive that escapes the current axis-diagonal
   obstruction.

**Verdict:** P1 is not retained yet, but it has narrowed from a generic
phenomenological guess to a concrete positive-parent / one-leg-amplitude
construction problem, now tightly coupled to the axis-vs-eigenvalue readout
obstruction.

## A.5  Updated status summary

| Piece | Updated status | Precision |
|---|---|---|
| R1 Circulant form on C_3 orbit | AXIOM-CLEAN | Exact |
| R2 Eigenvalue spectrum | AXIOM-CLEAN | Exact |
| A1 √2 equipartition | Charged-lepton-specific candidate principle; **not retained** | Exact if assumed |
| Koide Q = 2/3 | Conditional algebraic consequence of `R1+R2+A1+P1`; **not retained today** | Exact under those assumptions |
| **v_0 scale (O2)** | **HEURISTIC NEAR-MATCH ONLY** via `v × α_LM² × (7/8)`; **not a retained hierarchy input** | **0.22% on m_τ** |
| δ = 2/9 rad (O1) | PARTIAL: `δ = 2/dim(Herm_3)` exact; needs rad-unit bridge | Exact ratio, bridge open |
| Quark Koide extension | CHARGED-LEPTON-SPECIFIC (Q=2/3 not universal) | n/a |
| √m identification (P1) | **OPEN, narrowed** to positive-parent plus readout-primitive route | candidate internal construction |

## A.6  Remaining gaps — narrowed from 4 to 3

After follow-up verification, this candidate-extension note still leaves THREE
genuinely open structural questions, each more tractable than the original
three-mass-hierarchy problem:

1. **Derive a non-double-counted lepton-sector scale selector.** The
   numerical near-match `v × α_LM² × (7/8)` is interesting, but the
   first-power `(7/8)` factor is not retained today. The sharp question is
   whether a genuine lepton-sector selector produces that same value without
   reusing the hierarchy datum illegitimately.

2. **Find the charged-lepton selection principle for the equal-character-weight
   / A1 condition.** The exact bridge now identifies `A1` as the matrix-space
   form of the April 17 Koide condition. The open science is the mechanism that
   selects it, not the bridge itself.

3. **Derive the positive parent and readout primitive behind the `√m` amplitude
   operator.** The square-root functional calculus and one-leg amplitude logic
   are now clean. The missing science is the charged-lepton-specific positive
   parent `M` together with a retained route from its nontrivial eigenvalue
   channel to physical charged-lepton masses. Constructively, the cyclic
   `3`-response descendant law is now explicit; what remains is the microscopic
   source law for those three responses together with the one extra real
   selector equation inside that smaller family.

**Net reduction:** The three-mass problem reduces from "derive three
free parameters" to "derive one lepton-sector scale selector, one
selection principle for equal-character-weight / `A1`, and one positive-parent
plus readout construction behind the `√m` amplitude operator." Each is a more
tractable structural question.

## A.7  The near-critical structural picture

Follow-up scouting surfaced a suggestive combined observation worth
flagging:

- **Tau sits at 98.5% of the equipartition envelope** (|cos| ceiling)
- **Electron sits just below the critical massless angle π/12** (|cos| bound)

Charged leptons occupy the near-critical region of the circulant
parameter space — near-maximal AND near-massless boundary features
simultaneously. This is arguably why Koide Q = 2/3 holds exactly here
and fails in other sectors: the equipartition value ρ=√2 is the
boundary between "top-quark-like overshoot" (ρ > √2) and
"uniform-degenerate" (ρ < √2), and charged leptons sit precisely on it.

If a framework mechanism (e.g., renormalization-group fixed point, or
EWSB-critical-surface) drives charged-lepton dynamics to ρ=√2 while
color dynamics push quark sectors to ρ > √2, Koide becomes a
charged-lepton-specific critical-point prediction. This aligns with the
Sumino family-gauge-cancellation picture — different mechanism, same
critical-point story.
