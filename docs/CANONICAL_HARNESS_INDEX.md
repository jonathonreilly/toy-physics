# Canonical Harness Index

**Date:** 2026-04-04  
**Status:** retained harness index for reproduction and review

This index separates the scripts that new readers should treat as canonical
harnesses from the scripts that are still exploratory drivers.

## Canonical harnesses

These are the scripts and notes a skeptical reader should start from:

- [`scripts/canonical_regression_gate.py`](/Users/jonreilly/Projects/Physics/scripts/canonical_regression_gate.py)
- [`scripts/reproduction_audit_harness.py`](/Users/jonreilly/Projects/Physics/scripts/reproduction_audit_harness.py)
- [`scripts/mirror_2d_validation.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_2d_validation.py)
- [`scripts/mirror_mutual_information_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_chokepoint.py)
- [`scripts/mirror_chokepoint_joint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_chokepoint_joint.py)
- [`scripts/structured_chokepoint_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/structured_chokepoint_bridge.py)
- [`scripts/structured_chokepoint_bridge_extension.py`](/Users/jonreilly/Projects/Physics/scripts/structured_chokepoint_bridge_extension.py)
- [`scripts/lattice_3d_dense_10prop.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_10prop.py)
- [`scripts/lattice_3d_dense_window_extension.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_window_extension.py)
- [`scripts/lattice_3d_dense_refinement_reconciliation.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_refinement_reconciliation.py)
- [`scripts/gravity_observable_hierarchy.py`](/Users/jonreilly/Projects/Physics/scripts/gravity_observable_hierarchy.py)
- [`scripts/lattice_3d_l2_canonical_card.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_canonical_card.py)
- [`scripts/lattice_3d_l2_fast.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_fast.py)
- [`scripts/lattice_3d_l2_tail_stats.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_tail_stats.py)
- [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)
- [`scripts/lattice_nn_deterministic_rescale.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_deterministic_rescale.py)

Canonical notes:

- [`docs/START_HERE.md`](/Users/jonreilly/Projects/Physics/docs/START_HERE.md)
- [`docs/UNIFIED_PROGRAM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/UNIFIED_PROGRAM_NOTE.md)
- [`docs/CONTINUUM_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_BRIDGE_NOTE.md)
- [`docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md)
- [`docs/STRUCTURED_CHOKEPOINT_BRIDGE_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_CHOKEPOINT_BRIDGE_EXTENSION_NOTE.md)
- [`docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
- [`docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md)
- [`docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md)

## Bounded companion harnesses

These are useful and often still review-relevant, but they are not the first
thing a new reader should treat as canonical proof of the current story:

- [`scripts/valley_linear_same_harness_compare.py`](/Users/jonreilly/Projects/Physics/scripts/valley_linear_same_harness_compare.py)
- [`scripts/lattice_3d_valley_linear_card.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_valley_linear_card.py)
- [`scripts/lattice_4d_kernel_test.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_4d_kernel_test.py)
- [`scripts/transfer_norm_and_born.py`](/Users/jonreilly/Projects/Physics/scripts/transfer_norm_and_born.py)
- [`scripts/cross_family_robustness.py`](/Users/jonreilly/Projects/Physics/scripts/cross_family_robustness.py)
- [`scripts/evolving_network_prototype.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype.py)

## How to use them

- Start with `scripts/reproduction_audit_harness.py` for a quick skeptical
  replay.
- Add `--include-gate` when you want the full retained-frontier gate replay.
- Add `--full-cross-family` only when you specifically want the heavier 3D
  family sweep from the exploratory robustness lane.

## Legacy exploratory drivers

Treat these as historical experiments unless a newer note explicitly promotes
them:

- [`scripts/causal_field_full_test.py`](/Users/jonreilly/Projects/Physics/scripts/causal_field_full_test.py)
- [`scripts/continuum_limit_test.py`](/Users/jonreilly/Projects/Physics/scripts/continuum_limit_test.py)
- [`scripts/lorentz_symmetry_test.py`](/Users/jonreilly/Projects/Physics/scripts/lorentz_symmetry_test.py)
- [`scripts/three_d_joint_test.py`](/Users/jonreilly/Projects/Physics/scripts/three_d_joint_test.py)

## Reading rule

If a claim only appears in an exploratory driver, or only in chat / commit
language, treat it as unretained until the script / log / note chain lands.
