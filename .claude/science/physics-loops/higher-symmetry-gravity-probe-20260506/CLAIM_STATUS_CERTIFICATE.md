# Claim Status Certificate

actual_current_surface_status: bounded-support
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The branch repairs an audit-cache mismatch and proposes a bounded clean re-audit target; it does not self-ratify retained status."
audit_required_before_effective_retained: true
bare_retained_allowed: false

## Claimed Surface

For dense `Z2 x Z2` with `N=80,100,120`, `n_seeds=16`,
`z2z2_quarter=16`, `connect_radius=5.2`, `anchor_b=5.0`, and
`mass_count=4`, the runner computes a positive-row mass-bump power-law fit
inside `M in {2,3,5,8}`:

- `N=80`: fit rows `{3,5,8}`, `delta ~= 0.3668 * M^0.724`, `R^2=0.999`.
- `N=100`: fit rows `{2,5,8}`, `delta ~= 0.0748 * M^1.348`, `R^2=0.918`.
- `N=120`: fit rows `{2,3,5,8}`, `delta ~= 0.0504 * M^1.318`, `R^2=0.622`.

## Firewall

The claim excludes:

- rowwise positivity over the whole declared mass window;
- global gravity positivity over all displayed mass rows;
- Born-safety claims;
- clean retained gravity-law or distance-tail claims.

Independent audit is required before any repo authority surface changes the
effective audit status.

## Audit-Pipeline State After Repair

After running `bash docs/audit/scripts/run_pipeline.sh`, the row
`higher_symmetry_gravity_probe_note` is:

- `claim_type`: `bounded_theorem`
- `audit_status`: `unaudited`
- `effective_status`: `unaudited`
- `ready`: `true` in `docs/audit/data/audit_queue.json`

This is the intended author-side endpoint: ready for a fresh independent
audit, with no branch-local audit verdict.
