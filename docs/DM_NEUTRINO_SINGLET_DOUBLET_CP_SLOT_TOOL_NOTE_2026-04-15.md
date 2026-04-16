# DM Neutrino Singlet-Doublet CP Slot Tool

**Date:** 2026-04-15  
**Status:** exact structural tool identifying the minimal physical
non-circulant CP carrier after the exact circulant no-go  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_singlet_doublet_cp_slot_tool.py`

## Question

The branch now knows something harsher than before:

- the universal Dirac bridge gives zero CP kernel
- the exact `Z_3`-covariant circulant rescue class is also dead in the
  heavy-neutrino mass basis
- so the missing object is not merely “some non-circulant texture somehow”

What is the minimal exact physical carrier that survives the current Majorana
stack and can still support the standard leptogenesis CP tensor?

## Bottom line

It is a `Z_3`-basis singlet-doublet slot family.

Write the right-Gram / Hermitian kernel in the `Z_3` basis as

```text
K_Z3 =
[ sigma,            (u+v)e^{-i phi},   (u-v)e^{+i phi} ]
[ (u+v)e^{+i phi},  tau+rho,           m               ]
[ (u-v)e^{-i phi},  m^*,               tau-rho         ]
```

Then:

1. `u` is the residual-`Z_2`-even singlet-doublet slot amplitude.
2. `v` is the residual-`Z_2`-odd singlet-doublet slot amplitude.
3. The current right-handed Majorana matrix is diagonalized from the `Z_3`
   basis by a **real** `pi/4` rotation in the doublet block.
4. After that exact physical rotation,

   `(K_mass)_{01} = sqrt(2) (v cos phi - i u sin phi)`,

   `(K_mass)_{02} = sqrt(2) (u cos phi - i v sin phi)`.

So the standard leptogenesis tensor is

`Im[(K_mass)_{01}^2] = Im[(K_mass)_{02}^2] = -2 u v sin(2 phi)`.

At the exact weak source phase `phi = 2 pi / 3`, this becomes

`Im[(K_mass)_{0j}^2] = sqrt(3) u v`.

That is the cleanest exact statement yet:

> the physical denominator carrier is a singlet-doublet slot bridge with one
> even carrier amplitude and one odd activator amplitude.

## Inputs

This note reuses and sharpens:

- [DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md)
- the exact Majorana doublet diagonalization already used throughout the DM
  leptogenesis chain

The circulant tool identified the first exact CP-supporting structural target.
The mass-basis no-go then proved that whole exact circulant class still dies
physically. This note identifies what survives after that cut.

## Exact theorem

### 1. The singlet-doublet couplings split into one even and one odd slot

Let the two singlet-doublet couplings in the `Z_3` basis be

- `a = u + v`
- `b = u - v`

so the complex kernel entries are

- `K_01 = a e^{-i phi}`
- `K_02 = b e^{+i phi}`.

Under the residual doublet exchange `a <-> b`, the combinations become

- `u = (a + b)/2`
- `v = (a - b)/2`

so:

- `u` is exchange-even
- `v` is exchange-odd

This is the exact residual-`Z_2` slot decomposition.

### 2. The physical mass-basis entries depend only on those two slots

On the current stack, the heavy-neutrino mass basis is reached from the `Z_3`
basis by the real orthogonal doublet rotation

```text
R =
[ 1   0        0      ]
[ 0  1/sqrt(2) 1/sqrt(2) ]
[ 0 -1/sqrt(2) 1/sqrt(2) ].
```

Therefore

`K_mass = R^T K_Z3 R`.

The singlet-doublet entries become exactly

- `(K_mass)_{01} = sqrt(2) (v cos phi - i u sin phi)`
- `(K_mass)_{02} = sqrt(2) (u cos phi - i v sin phi)`

and are independent of the spectator diagonal / doublet-block entries
`sigma`, `tau`, `rho`, and `m`.

So the physical CP carrier is not a whole large Hermitian family. It sits
entirely in the singlet-doublet slot amplitudes.

### 3. The physical CP tensor is exactly proportional to `u v`

Squaring those entries gives

- `Im[(K_mass)_{01}^2] = -2 u v sin(2 phi)`
- `Im[(K_mass)_{02}^2] = -2 u v sin(2 phi)`

So:

- if `u = 0`, the tensor vanishes
- if `v = 0`, the tensor vanishes
- if `phi` is CP-trivial, the tensor vanishes

Hence both slots are required:

- an even carrier amplitude `u`
- an odd activator amplitude `v`

### 4. The exact source phase gives a fixed prefactor

At the exact weak-only `Z_3` source phase

`phi = 2 pi / 3`,

the tensor becomes

`Im[(K_mass)_{0j}^2] = sqrt(3) u v`.

So once the correct slot family is identified, the remaining coefficient law is
not arbitrary phase numerology. The phase prefactor is already exact.

### 5. This is genuinely beyond the circulant no-go class

The previous mass-basis no-go showed that every exact `Z_3`-covariant
circulant kernel is diagonal in the `Z_3` basis, so it has

- `K_01 = 0`
- `K_02 = 0`

exactly.

Therefore the singlet-doublet slot family is not a rewording of the old
circulant route. It turns on precisely the slots that are identically empty on
the exhausted circulant class.

## The theorem-level statement

**Theorem (Minimal physical singlet-doublet CP carrier on the current Majorana
stack).**
After the exact `Z_3`-covariant circulant bridge class is ruled out in the
heavy-neutrino mass basis, the minimal surviving physical Hermitian-kernel
carrier is a `Z_3`-basis singlet-doublet slot family with one residual-`Z_2`
even amplitude `u` and one residual-`Z_2` odd amplitude `v`. Under the exact
real Majorana doublet rotation, the standard leptogenesis tensor becomes
`Im[(K_mass)_{0j}^2] = -2 u v sin(2 phi)`, and at the exact source phase
`phi = 2 pi / 3` this specializes to `sqrt(3) u v`.

## What this closes

This closes another vague blocker phrase.

The branch no longer needs to say only:

- “we need some non-circulant, right-sensitive bridge”

It can now say more sharply:

- the missing physical object is a `Z_3`-basis singlet-doublet slot bridge
- it must turn on one even slot amplitude and one odd slot amplitude
- the exact source phase already fixes the phase prefactor

## What this does not close

This note does **not** yet derive:

- the microscopic origin of the even slot amplitude `u`
- the microscopic origin of the odd slot amplitude `v`
- that the currently admitted two-Higgs neutrino lane already forces those
  amplitudes without extra input

So full DM closure is still blocked on the activation law for those slot
amplitudes.

## Safe wording

**Can claim**

- the exact circulant class is physically exhausted
- the minimal physical carrier is now identified more sharply
- the standard CP tensor on that carrier is exactly proportional to `u v`
- the source-phase prefactor is exact

**Cannot claim**

- that the current stack already derives nonzero `u` and `v`
- that the two-Higgs lane is already fully closed as the microscopic source of
  those amplitudes

## Command

```bash
python3 scripts/frontier_dm_neutrino_singlet_doublet_cp_slot_tool.py
```
