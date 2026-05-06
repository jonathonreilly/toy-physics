# DM-eta G1 Cl(3)/SU(3) Embedding Promotion Theorem (V1)

**Date:** 2026-05-06
**Status (actual current surface):** `bounded_retained` algebraic
promotion theorem — derives the previously open numerical factor
`8/3 = dim(adj_3)/N_c` of the DM-eta G1 closure target from cited
retained Cl(3)/SU(3) embedding primitives. Two equivalent route-(a)
and route-(e) readings agree exactly. The DYNAMICAL step that installs
this density factor as the Wilson-bare-mass multiplier for the dark
hw=3 singlet remains the audit-ratifiable residual; the algebraic
identity is closed.

**Type:** algebraic promotion theorem (companion to the previously
bounded G1 lane), audit-ratifiable as `proposed_retained` after
independent review of the dynamical-coupling residual.

**Primary runner:** `scripts/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.py`
**Runner result:** `PASS = 12, FAIL = 0`.
**Output log:** `outputs/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.txt`

**Branch:** `claude/dm-eta-g1-cl3-adj3-embedding-2026-05-06`

## Cited authorities (one-hop, retained on framework surface)

- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — supplies SU(3)_c on the 3D symmetric base via Gell-Mann embedding,
  Tr[T^a T^b] = (1/2) δ^{ab}, dim(adj_3) = N_c² − 1 = 8, and the Fierz
  channel fraction F_adj = (N_c² − 1)/N_c² = 8/9.
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
  — adjoint Casimir C_2(adj) = N = 3 with Tr[T^a_adj T^b_adj] = N δ^{ab}.
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
  — staggered taste cube C^8 = (C^2)^⊗3 with Burnside Hamming-weight
  decomposition 1+3+3+1 = 8.
- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  — bounded DM-eta freezeout-bypass identity `eta = C · m_DM²`,
  audit-discovered candidate `m_DM = N_sites · v = 16 v`, Origin B
  factorization `16 = (8/3) · 6`.
- [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
  — explicit obstruction note ruling out the perturbative one-loop CW
  route and naming R3 (Cl(3)/SU(3) embedding) as the most promising
  alternative.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — retained `N_sites = 2^d = 16` on the minimal APBC block on Z^4.

## 0. Headline

The DM-eta G1 lane required deriving the numerical factor `8/3` that
bridges the chiral Wilson bare mass `6 v` to the audit-discovered
candidate `m_DM = 16 v = N_sites · v`. The previously published
obstruction note ruled out the perturbative one-loop Coleman-Weinberg
route and explicitly recommended Route R3 (Cl(3)/SU(3) embedding
identity) as the structurally most promising path.

This note delivers the R3 algebraic step. The factor 8/3 is the
**adjoint-density per color slot** of the framework's retained
Cl(3) → SU(3) embedding, derivable in two equivalent ways from
already-retained primitives:

```
ρ_{adj/c} := dim(adj_3) / N_c = (N_c² − 1) / N_c = 8/3.
```

Reading (a) — **carrier-dimension ratio**: `dim(C^8) / dim(C^3) = 8/3`,
where C^8 is the Cl(3) chiral cube (= dim(adj_3)) and C^3 is the SU(3)
fundamental.

Reading (e) — **Fierz adjoint density per color**: `N_c · F_adj =
N_c · (N_c² − 1)/N_c² = 8/3`, multiplying the retained Fierz channel
fraction by N_c.

Both readings use only retained CL3_COLOR_AUTOMORPHISM primitives.
Their equality is an exact identity at the `Fraction(8,3)` level.

## 1. Counterfactual Pass

Per the framework's `feedback_run_counterfactual_before_compute.md`
discipline, ≥4 candidate structural-identity routes were enumerated
and scored before this lane was pursued:

| Route | Inputs | Tract. | Cohere. | Risk | Total |
|---|---|---|---|---|---|
| (a) Cl(3) C^8 / N_c carrier ratio | H | H | H | M | 11/12 |
| (b) Cl(4)/Cl(3,1) pseudoscalar embedding | M | M | L | H | 5/12 |
| (c) Color-automorphism Z_3 trace ratio | H | H | H | H | 8/12 |
| (d) Casimir ratio C_A/C_F = 9/4 | H | H | M | H | 7/12 |
| (e) Fierz adjoint-per-color (N_c · F_adj) | H | H | H | L | 12/12 |

**Outcome:** routes (a) and (e) are coupled (both use the chiral cube
C^8 and the SU(3) Fierz embedding) and unanimously score highest. Both
are pursued together as dual readings of one identity. Routes (b)–(d)
are explicitly ruled out: (b) gives factor-of-2 dimensional ratios on
Cl(4), not 8/3; (c) gives Z_3 trace ratios that do not yield 8/3; (d)
gives the Casimir ratio 9/4, distinct from 8/3 (Test 9 in the runner
verifies 8/3 ≠ 9/4 explicitly).

## 2. Theorem statement

**Theorem (DM-eta G1 Cl(3)/SU(3) embedding promotion, V1).**
On the A_min surface with retained Cl(3)/SU(3) embedding primitives
(CL3_COLOR_AUTOMORPHISM, SU3_ADJOINT_CASIMIR, CL3_TASTE_GENERATION),
the DM-eta G1 numerical factor is

```
ρ_{adj/c}  =  dim(adj_3) / N_c  =  (N_c² − 1) / N_c  =  8/3,
```

derived two equivalent ways from one-hop retained authorities:

(R-a) **Carrier-dimension ratio.** The Cl(3) chiral taste cube has
dimension `dim(C^8) = 2³ = 8`; the SU(3)_c fundamental has dimension
`N_c = 3`. The ratio `dim(C^8) / N_c = 8/3` is the adjoint-rep
multiplicity per color slot.

(R-e) **Fierz adjoint density per color.** The retained Fierz channel
fraction `F_adj = (N_c² − 1) / N_c² = 8/9` (cited from
CL3_COLOR_AUTOMORPHISM, Section D), multiplied by the color count
N_c = 3, gives `N_c · F_adj = 8/3` — the adjoint-density of End(C^N_c)
viewed per color row.

(R-eq) **Equivalence.** R-a and R-e both equal `Fraction(8, 3)` exactly;
their equality is the algebraic identity `dim(adj_3) = N_c · (N_c · F_adj) =
N_c² · F_adj = N_c² − 1`.

(R-c) **Closure with the freezeout-bypass identity.** Composing with
the retained Origin-B factorization
[`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`,
§ Origin B]:

```
m_DM  =  ρ_{adj/c} · (2 r · hw_dark · v)
      =  (8/3) · 6 v
      =  16 v
      =  N_sites · v.
```

The integer match `dim(adj_3) · 2 · hw_dark / N_c = 8 · 6 / 3 = 16` is
exact (Test 7 in the runner). This anchors Origin A (spacetime APBC
count `2^d = 16`) to Origin B (Cl(3) chiral cube · SU(3) Casimir
factorization) at the integer level: both sides of the previously
flagged Origin A ↔ Origin B comparison now reduce to the same retained
identity dim(adj_3)/N_c = 8/3.

**Status:** `bounded_retained` — the algebraic identity is closed using
retained Fierz + chiral cube primitives without admitting new axioms.
The dynamical step (why `ρ_{adj/c}` is the natural multiplier of
the Wilson-bare mass for the dark hw=3 singlet, rather than e.g.
the Casimir ratio 9/4 or some other ratio) is the audit-ratifiable
residual; on independent ratification of the dynamical-coupling
identification, the route is `proposed_retained`.

### Proof

**Step 1 (cite N_c, dim(adj_3), Gell-Mann normalization).** By
CL3_COLOR_AUTOMORPHISM (Sections A–B): the Z³ spatial substrate forces
`N_c = 3`; SU(3)_c acts on the 3D symmetric base via Gell-Mann
generators T^a = λ^a/2 with `Tr[T^a T^b] = (1/2) δ^{ab}`; the adjoint
has `dim(adj_3) = N_c² − 1 = 8`.

**Step 2 (cite the Fierz identity).** By CL3_COLOR_AUTOMORPHISM
(Section D, Fierz completeness):

```
Σ_a (T^a)_{ij} (T^a)_{kl} = (1/2) δ_{il} δ_{kj} − (1/(2 N_c)) δ_{ij} δ_{kl},
F_adj  =  (N_c² − 1) / N_c²  =  8/9.
```

**Step 3 (Cl(3) chiral cube).** By CL3_TASTE_GENERATION (Section A):
the Z³ staggered-fermion doubling produces the chiral taste cube
`C^8 = (C^2)^⊗3` with Burnside Hamming-weight decomposition
`1 + 3 + 3 + 1 = 8`.

**Step 4 (Reading R-a, carrier-dimension ratio).** Both `C^8` (chiral
cube) and `adj_3` (SU(3) adjoint) have dimension 8. Their ratio with
the SU(3) fundamental dimension N_c = 3 is

```
ρ_{adj/c}  :=  dim(adj_3) / N_c  =  dim(C^8) / N_c  =  8 / 3.
```

This is the carrier-level adjoint-density-per-color of the embedding.

**Step 5 (Reading R-e, Fierz density per color).** Multiply the cited
Fierz channel fraction F_adj = 8/9 by N_c = 3:

```
N_c · F_adj  =  3 · (8/9)  =  8/3.
```

This is the Fierz-completeness-derived adjoint trace per color slot
of `End(C^N_c)`.

**Step 6 (Equivalence).** Steps 4 and 5 give equal numbers because
`dim(adj_3) = N_c² · F_adj = N_c² · (N_c² − 1)/N_c² = N_c² − 1`. So
the two derivations are not independent in content — they are dual
readings of the single identity `dim(adj) = N_c² − 1`.

**Step 7 (Identity equivalent to 2·C_F).** Note `C_F = (N_c² − 1)/(2 N_c)`
(retained, see SU3_ADJOINT_CASIMIR § A7), so `2·C_F = (N_c² − 1)/N_c =
ρ_{adj/c} = 8/3` for N_c = 3. The runner Test 10 verifies this third
algebraic equivalent reading.

**Step 8 (Composition with Origin B).** Substitute ρ_{adj/c} = 8/3 into
the Origin B factorization
(DM_ETA_FREEZEOUT_BYPASS, § Origin B, eq. `m_DM = (dim(adj_3)/N_c) · 2 · hw_dark · v`):

```
m_DM  =  (8/3) · 2 · 3 · v  =  (8/3) · 6 v  =  16 v.
```

Equivalently, `dim(adj_3) · 2 · hw_dark / N_c = 8 · 6 / 3 = 16 = N_sites`.
This integer identity anchors Origin A (spacetime, 2^d = 16) to Origin
B (chiral cube · adjoint density) at the integer level.

**QED on the algebraic step**; the dynamical step that selects ρ_{adj/c}
as the bare-Wilson-mass multiplier of the dark singlet is the audit
residual.

## 3. Status firewall fields

```yaml
actual_current_surface_status: bounded_retained
conditional_surface_status: proposed_retained
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  V1 lands the algebraic step of the DM-eta G1 closure: derives
  ρ_{adj/c} = dim(adj_3)/N_c = 8/3 from retained Cl(3)/SU(3) embedding
  primitives (CL3_COLOR_AUTOMORPHISM Fierz identity + dim(adj_3) = 8;
  CL3_TASTE_GENERATION chiral cube C^8). Two equivalent readings (a)
  carrier-dimension ratio and (e) Fierz density per color agree
  exactly at Fraction(8,3). The closure m_DM = (8/3) · 6 v = 16 v
  = N_sites · v is integer-exact and reproduces the previously
  audit-discovered candidate from the bounded freezeout-bypass theorem
  on retained framework primitives — no new axiom, no new combinatorial
  input, no new dynamical mechanism imported. The dynamical step
  (why ρ_{adj/c} multiplies the Wilson-bare mass for the dark
  hw=3 singlet) is the audit-ratifiable residual; on ratification
  the route promotes to proposed_retained.
audit_required_before_effective_retained: true
bare_retained_allowed: false
g1_dynamical_coupling_step_status: open_audit_ratifiable
g1_algebraic_step_status: closed_v1
counterfactual_pass_done: true
counterfactual_pass_routes_scored: 5
counterfactual_pass_winner: route_e_with_route_a_dual
runner_pass_count: 12
runner_fail_count: 0
m_dm_falsifiable_prediction: "3.94 TeV (m_DM = 16 v = (8/3) · 6 v)"
```

## 4. What is closed, bounded, and open

### Closed by V1

1. **Algebraic derivation of 8/3** from retained primitives via two
   equivalent readings (carrier-dim ratio and Fierz density per color).
2. **Integer match** `dim(adj_3) · 2 · hw_dark / N_c = 16 = N_sites`,
   anchoring Origin A ↔ Origin B equivalence at the integer level.
3. **Composition** with the freezeout-bypass identity gives `m_DM =
   (8/3) · 6 v = 16 v = N_sites · v` exactly on the canonical surface.
4. **Sanity ruleouts**: the Casimir ratio 9/4 (route d) is distinct
   from 8/3 (Test 9); the perturbative one-loop CW route (the
   previously ruled-out route) is not used.
5. **Burnside-decomposition consistency**: hw=0+hw=1+hw=2+hw=3 =
   1+3+3+1 = 8 = dim(adj_3) = dim(C^8), tying the chiral cube to the
   adjoint at the carrier level.

### Single open ingredient carried forward

1. **G1 dynamical-coupling step** — *why* ρ_{adj/c} = dim(adj_3)/N_c
   is the natural multiplier of the Wilson-bare mass for the dark
   hw=3 singlet. The algebraic identity is closed; the dynamical
   step is the audit-ratifiable residual. Two natural avenues for
   the dynamical promotion:
   (i) Explicit evaluation of the dark-singlet mass operator on the
       chiral cube with adjoint-projected SU(3) gauge insertion
       (paralleling the Higgs `m_H = v/(2 u_0)` derivation but with
       all-channel adjoint summation).
   (ii) Audit ratification: the algebraic identity itself is the
       collective-mode mass formula (the framework's convention
       choice), in which case the V1 result IS the closure and the
       residual is explicit reviewer ratification.

### Inherited bounded inputs (NOT closed by V1)

1. **A0 hierarchy compression** — inherited assumption from the source
   theorem; V1 does not elevate or close it.
2. **Sommerfeld band** S_vis/S_dark ∈ [1.4, 1.7] — inherited bounded.
3. **Freeze-out coefficient** x_F ∈ [22, 28] — inherited bounded.
4. **alpha_X = alpha_LM** — inherited bounded candidate-route choice.

## 5. What this theorem does NOT claim

- That the DM-eta G1 closure is now `retained` bare. The status is
  `bounded_retained` for the algebraic step, with audit ratification
  required to promote to `proposed_retained`.
- That the dynamical step is closed. V1 closes only the algebraic
  derivation of 8/3; the dynamical mechanism that selects ρ_{adj/c}
  as the Wilson-bare-mass multiplier remains open as the
  audit-ratifiable residual.
- That a new axiom is introduced. All ingredients are retained
  primitives: dim(adj_3) = 8 (CL3_COLOR_AUTOMORPHISM), Fierz F_adj =
  8/9 (CL3_COLOR_AUTOMORPHISM § D), chiral cube C^8 = (C^2)^⊗3
  (CL3_TASTE_GENERATION), Origin B factorization
  (DM_ETA_FREEZEOUT_BYPASS § Origin B), v retained
  (OBSERVABLE_PRINCIPLE_FROM_AXIOM), N_sites = 16 retained
  (HIGGS_MASS_FROM_AXIOM).

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.py
```

Expected: `PASS = 12, FAIL = 0`.

**Object-level matrix tests run:**

1. Gell-Mann normalization Tr[T^a T^b] = (1/2) δ^{ab} (max err < 1e-12).
2. Fierz identity at full 4-index resolution (max err < 1e-12).
3. F_adj = 8/9 at the Fraction level (exact).
4. C^8 dimension and 1+3+3+1 Burnside decomposition (exact).
5. Two equivalent readings of 8/3 (route-a carrier ratio, route-e
   Fierz density per color) agree at Fraction(8,3).
6. Closure identity (8/3) · 6 = 16 = N_sites (exact).
7. Origin A ↔ Origin B integer match (exact).
8. m_DM = (8/3) · 6 v = 16 v on the canonical-surface v (relative
   deviation = 0).
9. 8/3 ≠ Casimir ratio 9/4 (rules out route (d)).
10. Adjoint trace identity 2 · C_F = 8/3 (alternative reading).
11. Burnside hw-decomposition consistency (1+3+3+1 = 8).
12. Per-color adjoint density on End(C^N_c) = (N_c² − 1)/N_c = 8/3.

## 7. Honest residual

- **G1 dynamical-coupling step:** open as audit-ratifiable. The
  algebraic identity is closed; the dynamical-mechanism residual is
  whether ρ_{adj/c} = dim(adj_3)/N_c is the natural Wilson-bare-mass
  multiplier for the dark hw=3 singlet. Audit options: (i) explicit
  Coleman-Weinberg-on-chiral-cube derivation; (ii) framework-convention
  ratification of the algebraic identity itself as the collective-mode
  mass formula.
- **Sommerfeld + freeze-out bounded band**: not a single-point
  prediction; inherited from the source theorem.
- **alpha_X = alpha_LM**: inherited bounded candidate-route choice
  (DM_ETA_FREEZEOUT_BYPASS § G3).
- **A0 hierarchy compression**: inherited assumption from the source
  theorem; V1 does not lift A0.
- **Falsifiable prediction**: m_DM = 3.94 TeV (m_DM = (8/3) · 6 v
  = 16 v), unchanged from the source theorem; testable at LHC HL/HE
  upgrades with sufficient luminosity for WIMP-like DM searches.

## 8. Position on the publication surface

This V1 promotion theorem materially sharpens the DM-eta G1 lane:

- **The previously open numerical-factor-8/3 residual is now closed**
  at the algebraic level using only retained Cl(3)/SU(3) embedding
  primitives.
- **The previously flagged Origin A / Origin B duality** (DM_ETA_FREEZEOUT_BYPASS
  § F1 reviewer-honesty caveat) is anchored at the integer level:
  both reduce to `dim(adj_3) · 2 · hw_dark / N_c = 16`, with
  `dim(adj_3)/N_c = 8/3` the bridging identity.
- **The previously ruled-out perturbative route** (DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25)
  is bypassed: the closure is structural, not perturbative.
- **The G1 lane** is now reduced from "derive 8/3 from somewhere" to
  the explicit audit-ratifiable residual: "ratify or derive the
  dynamical-coupling step that installs ρ_{adj/c} as the
  Wilson-bare-mass multiplier".

The flagship paper line should remain `eta` IMPORTED with this
theorem listed as the **algebraic completion of the DM-eta G1
support package**, with the dynamical-coupling step flagged for audit
ratification. On audit ratification of the dynamical step (or
explicit Coleman-Weinberg derivation), the DM-eta lane promotes to
`proposed_retained`, closing the third publication gate at zero-import
grade.

## 9. Cross-references

- DM-eta freezeout-bypass quantitative theorem (source bounded theorem,
  Origin B factorization):
  [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- DM-eta N_sites · v structural support (V1 of the lift, framework-composed):
  [`DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md`](DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md)
- DM SU(3) gauge-loop obstruction (the prior ruleout naming R3 as the
  closure target):
  [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
- Cl(3) color automorphism (load-bearing one-hop authority):
  [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- SU(3) adjoint Casimir = 3 (companion):
  [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
- Cl(3) taste generation (chiral cube structure):
  [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
- Higgs mass from axiom (N_sites = 2^d = 16):
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
- Observable principle from axiom (retained EW v):
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

## 10. Hypothesis set used (formal)

```yaml
claim_type_author_hint: bounded_retained_promotion_theorem
claim_scope: |
  Algebraic derivation of the DM-eta G1 numerical factor 8/3 =
  dim(adj_3)/N_c via the retained Cl(3)/SU(3) embedding identity,
  with two equivalent readings (R-a carrier-dimension ratio and R-e
  Fierz adjoint density per color) anchored on cited authorities.
  Composition with the bounded freezeout-bypass theorem gives
  m_DM = (8/3) · 6 v = 16 v = N_sites · v exactly. Dynamical-coupling
  step is the audit-ratifiable residual.
upstream_dependencies:
  - cl3_color_automorphism_theorem
  - su3_adjoint_casimir_theorem
  - cl3_taste_generation_theorem
  - dm_eta_freezeout_bypass_quantitative_theorem
  - dm_su3_gauge_loop_obstruction_note
  - higgs_mass_from_axiom_note
  - observable_principle_from_axiom_note
admitted_context_inputs:
  - SU(N) Fierz identity (already in CL3_COLOR_AUTOMORPHISM)
  - Schur's lemma (mathematical, already in SU3_ADJOINT_CASIMIR)
  - Burnside lemma / character orthogonality (already in CL3_TASTE_GENERATION)
no_new_axioms: true
no_new_combinatorial_inputs: true
no_new_dynamical_mechanisms: true
counterfactual_pass_done: true
runner_passes: 12
runner_fails: 0
```

---

## Reading rule

This note is the claim boundary for the Cl(3)/SU(3) embedding step
of the DM-eta G1 closure. It sharpens the DM-eta lane on current
`main` from "8/3 needs derivation" to "algebraic 8/3 derived,
dynamical-coupling step is the audit residual". A successful audit
ratification of the dynamical-coupling step (or independent explicit
derivation) promotes the DM-eta lane to `proposed_retained` —
closing the third publication gate at zero-import grade.
