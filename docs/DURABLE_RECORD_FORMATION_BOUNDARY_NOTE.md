# Durable Record Formation Boundary Note

**Date:** 2026-04-25
**Status:** chronology-protection support note; sufficient finite record model,
not a full measurement derivation
**Probe:** `scripts/durable_record_formation_boundary_probe.py`
**Companions:**
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[U_MINUS_T_VS_PAST_SIGNALING_NOTE.md](U_MINUS_T_VS_PAST_SIGNALING_NOTE.md),
[CHRONOLOGY_OPERATOR_ALGEBRA_BOUNDARY_NOTE.md](CHRONOLOGY_OPERATOR_ALGEBRA_BOUNDARY_NOTE.md)

## Role

The operational no-past-signaling note uses durable records as physical degrees
of freedom. This note does not close the full measurement problem. It supplies
a bounded finite model showing what the chronology lane needs from record
formation:

- a record bit is copied into multiple local carriers;
- later operations on the original system do not remove those carriers;
- partial erasure leaves witnesses;
- redundant carriers allow stable readout under bounded damage.

That is sufficient for the chronology boundary:

```text
once a record exists as physical carriers, a later operation must include those
carriers in the state audit; it cannot omit them and call the past edited.
```

## Finite Record Model

Start with a system bit `S` and a visible record bit `R`. Record formation is
modeled by reversible copy gates:

```text
S -> R,
R -> E_0, E_1, ..., E_(k-1).
```

The environment carriers `E_i` are the durable copy sector. The model is still
globally reversible. Durability here means redundancy and persistence of
physical witnesses, not fundamental irreversibility.

The finite readout rule is majority decoding over the environment copies. For
odd `k`, the record is stable against up to `(k-1)/2` flipped copies.

## Probe Result

Run:

```bash
python3 -m py_compile scripts/durable_record_formation_boundary_probe.py
python3 scripts/durable_record_formation_boundary_probe.py
```

The probe checks:

- fanout writes all record carriers;
- later system flips do not change already-written carriers;
- majority decoding with `k=5` survives all `0`, `1`, and `2` flip patterns;
- majority decoding fails for some `3`-flip patterns, making the durability
  threshold explicit;
- erasing any proper subset of carriers leaves at least one witness;
- erasing every witness is full carrier erasure, not a past-directed signal.

## Boundary

This support note is intentionally not stronger than it should be.

- It does not derive the Born rule or measurement collapse.
- It does not derive why macroscopic records form in the full framework.
- It does not claim records are impossible to erase in the future.
- It does not replace the broader measurement/record lane.

It only gives the chronology lane a precise finite sufficient condition: once
record carriers exist, they are part of the state. Reversing or erasing the
past record requires acting on those carriers too.

## Safe Language

Use:

- "sufficient finite record-carrier model"
- "partial erasure leaves witnesses"
- "durability by redundant physical copies"
- "not a full measurement derivation"

Avoid:

- "measurement problem solved"
- "records are fundamentally irreversible"
- "future erasure is impossible"
- "record formation alone proves all chronology claims"
