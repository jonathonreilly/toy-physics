# Mirror Chokepoint Boundary Fit Note

**Date:** 2026-04-03  
**Status:** bounded finite-window certificate for the named dense boundary mirror card; no mirror-family theorem and no asymptotic law.

This note freezes one named finite parameter card from the mirror chokepoint
runner. The claim is intentionally bounded: the card is Born-clean,
gravity-positive, and decohering for `N = 40, 60, 80, 100`, has a gravity wall
at `N = 120`, and has a weak descriptive fit on the four retained rows. The
fit is not used to select the card or the retained rows.

**Primary runner:** [`scripts/mirror_chokepoint_boundary_fit_certificate.py`](../scripts/mirror_chokepoint_boundary_fit_certificate.py)

**Companion replay runner:** [`scripts/mirror_chokepoint_joint.py`](../scripts/mirror_chokepoint_joint.py)

**Registered output:** [`logs/runner-cache/mirror_chokepoint_boundary_fit_certificate.txt`](../logs/runner-cache/mirror_chokepoint_boundary_fit_certificate.txt)

**Canonical archival log:** [`logs/2026-04-03-mirror-chokepoint-boundary-canonical-n60-r5p0.txt`](../logs/2026-04-03-mirror-chokepoint-boundary-canonical-n60-r5p0.txt)

## Setup

- strict layer-1 chokepoint connectivity
- `NPL_HALF = 60` (`120` total nodes per layer)
- `connect_radius = 5.0`
- `layer2_prob = 0.0`
- `k = 5.0`
- `16` seeds
- retained `N = 40, 60, 80, 100`
- gravity wall at `N = 120`

The registered certificate replays this literal command before applying any
fit:

```bash
python3 scripts/mirror_chokepoint_joint.py --npl-half 60 --connect-radius 5.0 --n-layers 40 60 80 100 120 --layer2-prob 0.0
```

## Selection Firewall

The finite card is selected by the setup and the pre-fit retention gates, not
by the exponent. The gates are:

1. the replay header is `NPL_HALF=60 (total 120), k=5.0, 16 seeds`;
2. each retained mirror row has all `16` successful seeds;
3. each retained row has Born `|I3|/P < 1e-10`;
4. each retained row has `|k=0| <= 1e-12`;
5. each retained row has positive gravity with `gravity / SE > 2`;
6. each retained row has `pur_cl < 0.95`;
7. the `N = 120` mirror row has zero gravity and is excluded before fitting.

Only after those gates are fixed is the exponent computed from
`1 - pur_cl` on `N = 40, 60, 80, 100`.

## Retained Rows

The bounded boundary pocket is Born-clean, `k=0`-clean, gravity-positive, and
decohering through `N = 100`:

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | gravity/SE | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 40 | `0.6884` | `0.8608±0.03` | `0.9850` | `+4.7499±0.666` | `7.13` | `<1e-10` | `0.00e+00` |
| 60 | `0.4791` | `0.8440±0.03` | `0.9953` | `+3.9733±0.473` | `8.40` | `<1e-10` | `0.00e+00` |
| 80 | `0.4291` | `0.8182±0.03` | `1.0029` | `+3.0551±0.672` | `4.55` | `<1e-10` | `0.00e+00` |
| 100 | `0.2308` | `0.9043±0.02` | `1.0058` | `+1.3089±0.570` | `2.30` | `<1e-10` | `0.00e+00` |

`N = 120` is the wall row for this card: the replay returns mirror gravity
`+0.0000±0.000`, so the row is not retained and is not included in the fit.

## Canonical Decoherence Fit

Fit on the retained rows only, using `1 - pur_cl`. With
`x_i = log(N_i)` and `y_i = log(1 - pur_cl(N_i))`, ordinary least squares gives
`y = log(A) + alpha x`, hence `1 - pur_cl = A N^alpha`:

```text
(1 - pur_cl) = 0.3901 × N^(-0.245)
R² = 0.126
```

The registered certificate recomputes the unrounded values from the retained
rows:

```text
A = 0.3900585585
alpha = -0.2453900421
R² = 0.1258401054
```

The resulting illustrative extrapolations are:

```text
pur_cl = 0.95 at N = 4.321958e3
pur_cl = 0.99 at N = 3.048489e6
```

The retained values are non-monotone and the fit quality is poor. The
extrapolations are therefore only arithmetic consequences of the weak
four-point summary; they are not predictions and are not evidence for an
asymptotic law.

## Closure Chain

1. The primary certificate runner replays the companion mirror runner on the
   fixed dense boundary command.
2. The pre-fit retention gates certify the mirror rows `N = 40, 60, 80, 100`
   as Born-clean, `k=0`-clean, gravity-positive with `gravity / SE > 2`, and
   decohering with `pur_cl < 0.95`.
3. The `N = 120` mirror row has zero gravity, so it is the finite wall and is
   excluded before the fit.
4. Ordinary least-squares regression on `log(1 - pur_cl)` versus `log(N)` for
   the four retained rows gives the quoted `A`, `alpha`, and `R²`.
5. The note makes no claim beyond this finite replay and post-retention
   descriptive fit.

So the safe statement is:

- **mirror boundary pocket on the named card:** yes, through `N = 100`
- **canonical exponent fit:** `alpha = -0.245`, weak
- **gravity wall on the named card:** `N = 120`
- **bounded or asymptotic family law:** no
