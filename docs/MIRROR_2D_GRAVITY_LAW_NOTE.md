# Exact 2D Mirror Gravity-Law Cleanup Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28 per audit-lane verdict; claim narrowed 2026-05-09 to primary-runner-backed evidence per audit `runner_artifact_issue` repair target; imported-authority dependency lifted into the header 2026-05-10 per follow-up `runner_artifact_issue` repair target).
**Status:** bounded null-result note — the exact 2D mirror primary-runner evidence shows weak gravity-side mass-window and distance-tail fits, so no clean 2D mirror mass law and no clean 2D mirror distance law are supported on the searched windows.
**Claim type:** bounded_theorem
**Primary runner (load-bearing):** [`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py) (2D exact mirror linear propagator)
**Primary runner registered cache (load-bearing):** [`logs/runner-cache/mirror_2d_validation.txt`](../logs/runner-cache/mirror_2d_validation.txt) — registered cached stdout (`exit_code=0`, `status=ok`) that backs every load-bearing weakness row in the "Retained result (primary runner)" section below.
**Imported authority (load-bearing dependency):** [`scripts/mirror_born_audit.py`](../scripts/mirror_born_audit.py) — provides `gen_2d_mirror` (exact 2D mirror generator) and `propagate_LINEAR` (strictly linear propagator) imported by the primary runner.
**Imported authority registered cache (load-bearing dependency):** [`logs/runner-cache/mirror_born_audit.txt`](../logs/runner-cache/mirror_born_audit.txt) — registered cached stdout (`exit_code=0`, `status=ok`) verifying the imported generator and propagator on the strict mirror Born family, so the exact-2D-mirror linear-propagator premise is closed by a one-hop registered dependency.
**Primary runner historical log (audit-trail context):** [`logs/2026-04-03-mirror-2d-validation.txt`](../logs/2026-04-03-mirror-2d-validation.txt) — original completed stdout retained for audit trail; the registered runner-cache above is load-bearing.
**Companion cleanup runner (diagnostic-only, not load-bearing):** [`scripts/mirror_2d_gravity_law_cleanup.py`](../scripts/mirror_2d_gravity_law_cleanup.py) — slow gravity-law cleanup sweep over wider anchor / distance windows. The companion table below is recorded as diagnostic context only; it is not load-bearing for the bounded null-result claim.
**Companion cleanup runner cached log (diagnostic-only):** [`logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt`](../logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt).

This note freezes the exact 2D mirror gravity-law lane.

It uses the exact 2D mirror family retained in:

[`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py)

The goal was narrow:

- check fixed-anchor mass-window and fixed-geometry distance-tail behaviour on the primary 2D mirror runner
- keep the exact 2D mirror family fixed
- promote a law only if the primary-runner fit quality is genuinely clean

## Retained result (primary runner, load-bearing)

The exact 2D mirror family remains review-safe for Born, MI, decoherence, and
positive gravity, but the gravity-side fits on the primary runner are weak.

From [`logs/2026-04-03-mirror-2d-validation.txt`](../logs/2026-04-03-mirror-2d-validation.txt):

- gravity scaling across `N ∈ {25, 40, 60, 80, 100}`:
  `gravity = 6.48 * N^-0.210`, `R^2 = 0.168` (weak)
- fixed-anchor mass window:
  `delta ~= 0.8720 * M^0.132`, `R^2 = 0.167` (weak)
- distance sweep tail:
  `delta ~= 0.3418 * b^0.320`, `R^2 = 0.075` (weak)

These primary-runner fit qualities are themselves the load-bearing evidence
that no clean promoted 2D mirror mass law or distance law is supported on the
searched windows.

The strongest retained clean row from the exact 2D validation lane is:

- `N = 60`
- `MI = 0.756118`
- `1 - pur_min = 0.4420`
- `d_TV = 0.8572`
- gravity `+2.5687`
- Born `1.08e-15`
- `k=0 = 0.00e+00`

## Companion cleanup sweep (diagnostic-only, not load-bearing)

The companion cleanup runner (`scripts/mirror_2d_gravity_law_cleanup.py`) was
run as a wider diagnostic sweep over additional anchor and threshold windows.
Its rows are reproduced here for diagnostic context only; they are NOT load-
bearing for the bounded null-result claim above, which closes from the primary
runner alone.

Diagnostic rows (from [`logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt`](../logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt)):

- `N = 60`
  - best mass window: `anchor_b = 5.0`, `delta ~= 0.8676 * M^0.462`, `R^2 = 0.923`
  - best distance tail: `mass_count = 5`, `peak_thr = 3.0`, `delta ~= 0.8858 * b^0.307`, `R^2 = 0.872`
- `N = 80`
  - best mass window: `anchor_b = 5.0`, `delta ~= 1.0791 * M^0.458`, `R^2 = 0.820`
  - best distance tail: FAIL on the wider sweep
- `N = 100`
  - best mass window: `anchor_b = 6.0`, `delta ~= 1.0027 * M^0.204`, `R^2 = 0.568`
  - best distance tail: `mass_count = 4`, `peak_thr = 1.0`, `delta ~= 0.9961 * b^0.140`, `R^2 = 0.321`

The companion cleanup table is consistent with the primary-runner conclusion
(deteriorating fits at larger N, no `R^2 >= 0.95` promotable row), but the
bounded null-result claim does not require those rows.

## Cleanup Conclusion

The primary runner does not support a clean promoted 2D mirror mass law or
distance law. The retained exact 2D mirror gravity story on primary-runner
evidence is:

- positive
- bounded
- weakly fit-dependent

So the conservative synthesis is:

- **exact 2D mirror = review-safe bounded coexistence pocket**
- **exact 2D mirror = no primary-runner-supported promoted mass law**
- **exact 2D mirror = no primary-runner-supported promoted distance law**

The family remains scientifically useful, but on the gravity side it is still a
bounded pocket rather than a law-like result.

## Audit boundary (2026-05-09 — claim narrowing per `runner_artifact_issue`)

The 2026-05-08 audit verdict on this note was `audited_conditional` with the
repair target:

> runner_artifact_issue: provide the completed `mirror_2d_gravity_law_cleanup.py`
> output/cache and source, or narrow the note to the diagnostic core actually
> backed by current runner output.

This revision takes the second branch of the repair target. The bounded null-
result claim is now anchored entirely on the primary runner
(`scripts/mirror_2d_validation.py`) and its cached log
(`logs/2026-04-03-mirror-2d-validation.txt`). The wider companion cleanup
sweep is recorded as diagnostic-only context. The bounded null-result holds
from the primary-runner fit qualities alone (`R^2 = 0.168 / 0.167 / 0.075`),
without depending on the companion cleanup rows.

## Audit boundary (2026-04-28)

The earlier Status line ended in "no clean 2D mirror law `proposed_promoted`",
which the audit-lane parser read as a `proposed_promoted` claim even though
the literal sentence said the opposite. The Status line has been rephrased
to a positive bounded null-result framing.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the target is classified as `proposed_promoted`, but the source
> note and runner both say the cleanup found no clean promoted 2D mirror
> gravity law. Why this blocks: the best mass exponents are weak or
> deteriorating and the distance-tail fits are absent or low quality, so
> promoting a law would invert the actual result of the source packet.

> Repair target: change the Status line so the audit queue does not read
> this as `proposed_promoted`; the safe statement is the bounded
> null-result that the cleanup did not find a clean promoted mass or
> distance law.

## What this note does NOT claim

- A promoted 2D mirror mass law.
- A promoted 2D mirror distance law.
- That the bounded coexistence pocket is the same thing as a
  promoted-tier gravity result on the 2D mirror family.
- Any load-bearing conclusion drawn from the diagnostic-only companion
  cleanup table; the bounded null-result rests on the primary-runner
  log alone.

## What would close this lane (Path A future work)

Reinstating a promoted 2D mirror gravity law would require:

1. A registered primary-runner mass-exponent fit that clears a hard
   `R^2` threshold (e.g. `R^2 >= 0.95`) on at least three sizes — the
   current primary-runner mass-window fit is `R^2 = 0.167`, well below
   the bar.
2. A registered primary-runner distance-tail fit that clears the same
   hard threshold — currently `R^2 = 0.075` on the primary runner.
3. A first-principles argument that the fitted exponent is the
   mass-coupling exponent, not just an empirical curve fit.

## Audit boundary (2026-05-10 — imported-authority dependency lifted into the header)

This revision addresses the generated-audit repair target:

> runner_artifact_issue: supply scripts/mirror_born_audit.py or vendor its
> generator/propagator into the primary runner, then re-audit the same
> cached weak-fit rows.

This revision takes the first branch of the repair target: it lifts
`scripts/mirror_born_audit.py` and its registered cache
`logs/runner-cache/mirror_born_audit.txt` into the note header as direct
load-bearing dependencies (one-hop). The bounded null-result claim itself
is unchanged; the supplied audit packet now includes the exact-2D-mirror
generator and `propagate_LINEAR` authority alongside the primary-runner
weak-fit cache.

## Registered runner artifacts

The primary-runner source and registered cached stdout backing the three
weak-fit rows, plus the imported-authority cache, are all present in the
worktree as one-hop registered dependencies:

- Primary runner: `scripts/mirror_2d_validation.py` (load-bearing source for
  every weak-fit row in the "Retained result (primary runner, load-bearing)"
  section above).
- Primary runner cache: `logs/runner-cache/mirror_2d_validation.txt`
  (registered cached stdout; `exit_code=0`, `status=ok`).
- Imported generator/propagator authority: `scripts/mirror_born_audit.py`
  (provides `gen_2d_mirror` and `propagate_LINEAR`, imported by the primary
  runner — load-bearing for the exact-2D mirror linear-propagator premise).
- Imported authority cache: `logs/runner-cache/mirror_born_audit.txt`
  (registered cached stdout; `exit_code=0`, `status=ok`).
- Companion cleanup runner (diagnostic-only):
  `scripts/mirror_2d_gravity_law_cleanup.py`.

The bounded null-result claim closes from the primary runner's cached stdout
plus the imported-authority cache (for the exact-mirror generator and linear
propagator); the companion cleanup table remains diagnostic context.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [mirror_program_synthesis](MIRROR_PROGRAM_SYNTHESIS.md)
