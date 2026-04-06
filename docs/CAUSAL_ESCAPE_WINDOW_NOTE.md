# Causal-Escape Window: Qualitative Regime

**Date:** 2026-04-06
**Status:** retained positive — qualitative causal-only escape regime confirmed

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

This is a **qualitative** result, not just quantitative:
- Instantaneous gravity traps the beam (61% absorbed)
- Causal gravity lets it escape (3% absorbed)
- No static field proxy reproduces this

The causal propagation speed creates a fundamentally different trapping
regime. This is the discrete analog of the fact that a causally
propagating gravitational field cannot trap light that's already
outside the light cone of the source.

## Claim boundary

The causal-escape window is a retained, portable, qualitative regime
where the beam's fate (trapped vs escapes) depends on whether the
gravitational field propagates causally or instantaneously.

This does NOT claim:
- Equivalence to black hole escape physics
- A specific physical trap geometry
- Self-consistency of the field (the cone is imposed)
