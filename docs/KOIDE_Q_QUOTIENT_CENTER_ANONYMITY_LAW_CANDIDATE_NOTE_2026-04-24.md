# Koide Q quotient-center component-anonymity law candidate

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_quotient_center_anonymity_law_candidate.py`  
**Status:** conditional positive law; not retained closure

## Theorem Attempt

The charged-lepton source is prepared on the Morita-normalized quotient-center
source object, and source preparation is natural under all automorphisms of
that quotient source object.  If the retained reduction makes the two center
components source-anonymous, then the automorphism group is the transitive
two-point group `S2`; the unique invariant probability state is uniform.

This gives the exact conditional chain:

```text
w_plus = w_perp = 1/2
K_TL = 0
Y = I_2
E_+ = E_perp
kappa = 2
Q = 2/3
```

## Brainstormed Variants

The attack tested these variants and inversions:

- source-anonymous quotient object: `S2` naturality forces the uniform state;
- inherited Hilbert/rank trace inversion: `G_H=I` gives rank weights `1:2`,
  hence `w_plus=1/3` and `K_TL=3/8`;
- label-counting density variant: `G_label=P_plus+(1/2)P_perp` would equalize
  center labels exactly;
- equivariant Morita inversion: preserving retained `C3` orbit type blocks the
  component swap;
- source-visible orbit falsifier: labels `{0}` and `{1,2}` make the
  label-preserving automorphism group trivial.

## Executable Result

The runner proves the finite-state theorem:

```text
anonymous labels -> Aut = {id, swap}
Aut-invariant p=(w,1-w) -> w=1/2
```

and the falsifier:

```text
source-visible C3 orbit labels:
P_plus label = {0}
P_perp label = {1,2}
Aut_label = {id}
```

With only the identity automorphism, every probability state `(w,1-w)` is
natural.  In particular:

```text
w=1/3 -> Q=1, K_TL=3/8.
```

So quotient-center anonymity is the closest positive route so far, but it
closes `Q` only after adding the missing source-visibility theorem.

## Nature-Grade Boundary

The exact residual is:

```text
RESIDUAL_SCALAR = quotient_center_source_visibility_of_C3_orbit_type
```

A retained closure must derive:

```text
C3 orbit type is not source-visible after reduced observable/Morita
quotienting.
```

Without that theorem, the law is a renamed selector primitive.

## Hostile Review

- **Forbidden target import:** none.  `Q=2/3` appears only as a consequence of
  the conditional uniform state.
- **PDG/H_* pin:** none.
- **Hidden source-free premise:** not promoted.  The missing premise is named as
  source-invisibility of the retained `C3` orbit type.
- **Overbroad closure claim:** blocked.  The runner prints
  `Q_QUOTIENT_CENTER_ANONYMITY_CLOSES_Q=FALSE`.
- **Retained-structure caveat:** equivariant Morita preserves the trivial real
  orbit `{0}` versus nontrivial real orbit `{1,2}` unless a new physical quotient
  theorem removes source visibility of that distinction.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_quotient_center_anonymity_law_candidate.py
```

Expected closeout:

```text
PASSED: 15/15
KOIDE_Q_QUOTIENT_CENTER_ANONYMITY_LAW_CANDIDATE=TRUE
KOIDE_Q_CONDITIONAL_CLOSURE_UNDER_QUOTIENT_CENTER_ANONYMITY=TRUE
KOIDE_Q_RETAINED_CLOSURE_CLAIM=FALSE
Q_QUOTIENT_CENTER_ANONYMITY_CLOSES_Q=FALSE
Q_LAW_REVIEW_BARRIER=derive_C3_orbit_type_not_source_visible
RESIDUAL_SCALAR=quotient_center_source_visibility_of_C3_orbit_type
Q_LAW_FALSIFIER=source_visible_C3_orbit_type_allows_nonuniform_preparations
```

## Next Route

The next positive attack should try to prove the missing source-visibility
quotient directly: that the physical charged-lepton source is functorial only
on the reduced operational quotient and cannot observe retained `C3` orbit type.
If that fails, preserve the residual as a no-go and return to Q with a narrower
source-functor theorem.
