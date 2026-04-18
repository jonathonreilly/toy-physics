# Claim Surface Status Audit

**Date:** 2026-04-15  
**Purpose:** record what the repo actually supports before any claim narrowing
or manuscript demotion work

This note is an audit, not a claim rewrite. It distinguishes:

1. pure repo/front-door drift that can be fixed immediately;
2. live rows that are already clean enough;
3. live rows whose current public wording is stronger than the exact support
   presently carried by the repo.

## Resolved Repo Drift

These were real repo hygiene problems. They are now fixed on `main`.

### 1. One axiom versus five inputs

The repo had drifted into presenting two different counts as if they were
competing foundation stories.

What is now explicit:

- the accepted package statement is `Cl(3)` on `Z^3` as the physical theory
- [MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md) is the
  operational package-boundary memo used to audit the current implementation
  surface
- the one-axiom notes
  [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md)
  and
  [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md)
  are optional reduction/support notes for framework compression and
  physical-lattice scoping

Affected front-door files were updated directly.

### 2. Continuum-identification Lorentz drift

[CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md) had
still been saying that emergent Lorentz invariance was not yet established,
even though Lorentz had already been promoted on `main`.

That was stale wording, not a theorem gap. It is now fixed.

### 3. CKM atlas/axiom package scoping

The repo had drifted into mixing a real promoted quantitative package with
broader public labels like `closed / derived`.

What is now explicit:

- the live authority is the promoted CKM atlas/axiom package on the canonical
  tensor/projector surface
- public capture-status cells now use `promoted`, while claim-strength rows use
  `promoted quantitative package`
- canonical CMT `alpha_s(v)` is the quantitative coupling input, and the
  package is described via exact atlas counts, the exact `1/6` projector, the
  exact bilinear tensor carrier `K_R`, the exact `Z_3` source, and the exact
  Schur cascade
- older bounded Cabibbo / mass-basis / partial-Jarlskog notes remain route
  history only

Affected front-door and publication-control files were updated directly.

### 4. `\alpha_s` and EW normalization package scoping

The repo had drifted into a stale `retained / derived` split across one public
quantitative row, even though the live control surfaces already treated
`\alpha_s(M_Z)` and the EW normalization package as standalone retained
quantitative lanes with explicit `R_conn` and running-bridge qualifiers.

What is now explicit:

- `\alpha_s(M_Z)` is captured as a retained standalone quantitative lane across
  the public control surfaces
- the EW normalization package remains retained, with the extra derived
  `R_conn = 8/9 + O(1/N_c^4)` support and the retained `M_Z` running bridge
  named explicitly
- the retained EW matching audit is the right place for the `~0.4%–2.9%`
  bridge/matching envelope; the package is not being sold as an exact
  same-surface no-bridge theorem

Affected front-door and publication-control files were updated directly.

### 5. Higgs / top package scoping

The repo had drifted into mixing the now-retained YT/top transport lane with
older pre-retention summary wording, and one manuscript summary table was still
collapsing the retained top lane and the derived Higgs/vacuum lane together as
generic bounded rows.

What is now explicit:

- the YT/top package is a retained quantitative lane on `main`
- the canonical retained downstream top readout is the full-staggered-PT
  `m_t(pole) = 172.57 ± 6.50 GeV`, with explicit through-2-loop retained
  coverage
- the older `173.10 GeV` framework-side 3-loop top number remains a derived
  cross-check, not the controlling top authority row
- the Higgs / vacuum package remains derived, with the retention-decomposed
  budget `m_H = 125.04 ± 3.17 GeV` and the 2-loop support route named
  explicitly

Affected front-door and publication-control files were updated directly.

## Rows That Are Already Clean Enough

These are not current submission blockers at the claim-surface level.

### Confinement

Current package posture is appropriately split:

- exact structural theorem: `T = 0` confinement of the graph-first `SU(3)`
  gauge sector
- bounded quantitative row: `\sqrt{\sigma} \approx 465 MeV`

Authority:

- [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md)
- [frontier_confinement_string_tension.py](../../../scripts/frontier_confinement_string_tension.py)

### Emergent Lorentz invariance

After the continuum-note cleanup, the public package posture is coherent:

- exact structural theorem on the retained hierarchy surface
- retained hierarchy-scale interpretation for the `(E/M_{Pl})^2` suppression

Authority:

- [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
- [frontier_emergent_lorentz_invariance.py](../../../scripts/frontier_emergent_lorentz_invariance.py)

### Cosmology companion lane

Cosmology is already positioned as bounded / conditional companion material,
not as retained flagship core. The main hygiene work there is already done.

Authority:

- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
- [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md)

### Charged-lepton bounded package

The charged-lepton mass-hierarchy / Koide row is now coherently positioned as
a bounded package rather than a retained framework-native derivation.

Current package posture is appropriately explicit:

- retained structural compatibility package on the `hw=1` triplet
- observational three-real PDG pin
- repo status `bounded`
- no spare observable forecast beyond the pin
- no spare forecast and no claim that the framework derives Koide on the
  current surface

Authority:

- [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
- [HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](../../HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)

## Rows That Needed or Still Need Claim-Surface Adjustment

These are the rows where the public wording is currently stronger than the
exact support carried by the repo. No narrowing has been applied here yet; this
section only records the status.

### A. Electroweak hierarchy / `v`

**Current public posture**

- claims-table and manuscript language still say the electroweak scale is not
  an external input on the current paper surface
- front-door files still list retained electroweak hierarchy / `v`

Representative surfaces:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](../../CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)

**What the repo actually supports**

- the minimal hierarchy / selector theorem is real
- the exact minimal-block source-response structure is real
- the quoted numerical `v = 246.282818290129 GeV` now sits on the same
  canonical hierarchy surface used across the public code paths

Primary evidence:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py)
- [frontier_yt_zero_import_chain.py](../../../scripts/frontier_yt_zero_import_chain.py)

**Adjustment class**

- repo cleanup resolved on `main`; no separate `v` inconsistency remains

**Why**

The selector theorem and the pinned numeric value now sit on the same
canonical hierarchy surface.

### B. Gravity / QG paper posture

**Current public posture**

- the theorem chain is real
- the paper/front-door package now state it as exact on the chosen canonical
  textbook target, not as a blanket claim about every continuum realization

Representative surfaces:

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
- [README.md](../../README.md)

**What the repo actually supports**

- exact discrete `3+1` GR on the project route
- exact QG / continuum chain on the chosen canonical textbook target
- careful limitation notes already exist in the authority stack

Primary evidence:

- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
- [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md)
- [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing theorem on the
  retained route

**Why**

The internal notes and the public paper/front-door surfaces now line up: exact
discrete `3+1` GR on the project route, and exact QG / continuum closure on
one chosen canonical textbook target. The remaining work here is optional
presentation hardening, not claim-surface repair.

### C. Strong CP

**Current public posture**

- the live public package now states retained action-surface `\theta_eff = 0`
- the repo no longer presents this as a universal dynamical
  instanton/measure theorem

Representative surfaces:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [README.md](../../README.md)

**What the repo actually supports**

- Leg A: determinant positivity / no phase
- Leg B: CP-even Wilson gauge action
- Leg C: structural absence of a bare `\theta` term from the axiom-determined
  action surface

Primary evidence:

- [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md)
- [frontier_strong_cp_theta_zero.py](../../../scripts/frontier_strong_cp_theta_zero.py)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing theorem on the
  retained action surface

**Why**

Leg C is an exclusion-by-action-surface argument, not a dynamical
instanton-measure suppression theorem. The public wording now reflects that.

### D. CKM

**Current public posture**

- before cleanup, one public quantitative row had been marked `closed / derived`
- the live public package now presents a promoted CKM atlas/axiom package on
  the canonical tensor/projector surface

Representative surfaces:

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)

**What the repo actually supports**

- the current authoritative package is materially cleaner than the older
  Cabibbo / mass-basis / partial-Jarlskog routes
- hierarchy `v` is already demoted to a consistency check inside the promoted
  note
- exact counts / projector / tensor-slot / Schur cascade structure are real
- public numerics still rely on a selected canonical surface and a comparator
  structure that, before the terminology cleanup, was described more
  carelessly than `derived` or `promoted quantitative package`

Primary evidence:

- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [frontier_ckm_atlas_axiom_closure.py](../../../scripts/frontier_ckm_atlas_axiom_closure.py)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing theorem on the
  promoted package route

**Why**

The promoted package is real, but the old flagship wording was broader than
the exact support story needed. The public matrix/front-door rows now present
the package with valid `promoted` / `promoted quantitative package` labels on
the canonical tensor/projector surface.

### E. `\alpha_s` and EW normalization

**Current public posture**

- the live public package now treats `\alpha_s(M_Z)` and the EW normalization
  package as retained standalone quantitative lanes
- the extra `R_conn` support and the retained running bridge are named
  explicitly where they matter

Representative surfaces:

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
- [README.md](../../README.md)

**What the repo actually supports**

- strong standalone lanes
- public-facing separation between three different things:
  1. exact framework-side structure
  2. the extra connected-color-trace condition behind the `9/8` EW factor
  3. threshold/EFT running behind the `M_Z`-quoted numbers

Primary evidence:

- [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md)
- [frontier_yt_zero_import_chain.py](../../../scripts/frontier_yt_zero_import_chain.py)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing theorem on the live
  EW package surface

**Why**

The deeper notes were already more honest than the front-door summaries. The
remaining stale `derived` row has now been aligned with the retained package
status, and the public surfaces separate same-surface structure, derived
`R_conn` support, and retained running/matching bridges cleanly.

### F. Higgs / top

**Current public posture**

- the live package now separates the retained YT/top transport lane from the
  derived Higgs/vacuum lane
- front-door rows no longer collapse those two lanes into generic bounded
  summaries

Representative surfaces:

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [REVIEWER_SUMMARY.md](../../REVIEWER_SUMMARY.md)

**What the repo actually supports**

- retained YT/top transport lane
- derived Higgs/vacuum lane with a retention-decomposed budget
- framework-native 3-loop Higgs implementation exists
- current public tables now carry the retained YT authority stack and the
  explicit Higgs retention analysis rather than a generic inherited-YT caveat

Primary evidence:

- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](../../YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing theorem on the live
  YT/top and Higgs package surfaces

**Why**

The authority notes were already more honest than the stale summaries. The
public surfaces now track the retained YT/top transport lane and the derived
Higgs/vacuum lane with the same retention-decomposed budget language used in
the controlling notes.

### G. Three-generation matter / chirality defense

**Current public posture**

- retained three-generation matter structure with an explicit reviewer-facing
  three-generation / chirality boundary note on `main`

Representative surfaces:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)

**What the repo actually supports**

- the package already makes the physical-lattice reading explicit
- the axiom boundary is explicit
- the reviewer-facing Nielsen–Ninomiya / chiral-regulator boundary is now
  surfaced directly and tied to the accepted physical-lattice / no-rooting /
  anomaly-forced-chirality package boundary

Primary evidence:

- [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md)
- [GENERATION_AXIOM_BOUNDARY_NOTE.md](../../GENERATION_AXIOM_BOUNDARY_NOTE.md)
- [THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md](../../THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](../../PHYSICAL_LATTICE_NECESSITY_NOTE.md)

**Adjustment class**

- repo/manuscript cleanup resolved on `main`; no missing reviewer-facing
  defense note remains on the live package surface

**Why**

The dedicated reviewer-facing boundary note is now live, and the main package
surfaces already state the narrow answer: physical-lattice species structure,
no rooting in Hamiltonian `Cl(3)` on `Z^3`, no proper exact quotient on the
retained `hw=1` surface, and chirality only on the full-framework
anomaly-forced `3+1` surface. The remaining work here is optional presentation
hardening, not claim-surface repair.

## Working Conclusion

At the current repo state:

- the front-door axiom count problem was real and is now fixed
- the stale Lorentz contradiction was real and is now fixed
- the old claim-surface drift on gravity/QG framing, strong CP, CKM,
  `\alpha_s` / EW normalization, Higgs/top presentation, and the
  three-generation / chirality reviewer-facing boundary has now been cleaned
  on `main`
- no separate live claim-surface blocker remains recorded in this audit; what
  remains is optional presentation hardening

This note remains a living audit guide for future drift checks, not a record
of a current unresolved claim-surface blocker.
