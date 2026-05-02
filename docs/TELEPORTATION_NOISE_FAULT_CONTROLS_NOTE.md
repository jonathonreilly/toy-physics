# Teleportation Noise/Fault Controls Note

**Date:** 2026-04-25
**Status:** planning / first artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_noise_fault_controls.py`

## Scope

This note records a bounded noisy-control harness for ordinary qubit state
teleportation. It extends the prior ideal protocol, resource-fidelity, and
causal-record harnesses with explicit independent fault layers:

- resource depolarization;
- Bell-measurement readout bit flips;
- classical Bell-record bit flips, drops, and delays;
- Bob correction-control bit errors.

It does not claim matter teleportation, mass transfer, charge transfer, energy
transport, or faster-than-light communication.

## Fault Model

Registers are ordered as:

```text
A = Alice unknown qubit
R = Alice resource half
B = Bob resource half
```

The shared resource family is:

```text
rho_RB(v) = v |Phi+><Phi+| + (1-v) I/4
```

Alice's Bell measurement is still an ideal projective Bell measurement. The
"Bell-measurement bit-flip" controls model readout/record bit corruption after
that projection, not a derived nonprojective apparatus model.

The classical record then passes through independent bit flips, drop events,
and delay events. At the fixed readout deadline, a dropped or delayed record is
unavailable and Bob uses the identity fallback. Eventually, delayed records are
allowed to arrive and can be corrected; dropped records never arrive.

Bob correction errors are modeled as independent flips of the commanded `z` and
`x` correction bits before applying `Z^z X^x`.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_noise_fault_controls.py
```

Observed profile diagnostics:

```text
profile                                  v   D_now   D_evt     F_now     F_evt  Fmin_now  Fmin_evt     noSig  verdict_now
ideal reference                      1.000   1.000   1.000  1.000000  1.000000  1.000000  1.000000 3.053e-16    beats 2/3
resource depolarization v=0.90       0.900   1.000   1.000  0.950000  0.950000  0.950000  0.950000 2.776e-16    beats 2/3
resource boundary v=1/3              0.333   1.000   1.000  0.666667  0.666667  0.666667  0.666667 2.776e-16       at 2/3
Bell readout flips p=0.05            1.000   1.000   1.000  0.935000  0.935000  0.905000  0.905000 3.053e-16    beats 2/3
classical flips/drop/delay           1.000   0.720   0.900  0.813200  0.891500  0.791600  0.864500 3.053e-16    beats 2/3
Bob correction errors p=0.03         1.000   1.000   1.000  0.960600  0.960600  0.941800  0.941800 3.053e-16    beats 2/3
combined moderate controls           0.850   0.855   0.950  0.784603  0.816225  0.750455  0.778283 2.498e-16    beats 2/3
stress below deadline threshold      0.600   0.525   0.750  0.557577  0.582253  0.531611  0.545158 3.053e-16    below 2/3
```

Here `D_now` is the total probability that the record has arrived by the
readout deadline, and `D_evt` is the eventual non-dropped delivery probability.
Delays reduce `F_now`; they do not reduce `F_evt` once the delayed record
arrives.

## Thresholds

The runner reported:

```text
classical qubit average-fidelity benchmark: 0.6666666667
resource depolarization only: v > 0.3333333333
symmetric Bell-measurement record bit-flip error only: p < 0.2928932188
symmetric classical-record bit-flip error only: p < 0.2928932188
symmetric Bob correction-control bit error only: p < 0.2928932188
record drop probability only, identity fallback: p_drop < 0.6666666667
record delay past readout deadline only: p_delay < 0.6666666667
combined moderate non-resource faults require visibility by deadline: v > 0.4977698836
combined moderate non-resource faults require visibility eventually: v > 0.4479928952
```

The bit-flip thresholds are for independent symmetric flips of the two Bell
record bits with all other faults off. The drop and delay thresholds assume an
ideal resource and identity fallback when Bob lacks the record. They are
readout-deadline thresholds, not claims about usable correction before a
causal record arrives.

## No-Signaling Diagnostics

Observed no-signaling and normalization quantities:

```text
max Bob no-record trace distance to I/2: 6.384e-16
max pairwise Bob no-record distance across sampled inputs: 3.053e-16
max Bell-branch probability span across sampled inputs: 2.776e-16
max output trace error by deadline: 2.887e-15
max output trace error eventually: 2.887e-15
```

Record drop and delay probabilities are input-independent by construction. The
input-dependent high-fidelity state appears only after causal record delivery
and Bob-side correction.

## Acceptance Gates

The run reported `PASS` for:

- ideal reference fidelity;
- resource boundary at `2/3`;
- threshold crossing detection;
- combined moderate profile beating the deadline benchmark;
- stress profile falling below the deadline benchmark;
- Bob pre-record input-independence;
- trace preservation.

## Limitations

This remains a bounded first artifact.

- The Bell resource is supplied as a depolarized density matrix. It is not
  derived from native preparation dynamics.
- Bell measurement projection is still ideal. The added measurement fault is a
  classical readout-bit corruption layer.
- Faults are independent and input-independent. Correlated, adversarial, or
  apparatus-state-dependent faults are not modeled.
- Bob's fallback for missing records is fixed to identity.
- Delay is modeled as late classical delivery relative to a readout deadline,
  not as a spacetime propagation derivation.
- The no-signaling audit is a density-matrix check on Bob before record
  delivery. It is not a field-theoretic communication-channel proof.
- The input is a qubit state. No matter, charge, mass, energy, or macroscopic
  object is teleported.

## Status

The teleportation lane now has a first noisy/faulty controls harness. It
quantifies how supplied resource depolarization, record corruption, loss,
latency, and correction-control errors degrade fidelity while preserving the
strict causal-record boundary.
