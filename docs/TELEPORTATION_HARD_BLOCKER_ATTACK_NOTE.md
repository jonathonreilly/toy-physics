# Teleportation Hard Blocker Attack Note

**Date:** 2026-04-26
**Status:** planning / hard-blocker attack artifact
**Runner:** `scripts/frontier_teleportation_hard_blocker_attack.py`

## Scope

This artifact attacks the five remaining nature-grade blockers in the native
taste-qubit teleportation lane. It does not claim nature-grade closure.

The important result is mixed:

- sole-axiom apparatus selection is now obstructed by explicit nonuniqueness;
- amplitude-level field-equation uniqueness is now obstructed by explicit
  nonuniqueness;
- sparse 3D scaling has a side-6 negative control;
- calibrated ideal pulse schedules now exist for the retained-axis record slots;
- a local material spin-bath detector model now realizes the detector theorem.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Apparatus Selection Obstruction

The previous pass proved uniqueness only inside the stabilizer-diagonal native
write class with a fixed Bell-record desideratum. This pass shows why the
stronger "sole axiom uniquely selects the apparatus" claim is not available.

For any integer winding `m`, the active pointer flip angle

```text
theta_m = pi/2 + pi m
```

writes the same computational record bit from an active stabilizer projector:

```text
exp(-i theta_m X) |0> = phase(m) |1>.
```

The runner compares `m=0` and `m=1`. Both are native stabilizer-controlled
Hamiltonians and both write the same four Bell records, but their spectral norms
differ:

```text
inequivalent_hamiltonians = 2
same_record_map = True
max_pointer_error = 0.000e+00
spectral_norm_difference = 18.849556
```

This is a no-go for unqualified sole-axiom apparatus uniqueness. A stronger
review claim would need either an extra selection principle, a quotient that
identifies these windings as equivalent, or a physical cost/action minimization
rule.

## Amplitude Field Obstruction

The prior artifact proved a unique causal support/eikonal front in the positive
nearest-neighbor support class. That does not uniquely determine amplitudes.

This runner evolves the same source support using two normalized local kernels:

```text
K_c = c self + (1-c)/6 sum_six_neighbors
```

with different `c`. Both kernels have the same support front and the same first
arrival times on the audited 3D box. Their amplitudes differ:

```text
amplitude_laws = 2
arrival_error = 0
support_mismatch = 0
final_l2_difference = 0.380510
center_amplitude_difference = 0.203711
```

This is a no-go for deriving a unique amplitude-level retained field equation
from support/eikonal requirements alone. A stronger claim needs an additional
action principle, unitary/current conservation condition, or normalization law.

## Sparse 3D Scaling Control

The previous sparse `3D side=4` row found a high-fidelity retained resource at
`G=5000`. This pass adds `3D side=6` sparse controls:

```text
side=4, G=5000:  Bell*=0.959247, Fbest=0.972831, CHSH=2.715608
side=6, G=5000:  Bell*=0.434463, Fbest=0.622976, CHSH=1.290888
side=6, G=10000: Bell*=0.468888, Fbest=0.645925, CHSH=1.642606
side=6, G=20000: Bell*=0.489775, Fbest=0.659850, CHSH=1.880897
```

The side-6 controls do not preserve the side-4 high-fidelity window. This is
not just "more work remains"; it is a scaling warning. The current Poisson
ground-state window cannot be promoted as asymptotic evidence without a new
scalable mechanism, different coupling scaling, boundary analysis, or
preparation theorem.

## Calibrated Pulse Schedule

The runner supplies an ideal square-pulse schedule for retained-axis record
slots:

```text
slot_count = 8
duration = 1
rabi_frequency = pi/2
```

For the default area error `0.01`, the worst bit error is:

```text
ideal_bit_error = 3.749e-33
jitter_bit_error = 1.000e-04
slot_spread = 0
```

This closes the purely algebraic pulse-schedule gap for an ideal retained-axis
square-pulse model. It does not supply a physical controller, bandwidth bound,
leakage model, fabrication tolerance, or noise-calibrated hardware schedule.

## Material Spin-Bath Detector Model

The independent-fragment detector theorem is now realized by an explicit local
spin-bath Hamiltonian model. Each record component couples to `F` bath
fragments through local controlled rotations:

```text
H_det = sum_{record slot r, fragment f} |1><1|_r tensor X_{r,f}.
```

The default run uses coupling angle `0.800` and `24` fragments per component:

```text
local_terms = 192
fragment_overlap = 0.696707
max_record_overlap = 1.466e-19
entropy_defect = 0.000e+00
term_commutator = 0.000e+00
```

This is a microscopic local spin-bath construction, not just an abstract overlap
bound. It is still not a material detector medium, continuum irreversible limit,
or experimental design.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_hard_blocker_attack.py
```

Acceptance gates:

- sole-axiom apparatus selection obstruction is explicit;
- amplitude field equation uniqueness obstruction is explicit;
- 3D sparse scaling obstruction is recorded by side-6 controls;
- calibrated retained-axis pulse schedule writes equal-slot records;
- material spin-bath detector model gives classical records;
- claim boundary stays state-only and not FTL.

## Retained Status

The lane is stronger, but not promoted.

The next honest target is no longer "fill in details." It is to decide which
extra principle is admissible for nature-grade review:

- a cost/action/minimality principle for apparatus windings;
- a unitary/action principle for amplitude-level record fields;
- a scalable preparation mechanism that survives side-6 and beyond;
- hardware-level pulse and detector models with leakage/noise/bandwidth bounds.
