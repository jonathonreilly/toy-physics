# Archive: testable-ranking notes — stale wrappers without audited inputs

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed for both notes (terminal; ACCEPT)

## What is here

Two ranking/catalog notes were archived together because they share the
same failure mode:

- `MOONSHOT_OTHER_TESTABLES_NOTE.md`
- `TESTABLE_PREDICTIONS_MAP_NOTE.md`

## Why they are here

### `MOONSHOT_OTHER_TESTABLES_NOTE.md`

The note proposed the interferometric / waveguide phase-ramp analog as
"the best non-diamond testable" because it "maps directly onto the
strongest retained phase-sensitive observable." The audit found:

- The shortlist imports unnamed retained artifacts and an `R² ~ 0.96`
  phase-ramp result, then declares the analog the best testable.
- There is **no cited authority set, no ranking metric, and no runner**
  from which the top-testable conclusion follows.

Safe to claim: these are possible non-diamond analog directions and the
waveguide phase-ramp is an author-prioritized candidate. NOT safe to
claim: an audit-retained best testable grounded in retained science.

### `TESTABLE_PREDICTIONS_MAP_NOTE.md`

The note presented itself as a "compact, adversarial map of the best
current testable predictions across the retained science on main, with
each entry recording what is already retained." The audit found:

- Several entries marked as "already retained" are actually bounded,
  conditional, or still unaudited (diamond protocol/prediction lane,
  wavefield escalation, growing-graph expansion card, generated-family
  bridge).
- The note lists seven ranked entries but the later "current ranking"
  drops the grown-trapping and growing-expansion entries and reorders
  the list. The numbered ranking, top-3, and bottom-line sections
  disagree with each other.

Safe to claim: this is a stale editorial snapshot of candidate testable
lanes. NOT safe to claim: a retained current map of audit-clean
testable predictions.

## Repair targets (per the audit)

- For `MOONSHOT_OTHER_TESTABLES_NOTE.md`: add explicit audited-retained
  one-hop citations for each retained connection, define the ranking
  criteria, and provide a table or runner that recomputes the ordering
  from those inputs. Otherwise demote to open brainstorming.
- For `TESTABLE_PREDICTIONS_MAP_NOTE.md`: regenerate the map from the
  audit ledger, separating audited-clean / retained / conditional /
  bounded / unaudited items, and make the numbered ranking, top-3, and
  bottom-line sections mechanically consistent.

Neither repair has been done.

## Status

Both archived as terminal-failed historical records. Their audit rows
will remain `audited_failed` until the repairs above are completed.
