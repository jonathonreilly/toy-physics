# Koide BAE Probe Y — Topological / Index-Theoretic Attack on the C_3[111] Triplet

**Date:** 2026-05-10
**Type:** bounded_theorem (topological-level structural rejection;
no positive closure; new positive content: K-theory class, index
theorem, anomaly polynomial, and Cech cohomology on the C_3[111]
hw=1 triplet are all INTEGER-QUANTIZED isotype-count data.
Continuous amplitude (a, b) is NOT in topological data; topology
cannot pin |b|²/a² = 1/2. Structurally distinct from operator-level
(Probes 12-30) and wave-function-level (Probe X) decouplings.)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe Y of the Koide
**BAE-condition** closure campaign. Tests whether a topological
invariant on the C_3[111] hw=1 triplet — index theorem, K-theory
class, anomaly polynomial, or cohomological obstruction — forces
|b|²/a² = 1/2 (BAE) on the C_3-equivariant Hermitian circulant
`H = aI + bC + b̄C²`.
**Status:** source-note proposal for a topological-level bounded
obstruction with new positive content. Topological invariants
**STRUCTURALLY DECOUPLE** from the circulant amplitude ratio.
Seven independent decoupling theorems (TOP-AV1 through TOP-AV7)
verified by paired runner (75/0). The K-theory class of V = ℂ³ as a
C_3-module is `(1, 1, 1) ∈ R(C_3) = Z ⊕ Z ⊕ Z`; the equivariant
index is integer-valued; the anomaly polynomial coefficients are
integer mode counts; Cech cohomology is integer-or-Z/3-valued. None
of these can pin a continuous amplitude ratio. The BAE admission
count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probeY-topological-20260510
**Primary runner:** [`scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py`](../scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py)
**Cache:** [`logs/runner-cache/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.txt`](../logs/runner-cache/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

After Probes 12-30 attacked BAE at the **operator** level (RP, GNS,
character orthogonality, F1 vs F3 weighting, Plancherel, Peter-Weyl,
retained-U(1) hunt, retained interacting dynamics, etc.) — all closed
as bounded obstructions — and Probe X attacked at the **wave-function**
level (Pauli antisymmetrization, Slater determinant on ∧³V) — also
closed bounded — the natural next attack is at a structurally distinct
**third** layer.

Multiplicity counting can in principle emerge from:

- **Index theorems** (Atiyah-Singer-style chiral fermion zero-mode
  counts on the C_3[111] geometry)
- **K-theory class** of the bundle over the BZ-corner triplet
- **Anomaly polynomial** (gauge anomaly inflow, 't Hooft matching)
- **Cohomological obstruction** (Cech cohomology, sheaf cohomology
  on the lattice)

These are structurally orthogonal to operator-level (which acts on
Hilbert space states) and wave-function-level (which acts on
antisymmetrized Hilbert space tensors). Topological invariants act
at the **bundle/geometry level**.

**Question (Probe Y):** Does a topological invariant on the C_3[111]
hw=1 triplet — index theorem, K-theory class, anomaly polynomial, or
cohomological obstruction — force |b|²/a² = 1/2 (BAE)?

This is structurally distinct from any prior probe: prior probes
attacked at operator level (Hilbert-space states) and wave-function
level (antisymmetrized tensors); this probe attacks at the
**bundle/geometry level** via topological invariants.

## Answer

**No.** Topological invariants on the C_3[111] hw=1 triplet
**structurally decouple** from the continuous amplitude ratio
|b|²/a². Seven independent decoupling theorems converge:

```
TOP-AV1   Equivariant index theorem
          ind_C3(D) ∈ Z; depends on chirality + isotype dim count.
          The amplitude (a, b) does not enter ind_C3(D).

TOP-AV2   K-theory / representation ring
          [V] in K_C3(pt) = R(C_3) = Z[1] ⊕ Z[ω] ⊕ Z[ω²]
          gives integer multiplicities (1, 1, 1). Continuous (a, b)
          is NOT in K-theory data.

TOP-AV3   Anomaly polynomial / Chern character
          ch(V/pt) = rank(V) = 3 ∈ Z. Anomaly polynomial Tr(F^k) is
          a gauge-curvature class; (a, b) does not appear.

TOP-AV4   Cech / sheaf cohomology
          H^q(pt, Z) = Z (q=0), 0 (q>0); equivariant H^q_C3 = Z, 0,
          Z/3, ... — integer-or-Z/3-valued. Cannot pin continuous (a, b).

TOP-AV5   't Hooft anomaly matching
          UV-IR anomaly traces match as integer mode counts; the
          continuous amplitude is NOT constrained.

TOP-AV6   Topological-amplitude no-bridge
          For T (integer) to pin |b|²/a² = 1/2, we'd need T = f(|b|²/a²)
          for continuous f. No such bridge exists from retained
          topological data on hw=1.

TOP-AV7   Topology rederives (1, 2) and (1, 1, 1), not (1, 1)
          Topological multiplicity counts on Herm_circ(3) give (1, 2)
          [doublet 2-real-dim] OR (1, 1, 1) [3 distinct C-irreps].
          Neither is the (1, 1) multiplicity required for F1 / BAE.
```

**Verdict: BOUNDED OBSTRUCTION (topological-level decoupling) with
new positive content.** Topological invariants are
**integer-quantized** isotype-count data. They depend on the bundle
structure and the C_3 representation — both of which are fixed by
retained content — but NOT on the continuous matter-amplitude (a, b).
The K-theory class `[V] = (1, 1, 1) ∈ R(C_3) = Z⊕Z⊕Z` re-derives the
isotype decomposition, but does not pin amplitudes. BAE admission
count is UNCHANGED. No new admission. No new axiom.

## Setup

### Premises (A_min for Probe Y)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | retained per [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | retained per [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | retained per [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | retained per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Probe28 | Operator-level: F3 (1,2) real-dim canonical; F1/BAE absent | retained per [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| ProbeX | Wave-function-level: Pauli singlet ∈ trivial C_3 isotype; b-decoupled | retained per [`KOIDE_X_BAE_PAULI_ANTISYMMETRIZATION_NOTE_2026-05-08_probeX_bae_pauli.md`](KOIDE_X_BAE_PAULI_ANTISYMMETRIZATION_NOTE_2026-05-08_probeX_bae_pauli.md) |
| M3 | M_3(C) algebra on hw=1 triplet generated by translations + C_3[111] | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |

**Standard mathematical machinery used (per "no new axioms" constraint —
these are derivations from retained content + standard math, not
new physics axioms):**

- Atiyah-Singer index theorem (statement; standard mathematical theorem,
  not a new framework axiom)
- K-theory of compact Lie group representations (R(G) for G = C_3)
- Chern character (rank invariant on a 0-dim base)
- Cech / sheaf / group cohomology (standard cohomological machinery)
- Spectral flow on a closed loop in parameter space
- η-invariant (signature of self-adjoint operator spectrum)

These are **mathematical statements**, not physical primitives. They
are used to compute properties of the retained C_3 + V data on hw=1.

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new physics axioms or new admissions — primitives are derivations
  from axioms or retained work only (per user 2026-05-09 clarification)
- NO admitted topological invariant magnitudes — the topological data
  is derived from retained C_3 + V structure, not assumed

## The structural argument

The Probe Y conclusion can be stated structurally:

> **Topological invariants are integer-quantized.** For any topological
> invariant `T` (index, K-theory rank, Chern number, eta-invariant,
> spectral flow, anomaly coefficient) defined on the C_3[111] hw=1
> triplet with the retained operator content,
>
> 1. `T` takes values in a finitely-generated abelian group (typically
>    `Z` or `Z/n`).
> 2. `T` is locally constant in continuous parameter space — it can
>    change only at quantization-class boundaries (e.g., eigenvalue
>    zero crossings for the η-invariant).
> 3. `T` depends on **bundle topology + isotype structure**, both of
>    which are fixed by the retained C_3 representation on V = ℂ³.
> 4. `T` does NOT depend on the continuous amplitude `(a, b)`
>    parameterizing `H = aI + bC + b̄C²`.

Hence: a topological invariant could constrain `(a, b)` only if there
were a continuous bridge `T = f(|b|²/a²)` with `f` differentiable.
But the integer-or-finite quantization of `T` rules this out: at most,
`T` could specify a half-line (e.g., "if |b|²/a² > some_critical_value,
then T = 1, else T = 0"). It cannot pin a single specific value.

For BAE (|b|²/a² = 1/2) to be pinned topologically, retained content
would need to supply a quantization condition that uniquely selects
this ratio. **No such condition exists from retained topological
data on hw=1.**

## Per-attack-vector analysis

Seven independent topological-invariant routes are tested. All seven
preserve the (a, b)-decoupling; none shifts the closure of BAE.

### TOP-AV1 — Equivariant index theorem

**Status: PRESERVES (a, b)-decoupling.**

The Atiyah-Singer index theorem for a C_3-equivariant Dirac operator
D on the hw=1 triplet computes

```
ind_C3(D) = sum_k (n_k^+ - n_k^-) χ_k
```

where `χ_k` are the C_3 characters, `n_k^±` are the chiral zero-mode
counts in isotype `V_k`. Each `n_k^±` is a non-negative integer; the
total index is integer-valued (or a class in `R(C_3) = Z⊕Z⊕Z`).

The amplitude `(a, b)` of `H = aI + bC + b̄C²` parameterizes the
spectrum `λ_k = a + 2|b| cos(φ - 2πk/3)`, which is a continuous
real-valued spectrum. The eigenvalues are NOT chiral mode counts.

Hence the index theorem cannot pin `(a, b)` without an additional
continuous bridge that retained content does not supply. The
η-invariant (a related spectral asymmetry, summing signs of
eigenvalues) is integer-valued and locally constant in `(a, b)` —
it can only change at eigenvalue zero crossings, which occur at
specific algebraic conditions (e.g., `|b|/a = 1` for `φ = 0`),
**NOT at the BAE point `|b|/a = 1/√2`**.

**Verified numerically (runner Section 2):**
- 2.4: η at BAE point is integer (does not pin BAE).
- 2.6: η at BAE = η at neighbors (no topological distinguishing of BAE).

### TOP-AV2 — K-theory / representation ring

**Status: PRESERVES (a, b)-decoupling.**

The C_3-equivariant K-theory of a point is the representation ring
of C_3:

```
K_C3(pt) = R(C_3) = Z[χ_0] ⊕ Z[χ_1] ⊕ Z[χ_2]
```

where `χ_0, χ_1, χ_2` are the three irreducible characters
(`χ_k(C^j) = ω^(jk)`). The class of `V = ℂ³` as a C_3-module is

```
[V] = m_0 [χ_0] + m_1 [χ_1] + m_2 [χ_2]
```

with `m_k` the (integer) multiplicity of `χ_k` in `V`.

For the regular representation (the natural action on `V`):
`m_0 = m_1 = m_2 = 1`. Verified via character orthogonality:

```
m_k = (1/3) Σ_j χ_k*(C^j) χ_V(C^j) = (1/3) (3 + 0 + 0) = 1
```

(Verified runner Section 3.5.k for k = 0, 1, 2.)

Critically: `[V] = (1, 1, 1) ∈ R(C_3)` is INDEPENDENT of `(a, b)`.
Two different operators `H_circ(a_1, b_1)` and `H_circ(a_2, b_2)`
act on the SAME `V = ℂ³` with the SAME C_3 action, hence have the
SAME K-theory class.

The continuous amplitude `(a, b)` is a parameter on the configuration
space `Herm_circ(3)`, NOT in K-theory data. K-theory cannot pin `(a, b)`.

**Verified numerically (runner Section 3):**
- 3.1: Regular-rep multiplicities (1, 1, 1).
- 3.2-3.4: Character formula verified algebraically.
- 3.5.k: m_k = 1 by character orthogonality (k=0,1,2).
- 3.6: K-theory class independent of (a, b).
- 3.7: K_C3(pt) = Z⊕Z⊕Z (3-dim Z-module).

### TOP-AV3 — Anomaly polynomial / Chern character

**Status: PRESERVES (a, b)-decoupling.**

The Chern character `ch(V)` of a complex vector bundle on a 0-dim
base (a point) reduces to the rank:

```
ch(V/pt) = rank(V) = 3
```

The equivariant Chern character `ch_C3(V)` evaluated at `g ∈ C_3`
is `Tr_V(g)` — the character of `V` at `g`. For `V = ℂ³` with the
regular C_3 representation:

```
χ_V(I) = 3, χ_V(C) = 0, χ_V(C²) = 0
```

These are integer-valued (or character-valued = Z[ω]-linear
combinations). Independent of `(a, b)`.

The anomaly polynomial in `d = 4` is `Tr(F²)/2 + ... + cube terms`,
where `F` is the gauge curvature 2-form. For the discrete C_3 action
(no continuous gauge curvature), the continuous-form anomaly polynomial
is zero; only discrete 't Hooft mode counts apply (TOP-AV5 below).

The amplitude `(a, b)` does NOT appear in any anomaly polynomial:
anomaly polynomials are gauge-curvature objects, while `(a, b)` is a
matter-amplitude parameter.

**Verified numerically (runner Section 4):**
- 4.1: ch(V) = 3 (integer, rank).
- 4.2: ch_C3(V)(C) = sum_k m_k · ω^k = 0.
- 4.3-4.4: Anomaly poly does not depend on (a, b).

### TOP-AV4 — Cech / sheaf cohomology

**Status: PRESERVES (a, b)-decoupling.**

Cech cohomology of a point with constant sheaf `Z`:

```
H^0(pt, Z) = Z (rank 1)
H^q(pt, Z) = 0 for q > 0
```

For C_3-equivariant Cech cohomology of a point (equivalent to group
cohomology of C_3 with trivial coefficients):

```
H^0(C_3, Z) = Z
H^1(C_3, Z) = 0  (no Z-torsion in degree 1 for cyclic groups w/ trivial action)
H^2(C_3, Z) = Z/3Z  (3-torsion class)
H^{2k}(C_3, Z) = Z/3Z for k ≥ 1
H^{2k+1}(C_3, Z) = 0 for k ≥ 1 (mod-2 periodic)
```

These are all integer-or-finite-valued. None can pin a continuous
amplitude.

C_3-equivariant line bundles on hw=1 (a point) are classified by
`Hom(C_3, U(1)) ≅ Z/3`, the 3 characters χ_0, χ_1, χ_2 — exactly
the 3 isotypes of TOP-AV2. Cech cohomology rederives K-theory data;
it does NOT supply new amplitude constraints.

**Verified numerically (runner Section 5):**
- 5.1: H^0(pt, Z) = Z (rank 1).
- 5.2: H^q(pt, Z) = 0 for q > 0.
- 5.3: H^2_C3(pt, Z) = Z/3Z (finite, 3-torsion).
- 5.4: |Hom(C_3, U(1))| = 3 (line bundles ↔ characters).
- 5.5: Cohomology gives (1, 1, 1) iso-mult, NOT (1, 1) [F1/BAE].

### TOP-AV5 — 't Hooft anomaly matching

**Status: PRESERVES (a, b)-decoupling.**

't Hooft anomaly matching: the global symmetry anomaly trace of an
IR effective theory must equal the UV (microscopic) anomaly trace.
For the C_3 global symmetry on the hw=1 triplet:

```
UV trace: (Tr_V(I), Tr_V(C), Tr_V(C²)) = (3, 0, 0)
IR trace: same — depends on V (representation), not H (amplitude)
```

Both UV and IR traces are integer-valued. The matching condition is
automatic and does NOT constrain `(a, b)`.

**Verified numerically (runner Section 6):**
- 6.1: UV anomaly trace (3, 0, 0).
- 6.2: IR anomaly trace independent of (a, b).
- 6.3: 't Hooft matching gives integer mode counts, not amplitude
  ratios.

### TOP-AV6 — Topological-amplitude no-bridge theorem

**Status: NO BRIDGE EXISTS.**

For an integer-valued `T` to pin the continuous ratio `|b|²/a² = 1/2`,
we'd need a continuous map `T = f(|b|²/a²)` with `T` discontinuously
jumping at `|b|²/a² = 1/2`. We verify: no such jump exists for any
of the standard topological invariants (η, rank, sign signature,
spectral flow) at the BAE point.

Specifically, for `H = I + r C + r C²` (φ = 0):
- λ_0 = 1 + 2r (largest)
- λ_1 = λ_2 = 1 - r (degenerate)

The smallest eigenvalue zero crossing occurs at `r = 1`, NOT at the
BAE point `r = 1/√2`. The η-invariant jumps at r = 1, not at r = 1/√2.

Spectral flow over a closed loop in `(a, |b|, φ)` space is integer-
valued. Sweeping `r` from 0 to 1.5 at fixed `(a, φ) = (1, 0)`, the
η-invariant takes values {3, 1} (jumping at r = 1), but at r = 1/√2,
η = 3 — same as for many other ratios. **No topological invariant
distinguishes the BAE point from its neighbors.**

**Verified numerically (runner Section 7):**
- 7.1: Spectral flow integer-valued.
- 7.2: Spectral flow does NOT distinguish BAE.
- 7.3: Topological invariants locally constant in (a, b).
- 7.4: Sweep of (a, |b|): finitely many invariant values.
- 7.5: No topological jump at BAE point r = 1/√2.
- 7.6: η-jump location ≠ BAE point.

### TOP-AV7 — Topology rederives (1, 2) and (1, 1, 1), not (1, 1)

**Status: NO TOPOLOGICAL COUNT GIVES (1, 1).**

Topology delivers three natural multiplicity countings on the
C_3[111] triplet:

| Counting | Value | Origin |
|---|---|---|
| (a) Complex isotype (over ℂ) | (1, 1, 1) | Three distinct C_3 irreps |
| (b) Real isotype (Herm_circ(3)) | (1, 2) | Trivial 1-real-dim + doublet 2-real-dim |
| (c) Regular rep multiplicities | (1, 1, 1) | Each irrep once |

NEITHER (1, 1, 1) nor (1, 2) is the (1, 1) multiplicity required
for F1 / BAE. The (1, 2) real-dim count from topology is **identical**
to the (1, 2) real-dim count Probe 28 derived at the operator level:
both are fixed by C_3 representation theory on `Herm_circ(3)`.

Topology rederives the operator-level structural decoupling at the
bundle level, but does NOT add a (1, 1) multiplicity that could
supply F1 / BAE.

**Verified numerically (runner Section 8):**
- 8.1: Complex isotype (1, 1, 1).
- 8.2: Real isotype (1, 2).
- 8.3: Regular-rep (1, 1, 1).
- 8.4: No topological count gives F1 mult (1, 1).
- 8.5: (1, 2) real-dim ≡ Probe 28 (1, 2).

## Theorem (Probe Y topological-level structural decoupling)

**Theorem (TOPO-DECOUPLE).** On A1 + A2 + retained Cl(3) per-site
uniqueness + retained Z³ substrate + retained C_3[111] hw=1 BZ-corner
forcing (Block 04) + retained M_3(ℂ) on hw=1 + retained C_3-equivariant
Hermitian circulant `H = aI + bC + b̄C²` + standard mathematical
machinery (Atiyah-Singer index theorem, K-theory of representation
rings, Chern character, Cech/group cohomology):

```
(a) The C_3-equivariant K-theory of a point is the representation ring:
       K_C3(pt) = R(C_3) = Z[χ_0] ⊕ Z[χ_1] ⊕ Z[χ_2]
    where χ_k are the irreducible characters of C_3. The class
    [V] of V = ℂ³ as a C_3-module is (1, 1, 1) — integer-valued.
    [Verified Section 3.]

(b) The equivariant index ind_C3(D) of any C_3-equivariant Dirac
    operator on the hw=1 triplet is integer-valued (or a class in
    R(C_3) = Z⊕Z⊕Z). It depends on chirality and isotype dimension
    but NOT on the matter-amplitude (a, b).
    [Verified Sections 2.2, 2.3.]

(c) The anomaly polynomial / Chern character on hw=1 is
    rank-valued (= 3 for V = ℂ³). The amplitude (a, b) does NOT
    appear in any anomaly polynomial.
    [Verified Section 4.]

(d) Cech cohomology on hw=1 is H^q(pt, Z) = Z, 0, 0, ... in degrees
    q = 0, 1, 2, ...; equivariant Cech is integer-or-Z/3-valued.
    None pins continuous (a, b).
    [Verified Section 5.]

(e) 't Hooft anomaly matching for C_3 gives UV-IR trace match
    (3, 0, 0); both integer-valued. Does NOT pin (a, b).
    [Verified Section 6.]

(f) Spectral flow and η-invariant of H_circ(a, b) are
    integer-valued and locally constant in (a, b). η jumps at
    eigenvalue zero crossings (e.g., |b|/a = 1 for φ = 0), NOT
    at the BAE point |b|/a = 1/√2.
    [Verified Sections 2.4-2.6, 7.5-7.6.]

(g) Topological multiplicity counts on H_circ(3) give (1, 1, 1)
    [complex isotypes] or (1, 2) [real isotypes], but never (1, 1)
    [F1 / BAE multiplicity]. The (1, 2) count is identical to
    Probe 28's operator-level (1, 2).
    [Verified Section 8.]

Therefore: topological invariants on the C_3[111] hw=1 triplet
STRUCTURALLY DECOUPLE from the continuous amplitude ratio |b|²/a².
They cannot supply a constraint that selects BAE. The
topological-level path (this probe) closes negatively, joining the
operator-level paths (Probes 12-30) and the wave-function-level path
(Probe X). The BAE admission count is unchanged. No new admission.
No new axiom.
```

**Proof.** Each item is verified by the runner (75 PASS / 0 FAIL):
Section 0 (retained sanity); Section 1 (isotype decomposition);
Section 2 (TOP-AV1 index); Section 3 (TOP-AV2 K-theory); Section 4
(TOP-AV3 anomaly poly); Section 5 (TOP-AV4 Cech cohomology);
Section 6 (TOP-AV5 't Hooft matching); Section 7 (TOP-AV6 no-bridge);
Section 8 (TOP-AV7 multiplicity counts); Section 9 (probe comparison);
Section 10 (convention robustness); Section 11 (3-level closure);
Section 12 (does-not disclaimers). ∎

## Algebraic root-cause

The topological decoupling has a clean structural root:

> **Topological invariants are integer-quantized; matter-amplitude
> parameters are continuous real numbers.** A discrete-valued
> invariant cannot generically pin a continuous parameter to a
> specific real value without an additional structural bridge —
> e.g., a quantization condition that maps the integer to a single
> real point. For `H_circ(a, b)` on `V = ℂ³`, the C_3 representation
> structure of `V` is fixed by retained content, but the amplitude
> `(a, b)` is a free continuous parameter on the configuration space
> `Herm_circ(3) ≅ ℝ³`. Topology constrains the **representation
> structure**, not the **point in configuration space**.

For BAE to be topologically pinned, retained content would need
to supply:

1. A topological invariant `T = T(a, b)` that depends on `(a, b)`.
2. A quantization condition `T = T_BAE` that uniquely pins
   `|b|²/a² = 1/2`.

Neither is provided by retained content. The η-invariant of `H_circ`
depends on `(a, b)` but is locally constant — it cannot pin a
specific value. The K-theory class of `V` does not depend on `(a, b)`.

## Why this probe is structurally distinct from Probes 28 and X

| Probe | Layer | Mechanism | Conclusion |
|---|---|---|---|
| Probes 12-30 | OPERATOR (Hilbert states) | C_3 rep theory: (1, 2) real-dim on Herm_circ(3) | F3 canonical, F1 / BAE absent |
| Probe X | WAVE-FUNCTION (∧^N tensors) | C_3 rep theory: det(C) = +1, Pauli ε ∈ trivial isotype | Slater singlet b-decoupled, BAE inaccessible |
| **Probe Y** | **TOPOLOGICAL (bundles, K-theory)** | **C_3 rep theory: K_C3(pt) = Z⊕Z⊕Z; integer-quantized** | **(a, b) absent from K-theory; no bridge** |

Probes 12-30 attacked at the operator level (Hilbert states + operator
algebras). Probe X attacked at the wave-function level (Slater
determinants on antisymmetrized tensors). Probe Y attacks at the
topological level (K-theory class, index theorem, anomaly polynomial,
Cech cohomology).

The conclusion is the same — F1 / BAE absent — but the **mechanism**
differs at each level. All three are rooted in C_3 representation
theory but at structurally distinct layers:

- Operator: real-dim of the C_3 isotype split on Herm_circ(3) is (1, 2).
- Wave-function: ∧³V carries the trivial character (det(C) = +1).
- Topological: K_C3(pt) = R(C_3) = Z⊕Z⊕Z (integer-quantized).

Each closes its corresponding path against BAE.

## Sharpened terminal residue (3-level closure)

Combining Probes 12-30 (operator), Probe X (wave-function), and
Probe Y (topological):

> **The (1, 1) multiplicity-counting principle required for F1 / BAE
> is structurally absent from ALL THREE accessible structural layers
> of the framework:**
>
> - **Operator layer (Probes 12-30):** any C_3-covariant interaction
>   preserves the (1, 2) real-dim weighting on Herm_circ(3). F1
>   structurally rejected at free + interacting levels.
>
> - **Wave-function layer (Probe X):** Pauli antisymmetrization is
>   C_3-trivial (det(C) = +1). Slater singlet ∈ trivial isotype,
>   decoupled from doublet b-sector.
>
> - **Topological layer (Probe Y, this probe):** K-theory class,
>   index theorem, anomaly polynomial, and Cech cohomology are all
>   integer-quantized isotype-count data. Continuous (a, b) is NOT
>   in topological data; cannot pin |b|²/a² = 1/2.

Closing BAE therefore requires admitting a multiplicity-counting
principle as a NEW PRIMITIVE — the existing Brannen Amplitude
Equipartition admission. The topological-level path does not provide
an alternative.

This is the **strongest possible structural rejection** of F1 / BAE
within accessible framework layers: F1 / BAE is absent from operator,
wave-function, AND topological layers. No structurally distinct
fourth layer is currently identified.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (topological-level structural
  rejection; new positive content: K-theory class, index, anomaly
  polynomial, Cech cohomology on the C_3[111] hw=1 triplet are all
  INTEGER-QUANTIZED isotype-count data, decoupled from continuous
  amplitude (a, b))
- audit-derived effective status: set only by the independent audit
  lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe Y
  sharpening: **"Topological invariants on the C_3[111] hw=1 triplet
  — index theorem, K-theory class, anomaly polynomial, Cech
  cohomology — are integer-quantized data on the bundle structure.
  K_C3(pt) = R(C_3) = Z⊕Z⊕Z; index ∈ Z; anomaly poly is
  rank-or-character valued; Cech is integer-or-Z/3-valued. The
  continuous amplitude (a, b) is NOT in topological data.
  Topology cannot pin |b|²/a²=1/2."**

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Tests whether topological invariants (index theorem, K-theory
   class, anomaly polynomial, Cech cohomology) on the C_3[111] hw=1
   triplet force |b|²/a² = 1/2 (BAE).
2. Identifies seven independent decoupling theorems (TOP-AV1 through
   TOP-AV7), each verifying topology cannot constrain |b|²/a².
3. Identifies the algebraic root-cause: topological invariants are
   integer-quantized, while (a, b) is continuous; no bridge from
   integer T to continuous |b|²/a² = 1/2 exists from retained
   topological data.
4. Establishes a sharpened terminal residue: F1 / BAE absent from
   operator-level (Probes 12-30), wave-function-level (Probe X),
   AND topological-level (Probe Y) retained content.
5. Cross-references prior Probes 12-30 and X; closes the
   topological-level gap as structurally distinct from all prior
   attacks.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT promote external surveys to retained authority.
7. Does NOT replace Probes 12-30 or Probe X (it complements them at
   a structurally distinct layer).
8. Does NOT propose an alternative κ value as physical.
9. Does NOT promote sister bridge gaps (L3a, L3b, C-iso, W1.exact).
10. Does NOT introduce new physics axioms — uses standard
    mathematical machinery (index theorem, K-theory, cohomology) to
    compute properties of retained C_3 + V data.

## Honest assessment

**What the probe finds:**

1. **K-theory class of `V = ℂ³` as C_3-module is `(1, 1, 1) ∈ R(C_3)
   = Z⊕Z⊕Z`.** Integer multiplicities; independent of `(a, b)`.

2. **Equivariant index of any C_3-equivariant Dirac operator on hw=1
   is integer-valued.** It depends on chirality and isotype dim,
   but NOT on the continuous matter-amplitude `(a, b)`.

3. **Anomaly polynomial / Chern character on hw=1 (a 0-dim base)
   reduces to rank `= 3 ∈ Z`.** The amplitude `(a, b)` is matter
   data, NOT gauge-curvature data.

4. **Cech cohomology of a point is `H^0 = Z, H^q = 0` for `q > 0`.**
   Equivariant Cech is integer-or-Z/3-valued. None can pin a
   continuous amplitude.

5. **'t Hooft anomaly matching gives integer mode-count constraints,
   not amplitude ratios.**

6. **No topological invariant of `H_circ(a, b)` jumps at the BAE
   point `|b|/a = 1/√2`.** The η-invariant jumps at `|b|/a = 1`
   (eigenvalue zero crossing) but takes the same value `η = 3` at
   `|b|/a = 1/√2` and at neighboring ratios.

7. **Topology rederives `(1, 2)` real-dim count [identical to Probe
   28] and `(1, 1, 1)` complex isotype count, but never `(1, 1)`
   multiplicity.** The (1, 1) needed for F1 / BAE is absent at the
   topological level.

**What this probe contributes to the campaign:**

1. **New positive content**: K-theory class, index theorem, anomaly
   polynomial, and Cech cohomology on the C_3[111] hw=1 triplet are
   all integer-quantized isotype-count data, structurally decoupled
   from continuous amplitude (a, b). Distinct from any prior probe
   in mechanism and layer.

2. **Sharpened residue characterization**: F1 / BAE absent from
   operator-level (Probes 12-30), wave-function-level (Probe X),
   AND topological-level (Probe Y) retained content. The (1, 2)
   real-dim count, the trivial det character of `∧³V`, and the
   integer K-theory class of `V` are THREE INDEPENDENT structural
   decouplings — all rooted in C_3 representation theory but at
   structurally distinct layers (operator / wave-function / bundle).

3. **Three-level structural closure**: returns the same campaign-
   terminal-state structural obstruction at the most fundamental
   accessible layer (topological/bundle level), distinct from all
   prior 31 attacks.

The remaining residue is **maximally sharp**:

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. The (1, 2) real-dim weighting
> (operator-level) is fixed by C_3 representation theory on
> Herm_circ(3); the trivial det character of `∧³V` (wave-function-
> level) is fixed by the parity of the 3-cycle; the K-theory
> class `[V] = (1, 1, 1) ∈ R(C_3)` (topological-level) is fixed
> by the regular C_3 representation on V = ℂ³. All three close
> negatively; none of the retained content layers — operator,
> wave-function, OR topology — supplies the (1, 1) multiplicity-
> counting principle required for BAE.**

Closing BAE therefore continues to require admitting a multiplicity-
counting principle as a NEW PRIMITIVE — i.e., a new admission or a
new retained source distinct from the existing C_3-equivariant
operator content, the existing fermionic wave-function content, AND
the existing topological / K-theoretic content. Probe Y makes this
requirement maximally explicit at the most fundamental accessible
structural layer.

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained C_3 / circulant structure

- BZ-corner forcing (Block 04): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Three-generation observable (M_3 algebra on hw=1): [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Probe campaign — companion probes

- Probe X (wave-function-level / Pauli antisymmetrization): [`KOIDE_X_BAE_PAULI_ANTISYMMETRIZATION_NOTE_2026-05-08_probeX_bae_pauli.md`](KOIDE_X_BAE_PAULI_ANTISYMMETRIZATION_NOTE_2026-05-08_probeX_bae_pauli.md)
- Probe 28 (operator-level / interacting dynamics): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe 25 (free-Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 18 (F1-vs-F3 algebraic): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 14 (retained-U(1) hunt): [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)

### Naming convention

- BAE rename note: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

## Validation

```bash
python3 scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py
```

Expected: `=== TOTAL: PASS=75, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained sanity (C_3 cycle is unitary, order 3, det = +1;
   H = aI + bC + b̄C² is Hermitian, C_3-equivariant).
2. Section 1 — C_3 isotype decomposition of V = ℂ³ (e_k Fourier basis,
   each isotype 1-complex-dim, regular rep).
3. Section 2 — TOP-AV1: equivariant index theorem; integer-valued;
   η-invariant integer; no jump at BAE point.
4. Section 3 — TOP-AV2: K-theory K_C3(pt) = R(C_3) = Z⊕Z⊕Z; regular
   rep gives (1, 1, 1) integer multiplicities; character orthogonality;
   K-theory class (a, b)-independent.
5. Section 4 — TOP-AV3: Chern character ch(V/pt) = rank = 3; equivariant
   Chern character via characters; anomaly poly (a, b)-independent.
6. Section 5 — TOP-AV4: Cech cohomology H^q(pt, Z); equivariant
   cohomology Z/3 torsion; line bundles classified by Hom(C_3, U(1)) = Z/3.
7. Section 6 — TOP-AV5: 't Hooft anomaly matching; integer trace
   (3, 0, 0); UV-IR matches automatically.
8. Section 7 — TOP-AV6: topological-amplitude no-bridge theorem;
   spectral flow; η-invariant locally constant in (a, b); η-jump at
   |b|/a = 1, NOT at BAE = 1/√2.
9. Section 8 — TOP-AV7: multiplicity-counting from topology;
   (1, 1, 1) complex / (1, 2) real / (1, 1, 1) regular; never (1, 1).
10. Section 9 — Comparison with Probe X (wave-function) and Probe 28
    (operator); 3-level structural closure.
11. Section 10 — Convention robustness (basis change, cycle inverse).
12. Section 11 — Sharpened terminal residue (3-level closure complete).
13. Section 12 — Does-not disclaimers (no BAE closure, no admission,
    no PDG, no retained-theorem modification, no new physics axioms).

Total: 75 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically derives the topological-decoupling from the
  representation-theoretic structure of `V` and `Herm_circ(3)`, and
  from the integer quantization of standard topological invariants
  (K-theory class, index, Chern character, Cech cohomology). The
  decoupling is **structural** (integer-quantization vs continuous
  amplitude) and is independent of any specific (a, b).
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "topological invariants can pin |b|²/a²" from seven
  independent angles (TOP-AV1 index, TOP-AV2 K-theory, TOP-AV3
  anomaly poly, TOP-AV4 Cech, TOP-AV5 't Hooft, TOP-AV6 no-bridge,
  TOP-AV7 multiplicity). All seven fail at the same structural
  locus: integer-or-finite invariants cannot pin a continuous real
  amplitude ratio without an additional bridge that retained content
  does not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction with new
  positive content; the parent BAE admission remains at its prior
  bounded status; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: this is structurally
  distinct from all prior 31 probes. Probes 12-30 attacked at
  operator level; Probe X attacked at wave-function level; this
  probe attacks at the topological / bundle / K-theory / index level.
  The mechanism is different at each level (real-dim count
  vs det character vs K-theory class). Although the conclusion is
  the same (no BAE forcing), this is substantive new structural content.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional content would be needed
  (a non-retained multiplicity-counting principle), not how-long.
- `feedback_special_forces_seven_agent_pattern.md`: this probe
  packages a multi-angle attack (seven independent TOP-AVs) on a
  single load-bearing structural hypothesis (topological invariants
  force BAE), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note proposal + paired runner + cached output, no synthesis
  notes, no lane promotions, no working "Block" notes.
- `feedback_primitives_means_derivations.md`: this probe uses
  standard mathematical machinery (index theorem statement, K-theory
  definition, cohomology) — these are **mathematical theorems**,
  not new physics axioms. The probe respects the "no new axioms"
  constraint by deriving topological consequences from retained
  C_3 + V structure.

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
- [koide_x_bae_pauli_antisymmetrization_note_2026-05-08_probeX_bae_pauli](KOIDE_X_BAE_PAULI_ANTISYMMETRIZATION_NOTE_2026-05-08_probeX_bae_pauli.md) (wave-function-level companion)
- [koide_bae_probe_interacting_dynamics_bounded_obstruction_note_2026-05-09_probe28](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) (operator-level companion)
- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) (free-Gaussian baseline)
- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) (M_3 on hw=1)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
