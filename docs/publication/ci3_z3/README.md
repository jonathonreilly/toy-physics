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
2. [External reviewer guide](./EXTERNAL_REVIEWER_GUIDE.md)
3. [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-15.md)
4. [Prediction surface](./PREDICTION_SURFACE_2026-04-15.md)
5. [Publication matrix](./PUBLICATION_MATRIX.md)
6. [Quantitative summary table](./QUANTITATIVE_SUMMARY_TABLE.md)
7. [Inputs and qualifiers](./INPUTS_AND_QUALIFIERS_NOTE.md)
8. [What this paper does not claim](./WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
9. [Claims table](./CLAIMS_TABLE.md)
10. [Derivation atlas](./DERIVATION_ATLAS.md)
11. [Derivation / validation map](./DERIVATION_VALIDATION_MAP.md)
12. [Full claim ledger](./FULL_CLAIM_LEDGER.md)
13. [Frozen-out registry](./FROZEN_OUT_REGISTRY.md)
14. [Results index](./RESULTS_INDEX.md)

For one-note gravity/gauge continuum positioning across the current package,
use [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md).

## Current Package Shape

The package has four layers:

1. retained theorem core
2. retained standalone quantitative lanes (`alpha_s`, EW normalization)
3. bounded Yukawa/top and Higgs/vacuum lanes
4. bounded prediction surface plus live gates and frozen-out route
   history

The public manuscript surface on `main` is now arXiv-first. Journal-specific
packaging is private and is not kept as a competing public draft in this
directory.

The package is also already predictive in a reviewer-facing sense. For the
shortest summary of what is already predicted on `main`, use
[PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md).
For the explicit package boundary, use:

- [INPUTS_AND_QUALIFIERS_NOTE.md](./INPUTS_AND_QUALIFIERS_NOTE.md)
- [WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](./WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)

## Current Quantitative Component Stack

The current canonical quantitative stack is modular:

- [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_QFP_INSENSITIVITY_THEOREM.md](../../YT_QFP_INSENSITIVITY_THEOREM.md)
- [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md)
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
- bounded `y_t(v) = 0.9176`
- bounded `m_t(pole) = 172.57 GeV` (2-loop), `173.10 GeV` (3-loop)
  with the current `~3%` QFP/RGE-surrogate systematic carried explicitly by
  the Yukawa/top lane
- promoted CKM atlas/axiom closure package
  (no quark-mass or fitted CKM inputs; canonical CMT `alpha_s(v)` input):
  `|V_us| = 0.22727`,
  `|V_cb| = 0.04217`,
  `|V_ub| = 0.003913`,
  `delta = 65.905 deg`,
  `J = 3.331 x 10^-5`
- bounded Higgs / vacuum package:
  `m_H = 119.8 GeV` (2-loop support route),
  `125.3 GeV` (framework-side 3-loop route),
  bounded vacuum-stability readout inherited from the bounded `y_t` / QFP lane

## Package Rules

- the matrix is the publication inventory
- the claims table is the retained manuscript surface
- the derivation / validation map is the retained evidence contract
- the atlas is the reusable theorem / subderivation toolbox
- each live lane gets one canonical authority stack, not multiple competing
  route notes

If an older note is not linked from the package, it is not front-door
authority.

## Current Paper Surface

Retained backbone:

- weak-field gravity from the Poisson / Newton chain
- weak-field WEP and time dilation as retained corollaries on that gravity
  surface
- restricted strong-field gravity closure on the current star-supported
  finite-rank class under the exact static conformal bridge
- direct-universal exact global Lorentzian Einstein/Regge stationary action
  family on discrete `3+1` spacetime `PL S^3 x R`
- exact UV-finite partition-density family on the same discrete `3+1` route,
  with mean/stationary sector equal to that Einstein/Regge family
  - authority: [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](../../UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md)
- exact canonical geometric barycentric-dyadic refinement net for that same
  discrete partition-density and stationary-section family
  - authority: [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](../../UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md)
- exact inverse-limit Gaussian cylinder closure for that same canonical
  discrete QG family
  - authority: [UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md](../../UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md)
- exact abstract Gaussian / Cameron-Martin completion for that same canonical
  discrete QG family
  - authority: [UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md](../../UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md)
- exact project-native PL field realization for that same canonical discrete
  QG family
  - authority: [UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md)
- exact project-native PL weak/Dirichlet-form closure for that same canonical
  discrete QG family
  - authority: [UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md](../../UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md)
- exact project-native PL `H^1`-type Sobolev interface for that same canonical
  discrete QG family
  - authority: [UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md)
- exact external FE/Galerkin smooth weak-field and Gaussian measure
  equivalence for that same canonical discrete QG family
  - authority: [UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md)
- exact canonical textbook weak/measure equivalence for that same canonical
  discrete QG family
  - authority: [UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md)
- exact smooth local gravitational weak/Gaussian identification on the
  positive-background class
  - authority: [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md)
- exact smooth finite-atlas gravitational stationary-family identification on
  the chosen smooth realization
  - authority: [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md)
- exact smooth global weak gravitational stationary/Gaussian solution class on
  the chosen smooth realization
  - authority: [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md)
- exact canonical smooth gravitational weak/measure equivalence on the chosen
  smooth realization
  - authority: [UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md)
- exact canonical smooth geometric/action equivalence on the chosen smooth
  realization
  - authority: [UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md)
- exact canonical textbook Einstein-Hilbert-style geometric/action
  equivalence on the chosen smooth realization
  - authority: [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md)
- exact canonical textbook continuum gravitational weak/stationary action
  family on the chosen smooth realization
  - authority: [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md)
- exact native `Cl(3)` / `SU(2)`
- graph-first structural `SU(3)`
- exact `T = 0` confinement of the graph-first `SU(3)` gauge sector, with
  bounded `sqrt(sigma) ≈ 465 MeV`
- anomaly-forced `3+1`
- electroweak hierarchy / `v`
- retained `S^3` compactification / topology closure
- full-framework one-generation closure
- three-generation matter structure in the framework
  via the physical-lattice / no-rooting boundary and anomaly-forced
  full-framework chirality
- exact `I_3 = 0` theorem on the Hilbert surface
- exact CPT theorem on the free staggered lattice
- emergent Lorentz invariance with first anisotropic correction at dimension 6 and unique cubic-harmonic `\ell = 4` signature; on the retained hierarchy surface the correction is `(E/M_{Pl})^2` suppressed
- exact strong CP / `theta_eff = 0` theorem on the retained axiom-determined action surface

Reviewer-facing framing notes:

- the gravity capstone is full discrete `3+1` GR on the project route; do not
  silently upgrade that to an unqualified continuum-GR claim.
- the QG bridge now also has its canonical textbook weak/measure closure,
  smooth local gravitational identification, finite-atlas smooth gravitational
  patching, smooth global weak/Gaussian solution class, canonical smooth
  weak/measure equivalence, canonical smooth geometric/action equivalence,
  canonical textbook Einstein-Hilbert-style geometric/action equivalence, and
  canonical textbook continuum gravitational closure on the chosen
  realization.
- there is no remaining theorem gap on the chosen canonical textbook
  continuum target.
- the package-level gravity/gauge continuum positioning note is
  [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md):
  gravity is exact on the chosen canonical textbook target, while the gauge
  side is positioned through the structural `SU(3)` / Wilson / `alpha_s` /
  universality-EFT bridge rather than a parallel 19-step theorem chain.
- optional comparison against alternative textbook packaging conventions is
  collected separately in
  [UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md](../../UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md)
  and is packaging-only.

Bounded prediction surface:

- DM ratio `R = 5.48` vs `5.47`
- zero-import `\alpha_s(M_Z) = 0.1181`
- bounded top package:
  `y_t(v) = 0.9176`,
  `m_t(pole) = 172.57 GeV` (2-loop),
  `173.10 GeV` (3-loop),
  with the current `~3%` QFP/RGE-surrogate systematic
- promoted CKM atlas/axiom closure package with full sharp `|V_us|`, `|V_cb|`, `|V_ub|`, `\delta`, and `J`, no quark-mass or fitted CKM observables in the derivation, and canonical CMT `\alpha_s(v)` as the quantitative coupling input
- cosmology companions such as `\Omega_\Lambda`, `n_s`, `w = -1`
- sharp bounded secondary predictions already on `main`:
  proton lifetime, CKM neutron EDM, vacuum critical stability,
  benchmark gravitational decoherence
- Higgs and other bounded secondary lanes

Live high-impact gates:

1. DM relic mapping
