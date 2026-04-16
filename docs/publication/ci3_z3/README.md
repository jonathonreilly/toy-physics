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
2. retained standalone quantitative lanes (`alpha_s`, EW normalization)
3. derived-with-explicit-systematic Yukawa/top and derived-with-inherited-explicit-systematic Higgs/vacuum lanes
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
- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](../../YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)
- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

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
- derived-with-explicit-systematic `y_t(v) = 0.9176`
- derived-with-explicit-systematic canonical `m_t(pole) = 173.10 GeV` (3-loop),
  with retained `172.57 GeV` (2-loop) support
  with the current explicit bridge budget of `1.2147511%` conservative
  (`0.75500635%` support-tight) carried by the Yukawa/top lane
- promoted CKM atlas/axiom closure package
  (no quark-mass or fitted CKM inputs; canonical CMT `alpha_s(v)` input):
  `|V_us| = 0.22727`,
  `|V_cb| = 0.04217`,
  `|V_ub| = 0.003913`,
  `delta = 65.905 deg`,
  `J = 3.331 x 10^-5`
- derived-with-inherited-explicit-systematic Higgs / vacuum package:
  canonical `m_H = 125.1 GeV` (framework-side 3-loop route),
  with retained `119.8 GeV` (2-loop support route),
  vacuum-stability readout inherited from the explicit `y_t` systematic
- exact taste-block fermion-CW isotropy support theorem with bounded
  taste-scalar near-degeneracy companion:
  `m_taste = 124.91 GeV`, scalar-only `v_c/T_c = 0.3079`

## Other Bounded Families

- DM flagship gate, with exact transport-chain progress and stronger PMNS reduced-surface support
- older bounded CKM mass-basis / Cabibbo / partial Jarlskog route history
- cosmology bounded family such as `\Omega_\Lambda`, `n_s`, `w = -1`
- bounded secondary predictions already on `main`:
  proton lifetime, CKM neutron EDM, down-type flavor-mass CKM-dual ratios,
  vacuum critical stability, taste-scalar near-degeneracy, benchmark
  gravitational decoherence

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
