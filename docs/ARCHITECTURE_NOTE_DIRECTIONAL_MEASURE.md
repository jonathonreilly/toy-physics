# Architecture Note: Directional Path Measure

**Status:** provisional lead candidate for unitary propagator
**Date:** 2026-04-01

## Propagator

```
amplitude(edge) = exp(i k S_spent) / L^p × exp(-β θ²)
```

- `S_spent = delay - sqrt(delay² - L²)`
- `θ = acos(dx/L)` in 3D, `atan2(|dy|, dx)` in 2D
- `β = 0.8`

The directional weight penalizes edges that deviate from the forward (layer) direction. It is field-independent, scale-free, and multiplicative.

## Tested constraints

| test | 2D DAGs | 3D DAGs |
|---|---|---|
| Born rule (I₃) | 9.2e-16 PASS | — |
| interference (V) | 0.998 PASS | fixed-DAG smoke PASS (`V = 0.9963`) |
| linearity / normalization smoke | implied by path-sum form | fixed-DAG smoke PASS (`3.18e-14`, norm err `0`) |
| k=0 → zero | 0.000000 PASS | 0.000000 PASS |
| gravity sign | 90%+ attract | 5/8 attract |
| gravity scaling | R@25 ≥ R@12 PASS | R increases with N |
| family transfer | r=2..5 DAGs, neutral on trees | — |
| R_c compat | 8/10 (2 edge cases) | — |
| decoherence scaling | FAIL (purity rises) | — |
| b-dependence | mixed: raw R increases with b, but bounded response-density diagnostics decrease with b; the hierarchy transfers to the tree control and the crossover reduces to `lambda = h_mass / b` | — |

## What this establishes

The flat path measure (uniform weight over all causal paths) was causing CLT saturation of gravity. Adding a directional continuation preference prevents that saturation while preserving interference, Born rule, and k=0→0.

The directional weight also has a clean 3D generalization as `acos(dx/L)`
without modification. A bounded fixed-DAG smoke test now says this is not just
gravity-side support: the same 3D rule shows a real zero-field interference
pattern and preserves source-superposition linearity to machine precision.

The role of this note is now sharper after the topology pivot:

- this directional measure is the **retained unitary layer**
- it is not, by itself, the decoherence solution
- but it is the unitary core used in the later modular / gap-controlled DAG
  results where **both gravity and decoherence work on the same family**

## What this does not establish

- Decoherence scaling is not addressed. This is expected: the directional weight modifies the unitary propagator, and decoherence is a non-unitary (record/environment) problem.
- The 3D support is still a smoke package, not a full 3D Sorkin / three-slit theorem.
- The raw b-dependence (deflection/readout increasing with impact parameter) is not fixed. A bounded geometry-normalized response-density diagnostic now decreases with b on the tested random-DAG family, and the current bounded hierarchy is sharper than before: center-offset density is the asymptotic leading term, nearest-edge density `b - h_mass` is the robust finite-source correction once the source width is widened, and support-gap is a secondary discrete packet-support correction. The reduced-variable picture is now two-layered: `lambda = h_mass / b` is the compact crossover control, while `mu = edge_b / h_mass = 1 / lambda - 1` is the cleaner signed overlap diagnostic. Tree-like controls keep large positive `mu`, while widened dense families force the finite-source correction once low-`b` corners cross into `mu <= 0`, even though pure `response / b` still survives on the bounded family once singular center-offset trials are excluded. The low-`b` onset cards now support a sharper mechanism claim: sparse target-band occupancy is the leading transferable overlap-onset signal, while coarse local spacing is a family-dependent refinement. Tree layers densify around the target plane, while dense random-DAG layers keep only about `1-2` nodes in that band and therefore have to stretch widened source windows across much larger `y` gaps; on the second dense-family holdout, the original gap/span clause softens but an occupancy floor still isolates the overlap rows cleanly. A combined occupancy bridge card now compresses that further: across the original and holdout dense families together, `target_fill <= 0.4` captures `23/24` overlap rows, while no overlap rows survive once `target_fill > 2/3`, so occupancy shortage is now the promoted coarse bridge variable and spacing stays secondary.
- β = 0.8 is empirically chosen. A derivation from the axioms or from the graph's intrinsic geometry is still needed.
- The 2 R_c edge cases mean the weight slightly narrows the zero-field interference threshold at some geometries.

## Axiom connection

- Axiom 6 (continuation prefers local coherence): the weight directly implements this
- Axiom 3 (space inferred): the angle is intrinsic to the graph, not imposed
- This is a path-measure correction, not a new dynamical law

## Next work

The propagator is no longer the bottleneck. The next frontier is:
1. dynamic emergence of the topology that lets the retained non-unitary IF / CL route work
2. `b`-dependence as a separate gravity-sector question, now narrowed to deriving the asymptotic `b` leading term, its `b - h_mass` finite-source correction, and translating the promoted occupancy-shortage bridge (`target_fill`) into a cleaner layer-density / mass-geometry explanation for why dense families drive the overlap-margin diagnostic `mu = edge_b / h_mass` through zero while tree-like controls stay safely positive
3. principled derivation of `beta` from graph geometry
4. transfer of the joint gravity+decoherence story to dynamically generated or higher-dimensional graph families
