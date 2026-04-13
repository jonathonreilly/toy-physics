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
   - already retained: Poisson self-consistency + Newton law on `Z^3`
   - open for promotion: broader gravity bundle only
   - target items:
     - WEP / time dilation / conformal metric / geodesic / light bending
     - strong-field / frozen-star / echo package
   - do not spend time re-proving Newton unless needed for a new closure step
   - the current load-bearing weak point is the Poisson-forcing step
   - a finite-family sweep or mismatch residual is not enough to call Poisson
     uniqueness “derived for all local operators”
   - if you cannot prove the universal uniqueness theorem, keep Poisson as the
     weakest bounded link and build the rest of the gravity bundle honestly on
     top of that

2. **`S^3` compactification / topology closure**

3. **DM relic mapping**

4. **Renormalized `y_t` matching**

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

## Hard constraints

1. Do not call `S^3`, DM relic mapping, renormalized `y_t`, CKM, or the broad
   gravity bundle `closed` unless the underlying runner and note support that
   status directly.

1a. For gravity specifically:
   - `time dilation` and eikonal `WEP` are not standalone closure wins; they
     are built-in action identities once `S = L(1-f)` is accepted
   - geodesic / conformal-metric / GW results must carry their continuum-limit,
     WKB, or wave-equation-promotion assumptions explicitly
   - strong-field / frozen-star / echo work is companion-level unless it
     actually closes a sharp theorem surface

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
