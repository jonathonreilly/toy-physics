# Exact 2D Mirror Gravity-Law Cleanup Note

**Date:** 2026-04-03  
**Status:** gravity-law cleanup complete; no clean 2D mirror law promoted

This note freezes the exact 2D mirror gravity-law cleanup lane.

It uses the exact 2D mirror family retained in:

[`scripts/mirror_2d_validation.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_2d_validation.py)

and the cleanup sweep:

[`scripts/mirror_2d_gravity_law_cleanup.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_2d_gravity_law_cleanup.py)

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
