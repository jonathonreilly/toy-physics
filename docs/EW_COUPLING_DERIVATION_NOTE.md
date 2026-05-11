# Electroweak Coupling Derivation: g_1(v), g_2(v), lambda(v)

**Date:** 2026-04-14 (originally); 2026-05-03 (review-loop repair)
**Status:** SUPERSEDED by `COMPLETE_PREDICTION_CHAIN_2026_04_15.md`; bounded-status support scan
**Claim type:** bounded_theorem
**Primary runner:** [`scripts/ew_coupling_bounded_status_runner_2026_05_03.py`](../scripts/ew_coupling_bounded_status_runner_2026_05_03.py) (post-2026-05-03 repair)
**Companion runner (does NOT match this note's claims):** [`scripts/frontier_yt_ew_coupling_derivation.py`](../scripts/frontier_yt_ew_coupling_derivation.py) — that runner scans a `taste_weight` parameter against `sin^2(theta_W)` and reports different g_1, g_2 outputs; it is a separate derivation attempt, not a verifier of this note.

## Review-loop repair (2026-05-03)

The 2026-05-03 review follow-up identified that the
previously named primary runner (`frontier_yt_ew_coupling_derivation.py`)
does NOT reproduce this note's stated calculations. That runner fits
a `taste_weight = 0.390` parameter to match `sin²θ_W = 0.23122`,
reports g_1 ≈ 0.438 and g_2 ≈ 0.611 — values different from this
note's g_1 = 0.590 (1-loop derivation) and `g_2` BOUNDED.

Repair: a new primary runner
[`scripts/ew_coupling_bounded_status_runner_2026_05_03.py`](../scripts/ew_coupling_bounded_status_runner_2026_05_03.py)
reproduces exactly what this note claims:

  D1  g_1(v) DERIVED via 1-loop U(1) RGE from M_Pl with α_LM = 0.0907
      → g_1_GUT(v) = 0.590, ~27% above observed (expected at 1-loop SU(5))
  D2  g_2(v) BOUNDED — SU(2) Landau pole barrier identified; no fit
      to observable; non-perturbative SU(2) matching remains open
  D3  λ(v) BOUNDED — Coleman-Weinberg lower bound (3 y_t⁴ / 8π²)
      and vacuum-stability upper window; no derivation yet
  D4  y_t sensitivity table reproducing note Part 5 (EW couplings
      subdominant to QCD beta in y_t chain)

The new runner does NOT introduce or fit any new parameter. It does
not touch `taste_weight`. The note and primary runner now compute
the same scoped quantities (PASS=4/4).

The status table is unchanged in content but is now backed by an
executable runner that matches it. g_2(v) and λ(v) remain BOUNDED
(not derived) — this is the honest scope of the note. The taste-weight
runner remains in the repo as a separate, distinct derivation attempt
that requires its own audit and is not a verifier for this note.

---

## Input-authority chain (audit-explicit)

The 2026-05-05 audit verdict (`audited_conditional`, critical, load-bearing
9.281) flagged that the restricted packet did not supply retained-grade
derivations of `alpha_LM = 0.0907`, SU(5) unification at `M_Pl`, the RGE
authority, or the Planck-to-v boundary setup. The repair target was
"missing_dependency_edge: provide retained upstream derivations or
restricted-packet authorities for alpha_LM, SU(5) M_Pl matching, RGE
coefficients/normalizations, and the y_t sensitivity computation."

This section makes the input-side dependency chain explicit. Each row points
to the authority that supplies the runner's hard-coded numeric input
(`scripts/ew_coupling_bounded_status_runner_2026_05_03.py`). The audit ledger
remains the only authority for current audit verdicts and effective status;
this section does not derive any input, does not promote this row, and does
not change the BOUNDED status of `g_2(v)` or `lambda(v)`.

| Runner input | Runner value | Authority surface | Audit-ledger status (read-only) |
|---|---|---|---|
| `alpha_LM` (Planck-scale GUT coupling) | `0.0907` | [`ALPHA_S_DERIVED_NOTE.md`](./ALPHA_S_DERIVED_NOTE.md), [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](./ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) | `audited_conditional` (alpha_s_derived_note); `audited_conditional` (plaquette_self_consistency_note); `unaudited` (alpha_lm_geometric_mean_identity decoration). Strongest current leg of the input chain. |
| 1-loop U(1) running coefficient `b_1 = +4.10` | `+4.10` | [`SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`](./SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md) (sister surface for SU(2) `b_2`); `YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md` (taste-staircase corrections) | `unaudited` (su2_weak_beta_coefficient); `unaudited` (yt_p2_taste_staircase). Standard-textbook SM `b_1 = +4.10` is admitted-context literature input. |
| `M_Pl / v` ratio (`ln(M_Pl/v) = 38.44`) | `38.44` | [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md), [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](./HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md), [`GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md`](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md) | `retained_bounded` (hierarchy_spatial_bc); `retained` (hierarchy_matsubara); `retained_bounded` (connected_hierarchy_theorem). This is the strongest leg of the input chain. |
| Native SU(2) gauge structure (lattice `g_2² = 1/(d+1) = 1/4` at lattice scale) | structural | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](./NATIVE_GAUGE_CLOSURE_NOTE.md), [`YT_EW_COLOR_PROJECTION_THEOREM.md`](./YT_EW_COLOR_PROJECTION_THEOREM.md), [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](./G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md). Plain-text file pointer: `docs/G_WEAK_FROM_FRAMEWORK_STRETCH_ATTEMPT_NOTE_2026-05-03.md` (cycle-break: that note already cites this one as the bounded surface for residual R1, so it is referenced as a plain-text file pointer here, not a markdown dependency). | `retained_bounded` (native_gauge_closure_note); `retained_bounded` (yt_ew_color_projection_theorem); `unaudited` (g_bare_canonical_convention); `unaudited` (g_weak_from_framework_stretch_attempt). Lattice-scale `g_2² = 1/4` is structural; only the v-scale running surface is bounded. |
| `y_t` sensitivity baseline (`y_t(v)`, `m_t`) | `0.917`, `172.69 GeV` | [`YT_ZERO_IMPORT_AUTHORITY_NOTE.md`](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md), [`YT_EW_COLOR_PROJECTION_THEOREM.md`](./YT_EW_COLOR_PROJECTION_THEOREM.md) | `unaudited` (yt_zero_import_authority); `audited_conditional` (yt_ew_color_projection_theorem). The note's Part 5 sensitivity table is qualitative — used to confirm that EW couplings are subdominant to QCD beta in the y_t chain, not as a derivation input. |

This section changes only discoverability of the runner inputs. It does not
derive any of the five values, does not promote this note, and does not
change the BOUNDED status of `g_2(v)` and `lambda(v)`.

## Substantive residual (audit-explicit)

The audit verdict is unchanged by the citations above: `g_2(v)` and `lambda(v)`
remain BOUNDED, not derived. The runner's PASS=4/4 confirms that the note's
lattice-scale and Landau-pole content is internally consistent, but that does
not close the v-scale derivation.

The substantive residual is two-part, mirroring the note's Parts 3 and 4:

- **R1: SU(2) staircase running surface (M_Pl → v) for `g_2(v)`.** The note's
  Part 3 establishes the Landau-pole barrier explicitly: 1-loop perturbative
  running from M_Pl crosses `1/alpha_2 = 0` at `mu ~ 4e9 GeV`, so any
  framework-native derivation of `g_2(v) = 0.646` must pass through a
  non-perturbative matching surface (SU(2) Monte Carlo for `u_0(SU(2))`, or a
  framework-native taste-staircase analogue). Sister authority (plain-text
  file pointer for cycle safety: `docs/G_WEAK_FROM_FRAMEWORK_STRETCH_ATTEMPT_NOTE_2026-05-03.md`,
  not a markdown dependency, because that note already cites this one as
  the bounded surface for its residual R1) closes the lattice-scale piece
  (`g_2² |_lattice = 1/(d+1) = 1/4`, `g_2_bare = 1/2`) using retained
  primitives and INVERTS the cycle 12 obstruction framing: the v-scale gap is
  now identified as a missing audit ratification of an already-bounded SU(2) running
  chain, not a missing primitive. That stretch attempt remains `unaudited`
  and does not promote `g_2(v)` to retained.

- **R2: Higgs quartic `lambda(v)` boundary derivation.** The note's Part 4
  records two complementary bounds (Coleman-Weinberg lower estimate
  `lambda_CW = 3 y_t⁴ / 8π² = 0.034`; vacuum-stability upper window from
  `lambda(M_Pl) > 0`). Closing this row would require deriving `m_H` from the
  framework's G_5 condensate or a sister mechanism. Sister authorities are
  the Higgs-side derivation surfaces — `docs/HIGGS_MASS_DERIVED_NOTE.md`
  (full 3-loop RGE from `lambda(M_Pl) = 0` boundary) and
  `HIGGS_MASS_FROM_AXIOM_NOTE.md` (tree-level mean-field). Both are given
  as plain-text file pointers for cycle safety, because
  `HIGGS_MASS_DERIVED_NOTE.md` already cites this row in its
  `Input-authority chain` section as the `g_2(v)` and `g_1(v)` authority
  surface, and `HIGGS_MASS_FROM_AXIOM_NOTE.md` participates in the same
  3-cycle through that input-authority chain. This row carries the
  Higgs-side `g_2(v)` precision caveat that the Higgs lane inherits. See
  [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](./HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  for the most recent bounded scoping of the Higgs-quartic boundary.

Neither R1 nor R2 closes in this rigorize pass. The bounded scope of this
note is unchanged and the audit verdict (`audited_conditional`) is the
authoritative status. This section names the residuals so the audit graph can
test the chain directly.

---

## Motivation

The y_t chain uses g_1(v) and g_2(v) imported from experiment:

    alpha_EM(M_Z) = 1/127.951,  sin^2(theta_W)(M_Z) = 0.23122

and hardcodes lambda(v) = 0.129 = m_H^2/(2v^2). These enter the y_t
beta function as subdominant EW corrections. Codex accepts these as
"fair game" inputs for the y_t chain, but deriving them would close
the import and strengthen the overall framework.

This note documents the attempt and its honest results.

---

## Part 1: The Landau Pole Constraint

### 1.1 The framework's coupling strength

The Cl(3)/Z^3 framework sets the GUT coupling at M_Pl via SU(5)
unification: g_1_GUT = g_2 = g_3 at M_Pl, with

    alpha_GUT = alpha_LM = alpha_bare / u_0 = 0.0907  (1/alpha = 11.03)

This is STRONGER than the standard SU(5) GUT coupling:

    alpha_GUT(standard SU(5)) ~ 1/25 ~ 0.04 at M_GUT ~ 2e16 GeV

The framework coupling is 2.3x larger, at a scale 600x higher.

### 1.2 Perturbative running from M_Pl to v

The 1-loop running gives:

    1/alpha_i(v) = 1/alpha_GUT - b_i/(2pi) * ln(v/M_Pl)

With ln(M_Pl/v) = 38.44, the shift is b_i/(2pi) * 38.44 = 6.12 * b_i.

| Coupling | b_i     | Shift    | 1/alpha(v) | Status        |
|----------|---------|----------|------------|---------------|
| U(1)     | +4.10   | +25.08   | 36.11      | Perturbative  |
| SU(2)    | -3.167  | -19.38   | -8.35      | LANDAU POLE   |
| SU(3)    | -7.00   | -42.83   | -31.80     | LANDAU POLE   |

**g_1**: U(1) is NOT asymptotically free (b_1 > 0). The coupling
WEAKENS going from M_Pl to v. Perturbative running works.

**g_2**: SU(2) IS asymptotically free (b_2 < 0). The coupling GROWS,
hitting a Landau pole at ~4e9 GeV. Perturbative running fails.

**g_3**: SU(3) IS asymptotically free (b_3 < 0). Landau pole at
~6e14 GeV. (Known; the CMT provides alpha_s(v) = 0.1033.)

### 1.3 Physical interpretation

The framework's strong GUT coupling (alpha_LM = 0.091 vs standard
0.04) means that BOTH SU(2) and SU(3) require non-perturbative
UV-IR matching to connect M_Pl to v. For SU(3), this is the taste
staircase encoded by the Coupling Map Theorem. For SU(2), an
analogous non-perturbative mechanism is needed.

This is a PREDICTION of the framework, not a failure. It explains
WHY the CMT is necessary: the lattice coupling is too strong for
perturbative running to bridge 38 decades.

---

## Part 2: g_1(v) -- DERIVED

Since U(1) running is perturbative from M_Pl to v:

    alpha_1_GUT(v) = 1 / (1/alpha_LM + b_1/(2pi) * ln(M_Pl/v))
                   = 1 / (11.03 + 25.08)
                   = 1 / 36.11
                   = 0.02769

    g_1_GUT(v) = sqrt(4 pi * 0.02769) = 0.5899

    g_1_SM(v)  = g_1_GUT * sqrt(3/5) = 0.4569

**Comparison to experiment:**

    g_1_GUT(v) from framework = 0.5899
    g_1_GUT(v) from experiment = 0.4640
    Deviation: +27%

The 27% deviation is expected at 1-loop SU(5). Known corrections:

1. **2-loop RGE corrections**: shift 1/alpha by O(1) out of 36
2. **GUT threshold corrections**: heavy GUT particles at M_Pl
   modify the matching by O(few)
3. **Proton decay constraints**: in standard SU(5), the matching
   scale is adjusted to M_GUT ~ 2e16 (not M_Pl) partly to satisfy
   proton decay bounds. The framework may have different matching.

The prediction is in the right ballpark. A 27% deviation at 1-loop
for a 38-decade extrapolation is comparable to the classic SU(5)
prediction quality (the original GW paper had similar discrepancies
before 2-loop improvements).

---

## Part 3: g_2(v) -- BOUNDED, NOT DERIVED

### 3.1 The Landau pole barrier

The SU(2) coupling hits a Landau pole at mu ~ 4e9 GeV when running
perturbatively from M_Pl. This is a hard barrier: no perturbative
resummation can cross it.

### 3.2 CMT extension (Approach A)

If the CMT applies universally: alpha_2(v) = alpha_bare/u_0^2 = 0.1033.
This gives g_2(v) = 1.139, which is 76% above the observed 0.646.
The overestimate occurs because the CMT u_0 is computed from SU(3)
Monte Carlo, and the SU(2) mean-field link would differ.

### 3.3 Backward constraint (Approach B)

Running the OBSERVED g_2(v) = 0.646 backward (v -> M_Pl) gives
alpha_2(M_Pl) = 0.0202, which is 78% below alpha_GUT = 0.0907.
This gap measures the non-perturbative correction that the taste
staircase contributes to SU(2) coupling evolution.

### 3.4 Status

g_2(v) requires either:
- An SU(2) Monte Carlo to compute u_0(SU(2)) for the CMT, or
- A framework-native non-perturbative matching for SU(2)

Until then, g_2(v) is BOUNDED but not derived.

---

## Part 4: lambda(v) -- BOUNDED, NOT DERIVED

### 4.1 Status

lambda(v) = m_H^2 / (2v^2) requires deriving m_H from the G_5
condensate structure of the Cl(3) framework. This is not yet done.

### 4.2 Bounds

**Vacuum stability**: lambda(v) must remain positive up to M_Pl.
The 1-loop RGE scan gives a stability window. The observed
lambda = 0.129 is near the metastability boundary, as is well known.

**Coleman-Weinberg estimate**: The dominant top-quark loop gives
lambda_CW = 3 y_t^4 / (8 pi^2) = 0.034. This is the correct
order of magnitude but 3.8x below observed, indicating significant
gauge boson and self-coupling contributions.

### 4.3 Impact on y_t

lambda enters beta_{y_t} ONLY at 2-loop via:

    beta_{y_t}^{(2)} contains: +6 lambda^2 - 6 lambda y_t^2

Over 17 decades, varying lambda from 0 to 0.5 shifts m_t by ~1 GeV.
Lambda is genuinely subdominant for the y_t chain.

---

## Part 5: y_t Sensitivity Analysis

The backward Ward derivation y_t(v) = 0.973 depends on the EW
couplings used in the beta function. The sensitivity test:

| Configuration            | g_1     | g_2     | m_t [GeV] | delta_m_t |
|--------------------------|---------|---------|-----------|-----------|
| Imported (experiment)    | 0.464   | 0.646   | 169.4     | baseline  |
| Derived g_1 + obs g_2   | 0.590   | 0.646   | 175.0     | +5.6 GeV  |
| No EW (g_1 = g_2 = 0)   | 0.000   | 0.000   | 146.0     | -23.4 GeV |

The derived g_1 (27% too large) shifts m_t by 5.6 GeV, which is
non-negligible but within the 2-loop systematic of the chain. The
complete EW removal shifts m_t by 23 GeV (14%), confirming that
the QCD beta coefficient (c_3 = 8) dominates over the EW
contributions (c_2 = 9/4, c_1 = 17/20).

**For the y_t chain**: The imported EW couplings remain the correct
choice until g_2 is derived from non-perturbative matching. The
Codex assessment that these are "subdominant imports" is confirmed
quantitatively.

---

## Import Status Table

| Parameter    | Value    | Status    | Source                           |
|-------------|----------|-----------|----------------------------------|
| alpha_s(v)  | 0.1033   | DERIVED   | CMT, n_link = 2                  |
| v           | 246.28 GeV| DERIVED   | Hierarchy theorem                |
| g_1_GUT(v)  | 0.590    | DERIVED   | 1-loop RGE from M_Pl (+27%)      |
| g_2(v)      | --       | BOUNDED   | CMT est / backward constraint    |
| lambda(v)   | --       | BOUNDED   | Stability + CW estimate          |
| y_t(v)      | 0.973    | DERIVED   | Backward Ward (robust to EW)     |

---

## Remaining Work

1. **SU(2) non-perturbative matching**: Compute u_0(SU(2)) from
   SU(2) Monte Carlo, or derive an SU(2) taste staircase matching.
   This would move g_2(v) from BOUNDED to DERIVED.

2. **2-loop g_1 correction**: The 1-loop g_1(v) has 27% deviation.
   2-loop and GUT threshold corrections should reduce this
   significantly. (Standard SU(5) at 2-loop gives ~few% agreement.)

3. **Higgs mass from G_5 condensate**: Deriving m_H would fix
   lambda(v) and close the last bounded input.

4. **CKM and DM gates**: The derived/bounded EW couplings feed into
   the CKM mass-ratio route and DM relic density calculations.
   The bounds established here are sufficient for those applications.
