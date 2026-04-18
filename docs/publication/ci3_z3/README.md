# CI(3) / Z^3 Publication Package

This directory is the publication-facing entrypoint for the current `main`
package.

Use this package instead of browsing raw repo chronology.

Framework statement:

- the public package stands on the one-axiom reduction notes
  [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md)
  and
  [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md)
- [MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md) is the
  operational package-boundary memo for the current audited implementation
  surface, not a competing axiom count

## External Reviewer Read Order

1. [Public arXiv draft](./ARXIV_DRAFT.md)
2. [Prediction surface](./PREDICTION_SURFACE_2026-04-15.md)
3. [Inputs and qualifiers](./INPUTS_AND_QUALIFIERS_NOTE.md)
4. [What this paper does not claim](./WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
5. [AI assistance and accountability](./AI_ASSISTANCE_AND_ACCOUNTABILITY_NOTE.md)
6. [External reviewer guide](./EXTERNAL_REVIEWER_GUIDE.md)
7. [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-15.md)
8. [Publication matrix](./PUBLICATION_MATRIX.md)
9. [Quantitative summary table](./QUANTITATIVE_SUMMARY_TABLE.md)
10. [Claims table](./CLAIMS_TABLE.md)
11. [Derivation atlas](./DERIVATION_ATLAS.md)
12. [Derivation / validation map](./DERIVATION_VALIDATION_MAP.md)
13. [Full claim ledger](./FULL_CLAIM_LEDGER.md)
14. [Results index](./RESULTS_INDEX.md)

## Current Package Shape

The package has four layers:

1. retained theorem core
2. retained standalone quantitative lanes (`alpha_s`, EW normalization,
   exact lattice-scale Yukawa/gauge Ward theorem)
3. derived Yukawa/top and Higgs/vacuum lanes
4. bounded prediction surface plus live gates and frozen-out route history

The public manuscript surface on `main` is arXiv-first. Journal-specific
packaging is private and is not kept here as a competing public draft.

The package is already predictive in a reviewer-facing sense. For the shortest
summary of what is already predicted on `main`, use
[PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md).
For the explicit package boundary, use:

- [INPUTS_AND_QUALIFIERS_NOTE.md](./INPUTS_AND_QUALIFIERS_NOTE.md)
- [WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](./WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
- [AI_ASSISTANCE_AND_ACCOUNTABILITY_NOTE.md](./AI_ASSISTANCE_AND_ACCOUNTABILITY_NOTE.md)

## Current Quantitative Component Stack

The current canonical quantitative stack is modular:

- [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md)
- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](../../YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)
- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [KR_A1_VANISHING_SUPPORT_NOTE.md](../../KR_A1_VANISHING_SUPPORT_NOTE.md)

Current package status:

- retained `alpha_s(M_Z) = 0.1181`
- retained EW normalization package:
  `sin^2(theta_W)(M_Z) = 0.2306`,
  `1/alpha_EM(M_Z) = 127.67`,
  `g_1(v) = 0.4644`,
  `g_2(v) = 0.6480`
  where `alpha_s(v)` comes from the same-surface plaquette chain,
  `g_1(v), g_2(v)` use derived `R_conn = 8/9` support, and the `M_Z`
  rows use the retained running bridge
- retained exact lattice-scale Ward theorem:
  `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`
- derived `y_t(v) = 0.9176`
- derived canonical `m_t(pole) = 173.10 GeV` (3-loop),
  with retained `172.57 GeV` (2-loop) support
  and current primary-route standard-method residuals
- derived Higgs / vacuum package:
  `m_H = 125.1 GeV` (framework-side 3-loop route), with retained
  `119.8 GeV` (2-loop support route)
- promoted CKM atlas/axiom closure package
  (no quark-mass or fitted CKM inputs; canonical CMT `alpha_s(v)` input):
  `|V_us| = 0.22727`,
  `|V_cb| = 0.04217`,
  `|V_ub| = 0.003913`,
  `delta = 65.905 deg`,
  `J = 3.331 x 10^-5`
- exact CKM carrier-side support theorem:
  `K_R(q) = 0` for every pure `A1` background on the seven-site support block
  via [KR_A1_VANISHING_SUPPORT_NOTE.md](../../KR_A1_VANISHING_SUPPORT_NOTE.md)
- retained three-generation matter structure now also has an atlas-wired exact
  flavor support packet on `main`:
  the full BZ-corner site-phase / cube-shift bridge
  [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](../../SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md),
  the exact taste-cube `S_3` decomposition
  [S3_TASTE_CUBE_DECOMPOSITION_NOTE.md](../../S3_TASTE_CUBE_DECOMPOSITION_NOTE.md),
  the exact `S_3` `hw=1` mass-matrix no-go
  [S3_MASS_MATRIX_NO_GO_NOTE.md](../../S3_MASS_MATRIX_NO_GO_NOTE.md),
  and the exact residual `Z_2` Hermitian normal form
  [Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md](../../Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md);
  these are support theorems for the retained matter lane and future flavor
  work, not additional flagship flavor-numerics claims
- derived Higgs / vacuum package:
  canonical `m_H = 125.1 GeV` (framework-side 3-loop route),
  with retained `119.8 GeV` (2-loop support route),
  vacuum-stability readout inherited from the current `y_t` lane
- exact taste-block fermion-CW isotropy support theorem with bounded
  taste-scalar near-degeneracy companion:
  `m_taste = 124.91 GeV`, scalar-only `v_c/T_c = 0.3079`
- retained Bell/CHSH support theorem on explicit two-species lattice systems:
  KS taste operators are constructed explicitly, `G=0` stays exactly at
  `|S| = 2.000`, and periodic Poisson coupling yields finite-lattice CHSH
  violation on the retained 1D/2D/3D family
- retained discrete evanescent-barrier lattice bound + Schwarzschild
  tortoise-length identity on `Cl(3)/Z^3` with framework-axiom spacing
  `a = l_Planck`: (A) rigorous discrete-Schroedinger transfer-matrix bound
  `|G| <= C exp[-sum_i ln lambda_+(i)]` with
  `lambda_+(i) = (u_i + sqrt(u_i^2 - 4))/2`, `u_i = 2 + (V_i - E)/t`;
  (B) exact tortoise-length identity
  `L*(R_min, R_S; eps) = R_S ln((R_S - R_min)/eps) + eps + R_min - R_S`.
  The Planck-unit astrophysical exponent `exp[-(R_S/l_P) ln(R_S/R_min)]`
  carried by the bounded GW-echo null companion is (C-rate)-conditional on
  an order-one per-unit-tortoise-length rate lower bound and is NOT on the
  retained surface of this theorem

## Other Bounded Families

- Charged-lepton mass-hierarchy observational-pin closure (Koide `Q = 2/3`), carried on the repo as a bounded charged-lepton package. Reviewer entry point: [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md). Retained content: algebraic Koide-cone equivalence (Theorem 1); retained `hw=1` second-order-return shape theorem with three independent weight slots (Theorem 2, publication-grade robust); mass/mixing subspace disjointness theorem `dim(V_H ∩ V_D) = 0` (Theorem 3); six rigorous structural no-gos on retained non-Higgs-Yukawa mechanisms (§5); three higher-order structural theorems (transport identity, variational-principle survey with the real-irrep-block-democracy candidate primitive, fourth-order signed Clifford ordering cancellation — Theorems 4–6); observational-pin closure at 3-real PDG input (Theorem 7). The 3→3 pin produces no spare observable analogous to the retained neutrino-mixing 3→4 `δ_CP` forecast. Convention-invariant under mass-vs-mass-squared pin choice (Convention A/B cross-check). Pin is unique as a set up to positive scale; a residual `S_2` labeling ambiguity on `w_a ↔ w_b` persists on the retained surface and is invariant under Koide `Q` and the Σ spectrum. 19 runners, 518 PASS / 0 FAIL on origin/main base.
- DM flagship gate, with exact transport-chain progress, theorem-grade same-surface thermal bounding and a certified current-bank numerator-selector no-go, source-side reduction all the way to the `2`-real `Z_3` doublet-block law, plus a repo-live G1 PMNS-as-`f(H)` conditional/support package: the PMNS map from `H` is fixed and `q_H` is GAUGE-retained, but the chamber pin still depends on an imposed branch-choice rule, so the remaining live blocker is still the physical selector law / current-bank DM-mapping gap
- curated neutrino boundary/support packet on `main`, with exact current-stack
  Majorana zero law, exact mass reduction to the Dirac lane, and exact
  last-mile reduction to `(J_chi, mu)`; still outside the manuscript surface
- persistent exact-lattice compact-object companion on `main`, with one
  retained blended readout on the nearby family and a `top4` multistage floor
  that survives beyond the widened pocket, but still below persistent
  inertial-mass / matter closure because the inward-source directional
  boundary remains
- older bounded CKM mass-basis / Cabibbo / partial Jarlskog route history
- cosmology bounded family such as `\Omega_\Lambda`, `n_s`, `w = -1`
- bounded secondary predictions already on `main`, plus the CKM-only
  neutron-EDM corollary with bounded continuation:
  proton lifetime, down-type flavor-mass CKM-dual ratios, vacuum critical
  stability, taste-scalar near-degeneracy, benchmark gravitational
  decoherence

## Package Rules

- the matrix is the publication inventory
- the claims table is the retained manuscript surface
- the derivation / validation map is the retained evidence contract
- the atlas is the reusable theorem / subderivation toolbox
- each live lane gets one canonical authority stack, not multiple competing
  route notes

If an older note is not linked from the package, it is not front-door
authority.

## Optional History Bucket

- [Historical frozen-out registry](../../work_history/publication/FROZEN_OUT_REGISTRY.md)
- [Historical remote-branch audit](../../work_history/publication/REMOTE_BRANCH_AUDIT_2026-04-14.md)
- [Historical stale-authority audit](../../work_history/publication/STALE_AUTHORITY_AUDIT_2026-04-14.md)
