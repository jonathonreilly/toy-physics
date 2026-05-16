# DM Full Closure Same-Surface Numerator Selector Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py`

## Question

Does the current exact DM packet already furnish a theorem-grade selector on
the live same-surface numerator interval?

## Honest packet-scope answer

Not within the supplied packet.

The current exact DM packet gives two exact same-surface endpoint coupling
observables, both derived from the common surface ingredient
`alpha_bare = 1/(4 pi)` and the canonical plaquette `0.5934`:

- `alpha_lo = alpha_LM    = alpha_bare / u_0                 = 0.090667836017286`
- `alpha_hi = alpha_short = -log(1 - c_1 * alpha_bare) / c_1 = 0.092264992618360`

These two endpoints are distinct exact reals and both sit strictly above the
common ingredient `alpha_bare`, so they are two genuinely distinct retained
constructions on the same surface, not relabelings of a single observable. The
cited certified same-surface thermal authority sends those exact endpoints to
non-overlapping certified DM ratio intervals:

- `R(alpha_lo) in [5.442019867867, 5.442019867931]`
- `R(alpha_hi) in [5.482855571890, 5.482855571936]`

and therefore

- `Omega_DM(alpha_lo) in [0.267709052538, 0.267709052541]`
- `Omega_DM(alpha_hi) in [0.269717881594, 0.269717881596]`

So the current packet exhibits a two-element same-surface endpoint set that
lands disjoint certified DM ratio intervals. It does not, within this packet,
exhibit a selector between them.

## What this note proves (constructive content)

The runner verifies, by exact arithmetic on the cited authority outputs:

1. the two endpoint coupling values are well-defined exact reals;
2. they are distinct from each other and both strictly above the common
   ingredient `alpha_bare`, so they are two genuinely distinct same-surface
   constructions and not the same observable in disguise;
3. via the cited certified thermal authority, they map to non-overlapping
   certified DM ratio intervals (so *if* a selector exists within a larger
   packet, it must land one endpoint and exclude the other).

## What this note does not prove (packet-scope completeness declaration)

The runner explicitly does **not** prove the metatheoretical claim that no
selector exists. The earlier version of this runner asserted that absence with
two literal-`True` checks, and prior audit feedback correctly flagged those
literals as the load-bearing weakness of the note. The repaired runner removes
those literals and replaces the absence claim with a print-only **packet-scope
completeness declaration**:

> Within the supplied retained packet (the framework axiom Cl(3) on Z^3
> together with the cited same-surface thermal authorities recorded below), no
> additional exact same-surface DM scale-selection datum is supplied. Any
> selector that lands one of the two endpoints therefore requires a retained
> authority outside the current packet.

This is a statement about *what is in the current packet*, which is a
verifiable scope claim. It is not, and is not represented as, a proof that no
such authority can ever be added in a larger packet.

## Consequence

- **current packet:** exhibits two distinct same-surface endpoint observables
  with non-overlapping certified DM outputs, and supplies no further exact
  same-surface scale-selection datum;
- **current packet selector closure:** does not exist within this packet (this
  is a packet-scope declaration, not a metatheoretical no-go);
- **next honest science target:** if a constructive obstruction theorem
  modelled on the same-signature/different-output pattern used by
  `DM_NEUTRINO_SOURCE_BANK_Z3_DOUBLET_BLOCK_SELECTION_OBSTRUCTION_THEOREM_NOTE_2026-04-16.md`
  can be derived for the DM same-surface endpoint pair from Cl(3) on Z^3, this
  note's packet-scope declaration can be promoted to a no-go theorem against a
  specified class of selector inputs;
- **remaining honest science target:** whether such an obstruction theorem
  exists for the DM same-surface lane, or whether the one-scalar DM-side
  family must remain an admitted extension.

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
earlier rigorize wired the certified-endpoints / sensitivity / converged
support side and registered the completeness premise as an open
class D upstream gap, but it deliberately left the two literal `True`
checks in place in the runner and left the note's load-bearing claim
phrased as a metatheoretical no-go ("no theorem-grade current-bank
selector closure exists"). That phrasing made the runner output formally
incompatible with the actually-supplied content.

The current repair (2026-05-16) addresses that load-bearing weakness by
demoting both the runner content and the note phrasing to what the
restricted packet actually supplies:

- the two prior `check(name, True, ...)` literals in PART 3 are removed;
- PART 3 is replaced with four arithmetic distinctness checks that the
  runner can actually verify (endpoint distinctness from each other, and
  from the common ingredient `alpha_bare`, plus the non-overlap of the
  certified DM ratio intervals);
- the metatheoretical absence claim is replaced by an explicit
  print-only **packet-scope completeness declaration** that says only
  what the restricted packet contains, not what no future packet could
  contain;
- the note's "Honest packet-scope answer" / "What this note proves" /
  "What this note does not prove" sections now match the runner output
  one-to-one.

This addresses the class E load-bearing-step gap on its own terms: the
load-bearing step is no longer "no selector exists" (an absence claim
the runner cannot prove); it is the arithmetic distinctness of two
exact endpoint reals and the non-overlap of their certified DM ratio
intervals (both runner-checked from cited authority outputs), plus a
packet-scope declaration whose verifiable scope is exactly the supplied
retained packet.

Closing the remaining upstream gap — promoting this packet-scope
declaration to a constructive obstruction theorem against a specified
class of selector inputs — would model on the same-signature /
different-output pattern of
`DM_NEUTRINO_SOURCE_BANK_Z3_DOUBLET_BLOCK_SELECTION_OBSTRUCTION_THEOREM_NOTE_2026-04-16.md`,
which provides exactly that kind of constructive obstruction on the
neutrino source side. Local rewriting of this note does not by itself
supply such an obstruction; it removes the formal overreach in this
note and registers the obstruction itself as the next constructive
target.

## Scope of this rigorization

This rigorization is class C (load-bearing-step demotion to verifiable
arithmetic plus an explicit packet-scope declaration). It replaces the
two prior literal-`True` runner checks that audit feedback flagged as
the load-bearing weakness with four arithmetic distinctness checks on
the cited authority outputs, removes the metatheoretical absence claim
from the runner-checked tier, and rewords the note so that its
"answer", "what is proved", and "what is not proved" sections match the
runner output one-to-one. The cite chain and prior class D upstream gap
registration above remain in place. Independent audit owns any current
verdict or effective status after this source change.
