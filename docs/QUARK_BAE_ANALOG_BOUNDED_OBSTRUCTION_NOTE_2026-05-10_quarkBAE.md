# Quark-Sector BAE Analog — Bounded Obstruction (Tensor-Preservation)

**Date:** 2026-05-10
**Type:** bounded_theorem (sharpened obstruction; extends the
charged-lepton BAE bounded obstruction to the quark sector via tensor-
preservation of C_3 isotype ratios)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — tests whether the
quark-sector analog of the Brannen Amplitude Equipartition (BAE)
condition has a different trap profile than the charged-lepton BAE,
due to its 6-dim host space (3 colors × 2 weak doublet) versus the
charged-lepton 3-dim host space.
**Status:** source-note proposal for a sharpened bounded obstruction.
The C_3 representation theory on the quark 6D host space yields the
SAME (1, 2) real-DOF isotype ratio as the charged-lepton 3D sector,
because tensor-multiplication with a C_3-trivial passenger factor
(weak SU(2)) preserves isotype ratios uniformly. The quark BAE-analog
is structurally barred at κ = 1 (F3), NOT κ = 2 (F1 = BAE). The
BAE/A1 admission count is UNCHANGED — this probe EXTENDS the bounded
obstruction without introducing a new admission.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** quark-bae-analog-20260510
**Primary runner:** [`scripts/cl3_quark_bae_analog_2026_05_10_quarkBAE.py`](../scripts/cl3_quark_bae_analog_2026_05_10_quarkBAE.py)
**Cache:** [`logs/runner-cache/cl3_quark_bae_analog_2026_05_10_quarkBAE.txt`](../logs/runner-cache/cl3_quark_bae_analog_2026_05_10_quarkBAE.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming

Throughout this note:
- **physical `Cl(3)` local algebra** (legacy minimal-axiom alias:
  `A1`) = the repo's retained local algebra baseline per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- **"BAE"** = Brannen Amplitude Equipartition = the constraint
  `|b|²/a² = 1/2` for `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`
- **"quark BAE-analog"** = the analogous condition on the 6-dim
  quark sector `P_symm × I_fiber` = (3-color × 2-weak doublet) per
  [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- **"F1"** = (1, 1) multiplicity weighting (BAE direction; κ = 2)
- **"F3"** = (1, 2) real-DOF weighting (rank-weighted; κ = 1)

## Question

The 30-probe BAE campaign for charged-lepton sector reached terminal
bounded-obstruction state per
[`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md).
The structural reason: F1 multiplicity weighting `(1, 1)` is structurally
absent from retained C_3 representation theory on `Herm_circ(3)`
(3-dim host); the retained free Gaussian dynamics gives F3 `(1, 2)`
yielding κ = 1, not κ = 2 = BAE.

Probe 27 (PR #824) established that this F3 forcing is sector-independent
on the staggered Z³ APBC BZ-corner inventory `{0,1}³` — the F3 vs F1
distinction is C_3-rep-theoretic on 3-dim host spaces and persists
across hw=1 vs hw=2.

**The new angle**: The quark sector in `CL3_SM_EMBEDDING_THEOREM` lives
on a LARGER 6-dim host space:
```
P_symm × I_fiber = (3D symmetric base) × (2D weak doublet)  -- Y = +1/3
```
This 6D space is structurally distinct from the 3D BZ-corner sectors
explored by Probe 27. Could the larger sector have a DIFFERENT
multiplicity structure under retained C_3 generation cycle, potentially
escaping the F3 trap that bars charged-lepton BAE?

> Hypothesis (this probe): the quark sector's 6-dim host space has
> different C_3-isotype multiplicity counts, and may give F1 (κ = 2 =
> BAE-equivalent) where the charged-lepton 3D sector gave F3 (κ = 1).

## Answer

**No.** The quark sector's 6-dim host space gives the SAME `(1, 2)`
isotype real-DOF ratio as the charged-lepton 3-dim sector. The
multiplicity ratio is preserved by tensor-multiplication with a C_3-
trivial passenger factor.

**Verdict: STRUCTURAL OBSTRUCTION (sector-extension generalization).**

The claim:

> The Brannen-circulant ansatz `H_color = aI + bC + b̄C²` on the 3-color
> factor of the 6D quark sector `(3-color) ⊗ (2-weak)`, lifted via the
> trivial passenger structure `H_quark = H_color ⊗ I_2`, has C_3-isotype
> real-DOF count `(μ_quark, ν_quark) = (4, 8)`. This is `4 × (1, 2)` —
> same ratio as the charged-lepton `(μ_3D, ν_3D) = (1, 2)`, just scaled
> by the dim of the weak passenger space.

The BAE/A1 admission count is unchanged. The bounded obstruction
extends to the quark sector via tensor preservation.

## Setup

### Premises (A_min for this probe)

| ID | Statement | Class |
|---|---|---|
| Cl3 | physical `Cl(3)` local algebra | repo baseline; legacy alias `A1` in [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3 | `Z³` spatial substrate | repo baseline; legacy alias `A2` in the same source |
| SMEmbed | `Cl(3)` → SM embedding: P_symm × fiber = 6D quark block (3 colors × 2 weak doublet, Y = +1/3) | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 ≅ ℂ³ is `aI + bC + b̄C²` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `‖H‖² = 3a² + 6\|b\|²` on `M_3(ℂ)_Herm` | retained: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | Weight-class theorem: κ = 2μ/ν | retained: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| Probe27 | F3 vs F1 selection is sector-independent on Z³ BZ-corner inventory | upstream: [`KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md`](KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md) |
| Probe25 | F3 forced by free Gaussian dynamics on Herm_circ(3) at hw=1 | upstream: [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) |
| CrossSector | N_gen = N_color = 3 retained equality | retained: [`CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms or imports
- NO admitted SM Yukawa-coupling pattern as derivation input
- NO PMNS or CKM matrix elements as derivation input

## The structural lemma at issue

**Hypothesis (this probe):**

> The quark sector's 6-dim host space `(3-color × 2-weak)` admits a
> C_3-isotype decomposition with multiplicity ratio different from
> `(1, 2)`. In particular, F1 = `(1, 1)` may be reachable on 6D where
> it was structurally absent on 3D.

**Required chain:**

1. Identify the C_3 generation cycle action on 6D.
2. Decompose 6D = `C³ ⊗ C²` under C_3.
3. Compute C_3-invariant Hermitian operator space on 6D.
4. Count real DOFs by C_3 isotype.
5. Test whether ratio differs from `(1, 2)`.

**Step 5 fails**: tensor-multiplication with a C_3-trivial passenger
preserves isotype ratios uniformly.

This note demonstrates each step explicitly in the runner.

## Theorem (quark-sector BAE-analog bounded obstruction)

**Theorem.** On A1 + A2 + retained `CL3_SM_EMBEDDING_THEOREM`
(P_symm × I_fiber = 6D quark block with Y = +1/3) + retained
`KOIDE_CIRCULANT_CHARACTER_DERIVATION` + retained
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM` + retained
`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM` + Probe 27's framing
result (sector-independence of F3) + admissible standard math
machinery:

```
The hypothesis "quark-sector BAE-analog has different multiplicity
structure than charged-lepton BAE due to 6-dim host space, yielding F1
(κ = 2 = BAE) where 3-dim gave F3 (κ = 1)" cannot be derived from
retained Cl(3)/Z³ + SM-embedding content. Five independent structural
barriers each block the proposed chain:

  (B1) 6D = (3-color) ⊗ (2-weak) per CL3_SM_EMBEDDING_THEOREM. C_3
       acts on color factor only (weak factor C_3-trivial under
       retained content).
  (B2) Z_3 representation theory on color: 3-color = trivial ⊕ ω ⊕ ω̄,
       isotype dims (1, 1, 1).
  (B3) Tensor with C_3-trivial passenger of dim n: V_color ⊗ V_passenger
       gives isotype dims (n, n, n) — uniform scaling preserving ratio.
  (B4) Real-DOF count of C_3-invariant Hermitian on 6D: trivial isotype
       contributes 4 real DOFs (= 1 × dim(M_2(C)_Herm) = 4); doublet
       isotype contributes 4 + 4 = 8 real DOFs. Ratio (4, 8) = 4 × (1, 2).
  (B5) Even with C_3 acting non-trivially on weak factor (entangled
       color-weak Z_3 action), the tensor product of the regular Z_3
       rep with any V_2 gives dim(V_2) × regular rep — isotype dims all
       equal — preserving (1, 1) → (n, n, n) (still ratio 1:1:1, NOT
       favoring trivial vs doublet).

Therefore quark-sector BAE-analog closure is structurally barred under
the stated retained source-stack surface. The BAE/A1 admission count
is unchanged.
```

**Proof.** Each barrier is verified independently in the paired runner
with explicit numerical confirmations (55 PASS / 0 FAIL).

### Barrier 1: 6D = (3-color) ⊗ (2-weak) per CL3_SM_EMBEDDING

By retained `CL3_SM_EMBEDDING_THEOREM` Section F:
```
P_symm projector on 8D taste cube has rank 6.
P_symm × I_fiber = 6D block with Y eigenvalue +1/3 (quark).
Decomposition: P_symm acts on 3D symmetric base (3 colors via SU(3)_C);
              I_fiber acts on 2D weak doublet (SU(2)_weak).
```

Per retained `THREE_GENERATION_OBSERVABLE_THEOREM` and the Section H
discussion in the embedding script, the C_3 generation cycle on this
sector cycles the 3-color factor (axes-permutation `C_3[111]` on Z³).
The weak factor is a passenger under this C_3 — there is no retained
operator that mixes weak components via the generation cycle.

### Barrier 2: Z_3 isotype split on 3-color is (1, 1, 1)

The Z_3 acting on `ℂ³` via cyclic permutation has eigenvalues
`(1, ω, ω̄)` with ω = exp(2πi/3). Each is 1-dimensional. Verified
algebraically in the runner Section 2.

### Barrier 3: Tensor with C_3-trivial passenger preserves ratio

If C_3 acts trivially on `V_2` (so `V_2 ≅ n × trivial`), then
```
V_color ⊗ V_2 = (trivial ⊕ ω ⊕ ω̄) ⊗ (n × trivial)
              = n × trivial ⊕ n × ω ⊕ n × ω̄
```
Isotype dims `(n, n, n)`, ratios preserved.

For 6D quark sector with `V_2 = ℂ²` (weak passenger):
```
6D isotype dims: (2, 2, 2)
```

### Barrier 4: Real-DOF Hermitian count on 6D

C_3-invariant Hermitian operators on 6D split into BLOCK-DIAGONAL form
in the C_3 isotype basis (Schur's lemma: C_3-equivariance forces
zero off-diagonal blocks between distinct isotypes).

```
H = P_trivial ⊗ M_T + P_omega ⊗ M_O + P_omega_bar ⊗ M_OB
```
where each `M_X` is a 2×2 Hermitian on the 2D weak passenger space
(4 real DOFs each).

Counting:
- Trivial isotype: 4 real DOFs (= μ_quark)
- Omega isotype: 4 real DOFs
- Omega_bar isotype: 4 real DOFs
- Doublet (omega + omega_bar) total: 8 real DOFs (= ν_quark)
- Grand total: 12 real DOFs

Ratio `(μ_quark, ν_quark) = (4, 8) = 4 × (1, 2)`.

### Barrier 5: Even entangled C_3-color × C_3-weak preserves the structure

If C_3 acts non-trivially on weak (e.g., `C_3_weak = diag(ω, ω̄)`),
then by the regular-representation tensor identity:
```
(regular rep of Z_3) ⊗ V_2 = dim(V_2) × (regular rep of Z_3)
```
because `regular ⊗ X = dim(X) × regular` for any rep X over ℂ (since
the regular rep contains every irrep with multiplicity 1, and
`irrep_i ⊗ X` decomposes by character convolution that sums to
`dim(X) × irrep_i` when summed over `i`).

For `dim(V_2) = 2`: isotype dims still `(2, 2, 2)`.

Verified in the runner Section 11 with concrete enumeration of
`(a, b, c)` tensor splits on `V_2`.

## Numerical verification (in paired runner)

The runner `cl3_quark_bae_analog_2026_05_10_quarkBAE.py` verifies each
step explicitly:

- **Section 1**: Charged-lepton 3D baseline — Brannen ansatz Hermitian, C_3-equivariant; Frobenius decomposition `‖H‖² = 3a² + 6|b|²`; eigenvalue closed form; isotype real-DOF count `(μ, ν) = (1, 2)`; κ = 1.
- **Section 2**: 6D quark sector construction — `C_3 ⊗ I_2` on 6D has order 3, isotype dims `(2, 2, 2)`.
- **Section 3**: Basis of C_3-invariant Hermitian on 6D — 12 elements (3 color × 4 weak Hermitian), all C_3-invariant Hermitian.
- **Section 4**: Real-DOF isotype counts — `μ_quark = 4` (trivial), `ν_quark = 8` (doublet); ratio preserved.
- **Section 5**: Isotype-pure projector basis — `P_trivial`, `P_omega`, `P_omega_bar` rank-1 projectors; per-block Hermitian DOF count via Schur.
- **Section 6**: Brannen passenger lift — eigenvalues are 3 charged-lepton eigenvalues, each doubled (3 distinct levels with multiplicity 2).
- **Section 7**: Full 12-DOF Brannen-extended ansatz — generic 6 distinct eigenvalues.
- **Section 8**: Frobenius decomposition on 6D — `‖H_quark‖² = 6a² + 12|b|²` (passenger lift); ratio `6:12 = 1:2` preserved.
- **Section 9**: BAE-analog point test — at `a² = 2|b|²`, 6D passenger gives degenerate triplet (each doubled); κ = 1.
- **Section 10**: C_3-on-weak hypothesis test — even with `C_3_weak = diag(ω, ω̄)`, isotype dims remain `(2, 2, 2)`.
- **Section 11**: Generic Z_3 tensor isotype theorem — `(1,1,1) ⊗ (a,b,c) = (a+b+c, a+b+c, a+b+c)` regardless of `(a, b, c)`.
- **Section 12**: Schur Hermitian DOF count on 6D — `(μ, ν) = (4, 8)`, total 12.
- **Section 13**: Verdict — quark-sector BAE structurally barred at κ = 1 = F3 (NOT 2 = F1 = BAE).
- **Section 14**: Convention robustness — C_3 vs C_3⁻¹, weak swap, scaling.
- **Section 15**: Empirical falsifiability anchor — PDG quark Q values (post-derivation).

**Total: 55 PASS / 0 FAIL.**

## Comparison to prior 30-probe BAE campaign

The 30-probe campaign attacked F1/BAE closure on the charged-lepton
sector (3-dim host). All 30 probes terminated in bounded obstruction
or sharpened obstruction. Probe 27 (PR #824) tested the hw=N
sector-relocation hypothesis within the staggered Z³ APBC BZ-corner
inventory `{0,1}³` and barred all 4 sectors `(0, 1, 2, 3)`.

This probe extends the campaign to the **larger 6-dim quark sector**
of `CL3_SM_EMBEDDING_THEOREM` — a host space outside the BZ-corner
inventory of Probe 27 (since BZ corners alone don't capture the
weak-isospin doubling).

| Probe | Sector tested | Verdict |
|---|---|---|
| 25 (physical extremization) | 3-dim hw=1 charged-lepton | F3 forced; F1 barred |
| 27 (hw=N identification) | 3-dim hw=0,1,2,3 BZ corners on Z³ | F3 sector-independent |
| 28 (full retained interactions) | 3-dim hw=1 with all retained operators | F3 preserved |
| **This probe (quark BAE-analog)** | **6-dim P_symm × fiber (quark sector)** | **F3 ratio preserved by tensor invariance** |

**This probe's contribution:** Sharpens the meta-pattern further. F3
selection is not a *charged-lepton-localized* artifact — it is a
*tensor-invariance* consequence of C_3 representation theory acting
on host spaces of the form `(3-color C_3) ⊗ (passenger)`. Sector
extension via passenger does not recover BAE.

## What this closes

- **Quark BAE-analog bounded obstruction** (sector-extension closure).
  Five independent structural barriers verified.
- **Sharpens the "different sector might escape" hypothesis** for the
  quark analog. The hypothesis is structurally barred: tensor with
  C_3-trivial passenger preserves the (1, 2) isotype ratio.
- **Confirms the Probe 25/27/28 finding extends** beyond the 3-dim BZ
  corners — the F3 forcing applies to any host of form `3-color ⊗ passenger`.
- **Audit-defensibility**: explicit numerical verifications across all
  isotype counts, projector identities, and tensor-passenger structures.

## What this does NOT close

- BAE admission count is unchanged. BAE remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- The substep4 AC residual (`AC_φλ`, the explicit identification of
  framework's hw=1 3-fold structure with SM matter generations) is
  unaffected.
- Charged-lepton Koide closure remains a bounded observational-pin
  package; status unchanged.
- This probe does NOT imply quark Koide ratios `Q_up ≠ 2/3`,
  `Q_down ≠ 2/3` are derived — those remain empirical observations.
- The retained block-total Frobenius theorem retains its theorem
  status. This note does NOT retract that — it shows the 6-dim sector
  extension preserves the F3 forcing.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| 6D quark sector = 3-color × 2-weak | A retained derivation showing the SM embedding gives a different decomposition for the quark sector (e.g., not P_symm × fiber). |
| C_3 acts only on color factor | A retained operator that mixes weak doublet under generation cycle (currently absent from retained content). |
| Passenger preserves isotype ratio | A retained Z_3 rep theory result showing tensor with non-passenger gives different isotype dims (would require breaking ω, ω̄ pair). |
| Quark BAE = κ = 2 forced by retained dynamics on 6D | A retained free-Gaussian or interacting dynamics on the 6D Hermitian space that selects F1 (1, 1) ratio over F3 (1, 2). |
| Structural ratio (4, 8) for 6D | An explicit C_3-invariant Hermitian on 6D NOT of the form `P_color ⊗ M_weak` for one of the three isotype projectors and a Hermitian M_weak. (Schur's lemma forbids this.) |
| Numerical empirical anchor | PDG: `Q_up ≈ 0.892`, `Q_down ≈ 0.748`, neither matches 2/3. The probe's prediction `κ_quark = 1` (degenerate triplet) is incompatible with the PDG hierarchical mass spectrum, suggesting the framework's quark-mass derivation route also faces an analog of Probe 29's partial-falsification residue. |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative quark-BAE-analog
boundary: the hypothesis "quark-sector 6D host space yields F1 (BAE)"
is blocked by:

1. C_3 acts only on color factor of `3-color ⊗ 2-weak`.
2. Tensor with C_3-trivial passenger preserves isotype dim ratio uniformly.
3. C_3-invariant Hermitian on 6D = sum of `P_isotype ⊗ M_weak` blocks.
4. Real-DOF count: `(μ_quark, ν_quark) = (4, 8) = 4 × (1, 2)`.
5. Even with C_3 acting non-trivially on weak (entangled), regular-rep
   tensor identity preserves uniform isotype dims.

No new admissions are proposed. BAE remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "quark-sector might escape via 6-dim structure" hypothesis is sharpened from "open conjecture" to "structurally barred under retained content; tensor-passenger preserves the ratio." |
| V2 | New derivation? | The five-barrier obstruction argument applied to the 6-dim quark sector via tensor invariance is new structural content. Prior 30 probes worked on 3-dim host spaces only. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) 6D = 3-color × 2-weak per CL3_SM_EMBEDDING, (ii) C_3 action on color only, (iii) Z_3 isotype split (1,1,1) on color, (iv) Schur block-diagonal Hermitian structure, (v) regular-rep tensor identity for the entangled-C_3 case. |
| V4 | Marginal content non-trivial? | Yes — the tensor-invariance theorem for C_3 isotype ratios is a structural observation not previously catalogued in the BAE probe series. The extension to the SM-embedding quark sector is a structurally NEW route. |
| V5 | One-step variant? | No — this probe addresses the structurally NEW question of whether the larger SM-embedding host space changes the F-functional structure, not covered by the 30-probe campaign (all working at 3D). |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior BAE probes. The five-barrier obstruction
  argument applied to the SM-embedding 6D quark sector is new
  structural content with explicit numerical verifications.
- Identifies a NEW barrier class (sector EXTENSION via tensor
  passenger, not sector RELOCATION within BZ corners) not present in
  the prior 30 probes.
- Sharpens the "different sector via SM embedding" hypothesis from
  open-conjectural to closed-negatively, with a clear list of what
  new retained content would be required to reopen it.
- Provides explicit numerical verifications (6D construction, isotype
  decomposition, Schur block structure, passenger-tensor identity,
  Brannen lift eigenvalue degeneracy, regular-rep entangled case).
- Confirms the meta-pattern across now-31 probes: framework's
  retained content does not give a route to BAE closure, and the F3
  forcing is robust under host-space extensions of the form
  `3-color ⊗ passenger`.

## Cross-references

- BAE / A1 derivation status (parent): [`KOIDE_A1_DERIVATION_STATUS_NOTE.md`](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
- 30-probe campaign synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Probe 25 (physical extremization, F3 forcing): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 27 (sector-relocation barrier on Z³ BZ corners): [`KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md`](KOIDE_BAE_PROBE_HW_SECTOR_IDENTIFICATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe27.md)
- CL3 → SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Brannen circulant character: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Block-total Frobenius measure: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class theorem: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- Cross-sector closure N_gen = N_color: [`CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

## Validation

```bash
python3 scripts/cl3_quark_bae_analog_2026_05_10_quarkBAE.py
```

Expected output: structural verification of (i) 3D charged-lepton
baseline `(μ, ν) = (1, 2)`; (ii) 6D quark sector construction with
isotype dims `(2, 2, 2)`; (iii) basis of 12 C_3-invariant Hermitians;
(iv) projector identities; (v) tensor-passenger Hermitian structure;
(vi) eigenvalue degeneracy under passenger lift; (vii) full 12-DOF
generic spectrum with 6 distinct eigenvalues; (viii) Frobenius
decomposition `‖H_quark‖² = 6a² + 12|b|²`; (ix) BAE-point κ
calculation; (x) entangled C_3-weak preservation; (xi) generic
Z_3-tensor isotype theorem; (xii) Schur block-diagonal Hermitian
count; (xiii) verdict; (xiv) convention robustness; (xv)
falsifiability anchor.

**Total: 55 PASS / 0 FAIL.**

Cached: [`logs/runner-cache/cl3_quark_bae_analog_2026_05_10_quarkBAE.txt`](../logs/runner-cache/cl3_quark_bae_analog_2026_05_10_quarkBAE.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note applies
  the "consistency equality is not derivation" rule. The fact that 6D
  has the same `(1, 2)` ratio as 3D (scaled by passenger) is a
  consistency identity (via tensor invariance); it does NOT supply a
  new positive route to BAE closure.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "the host-space dimension forces a fixed F-functional
  structure" by exhausting the SM-embedding's quark-sector decomposition
  and verifying that tensor-passenger preserves isotype ratios.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent BAE admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier argument
  with explicit numerical verifications is substantive new structural
  content, not a relabel of any prior BAE probe.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional retained content would be
  needed (a non-passenger entanglement of color × weak under retained
  C_3, a non-Schur Hermitian structure, a different SM-embedding
  decomposition).
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent barriers, 15 sections in the
  runner) on a single structural hypothesis.
- `feedback_review_loop_source_only_policy.md`: this note is a source
  theorem note; the paired runner produces cached output; no
  output-packets, lane promotions, or synthesis notes are introduced.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: this probe is a
  fragmentation atom of the broader BAE closure problem, addressing
  the specific structural question "does sector extension to 6D escape
  the F3 trap?" without bundling other admissions.
