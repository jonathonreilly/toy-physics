# Wide-Family `h = 0.125` Bridge Reopen Audit

**Date:** 2026-04-05  
**Status:** reopened candidate only for a truly wider family; the current fixed
bridge family now resolves as bounded negative for weak-field closure

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

What the focused decision harness added afterward:

- a completed local `h = 0.125` row on the same fixed bridge family
- Born `6.59e-15`
- `k = 0` clean
- gravity `+0.029856` (`TOWARD`)
- `F~M alpha = 0.501`

## Why this is still not retained

The focused single-row replay makes the scale issue explicit:

- `h = 0.125`
- `117649` nodes
- `49` layers
- `276710448` dense transition entries in the focused replay

On this machine the original edge-list path remained computationally heavy,
but the focused dense-matrix replay now completes. That completion sharpens
the result rather than promoting it:

- the fixed bridge family no longer looks unresolved at `h = 0.125`
- it now looks like a completed same-family row that still fails the
  weak-field `F~M \approx 1` bridge criterion

That means the only safe present-tense reading is:

- the reduced-family `h = 0.125` negative still stands separately
- the current fixed bridge family now also completes without closing the
  weak-field mass-law gap
- the only remaining reopen candidate is a genuinely wider `h = 0.125`
  family, not the current fixed bridge family

## Safe read

The strongest honest statement right now is:

- the Claude-side `h = 0.125` story was worth reopening
- the current fixed bridge family now resolves as a bounded negative for
  weak-field closure
- a wider-family `h = 0.125` replay remains the only live reopen version

## Reopen condition

This lane should only be promoted if a fresh retained replay captures:

- the `h = 0.125` row on a genuinely wider family
- clean Born on the completed rows
- the same-family weak-field observables without a silent geometry change
- a reproducible log file or note chain on `main`

Until then, the fixed bridge family should be treated as resolved and the
reopen candidate should be interpreted narrowly as the wider-family version
only.
