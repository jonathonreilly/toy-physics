# Teleportation Causal Channel Note

**Date:** 2026-04-25
**Status:** planning / first causal-channel artifact
**Runner:** `scripts/frontier_teleportation_causal_channel.py`

## Question

Can the teleportation lane make the two-bit Bell record explicitly causal
without implying that the record is derived by the lattice/DAG machinery?

The tested answer is yes, with a strict boundary: the artifact models only a
classical record channel for the Bell-measurement bits. It does not model
faster-than-light signaling, matter teleportation, mass transfer, charge
transfer, or a derivation of the record from a CHSH or Poisson-coupled lane.

## Model

Alice's Bell measurement produces a two-bit classical record:

```text
sender = Alice
receiver = Bob
bits = (z, x)
created_at_tick = t
deliver_at_tick = t + path_latency + optional_extra_delay
```

The channel is a finite directed lattice/DAG. Edges move only in `+x` or `+y`,
so the route has a strictly increasing rank and cannot cycle. The channel
schedules and delivers a record; it does not compute the Bell bits.

For the first harness run:

```text
Alice node = (0, 0)
Bob node   = (3, 1)
route      = ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1))
latency    = 4 ticks
```

## Gates

The harness checks:

1. Positive causal latency: `deliver_at_tick > created_at_tick`.
2. No early delivery: Bob receives no record before the scheduled delivery
   tick.
3. Duplicate prevention: a reused record id is rejected, and a delivered
   record cannot be received twice.
4. Wrong-record controls: a wrong receiver cannot receive Bob's record, and a
   wrong Bell bit gives low correction fidelity on a non-stabilizer probe
   state.
5. Delayed-record control: an intentionally delayed record is still blocked at
   the base path-arrival tick and appears only at its later delivery tick.
6. Bob no-signaling before delivery: after Alice's Bell measurement but before
   the record arrives, Bob's averaged local density matrix is input-independent
   and equals `I/2` to numerical precision.

## Result

Command:

```bash
python3 scripts/frontier_teleportation_causal_channel.py
```

Observed first-artifact result:

```text
record: Psi- bits(z,x)=(1, 1) created t=7 deliver t=11
channel derives Bell bits: False
path latency ticks: 4
receive at t=10 blocked: True
duplicate record id rejected: True
receive at delivery exactly once: True
delayed control blocked at base arrival: True (base t=24, actual t=26)
delayed control delivered late: True
correct-record fidelity: 1.0000000000000000
wrong-bit control fidelity: 0.3333333333333334
max Bob trace distance to I/2 before Alice measurement: 2.220e-16
max Bob trace distance to I/2 after Alice measurement before delivery: 3.331e-16
max pairwise pre-delivery Bob-state distance across inputs: 1.388e-16
max Bell probability error from 1/4: 1.110e-16
explicit not derived record channel: PASS
positive channel latency: PASS
no early delivery: PASS
duplicate prevention: PASS
wrong/delayed record controls: PASS
post-delivery correction: PASS
Bob pre-delivery no-signaling: PASS
```

The wrong-bit control is not a security proof. It is only a sanity check that
Bob needs the actual Bell record for the selected non-stabilizer input.

## Claim Boundary

This note supports only a causal classical record model for the two-bit Bell
message used in ordinary quantum state teleportation.

It does not support:

- faster-than-light communication;
- controllable signaling before the classical record arrives;
- transport of matter, mass, charge, or energy;
- a final theory of measurement or durable records;
- a derivation of the Bell record from the directed lattice/DAG;
- a derivation of the Bell resource from the Poisson-coupled CHSH system.
