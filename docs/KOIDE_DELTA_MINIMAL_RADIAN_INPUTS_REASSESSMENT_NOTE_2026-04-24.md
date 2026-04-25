# Koide delta minimal radian-inputs reassessment

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_minimal_radian_inputs_reassessment.py`  
**Status:** reassessment; delta remains open

## Purpose

The older radian-bridge no-go named three minimal structural inputs that could
close the selected Brannen phase:

1. `Z3` orbit Wilson `d^2`-power quantization;
2. lattice propagator radian quantum;
3. `hw=1+baryon` non-uniform Wilson holonomy.

This packet attacks all three.

## Results

### 1. `Z3` Wilson `d^2`-power Quantization

Finite `C3` gives `W^9=1`, not `exp(2i)`.  Spin lift gives `W^9=-1`.
Projective phases are rephasable.  Imposing `W^9=exp(2i)` is exactly the new
`U(1)` Wilson radian-unit law.

### 2. Lattice Propagator Radian Quantum

One-clock `C3`-equivariant selected propagation allows

```text
G(1)=exp(i lambda)G0
```

with `lambda` free.  The closed APS scalar gives support `eta_APS=2/9`, but
the open propagator readout still has `lambda=s eta_APS+c`.

### 3. `hw=1+baryon` Wilson Holonomy

A `4x4` carrier can fix total support

```text
theta_selected + theta_baryon = eta_APS.
```

It does not force `theta_baryon=0` or endpoint offset `c=0`.

## Unified Residual

The three attacks all reduce to the same theorem:

```text
physical selected Brannen endpoint
  = based, orientation-preserving, primitive unit-degree image
    of the closed APS/Dirac class,
with no spectator channel and no endpoint counterterm.
```

Equivalently:

```text
mu = 1
c = 0
spectator_channel = 0
```

## Verdict

```text
KOIDE_DELTA_MINIMAL_RADIAN_INPUTS_REASSESSMENT=TRUE
DELTA_MINIMAL_RADIAN_INPUTS_CLOSES_DELTA=FALSE
RESIDUAL_PRIMITIVE=retained_selected_endpoint_radian_unit_support_law
RESIDUAL_SCALAR=selected_endpoint_degree_mu_minus_one_and_offset_c
NEXT_ATTACK=derive_selected_endpoint_radian_unit_support_law
```

## Verification

```bash
python3 scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py
python3 scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py
python3 scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py
python3 scripts/frontier_koide_delta_minimal_radian_inputs_reassessment.py
```
