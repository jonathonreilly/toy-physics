# Gate B Strong-Field Observable Split Note

**Date:** 2026-04-05  
**Status:** failure-audit synthesis on two retained grown-row probes

## Artifact chain

- [`docs/GATE_B_COMPLEX_ACTION_FALSIFIER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_COMPLEX_ACTION_FALSIFIER_NOTE.md)
- [`docs/GATE_B_GROWN_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_PROPAGATING_FIELD_NOTE.md)

## Question

The recent retained-grown-family strong-field probes disagree:

- the absorptive / complex-action proxy changes detector escape sharply
- the minimal causal-memory / retarded-like probe keeps escape at `1.000` and
  leaves the detector phase ramp flat

Is that mismatch telling us we picked the wrong observable family, or are the
two probes actually testing different mechanisms?

## Comparison

The two retained probes live on the same grown row (`drift = 0.2`,
`restore = 0.7`) but they do not perturb the system in the same way:

- the absorptive proxy changes the amplitude budget directly through `gamma`
- the causal-memory proxy changes only the layerwise field history and keeps
  exact `gamma = 0` reduction to the static baseline

Frozen readouts:

- absorptive proxy:
  - `escape(gamma)` drops from `0.215` to `0.000` as `gamma` increases from
    `0.05` to `0.50`
  - the detector centroid shifts slightly away from the mass side
  - the effect survives exact `gamma = 0` reduction
- causal-memory proxy:
  - `escape` stays at `1.000` to three decimals
  - detector-line phase ramp stays flat
  - only a tiny centroid shift survives
  - exact `gamma = 0` reduction also survives

## Safe read

The narrow, honest conclusion is:

- these are **not** the same mechanism
- the absorptive proxy is sensitive to attenuation of detector amplitude
- the minimal causal-memory proxy is too weak to produce a coherent causal
  observable on the retained grown row

So the mismatch is **not** just one bad observable choice.

It is more informative than that:

- the absorptive proxy is a real strong-field amplitude effect
- the minimal causal-memory probe is a clean no-go for propagating causality
  in that exact form

## Failure-Audit Verdict

Treat the causal-memory / retarded-like grown-row probe as a robust no-go for
that minimal architecture.

Treat the absorptive / complex-action proxy as a separate, bounded strong-field
observable that is still useful, but not evidence for a causal field.

## Branch implication

The next grown-family causal-field attempt should not be a small gamma tweak.
It needs a stronger architecture than simple layer-memory blending if it is to
produce a phase-ramp or escape observable beyond the static baseline.
