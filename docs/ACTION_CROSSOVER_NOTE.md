# Action Crossover: Spent-delay → Valley-linear with Regularity

**Date:** 2026-04-04
**Status:** Empirically confirmed — the bridge exists

## Finding

The optimal action formula transitions from spent-delay to valley-linear
as graph geometry becomes more regular:

| Regularity | Valley-linear | Spent-delay | Winner |
|-----------|--------------|-------------|--------|
| 0.0 (random) | 44% TOWARD | **67%** | Spent-delay |
| 0.2 | 56% | **67%** | Spent-delay |
| 0.4 | **67%** | 42% | Valley-linear |
| 0.6 | **61%** | 42% | Valley-linear |
| 0.8 | 61% | 61% | Tied |

Crossover at regularity ≈ 0.3-0.4.

## Interpretation

- **Spent-delay** S = dl - sqrt(dl^2 - L^2) is the better action on
  random DAGs because the sqrt(f) response handles the varied path
  lengths of irregular geometry.

- **Valley-linear** S = L(1-f) is the better action on regular geometry
  because the linear response gives coherent phase accumulation when
  paths have uniform structure.

- The **lattice** is the maximally regular limit, where valley-linear
  gives Newtonian gravity (F∝M=1.0, 1/b distance).

## The bridge

This crossover supports interpreting the two actions as the SAME theory
at different effective scales:

- Spent-delay = lattice-scale / UV effective action
- Valley-linear = continuum-scale / IR effective action

The transition between them is controlled by the regularity of the
geometry, which is analogous to an RG flow from discrete to continuum.

The model does NOT need two separate actions. It has ONE underlying
mechanism (phase valley from field distortion of continuation structure)
that manifests differently at different geometric scales.

## What this means for the axioms

Axiom 8 says: "Gravity is natural continuation in a distorted
continuation structure." Both actions satisfy this. The axiom is
scale-independent — it specifies the mechanism but not the formula.

The action formula is the effective description of how the mechanism
operates at a given geometric scale. This is no different from how
effective field theories in standard physics have running couplings
that depend on the energy scale.

## Scripts

- Inline test (in commit message — see git log)
- `lattice_3d_valley_linear_card.py` — canonical lattice card
- `dag_kernel_transfer.py` — DAG transfer test
