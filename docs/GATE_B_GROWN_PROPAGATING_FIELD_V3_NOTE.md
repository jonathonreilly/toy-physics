# Gate B Grown Propagating Field V3 Note

**Date:** 2026-04-05  
**Status:** bounded no-go for the frontier-echo self-consistent propagating-field architecture on the retained grown row

## Artifact chain

- [`scripts/gate_b_grown_propagating_field_v3.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_propagating_field_v3.py)
- [`logs/2026-04-05-gate-b-grown-propagating-field-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-propagating-field-v3.txt)

## Question

Can a genuinely more radical grown-geometry causal-field architecture, driven by a matched signal-minus-control frontier observable, produce a meaningful causal response while still reducing exactly back to the retained trap/control baseline at `chi = 0`?

This v3 probe stays narrow, but it is materially different from the previous no-gos:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- one static source-resolved baseline field
- one structural trap slab on the retained row
- one matched-control shell slab with the same cardinality but a frontier-shell placement
- one self-consistent frontier-echo field driven by the signal-minus-control detector-shell and detector-phase observables
- exact `chi = 0` reduction check
- promoted observables:
  - matched detector escape shift
  - matched detector shell-contrast shift
  - matched detector phase-slope shift

## Architecture

This is not another gamma blend, memory tweak, or beam-density feedback loop.

The feedback source is a matched-null frontier observable:

1. propagate the signal geometry through the current field
2. propagate the matched-control geometry through the same field
3. measure the signal-minus-control shell / phase / escape shifts relative to the `chi = 0` baseline
4. seed a detector-frontier echo field from those matched shifts
5. back-propagate that echo through the grown layers with a discrete wave-like recurrence
6. add the echo back into the field for the next iteration

The exact zero-coupling reduction is the important guardrail:

- `chi = 0` must reproduce the retained trap/control baseline exactly
- the matched shifts must vanish at `chi = 0`

## Frozen Result

The exact reduction passes.

But the promoted observables stay weak:

| `chi` | `signal escape` | `control escape` | matched escape shift | matched shell shift | matched phase shift | residual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.05` | `0.979` | `0.975` | `+0.004` | `+0.0002` | `+0.0001` | `1.508e-03` |
| `0.10` | `0.960` | `0.952` | `+0.008` | `+0.0004` | `+0.0002` | `3.008e-03` |
| `0.20` | `0.926` | `0.913` | `+0.013` | `+0.0006` | `+0.0003` | `6.024e-03` |
| `0.35` | `0.887` | `0.870` | `+0.017` | `+0.0008` | `+0.0005` | `1.056e-02` |
| `0.50` | `0.859` | `0.844` | `+0.015` | `+0.0009` | `+0.0010` | `1.509e-02` |

Weak-field mass-scaling sanity:

- `F~M` at `chi = 0`: `n/a` in this setup because the exact reduction forces the shift signal to zero
- `F~M` at `chi = 0.5`: `-0.021`

## Safe Read

The narrow, honest statement is:

- `chi = 0` is an exact matched-null reduction to the retained trap/control baseline
- the matched-shell and matched-phase observables do move with `chi`
- but the movement is tiny, and the residuals stay small enough that this still looks like a bounded transport modulation rather than a new propagating-field sector
- the weak-field sanity check is not salvaged; it is essentially flat at `chi = 0.5`

## Guardrail Note

This probe is intentionally stricter than the earlier v1/v2/radical no-gos.

It does not use density/current backreaction.
It does not use a simple layer-memory gamma blend.
It does not use the beam-sourced self-consistent field that already failed.

Even so, the new frontier-echo feedback does not generate a retained causal-field observable large enough to count as a new grown-geometry propagating-field architecture.

## Branch Verdict

Treat this as a bounded no-go.

The exact matched-null reduction is real, but the frontier-echo feedback does not produce a meaningful causal observable beyond a tiny transport modulation.
