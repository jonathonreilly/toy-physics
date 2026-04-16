# Majorana Unique Source Slot Theorem

**Date:** 2026-04-15  
**Status:** exact local-form theorem on the current neutrino lane; not yet an
axiom-forced existence theorem  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_unique_source_slot.py`

## Question

Once the current lane has been reduced to one missing object,

> a genuinely new charge-`2` microscopic primitive on the unique `nu_R`
> channel,

can the **local source form** of that missing object be fixed more sharply?

## Bottom line

Yes, under the minimal local-bilinear source assumption.

If the missing Majorana primitive enters the microscopic theory as a **local
linear bilinear source deformation**, then the current anomaly-fixed symmetry
solve leaves exactly **one complex source slot**

`m in C`

on the unique local seed

`S_unique = nu_R^T C P_R nu_R`.

Equivalently, the most general local Hermitian charge-`2` source deformation on
the current one-generation lane is

`delta I_M(m) = m S_unique + m^* S_unique^dag`.

So the next microscopic unknown is not a family of local couplings. It is the
activation law for one complex source coordinate.

That one-generation slot is now sharpened further by:

- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
- `scripts/frontier_neutrino_majorana_phase_removal.py`

Current result there: the local slot phase is removable on the current
one-generation `nu_R` lane, so the invariant datum is one real amplitude
`mu = |m|`.

The canonical local-block companion is now:

- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- `scripts/frontier_neutrino_majorana_canonical_local_block.py`

Current result there: after phase removal, the full one-generation local
antisymmetric block is canonically fixed as `mu J_2`.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- [NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md)
- [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md](./NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md)

The current exact chain already fixes:

1. the unique local same-chirality charge-`2` channel `S_unique`
2. the absence of any such primitive inside the retained normal grammar
3. the fact that the current atlas does not already contain it under another
   name

So the remaining honest question is no longer "which local channel?" It is
"what local source coordinate would a future realization carry?"

## Exact local source theorem

There are three exact ingredients.

### 1. The local charge-`2` channel is one-dimensional

On the anomaly-fixed one-generation surface, the local Lorentz- and
gauge-invariant same-chirality `Delta L = 2` channel space is one-dimensional:

`span_C { S_unique }`.

So any local charge-`2` bilinear deformation must be proportional to
`S_unique`.

### 2. Hermitian local source insertions add the conjugate channel automatically

If a local source deformation is linear in that bilinear and the microscopic
action is Hermitian, then the source must appear together with its conjugate:

`m S_unique + m^* S_unique^dag`.

The real Hermitian deformation space is therefore two-dimensional over `R`,
equivalently one-dimensional over `C`.

### 3. The local antisymmetric source block has one complex coordinate

On the unique canonical pairing block, every local antisymmetric `2 x 2`
source matrix is of the form

`m J_2`,  with  `J_2 = [[0,1],[-1,0]]`.

So the local bilinear source completion carries one complex slot `m`, not a
matrix of unrelated local coefficients.

## The theorem

**Theorem (Unique local source slot on the Majorana lane).**
Assume the current framework axioms, the anomaly-fixed one-generation matter
closure, and that any future Majorana-generating primitive enters first as a
local linear bilinear source deformation. Then the admissible local deformation
space is exactly

`delta I_M(m) = m S_unique + m^* S_unique^dag`

with one complex source coordinate `m`.

Equivalently: the current lane admits one complex local Majorana source slot,
not an arbitrary family of new local couplings.

## Relationship to the Pfaffian extension

This note does **not** choose a full microscopic realization.

But once the unique source slot `m` is embedded into an antisymmetric
Grassmann/Nambu Gaussian, the exact companion

- [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)

is recovered as one concrete realization of that same slot.

So the current logic is:

1. exact lane reduction says a new charge-`2` primitive is needed
2. this note says any local bilinear realization has one complex source slot
3. the Pfaffian note gives one admitted antisymmetric-Gaussian realization of
   that slot

## What this closes

This closes the next honest local-form question:

- if the missing primitive is local and bilinear, how many new source
  coordinates can it carry?

Answer:

- one complex slot `m`

So the next theorem target is no longer to search over an arbitrary local
coupling family. It is to derive or rule out an activation law for `m`.

After the phase-removal and canonical-block refinements, this can be read even
more sharply as:

- derive or rule out an axiom-side activation law for the single real
  amplitude `mu`

## What this does not close

This note does **not** prove:

- that the primitive exists in the full `Cl(3)` on `Z^3` axiom
- that the primitive must be realized by a Pfaffian/Nambu Gaussian
- that `m` is nonzero
- that `m` is fixed numerically

It is an exact local-form theorem, not an existence theorem.

## Safe wording

**Can claim**

- any future local bilinear Majorana source completion on this lane has one
  complex source slot
- the next microscopic unknown is the activation law for `m`, not a family of
  unrelated local coefficients
- the Pfaffian extension is one admitted realization of that unique slot

**Cannot claim**

- the axiom already forces the source slot to turn on
- the axiom already selects the Pfaffian realization uniquely
- the Majorana problem is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_unique_source_slot.py
```
