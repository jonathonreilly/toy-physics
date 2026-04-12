# CI(3) / Z^3 Publication Retain Audit

**Date:** 2026-04-12  
**Branch:** `codex/review-active`  
**Scope:** publication-facing review of the `CI(3)` / `Z^3` lane against the
current `main` retention bar.

## Verdict

No broad `CI(3)` / `Z^3` promotion wave should go to `main` in this pass.

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

Why not yet on `main`:

- the note currently sits beside later notes that claim native cubic `SU(3)`
  closure, so promoting it alone would leave the lane internally contradictory

Required rework:

- write a fresh bounded note that explicitly freezes the current honest read:
  `SU(2)` native positive, `SU(3)` native cubic not closed

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
- it introduces a new extra symmetry/identification layer rather than deriving
  `SU(3)` from the original `Cl(3)` lane

Required rework:

- reframe as a bounded algebraic side result:
  “with added `SU(2)` factorization plus `SWAP_23`, the commutant has a
  `3+1` structure”
- do not present it as closure of the original `Cl(3) on Z^3 => SU(3)` claim

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

### 6. Revised frozen-stars runner is still not retention-ready

Files:

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
