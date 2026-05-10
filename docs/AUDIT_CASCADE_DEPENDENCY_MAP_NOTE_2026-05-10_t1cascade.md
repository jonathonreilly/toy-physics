# Audit Cascade Dependency Map — Cross-Reference Note

**Date:** 2026-05-10
**Claim type:** cross_reference (NOT a synthesis claim, NOT a primitive,
NOT a retained-content modification, NOT a tier change for any item).
**Status authority:** independent audit lane only. This note documents
already-published cascade-relationships between source-notes; it does
not set, modify, or predict audit verdicts for any item it references.
**Source-note proposal disclaimer:** this is a cross-reference / dependency-map
note. It enumerates how four already-landed (or open) closure attempts
mechanically discharge downstream items via shared structural loads.
Every "CLOSED" cell in the tables below is a re-statement of the cited
upstream PR's own self-assessed verdict, not a new claim by this note.

**Primary runner:**
[`scripts/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.py`](../scripts/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.py)
**Cached output:**
[`logs/runner-cache/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.txt`](../logs/runner-cache/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.txt)

## 0. Why this note exists

Four recent closure attempts (PRs #1060, #1061, #1051, #1049, #890) each
declared "downstream cascade-closure" effects on multiple separately-tracked
admissions. Each upstream PR's body asserts its own list of downstream items
it closes. Audit reviewers (and later cross-referenced source-notes) need a
**single consolidated table** showing:

1. which upstream source-note carries which load,
2. which downstream items are claimed to be discharged by that upstream load,
3. the per-item self-assessed status from the upstream PR.

This note does NOT re-derive any of the closures. It does NOT promote any
admission. It does NOT claim that the upstream attempts succeed — those
verdicts belong to the independent audit lane. It only collects the
**cross-references** in one place so a reviewer auditing one node of the
cascade can see the full link structure without grepping multiple PR
bodies.

Pattern reference: `docs/CROSS_LANE_DEPENDENCY_MAP_NOTE_2026-04-30.md`.

## 1. The four cascades

### (A) B(b) cascade — canonical mass coupling

**Upstream load-bearing PR:** #1060 — `closure/c-bb-canonical-mass-coupling-2026-05-10`

**Upstream source-note:**
[`docs/CLOSURE_C_BB_CANONICAL_MASS_COUPLING_NOTE_2026-05-10_cBB.md`](CLOSURE_C_BB_CANONICAL_MASS_COUPLING_NOTE_2026-05-10_cBB.md)

**Load discharged:** M-linearity of the gravitational source map,
`rho_mass(x) = M * rho_grav(x)`, derived from the canonical Grassmann
staggered Dirac action `S_F = chi-bar (m + M_KS) chi`. The mass term
`m * (chi-bar chi)` is linear in `m` by action structure (bilinear in
chi, linear coefficient); combining with the unified Born identification
`<chi-bar_x chi_x> = rho_grav(x)` of gnewtonG2 gives `m * rho_grav(x)`.

**Cascade table:**

| Downstream item | Upstream load | Self-assessed status from PR #1060 |
|---|---|---|
| gnewtonG3 B(b) load (`V_grav = m*phi`) | M-linearity in coupling | **CLOSED** by canonical action structure |
| W-GNewton-Valley B(b) load (PR #1024, `rho_mass = M*rho_grav`) | M-linearity in source | **CLOSED** — same B(b) load as above |
| GRAVITY_CLEAN admission (b), M-linearity sub-part only | M-linearity in `rho` | **CLOSED** (Born-as-source identification, the *non-linearity* sub-part of admission (b), remains **BOUNDED** via gnewtonG2) |

**What is NOT discharged by the B(b) cascade:**

- The full admission (b) of GRAVITY_CLEAN — Born-as-source identification
  (`rho = |psi|^2` as the *unique gravitational source map*) is NOT
  closed by #1060. That sub-part remains bounded via gnewtonG2 per
  the PR's own "What this does NOT close" stanza.
- Admission (a) `L^{-1} = G_0` (skeleton selection) — remains open per gnewtonG1.
- Admission (c) `S = L(1 - phi)` (weak-field response) — gnewtonG3 closes
  it bounded-conditional only, with `V_grav = m*phi` as cited input.
- The staggered-Dirac realization gate itself (open per `MINIMAL_AXIOMS_2026-05-03`).

### (B) Staggered-Dirac cascade — LH content

**Upstream load-bearing PR:** #1061 — `closure/c-staggered-dirac-gate-2026-05-10`

**Upstream source-note:**
[`docs/CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md`](CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md)

**Load discharged:** Unified H_F = C^8 staggered taste-cube identification.
The retained `CL3_SM_EMBEDDING_THEOREM` Section A staggered embedding
`Gamma_1 = sigma_1 ⊗ I ⊗ I`, `Gamma_2 = sigma_3 ⊗ sigma_1 ⊗ I`,
`Gamma_3 = sigma_3 ⊗ sigma_3 ⊗ sigma_1` on `V = (C^2)^⊗3 = C^8` unifies
the per-site Cl(3) representation and the BZ-corner taste cube on the
*same* C^8.

**Cascade table (P-LH-Order-One four-admission decomposition from PR #1057):**

| Admission | Status before PR #1061 | Self-assessed status from PR #1061 |
|---|---|---|
| (A1) LH content (SM-vs-PS selection) | named primitive admission | **RELOCATED** to D_F class-selection (downstream of Chamseddine-Connes 2013 fine selection) |
| (A2) D_F construction | structurally undetermined | **CLOSED** — `D_F = Gamma_1 + Gamma_2 + Gamma_3` constructed explicitly |
| (A3) Order-one condition | named NCG admission | **STRUCTURALLY CLOSED** — testable on the constructed `D_F` (block-scalar vacuous; minimal viol ~16; Yukawa-like viol ~1.4 documented) |
| (A4) `A_F = C ⊕ H ⊕ M_3(C)` unification | sector obstruction | **CLOSED** — all summands acting on the same `C^8` |

**Net admission count change asserted by PR #1061:** 4 → 1 downstream question.

**What is NOT discharged by the staggered-Dirac cascade:**

- The relocated SM-vs-PS fine-selection question is now in the
  Chamseddine-Connes 2013 selection class — itself **OPEN** in literature
  and not claimed closed by #1061.
- Yukawa hierarchy / observable SM matching is NOT delivered (per #1061 HR3:
  "structural closure ≠ observable matching").
- The Connes 96-dim `H_F^Connes` is only PARTIALLY derived (one taste cube
  per generation candidate; full 96 = local triple × hw=1 Z_3 orbit ×
  particle/antiparticle).
- PR #1061 state is **CLOSED** (per GitHub PR state), so its salvage
  status follows the source-only review-loop policy. This dependency-map
  re-states verdicts from its own body; it does not assert the PR was
  merged or its claims retained.

### (C) BAE-Heavy-quark cascade — primitive M1 ≡ M2 election

**Upstream load-bearing PR:** #1049 — `primitive/p-bae-m1-m2-duality-2026-05-10`

**Upstream source-note:**
[`docs/PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md`](PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md)

**Load discharged:** Saddle-equivalence of two candidate primitives:
- M1 (multiplicity-counting trace state, log-functional form)
- M2 (isotype-reduced action integral, Lagrangian form)

Both algebraically force the BAE saddle `|b|^2/a^2 = 1/2`. PR #1049
records: **for BAE-closure purposes, M1 = M2** (saddle-equivalent); for
full one-loop fluctuation content, M1 ≠ M2 (Hessian factor of 2).

**Cascade table:**

| Downstream item | Upstream load | Self-assessed status from PR #1049 |
|---|---|---|
| BAE primitive election (M1 OR M2) | Saddle-equivalence at the BAE point | **CLOSED** at the saddle level — either choice yields BAE; recommendation to audit lane is to elect either |
| P-HeavyQ Casimir-closure D3 (`rho_lep = sqrt(2)`) | Inherits BAE-saddle as `sqrt(2)/2 → sqrt(2)` lepton-ρ identification | **NOT CLOSED** by #1049 — D3 is foreclosed by PR #828's 30-probe BAE campaign (Probe 29 records partial-falsification) per PR #1051's bounded no-go |
| Heavy-quark species-DIFFERENTIATION on `y_q(M_Pl)` | Inherits absence of multiplicity-counting primitive on `C_3`-isotype decomposition | **NOT CLOSED** by #1049 — species-DIFFERENTIATION gap remains **OPEN** per PR #1051 |

**Status authority note:** PR #1049 explicitly states "no retention requested"
and "audit lane retains full authority over classification and downstream
status." The "election" referenced here is the upstream PR's own
recommendation to elect either M1 or M2 as the canonical primitive
— it is NOT this dependency-map note's claim that such an election has
occurred.

**Companion upstream:** PR #1051 (`primitive/p-heavyq-casimir-closure-2026-05-10`,
source-note
[`docs/PRIMITIVE_P_HEAVYQ_CASIMIR_CLOSURE_NOTE_2026-05-10_pPheavyq_closure.md`](PRIMITIVE_P_HEAVYQ_CASIMIR_CLOSURE_NOTE_2026-05-10_pPheavyq_closure.md))
records the bounded no-go on Casimir derivation of (D1, D2, D3). The
combination of #1049 + #1051 makes explicit what the BAE primitive
election does (saddle equivalence) and does NOT do (heavy-quark
species-DIFFERENTIATION).

### (D) Substep-4 cascade — AC_φλ atom = BAE

**Upstream load-bearing PR:** #890 — `claude/substep4-ac-lambda-separate-closure-2026-05-10`

**Upstream source-note:**
[`docs/SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md`](SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md)

**Load discharged:** Sharpened partial separation of the substep-4 atomic
decomposition

`AC_narrow = AC_φ ∧ AC_λ ∧ AC_φλ`

where:
- `AC_φλ ≡ BAE` (Brannen Amplitude Equipartition, per `BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09` / PR #790)
- `AC_λ` separately closed conditionally under retained meta companion
  notes (PR #728 C_3-preservation, PR #729 conventions, PR #790 BAE rename)
  + Kawamoto-Smit block-diagonality
- `AC_φ` remains a bounded structural no-go candidate (untouched)

**Cascade table:**

| Downstream item | Upstream load | Self-assessed status from PR #890 |
|---|---|---|
| AC_λ atom separate-closure | Kawamoto-Smit + meta companions | **SHARPENED BOUNDED** (inherits bounded tier from Kawamoto-Smit upstream + audit-pending meta) |
| AC_φλ atom = BAE | Identical to BAE primitive saddle (PR #836 30-probe terminal synthesis) | **TERMINALLY BOUNDED** via 30-probe campaign (untouched here) |
| AC_φ atom | Untouched | bounded structural no-go candidate (unchanged) |
| Substep-4 surface tier | NA — only admission count/shape | **UNCHANGED** (still `bounded_theorem`) |

**Net atomic admission count change asserted by PR #890:** 3 → 2 atoms
(`AC_φ ∧ AC_φλ`) + inherited Kawamoto-Smit + retained-meta conditional.

**What is NOT discharged by the substep-4 cascade:**

- Substep-4 surface tier is NOT promoted (still `bounded_theorem`).
- AC_φλ closure remains terminal-bounded via PR #828 30-probe BAE campaign.
- AC_φ remains a bounded structural no-go candidate within `A_min`.
- PR #890 state is **CLOSED** (per GitHub PR state), so the salvage
  status follows the source-only review-loop policy.

## 2. Consolidated per-admission status table

| Admission / Downstream item | Upstream PR (cascade load) | Self-asserted post-cascade status | Cascade key |
|---|---|---|---|
| gnewtonG3 B(b) load | #1060 | CLOSED (M-linearity sub-part) | (A) |
| W-GNewton-Valley B(b) load (PR #1024) | #1060 | CLOSED (same B(b) load) | (A) |
| GRAVITY_CLEAN admission (b) | #1060 | CLOSED M-linearity sub-part; Born-as-source remains BOUNDED via gnewtonG2 | (A) |
| GRAVITY_CLEAN admission (a) `L^{-1} = G_0` | (not in cascade) | OPEN per gnewtonG1 | — |
| GRAVITY_CLEAN admission (c) `S = L(1 - phi)` | (not in cascade) | BOUNDED via gnewtonG3 (cited input `V_grav = m*phi`) | — |
| P-LH-Order-One (A1) LH content | #1061 | RELOCATED to Chamseddine-Connes 2013 fine selection | (B) |
| P-LH-Order-One (A2) D_F construction | #1061 | CLOSED (explicit Γ_1+Γ_2+Γ_3) | (B) |
| P-LH-Order-One (A3) Order-one condition | #1061 | STRUCTURALLY CLOSED (testable on D_F) | (B) |
| P-LH-Order-One (A4) A_F unification | #1061 | CLOSED (C ⊕ H ⊕ M_3(C) on C^8) | (B) |
| BAE primitive (M1 OR M2 election) | #1049 | Saddle-equivalent CLOSED at the BAE saddle | (C) |
| P-HeavyQ D3 (`rho_lep = sqrt(2)`) | #1049 + #1051 | NOT CLOSED — foreclosed by PR #828 30-probe campaign (Probe 29) | (C) |
| P-HeavyQ D1, D2 (`16/9`, `(7/8)+sqrt(2)/2`) | #1051 | NOT CLOSED — convention-level matches within Casimir basis density baseline | (C) |
| Heavy-quark species-DIFFERENTIATION on `y_q(M_Pl)` | #1049 + #1051 | OPEN — multiplicity-counting primitive structurally absent | (C) |
| AC_λ atom (substep-4) | #890 | SHARPENED BOUNDED | (D) |
| AC_φλ atom = BAE (substep-4) | (cascade-anchor only) | TERMINALLY BOUNDED via PR #828 | (D) |
| AC_φ atom (substep-4) | (untouched) | bounded structural no-go candidate | — |
| Substep-4 surface tier | #890 | UNCHANGED `bounded_theorem` | (D) |

## 3. Cross-cascade interaction summary

Two cascades share a **BAE-saddle anchor**:

- (C) BAE-Heavy-quark cascade: M1/M2 saddle-equivalence forces `|b|^2/a^2 = 1/2`.
- (D) Substep-4 cascade: `AC_φλ ≡ BAE` is the identical saddle.

The BAE saddle is **terminally bounded** per the 30-probe campaign
(PR #828); both cascades inherit that ceiling. PR #1049's "M1 ≡ M2
election" does not strengthen the BAE tier — it is a **dual-form**
observation at the saddle level.

Two cascades share an **action-structure anchor**:

- (A) B(b) cascade: M-linearity in mass coupling derived from the
  Grassmann staggered Dirac action.
- (B) Staggered-Dirac cascade: H_F = C^8 unification derived from the
  same staggered embedding `Gamma_1 + Gamma_2 + Gamma_3` (per
  `CL3_SM_EMBEDDING_THEOREM` Section A).

Both reduce the structural surface around the staggered Dirac realization
gate, but the realization gate **itself** remains open per
`MINIMAL_AXIOMS_2026-05-03`.

## 4. What this map does NOT do

- **Does NOT** retain, promote, or admit any item. All status assignments
  in this note are *self-assessments by the cited upstream PRs*;
  retention authority belongs only to the independent audit lane.
- **Does NOT** assert that the upstream cascade closures are themselves
  audit-clean. PR #1061 and PR #890 are **CLOSED** (per GitHub PR state)
  — their salvage status follows the source-only review-loop pattern.
  This note records what their bodies asserted *as they stood when the
  PRs were filed*, for cross-reference convenience only.
- **Does NOT** introduce new axioms, new primitives, or new theorems.
  This is a pure cross-reference note.
- **Does NOT** package any output-packets, working-block notes, lane
  promotions, or synthesis claims. Source-only review-loop policy.
- **Does NOT** modify retained content on `main`. Nothing in `docs/`,
  `audit/`, or `tests/` is changed by this note other than the present
  source-note file plus its paired runner + cache.
- **Does NOT** modify any audit-lane index, retention table, or canonical
  harness. Audit-lane authority is preserved.
- **Does NOT** close, narrow, or sharpen any downstream item beyond what
  the cited upstream PR already self-asserted.

## 5. Hostile-review pattern

A reviewer evaluating this note should check:

| Check | Pass criterion |
|---|---|
| HR1 — No new claims | Every "CLOSED/BOUNDED/RELOCATED" status in §1–§2 is a re-statement of the cited upstream PR's own body, not a new derivation. |
| HR2 — Source-only review-loop | One source-note + one runner + one cache; no synthesis notes, lane promotions, working-block notes, or output-packets. |
| HR3 — No retention requested | Note explicitly disclaims retention authority and downstream-status setting. |
| HR4 — Honest about closed PRs | PRs #1061 and #890 are flagged as `state=CLOSED` in §1; their salvage status is acknowledged. |
| HR5 — No new primitives | Cl(3) local algebra + Z^3 substrate baseline only. No primitive admissions, no derivational imports beyond what each cited PR already used. |
| HR6 — Link consistency | All cited PR numbers, file paths, and `state` values in §1–§2 match GitHub PR metadata at the time of this note (2026-05-10). |
| HR7 — Cross-cascade interactions are observations, not claims | §3 records that two cascades share BAE-saddle / staggered-action anchors; this is an observation about already-published structure, not a derivation. |

## 6. Test plan for the paired runner

The paired runner
[`scripts/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.py`](../scripts/cl3_audit_cascade_dependency_map_2026_05_10_t1cascade.py)
performs **link-consistency checks only** (it does NOT re-verify any of
the upstream closures):

- (T1) For each upstream source-note file path cited in §1, verify that
  the path matches a `docs/*.md` file shape (string-format check; not a
  filesystem check, so the runner is hermetic).
- (T2) For each cascade key (A, B, C, D), verify the per-admission table
  in §2 contains exactly the items the upstream PR self-asserted.
- (T3) For each "CLOSED / BOUNDED / RELOCATED / OPEN" status, verify
  the text in this note matches the upstream PR body's terminology.
- (T4) Verify the BAE-anchor cross-cascade interaction is reciprocally
  recorded in (C) and (D).
- (T5) Verify the staggered-Dirac realization gate is recorded as OPEN
  in *both* (A) and (B) "What is NOT discharged" stanzas.
- (T6) Verify no audit-lane-only verbs ("retain", "promote", "admit",
  "ratify", "approve", "elect") appear in any claim-bearing position in
  this note. Their only allowed occurrence is as quoted upstream content
  or as part of an explicit disclaimer.

## 7. References (file-path cross-reference table)

| Cascade | Source-note path | Runner path |
|---|---|---|
| (A) B(b) | `docs/CLOSURE_C_BB_CANONICAL_MASS_COUPLING_NOTE_2026-05-10_cBB.md` | `scripts/cl3_closure_c_bb_2026_05_10_cBB.py` |
| (B) staggered-Dirac | `docs/CLOSURE_C_STAGGERED_DIRAC_GATE_NOTE_2026-05-10_cStaggered.md` | `scripts/cl3_closure_c_staggered_2026_05_10_cStaggered.py` |
| (C) BAE M1/M2 | `docs/PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality.md` | `scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py` |
| (C) BAE → HeavyQ | `docs/PRIMITIVE_P_HEAVYQ_CASIMIR_CLOSURE_NOTE_2026-05-10_pPheavyq_closure.md` | `scripts/cl3_primitive_p_heavyq_casimir_2026_05_10_pPheavyq_closure.py` |
| (D) substep-4 AC_λ | `docs/SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md` | `scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py` |
| Cited downstream B(b) | `docs/G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md` | (gnewtonG3 runner) |
| Cited downstream B(b) | `docs/KOIDE_W_GNEWTON_VALLEY_LINEAR_BORN_NOTE_2026-05-10_probeW_GNewton_valley.md` | (W-GNewton-Valley runner) |
| Cited downstream B(b) | `docs/GRAVITY_CLEAN_DERIVATION_NOTE.md` | — |
| Cited downstream LH | `docs/PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md` | (P-HeavyQ proposal runner) |
| Companion meta | `docs/BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md` | — |
| Companion meta | `docs/KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md` | — |
| Pattern reference | `docs/CROSS_LANE_DEPENDENCY_MAP_NOTE_2026-04-30.md` | — |
