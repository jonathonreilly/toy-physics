# Goal: Lane 4F Σm_ν Cosmological Constraint

**Slug:** `neutrino-sigma-mnu-cosmology-20260428`
**Branch:** `frontier/neutrino-sigma-mnu-cosmology-20260428`
**Lane:** 4 (Neutrino quantitative closure) — sub-target 4F

## Primary target

Derive a structural bound or retention statement on `Σm_ν` (sum of
neutrino masses) consistent with the retained cosmology open-number
reduction surface and the retained `N_eff = 3.046` bookkeeping.

## Retained surface to build on

- `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`:
  the late-time bounded cosmology surface has 2 structural dof
  `(H_0, L)` at fixed admitted `R = Ω_r,0`, with
  `Ω_m,0 = 1 - L - R`.
- `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`:
  `N_eff = 3.046` retained from three-generation structure.
- `MINIMAL_AXIOMS_2026-04-11.md`: A_min foundation.
- `NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md`:
  bounded neutrino observables.

## The 4F structural identity entry point

The cosmology matter-budget split:

```text
Ω_m,0  =  Ω_b  +  Ω_DM  +  Ω_ν
```

with the standard CMB convention

```text
Ω_ν h²  =  Σm_ν / (93.14 eV)            (eq. 4F-1)
```

Equivalently (substituting the retained matter density expression):

```text
1 - L - R  =  Ω_b  +  Ω_DM  +  Σm_ν / (93.14 eV h²)            (eq. 4F-2)
```

This is an exact algebraic relation between `Σm_ν` and the retained
`(L, R, h, Ω_b, Ω_DM)` set. **The question is which combinations are
sufficient to retain a structural Σm_ν bound.**

## Phase-1 questions

1. Is `Σm_ν / (93.14 eV)` retainable as a function of retained-only
   inputs?
2. Which inputs (`Ω_b`, `Ω_DM`, `h`) are admitted observational layer
   numbers vs. retainable structural quantities?
3. Can a structural bound (e.g., upper or lower envelope) be retained
   under bounded `h` from Lane 5?
4. Does the recently-retained absolute-scale gate audit (Lane 5
   (C1) gate) constrain `h` enough to pin `Σm_ν`?

## Stop conditions

- Runtime budget reached (3h soft cap on this block).
- Honest stop after Deep Work Rules satisfied with no route passing
  dramatic-step gate.
- Honest closure of 4F sub-target (retained Σm_ν bound).
- Pivot when no productive single-cycle route remains.

## Success metric

Branch-local theorem retaining `Σm_ν` as a structural function of
retained inputs (or a bounded envelope under retained Lane 5
content) — analog of the integrated `Ω_m,0 = 1 - L - R` retention.
