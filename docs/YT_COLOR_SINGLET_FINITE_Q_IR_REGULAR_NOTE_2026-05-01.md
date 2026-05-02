# YT Color-Singlet Finite-Q IR Regularity Note

**Date:** 2026-05-01  
**Status:** exact-support / color-singlet finite-q IR regularity  
**Runner:** `scripts/frontier_yt_color_singlet_finite_q_ir_regular.py`  
**Certificate:** `outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json`

## Purpose

The color-singlet zero-mode theorem removes the exact `q=0` gauge mode from
the scalar singlet denominator.  This note checks the remaining finite-`q`
massless IR behavior.

## Theorem

In four dimensions, after excluding the color-singlet-cancelled `q=0` mode,
the massless gauge kernel is locally integrable:

```text
d^4q / q^2 ~ q^3 dq / q^2 = q dq
```

so the finite-`q` region has a finite IR limit.

## Runner Result

```text
python3 scripts/frontier_yt_color_singlet_finite_q_ir_regular.py
# SUMMARY: PASS=6 FAIL=0
```

The runner verifies:

- the parent color-singlet zero-mode cancellation is loaded;
- the four-dimensional finite-`q` kernel is locally integrable;
- the zero-mode-removed finite lattice kernel has a stable `mu_IR -> 0` limit;
- the large-volume sequence is stable on the scan;
- keeping the zero mode would retain the IR divergence.

## Claim Boundary

This is exact support, not retained closure.  It removes the finite-`q` IR
divergence concern after color-singlet zero-mode cancellation.  It still does
not derive the full interacting scalar kernel, an isolated scalar pole, the
inverse-propagator derivative, source/projector normalization, finite-`N_c`
continuum control, or production FH/LSZ evidence.
