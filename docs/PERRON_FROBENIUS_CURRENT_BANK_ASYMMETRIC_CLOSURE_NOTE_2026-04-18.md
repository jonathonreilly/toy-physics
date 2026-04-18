# Perron-Frobenius Current-Bank Asymmetric Closure

**Date:** 2026-04-18  
**Status:** exact science-only consequence theorem separating present-bank
negative closure from future-theory reopening asymmetry; on the current bank
no live positive route remains, but Wilson is still the main plausible future
reopening lever while PMNS-native production and plaquette scalar closure
remain independent blockers  
**Script:** `scripts/frontier_perron_frobenius_current_bank_asymmetric_closure_2026_04_18.py`

## Question

After the Wilson dependency audit and the new minimal frontier certificates,
what is the exact asymmetry of the current PF branch?

## Answer

The current bank is fully closed negatively.

But the future-theory reopening map is still asymmetric:

- there is no live positive route remaining on the present bank;
- under stronger science, Wilson is still the main plausible reopening lever;
- PMNS-native production and plaquette scalar closure remain independent
  blockers either way.

So weakening Wilson cannot make the branch more open.

It can only remove the most plausible future reopening lever, while the other
two blockers remain.

## Setup

From
[PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md](./PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md):

- the current branch reduces to three minimal frontier certificates,
- after full current-bank closure none of them is presently realized
  positively,
- while Wilson remains the main plausible future reopening lever and the
  PMNS-native / plaquette certificates remain current-bank blockers.

## Theorem 1: exact asymmetric closure of the current PF branch

On the current bank:

1. no live positive PF route remains;
2. the PMNS-native production certificate remains unresolved independently;
3. the plaquette scalar certificate remains unresolved independently.

Therefore the branch is asymmetrically structured in the following precise
sense:

- current-bank negative closure does not depend on Wilson alone,
- but any plausible future positive reopening still depends primarily on
  stronger Wilson science.

## Corollary 1: Wilson weakening makes the branch more clearly negative, not more open

If Wilson weakens, the current bank loses its main plausible future reopening
lever.

But the PMNS-native and plaquette blockers remain.

So the branch becomes more clearly negative, not more open.

## What this closes

- one exact consequence surface of the Wilson audit and frontier-certificate
  work
- one reviewer-facing statement of why Wilson robustness still matters
  asymmetrically even after full current-bank closure

## What this does not close

- a Wilson robustness theorem
- a positive global PF selector theorem
- the PMNS-native production certificate
- the plaquette scalar certificate

## Why this matters

This is the cleanest exact answer yet to the “does Wilson reopening matter?”
question.

The branch can now say:

- yes, Wilson matters for the strongest plausible **future positive** route,
- no, Wilson is not the whole branch,
- and weakening Wilson does not reopen the program positively.

## Command

```bash
python3 scripts/frontier_perron_frobenius_current_bank_asymmetric_closure_2026_04_18.py
```
