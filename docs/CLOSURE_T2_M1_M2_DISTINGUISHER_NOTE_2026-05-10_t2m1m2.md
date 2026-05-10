# Closure — T2 M1 vs M2 Distinguishing Observable Search

**Date:** 2026-05-10
**Type:** closure (distinguishing-observable analysis between two
saddle-equivalent candidate primitives M1 (multiplicity-counting
Frobenius-block log-functional) and M2 (isotype-reduced action
integral) for closing BAE algebraically)
**Claim type:** source-note proposal (audit-lane distinguishing-observable analysis)
**Scope:** Single-PR source-note. Extends PR #1049 (M1/M2 BOUNDED
duality) by searching for a *distinguishing observable* that elects
M1 vs M2, given PR #1049 proved them saddle-equivalent for BAE-closure
but fluctuation-distinct (Hessian factor 2). This note asks: is there
any PDG-comparable observable that picks out M1 or M2?
**Status:** source-note proposal. No primitive promoted. Pipeline-
derived status set only after independent audit-lane review.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Primary runner:** [`scripts/cl3_closure_t2_m1m2_distinguisher_2026_05_10_t2m1m2.py`](../scripts/cl3_closure_t2_m1m2_distinguisher_2026_05_10_t2m1m2.py)
**Cache:** [`logs/runner-cache/cl3_closure_t2_m1m2_distinguisher_2026_05_10_t2m1m2.txt`](../logs/runner-cache/cl3_closure_t2_m1m2_distinguisher_2026_05_10_t2m1m2.txt)

## Authority disclaimer

This is a source-note proposal that extends the M1/M2 BOUNDED-DUALITY
analysis from PR #1049 (PRIMITIVE_P_BAE_M1_M2_DUALITY) by searching
for a *distinguishing* observable. It does NOT introduce new primitives.
It does NOT modify retained content. It does NOT load-bear PDG. The
analysis is fully a *derivation* on top of PR #1049 plus minimal
axioms A1, A2 and retained Frobenius / isotype structure.

Pipeline-derived status is generated only after the independent audit
lane reviews. The `claim_type`, scope, and election recommendation
(if any) are author-proposed; the audit lane has full authority to
reject, retag, or modify the verdict.

## Recap of the question (from PR #1049)

PR #1049 proved that **M1 ≡ M2 at the saddle** (both force
`|b|²/a² = 1/2 = BAE`) but **M1 ≠ M2 at the fluctuation level**:

| Aspect | M1 | M2 |
|---|---|---|
| Action on constraint | `log E_+ + log E_⊥` | `(1/2)(log E_+ + log E_⊥)` (Lagrangian) |
| Saddle | `|b|²/a² = 1/2 = BAE` | `|b|²/a² = 1/2 = BAE` |
| Hessian at saddle | `diag(-12, -24)` | `diag(-6, -12)` = M1/2 |
| Gaussian width ratio | `σ_M2/σ_M1 = √2` |
| Induced measure on `x = E_+/N` | `x(1-x) = Beta(2, 2)` | `√(x(1-x)) = Beta(3/2, 3/2)` |

The audit lane therefore cannot elect M1 vs M2 *purely from BAE-saddle
behavior* — both give Q = 2/3 identically. **This note asks:** is there
any further observable — at fluctuation level or beyond — that
discriminates between M1 and M2 against the PDG benchmark?

## Result preview

**VERDICT: NO PDG-DISCRIMINATING OBSERVABLE EXISTS in current scope.**

The factor-2 Hessian distinction is HOMOGENEOUS across all
Gaussian-level observables — it scales every variance, every
susceptibility, and every one-loop correction by the same factor 2.
This makes the M1 ↔ M2 distinction **observationally degenerate with
a rescaling of an overall BAE coupling constant** (or "temperature"
β_M1 = 2 β_M2).

However, the **induced probability measures on the BAE constraint
surface are GENUINELY DISTINCT** (Beta(2,2) vs Beta(3/2, 3/2)):
their dimensionless higher cumulants differ in a way that
**cannot** be absorbed into rescaling. We catalogue these:

| Observable | M1 (Beta(2,2)) | M2 (Beta(3/2, 3/2)) | Ratio / diff | Type |
|---|---|---|---|---|
| Mean of `x = E_+/N` | 1/2 | 1/2 | identical | saddle |
| Variance of `x` | 1/20 | 1/16 | 4/5 (ratio) | scale |
| Skewness of `x` | 0 | 0 | identical | symmetry |
| Excess kurtosis of `x` | -6/7 | -1 | 1/7 (diff) | **DIMENSIONLESS** |
| `⟨x²⟩/⟨x⟩²` | 6/5 | 5/4 | 1/20 (diff) | **DIMENSIONLESS** |
| Partition function `Z` | 1/6 | π/8 | ratio | absolute |
| Free energy `F = -log Z` | log 6 | log(8/π) | 0.857... | absolute |
| KL(M1 ‖ M2) | — | — | 0.0237 | divergence |
| Symmetric KL | — | — | 0.0265 | divergence |

The excess kurtosis difference `Δkurt = 1/7 = 0.1429` and the ratio
`⟨x²⟩/⟨x⟩²` difference `1/20 = 0.05` are **clean dimensionless
discriminators** at the full-measure level.

**BUT:** these discriminators require **multiple independent
realizations** of the BAE configuration (samples from the induced
measure) to be tested. In the framework's current scope, our universe
provides **one** Koide measurement. Single-draw statistics cannot
distinguish two distributions whose modes coincide.

**Honest conclusion:**

- At PDG saddle level: M1 ≡ M2 (no discrimination possible).
- At PDG Gaussian fluctuation level: distinction is degenerate with
  rescaling of an undetermined overall scale.
- At full-measure level: M1 and M2 are *genuinely distinct* Beta
  distributions, but the distinction is **observationally
  inaccessible** with one Koide sample.

The audit lane therefore has **two equally-defensible elections**:
- **Elect M1** (Beta(2,2), tighter Gaussian, weight per real
  irreducible block of `Rep_ℝ(C_3)`, anchored in Etingof-Nikshych-
  Ostrik fusion-category theory).
- **Elect M2** (Beta(3/2, 3/2), broader Gaussian, weight per
  amplitude coordinate, anchored in Marsden-Weinstein-Meyer
  symplectic reduction).

**Both choices give the same predictions for every saddle-level PDG
observable.** The election is a **gauge / formalism choice**, not an
empirical question with current data.

## Method summary

1. **Catalog candidate distinguishing observables.** Enumerate every
   observable type that could in principle distinguish M1 from M2:
   - Saddle-level: Q, mass ratios, mode of induced measure.
   - Gaussian-level: variance, susceptibility, one-loop correction.
   - Full-measure: higher cumulants, partition function, KL divergence.
2. **Identify the homogeneous-rescaling degeneracy.** Show that all
   Gaussian-level observables differ by factor 2 between M1 and M2,
   and that this factor 2 can be absorbed into a redefinition of an
   overall scale β_M (so M1 = M2 with β doubled). Hence Gaussian-level
   observables cannot discriminate without independent calibration of β.
3. **Identify the FULL-MEASURE genuine distinction.** Show that the
   induced measures are Beta(2,2) vs Beta(3/2, 3/2) — genuinely distinct
   distributions whose dimensionless higher cumulants differ.
4. **Quantify the dimensionless discriminators.** Excess kurtosis
   difference 1/7; `⟨x²⟩/⟨x⟩²` difference 1/20.
5. **Identify observability constraint.** Single-realization framework
   cannot test variance/kurtosis without identifying a multi-realization
   observable.
6. **Honest election:** with no PDG discrimination available, the audit
   lane has two equally-defensible options.

## Detailed analysis

### 1. Catalog of candidate distinguishing observables

| Class | Observable | M1 prediction | M2 prediction | Discriminating? |
|---|---|---|---|---|
| Saddle | Koide Q | 2/3 | 2/3 | NO (identical) |
| Saddle | `|b|²/a²` | 1/2 | 1/2 | NO (identical) |
| Saddle | Mass ratios m_e/m_μ, m_μ/m_τ | free (fit) | free (fit) | NO |
| Saddle | Mode of `x = E_+/N` | 1/2 | 1/2 | NO |
| Gaussian | Variance of x | 1/20 | 1/16 | RATIO ONLY |
| Gaussian | Variance of Q (saddle expansion) | `σ²_M1` | `2 σ²_M1` | RATIO ONLY |
| Gaussian | Susceptibility χ_Q | `1/12` (a-direction) | `1/6` | RATIO ONLY |
| Gaussian | One-loop ⟨Q⟩ correction | `δ_M1` | `2 δ_M1` | RATIO ONLY |
| Full-measure | Excess kurtosis of x | -6/7 | -1 | **YES** (diff 1/7) |
| Full-measure | `⟨x²⟩/⟨x⟩²` | 6/5 | 5/4 | **YES** (diff 1/20) |
| Full-measure | Partition function Z | 1/6 | π/8 | YES (absolute) |
| Full-measure | KL(M1 ‖ M2) | — | — | 0.024 |

**Conclusion**: only the FULL-MEASURE dimensionless higher cumulants
genuinely discriminate.

### 2. Homogeneous-rescaling degeneracy at Gaussian level

The M1 action and M2 action are related by

> `S_M1 = 2 S_M2 + (constant terms)`

(specifically: `L_M1 = log E_+ + log E_⊥ = 2 · (1/2)(log E_+ + log E_⊥) =
-2 S_M2`, up to the Lagrange-multiplier term in M2 which is constant on
the constraint surface).

This means the M1 ↔ M2 transformation is **EXACTLY** a doubling of the
action: `S_M1 = 2 S_M2`. In statistical-mechanics language, M1 is M2 at
**half the temperature** (or twice the inverse-temperature β).

**All thermodynamic / fluctuation observables scale homogeneously
under β → 2β:**
- Variance of any observable: `σ² ∝ 1/β` → `σ²_M1 = σ²_M2 / 2`. ✓
  (Equivalent to M2 var = 2 × M1 var.)
- Susceptibility `χ = -∂⟨O⟩/∂h`: scales as `1/β` → factor 2.
- One-loop ⟨O⟩ correction: scales as `1/β` → factor 2.
- Free energy difference `ΔF = -log(Z_1/Z_2)`: scales as `1/β`.

Therefore: **all single-observable Gaussian-level distinctions are
degenerate with the choice of overall scale (β)**. Without independent
calibration of β, M1 and M2 are observationally indistinguishable at
Gaussian order.

This is the precise sense in which PR #1049's "factor-2 Hessian"
distinction is BOUNDED.

### 3. The full-measure genuine distinction

The full induced measures on the constraint surface (parametrized by
`x := E_+/N ∈ (0, 1)`) are:

- **M1**: `p_M1(x) ∝ x(1-x)` → `Beta(2, 2)` distribution.
- **M2**: `p_M2(x) ∝ √(x(1-x))` → `Beta(3/2, 3/2)` distribution.

These are NOT related by any rescaling — they are different functional
forms. Both are symmetric about `x = 1/2`, both have mode at `x = 1/2`,
but they have different **shapes**.

Standard `Beta(α, α)` formulas give:

| Quantity | Beta(α, α) | M1 (α=2) | M2 (α=3/2) |
|---|---|---|---|
| Mean | 1/2 | 1/2 | 1/2 |
| Variance | `1/(4(2α+1))` | `1/20` | `1/16` |
| Skewness | 0 | 0 | 0 |
| Excess kurtosis | `-6/(2α+3)` | **-6/7** | **-1** |

The **excess kurtosis differs by `Δ = 1/7 ≈ 0.143`** — a clean
dimensionless discriminator.

The ratio `⟨x²⟩/⟨x⟩² = 2(α+1)/(2α+1)` gives M1 = 6/5, M2 = 5/4,
**differing by 1/20 = 0.05** — another clean dimensionless discriminator.

### 4. Beta-distribution identification and exact partition functions

By inspection:

> `p_M1(x) dx = (1/Z_M1) · x · (1-x) dx = Beta(α=2, β=2)`

with `Z_M1 = B(2,2) = Γ(2)Γ(2)/Γ(4) = 1/6`.

> `p_M2(x) dx = (1/Z_M2) · √(x(1-x)) dx = Beta(α=3/2, β=3/2)`

with `Z_M2 = B(3/2, 3/2) = Γ(3/2)Γ(3/2)/Γ(3) = π/8`.

(`Γ(3/2) = √π/2`, so `Γ(3/2)² = π/4`, and `Γ(3) = 2!  = 2`, giving
`B(3/2,3/2) = π/8`.)

So:
- `Z_M1 = 1/6 ≈ 0.1667`.
- `Z_M2 = π/8 ≈ 0.3927`.
- `Z_M1 / Z_M2 = 8/(6π) = 4/(3π) ≈ 0.4244`.

These are **distinct, exact, dimensionless** partition functions. The
"absolute partition function" is itself a discriminator at the level
of the entire ensemble.

### 5. KL divergence and information-theoretic distance

Distinct measures have nonzero KL divergence. We compute:

- `KL(M1 ‖ M2) ≈ 0.0237`
- `KL(M2 ‖ M1) ≈ 0.0292`
- Symmetric KL = `(KL_12 + KL_21)/2 ≈ 0.0265`

These are nonzero (within numerical precision of trapezoid integration
over 10⁵ points), confirming **M1 and M2 are NOT the same probability
measure**. They share mean (1/2), skewness (0), and the support (0,1),
but differ in shape.

### 6. Observability constraint in current framework scope

For the framework to *test* the M1 ↔ M2 distinction via PDG data, we
would need either:

**(a)** An independent calibration of the overall scale β (e.g., from
some other observable that pins β = 1 unambiguously). Then the factor-2
variance distinction at Gaussian level becomes testable.

**(b)** A way to **sample** the induced measure across multiple
"Koide realizations" — i.e., independent draws from `p_M1` or `p_M2`.
Then the kurtosis difference is testable directly.

In current framework scope: (a) is not available (β/temperature/coupling
is currently a free parameter at the BAE level), and (b) is not
available (our universe gives ONE charged-lepton Koide value).

Speculative possibilities (NOT load-bearing):

- **Running of Q with scale.** If BAE is pinned at some scale μ_BAE
  and QED/QCD running modifies Q at other scales, the SCATTER of Q
  values across scales encodes BAE-fluctuations. But this requires
  identifying μ_BAE, which is not currently retained.

- **Cross-sector Koide values.** The framework computes
  `Q_ℓ, Q_d, Q_u` (charged leptons, down quarks, up quarks). If all
  three are samples from the same Brannen-Koide BAE distribution at
  the appropriate sectoral coupling, their joint scatter could test
  Beta-distribution shape. But the cross-sector couplings (α_s, α_em)
  are independent admissions, so this is also degenerate with rescaling.

For the audit lane's purposes, the conclusion is: **the M1/M2 election
is currently a gauge / formalism choice**, not an empirical decision.

### 7. Election recommendation (author's view, audit overrides)

Given no PDG-discriminating observable exists in current scope, the
election should rest on **formalism preference**:

- **Elect M2** if the framework's natural language is
  *measure-theoretic* (path integrals, statistical mechanics,
  Faddeev-Popov gauge-fixing). The MWM anchor is canonical.
- **Elect M1** if the framework's natural language is
  *operator-algebraic* (trace states, fusion categories,
  Hermitian-circulant algebra). The ENO anchor is canonical.

Currently the framework uses both languages (e.g., A1 is algebra-level,
but BAE is measure-level). The author's slight preference is **M2** because:

1. M1's *literal* trace-state form is degenerate (= ordinary Tr),
   so M1 must be reinterpreted as a Frobenius-block log-functional —
   one step removed from the design-note formulation.
2. M2's measure form has a direct canonical derivation (MWM) without
   requiring reinterpretation.
3. M2 is the natural language of saddle-point methods used downstream.

But this is a slight preference, not a discriminating verdict.

## Hostile-review classification

Following PR #1049's hostile-review classification scheme:

| Aspect | M1 vs M2 distinguishable? | Verdict |
|---|---|---|
| Saddle observables (Q, ratios) | NO | identical |
| Variance / susceptibility (Gaussian) | RATIO ONLY | factor-2 (rescaling-degenerate) |
| Higher cumulants (full measure) | YES dimensionless | distinct Beta distributions |
| PDG comparison | NO at saddle, INACCESSIBLE at variance | not testable |
| Formalism canonical anchor | M1 ← ENO, M2 ← MWM | both canonical |
| Election based on PDG data | NO discriminator exists | gauge choice |

**OVERALL VERDICT: NO PDG-OBSERVABLE DISCRIMINATES M1 FROM M2.**

The distinction exists analytically (Beta(2,2) ≠ Beta(3/2, 3/2)) but
is observationally inaccessible at PDG-comparison level.

## What if the assumptions are wrong?

### What if there IS a multi-realization observable I'm missing?

The most plausible candidate is **running of Q with scale**. If BAE is
pinned at one specific scale (say `μ_BAE`) and QED/QCD running affects
the lepton masses at other scales, then `Q(μ_pole), Q(μ_MS(mZ))` are
DIFFERENT "samples" from the BAE distribution. The framework currently
does NOT identify `μ_BAE`, so this remains speculative. A future probe
could:
1. Identify `μ_BAE` (e.g., as the QCD/QED matching scale or a
   characteristic flavor-breaking scale).
2. Compute `Q(μ)` at several scales using SM RGE.
3. Test whether the scatter is consistent with M1 (var 1/20, kurt -6/7)
   or M2 (var 1/16, kurt -1) prediction.

But this requires a new primitive identification of `μ_BAE`.

### What if I'm wrong about the rescaling-degeneracy at Gaussian level?

The argument is: M1 action = 2 × M2 action on the constraint surface
(up to Lagrangian terms). All saddle-Laplace expansions of any observable
take the form `<O> = O(saddle) + (1/(2 β)) · trace(Hess⁻¹ · ∂²O) + ...`
where β = 1 implicitly. Under `β → 2β`, all corrections halve. So all
*relative* observable corrections under M1 are HALF those under M2.

The only way out: an observable whose `β`-dependence is anomalous. The
Beta-distribution kurtosis is one such — but as noted, it's not a
single-draw observable.

### What if there's a SYMMETRY argument that pins M1 or M2?

PR #1049 discusses:
- M1 ← Etingof-Nikshych-Ostrik fusion-category structure on `Rep_ℝ(C_3)`
- M2 ← Marsden-Weinstein-Meyer symplectic reduction with U(1)_b gauge

Both are canonical mathematically. Neither has been derived from A1+A2
alone — both depend on a CHOICE (real-vs-complex FP dimension for M1;
gauging U(1)_b for M2). So neither structural argument is forced by
retained content. Election depends on which choice the audit lane
finds more natural.

### What if higher-order Probes 12, 13, 16 already imply one of M1 or M2?

Probes 12, 13 identify the U(1)_b ambiguity — its gauging is what makes
M2 canonical. If U(1)_b is RETAINED as gauge symmetry (currently it is
algebra-level only), M2 becomes the canonical choice. If U(1)_b remains
algebra-level (no gauging), M1 is structurally favored.

This is consistent with the verdict: the M1 vs M2 election is currently
tied to the U(1)_b gauge-vs-algebra-level election, which is itself
unresolved at retained-tier level.

## Elon first-principles minimum

**What is the literal minimum content that distinguishes M1 from M2 in
an observable manner?**

The minimum content is the **shape of the induced probability
distribution** on the BAE constraint surface:
- M1 induces Beta(2,2).
- M2 induces Beta(3/2, 3/2).

These are objectively distinct distributions. The minimum
**dimensionless observable** that distinguishes them is the **excess
kurtosis** of `E_+/N`: M1 → -6/7, M2 → -1.

The minimum **physical scenario** where this would be testable: any
context where MULTIPLE samples from the BAE distribution can be
observed (e.g., multi-scale Q values, multi-sector Q values calibrated
to one Koide-style coupling).

In current framework scope: no such scenario exists. Hence the M1/M2
election is a gauge choice.

## Compatibility with A1 + A2 + retained

This distinguisher analysis is compatible with all retained content:

- **A1 (Cl(3) local algebra)**: no new algebra.
- **A2 (Z³ lattice)**: no spatial structure modified.
- **Retained Frobenius isotype-split uniqueness**: respected.
- **Retained Q-readout factorization**: Q used as test observable.
- **PR #1049 (M1/M2 BOUNDED duality)**: this note extends, doesn't
  modify.

## Distinctness from prior probes and PR #1049

This note's contribution is distinct from PR #1049 (which identified
the BOUNDED duality) in that it specifically:

1. **Catalogs** every candidate discriminating observable (saddle,
   Gaussian, full-measure).
2. **Proves the homogeneous-rescaling degeneracy** at Gaussian level
   (M1 = M2 at half temperature, all variances scale by 2).
3. **Identifies the induced measures as exact Beta distributions**
   (Beta(2,2) and Beta(3/2,3/2)) with exact partition functions.
4. **Quantifies dimensionless full-measure discriminators**
   (Δkurt = 1/7, Δ⟨x²⟩/⟨x⟩² = 1/20).
5. **Computes KL divergence** between M1 and M2 induced measures.
6. **Concludes observability**: no PDG-comparable discriminator exists
   in current framework scope.

This is a *negative finding* analogous to past bounded-obstruction
notes — it BOUNDS what PDG data can tell us about the M1/M2 election.

## Honest assessment

**What this proposal contributes:**

1. **Catalog of candidate distinguishers** at three levels (saddle,
   Gaussian, full-measure).
2. **Proof of homogeneous-rescaling degeneracy** at Gaussian level
   (M1 = M2 up to β → 2β).
3. **Exact identification** of induced measures as Beta(2,2) and
   Beta(3/2, 3/2).
4. **Exact partition functions** Z_M1 = 1/6, Z_M2 = π/8.
5. **Exact dimensionless discriminators**: Δkurt = 1/7,
   Δ⟨x²⟩/⟨x⟩² = 1/20.
6. **Numerical KL divergence**: 0.0237 and 0.0292.
7. **Honest verdict**: no PDG discriminator exists in current scope.

**What this proposal does NOT do:**

1. Does NOT elect M1 or M2 as the canonical primitive (audit lane
   decides; author offers slight M2 preference based on formalism
   directness).
2. Does NOT close BAE (PR #1049 + PR #1039 already do, at saddle).
3. Does NOT introduce new axioms.
4. Does NOT modify retained content.
5. Does NOT load-bear PDG (Koide Q at PDG precision matches 2/3 to
   `6 × 10⁻⁶`, far below both Gaussian widths — saddle dominates).
6. Does NOT propose a SPECIFIC multi-realization observable that
   would discriminate (this is left as a future probe direction).

**What the audit lane should consider:**

1. Whether the homogeneous-rescaling-degeneracy argument is correct.
2. Whether the Beta(2,2) vs Beta(3/2, 3/2) identification is correct.
3. Whether election can be deferred (or whether one must be elected
   for downstream use).
4. Whether the speculative running-Q-with-scale or cross-sector-Q
   directions are worth pursuing in future probes.
5. Whether M2 should be elected (canonical MWM measure, direct
   formalism) absent any other discriminator.

## Cross-references

### Direct dependency (PR #1049 BOUNDED-DUALITY)

- M1/M2 duality note: [`PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md`](PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md)
  (the BOUNDED-DUALITY proof — the starting point for this note's
  distinguishing-observable search).

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- BAE rename meta: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

### Retained C_3 / circulant / isotype structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### U(1)_b gauge / algebra-level probes (relevant to M2 canonical choice)

- Probe 12 (Plancherel / Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)

### Literature anchors (external)

- **Beta distribution moments**: standard reference — see, e.g.,
  Johnson, Kotz & Balakrishnan, *Continuous Univariate Distributions*,
  Vol. 2 (Wiley, 1995), Ch. 25. Variance of Beta(α, α) = 1/(4(2α+1));
  excess kurtosis = -6/(2α+3). Both derived from
  `B(α+n, α) / B(α, α)` moment formula.
- **Symplectic reduction (MWM)** (M2 anchor — see PR #1049): Hoskins;
  Tran; Marsden, *Lectures on Mechanics* (1992).
- **Fusion categories / Frobenius-Perron dimension (ENO)** (M1 anchor —
  see PR #1049): Etingof, Nikshych, Ostrik, *On Fusion Categories*,
  Annals of Mathematics 162 (2005) 581-642.
- **Laplace / saddle-point method** (basis for the Gaussian-level
  analysis): Wikipedia, "Method of steepest descent"; Edinburgh Lecture 5.
- **Kullback-Leibler divergence**: standard reference — Cover & Thomas,
  *Elements of Information Theory* (Wiley, 2006), Ch. 2.

## Validation

```bash
python3 scripts/cl3_closure_t2_m1m2_distinguisher_2026_05_10_t2m1m2.py
```

Expected: `=== TOTAL: PASS=N, FAIL=0 ===` for an N specified by the runner.

The runner verifies:

1. Section 0 — Retained input sanity (PR #1049 setup unchanged).
2. Section 1 — Saddle-level observables: Q = 2/3 identically for both
   M1 and M2 (PR #1049 result, recap).
3. Section 2 — Gaussian Hessian comparison: M1 = 2 × M2 (PR #1049
   recap), and statement of homogeneous-rescaling degeneracy.
4. Section 3 — Identification of induced measures as Beta(2, 2) and
   Beta(3/2, 3/2): exact PDFs and partition functions.
5. Section 4 — Exact moments via standard Beta(α, α) formulas:
   variance, skewness, excess kurtosis.
6. Section 5 — Dimensionless discriminators: Δkurt = 1/7,
   Δ⟨x²⟩/⟨x⟩² = 1/20.
7. Section 6 — KL divergence (M1‖M2) and (M2‖M1) nonzero.
8. Section 7 — Susceptibility / one-loop scaling: factor-2 homogeneity.
9. Section 8 — Verdict: no PDG-discriminating observable in current
   scope.
10. Section 9 — Does-not disclaimers and election recommendation.

## User-memory feedback rules respected

- `feedback_primitives_means_derivations.md`: this analysis is a
  *DERIVATION* on top of PR #1049 + retained, not a new axiom.
- `feedback_consistency_vs_derivation_below_w2.md`: the Beta-distribution
  identification, partition function, excess kurtosis formulas are
  algebraic derivations (Beta(α,α) moments are standard), not
  consistency equalities. KL divergence is numerical-integral-derived.
- `feedback_hostile_review_semantics.md`: explicit hostile-review
  search for ANY observable that discriminates; finding that all
  Gaussian-level distinctions are rescaling-degenerate, only
  full-measure higher cumulants give genuine discrimination.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This is a source-note proposal; the audit
  lane decides election.
- `feedback_review_loop_source_only_policy.md`: this note is a
  single source-note proposal + paired runner + cached output, no
  synthesis notes, no lane promotions.
- `feedback_special_forces_seven_agent_pattern.md`: the distinguisher
  attack uses 3 narrow angles (saddle / Gaussian / full-measure) on a
  single load-bearing question (does ANY observable distinguish M1
  from M2?), with sharp PASS/FAIL deliverables.
- `feedback_compute_speed_not_human_timelines.md`: scope expressed
  in computational content, not time estimates.
- `feedback_physics_loop_corollary_churn.md`: this is novel
  distinguishing-observable analysis with negative-finding verdict,
  not relabeling of PR #1049's BOUNDED-DUALITY result. Adds material
  (Beta-distribution identification, kurtosis discriminator,
  observability constraint) distinct from PR #1049.

## Audit dependency repair links

- [primitive_p_bae_m1_m2_duality_note_2026-05-10_pPbae_duality](PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md)
- [primitive_p_bae_multiplicity_counting_proposal_note_2026-05-10_pPbae](PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md)
- [brannen_amplitude_equipartition_bae_rename_meta_note_2026-05-09](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
