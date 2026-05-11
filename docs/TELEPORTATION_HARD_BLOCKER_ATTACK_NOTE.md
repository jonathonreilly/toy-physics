# Teleportation Hard Blocker Attack Note

---

**This is a planning / blocker-inventory note. It does not establish
any retained claim.** The "Apparatus Selection Obstruction" and
"Amplitude Field Obstruction" sections are obstruction findings under
the audited candidate classes, the "Sparse 3D Scaling Control" section
is a finite numerical control, and the "Calibrated Pulse Schedule" /
"Material Spin-Bath Detector Model" sections are bounded ideal models.
None of these are audited here as separate retained claims.

---

**Date:** 2026-04-26
**Status:** support / planning record / blocker-inventory only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / planning record / blocker-inventory only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit outcome.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Runner:** `scripts/frontier_teleportation_hard_blocker_attack.py`

## Review scope (relabel 2026-05-10)

This file is a **planning blocker-inventory note** for the native
taste-qubit teleportation lane, mixing two obstruction findings, one
sparse-scaling finite control, and two bounded ideal apparatus
proxies. It is **not** a single retained theorem, no-go, or
bounded-finite-result row and **must not** be audited as one. The
generated-audit context identified this repair target:

> other: split into separate ledger rows for the apparatus no-go,
> amplitude no-go, sparse side-6 scaling control, ideal pulse
> schedule, and spin-bath detector model, each with its own scoped
> claim_type.

The minimal-scope response in this PR is to **relabel** this document
as a planning blocker-inventory record. Splitting into per-claim
ledger rows for the apparatus no-go, the amplitude no-go, the sparse
side-6 control, the ideal pulse schedule, and the spin-bath detector
model remains the alternative path the auditor offered; that work
belongs in dedicated review-loop passes. Until that split is done:

- This file makes **no** retained-claim assertions of its own.
- The five sections below are **planning-level inventory**, citeable
  only as a blocker inventory for ordinary state teleportation, with
  no matter, energy, object, or FTL transport claim.
- The retained-status surface for any teleportation-lane sub-claim is
  the audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus dedicated
  per-claim notes, **not** this attack inventory.

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
