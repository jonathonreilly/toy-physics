# Z_3 Character-Isomorphism Open Gate for Color and Generation Labels

**Date:** 2026-05-10

**Type:** open_gate
**Claim type:** open_gate

**Status authority:** independent audit lane only. Effective status is
pipeline-derived after audit ratification and dependency closure.

**Primary runner:** `scripts/frontier_z3_character_isomorphism_color_generation.py`

## 1. Scope

This note records a bounded diagnostic about a tempting color/generation
bridge. If the same cyclic order-three permutation is imposed on two abstract
three-label complex vector spaces, then the two representations have the same
`Z_3` character vector `(3, 0, 0)` and are isomorphic to the regular
representation of `Z_3`.

That calculation is useful, but it does not by itself derive a physical bridge
between the `SU(3)_c` color triplet and the generation triplet. The common
label action is an extra bridge assumption unless it is separately derived
from retained repo structure.

The durable review outcome is therefore an open gate:

1. The `SU(3)_c` center `Z_3` is not the desired bridge. On the fundamental
   color triplet its character is `(3, 3 omega, 3 omega^2)`, not `(3, 0, 0)`.
2. A shared axis-cycle/permutation action does give matching regular
   `Z_3` characters, but only after one has imposed the same label action on
   both sectors.
3. This does not promote the earlier integer equality `N_gen = N_color = 3`
   into a retained cross-sector structural theorem.

## 2. Repo Baseline and Imports

The repo baseline is the physical `Cl(3)` local algebra on the `Z^3` spatial
substrate. The `Z^3` spatial substrate has three coordinate axes, and its
cubic symmetry includes an order-three cycle of the axes:

```text
c: e_1 -> e_2 -> e_3 -> e_1
```

The finite-group representation calculations in this note use standard
character theory for `Z_3`. The following inputs are not established here and
remain open/imported bridge data for this surface:

- a physical identification of the three color labels with the three
  `Z^3` axes;
- a physical identification of the three generation labels with the same
  cyclic axis action;
- any downstream operator, readout, or mass-scale bridge that would use such
  an identification.

This note does not add a new axiom, primitive, or retained-surface premise.

## 3. The Calculated Label Fact

Let `T_3 = <c>` be an abstract cyclic group of order three represented by the
permutation matrix

```text
P = [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]]
```

Then `P^3 = I`, `det(P) = 1`, and the character of this three-dimensional
permutation representation is

```text
chi(e)   = 3
chi(c)   = 0
chi(c^2) = 0
```

The irreducible characters of `Z_3` are `chi_0`, `chi_omega`, and
`chi_omega^2`. Orthogonality gives multiplicity one for each irreducible, so
the permutation representation decomposes as

```text
V_perm = chi_0 + chi_omega + chi_omega^2.
```

Therefore two three-label spaces equipped with the same imposed cyclic
permutation action are isomorphic as `T_3` representations.

## 4. The Center Is Not the Bridge

The center of `SU(3)_c` also contains a `Z_3`, but it acts differently from
the permutation representation above. On the color fundamental, a center
element acts by scalar multiplication:

```text
z^n |v> = omega^n |v>
```

so its character vector is

```text
chi_center(e)   = 3
chi_center(z)   = 3 omega
chi_center(z^2) = 3 omega^2.
```

This is not the regular character `(3, 0, 0)`. A center-action argument cannot
identify the color triplet with a generation triplet carrying the regular
`Z_3` character.

## 5. Boundary

This open gate does not establish:

- a retained positive theorem;
- a new structural primitive;
- a load-bearing color/generation bridge;
- a promotion of the existing integer equality
  [`N_gen = N_color = 3`](CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md);
- a charged-lepton Lane 6 closure, a Koide closure, a `y_tau` Ward identity,
  or any empirical mass claim.

It only records the exact finite algebra and the bridge boundary: a common
axis-cycle action would be enough to make the two three-label representations
isomorphic, but that common action is the work still to be derived.

## 6. Related Surfaces

- Integer-equality cross-sector context:
  [`CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md)
- Generation-candidate context:
  [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
- Staggered-Dirac context:
  [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- Charged-lepton open route context:
  [`CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`](CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md)
