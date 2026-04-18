# Perron-Frobenius Current-Bank Asymmetric Closure

**Date:** 2026-04-18  
**Status:** exact science-only consequence theorem on the current bank; Wilson
is the only positive reopening lever, while PMNS-native production and
plaquette scalar closure remain independent current-bank blockers  
**Script:** `scripts/frontier_perron_frobenius_current_bank_asymmetric_closure_2026_04_18.py`

## Question

After the Wilson dependency audit and the new minimal frontier certificates,
what is the exact asymmetry of the current PF branch?

## Answer

The current bank is asymmetrically closed.

- There is exactly one remaining **positive reopening lever**:
  the Wilson local certificate.
- There are at least two remaining **independent current-bank blockers**:
  the PMNS-native production certificate and the plaquette scalar certificate.

So weakening Wilson cannot make the branch more open.

It can only remove the main positive reopening lever, while the other two
blockers remain.

## Setup

From
[PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md](./PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md):

- the current branch reduces to three minimal frontier certificates,
- only the Wilson certificate is currently a positive reopening lever,
- while the PMNS-native and plaquette certificates remain current-bank
  blockers.

## Theorem 1: exact asymmetric closure of the current PF branch

On the current bank:

1. the Wilson local certificate is the only positive reopening lever;
2. the PMNS-native production certificate remains unresolved independently;
3. the plaquette scalar certificate remains unresolved independently.

Therefore the branch is asymmetrically closed:

- positive reopening depends primarily on Wilson,
- negative closure does not.

## Corollary 1: Wilson weakening makes the branch more clearly negative, not more open

If Wilson weakens, the current bank loses its main positive reopening lever.

But the PMNS-native and plaquette blockers remain.

So the branch becomes more clearly negative, not more open.

## What this closes

- one exact consequence surface of the Wilson audit and frontier-certificate
  work
- one reviewer-facing statement of why Wilson robustness matters asymmetrically

## What this does not close

- a Wilson robustness theorem
- a positive global PF selector theorem
- the PMNS-native production certificate
- the plaquette scalar certificate

## Why this matters

This is the cleanest exact answer yet to the “does Wilson reopening matter?”
question.

The branch can now say:

- yes, Wilson matters for the **positive** route,
- no, Wilson is not the whole branch,
- and weakening Wilson does not reopen the program positively.

## Command

```bash
python3 scripts/frontier_perron_frobenius_current_bank_asymmetric_closure_2026_04_18.py
```
