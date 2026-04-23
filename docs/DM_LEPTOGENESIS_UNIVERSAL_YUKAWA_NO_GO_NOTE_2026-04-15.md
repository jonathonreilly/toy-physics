# Leptogenesis Universal-Yukawa No-Go

**Date:** 2026-04-15
**Status:** exact CP-kernel no-go on the current universal Dirac bridge
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_leptogenesis_universal_yukawa_nogo.py`

## Question

If the exact retained Dirac theorem is used only as the universal matrix

`Y = y_0 I`,

can the fixed `Z_3` Majorana texture and unitary basis changes alone produce a
nonzero leptogenesis asymmetry?

## Bottom line

No.

For any unitary left/right basis changes `U_L`, `U_R`,

`Y' = U_L^dag (y_0 I) U_R`

still obeys

`Y'^dag Y' = y_0^2 I`.

So every off-diagonal entry `[(Y'^dag Y')_{1j}]` vanishes, and therefore the
standard CP-asymmetry tensor

`Im[(Y'^dag Y')_{1j}^2]`

is identically zero.

So the current exact universal Dirac bridge is **not enough by itself** to
close leptogenesis, even after the branch fixes:

- `k_A = 7`, `k_B = 8`
- `eps/B = alpha_LM/2`
- texture factor `1/3`
- atmospheric benchmark `m_3`

The remaining honest missing object is now sharper:

> derive the non-universal Dirac flavor texture (or equivalent extra
> structure) that makes the CP kernel nonzero on the fixed `Z_3` Majorana
> surface.

## Inputs

This note combines:

- [DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md)
- [DM_Z3_TEXTURE_FACTOR_THEOREM_NOTE_2026-04-15.md](./DM_Z3_TEXTURE_FACTOR_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md)

Those notes already fix the coefficient, the bridge, and the reduced overlap
factor. So the remaining honest question is whether unitary basis changes alone
can turn that universal bridge into a nonzero CP kernel.

## Exact theorem

### 1. The universal bridge is central

If

`Y = y_0 I`,

then `Y` commutes with every unitary basis change.

### 2. `Y^dag Y` stays proportional to the identity

For any unitary `U_L`, `U_R`,

`Y' = U_L^dag Y U_R`

gives

`Y'^dag Y' = U_R^dag Y^dag U_L U_L^dag Y U_R = U_R^dag (y_0^2 I) U_R = y_0^2 I`.

### 3. The CP tensor vanishes

Therefore

`(Y'^dag Y')_{1j} = 0` for `j != 1`,

so

`Im[(Y'^dag Y')_{1j}^2] = 0`.

No nonzero leptogenesis asymmetry can come from that exact universal bridge
alone.

## The theorem-level statement

**Theorem (Universal-Yukawa CP-kernel no-go).**
If the Dirac neutrino Yukawa on the leptogenesis lane is exactly universal
`Y = y_0 I`, then for every unitary choice of charged-lepton and heavy-neutrino
bases the standard CP-asymmetry tensor vanishes identically. Therefore the
current exact universal Dirac bridge is insufficient by itself to produce
leptogenesis.

## What this closes

This closes a real loophole:

- the remaining denominator blocker is not just “write down the CP kernel a bit
  more carefully” while keeping the same universal `Y`

That cannot work.

## What this does not close

This note does **not** prove leptogenesis is impossible in the framework.

It only proves that a nonzero asymmetry now requires at least one more exact
ingredient, for example:

- a derived non-universal Dirac flavor texture
- a derived flavor-breaking insertion beyond the exact universal bridge
- an equivalent exact structure that makes `Y^dag Y` non-diagonal

## Safe wording

**Can claim**

- the current exact universal Dirac bridge alone gives zero leptogenesis
- the remaining blocker is now the non-universal flavor texture behind the CP
  kernel, not the staircase placement or split law

**Cannot claim**

- that leptogenesis is impossible in principle
- that the framework can never derive the needed non-universal structure

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_universal_yukawa_nogo.py
```
