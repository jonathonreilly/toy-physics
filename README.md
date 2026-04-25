# Cl(3)/Z^3 Physics Framework

This repository contains the public scientific package for a one-axiom
discrete-physics program based on `Cl(3)` on `Z^3`.

If you are coming from the paper, use the publication package rather than the
full repository chronology. The public package is now organized around four
questions:

- what the current package claims
- what it already predicts
- how to validate and reproduce the active package
- how the science is organized by domain

## Read First

1. [Public arXiv draft](docs/publication/ci3_z3/ARXIV_DRAFT.md)
2. [Prediction surface](docs/publication/ci3_z3/PREDICTION_SURFACE_2026-04-15.md)
3. [Quantitative summary table](docs/publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE.md)
4. [Reproduce guide](docs/publication/ci3_z3/REPRODUCE.md)
5. [Publication package README](docs/publication/ci3_z3/README.md)
6. [Manuscript claims surface](docs/publication/ci3_z3/CLAIMS_TABLE.md)
7. [Science map by domain](docs/publication/ci3_z3/SCIENCE_MAP.md)
8. [Inputs and qualifiers](docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md)
9. [What this paper does not claim](docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
10. [Derivation / validation map](docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md)
11. [Derivation atlas](docs/publication/ci3_z3/DERIVATION_ATLAS.md)

## What Is Already Predicted

- retained quantitative package:
  canonical `v = 246.282818290129 GeV`, retained `alpha_s(M_Z) = 0.1181`,
  the retained coupling-chain identity `alpha_LM^2 = alpha_bare alpha_s(v)`,
  electroweak normalization, retained top/Yukawa transport, promoted CKM
  atlas/axiom numerics including `lambda^2 = alpha_s(v)/2`,
  `A^2 = 2/3`, `cos^2(delta_CKM) = 1/6`, and the rescaled atlas-triangle
  right-angle identity `alpha_0 = 90 deg`; the Thales-pinned
  `alpha_s`-independent ratio class now includes
  `|V_ts|/|V_cb| = 1`, `|V_td|/|V_ub| = sqrt(5)`, and the cross-row
  identity `|V_td V_cb|^2 / |V_ts V_ub|^2 = 5`; the named leading CKM atlas
  identities now include
  `|V_us|_0^2 = alpha_s(v)/2`,
  `|V_ub|_0^2 = alpha_s(v)^3/72`,
  `|V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72`,
  `|V_cd|_0^2 = alpha_s(v)/2`,
  `|V_cs|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^2/6`,
  `|V_cb|_0^2 = alpha_s(v)^2/6`,
  `|V_td|_0^2 = 5 alpha_s(v)^3/72`, and
  `|V_ts|_0^2 = alpha_s(v)^2/6`; the CKM structural-counts packaging theorem
  now isolates the common off-diagonal surface
  `|V_us|_0^2 = alpha_s(v)/n_pair`,
  `|V_cb|_0^2 = |V_ts|_0^2 = alpha_s(v)^2/(n_pair n_color)`,
  `|V_ub|_0^2 = alpha_s(v)^3/(8 n_color^2)`,
  `|V_td|_0^2 = (n_quark-1) alpha_s(v)^3/(8 n_color^2)`,
  making the exact `n_pair` cancellation in `|V_ub|_0^2` explicit; with
  finite-`lambda` standard-matrix corrections guarded separately, plus the
  atlas-leading B_s mixing phase
  `phi_s = -alpha_s(v) sqrt(5)/6 = -0.03850 rad` and the NLO barred-triangle
  protected invariant `gamma_bar = arctan(sqrt(5))` with
  `rho_bar=(4-alpha_s(v))/24`, plus the Thales-mediated cross-system CP ratio
  `phi_s / sin(2 beta_d) = -alpha_s(v)/2` and CP-product estimator
  `alpha_s(v) = (18/5) sin(2 beta_d) sin(2 beta_s)` at atlas-leading order,
  plus the kaon epsilon_K CKM-bracket factorization through atlas `J_0`;
  and bounded
  confinement-string readout; the absolute
  lattice scale is tracked explicitly on a dedicated Planck-scale lane as the
  current package pin `a^(-1) = M_Pl` on the physical-lattice reading, with a
  conditional completion theorem, a source-unit normalization support theorem
  separating bare `G_kernel = 1/(4 pi)` from conditional physical
  `G_Newton,lat = 1`, and a finite-boundary density extension reducing the
  remaining Planck question to the gravitational boundary/action carrier
  identification; finite-response-only and carrier-only parent-source
  shortcuts are retained no-gos, and the simple-fiber Widom entropy-carrier
  class is now closed negatively at `c_Widom <= 1/6`, not `1/4`
- bounded but explicit forward/companion surface:
  neutrino absolute-mass observable bounds, proton lifetime, CKM-only neutron
  EDM continuation, vacuum criticality, taste-scalar near-degeneracy,
  benchmark gravitational decoherence, monopole mass, and bounded atomic
  lattice/scaffold lanes
- exact structural predictions and signatures:
  SM hypercharge uniqueness/electric-charge quantization, fractional-charge
  denominator from `N_c`, `SU(2)` Witten global-anomaly cancellation,
  `SU(3)^3` cubic gauge anomaly cancellation, B-L anomaly freedom as a
  gaugeable option on the retained content,
  emergent-Lorentz dimension-6 onset plus exact continuum-limit 1+1D / 3+1D
  boost-covariant free-scalar 2-point closure and fixed-`H_lat` unitary-kernel
  closure, action-surface `theta_eff = 0`, and the source-scoped vanishing of
  all theta-induced EDM response components
- remaining open flagship bridge package:
  charged-lepton Koide (`Q = 2/3`, `delta = 2/9`);
  the dark-matter exact-target package is already closed on the manuscript
  surface

## Repository Map

- manuscript and package entry surfaces:
  [docs/publication/ci3_z3](docs/publication/ci3_z3/README.md)
- science organized by domain:
  [docs/publication/ci3_z3/SCIENCE_MAP.md](docs/publication/ci3_z3/SCIENCE_MAP.md)
- methodology and AI-accountability lane:
  [docs/ai_methodology/README.md](docs/ai_methodology/README.md)
- reproduction and validation:
  [docs/publication/ci3_z3/REPRODUCE.md](docs/publication/ci3_z3/REPRODUCE.md)
- quantitative derivations and supporting theorem notes:
  [docs/START_HERE.md](docs/START_HERE.md)
- accepted frontier-lane planning note:
  [docs/FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md](docs/FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md)
- scientific boundaries and explicit non-claims:
  [docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md](docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md)
  and [docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)

## Scientific Areas

- spacetime, gravity, and quantum gravity
- gauge structure, matter structure, and strong CP
- quantitative electroweak, QCD, Yukawa, and Higgs lanes
- flavor, CKM, quark, and charged-lepton packages
- neutrino and dark-matter packages
- cosmology and companion phenomenology
- Planck-scale absolute-scale lane and derivation program
- frontier extension planning: teleportation, chronology protection, and
  signed gravitational response

## Scientific Scope

- exact discrete backbone:
  weak-field gravity, restricted strong-field closure, full discrete `3+1`
  GR, chosen-target QG/continuum closure, graph-first `SU(3)`,
  anomaly-forced `3+1`, retained three-generation structure with exact
  SM hypercharge uniqueness/electric-charge quantization, fractional-charge
  denominator from `N_c`, `SU(2)` Witten global-anomaly cancellation,
  `SU(3)^3` cubic gauge anomaly cancellation, B-L anomaly freedom as a
  gaugeable option, and exact taste-cube /
  residual-symmetry flavor support, exact `I_3 = 0`, exact CPT,
  retained Bell/CHSH support on explicit two-species lattice systems,
  emergent Lorentz invariance plus exact continuum-limit 1+1D / 3+1D
  boost-covariant free-scalar 2-point closure and fixed-`H_lat` unitary-kernel
  closure, retained strong-CP closure on the retained
  action surface, exact `T = 0` confinement with bounded `sqrt(sigma)`, and
  retained discrete evanescent-barrier and Schwarzschild-interior support,
  plus retained/admitted cosmology identities including `w = -1`, exact
  `R_base = 31/9` group-theory support for the bounded DM/cosmology cascade,
  a bounded freeze-out-bypass eta support route with candidate
  `m_DM = N_sites * v = 16 * v`, an honest SU(3) one-loop obstruction note
  on the simplest `8/3` enhancement route,
  the FRW kinematic reduction to the open `H_inf/H_0` ratio, the
  matter-radiation equality identity `1 + z_mr = Omega_m,0/Omega_r,0`, and
  the retained active-neutrino-count support `N_eff = 3 + 0.046 = 3.046`
  after the standard thermal correction, and the retained scalar, vector, and
  TT compactness spectral towers on `S^3`, including their pure-`Lambda`
  bridge with `m_TT(2)/m_vec(1) = sqrt(3)` as a structural ratio only
- retained quantitative lanes:
  canonical `v = 246.282818290129 GeV`, retained `alpha_s(M_Z) = 0.1181`,
  retained `alpha_LM` geometric-mean coupling identity, retained EW
  normalization, promoted CKM atlas/axiom closure, bounded Yukawa/top
  transport, and bounded Higgs/vacuum closure
- charged-lepton package:
  substantial Koide support stack; the latest native zero-section review
  pointed-origin exhaustion theorem, and objection-closure review reject full
  dimensionless closure. The April 25 criterion theorem lands the exact
  background-zero / `Z`-erasure algebra for `Q` while leaving physical
  source-free reduced-carrier selection open, plus a selected-line local
  boundary-source and based-endpoint theorem for `delta`
- dark-matter package:
  closed for the exact PMNS-target formulation treated in the manuscript,
  including the source-selection and ordered-current closure chain, with the
  stronger target-free global uniqueness question left out of scope
- bounded companion lanes:
  quark review/support packet, proton lifetime, neutron EDM, down-type
  flavor-mass CKM-dual ratios, vacuum critical stability, benchmark
  gravitational decoherence, compact-object companions, and bounded cosmology

## Scientific Boundaries

- package boundary:
  [docs/MINIMAL_AXIOMS_2026-04-11.md](docs/MINIMAL_AXIOMS_2026-04-11.md)
- one-axiom reduction context:
  [docs/SINGLE_AXIOM_INFORMATION_NOTE.md](docs/SINGLE_AXIOM_INFORMATION_NOTE.md)
  and [docs/SINGLE_AXIOM_HILBERT_NOTE.md](docs/SINGLE_AXIOM_HILBERT_NOTE.md)
- package limits and explicit non-claims:
  [docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
