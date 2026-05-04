# Teleportation Remaining Blocker Reduction Note

**Date:** 2026-04-26
**Status:** planning / blocker-reduction artifact
**Runner:** `scripts/frontier_teleportation_remaining_blocker_reduction.py`

## Scope

This artifact attacks the remaining native taste-qubit teleportation blockers
without promoting the lane to nature-grade closure.

It provides five bounded reductions:

- conditional uniqueness of the Bell-record transducer inside the
  stabilizer-diagonal native write class;
- a unique 3D+1 causal support/eikonal front inside the positive
  nearest-neighbor support class;
- sparse 3D side-4 Poisson resource evidence, beyond the dense side-2 probe;
- retained-axis readout/correction as an environment-blind apparatus class;
- an independent-fragment thermodynamic detector theorem.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Conditional Transducer Uniqueness

The native Bell stabilizers on Alice's two retained taste qubits are:

```text
S_z = Z_A Z_R
S_x = X_A X_R
```

The two-qubit Pauli algebra has 16 Pauli strings. The commutant of `S_z` and
`S_x` has dimension 4:

```text
span{I, S_z, S_x, S_x S_z}.
```

The four Bell branches give a full-rank Walsh table on this commutant. Once the
desired write bits are fixed,

```text
z = 1 iff S_x = -1
x = 1 iff S_z = -1
p = z xor x = 1 iff S_x S_z = -1,
```

the branch values determine the three projector controls uniquely:

```text
P_z^- = (I - S_x)/2
P_x^- = (I - S_z)/2
P_p^- = (I - S_x S_z)/2.
```

This closes uniqueness only inside the stabilizer-diagonal native write class.
It is not a proof that the sole `Cl(3)/Z^3` axiom uniquely forces a measurement
apparatus with no extra Bell-record desiderata.

## 3D+1 Support Carrier

The record carrier is treated as a causal support field, not yet as an
amplitude-normalized wave equation. In the positive nearest-neighbor support
class, the assumptions are:

- source support persists to the next tick;
- propagation is nontrivial;
- cubic isotropy treats all six axial directions identically;
- no support appears outside the one-tick nearest-neighbor cone.

Those assumptions leave exactly one support stencil:

```text
self + six axial nearest neighbors.
```

The first-arrival recurrence is then:

```text
T(r) = 0 at source
T(r) = 1 + min_{r' nearest r} T(r') otherwise.
```

The runner checks this on three 3D boxes and verifies zero arrival error, zero
eikonal residual, and zero outside-cone support.

This is a support/eikonal theorem. A unique amplitude law, normalization, and
retained relativistic field equation remain outside this artifact.

## Sparse 3D Side-4 Resource

The previous exact 3D resource probe was dense `side=2`, with `N=8` sites and
two-species Hilbert dimension `64`. This runner adds a sparse 3D `side=4` probe
with:

```text
N = 64 sites
H_dim = 4096
```

The runner builds:

```text
H = H1 tensor I + I tensor H1 + G V(i,j)
```

as a sparse matrix and solves the two lowest eigenpairs with `eigsh`. The
default rows are:

```text
G=0:    Bell*=0.500000, Fbest=0.666667, CHSH=2.000000, neg=0
G=1000: Bell*=0.716094, Fbest=0.810729, CHSH=2.178794, neg=0.216094
G=2000: Bell*=0.844599, Fbest=0.896399, CHSH=2.428986, neg=0.344599
G=5000: Bell*=0.959247, Fbest=0.972831, CHSH=2.715608, neg=0.459247
```

This moves the resource evidence beyond dense 3D side-2. It is still not an
asymptotic scaling theorem, a preparation proof, or a robustness theorem across
boundary conditions and couplings.

## Retained Readout/Correction Class

The retained readout/correction apparatus class uses:

```text
Z_r = I_cell tensor Z_retained tensor I_spectator
X_r = I_cell tensor X_retained tensor I_spectator.
```

The runner audits `3D side=2` and `3D side=4`, all three retained axes. It
checks:

- retained `Z_r` and `X_r` factor exactly as `O_logical tensor I_env`;
- retained `Z` and `X` projectors factor exactly;
- all four corrections `Z_r^z X_r^x` factor exactly;
- raw `xi_5` is rejected as a traced retained-axis `Z` in 3D.

Observed metrics:

```text
surfaces=6
retained_residual=0.000e+00
projector_residual=0.000e+00
correction_residual=0.000e+00
raw_xi5_min_rejection=2.000e+00
```

This supplies an algebraic retained-axis readout/correction class. It is not a
hardware pulse schedule or calibration model.

## Independent-Fragment Detector Theorem

The detector theorem abstracts away from the finite spin bath. If every
independent detector fragment has branch-overlap bound `q < 1`, then any two
Bell record branches separated by Hamming distance `d` have record overlap at
most:

```text
q^(d N)
```

where `N` is the number of independent fragments per code component. Since the
current record code has `d_min=5`, the default `q=0.700`, `N=24` gives:

```text
max_record_overlap = 2.581e-19
entropy_defect = 0.000e+00 bits
```

This is a detector-class theorem for independent fragment baths. It is not a
material detector construction from microscopic hardware couplings.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_remaining_blocker_reduction.py
```

Observed output:

```text
conditional transducer uniqueness: commutant_dim=4, noncommuting_paulis=12, branch_rank=4, write_nullity=0, projector_error=0.000e+00
3D+1 causal support carrier: support_stencils=1, shapes=3, points=260, arrival_error=0, eikonal_residual=0, outside_cone=0
sparse 3D side-4 resource rows:
  G=0, N=64, Hdim=4096, E0=-12, gap=2, Bell*=0.500000 (Phi+), Fbest=0.666667, CHSH=2.000000, neg=0.000000, purity=1.000000
  G=1000, N=64, Hdim=4096, E0=-25.005254, gap=0.881606, Bell*=0.716094 (Phi+), Fbest=0.810729, CHSH=2.178794, neg=0.216094, purity=0.865426
  G=2000, N=64, Hdim=4096, E0=-42.1038699, gap=0.599112, Bell*=0.844599 (Phi+), Fbest=0.896399, CHSH=2.428986, neg=0.344599, purity=0.888581
  G=5000, N=64, Hdim=4096, E0=-97.4741973, gap=0.290255, Bell*=0.959247 (Phi+), Fbest=0.972831, CHSH=2.715608, neg=0.459247, purity=0.962220
retained-axis readout/correction apparatus: surfaces=6, retained_residual=0.000e+00, projector_residual=0.000e+00, correction_residual=0.000e+00, raw_xi5_min_rejection=2.000e+00
independent-fragment detector theorem: d_min=5, q=0.700, fragments/component=24, max_record_overlap=2.581e-19, entropy_defect=0.000e+00, fragment_gram_min_eig=3.000e-01
```

Acceptance gates:

- transducer unique inside stabilizer-diagonal native write class;
- 3D+1 causal support carrier has unique eikonal front;
- sparse 3D side-4 Poisson resource has a high-fidelity window;
- retained-axis readout/correction apparatus factors through `I_env`;
- independent-fragment detector theorem drives records classical;
- claim boundary stays state-only and not FTL.

## Remaining Nature-Grade Gaps

The blocker list is now sharper:

- sole-axiom selection of the measurement apparatus is still not proved;
- the 3D+1 support front is unique, but the amplitude-level field equation is
  not uniquely derived;
- the side-4 sparse resource is positive, but asymptotic scaling and physical
  preparation remain open;
- retained readout/correction has an algebraic apparatus class, but no hardware
  pulse schedule;
- detector irreversibility has an independent-fragment theorem, but no material
  hardware construction.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [teleportation_native_record_apparatus_note](TELEPORTATION_NATIVE_RECORD_APPARATUS_NOTE.md)
- [teleportation_taste_readout_operator_model_note](TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md)
