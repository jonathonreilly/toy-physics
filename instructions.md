# Claude Execution Instructions

**Date:** 2026-04-13  
**Branch:** `claude/youthful-neumann`

Read only these two files before working:

1. `instructions.md`
2. `review.md`

If an older note, scorecard, packet, or script conflicts with `review.md`, then
`review.md` wins.

## Mission

Use Claude time on execution and theorem-boundary work for the remaining
publication-critical items. Codex will handle audit, promotion, and paper
authority.

## Where to land work

Land all real work here and push it:

- branch: `claude/youthful-neumann`
- remote: `origin/claude/youthful-neumann`

Do not leave the actual result only as local notes or only in a scorecard.
If you fix a claim, fix the pushed note/script on this branch.

## Publication standard

A lane is `closed` only if all of the following are true:

1. the theorem surface is genuinely first-principles at the paper bar
2. the note, script, and packet all say the same thing
3. the note states assumptions explicitly and narrowly
4. the script separates exact checks from bounded/model checks
5. no hidden imported physics or fitted coefficient is being re-labeled as
   “derived”

If any of those fail, the lane stays `bounded` or `open`.

## Current priority order

1. **Gravity extension beyond the retained weak-field core**
   - already retained: weak-field Newton law on `Z^3`
   - new useful work:
     - `GRAVITY_CLEAN_DERIVATION_NOTE.md`
     - `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`
   - these significantly strengthen the weak-field gravity writeup
   - open for promotion: broader gravity bundle only
   - target items:
     - WEP / time dilation / conformal metric / geodesic / light bending
     - strong-field / frozen-star / echo package
   - do not spend time re-proving Newton unless needed for a new closure step
   - the current load-bearing weak point is how strongly you phrase the full
     self-consistency `=>` Poisson step on the full framework surface
   - the new clean/full-self-consistency notes are acceptable as a strong
     weak-field presentation only if they carry the closure-condition status
     honestly
   - a finite-family sweep or mismatch residual is not enough to call Poisson
     uniqueness “derived for all local operators”
   - if you cannot defend `L^{-1} = G_0` as the framework’s own closure
     condition cleanly, do not call the whole weak-field chain “zero bounded”
   - broad gravity is still separate and still open

2. **`S^3` compactification / topology closure**
   - new useful work:
     - `S3_GENERAL_R_DERIVATION_NOTE.md`
     - `S3_RECOGNITION_GENERAL_NOTE.md`
     - `S3_SHELLABILITY_NOTE.md`
   - `S3_GENERAL_R_DERIVATION_NOTE.md` is a real strengthening and should be
     the main authority note for this lane
   - however the full gate is still not closed because compactification
     uniqueness / framework-level selection remains open
   - `S3_RECOGNITION_GENERAL_NOTE.md` is bounded computational support
   - do not use `S3_RECOGNITION_NOTE.md` / `frontier_s3_recognition.py` as the
     main authority anymore except as old `R = 2` support
   - do not say “the full `S^3` lane is closed” unless uniqueness/selection is
     explicitly discharged too

3. **DM relic mapping**
   - useful new work:
     - `DM_CLEAN_DERIVATION_NOTE.md`
     - `DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
     - `DM_K_INDEPENDENCE_NOTE.md`
   - those are real improvements
   - however the lane is still not closed at the paper bar
   - do not use the newest closure rhetoric as authority:
     - `DM_GRAPH_NATIVE_NOTE.md`
     - `DM_G_BARE_FROM_HAMILTONIAN_NOTE.md`
     - `DM_CLOSURE_CASE_NOTE.md`
     - `scripts/frontier_dm_graph_native.py`
   - specific current objections:
     - `g_bare = 1` is still not promoted to exact at the publication bar
     - `frontier_dm_graph_native.py` marks cosmological-factor cancellation as
       `EXACT` with a literal hardcoded pass rather than a derived check
     - the “pure graph theory / no imports” wording is still too strong
     - `DM_G_BARE_FROM_HAMILTONIAN_NOTE.md` says the framework lacks the
       Wilson/path-integral coupling route, while the graph-native chain later
       uses a plaquette/Wilson-style action to compute `alpha_s`
   - the current safe status is:
     - structural DM inputs materially strengthened
     - Stosszahlansatz improved
     - `k = 0` sensitivity likely demoted to negligible
     - full relic mapping still bounded

4. **Renormalized `y_t` matching**
   - the current safe status is:
     - bare UV theorem closed
     - `Cl(3)` preservation under RG exact
     - low-energy running, `alpha_s(M_Pl)`, and lattice-to-continuum matching
       still bounded
   - do not collapse those bounded pieces into “just mathematics” unless the
     actual note/script closes them at the paper bar

5. **CKM / flavor**
   - only if there is a real route to closure
   - user says CKM is still in flight; do not force closure rhetoric

6. **Companion predictions**
   - Higgs mass
   - proton lifetime
   - Lorentz violation
   - BH entropy
   - gravitational decoherence
   - magnetic monopoles
   - GW echo
   These are worth tightening, but they are not allowed to displace the live
   publication gates.

## What counts as useful work

Useful:

- a new theorem that actually narrows one of the key gates
- a new obstruction that sharply explains why a lane remains bounded
- a clean note that splits “retained exact core” from “bounded extension”
- a script whose final status matches the note honestly

Not useful:

- scorecards that claim more than the underlying notes/scripts
- “all gates closed” arguments built by collapsing bounded imports into rhetoric
- relitigating already-retained generation or `SU(3)` structure
- renaming a bounded phenomenology chain as a derivation

## Required output format for any serious attempt

For each lane touched, produce:

1. one note in `docs/`
2. one runnable script in `scripts/`

The note must contain:

1. `Status`
2. `Theorem / Claim`
3. `Assumptions`
4. `What Is Actually Proved`
5. `What Remains Open`
6. `How This Changes The Paper`
7. `Commands Run`

The script must:

- end with a clear status summary
- separate exact checks from bounded/model checks
- avoid unconditional theorem passes for things that were only argued in prose

## Mandatory handoff rule

Before asking Codex to review:

1. commit on `claude/youthful-neumann`
2. push `origin/claude/youthful-neumann`
3. update `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

The packet is acceptable only if it matches `review.md` and the touched
note/script pair exactly. If it overstates anything, it is not authority.
Right now the packet is still not authority if it says:
- only three live gates remain
- `S^3` is closed
- gravity is not a live publication-critical gate

## Hard constraints

1. Do not call `S^3`, DM relic mapping, renormalized `y_t`, CKM, or the broad
   gravity bundle `closed` unless the underlying runner and note support that
   status directly.

1a. For gravity specifically:
   - do not use `frontier_gravity_poisson_derived.py` as proof that the full
     self-consistency surface uniquely forces Poisson
   - the narrowed Poisson uniqueness theorem is acceptable as an exact
     sub-result; the broader forcing claim is not yet closed
   - `time dilation` and eikonal `WEP` are not standalone closure wins; they
     are built-in action identities once `S = L(1-f)` is accepted
   - geodesic / conformal-metric / GW results must carry their continuum-limit,
     WKB, or wave-equation-promotion assumptions explicitly
   - strong-field / frozen-star / echo work is companion-level unless it
     actually closes a sharp theorem surface

1b. For `S^3` specifically:
   - do not present an `R = 2` or finite-`R` recognition run as the general
     theorem itself
   - `S3_GENERAL_R_DERIVATION_NOTE.md` is the main theorem note
   - `S3_RECOGNITION_GENERAL_NOTE.md` is bounded computational support
   - the remaining live issue is compactification uniqueness / physical
     selection, not the old `R = 2` limitation

1c. For DM specifically:
   - do not label Stosszahlansatz, Boltzmann coarse-graining, or the
     `sigma v` coefficient as theorem-grade derived if the supporting step
     still leans on factorization arguments, coarse-graining heuristics, or
     standard threshold normalization structure

1d. For renormalized `y_t` specifically:
   - do not say SM running, the `alpha_s(M_Pl)` chain, or matching are fully
     discharged just because they operate on derived inputs
   - the current audit still keeps those pieces bounded

2. Do not use “Born rule derived.”
   Safe statement:
   - exact `I_3 = 0` / no-third-order interference

3. Do not use the physical-lattice premise as a late standalone `A5` add-on.
   The framework statement already says:
   - `Cl(3)` on `Z^3` is the physical theory

4. Do not re-open generation existence.
   Generation is closed in the framework.
   Only hierarchy/flavor remains bounded.

5. Do not treat `SU(3)` as a live blocker unless a concrete new issue appears.

## Short paper-safe reminders

- retained gravity claim:
  - weak-field Poisson / Newton core
- retained matter claim:
  - full-framework one-generation closure
  - three-generation matter structure in the framework
- retained exact companions:
  - exact `I_3 = 0`
  - exact CPT

Everything else should be tested against `review.md` before it is promoted.
