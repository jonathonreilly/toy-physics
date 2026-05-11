# DM Full Closure Same-Surface Thermal Bounding Theorem

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-17  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_bounding_theorem.py`

## Question

Can the same-surface DM thermal layer now be promoted from support status to a
rigorous evaluation/bounding result?

## Answer

Yes.

The thermal layer is now closed at theorem-grade **evaluation/bounding**
strength by combining:

1. the exact continuum integral representation on the retained `x_f = 25`
   slice,
2. the exact monotonicity theorem in the selected coupling `alpha`,
3. the exact positive-series / exact tail enclosure machinery.

## Certified Current-Bank Output

On the exact current-bank same-surface endpoints:

- `alpha_lo = 0.090667836017286`
- `alpha_hi = 0.092264992618360`

the exact thermal ratio is enclosed rigorously by:

- `R(alpha_lo) in [5.442019867867, 5.442019867931]`
- `R(alpha_hi) in [5.482855571890, 5.482855571936]`

Therefore, after fixing `Omega_b` from `eta_obs`,

- `Omega_DM(alpha_lo) in [0.267709052538, 0.267709052541]`
- `Omega_DM(alpha_hi) in [0.269717881594, 0.269717881596]`

and the current-bank no-go is rigorous:

- the current bank carries distinct exact endpoint images,
- the target lies between them,
- but the current bank still does not furnish a selector law.

## Certified One-Scalar DM-Family Root

On the one-scalar same-surface admitted family

`alpha(sigma) = alpha_lo + sigma (alpha_hi - alpha_lo)`,

exact monotonicity plus the certified endpoint/bisection enclosures force a
unique root interval:

- `sigma in [0.145076095756643, 0.145078095756643]`
- equivalently
  `alpha in [0.090899545261282, 0.090899548455595]`

with a narrow certified width produced by the theorem runner.

So the DM-side admitted family is no longer only numerically supported; it has
a certified unique root interval on the thermal layer itself.

## Honest Status

- current-bank selector closure: still **no**
- thermal layer: now **rigorous evaluation/bounding**, not just support
- admitted one-scalar DM-side family: now has a **certified unique root interval**
- remaining flagship question:
  whether the current exact bank itself can be made to select a value, or
  whether the DM-side one-scalar family must remain an admitted extension

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_bounding_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by prior 2026-05-05 audit feedback for
`dm_full_closure_same_surface_thermal_bounding_theorem_note_2026-04-17`.
The prior feedback identified the imported certification routines as
the load-bearing boundary: this packet does not include the derivations
or source for the continuum integral, monotonicity theorem, and
positive-series / tail enclosures, while the visible runner delegates
those steps to external common modules and then performs algebraic /
bracketing checks on their returned values. This addendum does not
promote the row or change the claim scope, which remains the bounded
thermal-layer evaluation theorem on the certified endpoint enclosures
and the one-scalar root interval on the admitted DM-side family.
Independent audit owns any current verdict or effective status after
this source change.

One-hop authorities cited:

- [`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_INTEGRAL_REPRESENTATION_THEOREM_NOTE_2026-04-16.md`](DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_INTEGRAL_REPRESENTATION_THEOREM_NOTE_2026-04-16.md)
  — audit row:
  `dm_full_closure_same_surface_thermal_integral_representation_theorem_note_2026-04-16`.
  Upstream authority for the exact continuum integral representation
  on the retained `x_f = 25` slice underlying ingredient (1) of the
  three-step combination.
- [`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_MONOTONICITY_THEOREM_NOTE_2026-04-17.md`](DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_MONOTONICITY_THEOREM_NOTE_2026-04-17.md)
  — audit row:
  `dm_full_closure_same_surface_thermal_monotonicity_theorem_note_2026-04-17`.
  Upstream authority for the exact monotonicity theorem in the
  selected coupling `alpha` underlying ingredient (2) of the
  three-step combination and the unique-root-interval consequence on
  the admitted family.
- [`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_SERIES_TAIL_SUPPORT_NOTE_2026-04-17.md`](DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_SERIES_TAIL_SUPPORT_NOTE_2026-04-17.md)
  — audit row:
  `dm_full_closure_same_surface_thermal_series_tail_support_note_2026-04-17`.
  Upstream authority for the exact positive-series / exact tail
  enclosure machinery underlying ingredient (3) of the three-step
  combination.
- `DM_FULL_CLOSURE_SAME_SURFACE_NUMERATOR_SELECTOR_BOUNDARY_NOTE_2026-04-16.md`
  — audit row:
  `dm_full_closure_same_surface_numerator_selector_boundary_note_2026-04-16`.
  Sibling boundary reference for the current-bank no_go that this
  bounded theorem explicitly preserves in its "Honest Status" section.
- `DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_SELECTOR_SENSITIVITY_BOUNDARY_NOTE_2026-04-16.md`
  — audit row:
  `dm_full_closure_same_surface_thermal_selector_sensitivity_boundary_note_2026-04-16`.
  Sibling boundary reference for the sensitivity boundary that frames
  the admitted-family root interval against the no-current-bank-selector
  conclusion.

Open upstream gaps registered for independent audit:

- the continuum integral representation authority;
- the monotonicity authority;
- the positive-series / tail-enclosure authority;
- the sibling current-bank no_go boundary.

The runner-checked content of this note (the certified
`R(alpha_lo)`, `R(alpha_hi)` enclosures; the certified
`Omega_DM(alpha_lo)`, `Omega_DM(alpha_hi)` intervals; and the
certified one-scalar root interval
`sigma in [0.145076..., 0.145078...]` /
`alpha in [0.090899545..., 0.090899548...]`) is verified composition
over the cited authorities' returned values and the algebraic /
bracketing checks performed in the local runner. The cite chain is
what supplies the upstream certification routines (continuum integral,
monotonicity, positive-series / tail enclosure) whose retained
source chain remains pending for independent audit.

## Honest auditor read

Prior audit feedback observed that the restricted packet does not
include the load-bearing derivations or source for the imported
certification routines and that the visible runner delegates those
steps to external common modules. The cite-chain repair above wires the
three ingredient-level upstream authorities, the sibling no_go, and the
sensitivity boundary as the explicit cite chain for this bounded
theorem. Closing those upstream rows is the path to a stronger chain;
local rewriting of this note does not by itself close that gap.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the prior feedback requested and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`, PR #899) and the `dm_neutrino` bosonic candidates
trio (commit `7bb12badd`, PR #926).
