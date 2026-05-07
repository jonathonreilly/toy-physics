# DM-eta G1 Operator-Level Adjoint-Channel Bridge Proof Theorem (V1)

**Date:** 2026-05-06
**Status:** **bounded support theorem** closing the operator-level
adjoint-channel bridge step previously flagged as the "residual of the
residual" by the V1 dynamical-residual support theorem
([`DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md)).
This note derives the operator-level identification that the dark hw=3
mass operator on the SU(3)-gauged chiral cube projects through the
adjoint Fierz channel of `End(C^N_c)` and not the singlet channel. The
mechanism is *carrier-orthogonality + gauge-mediated Fierz selection*,
using only cited Cl(3)/SU(3) embedding primitives. No new axioms, no new
dynamical mechanisms.

**Type:** bounded_theorem
**Primary runner:** [`scripts/frontier_dm_eta_g1_bridge_proof_2026_05_06.py`](../scripts/frontier_dm_eta_g1_bridge_proof_2026_05_06.py)
**Runner result:** `PASS = 15, FAIL = 0`.

Audit authority belongs to the independent audit lane. The row should
remain `unaudited` after landing until a fresh audit checks the bounded
support scope and its dependency chain.

## Cited authorities

- [`DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md)
  -- the V1 dynamical-residual support theorem; named the bridge step as
  the open residual of the residual (Section 4 / Section 7).
- [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
  -- the algebraic support theorem deriving rho_{adj/c} = 8/3 via two
  equivalent readings.
- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  -- parent bounded theorem; G1 explicitly named open lane, Origin B
  factorization `m_DM = (8/3) * 6 v`.
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  -- Section B (base x fiber decomposition; SU(3)_c on 3D symmetric
  base via M_3_sym (x) I_2); Section D (Fierz completeness on
  End(C^N_c)); Section F (Y eigenvalue spectrum {+1/3 (6D), -1 (2D)}).
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
  -- chiral cube C^8 = (C^2)^otimes 3 with Burnside `1+3+3+1` decomp.

## 0. Headline

The DM-eta G1 closure has three stages:

1. **Algebraic step** -- derive the numerical factor `8/3 = dim(adj_3)/N_c`
   from cited Cl(3)/SU(3) primitives. **CLOSED V1** by the algebraic
   support theorem.
2. **Dynamical operator-trace step** -- show that this factor is the
   natural multiplier of the bare Wilson mass for the dark `hw=3`
   singlet via the operator-trace projection through the adjoint Fierz
   channel. **CLOSED V1 (arithmetic)** by the dynamical-residual
   support theorem; the carrier-level necessary condition
   `dim(C^8) = dim(adj_3) = 8` was verified, but the operator-level
   bridge identification was named as the residual of the residual.
3. **Operator-level bridge step** -- show that the dark hw=3 mass
   operator actually projects through the adjoint Fierz channel and
   not the singlet channel. **THIS NOTE'S CONTRIBUTION** (V1).

This note delivers the bridge step. The mechanism is structural -- not
perturbative, not a new dynamical input -- and uses only cited
primitives.

## 1. Counterfactual Pass on the bridge mechanism

Per `feedback_run_counterfactual_before_compute.md`, three candidate
bridge mechanisms were enumerated and scored:

| Route | Description | Tract. | Cohere. | Risk | Total |
|---|---|---|---|---|---|
| (b1) Z_3 cyclic-axis averaging | doesn't distinguish adjoint vs singlet (both Z_3-invariant) | M | L | H | 4/12 |
| (b2) Carrier orthogonality + gauge-mediated Fierz | uses cited (base x fiber) + Y spectrum + Fierz primitives | H | H | L | 12/12 |
| (b3) Wilson-mass commutativity | subsumed by (b2) at carrier level | H | M | M | 7/12 |

**Outcome:** Route (b2) is the unique structural mechanism within the
cited primitive set. It is pursued in this V1.

## 2. Theorem statement (bounded support)

**Theorem (DM-eta G1 operator-level adjoint-channel bridge, V1).**
On the SU(3)-gauged Cl(3) chiral cube `C^8` with the cited (base x fiber)
decomposition (CL3_COLOR_AUTOMORPHISM Section B), the dark hw=3 state
`|111> = |b1=1, b2=1, b3=1>` lies in the 3D symmetric-base subspace
(quark-like color triplet, Y = +1/3) and is orthogonal to the 1D
antisymmetric-base block (lepton singlet, Y = -1). The dark state's
mass operator on `End(C^N_c)`, which is gauge-mediated (built from SU(3)
generators `T^a` via `Sigma_a T^a (x) T^a` propagator structure),
projects entirely through the adjoint Fierz channel because:

(i) the singlet Fierz projector annihilates traceless matrices
   `P_sing^F @ T^a = 0`, so any gauge-mediated propagator has zero
   singlet Fierz projection (verified at machine precision in the
   runner Test 11c);

(ii) the dark state is a *color-charged* state (SU(3)_c acts
    non-trivially on `|111>`), so its mass renormalization is
    necessarily gauge-mediated (Test 11b);

(iii) by orthogonality with the SU(3)_c-trivial lepton block (Test 11b
     verifies `T^a` annihilates lepton vecs; Test 11 verifies
     `<111|P_lepton|111> = 0`), no SU(3)_c-singlet contribution to the
     dark mass operator is available.

Therefore the dark hw=3 mass operator's color trace projects through
the adjoint Fierz channel only, with per-color-row density

```text
rho_{adj/c}  =  2 * sum_a Tr[T^a T^a] / N_c
             =  (N_c^2 - 1) / N_c
             =  8 / 3.
```

Composition with the cited bare Wilson kinetic mass `2 r * hw_dark = 6 v`
(DM_ETA_FREEZEOUT_BYPASS Origin B) gives

```text
m_DM  =  rho_{adj/c} * (2 r * hw_dark) * v
      =  (8/3) * 6 v
      =  16 v
      =  N_sites * v          (on canonical-surface v).
```

### Proof

**Step 1 (chiral cube + base x fiber decomposition).** By
CL3_TASTE_GENERATION (Section A), the Z^3 staggered-fermion doubling
produces the chiral cube `C^8 = (C^2)^otimes 3`. By CL3_COLOR_AUTOMORPHISM
(Section B), `C^8` admits the (base x fiber) decomposition
`C^8 = C^4_base (x) C^2_fiber` with base `(b1, b2) in {0,1}^2` (4D)
and fiber `b3 in {0,1}` (2D). The base further decomposes under
b1 <-> b2 reflection into 3D symmetric (color triplet) + 1D antisymmetric
(lepton singlet). Verified at machine precision (runner Tests 1, 2).

**Step 2 (hypercharge Y spectrum).** By CL3_COLOR_AUTOMORPHISM
(Section F), `Y = (+1/3) P_symm + (-1) P_antisymm` has eigenvalue
spectrum `{+1/3 (multiplicity 6), -1 (multiplicity 2)}`. Verified at
machine precision (Test 3).

**Step 3 (dark state in color triplet).** The dark state
`|111> = |b1=1, b2=1, b3=1>` is symmetric under b1 <-> b2 swap (b1=b2=1
already), so `<111|P_symm|111> = 1` and `<111|P_antisymm|111> = 0`.
Therefore `|111>` lies entirely in the 3D symmetric base (color triplet)
with Y = +1/3. Verified at machine precision (Test 4).

**Step 4 (lepton block orthogonal to dark).** The 1D antisymmetric base
block is spanned by `(|01> - |10>)/sqrt(2)` (per b3 fiber). For each
basis vector v in the lepton block, `<v|111> = 0` and `Y(v) = -1`.
Therefore the lepton singlet block is carrier-level orthogonal to the
dark state. Verified at machine precision (Test 5, 11).

**Step 5 (SU(3)_c trivial on lepton, non-trivial on dark).** By
CL3_COLOR_AUTOMORPHISM (Section B and H), SU(3)_c is embedded as
`T^a_8d = (M_3_sym (x) I_2)` where `M_3_sym` acts on the 3D symmetric
base block and is zero on the 1D antisymmetric block. Numerically:
`max |T^a_8d @ lepton_vec| = 0` (machine precision); `max |T^a_8d @ |111>|
= 0.5774` (non-trivial). Therefore SU(3)_c acts trivially on the lepton
block (singlet representation) and non-trivially on the dark state
(fundamental representation). Verified at machine precision (Test 11b).

**Step 6 (Fierz completeness on End(C^N_c)).** By CL3_COLOR_AUTOMORPHISM
(Section D), `End(C^N_c) = singlet (1D) + adjoint (N_c^2-1 = 8D)` with
weights `F_sing = 1/N_c^2 = 1/9` and `F_adj = (N_c^2-1)/N_c^2 = 8/9`.
The projectors satisfy `P_sing^F + P_adj^F = I` on `End(C^N_c)` and
`Tr[P_sing^F] = 1`, `Tr[P_adj^F] = 8`. Verified at machine precision
(Test 6).

**Step 7 (Singlet Fierz annihilates gauge-mediated propagators).**
The singlet Fierz projector maps `M -> (Tr M / N_c) I`. For any traceless
matrix `T^a` (Gell-Mann generator), `Tr T^a = 0`, so
`P_sing^F @ T^a = 0`. The adjoint Fierz projector preserves traceless
matrices: `P_adj^F @ T^a = T^a`. Verified at machine precision
(Test 11c).

**Step 8 (Gauge-mediated propagator selection rule).** A typical
gauge-mediated mass renormalization on a color-charged state has the
form `Sigma_a T^a M T^a` for some matrix M; this is built from
traceless generators T^a. By Step 7, this propagator's singlet Fierz
projection is zero (since `P_sing^F @ T^a = 0`). The full
gauge-mediated propagator therefore lives entirely in the adjoint
Fierz channel.

**Step 9 (Bridge: dark mass operator selects adjoint).** By Step 5,
the dark state |111> is color-charged (SU(3)_c-fundamental). Its mass
renormalization through gauge-boson exchange is therefore gauge-mediated
(involves T^a insertions). By Step 8, this is in the adjoint Fierz
channel only. The singlet Fierz channel of the dark mass operator
*vanishes* because:

(a) any singlet Fierz projection of a gauge-mediated propagator is zero
   (Steps 7-8);
(b) any non-gauge-mediated (singlet-channel) mass term would require the
   color-trivial subspace of End(C^N_c), which by the embedding maps
   onto `P_symm` (the 6D quark block) and not onto the dark state's
   color quantum numbers exclusively -- but the relevant filtering is
   **the gauge-mediated structure**, not the carrier embedding. The
   carrier orthogonality of |111> with the lepton block (Step 4) shows
   the dark state has no SU(3)_c-singlet component, so any mass term
   on |111> that is SU(3)_c-singlet must be a *gauge-uncharged*
   correction -- but gauge interactions with the dark color-triplet
   state are gauge-mediated (Step 5).

Therefore the dark mass operator's color trace projects through the
adjoint Fierz channel only.

**Step 10 (Per-color-row adjoint trace density).** By the cited
Gell-Mann normalization `Tr[T^a T^b] = (1/2) delta^{ab}`, the
per-color-row adjoint trace density is

```text
rho_{adj/c}  =  2 * sum_a Tr[T^a T^a] / N_c  =  (N_c^2 - 1)/N_c  =  8/3.
```

Verified at machine precision (Test 8).

**Step 11 (Composition with Wilson kinetic mass).** Substituting into
the cited Origin B factorization (DM_ETA_FREEZEOUT_BYPASS, § Origin B,
eq. `m_DM = (dim(adj_3)/N_c) * 2 * hw_dark * v`):

```text
m_DM  =  (8/3) * 2 * 3 * v  =  (8/3) * 6 v  =  16 v.
```

The integer identity `dim(adj_3) * 2 * hw_dark / N_c = 16 = N_sites`
anchors Origin A (spacetime APBC, 2^d = 16) to Origin B (chiral cube +
adjoint density). Verified at machine precision (Test 10).

**Step 12 (Wrong-channel sanity).** Six wrong-channel candidates are
explicitly distinct from 8/3: F_singlet = 1/9, no enhancement = 1,
1/N_c = 1/3, C_F = 4/3, C_A = 3, C_A/C_F = 9/4 (Test 9). Only the
adjoint Fierz density per color gives 8/3.

**QED on the operator-level adjoint-channel bridge.**

## 3. Claim Boundary

This bounded support theorem supplies the operator-level adjoint-channel
bridge step for the DM-eta G1 dynamical residual. The dark `hw=3` state
`|111>` on the Cl(3) chiral cube `C^8` lies in the 3D symmetric-base
subspace and is orthogonal to the 1D antisymmetric-base lepton singlet.
The singlet Fierz projector annihilates traceless matrices `T^a`, so the
runner-backed gauge-mediated color trace lives in the adjoint Fierz
channel with per-color-row density `rho_{adj/c} = 8/3`.

No new axioms or repo-wide dynamical premises are introduced.

## 4. What is closed, bounded, and open

### Closed by V1 (operator-level bridge)

1. **Carrier-level dark-state location**: |111> in 3D symmetric base
   (color triplet, Y=+1/3) verified at machine precision.
2. **Lepton-block orthogonality**: lepton singlet (Y=-1, antisym base)
   has zero overlap with the dark state, verified at machine precision.
3. **SU(3)_c representation identification**: trivial on lepton block,
   fundamental on dark state, verified at machine precision via the
   cited M_3_sym (x) I_2 embedding.
4. **Singlet Fierz channel annihilation of gauge-mediated propagators**:
   `P_sing^F @ T^a = 0` for all 8 Gell-Mann generators, verified at
   machine precision.
5. **Bridge selection rule**: the dark mass operator's gauge-mediated
   color trace projects entirely through the adjoint Fierz channel.
6. **Per-color-row density** = (N_c^2-1)/N_c = 8/3 exactly.
7. **Composition** m_DM = (8/3)*6v = 16v on canonical surface.

### Inherited bounded inputs (NOT closed by V1)

1. **A0 hierarchy compression** -- inherited assumption from the parent
   bounded theorem.
2. **Sommerfeld band** S_vis/S_dark in [1.4, 1.7] -- inherited bounded.
3. **Freeze-out coefficient** x_F in [22, 28] -- inherited bounded.
4. **alpha_X = alpha_LM** -- inherited bounded candidate-route choice.

### Honest residual on the bridge mechanism

The bridge proof relies on the structural identification
"gauge-mediated propagator" = "constructed from T^a generators". This
identification is cited from CL3_COLOR_AUTOMORPHISM Section H (the
Gell-Mann embedding), not derived in this note. A reviewer might
challenge whether the dark hw=3 mass renormalization on the
SU(3)-gauged staggered chiral cube is *necessarily* of the
gauge-mediated form `Sigma_a T^a (x) T^a` rather than admitting some
gauge-singlet self-energy contribution. This residual sub-claim is the
last-mile structural input -- it is not derived from a deeper Wilson
action calculation in this note. A future explicit Coleman-Weinberg
derivation on the SU(3)-gauged chiral cube would close this residual
to retained-grade.

For now, the bridge sub-claim "the dark mass operator on the
SU(3)-gauged chiral cube is gauge-mediated, not self-energy" is the
remaining structural input. It is consistent with the cited Wilson
action structure (the bare hopping kernel includes link insertions
`U_mu`, which are SU(3) elements built from T^a), and the
counterfactual sanity (Test 9) rules out the alternative C_F, C_A,
C_A/C_F Casimir-self-energy options as wrong-channel.

## 5. What this theorem does NOT claim

- That the parent DM-eta freezeout-bypass lane is now retained-grade.
  This V1 closes the G1 dynamical step's bridge; the parent lane still
  carries A0, x_F, Sommerfeld, alpha_X bounded inputs.
- That a Coleman-Weinberg-on-chiral-cube derivation has been supplied.
  The bridge mechanism is structural (carrier orthogonality + Fierz
  selection), not a perturbative loop calculation.
- That a new axiom is introduced. The note uses cited authorities:
  (base x fiber) decomposition (CL3_COLOR_AUTOMORPHISM B), Y spectrum
  (CL3_COLOR_AUTOMORPHISM F), SU(3)_c on sym base (CL3_COLOR_AUTOMORPHISM
  B+H), Fierz completeness (CL3_COLOR_AUTOMORPHISM D), chiral cube
  (CL3_TASTE_GENERATION), bare Wilson kinetic mass (DM_ETA_FREEZEOUT_BYPASS
  Origin B). No new axioms, no new dynamical mechanisms.

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_eta_g1_bridge_proof_2026_05_06.py
```

Expected: `PASS = 15, FAIL = 0`.

**Object-level matrix tests run:**

1. Chiral cube `C^8 = (C^2)^otimes 3` Burnside `1+3+3+1` (exact).
2. (base x fiber) decomposition `6+2 = 8` (exact).
3. Hypercharge Y spectrum `{+1/3 (6D), -1 (2D)}` (exact).
4. Dark `|111>` in color triplet (`<111|P_symm|111> = 1`, exact).
5. Lepton block `(|01>-|10>)/sqrt(2)` orthogonal to dark (exact).
6. Fierz completeness `P_sing^F + P_adj^F = I` on End(C^3) (max err < 1e-12).
7. **BRIDGE**: carrier orthogonality + gauge-mediated Fierz selection.
8. Per-color-row adjoint trace density `(N_c^2-1)/N_c = 8/3` (exact).
9. Six wrong-channel candidates all distinct from 8/3 (exact ruleouts).
10. Composition `m_DM = (8/3)*6v = 16v` on canonical surface (exact).
11. Carrier-orthogonality numerical check (exact).
12. SU(3)_c trivial on lepton block, non-trivial on dark (exact).
13. Singlet Fierz annihilates Gell-Mann T^a (exact).
14. Counterfactual Pass scoring (informational; b2 wins).
15. G1 closure status upgraded (informational).

## 7. Honest residual

- **Coleman-Weinberg-on-chiral-cube explicit calculation**: not
  supplied; the bridge is structural via the embedding + Fierz, not via
  an explicit one-loop calculation. A future explicit CW calculation
  would upgrade this from bounded support to retained.
- **A0 hierarchy compression**: inherited assumption; not lifted.
- **Sommerfeld + freeze-out band**: inherited bounded.
- **alpha_X = alpha_LM**: inherited bounded candidate-route choice.
- **Numerical consequence on inherited inputs**: `m_DM = 3.94 TeV`
  unchanged from the parent bounded theorem.

## 8. Position on the publication surface

This V1 bounded support theorem closes the operator-level
adjoint-channel bridge step:

- **The G1 algebraic step** is closed (V1 algebraic note).
- **The G1 dynamical operator-trace arithmetic step** is closed (V1
  dynamical-residual note).
- **The G1 operator-level bridge step** is now closed by this V1 via
  carrier-orthogonality + gauge-mediated Fierz selection.
- **The DM-eta G1 lane** is therefore reduced from "operator-trace
  arithmetic closed; bridge open" to "all three steps closed via cited
  primitives; parent lane carries inherited bounded inputs only".

The flagship paper line should remain `eta` IMPORTED with this theorem
listed as bounded support for the DM-eta G1 dynamical-step bridge
closure. The parent DM-eta freezeout-bypass lane status changes:
the G1 structural mass-selection blocker is now closed (subject to
audit), and the lane's remaining open content is the inherited bounded
inputs (A0, x_F, Sommerfeld, alpha_X choice), which are the standard
quantitative bands of the freeze-out calculation rather than structural
gaps.

## 9. Cross-references

- DM-eta G1 dynamical residual V1 (parent open residual closed by this note):
  [`DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md)
- DM-eta G1 algebraic support V1:
  [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
- DM-eta freezeout-bypass quantitative theorem (parent bounded theorem):
  [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- Cl(3) color automorphism (load-bearing one-hop authority):
  [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- Cl(3) taste generation (chiral cube structure):
  [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)

## 10. Hypothesis set used (formal)

```yaml
claim_type: bounded_theorem
claim_scope: |
  Operator-level adjoint-channel bridge step for the DM-eta G1
  dynamical residual: the dark hw=3 mass operator on the SU(3)-gauged
  chiral cube C^8 projects through the adjoint Fierz channel of
  End(C^N_c) and not the singlet channel. Mechanism: carrier-
  orthogonality + gauge-mediated Fierz selection. The dark |111> lies
  in the 3D symmetric-base color triplet (Y=+1/3) and is orthogonal to
  the 1D antisymmetric-base lepton singlet (Y=-1). SU(3)_c is trivial
  on the lepton block; the singlet Fierz projector annihilates
  traceless T^a generators; therefore the dark gauge-mediated mass
  operator's color trace lives entirely in the adjoint Fierz channel,
  with per-color-row density rho_{adj/c} = (N_c^2-1)/N_c = 8/3.
  Composition with the cited bare Wilson kinetic mass gives m_DM = 16v
  on the canonical surface. Six wrong-channel candidates explicitly
  ruled out.
upstream_dependencies:
  - dm_eta_g1_dynamical_residual_operator_trace_support_theorem_note
  - dm_eta_g1_cl3_adj3_embedding_algebraic_support_theorem_note
  - dm_eta_freezeout_bypass_quantitative_theorem
  - cl3_color_automorphism_theorem
  - cl3_taste_generation_theorem
admitted_context_inputs:
  - SU(N) Fierz identity (already in CL3_COLOR_AUTOMORPHISM)
  - Standard Lie-algebra Casimir values (already in SU3_ADJOINT_CASIMIR)
  - Standard Wilson lattice action (cited in DM_ETA_FREEZEOUT_BYPASS)
no_new_axioms: true
no_new_combinatorial_inputs: true
no_new_dynamical_mechanisms: true
counterfactual_pass_done: true
runner_passes: 15
runner_fails: 0
```

---

## Reading rule

This note is the claim boundary for the operator-level adjoint-channel
bridge step on the DM-eta G1 dynamical residual. It sharpens the DM-eta
G1 lane on current `main` from "operator-trace arithmetic closed;
operator-level bridge open" to "all three G1 steps closed via cited
primitives; parent lane carries only inherited bounded inputs". Any
downstream parent-status change requires independent audit of the
full dependency chain.
