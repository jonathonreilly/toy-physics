# Physics Critic Tracker

**Purpose:** adversarial review inbox for the strongest skeptical critiques of
the current science claims, retained results, control stack, portability
surface, and experimental framing.

## Open Critiques

| Date | Target Claim / Lane | Critique | Evidence / Files | What Would Falsify Or Resolve It | Status |
| --- | --- | --- | --- | --- | --- |
| _none yet_ |  |  |  |  |  |

## Resolved Critiques

| Date | Target Claim / Lane | Resolution | Evidence / Retest | Status |
| --- | --- | --- | --- | --- |
| 2026-04-11 | `60fbcad` harness loophole: the strict staggered `17`-card was not self-contained at the reviewed historical commit | Closed on retained `main`. The current repo-local runner no longer imports from `.claude/worktrees/sleepy-cerf`; it is self-contained, and the retained rerun reproduced the frozen strict-card surface on the repository tree alone. This resolves the specific reproducibility objection for the retained strict card, while leaving the separate semantic/control critiques of the force-based card untouched. | Current self-contained runner: [`scripts/frontier_staggered_17card.py`](../scripts/frontier_staggered_17card.py).<br>Retained note updated with the rerun status: [`docs/STAGGERED_FERMION_CARD_2026-04-10.md`](STAGGERED_FERMION_CARD_2026-04-10.md).<br>Reproduced scores on `main`: 1D `17/17`; 3D `n=9/11/13` all `17/17`, with `n=11,13` keeping the documented `4/6` family gate because `N_sites > 1000`. | resolved |

## Critic Rules

- Be maximally skeptical, but specific.
- Prefer concrete holes over general pessimism.
- Separate:
  - code / harness bugs
  - control failures
  - portability overclaims
  - interpretation overreach
  - experiment-readiness gaps
- Every critique must point to exact notes, scripts, logs, or commits.
- Every critique must include what evidence would resolve it.
- If a critique is answered, move it to `Resolved Critiques` with the retest or
  new artifact that closed it.
