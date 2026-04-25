# AI Methodology Synthesis

**Date:** 2026-04-25
**Status:** synthesized methodology surface from the raw annex; source material
for the methodology paper and reusable skill pack

This file is the first full synthesis pass over the raw AI-methodology archive.
It converts the prompt captures, review packets, workflow scaffolds, git
evidence, and repo-governance documents into a coherent method.

## Bottom Line

The observed method is not "ask an LLM for physics." It is a controlled loop:

1. open a bounded theoretical lane;
2. force the model to produce artifacts, not just prose;
3. attack those artifacts with adversarial review;
4. demote, reject, or preserve no-go results when closure fails;
5. selectively land only the honest subset;
6. keep a public claim boundary narrower than the exploration surface;
7. feed the lessons back into persistent prompts, review rules, and skills.

This is why the methodology is reusable inside this repo and plausible as a
template for other AI-theory projects. The value is in the loop discipline, not
in any single model answer.

## Raw Evidence Strata

The raw annex contains six distinct evidence classes.

| Evidence class | What it shows | Representative raw surfaces |
|---|---|---|
| Prompt/session captures | User/agent interaction patterns, course corrections, strategy pivots, and concrete research loops | `raw/prompts_session_current.md`, `raw/prompts_session_596e9a60_jonreilly.md`, `raw/prompts_session_fe95a681_jonreilly.md`, `raw/prompts_session_4ffea772_jonreilly.md` |
| Workflow commands | Explicit reusable role prompts for hypothesis, theory review, design, sweep, analyze, validate, sanity, frontier, and write-up | `raw/claude_project_commands.md`, `raw/workflow_tooling.md` |
| Review structures | Cross-tool review, branch-local `review.md` packets, selective landing, and review-branch naming conventions | `raw/claude_review_structure.md`, `raw/codex_review_structure.md`, `raw/codex_desktop_review_hygiene_2026-04-25.md` |
| Repo governance | Controlled vocabulary, active review queue, review workflow, retest playbook, work-history archive, and publication package boundaries | `docs/repo/`, `docs/work_history/repo/`, `raw/protocols.md` |
| Git/worktree evidence | High-throughput branch/commit trajectory, review/land worktrees, no-go/demotion commits, and landing cadence | `raw/claude_git_evidence_full.md`, `raw/codex_repo_hygiene.md`, `raw/repo_audit.md` |
| Persistent memory | Lessons promoted from local failures into future-agent operating rules | `raw/memory_files.md`, `raw/claude_settings_and_state.md` |

The synthesis below depends on all six. Prompt evidence shows what happened;
governance and git evidence show how it was contained.

## Observed Method Loop

The actual loop has nine recurring moves.

| Move | Description | Evidence signal |
|---|---|---|
| Broad target selection | User states an ambitious scientific or publication target rather than a narrow implementation task | Current-session prompts move from ToE gaps to methodology framing |
| Repo grounding | Agent rereads current `main`, claim tables, runner surfaces, and recent changes before revising the status map | Repeated "check latest main" prompts in `raw/prompts_session_current.md` |
| Candidate generation | AI produces theorem routes, runners, branches, notes, and attack vectors at high throughput | Project commands and prompt sessions show frontier, hypothesis, sweep, and first-principles roles |
| Artifact forcing | Candidate claims must become notes, runners, logs, or explicit derivations | Raw sessions repeatedly require script/log/note chains and runner-backed claims |
| Review pressure | Claude/Codex/user review attacks semantics, code, assumptions, and status language | `raw/claude_review_structure.md`, `raw/codex_review_structure.md`, hostile-review memory |
| Status correction | Claims are narrowed to retained, bounded, support, open, no-go, reject, or historical | Controlled vocabulary and review workflow |
| Selective landing | Only the honest subset reaches `main`; branch-local raw/review material stays off the front door | AI-methodology capture branch review and landing evidence |
| Historical preservation | Failed routes and no-go results remain available as useful negative evidence | Koide, Planck, area-law, and review-history surfaces |
| Rule feedback | Recurrent errors are promoted into memory, workflow prompts, review queues, and skills | `feedback_hostile_review_semantics`, review-hardening backlog, current skill pack |

The productive pattern is cyclic. A failed route is not wasted if it becomes a
guardrail, no-go theorem, review rule, or future skill instruction.

## Division Of Labor

The raw data shows a three-part labor structure.

| Actor | Actual role in the method |
|---|---|
| Human author | Chooses targets, rejects weak framings, corrects agent context, decides publication posture, and owns all physics claims. The current-session raw prompts show repeated human course-correction, including correcting timeline/context and rejecting overconfident or poorly framed claims. |
| Forward-production AI | Generates candidate routes, branch packets, theorem drafts, runner scaffolds, and broad search programs. Claude-side project commands encode roles such as hypothesis framing, experiment design, first-principles derivation, anomaly investigation, and write-up. |
| Review/integration AI | Applies adversarial pressure, finds artifact-chain mismatches, demotes overclaims, rewrites public surfaces, and performs selective landings. Codex-side raw review evidence repeatedly shows review branches, `review.md` packets, and narrower landings. |

The method works because these roles are not collapsed. Production and review
are intentionally in tension.

## Reviewer Backpressure

Reviewer backpressure is the key observed control mechanism in the raw archive.
It appears in three layers:

1. **Prompt-level pressure.** The user explicitly rejects smooth but unsupported
   outputs and demands theorem-grade executable artifacts.
2. **Agent-level pressure.** Codex/Claude review passes identify overclaims,
   placeholder runners, tautological checks, and unsupported status labels.
3. **Repo-level pressure.** Review findings become queue items, demotions,
   controlled-vocabulary rules, no-go notes, or selective landings.

The persistent hostile-review memory captures the principle: arithmetic can be
correct while the symbol-to-physics identification is wrong. Review must attack
semantics, not just algebra.

That is the central safety mechanism against AI-generated theoretical
overclaiming.

## Artifact-Chain Standard

The strongest repeated failure mode in the raw sessions is artifact-chain drift:
a note claims a result, but the cited runner does not actually check the
decisive step, or a script/log is only a placeholder.

The synthesized standard is:

- a claim note must name the exact support surface;
- the runner/log must check the load-bearing step, not only surrounding
  algebra;
- `PASS` assertions are not proof if they are hard-coded placeholders;
- if the decisive step is theorem-cited rather than executable, say so;
- if no support exists, demote or keep the claim off-main.

This is why the methodology paper should emphasize "evidence chain" rather
than "prompt quality." The repo must force language, code, and status to align.

## No-Go Results As Positive Method Output

The raw evidence repeatedly treats no-go production as useful:

- Koide route no-gos sharpen which charged-lepton bridges remain open.
- Planck/area-law no-gos prevent entropy-carrier overclaiming.
- Branch reviews preserve failed closure attempts as route-pruning evidence.
- Controlled vocabulary includes negative-result and exact-negative-boundary
  labels.

The method's progress metric is therefore not only "more retained theorems."
Progress includes eliminating tempting but false routes.

## Tooling And Skills

The raw Claude command set is the closest existing reusable-tool surface. It
decomposes AI science work into roles:

- `/hypothesis`: formulate falsifiable questions;
- `/theory-review`: check axiom compliance, consistency, falsifiability,
  minimality, and emergent-vs-imposed status;
- `/design-experiment`: define observables, parameters, controls, samples, and
  systematic errors;
- `/sweep`: build parameter scans;
- `/analyze`: extract statistics and verdicts from logs;
- `/validate`: test seeds, sensitivity, finite size, initialization, logic, and
  cherry-picking;
- `/sanity`: act as skeptical reviewer and artifact detector;
- `/frontier`: map explored/open/dead-end space;
- `/write-up`: archive the result.

The new methodology skills should not replace that evidence. They should
compress it into project-agnostic LLM behavior for theorem-oriented physics
work.

## Publication Method

The publication strategy implied by the raw data is:

- lead honestly with the AI-enabled methodology;
- use immediate scientific results as case-backed motivation, but keep their
  claim scope governed by the publication package;
- disclose AI use directly while making human responsibility explicit;
- show the repo's negative and review surfaces as credibility assets;
- do not let the methodology paper widen any physics claim.
- add related-work context and sanitized representative excerpts before
  external release.

The paper should therefore be "methods plus case studies," not a manifesto
alone and not a narrow disclosure note.

## Limits

This synthesis does not claim:

- that raw model output is reliable;
- that prompt history is itself scientific evidence;
- that all repo claims are equally current;
- that executable runners replace mathematical proof in every context;
- that AI systems are authors or final arbiters.
- that AI-assisted theory is generally superior to human-only theory work;
- that the raw prompt annex is ready as a public reproduction package without
  sanitization and excerpt selection.

The claim is narrower: high-throughput AI theory work becomes scientifically
usable only when embedded in an auditable artifact and review system.

## Implication For The Skill Pack

The skills should be rebuilt around observed failure modes:

- opening a lane without first defining status gates leads to overclaiming;
- writing a note before the evidence chain exists leads to drift;
- reviewing algebra without semantics misses real errors;
- landing whole branches imports noise;
- treating no-go results as failures wastes valuable route-pruning evidence;
- synthesis before raw-evidence selection produces generic methodology prose.

The revised skill pack should therefore encode artifact-chain discipline,
reviewer backpressure, selective landing, and case-study synthesis as mandatory
steps.
