# CI(3) / Z^3 Publication Retain Audit

**Date:** 2026-04-12  
**Branch:** `codex/review-active`  
**Scope:** publication-facing review of the `CI(3)` / `Z^3` lane against the
current `main` retention bar.

## Verdict

No broad `CI(3)` / `Z^3` promotion wave should go to `main` in this pass.

One bounded sub-lane is now retained on `main`:

- `docs/BOUNDED_NATIVE_GAUGE_NOTE.md`
- `scripts/frontier_non_abelian_gauge.py`

That promotion is intentionally narrow:

- retained: exact native cubic `Cl(3)` / `SU(2)` algebra
- explicit open: native cubic `SU(3)`
- not promoted: generations, dark matter, Higgs, cosmology, neutrino fits, or
  strong-field phenomenology

The lane is not blocked by lack of activity; it is blocked by claim hygiene:

- the algebraic core and the phenomenology layer are currently mixed together
- the strongest `SU(3)` / generations notes overstate what the scripts actually
  establish
- several phenomenology runners claim prediction while hard-coding observed
  values, Standard Model couplings, or matching conventions
- the cosmology and strong-field notes are still exploratory or toy-surface
  extrapolations, not retained closure artifacts

## What Is Closest To Retainable

### 1. Native cubic gauge / taste audit, after narrowing

Files:

- `docs/NON_ABELIAN_GAUGE_NOTE.md`
- `scripts/frontier_non_abelian_gauge.py`

Safe reading:

- native cubic staggered structure gives exact `Cl(3)` / `SU(2)` content
- native cubic `SU(3)` is still negative or incomplete on the audited surface

Current status:

- this bounded note is now on `main`
- it is the canonical retained entrypoint for the native gauge lane

### 2. Taste-orbit algebra, after stripping physical-generation language

Files:

- `docs/GENERATIONS_RIGOROUS_NOTE.md`
- `docs/GENERATIONS_WEAKNESS_ANALYSIS_NOTE.md`
- `docs/WILSON_BREAKS_EVERYTHING_NOTE.md`
- `scripts/frontier_generations_rigorous.py`
- `scripts/frontier_generations_weakness_analysis.py`
- `scripts/frontier_su3_generations.py`
- `scripts/frontier_wilson_breaks_everything.py`

Safe reading:

- exact orbit structure `8 = 1 + 1 + 3 + 3` under the audited `Z_3` action
- the orbit theorem itself is real
- Wilson deformation does track the fragility of the same taste structure

Why not yet on `main`:

- the current notes jump from orbit structure to “three physical generations”
  without clearing the taste-physicality / regulator objection
- the adversarial note itself explains that the physical content is conditional
  on treating tastes as fundamental degrees of freedom

Required rework:

- split the claim in two:
  - retained algebraic result: exact orbit structure on the cubic taste space
  - explicit hold: physical generations require taste physicality as a named
    axiom or separate closure argument

## Post-Audit Arrivals On `review-active`

These arrived after the first publication audit and do **not** change the
current promotion decision.

### 2a. Review thread summary is not the retention authority

Files:

- `docs/REVIEW_THREAD_SUMMARY_2026-04-12.md`

Current read:

- useful branch-local synthesis memo
- materially overstates the closure status of the native-cubic `SU(3)` lane and
  the frozen-stars / strong-field lane

Why not on `main`:

- promotion decisions are governed by this retain audit, not by a branch memo
- several "CLOSED" labels in the summary conflict with the audited scripts and
  the narrower hold surface recorded below

Required rework:

- keep the summary explicitly subordinate to this audit
- do not use it as manuscript or control-plane truth until its status labels
  are aligned with the retained claim boundaries

### 3. `SU(3)` commutant note does not close native cubic `SU(3)`

Files:

- `docs/SU3_COMMUTANT_NOTE.md`
- `scripts/frontier_su3_commutant.py`

Current read:

- the mathematically interesting result is a commutant statement for
  `SU(2)` on one tensor factor plus a discrete `SWAP_23` symmetry, yielding a
  `gl(3) + gl(1)` decomposition
- the script itself also shows that the **full** `Cl(3)` commutant is too
  small (`dim = 8`) to give `su(3) + u(1)`

Why not on `main`:

- this does not repair the original native-cubic `SU(3)` claim
- `SWAP_23` is indeed a real cubic lattice symmetry, so the issue is **not**
  that an unphysical operator was imported from outside the lattice
- the unresolved step is subtler: the current derivation uses the residual
  cubic exchange symmetry that preserves a chosen `SU(2)` factorization, and
  the note does not yet show that this weak-preserving `3+1` split is forced
  canonically and basis-independently by the retained cubic construction
- as written, the result is a correct commutant theorem for
  `SU(2)_weak + SWAP_23`, but it is not yet a closed derivation of
  native-cubic `SU(3)` from the full `Cl(3) on Z^3` lane

Required rework:

- reframe as a bounded algebraic side result:
  “given the derived `SU(2)` factorization and the compatible residual cubic
  exchange `SWAP_23`, the commutant has a
  `3+1` structure”
- if the goal is promotion beyond that, prove that the residual symmetry and
  the resulting `3+1` decomposition are intrinsic to the lattice construction
  rather than representation-level choices
- until then, do not present it as closure of the original
  `Cl(3) on Z^3 => SU(3)` claim

### 4. `SU(3)` dynamical-selection note strengthens the case, but does not close it

Files:

- `docs/SU3_DYNAMICAL_SELECTION_NOTE.md`
- `scripts/frontier_su3_dynamical_selection.py`

Current read:

- useful stress-test against the original hand-embedding objection
- still relies on inserted taste-breaking coefficients and small-volume
  weak-coupling diagnostics

Why not on `main`:

- the triplet/singlet splitting is not computed from the retained cubic lane
  itself; it is modeled via imported `O(a^2)` taste-breaking parameters
- the confinement section is explicitly only partial on a small weak-coupling
  lattice

Required rework:

- keep as a review-only strengthening note unless the taste-breaking operator
  is derived on the retained cubic surface rather than prescribed

### 4a. `SU(3)` basis-independence note narrows the presentation objection, but
still does not close native cubic `SU(3)`

Files:

- `docs/SU3_BASIS_INDEPENDENCE_NOTE.md`
- `scripts/frontier_su3_basis_independence.py`

Current read:

- this is a real improvement over the earlier commutant lane
- it shows that the `SU(2) + SWAP` commutant result is stable across:
  - several faithful `Cl(3)` representations
  - all three tensor-factor choices
  - unitary conjugation of the chosen setup
- this substantially weakens the earlier “mere first-factor presentation”
  objection

Why not on `main`:

- the script still defines the residual `SWAP` by hand relative to a chosen
  weak factor, then checks stability under that construction
- the random-conjugation tests conjugate `SWAP` together with `SU(2)`, which
  shows isomorphism invariance of the chosen setup, but does not independently
  derive the residual symmetry from the retained lattice construction
- the remaining canonicality gap is now narrower but still real:
  the note does not yet prove that the weak-preserving residual cubic symmetry
  is selected intrinsically from the lattice, nor that the surviving abelian
  factor deserves the hypercharge interpretation without extra input

Required rework:

- keep off `main`
- use it as a strengthening note for the paper draft if needed, but do not
  upgrade the retained claim past:
  “the commutant theorem is robust across admissible representations and weak
  axis choices”
- to close the lane, derive the residual symmetry canonically from the lattice
  stabilizer of the derived weak sector and separately justify the physical
  identification of the surviving `u(1)`

### 4b. Formal `SU(3)` theorem now fixes the old verifier mismatch, but changes
the claim surface

Files:

- `docs/SU3_FORMAL_THEOREM_NOTE.md`
- `scripts/frontier_su3_formal_theorem.py`
- `docs/HYPERCHARGE_IDENTIFICATION_NOTE.md`
- `scripts/frontier_hypercharge_identification.py`

Current read:

- the old explicit-construction mismatch is resolved: the rewritten verifier now
  passes `106/106`
- the audited positive is now a strong commutant theorem on the
  Kawamoto-Smit tensor product surface:
  - choose a distinguished spatial direction
  - let `su(2)` act on the corresponding `C^2` factor
  - let `SWAP` act on the two remaining factors
  - then `Comm{su(2), SWAP}` has compact semisimple part `su(3)`
- that is a real and much stronger result than the older hand-embedding lane

Why not on `main`:

- the rewritten theorem no longer derives the weak `su(2)` from the retained
  `Cl(3)` / bivector lane
- the verifier explicitly records that `T_2` and `T_3` are **not** in `Cl(3)`;
  they are canonical from the KS tensor decomposition, but they are not the old
  derived bivector generators
- so the current theorem closes:
  “KS tensor-factor `su(2)` plus residual swap symmetry gives `su(3)`”
  but it still does not close the stronger retained claim:
  “native cubic `Cl(3)` alone derives the full nonabelian gauge sector”
- the hypercharge companion is also narrower than its headline:
  the left-handed doublet sector gives the right `Y` eigenvalue ratio and
  charge formula, but the script itself shows the `U(1)^3` anomaly is nonzero
  on that surface, so anomaly freedom is not what fixes the identification here

Required rework:

- keep this off `main` for now
- paper-safe wording at this stage is:
  “within the KS tensor-factor realization of `Cl(3)` on `Z^3`, a distinguished
  factor `su(2)` together with the residual cubic swap has commutant
  `su(3) ⊕ u(1)`”
- to close the stronger lane, either:
  - bridge the retained bivector `su(2)` to this factor `su(2)` canonically, or
  - explicitly narrow the publication claim away from “`Cl(3)` alone”
- keep the hypercharge note conditional on the commutant theorem and rewrite
  its uniqueness claim around tracelessness / charge matching, not anomaly
  cancellation

### 5. Neutrino masses are a downstream phenomenology fit, not retained closure

Files:

- `docs/NEUTRINO_MASSES_NOTE.md`
- `scripts/frontier_neutrino_masses.py`

Current read:

- interesting speculative seesaw / `Z_3` selection-rule exercise
- multiple observables are obtained by best-fit scans over free structural and
  breaking parameters

Why not on `main`:

- the runner fits or targets experimental mass ratios, mixing angles, and
  cosmological bounds
- the note itself acknowledges tuned breaking parameters and tensions

Required rework:

- keep off `main`
- if reopened, rewrite as a bounded phenomenology note with explicit “fit, not
  derivation” language

### 5b. Top Yukawa from `alpha_s` is still a constrained phenomenology lane,
not a closed derivation

Files:

- `docs/YT_FROM_ALPHA_S_NOTE.md`
- `scripts/frontier_yt_from_alpha_s.py`

Current read:

- the lane is useful because it narrows the size of the remaining freedom in
  `y_t`
- the script finds a trace-identity candidate `y_t = g_s / sqrt(6)` and,
  after 1-loop RG running, gets `m_t = 178.8 GeV`, which is `+3.4%` high

Why not on `main`:

- the runner itself finishes with `8 PASS / 1 FAIL`
- its own summary says the exact Clebsch-Gordan coefficient is **not** uniquely
  determined yet
- the script compares multiple competing normalizations (`sqrt(6)`, `sqrt(7)`,
  bare vs unified coupling) and explicitly notes that the “best” coefficient is
  still unresolved
- so this is not a retained prediction from `Cl(3)`; it is a promising
  constraint lane with an unresolved operator-identification problem

Required rework:

- keep off `main`
- rewrite as: “`Cl(3)` constrains `y_t` to be `O(g)` with a coefficient near
  the observed value, but the exact trace-identity coefficient remains open”
- do not call this “the last free parameter removed” unless the operator choice
  and coupling normalization are fixed from the retained cubic lane

### 5a. Complex `Z_3` breaking still strengthens the fit, not the derivation

Files:

- `docs/NEUTRINO_COMPLEX_Z3_NOTE.md`
- `scripts/frontier_neutrino_complex_z3.py`

Current read:

- useful extension of the earlier neutrino fit because it relaxes the real
  `Z_3`-breaking restriction and improves the `\delta_CP` / `\Sigma m_i`
  tensions
- the complex phase story is physically suggestive and better motivated than
  the earlier purely real-breaking lane

Why not on `main`:

- the core runner is still a multi-parameter fit against measured
  `\theta_{12}`, `\theta_{23}`, `\theta_{13}`, `\delta_CP`,
  `\Delta m^2_{31}/\Delta m^2_{21}`, and the cosmological neutrino-mass bound
- the “resolved within systematics” language depends on experimental hints and
  an explicit tolerance to the cosmological bound
- this is still phenomenology matching, not a retained first-principles
  derivation from the cubic lane

Required rework:

- keep it off `main`
- if reused for publication, relabel as a bounded phenomenology-fit note and
  separate the algebraic motivation for complex breaking from the fitted
  numerical closure claims

### 5b. Electroweak phase transition lane is stronger, but still not
first-principles closure

Files:

- `docs/EWPT_STRENGTH_NOTE.md`
- `scripts/frontier_ewpt_strength.py`
- `docs/EWPT_LATTICE_MC_NOTE.md`
- `scripts/frontier_ewpt_lattice_mc.py`

Current read:

- `EWPT_STRENGTH` is a reasonable scenario/analogy note: extra bosons of the
  right order strengthen the transition, and 2HDM/xSM literature is relevant
- `EWPT_LATTICE_MC` improves on that by actually running a scalar 3D Monte
  Carlo instead of stopping at perturbation theory

Why not on `main`:

- the taste-scalar mass scale is still injected (`m_S = 80 GeV`) rather than
  derived from the retained cubic lane
- the scalar-only Monte Carlo gives the central value `v/T ~ 0.49`, which is
  borderline on its own
- the headline `v/T ~ 0.73` result multiplies the scalar MC by a literature
  enhancement factor `R_gauge = 1.5` rather than computing the gauge-field
  sector in the same simulation
- this makes the lane useful and much stronger than before, but still not a
  retained first-principles electroweak/baryogenesis closure

Required rework:

- keep both notes off `main`
- if reopened, write one bounded note that clearly separates:
  - scalar-only MC result on the tested surface
  - literature-anchored gauge enhancement estimate
  - uncomputed full gauge+scalar lattice closure

### 5c. Weinberg-angle threshold correction is still scenario-dependent

Files:

- `docs/WEINBERG_ANGLE_CORRECTION_NOTE.md`
- `scripts/frontier_weinberg_angle_correction.py`

Current read:

- useful correction of the earlier normalization bug
- useful as a reviewer-facing threshold-mechanism exploration showing the
  taste spectrum can move the running in the correct direction

Why not on `main`:

- the script’s taste-partner assignments are explicitly model-dependent,
  especially for leptons, where the note itself runs into colored-exotic
  partner ambiguity
- the best numerical match uses a fixed `alpha_U` from the SM-only
  extrapolation, while the self-consistent `alpha_U` section reopens the gap
  and pushes the result back toward the bad `0.176` baseline
- this is therefore not a closed prediction of `\sin^2\theta_W`, only a
  threshold-correction scenario study

Required rework:

- keep it off `main`
- reduce it to a bounded threshold-correction memo unless the taste-partner
  representation content and self-consistent unified coupling are both derived
  from the retained lane

### 6. Revised frozen-stars runner is still not retention-ready

Files:

- `docs/FROZEN_STARS_RIGOROUS_NOTE.md`
- `scripts/frontier_frozen_stars_rigorous.py`

Current read:

- stronger than the original 1D-only toy because it adds a sparse 3D Hartree
  surface and analytical scaling arguments
- still a strong-field exploratory runner, not a retained compact-object card

Why not on `main`:

- the astrophysical interpretation still outruns the audited numerical surface
- there is still no bounded note freezing the exact claim boundary for the new
  script

Required rework:

- write a bounded note first
- keep any claim at the level of “lattice self-gravity resists collapse on the
  tested Hartree surfaces,” not echo/Kerr/astrophysical phenomenology

## Explicit Holds

### A. `SU(3)` from `Cl(3)` on `Z^3` is not retained

Files:

- `docs/ULTIMATE_SIMPLIFICATION_NOTE.md`
- `docs/COMPLETE_DERIVATION_CHAIN_2026-04-12.md`
- `docs/REVOLUTIONARY_IMPLICATIONS_NOTE.md`
- `docs/SU3_COMMUTANT_NOTE.md`
- `docs/SU3_BASIS_INDEPENDENCE_NOTE.md`
- `docs/SU3_DYNAMICAL_SELECTION_NOTE.md`
- `scripts/frontier_ultimate_simplification.py`
- `scripts/frontier_su3_commutant.py`
- `scripts/frontier_su3_dynamical_selection.py`

Why held:

- the script constructs `SU(3)` by choosing 3 basis states from a 4-dimensional
  subspace and embedding the standard Gell-Mann matrices into that chosen
  subspace
- that is a compatible embedding, not an emergent native-cubic derivation
- the later narrative notes promote that embedding to “everything from Cl(3) on
  Z^3”, which is stronger than the audited code supports
- the newer commutant note changes the claim to `SU(2) + SWAP_23 -> su(3)+u(1)`,
  which is mathematically interesting but is **not** the same as native cubic
  `SU(3)` emergence from full `Cl(3)`
- the newer basis-independence note shows that the `SU(2) + SWAP` commutant
  theorem is robust across several representations and weak-axis choices, but
  it still does not independently derive the residual symmetry or the
  hypercharge interpretation from the retained lane
- the newer dynamical-selection note still depends on modeled taste-breaking
  coefficients and partial small-volume controls

What must be redone:

- either derive the triplet subspace from a graph- or algebra-selected
  criterion with no hand-picked 3-of-4 choice
- or downgrade the lane to: “the cubic taste algebra contains a compatible
  `SU(3)` embedding, but native `SU(3)` emergence remains open”

### B. Dark matter / `alpha_s` / annihilation ratio are not retained predictions

Files:

- `docs/ALPHA_S_DETERMINATION_NOTE.md`
- `docs/DM_RATIO_SOMMERFELD_NOTE.md`
- `docs/ANNIHILATION_RATIO_NOTE.md`
- `docs/DARK_MATTER_CLOSURE_NOTE.md`
- `docs/DARK_MATTER_SINGLETS_NOTE.md`
- `scripts/frontier_alpha_s_determination.py`
- `scripts/frontier_dm_ratio_sommerfeld.py`
- `scripts/frontier_annihilation_ratio.py`
- `scripts/frontier_dark_matter_closure.py`

Why held:

- the `alpha_s` runner hard-codes `g = 1`, PDG `alpha_s(M_Z)`, observed
  `Omega_DM/Omega_B`, and uses root-finding against the observed ratio
- the Sommerfeld runner hard-codes observed abundance values and freeze-out
  parameters
- the closure notes are often honest in the body, but the surrounding lane
  language still drifts toward “prediction”

What must be redone:

- keep only a bounded consistency-window note unless the coupling is derived
  without matching to the observed dark-matter ratio

### C. Higgs / mass spectrum / hierarchy are not first-principles closures

Files:

- `docs/HIGGS_MECHANISM_NOTE.md`
- `docs/HIGGS_MASS_NOTE.md`
- `docs/MASS_SPECTRUM_NOTE.md`
- `docs/MASS_HIERARCHY_RG_NOTE.md`
- `scripts/frontier_higgs_mechanism.py`
- `scripts/frontier_higgs_mass.py`
- `scripts/frontier_mass_spectrum.py`
- `scripts/frontier_mass_hierarchy_rg.py`

Why held:

- the Higgs mechanism note explicitly says the Higgs doublet quantum numbers
  and Yukawas are still missing
- the Higgs mass runner uses Standard Model weak-scale couplings and masses
- the hierarchy runner uses assumed `alpha_s` values and proxy gauge dynamics

What must be redone:

- either reduce this lane to “phenomenology consistency probes”
- or derive the electroweak representation content and couplings from retained
  cubic/taste structure first

### D. Cosmological constant / `Omega_Lambda` lane is not predictive

Files:

- `docs/OMEGA_LAMBDA_NOTE.md`
- `docs/CC_VALUE_NOTE.md`
- `docs/CC_FACTOR15_NOTE.md`
- `docs/UV_IR_COSMOLOGICAL_NOTE.md`
- `scripts/frontier_omega_lambda_derivation.py`
- `scripts/frontier_cc_value.py`
- `scripts/frontier_cc_factor15.py`
- `scripts/frontier_uv_ir_cosmological.py`

Why held:

- the `Omega_Lambda` runner hard-codes observed cosmology and explicitly frames
  itself as an honest negative
- the `CC_VALUE` and `CC_FACTOR15` lanes use observed `H_0` and
  `Omega_Lambda`
- the best current safe reading is reformulation / scaling structure, not a
  numerical cosmological-constant prediction

What must be redone:

- retain only a reformulation note unless `Omega_Lambda` is derived without
  feeding observed `Omega_Lambda` back into the argument

### E. Frozen stars / strong-field / prediction cards are exploratory

Files:

- `docs/FROZEN_STARS_NOTE.md`
- `docs/STRONG_FIELD_GR_NOTE.md`
- `docs/STRONG_FIELD_REGIME_NOTE.md`
- `docs/ACCESSIBLE_PREDICTION_NOTE.md`
- `docs/FROZEN_STARS_RIGOROUS_NOTE.md`
- `scripts/frontier_frozen_stars.py`
- `scripts/frontier_frozen_stars_rigorous.py`
- `scripts/frontier_strong_field_gr.py`
- `scripts/frontier_strong_field_regime.py`
- `scripts/frontier_accessible_prediction.py`

Why held:

- the frozen-stars runner is a 1D Hartree toy solver that is later interpreted
  as 3D compact-object phenomenology
- the revised “rigorous” runner adds analytical scaling and a sparse 3D Hartree
  surface, but still does not freeze a bounded astrophysical claim
- the strong-field note itself does not close horizon, Kerr, ringdown, or
  post-Newtonian structure
- the accessible-prediction lane is a memo/proposal card, not a result

What must be redone:

- no retention until a genuine 3D strong-field surface exists and the
  observables are derived on that surface rather than extrapolated from a 1D toy

### F. Echo search remains an active strong-field hold

Files:

- `docs/GW150914_ECHO_SEARCH_NOTE.md`
- `scripts/gw150914_echo_search.py`
- `scripts/gw150914_echo_definitive.py`
- `scripts/gw_echo_matched_filter.py`

Why held:

- the current pipelines are still in motion and are not yet a frozen
  publication-grade detection stack
- earlier search variants excluded the first predicted echo by construction
  through delayed post-merger windows
- the current “consistent with prediction” language is too strong until the
  pipeline includes the first predicted echo directly, has injection-calibrated
  false-alarm control, and freezes the tested template family

What must be redone:

- keep the entire echo lane on `review-active`
- no promotion until there is:
  - one frozen search window / template definition
  - direct inclusion of the first predicted echo
  - injection-calibrated significance and trials accounting

## Reviewer-Facing Memos, Not Retained Science

These are useful and should stay on `review-active`, but they are not promotion
targets for `main`:

- `docs/AXIOM_REDUCTION_NOTE.md`
- `docs/NOVELTY_LITERATURE_SEARCH_NOTE.md`
- `docs/BEYOND_LATTICE_QCD_NOTE.md`
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md`

## Main-Organization Recommendation

For the `CI(3)` / `Z^3` paper lane, `main` should not yet receive the current
review-active notes as written.

The next clean publication shape is:

1. one bounded algebra note for exact cubic `Cl(3)` / native `SU(2)`
2. one bounded taste-orbit note for `8 = 1 + 1 + 3 + 3`, explicitly marked
   algebraic and conditional
3. one negative/boundary note stating native cubic `SU(3)` is not yet closed
4. everything else stays on review until it is either:
   - downgraded to a consistency/proxy note, or
   - rebuilt without observational back-substitution

## Current Promotion Decision

`main` promotions from the `CI(3)` / `Z^3` cluster in this pass: **none**

Reason:

- the core algebraic story is not yet written in a form that is both honest and
  internally consistent with the audited code
- promoting the current notes would make `main` less trustworthy, not more
