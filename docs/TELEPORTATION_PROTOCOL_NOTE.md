# Native Taste-Qubit Teleportation Protocol Note

**Date:** 2026-04-25
**Status:** planning / first artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_protocol.py`

## Scope

This note records the first concrete artifact for the native taste-qubit
teleportation lane opened in
[`FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md`](FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md).

The result is ordinary quantum state teleportation on an encoded taste-qubit
register. It is not matter teleportation, mass transfer, charge transfer,
object transport, or faster-than-light transport.

## Native Register

The protocol stays on the same Hilbert/taste surface used by the retained CHSH
lane:

- a single staggered species has `C^N = C^N_cells tensor C^(2^d)` under the
  Kogut-Susskind cell/taste decomposition;
- the site-basis sublattice operator is `Z = I_cells tensor xi_5`;
- the site-basis pair-hop operator is `X = I_cells tensor xi_last`;
- on a fixed cell with spectator taste bits fixed, the last taste bit gives
  one encoded logical taste qubit.

The first runner uses the 3D side-4 lattice and the fixed cell `(0,0,0)`.
The encoded basis is:

```text
|0_L> = site index 0
|1_L> = site index 1
```

On this subspace the restricted native taste operators act as Pauli `Z` and
`X`, with zero anticommutator to numerical precision.

## Protocol

Registers are ordered as:

```text
A = Alice unknown encoded taste qubit
R = Alice half of a Bell resource
B = Bob half of a Bell resource
```

The input is an arbitrary encoded taste-qubit state:

```text
|psi>_A = alpha |0_L> + beta |1_L>
```

The resource is the ideal encoded Bell pair:

```text
|Phi+>_RB = (|0_L 0_L> + |1_L 1_L>) / sqrt(2)
```

Alice measures `A,R` in the four Bell projectors built from native taste-Pauli
stabilizers:

```text
P_zx = 1/4 (I + (-1)^x Z_A Z_R) (I + (-1)^z X_A X_R)
```

The two classical bits are:

```text
z = Bell phase bit
x = Bell flip bit
```

Bob receives the explicit classical record and applies the Pauli correction:

```text
U_zx = Z^z X^x
```

The order is immaterial up to a global phase for the `z=x=1` branch.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_protocol.py --trials 64 --seed 20260425
```

Observed output:

```text
Bell outcomes exercised: Phi+, Phi-, Psi+, Psi-
minimum corrected-state fidelity: 0.9999999999999993
maximum infidelity: 6.661e-16
max Bell probability error from 1/4: 2.220e-16
max Bob trace distance to I/2 before Alice measurement: 3.331e-16
max Bob trace distance to I/2 after Alice measurement but before message: 4.163e-16
max pairwise pre-message Bob-state distance across inputs: 3.886e-16
```

The script reports `PASS` for:

- native taste encoding;
- Bell projectors;
- random-state fidelity;
- all four Bell outcomes;
- Bob pre-message input-independence;
- explicit causal two-bit record channel.

## Second-Pass Limitation Artifacts

The first follow-up pass adds four bounded artifacts, one for each recorded
limitation.

- `scripts/frontier_teleportation_resource_fidelity.py` bounds non-ideal
  two-qubit resources. For the fixed Bell-basis protocol, it verifies
  `F_avg = (1 + 2 <Phi+|rho|Phi+>) / 3`, so the useful fixed-protocol
  threshold is `<Phi+|rho|Phi+> > 1/2`. The isotropic threshold is `v > 1/3`,
  while the isotropic CHSH threshold is higher at `v > 1/sqrt(2)`.
- `scripts/frontier_teleportation_resource_from_poisson.py` audits whether
  the existing Poisson/CHSH ground-state machinery can supply an encoded
  resource after tracing cells and spectator tastes. The `G=0` null case does
  not supply a Bell resource. The audited positive cases give traced Bell
  overlaps `0.997963` on `1D N=8, G=1000` and `0.970283` on `2D 4x4, G=1000`,
  with mean standard-teleportation fidelities `0.998621` and `0.979360`.
- `scripts/frontier_teleportation_measurement_record.py` adds an explicit
  orthogonal four-state Bell-record register for Alice's measurement. It
  verifies Bob's pre-record input-independence and post-record correction.
- `scripts/frontier_teleportation_causal_channel.py` replaces the minimal
  latency toy channel with a directed-lattice/DAG record harness, including
  no-early-delivery, duplicate-prevention, wrong-record, delayed-record, and
  pre-delivery no-signaling checks.

The corresponding notes are:

- `docs/TELEPORTATION_RESOURCE_FIDELITY_NOTE.md`
- `docs/TELEPORTATION_RESOURCE_FROM_POISSON_NOTE.md`
- `docs/TELEPORTATION_MEASUREMENT_RECORD_NOTE.md`
- `docs/TELEPORTATION_CAUSAL_CHANNEL_NOTE.md`

## Third-Pass Hardening Artifacts

The second follow-up pass adds four more bounded hardening artifacts.

- `scripts/frontier_teleportation_poisson_resource_sweep.py` sweeps the
  Poisson-derived resource over small `1D N=8` and `2D 4x4` surfaces, masses
  `0, 0.1, 0.5, 1`, and couplings `G=0, 1, 10, 50, 100, 500, 1000`. The
  `G=0` null controls remain clean. High-resource rows appear on `5/48`
  non-null points, so the Poisson result is a parameter-window result, not a
  uniform claim.
- `scripts/frontier_teleportation_encoding_portability.py` audits cells,
  spectator taste choices, logical axes, dimensions `1..3`, and side lengths
  `2,4,6,8`. The current fixed pair-hop `X` works for the last taste axis
  (`470/1330` surveyed encodings), while an axis-adapted taste `X` passes all
  `1330/1330` surveyed encodings.
- `scripts/frontier_teleportation_preparation_readout_probe.py` separates the
  offline Poisson ground-state extraction from an operational
  preparation/readout protocol. The positive default Poisson cases remain
  positive as offline traced resources, but dynamic cooling, adiabatic
  preparation, environment readout, and heralding are not demonstrated.
- `scripts/frontier_teleportation_noise_fault_controls.py` adds supplied
  depolarized resources, Bell-record bit flips, classical record
  flips/drops/delays, and Bob correction-control errors. It reports fidelity
  thresholds while keeping Bob's pre-record density matrix input-independent.

The corresponding notes are:

- `docs/TELEPORTATION_POISSON_RESOURCE_SWEEP_NOTE.md`
- `docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md`
- `docs/TELEPORTATION_PREPARATION_READOUT_PROBE_NOTE.md`
- `docs/TELEPORTATION_NOISE_FAULT_CONTROLS_NOTE.md`

## End-To-End Poisson Integration Artifact

The next integration step is
`scripts/frontier_teleportation_end_to_end_poisson.py`, documented in
`docs/TELEPORTATION_END_TO_END_POISSON_NOTE.md`.

This runner combines the pieces into one protocol-level audit:

```text
Poisson ground-state extraction
  -> traced logical taste resource
  -> Bell measurement
  -> causal two-bit record
  -> Bob correction
```

The default run keeps the `G=0` null case and the two positive Poisson cases:

| case | best Bell overlap | exact F_avg | sampled min fidelity | Bob pre-record pairwise distance | pass |
| --- | ---: | ---: | ---: | ---: | --- |
| `1d_null` | `0.500000` | `0.666667` | `0.500000` | `2.776e-16` | no |
| `1d_poisson_chsh` | `0.997963` | `0.998642` | `0.997963` | `2.220e-16` | yes |
| `2d_poisson_chsh` | `0.970283` | `0.980189` | `0.970283` | `2.220e-16` | yes |

The end-to-end audit therefore passes on the selected positive Poisson
resources and fails the null control as expected. It still inherits the
preparation/readout limitation: the resource is extracted offline and traced,
not prepared by a physical protocol.

## Fourth-Pass Operational Bridge Artifacts

The next batch probes the remaining bridge between an offline logical resource
and a candidate operational taste-qubit teleportation protocol.

- `scripts/frontier_teleportation_dynamical_resource_generation.py` evolves
  simple two-species product site states under the Poisson Hamiltonian and
  traces the logical taste-qubit resource over time. The `G=0` null remains
  non-useful. Interacting `1D N=8` cases open useful but low-fidelity windows:
  best Bell overlaps `0.616298` and `0.631187`, corresponding to framed mean
  teleportation fidelities `0.744199` and `0.754125`. No default trajectory
  reaches the high-fidelity `0.90` Bell-overlap threshold.
- `scripts/frontier_teleportation_adiabatic_prep_probe.py` audits the linear
  native coupling path `H(s)=H(G=0)+s(H(G_target)-H(G=0))`. Null paths stay
  clean. The `1D N=8` endpoint reaches `Phi+` overlap `0.997963` but has a
  small final sampled gap `0.018683` and a large conservative norm-bound
  diagnostic. The `2D 4x4` endpoint reaches `Phi+` overlap `0.970283` with
  sampled gap `0.246378` and is the cleaner bounded preparation candidate.
  This is still not a preparation proof.
- `scripts/frontier_teleportation_logical_readout_audit.py` separates valid
  reduced-state extraction from operational readout. The traced logical
  resources remain valid on the positive Poisson cases, and Bob's pre-message
  input-independence remains at numerical precision. Fixed-environment
  branches vary, so the lane still needs a taste-only apparatus/readout model
  or an explicit environment measurement and heralding workflow.
- `scripts/frontier_teleportation_cross_encoding_maps.py` extends the algebraic
  teleportation map from same-encoding registers to different Bob cells,
  spectator tastes, and logical axes. Axis-adapted cross maps pass all `9637`
  surveyed Alice/Bob maps over dimensions `1,2,3` and side lengths `2,4`, with
  minimum fidelity `0.9999999999999996` and Bob pre-message pairwise distance
  `5.551e-16`. The current fixed pair-hop convention passes only the expected
  last-axis subset `1113/9637`; wrong conversion and non-adapted correction
  controls fail as expected.

The corresponding notes are:

- `docs/TELEPORTATION_DYNAMICAL_RESOURCE_GENERATION_NOTE.md`
- `docs/TELEPORTATION_ADIABATIC_PREP_PROBE_NOTE.md`
- `docs/TELEPORTATION_LOGICAL_READOUT_AUDIT.md`
- `docs/TELEPORTATION_CROSS_ENCODING_MAPS_NOTE.md`

## Fifth-Pass Operational Gate Artifacts

The next batch turns several open bridge items into explicit planning gates.

- `scripts/frontier_teleportation_adiabatic_time_evolution.py` performs
  finite-time Schrodinger evolution under the native ramp
  `H(s)=H(G=0)+s(t)(H(G_target)-H(G=0))`. On the default `2D 4x4` case, the
  `G=0` null remains non-resource. The best default positive row is the
  smoothstep schedule at `T=40`, with final ground overlap `0.999985`,
  diabatic loss `1.546251e-05`, `Phi+` overlap `0.970437`, and standard
  `F_avg=0.980291`. Bob's pre-message pairwise input distance remains
  `2.220e-16`. This is a useful finite-time preparation-candidate diagnostic,
  not a preparation proof.
- `scripts/frontier_teleportation_taste_readout_operator_model.py` audits the
  operator condition `O_logical tensor I_env`. Retained-axis logical `Z`,
  retained-axis logical `X`, axis-built `Z+`, `X+`, `ZZ`, `XX`, and Bell
  projectors factor cleanly on the audited `dim=1,2,3`, `side=2,4` surfaces.
  The fixed pair-hop `X` equals retained-last-axis `X` in this lane. Raw
  native sublattice parity `Z=xi_5` is not a retained-bit-only logical `Z` in
  `dim>1`; it contains spectator taste signs and fails the traced taste-only
  criterion.
- `scripts/frontier_teleportation_bell_measurement_circuit.py` decomposes the
  ideal Bell projectors into equivalent ideal logical/taste measurements:
  direct `ZZ`/`XX` stabilizer measurements or `CNOT(A->R)`, `H(A)`, and
  computational `Z` readout. The pulled-back circuit projectors match `P_zx`
  to `1.110e-16`, all four outcomes are exercised, and the random-state
  correction fidelity remains unity to roundoff.
- `scripts/frontier_teleportation_three_register_cross_encoding.py` allows
  independent encodings for Alice's input `A`, Alice's resource half `R`, and
  Bob's resource half `B`. Axis-adapted three-register maps pass all `1609`
  bounded surveyed triples, with minimum fidelity `0.9999999999999996` and
  Bob pre-message pairwise distance `4.718e-16`. Missing `A->R` conversion,
  non-adapted Bell/correction operators, and wrong `R->B` resource conversion
  controls fail as expected.
- `scripts/frontier_teleportation_acceptance_suite.py` adds a consolidated
  lightweight harness. In the local run, required probes reported `8/8 PASS`
  and present optional hooks reported `4/4 PASS`. The suite is telemetry for
  bounded gates; a suite pass is not a proof of preparation, hardware readout,
  durable records, or physical transport.

The corresponding notes are:

- `docs/TELEPORTATION_ADIABATIC_TIME_EVOLUTION_NOTE.md`
- `docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md`
- `docs/TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md`
- `docs/TELEPORTATION_THREE_REGISTER_CROSS_ENCODING_NOTE.md`
- `docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md`

## Sixth-Pass Tightening Artifacts

The next tightening pass focuses on preventing ambiguity around the logical
`Z` convention and hardening the finite-time preparation candidate.

- `scripts/frontier_teleportation_operator_consistent_end_to_end.py` reruns
  the Poisson end-to-end audit using retained-axis logical `Z/X` operators for
  traced readout, Bell measurement, and Bob correction. The positive
  `1d_poisson_chsh` and `2d_poisson_chsh` cases still pass with exact
  `F_avg=0.998642` and `0.980189`, sampled minimum fidelities `0.997963` and
  `0.970283`, and Bob pre-record pairwise distances `2.220e-16`. Raw `xi_5`
  is accepted as retained `Z` only in 1D; in `2D side=4` and `3D side=2`, raw
  `xi_5` fails the traced operator guard with relative residual `1.000000`.
- `scripts/frontier_teleportation_adiabatic_convergence_robustness.py`
  tightens the `2D 4x4`, smoothstep, `T=40` finite-time result. The `320` and
  `640` step rows agree to `7.478e-07` in `F_avg`, `expm_multiply` and dense
  `eigh` propagation agree to roundoff at `160` steps, and modest runtime,
  `G`, and mass perturbations keep `F_avg >= 0.979339`. A deterministic
  schedule-noise row keeps high reduced fidelity but has diabatic loss
  `0.045212`, warning that reduced logical fidelity alone is not a ground-state
  preparation proof.
- `scripts/frontier_teleportation_initial_state_preparation_probe.py` audits
  the `G=0` initial state assumed by the finite-time ramp. On `1D N=8` and
  `2D 4x4`, the two-species `G=0` ground state is unique, gapped, separable,
  and exactly the tensor product of two single-species `H1` ground states.
  It is also fully delocalized in the native site-pair basis
  (`PR/dim=1.000000`), so the operational preparation gap is narrowed but not
  closed.
- `scripts/frontier_teleportation_acceptance_suite.py --strict-lane` adds a
  blocking current-lane telemetry profile. In the local run it reported
  `12/12 PASS`, including the full finite-time 2D smoothstep hook,
  taste-readout operator model, Bell-measurement circuit, and three-register
  cross-encoding checks.
- `docs/TELEPORTATION_Z_CONVENTION_CLARIFICATION.md` records the safe wording:
  raw `xi_5` can restrict to a signed logical `Z` on a fixed cell/spectator
  branch, while traced operational retained-bit readout/correction in
  `dim>1` must use retained-axis `Z_r tensor I_env` unless an explicit
  environment measurement, heralding rule, and branch-conditioned correction
  workflow is supplied.

The corresponding notes are:

- `docs/TELEPORTATION_OPERATOR_CONSISTENT_END_TO_END_NOTE.md`
- `docs/TELEPORTATION_ADIABATIC_CONVERGENCE_ROBUSTNESS_NOTE.md`
- `docs/TELEPORTATION_INITIAL_STATE_PREPARATION_PROBE_NOTE.md`
- `docs/TELEPORTATION_Z_CONVENTION_CLARIFICATION.md`

## Seventh-Pass 3D+1 Artifacts

The next pass reorients the lane toward the framework target: three spatial
directions plus one explicit causal/time direction.

- `scripts/frontier_teleportation_3d_resource_probe.py` audits the smallest
  exact 3D spatial resource surface, `3D side=2` (`N=8`, dense two-species
  dimension `64`). The `G=0` null remains non-resource. The non-null
  `G=500` and `G=1000` rows produce high Bell-frame resources with best Bell
  overlaps `0.991220` and `0.997724`, both in the `Psi+` frame. Fixed `Phi+`
  fidelity is low, so the Bell frame must be tracked explicitly.
- `scripts/frontier_teleportation_3d_operator_consistent_end_to_end.py`
  performs the retained-axis end-to-end audit on the same 3D side-2 resource.
  The fixed `Phi+` row for `G=1000` fails honestly (`F_avg=0.334850`) because
  the resource lands in `Psi+`. The known retained-axis `Psi+ -> Phi+`
  frame row passes with `F_avg=0.998483`, sampled minimum fidelity `0.997724`,
  and Bob pre-record pairwise distance `2.498e-16`.
- `scripts/frontier_teleportation_3d1_causal_record_channel.py` replaces the
  generic record-channel harness with a 3D spatial lattice plus one discrete
  time direction. In the default Manhattan-speed-one run, Alice at
  `(1,1,1), t=4` and Bob at `(5,3,2)` have distance `7`, so the earliest
  delivery tick is `11`. Outside-cone, early, duplicate, wrong-site,
  wrong-record, dropped, and delayed controls behave as expected while Bob's
  pre-delivery state remains input-independent.
- `scripts/frontier_teleportation_3d_initial_ramp_probe.py` pressures the
  preparation lane on `3D side=2`. The `G=0` state is unique, gapped, separable,
  and delocalized (`PR/dim=1.000000`). The finite-time smoothstep ramp at
  `T=40`, `320` steps tracks the `G=1000` target with overlap `0.999954` and
  yields best Bell overlap `0.997444` in the `Psi+` frame. This is a 3D
  side-2 resource candidate, not a scaling or preparation proof.
- `scripts/frontier_teleportation_3d_readout_convention_audit.py` makes the
  3D readout rule explicit for all retained axes on side `2` and side `4`.
  Retained-axis `Z_r/X_r` and retained-axis Bell projectors factor exactly.
  Raw `xi_5=Z_x Z_y Z_z` is a signed fixed-branch Pauli but fails traced
  retained-bit `Z` for all axes, with relative residual `1.000000`; raw-`xi_5`
  Bell projectors fail with max relative residual `0.707107`.

The corresponding notes are:

- `docs/TELEPORTATION_3D_RESOURCE_PROBE_NOTE.md`
- `docs/TELEPORTATION_3D_OPERATOR_CONSISTENT_END_TO_END_NOTE.md`
- `docs/TELEPORTATION_3D1_CAUSAL_RECORD_CHANNEL_NOTE.md`
- `docs/TELEPORTATION_3D_INITIAL_RAMP_PROBE_NOTE.md`
- `docs/TELEPORTATION_3D_READOUT_CONVENTION_NOTE.md`

## Eighth-Pass Candidate Theory Artifact

The next pass turns the 3D+1 diagnostics into an explicit candidate axiom
bundle for the lane, without promoting the lane.

- `docs/TELEPORTATION_NATIVE_AXIOMS_THEORY_NOTE.md` defines the native
  teleportation event as a framed, causally indexed channel rather than a bare
  state vector. The proposed lane-level axioms are retained-factor
  observability, Bell-frame connection, 3D+1 causal record separability,
  native resource genesis, and exhaustive branch accounting, with a standing
  no-transfer boundary.
- `scripts/frontier_teleportation_axiom_closure_checks.py` is a deterministic
  consistency harness for those principles. It checks that 3D raw `xi_5` is
  rejected as traced retained-bit `Z`, that the `Psi+` Bell frame composes with
  Bob correction as a discrete `Z2 x Z2` frame, that the default 3D+1 record
  delivery tick equals the Manhattan light-cone rule, and that nature-grade
  closure remains on hold.

This artifact adds theory obligations rather than empirical closure. It says a
future nature-grade version must derive or physically model resource genesis,
durable Bell measurement, record creation/transport, apparatus-level retained
readout, noise/leakage controls, and conservation ledgers.

## Ninth-Pass Native Transport Theory Artifact

The next theory pass gives the lane a more structural candidate mechanism
while preserving the planning boundary.

- `docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md` interprets native
  teleportation as trivialization of a discrete Pauli-frame connection on a
  retained taste-qubit fiber over a 3D+1 base. Bell resources become
  connection edges, Bell outcomes become local holonomy data, Bob's correction
  becomes connection trivialization, and the two-bit record must be a causal
  3D+1 section before it can enable reconstruction.
- `scripts/frontier_teleportation_transport_invariants.py` checks formal
  consequences of that theory: `Z2 x Z2` Bell-frame group closure, multi-hop
  xor holonomy, missing-record Pauli twirl, 3D+1 causal-section timing,
  commutation of fiber corrections with base ledgers, loop-holonomy defect
  detection, and hidden-branch dephasing.

This is a creative theory layer, not physical closure. It raises the
nature-grade obligations: derive the base/fiber split for an apparatus, derive
connection frames from native Poisson dynamics, derive durable record sections,
prove ledger commutation for conserved quantities, and audit loop holonomy and
hidden branches in any extended protocol.

## Tenth-Pass Native Record Apparatus Artifact

The next pass attacks the largest remaining record gap: the Bell record is
generated by a bounded native apparatus model and then carried by a 3D+1 local
record field, instead of being supplied directly to a classical channel.

- `scripts/frontier_teleportation_native_record_apparatus.py` couples Alice's
  Bell stabilizer measurement to a local `BellPointerRecord`, encodes the
  pointer as an eight-component redundant codeword
  `z z z | x x x | (z xor x) (z xor x)`, emits each codeword component as a
  local 3D+1 record-field pulse, decodes the delivered codeword at Bob, and
  applies the retained Pauli correction.
- `docs/TELEPORTATION_NATIVE_RECORD_APPARATUS_NOTE.md` records the gates and
  limitations. The default run generates all four Bell labels, corrects every
  one- and two-component record-code bit flip, propagates the carrier locally
  from `(1,1,1), t=4` to `(5,3,2), t=11`, keeps Bob's pre-delivery state
  input-independent, and restores Bob's state after decoded delivery.

This is the first end-to-end apparatus/carrier candidate in the lane. It is
still not a nature-grade detector derivation: the Bell-stabilizer transducer is
ideal/projective, the record code is a classical durability model, and the
record-field pulses are local but not derived from retained field equations.

## Eleventh-Pass Record-Field Closure Probe

The next pass goes after three remaining record-sector blockers: field-derived
carrier propagation, pointer durability thresholds, and conservation-ledger
accounting.

- `scripts/frontier_teleportation_record_field_closure.py` replaces the
  prescribed record pulse path with a local 3D eikonal routing field
  `D(r)=|r-b|_1`, verifies the local equation
  `D(r)=1+min_neighbor D(neighbor)`, routes every record pulse by local
  descent, and keeps the default delivery from `(1,1,1), t=4` to
  `(5,3,2), t=11`.
- The same runner adds adversarial pointer checks: the eight-component record
  code corrects all one- and two-component flips and all up-to-four erasures,
  with zero silent wrong decodes under that budget.
- It adds a thermal stability proxy for a size-9 ferromagnetic pointer domain
  at spin-flip probability `0.10`, giving component failure
  `8.909e-04`, word failure `3.947e-08`, and Arrhenius proxy `9.358e-14`.
- It adds conservation-ledger gates: Bob corrections commute with mass,
  charge, and support ledgers on the base, while record pulse/domain energy is
  independent of the carried bit polarity.

This narrows the field, durability, and ledger gaps. It still does not supply
a retained relativistic field equation, detector bath/entropy derivation, or
physical apparatus conservation theorem.

## Twelfth-Pass Apparatus Dynamics Closure Candidate

The next pass couples the remaining record/apparatus mechanisms into a single
dynamics candidate.

- `scripts/frontier_teleportation_apparatus_dynamics_closure.py` derives the
  eikonal carrier from a local retarded nearest-neighbor field front: the
  first-arrival time satisfies the eikonal distance exactly on the default
  3D lattice, with zero outside-cone support.
- The same runner replaces a bare projective Bell measurement with a
  finite-strength controlled-unitary transducer
  `U=sum_j P_j tensor U_j`. With default pointer angle `theta=0.620` and
  domain size `9`, the maximum Bell-record pointer overlap is `1.053e-22`.
- It replaces the thermal proxy with an explicit finite spin bath. With
  `phi=0.350` and four bath spins per pointer-domain spin, the maximum bath
  branch overlap is `1.104e-21`, the combined pointer-bath overlap is
  `1.163e-43`, and the record entropy is `2.000000000` bits.
- It checks apparatus-level conservation: branch energy spread is zero to
  roundoff, pulse count is branch independent, and Bob correction commutes
  with mass, charge, and support ledgers.

This is a nontrivial native apparatus candidate. It still does not derive a
unique retained relativistic field equation, a continuum thermodynamic
detector theorem, or a microscopic `Cl(3)/Z^3` interaction Hamiltonian for the
stabilizer transducer.

## Thirteenth-Pass Microscopic Closure Candidate

The next pass turns the remaining microscopic gaps into explicit candidate
theorems and Hamiltonian checks.

- `scripts/frontier_teleportation_microscopic_closure.py` constructs the
  Bell-record transducer Hamiltonian from native retained-axis stabilizers:
  `S_z=Z_A Z_R`, `S_x=X_A X_R`, and
  `H_int=(pi/2T)[P_z^- sum X_z + P_x^- sum X_x + P_p^- sum X_p]`, where
  `P_z^-=(I-S_x)/2`, `P_x^-=(I-S_z)/2`, and
  `P_p^-=(I-S_x S_z)/2`.
- On `3D side=2`, the retained-axis site/taste `Z_r` and `X_r` factor with
  zero residual, the native Bell stabilizers commute, the Hamiltonian terms
  commute, and finite-time Hamiltonian evolution writes the exact
  `z z z | x x x | (z xor x) (z xor x)` codeword for all four Bell records.
- The same runner upgrades the spin bath to a thermodynamic detector bound:
  `epsilon_N <= exp(-kappa N)`, with `d_min=5`, `kappa=10.984501`,
  `epsilon_9=1.163e-43`, and entropy defect at `N=21` equal to numerical zero.
- It also states and checks the native ledger theorem class
  `[L_support tensor I_taste tensor I_app,
  I_support tensor G_taste tensor A_app]=0`, including basis-level matrix
  audit, random Hermitian controls, and explicit stabilizer-controlled
  transducer terms.

This moves the remaining blockers from mechanism-level gaps to
derivation/uniqueness gaps. It still does not prove that this apparatus
Hamiltonian is uniquely forced by the sole framework axiom or that a hardware
implementation exists.

## Fourteenth-Pass Remaining Blocker Reduction

The next pass attacks the sharpened blockers directly with a bounded theorem and
sparse-resource runner:

- `scripts/frontier_teleportation_remaining_blocker_reduction.py` proves that,
  inside the stabilizer-diagonal native write class, the Bell-record transducer
  controls are unique. The two-qubit Pauli commutant of `Z_A Z_R` and `X_A X_R`
  has dimension `4`, the Bell-branch write table has rank `4`, and the write
  nullity is `0`.
- The same runner proves a unique causal support/eikonal front inside the
  positive nearest-neighbor 3D+1 support class: one admissible isotropic support
  stencil, zero arrival error, zero eikonal residual, and zero outside-cone
  support on the audited 3D boxes.
- It moves resource evidence beyond dense `3D side=2` by adding a sparse
  `3D side=4` Poisson ground-state probe with `N=64` and Hilbert dimension
  `4096`. The default positive window is `G=5000`, with `Bell*=0.959247`,
  best-frame `F_avg=0.972831`, `CHSH=2.715608`, and negativity `0.459247`.
- It supplies an algebraic retained-axis readout/correction apparatus class on
  `3D side=2` and `side=4`, all retained axes: retained projector and correction
  residuals are zero, while raw `xi_5` is rejected as a traced retained-axis
  readout with minimum residual `2.000e+00`.
- It upgrades the bath statement to an independent-fragment detector theorem:
  for fragment-overlap bound `q=0.700`, `24` fragments per code component, and
  record-code `d_min=5`, the maximum record overlap is `2.581e-19` and the
  two-bit entropy defect is numerical zero.

This reduces the remaining blocker list but does not close nature-grade review.
The transducer uniqueness is conditional on Bell-record desiderata, the carrier
is a support-front theorem rather than an amplitude-level field equation, the
side-4 resource is not an asymptotic scaling theorem or preparation proof,
readout/correction still lacks a calibrated pulse schedule, and the detector
theorem is not a material hardware construction.

## Fifteenth-Pass Hard Blocker Attack

The next pass attacks the five remaining blockers directly and separates
positive mechanisms from obstructions.

- `scripts/frontier_teleportation_hard_blocker_attack.py` exhibits two
  inequivalent native stabilizer-controlled transducer Hamiltonians that write
  the same Bell record. The active flip angles `pi/2` and `3pi/2` give the same
  record map with zero pointer error but different spectral norms. This is an
  obstruction to unqualified sole-axiom apparatus uniqueness unless an extra
  cost/action/minimality principle or equivalence quotient is supplied.
- It exhibits two distinct normalized nearest-neighbor amplitude kernels with
  the same 3D causal/eikonal support front but different amplitudes. This is an
  obstruction to amplitude-level field-equation uniqueness from support
  constraints alone.
- It adds sparse `3D side=6` resource controls. The side-4 high-fidelity row
  remains positive at `G=5000` (`Bell*=0.959247`), but side-6 rows at
  `G=5000,10000,20000` stay below the high-fidelity threshold, with best
  `Bell*=0.489775`. This blocks asymptotic promotion of the current resource
  window.
- It supplies an ideal calibrated square-pulse schedule for the retained record
  slots: `8` equal slots, duration `1`, Rabi frequency `pi/2`, ideal bit error
  `3.749e-33`, and area-error `0.01` bit error `1.000e-04`.
- It realizes the detector theorem with a local spin-bath Hamiltonian model:
  `192` local terms, coupling angle `0.800`, fragment overlap `0.696707`,
  maximum record overlap `1.466e-19`, and zero entropy defect.

This pass strengthens the lane by proving two underdetermination obstructions
and by adding concrete ideal pulse/detector models. It also makes the scaling
problem harder, because side-6 does not preserve the side-4 resource behavior.

## Sixteenth-Pass Nature-Grade Push

The next pass adds explicit selection principles and noisy models rather than
pretending the original axiom already supplies them.

- `scripts/frontier_teleportation_nature_grade_push.py` adds a
  causal-positive minimal action rule for transducer windings. Over windings
  `0..5`, it selects winding `0`, angle `pi/2`, with action gap `19.739209`.
  The note records that negative orientation remains action-degenerate unless
  causal-positive orientation is part of the rule.
- It adds a least-dwell massless-carrier principle in the isotropic
  nearest-neighbor amplitude class. The selected law has center weight `0` and
  neighbor weight `1/sqrt(6)`, with zero norm and isotropy residuals.
- It repairs the finite sparse scaling story by using the signed Poisson branch:
  at fixed `G=-1000`, sides `4,6,8` all have `Phi+` retained resources with
  `Bell* >= 0.999702` and best-frame `F_avg >= 0.999802`.
- It adds a noisy pulse decoder. With area error `0.01` and leakage probability
  `1e-5`, the effective slot error is `1.100e-04` and the decoded record word
  failure is `5.055e-11`.
- It hardens the spin-bath detector with thermal reset failure `0.01` and
  fragment loss `0.05`; the effective fragment count is `22/24`, the maximum
  record overlap is `8.770e-18`, and the entropy defect is numerical zero.

This is the strongest conditional closure so far. It still does not derive the
added principles from the original sole axiom, prove an asymptotic preparation
theorem, or replace independent-error apparatus models with hardware/material
constructions.

## Seventeenth-Pass Open-Item Attack

The next pass keeps the lane conditional but attacks the remaining open items
with sharper executable pressure.

- `scripts/frontier_teleportation_open_item_attack.py` promotes the prior
  minimal-action rule into a retained-action bridge principle inside the audited
  stabilizer-controlled write class. Over windings `0..7`, it selects winding
  `0`, angle `pi/2`, with action gap `19.739209`. Bare action remains
  orientation-degenerate; the bridge needs causal-positive orientation.
- It promotes the carrier rule into a no-dwell/cubic-covariant bridge. The
  selected amplitude law has center weight `0`, neighbor weight `1/sqrt(6)`,
  zero norm/isotropy residuals, and only global phase degeneracy in the audited
  class.
- It extends the signed sparse 3D branch to side `10` at fixed `G=-1000`.
  Sides `4,6,8,10` all remain `Phi+` retained resources with
  `Bell* >= 0.999702`; the side-10 row has gap `0.00459031`,
  `Fbest=0.999807`, and `CHSH=2.827610`.
- It records a finite-size preparation fit for the signed branch:
  `gap_power=1.821867`, `max_log_fit_residual=2.073e-02`,
  `max_Tadiabatic=3.278e+05`, and `max_beta_cooling=4.515e+03`. This is a
  fit over finite rows, not an asymptotic theorem.
- It replaces the independent pulse model with a correlated common-mode drift
  model plus local area error, leakage, and crosstalk. The decoded record word
  failure is `8.458e-12` mean and `1.449e-11` worst branch.
- It supplies a finite local 3D Ising-domain detector proxy: `5x5x5` spins per
  slot, `2400` local bonds across the eight record slots, word-failure bound
  `2.390e-133`, log10 record-overlap bound `-655.141`, and Arrhenius wall
  factor `1.929e-22`.

This narrows the remaining blocker list. It still does not derive the bridge
principles from the original sole axiom, prove asymptotic preparation/cooling,
or specify a laboratory material/controller implementation.

## Eighteenth-Pass Unconditional-Closure Attack

The next pass attacks the remaining blockers at theorem-premise level rather
than promoting the lane.

- `scripts/frontier_teleportation_unconditional_closure_attack.py` records a
  bare one-axiom underdetermination witness: `8` transducer windings times `4`
  carrier candidates give `32` equivalent local-Hermitian flow pairs with the
  same audited protocol observables. The selection entropy is `5` bits, so the
  bare Hilbert/local-flow surface still does not select the apparatus or
  amplitude law.
- It isolates the minimal variational completion that would select the current
  bridge principles: retarded causal-positive orientation, minimal generator
  action over equivalent Bell-record writers, and no-dwell cubic-covariant
  nearest-neighbor carrier. This selects winding `0`, angle `pi/2`, center
  weight `0`, and neighbor weight `1/sqrt(6)`.
- It turns the signed sparse resource fit into a conditional theorem schema.
  The audited rows satisfy `gap(L) >= 0.380/L^2` on sides `4,6,8,10`, with
  minimum `Bell*=0.999702` and monotone `gap*L^2`. If those two floors extend
  to all even `L >= 4`, then preparation has polynomial bounds
  `T_ad <= L^4 / 0.380^2 log(1/eps)` and
  `beta <= L^2 / 0.380 log((L^6 - 1)/eps)`.
- It replaces the pulse proxy with a threshold class: the length-8,
  distance-5 record code corrects two slot flips, and any hardware with worst
  conditional slot error below `2.622e-03` passes a `1e-6` word-failure target
  by union bound. The current correlated model has max slot error
  `5.631e-04`.
- It replaces the finite detector proxy with a thermodynamic Ising-domain
  class. At domain side `5`, the KL majority bound gives word failure
  `7.498e-131`, log10 record-overlap bound `-655.141`, and Arrhenius wall
  factor `1.929e-22`, with decay class
  `word~exp(-Theta(L^3)), wall~exp(-Theta(L^2))`.

This is a sharpened closure attack, not unconditional closure. The remaining
work is now explicit: derive or retain the variational completion, prove the
signed-branch gap/Bell floors asymptotically, and realize the threshold classes
in a material controller/detector model.

## Nineteenth-Pass Retention-Theorem Attack

The next pass pushes the remaining blockers into a retention decision plus a
side-12 certificate.

- `scripts/frontier_teleportation_retention_theorem_attack.py` closes the
  bare selector-derivation route negatively on the audited invariants:
  `32` equivalent local-Hermitian flow pairs remain, carrying `5` bits of
  selector entropy. The lane must therefore retain the variational completion,
  derive it from a stronger theorem, or not promote.
- The minimal sufficient completion is now explicit as three clauses:
  retarded causal-positive orientation, minimal generator/action norm over
  equivalent Bell-record writers, and no-dwell cubic-covariant nearest-neighbor
  carrier.
- The signed sparse branch now survives side `12` at fixed `G=-1000`. The
  side-12 row has `gap=0.003218725689`, `gap*L^2=0.463496`,
  `Bell*=0.999711313114`, `Fbest=0.999807542076`, and
  `CHSH=2.827610624410`.
- The finite theorem pressure is sharpened to
  `gap(L) >= 0.390/L^2` and `Bell*(L) >= 0.999702` on audited sides
  `4,6,8,10,12`. The remaining scaling proof is now the all-even-side induction
  or analytic operator inequality extending those floors.
- The pulse threshold class is mapped to a local controller envelope:
  slot threshold `2.622e-03`, area budget `0.050937 rad`, implemented area
  bound `0.023000 rad`, implemented slot error `5.589e-04`, and word-failure
  bound `9.757e-09`.
- The detector threshold class is mapped to a local Ising-domain material
  envelope: side `5`, `125` spins per slot, `2400` local bonds, `J/T=1`,
  defect probability `0.002`, word-failure bound `7.498e-131`, log10 overlap
  bound `-655.141`, and Arrhenius wall factor `1.929e-22`.

This is the strongest attack so far, but it remains conditional. It supplies a
retention route and local implementation envelopes, not a derivation from the
bare sole axiom, not an all-scale proof, and not a fabricated material device.

## Twentieth-Pass Remaining-Open-Item Attack

The next pass reduces the last open items to explicit obligations and target
specifications.

- `scripts/frontier_teleportation_remaining_open_item_attack.py` proves the
  three-clause selector completion is clause-minimal on the audited invariants.
  Without causal-positive orientation there are `2` residual selectors; without
  minimal action there are `8`; without no-dwell carrier selection there are
  `4`; with all three clauses the selector count is `1`.
- It keeps the signed branch evidence at sides `4,6,8,10,12` and records the
  induction target:
  `gap(L)*L^2 >= 0.390` and `Bell*(L) >= 0.999702` for every even
  `L >= 4` on the signed `G=-1000` branch.
- A direct side-14 sparse eigensolve was attempted and exceeded the local turn
  budget, so side 14 is not counted as evidence.
- It translates the pulse threshold into a controller requirement envelope:
  target word failure `1e-6`, slot threshold `2.622e-03`, leakage budget
  `1e-5`, crosstalk budget `2e-5`, area budget `0.050937 rad` (`2.918 deg`),
  implemented area bound `0.023000 rad`, and margin `2.215`.
- It translates the detector threshold into a material requirement envelope:
  domain side `5`, `125` spins per slot, `2400` local bonds, `J/T >= 1`,
  defect probability `<= 0.002`, word-failure bound `7.498e-131`, and log10
  overlap bound `-655.141`.

This pass does not add a new retained claim. It makes the remaining review
work concrete: retain or derive the three-clause selector completion, prove the
all-even-side signed-branch induction target, and map the controller/material
requirements to actual fabricated or measured systems.

## Twenty-First-Pass Conclusion Boundary

The current pass closes the planning lane without promoting it to nature-grade
closure.

- `scripts/frontier_teleportation_conclusion_boundary.py` records the selector
  conclusion: without the orientation clause there are `2` residual selectors,
  without minimal action there are `8`, without no-dwell there are `4`, and
  with all three clauses the selector count is `1`. The bare derivation status
  remains negative on audited invariants.
- The terminal selector decision is explicit: retain the three-clause
  completion as an added lane principle, derive it from a stronger theorem, or
  do not promote.
- The scaling conclusion records certified sides `4,6,8,10,12`, with
  `gap_floor=0.390/L^2`, `bell_floor=0.999702`, and minimum margin
  `2.750e-05`. The side-14 direct solve exceeded the local turn budget and is
  not counted as evidence.
- The terminal scaling decision is explicit: prove the all-even-side induction
  or operator inequality, or keep resource genesis at finite-certificate
  status.
- The hardware conclusion records target thresholds only: slot threshold
  `2.622e-03`, area budget `0.050937`, controller margin `2.215`, detector
  word bound `7.498e-131`, and detector log10 overlap `-655.141`. No measured
  device/material data is supplied.

The lane conclusion is therefore:

```text
planning_closed = True
unconditional_closed = False
promote_to_nature_grade = False
retained_status = planning closed as conditional theory; nature-grade closure HOLD
```

This is the terminal in-repo boundary for the current evidence set.

## What This Artifact Supports

This artifact supports the first planning-gate statement:

> Standard quantum state teleportation can be represented on an encoded
> taste-qubit register using the local Hilbert/tensor-product surface and the
> same native taste Pauli operators used by the CHSH lane.

It also gives a concrete protocol file and a numerical no-signaling audit for
Bob's reduced state before receipt of Alice's classical record.

## Limitations

This is a first ideal protocol artifact.

- The Bell resource in the base protocol is still ideal. A small-surface
  Poisson/CHSH resource audit is now positive on selected cases and survives a
  bounded sweep as a parameter-window result, but this is not yet a
  preparation/readout derivation across parameters, dimensions, boundary
  choices, and degeneracy controls.
- Simple product-state time evolution under the Poisson Hamiltonian creates
  useful low-fidelity logical resources on the audited `1D N=8` cases, but no
  high-fidelity default window. Raw product-state dynamics is therefore not yet
  the resource-generation mechanism.
- A bounded adiabatic/gap probe makes the linear `G=0 -> G_target` path worth
  further study, especially on the `2D 4x4` case, but it does not provide a
  finite-time schedule, diabatic-error bound, control-noise model, or
  preparation proof.
- Finite-time closed-system evolution now gives a strong small-surface
  preparation-candidate diagnostic for the `2D 4x4` smoothstep ramp, but still
  assumes ideal Hamiltonian control, an initially prepared `G=0` ground state,
  no bath/noise/leakage model, and no independent step-convergence or scaling
  proof.
- Step convergence, propagator comparison, and small perturbation controls now
  support the numerical stability of the `2D 4x4` smoothstep candidate.
  Schedule noise shows that high reduced logical fidelity can coexist with
  non-negligible full-state diabatic loss, so ground-state tracking and logical
  teleportation fidelity must both remain reported.
- The `G=0` initial state is now shown to be unique, gapped, separable, and
  analytically simple on the audited small surfaces, but a physical
  preparation/cooling/control protocol for that delocalized state is still not
  supplied.
- Smallest-surface 3D pressure tests are now positive: the `3D side=2`
  Poisson resource and finite-time ramp produce high-fidelity retained-axis
  Bell-frame resources. These are still side-2 dense diagnostics, not 3D
  scaling, robustness, or hardware-preparation proofs.
- The 3D positive resource lands in the `Psi+` Bell frame. Any 3D protocol
  statement must either track that known frame or explicitly supply the
  retained-axis local frame correction before standard feed-forward.
- The Bell measurement now has an explicit orthogonal record-register model,
  and its projectors have an ideal logical stabilizer/circuit decomposition.
  A native durable-record measurement derivation and physical logical gate or
  apparatus schedule remain open.
- The classical channel now has a directed-lattice/DAG causal harness, but it
  is still an explicit record channel, not a derived field-theoretic
  communication channel. A 3D+1 light-cone record model now fixes the intended
  causal geometry for the explicit two-bit record.
- Noise, loss, imperfect resource states, and record faults now have a first
  controls harness, but only for independent supplied-fault models, not a
  physical apparatus or environmental error model.
- Encoding portability is now surveyed algebraically across bounded small
  lattices. The current fixed pair-hop `X` is portable only for the last taste
  axis unless an axis-adapted taste `X` is supplied.
- Cross-encoding maps now pass algebraically for surveyed cells, spectator
  tastes, and logical axes when axis-adapted logical operators and explicit
  site-support conversion maps are supplied. These maps remain ideal logical
  objects, not an apparatus or transport derivation.
- Trace extraction is mathematically valid for taste-only observables on the
  audited positive Poisson cases, but operational taste-only readout remains
  unproved. The operator model supports retained-axis logical operators, but
  rules out raw sublattice parity `Z=xi_5` as a traced retained-bit-only
  readout/correction in `dim>1`. Fixed-environment branch variation cannot be
  promoted to a deterministic protocol without a readout/heralding model.
- The operator-consistent end-to-end audit now enforces the retained-axis
  `Z/X` convention and includes raw-`xi_5` rejection controls for `dim>1`.
  This narrows the convention risk but still assumes ideal logical
  measurement/readout/correction operators.
- The 3D readout convention is now separately audited across all retained
  axes. In 3D, raw `xi_5` is only a fixed-spectator-branch signed Pauli; traced
  retained-bit readout/correction requires retained-axis `Z_r tensor I_env`.
- Three-register cross-encoding passes a bounded algebraic survey when
  explicit `A->R` and `R->B` site-support maps and axis-adapted operators are
  supplied. This remains finite, ideal, and not a physical transport or
  apparatus derivation.
- The acceptance suite currently passes its required bounded probes, but it is
  an orchestration harness rather than a claim surface. The strict-lane profile
  adds blocking current-lane telemetry, not a proof of native hardware
  preparation or readout.
- The artifacts still do not implement transport through a full staggered
  Hamiltonian or a physical resource-preparation/readout workflow.
- No matter, charge, mass, or energy is teleported. Only an unknown quantum
  state on Bob's already-present encoded taste qubit is reconstructed after
  Bob receives Alice's classical bits.

## Status

The first artifact passes the initial numerical gates in the bounded planning
lane, and the consolidated acceptance suite passes the current required
bounded probes. This does not promote the lane beyond planning / first
artifact status.
