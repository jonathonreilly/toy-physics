# Claude Review Packet Full Bodies

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`. Most of the
review documents below were authored by earlier Claude Sonnet/Opus sessions
or by Codex review passes; they are part of the Claude-side workflow surface
because they live in the same repo and feed back into Claude's behavior.

**Workspace:** `/Users/jonreilly/Projects/Physics`

**Scope note:** Verbatim full-body dump of representative review-related
artifacts from the repo: the incoming `review.md` of this very capture
branch, a closed-out branch summary, a representative review packet, the
repo-level review-queue and review-feedback documents, and one
session-synthesis rollup. These are the actual review-process documents that
shape the Claude-side feedback loop. The `*_REVIEW_PACKET_*.md` family alone
has 17+ visible files (see inventory in `claude_review_structure.md` §3);
this bundle dumps one full example plus the structural docs.

---

## review.md (incoming review of this branch)

**Path:** `/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8/review.md`

**Bytes:** 3021, **Lines:** 92

```markdown
# Review: `claude/ai-methodology-capture-2026-04-25`

## Verdict

Useful raw archive, but **not approved verbatim** for `main`.

The branch contains valuable source material for a methodology paper, but the
submitted surface is still a branch-local capture packet rather than a clean
public methodology lane.

I took a **selective landing** instead. The curated subset now on `main`
(`4da26702`) is:

- `docs/AI_METHODOLOGY_NOTE_2026-04-25.md`
- `docs/ai_methodology/README.md`
- `docs/ai_methodology/CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`
- `docs/ai_methodology/AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md`

That is the correct live surface for now.

## Why the full branch was not landed as-is

### 1. The front-door note is explicitly raw and incomplete

The main note says:

- `Status: RAW INFO CAPTURE`
- Claude-only on this pass
- Codex/OpenAI history to be added later

That makes it a good working packet, but not yet a stable `main` lane. The
methodology lane on `main` needs to read as a curated, citable surface rather
than a temporary archive state.

### 2. The raw annex is too machine-local for a public mainline surface

The raw files carry:

- machine-local absolute paths;
- branch/base snapshots tied to a particular checkout moment;
- full prompt/session dumps;
- full protocol dumps;
- mixed archival and live material.

That material is useful as evidence, but it should not be the first public
surface readers encounter on `main` without a stronger sanitization/indexing
pass.

### 3. The Codex side of the methodology is not yet captured

The branch is heavily Claude-side. But the repo's actual working method is now
Claude-plus-Codex, especially on:

- branch review;
- overclaim detection;
- selective landing;
- repo-hygiene and claim-surface correction.

So a methodology lane that stops at the Claude capture is incomplete.

## What the selective landing preserved

The `main` landing keeps the part that is already mature enough to be public:

- a front-door methodology note;
- a methodology index;
- a short per-paper disclosure paragraph;
- a longer package-level accountability note.

It also keeps the methodology lane **out of the science claim surfaces**. This
is the right separation.

## Follow-up worker tasks

The next workers should extend the methodology lane by capturing the Codex side
at the same editorial standard:

1. Codex prompt/session capture.
2. `review.md` corpus and branch-review patterns.
3. Selective-landing case studies.
4. Repo-hygiene / claim-surface correction examples.
5. Cross-tool disagreement and reconciliation examples.
6. Sanitized archival index for raw prompt/protocol material, if that archive
   is still wanted on `main`.

## Bottom Line

This branch was the right raw evidence-gathering step, but not the right final
repo surface. The methodology lane now exists on `main` in a curated form, and
the remaining Codex/review/hygiene capture should build on that live lane
rather than trying to land the entire raw archive unchanged.
```

## docs/BRANCH_SUMMARY_DISTRACTED_NAPIER.md (closed-out branch rollup)

**Path:** `/Users/jonreilly/Projects/Physics/docs/BRANCH_SUMMARY_DISTRACTED_NAPIER.md`

**Bytes:** 4486, **Lines:** 91

```markdown
# Branch Summary: claude/distracted-napier

**Date:** 2026-04-04
**Focus:** historical import memo for the continuum / dimension-dependent-kernel branch

This file is a branch-summary memo, not a canonical project-state note.

Use it as a historical import record only. For the current review-safe read of
the kernel branch on `main`, prefer:

- [`docs/CONTINUUM_CONVERGENCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_CONVERGENCE_NOTE.md)
- [`docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md)
- [`docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md)

## Historical Branch Results

### 1. 3D gravity with the original 1/L kernel failed the refinement replay
The 3D dense lattice fixed-scale card at `h=1.0` showed TOWARD gravity, but
the corrected refinement replay on the same family flips that read negative by
`h=0.5`. This was the key negative result that reopened the propagator lane.
(Script: `lattice_2d3d_continuum_check.py`)

### 2. 2D ordered-lattice refinement remained the strongest retained success
TOWARD strengthens from `h=1.0` to `h=0.25`. `MI`, `d_TV`, and decoherence all
improve under refinement, and the 2D tail remains close to the expected
`1/b`-type falloff. Born stays at machine precision on the tested range.
(Scripts: `lattice_nn_continuum.py`, `lattice_2d_continuum_distance.py`)

### 3. The imported dimension-dependent-kernel branch became the strongest empirical persistence candidate on ordered lattices
The branch evidence suggested the following bounded pattern:
- 2D: `1/L` remains the strongest current persistence candidate
- 3D: `1/L^2` looks more persistent than `1/L` on the tested lattices
- 4D: `1/L^3` looks stronger than nearby lower powers on longer tested lattices

This was and remains an empirical persistence read, not a theorem of unique
selection. It also still needs reconciliation with the stricter local
transfer-norm probe already frozen on `main`.
(Scripts: `lattice_3d_l2_fast.py`, `lattice_4d_kernel_test.py`,
`transfer_norm_and_born.py`)

### 4. RG-style scaling looked promising but remained bounded
One exploratory lane suggested that a schedule of the form
`s(h) = s₀ × h^alpha` can keep the 3D inverse-square branch finite over the
tested refinement range. That result was useful enough to keep, but not strong
enough to promote as a closed RG theorem.

### 5. Born rule held at the tested dimensions and kernel powers
- 2D 1/L: 2.3e-16
- 3D 1/L^2: 4.0e-15
- 4D 1/L^3: 1.3e-15

### 6. Kernel transfer to random DAGs stayed negative
On random/mirror DAGs, all kernel powers give similar (noisy) gravity.
The dimension-dependent kernel is lattice-specific.
(Script: `dag_kernel_transfer.py`)

## Sanity Audit
Verdict: SUSPICIOUS (weak)
- FLAG 1 (axiom fork): Softened — 3-dimension empirical selection
- FLAG 2 (diverging gravity): Resolved — RG scaling works
- FLAG 3 (sign discontinuity): Inherent — lattice entering scaling regime

## Scripts Created
| Script | Purpose |
|--------|---------|
| `lattice_2d3d_continuum_check.py` | 2D vs 3D gravity refinement |
| `lattice_2d_continuum_distance.py` | 2D distance law convergence |
| `lattice_3d_continuum_convergence.py` | 3D continuum (negative with 1/L) |
| `lattice_3d_fixes.py` | 5 fix strategies compared |
| `lattice_3d_tapered_card.py` | Tapered lattice (TOWARD but breaks distance) |
| `lattice_3d_ytaper_card.py` | Y-only taper (ALL AWAY) |
| `lattice_3d_kernel_l2.py` | First 1/L^2 test |
| `lattice_3d_l2_numpy.py` | Numpy-optimized 1/L^2 |
| `lattice_3d_l2_fast.py` | Layer-by-layer with h^2 measure |
| `lattice_3d_l2_wide.py` | Wide lattice distance law |
| `lattice_4d_kernel_test.py` | 4D kernel persistence comparison |
| `transfer_norm_and_born.py` | Transfer norm + 4D Born |
| `dag_kernel_transfer.py` | Kernel transfer to random DAGs |

## Historical Merge Notes
This branch contributed useful exploratory material to `main`, but it should
not be read as the canonical project state on its own. The most useful imports
were:
- the negative replay showing that refined 3D `1/L` does not hold up
- the stronger ordered-lattice persistence evidence for the `1/L^(d-1)` family
- Born checks at the tested dimensions
- the negative transfer result on random DAGs

For the current bounded read after cleanup, use the notes linked at the top of
this file instead of the historical branch language here.
```

## docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md (representative review packet)

**Path:** `/Users/jonreilly/Projects/Physics/docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`

**Bytes:** 18146, **Lines:** 284

```markdown
# Charged-Lepton Koide Support Packet (2026-04-18)

## Scope

This is the current support packet for the charged-lepton Koide lane.

It consolidates the package-level support stack, the open-bridge boundaries,
and the archived route-pruning record needed to understand how the lane was
compressed.

**2026-04-21 package update.** The April 21 Koide package is now the
authoritative support surface for the charged-lepton lane. It is much
stronger than the April 18-20 state, but it does not yet give
retained closure for either `Q = 2/3` or `δ = 2/9`. The older
conditional evening discussion below remains historical provenance.

**2026-04-22 support update.** The April 22 batch materially strengthens the
charged-lepton lane without changing that open status. What it adds is:

- an explicit A1 landscape audit that documents failed standard bridge
  mechanisms and isolates the strongest remaining candidate routes;
- explicit Lefschetz/spectral-flow support calculations for the APS value
  `|η| = 2/9`;
- exact selected-line Brannen geometry on the retained first branch, plus a
  finite-lattice `L = 3` Wilson-Dirac support illustration of the ambient
  `2/9` value;
- a concrete Callan-Harvey anomaly-descent candidate route on the accepted
  physical-lattice reading, with the remaining Berry/inflow map isolated
  explicitly rather than hidden;
- explicit gauge-by-gauge Yukawa Casimir enumeration and BZ cross-check
  support for the charged-lepton radiative lane;
- a new axiom-native support batch of selected-line/Fourier bridge tools,
  positive-parent support constructions, set-equality / mass-assignment
  reframings, and integrated regression runners;
- a new exact second-order `Q` support batch that lands first-live readout
  factorization, the reduced two-block observable law, a normalized
  effective-action candidate route, and a no-hidden-source audit that compress
  the remaining `Q` gap to one explicit primitive;
- a new `O_h` covariance no-go showing the retained affine Hermitian chart is
  not cubic-point-group covariant beyond parity, so the surviving spin-1
  structural route cannot be justified by inherited `O_h` isotropy alone;
- a clean list of atlas issues and caveats that still matter for honest
  package scoping.

**2026-04-24 support/no-go update.** The April 24 native-dimensionless packet
is now the authoritative guardrail on the open dimensionless side. The new
Round-10 fractional-topology / math-literature batch adds five further no-go
probes (orbifold Chern, `η`-lift, FQHE analog, twisted K-theory, and
Cheeger-Simons). These do not close `δ = 2/9`; they sharpen the remaining
Type-B-to-radian primitive to the cleanest current statement: a period-`1 rad`
vs canonical period-`2π rad` convention choice on the selected-line
observable.

## Historical Route-Pruning Record (Archival)

Before the final April 21 support package, the stack passed through the following
reductions:

- the authoritative retained status before the April 21 support package was
  still the April 17 bounded review:
  no retained Koide derivation on the current surface
- the April 18 support stack closes the exact circulant/character bridge to the
  April 17 Koide package
- the full-cube `Gamma_i` route now closes exactly onto the same three Koide
  channels
- the positive one-clock family and observable selector reduce the candidate
  route to one selected real line
- the selected-line bridge reduces the remaining charged-lepton promotion gap
  to one scalar cyclic-response law
- the selected-slice kernel now reduces further to a frozen slot/CP bank plus
  one real microscopic coefficient
- the one-scalar obstruction triangulation theorem now shows that the live
  charged-lepton promotion gap is exactly one real scalar condition
  `kappa = 2`
- the reviewed Cl(3) doublet/Kramers route now also closes negatively: it
  sharpens one structural support route but still does not derive the physical
  selector point
- the exact `Z_3` scalar-potential support note derives the Clifford-fixed
  selected-slice potential but also records honestly that its minimum does not
  select the physical point
- the exact `C_3` singlet-extension reduction sharpens the old `4 x 4` route
  to one scalar Schur law, and the fixed-coupling follow-up shows that
  constant singlet dressing only reparameterizes a continuum of first-branch
  stationary points rather than selecting the physical one
- the exact selected-slice spectral-completion theorem now also closes the
  remaining simple intrinsic spectral-selector hope negatively: the canonical
  `2 x 2` block is spectrally complete but sign-blind, and its low-complexity
  spectral laws only reparameterize the same one-scalar gap
- the exact eigenvalue-`Q = 2/3` surface theorem now also closes the strongest
  `M2` assumption escape negatively: replacing slot readout by eigenvalues of
  `exp(beta H_sel(m))` gives a monotone one-real surface `beta_q23(m)`, not a
  selected physical point
- the exact scale-selector reparameterization theorem now also closes the
  strongest `M1` assumption escape negatively: the near-miss condition
  `u*v*w = 1` uses the Koide-completed slot `u_small(v,w)`, so it is a
  reparameterization on the already-imposed cone rather than an independent
  derivation
- the old transport-gap observation `1/eta_ratio ~= 4pi/sqrt(6)` is now also
  demoted honestly: even an exact identity there would only compare two
  branch-level constants and would still not furnish an `m`-selection law
- the natural weighted extension of the old `Z_3` character-source cross-check
  is now also closed negatively: arbitrary left/right central class-function
  weights still keep the source kernel diagonal in the canonical source basis,
  so unique tops are basis axes with `Q = 1` and degenerate tops still do not
  force a unique Koide ray
- the strongest surviving Higgs-dressed transport route is now also reduced to
  one scalar: on the missing-axis resolvent lift with baseline `h_0 = 0`,
  `Q = 2/3` occurs at a unique small positive root
  `lambda_* = 0.015808703285395...`, giving direction cosine `0.996266...`
  to the PDG `sqrt(m)` direction; chamber slack is only a near-hit, not the
  exact root
- **(April 20 evening — conditional closure support)** the qubit-lattice-dim
  algebraic closure note packages a candidate route for BOTH
  `Q = 2/3` and `delta = 2/9` from the retained structural identity
  `dim(Cl(3) spinor) / dim(Z^3 lattice) = 2/3`, combined with the
  A-select axiom `SELECTOR = sqrt(6)/3` satisfying `SELECTOR^2 = Q = 2/3`.
  The strongest Brannen-phase route on that surface is dependent rather than standalone:
  `|Im(b_F)|^2 = Q/d` plus Phase-Structural Equivalence `d*delta = Q`.
  The quark-lepton bridge is explicit: the same unique traceless U(1) from
  the `{SU(2)_weak, SWAP_{23}}` commutant forces `|Y(d_R)| = 2/3` via
  tracelessness, and the factor 2 in `|Y(d_R)/Y(Q_L)| = 2` matches
  `dim(Cl(3) spinor) = 2`. See
  `KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md` and
  `HYPERCHARGE_IDENTIFICATION_NOTE.md`.

So the current charged-lepton package status is:

- exact candidate-route closure
- executable Frobenius-isotype / AM-GM support for `Q = 2/3` in
  `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
- executable ABSS fixed-point / topological-robustness support for
  `δ = 2/9` in
  `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
- April 22 support batch: explicit A1 route audit in
  `KOIDE_A1_DERIVATION_STATUS_NOTE.md`,
  `KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md`,
  `KOIDE_A1_LOOP_INVESTIGATION_SUMMARY.md`, and
  `KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md`
- April 22 explicit support calculations in
  `KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`
- April 22 axiom-native support batch summary in
  `KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md`
- April 22 second-order `Q` support batch summary in
  `KOIDE_Q_SECOND_ORDER_SUPPORT_BATCH_NOTE_2026-04-22.md`
- April 22 Brannen geometry / Dirac support addendum in
  `KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`
- April 22 Callan-Harvey physical-bridge candidate in
  `KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`
- April 24 native-dimensionless / objection-review packet in
  `KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md`,
  `KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`,
  and `KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md`
- April 24 A1/radian audit plus Round-10 fractional-topology batch in
  `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`,
  `KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`, and
  `KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md`
- remaining open bridge behind `Q = 2/3`: why the physical charged-lepton
  packet must extremize the block-total Frobenius functional; after the
  second-order support batch this is now sharpened further to the source-free
  law `K = 0` on the normalized second-order reduced carrier if that carrier is
  accepted
- remaining open bridge behind `δ = 2/9`: why the physical selected-line
  Brannen phase equals the ambient APS invariant; after the Round-10
  fractional-topology batch, the residual Type-B-to-radian step is sharpened
  further to the period-`1 rad` vs canonical period-`2π rad` convention choice
  on the selected-line observable
- selected-line witness `m_*` / `w/v` remains downstream of the physical
  Brannen-phase bridge
- overall lepton mass scale `v_0` remains a separate support lane: the
  April 22 radiative/Yukawa calculations strengthen it materially, but it is
  still not promoted on the current package surface

## Read In Order

1. [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](./CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
2. [KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
3. [KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md)
4. [KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md)
5. [KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md)
6. [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
7. [KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md)
8. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
9. [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
10. [KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md](./KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md)
11. [KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md](./KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md)
12. [KOIDE_CL3_SELECTOR_GAP_NOTE_2026-04-19.md](./KOIDE_CL3_SELECTOR_GAP_NOTE_2026-04-19.md)
13. [KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md](./KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md)
14. [KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md](./KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md)
15. [KOIDE_C3_CONSTANT_SINGLET_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md](./KOIDE_C3_CONSTANT_SINGLET_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md)
16. [KOIDE_SELECTED_SLICE_SPECTRAL_COMPLETION_AND_MINIMAL_LOCAL_SPECTRAL_LAW_NO_GO_NOTE_2026-04-20.md](./KOIDE_SELECTED_SLICE_SPECTRAL_COMPLETION_AND_MINIMAL_LOCAL_SPECTRAL_LAW_NO_GO_NOTE_2026-04-20.md)
17. [KOIDE_EIGENVALUE_Q23_SURFACE_THEOREM_NOTE_2026-04-20.md](./KOIDE_EIGENVALUE_Q23_SURFACE_THEOREM_NOTE_2026-04-20.md)
18. [KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md](./KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md)
19. [KOIDE_TRANSPORT_GAP_CONSTANT_NO_GO_NOTE_2026-04-20.md](./KOIDE_TRANSPORT_GAP_CONSTANT_NO_GO_NOTE_2026-04-20.md)
20. [KOIDE_WEIGHTED_CHARACTER_SOURCE_AXIS_THEOREM_NOTE_2026-04-20.md](./KOIDE_WEIGHTED_CHARACTER_SOURCE_AXIS_THEOREM_NOTE_2026-04-20.md)
21. [KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md](./KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md)
22. [KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md](./KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md) **(evening closure)**
23. [KOIDE_A1_DERIVATION_STATUS_NOTE.md](./KOIDE_A1_DERIVATION_STATUS_NOTE.md)
24. [KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md](./KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md)
25. [KOIDE_A1_LOOP_INVESTIGATION_SUMMARY.md](./KOIDE_A1_LOOP_INVESTIGATION_SUMMARY.md)
26. [KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md](./KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md)
27. [KOIDE_EXPLICIT_CALCULATIONS_NOTE.md](./KOIDE_EXPLICIT_CALCULATIONS_NOTE.md)
28. [KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md](./KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md)
29. [KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md](./KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md)
30. [KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md](./KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
31. [KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md](./KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
32. [KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md](./KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md)
33. [KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md](./KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md)
34. [KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md](./KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md)
35. [KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md](./KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
36. [KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md](./KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md)
37. [KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md](./KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md)

## Package Role

- charged-lepton intake for the current package
- exact statement of what changed after the April 17 bounded support baseline
- one-place summary of what is truly closed and what is still open

## Package Standard

This packet is clean enough for package use, atlas use, and consolidation on
the current package surface.

The cycle-1 no-go stack (notes 14-21) sharpened the open gap: the missing
step was one scalar condition, not derivable from the selected-slice scalar
potential or the canonical `2 x 2` spectral carrier. The strongest nearby
assumption escapes (eigenvalue-`Q` surface, scale-selector near-miss,
weighted character-source, Higgs-dressed resolvent, transport-gap constant)
were all formalized and closed honestly as reparameterizations or
constant-vs-constant bridges, not `m`-selection laws.

**(April 20 evening — conditional closure, note 22)** The qubit-lattice-dim
algebraic closure proposes a derivation of BOTH `Q = 2/3` AND `delta = 2/9`
from the retained structural identity `dim(Cl(3) spinor) / dim(Z^3 lattice)
= 2/3` combined with the A-select axiom `SELECTOR = sqrt(6)/3`
(`SELECTOR^2 = 2/3`). Supporting identities: `|Y(d_R)| = 2/3` (anomaly
cancellation), and `delta = Tr[Y^3]_quark_LH = 2/9` (direct anomaly
arithmetic at d=3). The quark-lepton bridge is explicit via the retained
U(1) hypercharge commutant.

**Important caveat:** note 22 does NOT overturn note 21
(`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`), which rules
out four specific character-data candidates for the radian bridge P.
Note 22 uses a DIFFERENT route: Q-closure via qubit-lattice-dim +
anomaly arithmetic, then CPC d·delta = Q derives delta. Whether this
constituted a valid structural bridge was the live package question on the
April 20 evening surface. That historical state is now superseded by the
April 21 support package.

**(April 20 late - reduction note 24)** Even if note 22 is treated only as
full closure, the open content of the Brannen-phase radian-bridge step is now much sharper. The new
selected-line local no-go proves the actual `CP^1` Berry packet is too simple
to pick the interior point `delta = 2/9`, while the retained anomaly-forced-
time theorem already fixes the native ambient as one-clock physical `3+1`.
So the live native route is no longer "find a smarter local Berry scalar." It
is now: derive a one-clock ambient `3+1` endpoint/transport law, or derive an
extra Wilson/lattice phase datum on that ambient, whose pullback fixes the
Koide point. This remains useful provenance for how the search space
collapsed, but it is no longer the canonical closure posture after the
April 21 package.

Items that remain open:

- overall lepton mass scale `v_0 ~ 17.72 sqrt(MeV)` is a separate hierarchy
  input, not part of Koide/Brannen closure.
- quark-sector and neutrino-sector Koide analogs are sector-specific open
  problems.

So the current package classification is:

- strongest current executable support for `Q = 2/3`, with the
  extremal-principle bridge still open; strongest remaining A1 routes are now
  the Yukawa Casimir-difference lemma, the Lie-theoretic / Clifford
  dimension-ratio lemma family, and the quartic-potential import route
- strongest current executable support for `delta = 2/9`, with the physical
  Brannen-phase bridge still open; the April 22 batch adds explicit
  Lefschetz/spectral-flow support, exact selected-line geometric support,
  a conditional Route-3 Wilson-line support law, and a finite-lattice
  `L = 3` Wilson-Dirac illustration; it also now packages a concrete
  Callan-Harvey anomaly-descent candidate route, but not the physical
  identification theorem
- retained promotion for charged-lepton ratios is still conditional on those
  two bridges, modulo the separate overall lepton scale input `v_0`
```

## docs/repo/ACTIVE_REVIEW_QUEUE.md

**Path:** `/Users/jonreilly/Projects/Physics/docs/repo/ACTIVE_REVIEW_QUEUE.md`

**Bytes:** 2270, **Lines:** 62

```markdown
# Active Review Queue

**Status:** canonical live queue for current-main review feedback  
**Purpose:** single place to record reviewer findings that still need a decision,
fix, or explicit rejection on `main`

## Rule

Use this file for **active** review feedback only.

- add new reviewer findings here first
- keep each item short and decision-oriented
- link any long-form packet in
  [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
- when an item is resolved, remove it from the open list and record it in the
  queue history section or the linked detailed packet

Do not use scattered backlog notes or branch-local memos as the live review
truth surface.

## Current State

As of `2026-04-18`, there are **no live repo-governance or claim-surface
blockers** waiting in the review queue. The remaining items are science-facing
open lanes rather than review-hygiene debt.

Current science/open-lane follow-ups:

- irregular off-lattice sign lane: portability beyond the bounded centered
  core-packet surface remains open
- periodic 2D torus diagnostics: nearby torus probes still need code audit
  before reuse outside the corrected retained notes
- Wilson two-body lane: full both-masses law and action-reaction remain open
- boundary-law / holographic lane: keep the effect bounded and do not overread
  it as a holography derivation
- memory lane: protocol- and geometry-stable observable remains open
- emergent-geometry growth: multi-size, multi-seed stability remains open

## Intake Format

Record each new finding as one bullet:

- `ID`
  short label; date if needed
- `Scope`
  affected lane, note, script, or package surface
- `Finding`
  one-sentence statement of the issue
- `Disposition`
  one of: `triage`, `fix on main`, `support-only demotion`, `science-needed`,
  `reject`
- `Detail`
  optional link to a longer packet in work history

## Queue History

- `2026-04-18`
  repo-wide review/backlog cleanup completed; the old operational review
  packets and planning backlogs were moved out of the front-door `docs/`
  surface into [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
  and [`docs/work_history/repo/backlog/`](../work_history/repo/backlog/README.md)
```

## docs/repo/REVIEW_FEEDBACK_WORKFLOW.md

**Path:** `/Users/jonreilly/Projects/Physics/docs/repo/REVIEW_FEEDBACK_WORKFLOW.md`

**Bytes:** 2424, **Lines:** 63

```markdown
# Review Feedback Workflow

**Purpose:** define the canonical process for landing, reviewing, triaging, and
closing repo feedback on `main`

## Canonical Files

- active queue:
  [`ACTIVE_REVIEW_QUEUE.md`](./ACTIVE_REVIEW_QUEUE.md)
- historical detailed packets:
  [`docs/work_history/repo/review_feedback/README.md`](../work_history/repo/review_feedback/README.md)
- historical planning backlogs:
  [`docs/work_history/repo/backlog/README.md`](../work_history/repo/backlog/README.md)

## Default Process

1. Land the candidate work on `main` if it is already honest enough to keep.
2. Have the reviewer check the landed surface or the clean science-only review
   branch.
3. Record any actionable finding in
   [`ACTIVE_REVIEW_QUEUE.md`](./ACTIVE_REVIEW_QUEUE.md).
4. If the review needs more than a short bullet list, add a detailed packet in
   [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
   and link it from the queue.
5. Triage each item into one of five buckets:
   - `fix on main`
   - `support-only demotion`
   - `science-needed`
   - `reject`
   - `historical only`
6. Resolve the item on `main` if it is wording, packaging, code, or honest
   demotion work.
7. Remove the item from the active queue once the repo-facing state is correct.

## Decision Rule

Use the narrowest honest fix:

- if the issue is wording, packaging, stale status language, or a reproducible
  code bug, fix it on `main`
- if the issue is a real missing theorem step or unjustified selector, do not
  fake closure; either demote the claim or keep the science off-main until the
  derivation exists
- if the issue concerns a historical lane that is no longer part of the live
  evidence chain, classify it as `historical only` rather than treating it as a
  live blocker

## Placement Rule

- do **not** put new review packets in the front-door `docs/` root unless they
  are themselves part of the live science package
- do **not** create new free-floating backlog files for current review work
- do **not** use branch-local notes as the long-term review source of truth

## What Belongs Where

- `docs/repo/ACTIVE_REVIEW_QUEUE.md`
  current actionable review state
- `docs/work_history/repo/review_feedback/`
  older audit notes, detailed review packets, and resolved review histories
- `docs/work_history/repo/backlog/`
  planning/backlog notes that are not current review truth surfaces
```

## docs/SESSION_SYNTHESIS_2026-04-09.md (sample end-of-day rollup)

**Path:** `/Users/jonreilly/Projects/Physics/docs/SESSION_SYNTHESIS_2026-04-09.md`

**Bytes:** 8504, **Lines:** 173

```markdown
# Session Synthesis — 2026-04-09

## What happened

A single session attacked all 20 proposed moonshot frontiers, went through
10+ review rounds, and ended by discovering that the model's "gravity"
mechanism was not gravity — leading to a fundamental modification (the
Lorentzian split-delay action) that produces genuine geometric gravity.

~70 scripts delivered. ~15 PRs merged. Every claim was narrowed by review
at least once.

## The three discoveries (in order of importance)

### 1. The original model's gravity is a dispersive wave force, not geometry

The geodesic test (frontier_geodesic_gravity_test.py) showed that shortest
paths on the delay landscape bend AWAY from mass, not toward it. The delay
formula delay = L×(1+f) makes all delays longer near mass, so geodesics
avoid the slow region. The TOWARD deflection at k=5 is a wave-interference
resonance that OVERRIDES the repulsive geometric baseline.

Evidence:
- 2D geodesics: mass-side delayed +4.31 vs far-side +1.91 (AWAY)
- 3D geodesics: mass-side delayed +0.000471 vs far-side +0.000122 (AWAY)
- k-sweep: gravity oscillates TOWARD/AWAY with period ~π in k
- Spectral averaging: universally AWAY on the retained lattice
- First-principles derivation: Axiom 8 predicts AWAY from the delay landscape

### 2. The Lorentzian split-delay action fixes this

Replacing the uniform delay with a causal/spatial split:

  S = L × (1 - f × cos(2θ))

where θ is the edge angle from the causal direction, gives:
- θ=0 (causal): S = L(1-f) — action decreases near mass (time dilation)
- θ=π/2 (spatial): S = L(1+f) — action increases near mass (spatial stretch)

This matches the Schwarzschild metric structure (g₀₀ shrinks, g_rr grows)
and makes geodesics bend TOWARD mass.

The Lorentzian model at k=7 passes all core tests:
- Born: 1.50e-15 (machine precision)
- Gravity: +0.001079 TOWARD (2.5× stronger than Euclidean k=5)
- F∝M: 1.00 (R²=1.0000)
- Distance: 5/6 TOWARD, b^(-1.23) (R²=0.96)
- Decoherence: 31.1%

### 3. F∝M = 1.00 is structural to the action, not to gravity

The linearity of deflection with field strength holds at ALL k values
(1.0 through 10.0), in both TOWARD and AWAY windows, with R²=1.0000
everywhere. This comes from the valley-linear action's linearity in f,
not from a gravitational mechanism. It survives any reinterpretation.

## What survived all reviews (no asterisks)

### Structural (mechanism-independent)
- Born rule: kernel-independent, machine precision on static and grown DAGs
- Gauge connections: U(1), AB modulation (cos²(φ/2), depth=1.0)
- F∝M = 1.00: structural to valley-linear action, all k values
- Dynamic growth: self-regulating, Born at 4.3e-17 (2D) and 8.3e-17 (3D)
- Causal set: valid poset, metric from chains at r=0.997
- Parity charge: Z₂ conserved quantum number

### Euclidean model (S = L(1-f)) — now understood as dispersive
- Attractive window k=1.5-6.0 on 3D lattice (phase diagram mapped)
- Repulsive geometric baseline (geodesics AWAY)
- 3D Laplacian solver confirms analytic field is not misleading
- 3+1D feasibility at h=0.5 (TOWARD at k=5, but this is wave resonance)
- Superposition 0.01% on additive fields in 3D (propagator linearity)
- Action constrained from axioms (valley-linear at leading order)

### Lorentzian model (S = L(1-f·cos(2θ))) — NEW, needs validation
- Geometric gravity: geodesics TOWARD mass at strong field (5e-2).
  At weak field (5e-5, the closure-card regime), lattice cannot resolve
  geodesic deflection (both models show NONE). The geometric mechanism
  is demonstrated at strong field only.
- All core tests pass at k=7 on 3D lattice (h=0.5, W=6, L=12):
  Born 1.50e-15, gravity +0.001 TOWARD, F∝M=1.00, 5/6 TOWARD b^(-1.23)
- Born, F∝M, d_TV, decoherence identical to Euclidean (flat-space same)
- Attractive window shifted: k=6.5-7.5 and k=10-12
- NOT YET VALIDATED: spectral averaging, 3+1D, multi-L, Laplacian field

## Honest negatives

- Energy levels don't converge to n² (lattice-dominated spectrum)
- Rotational isotropy doesn't improve with h (angular kernel intrinsic)
- Continuum dispersion: cone and parabola indistinguishable at h=0.25
- Hawking T~1/M: falsified (thermal shape is lattice geometry)
- Lorentz invariance: not emergent (τ invariance is assumed, not derived)
- Dimensional preference: falsified (all dimensions 1+1D-4+1D pass)
- Spectral averaging: AWAY on Euclidean retained lattice
- Propagator is diffusive, not causal (no light cone from amplitude alone)
- Angular kernel: not derived (heuristic phase-coherence story only)

## The resonance mechanism

Gravity in both models is a resonance phenomenon:
- The deflection oscillates between TOWARD and AWAY as k varies
- The period is ~π in k on the 3D lattice
- The mechanism is complex multi-path interference, not simple two-path
- The resonance structure is geometry-dependent (changes with lattice size)
- Spectral averaging washes out the resonance (no universal attraction)
- F∝M = 1.00 holds at ALL k values (structural to the action)

The Euclidean model has the resonance fighting a repulsive baseline.
The Lorentzian model has the resonance reinforcing an attractive baseline.

## Open questions for the next session

### Validation of the Lorentzian model
1. Spectral averaging: does the Lorentzian model survive it better?
   (The geometric baseline is now TOWARD, so the average might be TOWARD)
2. 3+1D: does the Lorentzian model work in physical spacetime?
3. Multi-L companion checks at k=7
4. Self-consistent Laplacian field on the Lorentzian model
5. The attractive window k=6.5-7.5 is narrow — is this stable?

### Theoretical
6. Can cos(2θ) be derived from the axioms? (The split distinguishes causal
   from spatial edges — this might follow from Axiom 3 or 4)
7. Does the Lorentzian action change the effective Hamiltonian/dispersion?
8. Is k=7 "natural" or does the model need a k-selection mechanism?
9. Does the Lorentzian model produce geometric gravity that survives
   spectral averaging? (This would be THE decisive test)

### The paper
10. Frame as: "A linear path-sum on a discrete causal graph with Lorentzian
    split-delay action produces geometric gravitational attraction, Born rule,
    gauge connections, and dynamic graph growth."
11. The Euclidean→Lorentzian transition is a discovery worth documenting
12. The resonance mechanism is novel physics worth describing

## File inventory

### Derivations
- distance-law-analytic-theorem-2026-04-09.md
- action-uniqueness-theorem-2026-04-09.md (renamed to constraint theorem)
- geometric-vs-dispersive-gravity-2026-04-09.md

### Key scripts (in rough importance order)
- frontier_lorentzian_closure_card.py — Lorentzian head-to-head
- frontier_lorentzian_k8_card.py — k=7 full card (ALL PASS)
- frontier_lorentzian_delay_geodesic.py — geodesics TOWARD with split delay
- frontier_geodesic_gravity_test.py — geodesics AWAY on Euclidean
- frontier_fm_vs_k.py — F∝M=1.00 at all k
- frontier_wave_geodesic_decomposition.py — wave vs geometric separation
- frontier_resonance_phase_diagram.py — broad attractive plateau
- frontier_spectral_on_lattice.py — spectral averaging AWAY
- frontier_3d_laplacian_closure.py — self-consistent field confirmed
- frontier_retained_field_growth.py — Laplacian gravity on grown DAG
- frontier_dynamic_growth.py — Born on grown DAG
- frontier_3d_dynamic_growth.py — Born on grown 3D DAG
- frontier_angular_kernel_investigation.py — 7 kernels tested
- frontier_cos2_closure_card.py — cos²(θ) comparison
- frontier_3plus1d_same_geometry_refinement.py — resolution confirmed
- frontier_2d_gravity_sign_diagnosis.py — field strength + attenuation
- frontier_pn_suppression_math.py — weak-field enhances, strong oscillates
- frontier_born_from_information.py — composability → linearity → p=2
- frontier_causal_set_bridge.py — valid poset, r=0.997
- frontier_gauge_invariance.py — U(1) + AB + SU(2)
- frontier_spin_from_symmetry.py — Z₂ parity charge
- frontier_why_3plus1.py — all dimensions pass
- frontier_cosmological_expansion.py — 14% separation growth
- frontier_geometry_superposition.py — phase differences real
- frontier_experimental_prediction.py — Planck-suppressed
- frontier_decoherence_local_entangle.py — exponential scaling
- frontier_wave_particle_transition.py — imposed complementarity
- frontier_hawking_analog.py — thermal shape = lattice geometry
- frontier_causal_propagator.py — diffusive, no light cone
```

