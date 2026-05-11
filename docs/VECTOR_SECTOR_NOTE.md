# Vector Sector: Circular Orbit Handedness

**Date:** 2026-04-06
**Status:** proposed_retained positive — phase-locked handedness (1H amplitude 0.018), not universal DC
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-04-27):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "The
live runner reproduces the phase-locked harmonic/nulled protocol, but
the note does not close the bridge from that selected lock-in
readout to an unqualified retained vector-sector observable; the
current runner output also does not independently report the claimed
matched scalar exposure table." This rigorization edit only sharpens
the boundary of the conditional perimeter; nothing here promotes
audit status. The supported content of this note is the lock-in
harmonic / nulled protocol itself: the §"Decisive tests" results
(phase-averaged DC = +0.000012, 1H amplitude = 0.018, 1529:1 ratio,
f-oddness clean, time-order non-trivial) reproduced live by the
registered runner
[`scripts/vector_sector_circular_orbit.py`](../scripts/vector_sector_circular_orbit.py).
The matched-scalar-exposure table at f=0.02 in §"Result" is reported
in the note but is not independently reproduced by the current runner
output as a labeled column; the §"What this means" framing as a
"phase-locked first-harmonic handedness signal" is bounded
interpretation that does not promote to an unqualified retained
vector-sector observable. The supported perimeter is the lock-in
harmonic protocol and its outputs; bridge-to-retained-vector-sector
language remains conditional. A future runner-cache deposit
explicitly logging the matched-exposure column under audit-lane
runner timeout would close that gap.

## Artifact chain

- [`scripts/vector_sector_circular_orbit.py`](../scripts/vector_sector_circular_orbit.py)
- [`logs/2026-04-06-vector-sector-circular-orbit.txt`](../logs/2026-04-06-vector-sector-circular-orbit.txt)
- This note

## Question

Does an orbiting source produce a deflection that depends on the orbit
direction (handedness), with matched scalar exposure?

## Result

At f=0.02, R=4.0, s=0.004:

| Metric | CCW | CW |
| --- | ---: | ---: |
| dz | **+0.007** | **-0.008** |
| avg 1/r | 0.17724 | 0.17724 |

The dz component flips sign between CCW and CW. Scalar exposure is
exactly matched.

### What passes

- **Exposure match**: avg_1/r(CCW) = avg_1/r(CW) exactly
- **dz sign flip**: CCW gives +dz, CW gives -dz (f=0.01-0.07)
- **Nulls**: s=0 exact, f=0 gives CCW=CW exactly
- **Family portable**: 3/3 families show the flip
- **Speed dependence**: effect present at f=0.01-0.07, vanishes at f=0.10

### What doesn't pass cleanly

- **Start-phase dependence**: 3 of 5 starting phases show the dz flip,
  but 2 do not (phi0=pi/2 and phi0=3*pi/2). The handedness is not
  fully phase-independent.

## Why linear drift fails but circular orbit succeeds

Linear drift changes the scalar exposure: +v brings the source closer
(more 1/r), -v takes it farther (less 1/r). The force asymmetry is
entirely from distance change.

Circular orbit keeps the same distance at all times. The asymmetry
comes from the ORDER in which the source passes through different
positions along the beam path. CW and CCW trace the same positions
but in opposite temporal order, creating a chirality in the
accumulated phase pattern.

This is the discrete analog of the right-hand rule: a current loop
creates a magnetic field with handedness determined by the current
direction. Here, the orbiting source creates a phase pattern with
handedness determined by the orbit direction.

## Decisive tests (all completed)

### Phase-averaged: ZERO
<dz>_CCW - <dz>_CW = +0.000012 over 12 starting phases.
The handedness averages out — it is phase-locked, not universal.

### First-harmonic: STRONG
1H amplitude = 0.018, DC = 0.000012. Ratio 1529:1.
The handedness is entirely in the first harmonic referenced to phi0.
This is the correct lock-in readout.

### f-oddness: CLEAN
+f and -f give opposite dz at f=0.01, 0.02, 0.05.

### Time-order: NOT just ordering
Time-reversed CCW gives dz=+0.012, not -0.008 (CW).
The effect is not reducible to temporal ordering of positions.

## What this means

The vector sector is a **phase-locked first-harmonic handedness signal**.
Like measuring a magnetic field with a lock-in amplifier: the DC
readout is zero, but the first-harmonic at the drive frequency is
nonzero and tracks the orbit direction.

This is NOT a universal magnetic-like force (no DC component).
It IS a phase-sensitive dynamic effect that requires lock-in detection.
