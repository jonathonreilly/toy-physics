# Teleportation Apparatus Dynamics Closure Candidate Note

**Date:** 2026-04-26
**Status:** planning / coupled field-bath-apparatus dynamics candidate
**Runner:** `scripts/frontier_teleportation_apparatus_dynamics_closure.py`

## Scope

This artifact goes after the remaining record/apparatus blockers with a
single coupled dynamics candidate:

- derive the eikonal carrier from a local retarded field front;
- replace the ideal/projective Bell measurement by a finite-strength unitary
  transducer controlled by Bell stabilizers;
- replace the thermal proxy by an explicit finite spin bath that decoheres the
  pointer when traced;
- check conservation on the full apparatus candidate, not only Bob's fiber
  correction.

This remains a planning artifact. It does not prove a unique retained
relativistic field equation, a continuum thermodynamic detector, or a
microscopic `Cl(3)/Z^3` apparatus Hamiltonian.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Dynamical Components

### Retarded Field Front

The carrier field is no longer introduced as a static eikonal path. A local
first-order retarded support field is emitted from Bob's site:

```text
F_{t+1}(r) = F_t(r) OR any_neighbor F_t(neighbor).
```

The first-arrival time of this field is then measured across the lattice. On
the default 3D lattice it exactly reproduces the eikonal distance:

```text
first_arrival(r) = |r - b|_1.
```

Thus the eikonal carrier used by the prior pass is now derived as the
first-arrival surface of a local nearest-neighbor field equation.

### Finite-Strength Bell Transducer

The Bell apparatus is modeled as a unitary controlled by the four commuting
Bell-stabilizer projectors:

```text
U = sum_j P_j tensor U_j.
```

Each `U_j` writes a finite-strength pointer domain for the Bell codeword. The
pointer states are not asserted as projective records. They have finite
overlap determined by the coupling angle and domain size. In the default run:

```text
theta = 0.620
domain size = 9
max pointer branch overlap = 1.053e-22
```

The transducer is therefore an explicit finite-strength premeasurement model:
near-orthogonal enough to decode, but represented as controlled unitary
dynamics rather than collapse.

### Finite Spin Bath

The pointer domain is coupled to a finite spin bath. For differing Bell
records, bath branches have overlap controlled by a separate coupling `phi`
and the number of bath spins per pointer-domain spin.

Default run:

```text
phi = 0.350
bath spins per domain spin = 4
max bath branch overlap = 1.104e-21
max combined pointer-bath overlap = 1.163e-43
record entropy = 2.000000000 bits
```

Tracing the bath therefore produces an effectively classical durable record
without inserting a projective collapse step.

### Apparatus Conservation

The candidate apparatus ledger includes:

- base mass, charge, and support ledgers;
- pointer domain energy;
- bath spin excitation energy;
- fixed-count carrier pulse energy.

The default branch-energy spread across all four Bell records is zero to
roundoff, and Bob's correction commutes with the base ledgers. The record
energy cost is branch independent, so the apparatus does not leak the unknown
input or move conserved support from Alice to Bob.

## First Run

Commands:

```bash
python3 -m py_compile scripts/frontier_teleportation_apparatus_dynamics_closure.py
python3 scripts/frontier_teleportation_apparatus_dynamics_closure.py
```

Observed output:

```text
retarded field front: distance=7, max_arrival_error=0, eikonal_residual=0, outside_cone_violations=0
finite-strength transducer: theta=0.620, domain=9, max_pointer_overlap=1.053e-22, controlled_unitary_error=0.000e+00
finite spin bath: phi=0.350, bath_spins/domain_spin=4, max_bath_overlap=1.104e-21, max_combined_overlap=1.163e-43, record_entropy_bits=2.000000000
Bob before field record delivery: trace_distance_to_I/2=3.053e-16, pairwise_input_distance=2.220e-16
generated Bell labels: Phi+, Phi-, Psi+, Psi-
minimum corrected fidelity after delivered record: 0.9999999999999998
maximum corrected infidelity: 2.220e-16
max corrected-state trace distance to input: 1.943e-16
apparatus conservation: energy_spread=0.000e+00, branch_energy=66.170059..66.170059, ledger_commutator=0.000e+00, pulse_count=8..8
```

Acceptance gates:

- retarded field front derives eikonal carrier;
- Bell transducer is finite-strength unitary, not projection;
- finite pointer domains distinguish all Bell records;
- finite spin bath decoheres records irreversibly when traced;
- Bob pre-delivery state is input-independent;
- delivered record restores Bob state;
- apparatus energy and ledgers are branch independent;
- claim boundary stays state-only and not FTL.

## What This Narrows

This pass materially narrows four blockers:

1. The eikonal carrier is no longer merely postulated; it is the
   first-arrival surface of a local retarded field equation.
2. The Bell measurement is no longer modeled as a bare projector; it is an
   explicit controlled-unitary premeasurement with finite pointer overlap.
3. The bath is no longer only an Arrhenius/stability proxy; it is a finite
   spin bath whose traced overlap suppresses record coherences.
4. Conservation is checked across the full candidate apparatus ledger, not
   just Bob's retained-fiber correction.

## Remaining Nature-Grade Blockers

This still does not close nature-grade review.

- The retarded field equation is a local nearest-neighbor carrier candidate,
  not a unique retained relativistic field equation.
- The spin bath is finite and explicit, but not a continuum thermodynamic
  detector or entropy-production theorem.
- The stabilizer-controlled unitary is engineered at the Bell-stabilizer
  level; a microscopic `Cl(3)/Z^3` interaction Hamiltonian is still open.
- Conservation is proved for this candidate ledger split, not for all possible
  native apparatus implementations.
- The Bell resource and retained readout/correction still rely on previous
  bounded lane components.

## Retained-Theory Impact

The retained teleportation theory now has a plausible dynamical record stack:

```text
local retarded field front
  -> eikonal carrier surface
  -> finite-strength Bell-stabilizer transducer
  -> finite pointer domains
  -> finite spin-bath decoherence
  -> apparatus-ledger-conserving correction
```

This is still planning-level, but it is a nontrivial native apparatus
candidate rather than a supplied classical bit channel or a projective
measurement placeholder.
