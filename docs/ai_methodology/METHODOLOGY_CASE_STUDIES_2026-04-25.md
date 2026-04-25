# Methodology Case Studies

**Date:** 2026-04-25
**Status:** derivation-centered case-study packet from raw methodology evidence

These case studies are the scientific spine for the methodology paper. They are
not meant to be generic workflow anecdotes. Each one tells the story of a hard
physics unlock: what made the target difficult, how AI accelerated the search,
which repo skills kept the work honest, what artifact was left behind, and
where the current claim boundary sits.

The case studies deliberately mix retained, bounded, support, and no-go
outcomes. That is the point of the methodology: AI-assisted theory is useful
only when the repository can distinguish closure from support, support from
open work, and failed routes from useless work.

## Case Study 1: Cl(3)/Z^3 To Standard-Model Algebra

**Hard physics problem:** Starting from the small framework stack, recover
Standard-Model-like gauge and matter structure without silently inserting the
answer: native `SU(2)`, hypercharge, color `SU(3)`, three generation candidates,
and the electroweak/color normalization factors all have to come from the same
`Cl(3)` on `Z^3` surface.

**Why this is hard:** The danger is numerology. Dimension counts such as
`d+1`, `d+2`, `N_c = 3`, and `8/9` are easy to state after the fact, but the
actual claim requires explicit operators, commutators, projectors, eigenvalue
spectra, Fierz identities, and status boundaries. A smooth AI derivation could
hide the hard part by using words like "natural" or "emergent" where the repo
needs matrices.

**AI/repo move:** AI production explored many equivalent algebraic framings;
review pressure forced the work into exact representation artifacts. The lane
landed as theorem notes plus a regression runner rather than a single narrative
claim:

- `docs/CL3_SM_EMBEDDING_THEOREM.md`
- `docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md`
- `docs/CL3_TASTE_GENERATION_THEOREM.md`
- `docs/CL3_SM_EMBEDDING_MASTER_NOTE.md`
- `scripts/verify_cl3_sm_embedding.py`

The repo-skill pattern was: decompose the physics target into load-bearing
subclaims, require explicit matrix checks, and keep the master note as a
synthesis surface rather than a new axiom.

**Artifact outcome:** The master packet reports `95/95` checks across Clifford
anticommutation, `Cl+(3) ~= H`, central omega, bare `g_2^2 = 1/4`,
`g_Y^2 = 1/5`, hypercharge spectrum `(+1/3, -1)`, `S_3`/`Z_3` taste generation
structure, `SU(3)_c`, Fierz, `R_conn = 8/9`, and L-sector Kramers support.

**Current boundary:** Reviewed algebraic support synthesis on current `main`.
It sharpens the Standard-Model embedding layer but does not by itself promote
generation mass splitting, running couplings, full anomaly closure, or
downstream phenomenology.

**Methodology lesson:** AI was valuable because it could traverse a large
operator-algebra search space quickly. The repo made that useful by forcing the
result into exact, reviewable artifacts with a narrow claim boundary.

## Case Study 2: The Quantitative Electroweak / Top / Hierarchy Chain

**Hard physics problem:** Connect the framework's canonical lattice surface to
quantitative observables such as `v`, `alpha_s`, electroweak couplings, and the
top/Yukawa lane without importing hidden fit parameters or losing track of
normalization conventions.

**Why this is hard:** This lane is full of traps: tadpole improvement powers,
color projection, `g_bare` normalization, whether `8/9` enters electroweak
couplings or Higgs mass, whether `alpha_LM` and `alpha_s(v)` are independent
knobs, and whether a Yukawa relation is really a derived observable rather than
a bare vertex identification.

**AI/repo move:** AI generated candidate derivation routes, but the durable
unlock came from repeatedly narrowing the evidence chain:

- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` forced the scalar observable
  generator to `log|det(D+J)|` from Grassmann factorization, additivity, and
  CPT-even scalar response.
- `docs/ALPHA_S_DERIVED_NOTE.md` separated the retained same-surface strong
  coupling lane from downstream running.
- `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` isolated the electroweak color
  projection factor `R_conn = 8/9`.
- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` recast the top Yukawa relation
  as a same-theory 1PI identity, `y_t/g_s = 1/sqrt(6)`, with no independent
  Yukawa parameter.
- `docs/HIGGS_MASS_FROM_AXIOM_NOTE.md` tracked `N_c` explicitly and prevented
  the electroweak color factor from being incorrectly reused in the Higgs
  channel.

The repo-skill pattern was artifact-chain alignment: every numerical row had
to identify whether it came from the canonical lattice surface, a structural
identity, a running bridge, or a bounded support route.

**Artifact outcome:** The current minimal-input memo records retained
quantitative rows including `v = 246.282818290129 GeV`, `alpha_s(M_Z) =
0.1181`, electroweak coupling readouts, the exact lattice-scale
`y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)`, and downstream top/Higgs support with
explicit bridge budgets.

**Current boundary:** Retained quantitative package with bridge-conditioned
downstream rows. The top Ward identity is exact on its stated tree-level
surface; Higgs mass rows carry support/bounded status where loop or
continuum-bridge effects remain live.

**Methodology lesson:** The AI contribution was not just speed. It enabled
parallel route discovery and convention auditing, while the repo skills made
normalization, hidden-input, and cross-lane-contamination errors visible before
they became public claims.

## Case Study 3: CKM Structure From Counts Instead Of CKM Fits

**Hard physics problem:** Derive CKM phase and magnitude structure from the
framework's count/atlas surface rather than fitting the CKM matrix and reading
the structure backward.

**Why this is hard:** CKM phenomenology is dense with standard conventions,
finite-`lambda` corrections, fitted global parameters, and observation-facing
comparators. A candidate AI derivation can look impressive while quietly using
the very CKM observables it claims to predict.

**AI/repo move:** The AI workflow split the CKM atlas into small theorem-grade
surfaces, each with an explicit no-fitted-CKM-input clause and a runner. Review
pressure then made the status boundaries local:

- `docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` extracts
  `rho = 1/6`, `eta = sqrt(5)/6`, `tan(delta_CKM) = sqrt(5)`, and
  `J_0 = alpha_s(v)^3 sqrt(5) / 72`.
- `docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md` packages
  the five leading off-diagonal magnitudes into one structural-counts surface.
- `docs/CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md`
  factorizes the CKM imaginary bracket for `epsilon_K` through `J_0`.
- `docs/CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md` derives
  the leading `B_s` phase identity `phi_s,0 = -alpha_s(v) sqrt(5) / 6`.

The repo-skill pattern was theorem extraction: take an implicit atlas result,
name the exact inputs, write the algebra, run a focused regression, and state
what the note does not claim.

**Artifact outcome:** The CKM case now has multiple retained structural
identity notes with explicit reproduction commands and pass counts. The
comparators are downstream checks, not derivation inputs.

**Current boundary:** Retained CKM-structure theorems on the promoted
atlas/axiom surface, with finite-`lambda` and standard-phenomenology bridges
kept explicit.

**Methodology lesson:** AI made it possible to rapidly refactor a broad CKM
atlas into independently reviewable claims. The repo prevented the most
dangerous mistake: confusing post-diction against CKM data with derivation from
framework structure.

## Case Study 4: DM, Leptogenesis, And The Selector Problem

**Hard physics problem:** Turn a complicated dark-sector/leptogenesis package
into a controlled claim boundary: source-sector primitives, PMNS target surface,
branch selection, baryon asymmetry, and dark-matter abundance all interact, and
several tempting closure routes fail.

**Why this is hard:** The live blocker was not a single arithmetic gap. It was
the selector problem: which branch or chamber is physically selected, which
ingredients are source-native, and which are target-surface or observational
bridges. AI can easily close the wrong problem by proving a local identity
while leaving the global sign or selector ambiguity untouched.

**AI/repo move:** The method treated no-go results as map data. Obstruction
audits and chamber-blindness results narrowed the target until a more precise
claim could be stated:

- `docs/DM_ABCC_EXACT_TARGET_SURFACE_SOURCE_CUBIC_CLOSURE_THEOREM_NOTE_2026-04-21.md`
  shows that, once the exact PMNS target surface is granted, the
  coefficient-free source cubic selects Basin 1 on the chamber root set.
- `docs/DM_CURRENT_BANK_QUANTITATIVE_MAPPING_NOTE_2026-04-21.md` assembles the
  current exact bank into a quantitative public mapping with `17/17` checks.
- `docs/DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`
  records the later bounded support theorem for the eta blocker, including the
  audit-discovered candidate `m_DM = N_sites * v = 16v` and a null-distribution
  audit.

Reviewer backpressure mattered especially on the April 25 eta theorem: the
note was revised to say that `m_DM = 16v` is a candidate structural identity,
not a closed dark-sector mechanism.

**Artifact outcome:** The DM lane gained a sharper target-surface A-BCC
closure theorem, an explicit quantitative current-bank table, and a bounded
freezeout-bypass support result with a falsifiable `3.94 TeV` candidate mass.

**Current boundary:** Mixed. Some subtheorems are exact on their stated target
surface; the eta/freezeout mass-origin story remains bounded support with open
lanes for dark-sector hierarchy compression and a mechanism fixing `16v`.

**Methodology lesson:** AI was strongest at enumerating basins, no-go routes,
and candidate identities. The repo skill was deciding which surface the result
actually lived on and refusing to let a target-surface theorem masquerade as a
global native closure.

## Case Study 5: Koide As A High-Value Partial Unlock, Not A Fake Closure

**Hard physics problem:** Explain charged-lepton Koide structure and the
Brannen phase from the framework, including why `Q = 2/3` and the phase target
should arise rather than being fitted.

**Why this is hard:** Koide is exactly the kind of problem where AI can generate
beautiful but fragile derivations. There are many nearby mathematical
structures: `Z_3`, modular forms, Chern-Simons/TQFT, Schur complements,
baryon-extended holonomies, APS/topological phases, and extremal functionals.
Most can be made to sound plausible. Closure requires showing that the
framework forces the physical charged-lepton packet onto the right surface.

**AI/repo move:** AI explored many routes quickly, but reviewer backpressure
kept the lane from promoting a false closure. The reusable pattern was:
generate route, demand decisive artifact, test the semantic bridge, and convert
failures into narrowed targets or no-go notes. Representative artifacts include:

- `docs/KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`, which narrows
  `Q = 2/3` to the remaining question of why the charged-lepton packet realizes
  the admissible primitive;
- `docs/KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`,
  which records a broad fractional-topology / math-literature no-go synthesis
  for the `2/9 rad` bridge;
- raw review evidence showing that some claimed closures cited runners that
  did not execute the decisive APS/spatial-rotation step, or used literal
  assertion checks where theorem obligations remained.

**Artifact outcome:** The Koide lane did not receive unrestricted retained
closure. It did receive support results, exact bridge narrowing, and no-go
surfaces that prune large families of tempting but non-closing routes.

**Current boundary:** High-value open/support lane. Koide remains useful for
the methodology paper precisely because it shows the system refusing a flashy
AI-generated closure when the evidence chain does not support it.

**Methodology lesson:** A failed closure can be a major scientific output if it
collapses an enormous search space into a smaller, named obstruction. This is
the reviewer-backpressure methodology in its most important form.

## Case Study 6: Gravity And Wave Lanes Under Frozen Replay

**Hard physics problem:** Test whether the framework can produce gravity-like
or wave-like behavior in simulation: retarded fields, lightcones, lensing
functional forms, self-gravity, Born compatibility, and distance laws.

**Why this is hard:** Numerical frontier work is artifact-sensitive. A result
can depend on grid width, normalization, baseline choice, finite-size effects,
or the exact frozen harness. AI-generated scripts can produce a plausible
frontier story before the validation harness is strong enough to carry it.

**AI/repo move:** The early AI workflow produced broad simulation probes and
then used frozen replay and adversarial review to separate retained positives
from overclaims. Representative artifacts include:

- `docs/WAVE_3PLUS1D_PROMOTIONS_NOTE.md`, which retains strict `(3+1)D`
  lightcone and retarded-vs-instantaneous wave results on its stated surface;
- `docs/LENSING_DEFLECTION_NOTE.md`, which demotes a standard `1/b` lensing
  headline to a cleaner but non-standard power-law result after refinement;
- correction/no-go notes in the gravity and wave lanes where later runs found
  mismatched lattice widths, inconsistent absorption normalization, or
  zero-field baselines.

**Artifact outcome:** The wave/gravity history contains retained positives,
bounded positives, and demotions. The public surface is narrower than the raw
exploration, but the surviving results are more credible because the old
headlines were allowed to change.

**Current boundary:** Mixed retained/bounded/support surface by lane. The
methodology paper should use these as examples of artifact-chain correction,
not as a single global claim that emergent gravity is closed.

**Methodology lesson:** AI gives enough throughput to explore a simulation
frontier, but only frozen replay, controls, and review can decide which
signals survive.

## Cross-Case Pattern

Across the derivation stories, the recurring mechanism is:

1. AI expands the route space faster than a human-only workflow could.
2. The repo forces candidates into notes, runners, logs, exact derivations, or
   no-go artifacts.
3. Review attacks the decisive bridge, not just the surrounding algebra.
4. The claim is promoted, demoted, bounded, or rejected according to the
   evidence chain.
5. The lesson becomes a reusable skill instruction.

This is the methodology paper's central empirical claim: the scientific gain
comes from AI plus repository discipline, not AI alone.
