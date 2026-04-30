# Shapiro Scaling Note

**Date:** 2026-04-08  
**Status:** support - structural or confirmatory support note

## Pointer

The canonical scaling replay is now the direct replay note:

- [`docs/SHAPIRO_SCALING_DIRECT_REPLAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_SCALING_DIRECT_REPLAY_NOTE.md)

## Why

The earlier scaling lane was anchored on a reconstruction chain and commit
`1730b52`. The direct replay replaces that with frozen repo data for:

- the `s` law from the experimental card
- the `b` law from the experimental card
- the `k` law from the experimental card
- the exact zero controls from the experimental card and portable delay log

## Closure Read

The scaling lane no longer needs to stay active as a reconstruction-only
artifact chain. The direct replay keeps the retained values explicit and
separates the exact controls from the monotone tail laws.
