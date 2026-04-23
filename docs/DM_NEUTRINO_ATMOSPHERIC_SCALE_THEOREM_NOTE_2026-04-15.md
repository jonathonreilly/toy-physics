# DM Neutrino Atmospheric-Scale Theorem

**Date:** 2026-04-15
**Status:** exact positive atmospheric-scale theorem on the current diagonal
benchmark
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_atmospheric_scale_theorem.py`

## Question

Once the branch already has:

- the exact retained Dirac coefficient `y_nu^eff = g_weak^2 / 64`
- the exact doublet anchor `k_B = 8`
- the exact singlet placement `k_A = 7`
- the exact split law `eps/B = alpha_LM / 2`

does the atmospheric neutrino scale still need to be fitted?

## Bottom line

No on the current diagonal benchmark.

The exact chain

- `y_nu^eff = g_weak^2 / 64`
- `v = M_Pl * C * alpha_LM^16`
- `M_1 = M_Pl * alpha_LM^8 * (1 - alpha_LM/2)`

predicts

`m_3 = y_nu^2 v^2 / M_1 = 5.058e-2 eV`

without fitting `m_3`.

The corresponding diagonal atmospheric gap is

`Dm^2_31 = 2.539e-3 eV^2`,

which lands within a few percent of the observed atmospheric scale.

So the branch no longer needs to treat `m_3 ~ 0.050 eV` as a fitted leftover
on this benchmark chain.

## Inputs

This note combines:

- [DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md)
- [NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md)

Those notes already fix:

1. the exact retained local Dirac coefficient
2. the Majorana doublet anchor
3. the singlet placement
4. the doublet split law

So the remaining honest question is whether the atmospheric scale itself still
needs a fit.

## Exact theorem

### 1. The heavy scale is fixed

The current bridge gives

`M_1 = B (1 - eps/B) = M_Pl * alpha_LM^8 * (1 - alpha_LM/2)`.

### 2. The Dirac coefficient is fixed

The retained local Dirac theorem already gives

`y_nu^eff = g_weak^2 / 64`.

### 3. The electroweak scale is fixed

The hierarchy theorem gives

`v = M_Pl * C * alpha_LM^16`.

### 4. The atmospheric scale follows

On the current diagonal benchmark:

`m_3 = y_nu^2 v^2 / M_1`.

Plugging the exact ingredients above into that expression gives

`m_3 = 5.058e-2 eV`.

The corresponding diagonal atmospheric gap

`Dm^2_31 = m_3^2 - m_1^2`

then lands at

`2.539e-3 eV^2`.

## The theorem-level statement

**Theorem (Atmospheric-scale theorem on the exact minimal bridge).**
On the current diagonal benchmark, the exact Dirac coefficient
`y_nu^eff = g_weak^2 / 64` together with the exact Majorana bridge
`k_A = 7`, `k_B = 8`, `eps/B = alpha_LM/2` predicts the atmospheric neutrino
mass scale without fitting `m_3`.

## What this closes

This closes one real denominator-side fit:

- `m_3 ~ 0.050 eV` no longer needs to be treated as a fitted input on the
  benchmark leptogenesis chain

## What this does not close

This note still does **not** derive:

- the solar gap `Dm^2_21`
- the full PMNS / non-universal Yukawa texture
- the exact leptogenesis CP-asymmetry kernel

So the remaining blocker moves downstream to CP-kernel and full-matrix flavor
closure, not the atmospheric benchmark scale.

## Safe wording

**Can claim**

- the atmospheric neutrino scale is predicted on the exact benchmark chain
- the old fitted `m_3` placeholder is no longer needed there

**Cannot claim**

- that full neutrino phenomenology is already closed
- that the solar/PMNS lane is solved

## Command

```bash
python3 scripts/frontier_dm_neutrino_atmospheric_scale_theorem.py
```
