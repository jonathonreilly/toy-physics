# Archive: portable-package extension — stale wrappers over un-audited inputs

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed (terminal; ACCEPT)

## Why this is here

`PORTABLE_PACKAGE_EXTENSION_NOTE.md` claimed a retained extension of
the portable fixed-field package beyond the first two grown families,
asserting that "only the sign-law core is broadly portable while the
distance law and complex-action branches are stricter subsets." The
audit found the portability claim is built on un-audited / weakly-audited
inputs:

- `SIGN_PORTABILITY_INVARIANT_NOTE` is **audited_conditional**.
- `DISTANCE_LAW_PORTABILITY_NOTE` is **unknown / unaudited**.
- `COMPLEX_SELECTIVITY_COMPARE_NOTE` is **unknown / unaudited**.
- The runner `scripts/PORTABLE_PACKAGE_EXTENSION_COMPARE.py` only prints
  a hard-coded comparison table — it does NOT recompute the
  zero/neutral/sign/slope, distance-tail, or complex-action checks for
  each listed family. It is a static summary, not a derivation.

So the retained cross-family package extension does not have computed
or audited-clean support for every family row. The companion file
`PORTABLE_CARD_EXTENSION_NOTE.md` is also archived in this directory as
the related sibling that suffered the same dependency problem.

The safe-claim boundary (per the audit) is: this is an editorial
portability taxonomy or worklist; NOT an audit-retained portable
fixed-field package extension beyond the first two grown families.

## Repair target

Audit or repair the sign, distance-law, and complex-action source
notes, then replace the static table with a runner that recomputes the
zero/neutral/sign/slope, distance-tail, and complex-action checks for
each listed family. That repair has not been done.

## Status

Archived as terminal-failed historical records. Their audit rows will
remain `audited_failed` until the dependency notes are themselves
brought to audit-clean status and the runner is upgraded to recompute
rather than tabulate.
