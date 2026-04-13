# Codex Review State

**Date:** 2026-04-13  
**Primary audited source:** `origin/codex/review-active`  
**Canonical claims ledger:** `origin/codex/publication-prep`

If any older note, scorecard, packet, or summary conflicts with this file, this
file wins.

## Authority stack

Use these as the real Codex authority documents:

1. [/private/tmp/physics-review-active/docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md](/private/tmp/physics-review-active/docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md)
2. [/private/tmp/physics-review-active/docs/FULL_CLAIM_LEDGER.md](/private/tmp/physics-review-active/docs/FULL_CLAIM_LEDGER.md)
3. [/private/tmp/physics-publication-prep/docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md](/private/tmp/physics-publication-prep/docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md)

The publication-prep ledger is the canonical place where every paper-facing
claim must end up as:

- promoted
- bounded/open
- candidate-missed
- off-scope historical
- stale / not-for-paper

## Retained backbone

These are already strong enough for the flagship paper surface:

- framework statement:
  - we take `Cl(3)` on `Z^3` as the physical theory
  - everything else is derived
- weak-field gravity core:
  - Poisson self-consistency / operator-family uniqueness
  - Newton inverse-square law from the lattice Green’s function
- exact native `SU(2)`
- graph-first structural `SU(3)`
- left-handed charge matching on the selected-axis surface
- anomaly-forced `3+1`
- full-framework one-generation matter closure
- three-generation matter closure in the framework
- exact `I_3 = 0` / no-third-order interference
- exact CPT on the free staggered lattice

## Framework-premise rule

Codex accepts the physical-graph premise at the paper bar, but only in its
proper place:

- acceptable:
  - the framework statement itself says `Cl(3)` on `Z^3` is the physical theory
- not acceptable:
  - introducing “the graph/lattice is physical” later as a new rescue axiom
    for one specific lane

This premise can resolve interpretation-dependent disputes such as
artifact-vs-physical questions. That is why generation physicality is now
closed in the framework.

This premise does **not** by itself close bridge-derivation lanes that still
need real mathematics or physics. In particular, it does not automatically
close:

- gravity extension beyond the retained weak-field core
- `S^3`
- DM relic mapping
- renormalized `y_t`
- CKM / flavor

## Key open items for a clean publication

These are the real remaining publication-critical items.

## Promotion tests

For any live gate, the question is not “is there a stronger note now?” but:

1. what exact claim is being promoted?
2. what file is the authority for that claim?
3. what premise still remains?
4. does the script actually test that premise, or just assert it?
5. if the lane is still bounded, is the residual now sharply narrower?

If those are not answered explicitly, the gate is not promoted.

### 1. Gravity extension beyond the retained weak-field core

Retained already:

- Poisson uniqueness
- Newton law

Still bounded:

- WEP
- time dilation
- conformal metric
- geodesic equation
- light bending
- strong-field / frozen-star / echo package

What would count as promotion:

- a clean exact or tightly bounded sub-bundle with clear assumptions
- or a sharp boundary note that says exactly what gravity claim is retained and
  what remains outside the flagship paper

What does **not** count:

- a blanket “gravity derived” statement that merges weak-field and strong-field
  claims without separating them

Latest gravity-bundle review:

- [GRAVITY_SUB_BUNDLE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/GRAVITY_SUB_BUNDLE_NOTE.md) is directionally good and is the right kind of tier-separation note.
- It usefully distinguishes:
  - retained Newton/Poisson core
  - built-in action identities
  - conditional continuum/eikonal claims
  - strong-field companion work
- But the load-bearing weak point remains the Poisson-forcing step.
  - the note itself marks Poisson as `BOUNDED`
  - the new runner still overstates that step as fully derived
- Current Codex bar:
  - Newton from Poisson is strong
  - broad gravity is still not closed
  - gravity promotion now depends mainly on whether Poisson uniqueness can be
    raised from finite-family/numerical evidence to theorem-grade closure

Paper-safe wording:

> weak-field gravity core retained; broader GR-signature and strong-field
> bundle still bounded.

Latest gravity update:

- [GRAVITY_CLEAN_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/GRAVITY_CLEAN_DERIVATION_NOTE.md)
  and
  [GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
  materially strengthen the weak-field core.
- The real improvement is that the Poisson step is now written as an algebraic
  closure argument rather than only as a finite-family sweep.
- The remaining review issue is precise:
  - do not silently treat `L^{-1} = G_0` as a proved theorem of pure
    mathematics
  - it is the framework’s closure condition for self-consistency
- Safe read:
  - weak-field gravity core is in strong paper shape
  - broad gravity is still not closed

Promotion test for gravity:

- acceptable promotion:
  - weak-field Newton/Poisson core retained with explicit closure-condition
    wording on `L^{-1} = G_0`
- not acceptable promotion:
  - broad gravity closed
  - “zero bounded steps” while the closure condition is still being used as
    framework logic rather than derived pure algebra

### 2. `S^3` compactification / topology closure

Current status:

- still bounded

What improved:

- cap-map uniqueness
- theorem-application notes
- PL / closure-case notes

Why still not promoted:

- the overnight work still depends on a theorem-application chain that Codex
  has not promoted to full flagship closure
- the overnight scorecard and packet overstate this lane

Paper-safe wording:

> `S^3` is a strengthened bounded topology lane, not yet retained closure.

Latest `S^3` update:

- [S3_GENERAL_R_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
  is the strongest topology note so far.
- It gives a real general-`R` theorem chain for the standard cone-capped
  family and is much better than the old `R=2`-only recognition note.
- However, it still does not close the full publication gate because its own
  `What remains open` section keeps:
  - uniqueness of compactification
  - framework-level selection of this compactification
- So:
  - acceptable as a strong theorem for the chosen cone-cap family
  - not yet acceptable as “the full `S^3` compactification lane is closed”

Promotion test for `S^3`:

- acceptable promotion:
  - a theorem that also closes compactification uniqueness / framework-level
    selection
  - or a narrower promoted claim explicitly limited to the chosen cone-cap
    family
- not acceptable promotion:
  - packet says `S^3` closed while the theorem note still lists uniqueness /
    selection as open
  - finite-`R` recognition is used as the theorem itself

### 3. DM relic mapping

Current status:

- still bounded

What improved:

- direct lattice contact / Sommerfeld structure
- Stosszahlansatz tightening
- first Friedmann from Newton tightening
- `sigma v` coefficient work

Why still not promoted:

- Boltzmann/Stosszahlansatz remains bounded at the paper bar
- radiation-era expansion / relic mapping still relies on a bounded bridge
- `g_bare` normalization remains bounded

Paper-safe wording:

> structural DM inputs plus bounded relic mapping; not first-principles relic
> closure.

Latest DM update:

- [DM_CLEAN_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_CLEAN_DERIVATION_NOTE.md)
  is still the strongest honest base note for the lane.
- [DM_STOSSZAHLANSATZ_THEOREM_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_STOSSZAHLANSATZ_THEOREM_NOTE.md)
  is a real sub-result and narrows the coarse-graining objection.
- [DM_K_INDEPENDENCE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_K_INDEPENDENCE_NOTE.md)
  is useful: it can demote `k = 0` from a serious bound to a numerically
  irrelevant sensitivity issue for freeze-out.
- But the lane is still not promoted because the newest “graph-native” closure
  attempt still overreaches:
  - `DM_GRAPH_NATIVE_NOTE.md` says `R` is derived from pure graph theory with
    no imported physics
  - `frontier_dm_graph_native.py` marks cosmological-factor cancellation as
    `EXACT` with a literal `True`, not a real derivation check
  - `DM_G_BARE_FROM_HAMILTONIAN_NOTE.md` says the framework lacks the
    Wilson/path-integral coupling route, while the graph-native chain later
    uses a plaquette/Wilson-style action to compute `alpha_s`
- Safe read:
  - DM is materially strengthened
  - Stosszahlansatz and `k` sensitivity are improved
  - full relic mapping is still bounded

Promotion test for DM:

- acceptable promotion:
  - `g_bare = 1` and the relic-ratio cancellation route are both discharged at
    the same publication bar as the rest of the framework
  - the support script actually checks those claims rather than hardcoding
    exact passes
  - the note/script no longer conflict on whether Wilson/plaquette-style
    structure is available inside the framework
- not acceptable promotion:
  - “pure graph theory / zero imports” wording while `g_bare` is still
    framework-dependent and the ratio-cancellation step is asserted rather
    than derived

### 4. Renormalized `y_t`

Current status:

- still bounded

Closed sub-results:

- bare UV coefficient `1/sqrt(6)`
- `Cl(3)` preservation under block-spin RG
- strong lattice-scale ratio-protection story

Why still not promoted:

- low-energy continuum running is still not paper-safe exact closure
- `alpha_s(M_Pl)` chain is still bounded
- lattice-to-continuum matching remains bounded

Paper-safe wording:

> bare theorem closed; renormalized `y_t` still bounded.

Promotion test for `y_t`:

- acceptable promotion:
  - one authority note identifies exactly one residual and that residual is
    actually computed away
- not acceptable promotion:
  - calling SM running or `alpha_s(M_Pl)` “not an import” as if that alone
    closes the lane

### 5. CKM / flavor

Current status:

- still bounded

What improved overnight:

- NNI / texture / coefficient work
- `c_23` analytic improvement

Why still not promoted:

- Higgs `Z_3` universality is still not flagship-grade closure
- the coefficient story is improved but still not ab initio enough for paper
  promotion
- user explicitly says CKM is still in flight

Paper-safe wording:

> bounded flavor support, not a closed CKM theorem.

Promotion test for CKM:

- acceptable promotion:
  - Higgs `Z_3` / coefficient / hierarchy story is quantitatively closed
- not acceptable promotion:
  - structural flavor support being rephrased as quantitative CKM closure

## Companion claims that matter but are not core promotions

These should stay on the ledger and can support arXiv/SI or future companion
papers, but they do not currently move the flagship core:

- Higgs / Coleman-Weinberg mass lane
- proton lifetime
- Lorentz-violation cubic fingerprint
- BH entropy / RT ratio
- gravitational decoherence
- magnetic monopole mass
- GW echo timing
- cosmology companions (`w=-1`, graviton mass, `Omega_Lambda`, `n_s`)
- gauge-coupling normalization notes

If one of these is strengthened, add it to the ledger. Do not silently drop it.

## What is explicitly not a live blocker anymore

- generation existence
- `SU(3)` structural closure
- anomaly-forced `3+1`
- full-framework RH completion
- exact `I_3 = 0`
- exact CPT

## Unsafe authority docs

These files are not reliable if they conflict with the audited state:

- `docs/MASTER_DERIVATION_SCORECARD.md`
- `docs/OVERNIGHT_WORK_SUMMARY.md`
- `docs/UNIFIED_GATE_CLOSURE_ARGUMENT.md`
- `docs/CODEX_REVIEW_PACKET_2026-04-12.md` if it re-promotes bounded lanes
- `docs/CODEX_REVIEW_PACKET_2026-04-12.md` in its current state if it says:
  - only three live gates remain
  - `S^3` is closed
  - gravity is no longer a live publication-critical lane
- `docs/DM_GRAPH_NATIVE_NOTE.md` if it is used as authority that the DM lane
  is now “pure graph theory” with zero imports
- `docs/DM_G_BARE_FROM_HAMILTONIAN_NOTE.md` if it is used to upgrade
  `g_bare = 1` to exact without resolving its tension with later
  plaquette/Wilson-style `alpha_s` steps
- `scripts/frontier_dm_graph_native.py` if it is used as proof that
  cosmological-factor cancellation is exact when that step is currently
  asserted by a hardcoded pass rather than derived
- any `*_FULL_CLOSURE_*` note for `S^3`, DM, `y_t`, or gauge couplings
- any note that says “Born rule derived” instead of exact `I_3 = 0`
- `scripts/frontier_gravity_poisson_derived.py` if it is used as proof that
  Poisson uniqueness is theorem-grade without a universal uniqueness proof
- `docs/S3_RECOGNITION_NOTE.md` and `scripts/frontier_s3_recognition.py` if
  they are used as anything more than bounded `R=2` support
- `docs/GRAVITY_COMPLETE_CHAIN.md` if it is used to flatten the bounded
  Poisson-forcing step into an all-exact gravity derivation
- `docs/GR_SIGNATURES_DERIVED_NOTE.md` if it is used to promote geodesic / GW
  sub-results without carrying their continuum-limit and wave-promotion
  assumptions

## Hard “do not overclaim” list

Do not say:

- `S^3` closed
- DM relic mapping closed
- renormalized `y_t` closed
- CKM closed
- broad gravity closed
- Born rule derived
- generation closed because of the EWSB cascade
- RH sector derived from the spatial graph alone

Also do not say:

- Poisson uniqueness fully derived from a finite operator-family sweep
- the full self-consistency `=>` Poisson step is a pure theorem with zero
  framework-level closure condition
- `R = Omega_DM/Omega_b` derived from pure graph theory with zero imports
  unless the ratio-cancellation and `g_bare` steps are actually discharged at
  the paper bar
- geodesic / GW sub-bundle fully derived without noting the conformal-metric,
  WKB, or d'Alembertian-promotion assumptions
- strong-field / frozen-star / echo package is part of the retained flagship
  core

## The current Codex publication bar

Before a claim is promoted into the flagship paper surface, it must either:

1. already be retained in the authority docs above, or
2. be added to the canonical ledger with honest bounded wording, or
3. be explicitly labeled off-scope / companion / stale

## Immediate execution map

If Claude wants the shortest path to useful work:

1. **Gravity**
   - either make the weak-field note honest on the closure-condition status
   - or close a broader gravity sub-bundle with assumptions carried explicitly

2. **S^3**
   - either close uniqueness / selection
   - or rewrite the packet and lane notes so the family theorem is promoted
     without overstating full compactification closure

3. **DM**
   - either reconcile `g_bare` / Wilson-action tension and derive the ratio
     cancellation properly
   - or keep the lane bounded and preserve only the sharpened sub-results

4. **y_t**
   - either compute away the last residual
   - or keep one sharp bounded authority note

5. **CKM**
   - only pursue if a real quantitative closure route exists

If a claim is not on the ledger, add it before using it in a paper-facing way.
