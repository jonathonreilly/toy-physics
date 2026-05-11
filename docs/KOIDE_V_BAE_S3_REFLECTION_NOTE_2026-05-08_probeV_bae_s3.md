# Probe V-BAE-S3-Reflection -- S_3 = C_3 ⋊ Z_2 Representation Theory Does NOT Force BAE: No-Go Source Note

**Date:** 2026-05-08
**Type:** no_go (negative route check -- structural rejection extends 3 -> 4 levels; no positive closure; no new admission)
**Claim type:** no_go
**Scope:** review-loop source-note proposal -- Probe V of the Koide
BAE-condition closure campaign. Tests whether the larger natural
symmetry `S_3 = C_3 ⋊ Z_2` (where the `Z_2` reflection input is
`P_{23}` from the cited circulant-parity and CPT surfaces) structurally
forces the Brannen Amplitude
Equipartition (BAE) condition `|b|²/a² = 1/2` on `C_3`-equivariant
Hermitian circulants `H = a I + b C + b̄ C²` on `hw=1`.
**Status:** source-note proposal for a NEGATIVE no-go obstruction
extending the BAE structural rejection from 3 levels (C_3 + K + RGE)
to 4 levels (full S_3). The hypothesis fails for a clean structural
reason: although `S_3 = C_3 ⋊ Z_2` is the natural symmetry of the
`Z³ × C_3` substrate, the `C_3` part acts TRIVIALLY on `Herm_circ(3)`
(because every circulant commutes with the cyclic shift `C`).
Therefore the standard 2d irrep of `S_3` (which the campaign
hypothesis hoped would re-couple `b` and `b̄`) does NOT appear in
the natural action; only trivial and sign irreps appear. The
doublet of `C_3` (= span of `b` and `b̄` characters) decomposes
under `S_3` as `(Re b)·B_1` (trivial) ⊕ `(Im b)·B_2` (sign) -- a
finer split, NOT a re-coupling of `(a, b)`. The BAE admission count
is UNCHANGED.
**Authority role:** source-note proposal -- audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probeV-s3-reflection-20260508
**Primary runner:** [`scripts/cl3_koide_v_bae_s3_2026_05_08_probeV_bae_s3.py`](../scripts/cl3_koide_v_bae_s3_2026_05_08_probeV_bae_s3.py)
**Cache:** [`logs/runner-cache/cl3_koide_v_bae_s3_2026_05_08_probeV_bae_s3.txt`](../logs/runner-cache/cl3_koide_v_bae_s3_2026_05_08_probeV_bae_s3.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named inputs, and
no-go classification are author-proposed; the audit lane has full
authority to retag, narrow, or reject the proposal. The cited upstream
surfaces are dependency inputs for this route check; this note does
not assert that they are currently retained-grade.

## Naming-collision warning

In this note:

- **physical `Cl(3)` local algebra** and **`Z^3` spatial substrate**
  are repo baseline semantics per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), not
  new axioms added by this note. Legacy `A1` / `A2` shorthand in older
  filenames is not used here as theorem language.
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md), **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

The 30-probe BAE campaign synthesis
([`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md))
established a multi-level structural rejection of BAE rooted in `C_3`
representation theory:

> **Within the cited campaign surfaces, the (1,2) real-dim weighting on
> `Herm_circ(3)` is C_3 representation-theoretic** (1 trivial real-dim
> for the `a`-direction + 2 doublet real-dims for the `(Re b, Im b)`
> directions, since `b ∈ ℂ`). This forces F3 (rank-weighted, (1,2),
> giving κ=1) over F1 (multiplicity-weighted, (1,1), giving κ=2 = BAE).

Probes 25, 27, 28 collectively tested this under free Gaussian
dynamics (Probe 25), all `hw=N` sectors (Probe 27), and the cited
interaction surface (Probe 28).

The user-prompt observation: under the larger group `S_3 = C_3 ⋊ Z_2`
(the natural symmetry of the `Z³ × C_3` substrate, where `Z_2 =
⟨P_{23}⟩` is the cyclic-reversal involution), `S_3` has 3 irreps:

- Trivial 1-dim (carries 1)
- Sign 1-dim (sign of permutation)
- Standard 2-dim (could in principle mix `b` and `b̄` via reflection)

**Could the standard 2d irrep of S_3 unblock BAE?** Specifically, do
`a` (diagonal) and `b` (off-diagonal) live in the SAME `S_3`
isotype (instead of distinct `C_3` isotypes), thereby supplying the
multiplicity-counting principle the campaign identified as missing?

## Answer

**No.** `S_3` representation theory STILL DECOUPLES `(a, b)`-isotypes;
extends the structural rejection from 3 to 4 levels.

**Verdict: NEGATIVE bounded obstruction.** The hypothesis fails for a
clean structural reason: although `S_3 = C_3 ⋊ Z_2` is the full natural
symmetry, the `C_3` part acts TRIVIALLY on `Herm_circ(3)` (because
circulants commute with the cyclic shift `C`). Therefore:

- The `S_3` rep on `Herm_circ(3)` factors through `Z_2 = S_3 / C_3`.
- The standard 2d irrep of `S_3` does NOT appear in `Herm_circ(3)`.
- Only the trivial and sign irreps of `S_3` appear; the multiplicity
  decomposition is `Herm_circ(3) = 2·(S_3-trivial) + 1·(S_3-sign)`.
- The user-hoped re-coupling of `(a, b)` via the standard 2d irrep
  IS STRUCTURALLY ABSENT.

The BAE admission count is UNCHANGED. No new admission. No new axiom.

## Setup

### Premises for Probe V-BAE-S3-Reflection

| ID | Statement | Class |
|---|---|---|
| Cl3Baseline | physical `Cl(3)` local algebra | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3Substrate | `Z³` spatial substrate | repo baseline; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| CircParity | P_{23}-Z_2 acts on Hermitian-circulant family decomposing it into `(d, c_even)` trivial and `c_odd` sign | source dependency; see [`CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md`](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md) T1, T2 |
| CPTexact | `T = K` (entry-wise complex conjugation); CPT antiunitary, `(CPT)² = id` | source dependency; see [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), [`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md) |
| Probe7 | Five Z_2 candidates fail to force BAE; `S_3 = Z_3 ⋊ Z_2` semidirect (NOT direct `Z_6 = Z_2 × C_3`) | source dependency; see [`KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md) |
| Probe13 | K-real-structure supplies Z_2 part of (1,1)-counting but not SO(2) angular quotient; K-orbit-uniform extremum gives κ=4 | source dependency; see [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) |
| Probe18 | F1 vs F3 ambiguity; F2 structurally ruled out | source dependency; see [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new repo-wide axioms. The `S_3` route is constructed from the
  named `C_3` and `Z_2 = ⟨P_{23}⟩` dependency surfaces above; their
  retained-grade status is left to the independent audit lane.

## The structural argument

### S_3 dependency boundary (Section 11 of runner)

`S_3 = C_3 ⋊ Z_2` is built from existing named dependency surfaces:

1. `C_3 = ⟨C⟩` (cyclic shift): cited via
   [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
   + [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md).
2. `Z_2 = ⟨P_{23}⟩` (residual transposition): cited via
   [`CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md`](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md)
   T1 (`P_{23} S P_{23} = S²`) and T2 (decomposes circulants into
   `(d, c_even)` trivial + `c_odd` sign).
3. The composition relation `P_{23} C P_{23} = C^{-1}` is the
   defining semidirect-product structure: the `Z_2` inverts the
   `C_3`. (Verified by runner Section 2.)
4. Equivalently, `Z_2 = ⟨K⟩` where `K` is entry-wise complex
   conjugation: cited via
   [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md). On Herm_circ basis,
   `K` and `P_{23}` act identically (sending `(a, Re b, Im b) →
   (a, Re b, -Im b)`).

**Review boundary:** this note does not add a new axiom and does not
claim the cited dependencies are retained-grade. It only states the
conditional route result over those named inputs.

### S_3 acts on Herm_circ(3) via Z_2 only (Sections 3, 4 of runner)

The critical structural observation:

> **Every Hermitian circulant `H = aI + bC + b̄C²` commutes with `C`,
> since `{I, C, C²}` are pairwise-commuting (forming a
> commutative subalgebra of `M_3(ℂ)`).** Therefore
> `C · H · C^{-1} = H` for every `H ∈ Herm_circ(3)`, i.e., the
> `C_3` part of `S_3` acts TRIVIALLY on `Herm_circ(3)`.

This means the `S_3` rep on `Herm_circ(3)` factors through the
quotient `Z_2 = S_3 / C_3`. The non-trivial action comes entirely
from `P_{23}`:

```
P_{23} · I · P_{23}            =  I            (trivial)
P_{23} · (C + C²) · P_{23}     =  C + C²       (trivial)
P_{23} · i(C - C²) · P_{23}    =  -i(C - C²)   (sign)
```

(Per the cited `CIRCULANT_PARITY_CP_TENSOR` T2 surface.)

### S_3 isotype decomposition of Herm_circ(3) (Section 5 of runner)

Computing the character of `Herm_circ(3)` as an `S_3` rep:

| Element `g` | `χ_Herm(g)` |
|---|---|
| `e`        | 3 |
| `C`        | 3 |
| `C²`       | 3 |
| `P_{23}`   | 1 |
| `C P_{23}` | 1 |
| `C² P_{23}`| 1 |

Inner products with `S_3` irreducible characters:

```
⟨χ_Herm, χ_trivial⟩  =  (1/6)(3 + 3 + 3 + 1 + 1 + 1)  =  12/6  =  2
⟨χ_Herm, χ_sign⟩     =  (1/6)(3 + 3 + 3 - 1 - 1 - 1)  =   6/6  =  1
⟨χ_Herm, χ_standard⟩ =  (1/6)(2·3 - 1·3 - 1·3 + 0 + 0 + 0) =  0/6 = 0
```

So:

```
Herm_circ(3)  =  2·(S_3-trivial)  ⊕  1·(S_3-sign)  ⊕  0·(S_3-standard).
                 ↑                    ↑                ↑
                 a·I, (Re b)·B_1     (Im b)·B_2       NOT PRESENT
```

**The standard 2d irrep of `S_3` is ABSENT from `Herm_circ(3)`.**

This refutes the user-prompt hypothesis that the standard 2d irrep
could mix `b` and `b̄` via reflection. The natural action of `S_3`
on `Herm_circ(3)` simply DOES NOT REALIZE this irrep.

### Why this happens structurally

The standard 2d irrep of `S_3` is realized by the natural action of
`S_3` on `ℂ³`/`(diagonal)`, i.e., on the 2-dim subspace of vectors
`(x_1, x_2, x_3)` with `x_1 + x_2 + x_3 = 0`. But `Herm_circ(3)` is
NOT this 2d standard rep: it is the COMMUTATIVE subalgebra of
`M_3(ℂ)` generated by `{I, C, C²}`, which is isomorphic to the
representation of `S_3` on `(F_S3)`/`(rotation)`, where each
generator acts on its own coordinate. Since circulants commute with
`C`, the `C_3` action is trivial; only the reflection acts.

Equivalently: the standard 2d irrep of `S_3` lives on the Brillouin
zone "non-trivial" momentum directions (where `C_3` acts as a
non-trivial rotation), whereas `Herm_circ(3)` lives on the
"momentum-zero" subspace (where `C_3` acts as identity).

### S_3 multiplicity weighting does NOT give BAE (Section 6 of runner)

Applying the natural `(1,1)` `S_3`-multiplicity-weighted log-functional:

```
F_S3(H)  =  log(E_trivial_S3)  +  log(E_sign_S3)
        =  log(3 a² + 6 (Re b)²)  +  log(6 (Im b)²)
```

Extremization under `E_total = E_trivial_S3 + E_sign_S3 = const`:

```
E_trivial_S3  =  E_sign_S3  =  E_total / 2
3 a² + 6 (Re b)²  =  6 (Im b)²    (extremum hypersurface)
```

This is a **codim-1 hypersurface** in the 3-real-parameter space
`(a, Re b, Im b)`, NOT a single forced point. It intersects the
BAE locus `|b|² = a²/2` only on a curve, not on a forced point.

**Numerical verification (runner Section 6):**

| Sample point on extremum hypersurface | `\|b\|² / a²` | BAE? |
|---|---|---|
| `(a=1, Re b=0, Im b=1/√2)`              | 0.500 | yes (one point in continuum) |
| `(a=1, Re b=0.5, Im b=√0.75)`           | 1.000 | NO |
| `(a=1, Re b=√0.5, Im b=1)`              | 1.500 | NO |

So the `(1,1)` weighting on `S_3` isotypes does not structurally
force BAE.

### S_3 real-Plancherel weighting gives F3-class κ=1 (Section 7 of runner)

The natural rep-dim²/|G| weighting on `S_3` irreps gives
`(w_trivial, w_sign, w_standard) = (1/6, 1/6, 4/6)`. Applied to
`Herm_circ(3)` with multiplicities `(2, 1, 0)`, the effective
weights are:

```
w_eff_trivial  =  2 × (1/6)  =  1/3
w_eff_sign     =  1 × (1/6)  =  1/6
w_eff_standard =  0
```

Ratio `w_eff_trivial : w_eff_sign = 2 : 1`. Extremization under
`E_total = const` gives `E_trivial_S3 = (2/3) E_total`,
`E_sign_S3 = (1/3) E_total`, structurally identical to F3
((1,2) on (E_+, E_⊥)) which gives **κ=1, NOT BAE**.

### S_3-invariant subspace gives free `|b|²/a²` (Section 8 of runner)

If we impose full `S_3`-invariance on `H` (require `P_{23} H P_{23}
= H`), we force `Im b = 0`, i.e., `b ∈ ℝ`. The resulting `S_3`-
invariant subspace is the 2-real-parameter family `{a I + b (C +
C²) : a, b ∈ ℝ}`.

On this subspace, `|b|²/a² = b²/a²` is **a free parameter**:

| `a` | `b` | `\|b\|²/a²` |
|---|---|---|
| 1.0 | 0.05  | 0.0025 |
| 1.0 | 0.5   | 0.25   |
| 1.0 | 1/√2  | 0.50 (BAE) |
| 1.0 | 2.0   | 4.0    |
| 1.0 | 5.0   | 25.0   |

BAE is **codim-1 within the 2D plane**, NOT a forced point. This
exactly replicates Probe 7 Barrier 1 (KOIDE_A1_PROBE_Z2_C3_PAIRING).

### Probe 13 K-orbit κ=4 unchanged under full S_3 (Section 10 of runner)

Probe 13 (REAL_STRUCTURE) computed the K-orbit-uniform Lagrangian
extremum on `K`-orbits `{χ_1} + {χ_ω, χ_ω̄}` of `C_3` characters,
finding `|b|² = a²/4` (κ = 4, NOT BAE = 2).

This probe verifies: under the full `S_3 = C_3 ⋊ K`, the result is
UNCHANGED. The `C_3` part adds nothing (since trivial on Herm_circ),
so the `S_3`-orbit-uniform extremum equals the `K`-orbit-uniform
extremum.

## Theorem (Probe V-BAE-S3-Reflection no-go obstruction)

**Theorem.** Conditional on physical `Cl(3)` local algebra, the `Z^3`
spatial substrate, the cited `C_3`-equivariance surface, the cited
`P_{23}` / CPT reflection surfaces, the cited block-total Frobenius and
MRU surfaces, and the cited Probe 7, 12, 13, 18, 25, 27, 28 surfaces:

```
(a) The natural symmetry of the Z³ × C_3 substrate is S_3 = C_3 ⋊ Z_2,
    where Z_2 = ⟨P_{23}⟩ is the cited reflection input from the
    circulant-parity and CPT surfaces. The defining relation
    P_{23} C P_{23} = C^{-1} = C² is the semidirect-product structure
    (Probe 7 Barrier 1 verified).
    [Verified Section 2 of runner.]

(b) C_3 acts TRIVIALLY on Herm_circ(3): every H = aI + bC + b̄C²
    commutes with C, since {I, C, C²} pairwise commute (form a
    commutative subalgebra). Therefore C · H · C^{-1} = H for every
    H ∈ Herm_circ(3).
    [Verified Section 3 of runner.]

(c) Therefore the S_3 representation on Herm_circ(3) factors through
    Z_2 = S_3 / C_3. The non-trivial action comes entirely from
    P_{23} (or equivalently K).
    [Algebraic; Section 3.]

(d) Computing the character of Herm_circ(3) as an S_3 representation
    and the inner products with S_3 irreducible characters yields:
        ⟨χ_Herm, χ_trivial⟩  = 2,
        ⟨χ_Herm, χ_sign⟩     = 1,
        ⟨χ_Herm, χ_standard⟩ = 0.
    Hence Herm_circ(3) = 2·(S_3-trivial) ⊕ 1·(S_3-sign) ⊕
    0·(S_3-standard). The STANDARD 2d IRREP OF S_3 IS ABSENT.
    [Verified Section 5 of runner.]

(e) The (1,1) S_3-isotype-multiplicity-weighted log-functional
    F_S3 = log E_trivial_S3 + log E_sign_S3 has its extremum on the
    hypersurface 3a² + 6(Re b)² = 6(Im b)², a codim-1 surface in the
    3-real-parameter space (a, Re b, Im b). This hypersurface
    intersects BAE = (|b|² = a²/2) only on a curve, NOT on a forced
    point.
    [Verified Section 6 of runner.]

(f) The S_3 real-Plancherel-weighted (rep-dim²/|G|) functional gives
    effective weights (2/6, 1/6, 0) on (trivial, sign, standard) and
    extremum (E_trivial_S3, E_sign_S3) = (2N/3, N/3) -- structurally
    identical to F3 ((1,2) on (E_+, E_⊥)), giving κ=1, NOT BAE.
    [Verified Section 7 of runner.]

(g) S_3-invariant Hermitian circulants (P_{23} H P_{23} = H) form a
    2-real-parameter family {aI + b(C+C²) : a, b ∈ ℝ}. BAE is
    codim-1 within this 2D plane, NOT a forced point. Replicates
    Probe 7 Barrier 1.
    [Verified Section 8 of runner.]

(h) Probe 13's K-orbit-uniform extremum gives |b|²/a² = 1/4 (κ = 4,
    NOT BAE = 2). Adding the C_3 part to K under full S_3 does NOT
    change this result, since C_3 acts trivially on Herm_circ(3).
    [Verified Section 10 of runner.]

Therefore: S_3 representation theory does NOT structurally force
BAE. The structural rejection is extended from "C_3 alone"
(Probes 25, 27, 28) to "full S_3 = C_3 ⋊ Z_2" (this probe).
The user-prompt hypothesis that the standard 2d irrep of S_3
could re-couple (a, b) is structurally false: this irrep is
ABSENT from Herm_circ(3) under the natural action.

The BAE admission count is unchanged. No new admission.
No new axiom.
```

**Proof.** Each item is verified by the runner (63 PASS / 0 FAIL):
Section 1 (named input algebra sanity); Section 2 (S_3 semidirect structure);
Section 3 (C_3 trivial on Herm_circ); Section 4 (P_{23} action via
CIRCULANT_PARITY T2); Section 5 (S_3 isotype decomposition); Section
6 ((1,1) S_3 multiplicity extremum); Section 7 (real-Plancherel S_3
gives F3-class κ=1); Section 8 (S_3-invariant subspace); Section 9
(F1 vs F3 under S_3); Section 10 (Probe 13 K-orbit κ=4 cross-check);
Section 11 (dependency disclosure); Section 12 (verdict synthesis). ∎

## Why the user-prompt hypothesis fails

The user-prompt observation (paraphrased) was:

> "In the standard 2d rep of S_3, the basis vectors mix `b` and `b̄`
> via the Z_2 reflection. The diagonal (a) and off-diagonal (b) are
> NOT in different isotypes under S_3 the way they are under C_3.
> This might unblock BAE structural derivation."

The structural reason this fails:

1. The standard 2d irrep of `S_3` is realized on the
   `(x_1, x_2, x_3)`-with-`Σx_i = 0` subspace of `ℂ³`, NOT on
   `Herm_circ(3)`.
2. `Herm_circ(3)` is the COMMUTATIVE subalgebra of `M_3(ℂ)`
   generated by the cyclic shift; circulants commute with `C` by
   construction.
3. Therefore `C_3` acts as IDENTITY on `Herm_circ(3)`, killing the
   `C_3`-non-trivial part of any `S_3` rep restricted to this
   subspace.
4. Only `Z_2 = S_3/C_3`-non-trivial reps survive. The standard 2d
   irrep of `S_3` would require a non-trivial `C_3` action; absent
   that, it cannot appear in `Herm_circ(3)`.
5. The `S_3` decomposition is therefore `2·(trivial) + 1·(sign)` --
   a finer split of the `C_3`-doublet `(Re b, Im b)` into
   `Z_2`-trivial `(Re b)` + `Z_2`-sign `(Im b)`, NOT a re-coupling
   of `(a, b)`.

This is a clean structural rejection. The hypothesis is impossible
even in principle, not merely algebraically failed.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `no_go` (NEGATIVE -- structural rejection
  extends 3 -> 4 levels; no positive closure; no new admission)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` -- the residual admission, with the Probe V
  sharpening: **"Even under the FULL S_3 = C_3 ⋊ Z_2 natural symmetry
  (where Z_2 is supplied by the cited CIRCULANT_PARITY_CP_TENSOR + CPT_EXACT_NOTE surfaces),
  the standard 2d irrep of S_3 is ABSENT from Herm_circ(3) under the
  natural action (since C_3 acts trivially on Herm_circ). The
  representation-theoretic decoupling of (a, b) into distinct isotypes
  PERSISTS at the S_3 level. BAE remains unforced."**

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Tests whether the larger natural symmetry `S_3 = C_3 ⋊ Z_2`
   (vs `C_3` alone) supplies the multiplicity-counting principle
   identified by Probes 25, 27, 28 as missing.
2. Discloses the `Z_2 = ⟨P_{23}⟩` dependency surfaces
   (CIRCULANT_PARITY_CP_TENSOR and CPT_EXACT_NOTE); retained-grade
   status remains audit-owned.
3. Computes the character of `Herm_circ(3)` as an `S_3`
   representation and shows the standard 2d irrep is ABSENT.
4. Shows the `(1,1)` `S_3`-multiplicity weighting gives a
   hypersurface NOT BAE.
5. Shows the real-Plancherel `S_3` weighting gives the F3-class
   `κ=1` (NOT BAE).
6. Shows the `S_3`-invariant subspace gives a 2D family with BAE
   as one point in continuum (Probe 7 Barrier 1 replicated).
7. Cross-checks Probe 13's `K`-orbit `κ=4` result (unchanged under
   full `S_3`).
8. Extends the structural rejection from 3 levels (`C_3` + free +
   interacting) to 4 levels (full `S_3` covering all of these).

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any upstream theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT promote external surveys to retained authority.
7. Does NOT propose `S_3 (1,1)` extremum as a physical principle.
8. Does NOT promote Probes 19, 24 (the campaign's positive results)
   to retained.
9. Does NOT explore beyond `S_3` (e.g., `A_4`, `S_4`, larger
   discrete groups, or the `O(2)` continuous extension of `K`).

## Honest assessment

**What the probe finds:**

1. **`S_3 = C_3 ⋊ Z_2` is the bounded route under test**, built from
   the cited `C_3` cyclic-shift surfaces and the cited
   `Z_2 = ⟨P_{23}⟩` / `K = T` reflection surfaces. This note does
   not assert those dependencies are retained-grade.

2. **`C_3` acts trivially on `Herm_circ(3)`** because circulants
   commute with `C`. Therefore the `S_3` rep on `Herm_circ(3)`
   factors through `Z_2 = S_3/C_3`.

3. **The standard 2d irrep of `S_3` is ABSENT from `Herm_circ(3)`**
   under the natural action. The user-prompt hypothesis is
   structurally impossible.

4. **The `S_3`-isotype decomposition is `2·(trivial) + 1·(sign)`**
   -- a finer split of the `C_3` doublet into `Re b` (trivial)
   + `Im b` (sign), NOT a re-coupling of `(a, b)`.

5. **`(1,1)` `S_3`-multiplicity weighting gives a hypersurface NOT
   BAE.** Real-Plancherel `S_3` weighting gives the F3-class `κ=1`
   (NOT BAE).

6. **`S_3` does not supply the missing multiplicity-counting
   principle.** The structural rejection extends from 3 levels
   (`C_3` + free + interacting, per Probes 25, 27, 28) to 4 levels
   (full `S_3`).

**What this probe contributes to the campaign:**

1. **New negative content**: the user-prompt hypothesis (that S_3's
   larger structure could unblock BAE via the standard 2d irrep)
   is REFUTED structurally.
2. **Sharpened residue**: the structural rejection is now known to
   be robust under the full `S_3 = C_3 ⋊ Z_2` natural symmetry,
   not just under `C_3` alone.
3. **Closes a discrete-group symmetry-extension lane**: `S_3` is
   the maximal symmetry checked in this bounded package. Any larger
   group would require extra primitives such as an `O(2)` continuous
   extension, which this note does not add.
4. **Confirms Probe 7 Barrier 1 via direct computation** (the
   `S_3`-invariant subspace gives a 2D family with BAE codim-1).
5. **Confirms Probe 13 K-orbit `κ=4` is unchanged under `S_3`**.

**The remaining residue is unchanged:**

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. The cited `C_3` representation
> theory and the natural extension to `S_3 = C_3 ⋊ Z_2` both give
> the (1, 2) real-dim weighting, NOT (1, 1). The (1, 2) weighting
> persists because (a) under `C_3`, the doublet of `b, b̄` is
> 2-real-dim, and (b) under `S_3`, `C_3` acts trivially on
> `Herm_circ(3)`, so the standard 2d irrep that could mix `b`
> with `b̄` via reflection is structurally ABSENT.**

Closing BAE therefore continues to require either (a) a
multiplicity-counting principle distinct from `C_3` and `S_3`
representation theory on `Herm_circ(3)`, or (b) an admission
distinct from BAE itself. Probe V makes the `S_3`-extension lane
explicit as exhausted within this bounded route.

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### C_3 / circulant structure (load-bearing for the structural argument)

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Z_2 / reflection structure (load-bearing for the S_3 construction)

- Circulant parity (Z_2 = ⟨P_{23}⟩, T1, T2): [`CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md`](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md)
- CPT exact (T = K complex conjugation): [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- (CPT)² = id: [`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Prior BAE probes (parallel structural rejections)

- Probe 7 (Z_2 × C_3 = Z_6 vs S_3): [`KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md) -- explicit `S_3 = Z_3 ⋊ Z_2` semidirect identification, 5 Z_2 candidates fail.
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure / K-orbit): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) -- K-orbit-uniform gives κ=4, not BAE.
- Probe 14 (U(1) hunt): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 18 (F1 vs F3 algebraic): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 25 (free Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 27 (hw=N sector identification): [`KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md`](KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md)
- Probe 28 (cited interaction surface): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)

### Campaign synthesis

- 30-probe terminal synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- BAE rename meta: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

### C_3 symmetry preservation (interpretive context)

- C_3 symmetry preserved interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)

## Validation

```bash
python3 scripts/cl3_koide_v_bae_s3_2026_05_08_probeV_bae_s3.py
```

Expected: `=== TOTAL: PASS=63, FAIL=0 ===`

The runner verifies (12 sections):

1. **Section 1** -- Named input algebra sanity: C unitary, order 3,
   eigenvalues `{1, ω, ω̄}`; P_{23} unitary, real, involutive (P² = I).
2. **Section 2** -- S_3 = C_3 ⋊ Z_2 semidirect: P_{23} C P_{23} = C^{-1}
   (defining relation); ⟨C, P_{23}⟩ has 6 elements = |S_3|.
3. **Section 3** -- C_3 acts trivially on Herm_circ(3): basis B_0, B_1,
   B_2 all C-fixed; random circulants commute with C.
4. **Section 4** -- P_{23} action on Herm_circ basis: (a, u, v) →
   (a, u, -v) (matching the cited CIRCULANT_PARITY T2 surface).
5. **Section 5** -- S_3 isotype decomposition: ⟨χ_Herm, χ_trivial⟩ = 2,
   ⟨χ_Herm, χ_sign⟩ = 1, ⟨χ_Herm, χ_standard⟩ = 0 (standard 2d
   irrep ABSENT).
6. **Section 6** -- (1,1) S_3-multiplicity extremum: hypersurface
   3a² + 6(Re b)² = 6(Im b)²; intersects BAE only on a curve, three
   sample points showing |b|²/a² ∈ {0.5, 1.0, 1.5}.
7. **Section 7** -- Real-Plancherel S_3 weighting: effective ratio
   2:1, identical to F3 (1,2) class, gives κ=1 NOT BAE.
8. **Section 8** -- S_3-invariant subspace (b ∈ ℝ): 2D plane with
   BAE codim-1; sample ratios {0.0025, 0.25, 0.5, 4.0, 25.0}.
9. **Section 9** -- F1 vs F3 under S_3: same (1,2) imbalance under
   different decompositions; κ varies, NOT constant 2 = BAE.
10. **Section 10** -- Probe 13 K-orbit κ=4 cross-check: unchanged
    under S_3 since C_3 trivial on Herm_circ.
11. **Section 11** -- Dependency disclosure: the C_3 and Z_2 inputs
    are named; retained-grade status is not asserted by the runner.
12. **Section 12** -- Verdict synthesis: NEGATIVE; structural
    rejection extends 3 → 4 levels.

Total: 63 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  derives a structural impossibility (the standard 2d irrep is
  ABSENT) by direct computation of `S_3` characters on the
  natural rep on `Herm_circ(3)` -- not just an algebraic-equivalence
  consistency check. The (1,2) → F3 outcome under S_3 real-Plancherel
  is structurally identical to the C_3 result, derived by the same
  rep-theoretic mechanism.
- `feedback_hostile_review_semantics.md`: the note stress-tests the
  user-prompt semantic claim "S_3 standard 2d irrep could re-couple
  (a, b)" at the action-level (rep-theoretic computation on the
  actual `S_3` action on `Herm_circ(3)`) and finds the irrep
  ABSENT. The hypothesis fails at the action-level identification,
  not just algebraically.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This note is a bounded
  no-go obstruction; the parent BAE admission remains at its
  prior bounded status; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: this note explores a
  structurally-distinct hypothesis (standard 2d irrep of S_3) that
  prior probes did not directly test. Probe 7 noted `S_3` as a
  group but did not compute its representation theory on
  `Herm_circ(3)` to find the standard 2d irrep absent. This is
  substantive new structural content.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  routes (closing BAE at the discrete-group-extension level)
  characterized as exhausted within this bounded `S_3` route; further
  extensions would require additional primitives like O(2)
  continuous extension or A_4 / S_4 admissions.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a single-shot multi-section attack (12 sections,
  63 PASS) on a single load-bearing structural hypothesis (S_3
  representation theory unblocks BAE) with sharp PASS/FAIL
  deliverables.
- `feedback_review_loop_source_only_policy.md`: this note is a
  single source-note proposal + paired runner + cached output, no
  synthesis notes, no lane promotions, no working "Block" notes.
- `feedback_primitives_means_derivations.md`: S_3 is constructed
  from named C_3 and Z_2 = ⟨P_{23}⟩ dependency surfaces; no new
  axiom is admitted here.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [koide_a1_probe_z2_c3_pairing_bounded_obstruction_note_2026-05-08_probe7](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md) (S_3 = Z_3 ⋊ Z_2 baseline)
- [circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md) (Z_2 input)
- [cpt_exact_note](CPT_EXACT_NOTE.md) (T = K input)
- [cpt_squared_is_identity_theorem_note_2026-05-02](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md) ((CPT)² = id)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) (C_3 input)
- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) (BZ-corner forcing)
- [koide_a1_probe_real_structure_bounded_obstruction_note_2026-05-09_probe13](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) (K-orbit κ=4 cross-check)
- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) (F1 vs F3 framing)
- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) (free dynamics)
- [koide_bae_probe_hw_sector_identification_bounded_obstruction_note_2026-05-09_probe27](KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md) (hw=N sectors)
- [koide_bae_probe_interacting_dynamics_bounded_obstruction_note_2026-05-09_probe28](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) (interacting dynamics)
- [koide_bae_30_probe_campaign_terminal_synthesis_meta_note_2026-05-09](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md) (campaign synthesis)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
