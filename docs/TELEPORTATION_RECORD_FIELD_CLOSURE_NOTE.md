# Teleportation Record-Field Closure Probe Note

---

**This is a planning / finite-model probe note. It does not establish
any retained claim.** For retained claims on the teleportation lane,
see the per-claim notes referenced from the `## Review scope` block
below.

---

**Date:** 2026-04-26
**Status:** support / planning record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / planning record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit outcome.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Runner:** `scripts/frontier_teleportation_record_field_closure.py`

## Review scope (relabel 2026-05-10)

This file is a **planning record-field, durability, and ledger closure
probe**. It is **not** a retained closure theorem and **must not** be
audited as one. Generated-audit context identified this repair target:

> scope_too_broad: Declare the native apparatus row as a dependency
> and close it cleanly, then replace the eikonal carrier, pointer
> bath, and ledger split with retained derivations or narrow the
> claim to an explicit finite-model planning gate.

The minimal-scope response in this PR is to **relabel** this document
as a finite-model planning gate / labeled support record, taking the
"narrow the claim" branch of the auditor's repair target. The
alternatives — declaring and closing the native apparatus dependency,
or replacing the eikonal carrier, pointer bath, and ledger split with
retained derivations — belong in dedicated review-loop or per-target
audit passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The eikonal record field, durable pointer threshold, ledger gates,
  and "Retained-Theory Impact" wording below are **planning-level
  finite-model evidence only**, conditional on imported native
  apparatus / Bell-transducer / readout / detector premises that are
  not derived in this artifact.
- The retained-status surface for any teleportation-lane sub-claim is
  the audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus dedicated
  per-claim notes, **not** this probe.

The "Remaining Nature-Grade Blockers" section below already records
the upstream open items (relativistic field equation, bath /
entropy-production / detector derivation, projective-Bell transducer,
physical conservation laws, ideal Bell-resource and readout). Treating
this note as a planning probe rather than as a closure theorem keeps
those open items as the live retained-status surface for the lane.

## Scope

This artifact goes after the remaining native-record blockers after the first
apparatus/carrier pass:

- the record carrier should be derived from a local 3D+1 field rule, not a
  prescribed worldline;
- the pointer should have explicit durability and fault thresholds, not just a
  redundant codeword;
- the no-transfer claim should be tied to conservation ledgers, not only
  stated in prose.

This is still a planning artifact. It does not derive a retained relativistic
field equation, a physical detector, environmental decoherence, or a
thermodynamic bath. It does not promote the teleportation lane to retained
nature-grade closure.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## New Model Pieces

### 1. Local Eikonal Record Field

The record carrier route is now generated from a 3D lattice eikonal field

```text
D(r) = |r_x - b_x| + |r_y - b_y| + |r_z - b_z|
```

with Bob's target site `b` as the sink. The local routing equation is:

```text
D(r) = 1 + min_neighbor D(neighbor),  D(b) = 0.
```

Each record pulse moves only to a nearest neighbor with `D -> D - 1`. The
carrier route is therefore derived from a local field rule and arrives after
exactly the Manhattan distance.

For the default geometry:

```text
lattice shape = (8, 6, 5)
Alice site/tick = (1,1,1), t=4
Bob site = (5,3,2)
Manhattan distance = 7
field-delivery tick = 11
```

### 2. Durable Pointer Threshold

The previous record code remains:

```text
z z z | x x x | p p,  p = z xor x
```

This pass adds two explicit durability checks:

- adversarial decoding corrects all one- and two-component bit flips;
- erasure-aware decoding corrects all one-, two-, three-, and four-component
  erasures.

It also adds a small thermodynamic stability proxy: each component is an odd
ferromagnetic domain of size `9`, decoded by majority. At independent spin
flip probability `p=0.10`, the exact word-failure probability is below
`1e-6` after the outer code corrects up to two failed components.

### 3. Conservation-Ledger Gates

The runner separates base ledgers from the retained taste-qubit fiber. Bob's
Pauli correction is checked as

```text
I_base tensor P_fiber
```

and commutes with mass, charge, and support ledgers on the base. The record
carrier uses fixed-length polarity pulses, so pulse energy and domain memory
size are independent of whether the carried bit is `0` or `1`.

This does not derive all physical conservation laws, but it turns the
no-transfer boundary into concrete algebraic gates for this candidate model.

## First Run

Commands:

```bash
python3 -m py_compile scripts/frontier_teleportation_record_field_closure.py
python3 scripts/frontier_teleportation_record_field_closure.py
```

Observed output:

```text
lattice shape: (8, 6, 5)
source -> target: (1, 1, 1)@t=4 -> (5, 3, 2)@t=11
eikonal max residual: 0
spatial Manhattan distance: 7
max route length: 8
max delivery tick error: 0
field-derived routes local/monotone: True
carrier payloads from Bell transducer: True
generated Bell labels: Phi+, Phi-, Psi+, Psi-
early decode blocked: True
max Bob trace distance to I/2 before field delivery: 3.053e-16
max pairwise pre-delivery Bob-state distance across inputs: 2.220e-16
minimum field-delivered corrected fidelity: 0.9999999999999998
maximum field-delivered infidelity: 2.220e-16
max corrected-state trace distance to input: 1.943e-16
adversarial pointer code: flip_cases=148, erasure_cases=652, two_flip_corrected=True, four_erasure_corrected=True, silent_wrong=0
thermal pointer proxy: domain=9, majority_fail_at=5, p_spin=0.100, p_component_fail=8.909e-04, p_word_fail=3.947e-08, barrier=10.000, arrhenius=9.358e-14
conservation ledgers: max_commutator=0.000e+00, pulse_energy=8..8, domain_energy=8..8, pulse_count_conserved=True
```

The runner reports `PASS` for:

- 3D eikonal record field solves local routing equation;
- record carrier route is field-derived and local;
- carrier payload is generated by Bell transducer;
- Bob pre-delivery state is input-independent;
- field-delivered record restores Bob state;
- pointer code corrects bounded flips and erasures;
- thermal pointer proxy is stable below threshold;
- corrections commute with conservation ledgers;
- claim boundary stays state-only and not FTL.

## What This Closes Relative To The Prior Pass

The prior native apparatus artifact emitted local pulses along a finite path.
This pass derives that path from a local eikonal field and checks the field
equation across the whole 3D lattice. It also adds explicit record durability
and ledger gates.

The record stack is now:

```text
Bell stabilizer transducer
  -> redundant pointer code
  -> local eikonal record field
  -> fault/erasure-tolerant decode
  -> ledger-commuting Pauli correction
```

## Remaining Nature-Grade Blockers

The artifact narrows, but does not eliminate, the nature-grade blockers:

- the eikonal carrier is a discrete local carrier candidate, not a retained
  relativistic field equation;
- the thermodynamic pointer calculation is a stability proxy, not a bath,
  entropy-production, or irreversible detector derivation;
- the Bell-stabilizer transducer remains ideal/projective;
- conservation ledgers are algebraic for the candidate split, not derived for
  a physical apparatus;
- the Bell resource and retained readout/correction still rely on earlier
  bounded ideal components.

## Planning-Level Probe Outcome (not retained-theory impact)

Per the relabel block above, this note does not propagate retained-grade.
The probe-level observation is:

> Within the modeled native-apparatus + finite-proxy stack, a Bell record
> can be generated by the modeled native transducer, encoded as a
> redundant durable pointer, routed by a local 3D eikonal field, decoded
> after causal arrival, and used by Bob through a correction that
> commutes with base conservation ledgers.

This statement is **conditional on** the imported native apparatus /
transducer / readout / detector premises and the finite-proxy
durability and ledger checks above; it is **not** a retained closure
of the teleportation lane.
