# Inverse Problem: What Does Newton+Born Require of the Network?

**Status:** support — narrowed graph-requirements diagnostic. Honest narrowing
2026-05-10 to match the live runner output: the `heavy_delete_70` perturbation
is a TOWARD-failure on the bounded harness, so the original universal-robustness
phrasing is withdrawn and the surviving claim is the smaller one stated below.
**Claim type:** bounded_theorem
**Date:** 2026-04-04 (note); 2026-05-10 (rigorization sync)
**Primary runner:** scripts/inverse_problem_graph_requirements.py

## Bounded answer (narrowed)

On the retained 3D valley-linear family at `h=0.5`, `W=8`, `L=12`,
`max_d=3`, field strength `5e-5`, `mass_z=3.0`, `phase_k=5.0`, the runner
sweeps five graph variants and reports:

| Perturbation | Born | Gravity sign | Gravity magnitude | k=0 | no-field |
|---|---:|---:|---:|---:|---:|
| baseline | 2.35e-15 | TOWARD | +3.473338e-05 | 0.000000e+00 | 0.000000e+00 |
| heavy_delete_70 (70% random edge deletion) | 1.81e-15 | **AWAY** | -2.583639e-05 | 0.000000e+00 | 0.000000e+00 |
| asym_zpos_removed (z>0 edges removed) | 1.74e-15 | TOWARD | +2.105958e-05 | 0.000000e+00 | 0.000000e+00 |
| jitter_0.5h (transverse position jitter) | 2.35e-15 | TOWARD | +2.894246e-05 | 0.000000e+00 | 0.000000e+00 |
| sparse_nn_only (NN-only, max_d=1) | 3.90e-16 | TOWARD | +1.287412e-04 | 0.000000e+00 | 0.000000e+00 |

Born stays at machine precision on every variant, and the `k=0` and
`no-field` controls are exactly zero.

## What survives, what does not

What survives:

1. **Born cleanliness** holds on every tested variant.
2. **Field coupling and phase are necessary**: with `k=0` or no field,
   the gravity readout is identically zero on all five variants.
3. **Three of the four perturbations preserve TOWARD**: `asym_zpos_removed`,
   `jitter_0.5h`, and `sparse_nn_only` all report TOWARD on this harness.

What does **not** survive:

- The original "gravity survives all tested graph perturbations" framing is
  **falsified** by `heavy_delete_70`: removing 70% of edges flips the sign
  to AWAY (`-2.58e-05`) on this same setup. So the bounded harness shows a
  graph-class boundary, not a universality result.

## Bounded conclusion

On this harness, Born holds across all five graph variants, and TOWARD
gravity holds across the four non-heavy-delete variants (baseline,
asymmetric, jittered, sparse). Heavy random edge deletion
(70%) is a bounded counterexample: it preserves Born but breaks TOWARD.

The model is **forgiving but not unrestricted** about graph structure: a
graph that retains enough connectivity to support a coherent path sum
(jitter, asymmetry, even NN-only sparsity) gives TOWARD gravity, but
heavy random edge deletion at 70% is past that boundary on this setup.

The narrowed claim is:

> On the retained 3D valley-linear family with the parameters above, Born
> holds across baseline, heavy_delete_70, asym_zpos_removed, jitter_0.5h,
> and sparse_nn_only. TOWARD gravity holds for the four non-heavy-delete variants
> (baseline, asym, jittered, sparse) but **fails** for heavy_delete_70.

This is a bounded inverse-problem diagnostic, not a universal "graph
structure is irrelevant" theorem.

## What this means for downstream growth rules

The downstream guidance is correspondingly narrowed: a growth rule that
produces a causal graph with forward edges and roughly local connectivity
(NN-only is enough on this harness) gives TOWARD gravity. A rule that
randomly removes a large fraction of edges is **not** safe; the
heavy_delete_70 row shows the sign can flip.
