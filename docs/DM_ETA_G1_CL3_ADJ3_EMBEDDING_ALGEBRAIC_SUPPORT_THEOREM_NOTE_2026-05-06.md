# DM-eta G1 Cl(3)/SU(3) Embedding Algebraic Support Theorem (V1)

**Date:** 2026-05-06
**Status:** bounded support theorem on the algebraic `8/3` identity.
This note derives the numerical factor `8/3 = dim(adj_3)/N_c` used in
the DM-eta G1 closure target from cited Cl(3)/SU(3) embedding
authorities. Two equivalent route-(a) and route-(e) readings agree
exactly. The dynamical step that would install this density factor as
the Wilson-bare-mass multiplier for the dark `hw=3` singlet remains
open; this note does not change the DM-eta lane's ledger status.

**Type:** bounded_theorem

**Primary runner:** [`scripts/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.py`](../scripts/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.py)
**Runner result:** `PASS = 12, FAIL = 0`.
**Output log:** [`outputs/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.txt`](../outputs/frontier_dm_eta_g1_cl3_adj3_embedding_2026_05_06.txt)

Audit authority belongs to the independent audit lane. The row should
remain `unaudited` after landing until a fresh audit checks the bounded
algebraic scope and its dependency chain.

## Cited authorities

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
  prior candidate `m_DM = N_sites · v = 16 v`, Origin B factorization
  `16 = (8/3) · 6`.
- [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
  — explicit obstruction note ruling out the perturbative one-loop CW
  route and naming R3 (Cl(3)/SU(3) embedding) as the most promising
  alternative.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — source note for `N_sites = 2^d = 16` on the minimal APBC block on
  Z^4.

## 0. Headline

The DM-eta G1 lane required deriving the numerical factor `8/3` that
bridges the chiral Wilson bare mass `6 v` to the prior
candidate `m_DM = 16 v = N_sites · v`. The previously published
obstruction note ruled out the perturbative one-loop Coleman-Weinberg
route and explicitly recommended Route R3 (Cl(3)/SU(3) embedding
identity) as the structurally most promising path.

This note delivers the R3 algebraic step. The factor 8/3 is the
**adjoint-density per color slot** of the framework's cited
Cl(3) → SU(3) embedding, derivable in two equivalent ways from
cited primitives:

```
ρ_{adj/c} := dim(adj_3) / N_c = (N_c² − 1) / N_c = 8/3.
```

Reading (a) — **carrier-dimension ratio**: `dim(C^8) / dim(C^3) = 8/3`,
where C^8 is the Cl(3) chiral cube (= dim(adj_3)) and C^3 is the SU(3)
fundamental.

Reading (e) — **Fierz adjoint density per color**: `N_c · F_adj =
N_c · (N_c² − 1)/N_c² = 8/3`, multiplying the cited Fierz channel
fraction by N_c.

Both readings use only the cited CL3_COLOR_AUTOMORPHISM primitives.
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

**Theorem (DM-eta G1 Cl(3)/SU(3) embedding algebraic support, V1).**
On the A_min surface with cited Cl(3)/SU(3) embedding primitives
(CL3_COLOR_AUTOMORPHISM, SU3_ADJOINT_CASIMIR, CL3_TASTE_GENERATION),
the DM-eta G1 numerical factor is

```
ρ_{adj/c}  =  dim(adj_3) / N_c  =  (N_c² − 1) / N_c  =  8/3,
```

derived two equivalent ways from the cited one-hop authorities:

(R-a) **Carrier-dimension ratio.** The Cl(3) chiral taste cube has
dimension `dim(C^8) = 2³ = 8`; the SU(3)_c fundamental has dimension
`N_c = 3`. The ratio `dim(C^8) / N_c = 8/3` is the adjoint-rep
multiplicity per color slot.

(R-e) **Fierz adjoint density per color.** The cited Fierz channel
fraction `F_adj = (N_c² − 1) / N_c² = 8/9` (cited from
CL3_COLOR_AUTOMORPHISM, Section D), multiplied by the color count
N_c = 3, gives `N_c · F_adj = 8/3` — the adjoint-density of End(C^N_c)
viewed per color row.

(R-eq) **Equivalence.** R-a and R-e both equal `Fraction(8, 3)` exactly;
their equality is the algebraic identity `dim(adj_3) = N_c · (N_c · F_adj) =
N_c² · F_adj = N_c² − 1`.

(R-c) **Closure with the freezeout-bypass identity.** Composing with
the cited Origin-B factorization
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
flagged Origin A ↔ Origin B comparison now reduce to the same algebraic
identity dim(adj_3)/N_c = 8/3.

**Status boundary:** the algebraic identity is checked as a bounded
support theorem using cited Fierz and chiral-cube authorities without
admitting new axioms. The dynamical step (why `ρ_{adj/c}` is the
natural multiplier of the Wilson-bare mass for the dark `hw=3`
singlet, rather than e.g. the Casimir ratio `9/4` or some other ratio)
is not closed here.

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
(cited from SU3_ADJOINT_CASIMIR § A7), so `2·C_F = (N_c² − 1)/N_c =
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
as the bare-Wilson-mass multiplier of the dark singlet remains open.

## 3. Audit boundary fields

```yaml
claim_type_author_hint: bounded_theorem
audit_status_authority: independent audit lane only
effective_status_authority: pipeline-derived after independent audit
claim_scope: |
  Bounded algebraic support theorem deriving
  ρ_{adj/c} = dim(adj_3)/N_c = 8/3 from cited Cl(3)/SU(3) embedding
  authorities, with two equivalent readings: carrier-dimension ratio
  and Fierz adjoint density per color. Composition with the bounded
  freezeout-bypass identity gives m_DM = (8/3) · 6 v = 16 v exactly
  conditional on the inherited canonical v and Wilson-mass inputs.
  The dynamical coupling step that selects ρ_{adj/c} as the dark
  Wilson-bare-mass multiplier is not closed by this note.
g1_dynamical_coupling_step_status: open
g1_algebraic_step_status: closed_v1
counterfactual_pass_done: true
counterfactual_pass_routes_scored: 5
counterfactual_pass_winner: route_e_with_route_a_dual
runner_pass_count: 12
runner_fail_count: 0
```

## 4. What is closed, bounded, and open

### Closed by V1

1. **Algebraic derivation of 8/3** from cited primitives via two
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
   step remains open. Two natural avenues for
   the downstream dynamical bridge:
   (i) Explicit evaluation of the dark-singlet mass operator on the
       chiral cube with adjoint-projected SU(3) gauge insertion
       (paralleling the Higgs `m_H = v/(2 u_0)` derivation but with
       all-channel adjoint summation).
      (ii) an independently ratified framework convention identifying the
       algebraic density itself as the collective-mode mass formula.

### Inherited bounded inputs (NOT closed by V1)

1. **A0 hierarchy compression** — inherited assumption from the source
   theorem; V1 does not elevate or close it.
2. **Sommerfeld band** S_vis/S_dark ∈ [1.4, 1.7] — inherited bounded.
3. **Freeze-out coefficient** x_F ∈ [22, 28] — inherited bounded.
4. **alpha_X = alpha_LM** — inherited bounded candidate-route choice.

## 5. What this theorem does NOT claim

- That the DM-eta G1 closure is retained. This note is bounded
  algebraic support and remains subject to independent audit.
- That the dynamical step is closed. V1 closes only the algebraic
  derivation of 8/3; the dynamical mechanism that selects ρ_{adj/c}
  as the Wilson-bare-mass multiplier remains open.
- That a new axiom is introduced. The algebra uses cited authorities:
  `dim(adj_3) = 8` (CL3_COLOR_AUTOMORPHISM), Fierz `F_adj = 8/9`
  (CL3_COLOR_AUTOMORPHISM § D), chiral cube `C^8 = (C^2)^⊗3`
  (CL3_TASTE_GENERATION), Origin B factorization
  (DM_ETA_FREEZEOUT_BYPASS § Origin B), inherited canonical `v`
  (OBSERVABLE_PRINCIPLE_FROM_AXIOM), and `N_sites = 16`
  (HIGGS_MASS_FROM_AXIOM). Their audit statuses and dependency closure
  are controlled by the audit ledger, not by this note.

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

- **G1 dynamical-coupling step:** open. The
  algebraic identity is closed; the dynamical-mechanism residual is
  whether ρ_{adj/c} = dim(adj_3)/N_c is the natural Wilson-bare-mass
  multiplier for the dark hw=3 singlet. A later closure needs either
  an explicit Coleman-Weinberg-on-chiral-cube derivation or an
  independently ratified framework convention identifying the
  algebraic density as the collective-mode mass formula.
- **Sommerfeld + freeze-out bounded band**: not a single-point
  prediction; inherited from the source theorem.
- **alpha_X = alpha_LM**: inherited bounded candidate-route choice
  (DM_ETA_FREEZEOUT_BYPASS § G3).
- **A0 hierarchy compression**: inherited assumption from the source
  theorem; V1 does not lift A0.
- **Numerical consequence on inherited inputs**: `m_DM = 3.94 TeV`
  (`m_DM = (8/3) · 6 v = 16 v`) is unchanged from the source theorem
  and remains conditional on the inherited canonical `v`,
  Wilson-mass, and DM-eta setup.

## 8. Position on the publication surface

This V1 bounded support theorem sharpens the DM-eta G1 lane:

- **The previously open numerical-factor-8/3 algebraic residual is now
  closed** at the algebraic level using cited Cl(3)/SU(3) embedding
  authorities.
- **The previously flagged Origin A / Origin B duality** (DM_ETA_FREEZEOUT_BYPASS
  § F1 reviewer-honesty caveat) is anchored at the integer level:
  both reduce to `dim(adj_3) · 2 · hw_dark / N_c = 16`, with
  `dim(adj_3)/N_c = 8/3` the bridging identity.
- **The previously ruled-out perturbative route** (DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25)
  is bypassed: the closure is structural, not perturbative.
- **The G1 lane** is now reduced from "derive 8/3 from somewhere" to
  the open bridge: "derive the dynamical-coupling step that installs
  ρ_{adj/c} as the Wilson-bare-mass multiplier".

The flagship paper line should remain `eta` imported with this theorem
listed, at most, as bounded algebraic support for the DM-eta G1 support
package. The dynamical-coupling step remains an open bridge until an
explicit derivation or independently ratified convention exists.

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
- Observable principle from axiom (EW v source):
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

## 10. Hypothesis set used (formal)

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: |
  Algebraic derivation of the DM-eta G1 numerical factor 8/3 =
  dim(adj_3)/N_c via the cited Cl(3)/SU(3) embedding identity,
  with two equivalent readings (R-a carrier-dimension ratio and R-e
  Fierz adjoint density per color) anchored on cited authorities.
  Composition with the bounded freezeout-bypass theorem gives
  m_DM = (8/3) · 6 v = 16 v = N_sites · v exactly. Dynamical-coupling
  step remains open.
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

This note is the claim boundary for the Cl(3)/SU(3) algebraic embedding
step of the DM-eta G1 closure. It sharpens the DM-eta lane on current
`main` from "8/3 needs derivation" to "algebraic 8/3 derived,
dynamical-coupling step remains open". Any downstream parent-status
change requires a separate source derivation and independent audit of
the full dependency chain.
