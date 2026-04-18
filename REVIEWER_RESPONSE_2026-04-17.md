# Reviewer Response v2 — `claude/g1-complete` resubmission (Option A)

**Date:** 2026-04-17 (second review pass, after commit `5c70c15d` review)
**Addressed:** reviewer verdict "do not merge as-is" with three blockers
plus branch-hygiene instructions (review.md as of the 5c70c15d
assessment).
**Outcome:** **Option A** applied — honest-label demotion of the two
load-bearing non-retained ingredients; flagship closure headline
explicitly demoted from `CLOSED` to `conditional / support`; branch
hygiene restored on top of `origin/main`.

Option B (derive the Schur live-sheet commutation premise and the
branch-choice principle from the retained atlas) is flagged as a
separate open item; the G1 package on this branch stands as a
conditional / support closure with the non-retained ingredients made
explicit.

## Blocker disposition

| Blocker | Disposition | Mechanism |
|---------|-------------|-----------|
| 1. Schur premise still imposed on the live sheet | **Option-A demotion** + **explicit non-commutation witness** | Schur runner Part 6 measures `‖[H_live, C_3]‖_F ≈ 3.96` and `‖[H_live, P_i]‖_F ≠ 0` for `i=1,2,3` at the closure pin; note relabeled as *commutant-class lemma only — NOT a live-sheet promotion*; `Q = 6(δ²+q_+²)/m²` is no longer claimed as live-sheet curvature. |
| 2. Inertia selector is imposed branch-choice, not derived | **Option-A demotion** | Perturbative-uniqueness runner Part 3 PASS labels rewritten to *"admissible under the imposed rule"*; note retitled to *"Conditional Basin-Uniqueness via an Imposed Branch-Choice Admissibility Rule"*; Sylvester's law of inertia kept as a textbook algebraic fact, but the SELECTION of the baseline-connected branch as the physical live sheet is labeled as imposed, not derived. |
| 3. Flagship headline says `CLOSED` | **Demoted to `conditional / support`** | Flagship closure review note retitled *"DM Flagship Gate — Conditional / Support Closure Review"*; "Position on flagship paper surface" explicitly states "the DM flagship gate is **NOT** declared CLOSED on the current branch tip. Its honest current status is **conditional / support closure**." All three companion notes (Schur, perturbative, PMNS closure) re-labeled consistently. |
| **Branch hygiene** | **Rebased** onto latest `origin/main` | G1 branch reset to `origin/main` (`e880d45b`) and only the 31 G1-added files re-staged: 14 new runners + 16 new notes + this REVIEWER_RESPONSE + the review.md carry-in. All 43 regressed shared-file mods from the prior tip have been dropped. |

## Runner total

| Runner | PASS | Δ vs prior |
|---|---:|---:|
| `frontier_dm_neutrino_source_surface_schur_scalar_baseline_theorem.py` | 26 | +7 (Part 6 live-sheet non-commutation witness) |
| `frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py` | 26 | 0 |
| `frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py` | 26 | 0 |
| `frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py` | 22 | 0 |
| `frontier_dm_neutrino_transport_chamber_blindness_theorem.py` | 16 | 0 |
| `frontier_dm_neutrino_source_surface_parity_mixing_selection_obstruction.py` | 27 | 0 |
| `frontier_dm_neutrino_observable_bank_exhaustion_theorem.py` | 36 | 0 |
| `frontier_dm_neutrino_source_surface_quartic_isotropy_and_u2_obstruction.py` | 18 | 0 |
| `frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py` | 35 | 0 |
| `frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py` | 37 | 0 |
| `frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py` | 46 | 0 (labels rewritten, no algorithmic change) |
| `frontier_pmns_theta23_upper_octant_chamber_closure_prediction.py` | 31 | 0 |
| `frontier_charged_lepton_ue_identity_via_z3_trichotomy.py` | 40 | 0 |
| `frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py` | 43 | 0 |
| **TOTAL** | **429** | **+7** |

All PASSes verify the stated mathematical content; the `+7` on the
Schur runner are the Part 6 live-sheet non-commutation witness at the
closure pin.

## Blocker-by-blocker

### Blocker 1 — Schur "must commute" premise not imposed on the live sheet

**Reviewer point.** The prior Schur runner invoked *"the retained zero-
source baseline must commute with the retained three-generation algebra"*
to promote `D = m I_3` and `Q = 6(δ² + q_+²)/m²` into theorem-native
live-sheet curvature. The "must commute" premise is not a retained
theorem of the atlas.

**Option-A fix.**

1. **New runner Part 6 — live-sheet non-commutation witness.** The
 Schur runner now evaluates the live Hermitian curvature
 `H_live = m_* I_3 + δ_* T_δ + q_+* T_q` at the PMNS closure pin
 `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` and measures:
 - `signature(H_live) = (2, 0, 1)` (non-degenerate Hermitian on the
   baseline-connected branch);
 - `H_live ≠ m · I_3` for any scalar `m` (`‖H_live − m I‖_F ≈ 2.88`);
 - `‖[H_live, C_3]‖_F ≈ 3.96` ≠ 0 (fails Schur premise against the
   cyclic generator);
 - `‖[H_live, P_i]‖_F ≠ 0` for `i = 1, 2, 3` (≈ 2.35, 1.06, 2.54 —
   projectors are outside the Z_3 circulant algebra).

 Seven PASS lines document these witnesses. The witness makes it
 explicit, in the runner itself, that the Schur premise FAILS on the
 live sheet at the closure pin.

2. **Runner docstrings rewritten.** The module docstring now reads
 "Schur SCALAR-BASELINE COMMUTANT-CLASS LEMMA (conditional only; NOT
 a live-sheet promotion)". Parts 3, 4, 5 are relabeled as
 "commutant-class conditional only"; Part 5 "Honest gap statement"
 explicitly withdraws the prior two-unknowns-to-one narrative and
 flags the Option-B live-sheet derivation as an open item.

3. **Note retitled and rewritten.** The Schur note retitled to
 *"Commutant-Class Structural Lemma (Schur Scalar Baseline) —
 CONDITIONAL ONLY"*. "Why this is a genuine promotion" section
 replaced by "Why the previous 'genuine promotion' claim is
 withdrawn". "Narrowed gap statement" replaced by "Honest gap
 statement (Option-A — withdrawal of earlier 'narrowed gap' claim)".
 Position on publication surface says: *"This note must NOT be used
 to promote anything in the flagship paper quantitative section."*

4. **Flagship note coverage row** for the Schur runner relabeled
 "baseline (commutant-class lemma only)"; the result column records
 the explicit non-commutation witness with Frobenius norms.

The Schur lemma remains retained as a textbook algebraic fact on
operators that do commute with the retained algebra. The live sheet
does not satisfy that premise, and nothing on this branch claims it
does.

### Blocker 2 — Inertia-preservation selector is imposed branch-choice, not derived

**Reviewer point.** The perturbative-uniqueness runner labels
"inertia preservation = retained Sylvester invariant = axiom-native
selector". Sylvester's law of inertia is a textbook fact about a
Hermitian form; it does NOT establish that the physical live sheet
must be the baseline-connected component of the caustic complement.
That selection is a post-axiom input.

**Option-A fix.**

1. **Runner Part 3 relabeled as branch-choice admissibility rule.**
 All Part 3 PASS labels rewritten:
 - *"Under imposed branch-choice rule: exactly one in-chamber basin
   is admissible"*
 - *"Admissible (under imposed rule) basin preserves signature (2, 0, 1)"*
 - *"Consistency: Frobenius scale picks the same basin as the imposed
   branch-choice rule"*
 No algorithmic content is changed; only the labeling is demoted.

2. **Note retitled and rewritten.** Title rewritten from *"Retained
 Basin-Uniqueness via Inertia Preservation on the Source Branch"* to
 *"Conditional Basin-Uniqueness via an Imposed Branch-Choice
 Admissibility Rule"*. Status block:
 > *Sylvester's `signature` **is** an algebraic congruence-invariant
 > of a Hermitian form, but that does NOT derive the selection of
 > the baseline-connected branch as the physical one. That choice
 > is the load-bearing non-retained ingredient.*

 The "Theorem (Inertia-Preservation Basin-Uniqueness)" heading is
 rewritten to *"Statement (Basin-Uniqueness Under the Imposed
 Branch-Choice Rule; NOT a retained theorem)"*. The "previous-upgrade
 notice" now withdraws the earlier first-pass inertia promotion
 rather than re-asserting it.

3. **Flagship note coverage row** for the perturbative runner is
 relabeled "branch-choice rule (conditional admissibility)" with
 result column explicit: *"The rule itself is NOT a retained theorem
 on this branch (Option B open item)."*

Option B (derive, on the live sheet, why the baseline-connected branch
must be the physical live sheet — e.g. via a live-sheet Schur
argument or a transport/holonomy route) is a separate open item.

### Blocker 3 — Flagship closure headline `CLOSED` too strong

**Reviewer point.** With the Schur premise and inertia-selector both
non-retained, the flagship closure headline `CLOSED` overstates the
actual claim.

**Option-A fix.**

1. **Flagship closure review note retitled.** From *"DM Flagship Gate
 Closure Review"* to *"DM Flagship Gate — Conditional / Support
 Closure Review"*. Status block now reads:
 > **Status:** `CONDITIONAL / SUPPORT closure` — NOT unconditionally
 > `CLOSED` on the current branch tip. Two load-bearing non-retained
 > ingredients are explicit: (a) the imposed branch-choice
 > admissibility rule; (b) the SM-canonical `q_H = 0`.

2. **"Position on flagship paper surface" rewritten.** Now reads:
 > The DM flagship gate is **NOT** declared CLOSED on the current
 > branch tip. Its honest current status is **conditional / support
 > closure**, because two load-bearing ingredients are non-retained:
 > the imposed branch-choice admissibility rule, and `q_H = 0`.

3. **Runner coverage row 14** (the PMNS closure runner) relabeled
 from the previous `CLOSED` column to
 *"**CONDITIONAL / SUPPORT CLOSURE** — Retained PMNS-as-f(H) map
 + observational chamber pin, conditional on the imposed
 branch-choice admissibility rule and `q_H = 0`, `σ_hier = (2,1,0)`,
 upper octant"*.

4. **"What this file must never say" rewritten** to prohibit
 downstream language saying "flagship gate CLOSED", "retained
 Sylvester inertia selector", "Schur-derived live-sheet curvature",
 etc. Each of the three companion notes (Schur, perturbative, PMNS
 closure) has an equivalent prohibition block.

### Branch hygiene — rebased onto latest `origin/main`

The previous branch tip (`g1-old-tip-5c70c15d`) contained 31 G1-added
files *and* 43 shared-file modifications that were unrelated
regressions from the previous session. The branch was reset to
`origin/main` (`e880d45b`) and only the 31 G1-added files were
re-staged. The 43 regressed shared-file mods have been dropped
entirely.

Staged set on `claude/g1-complete`:

- 14 new runners (`scripts/frontier_*.py`)
- 16 new theorem/note files (`docs/*_NOTE_2026-04-17.md` + canonical-harness-index additions for the two G1 rows)
- `REVIEWER_RESPONSE_2026-04-17.md` (this file)
- `review.md` (reviewer's carry-in)

No CKM / YT / Higgs / evanescent / charged-lepton file regressions
remain on the branch.

## What this resubmission positively claims

1. **14 G1 runners pass** at `PASS = 429, FAIL = 0` total on the
 current surface, with all non-retained ingredients explicitly
 labeled at the PASS line.

2. **Nine obstruction theorems** (rows 2-10) are unchanged and
 retained-grade: info-geometric selection obstruction, cubic-
 variational obstruction, Z_3 parity-split, transport chamber-
 blindness, parity-mixing selection obstruction, observable-bank
 exhaustion (P1/P2/P3 stratification), quartic-isotropy / U(2)
 obstruction, microscopic-polynomial impossibility, bifundamental-
 invariance obstruction.

3. **The PMNS-as-f(H) map** `(m, δ, q_+) → (θ_12, θ_13, θ_23, δ_CP)`
 is built explicitly as an `f(H)` map from retained inputs. The
 MAP itself is theorem-grade; the CLOSURE (chamber pin) is
 conditional / support.

4. **The chamber pin**
 `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` matches
 NuFit 5.3 NO 3-σ in all 9 entries of `|U_PMNS|` and predicts
 `sin δ_CP = −0.9874` — under the imposed branch-choice rule,
 `q_H = 0`, and `σ_hier = (2, 1, 0)`.

5. **Two falsifiable CONDITIONAL predictions** are produced:
 `sin δ_CP = −0.9874 ± resolution` and `sin² θ_23 > 0.5409`
 (upper-octant threshold), testable at DUNE / JUNO / Hyper-K.

## What this resubmission does NOT claim

1. That the DM flagship gate is `CLOSED` (it is conditional / support
 on this branch).
2. That the Schur conditional fires on the live sheet (it does not;
 Part 6 witness verifies).
3. That the inertia-preservation selector is a retained theorem (it
 is an imposed branch-choice admissibility rule).
4. That `q_H` is derived from the axiom (it is the SM-canonical
 assignment).
5. That the chamber pin is unconditionally unique (uniqueness holds
 only under the three load-bearing conditionals).

## Option B — open path to unconditional retained closure

An Option-B upgrade of the DM flagship gate to unconditionally
`CLOSED` on the retained surface requires closing the two
non-retained load-bearing ingredients:

(i) **Derive the branch-choice rule.** Show, on the live source-
oriented sheet, why the physical live sheet must be the
baseline-connected component of the caustic complement. The natural
candidate is a live-sheet Schur-type argument that derives the
commutation premise from retained structure (transport? holonomy?
consistency conditions?).

(ii) **Derive `q_H = 0`** from the retained atlas, rather than
accepting it as SM-canonical.

Either of these closing would allow relabeling the flagship headline
from `conditional / support` to `CLOSED` without the Option-A
honest-label demotions. This is flagged as a forward work item; the
current branch stands as a conditional / support closure.

## Acknowledgements

The reviewer's objections on Blockers 1 and 2 are correct and the
Option-A demotions applied here are the honest way to reconcile the
technical content with the labeling. The runner infrastructure and
the `f(H)` map construction are unchanged; only the retained-grade
labels have been demoted to conditional / support. No merged content
is lost; no retained theorems are disturbed; two load-bearing
non-retained ingredients are now explicit in the runner PASS lines
and in the companion notes.
