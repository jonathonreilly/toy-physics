# Replay Environment Note

**Date:** 2026-04-05
**Status:** narrow reproducibility note for proposed_retained numpy replay lanes

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
