# Claude Execution Instructions

**Date:** 2026-04-12  
**Branch:** `claude/youthful-neumann`

Read only these two files before working:

1. `instructions.md` — execution rules
2. `review.md` — Codex-audited paper state and live blockers

If older notes or scripts conflict with `review.md`, follow `review.md`.

## Mission

Use Claude time on execution, derivation attempts, and clean theorem-boundary
 notes. Do not spend time doing broad review. Codex will review the deltas.

## Where to land work

Land all execution work on this branch and push it:

- branch: `claude/youthful-neumann`
- remote: `origin/claude/youthful-neumann`

Do not leave the real fix only as local untracked notes in another worktree.
If you are replacing a stale pushed claim, update the pushed note/script on
this branch so Codex can review the actual branch state.

## Working rules

1. Work from the audited state in `review.md`, not from older broader claims.
2. A lane is `closed` only if the theorem surface is actually first-principles.
3. If a result is model-dependent, fitted, finite-size anchored, or uses an
   extra assumption, label it `bounded`.
4. If the surface cannot currently close, document the obstruction cleanly.
5. Do not widen assumptions silently.
6. Do not use “gate closed”, “theorem proved”, or similar language unless the
   final note and script match the audited surface exactly.
7. If `review.md` says a pushed file is overstating a lane, either:
   - fix that pushed file directly on this branch, or
   - replace it with a new pushed boundary note/script and say the old file is
     superseded in `CODEX_REVIEW_PACKET_2026-04-12.md`.

## Priority order

1. `S^3` compactification / cap-map uniqueness
2. DM relic mapping
3. renormalized `y_t` matching
4. CKM only if the Higgs `Z_3` step becomes genuinely `L`-independent

## What counts as useful work

Useful:

- a genuinely new theorem or obstruction on the current surface
- a script with exact checks separated from bounded/model checks
- a note that narrows a lane to the strongest honest paper-safe claim
- replacing stale overclaiming notes with clean boundary notes

Not useful:

- re-asserting an already-audited claim with stronger rhetoric
- calling a modeled benchmark “closure”
- broad phenomenological prose without a tighter theorem surface

## Required outputs for every serious attempt

For each lane touched, produce:

1. one note in `docs/`
2. one runnable script in `scripts/`

Naming pattern:

- `docs/<LANE>_NOTE.md` or `docs/<LANE>_THEOREM_NOTE.md`
- `scripts/frontier_<lane>.py`

Every note must contain these sections:

1. `Status`
2. `Theorem / Claim`
3. `Assumptions`
4. `What Is Actually Proved`
5. `What Remains Open`
6. `How This Changes The Paper`
7. `Commands Run`

Every script must:

- end with a clear `PASS=n FAIL=m`
- separate exact checks from bounded/model checks
- avoid unconditional `True` theorem checks except for clearly labeled
  supporting remarks

Every serious execution pass must also:

- commit the changes on `claude/youthful-neumann`
- push `origin/claude/youthful-neumann`
- make sure the files you want reviewed are actually on the pushed branch

## Mandatory handoff packet

Before asking Codex to review, create or update:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

For each touched lane include:

- files changed
- commands run
- final exit code
- claimed status: `closed`, `bounded`, or `open`
- one paragraph explaining why the claim is not overstated

## Fast paper-safe reminders

- Time / `3+1`: closed on the single-clock codimension-1 theorem surface
- RH matter: closed at the full-framework level, not from the spatial graph alone
- Generation: treat as closed in the framework. Do not keep re-litigating
  generation existence; only work on hierarchy/flavor if there is real new
  closure.
- CKM: still bounded unless the Higgs `Z_3` step is made universal

## Current live review findings you must respect

1. `frontier_ewsb_generation_cascade.py` is **not** the generation-closure theorem.
   The exact safe status is:
   - exact `1+2` split
   - bounded `1+1+1` hierarchy model
   - it must not be presented as the reason generations close

2. `EWSB_GENERATION_CASCADE_NOTE.md` must not say:
   - `three distinct masses => three physical generations`
   - `generation physicality gate: closed`

3. `frontier_ckm_interpretation_derivation.py` is still bounded.
   The live blocker is:
   - Higgs `Z_3` charge is still finite-size / `L=8` anchored, not universal

4. There is no live structural `SU(3)` blocker right now.
   Do not spend cycles “re-closing” `SU(3)` unless a new concrete issue appears.

5. `CODEX_REVIEW_PACKET_2026-04-12.md` must not overstate lane status.
   Right now Codex considers these statuses too strong:
   - `S^3` = `STRUCTURAL`
   - renormalized `y_t` = `CLOSED`

6. `PUBLICATION_CARD_FINAL_2026-04-12.md` is not review authority.
   It may be used as a summary card, but `review.md` still wins on status.

7. `GENERATION_GAP_CLOSURE_NOTE.md` and `frontier_generation_gap_closure.py`
   currently overclaim taste-physicality and hierarchy closure.

8. `RENORMALIZED_YT_THEOREM_NOTE.md` currently overstates closure relative to
   its own runner. Keep that lane bounded unless the note and script are
   brought into alignment at theorem grade.

9. `DM_RELIC_GAP_CLOSURE_NOTE.md` must not say the DM relic mapping gate is
   closed.
   Current Codex view:
   - direct lattice Coulomb/Sommerfeld support is useful
   - thermodynamic-limit arguments are useful
   - full relic mapping is still bounded/open

10. `S3_PL_MANIFOLD_NOTE.md` must not be treated as closing the topology lane.
    Current Codex view:
    - it is a useful bounded structural attack
    - the general cap/link proof is still not formalized strongly enough to
      upgrade the lane beyond bounded/open review status

11. `G_BARE_DERIVATION_NOTE.md` must not be treated as eliminating the DM
    coupling assumption at theorem grade.
    Current Codex view:
    - it is a bounded normalization argument
    - the key vulnerability remains whether the Cl(3) normalization is a
      constraint or just a convention

12. `CODEX_REVIEW_PACKET_2026-04-12.md` still cannot present:
    - `S^3` as `STRUCTURAL`
    - renormalized `y_t` as `CLOSED`
    - DM relic mapping as `CLOSED`
    unless the underlying notes and runners genuinely support those statuses

13. The newest honest bounded additions are:
    - `GENERATION_ANOMALY_FORCES_THREE_NOTE.md`
    - `frontier_generation_anomaly_forces_three.py`
    - `DM_THERMODYNAMIC_CLOSURE_NOTE.md`
    - `frontier_dm_thermodynamic_closure.py`
    These are useful. They may be cited as bounded strengthenings, but they do
    not upgrade the corresponding gates to closed status.

14. `CODEX_REVIEW_PACKET_2026-04-12.md` is still not self-consistent all the
    way through.
    Even if the top summary is bounded, later sections must not re-promote:
    - `S^3` to `STRUCTURAL`
    - renormalized `y_t` to `CLOSED`
    until the underlying lane notes actually support that upgrade.

15. `GENERATION_ROOTING_UNDEFINED_NOTE.md` is a useful exact obstruction note,
    but it does NOT by itself establish the retained generation result.
    Do not let the companion script synthesis jump from
    “rooting is undefined” to
    “therefore the triplet orbits are physical generations.”

16. `RP3_VS_S3_NOTE.md` is a useful bounded consistency note.
    Safe use:
    - the RP^3 eigenvalue correction is useful
    - the fiber/base distinction is useful
    Unsafe use:
    - do not treat it as closing the overall `S^3` compactification lane
    - do not say `S^3` is now derived from the framework based on this note

17. The newest honest bounded/negative additions you may reuse are:
    - `GENERATION_LITTLE_GROUPS_NOTE.md` / `frontier_generation_little_groups.py`
    - `GENERATION_ROOTING_UNDEFINED_NOTE.md` / `frontier_generation_rooting_undefined.py`
    - `GENERATION_3FAILS_INVESTIGATION_NOTE.md` / `frontier_generation_3fails_investigation.py`
    - `RP3_VS_S3_NOTE.md` / `frontier_rp3_vs_s3.py`
    - `G_BARE_SELF_DUALITY_NOTE.md` / `frontier_g_bare_self_duality.py`
    - `GENERATION_PHYSICALITY_DEEP_ANALYSIS.md`
    - `GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md`
    - `MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE.md`
    - `REMAINING_CRITIQUE_TARGETS_2026-04-12.md`
    Treat them as obstruction or consistency notes, not gate-closure notes.

18. `GENERATION_3FAILS_INVESTIGATION_NOTE.md` is acceptable as bounded support.
    But the companion script must not say:
    - `This is exactly the SM generation structure`
    It is a bounded commutant-inequivalence result, not a closed generation theorem.

19. Latest Codex view on generation:
    - the new axiom-boundary work is a REAL upgrade
    - safe paper claim:
      `generation is closed`
    - interpret that carefully:
      the physical-lattice premise belongs in the framework section once.
      Do not keep appending it as a qualifier to every generation sentence.
    - not safe:
      `the EWSB cascade or a flavor model is what closes generation`

20. Latest Codex view on the unified A5 story:
    - acceptable for generation if phrased as the framework's
      physical-lattice assumption, not as a newly introduced standalone axiom
    - NOT yet acceptable as a full collapse of `S^3`, DM, and renormalized
      `y_t` to `only A5` / `only the physical-lattice assumption`
    because those lanes still retain additional mathematical or imported-physics
    gaps in their own notes.

## Immediate tasking

Start with the highest-value open gate from `review.md`.
