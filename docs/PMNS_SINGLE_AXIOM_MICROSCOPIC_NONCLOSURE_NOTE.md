# PMNS Single-Axiom Microscopic Nonclosure

**Status:** exact global boundary theorem at the sole-axiom level  
**Script:** [`frontier_pmns_single_axiom_microscopic_nonclosure.py`](../scripts/frontier_pmns_single_axiom_microscopic_nonclosure.py)

## Sole Axiom

The sole axiom is:

`Cl(3)` on `Z^3`.

No additional PMNS-side axiom is admitted here.

## Question

Does the sole axiom already force the full microscopic lepton-operator values
needed for positive PMNS / neutrino closure?

## Answer

No.

On the fixed `hw=1` generation triplet, the native projected operator span
coming from the full `Cl(3)` taste algebra is already the full matrix algebra
`M(3,C)` on each lepton charge sector. Together with exact sector exchange
between `E_nu` and `E_e`, this means the sole axiom fixes the **carrier** of
the microscopic lepton pair, but not its **values**.

## Theorem

**Theorem (single-axiom microscopic nonclosure).**

From `Cl(3)` on `Z^3` alone:

1. the projected native operator span on each `hw=1` triplet is full `M(3,C)`,
2. the passive monomial basis lies in that native span,
3. the active seed basis lies in that native span,
4. the active corner-breaking basis lies in that native span,
5. exact sector exchange preserves the sole-axiom carrier while flipping the
   active-sector choice,
6. therefore the sole axiom does not uniquely determine
   - the sector-orientation bit,
   - the passive monomial law,
   - the active seed pair,
   - the active `5`-real corner-breaking source.

So full positive PMNS / neutrino closure is **not derivable from the sole
axiom alone**.

## Why This Is Global

This is not a local no-go on one formula family. It is a statement about the
entire sole-axiom microscopic carrier:

- the unresolved PMNS data are not outside the native operator algebra,
- they are inside it already,
- and they appear as independent native directions on the fixed lepton supports.

So the sole axiom does not secretly contain a unique microscopic PMNS value
law waiting to be unpacked. It fixes the admissible operator carrier, not a
unique point in that carrier.

## Exact Content

The runner verifies:

- full projected native `Cl(3)` span = `M(3,C)` on the `hw=1` triplet
- exact inclusion of
  - `I`,
  - `C`,
  - `C^2`,
  - zero-sum diagonal generators,
  - zero-sum cycle-channel generators,
  - the oriented phase direction
  in the native span
- exact realization of both
  - passive monomial examples
  - generic active off-seed examples
  on each native triplet sector
- exact sector-exchange involution on `E_nu ⊕ E_e`
- existence of distinct sole-axiom-native coordinate tuples on the same
  microscopic carrier

## Boundary

This theorem does **not** say that the framework can never close neutrino
physics.

It says only this:

- `Cl(3)` on `Z^3` by itself does not force full PMNS microscopic values.

Therefore any future positive full closure would need a further **derived
dynamical law inside the same framework**, not merely more repackaging of the
sole axiom.

## Consequence for the Lane

This is the honest negative endpoint for the closeout plan.

After this theorem, the lane is scientifically closed at the sole-axiom
boundary:

- the carrier is known exactly,
- the unresolved value directions are known exactly,
- and the sole axiom is proved insufficient to fix them uniquely.
