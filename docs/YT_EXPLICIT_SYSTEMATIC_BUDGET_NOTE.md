# `y_t` Residual-Budget and Bridge Cross-Check Note

**Date:** 2026-04-17
**Status:** support note for the current YT authority surface
**Primary runner:** `scripts/frontier_yt_explicit_systematic_budget.py`

## Role

This note is no longer the package authority for the older intermediate YT-lane
classification that sat between bounded and fully retained.

Its current role is narrower:

1. record the residual budget on the Schur-coarse-bridge cross-check path
2. distinguish that bridge-path budget from the current Ward-primary
   standard-method residual budget
3. preserve the exact-bridge tail accounting as useful support rather than as
   the load-bearing package qualifier on the live YT lane

## Current package posture

The live YT authority now reads:

> `y_t(v)` and `m_t(pole)` are **derived quantitative rows** whose primary
> precision caveat is carried by standard lattice-to-continuum matching and
> standard SM running on the Ward-primary route.

So the present note is about the **bridge cross-check path**, not the live
primary classification.

## Bridge-path budget

On the Schur-coarse-bridge route, the residual budget is still carried by two
named exact-bridge tails:

- higher-order local tail:
  `7.123842e-3 = 0.7123842%`
- nonlocal tail:
  `5.023669e-3 = 0.5023669%` conservative
  or
  `4.262215e-4 = 0.04262215%` support-tight on the current viable family

Two further diagnostics remain negligible or closed:

- selector-anchor mismatch:
  `5.44897e-6` relative
- structural class residual:
  closed on the current tested scale on the tested locality tube

That leaves the bridge-path endpoint budget at:

- conservative:
  `1.2147511%`
- support-tight:
  `0.75500635%`

around the current central value `y_t(v) = 0.9176`.

## How this budget is used now

This budget is no longer the package's load-bearing qualifier on the live
Ward-primary YT lane. It now serves three narrower purposes:

1. it quantifies the independent Schur-bridge cross-check path
2. it documents that the bridge route remains controlled and scientifically
   meaningful
3. it provides a comparison surface against the Ward-primary standard-method
   residual budget

## Comparison with the live primary path

The current package carries two distinct precision stories:

- **Ward-primary path:**
  standard lattice 1-loop matching at the `M_Pl` interface plus standard SM
  RGE truncation; current budget of order `~1.95%`
- **Schur-bridge cross-check path:**
  intrinsic bridge-path residual budget
  `1.2147511%` conservative / `0.75500635%` support-tight

The point of the current package update is that the second budget remains
useful and real, but it is no longer the reason the primary lane is classified
the way it is.

## Propagation on the bridge path

If one reads the Schur-bridge route by itself, the same bridge budget
propagates directly to the top-mass readout:

- `m_t(pole, 2-loop) = 172.57 GeV`
  with bridge-path budget
  `±2.097 GeV` conservative,
  `±1.303 GeV` support-tight
- `m_t(pole, 3-loop) = 173.10 GeV`
  with bridge-path budget
  `±2.103 GeV` conservative,
  `±1.307 GeV` support-tight

That propagation remains a valid cross-check statement.

## Honest boundary

This note does **not** claim:

- that the live package still needs the old bridge-budget classification on the
  primary YT lane
- that the bridge-path budget should be discarded
- that the Ward-primary path has become fully retained from `M_Pl` to `v`

What it does claim is narrower:

> the exact-bridge tail accounting remains valid and should now be read as the
> residual budget of the independent Schur-bridge cross-check path.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `yt_bridge_higher_order_corrections_note` / `YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md`
  (see-also cross-reference, not a load-bearing dependency — backticked
  to break cycle-0006 in the citation graph. This budget note records
  the Schur-bridge cross-check tail amplitudes that the
  higher-order-corrections note's amplitude-tube hierarchy result
  consumes; the dependency arrow runs from the corrections note back
  to this budget surface, not vice versa.)
- `yt_bridge_nonlocal_corrections_note` / `YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md`
  (see-also cross-reference, not a load-bearing dependency — backticked
  to break the sibling 5-cycle through `yt_bridge_nonlocal_corrections`
  that survived the cycle-0006 break in the citation graph. As above,
  the dependency arrow runs from the corrections note back to this
  budget surface, not vice versa: this budget records the bridge-tail
  amplitude that the corrections note's runner-based result consumes.)
- [yt_exact_schur_normal_form_uniqueness_note](YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md)

<!--
Cycle-break (2026-05-06): the back-edge to
`YT_ZERO_IMPORT_AUTHORITY_NOTE.md` was removed from this section because
the authority note already cites this budget note as a forward authority
(see its sibling list under "Use this note together with"). Retaining the
bookkeeping back-link as a Markdown citation produced cycle-0003 in the
citation graph (`docs/audit/data/cycle_inventory.json`). File pointer:
`YT_ZERO_IMPORT_AUTHORITY_NOTE.md`.
-->
