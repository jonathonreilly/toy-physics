# Source-Resolved Wavefield Mechanism Note

**Date:** 2026-04-05  
**Status:** retained exact-lattice wavefield mechanism probe on the larger exact family

## Artifact chain

- [`scripts/source_resolved_wavefield_mechanism.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_wavefield_mechanism.py)
- [`logs/2026-04-05-source-resolved-wavefield-mechanism.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-wavefield-mechanism.txt)

## Question

Can the strongest retained exact-lattice wavefield lane be pushed one step
past a pure source-strength law and into a more structural mechanism question?

This probe asks whether the detector-line phase-ramp observable depends not
just on source strength, but also on source-detector depth on the retained
exact family.

This stays narrow:

- one larger exact lattice family at `h = 0.25`
- one exact zero-source reduction check
- one instantaneous `1/r` control
- one same-site-memory control
- one finite-speed wavefield candidate
- a small source-layer scan on the retained family
- the promoted observable:
  detector-line phase-ramp slope and span, plus their depth dependence

## Mechanistic idea

The earlier wavefield cards already established that the detector-line ramp is
coherent and source-strength dependent.

This mechanism probe asks the harder question:

- does the ramp coefficient also change when the source is moved deeper or
  shallower relative to the detector plane?

If yes, that is a better bridge to causal-field intuition than a pure
amplitude-law fit.

## Retained result

This probe does not add a new law fit. It adds a mechanism control:
the detector-line phase-ramp steepens as the source moves closer to the
detector plane, while the weak-field `F~M` class stays near unity.
It remains on the retained exact-family `TOWARD` branch established by the
parent wavefield cards.

Measured on the retained exact family at `h = 0.25`:

- exact zero-source reduction survives
  - same-site shift span: `+0.000000e+00 .. +0.000000e+00`
  - wavefield shift span: `+0.000000e+00 .. +0.000000e+00`
- source-layer scan at layers `1, 2, 3, 4` with detector layer fixed at the far plane
- phase-ramp slope becomes more negative as depth decreases:
  - layer 1, depth 31: mean ramp slope `-0.2422`, `R^2 = 0.969`
  - layer 2, depth 30: mean ramp slope `-0.2718`, `R^2 = 0.967`
  - layer 3, depth 29: mean ramp slope `-0.2989`, `R^2 = 0.966`
  - layer 4, depth 28: mean ramp slope `-0.3226`, `R^2 = 0.965`
- mean phase lag also steepens monotonically:
  - `-0.589`, `-0.696`, `-0.793`, `-0.877`
- wave/same detector-line ratio stays large:
  - `36.092`, `39.213`, `42.094`, `44.431`
- depth scaling of the phase-ramp coefficient:
  - slope exponent `-2.77`
  - span exponent `-2.65`

The retained interpretation is narrow:

- the phase-ramp observable remains coherent
- the ramp coefficient depends systematically on source depth
- weak-field mass scaling stays near linear on the same exact family
- this is a mechanism-level refinement of the exact-lattice wavefield lane,
  not a continuum theorem or a generated-geometry transfer claim

## Safe claim surface

The claim surface should stay narrow:

- exact zero-source reduction must survive
- `TOWARD` must survive on the retained exact family
- `F~M` must remain near unity
- the phase-ramp observable should remain coherent
- the new ingredient is a source-depth dependence of the ramp coefficient

What this is not:

- not a continuum theorem
- not generated-geometry transfer
- not an absolute amplitude claim for experiment

## Branch Verdict

Treat this as a mechanism-level refinement of the exact-lattice wavefield
lane:

- the detector-line phase ramp remains the promoted observable
- the new question is whether its coefficient depends systematically on source
  depth as well as source strength
- if it does, that is the cleanest exact-lattice step toward a causal-field
  interpretation
