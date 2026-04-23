# Majorana `eps/B` Residual-Ratio Obstruction

**Date:** 2026-04-15
**Status:** exact blocker-sharpening theorem on the fixed staircase placement
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_eps_over_b_residual_ratio_obstruction.py`

## Question

After the branch fixes the staircase placement

`k_A = 7`, `k_B = 8`,

does the current exact stack also fix the remaining doublet-splitting ratio

`eps/B`?

## Bottom line

No.

Once the staircase placement is fixed, the current exact stack still leaves

`r = eps/B`

as a residual dimensionless deformation parameter inside the same exact
three-generation `Z_3` texture class.

For every admissible `r`, the branch still has:

- the same symmetric `Z_3` matrix shape
- the same charge-`2` pairing sector
- the same singlet-plus-doublet eigenvalue decomposition
- the same fixed staircase placement `A/B = alpha_LM^{-1}`

What changes is the normalized doublet spectrum.

So the current exact stack fixes **where** the singlet and doublet sit, but
not **how far apart** the doublet pair is split.

## Inputs

This note uses:

- [NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)

Those notes already fix:

1. the absolute doublet anchor `k_B = 8`
2. the singlet placement `k_A = 7`
3. the exact `Z_3` texture form `[[A,0,0],[0,eps,B],[0,B,eps]]`

So the remaining honest texture question is no longer the staircase
placement. It is the residual dimensionless ratio `eps/B`.

## Exact theorem

Let

`M(r) = [[A,0,0],[0,rB,B],[0,B,rB]]`

with fixed staircase placement

`A/B = alpha_LM^{-1}`.

Then for every admissible `r`:

1. `M(r)` remains symmetric
2. `Delta(r) = M(r) tensor J_2` remains a legitimate pairing block
3. the eigenvalues remain exactly
   `A`, `B(1+r)`, `B(r-1)`
4. the singlet/doublet structure remains the same
5. the staircase placement remains the same

But the normalized doublet spectrum changes continuously with `r`.

So `r = eps/B` is not fixed by the current exact placement theorems.

## The theorem-level statement

**Theorem (Residual-ratio obstruction after fixed staircase placement).**
Assume:

1. the midpoint theorem fixing `k_B = 8`
2. the adjacent-placement theorem fixing `k_A = 7`
3. the current exact `Z_3` Majorana texture class

Then the residual splitting ratio `eps/B` remains a free dimensionless
deformation parameter on the present exact stack.

Equivalently: the branch now fixes the staircase placement, but not the
doublet splitting law.

## What this closes

This closes one ambiguity in the blocker wording.

The live denominator blocker is no longer vaguely:

- the whole `A/B/epsilon` texture

It is now sharply:

- derive `eps/B` (or prove a no-go)
- then close the remaining downstream texture amplitudes

## What this does not close

This note does **not** prove:

- that `eps/B` can never be derived
- that the final texture amplitudes are impossible
- that leptogenesis is dead

It only proves that the current exact stack does not already fix `eps/B`
once the staircase placement is fixed.

## Safe wording

**Can claim**

- the branch now fixes the staircase placement `k_A = 7`, `k_B = 8`
- the remaining dimensionless splitting `eps/B` is still not fixed on the
  current exact stack
- the denominator blocker is now exactly the doublet-splitting law and the
  remaining downstream texture amplitudes

**Cannot claim**

- full `A/B/epsilon` is now derived
- full zero-import `eta` is already closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_eps_over_b_residual_ratio_obstruction.py
```
