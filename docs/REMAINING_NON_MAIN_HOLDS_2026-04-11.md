# Remaining Non-Main Holds

**Date:** 2026-04-11  
**Scope:** review-worktree items that are still not safe for `main`

This is the consolidated inventory for follow-through. It names the missing
control for each held lane.

## Already on `main`

These are not part of the hold list:

- `ACTION_UNIQUENESS_AUDIT_2026-04-11.md`
- `scripts/action_uniqueness_investigation.py`
- `IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`
- `scripts/frontier_irregular_sign_core_packet_gate.py`
- `STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`
- `DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`
- `NEWTON_DERIVATION_NOTE.md`
- `NEWTON_PERSISTENT_PATTERN_CONTROL_NOTE_2026-04-11.md`
- `EMERGENT_PRODUCT_LAW_NOTE.md`
- `EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md`
- `scripts/frontier_emergent_product_law.py`
- `ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`
- `scripts/frontier_architecture_portability_sweep.py`

## Holds

### 0. Overnight Claude audit bundle

Files:

- `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `scripts/frontier_emergent_gr_signatures.py`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `scripts/frontier_electromagnetism_probe.py`
- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `scripts/frontier_second_quantized_prototype.py`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `scripts/frontier_holographic_entropy.py`
- `docs/HAWKING_ANALOG_NOTE.md`
- `scripts/frontier_hawking_analog.py`
- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `scripts/frontier_dimension_emergence.py`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `scripts/frontier_cosmological_expansion.py`
- `scripts/frontier_dispersion_relation.py`

Why held:

- the overnight branch contains useful new artifacts, but none of them crosses
  the current `main` retention bar without substantial narrowing
- GR-signatures and electromagnetism remain consistency checks rather than
  GR/Maxwell derivations
- second-quantized, holographic, and Hawking results remain prototype-scale
  field-theory probes
- dimension and cosmology remain bounded proxy studies
- the new dispersion runner is still an honest negative with anomalous scaling

Next control:

- use the lane-specific blockers in `OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- do not promote any of these files to `main` without a new bounded audit note

### 1. Wilson mutual-attraction side lane

Files:

- `docs/TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/WILSON_SIDE_LANE_PROMOTION_REVIEW_2026-04-11.md`
- `docs/WILSON_BOTH_MASSES_ACCEL_NOTE_2026-04-11.md`
- `docs/WILSON_CAUSAL_DISCRIMINATOR_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction.py`
- `scripts/frontier_two_body_attraction_robustness.py`
- `scripts/frontier_two_body_attraction_temporal_robustness.py`
- `scripts/frontier_wilson_both_masses_accel.py`
- `scripts/frontier_wilson_both_masses_local_balance.py`
- `scripts/frontier_wilson_causal_discriminator.py`

Why held:

- the open-Wilson mutual channel is real
- the early/mid-window near-inverse-square law is real
- the frozen/static-source control has now been run and still does not
  separate dynamic shared backreaction cleanly from a static explanation
- the lagged source-refresh discriminator has now been run and the response is
  still too adiabatic to isolate causal timing cleanly on this surface
- full Newton closure is still open

Next control:

- same open 3D Wilson surface
- if reopened, move to an intervention-style observable rather than another
  source-refresh lag
- do not promote until the causal discriminator is clean

### 2. Exact two-particle product law

Files:

- `docs/EXACT_TWO_PARTICLE_PRODUCT_LAW_FRONTIER_NOTE_2026-04-11.md`
- `scripts/exact_two_particle_product_law.py`

Why held:

- the bilinear factor is built into the Hamiltonian ansatz
- exact diagonalization confirms the imposed kernel, not emergent product law
- the model is a 1D open-boundary toy, not the primary staggered surface

Next control:

- move the bilinear factor out of the ansatz
- add a frozen/static-source control
- replay on the primary staggered/open-cubic surface

### 3. Irregular transport / portability beyond the bounded core-packet gate

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NEXT_STEPS_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_REINFORCEMENT_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_SIZE_PORTABILITY_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_OBSERVABLE_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_THIRD_FAMILY_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_reinforcement.py`
- `scripts/frontier_irregular_endogenous_sign_observable.py`
- `scripts/frontier_irregular_endogenous_sign_size_portability.py`
- `scripts/frontier_irregular_endogenous_sign_third_family.py`

Why held:

- the bounded core-packet same-surface separator is now retained on `main`
- what remains open is portability beyond that surface
- the third packet family still does not close the lane
- the size-portability sweep still fails to make the sign separator portable
  across graph growth
- the new transport observable improves the readout, but `cut2` still fails on
  most of the audited rows, so the lane is not yet portable or transport-closed

Next control:

- if reopened, do not rerun the retained core-packet gate
- use a portability-grade transport or invariant observable on the same
  irregular surface, not another packet-family sweep

### 4. Staggered two-body closure family

Files:

- `docs/STAGGERED_DIRECT_COM_CLOSURE_NOTE_2026-04-11.md`
- `docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_PORTABILITY_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_TRANSPORT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_LINK_CURRENT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_MOMENTUM_FLUX_NOTE_2026-04-11.md`
- `docs/STAGGERED_X_FLUX_REFINEMENT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_direct_com_closure.py`
- `scripts/frontier_staggered_both_masses.py`
- `scripts/frontier_staggered_two_body_portability.py`
- `scripts/frontier_staggered_two_body_transport.py`
- `scripts/frontier_staggered_two_body_link_current.py`
- `scripts/frontier_staggered_two_body_momentum_flux.py`

Why held:

- partner-force is real
- direct-CoM closure still fails
- both-masses closure is still negative / force-led
- detector-side transfer is still negative on the audited open-cubic surface
- the true link-current readout is still negative on the audited open-cubic
  surface
- the packet-local momentum-flux / impulse readout is also still negative on
  the audited open-cubic surface
- the x-directed shell-flux refinement fixes the sign gate, but the impulse
  remains non-convergent and the lane still lacks a retained trajectory law

Next control:

- stop centroid and shell-flux variants
- the current lane has now been tried; only a genuinely different conserved
  current or a different graph geometry would be credible if this family is
  revisited

## Bottom Line

The review worktree now contains explicit holds only. Nothing else should be
promoted without the missing control named in its section.
