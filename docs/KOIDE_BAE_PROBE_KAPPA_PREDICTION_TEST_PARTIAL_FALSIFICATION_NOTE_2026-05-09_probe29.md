# Koide BAE Probe 29 — κ Prediction Test: Partial Falsification of Charged-Lepton Sector (Bounded)

**Date:** 2026-05-09
**Type:** bounded_theorem (partial falsification of the charged-lepton
sector under cited source-stack content alone; κ-prediction test against empirical
κ ≈ 2)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 29 of the Koide
**BAE-condition** closure campaign. Tests what κ-value the framework's
cited source-stack content actually **predicts** for charged leptons, then compares
that prediction against the empirical observation (PDG charged-lepton
masses give κ ≈ 2 = BAE = Q = 2/3).
**Status:** source-note proposal for a **partial falsification** of the
framework's charged-lepton matter-sector prediction under retained
content alone. The framework's combined cited source-stack content (free Gaussian
on Herm_circ(3) + Plancherel-uniform on Ĉ_3 + spectrum-cone bridge
identity) gives a canonical κ-predictor functional `Φ_canonical` whose
extremum is κ = 1, NOT κ = 2 (BAE). Empirical PDG charged-lepton masses
give κ ≈ 2.000037. The framework's cited-source-stack κ-prediction
**disagrees** with the empirical observation by a factor 2 in κ. **This
is honest partial falsification of the framework's charged-lepton sector
under cited source-stack content alone.** No new admission is added; the BAE
admission count is UNCHANGED. The framework would need a multiplicity-
counting principle (not derivable from cited source-stack content per Probe 25)
as a SEPARATE PRIMITIVE to give κ = 2 = BAE.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** koide-bae-probe-kappa-prediction-test-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_kappa_prediction_test_2026_05_09_probe29.py`](../scripts/cl3_koide_bae_probe_kappa_prediction_test_2026_05_09_probe29.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_kappa_prediction_test_2026_05_09_probe29.txt`](../logs/runner-cache/cl3_koide_bae_probe_kappa_prediction_test_2026_05_09_probe29.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
partial-falsification classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md), **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

The 28-probe campaign through Probe 28 has explored every conceivable
cited-source-stack angle to **close** BAE — i.e., to derive κ = 2 from
A1+A2 plus retained derivations. Probe 25 in particular found that the
retained free Gaussian dynamics on Herm_circ(3) canonically gives F3
(real-dim weighting (1, 2)) and therefore κ = 1, NOT κ = 2.

This probe **inverts the framing**:

> Instead of asking "can cited source-stack content close BAE?", take the
> framework's cited source-stack content seriously as a **predictor** of κ, and
> test that prediction against the empirical observation κ ≈ 2.

Three honest outcomes were considered before running:

1. **CLOSURE**: framework predicts κ = 2 via specific cited-source-stack
   chain ⇒ BAE closes.
2. **PARTIAL FALSIFICATION**: framework predicts κ ≠ 2 ⇒ framework's
   charged-lepton sector is wrong or incomplete.
3. **AMBIGUOUS**: cited source-stack content does not pin κ uniquely.

## Answer

**Outcome (2): PARTIAL FALSIFICATION.** The framework's retained
content gives a unique canonical κ-predictor functional whose extremum
is κ = 1, NOT κ = 2 (= BAE = empirical PDG value).

The framework's free cited matter-sector dynamics on Herm_circ(3)
predicts κ = 1, which corresponds to the algebraic constraint
`a² = |b|²` on the (a, |b|)-plane. At this κ-value, the lambda triple
`λ_k = a + 2|b|cos(δ + 2πk/3)` for δ = 0 contains a NEGATIVE eigenvalue
`λ_min = a - 2|b| = -|b|`, which violates the sqrt-mass positivity
required for the Koide ratio to be well-defined; even with optimal δ,
the predicted lepton mass ratios are far from the empirical `m_μ/m_e ≈ 207,
m_τ/m_μ ≈ 16.8`.

**This is honest partial falsification of the framework's charged-lepton
sector under cited source-stack content alone.**

Closing BAE (and thus matching the charged-lepton sector empirically)
requires a **multiplicity-counting primitive** (the F1 = (μ, ν) = (1, 1)
weighting) that is **not derivable from cited Hamiltonian dynamics**
per Probe 25 (the Gaussian path-integral measure on Herm_circ(3) gives
real-dim counting (1, 2), not multiplicity counting (1, 1)).

**Verdict: PARTIAL FALSIFICATION of the charged-lepton sector under
cited source-stack content alone, with a single-clause characterization of the
admission needed for closure.** No new admission is added by this
probe; the BAE admission count is UNCHANGED.

## Setup

### Premises (A_min for Probe 29)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm`; §4 enumerates `(μ, ν)` log-laws | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is the unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | source dependency; see [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ κ = 2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Bridge | Cone slack = -9 × BAE slack; spectrum-cone is operator-side equivalent | source dependency; see [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md) |
| LR | Lieb-Robinson microcausality + finite-range r=1 matter Hamiltonian | source dependency; see [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| Probe25 | Retained Gaussian dynamics on Herm_circ(3) gives F3 (real-dim weighting); F1 structurally absent | source dependency; see [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) |
| Probe22 | Spectrum-cone pivot bridge-equivalent to operator-side BAE | source dependency; see [`KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md`](KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md) |
| Probe18 | F1 vs F3 algebraic ambiguity (F2 ruled out structurally) | source dependency; see [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) |
| Probe12 | Plancherel-uniform on `Ĉ_3` gives (1, 2) → F3 | source dependency; see [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) |
| Probe19 | Wilson chain `m_τ = M_Pl (7/8)^{1/4} u_0 α_LM^{18}` fixes mass scale | source dependency; see [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md) |
| Probe24 | φ_dimensionless = 2/9 from C_3 character algebra (n_eff/d² = 2/9) | source dependency; see [`KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md`](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md) |
| Probe26 | Wilson chain rescaling H → rH preserves κ (κ scale-invariant) | source dependency; see [`KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md`](KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md) |
| Probe21 | Native bilinear matter Hamiltonian: `S_native = α Tr(H_x²) + κ Tr(H_x H_y)` | source dependency; see [`KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input for KP-AV1
  through KP-AV7 (κ-derivation routes)
- PDG values appear ONLY in KP-AV8 as the empirical-test target of
  the derived κ-prediction
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are retained derivations only
- NO admitted SM Yukawa-coupling pattern as derivation input

## The framework's canonical κ-predictor functional

After Probe 25, the canonical retained-dynamics functional on the
(a, |b|)-plane is

```
Φ_canonical(a, |b|)  =  (1/2) [1 · log E_+  +  2 · log E_⊥]
                     =  (1/2) F3(a, |b|)
```

where `E_+ = 3a²` and `E_⊥ = 6|b|²`. The (1, 2) weighting is the
**real-dimension count** of the trivial and doublet isotypes,
structurally fixed by the retained Block-Total Frobenius isotype
decomposition.

The extremum of `Φ_canonical` on the constraint `E_+ + E_⊥ = N` lands
at

```
E_⊥ = 2N/3,  E_+ = N/3,  κ = a²/|b|² = (E_+/3) · (6/E_⊥) = 2 (N/3) / (2N/3) = 1.
```

**The framework's cited-source-stack κ-prediction is κ = 1.**

## Why this is a partial falsification

Empirically, charged-lepton masses satisfy Koide's relation
`Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² ≈ 2/3` to ~5 × 10⁻⁵
precision. By the retained
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
and [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md),
this is exactly equivalent (via the bridge identity
`a₀² - 2|z|² = 3(a² - 2|b|²)` with prefactor 3, and cone-slack
identity with prefactor -9) to operator-side `κ = 2`.

So:

| | κ value | Source |
|---|---|---|
| Empirical (PDG) | 2.000037 | Q = 2/3 + bridge identity |
| Framework prediction (cited source-stack content alone) | 1 | Probe 25 / Probe 29 |
| Discrepancy | 1 (factor 2 in κ) | this note |

At κ = 1, even with the optimal phase δ, the predicted charged-lepton
mass ratios are `m_μ/m_e ≈ 1.56, m_τ/m_μ ≈ 15.95`, far from the
empirical `(207, 16.8)` (log-score discrepancy ≈ 4.94). Moreover, at
δ = 0 the smallest sqrt-mass eigenvalue `λ_min = a - 2|b| = -|b|` is
**negative** at κ = 1, violating the sqrt-mass positivity required
for the Koide invariant to be well-defined.

**This is honest partial falsification of the framework's charged-
lepton sector under cited source-stack content alone.**

## Per-attack-vector verification

Nine attack vectors (KP-AV1 through KP-AV9) verify the κ = 1 prediction
from distinct cited-source-stack angles. All converge.

### KP-AV1 — Free Gaussian path-integral on Herm_circ(3)

**Status: gives κ = 1.**

Per Probe 25, the Gaussian path integral over Herm_circ(3) with the
retained bilinear matter Hamiltonian `S_native[H] = α Tr(H²) + …` has
log-functional-determinant

```
Φ_G  =  (1/2) (1 · log E_+ + 2 · log E_⊥)  =  (1/2) F3 + const.
```

Extremum at E_⊥ = 2N/3, κ = 1.

### KP-AV2 — Plancherel-uniform on Ĉ_3

**Status: gives κ = 1.**

Per Probe 12, the Plancherel-uniform state on the dual `Ĉ_3 =
{χ_0, χ_1, χ_2}` weights each character equally; restriction to
Herm_circ(3) gives weights `1` on the trivial isotype (1 character)
and `2` on the doublet isotype (2 characters χ_1, χ_2 = ω, ω̄). This
is the (1, 2) weighting → F3 → κ = 1.

### KP-AV3 — Spectrum-level cone (Probe 22 bridge)

**Status: gives κ = 1.**

Per Probe 22, the bridge identity makes spectrum-level cone
localization arithmetically equivalent to operator-level BAE. The
spectrum-level extremization functional reduces to the same (a, |b|)
extremum, with the same canonical cited dynamics → F3 → κ = 1.

### KP-AV4 — Wilson chain m_τ scale (κ-neutral)

**Status: κ-neutral.**

Per Probe 19 + Probe 26, the m_τ Wilson chain
`m_τ = M_Pl (7/8)^{1/4} u_0 α_LM^{18}` acts on H as a scalar rescaling
H → rH, preserving κ = a²/|b|². It pins the mass scale, not the
amplitude ratio.

### KP-AV5 — φ_dimensionless = 2/9 (κ-neutral)

**Status: κ-neutral.**

Per Probe 24, φ_dimensionless = n_eff/d² = 2/9 is a phase-readout
primitive from C_3 character algebra (n_eff = 2 from conjugate-pair
forcing, d = 3). The phase δ does NOT pin (a, |b|); different (a, |b|)
at the same φ give different κ.

### KP-AV6 — Combined cited-source-stack canonical functional

**Status: gives κ = 1.**

Combining KP-AV1 + KP-AV2 + KP-AV3 (κ-determining content) and
factoring out KP-AV4 + KP-AV5 (κ-neutral content), the unique
canonical κ-predictor functional is `Φ_canonical = (1/2) F3`. Its
extremum gives κ = 1.

### KP-AV7 — MRU image: only F1 (μ = ν) gives κ = 2

**Status: structural barrier.**

Per the MRU theorem, κ = 2μ/ν. The κ = 2 = BAE constraint requires
μ = ν, integer-minimal at (1, 1) = F1. F1 is the multiplicity-(1, 1)
weighting. Per Probe 25, F1 is **structurally absent** from retained
Gaussian dynamics: the doublet has real dim 2, and the Gaussian
measure integrates over both real DOFs, contributing weight 2 (not 1)
to the doublet log-functional.

### KP-AV8 — Falsification arrow vs PDG empirical

**Status: framework prediction κ = 1 disagrees with empirical κ ≈ 2.**

PDG charged-lepton masses give Q ≈ 2/3 to ~5 × 10⁻⁵, equivalently
κ ≈ 2.000037. The framework's cited-source-stack prediction κ = 1
disagrees by factor 2 in κ. At κ = 1 the predicted mass ratios are
far from empirical, and (at the canonical δ = 0) sqrt-mass positivity
is violated.

### KP-AV9 — Admission needed to close BAE

**Status: characterized as a single primitive.**

The framework would close BAE iff a **multiplicity-counting principle**
were admitted as a separate primitive: each real isotype contributes
weight 1 regardless of real dim. Equivalently: F1 is the canonical
retained Q-functional, not F3.

This admission is **not derivable from cited source-stack content** per Probe 25
(all retained Gaussian/heat-kernel/mode-counting routes give real-dim
weighting (1, 2), not multiplicity weighting (1, 1)). Closing BAE
therefore requires an external primitive.

## Theorem (Probe 29 partial falsification)

**Theorem.** On A1 + A2 + cited Hamiltonian dynamics + retained
Block-Total Frobenius + retained MRU + retained Frobenius Isotype
Split + retained Bridge Identity (Probe 22) + retained Probes 12, 18,
19, 21, 24, 25, 26:

```
(a) The unique canonical κ-predictor functional combining all retained
    matter-sector content on the (a, |b|)-plane is
        Φ_canonical(a, |b|)  =  (1/2) F3(a, |b|)
                              =  (1/2) [log E_+ + 2 log E_⊥]
    Mass-scale (Probes 19, 26) and phase (Probe 24) factors are
    κ-neutral and drop out.
    [Verified Sections 2-7.]

(b) Φ_canonical extremum on E_+ + E_⊥ = const gives κ = 1, NOT κ = 2.
    [Verified Sections 2, 7, 8, 11.]

(c) F1 = (μ, ν) = (1, 1) is the integer-minimal MRU generator giving
    κ = 2 = BAE; F1 is the multiplicity-(1, 1) weighting. F1 is
    structurally absent from retained Gaussian dynamics per Probe 25.
    [Verified Section 8.]

(d) Empirical PDG charged-lepton masses give Q ≈ 2/3, equivalently
    κ ≈ 2.000037, by the retained Charged-Lepton Cone Algebraic
    Equivalence + Bridge Identity.
    [Verified Section 9.1.]

(e) Framework prediction κ = 1 disagrees with empirical κ ≈ 2 by
    factor 2 in κ.
    [Combined (b) + (d); Section 9.2.]

(f) At κ = 1 (framework prediction), the implied charged-lepton mass
    ratios are far from empirical (log-score discrepancy ≈ 4.94 over
    optimal δ); at δ = 0, sqrt-mass positivity is violated.
    [Section 9.3, 9.4.]

(g) Closing BAE requires admitting a multiplicity-counting principle
    distinct from retained real-dim counting; this admission is not
    derivable from cited source-stack content per Probe 25.
    [Section 10.]

Therefore: the framework's cited source-stack content gives a unique κ-prediction
κ = 1, which disagrees with the empirical PDG value κ ≈ 2 by factor 2
in κ. This is honest partial falsification of the framework's
charged-lepton sector under cited source-stack content alone. No new admission
is added; the BAE admission count is UNCHANGED.
```

**Proof.** Each item is verified by the runner (57 PASS / 0 FAIL):
Section 0 (retained sanity); Section 1 (MRU formula κ = 2μ/ν);
Sections 2-6 (KP-AV1-AV5); Section 7 (KP-AV6 combined functional);
Section 8 (KP-AV7 MRU image structural barrier); Section 9 (KP-AV8
falsification arrow); Section 10 (KP-AV9 admission characterization);
Section 11 (verdict synthesis); Section 12 (does-not disclaimers);
Section 13 (comparison with prior probes). ∎

## Honest assessment

**The framework's cited source-stack content currently predicts the wrong
charged-lepton Koide ratio.**

Probes 1-26 attacked the BAE-closure problem from the closure side
("can cited source-stack content force κ = 2?"). The answer was uniformly
"no" — all routes either give κ = 1 (Probes 12, 25, this probe) or
are κ-neutral (Probes 19, 24, 26) or are bounded obstructions
(Probes 1-18, 20-23).

This probe inverts the framing: it takes the framework's retained
content **as a predictor** and tests against empirical observation.
The result:

1. **Framework prediction is unique**: combining all κ-determining
   cited source-stack content (free Gaussian dynamics, Plancherel state, spectrum
   bridge) gives a single canonical functional `Φ_canonical = (1/2) F3`.

2. **The prediction is κ = 1**: structural, not algebraic; locked by
   the (1, 2) real-dim count of the isotype decomposition.

3. **The prediction is wrong empirically**: PDG gives κ ≈ 2; framework
   gives κ = 1. Factor 2 discrepancy.

4. **Closing this requires a multiplicity-counting admission**: not
   derivable from cited source-stack content per Probe 25.

This is not a probe-failure or a hidden-residue technicality — it is
the honest assessment that **the framework's matter-sector retained
content, as currently stated, does not reproduce the empirical
charged-lepton Koide hierarchy**. Either:

- (a) An additional primitive (multiplicity-counting on the doublet)
  is admitted, closing BAE and matching empirical κ ≈ 2. The BAE
  admission count moves from 1 to 0; the multiplicity-counting
  admission is added.

- (b) The framework's charged-lepton-sector prediction κ = 1 stands,
  in which case the framework is **partially falsified** by the
  empirical observation κ ≈ 2.

Both options are explicit; the choice between them is a user/audit
decision. This probe documents the situation honestly without
attempting to obscure either option.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem`
- audit-derived effective status: set only by the independent audit lane after review, with
  scope-tag "partial falsification of charged-lepton sector under
  cited source-stack content alone"
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — UNCHANGED. The κ = 1 framework prediction is a
  derived consequence, not a new admission.

**No new admissions added by this probe. The BAE admission count is
UNCHANGED at 1.**

### What this probe DOES

1. Combines all κ-determining cited source-stack content (KP-AV1-AV3) into a
   single canonical κ-predictor functional `Φ_canonical = (1/2) F3`.
2. Computes the framework's κ-prediction = 1 from this functional's
   extremum.
3. Verifies that κ-neutral cited source-stack content (KP-AV4-AV5) does not
   shift the prediction.
4. Identifies the empirical κ ≈ 2 from PDG charged-lepton masses via
   the retained Bridge Identity (KP-AV8).
5. Documents the factor-2 discrepancy honestly as partial falsification
   of the framework's charged-lepton sector under cited source-stack content.
6. Characterizes the single admission (multiplicity-counting principle)
   that would close BAE.
7. Cross-validates Probes 12, 18, 22, 24, 25, 26: same prediction
   κ = 1 from distinct retained routes.
8. Provides paired runner with explicit numerical/algebraic verification
   for all nine KP-AVs.

### What this probe DOES NOT do

1. Does NOT close BAE.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step (KP-AV1-AV7
   are derived from cited source-stack content; PDG appears only in KP-AV8 as
   the falsification-test target).
6. Does NOT promote external surveys to retained authority.
7. Does NOT propose F3-extremum κ = 1 as the physical Koide value (it
   is the framework's derived prediction; the empirical κ ≈ 2 remains
   an external observation that the framework currently does not
   reproduce).
8. Does NOT advocate for either of the two honest options (admit
   mult-counting vs accept partial falsification); user/audit decides.

## Comparison with prior probes

| Probe | Mechanism | Concludes |
|---|---|---|
| Probe 12 | Plancherel-uniform on Ĉ_3 (state level) | (1, 2) → F3 → κ = 1 |
| Probe 18 | F1 vs F2 vs F3 algebraic | F2 ruled out; F1 vs F3 ambiguous algebraically |
| Probe 19 | Wilson chain m_τ scale (parameter level) | mass scale fixed; κ-neutral |
| Probe 21 | Native bilinear lattice flow | identity flow, neutral fixed-point family |
| Probe 22 | Spectrum-cone pivot | bridge-equivalent to operator BAE; same (a, |b|)-plane |
| Probe 24 | φ = 2/9 from Z_3 character algebra | dimensionless φ pinned; κ-neutral |
| Probe 25 | Retained Hamiltonian dynamics extremization (functional level) | F1 structurally rejected; F3 canonical |
| Probe 26 | Wilson chain rescaling | κ scale-invariant; mass scale ≠ κ-determination |
| **Probe 29** | **Synthesizes all cited source-stack content into κ-predictor; tests against PDG** | **κ = 1 prediction; PARTIAL FALSIFICATION vs PDG κ ≈ 2** |

Probe 29's contribution: the first probe that **combines** all
retained κ-determining content into a single canonical functional and
tests its prediction against empirical observation. Prior probes
attacked the closure question; this probe inverts the framing and
tests the framework's actual prediction.

This is the natural next step after Probe 25: Probe 25 says "retained
dynamics gives F3"; Probe 29 says "F3 → κ = 1, PDG → κ ≈ 2;
discrepancy = factor 2 in κ".

## Convention-robustness check

The runner verifies (Section 0, 1, 11):

- **Scale-invariance under H → cH:**
  - kappa(rH) = kappa(H) for any positive r (Probe 26 cross-check).
  - All AVs preserve extremization location.

- **Basis change C → C² = C^{-1}:**
  preserves the isotype decomposition; E_+, E_⊥ unchanged.

- **All cited-source-stack κ-determining AVs converge on κ = 1:**
  Φ_G, F3, Plancherel, Φ_canonical all give kappa ≈ 1.0010 at sweep
  precision; max mutual deviation < 0.001 (sweep-granularity).

- **Bridge identity verified at multiple δ:**
  cone_slack = -9 × bae_slack to < 1e-10 at all sample (a, |b|, δ).

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained matter-sector dynamics (load-bearing)

- Probe 25 (canonical free-Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 21 (native bilinear matter Hamiltonian): [`KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md)
- Lieb-Robinson microcausality: [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- Reflection positivity / transfer matrix: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius (with §4 explicit F1/F3 enumeration): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class theorem: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- Spectrum-operator bridge identity: [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Probe campaign (BAE-closure)

- Eleven-probe synthesis: [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 18 (F1 canonical): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 19 (Wilson chain m_τ): [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- Probe 22 (spectrum cone): [`KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md`](KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md)
- Probe 24 (φ from Z_3 character): [`KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md`](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md)
- Probe 25 (physical extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 26 (Wilson dimensional consistency): [`KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md`](KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md)

### Naming convention

- BAE rename note (PR #790, 2026-05-09): "Brannen Amplitude
  Equipartition (BAE)" is the primary name; "A1-condition" is the
  legacy alias.

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_kappa_prediction_test_2026_05_09_probe29.py
```

Expected: `=== TOTAL: PASS=57, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained input sanity (C unitary, order 3; E_+ = 3a²;
   E_⊥ = 6|b|²; equipartition at BAE).
2. Section 1 — MRU formula κ = 2μ/ν verified at multiple (μ, ν).
3. Sections 2-6 — KP-AV1-AV5: free Gaussian (κ = 1), Plancherel-uniform
   (κ = 1), spectrum-cone bridge (κ = 1), Wilson m_τ scale
   (κ-neutral), φ = 2/9 (κ-neutral).
4. Section 7 — KP-AV6: combined cited source-stack content gives Φ_canonical
   with κ = 1 prediction.
5. Section 8 — KP-AV7: MRU image of integer-(μ, ν) class shows F1
   structurally absent from cited dynamics.
6. Section 9 — KP-AV8: empirical PDG κ ≈ 2 vs framework prediction
   κ = 1 = factor 2 discrepancy = partial falsification.
7. Section 10 — KP-AV9: minimum admission (multiplicity-counting)
   characterized as single primitive.
8. Section 11 — Verdict synthesis: all retained AVs converge on
   κ = 1; PDG gives κ ≈ 2; partial falsification.
9. Section 12 — Does-not disclaimers (no closure, no admission, no
   PDG-derivation, no theorem modification).
10. Section 13 — Comparison with prior probes (12, 18, 22, 25).

Total: 57 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note explicitly
  separates the retained-derived κ = 1 prediction (KP-AV1-AV7) from the
  external empirical κ ≈ 2 falsification target (KP-AV8). The framework
  derives κ = 1; the discrepancy with PDG is a separate empirical
  observation, not algebraic consistency.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "framework predicts κ = 2" by directly computing the
  framework's κ-prediction and comparing against empirical κ. The
  honest answer is "framework predicts κ = 1, not κ = 2".
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded partial falsification;
  the BAE admission remains at its prior bounded status; no retained-
  tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: this note synthesizes
  the campaign-terminal residue from a NEW angle (predictor framing
  vs closure framing) — not a relabel of any prior probe. Probe 25's
  conclusion ("dynamics gives F3") becomes Probe 29's prediction
  ("framework predicts κ = 1") with explicit empirical falsification
  arrow.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (closing BAE) characterized in terms of WHAT additional content
  would be needed (multiplicity-counting principle), not in time.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a 9-vector (KP-AV1-AV9) attack with sharp PASS/FAIL deliverables on
  a single load-bearing structural hypothesis (framework's κ-prediction
  matches empirical κ).
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note proposal + paired runner + cached output, no synthesis
  notes, no lane promotions.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- [koide_bae_probe_native_lattice_flow_bounded_obstruction_note_2026-05-09_probe21](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md)
- [koide_bae_probe_spectrum_cone_bounded_obstruction_note_2026-05-09_probe22](KOIDE_BAE_PROBE_SPECTRUM_CONE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe22.md)
- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- [koide_bae_probe_phi_from_z3_character_sharpened_note_2026-05-09_probe24](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md)
- [koide_bae_probe_wilson_chain_mass_sharpened_note_2026-05-09_probe19](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- [koide_a1_probe_plancherel_peter_weyl_bounded_obstruction_note_2026-05-09_probe12](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_kappa_spectrum_operator_bridge_theorem_note_2026-04-19](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [physical_lattice_foundational_interpretation_note_2026-05-08](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
