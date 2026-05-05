# Plaquette 3+1D Wilson MC Finite-Size Numerical Theorem Note

**Date:** 2026-05-05
**Type:** positive_theorem
**Claim scope:** on the accepted periodic `3 spatial + 1 derived time`
`SU(3)` Wilson plaquette evaluation surface at `beta = 6`, the committed
five-volume Monte Carlo artifacts `L in {3, 4, 5, 6, 8}` and paired verifier
produce a reproducible finite-size extrapolation
`P_inf = 0.59400 +/- 0.00037` under the `1/L^4` fit, with the independent
`1/L^2` fit giving `P_inf = 0.59288 +/- 0.00033`. The canonical comparator
`0.5934` lies inside the verifier's `1/L^4` two-sigma bracket. This is a
numerical theorem candidate for the accepted Wilson surface, not an analytic
closed-form plaquette derivation and not a source-note status promotion.
**Status authority:** independent audit lane only. This note proposes a
numerical `positive_theorem` claim for audit; effective status is
pipeline-derived after audit ratification and retained-grade dependency
closure.
**Primary runner:** `scripts/frontier_su3_4d_plaquette_fss_verify_2026_05_05.py`
**Data generator:** `scripts/frontier_su3_4d_plaquette_fss_data_2026_05_05.py`
**Generated artifacts:** `outputs/su3_plaquette_fss_2026_05_05/`

## Question

The bounded finite-volume support note
[`PLAQUETTE_4D_MC_SUPPORT_NOTE_2026-05-04.md`](PLAQUETTE_4D_MC_SUPPORT_NOTE_2026-05-04.md)
showed that direct Metropolis computation on the full periodic `3+1D`
Wilson surface is already in the canonical plaquette region at small
volume. Can the repo now carry a stronger, reproducible finite-size
numerical theorem candidate for the same accepted Wilson surface?

## Answer

Yes, as an audit-facing numerical theorem candidate with explicit caveats.
The PR #539 data generator produced five repo-local JSON artifacts for
`L = 3, 4, 5, 6, 8`. The verifier consumes only those artifacts and computes:

- a Madras-Sokal integrated autocorrelation estimate per volume;
- block-jackknife means and standard errors with block size at least
  `2 * tau_int`;
- weighted finite-size fits using `1/L^4` and `1/L^2` correction forms;
- leave-one-out fit sensitivity;
- a transparent comparator-distance report.

The verifier does not fit to the comparator. It computes the extrapolation
from the finite-volume data and reports whether the canonical context value
lies inside the resulting uncertainty bracket.

## Protocol

The data generator uses:

- gauge group `SU(3)`;
- Wilson action at `beta = 6`;
- isotropic periodic `L^4` lattices for `L = 3, 4, 5, 6, 8`;
- cold starts, deterministic per-volume seeds `SEED + L` with module-level
  `SEED = 42`;
- Metropolis-with-staple link updates with three hits per link;
- step-size tuning during thermalization, then a frozen measurement step;
- repo-local JSON artifacts containing the raw plaquette samples.

The load-bearing evaluation surface and `beta = 6` context are inherited from
the current plaquette stack and canonical normalization discussion in
[`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
and [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md). The accepted
Wilson surface grammar is the same one used in
[`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md).

## Runner Result

Reproduce the committed artifacts, when long MC generation is intended:

```bash
python3 scripts/frontier_su3_4d_plaquette_fss_data_2026_05_05.py --mode extra
```

Verify the committed artifacts:

```bash
python3 scripts/frontier_su3_4d_plaquette_fss_verify_2026_05_05.py
```

Expected verifier summary on the committed artifacts:

```text
M1_inv_V:  P_inf = 0.59400 +/- 0.00018 (fit), +/- 0.00032 (LOO)
M2_inv_L2: P_inf = 0.59288 +/- 0.00031 (fit), +/- 0.00009 (LOO)
M1 two-sigma bracket = [0.59327, 0.59473]
SUMMARY: PASS=11 FAIL=0
```

The per-volume means are:

| L | tau_int | n_eff | P(L) | SE |
|---:|---:|---:|---:|---:|
| 3 | 3.73 | 40.2 | 0.60111 | 0.00182 |
| 4 | 5.32 | 28.2 | 0.59717 | 0.00101 |
| 5 | 4.28 | 73.0 | 0.59546 | 0.00041 |
| 6 | 11.94 | 41.9 | 0.59502 | 0.00034 |
| 8 | 7.69 | 65.0 | 0.59395 | 0.00019 |

## What This Closes

This closes a source-control and review-loop gap left by the bounded PR #528
salvage: the repo now has persistent artifacts and a paired verifier for a
five-volume finite-size plaquette calculation on the accepted Wilson surface.

The clean claim is:

> The committed five-volume MC artifacts and verifier produce an
> uncertainty-bearing `L -> infinity` numerical estimate whose primary
> `1/L^4` bracket contains the canonical plaquette comparator.

## What This Does Not Close

This note does not:

- derive a closed-form analytic value for `P(beta=6)`;
- prove from `Cl(3)/Z^3` alone that the Wilson action surface is uniquely
  forced;
- update downstream `alpha_LM`, `u_0`, or `alpha_s` authority surfaces;
- apply any audit verdict or effective retained status.

The open-gate boundary note `GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md`
remains context rather than a retained-grade dependency for this numerical
row. It says two proposed anisotropy routes do not force a new gauge-action
split; it does not itself promote the action surface.

## Import And Support Inventory

- **Computed inputs:** five committed finite-volume MC sample series and the
  verifier's autocorrelation, block-jackknife, and FSS calculations.
- **Admitted numerical method:** finite-volume Metropolis lattice-gauge
  sampling with deterministic seeds and repo-local artifacts.
- **Comparator only:** `0.5934` is used as a canonical context comparator,
  not as a fitted target.
- **Open dependencies:** audit/effective-status promotion depends on the
  independent audit lane and on retained-grade closure of the cited upstream
  plaquette and normalization surfaces.
