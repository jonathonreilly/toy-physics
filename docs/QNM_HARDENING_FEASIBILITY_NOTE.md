# QNM Hardening Feasibility Note

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-05  
**Scope:** decide whether any exact-lattice self-consistent spectral claim can
be made review-safely from the current code/branch context

This note is intentionally conservative. It does **not** promote the branch
QNM story to a retained `main` claim. It only asks what would be required to
make the claim review-safe, and whether the current chain is already close
enough.

Relevant branch-side anchor:

- `claude/distracted-napier:scripts/qnm_scaling.py`
- `claude/distracted-napier:archive_unlanded/poisson-self-consistency-stale-runners-2026-04-30/BACKREACTION_NOTE.md`

Relevant current `main` context:

- [POISSON_SELF_GRAVITY_LOOP_NOTE.md](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_LOOP_NOTE.md)
- [POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md)
- [GATE_B_POISSON_SELF_GRAVITY_NOTE.md](/Users/jonreilly/Projects/Physics/docs/GATE_B_POISSON_SELF_GRAVITY_NOTE.md)

## Branch claim surface

The branch harness sweeps self-coupling `G` and source mass `s`, then looks
for escape-spectrum minima across a `k` scan.

The strongest branch-side headline is:

- peak locations depend on `G`
- peak locations are approximately independent of `s`

That is scientifically interesting, but it is not yet review-safe as a
mainline spectral claim.

## Why it is not yet review-safe

The current branch story is missing the controls that the retained `main`
bars now require.

### 1. No `G = 0` null

There is no frozen `G = 0` spectral null showing that the peaks collapse to the
baseline when self-coupling is removed.

Without that, the claim can still be a coupling trend, but not yet a clean
self-consistent spectral effect.

### 2. Nyquist artifact risk is real

The branch audit already flagged a `k = 6.5` artifact tied to the Nyquist
boundary.

That means the spectrum cannot be promoted until the non-Nyquist peaks are
shown to survive:

- peak-threshold changes
- `h` refinement
- `W` changes
- damping changes
- explicit exclusion of the Nyquist-adjacent artifact

### 3. No matched fixed-field control

The branch harness compares self-consistent field runs, but it does not yet
freeze a matched fixed-field control that isolates the spectral effect from the
field-update loop itself.

That control is needed if the final claim is to be interpreted as a
self-consistent spectral signature rather than a generic escape-minimum
pattern.

### 4. No Born check on the converged field

The mainline self-gravity audit already showed that step-local Born can be
clean while end-to-end Born drifts in the loop.

The branch QNM harness does not yet package a corresponding Born audit on the
converged spectral family.

That matters because a spectral claim that depends on the self-consistent loop
needs to survive the same linearity checks as the rest of the project.

### 5. No refinement / threshold stability pack

The branch harness does not yet freeze a stability pack showing that the peak
locations and spacings are stable under:

- spatial refinement
- peak-threshold variation
- window selection
- damping variation

Without that, the peak spacing is still analysis-choice sensitive.

## What would be needed

To make a QNM-style claim review-safe, the branch would need a narrow,
frozen chain with all of the following:

1. `G = 0` null
2. fixed-field matched control
3. Born check on the converged field
4. explicit Nyquist-artifact exclusion
5. refinement and threshold stability
6. a dedicated note/log pair

## Safest current phrasing

The safest claim surface today is:

- the branch QNM harness suggests a `G`-dependent escape spectrum on a
  self-consistent field family
- the result is still exploratory
- it is **not** yet safe to call it a retained exact-lattice spectral law

## Verdict

**feasibility: not yet review-safe**

The QNM lane is worth hardening only if we can add the missing controls above.
Until then, it should remain a branch-side exploratory spectral probe rather
than a retained mainline claim.
