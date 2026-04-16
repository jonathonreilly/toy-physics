# Historical YT Bound Reduction Options

**Date:** 2026-04-15
**Branch:** `codex/yt-unbounded-main-package-2026-04-15`
**Purpose:** historical planning note listing routes that were considered while
the live `y_t` lane was being promoted to `derived with explicit systematic`

## Executive summary

The current lane is already much tighter than a generic bounded result. The
remaining problem is not the central value; it is the status of the
transport/bridge error above `v`.

There are three realistic reduction paths:

1. **Prove a smaller correction budget for the exact interacting bridge**
2. **Replace the backward-Ward surrogate with a package-native bridge**
3. **Keep the surrogate but convert the residual into an explicit systematic**

The first two can potentially shrink or eliminate the current
`1.2147511%` conservative / `0.75500635%` support-tight bound. The third is
now effectively achieved on the current package: the residual is explicit enough to
support `derived with explicit systematic`.

## Current live evidence

The branch already has the following support stack:

- exact lattice-scale ratio `y_t / g_s = 1 / sqrt(6)`
- physical endpoint selection at `v`
- QFP insensitivity at the few-percent level
- a strong one-shot gauge-crossover companion no-go
- a constructive UV-localized bridge class
- a dominant bridge action invariant
- a rearrangement principle forcing UV localization
- a two-moment closure on the viable UV window
- a conditional variational selector
- a leading-order Hessian selector explanation

That stack is enough to say the lane is constrained and internally coherent.
It is not enough to remove the residual systematic.

## Route 1: shrink the bound by proving a smaller bridge correction

### What would have to be true

- the exact interacting lattice bridge is shown to lie in the forced
  UV-localized class, not just in the scanned proxy families
- the higher-order and nonlocal corrections above the local Hessian selector
  are explicitly bounded
- the resulting bound is smaller than the current
  `1.2147511% / 0.75500635%` bridge envelope

### What this would buy

- the status could move from the current explicit bounded budget to a narrower
  bounded status
- the lane would still be bounded, but with a smaller and more precise error
  envelope

### What blocks it today

- the current bridge stack is still proxy support, not a full microscopic
  theorem
- the branch does not yet control the higher-order / nonlocal corrections
  tightly enough to quote a smaller validated bound

## Route 2: replace the surrogate with a package-native bridge

### What would have to be true

- the exact interacting lattice bridge supplies the low-energy `y_t(v)` endpoint
  directly
- the transport from the lattice boundary to `v` is no longer carried by the
  backward-Ward / QFP surrogate
- the bridge theorem is package-native, not an import-allowed interpolation

### What this would buy

- this is the cleanest route to `derived with explicit systematic`
- if the only remaining uncertainty is a normal numerical or truncation error,
  the lane can be stated as a derived central value with a declared systematic

### What blocks it today

- no branch-native proof yet shows the exact interacting bridge itself is the
  transport law
- direct low-energy lattice bypass on accessible lattices still appears
  infeasible

## Route 3: keep the surrogate but make the systematic explicit

### What would have to be true

- the backward-Ward / QFP transport remains the practical bridge
- but the residual uncertainty is decomposed into explicit pieces
  (for example: truncation, finite-volume, matching, or controlled nonlocal
  correction terms)
- those pieces are individually bounded or computed on the branch
- the package wording is updated so the claim is a derived central value with an
  explicit systematic, not a soft bounded caveat

### What this would buy

- this is the most conservative route to a status change
- it does not require removing every approximation, only accounting for it
  cleanly

### What still limits it

- the explicit systematic is not yet below the paper bar
- the exact-bridge tails are not yet driven to zero

## Practical recommendation

The strongest remaining lever is still the microscopic bridge correction
control:

1. prove the exact interacting bridge is forced into the UV-localized class
2. quantify the higher-order / nonlocal corrections above the local Hessian
   selector
3. if the correction budget is small enough, reclassify to a narrower bounded
   status
4. if the correction budget becomes explicit and fully enumerated, reclassify
   to `derived with explicit systematic`

That path is better than trying to squeeze more value out of the existing
surrogate alone.

## Status transition matrix

| Current status | Required next fact | Likely new status |
|---|---|---|
| `bounded (1.2147511% / 0.75500635%)` | smaller validated correction budget from the exact interacting bridge | narrower bounded status |
| `bounded (1.2147511% / 0.75500635%)` | package-native bridge replaces the surrogate transport law | `derived` or `derived with explicit systematic` |
| `bounded (1.2147511% / 0.75500635%)` | residual uncertainty fully enumerated as explicit truncation / matching / finite-volume systematics | `derived with explicit systematic` |

## What not to rely on

These are useful diagnostics, but not by themselves status-changing:

- more Higgs work
- more EW normalization work
- more profile scans inside the same proxy family
- more direct one-scale lattice Yukawa measurements at the cutoff

They can refine the picture, but they do not by themselves remove the transport
problem.

## Bottom line

The branch is now at the point where further progress has to come from a real
bridge-correction theorem or from a tighter explicit systematic budget.

Route 3 now supports a live status move to `derived with explicit systematic`.
Further progress means tightening or collapsing that systematic, not creating it
from scratch.
