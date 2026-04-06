# Causal-Escape Window: Qualitative Regime

**Date:** 2026-04-06
**Status:** retained positive — escape regime exists but mechanism is exposure reduction, not irreducible cone geometry

## Artifact chain

- [`scripts/causal_escape_window.py`](../scripts/causal_escape_window.py)
- This note

## Question

Is there a regime where the instantaneous field traps the beam but
the causal field allows escape?

## Result: YES

At eta=20, s=0.004, c=0.25:

| Field | Escape | Status |
| --- | ---: | --- |
| Instantaneous | 0.39 | **TRAPPED** (≤0.5) |
| Forward-only (static proxy) | 0.56 | not escaping (< 0.85) |
| Dynamic (c=0.5) | 0.90 | **ESCAPES** (≥0.85) |
| Dynamic (c=0.25) | 0.97 | **ESCAPES** (≥0.85) |

## Gates

| Gate | Result | Pass? |
| --- | --- | --- |
| eta=0 null | All = 1.000000 | YES |
| inst trapped (≤0.5) | 0.39 | YES |
| dyn escapes (≥0.85) | 0.97 | YES |
| static proxy NOT escaping | 0.56 | YES |
| Portable (3 families) | 0.976, 0.977, 0.975 | YES |
| Seed robust (4 seeds) | 0.97-0.99 | YES |

## Static-proxy discriminator

The forward-only static field (same 1/r profile, just truncated at
the source layer) gives escape = 0.56. This is OUTSIDE the escape
window (< 0.85). Only the dynamic cone with finite propagation speed
produces escape.

The causal cone is not merely a truncation — it restricts the field
to a narrow transverse region at each layer, reducing the effective
trap strength much more than forward-only truncation.

## What this means

The escape window is real:
- Instantaneous gravity traps the beam (61% absorbed)
- Causal gravity lets it escape (3% absorbed)
- The forward-only static proxy does NOT reproduce escape (44% absorbed)

However, an exposure-matched static proxy (uniform per layer, same average
field as the dynamic cone) DOES reproduce escape. The mechanism is
average-exposure reduction: the causal cone restricts the field spatially,
lowering the total field the beam encounters. Any static field with the
same average gives the same escape.

## Claim boundary

The causal-escape window is a retained, portable, qualitative regime
where the beam's fate (trapped vs escapes) depends on whether the
gravitational field propagates causally or instantaneously.

## Boundary law

At the inst trap threshold (eta_crit = 14.7, inst escape = 0.50):

| c | dyn escape | Status |
| ---: | ---: | --- |
| 2.0 | 0.75 | marginal |
| 1.0 | 0.82 | marginal |
| 0.5 | 0.92 | ESCAPES |
| 0.25 | 0.98 | ESCAPES |
| 0.1 | 1.00 | ESCAPES |

Critical cone speed: c_crit ~ 0.7 for escape at the inst trap point.

eta_max(c) where dyn escape drops to 0.85:

| c | eta_max |
| ---: | ---: |
| 2.0 | 8 |
| 1.0 | 12 |
| 0.5 | 33 |
| 0.25 | 250 |
| 0.1 | 500+ |

Approximately eta_max ~ 1/c^2. Slower cone → vastly more protection.

## S-dependence (eta=20, c=0.25)

| s | inst escape | dyn escape | ratio |
| ---: | ---: | ---: | ---: |
| 0.001 | 0.79 | 0.99 | 1.3 |
| 0.004 | 0.39 | 0.97 | 2.5 |
| 0.016 | 0.03 | 0.92 | 33 |

Protection grows strongly with field strength.

## Static-proxy discriminator

Forward-only static field gives escape = 0.56 at eta=15 — OUTSIDE the
escape window (< 0.85).

However, an **exposure-matched** static field (uniform per layer, with
the same per-layer average as the dynamic cone) gives escape = 0.987 —
INSIDE the escape window. This means:

- The escape mechanism is **average-exposure reduction**, not cone geometry
- The dynamic cone restricts the field spatially, lowering the average
  field the beam encounters
- Any static field with the same average exposure produces the same escape
- The cone geometry per se is NOT an irreducible discriminator

The retained discriminator is: forward-only (same 1/r structure but
unmatched exposure) does NOT escape, while exposure-matched (different
structure, matched exposure) DOES. The causal effect is quantitative
(how much field the beam sees), not geometric (the shape of the field).

This does NOT claim:
- Equivalence to black hole escape physics
- A specific physical trap geometry
- Self-consistency of the field (the cone is imposed)
