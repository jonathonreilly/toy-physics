# Stale Narrative Policy

**Status:** binding rule for the audit lane.

This policy handles source notes whose narrative frame has gone stale after
audit. It is parallel to `ALGEBRAIC_DECORATION_POLICY.md`, but applies to
failed wrapper narratives rather than algebraic rollups.

## 1. Failed frame with no survivors
When `audit_status = audited_failed` invalidates the entire narrative frame,
archive the source note under `archive_unlanded/<cluster-tag>/`.
Use this path when no durable structural observation remains. The audit
ledger row stays in place with its terminal failed verdict; that row is the
canonical negative-result record.

## 2. Failed wrapper with surviving sub-observations
When a wrapper note fails but some sub-observations survive, extract the
surviving content into one consolidated `support` note before archiving the
wrapper.

Use a single salvage note for narrow clusters, such as route-specific no-gos
under a failed exhaustion claim. Do not fragment the cluster into many
one-claim notes unless each observation is independently substantial.

The salvage note must state what failed, what survived, and the source
wrapper's archive recovery path. It must not restate the failed global
conclusion.

## 3. Recovery surface
Never delete stale source content entirely. `archive_unlanded/` is the
recovery surface, and git history remains the final fallback.

## 4. Ledger behavior
The audit ledger row for an archived failed note remains in the ledger with
`audit_status = audited_failed`. Do not gate these rows out in the seeder:
removing them erases the negative-result history and invites future
re-attempts of the same stale narrative.

The archived note should leave the active citation graph because it is
no longer under `docs/`, but the ledger trail remains available for
audit history and review.

## 5. Cross-References
- `ALGEBRAIC_DECORATION_POLICY.md` handles algebraic-consequence rollup.
- This policy handles stale-narrative-wrapper archival.
- Both policies manage the public claim surface without pretending
  failed or derivative content is stronger than it is.
