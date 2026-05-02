# Teleportation 3D+1 Causal Bell-Record Channel Note

**Date:** 2026-04-26
**Status:** planning / first 3D+1 local record-propagation artifact
**Runner:** `scripts/frontier_teleportation_3d1_causal_record_channel.py`

## Scope

This artifact replaces the earlier generic directed-DAG record harness with an
explicit 3D spatial lattice plus one discrete causal/time direction. It remains
only a classical Bell-record channel for ordinary quantum state teleportation.

The model does not transport matter, mass, charge, energy, or objects. It does
not claim faster-than-light signaling or controllable pre-message influence.

## Model

Alice emits an already-created two-bit Bell record at a 3D lattice site and
integer tick:

```text
record = (z, x)
source event = (x_A, y_A, z_A, t_A)
target site = (x_B, y_B, z_B)
```

The channel accepts either a 3D Manhattan or 3D Chebyshev metric. The default
run uses Manhattan locality with speed one site per tick:

```text
distance = |dx| + |dy| + |dz|
earliest_delivery_tick = emitted_at_tick + ceil(distance / speed)
```

For the default audit:

```text
lattice shape = (8, 6, 5)
Alice site/tick = (1, 1, 1), t=4
Bob site = (5, 3, 2)
metric/speed = manhattan / 1 site per tick
distance = 7
earliest delivery tick = 11
```

The emitted worldline is local at each tick:

```text
t=4:(1, 1, 1)
 -> t=5:(2, 1, 1)
 -> t=6:(3, 1, 1)
 -> t=7:(4, 1, 1)
 -> t=8:(5, 1, 1)
 -> t=9:(5, 2, 1)
 -> t=10:(5, 3, 1)
 -> t=11:(5, 3, 2)
```

The channel schedules and delivers the record. It does not derive the Bell
bits from the lattice, from a measurement apparatus, or from the Bell resource.

## Gates

The runner checks:

1. The 3D+1 worldline is local under the configured metric and integer speed.
2. The earliest delivery tick equals the distance/velocity rule.
3. A target event outside the future cone fails, and Bob cannot receive before
   the cone reaches the target.
4. A duplicate record id is rejected and a delivered record cannot be received
   twice.
5. Wrong receiver and wrong 3D-site receives fail.
6. The correct delivered two-bit record restores Bob's branch state.
7. Wrong, dropped, and delayed records act as controls.
8. Bob's pre-delivery local state is input-independent and equals `I/2` to
   numerical precision.

## First Run

Commands:

```bash
python3 -m py_compile scripts/frontier_teleportation_3d1_causal_record_channel.py
python3 scripts/frontier_teleportation_3d1_causal_record_channel.py
```

Observed output:

```text
metric / speed: manhattan / 1 site(s)/tick
spatial distance: 7
expected light-cone latency: 7 tick(s)
earliest delivery tick: 11
worldline local under metric: True
delivery event inside future cone: True
record: Psi- bits(z,x)=(1, 1) id=bell-record-3d1-0001
channel derives Bell bits: False
Bell branch probability: 0.2499999999999999
earliest tick equals distance/velocity rule: True
target event at t=10 outside cone rejected: True
receive before cone arrival blocked: True
wrong receiver blocked: True
wrong 3D site blocked: True
duplicate record id rejected: True
receive at delivery exactly once: True
correct delivered-record fidelity: 1.0000000000000000
wrong-record fidelity: 0.3333333333333334
dropped/pre-delivery no-correction fidelity: 0.3333333333333333
dropped record remains undelivered: True
delayed control blocked at base arrival: True (base t=11, actual t=13)
delayed control delivered late: True
delayed delivered-record fidelity after waiting: 1.0000000000000000
max Bob trace distance to I/2 before Alice measurement: 2.220e-16
max Bob trace distance to I/2 after Alice measurement before delivery: 3.331e-16
max pairwise pre-delivery Bob-state distance across inputs: 1.388e-16
max Bell probability error from 1/4: 1.110e-16
```

The runner reports `PASS` for:

- 3D+1 light-cone locality;
- distance/velocity earliest arrival;
- outside-cone attempts fail;
- no duplicate delivery;
- correct record restores Bob state;
- wrong/dropped/delayed controls;
- Bob pre-delivery input-independence;
- explicit not-derived record channel.

## Limitations

- The Bell record is supplied to the channel; the channel does not derive it.
- The Bell measurement, durable classical record, and apparatus dynamics remain
  idealized.
- The Bell resource is assumed by this runner.
- The dropped and wrong-record controls are sanity checks, not security proofs.
- The lattice is a discrete planning model, not a relativistic field theory.
- The artifact supports ordinary quantum state teleportation only. It does not
  transfer matter, mass, charge, energy, or objects, and it does not support
  faster-than-light signaling.
