# DM Neutrino Operator Selection Obstruction Note

**Date:** 2026-04-14
**Branch:** `codex/dm-across-the-line`

---

## Status

**EXACT OBSTRUCTION, NOW PARTIALLY RESOLVED**

This note records the exact mismatch that exposed the old operator-selection
problem. That specific `Gamma_1` versus `Xi_5` choice on the local chiral
post-EWSB surface is now addressed by
[`docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](/Users/jonBridger/Toy%20Physics-dm/docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md).

So this note remains useful as the obstruction audit, but it is no longer the
final authority on the remaining blocker.

The neutrino-Yukawa blocker is now sharper than "the scale is not derived."
Before normalization, the branch still has not derived **which operator**
represents the physical neutrino Dirac Yukawa after the `3+1` completion.

There are currently two inequivalent framework-native operator surfaces on the
branch:

1. `Xi_5` -- the exact staggered mass operator used in the top-Yukawa lane
2. `Gamma_1` -- the weak-axis EWSB insertion used in the generation / neutrino
   cascade lane

The new runner
[`scripts/frontier_dm_neutrino_operator_selection_obstruction.py`](/Users/jonBridger/Toy%20Physics-dm/scripts/frontier_dm_neutrino_operator_selection_obstruction.py)
shows they are not two descriptions of the same object.

---

## What The New Runner Proves

The obstruction runner establishes four exact facts:

1. `Gamma_1` and `Xi_5` are both Hermitian involutions, so both are
   framework-native candidate operator surfaces.

2. They have **different 3+1 chirality behavior**:
   - `Gamma_1` anticommutes with the `3+1` chirality operator `gamma_5`
   - `Xi_5` commutes with `gamma_5`

3. They have **different locality / hop order** on the taste cube:
   - `Gamma_1` is a one-hop weak-axis insertion
   - `Xi_5` is a four-hop opposite-corner operator

4. They have **different orbit-level action**:
   - `Gamma_1` follows the adjacent-Hamming cascade
     `O_0 <-> T_1 <-> T_2 <-> O_3`
   - `Xi_5` pairs opposite sectors directly
     `O_0 <-> O_3` and `T_1 <-> T_2`

So the branch now has an exact proof that the two operator stories are
genuinely different.

---

## Why This Matters For DM / Eta

The top-Yukawa theorem lane still says the Yukawa operator inherits the
staggered mass surface:

- [`docs/YT_FORMAL_THEOREM_NOTE.md`](/Users/jonBridger/Toy%20Physics-dm/docs/YT_FORMAL_THEOREM_NOTE.md)
- [`docs/YT_WARD_IDENTITY_NOTE.md`](/Users/jonBridger/Toy%20Physics-dm/docs/YT_WARD_IDENTITY_NOTE.md)

Meanwhile the neutrino / generation-cascade lane uses the weak-axis EWSB
surface:

- [`docs/EWSB_GENERATION_CASCADE_NOTE.md`](/Users/jonBridger/Toy%20Physics-dm/docs/EWSB_GENERATION_CASCADE_NOTE.md)
- [`docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md`](/Users/jonBridger/Toy%20Physics-dm/docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md)

The `3+1` completion and right-handed-sector work help by making the mismatch
precise:

- they add the physical chirality split `C^16 = C^8_L + C^8_R`
- they fix the existence of `nu_R`
- but they do **not** derive the bridge from the exact staggered mass surface
  `Xi_5` to the weak-axis insertion `Gamma_1`

That is why the gravity-side `3+1` work sharpens the denominator program but
does not close it.

---

## What This Rules Out

The branch can no longer honestly say any of the following:

1. "The neutrino Yukawa theorem is only missing a prefactor."
2. "The `3+1` completion already identifies the physical Yukawa operator."
3. "The top-Yukawa theorem automatically transfers to neutrinos."

The problem is upstream of normalization. The operator itself is not yet
selected theorem-grade.

---

## Relation To The Old Higgs-Charge Route

This obstruction should **not** be hidden behind the older Higgs-charge
stories. On the current branch, the CKM radiative note explicitly says the
Higgs `Z_3` charge route was superseded:

- [`docs/CKM_RADIATIVE_NOTE.md`](/Users/jonBridger/Toy%20Physics-dm/docs/CKM_RADIATIVE_NOTE.md)

So the operator-selection gap cannot honestly be treated as already solved by
that lane.

---

## Clear Blocker

The theorem-grade blocker is now:

> derive the bridge that selects the physical neutrino Dirac Yukawa operator
> on the `3+1` completed lattice, i.e. explain why the physical post-EWSB
> neutrino mass should live on the weak-axis `Gamma_1` surface rather than on
> the exact staggered mass surface `Xi_5`, or prove the opposite.

Until that bridge exists, the `k_B = 8` leptogenesis story remains conditional
even if the second-order cascade mechanism is structurally attractive.
