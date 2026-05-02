# Observable-Principle From-Axiom Note — Status Correction Audit

**Date:** 2026-05-02
**Status:** demotion / status correction packet for
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
which has audit verdict `audited_conditional` with td=294, lbs=26.70.
**Primary runner:** `scripts/frontier_observable_principle_audit.py`
**Authority role:** dep-declaration / status-correction packet for
parent's load-bearing assumption chain.

## 0. Audit context

The parent note `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` proves that on
the exact minimal hierarchy block, the framework-native scalar observable
generator is `W[J] = log |det(D+J)| - log |det D|`, forced by:

1. exact Grassmann factorization
2. scalar additivity on independent subsystems
3. CPT-even bosonic insensitivity to the fermionic phase
4. minimal regularity (continuity)
5. normalization choice

The audit verdict flagged: *"the note proves the log|det(D+J)| source-response
result only after adding scalar additivity, CPT-even phase blindness,
continuity, and normalization assumptions, and its electroweak-scale
consequence imports the current hierarchy baseline rather than deriving
that normalization here."*

So the load-bearing chain has 4 admitted bridge assumptions plus a
hierarchy-baseline import. The verdict's repair target: derive these
assumptions or accept them as admitted-with-narrow-non-derivation-role.

## 1. The 4+1 admitted assumptions

| # | Assumption | Class | Derivation status |
|---|---|---|---|
| 1 | scalar additivity on independent subsystems | physical principle | admitted; standard QFT convention for scalar bosonic observables |
| 2 | CPT-even phase blindness | physical principle | admitted; CPT_EXACT_NOTE.md provides retained CPT but blindness is a separate scheme choice |
| 3 | continuity (minimal regularity) | mathematical regularity | admitted; standard functional equation regularity |
| 4 | normalization choice | gauge-fixing | admitted; trivial up to overall constant |
| 5 | electroweak hierarchy baseline import | external hierarchy values | admitted standard package |

## 2. Seven retained-proposal certificate criteria

| # | Criterion | Pass? |
|---|---|---|
| 1 | `proposal_allowed: true` | **NO** |
| 2 | No open imports | **NO** (5 admitted assumptions/imports) |
| 3 | No load-bearing observed/fitted/admitted unit conventions | **PARTIAL** (4 admitted physical principles + 1 admitted hierarchy baseline) |
| 4 | Every dep retained | **N/A** (deps=[] in ledger; analogous dep-declaration issue to cycle 7) |
| 5 | Runner checks dep classes | **YES** (the runner verifies the structural argument) |
| 6 | Review-loop disposition `pass` | **PENDING** |
| 7 | PR body says independent audit required | **YES** |

**Result:** Criteria 1, 2, 4 fail; Criterion 3 partial. Honest tier:
**bounded support theorem** modulo 5 admitted bridge assumptions.

## 3. Recommended status correction

```yaml
# observable_principle_from_axiom_note (parent)
current_status: bounded support theorem  # was: unknown
audit ledger verdict remains conditional; no review-side change
effective_status: audited_conditional      # unchanged
proposal_allowed: false
proposal_allowed_reason: |
  The W = log|det(D+J)| derivation rests on 4 admitted physical-principle
  bridge assumptions (scalar additivity, CPT-even phase blindness,
  continuity, normalization) + 1 admitted hierarchy baseline import.
  These cannot be reduced without further derivation or governance
  classification under Criterion 3.
```

## 4. Path to retention

| Bridge assumption | Retirement path |
|---|---|
| (1) scalar additivity | could be derived from physical-principle of independent-subsystem locality, but currently admitted |
| (2) CPT-even phase blindness | could lift from CPT_EXACT_NOTE retained primitive + a separate "scalar bosonic insensitivity to phase" theorem |
| (3) continuity | mathematical regularity; could be proved as a corollary of the framework's smoothness assumptions |
| (4) normalization | trivial up to overall constant; could be absorbed into convention reclassification |
| (5) hierarchy baseline | depends on hierarchy lane retention |

## 5. What this packet closes

- Identifies the 5 admitted bridge assumptions explicitly
- Recommends honest demotion from `unknown` to `bounded support theorem`
- Documents the path to retention via 5 bridge-assumption retirements

## 6. What this packet does NOT close

- Any of the 5 bridge assumptions themselves
- The retention status of dependent claims downstream

## 7. Cross-references

- Parent: [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- Sister: `CPT_EXACT_NOTE.md` (retained, supplies CPT but not phase blindness)
