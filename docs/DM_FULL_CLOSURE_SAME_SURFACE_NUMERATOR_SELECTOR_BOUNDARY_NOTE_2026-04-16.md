# DM Full Closure Same-Surface Numerator Selector Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py`

## Question

Does the current exact DM bank already furnish a theorem-grade selector on the
live same-surface numerator interval?

## Answer

No.

The current exact DM bank gives two exact same-surface endpoint observables:

- `alpha_lo = alpha_LM = alpha_bare/u_0 = 0.090667836017286`
- `alpha_hi = alpha_short = -log(P_1)/c_1 = 0.092264992618360`

Those exact endpoints induce distinct certified DM outputs on the corrected
same-surface thermal map:

- `R(alpha_lo) in [5.442019867867, 5.442019867931]`
- `R(alpha_hi) in [5.482855571890, 5.482855571936]`

and therefore

- `Omega_DM(alpha_lo) in [0.267709052538, 0.267709052541]`
- `Omega_DM(alpha_hi) in [0.269717881594, 0.269717881596]`

So the current bank gives an interval, not a selector.

## Why This Closes The Current-Bank Question

The same-surface DM lane already has:

1. exact endpoint observables;
2. an exact structural prefactor `R_base = 31/9`;
3. a certified same-surface thermal evaluation/bounding result that sends those
   endpoints to distinct outputs.

What it does **not** have is any further exact scale-selection law on that DM
lane. So there is no theorem-grade current-bank selector closure.

## Consequence

The current-bank DM selector question is now settled:

- **current bank:** no selector closure
- **next honest science target:** theorem-grade evaluation or bounding of the
  current-bank DM lane is now satisfied on this branch
- **remaining honest science target:** whether the current bank itself can
  supply a selector, or whether the one-scalar DM-side family must remain an
  admitted extension

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by prior 2026-05-05 audit feedback for
`dm_full_closure_same_surface_numerator_selector_boundary_note_2026-04-16`.
The prior feedback identified the completeness / absence premise as the
load-bearing boundary: the negative selector conclusion depends on the
claim that the current DM bank has no further exact scale-selection
datum, while the runner asserts that premise with literal `True`
checks. This addendum does not promote the row or change the claim
scope, which remains the restricted-packet claim that the current exact
DM bank supplies two same-surface endpoints with distinct DM outputs
but no theorem-grade selector choosing among them. Independent audit
owns any current verdict or effective status after this source change.

One-hop authorities cited:

- [`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_INTEGRAL_REPRESENTATION_THEOREM_NOTE_2026-04-16.md`](DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_INTEGRAL_REPRESENTATION_THEOREM_NOTE_2026-04-16.md)
  — audit row:
  `dm_full_closure_same_surface_thermal_integral_representation_theorem_note_2026-04-16`.
  Upstream authority for the certified same-surface thermal
  evaluation / bounding result that maps the two exact endpoint
  observables to distinct certified `R(alpha)` and `Omega_DM(alpha)`
  intervals quoted in the "Answer" and "Why This Closes The
  Current-Bank Question" sections.
- `DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_SELECTOR_SENSITIVITY_BOUNDARY_NOTE_2026-04-16.md`
  — audit row:
  `dm_full_closure_same_surface_thermal_selector_sensitivity_boundary_note_2026-04-16`.
  Boundary reference for the thermal-layer sensitivity result that
  provides compatible framing of "no selector closure on the
  current bank" complementing this no_go.
- `DM_FULL_CLOSURE_SAME_SURFACE_CONVERGED_THERMAL_SELECTOR_SUPPORT_NOTE_2026-04-16.md`
  — audit row:
  `dm_full_closure_same_surface_converged_thermal_selector_support_note_2026-04-16`.
  Boundary reference for the converged thermal selector support
  route whose admitted-extension status is consistent with the no_go
  recorded here.

Open upstream gap registered for independent audit:

- the completeness / absence premise that the live DM bank carries no
  further exact scale-selection datum.

The runner-checked content of this note (the two exact same-surface
endpoint values, the certified `R(alpha)` and `Omega_DM(alpha)`
intervals at those endpoints, and the absence-of-selector check) is
exact arithmetic on values supplied by the cited thermal-evaluation
authority and is independent of the cited upstream authorities at the
arithmetic layer. The cite chain is what supplies the
completeness / absence premise — the DM bank has no further exact
scale-selection datum — that turns the runner's `True` check into a
no_go conclusion, exactly as the prior feedback observed.

## Honest auditor read

Prior audit feedback observed that the negative selector conclusion
depends on the unproved completeness premise that the current DM bank
has no further exact scale-selection datum, and that the runner asserts
that premise with literal `True` checks while importing endpoint / map
machinery from modules not provided in the restricted packet. The
cite-chain repair above wires the certified endpoints, sensitivity
boundary, and converged-selector support side, while registering the
completeness / absence premise itself as the open class D upstream gap.
Closing that gap is the path to a stronger chain; local rewriting of
this note does not by itself close that gap.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the prior feedback requested and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`, PR #899) and the `dm_neutrino` bosonic candidates
trio (commit `7bb12badd`, PR #926).
