# Portable Package Extension Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/portability-stale-extension-wrappers-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- Date archived: 2026-04-30
- Archive directory: `archive_unlanded/portability-stale-extension-wrappers-2026-04-30/`
- Audit verdict (`verdict_rationale` from [audit_ledger.json](../../docs/audit/data/audit_ledger.json), claim_id `portable_package_extension_note`, `audit_status: audited_failed`, `effective_status: retained_no_go`):

> "Issue: The retained comparison treats sign portability, distance-law portability, and complex-action selectivity as already established across multiple families, but the cited authorities are not audit-clean: SIGN_PORTABILITY_INVARIANT_NOTE is audited_conditional, DISTANCE_LAW_PORTABILITY_NOTE and COMPLEX_SELECTIVITY_COMPARE_NOTE are unknown/unaudited, and the runner only prints a hard-coded comparison table. Why this blocks: a retained cross-family package extension requires computed or audited-clean support for every family row, not a static table over unratified inputs. Repair target: audit or repair the sign, distance-law, and complex-action source notes, then replace the static table with a runner that recomputes the zero/neutral/sign/slope, distance-tail, and complex-action checks for each listed family. Claim boundary until fixed: it is safe to present this as an editorial portability taxonomy or worklist; it is not safe to claim an audit-retained portable fixed-field package extension beyond the first two grown families."

Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

---

## Artifact Chain

- [`scripts/PORTABLE_PACKAGE_EXTENSION_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/PORTABLE_PACKAGE_EXTENSION_COMPARE.py)
- [`logs/2026-04-06-portable-package-extension-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-portable-package-extension-compare.txt)
- retained comparison sources:
  - [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
  - [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md)
  - [`docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md)

## Question

Does the portable fixed-field package extend cleanly beyond the first two grown families?

## Comparison

The retained rows say:

- the sign-law package is broadly portable across the structured retained families
- the distance law is portable only as a stricter subset and becomes selective or breaks on newer families
- complex-action survival is narrower still and remains anchor-local or boundary-sensitive

## Safe Read

The broad portable package is the signed-control fixed point:

- exact zero-source cancellation
- exact neutral same-point cancellation
- plus/minus antisymmetry
- weak-field response pinned near unit slope

That broad package survives across the retained structured families. What changes from family to family is basin width, seed selectivity, and whether the stricter distance-law and complex-action branches also survive.

## Exact Mismatch

- the first two grown families retain the near-Newtonian distance tail
- the newer retained families do not preserve that tail uniformly
- complex-action survival does not follow sign portability by itself
- the fifth-family radial row is a directional holdout, but its distance exponent flattens and it does not restore broad distance-law portability

## Final Verdict

**retained narrow comparison positive: the portable fixed-field package extends beyond the first two grown families, but only the signed-control core is broadly portable; the distance law is a stricter subset and complex-action is narrower still**
