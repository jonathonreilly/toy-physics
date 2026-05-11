# Koide BAE Probe V — MaxEntropy / Thermodynamic Attack on the C_3[111] Triplet

**Date:** 2026-05-10
**Type:** no_go (thermodynamic-level route rejection;
no positive closure; bounded support: MaxEntropy on Born density
restricted to circulant Hamiltonians, with trace and energy constraints
(Tr ρ = 1, Tr ρH = E), gives the Gibbs state ρ ∝ exp(-βH); the Gibbs
state imposes NO constraint on |b|²/a² and the thermodynamic
potentials F, S, ⟨H⟩ are all C^∞ across the BAE point. This claim is
limited to the thermodynamic / MaxEntropy route.)
**Claim type:** no_go
**Scope:** review-loop source-note proposal — Probe V of the Koide
**BAE-condition** closure campaign. Tests whether maximum-entropy on
the Born density restricted to circulant Hamiltonians, with
trace and energy constraints, forces |b|²/a² = 1/2 (BAE) on the
C_3-equivariant Hermitian circulant `H = aI + bC + b̄C²`.
**Status:** source-note proposal for a thermodynamic-level no-go
route check. MaxEntropy with trace and energy
constraints **STRUCTURALLY DECOUPLES** from the circulant amplitude
ratio. Six independent decoupling theorems (TH-AV1 through TH-AV6)
verified by paired runner (64/0). The Gibbs state ρ = e^{-βH}/Z is
diagonal in the C_3 Fourier basis with eigenvalues p_k = e^{-βλ_k}/Z
where λ_k = a + 2|b|cos(φ - 2πk/3). The amplitude (a, b) parameterizes
H, NOT ρ; MaxEntropy does not optimize over (a, b). The naive
"equipartition" argument "1 a-mode = 2 b-modes summed" requires
isotype-equipartition `E_+(H) = E_⊥(H)` where `E_+ = 3a²` and
`E_⊥ = 6|b|²` (cited BlockTotalFrob surface); this is ALGEBRAICALLY
equivalent to BAE (3a² = 6|b|² ⟺ |b|²/a² = 1/2) but is the (1, 1)
multiplicity-counting admission, NOT a consequence of MaxEntropy.
The BAE admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probeV-maxentropy-20260510
**Primary runner:** [`scripts/cl3_koide_v_bae_maxent_2026_05_08_probeV_bae_maxent.py`](../scripts/cl3_koide_v_bae_maxent_2026_05_08_probeV_bae_maxent.py)
**Cache:** [`logs/runner-cache/cl3_koide_v_bae_maxent_2026_05_08_probeV_bae_maxent.txt`](../logs/runner-cache/cl3_koide_v_bae_maxent_2026_05_08_probeV_bae_maxent.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named inputs, and
no-go classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **Physical `Cl(3)` local algebra** = repo baseline local algebra;
  see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **`Z³` spatial substrate** = repo baseline spatial substrate;
  see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

The very name **Brannen Amplitude Equipartition** suggests classical
**equipartition** — a thermodynamic origin distinct from the
operator-level attacks already explored. Classical
statistical mechanics: equipartition gives `kT/2` per quadratic
degree of freedom. The Cl(3) circulant has 3 modes naively:

- 1 a-mode (real diagonal element, trivial isotype)
- 2 b-modes (complex off-diagonal: b and b̄ counted as 2 dofs)

Equipartition: each mode carries equal energy. `|a|²` (one mode) =
`2|b|²` (two modes summed). Inverting: `|b|²/|a|² = 1/2 = BAE`.

This route is worth checking because:

- The repo has a Born-density readout surface
  `ρ_grav(x) = ⟨x|ρ̂|x⟩` (per
  [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)).
- The repo has a KMS / Gibbs-state surface at inverse temperature
  `β_th = 2π/κ` (Block 01 (K1)).
- MaxEntropy with constraints `Tr ρ = 1`, `Tr ρH = E` is standard
  Jaynes 1957 derivation of the Gibbs state ρ = e^{-βH}/Z by
  variational calculus + Lagrange multipliers — derivable from
  cited source content + standard math, NOT a new physics axiom.

**Question (Probe V):** Does maximum-entropy on the Born density
restricted to circulant Hamiltonians, with trace and energy constraints
(Tr ρ = 1, Tr ρH = E), force |b|²/a² = 1/2 (BAE)?

This is structurally distinct from operator-level probes: those
probes attack Hilbert-space states and operator algebras, while this
probe attacks the **statistical / variational / thermodynamic level**
via MaxEntropy and the Gibbs state.

## Answer

**No.** MaxEntropy on Born density restricted to circulant
Hamiltonians, with trace and energy constraints, **structurally decouples**
from the continuous amplitude ratio |b|²/a². Six independent
decoupling theorems converge:

```
TH-AV1   Gibbs state from MaxEnt with trace and energy constraints
         MaxEnt[ρ] s.t. Tr ρ = 1, Tr ρH = E gives Gibbs ρ ∝ e^{-βH}.
         For circulant H, Gibbs is diagonal in the C_3 Fourier basis
         with p_k = e^{-βλ_k}/Z. Eigenvalues λ_k = a + 2|b|cos(φ -
         2πk/3) depend on (a, b); Gibbs imposes NO constraint on
         |b|²/a². [Verified Section 2.]

TH-AV2   Liouville on isotype blocks rederives operator-level (1, 2)
         The natural phase-space measure on Herm_circ(3) is the
         3-real-dim flat measure on (a, Re b, Im b). Equipartition
         over this measure gives ⟨|b|²⟩/⟨a²⟩ = 2 k_a/k_b — depends on
         coupling constants k_a, k_b in H, NOT on MaxEntropy.
         [Verified Section 3.]

TH-AV3   Equipartition over isotypes E_+ = E_⊥ does give 1/2
         BUT is the (1, 1) multiplicity-counting admission
         E_+(H) = 3a², E_⊥(H) = 6|b|² (cited BlockTotalFrob surface).
         Setting E_+ = E_⊥ gives 3a² = 6|b|² ⟺ |b|²/a² = 1/2 = BAE.
         But isotype-equipartition is NOT implied by Tr(ρH) = E;
         it is the (1, 1) admission already named in the MRU
         weight-class theorem. [Verified Section 4.]

TH-AV4   Counting-of-degrees no-bridge
         Naively: 1 a-dof + 2 b-dofs (b and b̄). But b and b̄ are
         conjugates, NOT 2 independent quantum modes; the 3 real
         dofs of H are (a, Re b, Im b). The 3 eigenvalues are
         constrained by trace + circulant structure. Equipartition
         over (a, Re b, Im b) with EQUAL couplings gives
         ⟨|b|²⟩ = 2⟨a²⟩, OPPOSITE of BAE. [Verified Section 5.]

TH-AV5   Boltzmann/Gibbs has no special structure at BAE
         Sweep |b|/a from 0.1 to 1.5 at fixed a, β: free energy F,
         entropy S, energy ⟨H⟩ are all C^∞ across the BAE point
         |b|/a = 1/√2. No thermodynamic phase transition; entropy
         is not maximized at BAE. [Verified Section 6.]

TH-AV6   Classical equipartition with explicit H_HO
         For H_HO = (1/2) k_a a² + (1/2) k_b |b|², MB gives
         ⟨|b|²⟩/⟨a²⟩ = 2 k_a/k_b. This depends on the EXTERNAL
         coupling constants k_a, k_b of the Hamiltonian, NOT on
         MaxEntropy itself. To get BAE, need k_b = 4 k_a — yet
         another way of stating the (1, 1) multiplicity admission.
         [Verified Section 7.]
```

**Verdict: NO-GO route check (thermodynamic-level decoupling) with
bounded support.** MaxEntropy on Born density with trace and energy
constraints gives the Gibbs state, which is parameterized by β but
does NOT pin (a, b). The free energy `F = -kT log Z`, entropy
`S = -k Tr(ρ log ρ)`, and energy `⟨H⟩ = Tr(ρH)` are smooth functions
of (a, b, β); there is no thermodynamic transition at the BAE point.
The "isotype equipartition" `E_+ = E_⊥` is algebraically equivalent
to BAE but is the (1, 1) multiplicity-counting admission, NOT a
consequence of MaxEntropy. **The BAE admission count is UNCHANGED.
No new admission. No new axiom.**

## Setup

### Premises (Probe V inputs)

| ID | Statement | Class |
|---|---|---|
| Cl3Baseline | Physical `Cl(3)` local algebra | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3Substrate | `Z³` spatial substrate | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; audit status set by ledger: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; audit status set by ledger: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | source dependency; audit status set by ledger: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | source dependency; audit status set by ledger: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; audit status set by ledger: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | source dependency; audit status set by ledger: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| BornGrav | Position-density Born readout `ρ_grav(x) := ⟨x|ρ̂|x⟩`, defined for all density operators | bounded-supported per [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| Gibbs/KMS | Finite-temperature Gibbs state on RP-reconstructed transfer-matrix Hilbert space at β_th = L_τ a_τ; KMS condition (K1)-(K4) | source dependency; audit status set by ledger: [`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md) |
| Probe28 | Operator-level: F3 (1,2) real-dim canonical; F1/BAE absent | source dependency; audit status set by ledger: [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| M3 | M_3(C) algebra on hw=1 triplet generated by translations + C_3[111] | source dependency; audit status set by ledger: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |

**Standard mathematical machinery used (per "no new axioms" constraint —
these are derivations from cited source content + standard math, not
new physics axioms):**

- Variational calculus with Lagrange multipliers (standard analysis;
  not a physics axiom)
- Jaynes 1957 MaxEntropy principle (cited as standard textbook
  formulation of the variational derivation of the Gibbs distribution
  from MaxEnt with linear constraints; the GIBBS state itself is
  linked through the Block 01 (K1) source surface)
- Maxwell-Boltzmann sampling on classical phase space (standard
  statistical mechanics; not a new physics axiom)
- Shannon / von Neumann entropy `S[ρ] = -Tr(ρ log ρ)` (standard
  information-theoretic functional; not a new physics axiom)

These are **mathematical statements**, not physical primitives. They
are used to compute properties of the cited Born-density surface on
circulant Hamiltonians.

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new physics axioms or new admissions — inputs are the repo baseline,
  cited source surfaces, and standard mathematics
- NO admitted Boltzmann distribution magnitudes — the Gibbs state is
  derived from MaxEnt principle on the cited Born-density surface via standard
  variational calculus with Lagrange multipliers

## The structural argument

The Probe V conclusion can be stated structurally:

> **MaxEntropy with trace and energy constraints fixes the FUNCTIONAL FORM of
> ρ but not the EXTERNAL PARAMETERS of H.** For
> `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`,
>
> 1. MaxEnt[ρ] subject to `Tr(ρ) = 1`, `Tr(ρH) = E` gives Gibbs
>    `ρ = e^{-βH}/Z` with `β` the Lagrange multiplier dual to `E`.
> 2. The eigenvalues `p_k = e^{-βλ_k}/Z` of ρ are smooth functions
>    of `(a, b, β)`.
> 3. The amplitude `(a, b)` is an EXTERNAL parameter of `H`; it is
>    NOT optimized over by MaxEnt. MaxEnt only optimizes over the
>    state ρ.
> 4. Hence: MaxEnt cannot pin `(a, b)`; it only fixes the form of ρ
>    given `H`.

For BAE (|b|²/a² = 1/2) to be pinned thermodynamically, the cited
source surfaces would need to supply:

1. An additional constraint coupling `a` and `|b|` (e.g., isotype
   equipartition `E_+(H) = E_⊥(H)`).
2. A variational principle that pins this constraint as an extremum
   of free energy.

**Neither is provided by the cited source surfaces.** The trace and energy constraints
are `Tr(ρ) = 1` (probability normalization) and `Tr(ρH) = E` (fixed
energy expectation); these do not impose isotype equipartition.
Imposing `E_+ = E_⊥` is the (1, 1) multiplicity-counting principle,
which is the BAE admission itself, NOT an output of MaxEnt.

## Per-attack-vector analysis

Six independent thermodynamic-invariant routes are tested. All six
preserve the (a, b)-decoupling; none shifts the closure of BAE.

### TH-AV1 — Gibbs state from MaxEnt with trace and energy constraints

**Status: PRESERVES (a, b)-decoupling.**

Standard variational derivation (Jaynes 1957). The Lagrangian is:

```
L[ρ] = -Tr(ρ log ρ) + α (Tr ρ - 1) + β (E - Tr ρH)
```

Setting `δL/δρ = 0`:

```
-log ρ - 1 + α - β H = 0
⟹  ρ = exp(α - 1 - β H) = e^{-β H} / Z
```

where `Z = Tr(e^{-β H})` and `α = 1 - log Z` is the normalization
multiplier.

For the C_3-equivariant circulant `H = aI + bC + b̄C²`, the eigenvalues
are `λ_k = a + 2|b|cos(φ - 2πk/3)`, and Gibbs is diagonal in the C_3
Fourier basis `e_k = (1/√3)(1, ω^k, ω^{2k})`:

```
ρ = sum_k p_k |e_k⟩⟨e_k|     where p_k = e^{-βλ_k} / Z
```

Critically: `p_k` depends on `(a, b, β)` smoothly, but no value of
`(a, b)` is singled out. Sweeping `|b|/a` from 0 to ∞ at fixed
`(a, β)` produces a smooth family of Gibbs states.

**Verified numerically (runner Section 2):**
- 2.1: Eigenvalues match `a + 2|b|cos(φ - 2πk/3)`.
- 2.2: Gibbs distribution `p_k` smooth across BAE point.
- 2.3: At BAE, Gibbs `p_k ≠ (1/3, 1/3, 1/3)` — no isotype equipartition.
- 2.4: `Tr(ρ) = 1`, `Tr(ρH) = E` for sampled `(a, b)`.
- 2.5: MaxEnt with `(Tr=1, Tr-H=E)` does NOT optimize over `(a, b)`.

### TH-AV2 — Liouville on isotype blocks → (1, 2) operator weighting

**Status: PRESERVES (a, b)-decoupling.**

The configuration space `Herm_circ(3)` is 3-real-dim:
`(a, Re b, Im b) ∈ ℝ³`. The C_3 isotype split gives:

- trivial isotype: 1-real-dim (a-axis)
- doublet isotype: 2-real-dim ((Re b, Im b)-plane)

Total: 1 + 2 = 3 real dofs. This is the same `(1, 2)` weighting that
Probe 28 found at the operator level. Equipartition over the 3-coord
flat measure with EQUAL couplings gives `⟨a²⟩ = ⟨(Re b)²⟩ = ⟨(Im b)²⟩
= σ²`, so `⟨|b|²⟩ = 2σ²`, giving `⟨|b|²⟩/⟨a²⟩ = 2` — OPPOSITE of BAE.

For the ratio to be 1/2 (BAE), the couplings must satisfy `k_b = 4 k_a`.
This is yet another way of stating the (1, 1) multiplicity-counting
admission: 1 dof per isotype, weighted equally.

**Verified numerically (runner Section 3):**
- 3.1: Herm_circ(3) is 3-real-dim.
- 3.2: Isotype split (1, 2).
- 3.3: Equipartition over (a, Re b, Im b) gives `⟨|b|²⟩/⟨a²⟩ = 2 k_a/k_b`.
- 3.4: Equipartition does NOT force `k_a/k_b = 1/4`.

### TH-AV3 — Isotype-equipartition E_+ = E_⊥ ↔ BAE

**Status: PRESERVES (a, b)-decoupling at MaxEnt level; isotype
equipartition is the (1, 1) admission.**

BlockTotalFrob source surface
([`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)):

```
E_+(H) = ‖π_+(H)‖_F² = 3 a²    (trivial isotype)
E_⊥(H) = ‖π_⊥(H)‖_F² = 6 |b|²   (doublet isotype)
```

The BAE point `|b|²/a² = 1/2` is precisely `E_+ = E_⊥`:

```
3 a² = 6 |b|²  ⟺  |b|²/a² = 1/2  ⟺  BAE
```

But `E_+ = E_⊥` is NOT implied by `Tr(ρH) = E`. The trace constraint
gives the TOTAL energy expectation:

```
Tr(ρH) = (1/Z) Σ_k λ_k e^{-β λ_k}
```

This is a single equation in the 3 real dofs `(a, Re b, Im b)`. Imposing
`E_+(H) = E_⊥(H)` would require an ADDITIONAL second equation. This
extra constraint is the (1, 1) multiplicity-counting principle that
the MRU weight-class theorem already names as the `(1, 1) → κ = 2`
case. Imposing it ALONE (without MaxEnt) gives BAE algebraically; but
imposing it requires the very admission BAE encodes.

**Verified numerically (runner Section 4):**
- 4.1: `‖H‖_F² = E_+ + E_⊥` for sampled `(a, b)`.
- 4.2: BAE point: `|b|²/a² = 1/2`.
- 4.3: At BAE, `E_+ = E_⊥`.
- 4.4: `Tr(ρH) = E` does NOT imply `E_+ = E_⊥`.
- 4.5: `E_+ = E_⊥` ⟺ `(1, 1)` multiplicity = BAE admission.
- 4.6: `E_+ = E_⊥` algebraically ⟺ `|b|²/a² = 1/2`.

### TH-AV4 — Counting-of-degrees no-bridge

**Status: NAIVE EQUIPARTITION FAILS STRUCTURALLY.**

The naive counting "1 a-mode + 2 b-modes (b and b̄) → equipartition
gives `a² = 2|b|²`" is structurally flawed for THREE reasons:

1. **b and b̄ are conjugates, NOT 2 independent dofs.** `b̄ = conj(b)`
   is determined by `b`; it's the same complex number presented two
   ways. The 3 real dofs of `H` are `(a, Re b, Im b)`.

2. **Equal-coupling equipartition gives `|b|²/a² = 2`, OPPOSITE of
   BAE.** With `⟨a²⟩ = ⟨(Re b)²⟩ = ⟨(Im b)²⟩ = σ²`, we get
   `⟨|b|²⟩ = ⟨(Re b)²⟩ + ⟨(Im b)²⟩ = 2σ² = 2⟨a²⟩`.

3. **The 3 eigenvalues `λ_0, λ_1, λ_2` are NOT 3 independent dofs.**
   They are functions of `(a, |b|, φ)` via the circulant-eigenvalue
   formula: `λ_k = a + 2|b|cos(φ - 2πk/3)`. Constraints: trace `Σ λ_k
   = 3a`, variance `(1/3) Σ (λ_k - a)² = 2|b|²`.

Thus the naive equipartition argument is NOT a derivation from MaxEnt;
it is a heuristic that gets the ratio WRONG (factor-of-4 off) without
the additional `(1, 1)` multiplicity admission.

**Verified numerically (runner Section 5):**
- 5.1: `b̄ = conj(b)`; not independent.
- 5.2: Equal-coupling equipartition gives `|b|²/a² = 2`.
- 5.3: Trace constraint `Σ λ_k = 3a`.
- 5.4: Eigenvalue variance `= 2|b|²`.

### TH-AV5 — Boltzmann/Gibbs has no special structure at BAE

**Status: NO THERMODYNAMIC TRANSITION AT BAE.**

Sweep `|b|/a ∈ [0.05, 1.5]` at fixed `(a=1, β=1)`:

- Free energy `F(|b|) = -(1/β) log Z(β)`: smooth, `F''` bounded.
- Entropy `S(|b|) = -Σ p_k log p_k`: smooth, `S''` bounded.
- Energy `⟨H⟩(|b|) = Σ p_k λ_k`: smooth, `E''` bounded.

None of these has a kink, jump, or critical point at the BAE point
`|b|/a = 1/√2`. The maximum of S over the grid does NOT occur at BAE
(it occurs at `|b| → 0` where eigenvalue spread is smallest, hence
Gibbs is closest to maximally-mixed).

If thermodynamics could pin BAE, we'd expect:

- Free energy minimized at BAE (no — F continues decreasing past BAE).
- Entropy maximized at BAE (no — entropy maximum at `|b| → 0`).
- Phase transition at BAE (no — F, S, E all C^∞).

None of these holds. **No thermodynamic potential singles out BAE.**

**Verified numerically (runner Section 6):**
- 6.1-6.3: F, S, E all smooth across BAE.
- 6.4: No phase transition at BAE.
- 6.5: Max entropy on grid does NOT occur at BAE.

### TH-AV6 — Classical equipartition with explicit H_HO

**Status: COUPLINGS-DEPENDENT, NOT PINNED BY MaxEnt.**

For a classical harmonic-oscillator Hamiltonian on `(a, Re b, Im b)`:

```
H_HO = (1/2) k_a a² + (1/2) k_b (Re b)² + (1/2) k_b (Im b)²
     = (1/2) k_a a² + (1/2) k_b |b|²
```

Maxwell-Boltzmann at temperature `T = 1/β`:

```
⟨a²⟩       = 1 / (β k_a)
⟨(Re b)²⟩ = ⟨(Im b)²⟩ = 1 / (β k_b)
⟨|b|²⟩    = 2 / (β k_b)
```

Ratio:

```
⟨|b|²⟩ / ⟨a²⟩ = 2 k_a / k_b
```

This depends on the EXTERNAL coupling constants `(k_a, k_b)`, NOT on
MaxEntropy itself. To get BAE (ratio 1/2), need `k_b = 4 k_a` —
equivalent to declaring the `(1, 1)` multiplicity admission.

Verified by MC: with `k_a = k_b = 1`, sampled ratio ≈ 2 (not BAE).
With `k_b = 4 k_a`, sampled ratio ≈ 1/2 (BAE), but only because the
input couplings encoded the BAE assumption.

**Verified numerically (runner Section 7):**
- 7.1: Equal-coupling MB: ratio ≈ 2.
- 7.2: `k_b = 4 k_a` MB: ratio ≈ 1/2.
- 7.3: `k_b = 0.5 k_a` MB: ratio ≈ 4.
- 7.4: Classical equipartition depends on couplings, not on MaxEnt.

## Theorem (Probe V thermodynamic-level structural decoupling)

**Theorem (THERMO-DECOUPLE).** Conditional on the physical `Cl(3)`
local algebra, the `Z³` spatial substrate, the cited `C_3[111]` hw=1
BZ-corner forcing surface, the cited `M_3(ℂ)` hw=1 surface, the cited
`C_3`-equivariant Hermitian circulant form
`H = aI + bC + b̄C²`, the cited position-density Born readout
`ρ_grav(x) = ⟨x|ρ̂|x⟩`, the cited KMS/Gibbs-state surface at `β_th`,
and standard mathematical machinery
(variational calculus, Lagrange multipliers, Shannon/von Neumann
entropy):

```
(a) MaxEntropy on Born density restricted to circulants, with
    constraints Tr(ρ) = 1 and Tr(ρH) = E, gives the Gibbs state
    ρ = e^{-βH} / Z
    where β is the Lagrange multiplier dual to E.
    [Verified Sections 1, 2.]

(b) For circulant H, Gibbs is diagonal in the C_3 Fourier basis with
    eigenvalues p_k = e^{-βλ_k}/Z, where λ_k = a + 2|b|cos(φ - 2πk/3).
    The eigenvalues p_k are smooth functions of (a, b, β); MaxEnt
    does NOT optimize over (a, b).
    [Verified Section 2.]

(c) The trace and energy constraints Tr(ρ) = 1 and Tr(ρH) = E impose 2 scalar
    conditions on the 3+1 = 4 real parameters (a, Re b, Im b, β).
    MaxEnt fixes one of these (β as the entropy-maximizer); (a, b)
    remain external.
    [Verified Section 2.]

(d) The cited BlockTotalFrob measure E_+(H) = 3a² (trivial isotype)
    and E_⊥(H) = 6|b|² (doublet isotype) gives ‖H‖_F² = E_+ + E_⊥.
    Imposing isotype-equipartition E_+ = E_⊥ algebraically gives
    3a² = 6|b|² ⟺ |b|²/a² = 1/2 = BAE. But E_+ = E_⊥ is NOT
    implied by Tr(ρH) = E; it is the (1, 1) multiplicity-counting
    admission.
    [Verified Section 4.]

(e) The thermodynamic potentials F = -kT log Z, S = -Tr(ρ log ρ),
    and ⟨H⟩ = Tr(ρH) are all C^∞ functions of (a, b, β). No
    thermodynamic phase transition occurs at the BAE point
    |b|/a = 1/√2. Free energy, entropy, and energy are smooth
    across BAE.
    [Verified Section 6.]

(f) The naive "equipartition" argument "1 a-mode = 2 b-modes summed"
    is structurally flawed: b and b̄ are conjugates (not 2 dofs);
    the 3 eigenvalues are constrained by trace + circulant structure;
    equal-coupling equipartition gives |b|²/a² = 2, OPPOSITE of BAE.
    [Verified Section 5.]

(g) Classical equipartition with explicit H_HO gives
    ⟨|b|²⟩/⟨a²⟩ = 2 k_a/k_b, which depends on EXTERNAL coupling
    constants (k_a, k_b), NOT on MaxEnt. To get BAE, need k_b = 4 k_a
    — equivalent to the (1, 1) multiplicity admission.
    [Verified Section 7.]

Therefore: MaxEntropy on Born density restricted to circulants, with
trace and energy constraints, STRUCTURALLY DECOUPLES from
the continuous amplitude ratio |b|²/a². It cannot supply a constraint
that selects BAE. The thermodynamic-level path (this probe) closes
negatively. This note does not claim broader route-family closure.
The BAE admission count is unchanged. No new admission.
No new axiom.
```

**Proof.** Each item is verified by the runner (64 PASS / 0 FAIL):
Section 0 (input sanity); Section 1 (MaxEnt variational derivation;
Gibbs is entropy maximizer at fixed (Tr, Tr-H)); Section 2 (TH-AV1
Gibbs on circulants); Section 3 (TH-AV2 Liouville on Herm_circ(3));
Section 4 (TH-AV3 isotype-equipartition ↔ BAE); Section 5 (TH-AV4
counting-of-degrees no-bridge); Section 6 (TH-AV5 Boltzmann/Gibbs no
special structure); Section 7 (TH-AV6 classical equipartition);
Section 8 (probe-comparison and claim boundary); Section 9 (convention
robustness); Section 10 (sharpened terminal residue); Section 11
(does-not disclaimers). ∎

## Algebraic root-cause

The thermodynamic decoupling has a clean structural root:

> **MaxEntropy fixes the FUNCTIONAL FORM of ρ (Gibbs) but does not
> fix the EXTERNAL PARAMETERS of H.** For `H = aI + bC + b̄C²`,
> MaxEnt with constraints `Tr(ρ) = 1` and `Tr(ρH) = E` gives
> `ρ = e^{-βH}/Z`, parameterized by `β` (Lagrange multiplier dual to
> `E`). The amplitude `(a, b)` parameterizes `H`, NOT ρ; MaxEnt
> optimizes over the state ρ at fixed `H`, not the other way around.
> No additional thermodynamic principle in the cited source surfaces imposes a
> coupling between `a` and `|b|`.

For BAE to be thermodynamically pinned, the cited source surfaces would need
to supply:

1. An additional thermodynamic constraint coupling `a` and `|b|`
   (e.g., `E_+(H) = E_⊥(H)`).
2. A variational principle that pins this constraint as an extremum
   of free energy.

Neither is provided by the cited source surfaces. The trace and energy constraints
are `Tr(ρ) = 1` and `Tr(ρH) = E`. The cited KMS/Gibbs-state surface
is parameterized by `β_th = 2π/κ`; this fixes the temperature, not
the amplitude `(a, b)`.

## Why this probe is structurally distinct from operator-level probes

| Probe | Layer | Mechanism | Conclusion |
|---|---|---|---|
| Probes 12-30 | OPERATOR (Hilbert states) | C_3 rep theory: (1, 2) real-dim on Herm_circ(3) | F3 canonical, F1 / BAE absent |
| **Probe V** | **THERMODYNAMIC (density operators, MaxEnt)** | **Variational principle: Gibbs ρ ∝ e^{-βH} is smooth in (a, b)** | **(a, b) external to MaxEnt; no thermodynamic pinning** |

Probes 12-30 attacked at the operator level (Hilbert states + operator
algebras). Probe V attacks at the thermodynamic level (MaxEntropy
variational principle, Gibbs distribution, free energy).

The conclusion is the same — F1 / BAE absent — but the **mechanism**
differs: the operator route uses the C_3 isotype split on Herm_circ(3),
while this route uses the Gibbs-state variational structure.

- Operator: real-dim of the C_3 isotype split on Herm_circ(3) is (1, 2).
- Thermodynamic: Gibbs from MaxEnt is parameterized by β, not (a, b).

This note closes only the thermodynamic path against BAE.

## Sharpened terminal residue (thermodynamic route)

For the thermodynamic route tested here:

> **The (1, 1) multiplicity-counting principle required for F1 / BAE
> is not supplied by MaxEntropy / Gibbs structure:**
>
> - **Thermodynamic layer (Probe V, this probe):** MaxEntropy with
>   trace and energy constraints (Tr ρ = 1, Tr ρH = E) gives Gibbs ρ ∝ e^{-βH};
>   the Gibbs state is smooth in (a, b) with no thermodynamic phase
>   transition at BAE. Isotype-equipartition E_+ = E_⊥ is the (1, 1)
>   admission, NOT a consequence of MaxEnt.

Closing BAE therefore requires admitting a multiplicity-counting
principle as a NEW PRIMITIVE — the existing Brannen Amplitude
Equipartition admission. The thermodynamic-level path does not
provide an alternative.

This is a thermodynamic-route rejection only; it should not be read as
ratifying companion route-family claims that are not live source
dependencies of this note.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `no_go` (thermodynamic-level structural
  route rejection; bounded support: MaxEntropy on Born density
  restricted to circulants, with trace and energy constraints, gives Gibbs
  state ρ ∝ e^{-βH}, decoupled from continuous amplitude (a, b))
- audit-derived effective status: set only by the independent audit
  lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe V
  sharpening: **"MaxEntropy on Born density restricted to circulant
  Hamiltonians, with trace and energy constraints (Tr ρ = 1, Tr ρH = E),
  gives the Gibbs state ρ = e^{-βH}/Z. The Gibbs state is smooth in
  (a, b) with no thermodynamic phase transition at BAE. Isotype-
  equipartition E_+ = E_⊥ is algebraically equivalent to BAE but is
  the (1, 1) multiplicity-counting admission, NOT a consequence of
  MaxEntropy with trace and energy constraints."**

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Tests whether MaxEntropy on Born density restricted to circulant
   Hamiltonians, with trace and energy constraints (Tr ρ = 1, Tr ρH = E),
   forces |b|²/a² = 1/2 (BAE).
2. Identifies six independent decoupling theorems (TH-AV1 through
   TH-AV6), each verifying MaxEntropy cannot constrain |b|²/a².
3. Identifies the algebraic root-cause: MaxEntropy fixes the
   FUNCTIONAL FORM of ρ (Gibbs) but does not pin the EXTERNAL
   parameters of H; (a, b) are H's parameters, not the state's.
4. Establishes a sharpened thermodynamic residue: MaxEnt/Gibbs does
   not supply the (1, 1) multiplicity-counting principle required for
   BAE.
5. Cross-references live operator-level probes as context; closes the
   thermodynamic-level gap without relying on missing companion routes.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any source theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT promote external surveys to source authority.
7. Does NOT replace operator-level probes; it complements them at
   a structurally distinct thermodynamic layer.
8. Does NOT propose an alternative κ value as physical.
9. Does NOT promote sister bridge gaps (L3a, L3b, C-iso, W1.exact).
10. Does NOT introduce new physics axioms — uses standard
    mathematical machinery (variational calculus, Lagrange multipliers,
    Shannon/von Neumann entropy) to compute properties of the cited
    Born-density surface on circulant Hamiltonians.
11. Does NOT admit "Boltzmann distribution" as external — derives
    Gibbs from MaxEnt principle via variational calculus.

## Honest assessment

**What the probe finds:**

1. **MaxEntropy on Born density restricted to circulants, with
   trace and energy constraints (Tr ρ = 1, Tr ρH = E), gives Gibbs
   ρ = e^{-βH}/Z.** Standard Jaynes 1957 derivation; Lagrange
   multiplier `β` dual to `E`.

2. **For circulant H, Gibbs is diagonal in C_3 Fourier basis with
   eigenvalues `p_k = e^{-βλ_k}/Z`.** Smooth functions of `(a, b, β)`;
   MaxEnt does NOT optimize over `(a, b)`.

3. **The thermodynamic potentials F, S, ⟨H⟩ are all C^∞ across the
   BAE point.** No phase transition; no critical point; entropy
   maximum on grid does NOT occur at BAE.

4. **Isotype-equipartition `E_+(H) = E_⊥(H)` algebraically gives BAE
   (3a² = 6|b|² ⟺ |b|²/a² = 1/2).** But this is the (1, 1)
   multiplicity-counting admission, NOT a MaxEnt consequence.

5. **Equal-coupling equipartition over `(a, Re b, Im b)` gives
   `⟨|b|²⟩/⟨a²⟩ = 2`, OPPOSITE of BAE.** Naive "1 a-mode + 2 b-modes"
   counting is structurally flawed.

6. **No cited thermodynamic source principle distinguishes BAE.** The
   Gibbs state, KMS condition, and Born density are all smooth in
   `(a, b)`; none singles out `|b|²/a² = 1/2`.

**What this probe contributes to the campaign:**

1. **Bounded support**: MaxEntropy on Born density restricted to
   circulants, with trace and energy constraints, gives Gibbs
   ρ = e^{-βH}/Z; the Gibbs state is smooth in (a, b) with no
   thermodynamic phase transition at BAE. Distinct from any prior
   probe in mechanism and layer.

2. **Sharpened residue characterization**: at the density-operator
   layer, Gibbs-state smoothness in `(a, b)` does not supply the
   (1, 1) multiplicity-counting principle. Operator-level probes remain
   useful context, but this note does not depend on absent companion
   wave-function or topological surfaces.

3. **Thermodynamic route closure**: returns the same route-negative
   obstruction at the variational MaxEntropy level, distinct from the
   operator-level mechanisms.

The remaining residue is **maximally sharp**:

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. The (1, 2) real-dim weighting
> (operator-level) is live context from the cited operator probes; the
> Gibbs state ρ ∝ e^{-βH} (thermodynamic-level) from MaxEntropy with
> trace and energy constraints is parameterized by β (not (a, b)).
> This thermodynamic route does not supply the (1, 1)
> multiplicity-counting principle required for BAE.**

Closing BAE therefore continues to require admitting a multiplicity-
counting principle as a NEW PRIMITIVE — i.e., a new admission or a
new source surface distinct from the existing C_3-equivariant
operator content and the thermodynamic / MaxEntropy content tested
here. Probe V makes this requirement explicit at the variational
layer.

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### C_3 / circulant source surfaces

- BZ-corner forcing (Block 04): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Three-generation observable (M_3 algebra on hw=1): [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Born density / Gibbs / KMS source surfaces

- Born-as-source position-density: [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)
- KMS / Gibbs state on transfer-matrix Hilbert space: [`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)

### Probe campaign — live companion probes

- Probe 28 (operator-level / interacting dynamics): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe 25 (free-Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 18 (F1-vs-F3 algebraic): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)

### Naming convention

- BAE rename note: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

## Validation

```bash
python3 scripts/cl3_koide_v_bae_maxent_2026_05_08_probeV_bae_maxent.py
```

Expected: `=== TOTAL: PASS=64, FAIL=0 ===`

The runner verifies:

1. Section 0 — Input sanity (C_3 cycle is unitary, order 3,
   det = +1; H = aI + bC + b̄C² is Hermitian, C_3-equivariant; Gibbs
   state Tr=1, PSD, commutes with H; Born density non-negative,
   normalized).
2. Section 1 — MaxEnt variational derivation: Gibbs is the entropy
   maximizer at fixed (Tr=1, Tr-rho-H=E), verified by
   constraint-projected random search.
3. Section 2 — TH-AV1: Gibbs on circulants; eigenvalues
   λ_k = a + 2|b|cos(φ - 2πk/3); p_k smooth in (a, b); no
   isotype equipartition at BAE; constraints satisfied; (a, b)
   external to MaxEnt.
4. Section 3 — TH-AV2: Liouville on Herm_circ(3); 3-real-dim
   configuration space; (1, 2) isotype split; equipartition gives
   couplings-dependent ratio.
5. Section 4 — TH-AV3: Block-total Frobenius E_+ = 3a², E_⊥ = 6|b|²;
   E_+ = E_⊥ ⟺ BAE; Tr(ρH) = E does NOT imply E_+ = E_⊥.
6. Section 5 — TH-AV4: counting-of-degrees no-bridge; b̄ = conj(b);
   equal-coupling equipartition gives ratio 2 (NOT BAE);
   eigenvalue trace and variance formulas.
7. Section 6 — TH-AV5: Boltzmann/Gibbs has no kink at BAE; F, S, ⟨H⟩
   all smooth across BAE point; max entropy NOT at BAE.
8. Section 7 — TH-AV6: classical equipartition with H_HO; ratio
   depends on couplings k_a, k_b; verified by MC for multiple cases.
9. Section 8 — probe comparison and claim boundary.
10. Section 9 — Convention robustness (basis change, β sweep, φ
    C_3-symmetry).
11. Section 10 — Sharpened terminal residue for the thermodynamic route.
12. Section 11 — Does-not disclaimers (no BAE closure, no admission,
    no PDG, no source-theorem modification, no new physics axioms).

Total: 64 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically derives the thermodynamic-decoupling from the
  variational structure of MaxEntropy with trace and energy
  constraints, and from the smoothness of the Gibbs distribution
  in (a, b). The decoupling is **structural** (state ρ is Gibbs;
  amplitude (a, b) parameterizes H, not ρ) and is independent of
  any specific (a, b).
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "MaxEntropy with trace and energy constraints can pin
  |b|²/a²" from six independent angles (TH-AV1 Gibbs derivation,
  TH-AV2 Liouville, TH-AV3 isotype-equipartition, TH-AV4
  counting-of-degrees, TH-AV5 Boltzmann smoothness, TH-AV6 classical
  equipartition). All six fail at the same structural locus:
  MaxEnt does not optimize over the external parameters of H.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a no-go route check with bounded
  support; the parent BAE admission remains at its prior
  bounded status; no source-status promotion implied.
- `feedback_physics_loop_corollary_churn.md`: this is structurally
  distinct from the live operator-level probes: those attack operator
  algebra and Hilbert-space structure, while this probe attacks the
  thermodynamic / variational / MaxEntropy level. Although the
  conclusion is the same (no BAE forcing), this is substantive new
  structural content.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional content would be needed
  (an additional multiplicity-counting principle), not how-long.
- `feedback_special_forces_seven_agent_pattern.md`: this probe
  packages a multi-angle attack (six independent TH-AVs) on a
  single load-bearing structural hypothesis (MaxEnt on Born density
  forces BAE), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note proposal + paired runner + cached output, no synthesis
  notes, no lane promotions, no working "Block" notes.
- `feedback_primitives_means_derivations.md`: this probe uses
  standard mathematical machinery (variational calculus, Lagrange
  multipliers, Shannon/von Neumann entropy, Maxwell-Boltzmann
  sampling) — these are **mathematical theorems**, not new physics
  axioms. The probe respects the "no new axioms" constraint by
  deriving thermodynamic consequences from the cited Born-density surface on
  circulant Hamiltonians.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) (hw=1 triplet)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) (H = aI + bC + b̄C²)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) (KoideAlg ⟺ BAE)
- [g_newton_born_as_source_positive_theorem_note_2026-05-10_gnewtonG2](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) (Born density)
- [axiom_first_kms_condition_theorem_note_2026-05-01](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md) (KMS / Gibbs)
- [koide_bae_probe_interacting_dynamics_bounded_obstruction_note_2026-05-09_probe28](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) (operator-level companion)
- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) (free-Gaussian baseline)
- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) (M_3 on hw=1)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
