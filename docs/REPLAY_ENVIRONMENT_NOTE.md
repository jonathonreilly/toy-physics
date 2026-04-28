# Replay Environment Note

**Date:** 2026-04-05 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** support / operational reproducibility documentation for numpy replay lanes; not a scientific claim and not a tier-ratified physics result.

This note exists to keep the retained numpy replays from depending on an
accidental interpreter choice.

## What happened on this machine

There are two relevant interpreters on path:

- Homebrew `python3`:
  - `/opt/homebrew/opt/python@3.13/bin/python3.13`
  - Python `3.13.5`
  - does **not** have `numpy`
- System `/usr/bin/python3`:
  - `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`
  - Python `3.9.6`
  - does have `numpy 2.0.2`

That means a replay can look broken if it is launched with the wrong
`python3`, even though the same script is fine under the system interpreter.

## Current convention

Retained numpy replay scripts on this machine should either:

- be launched with `/usr/bin/python3`, or
- call [`scripts/numpy_replay_bootstrap.py`](/Users/jonreilly/Projects/Physics/scripts/numpy_replay_bootstrap.py)
  before importing numpy-heavy modules.

The bridge wrappers for the wide-family `h = 0.125` lane now follow that
pattern.

## Why this matters

The scientific claims do not change here.
This is only about making replay behavior reproducible and less sensitive to
which interpreter happens to be first on `PATH`.

## Safe read

- Homebrew `python3` is not a safe default for retained numpy replays on this
  machine.
- `/usr/bin/python3` is the current stable replay interpreter.
- The repo now has a narrow bootstrap helper so future retained replay lanes
  can follow the same convention without repeating the environment debugging.

## Audit boundary (2026-04-28)

The earlier Status line called this a "narrow reproducibility note for
`proposed_retained` numpy replay lanes". The audit-lane parser caught
the literal token even though the sentence is a description of an
operational convention, not a scientific claim.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The row is parsed as `proposed_retained` from a note whose
> own content says the scientific claims do not change and records a
> local machine interpreter convention rather than a physics theorem.
> Why this blocks: a host-specific PATH/numpy observation without a
> runner, lockfile, or CI check cannot carry retained-claim status in
> the audit ledger, and retaining it would confuse operational
> reproducibility guidance with scientific evidence.

The note is operational documentation; it has been re-tiered to
`support`.

## What this note does NOT claim

- A scientific theorem, derivation, or physics result.
- A pinned replay environment contract enforced by CI.
- That the recorded machine convention generalizes beyond this host.

## What would close this lane (Path A future work)

If a tier-promotable replay environment contract is desired, it would
require a deterministic environment-check runner plus a pinned replay
environment contract enforced in CI (lockfile, hash, or version pin).
