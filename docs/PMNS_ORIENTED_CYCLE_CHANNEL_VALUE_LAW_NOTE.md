# PMNS Oriented Cycle Channel Value Law

**Date:** 2026-04-16  
**Status:** exact native observable/value law  
**Script:** `scripts/frontier_pmns_oriented_cycle_channel_value_law.py`

## Question

Can the remaining positive carrier on the retained PMNS active class be
equipped with an exact axiom-native observable/value law?

## Answer

Yes.

On the `hw=1` triplet:

- the exact coordinate-cycle unitary projects to the forward cycle operator
  `C`
- the projected scalar site projectors give the diagonal matrix units
  `E_11, E_22, E_33`
- their products give the canonical forward-cycle edge basis
  `E_12, E_23, E_31`

Therefore any canonical active block has the exact native oriented-cycle
decomposition

`A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31`

with coefficient law

`(c_1, c_2, c_3) = diag(A C^dagger)`.

Equivalently,

`c_i = Tr((P_i C)^dagger A)`,

where `P_i` are the projected scalar triplet projectors.

## Exact chain

### 1. Native forward cycle operator

Let `U_C3` be the exact coordinate-cycle unitary on the taste space. On the
`hw=1` triplet,

`P_hw1^dag U_C3^2 P_hw1 = C`.

So the forward cycle operator is not introduced by hand. It is projected from
the exact coordinate-cycle symmetry.

### 2. Native edge basis

The projected scalar site projectors are exactly

- `P_1 = E_11`
- `P_2 = E_22`
- `P_3 = E_33`

Multiplying by the native forward cycle gives

- `P_1 C = E_12`
- `P_2 C = E_23`
- `P_3 C = E_31`

So the whole forward-cycle channel has an exact native basis.

### 3. Exact coefficient law

For any canonical active block `A`, the forward-cycle coefficients are

`c = diag(A C^dagger)`.

That reproduces exactly the three oriented cycle entries:

- `c_1 = A_12`
- `c_2 = A_23`
- `c_3 = A_31`

The channel mean

`sigma = (c_1 + c_2 + c_3) / 3`

matches the already-derived odd transport mode.

### 4. Lower-level response profile version

If the active lower-level response columns are given, first derive the active
block `A`, then apply the same formula above.

So the oriented-cycle values are read exactly from the lower-level active
response profile as well.

## Consequence

This is not a full sole-axiom closure theorem. It does **not** say the sole
axiom selects the values `(c_1,c_2,c_3)`.

What it does say is stronger than a vague carrier statement:

> the remaining positive carrier now has an exact native observable/value law.

So the unresolved question is no longer “what is the right non-scalar object?”
It is only:

> what law, if any, selects the oriented-cycle values from the sole axiom or a
> further admitted extension?

## Boundary

This note equips the oriented cycle channel with a native observable law.

It does **not** derive the values from `Cl(3)` on `Z^3` alone.

## Command

```bash
python3 scripts/frontier_pmns_oriented_cycle_channel_value_law.py
```
