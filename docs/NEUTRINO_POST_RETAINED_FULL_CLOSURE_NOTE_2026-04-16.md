# Neutrino Post-Retained Full Closure

**Date:** 2026-04-16  
**Status:** exact post-retained observational-closure package for the live
neutrino lane on the current `main`-derived branch  
**Script:** `scripts/frontier_neutrino_post_retained_full_closure.py`

## Question

What does the current neutrino work on `main` close exactly on the live
post-retained lane?

## Bottom line

The live charged-lepton-active `N_e` lane is exact, but only on the current
observational closure surface.

The branch now has one exact positive lane that is closed end to end:

1. the PMNS-assisted `N_e` source is fixed by the sole-axiom effective-action
   selector on the exact reduced domain;
2. the selected charged Hermitian block `H_e` gives
   `eta / eta_obs = 1` on the favored exact transport column;
3. the remaining microscopic charge-preserving completion is spectator-inert,
   because charged source-response factors only through the Schur value
   `L_e = Schur_{E_e}(D_-) = H_e`;
4. the Majorana side is already fixed by the exact minimal bridge
   `k_B = 8`, `k_A = 7`, `eps/B = alpha_LM/2`.

So the branch should no longer be read as “positive neutrino still structurally
open.” The pure-retained lane is still closed negative, and the live
post-retained lane is structurally closed on the exact observational surface
`eta / eta_obs = 1`.

What remains open is the observation-free normalization/value law that would
recover the same positive lane without using that closure surface.

## Exact PMNS closeout on the promotable lane

The exact selected charged-lepton-active source is the same low-action branch
already isolated by the reduced-domain effective-action theorems:

- `x = (0.47167533, 0.55381069, 0.66451397)`
- `y = (0.20806279, 0.46438280, 0.24755440)`
- `delta ~ 0`

Its packet is exactly

```text
|U_e|^2^T =
[[0.035659, 0.417918, 0.546423],
 [0.894898, 0.103524, 0.001578],
 [0.069443, 0.478558, 0.451999]]
```

and the exact transport values are

- `eta / eta_obs = (1.0, 0.75917896, 0.48458840)`

with favored column `i_* = 0`.

So the PMNS-assisted positive lane is no longer merely “near-closing” and no
longer merely support. On the exact reduced domain it already carries an exact
closure point.

## Why the microscopic `D` tail no longer blocks promotion

The remaining `D`-level ambiguity was the main reason the branch had not yet
been packaged as a full positive lane.

That ambiguity is now killed exactly:

1. for any admissible positive `H_e`, there exist exact charge-preserving
   microscopic completions `D = D_0 ⊕ D_- ⊕ D_+` whose charged Schur value is
   `Schur_{E_e}(D_-) = H_e`;
2. for sources supported on the charged-lepton support `E_e`, the nonlinear
   source-response law factors exactly through that Schur value;
3. therefore different microscopic spectator completions with the same `H_e`
   give the same charged source-response law, the same reconstructed `H_e`, the
   same packet, and the same `eta`.

So the branch no longer needs a separate full-microscopic `D` value law to
promote this lane. On the live positive lane, that microscopic completion data
are quotient / spectator data.

## Majorana side on the same lane

The positive Majorana bridge already supplies:

- `k_B = 8`
- `k_A = 7`
- `eps/B = alpha_LM / 2`

which gives the ordered heavy texture

- `M_1 = 5.323014e+10 GeV`
- `M_2 = 5.828558e+10 GeV`
- `M_3 = 6.149685e+11 GeV`

The exact DM package already uses the same `M_1` anchor, so the positive PMNS
and positive Majorana closes on one coherent integrated lane rather than two
separate stories.

## What remains true

Two older statements remain true and should not be blurred:

- the pure-retained sole-axiom lane is still closed negative at
  `(J_chi, mu) = (0, 0)`
- this positive package is the **post-retained** live lane, not a rescue of the
  pure-retained lane

So the correct science wording should be:

> the current branch now contains one exact post-retained neutrino lane,
> centered on the charged-lepton-active `N_e` selector, with exact
> Schur-completed microscopic closure and the already-fixed Majorana bridge,
> closed on the observational surface `eta / eta_obs = 1`.

## Consequence for the branch package

This note supersedes the older reading that the positive neutrino program was
still open because the off-seed microscopic `D` data had not been fixed.

That older boundary is no longer the live authority surface, because the exact
effective-action selector now fixes the positive `N_e` source and the remaining
microscopic completion has been quotiented by exact Schur invariance.

But this capstone does **not** replace the separate normalization boundary:
the current positive lane is still closed on `eta / eta_obs = 1`, and the
observation-free value law that would remove that input remains open.

## Command

```bash
python3 scripts/frontier_neutrino_post_retained_full_closure.py
```
