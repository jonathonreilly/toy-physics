# Koide April 22 Axiom-Native Support Batch

**Date:** 2026-04-22  
**Scope:** Charged-lepton Koide support additions landed after the April 21
review package.  
**Status:** Bounded support batch. This note does **not** promote charged-lepton
Koide closure.

## What this batch adds

This batch adds new executable support tools and bridge-targeting diagnostics
to the charged-lepton lane:

- explicit `Z_3` weight-uniqueness verification on the charged-lepton triplet;
- selected-line axis/Fourier bridge calculations on the retained selected line;
- positive-parent / `sqrt(m)` construction attempts and related carrier checks;
- mass-assignment and set-equality reframings of the charged-lepton readout;
- hierarchy derivation audit consolidating the retained `v_EW` chain;
- explicit zero-mode / APS and radiative Yukawa support calculations;
- an integrated regression runner for the enlarged Koide support stack.

These additions materially improve atlas reuse and future closure targeting.

An additional April 22 support addendum now also lands:

- exact selected-line Brannen geometry, including the rigid-triangle rotation
  picture and the exact first-branch span `π/12 = 2π/|O|`;
- a clearly named conditional Route-3 Wilson-line support law on the
  one-clock natural-time route;
- an explicit finite-lattice `L = 3` Wilson-Dirac illustration showing
  recurrence of per-fixed-site `η = 2/9` on the natural 3-generation carrier.

A further April 22 support layer now also lands:

- an exact second-order `Q` support batch that isolates the first-live
  second-order readout quotient, the unique minimal scale-free selector
  variable on that carrier, the exact reduced two-block observable law, and a
  no-hidden-source audit that compresses the remaining `Q` gap to one explicit
  primitive: why the physical charged-lepton selector is source-free on the
  normalized second-order carrier.

## What this batch does not close

The open scientific status is unchanged.

### 1. The `Q = 2/3` physical/source-law bridge remains open

The package still does not derive why the physical charged-lepton packet must
extremize the block-total Frobenius functional. The new April 22 scripts add
bridge candidates, consistency checks, and reformulations, but they do not
discharge that physical identification theorem.

The second-order addendum sharpens that statement further: the remaining
primitive is no longer best read as “find the right extremal functional,” but
as “derive why the physical charged-lepton selector is source-free on the
normalized second-order reduced carrier.”

### 2. The `δ = 2/9` physical Brannen-phase bridge remains open

The package still does not derive why the physical Brannen phase on the
selected-line `CP^1` carrier equals the ambient APS invariant. The new
zero-mode / APS scripts strengthen that route and provide cleaner candidate
structures, but they do not remove the need for the physical-observable bridge.

### 3. The overall charged-lepton scale `v_0` remains a separate support lane

The radiative Yukawa support scripts materially sharpen the `m_τ` / `v_0`
story, especially by isolating the charged-lepton-specific Casimir route.
They still rely on textbook electroweak normalization choices and remain a
support lane rather than a retained closure theorem.

## How to use this batch

Use these scripts as:

- atlas tools for future Koide bridge work;
- executable support when reviewing the charged-lepton lane;
- candidate-bridge diagnostics, not as authority for front-door closure claims.

## Main artifacts

### Integrated runners

- `scripts/frontier_koide_lane_regression.py`
- `scripts/frontier_koide_equivariant_berry_aps_selector.py`
- `scripts/frontier_koide_dirac_zero_mode_phase_theorem.py`
- `scripts/frontier_koide_brannen_route3_geometry_support.py`
- `scripts/frontier_koide_brannen_dirac_support.py`
- `scripts/frontier_charged_lepton_radiative_yukawa_theorem.py`

### Supporting bridge tools

- `scripts/frontier_koide_hierarchy_derivation_audit.py`
- `scripts/frontier_koide_mass_assignment_derivation.py`
- `scripts/frontier_koide_name_free_set_equality.py`
- `scripts/frontier_koide_p1_sqrtm_amplitude_derivation.py`
- `scripts/frontier_koide_positive_parent_operator_construction.py`
- `scripts/frontier_koide_q_equals_lefschetz_sum.py`
- `scripts/frontier_koide_real_irrep_block_democracy.py`
- `scripts/frontier_koide_selected_line_axis_fourier_bridge.py`
- `scripts/frontier_koide_z3_weight_uniqueness.py`

## Bottom line

This batch should be read as a **support expansion** of the April 21 Koide
package. It makes the remaining open bridges more explicit and gives future
closure work better tools, but it does not change the current public status:

- `Q = 2/3` support is stronger, not closed;
- `δ = 2/9` support is stronger, not closed;
- `v_0` support is stronger, not closed.

For the Brannen-specific addendum, see
`docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`.
For the second-order `Q` addendum, see
`docs/KOIDE_Q_SECOND_ORDER_SUPPORT_BATCH_NOTE_2026-04-22.md`.
