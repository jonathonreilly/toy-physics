# y_t Bridge Operator Closure Proxy Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_operator_closure.py`

## Role

This note supports one narrow part of the unbounded `y_t` program:

> can broad electroweak-side operator freedom rescue a diffuse interacting
> bridge once the exact endpoint data are fixed?

If the answer were yes, then the missing bridge theorem would still be badly
under-determined. If the answer is no, the remaining theorem target is much
cleaner.

## Setup

The runner fixes the exact endpoint data:

- `g_3(v)` from the coupling-map theorem
- `g_3(M_Pl)` from the lattice coupling
- `y_t(M_Pl) = g_3(M_Pl)/sqrt(6)` from the Ward identity

It then compares two representative bridge shapes:

1. a **diffuse** bridge deformation
2. a **UV-localized** bridge deformation

For each shape, it scans a deliberately wide electroweak window:

- `g_1(v)` over `[0.30, 0.60]`
- `g_2(v)` over `[0.40, 0.90]`

So the question is not whether the EW inputs are exact. The question is whether
reasonable electroweak-side freedom can hide the bridge problem.

## Result

The answer is no.

- the best diffuse bridge still misses the accepted `y_t(v)=0.9176` target by
  more than `5%`
- the UV-localized bridge still lands within `1%`
- the EW scan span is too small to convert the diffuse bridge into a viable
  endpoint

So the accepted endpoint is not being “rescued” by broad electroweak operator
freedom.

## Meaning

This is a bounded operator-closure proxy:

- the dominant control of the bridge lives in the `g_3 / y_t` transport shape
- the remaining theorem target is not hidden in broad subleading EW-side
  deformations
- the bridge must therefore be closed at the dominant gauge/Yukawa level, with
  the already identified UV-localized structure

## What it does not prove

This note does **not** prove a final operator theorem.

It does not yet show:

- full uniqueness of the interacting bridge
- exact exclusion of every possible higher operator family
- disappearance of the current bounded surrogate envelope

It does show something narrower and still useful:

> the unresolved bridge is not plausibly being absorbed into wide EW-side
> operator ambiguity.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
substantive observation that the load-bearing comparison is an
external-target numerical comparator using hard-coded physical and
endpoint inputs (Ward boundary condition, accepted `y_t(v)` target, beta
function model, profile family) rather than a first-principles closure
from the axiom. The runner does compute the reported scan outcomes, but
the conditional status comes from imported endpoint data and a chosen
two-shape proxy family. The note already states above that this is a
bounded operator-closure proxy, not a final theorem.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
EW-window scan numerics or their bounded scope.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the EW-window
scan and Ward boundary condition rely on. It does not promote this note
or change the audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class premise the comparator uses.
- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the UV-localized bridge family used as the comparator's viable side.
- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the v boundary that anchors the accepted `y_t(v)` target.
- [YT_EW_COUPLING_BRIDGE_NOTE.md](YT_EW_COUPLING_BRIDGE_NOTE.md)
  for the EW-coupling bridge inputs and SM-RGE surrogate the scan reuses.
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
  for the QFP-stability bound on the EW-window dependence.
