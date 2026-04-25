# Postselection No-Signaling Audit

**Date:** 2026-04-25
**Status:** chronology-protection companion audit; probability-table witness
**Companions:**
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md),
[U_MINUS_T_VS_PAST_SIGNALING_NOTE.md](U_MINUS_T_VS_PAST_SIGNALING_NOTE.md),
[`scripts/postselection_ctc_nonlinearity_probe.py`](../scripts/postselection_ctc_nonlinearity_probe.py)

## Purpose

This audit isolates the postselection ambiguity:

```text
P(earlier record | later outcome selected) can shift
```

does not imply

```text
the later selection edited the earlier durable record in the same run.
```

The retained chronology claim remains:

> On the retained single-clock, local-data framework surface, the theory admits
> reversible reconstruction but no operational signaling to an earlier durable
> record.

## Probability-Table Witness

The companion script uses an exact finite table. The earlier durable record
`R(t0)` has unconditioned distribution:

```text
P(R=0) = 1/2
P(R=1) = 1/2
```

The later outcome `L(t1)` is correlated with the record:

```text
P(L=selected | R=0) = 1/5
P(L=selected | R=1) = 4/5
```

So the joint table is:

| earlier durable record | later outcome | probability |
|---:|---|---:|
| `R=0` | `selected` | `1/10` |
| `R=0` | `discarded` | `2/5` |
| `R=1` | `selected` | `2/5` |
| `R=1` | `discarded` | `1/10` |

Conditioning on the later selected outcome gives:

```text
P(R=1 | L=selected) = 4/5
```

That is a real retrodictive shift from the prior value `P(R=1) = 1/2`.
But the unconditioned earlier marginal is unchanged when both later outcomes
are retained:

```text
P(R=1)
  = P(L=selected)  P(R=1 | L=selected)
  + P(L=discarded) P(R=1 | L=discarded)
  = (1/2)(4/5) + (1/2)(1/5)
  = 1/2.
```

The discarded subensemble still contains the run classes with raw probabilities
`2/5` for `R=0` and `1/10` for `R=1`. They are absent from the selected report;
they are not rewritten.

## Operational Audit

The script checks three separate claims:

- the selected conditional distribution differs from the unconditioned earlier
  record distribution;
- the raw selected rows plus the raw discarded rows exactly reconstruct the
  original joint table;
- conditioning preserves the selected run-class record identities and leaves
  the discarded run classes present and unedited.

This is why the safe language is:

```text
postselection changes the selected subensemble statistics
```

not:

```text
postselection changed what happened in discarded runs
```

## Classification

Ordinary postselection is a conditional-subensemble operation. If the selected
later outcome is instead imposed as a deterministic rule defining which
histories are allowed, the construction has imported a final-boundary
condition. Either way, it is not an operational channel that lets a later
agent edit an already-realized durable record at `t0`.

Retained classification:

```text
postselection -> conditional subensemble/final-boundary import
operational past signaling -> no
```

## Relation To The Nonlinearity Probe

[`scripts/postselection_ctc_nonlinearity_probe.py`](../scripts/postselection_ctc_nonlinearity_probe.py)
addresses a different layer. It shows that a normalized postselected
effective map has an input-dependent denominator and therefore fails
convex-linearity. That is the dynamical-map reason P-CTC-style normalized
postselection is outside ordinary linear CPTP evolution.

This audit is the ensemble-bookkeeping companion. It shows that even in a
classical finite probability table, a later filter can make
`P(past | future selected)` differ from `P(past)` without any same-run past
editing. The two probes therefore cover both common overclaims:

- the nonlinearity probe blocks treating normalized postselection as an
  ordinary retained local channel;
- this audit blocks treating a conditional probability shift as a physical
  rewrite of earlier durable records or discarded runs.

## Command

```bash
python3 -m py_compile scripts/postselection_no_signaling_audit.py
python3 scripts/postselection_no_signaling_audit.py
```
