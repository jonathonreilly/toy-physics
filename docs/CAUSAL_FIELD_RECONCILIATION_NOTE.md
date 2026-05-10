# Causal Field Reconciliation Note

**Date:** 2026-04-06 (status line rephrased + claim narrowed 2026-04-28 per audit-lane verdict; audit-status note added 2026-05-10)
**Status:** bounded harness-boundary diagnostic for the fixed-anchor cross-family replay; the upstream center-family causal-field result is **not** asserted as valid by this note (the cited runner emits no executable verification and the cited diagnostic logs are missing).

## Artifact Chain

- [`scripts/causal_field_portability_probe.py`](../scripts/causal_field_portability_probe.py)
- [`logs/2026-04-06-causal-field-portability-probe.txt`](../logs/2026-04-06-causal-field-portability-probe.txt)
- [`logs/2026-04-06-causal-field-reconciliation-diagnostic.txt`](../logs/2026-04-06-causal-field-reconciliation-diagnostic.txt)
- archived causal-field note:
  - [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- portability boundary note:
  - [`CAUSAL_FIELD_PORTABILITY_NOTE.md`](CAUSAL_FIELD_PORTABILITY_NOTE.md)

## Question

The retained causal-field note says the dynamic `c=0.5` cone gives a stable
`~0.45` observable on the center grown family and preserves the crossover.
The low-SNR cross-family replay, however, reported a family boundary.

Are these results contradictory, or are they probing different regimes?

## Diagnosis

They are not the same measurement in practice.

The retained `c=0.5` result is a center-family causal-field observable in a
regime where the dynamic cone signal is already resolved and stable.

The portability probe fixes a single nominal source target
`(y, z) = (0, 3)` at `source_layer = 8` and reuses that same target across
the three grown families. That means the actual selected source node shifts
slightly family-to-family even though the nominal target is fixed.

The diagnostic log shows the resulting issue clearly:

- the exact-null control remains exact
- but the centroid shifts are only `O(10^-7)` to `O(10^-6)`
- the associated standard errors are of comparable size
- the `dynamic(c=0.5)/instantaneous` ratio therefore becomes source-placement
  sensitive and can even flip sign across families

The small-signal ratio is not stable enough to override the retained
center-family result.

## What Causes The Mismatch

Primary cause:
- fixed source placement across different growth families

Secondary cause:
- low-SNR centroid observable in the replay

Not the main cause:
- seed handling
- zero-control failure
- a field-strength-only effect

The field-strength scan in the reconciliation diagnostic shows that the
family-specific ratios do not collapse to the retained `~0.45` value simply
by increasing strength within the same fixed-anchor replay. So this is not
just a single bad strength window.

## Safe Conclusion

The low-SNR cross-family replay is trustworthy as a **diagnosis of the fixed
anchor replay harness boundary**, but not as a refutation of the retained
center-family causal-field result.

So the correct retained split is:

- **retained positive:** the center-family dynamic causal cone observable
  with `c=0.5` and preserved crossover
- **diagnosed boundary:** the same fixed-anchor replay does not stay portable
  across all three families

## Recommended Next Step

If we want to push this lane further, the next discriminating test should use
either:

- family-registered source placement, or
- a higher-SNR observable that does not rely on tiny centroid differences

That would tell us whether the family boundary is fundamental or just an
artifact of the fixed-anchor replay geometry.

## Audit boundary (2026-04-28)

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the reconciliation note preserves a proposed-retained
> center-family causal-field result while the cited causal-field
> runner emits no executable verification, and the cited
> reconciliation diagnostic logs for source-node shifts and
> field-strength scans are missing from the audit packet. Why this
> blocks: a hostile physicist can replay the portability runner and
> accept the exact-null control plus fixed-anchor family-boundary
> table, but cannot verify the original 0.45 center-family
> dynamic-cone observable, its claimed seed/strength stability, or
> the diagnosis that source placement rather than family choice is
> the load-bearing variable.

The Status line has been narrowed: the upstream center-family
causal-field result is no longer asserted as valid by this note. The
note retains the bounded harness-boundary diagnostic only.

## What this note does NOT claim

- The 0.45 center-family dynamic-cone observable (the cited runner
  emits no executable verification).
- Seed or field-strength stability for that observable (the cited
  diagnostic logs are missing).
- That source placement rather than family choice is load-bearing
  (this diagnosis depends on the missing diagnostic logs).

## Audit-status note (2026-05-10)

The 2026-05-05 audit verdict (`audited_conditional`, chain_closes=false)
ratified the bounded fixed-anchor cross-family replay diagnostic — the
exact-null control survives, and the configured forward-only and
dynamic-cone ratios split across the three configured grown families
rather than refuting the upstream center-family result — but flagged
that the only one-hop dependency is itself `audited_conditional` rather
than retained-grade.

> "The supplied runner genuinely computes the fixed-anchor cross-family
> replay and supports the bounded harness-boundary diagnostic. However,
> the only cited authority is marked audited_conditional/support, so
> retained-grade closure does not propagate under the rubric."

Per-input current status:

- [`CAUSAL_FIELD_PORTABILITY_NOTE.md`](CAUSAL_FIELD_PORTABILITY_NOTE.md)
  — `audited_conditional` (bounded portability probe; the 2026-05-04
  verdict pinned a missing-dependency edge for the imported
  `evolving_network_prototype_v6` framework-operator module, and the
  2026-05-10 audit-status note narrows the claim to a bounded
  computational diagnostic on the configured fixed-anchor probe).

Blocked-on: this reconciliation note stays `audited_conditional` until
the cited portability authority advances to retained-grade or until
the runner is cited directly as a bounded retained artifact under a
retained portability-criterion theorem. The bounded harness-boundary
diagnostic itself — that the low-SNR fixed-anchor replay diagnoses a
configured-probe boundary rather than refuting the archived
center-family result — is unaffected by this status note; the change
is purely upstream propagation accounting on the one-hop dependency.

## What would close this lane (Path A future work)

A reinstated center-family causal-field result would require:

1. A registered causal-field runner that emits executable
   verification of the 0.45 dynamic-cone observable.
2. Archived diagnostic logs for the source-node-shift and
   field-strength scans cited by this note.
3. A reconciliation theorem that derives the source-placement
   diagnosis from the registered runners.
