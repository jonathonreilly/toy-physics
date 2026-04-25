# CTC Fixed-Point Taxonomy Note

**Date:** 2026-04-25
**Status:** chronology-protection companion note; finite fixed-point classifier
**Companions:**
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md),
[`scripts/ctc_fixed_point_taxonomy_probe.py`](../scripts/ctc_fixed_point_taxonomy_probe.py)

## Role

This note classifies the finite fixed-point behavior imported by closed
timelike curve (CTC) consistency conditions. It does not add a time-machine
operation to the retained `Cl(3)/Z^3` chronology surface.

The retained chronology statement remains:

```text
CTC consistency is global fixed-point import, not retained local Cauchy
evolution or operational past signaling.
```

The taxonomy separates three cases that are often blurred:

1. no fixed point: inconsistent history;
2. unique fixed point: no controllable message remains;
3. multiple fixed points: an extra hidden selector is required.

## Minimal Bit-Map Model

Use one loop bit `b` and one late attempted message bit `m`. The CTC
consistency condition is:

```text
b = F_m(b)
```

Here `b` is the value at the early mouth of the loop, and `F_m(b)` is the value
returned to that mouth after one circuit, with any late operation encoded by
`m`.

On a retained retarded Cauchy surface, `b` would be freely specified as local
data and then evolved forward. In the CTC reading, `b` is not accepted merely
because it was locally chosen. It is accepted only if it is a fixed point of
the loop-wide map.

## Taxonomy

| class | loop map | fixed points | retained classification |
|---|---|---:|---|
| no fixed point | `F(b) = 1 - b` | none | inconsistent history; no admissible global solution |
| unique fixed point | `F_m(b) = 0` | `{0}` for every `m` | global solution is fixed; attempted message is not controllable |
| multiple fixed points | `F(b) = b` | `{0, 1}` | consistency alone underdetermines the history; hidden selector required |

### Class 1: No Fixed Point / Inconsistent History

The bit-flip loop gives:

```text
0 -> 1
1 -> 0
```

No bit equals its returned value. The CTC consistency rule rejects every local
choice for `b`. This is not a channel that sends a contradiction into the past;
it is an empty admissible-history set for that attempted loop.

### Class 2: Unique Fixed Point / No Controllable Message

The reset loop gives:

```text
0 -> 0
1 -> 0
```

The only fixed point is `b = 0`. In the probe, the late attempted message bit
`m` can be `0` or `1`, but the retained early loop bit remains `0`. The unique
global solution removes local freedom; it does not create a controllable
past-directed message.

### Class 3: Multiple Fixed Points / Hidden Selector Required

The identity loop gives:

```text
0 -> 0
1 -> 1
```

Both bits are globally consistent. Consistency alone therefore does not say
which history is realized. A rule such as "choose the lower fixed point,"
"choose the higher fixed point," "sample from a measure," or "use a hidden
state" is extra imported structure. Without that selector, the CTC constraint
is an admissible-set statement, not deterministic local evolution.

## Relation To The Retained Surface

The retained chronology surface assumes a single Hamiltonian clock,
codimension-1 local data, and retarded support semantics. CTC consistency
replaces that local-data problem with a global fixed-point problem.

The three classes above show why this replacement is not operational past
signaling:

- no fixed point removes the history instead of transmitting a message;
- one fixed point fixes the loop value globally instead of preserving a
  freely controlled message degree of freedom;
- several fixed points require an additional selector before a realized
  history is specified.

Thus a paradox-free CTC model may be mathematically definable, but the
paradox-free mechanism is precisely the imported fixed-point condition.

## Probe

Run:

```bash
python3 scripts/ctc_fixed_point_taxonomy_probe.py
```

Expected retained classification:

```text
CTC consistency is global fixed-point import, not retained local Cauchy
evolution or operational past signaling.
```
