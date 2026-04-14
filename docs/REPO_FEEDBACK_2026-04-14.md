# Repo Landing Surface Review -- 2026-04-14

External-eye review of the `cl3-lattice-framework` repository as a first-time
visitor would encounter it. Covers: interest level, impact potential, and the
biggest gaps a reviewer or referee would raise.

**Revision 2** (post-Codex cleanup): updated after 20+ new derivation notes,
expanded script coverage, tighter publication matrix, and stale-authority audit
landed on `main`. Papers have not been written yet; this review assesses the
repo and its supporting evidence, not a manuscript.

---

## How Interesting Is This Paper?

**Very interesting -- 8.5/10.** (Up from 8 after the expanded companion
portfolio.)

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
BH entropy) now gives the framework genuine phenomenological surface area, even
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

## What Changed After Codex Cleanup

- **16 new derivation/authority notes** now back every bounded companion row
  (DM relic, y_t closure, CKM mass-basis NNI, Higgs mass, proton lifetime,
  Lorentz violation, monopole, BH entropy, cosmological constant, dark energy
  EOS, primordial spectrum, S^3 cap uniqueness, S^3 general-R, y_t vertex
  power, y_t gauge crossover theorem, y_t zero-import closure).
- **~20 new frontier scripts** with genuine computational verification.
- **m_t zero-import improved** from 165.4 GeV (-4.2%) to 169.4 GeV (-1.9%) via
  a 2-loop chain.
- **Stale-authority audit** quarantines old docs that previously cluttered the
  claim surface.
- **Publication matrix** now has every row cross-referenced to authority note +
  runner + frozen-out registry entry.
- Every claim in the matrix now has both a derivation note AND a runner script.

---

## The Front Door Experience

### What works well

- The README -> CURRENT_FLAGSHIP_ENTRYPOINT -> publication package path is clear
  and disciplined.
- The four-tier system (retained / bounded / open / frozen-out) is now backed by
  actual authority notes for every row.
- Every claim in the matrix has both a derivation note AND a runner script.
  That dual-evidence contract is rare and impressive.
- The FROZEN_OUT_REGISTRY and STALE_AUTHORITY_AUDIT are genuine quality controls
  not seen in other physics repos.
- The EXTERNAL_REVIEWER_GUIDE gives a clean three-tier orientation.

### What still feels off

- The README title is "Physics Repo" -- tells a visitor nothing. The framework
  sentence ("We take Cl(3) on Z^3 as the physical theory") is buried in the
  publication package README, not up front.
- A visitor's first impression is a bullet list of claims with no compelling
  hook. There is no abstract, no "here is why you should care" paragraph.
- The sheer volume of docs (40+ in `/docs/`, 22 in `publication/ci3_z3/`) is
  intimidating without a single one-page summary that a newcomer could read in
  five minutes.

---

## What Is Genuinely Strong

### Retained results that would survive hostile review

1. **Newton's law from self-consistency.** The 9-step Poisson chain is clean,
   zero free parameters, numerically verified. The closure condition L^{-1} =
   G_0 is a physical postulate, not a theorem, but it is a good postulate --
   transparent and minimal. (8.5/10)

2. **Exact SU(2).** Trivially correct from Cl(3) bivectors. Unassailable.
   (9.5/10)

3. **CPT exact.** Verified to machine precision on the free lattice. Modest
   claim, modest scope, bulletproof within that scope. (9.5/10)

4. **Anomaly-forced d_t = 1.** The logic (anomaly cancellation + chirality
   requires even total d + single-clock excludes d_t > 1) is sound. The
   single-clock assumption is stated, not smuggled. (7.5/10)

5. **Electroweak scale v = 245.08 GeV.** The observable principle (additive +
   CPT-even forces log|det|) is mathematically forced on the minimal block. The
   0.46% residual lives in the u_0 baseline. The orbit selection L_t = 4 is
   unique. This is the most quotable result. (8.5/10 for the derivation
   structure; see caveats on framing below.)

6. **S^3 topology.** The general-R proof (van Kampen + Perelman) is rigorous.
   Cap uniqueness is mostly solid but relies on boundary chi = 2 being verified
   only for R <= 10, not proved in general. (7.5/10)

7. **WEP and time dilation.** Genuine weak-field corollaries of the derived
   action. k-independence is non-trivial. (8/10)

### Computational standouts

Two scripts deserve special mention as models of honest scientific reporting:

- `frontier_higgs_mass_derived.py` explicitly marks its own Tier 3 as FAIL,
  scores itself 85%. This is what intellectual honesty looks like.
- `frontier_cosmological_constant.py` concludes "the framework does NOT solve
  the cosmological constant problem." A negative result reported honestly.

Overall, 7 of 10 sampled scripts perform genuine numerical computation with
honest PASS/FAIL/BOUNDED classification.

---

## What Is Honestly Bounded (and the docs say so)

- **DM ratio R = 5.48 vs 5.47.** Good match, but g_bare = 1 is assumed, not
  derived. The DM_RELIC_PAPER_NOTE has the best provenance labeling in the repo
  (7 NATIVE / 5 DERIVED / 1 ASSUMED / 2 IMPORTED).
- **alpha_s(M_Z) = 0.1181.** Multiple independent methods converge. Real
  result, bounded by the coupling-map assumption.
- **m_t = 169.4 GeV (zero-import).** Improved from 165.4, now -1.9% off. But
  the 2-loop forward run crashes and success depends on the backward run. The
  y_t chain is the weakest computational link.
- **CKM magnitudes.** V_us and V_cb are excellent. V_ub improved from 5.3x PDG
  to 1.14x via mass-basis NNI normalization. But Jarlskog invariant is still
  suppressed 7x. The framework is missing something fundamental about CP
  violation.
- **Cosmology companions.** Lambda, w = -1, Omega_Lambda, n_s all follow from
  defining dark energy as the S^3 spectral gap. The arithmetic works but these
  are parameterizations, not predictions. Correctly frozen out (F04).
- **Higgs mass.** v is derived but m_H is not. The Coleman-Weinberg window
  gives the right order of magnitude with m_H/m_W ~ 1.85 (SM value 1.56, 19%
  high). Correctly classified as open/bounded.

---

## What Is Weaker Than The Docs Suggest

### 1. "Zero-import" language is too generous

Several notes claim "zero imports" while using standard 2-loop SM RGE running,
Lepage-Mackenzie coefficients, and V-to-MSbar conversion formulas. These are
standard tools, but they are still external theoretical infrastructure. The
honest framing is "zero *electroweak* imports," not "zero imports."

### 2. Cosmological predictions are parameterizations

Lambda = 3/R_H^2 gives Lambda to within factor 1.46 of observation. But the
remaining factor 1.46 is just 1/Omega_Lambda -- circular if you already need the
matter content. The coincidence-problem "resolution" (R = R_H by fiat) is
asserting a solution, not deriving one. The quantitative summary table presents
these as "near-match" without flagging the by-construction aspect.

### 3. BH entropy S/S_max ~ 0.24

Presented as "5.4% from 1/4" but really a 5% numerical coincidence on a 2D
lattice. No derivation of why the RT ratio should be 1/4. The identification
(lattice entanglement = gravity) is asserted, not proved.

### 4. Graph-first SU(3) selector

Still the same gap: the cube-shift selector is introduced geometrically but not
forced by Cl(3) + Z^3 alone. No enumeration of alternative selectors. This will
be the first thing a lattice gauge theorist attacks.

### 5. Three generations

The orbit algebra 8 = 1 + 1 + 3 + 3 is exact. But calling this "three
generations" rather than "staggered tastes" is the single boldest interpretive
choice in the framework, and the docs do not adequately defend it. Standard
lattice QCD treats this exact same structure as an artifact to be removed via
rooting. You need a killer argument for why it is physical here.

### 6. The y_t chain needs work

`frontier_yt_2loop_chain.py` is the weakest script in the set. The forward
integration (Approach B) crashes. Success depends entirely on the backward run
with CMT-derived coupling as input, then recovering the Ward identity -- which
is somewhat circular. The 2% pass criterion is asserted, not derived. This
script backs one of the three live gates and needs tightening before anyone
external runs it.

---

## What a Referee Would Hit Hardest

In priority order (updated from first review):

### 1. "Why is your lattice physical and not a regulator?"

This is the existential question. Every lattice QFT paper in history treats the
lattice as a computational tool. This paper claims it is ontological. The
defense needs to be front and center in any manuscript, not buried in SI
framing. Without a clear answer, a referee will not engage with the rest.

### 2. "You derive gauge groups but not masses or mixing -- what does this predict?"

The retained core gives structure (gauge groups, spacetime dimension, topology,
electroweak scale). The bounded portfolio gives numbers (masses, mixing,
cosmology). But the numbers all require imports or assumptions. The gap between
structure and phenomenology is the real vulnerability.

### 3. SU(3) selector uniqueness

How many selectors exist on the cube-shift graph? What do the others give? If
only one gives SU(3), prove it. If many do, explain why this one is physical.

### 4. Staggered tastes as generations

Every lattice practitioner will say "those are doublers, not generations." The
paper needs either: (a) a physical observable that distinguishes the
interpretation, or (b) a proof that the standard rooting/taste-removal procedure
fails on Cl(3).

### 5. The 0.46% -- prediction or fit?

If u_0 is imported, the electroweak scale result is a one-parameter fit, not a
zero-parameter prediction. The derivation of the functional form and orbit
selection is genuine, but the headline number depends on the baseline. The
framing as "exact theorem" will draw fire.

### 6. Closure condition L^{-1} = G_0

The linchpin of gravity. Physically motivated, but a postulate, not a theorem.
A hostile reviewer will say "you assumed Poisson." The defense should frame it
as the framework's defining physical postulate and argue minimality/uniqueness.

### 7. Continuum limit

If the lattice is physical, what sets the lattice spacing? Is it Planck-scale?
How do continuum-looking phenomena (geodesics, light bending, Riemannian
geometry) emerge? This is not addressed in the current docs.

### 8. No comparison with existing approaches

No discussion of string theory, loop quantum gravity, Connes' noncommutative
geometry, or other discrete/algebraic approaches to unification. Reviewers in
those communities will want positioning.

---

## Technical Rigor Summary (Revised)

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

## Computational Honesty Audit

Scripts were sampled and graded on: whether they compute or just print,
independence of verification, honest PASS/FAIL/BOUNDED classification, and
absence of tautological hardcoded targets.

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

## Strengths Worth Highlighting

1. **Exceptional organizational transparency.** The retained / bounded /
   frozen-out taxonomy is better than most published theoretical physics. The
   FROZEN_OUT_REGISTRY and STALE_AUTHORITY_AUDIT are genuine quality controls.
2. **No circular reasoning detected** in the core derivation chain. The
   framework carefully distinguishes verification from derivation.
3. **Computational verification is thorough.** Machine-precision checks, honest
   EXACT vs BOUNDED classification in every runner. Two scripts
   (higgs_mass_derived, cosmological_constant) set the standard for honest
   self-assessment.
4. **Self-aware about gaps.** The three live gates are explicitly named and
   honestly bounded. No overclaiming in the retained core.
5. **Zero adjustable parameters** in the retained core (conditional on the
   self-consistency closure axiom and the graph-first selector).
6. **Every claim is dual-evidenced.** The derivation/validation map enforces
   one authority note + one runner per claim. This contract is rare in
   theoretical physics.

---

## Overall Rating (Revised)

| Dimension | Score | Comment |
|-----------|-------|---------|
| Scientific interest | 8.5/10 | Up from 8. Expanded companion portfolio shows genuine breadth |
| Retained core rigor | 7.5/10 | Gravity, SU(2), CPT, anomaly-forced 3+1 are solid. SU(3) and three-gen are weak links |
| Bounded portfolio quality | 7/10 | Improved. DM, alpha_s, CKM are real results. y_t chain needs work |
| Organizational discipline | 9.5/10 | Best seen in a physics repo. Frozen-out registry and stale audit are exceptional |
| Publication readiness | 4/10 | No manuscript exists. The infrastructure is ready; the writing is not |
| Likely referee survival | 6/10 | The existential questions (lattice-as-physics, taste-as-generations, SU(3) uniqueness) are not yet answered |

**Net:** The science got meaningfully stronger with the Codex cleanup. The repo
is now a well-organized research program with genuine results, honest
self-assessment, and clear open problems. The gap is no longer "do you have
results?" -- it is "can you write a paper that survives the five questions
above?"

---

## Priority Actions for Manuscript

1. **Write the paper.** The infrastructure is ready. The arXiv draft needs
   actual equations -- at minimum the Poisson chain, the anomaly-forces-time
   proof, the observable-principle theorem, and the hierarchy block calculation.
2. **Lead with the existential defense.** "Why is the lattice physical?" must
   be the first thing a reader encounters, not an afterthought.
3. **Address SU(3) selector uniqueness.** Enumerate alternatives or prove the
   selector is forced.
4. **Defend tastes as generations.** Either show rooting fails on Cl(3) or
   identify an observable that distinguishes the interpretations.
5. **Fix the "exact theorem" framing for v.** Separate what is derived
   (functional form, orbit, selector correction) from what is imported (u_0).
6. **Generate figures.** Derivation flowchart, lattice/taste diagrams,
   numerical convergence plots.
7. **Add positioning.** Compare with string theory, LQG, noncommutative
   geometry, other discrete models.
8. **Tighten the y_t chain.** Fix or explain the forward-run crash. Justify
   the pass criterion independently.
