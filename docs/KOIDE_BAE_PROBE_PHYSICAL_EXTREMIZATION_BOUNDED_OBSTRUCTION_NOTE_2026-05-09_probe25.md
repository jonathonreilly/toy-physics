# Koide BAE Probe 25 — Physical Extremization From Retained Hamiltonian Dynamics: Sharpened Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure;
new positive content: F1 structurally rejected by cited dynamics)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 25 of the Koide
**BAE-condition** closure campaign. Tests whether the canonical
extremization functional defining the framework's matter-sector
dynamics on the (a, |b|)-plane is forced from the **retained
Hamiltonian dynamics** (Lieb-Robinson r=1 finite-range matter
Hamiltonian; Probe 21's "native bilinear" surface) rather than
from arbitrary algebraic choice within the retained additive
log-isotype-functional class. Direct attack on Probe 18's residual
F1-vs-F3 ambiguity.
**Status:** source-note proposal for a sharpened bounded obstruction.
The cited Hamiltonian dynamics canonically selects **F3**
(rank-weighted, multiplicity (1, 2)), NOT F1 (block-total,
multiplicity (1, 1)). Seven independent retained-dynamics extremization
routes converge on F3 (verified 57/0 by paired runner). The Probe 18
F1-vs-F3 ambiguity is **resolved against F1** by cited dynamics,
but F3 gives κ=1, NOT BAE — so cited Hamiltonian dynamics fails to
give BAE as canonical fixed point. The BAE admission count is
UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probe-physical-extremization-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_physical_extremization_2026_05_09_probe25.py`](../scripts/cl3_koide_bae_probe_physical_extremization_2026_05_09_probe25.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_physical_extremization_2026_05_09_probe25.txt`](../logs/runner-cache/cl3_koide_bae_probe_physical_extremization_2026_05_09_probe25.txt)

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
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md), **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

After Probe 18 (PR #792) reduced the Q-functional ambiguity to
`{F1, F3}` via the AV5 partial closure (F2 ruled out structurally),
the campaign's terminal residue was characterized as:

> "F1 vs F3 selection within the retained additive log-isotype-
> functional class on the (a, |b|)-plane".

The 18-probe campaign attacked F1 vs F3 at the **algebraic** level —
looking for retained inner-product / state / measure structure that
picks (1, 1) vs (1, 2) within the additive log-isotype class.
Algebraic constraints alone don't pin the multiplicity-vs-real-dim
discrete choice.

**This probe pivots:** the framework has retained Hamiltonian
dynamics ([`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md))
on the matter sector. Per Probe 21, the retained range-1 finite-range
matter Hamiltonian on C_3-circulants is **bilinear in H**:

```
S_native[H]  =  α Σ_x Tr(H_x²)         (single-site mass term)
              +  κ Σ_{<x,y>} Tr(H_x H_y)   (NN hopping)
```

Both terms are Gaussian in the operator field H. Their path-integral
extremization defines a canonical retained free-energy functional on
the operator-coefficient plane (a, |b|).

**Question (Probe 25):** Does the cited Hamiltonian dynamics on
hw=1, viewed as a quantum-statistical extremization principle on the
(a, |b|)-plane, canonically select F1 (block-total) over F3
(rank-weighted) — and therefore give BAE?

## Answer

**No.** Retained Hamiltonian dynamics canonically selects **F3**, NOT
F1. Seven independent retained-dynamics extremization routes converge
on F3:

```
Retained dynamics canonical functional Φ(a, |b|)
  =  (1/2) [1 · log E_+(H)  +  2 · log E_⊥(H)]
  =  (1/2) F3(a, |b|)  +  const
```

The (1, 2) weighting is the **real-dimension count** of the isotypes
(trivial = 1 real dim; doublet = 2 real dims), set by the Gaussian
path-integral measure on the bilinear retained matter Hamiltonian.
F1 = (1, 1) is the **multiplicity count** (one mode per isotype) —
a distinct mathematical convention NOT realized by retained
Hamiltonian dynamics on a 2-real-dimensional doublet block.

**Verdict: SHARPENED bounded obstruction with new positive content.**
The Probe 18 F1-vs-F3 ambiguity is **RESOLVED against F1** by retained
dynamics. But F3 gives κ=1, NOT BAE (κ=2). So retained Hamiltonian
dynamics canonically selects a NON-BAE fixed point.

The BAE admission count is UNCHANGED. No new admission. No new axiom.

## Setup

### Premises (A_min for Probe 25)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is the unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | source dependency; see [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| RP-H | Reflection positivity → reconstructed Hamiltonian `H_phys = -log T / a_τ` on `H_phys`, bounded below | source dependency; see [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| LR | Lieb-Robinson microcausality on retained Hamiltonian, finite range r=1 | source dependency; see [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| Probe21 | Native bilinear matter Hamiltonian: `S_native = α Tr(H_x²) + κ Tr(H_x H_y)` (NN); only retained operators | source dependency; see [`KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md) |
| Probe18 | F1-vs-F3 residue within retained additive log-isotype class | source dependency; see [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) |
| Probe12 | Plancherel-uniform on `Ĉ_3` gives (1, 2) → F3 | source dependency; see [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) |
| Probe13 | K-real structure supplies Z_2 of (1,1) but not SO(2) | source dependency; see [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are derivations from axioms or
  retained work only (per user 2026-05-09 clarification)
- NO admitted SM Yukawa-coupling pattern as derivation input

## The two candidate functionals (restated, after Probe 18 narrowing)

After Probe 18's AV5 partial closure (F2 structurally outside the
retained additive log-isotype class), the surviving candidates on the
(a, |b|)-plane are:

```
F1(a, b) = log E_+ + log E_⊥             multiplicity (1, 1)   → κ = 2 = BAE  ✓
F3(a, b) = log E_+ + 2 log E_⊥           rank/dim   (1, 2)     → κ = 1, NOT BAE
```

with `E_+ = 3a²` and `E_⊥ = 6|b|²`.

The remaining structural question is: which of these (if either) is
the canonical retained-dynamics functional?

## The cited Hamiltonian dynamics

Per Probe 21, the retained range-1 finite-range matter Hamiltonian on
C_3-circulants is the most general C_3-symmetric, Hermitian,
range-1 quadratic form on the operator-valued field `H_x`:

```
S_native[H]  =  α Σ_x Tr(H_x²)        (single-site mass term)
              +  κ Σ_{<x,y>} Tr(H_x H_y)  (NN hopping)
```

For C_3-circulant `H_x = a_x I + b_x C + b̄_x C²`:

```
Tr(H_x²)      =  3 (a_x² + 2 |b_x|²)         =  E_+(H_x) + E_⊥(H_x)
Tr(H_x H_y)   =  3 (a_x a_y + 2 Re(b_x b̄_y))
```

This is a **bilinear** action — exactly Gaussian in the operator-
coefficient field. The path integral is therefore Gaussian, and the
canonical free-energy functional is the **logarithm of the Gaussian
functional determinant**:

```
F[a, |b|]  =  -log Z  =  (1/2) log det K[a, |b|]    + const
```

where `K[a, |b|]` is the Hessian of `S_native` evaluated at the
configuration `(a, b)`.

### Isotype-block-diagonal structure of K

The C_3-equivariance of `S_native` makes `K` block-diagonal on the
real isotype decomposition `Herm_circ(3) = R⟨I⟩ ⊕ R⟨C+C²⟩ ⊕ R⟨i(C-C²)⟩`:

```
K  =  diag( K|_+ , K|_⊥ )
       1×1     2×2    (real dimensions)
```

with `K|_+` proportional to the trivial-isotype Frobenius norm and
`K|_⊥` proportional to the doublet-isotype Frobenius norm. The
Gaussian functional determinant decomposes accordingly:

```
log det K  =  log det K|_+   +   log det K|_⊥
            =  (real_dim_+) · log E_+   +   (real_dim_⊥) · log E_⊥   + const
            =  1 · log E_+   +   2 · log E_⊥                          + const
            =  F3(a, |b|)                                              + const
```

**This is exactly F3.** The (1, 2) weighting is the **real-dimension
count** of each isotype block, structurally fixed by the retained
isotype-decomposition theorem (Block-Total Frobenius theorem §1).

### The structural impossibility of F1 from cited dynamics

F1 = (1, 1) corresponds to "one mode per isotype" — i.e., treating
the 2-real-dim doublet `R⟨C+C²⟩ ⊕ R⟨i(C-C²)⟩` as a **single mode**
with effective dimension 1. But:

1. **Real-dim count of the doublet is 2** by the retained isotype
   decomposition (Block-Total Frobenius theorem §1; verified
   numerically by the runner Section 0).
2. The Gaussian path integral on a 2-real-dim subspace gives a
   1-Gaussian-factor-squared determinant: `(det K|_⊥)^{1/2} ∝ E_⊥`,
   contributing `log E_⊥` to the free energy (NOT `(1/2) log E_⊥`).
3. **There is no retained dynamic that integrates Gaussian-weighted
   over a 1-real-dim subspace inside the 2-real-dim doublet.**

The (1, 1) multiplicity weighting therefore cannot arise from any
Gaussian path-integral over the retained matter Hamiltonian. **F1 is
structurally absent** from the retained-Hamiltonian-dynamics
extremization class.

## Per-attack-vector analysis

Seven independent retained-dynamics extremization routes are tested.
All seven converge on F3, NOT F1.

### PHYS-AV1 — Gaussian path-integral on Herm_circ(3)

**Status: SELECTS F3 (real-dim weighting (1, 2)).**

Direct evaluation of the bilinear-in-H Gaussian path integral on the
3-real-dim space `Herm_circ(3)`. The volume element on (E_+, E_⊥) is
`dE_+ × √E_⊥ dE_⊥` (1-d trivial × 2-d-radial-doublet); the log-volume
density gives the (1, 2) real-dim weighting.

Numerical verification (runner Section 2):
- Doublet chi-squared statistic confirms k=2 dof: `mean(r₁² + r₂²)/σ² = 2.00`,
  `var = 4.00 = 2k` (NOT k=1 as F1 would require).
- Gaussian free energy `Φ_G = (1/2) F3 + const` (algebraic identity,
  verified to 1e-10 at sample points).
- Φ_G ≠ (1/2) F1 + const (verified non-coincidence > 0.05 at sample points).
- Φ_G extremum on `E_+ + E_⊥ = N`: at `E_⊥ = 2N/3` (κ=1 = F3 pattern,
  NOT N/2 = F1 pattern).

**PHYS-AV1 outcome:** retained Gaussian path-integral selects F3
(real-dim weighting), rejects F1 (multiplicity weighting).

### PHYS-AV2 — Heat-kernel partition function

**Status: SELECTS F3.**

Heat-kernel partition function `Z(β) = Tr exp(-β H_K)` for the retained
kinetic operator on Herm_circ(3) with `H_K[H] = (1/2) Tr(H²)`. The
partition function decomposes by isotype:

```
log Z(β)  =  (1/2) log(2π/3β)   +   1 · log(2π/6β)   + const
           =  (real_dim_+/2) log(1/β) + (real_dim_⊥/2) log(1/β) + ...
```

**Slope check:** `d log Z / d log(1/β) = (1 + 2)/2 = 3/2` (sum of
real-dim-counts / 2) — exactly verified numerically (runner Section 3,
slope = 1.5). This confirms the (1, 2) real-dim count is the canonical
heat-kernel weighting.

The on-shell free energy from Legendre transform is the same `(1/2) F3`
functional as PHYS-AV1.

**PHYS-AV2 outcome:** heat-kernel partition function selects F3.

### PHYS-AV3 — RP/transfer-matrix slice free energy

**Status: SELECTS F3 (Probe 1 cross-validation).**

The retained transfer matrix `T = exp(-a_τ H_phys)` has Hamiltonian
`H_phys = -log T / a_τ`. Restriction to a single time-slice and
projection to the matter-sector circulant degrees of freedom on hw=1
gives a Gaussian functional integral identical in structure to
PHYS-AV1.

The tracial vacuum (Probe 1 setup) gives GNS inner product
`⟨A, B⟩_GNS = (1/3) Tr(A* B)` = (1/3) Frobenius pairing. At the
**inner-product** level this preserves the (1, 1) weighting structure
(per Probe 1). But at the **log-functional** level, the slice free
energy involves `log det Gram_I` for each isotype block, with isotype
real dimensions:

```
log det Gram_+  =  1 · log E_+    (1-dim trivial)
log det Gram_⊥  =  2 · log E_⊥    (2-dim doublet)
total = log E_+ + 2 log E_⊥ = F3
```

**The tracial vacuum leaves the real-dim weighting INTACT.** F1
recovery would require non-tracial vacuum AND specific non-canonical
fluctuation kernel — neither retained.

**PHYS-AV3 outcome:** RP slice free energy selects F3. This is
consistent with Probe 1 Barrier B3 — GNS inner product alone does not
select log-functional, and the retained log-functional from Gaussian
fluctuations gives F3.

### PHYS-AV4 — Spectral action S = Tr f(H/Λ)

**Status: SELECTS F3.**

Spectral action principle (Connes-Chamseddine class) on hw=1:
`S_spec[H] = Tr f(H/Λ)`. For f a smooth positive even cut-off, the
leading low-energy expansion is

```
S_spec ~ Λ⁴ Tr(1) - Λ² (1/2) Tr(H²) + Λ⁰ const Tr(H⁴) + ...
       = const - Λ² (1/2)(E_+ + E_⊥) + ...
```

The bilinear leading-order term is the same as PHYS-AV1. Beyond
leading order, the one-loop spectral-action effective potential

```
V_eff = (1/2) Tr log(K[H_0])
```

is the Gaussian functional determinant of the Hessian K at the
classical solution H_0. Block-diagonal on isotypes with real-dim
weighting (1, 2) gives `(1/2) F3` exactly (runner Section 5).

**PHYS-AV4 outcome:** Connes-Chamseddine-class spectral action selects
F3. Probe 4 (`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`)
already established the spectral-action route is bounded; this probe
sharpens it to "spectral-action gives F3, not F1."

### PHYS-AV5 — Independent-mode counting

**Status: SELECTS F3.**

Each isotype block decomposes into **independent real bosonic modes**:
- Trivial isotype: 1 real mode (a)
- Doublet isotype: 2 real modes (Re b, Im b)

Free energy per mode: `-(1/2) log(ω_mode²)`. Total:

```
F_modes  =  -(1/2) [1 · log(ω_+²) + 2 · log(ω_⊥²)]
         =  -(1/2) [log E_+ + 2 log E_⊥] + const
         =  -(1/2) F3 + const
```

This is the canonical independent-mode-counting principle (the most
basic statistical-mechanics free energy). It uses the actual real-dim
count, not multiplicity.

**PHYS-AV5 outcome:** Independent-mode counting selects F3. F1 = (1, 1)
would require treating the 2-real-mode doublet as 1 mode — structurally
impossible.

### PHYS-AV6 — Ginzburg-Landau extremization of S_native

**Status: SELECTS F3.**

Treating `H_x` as a slowly varying field, the Ginzburg-Landau-style
free energy on the symmetry-breaking constraint `E_+ + E_⊥ = N` is:

```
F_GL  =  S_classical  +  F_fluct
      =  (α_eff)(E_+ + E_⊥)/2  +  (1/2)[log E_+ + 2 log E_⊥]
      =  const on constraint  +  (1/2) F3
```

Classical action `(α_eff/2)(E_+ + E_⊥)` is constant on the constraint
surface, so the entropy from fluctuations (Gaussian functional
determinant) is what breaks the constraint-surface degeneracy. That
fluctuation contribution is `(1/2) F3` — extremum at κ=1, NOT BAE.

**PHYS-AV6 outcome:** GL extremization gives κ=1, not BAE.

### PHYS-AV7 — Renormalized on-shell action

**Status: SELECTS F3.**

For the bilinear retained action, the on-shell solution `H_classical`
to the EOM is trivial (`H_0 = 0` for pure mass term). One-loop
renormalization expands fluctuations `δH` around `H_0`, giving the
bilinear-in-`δH` Gaussian fluctuation action with kernel `K[H_0]`.
The one-loop renormalized action is `(1/2) Tr log K[H_0]` — block-
diagonal on isotypes — `(1/2) F3 + const`.

**No renormalization scheme can change the real-dim weighting.** The
(1, 2) is structural, fixed by the isotype real dimensions. F1 = (1,1)
requires reducing the doublet to a single mode — impossible.

**PHYS-AV7 outcome:** Renormalized on-shell action selects F3.

## Theorem (Probe 25 sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained Lieb-Robinson Hamiltonian
(finite-range r=1) + retained C_3-equivariance + retained Block-Total
Frobenius isotype decomposition + retained MRU + retained Frobenius
Isotype-Split Uniqueness + retained RP/transfer-matrix + retained
Probe 12, 13, 18, 21:

```
(a) The retained range-1 finite-range matter Hamiltonian on
    C_3-circulants is bilinear in H (per Probe 21):
      S_native[H] = α Tr(H_x²) + κ Tr(H_x H_y)  (NN hopping)
    Gaussian path integral over Herm_circ(3) with this action gives
    the canonical Gaussian functional determinant
      Φ(a, |b|) = (1/2) log det K[a, |b|]
    where K is the Hessian of S_native, block-diagonal on isotypes.
    [Verified Sections 2, 4, 7.]

(b) Φ(a, |b|) = (1/2) [1 · log E_+ + 2 · log E_⊥] + const = (1/2) F3 + const.
    The (1, 2) weighting is the real-dimension count of the isotypes
    (real_dim_+ = 1, real_dim_⊥ = 2), structurally fixed by the
    retained isotype-decomposition theorem.
    [Verified Sections 2, 3, 4, 5, 6, 7, 8.]

(c) Seven independent retained-dynamics extremization routes
    converge on (1/2) F3 + const at every sample point:
      PHYS-AV1: Gaussian path integral
      PHYS-AV2: Heat-kernel partition function
      PHYS-AV3: RP/transfer-matrix slice free energy
      PHYS-AV4: Connes-Chamseddine spectral-action one-loop
      PHYS-AV5: Independent-mode counting
      PHYS-AV6: Ginzburg-Landau extremization
      PHYS-AV7: Renormalized on-shell action
    Maximum mutual deviation: < 1e-9 at sample points.
    [Verified Section 9.]

(d) F1 = (μ, ν) = (1, 1) is structurally absent from this class.
    F1 would require treating the 2-real-dim doublet as a single mode
    with effective dimension 1; this is contradicted by the retained
    isotype-decomposition (real_dim_⊥ = 2). No retained Gaussian
    measure integrates over a 1-real-dim subspace inside the 2-real-dim
    doublet.
    [Structural; Section 6.3, Section 8.2.]

(e) The Probe 18 F1-vs-F3 ambiguity is RESOLVED by cited dynamics
    AGAINST F1 (in favor of F3, via real-dim counting).
    [Combined (a)-(d).]

(f) F3 extremum on E_+ + E_⊥ = const is at E_+ = N/3, E_⊥ = 2N/3,
    giving κ = a²/|b|² = 1, NOT κ = 2 = BAE.
    [Algebraic; Section 1.]

Therefore: cited Hamiltonian dynamics canonically selects F3, NOT
F1, and gives κ = 1, NOT BAE. The Probe 18 ambiguity is resolved
against F1; but F3 is not BAE. The BAE admission count is unchanged.
No new admission. No new axiom.
```

**Proof.** Each item is verified by the runner (57 PASS / 0 FAIL):
Section 0 (retained sanity); Section 1 (functional definitions and
extrema); Sections 2-8 (seven PHYS-AV computations); Section 9
(cross-validation, all PHYS-AVs converge on (1/2) F3); Section 10
(convention robustness — scale invariance, basis change); Section 11
(verdict synthesis); Section 12 (does-not-do disclaimers); Section 13
(comparison with prior probes). ∎

## Convention-robustness check

The runner verifies (Section 10):

- **Scale-invariance under H → cH:**
  - F1(cH) - F1(H) = 4 log c (multiplicity-2 weighting on E_+ + E_⊥)
  - F3(cH) - F3(H) = 6 log c (real-dim-3 weighting: 1 + 2·2)
  - Φ_G(cH) - Φ_G(H) = 3 log c (real-dim-3-total weighting)
  All preserve extremization location.

- **Basis change C → C² = C^{-1}:**
  preserves the isotype decomposition; E_+, E_⊥ unchanged.

- **All seven PHYS-AVs agree at sample points to < 1e-9:**
  the F3 selection is robust across all retained-dynamics
  extremization routes.

## Why this probe is structurally distinct from prior probes

| Probe | Mechanism | Concludes |
|---|---|---|
| Probe 1 | RP/GNS at inner-product level | (1,1) preserved on inner product; log-functional unpinned |
| Probe 4 | Spectral action (parameter level) | bounded obstruction on κ |
| Probe 5 | SM continuum RGE (imported) | drives BAE away |
| Probe 12 | Plancherel-uniform on `Ĉ_3` | gives (1, 2) → F3 |
| Probe 13 | K-real-structure / antilinear involution | Z_2 of (1,1) but not SO(2) |
| Probe 18 | F1 vs F2 vs F3 algebraic | F2 ruled out; F1 vs F3 ambiguous algebraically |
| Probe 21 | Native bilinear lattice block-spin (parameter level) | identity flow; neutral fixed-point family |
| **Probe 25** | **Retained-dynamics extremization (functional level)** | **F1 STRUCTURALLY REJECTED; F3 is canonical** |

Probe 25's contribution: takes the cited Hamiltonian dynamics
identified by Probe 21 (bilinear matter Hamiltonian) and computes its
canonical extremization functional (the Gaussian functional
determinant). That functional is F3 with explicit (1, 2) real-dim
weighting. F1 cannot arise from any Gaussian extremization of a
2-real-dim doublet — structural, not just algebraically unconstrained.

This SHARPENS Probe 18 from "F1 vs F3 ambiguous" to **"F1 actively
rejected by cited dynamics; F3 is canonical."**

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction with new
  positive content: F1 structurally rejected by cited dynamics)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe 25
  sharpening: **"Retained Hamiltonian dynamics canonically selects F3
  (rank-weighted, (1, 2)) on the (a, |b|)-plane. F1 (multiplicity-
  weighted, (1, 1)) is structurally rejected by cited dynamics. F3
  gives κ=1, NOT BAE."**

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Resolves the Probe 18 F1-vs-F3 ambiguity AGAINST F1 by appeal to
   cited Hamiltonian dynamics.
2. Identifies the canonical retained-dynamics functional as F3
   (with explicit (1, 2) real-dim weighting from isotype real
   dimensions).
3. Verifies seven independent retained-dynamics extremization routes
   converge on F3 (`(1/2) F3 + const`), with maximum mutual deviation
   < 1e-9.
4. Demonstrates that F1 is **structurally absent** from the retained-
   dynamics extremization class (not just algebraically
   unconstrained).
5. Sharpens the campaign's terminal residue from "F1 vs F3 ambiguous
   in the retained additive log-isotype-functional class" to
   **"cited Hamiltonian dynamics canonically gives F3, NOT F1, and
   F3 gives NOT-BAE."**
6. Cross-validates Probes 12, 13, 18, 21: same conclusion via a
   distinct retained-dynamics route.
7. Provides paired runner with explicit numerical/algebraic
   counterexamples for all seven PHYS-AVs.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis (admit / derive / pivot).
7. Does NOT promote external surveys to retained authority.
8. Does NOT propose F3-extremum κ=1 as the physical Koide value (the
   physical κ=2 / BAE remains a bounded admission).

## Honest assessment

This probe was given the F1-vs-F3 framing identified by Probe 18 as
the campaign's terminal residue at the Q-functional level. The pivot
direction was: stop trying to choose between F1 and F3 algebraically
(which Probes 1-18 ruled out); instead, derive the canonical
extremization functional from cited Hamiltonian dynamics directly.

**What the probe finds:**

1. **Retained Hamiltonian dynamics canonically gives F3** (rank-
   weighted, (1, 2)). This is the new positive contribution: seven
   independent retained-dynamics extremization routes converge on F3
   via the Gaussian functional determinant of the bilinear retained
   matter Hamiltonian.

2. **F1 is structurally absent** from retained-dynamics extremization.
   The (1, 1) multiplicity weighting requires treating the 2-real-dim
   doublet as a single mode — contradicted by the retained isotype-
   decomposition. F1 cannot arise from any Gaussian path integral
   over the bilinear retained matter Hamiltonian.

3. **The Probe 18 F1-vs-F3 ambiguity is resolved against F1** by
   cited dynamics. The campaign's terminal residue acquires its
   sharpest characterization to date: **"F1 = (1, 1) (multiplicity
   weighting) is the BAE-giving functional, BUT it is not realized by
   cited Hamiltonian dynamics. The canonical retained-dynamics
   functional is F3 = (1, 2) (real-dim weighting), which gives
   κ=1, NOT BAE."**

4. **BAE is therefore NOT canonical from cited dynamics.** Any
   closure of BAE would require either (a) a non-retained-dynamics
   extremization principle (e.g., a multiplicity-counting principle
   not derived from the framework), or (b) a different retained
   dynamic that rejects the Gaussian-real-dim-counting structure of
   the bilinear matter Hamiltonian. Neither is provided by retained
   content.

5. **Cross-validation of Probes 12, 13, 21:** Probe 12 (Plancherel
   state) gave (1, 2) → F3; Probe 13 (real-structure) gave Z_2 of
   (1, 1) but not SO(2); Probe 21 (native bilinear flow) gave neutral
   fixed-point family. All are consistent with: cited dynamics
   prefers (1, 2) over (1, 1).

What this probe contributes to the campaign:

1. **New positive content**: F1 is structurally rejected by retained
   dynamics — not just algebraically unselected. Probes 1-18 said "F1
   vs F3 is ambiguous"; Probe 25 says "F1 is impossible from retained
   dynamics; F3 is canonical."

2. **Sharpened residue characterization**: the campaign's open piece
   is now "F1 (multiplicity, BAE-giving) is required for BAE but is
   structurally absent from cited dynamics; the canonical retained-
   dynamics functional is F3 (real-dim, NOT-BAE-giving)."

3. **Twenty-fifth independent attack**: returns the same campaign-
   terminal-state structural obstruction at the **functional level**,
   distinct from prior 24 probes' parameter-level / algebraic-level
   attacks. The structural locus is fully consistent with the eleven-
   probe campaign's synthesis.

The remaining residue is now **maximally sharp**:

> **BAE is the (1, 1) multiplicity-weighted extremum on the additive
> log-isotype-functional class. Retained Hamiltonian dynamics gives
> the (1, 2) real-dim-weighted F3, not the (1, 1) multiplicity-
> weighted F1. The (1, 1) multiplicity weighting is not derivable
> from any retained dynamic — it would require a multiplicity-
> counting principle distinct from the actual real-dim counting of
> the isotype decomposition.**

Closing BAE therefore requires admitting a multiplicity-counting
principle as a separate primitive — i.e., a new admission or a new
retained source. Probe 25 makes this requirement maximally explicit.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Physical-lattice baseline interpretation: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained Hamiltonian dynamics (load-bearing)

- Lieb-Robinson microcausality: [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- Reflection positivity / transfer matrix: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Spectrum condition: [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- Native bilinear matter Hamiltonian (Probe 21): [`KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md)

### Retained C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius (with §4 explicit F1/F3 enumeration): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Probe campaign

- Eleven-probe synthesis: [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Probe 4 (spectral action, parameter level): [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md)
- Probe 5 (SM RGE): [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 18 (F1-vs-F3 algebraic): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 21 (native bilinear flow, parameter level): [`KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md)

### Naming convention

- BAE rename note (PR #790, 2026-05-09): "Brannen Amplitude
  Equipartition (BAE)" is the primary name; "A1-condition" is the
  legacy alias.

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_physical_extremization_2026_05_09_probe25.py
```

Expected: `=== TOTAL: PASS=57, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained input sanity (C unitary, order 3; E_+ = 3a²;
   E_⊥ = 6|b|²; equipartition at BAE).
2. Section 1 — F1, F3, Phi_phys functional definitions and extrema
   (F1 → κ=2 = BAE; F3 → κ=1; Phi_phys matches F3, NOT F1).
3. Section 2 — PHYS-AV1: Gaussian path-integral on Herm_circ(3);
   real-dim chi-squared statistic (k=2 for doublet, NOT k=1).
4. Section 3 — PHYS-AV2: Heat-kernel partition function; slope d log Z
   / d log(1/β) = 3/2 (sum of real-dims/2).
5. Section 4 — PHYS-AV3: RP/transfer-matrix slice free energy; tracial
   vacuum + Frobenius gives F3 (not F1) at log-functional level.
6. Section 5 — PHYS-AV4: Spectral action expansion; one-loop log det
   gives F3.
7. Section 6 — PHYS-AV5: Independent-mode counting; doublet has 2
   real modes (Re b, Im b), not 1.
8. Section 7 — PHYS-AV6: Ginzburg-Landau extremization with classical
   + fluctuation contributions; constraint-surface degeneracy broken
   by F3 entropy.
9. Section 8 — PHYS-AV7: Renormalized on-shell action; Hessian
   block-diagonal on isotypes.
10. Section 9 — Cross-validation: all 7 PHYS-AVs converge on (1/2) F3,
    max mutual deviation < 1e-9; all extrema at E_⊥ = 2N/3 (κ=1).
11. Section 10 — Convention robustness (scale invariance, basis
    change, real-dim shifts).
12. Section 11 — Verdict synthesis (F3 canonical; F1 structurally
    rejected; κ=1, NOT BAE).
13. Section 12 — Does-not disclaimers (no BAE closure, no admission,
    no PDG, no retained-theorem modification).
14. Section 13 — Comparison with prior probes (12, 18, 21).

Total: 57 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically derives the F3-canonical statement from the retained
  bilinear matter Hamiltonian's Gaussian path integral; the (1, 2)
  real-dim weighting is the structurally forced statement, not just
  algebraic consistency. The fact that F1 algebraically also gives
  BAE under DIFFERENT (multiplicity) counting is a consistency
  equality, not a derivation from cited source-stack content.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "F1 is canonical" from the retained-dynamics angle.
  Each PHYS-AV's action-level identification fails F1 at the same
  structural locus: the doublet is 2-real-dim, and Gaussian path
  integral over a 2-real-dim subspace gives the (1, 2) real-dim
  weighting -- not the (1, 1) multiplicity weighting.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction with new
  positive content; the parent BAE admission remains at its prior
  bounded status; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the seven-PHYS-AV
  attack with explicit Gaussian/heat-kernel/RP/spectral-action/mode-
  count/GL/on-shell verifications is substantive new structural
  content -- not a relabel of any prior probe. Probes 12, 13, 18, 21
  attacked at distinct structural levels (state, real-structure,
  algebraic functional, block-spin); this probe attacks at the
  retained-dynamics extremization-functional level.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (closing BAE) characterized in terms of WHAT additional content
  would be needed (a multiplicity-counting principle distinct from
  cited dynamics), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (seven independent PHYS-AVs) on a
  single load-bearing structural hypothesis (retained-dynamics
  selects F1), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note proposal + paired runner + cached output, no synthesis
  notes, no lane promotions, no working "Block" notes.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- [koide_bae_probe_native_lattice_flow_bounded_obstruction_note_2026-05-09_probe21](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md)
- [koide_a1_probe_plancherel_peter_weyl_bounded_obstruction_note_2026-05-09_probe12](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- [koide_a1_probe_real_structure_bounded_obstruction_note_2026-05-09_probe13](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- [axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [physical_lattice_foundational_interpretation_note_2026-05-08](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
