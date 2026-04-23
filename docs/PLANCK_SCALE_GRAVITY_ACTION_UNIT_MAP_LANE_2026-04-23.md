# Planck-Scale Gravity/Action Unit-Map Lane

**Date:** 2026-04-23  
**Scope:** science-only lane note  
**Audit runner:** `scripts/frontier_planck_gravity_action_unit_map_lane.py`

## Verdict

The strongest candidate theorem in this lane is a **discrete gravity/action
unit-map theorem**:

> derive the unique physical unit conversion between the retained discrete
> gravity/action stack and the textbook Einstein-Hilbert normalization without
> importing measured `G` or `M_Pl`.

That theorem is the right target because the current gravity stack already
fixes the dimensionless weak-field structure, but it does not yet fix the
absolute physical scale.

On the current repo evidence, this route is **not yet a derivation of the
physical unit map**. It should currently remain a **pinned-observable lane**.

The strongest current branch-local result is now the sharper no-go in
[PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md):
the admitted gravity/action family is homogeneous under one positive global
unit-map rescaling, so it fixes a scale ray rather than an absolute anchor.
That does not kill the route, but it does change the target. Any future
success now has to come from a genuinely new unit-bearing same-surface
observable, not from reusing the current admitted family alone.

## Why This Is Still the Best Candidate

The lane is still the best open route because it is the only one that keeps
the dimensionless gravity/action stack intact while leaving exactly one gap:
the map from lattice units to SI/GeV.

The relevant load-bearing facts are:

- the clean gravity derivation reaches `G_N = 1/(4 pi)` in lattice units;
- the action-normalization note fixes the weak-field coefficient only after
  tying `G` to observation;
- the canonical Einstein-Hilbert-style equivalence note closes the geometric
  comparison, but not the absolute unit conversion.

So the route is not blocked by a retained no-go theorem. It is blocked by the
absence of a framework-native scale anchor.

## Strongest Candidate Theorem

The best candidate theorem can be stated as:

> If the discrete gravity/action kernel and its canonical textbook
> Einstein-Hilbert counterpart are truly the same physical operator family,
> then the weak-field normalization should determine a unique physical unit
> map, not merely a dimensionless equivalence.

That would have to do more than prove geometric equivalence. It would need to
identify the lattice spacing, or an equivalent physical length, from the
internal structure of the theory itself.

At present, the repo does not have that theorem.

## Exact Blockers

1. **Gravity stops at lattice units.**  
   The clean gravity note explicitly states that the derivation gives
   `G_N = 1/(4 pi)` in lattice units and that converting to SI requires one
   calibration.

2. **Action normalization still uses observation at the last step.**  
   The action-normalization note fixes the coupling coefficient by requiring
   the observed light-bending ratio and by defining `G` from observation.
   That is a normalization success, not a unit-map derivation.

3. **The canonical EH equivalence is not an absolute-scale theorem.**  
   The textbook geometric/action equivalence note closes the canonical
   comparison on the chosen target, but it explicitly treats the remaining
   comparison work as packaging-only. It does not produce `a`, `l_P`, or
   `M_Pl`.

4. **No internal observable currently pins the absolute length scale.**  
   The existing route gives the right dimensionless structure, but nothing in
   the admitted stack currently identifies the lattice spacing with a physical
   length without outside calibration.

5. **The current family is homogeneous under the remaining unit-map ray.**  
   The new scale-ray no-go theorem shows that the Einstein-Hilbert-style
   action, Newton potential, hierarchy product, and retained spectral-gap
   identities all remain exact along one positive rescaling ray. So the
   missing anchor is not just absent in practice; it is absent on the current
   admitted family in principle.

## Honest Lane Decision

This lane is still scientifically meaningful, but only as a pinned-observable
lane for now.

What is plausible:

- a future theorem may turn the existing gravity/action equivalence into a
  physical unit map;
- if that happens, it would likely collapse a large part of the remaining
  Planck-scale calibration problem.

What is not yet justified:

- claiming that the current stack already derives the physical unit map;
- claiming that the route has removed the need for one calibration;
- treating the current Einstein-Hilbert equivalence as enough to fix SI/GeV
  units.
- treating the current admitted gravity/action family as if it secretly
  contained a hidden absolute-scale anchor.

## Lane Summary

- **Best theorem candidate:** discrete gravity/action unit-map theorem
- **Current blocker:** missing framework-native non-homogeneous physical scale
  anchor
- **Current status:** pinned-observable lane, not derived unit map
- **Reason:** the repo closes the dimensionless gravity/action structure, but
  not the absolute unit conversion, and the current admitted family now has a
  scale-ray no-go on that point
