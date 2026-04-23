# DM Neutrino Post-Canonical Right-Frame Obstruction

**Date:** 2026-04-15
**Status:** exact current-stack obstruction theorem on intrinsic derivation of
the post-canonical slot-supported bridge
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_postcanonical_right_frame_obstruction.py`

## Question

After the branch isolates the remaining denominator object to a

- post-canonical
- right-sensitive
- slot-supported
- two-amplitude mixed bridge

can the **current** axiom/atlas stack actually derive that bridge intrinsically?

Or is it still only an extension-class target?

## Bottom line

No. Not on the current stack.

The retained denominator bank fixes the left/Hermitian data

`H = Y Y^dag`

and the current Majorana basis change, but it does **not** fix a canonical
right-handed frame.

Along the exact right orbit

`Y -> Y U_R^dag`,

the retained `H` stays fixed while

`K = Y^dag Y`

conjugates, and with it:

- the singlet-doublet slot amplitudes `u,v`
- the physical heavy-neutrino-basis CP tensor

So the post-canonical slot-supported bridge is still basis-conditional on the
current stack.

## Inputs

This note packages the DM-side analogue of the already-proven PMNS right-frame
obstruction:

- [DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_SLOT_SUPPORT_CLASS_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_SLOT_SUPPORT_CLASS_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md:1)

The PMNS note gives the structural pattern. This note applies it directly to
the live DM denominator object.

## Exact theorem

### 1. The retained bank fixes `H`, not a canonical right frame

Take any Yukawa representative `Y`. For every `U_R in U(3)`,

`Y -> Y U_R^dag`

leaves

`H = Y Y^dag`

unchanged.

So any stack that sees only `H` and left/Hermitian data determines a
right-orbit bundle, not a canonical right frame.

### 2. The post-canonical slot data move on that same orbit

The post-canonical DM bridge is right-sensitive by construction. Its physical
carrier lives in

`K = Y^dag Y`

after transforming to the `Z_3` basis and then to the heavy-neutrino basis.

The runner shows explicitly on a DM-side sample that along an exact right orbit:

- `H` stays fixed
- the singlet-doublet slot amplitudes `u,v` change
- the physical CP tensor changes

So those bridge data are not intrinsic on the current retained stack.

### 3. What is still missing

Therefore isolating the post-canonical bridge as an extension class and as a
support class is not yet the same as deriving it.

To derive it intrinsically, the stack still needs:

- a canonical right-frame-fixing theorem, or
- a genuinely right-sensitive observable principle

that makes the slot-supported bridge intrinsic rather than orbit-dependent.

## The theorem-level statement

**Theorem (Current-stack right-frame obstruction for the post-canonical DM
bridge).**
Assume the current DM denominator stack together with the exact post-canonical
extension-class theorem and the exact post-canonical slot-support-class
theorem. Then the retained bank fixes `H = Y Y^dag` but not a canonical right
frame. Along the exact right-unitary orbit `Y -> Y U_R^dag`, the post-canonical
slot amplitudes `u,v` and the corresponding heavy-neutrino-basis CP tensor
vary while `H` stays fixed. Therefore the post-canonical slot-supported bridge
is still basis-conditional and is not intrinsically derived by the current
stack.

## What this closes

This closes the direct user question cleanly.

The branch no longer needs to hedge with “maybe we can now derive the
post-canonical bridge from the current bank.”

The exact answer is:

- not yet
- not without a new right-frame-fixing theorem or right-sensitive observable
  principle

## What this does not close

This note does **not** prove that such a new theorem is impossible.

It proves only that the current stack does not already contain it.

## Command

```bash
python3 scripts/frontier_dm_neutrino_postcanonical_right_frame_obstruction.py
```
