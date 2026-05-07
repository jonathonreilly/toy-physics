# DM-eta G1 Dynamical Residual: Operator-Trace Support Theorem (V1)

**Date:** 2026-05-06
**Status:** **bounded support theorem** on the dynamical step of the
DM-eta G1 closure. This note sharpens the previously-flagged dynamical
residual by deriving `rho_{adj/c} = 8/3`
from the operator-trace projection through the adjoint Fierz channel
on End(C^N_c), conditional on a named "residual-of-the-residual" bridge
step. It does NOT change the parent DM-eta lane's ledger status.

**Type:** bounded_theorem
**Primary runner:** [`scripts/frontier_dm_eta_g1_dynamical_residual_2026_05_06.py`](../scripts/frontier_dm_eta_g1_dynamical_residual_2026_05_06.py)
**Runner result:** `PASS = 12, FAIL = 0`.
**Output log:** [`outputs/frontier_dm_eta_g1_dynamical_residual_2026_05_06.txt`](../outputs/frontier_dm_eta_g1_dynamical_residual_2026_05_06.txt)

Audit authority belongs to the independent audit lane. The row should
remain `unaudited` after landing until a fresh audit checks the bounded
support scope and its dependency chain.

## Cited authorities

- [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
  -- the algebraic support theorem deriving `rho_{adj/c} = 8/3` via two
  equivalent readings; flagged the dynamical step as the named open
  residual.
- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  -- parent bounded theorem; G1 explicitly named open lane, Origin B
  factorization `m_DM = (8/3) * 6 v`.
- [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
  -- the obstruction note ruling out the perturbative one-loop CW route
  and naming the three alternative routes (R1 Wilson doubling,
  R2 non-perturbative condensate, R3 Cl(3)/SU(3) embedding identity).
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  -- Section D Fierz completeness on End(C^N_c), singlet weight `1/N_c^2`,
  adjoint weight `(N_c^2-1)/N_c^2 = 8/9`, and `R_conn = 8/9`.
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
  -- chiral cube `C^8 = (C^2)^otimes 3` with Burnside `1+3+3+1` decomp.
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
  -- standard Casimir values `C_F = 4/3`, `C_A = 3` used in Counterfactual
  Pass ruleouts.

## 0. Headline

The DM-eta G1 closure has two stages:

1. **Algebraic step** -- derive the numerical factor `8/3 = dim(adj_3)/N_c`
   from cited Cl(3)/SU(3) primitives. **CLOSED V1** by the algebraic
   support theorem (2026-05-06).
2. **Dynamical step** -- show that this factor is the natural multiplier
   of the bare Wilson mass for the dark `hw=3` singlet, rather than
   `1`, `1/N_c`, `C_F = 4/3`, or `C_A/C_F = 9/4`. **OPEN** at V1 of the
   algebraic step.

This V1 sharpens the bounded dynamical step. After a 5-way Counterfactual
Pass on dynamical mechanisms, the unique
tractable route within the cited primitive set is the **operator-trace
projection through the adjoint Fierz channel on End(C^N_c)**. The
arithmetic is verified at the matrix-element level (`PASS = 12, FAIL = 0`).

The "residual of the residual" -- the bridge step that the dark `hw=3`
mass operator on the SU(3)-gauged chiral cube actually projects through
the adjoint Fierz channel rather than the singlet channel -- is not
closed here. The carrier-level necessary condition `dim(C^8) = dim(adj_3) = 8`
holds exactly; the operator-level bridge identification requires a
separate theorem.

## 1. Counterfactual Pass on dynamical mechanisms

Per `feedback_run_counterfactual_before_compute.md`, five candidate
dynamical mechanisms were enumerated and scored before this lane was
pursued:

| Route | Description | Tract. | Cohere. | Risk | Total |
|---|---|---|---|---|---|
| (a) 1-loop CW gauge boson | already ruled out (gives 0 for color singlet) | M | L | H | 4/12 |
| (b) Symmetry-pattern selection | naming, not mechanism | L | L | H | 3/12 |
| (c) Adjoint Fierz channel projection | uses cited Fierz primitive | H | H | M | 11/12 |
| (d) Per-color-row identification | subsumed by (c) | H | M | M | 7/12 |
| (e) Higgs-analog all-channel sum | gives N_taste = 16, not 8/3 | M | L | H | 4/12 |

**Outcome:** Route (c) is the unique tractable framework-native
mechanism. It is pursued in this V1.

**Sanity ruleouts:**
- (a) is dead by the existing obstruction note (1-loop CW gives zero
  for color-singlet scalars).
- (b) re-labels the problem; still needs `8/3` from somewhere.
- (d) is the same identity as (c) read per-color-row; subsumed.
- (e) gives `N_taste = 16` directly via an all-channel coherent sum
  (the Higgs-analog reading), not `8/3`. The factor `8/3` is the
  channel-density per axis, not the all-channel count.

## 2. Theorem statement (bounded support)

**Theorem (DM-eta G1 dynamical residual via operator-trace, V1).**
On End(C^N_c) with the cited Fierz completeness from CL3_COLOR_AUTOMORPHISM,
the operator-trace projection of the bare Wilson taste-mass kernel
through the **adjoint Fierz channel** gives the per-color-row trace
density

```text
rho_{adj/c}  =  N_c * F_adj  =  N_c * (N_c^2 - 1) / N_c^2
             =  (N_c^2 - 1) / N_c
             =  8 / 3.
```

Composition with the cited bare Wilson mass for the dark `hw=3`
singlet (`m_S3_bare = 2 r * hw_dark = 6` in lattice units; cited Origin B
factorization) gives

```text
m_DM  =  rho_{adj/c} * 2 r * hw_dark * v
      =  (8/3) * 6 * v
      =  16 v
      =  N_sites * v          (on canonical-surface v).
```

**Status boundary:** the operator-trace ARITHMETIC is closed by this
note's runner (12 PASS, 0 FAIL). The dark-`hw=3`-mass-operator-projection
BRIDGE step -- that the projection actually goes through the adjoint
Fierz channel and not the singlet channel -- is the **residual of the
residual**, conditional on a separate projection-identification theorem.
Carrier-level necessary condition `dim(C^8) = dim(adj_3) = 8` holds
exactly; the operator-level bridge is open.

### Proof

**Step 1 (Fierz completeness on End(C^N_c)).** By CL3_COLOR_AUTOMORPHISM
Section D, the matrix algebra `End(C^N_c)` decomposes into singlet
(weight `1/N_c^2`) and adjoint (weight `(N_c^2-1)/N_c^2 = 8/9`)
Fierz channels. Numerical verification (Test 1 in the runner):
the projectors `P_singlet`, `P_adj` on End(C^3) satisfy
`P_singlet + P_adj = I` to machine precision.

**Step 2 (Trace counts).** By construction, `Tr[P_singlet] = 1` (one
singlet basis vector) and `Tr[P_adj] = N_c^2 - 1 = 8` (`N_c^2-1`
adjoint basis vectors). Verified at machine precision (Test 2).

**Step 3 (Per-color-row trace density).** The adjoint trace density
per color row is `2 * sum_a Tr[T^a T^a] / N_c = (N_c^2 - 1)/N_c`.
By Gell-Mann normalization (cited), `Tr[T^a T^a] = 1/2` per generator,
so `sum_a Tr[T^a T^a] = (N_c^2 - 1)/2` and the per-color-row density
is `(N_c^2 - 1)/N_c = 8/3`. Verified to `1e-12` (Test 3).

**Step 4 (Wilson hop count on chiral cube).** By CL3_TASTE_GENERATION,
the chiral cube `C^8 = (C^2)^otimes 3` has 8 states indexed by Hamming
weight. The dark `hw=3` singlet `|111>` has Hamming distance 3 from the
vacuum `|000>`, so the bare Wilson mass is `2 r * hw_dark = 6` in
lattice units (Test 4).

**Step 5 (operator-trace closure on the canonical surface).** Composing
Steps 3 and 4 with the canonical-surface `v`:

```text
m_DM  =  (Wilson hop count) * (adjoint trace density per color) * v
      =  6 * (8/3) * v
      =  16 v
      =  N_sites * v        (since N_sites = 2^d for d = 4).
```

Verified at relative deviation `< 1e-12` (Tests 5, 7, 9).

**Step 6 (Wrong-channel sanity).** Six wrong-channel candidates are
explicitly checked NOT to give 8/3 (Test 8):

```text
F_singlet     = 1/9    !=  8/3
no enhancement = 1     !=  8/3
1/N_c        = 1/3     !=  8/3
C_F          = 4/3     !=  8/3
C_A          = 3       !=  8/3
C_A/C_F      = 9/4     !=  8/3
```

This rules out: (i) the singlet Fierz channel as the wrong projector,
(ii) no-enhancement (bare Wilson mass without color trace), (iii) singlet
dilution, (iv) C_F Casimir self-energy, (v) C_A adjoint Casimir
absolute, and (vi) C_A/C_F Casimir ratio. Only the adjoint Fierz
density per color gives 8/3.

**Step 7 (Carrier-level necessary condition).** The carrier-level
identity `dim(C^8) = dim(adj_3) = 8` holds exactly (Test 10). This is
a NECESSARY condition for the bridge step -- the dark hw=3 chiral
mode's space matches in dimension the adjoint sector of End(C^3).
The bridge step that this dimensional match is dynamically realized
by the projection of the Wilson mass operator through the adjoint
Fierz channel -- and not the singlet -- is the residual of the
residual.

**QED on the operator-trace ARITHMETIC**; the operator-level bridge
identification remains open.

## 3. Claim Boundary

This bounded support theorem derives `rho_{adj/c} = 8/3` from the
operator-trace projection through the adjoint Fierz channel on
`End(C^N_c)`, conditional on the named open bridge step that the dark
`hw=3` Wilson mass operator on the SU(3)-gauged chiral cube projects
through the adjoint Fierz channel and not the singlet channel.
Composition with the cited bare Wilson mass gives `m_DM = 16 v` on the
canonical surface. Six wrong-channel candidates are explicitly ruled out
by the runner.

## 4. What is closed, bounded, and open

### Closed by V1 (operator-trace arithmetic)

1. **Operator-trace projection arithmetic** through the adjoint Fierz
   channel on End(C^N_c) gives `rho_{adj/c} = N_c * F_adj = 8/3`
   exactly.
2. **Six wrong-channel candidates** explicitly ruled out: singlet
   Fierz channel, no enhancement, singlet dilution, C_F, C_A,
   C_A/C_F.
3. **Composition** with the cited bare Wilson mass gives `m_DM = 16 v`
   exactly on the canonical surface.
4. **Counterfactual Pass winner**: route (c) [adjoint Fierz channel
   projection] is the unique tractable mechanism within the cited
   primitive set. (a) ruled out, (b) is naming, (d) subsumed by (c),
   (e) gives wrong factor.
5. **Carrier-level necessary condition**: `dim(C^8) = dim(adj_3) = 8`
   holds exactly.

### Single open ingredient carried forward (residual of the residual)

1. **Operator-level adjoint-channel bridge step** -- the projection-
   identification theorem stating that the dark hw=3 mass operator on
   the SU(3)-gauged chiral cube projects through the adjoint Fierz
   channel of End(C^N_c) and not the singlet channel. The carrier-
   level necessary condition holds; the operator-level identification
   is open. A natural avenue:
   (i) explicit construction of the projector `P_dark_hw3` on the
       SU(3)-gauged minimal block, computing
       `Tr_color[P_dark_hw3 * P_adj] / Tr_color[P_dark_hw3 * P_singlet]`
       and verifying the ratio is 8 = dim(adj_3);
   (ii) an independently ratified framework convention identifying the
       dark hw=3 collective-mode mass with the adjoint trace density,
       paralleling the Higgs `m_H = v/(2u_0)` convention.

### Inherited bounded inputs (NOT closed by V1)

1. **A0 hierarchy compression** -- inherited assumption from the parent
   bounded theorem.
2. **Sommerfeld band** `S_vis/S_dark in [1.4, 1.7]` -- inherited bounded.
3. **Freeze-out coefficient** `x_F in [22, 28]` -- inherited bounded.
4. **alpha_X = alpha_LM** -- inherited bounded candidate-route choice.
5. **Algebraic step** -- closed at V1 of the algebraic note; inherited
   here.

## 5. What this theorem does NOT claim

- That the DM-eta G1 closure is now retained. This is bounded support
  on the dynamical step, conditional on the open bridge.
- That the bridge step is closed. The carrier-level necessary
  condition holds; the operator-level identification is open.
- That a new axiom is introduced. The note uses cited authorities:
  Fierz completeness (CL3_COLOR_AUTOMORPHISM section D), chiral cube
  (CL3_TASTE_GENERATION), bare Wilson mass identity (DM_ETA_FREEZEOUT_BYPASS
  Origin B), and standard Lie-algebra Casimir values (SU3_ADJOINT_CASIMIR).
  No new dynamical mechanism is admitted.
- That the parent DM-eta freeze-out-bypass status changes. The lane
  remains bounded-with-open-G1; this V1 sharpens the open lane to
  "operator-trace arithmetic closed; operator-level bridge open".

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_eta_g1_dynamical_residual_2026_05_06.py
```

Expected: `PASS = 12, FAIL = 0`.

**Object-level matrix tests run:**

1. Fierz completeness `P_singlet + P_adj = I` on End(C^3) (max err < 1e-12).
2. Trace counts `Tr[P_singlet] = 1, Tr[P_adj] = 8` (exact).
3. Per-color-row adjoint trace density `(N_c^2-1)/N_c = 8/3` (exact).
4. Bare Wilson mass on `|111>` is `2 r * hw_dark = 6` (exact).
5. `rho_{adj/c} = N_c * F_adj = 8/3` at the Fraction level (exact).
6. Singlet:adjoint ratio is `1 : 8 = dim(adj)` (exact).
7. Operator-trace closure: `6 * 8/3 = 16 = N_sites` (exact).
8. Six wrong-channel candidates all distinct from 8/3 (exact ruleouts).
9. Composition `m_DM = 16 v` on canonical-surface v (rel dev = 0).
10. Carrier-level bridge: `dim(C^8) = dim(adj_3) = 8` (exact).
11. Counterfactual Pass scoring (informational, route c wins).
12. Status firewall sanity (parent status unchanged).

## 7. Honest residual

- **Operator-level adjoint-channel bridge step**: open. The carrier-
  level necessary condition holds; the projection-identification
  theorem on the SU(3)-gauged chiral cube is open. This is the
  residual of the residual.
- **Sommerfeld + freeze-out band**: inherited bounded; not a single-
  point prediction.
- **alpha_X = alpha_LM**: inherited bounded candidate-route choice.
- **A0 hierarchy compression**: inherited assumption.
- **Numerical consequence on inherited inputs**: `m_DM = 3.94 TeV`
  (`m_DM = 16 v`) is unchanged from the parent bounded theorem.

## 8. Position on the publication surface

This V1 bounded support theorem sharpens the DM-eta G1 lane:

- **The G1 algebraic step is closed** at V1 of the algebraic note.
- **The G1 dynamical step's operator-trace ARITHMETIC** is now closed
  by this V1: the cleanest framework-native mechanism (operator-trace
  through the adjoint Fierz channel) reproduces the 8/3 factor exactly
  at the matrix-element level. Six wrong-channel candidates are
  explicitly ruled out.
- **The G1 dynamical step's operator-level BRIDGE** -- whether the
  dark hw=3 mass operator actually projects through the adjoint Fierz
  channel rather than the singlet channel -- remains the named open
  residual of the residual.
- **The G1 lane** is now reduced from "derive 8/3 dynamically" to
  "verify the operator-level adjoint-channel bridge".

The flagship paper line should remain `eta` IMPORTED with this theorem
listed, at most, as bounded support for the DM-eta G1 dynamical step.
The bridge identification step is the remaining open residual, and the
parent DM-eta freeze-out-bypass lane status remains unchanged.

## 9. Cross-references

- DM-eta G1 algebraic support (companion V1, the first stage):
  [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
- DM-eta freezeout-bypass quantitative theorem (parent bounded theorem):
  [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- DM-eta N_sites · v structural support:
  [`DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md`](DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md)
- DM SU(3) gauge-loop obstruction (the prior ruleout naming R3):
  [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
- Cl(3) color automorphism (Fierz primitive):
  [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- SU(3) adjoint Casimir = 3 (companion):
  [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
- Cl(3) taste generation (chiral cube structure):
  [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
- Higgs mass from axiom (analog mass-operator pattern):
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)

## 10. Hypothesis set used (formal)

```yaml
claim_type: bounded_theorem
claim_scope: |
  Operator-trace projection mechanism for the DM-eta G1 dynamical
  residual: rho_{adj/c} = 8/3 emerges as the per-color-row adjoint
  Fierz channel trace density on End(C^N_c). Conditional on the
  named open bridge step that the dark hw=3 Wilson mass operator
  on the SU(3)-gauged chiral cube projects through the adjoint
  Fierz channel and not the singlet channel. Composition with the
  cited bare Wilson mass gives m_DM = 16 v on the canonical surface.
  Six wrong-channel candidates explicitly ruled out.
upstream_dependencies:
  - dm_eta_g1_cl3_adj3_embedding_algebraic_support_theorem
  - dm_eta_freezeout_bypass_quantitative_theorem
  - dm_su3_gauge_loop_obstruction_note
  - cl3_color_automorphism_theorem
  - cl3_taste_generation_theorem
  - su3_adjoint_casimir_theorem
admitted_context_inputs:
  - SU(N) Fierz identity (already in CL3_COLOR_AUTOMORPHISM)
  - Standard Lie-algebra Casimir values (already in SU3_ADJOINT_CASIMIR)
  - Standard Wilson lattice action (cited in DM_ETA_FREEZEOUT_BYPASS)
no_new_axioms: true
no_new_combinatorial_inputs: true
no_new_dynamical_mechanisms: true
counterfactual_pass_done: true
runner_passes: 12
runner_fails: 0
```

---

## Reading rule

This note is the claim boundary for the operator-trace mechanism on the
G1 dynamical step. It sharpens the DM-eta G1 lane on current `main` from
"algebraic 8/3 derived, dynamical step open" to "algebraic 8/3 derived,
dynamical operator-trace arithmetic closed, operator-level adjoint-
channel bridge open". Any downstream parent-status change requires a
separate source derivation (closing the bridge step) and independent
audit of the full dependency chain.
