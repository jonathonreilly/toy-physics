# Neutrino Majorana `nu_R` Charge-2 Primitive Reduction

**Date:** 2026-04-16  
**Script:** `scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py`

## Question
On the retained one-line `nu_R` lane, if a sole-axiom Majorana reopening ever
exists, what is the exact missing object? Is it still a matrix family, or has
the problem already reduced to one canonical source slot?

## Answer
It has already reduced all the way down.

On the doubled `nu_R` line, the charge-`(+2)` adjoint eigenspace is exactly the
one-dimensional slot `E12`. After the local antisymmetry / Nambu completion,
that slot becomes the one-complex-parameter block

`A_M(m) = m J_2`,  with  `J_2 = [[0,1],[-1,0]]`.

The existing local `nu_R` rephasing removes the phase of `m`, so every future
retained one-generation Majorana reopening is equivalent to the unique normal
form

`mu J_2`,  with  `mu >= 0`.

So the current Majorana blocker is not a hidden matrix family. It is one new
off-diagonal charge-`2` source amplitude on the doubled `nu_R` line.

## Exact Content

The theorem proves:

1. the charge-`(+2)` eigenspace of the doubled-line adjoint action is exactly
   one-dimensional
2. that eigenspace is the upper-right slot `E12`
3. the paired antisymmetric / Nambu completion is exactly the single-complex
   family `m J_2`
4. local `nu_R` rephasing removes the phase of `m`, leaving the unique real
   normal form `mu J_2`
5. the current scalar transfer / response bank still misses precisely that
   off-diagonal slot

## Consequence

This sharpens the Majorana side of the full-closure frontier.

The branch already showed:

- the retained `nu_R` support is rank `1`
- every sole-axiom projected observable on that support is scalar
- the induced Nambu lifts are diagonal and have zero anomalous block

This new theorem closes the remaining geometric ambiguity:

> if Majorana is ever reopened on the retained `nu_R` line, the missing object
> is exactly one rephasing-reduced off-diagonal charge-`2` amplitude `mu`.

So the current exact bank does not fail because it leaves a large unexplored
matrix family. It fails because it does not yet generate the one exact source
slot that Majorana would need.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py
```
