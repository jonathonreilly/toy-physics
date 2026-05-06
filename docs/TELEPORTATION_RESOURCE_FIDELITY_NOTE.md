# Teleportation Resource-Fidelity Note

**Date:** 2026-04-25
**Status:** bounded open-gate derivation artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_resource_fidelity.py`

## Scope

This note records a bounded stress test of the ideal Bell-resource assumption
in the native teleportation lane. The scope is ordinary quantum state
teleportation only.

The harness keeps the Bell measurement, two-bit classical record, and Bob-side
Pauli correction ideal. It varies only the shared two-qubit resource density
matrix `rho_RB`.

It does not claim matter teleportation, mass transfer, charge transfer, energy
transport, or faster-than-light communication.

## Harness

Registers are ordered as:

```text
A = Alice unknown qubit
R = Alice resource half
B = Bob resource half
```

For each input state `rho_A` and resource `rho_RB`, the script forms:

```text
rho_ARB = rho_A tensor rho_RB
```

Alice measures `A,R` in the four Bell projectors, Bob receives the two-bit
record, and Bob applies the fixed correction:

```text
U_zx = Z^z X^x
```

For each resource the script reports:

- exact average teleportation fidelity from the channel Choi matrix;
- sampled average/min/max fidelity on six Pauli-axis probes plus random states;
- Bell overlaps, especially `<Phi+|rho|Phi+>`;
- negativity and Horodecki `S_CHSH`;
- Bob marginal bias from `I/2`;
- no-signaling distances for Bob before the classical Bell record is available;
- branch-probability input dependence as a limitation diagnostic.

The runner also accepts an optional arbitrary 4x4 density matrix through
`--matrix-json`.

## Thresholds

For this fixed Bell-basis measurement and fixed Pauli-correction convention,
the exact average fidelity obeys:

```text
F_avg = (1 + 2 * <Phi+|rho|Phi+>) / 3
```

Therefore the fixed-protocol threshold for beating the qubit classical
benchmark is:

```text
F_avg > 2/3  iff  <Phi+|rho|Phi+> > 1/2
```

For the isotropic family:

```text
rho(v) = v |Phi+><Phi+| + (1-v) I/4
```

the teleportation threshold is `v > 1/3`. The CHSH threshold for the same
isotropic family is higher, `v > 1/sqrt(2)`, so a resource can beat the
teleportation benchmark without violating CHSH.

## Fixed-Protocol Derivation

Let `g=(z,x)` label the four Bell states
`|beta_g> = |Phi+>, |Phi->, |Psi+>, |Psi->`, with the same bit convention used
by the runner, and let `P_g` be the corresponding Pauli on Bob's qubit, up to
an irrelevant overall phase:

```text
P_00 = I,   P_10 = Z,   P_01 = X,   P_11 = ZX.
```

The resource is an arbitrary physical two-qubit density matrix on `R,B`. Expand
it in this Bell basis:

```text
rho_RB = sum_{g,h} rho_{g,h} |beta_g><beta_h|.
```

For a pure input state `|psi>` and Bell-measurement outcome `m`, the branch
amplitude from a pure resource component `|beta_g>` is:

```text
(<beta_m|_AR tensor I_B)(|psi>_A tensor |beta_g>_RB)
    = (1/2) phase(m,g) P_m^\dagger P_g |psi>_B.
```

After Bob applies the fixed correction `P_m`, that branch becomes:

```text
(1/2) phase(m,g) P_g |psi>_B.
```

Thus an off-diagonal Bell-basis resource element
`|beta_g><beta_h|` contributes, after summing over the four classical records,

```text
(1/4) sum_m phase(m,g) phase(m,h)^* P_g |psi><psi| P_h^\dagger.
```

The phases are the four characters of the two-bit Pauli/Bell label group, so
their record sum is orthogonal. Equivalently, for `m=(z_m,x_m)` the relative
branch phase can be chosen in the form

```text
phase(m,g) phase(m,h)^*
    = c_{g,h} (-1)^{z_m (x_g xor x_h) + x_m (z_g xor z_h)},
```

where `c_{g,h}` is independent of the measurement record. Summing over the four
records gives:

```text
(1/4) sum_m phase(m,g) phase(m,h)^* = delta_{g,h}.
```

All Bell-basis coherences in `rho_RB` therefore drop out of this fixed
Bell-measurement/Pauli-correction protocol. By linearity, the corrected
teleportation channel is exactly the Pauli channel

```text
T_rho(sigma) = sum_g p_g P_g sigma P_g^\dagger,
    p_g = <beta_g|rho_RB|beta_g>.
```

The Choi state of this channel is diagonal in the same Bell basis:

```text
J(T_rho) = sum_g p_g |beta_g><beta_g|.
```

Therefore the channel entanglement fidelity against the identity channel is
just the identity-error probability

```text
F_e = <Phi+|J(T_rho)|Phi+> = p_00 = <Phi+|rho_RB|Phi+>.
```

For a trace-preserving single-qubit channel, the Haar-average pure-state
fidelity is related to entanglement fidelity by

```text
F_avg = (2 F_e + 1) / 3.
```

Combining the last two equations gives the fixed-protocol formula used by the
runner:

```text
F_avg = (1 + 2 * <Phi+|rho_RB|Phi+>) / 3.
```

The qubit classical benchmark is `2/3`, so this fixed convention beats the
benchmark exactly when:

```text
<Phi+|rho_RB|Phi+> > 1/2.
```

This is not an optimized teleportation-fidelity theorem. A resource whose
largest Bell overlap is in another Bell frame can be rescued by relabeling or
changing local frames; this note's threshold is only for the fixed `Phi+`
measurement/correction convention above.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_resource_fidelity.py --trials 128 --seed 20260425 --random-resources 4
```

Observed threshold and formula checks:

```text
classical qubit average-fidelity benchmark: 0.6666666667
fixed-protocol quantum-useful threshold: <Phi+|rho|Phi+> > 0.5
isotropic rho(v)=v|Phi+><Phi+|+(1-v)I/4 threshold: v > 1/3
isotropic CHSH Horodecki threshold: v > 0.7071067812
amplitude damping on both halves numeric fixed-protocol threshold: gamma < 0.9999999851
amplitude damping on Bob half numeric fixed-protocol threshold: gamma < 0.8284271247
max exact-vs-Bell-overlap formula error in this run: 4.441e-16
random arbitrary resources beating 2/3 in this seed: 0/4
```

Representative resource outcomes:

```text
ideal Phi+ resource                    F_avg=1.000000  p_Phi+=1.000000  S_CHSH=2.82843
isotropic v=0.90                       F_avg=0.950000  p_Phi+=0.925000  S_CHSH=2.54558
isotropic v=1/sqrt(2)                  F_avg=0.853553  p_Phi+=0.780330  S_CHSH=2.00000
isotropic v=1/3 boundary               F_avg=0.666667  p_Phi+=0.500000  S_CHSH=0.94281
isotropic v=0.30                       F_avg=0.650000  p_Phi+=0.475000  S_CHSH=0.84853
Bell phase-flip p=0.25                 F_avg=0.833333  p_Phi+=0.750000  S_CHSH=2.23607
Bell phase-flip p=0.50 boundary        F_avg=0.666667  p_Phi+=0.500000  S_CHSH=2.00000
amplitude damping both gamma=0.50      F_avg=0.750000  p_Phi+=0.625000  S_CHSH=1.41421
amplitude damping Bob gamma=0.50       F_avg=0.819036  p_Phi+=0.728553  S_CHSH=2.00000
```

The four random arbitrary two-qubit density matrices generated with seed
`20260425` had exact average fidelities between `0.400771` and `0.466959`, so
none beat the `2/3` benchmark in this run.

## No-Signaling Diagnostics

Observed no-signaling quantities:

```text
max trace distance between Bob no-record state and resource Bob marginal: 5.274e-16
max pairwise Bob no-record distance across sampled inputs: 3.053e-16
max Bob marginal bias from I/2 across resources: 5.000e-01
max Bell-outcome probability span across sampled inputs: 5.000e-01
```

The first two quantities are the no-signaling checks and remain at numerical
precision. The latter two are limitation diagnostics: a non-ideal resource can
give Bob a biased pre-shared marginal, and Alice's Bell-outcome probabilities
can depend on the input state. Neither effect gives Bob Alice's unknown state
before the two-bit classical record arrives.

## Acceptance Gates

The first run reported `PASS` for:

- all resource matrices physical;
- ideal resource fidelity;
- fixed Bell-overlap formula;
- isotropic threshold bracket;
- Bob pre-message input-independence;
- corrected channel trace preservation.

## Limitations

This is still a bounded open-gate artifact.

- The Bell resource is supplied as a density matrix. The runner does not derive
  it from the Poisson-coupled CHSH Hamiltonian or any native preparation
  dynamics.
- The Bell measurement and Bob correction are ideal. Measurement noise,
  classical record corruption, loss, and timing faults are not included.
- The fidelity threshold is for the fixed Bell-basis protocol. The script
  reports the best overlap among the four Bell labels, but it does not optimize
  arbitrary local unitaries or measurement settings.
- The no-signaling audit concerns Bob's pre-message density matrix only. It
  does not derive a field-theoretic communication channel.
- The input is a qubit state. No matter, charge, mass, energy, or macroscopic
  object is teleported.

## Status

The ideal Bell-resource assumption is now bounded by a concrete fidelity
harness. The useful fixed-protocol resource condition is explicit:
`<Phi+|rho|Phi+> > 1/2`. This closes the supplied-density-matrix,
fixed-protocol threshold derivation only; the broader teleportation lane
remains open-gate outside this narrow scope.
