# Repo Landing Surface Review -- 2026-04-14

External-eye review of the `cl3-lattice-framework` repository as a first-time
visitor would encounter it. Covers: interest level, impact potential, and the
biggest gaps a reviewer or referee would raise.

**Revision 3** (post-framing pass): updated after Codex sharpened the README,
START_HERE, CURRENT_FLAGSHIP_ENTRYPOINT, EXTERNAL_REVIEWER_GUIDE, and both
draft manuscripts. Papers have not been written yet (the drafts are structured
outlines, not finished manuscripts); this review assesses the repo surface and
its supporting evidence.

---

## How Interesting Is This Paper?

**Very interesting -- 8.5/10.**

The core idea -- take Cl(3) on Z^3 literally as the physical theory (not a
regulator) and derive everything from it -- is genuinely novel. Most lattice
approaches treat the lattice as an approximation to continuum physics. This
inverts the logic: the lattice *is* the physics. If the claims hold, this is a
fundamentally new approach to unification.

The scope is ambitious: gravity, gauge structure, spacetime dimension, matter
content, and electroweak scale all from one combinatorial object. The structural
results (SU(2) from bivectors, 3+1 from anomaly cancellation, v within 0.46%)
are non-trivial and would catch the attention of anyone in mathematical/lattice
physics.

The breadth of the bounded portfolio (DM ratio, alpha_s, m_t, CKM magnitudes,
cosmology, Higgs mass window, proton lifetime, Lorentz violation, monopole mass,
BH entropy) gives the framework genuine phenomenological surface area, even
where results remain conditional.

---

## How Impactful Would It Be?

**If the retained claims survive peer review: very high impact (Nature Physics /
PRL tier).**

Specifically:

- **Deriving Newton's law** from a self-consistency condition on a discrete
  structure with zero free parameters is a clean, quotable result.
- **Anomaly-forcing d_t = 1** is an elegant argument that the physics community
  would engage with.
- **Electroweak scale within 0.46%** from a lattice determinant is striking.
- **Exact SU(2)** from Cl(3) bivectors is mathematically watertight.
- **15+ quantitative predictions** (even if most are bounded) gives the paper a
  rich observational surface.

**Realistic impact rating: 7--8/10 for retained core alone.** Could be 9+ if
the three gates close.

---

## What Changed In This Pass (Rev 3 vs Rev 2)

Codex addressed several of the front-door issues flagged in revision 2:

1. **README now leads with the research question.** The opening paragraph
   frames this as "a graph-first theoretical physics program built around one
   working axiom" and states the goal (recover gauge/matter/gravity/3+1/EW
   scale). This replaces the old bare bullet list. Status labels
   (retained/bounded/live gate) are defined up front.

2. **START_HERE now has a motivating question.** The blockquote "can a single
   discrete axiom recover a nontrivial unified physics package?" gives a
   newcomer an immediate hook.

3. **CURRENT_FLAGSHIP_ENTRYPOINT now opens with the existential claim.** The
   blockquote "start from the discrete axiom Cl(3) on Z^3, treat the lattice as
   physical rather than as a regulator, and ask how much of observed physics can
   be recovered" is exactly the framing a reviewer needs. Status labels are
   defined inline.

4. **EXTERNAL_REVIEWER_GUIDE now addresses three framing points.** It explains:
   (a) v is a theorem + pinned evaluation, not two separate claims;
   (b) SU(3) is a selector-uniqueness statement, not an arbitrary commutant;
   (c) three generations are physical species, not disposable taste artifacts.
   These are direct responses to the reviewer-attack items flagged in Rev 2.

5. **NATURE_DRAFT and ARXIV_DRAFT are substantially better.** They are still
   structured outlines (not finished papers), but they now contain:
   - An abstract that states retained claims precisely
   - The self-consistency argument framed as "unique fixed point in the audited
     operator family" rather than as a separate postulate
   - A selector-uniqueness argument for SU(3) ("alternative selector families
     fail the same charge and commutant audit")
   - A defense of three generations ("the same selector and charge audit that
     fixes the retained gauge surface also keeps the triplet structure visible")
   - A clear statement that "the claim surface is disciplined and unusually
     strong" followed immediately by "the remaining bridge problems should be
     stated directly"
   - Compact comparative positioning against other programs
   - Explicit negative results in the arXiv draft (Section 5)
   - Strong-field gravity correctly qualified as "not full nonlinear GR in full
     generality" throughout

6. **Publication package README now has "reviewer-facing framing notes."** These
   explain the gravity self-consistency principle, the SU(3) selector-uniqueness
   framing, the three-generation physical-species interpretation, and the v
   theorem + evaluation relationship.

---

## What Now Works Well (Front Door)

- **The research question is front and center.** A visitor immediately
  understands what the program is trying to do.
- **Status labels are defined early.** Retained / bounded / live gate are
  explained before the bullet lists, so a newcomer knows what the categories
  mean.
- **The three hardest reviewer attacks are pre-addressed.** Selector uniqueness,
  taste-as-generations, and the v theorem/evaluation distinction are now
  explicitly framed in the reviewer guide and the pub-package README.
- **The Nature draft reads like a paper outline, not a claim list.** It has an
  abstract, a logical flow, figure callouts, and a conclusion. It still needs
  equations, but the argumentative structure is present.
- **The arXiv draft has honest negative results.** Section 5 ("Negative Results
  That Matter") is rare and strengthens credibility.
- **Strong-field gravity is properly qualified everywhere.** "Not full nonlinear
  GR in full generality" appears consistently across README, START_HERE,
  flagship entrypoint, and both drafts.

---

## What Still Needs Work

### 1. The drafts are outlines, not manuscripts (Still critical, but improving)

The Nature and arXiv drafts now have argumentative structure, but they still
contain zero equations, zero inline derivations, and zero proofs. Every
technical claim defers to an external derivation note or runner script.

For publication, the arXiv draft needs at minimum:
- The Poisson self-consistency argument (the 9-step chain, or at least the key
  steps)
- The anomaly-forces-time proof (the chirality + single-clock argument)
- The observable-principle theorem (additive + CPT-even forces log|det|)
- The hierarchy block calculation (determinant exponent = 16, orbit selection)
- The SU(3) commutant calculation (at least a sketch)
- The S^3 general-R proof (van Kampen + Perelman, compactly)

The Nature draft can be shorter, but it needs at least one worked example
(probably the Poisson chain or the hierarchy calculation) to show a referee that
the math is real.

**Status: upgraded from "critical" to "critical but the scaffold is ready."**

### 2. SU(3) selector uniqueness now has a claim but not a proof

The drafts now say "alternative selector families fail the same charge and
commutant audit." This is the right claim to make. But the proof is not shown
in the manuscript or in the reviewer guide. A referee will ask: how many
selectors were tested? What do the failing ones look like? Is there a
classification theorem or just an enumeration?

**Fix:** The arXiv draft needs either an inline proof sketch or a clear pointer
to the derivation note with enough detail that a reviewer can verify the
uniqueness claim without running the script.

### 3. Three-generation defense is stated but not argued

The drafts now say "the same selector and charge audit that fixes the retained
gauge surface also keeps the triplet structure visible." This is the right
framing. But a lattice QCD practitioner will still ask: if I use rooting, do
the triplet sectors disappear? If they do, your "physical species" claim is
convention-dependent. If they don't, you have a real result.

**Fix:** The paper needs to either (a) show that rooting is inconsistent on
Cl(3), or (b) identify an observable that distinguishes physical generations
from taste artifacts. The current framing asserts but does not demonstrate.

### 4. The v framing is clearer but still risks "exact theorem" misreading

The reviewer guide now explains "v is a theorem plus a pinned numerical
evaluation on the current u_0 / plaquette surface, not two separate claims."
This is correct and much better than before. But "exact theorem" still appears
in the claims table and the Nature draft. A reviewer seeing "exact theorem"
next to a 0.46% error will be confused.

**Fix:** Consider replacing "exact theorem" with "exact hierarchy theorem" or
"derived hierarchy relation" in the claims table. The theorem *is* exact (the
functional form, orbit selection, and selector correction). The number is
derived on a specific plaquette surface. Separating these two in the labeling
prevents misreading.

### 5. Closure condition framing improved but needs more

The drafts now say "Poisson is the unique local fixed point in the audited
operator family" and clarify "self-consistent means the audited local operator
family has a unique fixed point, not a separate postulate." This is better than
"assumed the answer." But the phrase "audited operator family" is still not
defined in the manuscript. What operators are in the family? Why that family?

**Fix:** The arXiv draft should define the operator family explicitly (even if
briefly: "all symmetric local operators up to range R on Z^3") so a reviewer
can evaluate the uniqueness claim.

### 6. Comparative positioning is stated but empty

The Nature draft says "relative to standard discrete-program alternatives, the
present paper should be read narrowly." The arXiv draft says "appropriate
positioning against other discrete or unification programs is compact, not
encyclopedic." Both say "this is not a survey." That is fine positioning
language, but neither draft actually names a single alternative approach.

A reviewer in string theory, LQG, or noncommutative geometry will want to know:
how does this compare? What does Cl(3)/Z^3 do that those programs don't? What
do they do that this program can't? Even two sentences per alternative would
help.

### 7. Figures still do not exist

Both drafts now have explicit figure callouts (Fig. 1--4 plus Extended Data
Fig. 1--2), and the figure plan exists. But the actual figures have not been
generated. This is a practical blocker for any submission.

### 8. The y_t chain is still the weakest link

No changes to the y_t scripts or notes in this pass. The forward-run crash in
`frontier_yt_2loop_chain.py` is still present. The bounded m_t = 169.4 GeV
result (-1.9%) is real but the validation chain backing it needs tightening.

---

## Items From Rev 2 That Are Now Resolved Or Improved

| Issue (Rev 2) | Status (Rev 3) |
|----------------|----------------|
| README title "Physics Repo" tells visitor nothing | **Partially fixed.** Title is still "Physics Repo" but opening paragraph now frames the research question clearly |
| No "why should I care" paragraph | **Fixed.** START_HERE and flagship entrypoint both open with motivating blockquotes |
| Status labels undefined | **Fixed.** Retained/bounded/live gate defined in README, START_HERE, and flagship entrypoint |
| SU(3) selector uniqueness not addressed | **Partially fixed.** Uniqueness claim now stated in drafts and reviewer guide; proof not yet shown |
| Three-generation claim not defended | **Partially fixed.** Physical-species framing now explicit; rooting argument not yet made |
| Strong-field gravity overqualified | **Fixed.** "Not full nonlinear GR in full generality" appears consistently throughout |
| v framing as "exact theorem" misleading | **Partially fixed.** Reviewer guide clarifies theorem + evaluation; "exact theorem" label persists in claims table |
| No comparative positioning | **Partially fixed.** Positioning language exists; specific alternatives not yet named |

---

## Technical Rigor Summary (Unchanged from Rev 2)

| Component | Status | Rigor |
|-----------|--------|-------|
| Newton's law F ~ 1/r^2 | **Derived** | 8.5/10 |
| WEP | **Derived** | 8/10 |
| Time dilation | **Derived** | 8/10 |
| CPT exact (free lattice) | **Derived** | 9.5/10 |
| Anomaly cancellation arithmetic | **Derived** | 9/10 |
| Temporal dimension d_t = 1 | **Derived** | 7.5/10 |
| SU(2) | **Derived** | 9.5/10 |
| SU(3) structural | **Bounded** | 6.5/10 |
| Scalar observable principle | **Derived** (minimal block) | 8.5/10 |
| Hierarchy v_EW | **Predicted** (0.46% error) | 7/10 |
| S^3 topology | **Derived** (general-R proof) | 7.5/10 |
| One-generation closure | **Derived** | 7.5/10 |
| Three generations | **Exact algebra / bounded interpretation** | 6/10 |
| Geodesics and light bending | **Bounded** | 5/10 |
| DM ratio R = 5.48 | **Bounded** (1 assumed param) | 7/10 |
| alpha_s = 0.1181 | **Bounded** | 7/10 |
| m_t = 169.4 GeV (zero-import) | **Bounded** | 5.5/10 |
| m_t = 171.0 GeV (import-allowed) | **Bounded** | 6/10 |
| CKM magnitudes | **Bounded** (V_ub 1.14x PDG) | 6.5/10 |
| Jarlskog invariant | **Bounded** (7x suppressed) | 3/10 |
| Cosmology (Lambda, w, n_s) | **Bounded/conditional** | 4/10 |
| Higgs mass | **Open** | 3/10 |
| BH entropy | **Bounded** (5% from 1/4) | 4/10 |
| Proton lifetime | **Bounded** (imported EFT) | 5/10 |
| Lorentz violation | **Bounded** (well-derived fingerprint) | 7/10 |
| Monopole mass | **Bounded** (imported alpha_EM) | 5/10 |

---

## Computational Honesty Audit (Unchanged from Rev 2)

| Script | Honesty | Independence | Overall |
|--------|---------|-------------|---------|
| frontier_s3_cap_uniqueness.py | YES | YES | 9/10 |
| frontier_s3_general_r.py | YES | YES | 9/10 |
| frontier_dm_relic_paper.py | YES | WEAK (1 assumed) | 7/10 |
| frontier_yt_2loop_chain.py | PARTIAL | WEAK | 5/10 |
| frontier_ckm_mass_basis_nni.py | YES | YES | 9/10 |
| frontier_higgs_mass_derived.py | EXCELLENT | YES | 10/10 |
| frontier_proton_lifetime_derived.py | YES | WEAK (alpha_GUT) | 7/10 |
| frontier_alpha_s_determination.py | EXCELLENT | YES | 9/10 |
| frontier_vertex_power.py | YES | YES | 9/10 |
| frontier_cosmological_constant.py | EXCELLENT | YES | 10/10 |

---

## Overall Rating (Revised)

| Dimension | Rev 2 | Rev 3 | Comment |
|-----------|-------|-------|---------|
| Scientific interest | 8.5/10 | 8.5/10 | Unchanged |
| Retained core rigor | 7.5/10 | 7.5/10 | Unchanged -- no new derivations, just better framing |
| Bounded portfolio quality | 7/10 | 7/10 | Unchanged -- no new results this pass |
| Organizational discipline | 9.5/10 | 9.5/10 | Already excellent; maintained |
| Front-door clarity | 5/10 | 7.5/10 | **Major improvement.** Research question front and center, status labels defined, reviewer attacks pre-addressed |
| Publication readiness (drafts) | 4/10 | 5.5/10 | **Improved.** Drafts now have argumentative structure and abstracts. Still no equations. Scaffold is ready for writing |
| Likely referee survival | 6/10 | 6.5/10 | **Slight improvement.** Selector uniqueness and taste-as-generations are now framed, but not yet proved. Existential defense is now stated up front |

---

## Priority Actions (Updated)

### Highest priority (blockers for any submission)

1. **Write equations into the arXiv draft.** The scaffold is ready. Fill in:
   Poisson chain, anomaly-forces-time proof, observable-principle theorem,
   hierarchy block calculation, SU(3) commutant sketch, S^3 proof sketch.
2. **Generate figures.** Fig. 1--4 and Extended Data Fig. 1--2 are called out
   in both drafts. They need to exist.
3. **Prove SU(3) selector uniqueness** or provide an explicit enumeration of
   tested selectors with their failure modes.

### High priority (would significantly strengthen the paper)

4. **Defend tastes as generations.** Show rooting is inconsistent on Cl(3), or
   identify a physical observable that distinguishes the interpretations.
5. **Define "audited operator family" explicitly** so the Poisson uniqueness
   claim is verifiable from the manuscript alone.
6. **Replace "exact theorem" label** for v in the claims table with "exact
   hierarchy theorem" or similar, to separate the theorem from the numerical
   evaluation.
7. **Name specific alternative programs** in the comparative positioning
   (string theory, LQG, Connes NCG, causal sets -- even two sentences each).

### Medium priority (would improve robustness)

8. **Fix the y_t forward-run crash** or explain why backward-run validation is
   sufficient and independent.
9. **Address the Jarlskog 7x suppression** -- this is an honest failure that
   needs at least a hypothesis for what is missing.
10. **Tighten cosmology companion framing** to flag explicitly where matches are
    by construction vs. genuine predictions.
