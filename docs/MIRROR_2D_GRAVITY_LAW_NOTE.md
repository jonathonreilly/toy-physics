# Exact 2D Mirror Gravity-Law Cleanup Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28 per audit-lane verdict; cleanup runner cached output added 2026-05-08)
**Status:** bounded null-result note — gravity-law cleanup found no clean 2D mirror mass law and no clean 2D mirror distance law on the searched windows.
**Primary runner:** [`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py) (2D exact mirror linear propagator)
**Cleanup runner:** [`scripts/mirror_2d_gravity_law_cleanup.py`](../scripts/mirror_2d_gravity_law_cleanup.py) — slow gravity-law cleanup sweep that produced the N=60/80/100 mass-window and distance-tail fits below.
**Cached cleanup log:** [`logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt`](../logs/2026-04-03-mirror-2d-gravity-law-cleanup.txt) — completed stdout reproducing every fit row in the "Retained result" section.

This note freezes the exact 2D mirror gravity-law cleanup lane.

It uses the exact 2D mirror family retained in:

[`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py)

and the cleanup sweep:

[`scripts/mirror_2d_gravity_law_cleanup.py`](../scripts/mirror_2d_gravity_law_cleanup.py)

The goal was narrow:

- test fixed-anchor mass windows more widely
- test fixed-geometry distance tails more widely
- keep the exact 2D mirror family fixed
- promote a law only if the fit quality is genuinely clean

## Retained result

The exact 2D mirror family remains review-safe for Born, MI, decoherence, and
positive gravity, but the gravity-side fits remain weak across the cleanup
search.

The strongest retained clean row from the exact 2D validation lane remains:

- `N = 60`
- `MI = 0.756118`
- `1 - pur_min = 0.4420`
- `d_TV = 0.8572`
- gravity `+2.5687`
- Born `1.08e-15`
- `k=0 = 0.00e+00`

The wider gravity-law cleanup confirmed that the best fitted windows are still
bounded rather than law-like:

- `N = 60`
  - best mass window: `anchor_b = 5.0`, `delta ~= 0.8676 * M^0.462`, `R^2 = 0.923`
  - best distance tail: `mass_count = 5`, `peak_thr = 3.0`, `delta ~= 0.8858 * b^0.307`, `R^2 = 0.872`
- `N = 80`
  - best mass window: `anchor_b = 5.0`, `delta ~= 1.0791 * M^0.458`, `R^2 = 0.820`
  - best distance tail: no review-safe promoted fit
- `N = 100`
  - best mass window: `anchor_b = 6.0`, `delta ~= 1.0027 * M^0.204`, `R^2 = 0.568`
  - best distance tail: `mass_count = 4`, `peak_thr = 1.0`, `delta ~= 0.9961 * b^0.140`, `R^2 = 0.321`

## Cleanup Conclusion

The wider gravity-law cleanup did not produce a review-safe promoted law.

The retained exact 2D mirror gravity story is still:

- positive
- bounded
- weakly fit-dependent

So the conservative synthesis is:

- **exact 2D mirror = review-safe bounded coexistence pocket**
- **exact 2D mirror = no clean promoted mass law**
- **exact 2D mirror = no clean promoted distance law**

The family remains scientifically useful, but on the gravity side it is still a
bounded pocket rather than a law-like result.

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

## What would close this lane (Path A future work)

Reinstating a promoted 2D mirror gravity law would require:

1. A registered runner whose mass-exponent fit clears a hard `R^2`
   threshold (e.g. `R^2 >= 0.95`) on at least three sizes — the current
   best is `R^2 = 0.923` at `N = 60` and degrades to `R^2 = 0.568` at
   `N = 100`.
2. A registered runner whose distance-tail fit clears the same hard
   threshold — currently the `N = 80` row has no review-safe fit and
   `N = 100` has `R^2 = 0.321`.
3. A first-principles argument that the fitted exponent is the
   mass-coupling exponent, not just an empirical curve fit.
