# DM Neutrino Source-Amplitude Theorem

**Date:** 2026-04-15  
**Status:** exact sharp-branch source-amplitude theorem on the refreshed
`main`-derived DM lane  
**Script:** `scripts/frontier_dm_neutrino_source_amplitude_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the DM weak-to-triplet transfer coefficients are fixed, what is still
left on the source side?

Can the selector amplitude `a_sel` and the symmetric weak source amplitude
`tau_+ = tau_E + tau_T` be fixed canonically on the sharp source-oriented
branch?

## Bottom line

Yes.

On the sharp source-oriented branch:

- `a_sel = 1/2`
- `tau_E = tau_T = 1/2`
- `tau_+ = 1`

Therefore, using the already-derived transfer coefficients,

- `gamma = c_odd a_sel = 1/2`
- `E1 = sqrt(8/3) tau_+ = sqrt(8/3)`
- `E2 = (sqrt(8)/3) tau_+ = sqrt(8)/3`

So on the refreshed `main`-derived branch, the source side is no longer a
floating pair of amplitudes on the sharp branch. It is canonically fixed.

## Selector amplitude

The reduced selector lane already gives one exact class with one real
amplitude,

`B_red = a_sel S_cls`

with

`S_cls = chi_N_nu - chi_N_e`.

The sign theorem already says `a_sel > 0` picks the neutrino-side branch.

The new step is the sharpness normalization. Reusing the bosonic-bilinear
selector principle, the selected branch is not treated as a soft weighted
mixture. It is treated as a sharp resolved branch projector.

On the reduced `N_nu/N_e` block, the source-oriented sharp selector is

`P_nu = diag(1,0)`

and its centered selector part is

`P_nu - (1/2)(P_nu + P_e) = (1/2) S_cls`.

So the canonical sharp selector amplitude is

`a_sel = 1/2`.

## Symmetric weak source amplitude

The exact weak source carrier is the two-column bright bundle

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]`.

The swap-reduction theorem already showed that only the symmetric source mode
survives into the exact even-response law:

`tau_+ = tau_E + tau_T`.

The sharp bosonic-even source on that exact two-channel factor is the swap-even
projector

`P_+ = (1/2)(I + P_swap) = (1/2) [[1,1],[1,1]]`.

Its source coordinates are exactly

`(tau_E, tau_T) = (1/2, 1/2)`,

so

`tau_+ = 1`.

## Immediate DM consequence

The coefficient theorems already gave:

- `c_odd = +1`
- `v_even = (sqrt(8/3), sqrt(8)/3)`.

Substituting the sharp source amplitudes gives the exact triplet-side source
data

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`.

That is the strongest exact source-side closure point reached so far on the
refreshed `main`-derived DM branch.

## What this does not close

This note does **not** by itself claim final `eta` closure.

Its role is narrower and exact: it fixes the sharp-branch source amplitudes
that feed the downstream kernel. The benchmark rewrite is now carried by
`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`.

So this remains the canonical source-amplitude theorem, while the exact-kernel
note is the downstream benchmark authority.

## Command

```bash
python3 scripts/frontier_dm_neutrino_source_amplitude_theorem.py
```
