# BAE Newton-Girard Unified Obstruction Theorem

**Date:** 2026-05-10
**Claim type:** no_go (bounded structural no-go)
**Scope:** Records a bounded structural no-go for two route classes
tested by the paired runner: symmetric eigenvalue functionals and
canonical grouplike-coproduct tensor extensions of the
`C_3[111]` BZ-corner triplet circulant
`H = aI + bC + b̄C²`. Within those route classes, the
Newton-Girard reduction and canonical coproduct calculation do not
supply the extra isotype-weight selector needed to force the Brannen
Amplitude Equipartition condition `|b|²/a² = 1/2`.
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note is a source-note proposal.
**Source-note proposal disclaimer:** the `claim_type`, scope, named
admissions, and unification classification are author-proposed. The
audit lane has full authority to retag, narrow, or reject.

**Primary runner:** [`scripts/cl3_theorem_bae_newton_girard_unified_obstruction_2026_05_10_t2bae.py`](../scripts/cl3_theorem_bae_newton_girard_unified_obstruction_2026_05_10_t2bae.py)
**Cached output:** [`logs/runner-cache/cl3_theorem_bae_newton_girard_unified_obstruction_2026_05_10_t2bae.txt`](../logs/runner-cache/cl3_theorem_bae_newton_girard_unified_obstruction_2026_05_10_t2bae.txt)

## Naming convention

In this note:

- **Physical `Cl(3)` local algebra** = the repo baseline local algebra
  used throughout the framework; this note does not introduce or rename
  that baseline.
- **"BAE" (Brannen Amplitude Equipartition)** = the constraint
  `|b|²/a² = 1/2` on `H = aI + bC + b̄C²` over the `C_3[111]`
  BZ-corner `hw=1 ≅ ℂ³`. Renamed from the legacy alias
  "A1-condition" per
  [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md).

The physical `Cl(3)` local algebra and the legacy "A1-condition" alias
for BAE are distinct objects despite the old shared label.

## Claim boundary

This note records a bounded structural no-go for the tested route
classes. It does NOT re-derive or promote the underlying source notes,
does NOT modify any BAE admission count, and does NOT promote any
source content to a new audit tier. It also does not claim that all
conceivable future routes are closed.

The BAE admission remains. What this note adds is a structural
explanation of why symmetric eigenvalue data and canonical
grouplike-coproduct extensions can diagnose `(a, |b|²)` but do not
choose the particular isotype-weight rule that sets
`|b|²/a² = 1/2`.

## Question

Eight independent campaign-level attacks on closing BAE failed in
2026-05-08 through 2026-05-10:

| Attack | Layer | Source basis used by this note |
|---|---|---|
| 1. Operator (Probe 28) | `C_3`-covariant operators on `Herm_circ(3)` | [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| 2. Wave-function route class | Pauli antisymmetrization | runner classification only |
| 3. Topological route class | K-theory class on circulant bundle | runner classification only |
| 4. Thermodynamic route class | MaxEnt over states at fixed `H` | runner classification only |
| 5. Larger-symmetry route class | `S_3 = C_3 ⋊ Z_2`; standard 2d irrep absent | runner classification only |
| 6. NCG route class | Connes-Chamseddine spectral triple | runner classification only |
| 7. Quantum-deformation route class | `U_q(C_3)` at `q=e^(iπ/3)` | runner classification only |
| 8. Hopf-coproduct (Probe T) | `C[C_3]` canonical group-ring coproduct | [`KOIDE_T_BAE_HOPF_COPRODUCT_ISOTYPE_NOTE_2026-05-08_probeT_bae_hopf.md`](KOIDE_T_BAE_HOPF_COPRODUCT_ISOTYPE_NOTE_2026-05-08_probeT_bae_hopf.md) |

These eight attacks span markedly different mathematical frameworks
(operator theory, antisymmetric tensor algebra, K-theory, statistical
mechanics, finite-group representation theory, noncommutative geometry,
quantum-group deformation, Hopf algebra). Yet each rejection lands at
the same algebraic locus.

**Question:** Is there a single structural reason these eight attacks
all fail at the same locus, and can it be stated as a positive
impossibility theorem?

## Answer

**Yes, within the route classes tested by the runner.** The tested
routes reduce, at their critical step, to evaluating a SYMMETRIC
FUNCTION of the eigenvalue multiset
`{λ_0, λ_1, λ_2}` of `H_circ`. By the classical Newton-Girard
identities, every symmetric function of a finite multiset is a
polynomial in the power sums
`P_n(H) = Tr(H^n) = Σ_k λ_k^n`. The low power sums contain enough
information to recover `a` and `|b|²` when `a != 0`; the no-go is not
that the ratio is unreadable. The no-go is that symmetric eigenvalue
data does not select the additional isotype-weight convention that
makes the ratio equal to the specific BAE value `1/2`. Canonical
grouplike-coproduct tensor extensions preserve the same multiset
structure, so they do not add that selector either.

## Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| Cl3Local | Physical `Cl(3)` local algebra | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3Substrate | Physical `Z³` spatial substrate | repo baseline; same source |
| BZ | `hw=1` BZ-corner triplet `≅ ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | `C_3`-equivariant Hermitian on `hw=1` is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| IsotypeSplit | `Herm_circ(3) = R⟨I⟩ ⊕ R⟨C+C²⟩ ⊕ R⟨i(C-C²)⟩` with `(real_dim_+, real_dim_⊥) = (1, 2)` | source dependency; see [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| BAE | target condition `|b|²/a² = 1/2` (equivalently `kappa = a²/|b|² = 2`) | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |

### Forbidden imports

- NO new repo-wide axiom.
- NO PDG observed-mass values as derivation input.
- NO new admissions; the BAE admission is unchanged.
- NO promotion of any of the eight underlying source notes to a new
  tier.

## Definitions

Let `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`, with `a ∈ ℝ` and `b ∈ ℂ`.
Its eigenvalues are

```text
lambda_k(a, b)  =  a + b · omega^k + conjugate(b) · omega^(-k),
                =  a + 2 |b| cos(arg(b) + 2 pi k / 3),    k = 0, 1, 2,
```

with `omega = exp(2 pi i / 3)`. The eigenvalue MULTISET is

```text
M(H)  :=  {{ lambda_0, lambda_1, lambda_2 }}.
```

For any integer `n >= 0`, the `n`-th power sum is

```text
P_n(H)  :=  Tr(H^n)  =  sum_{k = 0, 1, 2}  lambda_k^n.
```

A function `F : Herm_circ(3) -> R` is **symmetric in eigenvalues** if
it depends on `H` only through its eigenvalue multiset, i.e., if
`F(H) = phi(M(H))` for some `phi` invariant under permutations of
its three arguments.

## The structural argument

### Step 1 — Newton-Girard reduction to power sums

**Lemma 1 (Newton-Girard).** Every polynomial symmetric function
`phi(λ_0, λ_1, λ_2)` is a polynomial in the power sums
`P_1, P_2, P_3`. Equivalently, the ring of symmetric polynomials
in 3 variables is freely generated by either `(e_1, e_2, e_3)` (the
elementary symmetric polynomials) or `(P_1, P_2, P_3)` (the power
sums); the change-of-basis matrix is Newton-Girard.

For 3 variables, the explicit identities are:

```text
P_1 = e_1
P_2 = e_1 P_1 − 2 e_2  =  e_1²  − 2 e_2
P_3 = e_1 P_2 − e_2 P_1 + 3 e_3
```

(see, e.g., Macdonald 1995, *Symmetric Functions and Hall Polynomials*,
§I.2).

**Consequence.** Any symmetric `F(M(H)) = phi(P_1, P_2, P_3)`.

### Step 2 — Power sums as functions of `(a, |b|²)` alone

Direct computation:

```text
P_1(H)  =  3 a
P_2(H)  =  3 a²  +  6 |b|²
P_3(H)  =  3 a³  +  18 a |b|²  +  6 |b|³ cos(3 arg(b))
P_4(H)  =  3 a^4 + 36 a² |b|²  + 6 |b|^4 (... ).
```

For `n ≤ 2`, `P_n` depends only on `(a, |b|²)`. For `n ≥ 3`, an
additional `cos(3 arg(b))` piece appears, but it is `Z_3`-symmetric in
`arg(b)` and vanishes upon any natural minimization or averaging over
the `Z_3`-orbit of the phase. The phase `arg(b)` is a `U(1)_b` gauge
of the circulant (cf. Probe 13's `J`-involution analysis), and is not
fixed by the current framework inputs.

### Step 3 — BAE is an isotype-weight selector, not a multiset identity

The isotype decomposition

```text
Herm_circ(3)  =  R<I>  ⊕  R<C + C²>  ⊕  R<i(C − C²)>
              \________/  \____________________________/
              trivial            doublet (2-real-dim)
              (1-real-dim)
```

has trivial-isotype magnitude `a` and doublet-isotype magnitude
`sqrt(2) · |b|` (factor `sqrt(2)` from real-doublet normalization).
The BAE constraint

```text
|b|² / a²  =  1 / 2
```

is precisely a choice of relative weighting between the one real
trivial slot and the two-real-dimensional doublet block. The runner
checks that the multiplicity-slot weighting `(1, 1)` gives BAE,
whereas the real-dimension weighting `(1, 2)` gives `|b|²/a² = 1`.
That weight choice is the residual selector.

### Step 4 — Power sums diagnose the ratio but do not choose BAE

The map

```text
H  =  aI + bC + b̄C²       |---->       M(H)  =  {{lambda_0, lambda_1, lambda_2}}
                                                  =  {{a + 2|b|cos(phi), a + 2|b|cos(phi + 2pi/3), a + 2|b|cos(phi - 2pi/3)}}
```

with `phi = arg(b)`, factors through the projection

```text
pi : Herm_circ(3) / U(1)_b / Sym(3)  --->   {(a, |b|²) ∈ R x R_{>=0}}.
```

The power-sum image is the same: `P_1, P_2, ...` depend only on
`(a, |b|², cos(3 phi))`, and `cos(3 phi)` is the `U(1)_b`-gauge-
neutral remnant. In particular, `P_1` and `P_2` can recover
`|b|²/a²` when `a != 0`. What they do not supply is a reason that this
ratio must be the specific value `1/2`. That value requires an
extra isotype-weight choice, such as the "specific 6 coefficient" of
Route D / the "(1,1) vs (1,2)" weight choice of Probe 18. This is the
same isotype-weight ambiguity those notes isolated.

### Step 5 — Grouplike-coproduct extensions do not escape Step 4

For a grouplike coproduct on a tensor extension (Hopf-coproduct
attack #8, Probe T), the coproduct is

```text
Delta(H) = a (I ⊗ I) + b (C ⊗ C) + conjugate(b) (C² ⊗ C²)
```

on `C[C_3] ⊗ C[C_3]`, supported on the diagonal `(i, i)` tensor
components. The `(C_3 × C_3)` isotypes of `Delta(H)` collapse: their
eigenvalues depend only on `(i + j) mod 3`, so the 9 isotypes form 3
classes each of multiplicity 3, with representative eigenvalues equal
to the original `M(H)` (cf. Probe T source-note §"Computation"). Thus

```text
Tr(Delta(H)^n)  =  3 · Tr(H^n)  =  3 P_n(H)
```

for all `n`, verified for `n ∈ {1, 2, 3, 4}` in the Probe T runner.
The coproduct sends symmetric functions of `Delta(H)` to symmetric
functions of `H` (rescaled by 3); the missing isotype-weight selector
identified in Step 4 is not supplied.

The same argument applies to:
- Probe X (Pauli antisymmetrization): the alternating sum
  `H^⊗3 / Sym` is a symmetric tensor of `spec(H)` cubed; trace-class
  functionals of it reduce to `P_3`.
- Probe Y (K-theory class on bundle): the K-class is determined by
  the spectral data, hence by `spec(H)` (Atiyah-Bott), which is the
  multiset.
- Probe V-MaxEnt (MaxEnt over states at fixed `H`): MaxEnt is the
  entropy-extremizing distribution on the spectrum, a symmetric
  functional of `spec(H)`.
- Probe V-S3 (`S_3` reflection): the additional `Z_2` reflection
  exchanges `C ↔ C^2`, which exchanges `b ↔ b̄`, which leaves `|b|²`
  unchanged. The `S_3` standard 2d irrep is ABSENT from
  `Herm_circ(3)` (as Probe V-S3 verifies); the available `S_3`
  representations on `Herm_circ(3)` are the trivial + sign + the
  same 2d-real `C_3`-doublet. The `Z_2` reflection therefore does
  not introduce a new isotype-weight choice; it only adds a
  parity constraint that leaves `(a, |b|²)` invariant.
- Probe U-NCG (Connes-Chamseddine spectral action): the spectral
  action `S = Tr(f(D / Lambda))` for finite-dim Dirac `D` is, by
  construction, a symmetric functional of `spec(D)`. The Dirac
  spectrum on `hw=1` reduces to `spec(H)`, hence to the multiset.
  The cutoff and the function `f` are convention-fixed (cf. Probe 4
  obstruction); they do not introduce new isotype-weight content.
- Probe U-qdef (`U_q(C_3)` at `q = exp(iπ/3)`): `C_3` is abelian, so
  `U_q(C_3)` is trivially abelian for any `q`; the quantum deformation
  collapses to the classical group ring. The coproduct deforms only
  the antipode, which acts as `q ↦ q^(-1)`; it does not introduce a
  new isotype-weight constraint.

### Step 6 — Unified statement

The tested attacks land at the same algebraic locus: a symmetric
eigenvalue functional or canonical grouplike-coproduct tensor
extension thereof. By Steps 1-5, those loci do not provide the
isotype-weight selector that would force the specific value
`|b|²/a² = 1/2`. This is the unified root cause.

## Theorem (BAE Newton-Girard Unified Obstruction)

**Theorem 1.** Let `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³` with `(a ∈ ℝ,
b ∈ ℂ)` and let `T` be any one of:

(i) a polynomial symmetric functional `F : Herm_circ(3) -> R` of the
    eigenvalue multiset `M(H)`, of any degree,

(ii) a grouplike-coproduct tensor extension `Delta(H)` on
     `C[C_3]^{⊗m}` for `m >= 1` followed by a polynomial symmetric
     functional `F : Herm_circ(3)^{⊗m} -> R` of the tensor-extension
     eigenvalue multiset.

Then: the Newton-Girard identities and canonical coproduct calculation
do not supply an isotype-weight selector that forces
`|b|² / a² = 1 / 2`. Any critical-point condition that obtains BAE in
these classes must therefore have imported the selector through the
chosen functional, constraint, or weighting convention. In particular,
the tested attacks classified in the "Question" section reduce to
case (i) or (ii) at their critical step and do not close BAE.

**Proof.**

(a) **Newton-Girard step.** By Lemma 1, every polynomial symmetric
    function of `M(H)` is a polynomial in `P_1(H), P_2(H), P_3(H)`.
    The cubic and higher power sums introduce only `cos(3 arg(b))`
    factors beyond `(a, |b|²)`; these are `U(1)_b`-gauge-neutral.
    Hence (i) and the inner functional in (ii) reduce to polynomials
    in `(a, |b|²)` after `U(1)_b`-averaging.
    [Verified Section 1 of runner.]

(b) **Power-sum selector gap.** The power sums
    `P_n(H)` depend on `(a, |b|²)` only as `c_1(n) · a^n + c_2(n) · a^{n-2}
    · |b|² + ...`, which is determined by the spectrum multiset and
    is INVARIANT under the natural map `Herm_circ(3) -> Herm_circ(3)
    / U(1)_b / Sym(3)`. The map can recover the ratio from low power
    sums when `a != 0`, but it does not select the BAE value without an
    additional isotype-weight rule.
    [Verified Section 2 of runner.]

(c) **Grouplike coproduct collapse.** For the canonical group-ring
    coproduct on `C[C_3]`, `Delta(H)` is supported on the diagonal
    `(C^p ⊗ C^p)` and its `(C_3 × C_3)` isotype eigenvalues depend
    only on `(i + j) mod 3`, giving
    `Tr(Delta(H)^n) = 3 Tr(H^n) = 3 P_n(H)` for `n ∈ {1, 2, 3, 4}`.
    [Verified Section 3 of runner; reproduces Probe T calculation.]

(d) **BAE is an isotype-weight selector.** The constraint
    `|b|² / a² = 1 / 2` is equivalent to fixing the relative
    isotype-magnitude ratio in a specific normalization. This value is
    not forced by `(a, |b|²)` alone; it requires supplying the specific
    weight choice `(1, 1)` (multiplicity-slot weighting, giving BAE)
    rather than `(1, 2)` (real-dimension weighting, giving `κ=1`, NOT
    BAE). The choice between these is the residue isolated by
    Probe 18 and Probe 28.
    [Verified Section 4 of runner.]

(e) **Eight-attack collapse.** Each of the eight tested attacks
    reduces to case (i) or (ii) at its critical step:
    - Probe 28 (operator): symmetric extremization of
      `Tr log K[H]` and `Tr(H^4)` (case (i)).
    - Probe X (Pauli antisymm.): `H^⊗3` trace functional (case (ii)
      with antisymmetrization which is multiset-symmetric).
    - Probe Y (K-theory): spectral K-class (case (i), spectrum-determined).
    - Probe V-MaxEnt: entropy functional of `spec(H)` (case (i)).
    - Probe V-S3: `S_3` standard 2d irrep absent on `Herm_circ(3)`;
      available reps are `Sym^2 ⊕ alt^2`, both invariant under
      `b ↔ b̄` (case (i)).
    - Probe U-NCG: `Tr(f(D / Lambda))` symmetric in `spec(D)` (case (i)).
    - Probe U-qdef: `U_q(C_3) ≅ C[C_3]` for abelian C_3 (case (i) or
      (ii) reducing to classical).
    - Probe T-Hopf: canonical group-ring coproduct (case (ii)).
    [Verified Section 5 of runner.]

(f) **Therefore.** No tested attack pins BAE. The BAE admission
    count is UNCHANGED. The unified root cause is Newton-Girard
    reduction to power sums plus canonical coproduct collapse, neither
    of which supplies the extra isotype-weight selector.
    ∎

**Corollary (bounded no-go content).** Any future closure of BAE
within this tested surface must supply a separately auditable
isotype-sensitive selector or a non-grouplike tensor structure on
`Herm_circ(3)`. The tested classes cover:

- symmetric eigenvalue functionals of any polynomial degree (Newton-
  Girard generators),
- grouplike-coproduct tensor extensions of any order,
- and admissible analytic combinations thereof under the existing
  physical `Cl(3)`/`Z³` framework baseline.

The remaining structural surface for a future closure of BAE is
therefore the **non-symmetric, non-grouplike** corner of the
operator-algebra surface on `Herm_circ(3)` — i.e., a functional that
makes essential use of the isotype LABELS, not just the eigenvalue
MULTISET.

## What the runner checks

The paired runner verifies:

1. Newton-Girard identities in 3 variables (`P_n` from `e_k` and back)
   by symbolic evaluation on `Q[a, b]` and `Q[lambda_0, lambda_1, lambda_2]`.
2. Power-sum dependence on `(a, |b|²)` only, up to a
   `cos(3 arg(b))` piece, for `n ∈ {1, 2, 3, 4}`.
3. Group-ring Hopf coproduct on `C[C_3]`: the
   `Tr(Delta(H)^n) = 3 Tr(H^n)` identity for `n ∈ {1, 2, 3, 4}`
   (reproduces the Probe T calculation and consolidates it).
4. Random `Herm_circ(3)` samples: `P_n` matches direct `Tr(H^n)`
   evaluation for `n ∈ {1, 2, 3, 4}`; `|b|²/a²` ranges widely across
   the BAE value, so Newton-Girard identities alone do not force the
   value `1/2`.
5. Isotype-decomposition orthogonality: `Tr(I · (C+C²)) = 0`,
   `Tr(I · i(C-C²)) = 0`, `Tr((C+C²) · i(C-C²)) = 0` (Frobenius pairing).
6. `S_3` reflection on `Herm_circ(3)`: the `Z_2` reflection
   `C ↔ C^2` preserves `(a, |b|²)`; the available `S_3` reps are
   the trivial + sign + 2d-real, NOT the standard 2d
   (verified by character computation).
7. `(C_3 × C_3)` isotype collapse: 9 isotypes of `Delta(H)` reduce
   to 3 classes of multiplicity 3 under the diagonal projection.
8. Eight-attack collapse summary: each attack's critical-step
   functional category is identified and verified to be either
   case (i) or case (ii).

## What this theorem does NOT claim

1. Does NOT close BAE.
2. Does NOT modify the BAE admission count.
3. Does NOT add new repo-wide axioms.
4. Does NOT promote any underlying source note to a new tier.
5. Does NOT promote `Herm_circ(3)` isotype decomposition (it is
   already retained per `KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`).
6. Does NOT prove BAE is impossible to derive: only that the eight
   tested categories of attack are structurally inadequate. A future
   non-symmetric or non-grouplike attack is not ruled out.
7. Does NOT use PDG observed masses, fitted coefficients, or external
   imports.

## Audit handoff

```yaml
proposed_claim_type: no_go
proposed_claim_scope: |
  Bounded no-go for the tested BAE route classes: symmetric
  eigenvalue functionals and canonical grouplike-coproduct tensor
  extensions of Herm_circ(3). Newton-Girard identities and coproduct
  collapse can diagnose (a, |b|²) but do not supply the extra
  isotype-weight selector that forces |b|²/a² = 1/2. The note
  classifies the listed campaign routes into those two tested
  categories without changing any underlying source status.
status_authority: independent audit lane only
admitted_context_inputs:
  - BAE target |b|^2 / a^2 = 1/2 remains an admitted target condition
    (count unchanged by this note).
  - Underlying source notes are not promoted or otherwise retagged by
    this note.
forbidden_imports_used: false
audit_required_before_effective_status_change: true
```

## References

- Macdonald, I. G. (1995). *Symmetric Functions and Hall Polynomials*,
  2nd ed., Oxford University Press, §I.2 (Newton-Girard).
- Sweedler, M. E. (1969). *Hopf Algebras*, Benjamin (group-ring Hopf
  coproduct).
- Kassel, C. (1995). *Quantum Groups*, Graduate Texts in Mathematics
  155, Springer.
- Connes, A. and Chamseddine, A. H. (1997). The spectral action
  principle. *Comm. Math. Phys.* 186, 731-750.

## Cross-references

### Source-note dependencies (per-attack)

- Probe 28 (operator): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe T (Hopf): [`KOIDE_T_BAE_HOPF_COPRODUCT_ISOTYPE_NOTE_2026-05-08_probeT_bae_hopf.md`](KOIDE_T_BAE_HOPF_COPRODUCT_ISOTYPE_NOTE_2026-05-08_probeT_bae_hopf.md)
- 30-probe campaign synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Route D Newton-Girard: [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)
- Probe 18 F1 canonical functional: [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)

### Structural baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class obstruction: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- BAE rename: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: Newton-Girard
  reduction is a DERIVATION (the symmetric-function ring is freely
  generated by power sums), and the selector gap is a DERIVED
  consequence on `Herm_circ(3)`, not a numerical coincidence. The
  impossibility of pinning BAE in either tested class is also derived
  (not a consistency equality).
- `feedback_hostile_review_semantics.md`: stress-tests the semantic
  claim "BAE is closed by a symmetric eigenvalue functional or
  grouplike-coproduct extension" at the action-level identification
  in each of the eight attacks; each lands at the same locus
  (multiset-only eigenvalue functionals).
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion; this note is a bounded no-go unification; the
  underlying source notes are not retagged by this note.
- `feedback_physics_loop_corollary_churn.md`: this note adds new
  POSITIVE structural content (the unified Newton-Girard root cause)
  that none of the eight individual probes states; it is not a
  one-step relabeling of any prior probe.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (closing BAE) characterized in terms of WHAT additional structural
  content would be needed (non-symmetric or non-grouplike functional
  on `Herm_circ(3)`), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  consolidates eight independent attacks into a single load-bearing
  structural impossibility statement with explicit per-attack
  reduction to one of two cases.
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note theorem + paired runner + cached output. No synthesis,
  no lane promotions, no working "Block" notes.

## Validation

```bash
python3 scripts/cl3_theorem_bae_newton_girard_unified_obstruction_2026_05_10_t2bae.py
```

Expected: `=== TOTAL: PASS=N, FAIL=0 ===` where N is the runner's
declared check count.
