# DM A-BCC Corrected Five-Basin Chamber-DPLE Support Theorem

**Date:** 2026-04-21
**Lane:** Dark-matter A-BCC native chamber+DPLE route
**Status:** SUPPORT THEOREM. The old chamber+DPLE route survives the
five-basin correction: on the corrected retained chart
`{Basin 1, Basin N, Basin P, Basin 2, Basin X}`, the active-chamber
survivors are `{Basin 1, Basin 2, Basin X}`, Basin 2 fails the DPLE
`F_4` selector outright, and the corrected composition
`(C1) chamber ∩ (C2) F_4` still selects Basin 1 uniquely.
**Boundary:** This is **not** yet full axiom closure of the DM flagship lane.
It sharpens the strongest current native A-BCC route, but it still works on
the retained five-basin source chart rather than deriving that chart from
`Cl(3)/Z^3` alone. It therefore does not supersede the review branch’s
retained-measurement A-BCC closure grade.
**Primary runner:**
`scripts/frontier_dm_abcc_five_basin_chamber_dple_support_2026_04_21.py`

---

## 0. Executive summary

The retained basin-enumeration completeness theorem corrected the old
four-basin A-BCC chamber+DPLE note by adding the missing in-chamber basin

    Basin 2 = (28.006, 20.722, 5.012),

which lies in `C_neg`. That left one explicit science gap:

> does the chamber+DPLE route still work once Basin 2 is added?

This note answers yes.

On the corrected retained five-basin chart:

- chamber survivors are `{Basin 1, Basin 2, Basin X}`;
- `F_4(Basin 1) = TRUE`;
- `F_4(Basin 2) = FALSE`;
- `F_4(Basin X) = FALSE`.

So the corrected composition is

```text
{Basin 1, Basin N, Basin P, Basin 2, Basin X}
    -- chamber --> {Basin 1, Basin 2, Basin X}
    -- F_4     --> {Basin 1}
```

The strongest current native chamber+DPLE route therefore survives the
five-basin correction intact.

What this buys:
- it removes the explicit Basin 2 hole left open in the completeness note;
- it preserves the strongest current native A-BCC candidate route;
- it narrows the remaining stricter gap further: the unresolved issue is no
  longer Basin 2 or chamber bookkeeping, but the derivation of the physical
  source chart / selector structure itself.

---

## 1. Setup

Take the corrected retained five-basin chart:

| Basin | `(m, delta, q_+)` | chamber? | `det(H)` |
|---|---|---|---:|
| Basin 1 | `(0.657061, 0.933806, 0.715042)` | IN | `+0.959` |
| Basin N | `(0.501997, 0.853543, 0.425916)` | OUT | `+0.567` |
| Basin P | `(1.037883, 1.433019, -1.329548)` | OUT | `-9.861` |
| Basin 2 | `(28.006, 20.722, 5.012)` | IN | `-70538.6` |
| Basin X | `(21.128264, 12.680028, 2.089235)` | IN | `-20296.1` |

The chamber filter is the retained structural inequality

```text
q_+ + delta >= sqrt(8/3).
```

The DPLE selector is the cubic `d = 3` condition

```text
F_4(H_base, J_B)) :
    Delta = c_2^2 - 3 c_1 c_3 > 0
    and there exists an interior Morse-index-0 critical point
    t_* in (0,1) with p(t_*) > 0
```

for

```text
p(t) = det(H_base + t J_B) = c_0 + c_1 t + c_2 t^2 + c_3 t^3.
```

---

## 2. Corrected chamber survivors

The corrected chamber filter gives:

- Basin 1: IN
- Basin 2: IN
- Basin X: IN
- Basin N: OUT
- Basin P: OUT

So after the five-basin correction, chamber survivors are

```text
{Basin 1, Basin 2, Basin X}.
```

This is the only structural change relative to the older four-basin route.

---

## 3. Basin 2 fails `F_4`

For Basin 2, the exact cubic coefficients are

```text
c_0 = +5.0283...
c_1 = -333.785...
c_2 = +7653.526...
c_3 = -77863.373...
```

The DPLE discriminant is

```text
Delta_2 = c_2^2 - 3 c_1 c_3 = -1.9392452885... x 10^7 < 0.
```

So `p'(t)` has no real roots at all. There is no interior critical point, hence
no interior Morse-index-0 minimum, hence

```text
F_4(Basin 2) = FALSE.
```

This is stronger than the earlier expectation-level statement in the
basin-completeness note: the missing Basin 2 case is now checked exactly.

---

## 4. Corrected composition theorem

> **Theorem (corrected five-basin chamber+DPLE composition).**
>
> On the corrected retained five-basin chart, the composition
> `chamber ∩ F_4` selects Basin 1 uniquely.

### Proof

- Chamber survivors are `{Basin 1, Basin 2, Basin X}`.
- `F_4(Basin 1) = TRUE`.
- `F_4(Basin 2) = FALSE` by the negative discriminant above.
- `F_4(Basin X) = FALSE` by the existing DPLE check.

Therefore

```text
{Basin 1, Basin 2, Basin X} ∩ {Basin 1} = {Basin 1}.
```

QED.

---

## 5. What this does and does not close

### 5.1 What it closes

- the explicit Basin 2 hole in the older chamber+DPLE route;
- the basin-enumeration note’s pending “needs verification” item for
  `F_4(Basin 2)`.

### 5.2 What it does not close

- full axiom closure of the DM flagship lane;
- derivation of the five-basin source chart from `Cl(3)/Z^3` alone;
- the finer right-sensitive microscopic selector law.

So the honest status is:

- the native chamber+DPLE route is stronger than before;
- the branch still does not have full axiom closure end-to-end.

---

## 6. Review consequence

This theorem does **not** change the branch’s package-surface headline, which
already uses the retained-measurement A-BCC closure theorem as the operative
closure grade. What it does change is the native-route map behind that review
surface:

- the strongest chamber+DPLE native route is now internally consistent on the
  corrected five-basin chart;
- the next stricter target is not “recheck Basin 2,” but rather “derive the
  relevant source chart / selector structure natively.”

---

## 7. Verification

The runner:

- verifies the corrected chamber survivor set `{Basin 1, Basin 2, Basin X}`;
- checks `F_4` on all five retained basins by three independent routes
  (closed-form discriminant, Newton on `p'(t)`, and direct sampling);
- proves `F_4(Basin 2) = FALSE`;
- verifies the corrected composition `chamber ∩ F_4 = {Basin 1}`.

See
`scripts/frontier_dm_abcc_five_basin_chamber_dple_support_2026_04_21.py`.

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by prior 2026-05-05 audit feedback for
`dm_abcc_five_basin_chamber_dple_support_theorem_note_2026-04-21`.
The prior feedback accepted the finite algebraic / numerical check on
the provided basin coordinates and runner definitions, but identified
an upstream-source gap: the broader support theorem imports the
five-basin source chart and selector structure without deriving them in
this packet. This addendum does not promote the row or change the claim
scope, which remains the corrected five-basin
`chamber ∩ F_4 = {Basin 1}` finite verification on the explicitly
tabulated basin coordinates. Independent audit owns any current verdict
or effective status after this source change.

One-hop authorities cited:

- [`DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md`](DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md)
  — audit row: `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19`.
  Upstream source authority for the DPLE / `F_4` cubic-discriminant
  selector that this note's Section 3 evaluates pointwise on each
  basin.
- [`DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md`](DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md)
  — audit row: `dm_abcc_chamber_bound_derivation_note_2026-04-20`.
  Upstream authority candidate for the structural inequality
  `q_+ + delta >= sqrt(8/3)` that defines the chamber filter applied in
  Section 2.
- [`DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md`](DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md)
  — audit row:
  `dm_abcc_closure_via_chamber_bound_and_dple_f4_note_2026-04-19`.
  Upstream authority candidate for the four-basin chamber+DPLE route
  that this note corrects to the five-basin chart by adding Basin 2.
- [`DM_ABCC_BASIN_FINITE_SEARCH_SUPPORT_NOTE_2026-04-30.md`](DM_ABCC_BASIN_FINITE_SEARCH_SUPPORT_NOTE_2026-04-30.md)
  — audit row: `dm_abcc_basin_finite_search_support_note_2026-04-30`.
  Upstream authority candidate for the five-basin chart enumeration
  completeness whose missing in-chamber Basin 2 motivated this support
  theorem.

Open upstream gaps registered for independent audit:

- the chamber-bound source-cubic authority;
- the four-basin chamber+DPLE route authority;
- the five-basin enumeration-completeness authority.

The runner-checked content of this note (corrected chamber survivors
on the five-basin chart; closed-form, Newton, and sampled `F_4`
agreement on each basin; `Basin 2` discriminant negativity; corrected
composition `chamber ∩ F_4 = {Basin 1}`) is exact finite-dimensional
arithmetic on the explicitly tabulated basin coordinates and is
independent of the cited upstream authorities. The cite chain is what
supplies the upstream source chart and selector structure that this
note imports rather than derives.

## Honest auditor read

Prior audit feedback observed that the finite algebraic check closes on
the provided basin coordinates and runner definitions, but the broader
theorem imports the five-basin source chart and selector structure
without a cited source authority or first-principles derivation in the
restricted packet. The cite-chain repair above wires the DPLE / `F_4`
selector authority and registers the chamber-bound, four-basin closure,
and finite-search candidates on the source-chart side. Closing those
upstream rows is the path to a stronger chain; local rewriting of this
note does not by itself close that gap.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the prior feedback requested and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`, PR #899) and the `dm_neutrino` bosonic candidates
trio (commit `7bb12badd`, PR #926).
