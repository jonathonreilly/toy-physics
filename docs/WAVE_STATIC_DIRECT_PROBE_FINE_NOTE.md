# Wave Static Direct-Comparator Fine Check

**Date:** 2026-04-08
**Status:** proposed_retained fine-point negative — on the moving-source Lane 6 setup at `H = 0.25`, the exact direct discrete static solve gives `dS = +0.011563` with residual `2.000e-10`, but it does **not** improve on the best existing comparator. Its mismatch to the retarded field is `rel_MS = 37.62%`, worse than the equilibrated cached-static comparator's `rel_MIeq = 23.16%`. So the simple "exact direct static solve at the same beam box rescues the moving-source magnitude" story does not land at the fine point.

## Artifact chain

- [`scripts/wave_static_direct_probe.py`](../scripts/wave_static_direct_probe.py)
- [`scripts/wave_static_direct_probe_freeze.py`](../scripts/wave_static_direct_probe_freeze.py)
- [`logs/2026-04-08-wave-static-direct-probe.txt`](../logs/2026-04-08-wave-static-direct-probe.txt)

## Question

The exact discrete static comparator remained scientifically alive after the
frozen-source and shared-geometry probes:

- frozen off-center source: `dS` tracked `dM` closely
- matrix-free engine: matches the direct static solve on a shared geometry

The next narrow question is stricter:

> On the actual moving-source lane, at the finest retained H point, does the
> exact direct static comparator beat the best current approximate comparator
> (`dIeq`)?

## Result

Fine point only: moving-source Lane 6 setup at `H = 0.25`.

| quantity | value |
| --- | ---: |
| `dM` | `+0.007212` |
| `dI` | `+0.012743` |
| `dIeq` | `+0.005542` |
| `dS` | `+0.011563` |
| `rel_MI` | `43.40%` |
| `rel_MIeq` | `23.16%` |
| `rel_MS` | `37.62%` |
| `rel_IeqS` | `52.07%` |
| worst static residual | `2.000e-10` |

## Honest read

This is a clean negative for the simplest direct-static rescue:

- the exact discrete static solve is numerically clean (`~2e-10` residual)
- but on the real moving-source lane it sits far from both `dM` and `dIeq`
- at this fine point, `dIeq` is still the least-bad comparator

So the direct-static result is now split:

- **frozen-source diagnostic:** useful
- **moving-source fine-point magnitude rescue:** negative

That does **not** close the entire exact-comparator lane. One decisive run still
remains:

> the moving-source **fixed-beam boundary** test, where only the field box is
> widened while the beam DAG is held fixed.

If that boundary-controlled moving-source test still shows material `dS` / `rel_MS`
movement, the exact-comparator lane should be demoted behind direct-`dM`.

## Boundary

This note does **not** claim:

- that the exact comparator lane is fully closed
- that `dS` is worse than `dIeq` at all H values
- that the frozen-source positive is invalid

It only says:

> at the quoted fine point `H = 0.25`, on the actual moving-source lane,
> the direct static comparator does not beat `dIeq`.
