# DM Leptogenesis Transport-Decomposition Theorem

**Date:** 2026-04-16 (derivation expanded 2026-05-16)
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_transport_decomposition_theorem.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Statement of the theorem

Given the cluster's already-closed inputs (exact source package, exact
projection law `K00 = 2`, exact equilibrium-conversion constants, and the
standard heavy-basis Boltzmann transport ODE on a chosen expansion branch
`H`), the baryon-to-photon ratio factorizes as

```
eta[H] = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom[H],    (*)
```

where every factor on the right-hand side is fixed by a separate retained
identity, and the **unique remaining transport object** is

```
kappa_axiom[H] := | N_{B-L}( z -> infty ; H ) |,
```

i.e. the late-time normalized asymmetry yield of the heavy-basis Boltzmann
transport ODE on the expansion branch `H`, with the CP asymmetry factored out.

## What is actually derived (vs. declared)

The runner derives the factorization step by step. The previous version of
this note merely declared the factorization and asserted the demotion of
`kappa_fit(K)`. The current runner is a constructive derivation:

1. **Definition.** From the cluster's existing exact transport-integral
   theorem note, the normalized heavy-basis Boltzmann ODE is
   ```
   dN_{N1}/dz   = -D_H(z) * (N_{N1} - N_{N1}^eq)
   dN_{B-L}/dz  =  D_H(z) * (N_{N1} - N_{N1}^eq)  -  W_H(z) * N_{B-L}
   ```
   with `D_H, W_H` derived in
   `DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md`. We
   *define*
   ```
   kappa_axiom[H] := | N_{B-L}( z -> infty ; H ) |
   ```
   as the late-time output of this ODE, with `epsilon_1` factored OUT of
   the source term so that `kappa_axiom` is the pure transport functional.

2. **Yield conversion (b).** The equilibrium-conversion theorem
   (`DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md`)
   gives the relativistic Majorana yield
   ```
   d_N = Y_{N1}^eq(z -> 0) = 135 zeta(3) / (4 pi^4 g_*) = 3.901498...e-3.
   ```
   Putting the CP factor back, the produced lepton-asymmetry yield is
   ```
   Y_{B-L} = d_N * epsilon_1 * kappa_axiom[H].
   ```

3. **Sphaleron reprocessing (c).** With three SM lepton flavors and one
   Higgs doublet, the equilibrium sphaleron coefficient is the textbook
   ```
   C_sph = 28/79,
   ```
   giving `Y_B = C_sph * Y_{B-L}`.

4. **Late entropy/photon conversion (d).** Entropy conservation across
   electron-positron annihilation (same theorem note as (b)) gives
   ```
   s/n_gamma = (pi^4 / 45 zeta(3)) * g_{*S}(today) = 7.0394336...,
   ```
   and `eta = n_B / n_gamma = Y_B * (s/n_gamma)`.

5. **Assembly (e).** Combining (b)+(c)+(d) yields
   ```
   eta[H] = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom[H].   (*)
   ```
   Every factor except `kappa_axiom[H]` is a closed retained-tier identity,
   so `kappa_axiom[H]` is the unique remaining transport datum in `eta[H]`.

6. **Numerical witness.** On the exact radiation expansion branch
   `H_rad` (`E_H(z) = 1`), the runner actually solves the normalized
   Boltzmann ODE (via `solve_normalized_transport` in
   `dm_leptogenesis_exact_common.py`) and computes
   ```
   kappa_axiom[H_rad] = 0.004829545290766509
   ```
   directly. The same value is independently reproduced by the exact
   formal transport integral. Plugging into (*) gives
   ```
   eta[H_rad] / eta_obs = 0.188785929502.
   ```

## Comparator status

With the decomposition (*) **derived**, the demotion of the old
strong-washout fit is a corollary, not a stipulation. On the same
expansion branch and at the same exact value of `K`, the legacy
phenomenological fit
```
kappa_fit(K) = (0.3 / K) * (log K)^0.6
```
gives
```
kappa_fit / kappa_axiom = 2.955066...
```
i.e. the fit overstates the true transport by a factor ~2.96. Substituting
`kappa_fit` into the SAME factorization (*) recovers the long-standing
"physically consistent fit" benchmark `eta/eta_obs ~ 0.5579`. So:

- the **factorization (*) is independent** of which kappa is plugged in;
- only `kappa_axiom[H]` is the **authority path**, because only it comes
  from the actual Boltzmann ODE;
- `kappa_fit(K)` is retained **only as a diagnostic comparator** -- the
  factorization (*) then automatically demotes it.

For the record, the comparator values are:
- legacy rounded bookkeeping: `eta/eta_obs = 0.557919848420251`
- same fit with exact bookkeeping: `eta/eta_obs = 0.557874966110017`

## Scope and honest read

This note's substantive content is the **factorization (*) itself**, derived
from the Boltzmann transport ODE plus the cluster's already-closed
thermodynamic/source identities. The factorization is exact and
unconditional once those upstream identities are accepted.

The numerical value `kappa_axiom[H_rad] = 0.004829...` is the runner's direct
ODE solve on the radiation branch and is reproducible; it is not the
load-bearing claim of this note. The load-bearing claim is the
factorization (*), with `kappa_axiom[H]` identified as the unique remaining
transport object. The cluster's `TRANSPORT_STATUS` note carries the
honest scientific status of the full chain (the lane remains open at a
right-sensitive microscopic selector law downstream of this
decomposition).

## Audit dependency repair links

This section makes the load-bearing one-hop dependencies explicit in
response to the 2026-05 `audited_renaming` verdict, which flagged that the
prior version of this note introduced `kappa_axiom[H]` and the demotion of
`kappa_fit(K)` as definitional statements rather than derived results. The
current runner derives the factorization (*) step by step from the
upstream identities below, and exhibits `kappa_axiom[H_rad]` as an
ODE-computed quantity rather than a benchmark number.

- [DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md](DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md)
  — supplies the normalized heavy-basis Boltzmann transport ODE, the
  decay/washout profiles `D_H(z), W_H(z)`, and the equivalence between
  `kappa_axiom[H] = |N_{B-L}(infty;H)|` from the direct ODE solve and the
  exact formal transport integral. Step (a) of the derivation reads off
  the definition of `kappa_axiom[H]` from this theorem note.
- [DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md](DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md)
  — supplies the equilibrium-conversion constants
  `d_N = 135 zeta(3)/(4 pi^4 g_*)` and `s/n_gamma = (pi^4/45 zeta(3)) g_{*S}`
  used in steps (b) and (d) of the derivation, including the underlying
  `g_* = 106.75` and `g_{*S}(today) = 43/11` accountings.
- [DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)
  — supplies the exact source package `gamma = 1/2, E1 = sqrt(8/3),
  E2 = sqrt(8)/3, K00 = 2` and the exact coherent kernel
  `epsilon_1/epsilon_DI = 0.9276...` that the factorization (*) inherits
  through `exact_package()`.
- [DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md](DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md)
  — supplies the exact radiation-expansion law
  `H_rad(T) = sqrt(4 pi^3 g_*/45) T^2 / M_Pl`, i.e. the expansion branch
  on which `kappa_axiom[H_rad]` is computed in Part 3 of the runner.
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
  — supplies the exact projection law `K00 = 2` used both in the source
  package and as the "K is doubled when the source includes K00 = 2"
  bookkeeping that propagates through the factorization.

The runner-side carrier of all these constants is
[`scripts/dm_leptogenesis_exact_common.py`](../scripts/dm_leptogenesis_exact_common.py),
which exposes `exact_package`, `D_THERMAL_EXACT`, `S_OVER_NGAMMA_EXACT`,
`C_SPH`, `solve_normalized_transport`, and `kappa_axiom_reference`. The
runner imports these objects directly so that the factorization (*) is
exhibited as an algebraic identity in those quantities.

The factorization (*) is a derived algebraic identity in the cluster's
already-closed constants, valid on any expansion branch `H` for which the
Boltzmann transport ODE is well-posed; it is not a numerical-match claim.
The closure of the DM flagship lane depends on a separate
right-sensitive microscopic selector law, tracked by the
`TRANSPORT_STATUS` leaf, and is not implied by this decomposition.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_transport_decomposition_theorem.py
```

Runner expected to print `SUMMARY: PASS=17 FAIL=0`.
