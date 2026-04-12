# S(3) -> Z(2) Weak-Axis Selector: Blocker Note

**Status:** BLOCKED - current retained ingredients do not canonically select a weak axis
**Script:** `scripts/frontier_s3_to_z2_weak_axis_selector.py`

## Claim under test

Does the existing lattice/taste structure, together with the retained
native `Cl(3)` / KS commutant ingredients, canonically select one weak
axis up to cubic conjugacy?

## Verdict

**No, not from the currently retained ingredients alone.**

The algebraic surface that is already retained is enough to show that:

1. the cubic axis-permutation symmetry is `S_3`,
2. the axis representation has one symmetric singlet and a two-dimensional
   standard subspace, and
3. any specific weak-axis choice is one of three symmetry-related vacua
   with `Z_2` stabilizer.

What is *not* yet supplied is an intrinsic order parameter or dynamical
potential on the same taste surface that picks one of those three vacua
canonically.

## Why the current material is insufficient

The current review-safe inputs are:

- the bounded native cubic `Cl(3)` / `SU(2)` result,
- the KS-surface commutant theorem giving `su(3) \oplus u(1)` once a
  distinguished weak factor and residual swap are chosen,
- basis-independence of that commutant once a factorization is fixed.

Those results establish equivalence under cubic conjugacy. They do not
establish a canonical selector.

In particular:

- the `S_3`-invariant algebra on the three axis labels is only
  `a I + b J`, so it yields the singlet-plus-standard decomposition
  `1 \oplus 2`, not a canonical axis projector;
- the three axis basis vectors form one `S_3` orbit, so picking one of
  them requires extra symmetry breaking input;
- the existing CW / EWPT / taste-breaking notes are not a same-surface
  selector theorem. They either live on a different phenomenology surface
  or use modeled taste-breaking coefficients, so they do not canonically
  select a weak axis on the retained taste space.

## What would close the gap

To upgrade this from blocker to theorem, the review branch would need an
explicit same-surface order parameter `Phi` with:

1. `Phi` transforming nontrivially under the axis-permutation `S_3`,
2. an `S_3`-symmetric effective potential or equivalent dynamical rule,
3. three degenerate axis-selecting minima,
4. a proven residual `Z_2` stabilizer for each minimum, and
5. a basis-free bridge from the native bivector weak lane to the chosen
   vacuum.

Absent that, the honest publication claim is still:

- `S_3`-related weak-axis choices are equivalent up to cubic conjugacy,
- but the current retained ingredients do not canonically select one.

