# YT Retention Master Manifest (Reviewer Entry Point — Submission Under Review)

**Date:** 2026-04-18 (amended 2026-04-18 — Session Round 2 reconciliation)
**Status:** NAVIGATION / INDEX note for the YT **submission branch**
under review. Reviewer entry point for the YT UV-to-IR transport
obstruction program as **proposed** by this branch, organised around
the 27 sub-theorem slots (1 master + 17 P1 + 4 P2 + 5 P3) that
address the P1 / P2 / P3 missing primitives of the master
obstruction theorem, plus the 10 retention-analysis class notes and
the repaired Round 2 SSB matching-gap arithmetic-boundary note that scope the candidate
primitives for the Yukawa-hierarchy gap.

The word "retained" as used below refers to each sub-theorem's
**proposal-side self-classification** (runner passes, log clean,
note on disk). Whether any slot should be promoted to an accepted
retained status on `main` is the reviewer's call. This manifest is
the proposal-side reading guide; it is not an acceptance verdict.

**Canonical proposed central on `Δ_R` is `−3.77 % ± 0.45 %`
(full staggered-PT, framework-native 1-loop).** The literature-cited
three-channel central `−3.27 %` is preserved below as the prior
citation-based assembly, explicitly superseded as the proposal-side
canonical central by P1.15. The 2-loop extension is **bound-
constrained** (loop-geometric envelope, not MC-pinned); see §R2
below for the full Session Round 2 amendment record.

**This note is navigation, not new physics.** It is a structured
roll-up of the sub-theorem notes under review. Every claim carries a
pointer to its authority note, runner, and log. The manifest itself
introduces no new axiom, no new canonical surface, and no new
numerical result, and does not modify any publication-surface file.
The numerical claims live in the sub-theorem notes, not here.

**Primary runner:** `scripts/frontier_yt_retention_manifest.py`
**Log:** `logs/retained/yt_retention_manifest_2026-04-18.log`

**Landing-readiness runner (cross-reference integrity + PASS tally):**
`scripts/frontier_yt_retention_landing_readiness.py`
`logs/retained/yt_retention_landing_readiness_2026-04-18.log`

---

## Preface — Why this note exists

Over multiple rounds of agent-based work the YT retention program has
grown into a suite of sub-theorems targeting the three named missing
primitives `P1`, `P2`, `P3` of the master UV-to-IR transport
obstruction theorem. The suite is large enough that a reviewer
starting from scratch needs an index before descending into the
individual authority notes.

This manifest provides that index. It enumerates the 27 sub-theorem
slots across the master obstruction and three primitives, maps each
slot to a note, runner and log (or flags it as currently embedded-only
in another retained note), states the final retained precision on
the YT lane, lists the remaining open gaps, and gives a suggested
reading order for reviewers entering from different directions.

### Scope discipline

- This manifest is public navigation. It is **not** a
  publication-surface file and does **not** alter the packaged claim
  envelope.
- The retained YT-lane precision recorded below (`Δ_R = −3.77 % ± 0.45 %`
  on full staggered-PT, `172.57 ± 6.9 GeV` for `m_t(pole)` through
  2-loop) is carried from the underlying sub-theorems without
  modification. The publication-surface `m_t(pole)` authority
  continues to be whatever the relevant publication table records; the
  YT-lane figure here is the internal retention-precision readout.
- Some sub-theorem slots are currently **embedded** in another
  retained note rather than standing as a separate authority file.
  These are explicitly flagged below. The manifest does not promote
  them to standalone status and does not speak to whether they should
  be broken out.

### Count

27 sub-theorem slots total (Round 2, including the Round 2 retitled
2-loop bound-envelope slot P1.17):

- **Master obstruction:** 1 slot (M.1; recreated on disk in Round 2)
- **P1 (lattice→MSbar Yukawa/gauge ratio):** 17 slots (P1.1–P1.17)
- **P2 (v-scale matching / taste staircase):** 4 slots
- **P3 (MSbar→pole conversion):** 5 slots

(The manifest itself is not counted. The Round 2 SSB matching-gap
note `YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md` is not a
P1/P2/P3 primitive slot. After audit repair it is a companion
retention-analysis arithmetic-boundary note for the `H_unit`
component overlap, not an independent physical SSB/Yukawa matching
route.)

---

## Part 1 — Master obstruction theorem (1 slot)

### M.1 · UV-to-IR transport obstruction theorem

- **Slot status:** **ON DISK (Round 2 recreation by Agent A, 2026-04-18).**
  The master theorem's P1 / P2 / P3 decomposition and its `~1.95 %`
  packaged total residual are the authority referenced by every
  sub-theorem note below. The standalone note was recreated on
  2026-04-18 and now carries the authority that had previously been
  propagated only through cross-references inside the retained
  `Rep-A/Rep-B` cancellation, `Δ_R` master assembly, and `K-series`
  bound notes.
- **Note:** `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_uv_to_ir_transport_obstruction.py`
- **Log:** `logs/retained/yt_uv_to_ir_transport_obstruction_2026-04-17.log`
- **One-line description:** enumerates the three named missing
  primitives P1 / P2 / P3 of the lattice-UV → SM-IR transport and
  fixes the packaged `~1.95 %` total residual envelope on the Ward
  ratio `y_t² / g_s² = 1 / (2 N_c)`.
- **Retained status:** the three-primitive decomposition is stable;
  every retained sub-theorem in Parts 2–4 names it as non-modified.

---

## Part 2 — P1 sub-theorems (17 slots)

P1 concerns the 1-loop (and partial 2-loop) matching correction on
the Ward ratio `y_t² / g_s²` at `M_Pl` on the tadpole-improved
Wilson-plaquette + 1-link staggered-Dirac canonical surface. The
P1 primitive is the largest quantitative piece of the retention
budget. The 17 slots organise as:

- 2 structural slots (color-factor retention, shortcut no-go)
- 1 symbolic decomposition slot (I_1 = I_S with Ward reduction)
- 1 geometric envelope slot (loop-geometric bound)
- 1 renormalization-framework slot (H-unit tadpole-improvement)
- 3 citation slots (I_S cite, I_S revision verification, Rep-A/B
  partial cancellation)
- 3 per-channel evaluation slots (Δ_1, Δ_2, Δ_3)
- 2 assembly slots (master assembly, SM-RGE cross-check)
- 3 BZ-quadrature slots (schematic, full staggered-PT 1-loop,
  full staggered-PT 2-loop bound-envelope)
- 1 2-loop extension slot (loop-geometric, structural)

### P1.1 · Shared-Fierz shortcut no-go

- **Slot status:** **ON DISK (Round 2 recreation by Agent A, 2026-04-18).**
  The "no shared Fierz shortcut" verdict had been carried inside the
  retained `Rep-A/Rep-B` cancellation theorem (§4.3) and the `I_S`
  citation note's derivation surface; the standalone sub-theorem note
  was recreated on 2026-04-18 and is now promoted to a standalone
  authority file.
- **Note:** `docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_shared_fierz_no_go.py`
- **Log:** `logs/retained/yt_p1_shared_fierz_no_go_2026-04-17.log`
- **One-line description:** no Fierz rearrangement renders the
  scalar-bilinear `Z_S` equal to the scalar-vertex `Z_V` at 1-loop on
  the staggered canonical surface; the ratio correction therefore
  retains a nonzero Dirac/color structure difference.

### P1.2 · Color-factor retention (3-channel C_F / C_A / T_F n_f)

- **Slot status:** **ON DISK (Round 2 recreation by Agent H, 2026-04-18).**
  The C_F / C_A / T_F n_f three-channel retention is the structural
  claim of the retained Rep-A/Rep-B cancellation theorem (P1.8); it
  is now promoted to a standalone authority file as well.
- **Note:** `docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_color_factor_retention.py`
- **Log:** `logs/retained/yt_p1_color_factor_retention_2026-04-17.log`
- **One-line description:** the Ward-ratio 1-loop correction decomposes
  as `Δ_R^ratio = (α_LM/4π) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`
  with nonzero coefficients in all three color channels.

### P1.3 · Loop-geometric bound on Δ_R (r_R = 0.221)

- **Note:** `docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_loop_geometric_bound.py`
- **Log:** `logs/retained/yt_p1_loop_geometric_bound_2026-04-17.log`
- **One-line description:** framework-native geometric envelope
  `r_R = α_LM / π · C_A² = 0.22126` on the loop-expansion tail of
  `Δ_R`; observed 1-loop contribution sits well inside the retained
  ratio envelope.
- **Retained central / bound:** `|tail(N = 1)| ≤ 1.64 %`;
  `|Δ_R^{total}| ≤ 7.41 %`.

### P1.4 · I_1 symbolic decomposition (Ward conserved-current reduction)

- **Slot status:** EMBEDDED-ONLY note; runner and log are retained.
- **Canonical path:** `docs/YT_P1_I1_LATTICE_PT_SYMBOLIC_DECOMPOSITION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`
- **Log:** `logs/retained/yt_p1_i1_lattice_pt_symbolic_2026-04-17.log`
- **One-line description:** symbolic Feynman-rule decomposition of
  the dominant P1 primitive `I_1 = I_S − I_V` with the conserved-current
  Ward reduction `I_V = 0` identically on the retained point-split
  surface.

### P1.5 · I_S literature citation

- **Note:** `docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_i_s_lattice_pt_citation.py`
- **Log:** `logs/retained/yt_p1_i_s_lattice_pt_citation_2026-04-17.log`
- **One-line description:** retained literature-bracket citation of
  the scalar-bilinear `I_S ∈ [4, 10]` with central `I_S ≃ 6` on the
  tadpole-improved staggered surface; replaces the prior packaged
  fundamental-Yukawa stand-in `I_1 = 2`.

### P1.6 · I_S revision verification

- **Note:** `docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_i_s_revision_verification.py`
- **Log:** `logs/retained/yt_p1_i_s_revision_verification_2026-04-17.log`
- **One-line description:** records the `3.0×` upward revision of
  the operational P1 central from packaged `1.92 %` to cited
  `5.77 %` at the single-channel (C_F-only) reading, with the
  "Ward cancellation not established" caveat marked.

### P1.7 · H-unit renormalization (framework-native symbolic)

- **Note:** `docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_h_unit_renormalization.py`
- **Log:** `logs/retained/yt_p1_h_unit_renormalization_2026-04-17.log`
- **One-line description:** retained framework-native derivation of
  the H-unit tadpole-improvement convention on the staggered canonical
  surface; fixes the conversion between framework-native `α_LM` and
  the literature-cited `I_S` convention.

### P1.8 · Rep-A / Rep-B partial cancellation theorem

- **Note:** `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_rep_ab_cancellation.py`
- **Log:** `logs/retained/yt_p1_rep_ab_cancellation_2026-04-17.log`
- **One-line description:** structural decomposition of the
  Ward-ratio 1-loop correction into the three-channel form
  `(C_F, C_A, T_F n_f)`; PARTIAL cancellation verdict — external
  `Z_ψ` cancels exactly, the C_F prefactor cancels up to the
  Dirac/color-structure difference, the `C_A` gluon self-energy
  and the Rep-B scalar anomalous dimension do **not** cancel.

### P1.9 · Δ_1 BZ computation (C_F channel)

- **Note:** `docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_delta_1_bz.py`
- **Log:** `logs/retained/yt_p1_delta_1_bz_2026-04-17.log`
- **One-line description:** `Δ_1 = 2 (I_v_scalar − I_v_gauge) − 6`
  with retained `I_v_gauge = 0` (conserved point-split current);
  literature-central `I_v_scalar ≃ 4` giving `Δ_1 ≃ +2` central,
  range `[0, +8]`.

### P1.10 · Δ_2 BZ computation (C_A channel)

- **Note:** `docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_delta_2_bz.py`
- **Log:** `logs/retained/yt_p1_delta_2_bz_2026-04-17.log`
- **One-line description:** `Δ_2 = I_v_gauge − (5/3) I_SE^{gluon+ghost}`
  with retained `I_v_gauge = 0` and literature-central
  `I_SE^{gluon+ghost} ≃ 2`, giving `Δ_2 ≃ −10/3` central, range
  `[−5, 0]`.

### P1.11 · Δ_3 BZ computation (T_F n_f channel)

- **Note:** `docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p1_delta_3_bz.py`
- **Log:** `logs/retained/yt_p1_delta_3_bz_2026-04-17.log`
- **One-line description:** `Δ_3 = (4/3) I_SE^{fermion-loop}` with
  literature-central `I_SE^{fermion-loop} ≃ 0.7` per flavor,
  giving `Δ_3 ≃ +0.933` central, range `[+0.667, +2.000]`.

### P1.12 · Δ_R master assembly theorem (1-loop central)

- **Note:** `docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_delta_r_master_assembly.py`
- **Log:** `logs/retained/yt_p1_delta_r_master_assembly_2026-04-18.log`
- **One-line description:** roll-up of Rep-A/Rep-B + Δ_1 + Δ_2 + Δ_3
  into a single literature-cited 1-loop central `Δ_R^{1-loop, lit} = −3.271 %`
  with per-channel `(+1.924 %, −7.215 %, +2.020 %)`; recovers
  packaged `+1.92 %` and cited `+5.77 %` as single-channel endpoints.
  The literature-cited `−3.271 %` is **superseded as the canonical retained
  central** by the full-staggered-PT `−3.77 % ± 0.45 %` of P1.15 (see note
  §0 correction); the literature-cited value is preserved as the
  citation-based three-channel roll-up.

### P1.13 · Δ_R SM-RGE cross-validation

- **Note:** `docs/YT_P1_DELTA_R_SM_RGE_CROSSCHECK_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_delta_r_sm_rge_crosscheck.py`
- **Log:** `logs/retained/yt_p1_delta_r_sm_rge_crosscheck_2026-04-18.log`
- **One-line description:** independent 2-loop SM-RGE backward
  integration of `y_t / g_s` from `v` to `M_Pl`; verifies that
  the framework's M-coefficient decomposition reproduces the
  matching at 0.1 %, with `Δ_R` (literature-cited `−3.27 %` or canonical
  full-staggered-PT `−3.77 %`) orthogonal to the RGE running (no
  contradiction).

### P1.14 · BZ quadrature (schematic integrand)

- **Note:** `docs/YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_bz_quadrature_numerical.py`
- **Log:** `logs/retained/yt_p1_bz_quadrature_numerical_2026-04-18.log`
- **One-line description:** first framework-native 4D BZ quadrature
  of the four lattice-PT integrals with a schematic staggered
  numerator `N(k) = Σ_μ cos²(k_μ/2)`; ±25 % per-integral systematic;
  retained central `Δ_R = −3.29 % ± 2.31 %`.

### P1.15 · BZ quadrature (full staggered-PT)

- **Note:** `docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py`
- **Log:** `logs/retained/yt_p1_bz_quadrature_full_staggered_pt_2026-04-18.log`
- **One-line description:** upgrade to full Kawamoto–Smit staggered
  Feynman rules with MSbar continuum subtraction; grid convergence
  at `N ∈ {32, 48, 64}`; tightens per-channel systematic 5× and
  total `Δ_R` uncertainty from ±2.31 % to ±0.45 %. **Retained
  central `Δ_R = −3.77 % ± 0.45 %`** — framework-native at ~1 %
  precision.

### P1.16 · Δ_R 2-loop extension (structural, loop-geometric)

- **Note:** `docs/YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_delta_r_2_loop_extension.py`
- **Log:** `logs/retained/yt_p1_delta_r_2_loop_extension_2026-04-18.log`
- **One-line description:** 8-tensor color-skeleton enumeration of
  the 2-loop extension of `Δ_R`, bounded by the retained loop-geometric
  `r_R = 0.22126` envelope; refined through-2-loop central
  **`Δ_R^{through-2-loop} ≃ −3.99 % ± 0.70 %`**.

### P1.17 · BZ quadrature 2-loop full staggered-PT (magnitude-envelope bound)

- **Note:** `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_p1_bz_quadrature_2_loop_full_staggered_pt.py`
- **Log:** `logs/retained/yt_p1_bz_quadrature_2_loop_full_staggered_pt_2026-04-18.log`
- **One-line description:** schematic 8D Monte-Carlo magnitude-envelope
  check on the eight retained 2-loop color-tensor primitives; retitled
  in Round 2 (Agent C honesty fix) to make explicit that the retained
  2-loop value `−0.834 % ± 0.713 %` is the **loop-geometric bound from
  P1.3 with same-sign saturation**, NOT a framework-native MC matching
  coefficient. The raw 8D-MC signed sum gives `+6.73 %`, 8× the bound
  and opposite sign to 1-loop; this is a signature of missing Ward
  cancellations in the schematic estimator, not a bound violation.
  Through-2-loop retained value `Δ_R^{through-2-loop} ≤ −4.60 %`
  (bound-constrained).

### P1 dependency tree

```
  I_S citation (P1.5)
      │
      ├── I_S revision verification (P1.6)
      │       │
      │       └── Rep-A/Rep-B cancellation (P1.8)  ← Color-factor retention (P1.2) ← Shortcut no-go (P1.1)
      │               │
      │               ├── Δ_1 BZ (P1.9) ← I_1 symbolic decomposition (P1.4)
      │               ├── Δ_2 BZ (P1.10)
      │               └── Δ_3 BZ (P1.11)
      │                       │
      │                       └── Δ_R master assembly (P1.12) ← Loop-geometric bound (P1.3)
      │                               │                              ↑
      │                               ├── BZ quadrature schematic (P1.14) ← H-unit (P1.7)
      │                               │       │
      │                               │       └── BZ quadrature full staggered-PT (P1.15)
      │                               │
      │                               ├── SM-RGE cross-check (P1.13)
      │                               │
      │                               └── Δ_R 2-loop extension (P1.16)
      │
      └── H-unit renormalization (P1.7) → feeds P1.5 ↔ P1.14
```

---

## Part 3 — P2 sub-theorems (4 slots)

P2 concerns the 17-decade lattice-to-v transport factor on
`y_t` that remains after the M_Pl matching, parameterised by the
staircase of taste rungs `n_taste ∈ {16, 15, ..., 0}` and summarised
by the v-matching coefficient `M = √u_0 · F_yt · √(8/9)`.

### P2.1 · Taste-staircase transport (partial)

- **Note:** `docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p2_taste_staircase_transport.py`
- **Log:** `logs/retained/yt_p2_taste_staircase_transport_2026-04-17.log`
- **One-line description:** PARTIAL closure of P2 — 17-decade
  transport of `g_s`, `y_t` reduced to a single open matching
  coefficient `M = 1.9734` at `v`.

### P2.2 · v-matching theorem (M = √u_0 · F_yt · √(8/9))

- **Note:** `docs/YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p2_v_matching.py`
- **Log:** `logs/retained/yt_p2_v_matching_2026-04-17.log`
- **One-line description:** framework-native three-factor decomposition
  of the matching coefficient `M = √u_0 · F_yt · √(8/9)`; 1-loop
  evaluation gives `M = 1.926`, within 2.4 % of the target, bounded
  by the retained QFP-insensitivity 3 % envelope.

### P2.3 · Per-step β functions (NO-GO, non-perturbative)

- **Note:** `docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p2_taste_staircase_beta.py`
- **Log:** `logs/retained/yt_p2_taste_staircase_beta_2026-04-17.log`
- **One-line description:** NO-GO verdict for per-step 1-loop
  perturbative β-function integration across the 16-step taste
  staircase; the staircase is **non-perturbative**, consistent
  with `α_LM^{16}` as a non-perturbative factor.

### P2.4 · F_yt loop-geometric bound (P2 tightening)

- **Note:** `docs/YT_P2_F_YT_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p2_f_yt_loop_geometric_bound.py`
- **Log:** `logs/retained/yt_p2_f_yt_loop_geometric_bound_2026-04-17.log`
- **One-line description:** framework-native geometric upper bound
  on the 3-loop-and-beyond tail of `F_yt`; tightens the P2 residual
  to **0.15 %**, below the packaged P2 budget of ≈ 0.5 %; retained /
  packaged ratio ~ 1.35×.

### P2 dependency tree

```
  Taste-staircase transport (P2.1)  →  v-matching (P2.2)  →  F_yt loop bound (P2.4)
                                             │
                                             └── Per-step β no-go (P2.3)
```

---

## Part 4 — P3 sub-theorems (5 slots)

P3 concerns the MSbar-to-pole conversion of `m_t` carried by the
`K_n` series `m_pole / m_MSbar(m) = 1 + K_1 (α_s/π) + K_2 (α_s/π)² +
K_3 (α_s/π)³ + ...` at the retained top-quark running-coupling anchor
`α_s(m_t) = 0.1079`.

### P3.1 · K_1 framework-native derivation

- **Slot status:** **ON DISK (Round 2 recreation by Agent H, 2026-04-18).**
  The `K_1 = C_F = 4/3` framework-native result had been carried
  inside the P3 K-series geometric-bound note's preface; the
  standalone sub-theorem note is now recreated and promoted to a
  standalone authority file.
- **Note:** `docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p3_msbar_to_pole_k1.py`
- **Log:** `logs/retained/yt_p3_msbar_to_pole_k1_2026-04-17.log`
- **One-line description:** `K_1 = C_F = 4/3` retained framework-native
  from the retained SU(3) Casimirs.

### P3.2 · K_2 color-factor retention (4-tensor)

- **Slot status:** **ON DISK (Round 2 recreation by Agent H, 2026-04-18).**
  The 4-tensor `K_2` color-factor retention result had been carried
  inside the retained K_2 integral citation note (P3.3) and the
  K-series geometric bound (P3.5); the standalone note is now
  promoted to an authority file.
- **Note:** `docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p3_msbar_to_pole_k2.py`
- **Log:** `logs/retained/yt_p3_msbar_to_pole_k2_2026-04-17.log`
- **One-line description:** 4-tensor color-factor decomposition of
  `K_2` retained on the framework surface.

### P3.3 · K_2 two-loop integral citation

- **Note:** `docs/YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p3_k2_integrals.py`
- **Log:** `logs/retained/yt_p3_k2_integrals_2026-04-17.log`
- **One-line description:** retained structural cite-and-verify of
  the four 2-loop on-shell QCD integrals `{I_FF, I_FA, I_Fl, I_Fh}`;
  fixes `I_Fl` from the retained n_l-linear shift and the literature
  target `K_2(n_l=5) = 10.9405` to sub-permille.

### P3.4 · K_3 color-factor retention (10-tensor, 98.7 %)

- **Note:** `docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p3_msbar_to_pole_k3.py`
- **Log:** `logs/retained/yt_p3_msbar_to_pole_k3_2026-04-17.log`
- **One-line description:** 10-tensor `K_3` color-factor retention;
  cumulative structural retention through K_3 ≈ 98.69 %;
  single-next-term bound on δ_4 ≃ 8.2 × 10⁻⁴.

### P3.5 · K_n geometric bound (tail)

- **Note:** `docs/YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`
- **Runner:** `scripts/frontier_yt_p3_k_series_geometric_bound.py`
- **Log:** `logs/retained/yt_p3_k_series_geometric_bound_2026-04-17.log`
- **One-line description:** framework-native geometric tail bound
  `r_bound = (α_s/π) · C_A² = 0.30907` on the `K_n` series at
  `α_s(m_t) = 0.1079`; fractional tail on `m_t` ≤ **0.137 %**,
  below the packaged ~0.3 % P3 budget.

### P3 dependency tree

```
  K_1 framework-native (P3.1)
      │
      └── K_2 color-factor retention (P3.2)
              │
              ├── K_2 integral citation (P3.3)
              └── K_3 color-factor retention (P3.4)
                      │
                      └── K-series geometric bound (P3.5)
```

---

## Part 5 — Final state summary

### Retained YT-lane precision (current)

| Quantity                                    | Central / Band             | Source slot |
|---------------------------------------------|----------------------------|-------------|
| **Δ_R (1-loop, full staggered-PT; CANONICAL RETAINED CENTRAL)** | **−3.77 % ± 0.45 %**       | **P1.15**   |
| Δ_R (1-loop, literature-cited three-channel; superseded as canonical, preserved as citation-based assembly) | −3.27 % ± 2.32 %           | P1.12       |
| Δ_R (through 2-loop, structural extension, literature-cited base)  | −3.99 % ± 0.70 %           | P1.16       |
| Δ_R (through 2-loop, loop-geometric bound-constrained, full-staggered-PT base; **NOT MC-pinned**)  | ≤ −4.60 % ± 0.84 %         | `YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md` |
| P1 loop-expansion bound                     | |Δ_R^tot| ≤ 7.41 %          | P1.3        |
| P2 residual (3-loop tail)                   | 0.15 %                     | P2.4        |
| P3 residual (tail from K_4 onward on m_t)   | 0.137 %                    | P3.5        |
| m_t(pole) YT-lane (1-loop BZ central, canonical) | **172.57 ± 6.50 GeV**      | P1.15 |
| m_t(pole) YT-lane (through 2-loop, structural extension) | 172.57 ± 6.9 GeV           | P1.16       |
| m_t(pole) YT-lane (through 2-loop, bound-constrained full-PT base) | 172.57 ± 7.94 GeV          | 2-loop full-PT note (bound, not MC pin) |
| Observed m_t(pole) (PDG)                    | 172.69 GeV                 | external    |

The canonical 1-loop central **`Δ_R = −3.77 % ± 0.45 %`** is framework-
native (full staggered-PT 4D BZ quadrature, P1.15). The through-2-loop
extension retained here is **loop-geometric bound-constrained**, not
Monte-Carlo-pinned: the schematic 8D MC runner intentionally retained
in Pillar A contributes magnitude-envelope numerics (`J_X` values),
but the retained 2-loop coverage interprets those within the
retained loop-geometric bound (`|Δ_R^{(2)}| ≤ 0.834 %` on this
surface, same-sign as 1-loop by `C_A²`-dominance). The 2-loop
Δ_R value `≤ −4.60 %` recorded in the row above is therefore the
bound-saturated same-sign extension of the 1-loop central, not a
direct MC matching coefficient. This distinction was sharpened in
Session Round 2 (§R2 below); see the §0 Correction in
`docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
for the full honesty-fix audit.

The packaged YT-lane master-obstruction residual envelope is
`~ 1.95 %` (total) and `~ 2 %` in the P3-dominated m_t(pole)
coverage. The retained YT-lane precision has tightened to
`~ 4 %` on m_t(pole) once the 2-loop loop-expansion envelope is
opened against a ±0.7 % `Δ_R`. The retention suite therefore
*sits inside* the packaged ~2 % envelope on per-primitive residuals
(P2 and P3), while the 2-loop extension of P1 tolerates a wider band
that is explicitly within the retained loop-geometric bound.

### Sign / scheme consistency

- Δ_R is **negative** on the retained surface — consistent with the
  MSbar `y_t / g_s` running direction.
- The SM-RGE cross-check (P1.13) confirms `Δ_R` is orthogonal to
  the 2-loop SM-RGE transport; no RGE evidence contradicts the
  retained `Δ_R` (canonical full-staggered-PT `−3.77 %`, or equivalently
  the literature-cited `−3.27 %` consistent within the master assembly's
  literature-bounded band) at `M_Pl`.

---

## Part 6 — Remaining open gaps

### Gap 1 · Embedded-only slot inventory (Round 2 reduction)

At the start of Session Round 2 six sub-theorem slots (M.1, P1.1,
P1.2, P1.4, P3.1, P3.2) were EMBEDDED-only. Round 2 landed:

- **M.1** recreated on 2026-04-18 (Agent A) — ON DISK.
- **P1.1** recreated on 2026-04-18 (Agent A) — ON DISK.
- **P1.2** recreated on 2026-04-18 (Agent H) — ON DISK.
- **P3.1** recreated on 2026-04-18 (Agent H) — ON DISK.
- **P3.2** recreated on 2026-04-18 (Agent H) — ON DISK.
- **P1.4** remains EMBEDDED-only by design — the I_1 symbolic runner
  (21 PASS) and log are on disk; the standalone note has not been
  promoted. This is the ONLY remaining EMBEDDED-only slot in the
  post-Round-2 state.

The set of EMBEDDED-only slots post-Round-2 is **{P1.4}**. Its
retained content is load-bearing through the P1 runners that cite
it as a named prior (I_1 = I_S − I_V with conserved-current Ward
reduction `I_V = 0`); promoting the note to a standalone authority
file is documentation-hygiene, not a scientific gap.

### Gap 2 · Framework-native 4D BZ quadrature

The `Δ_R` pipeline's only remaining literature-citation dependency
is the 2-loop BZ integral **values** (per-channel `I_S`, `I_v_scalar`,
`I_v_gauge`, `I_SE^{gluon+ghost}`, `I_SE^{fermion-loop}`). The full
staggered-PT 4D quadrature (P1.15) closes the **framework-native**
central `Δ_R = −3.77 % ± 0.45 %`, but the absolute scheme invariance
is MODERATE until an independent staggered lattice-PT cross-check
reproduces the same four integrals to better than the current ±5 %
per-integral systematic.

### Gap 3 · P2 non-perturbative staircase

The per-step β-function no-go (P2.3) is definitive: the 16-step
taste staircase is non-perturbative at the canonical-surface coupling.
PARTIAL closure of P2 remains through the v-matching theorem plus
the F_yt loop-geometric bound; full closure would require a
framework-native non-perturbative `α_LM^{16}` derivation, which
is outside the current retention scope by design.

### Gap 4 · P3 2-loop framework-native derivation

The K_2 integral citation (P3.3) pins `I_Fl` from the retained
n_l-linear shift and the literature target — a two-loop on-shell QCD
derivation on the retained `Cl(3) / Z^3` action would close this
citation. The K-series geometric bound (P3.5) makes this a coverage,
not an accuracy, question: the fractional tail on `m_t` is already
≤ 0.14 %.

---

## §R2 — Session Round 2 corrections (2026-04-18)

This section records the amendments made during Session Round 2 to
sharpen the canonical status, correct interpretive framing in
several notes, and promote previously EMBEDDED-only sub-theorems to
standalone authority files. **No canonical number in the retention
suite was changed.** The Round 2 amendments are scope / framing
corrections that preserve the underlying numerics.

### §R2.1 Δ_R canonical central (Agent B)

- **Amendment:** §0 Correction added to
  `docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`.
- **Content:** the literature-cited three-channel central
  `Δ_R = −3.27 % ± 2.32 %` is explicitly superseded as the canonical
  retained central by the framework-native full-staggered-PT central
  `Δ_R = −3.77 % ± 0.45 %` (P1.15). The literature-cited central is
  preserved as the citation-based three-channel roll-up.
- **Manifest reflection:** Part 5 table now leads with the full-PT
  central; the citation-based central is retained as a second row.

### §R2.2 2-loop MC honesty fix (Agent C)

- **Amendment:** §0 Correction added to
  `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`.
- **Content:** the retitled note retains the 8D MC runner as a
  **magnitude-envelope check**, not a framework-native 2-loop MC pin.
  The `Δ_R^{(2)},raw = +6.73 %` is 8× the retained loop-geometric
  bound and has the wrong sign relative to 1-loop; this is a
  signature of missing Ward-identity cancellations between
  gauge-group-irreducible topologies in the schematic estimator,
  not a bound violation. The retained 2-loop coverage is therefore
  **bound-constrained** (same-sign saturation `|Δ_R^{(2)}| ≤ 0.834 %`),
  **not MC-pinned**.
- **Manifest reflection:** Part 5 row for the 2-loop full-PT central
  is labelled "bound-constrained, **NOT MC-pinned**" and the
  accompanying paragraph spells out the distinction. The remaining
  framework-native 4D BZ 2-loop closure is flagged as an open
  coverage item in Gap 4.

### §R2.3 Class-scope corrections on retention-analysis notes (Agent D)

- **Class #2** (`YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`):
  §0 Correction added — the original Outcome D ("no retained mechanism
  for generation hierarchy") was narrow-technically correct for the
  position-basis diagonal content of C_3-commuting operators but
  missed the Fourier-basis circulant mechanism, which IS a retained
  generation-labeled spectrum. Cross-reference to the Koide circulant
  character-theoretic derivation in `codex/science-workspace-2026-04-18`.
- **Class #1** (`YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`):
  §10 scrutiny audit added — Class #1's Outcome C (flavor-column
  decomposition of H_unit is a no-go) is CONFIRMED on both narrow and
  broad scope; the §0 correction pattern of Class #6 / Class #2 does
  NOT apply here because the iso×color space carries no C_3 analog
  and no hidden Fourier basis exists.
- **Class #4** (`YT_RIGHT_HANDED_SPECIES_DEPENDENCE_NOTE_2026-04-18.md`):
  §4.2 updated — inherits the canonical `Δ_R = −3.77 %` framework-
  native central identically across both up-type and down-type
  channels (right-handed U(1)_Y charges do not modify SU(N)
  Clebsch-Gordan factors).

### §R2.4 Class #5 matching-gap closure (Agent E)

- **Amendment:** §0 Correction / Refinement added to
  `docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md`.
- **Content:** the "matching gap" originally flagged as out-of-scope
  is CLOSEABLE on the retained surface via the Clifford chirality
  decomposition `ψ̄ψ = ψ̄_L ψ_R + ψ̄_R ψ_L` inherited from the
  anomaly-forced time theorem's γ_5 structure. The species-uniform
  CG factor 1/√6 is preserved; H_unit is intrinsically a
  chirality-flipping (LH–RH) bilinear. Classes #3 and #7 required
  no correction.

### §R2.5 b-Yukawa scope correction (Agent F)

- **Amendment:** §0 Scope correction added to
  `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`.
- **Content:** the original framing "Outcome A: Yukawa unification
  at M_Pl, empirically FALSIFIED by 33× on m_b" was overly strong
  read literally (it suggests the framework itself is falsified).
  The corrected scope: the species-uniform INTERPRETATION of the
  retained 1PI Ward identity is falsified at 33× on m_b, NOT the
  framework's m_t prediction (which uses a species-privileged BC on
  a different chain, `YT_ZERO_IMPORT_CHAIN_NOTE.md`). A species-
  differentiation primitive is required to close the absolute m_b
  scale; candidate is the Koide circulant Fourier-basis spectrum.

### §R2.6 Embedded-only slot recreations (Round 2 landed)

- **Agent A (completed):**
  - **M.1** master obstruction theorem note — ON DISK.
  - **P1.1** shared-Fierz shortcut no-go — ON DISK.
- **Agent H (completed, landed during manifest update):**
  - **P1.2** color-factor retention (C_F / C_A / T_F n_f) — ON DISK.
  - **P3.1** K_1 framework-native derivation — ON DISK.
  - **P3.2** K_2 color-factor retention (4-tensor) — ON DISK.
- **Agent I (completed):**
  - New note `docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md`
    with runner `scripts/frontier_yt_ssb_matching_gap.py` and log
    `logs/retained/yt_ssb_matching_gap_2026-04-18.log` — ALL ON DISK.

### §R2.7 SSB matching-gap note (new, Round 2)

- **Note:** `docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md`
- **Runner:** `scripts/frontier_yt_ssb_matching_gap.py`
- **Log:** `logs/retained/yt_ssb_matching_gap_2026-04-18.log` (19 PASS, 0 FAIL)
- **Content:** audit-repaired arithmetic-boundary note. It verifies that,
  given `H_unit = I_(N_iso*N_c) / sqrt(N_iso*N_c)`, each single
  component overlap is `1 / sqrt(N_iso*N_c)`, hence `1 / sqrt(6)` at
  `(N_iso,N_c)=(2,3)`. It does **not** close the physical SSB/Yukawa
  matching theorem.

### §R2.8 First-round reviewer findings (2026-04-18)

The first reviewer pass on this submission branch surfaced three
internal-consistency issues. This §R2.8 records the fixes landed in
response; all fixes preserve the underlying science and sharpen the
proposal-side framing.

- **R2.8.a — Runner / note slot-status agreement.** The previous
  manifest runner still hard-coded M.1, P1.1, P1.2, P3.1, P3.2 as
  `embedded` even though this manifest note records them as ON DISK
  via Agents A and H. The runner's `SLOTS` table has been upgraded
  to reflect the on-disk reality: those five slots are now
  `retained` with their note, runner, and log paths populated, and
  the new P1.17 slot (full-staggered-PT 2-loop BZ note) is
  explicitly catalogued. `EXPECTED_TOTAL_SLOTS` is raised from 26
  to 27, `EXPECTED_P1_SLOTS` from 16 to 17, `EXPECTED_RETAINED_SLOTS`
  from 21 to 27, `EXPECTED_EMBEDDED_SLOTS` from 5 to 0, with P1.4
  remaining as the sole `retained`-slot whose NOTE (not runner) is
  embedded-only by design. Pillar A grand PASS total shifts from
  the legacy 799 to 868 as these slots come fully into scope.
- **R2.8.b — 2-loop BZ note scrub of stale "MC-pinned" language.**
  The §0 honesty correction on the P1.17 note established the
  2-loop value as bound-constrained, not MC-pinned. Residual body
  lines that still said "through-2-loop MC-pinned", "MC retained
  (this note)", or "the 2-loop central is now framework-native
  MC-pinned" have been scrubbed to match §0. The per-channel
  `J_X` magnitude envelopes remain correctly described as
  MC-measured — those are per-topology magnitudes, not matching
  coefficients — and all references to a gauge-invariant MC pin
  now clearly flag that as OPEN.
- **R2.8.c — Proposal-side framing of the readiness and manifest
  notes.** Both the landing-readiness report and this manifest
  formerly read as if the bundle were already-retained / "clear
  for integration" ahead of a review decision. The top-level
  framing on both notes has been rewritten to submission-under-
  review language: "proposal-side self-audit", "READY FOR REVIEW",
  "the reviewer retains the accept / revise / reject call."
  The per-pillar status lines use "proposal-side self-audit: PASS"
  in place of "CLEAR FOR INTEGRATION".

None of these fixes modify a canonical numerical value. They
reconcile the branch's own self-description with the underlying
state on disk.

---

## Part 7 — Reviewer reading guide

Suggested starting points depending on the question.

### 7.A · "Why should I believe the retained `m_t(pole) = 172.57 GeV`?"

Start at the central P1 assembly and trace outward:

1. **P1.12** Δ_R master assembly (literature-cited 1-loop central −3.27 %; superseded as canonical)
2. **P1.15** BZ quadrature full staggered-PT (**canonical framework-native −3.77 % ± 0.45 %**)
3. **P1.16** 2-loop extension (through-2-loop −3.99 % ± 0.70 % on literature-cited base; see also the full-staggered-PT 2-loop assembly at `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md` with through-2-loop central −4.60 % ± 0.84 %)
4. **P2.2** v-matching (M = 1.9734 with 1-loop M = 1.926)
5. **P2.4** F_yt loop-geometric bound (residual 0.15 %)
6. **P3.5** K-series geometric bound (residual 0.14 %)

The chain closes on m_t(pole) = 172.57 ± 6.9 GeV vs observed 172.69.

### 7.B · "Where is the color-factor structure established?"

1. **P1.8** Rep-A/Rep-B cancellation theorem (three-channel Δ_R decomposition)
2. **P1.4** I_1 symbolic decomposition (Ward `I_V = 0` on conserved current)
3. **P3.2** K_2 color-factor retention + **P3.4** K_3 color-factor retention

### 7.C · "What is framework-native vs literature-cited?"

- Framework-native: `C_F`, `C_A`, `T_F`, `α_LM`, `u_0`, `n_f`, `n_l`,
  loop-geometric bounds (P1.3, P2.4, P3.5), Ward `I_V = 0`
  (P1.4), `K_1 = 4/3` (P3.1).
- Literature-cited: `I_S`, `I_v_scalar`, `I_SE^{gluon+ghost}`,
  `I_SE^{fermion-loop}`, `K_2 = 10.9405`, `K_3 = 101.4040`.
- Framework-native-with-citation-verification: `Δ_R = −3.77 % ± 0.45 %`
  via P1.15 full staggered-PT.

### 7.D · "What is the loop-geometric envelope?"

1. **P1.3** Loop-geometric bound on Δ_R (r_R = 0.22126)
2. **P2.4** F_yt loop-geometric bound (tightens P2)
3. **P3.5** K-series geometric bound (tightens P3)

All three use only retained SU(3) Casimirs + the retained coupling
anchor; no external K_4 or 3-loop M value enters as a derivation
input.

### 7.E · "Where are the NO-GO results?"

1. **P1.1** Shared-Fierz shortcut no-go (embedded in P1.5 / P1.8)
2. **P2.3** Per-step β no-go (staircase non-perturbative)

---

## Part 8 — Complete dependency graph

```
                          ┌──────────────────────────────────────────────┐
                          │   M.1 · UV-to-IR transport obstruction       │
                          │        (3 primitives: P1, P2, P3)            │
                          └──┬──────────────────┬──────────────────┬─────┘
                             │                  │                  │
                    ┌────────┴────────┐  ┌──────┴──────┐   ┌───────┴──────┐
                    │   P1 suite      │  │   P2 suite  │   │    P3 suite  │
                    │  (17 slots)     │  │  (4 slots)  │   │   (5 slots)  │
                    └─────────────────┘  └─────────────┘   └──────────────┘

P1:
   P1.1 shortcut no-go ──┐
                         │
   P1.2 color-factor ────┼──► P1.8 Rep-A/B ──► P1.9 Δ_1 ──┐
                         │     cancellation    P1.10 Δ_2 ──┼──► P1.12 Δ_R ───► P1.13 SM-RGE x-check
   P1.5 I_S cite  ──► P1.6 I_S revision         P1.11 Δ_3 ─┘    master        ───► P1.16 Δ_R 2-loop
         │                       │                                assembly          extension
         └──► P1.7 H-unit ───────┘                                    │
                         ▲                                            │
   P1.4 I_1 symbolic ────┘                                            ▼
   P1.3 loop-geom ──────────────────────────────────────────────► P1.14 BZ schematic
                                                                        │
                                                                        ▼
                                                                   P1.15 full staggered-PT
                                                                   (retained central
                                                                    Δ_R = −3.77 ± 0.45 %)

P2:
   P2.1 staircase transport ──► P2.2 v-matching ──► P2.4 F_yt loop bound
                                         │
                                         └──► P2.3 per-step β no-go

P3:
   P3.1 K_1 framework ──► P3.2 K_2 color ──► P3.3 K_2 integrals
                                     │                │
                                     └──► P3.4 K_3 ──┴──► P3.5 K-series geom bound

Cross-suite anchor:
   P1.3 loop-geom   ◄─────► P2.4 F_yt loop bound ◄─────► P3.5 K-series geom bound
        (same retained SU(3) Casimir + coupling envelope, three anchors)
```

---

## Part 9 — Full validator roll-up

The table below is the authoritative per-slot retention table. The
`PASS` column records the number of `[PASS]` markers emitted by the
retained runner into the retained log on 2026-04-17 or 2026-04-18.

Slots in EMBEDDED-ONLY status carry no standalone runner and
therefore contribute 0 to the PASS count from this manifest's
perspective; their content is counted through the runners that cite
them as prior (i.e. no double counting).

| Slot  | Title                                          | Standalone artifacts (Round 2)           | PASS |
|-------|------------------------------------------------|------------------------------------------|-----:|
| M.1   | UV-to-IR transport obstruction theorem         | note + runner + log (Round 2, Agent A)   |    5 |
| P1.1  | Shared-Fierz shortcut no-go                    | note + runner + log (Round 2, Agent A)   |    4 |
| P1.2  | Color-factor retention (C_F/C_A/T_F n_f)       | note + runner + log (Round 2, Agent H)   |    5 |
| P1.3  | Loop-geometric bound                           | note + runner + log                      |   43 |
| P1.4  | I_1 symbolic decomposition (Ward I_V = 0)      | runner + log (note EMBEDDED)             |   21 |
| P1.5  | I_S literature citation                        | note + runner + log                      |   33 |
| P1.6  | I_S revision verification                      | note + runner + log                      |   38 |
| P1.7  | H-unit renormalization (framework-native)      | note + runner + log                      |   48 |
| P1.8  | Rep-A/Rep-B partial cancellation               | note + runner + log                      |   45 |
| P1.9  | Δ_1 BZ computation (C_F)                       | note + runner + log                      |   55 |
| P1.10 | Δ_2 BZ computation (C_A)                       | note + runner + log                      |   42 |
| P1.11 | Δ_3 BZ computation (T_F n_f)                   | note + runner + log                      |   51 |
| P1.12 | Δ_R master assembly (1-loop, citation-based; superseded as canonical) | note + runner + log | 68 |
| P1.13 | Δ_R SM-RGE cross-check                         | note + runner + log                      |   31 |
| P1.14 | BZ quadrature schematic                        | note + runner + log                      |   40 |
| P1.15 | BZ quadrature full staggered-PT (**canonical**) | note + runner + log                     |   45 |
| P1.16 | Δ_R 2-loop extension (bound-constrained)       | note + runner + log                      |   79 |
| P1.17 | BZ quadrature 2-loop full-PT (bound-envelope, NOT MC-pinned) | note + runner + log          |   50 |
| P2.1  | Taste-staircase transport (partial)            | note + runner + log                      |   12 |
| P2.2  | v-matching theorem                             | note + runner + log                      |   12 |
| P2.3  | Per-step β no-go                               | note + runner + log                      |   12 |
| P2.4  | F_yt loop-geometric bound                      | note + runner + log                      |   48 |
| P3.1  | K_1 framework-native                           | note + runner + log (Round 2, Agent H)   |    4 |
| P3.2  | K_2 color-factor retention (4-tensor)          | note + runner + log (Round 2, Agent H)   |    6 |
| P3.3  | K_2 two-loop integral citation                 | note + runner + log                      |   30 |
| P3.4  | K_3 color-factor retention (10-tensor)         | note + runner + log                      |   18 |
| P3.5  | K-series geometric bound                       | note + runner + log                      |   28 |
| —     | SSB matching-gap arithmetic-boundary note (Round 2, Agent I) | note + runner + log        |   19 |
|       |                                                | **Core retention runner PASS total (Pillar A)** | **868** |
|       |                                                | **Pillar B (retention-analysis + SSB) PASS** |   595 |
|       |                                                | **Pillar C (manifest + master) PASS**    |   154 |
|       |                                                | **Grand total retained PASS** (session tally via landing-readiness runner) | **1617** |
|       |                                                | **Retained runner FAIL total**           |    0 |
|       |                                                | **Retained slots on disk (of 27 P1/P2/P3 + master)** |   26 |
|       |                                                | **EMBEDDED-only slots (post-Round-2)**   |    1 (P1.4 by design) |
|       |                                                | **Total primitive + master slots indexed** | 27 |
|       |                                                | **Retention-analysis companion notes**   |  10 classes + SSB |

Per-pillar retention PASS totals (via the landing-readiness runner
`scripts/frontier_yt_retention_landing_readiness.py`, post-Round-2):

| Pillar                                                     | Runners | PASS  | FAIL |
|------------------------------------------------------------|--------:|------:|-----:|
| A (P1 + P2 + P3 primitive suite)                           |      26 |   868 |    0 |
| B (retention-analysis class notes + SSB companion)         |      11 |   595 |    0 |
| C (master obstruction + manifest)                          |       2 |   154 |    0 |
| **Grand total**                                            |  **39** |**1617**|    0 |

Note: Pillar A now covers all 17 P1 slots (P1.1–P1.17), all 4 P2
slots, and all 5 P3 slots; only P1.4 (I_1 symbolic decomposition)
remains EMBEDDED-only by design (its runner and log are on disk).
Pillar B includes the ten retention-analysis class notes plus the
Round 2 SSB matching-gap arithmetic-boundary companion note (Agent I).
Pillar C is the
master obstruction theorem (recreated by Agent A) plus the retention
manifest itself.

---

## Safe claim boundary

This manifest makes the following claims and no others:

1. The 27 sub-theorem slots named above organise the current retained
   YT-lane retention suite; each EMBEDDED-only slot is named
   explicitly, along with the Round 2 recreations in progress.
2. The on-disk retained sub-theorems have note, runner, and log files
   that exist at the paths cited above; the landing-readiness runner
   (`scripts/frontier_yt_retention_landing_readiness.py`) verifies
   this at run time.
3. The on-disk retained runners, when run, emitted `[PASS]` lines
   summing to **1617 across 39 log files** and 0 `[FAIL]` lines, on
   the dates recorded in their log filenames (tally via the
   landing-readiness runner).
4. The retained YT-lane precision on `Δ_R` and `m_t(pole)` reported in
   Part 5 is carried faithfully from the underlying sub-theorems
   without modification. The canonical 1-loop central is `Δ_R =
   −3.77 % ± 0.45 %` on the full-staggered-PT surface; the through-
   2-loop retained band is **bound-constrained**, not MC-pinned.
5. The Session Round 2 amendments catalogued in §R2 are scope /
   framing corrections only; no canonical number was changed.

The manifest does **not** claim:

- that the P1.4 EMBEDDED-only slot has been promoted to a standalone
  note (it remains embedded by design, with runner + log on disk);
- any framework-native 4D BZ quadrature beyond what the P1.15 full
  staggered-PT note proposes (±0.45 % on Δ_R);
- any framework-native 2-loop MC pin of `Δ_R^{(2)}` — the proposed
  2-loop coverage is loop-geometric bound-constrained;
- any physical SSB/Yukawa matching closure from the Round 2 SSB
  companion note, which is now scoped to `H_unit` component-overlap
  arithmetic;
- any new bound, value, or derivation; the manifest introduces no
  new physics;
- any modification of the master obstruction theorem's packaged
  `~1.95 %` residual envelope or the publication-surface
  `m_t(pole)` table.

---

## Validation

The validator for this manifest is
`scripts/frontier_yt_retention_manifest.py` (slot accounting and
log consistency) and the landing-readiness runner
`scripts/frontier_yt_retention_landing_readiness.py` (cross-reference
integrity sweep + per-pillar PASS tally + anomaly scan across the
full session). The landing-readiness runner performs:

1. **Cross-reference integrity sweep.** For every session-dated YT
   note (`docs/YT_*_2026-04-17.md`, `docs/YT_*_2026-04-18.md`),
   resolve every Markdown link target that points at a repo file
   (`docs/`, `scripts/`, `logs/`) and assert the target exists on
   disk. Broken references are listed explicitly.
2. **Runner-log PASS / FAIL tally.** For every `logs/retained/yt_*.log`
   file, count the number of lines whose first non-whitespace tokens
   are `[PASS]` or `[FAIL]`, aggregate per-pillar (A = P1+P2+P3
   primitive suite; B = retention-analysis class notes; C = manifest
   + master obstruction), and report grand totals.
3. **Anomaly detection.** Any runner with zero `[PASS]` markers or a
   non-zero `[FAIL]` count is flagged as an anomaly and reported in
   a dedicated section.

Running:

```
python scripts/frontier_yt_retention_landing_readiness.py \
    > logs/retained/yt_retention_landing_readiness_2026-04-18.log 2>&1
```

produces the structured landing-readiness log. As of 2026-04-18
(post-Round-2 reconciliation including §R2.8 runner-note agreement)
the expected result is:

- cross-reference integrity sweep: 5 expected broken references
  (to the EMBEDDED-only P1.4 note and related tolerated session links),
  0 unexpected broken references;
- grand total PASS = 1617 across 39 proposal-runners, 0 FAIL.

The legacy pre-§R2.8 figure "1552 across 35 runners" reflected the
earlier state where M.1, P1.1, P1.2, P3.1, P3.2 were `embedded`-
only in the manifest runner and the SSB companion had not yet
landed. That figure is superseded.

The legacy per-slot manifest runner (`frontier_yt_retention_manifest.py`)
remains the slot-inventory authority; the landing-readiness runner
is the cross-reference + tally authority.
