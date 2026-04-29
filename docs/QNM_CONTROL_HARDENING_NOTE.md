# QNM Control Hardening Note

**Date:** 2026-04-05 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded control program only; no spectral claim and no quasi-normal-mode result asserted by this note.

This note is the narrowest review-safe way to keep the QNM lane alive on
`main` without overclaiming.

It does **not** promote a quasi-normal mode result.
It only freezes the control program that would be required before any QNM-style
escape-spectrum claim could be reviewed safely.

## Why this is still not promotable

The current retained `main` chain still lacks:

- a frozen `G = 0` spectral null
- a matched fixed-field control on the same geometry family
- a Born audit on the converged spectral family
- explicit exclusion of the Nyquist-adjacent artifact
- refinement / threshold stability under the same analysis rule

Without those pieces, the strongest branch-side spectral story remains
scientifically interesting but not review-safe.

## Narrow retained control program

The control program for the QNM lane is:

1. establish a `G = 0` null on the same lattice family
2. compare against a matched fixed-field control, not just self-consistent
   updates
3. audit Born on the converged field, not only step-local linearity
4. explicitly exclude the Nyquist-adjacent peak family
5. verify stability under refinement and threshold changes

If any one of these fails, the QNM lane stays exploratory.
If all five survive, the lane can be reopened as a narrow `G`-dependent
escape-spectrum candidate.

## Current verdict

**QNM remains a hardening target, not a retained spectral claim.**

The correct claim surface on `main` is only:

- the branch-side QNM story is interesting
- it is currently blocked by missing controls
- it should not be promoted until the control program above is frozen


## Audit boundary (2026-04-28)

The earlier Status line read "bounded control program only; no
`proposed_retained` spectral claim yet". The audit-lane parser caught
the literal `proposed_retained` token even though the sentence asserts
the opposite. The Status line has been rephrased.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The queued row is `proposed_retained` only because the status
> line contains that token in a negation; the note itself says this is
> a bounded control program only and not a `proposed_retained`
> spectral claim. Why this blocks: there is no runner, frozen null,
> matched control, Born audit, Nyquist exclusion, or escape-spectrum
> result registered against this note that would let the audit lane
> ratify a spectral claim.

## What this note does NOT claim

- A quasi-normal-mode spectral result.
- An escape-spectrum claim.
- That the bounded control program is itself a positive QNM result.

## What would close this lane (Path A future work)

Reinstating a QNM-style escape-spectrum claim would require a runner
that lands all of: a frozen null comparator, a matched control, a
Born-audit pass, a Nyquist exclusion check, and an escape-spectrum fit
that clears explicit pass thresholds.
