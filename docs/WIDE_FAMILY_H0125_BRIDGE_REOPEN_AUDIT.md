# Wide-Family `h = 0.125` Bridge Reopen Audit

**Date:** 2026-04-05  
**Status:** reopened candidate, not retained on `main` yet

This note is a narrow audit of the Claude-side claim that the wider fixed
family behind the 3D dense `1/L^2 + h^2` lane can still complete the `h =
0.125` continuation test.

It is intentionally narrower than the earlier reduced-family `h = 0.125`
bridge note. The point here is not to relitigate the reduced audit-family
negative. The point is to isolate whether the wider fixed family deserves a
fresh, narrow reopen path.

## Existing artifacts

- [`scripts/lattice_3d_l2_numpy_h0125_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_bridge.py)
- [`scripts/lattice_3d_l2_numpy_h0125_only.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_only.py)
- [`scripts/lattice_3d_l2_wide.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide.py)
- [`docs/LATTICE_3D_L2_NUMPY_H0125_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_L2_NUMPY_H0125_BRIDGE_NOTE.md)
- [`docs/H2T_H0125_NARROW_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/H2T_H0125_NARROW_BRIDGE_NOTE.md)

## What the current local replay confirmed

I replayed the wide-family bridge under the retained system interpreter
because the default Homebrew `python3` on this machine does not ship with
`numpy`, while `/usr/bin/python3` does.

The replay wrappers now call
[`scripts/numpy_replay_bootstrap.py`](/Users/jonreilly/Projects/Physics/scripts/numpy_replay_bootstrap.py)
so future numpy-heavy retained replays land on the same interpreter
convention without depending on shell `PATH` order.

The local replay confirmed:

- the bridge script is runnable in a clean venv
- the family reproduces the same coarse rows as the retained note
- the replay reaches the `h = 0.25` row cleanly
- the wide-family setup is therefore not identical to the reduced-family
  dead-end audit

What it did **not** freeze in this session:

- a completed local `h = 0.125` row
- a new retained `main` note chain for the wide-family bridge

## Why this is still not retained

The decisive `h = 0.125` continuation row was not captured cleanly enough in
this session to promote the result, even after the interpreter mismatch was
removed and the replay reached the `h = 0.25` row cleanly.

The focused single-row replay makes the scale issue explicit:

- `h = 0.125`
- `117649` nodes
- `49` layers
- `155692848` edges

On this machine the row remained computationally heavy for several minutes and
did not complete inside the review window, so there is still no clean retained
`h = 0.125` row to freeze on `main`.

That means the only safe present-tense reading is:

- the wide-family bridge is a legitimate reopened candidate
- the reduced-family `h = 0.125` negative still stands separately
- the wider family has not yet been retained as a new positive on `main`

## Safe read

The strongest honest statement right now is:

- the Claude-side wide-family `h = 0.125` bridge is worth reopening
- it is not yet a retained `main` result
- the current artifact chain is insufficient to upgrade the official claim
  surface beyond "promising but unresolved"

## Reopen condition

This lane should only be promoted if a fresh retained replay captures:

- the `h = 0.125` row on the wider family
- clean Born on the completed rows
- the same-family weak-field observables without a silent geometry change
- a reproducible log file or note chain on `main`

Until then, this remains a narrow reopen candidate, not a retained bridge.
