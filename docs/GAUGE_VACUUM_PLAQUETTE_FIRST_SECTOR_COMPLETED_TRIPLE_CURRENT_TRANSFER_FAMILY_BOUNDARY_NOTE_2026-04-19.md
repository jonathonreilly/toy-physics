# Gauge-Vacuum Plaquette First-Sector Completed Triple Current Transfer-Family Boundary

**Date:** 2026-04-19 (originally); 2026-05-03 (dense-grid certificate added); 2026-05-10 (scope-narrowed per audit verdict)
**Claim type:** no_go
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py`](../scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py) (dense-grid sampled certificate, PASS=3, FAIL=0)
**Companion runner:** [`scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py`](../scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py) (original local-perturbation check)

## Claim

On the explicit `1440`-point dense grid covering the audited parameter
box

```text
tau_transfer  in [10^-4, 5e-2]   (6 log-spaced points)
tau_boundary  in [0.5, 4.0]      (6 linearly-spaced points)
asym_decay    in [10^-8, 10^-4]  (5 log-spaced points)
linear_decay  in [0.05, 1.0]     (8 linearly-spaced points)
```

at the explicit `beta = 6` `spatial_pair` witness, no sampled grid
point realizes the completed first-sector triple

```text
Z^min = (0.135165279562..., 0.374012880009..., 0.543843858544...)
```

exactly. The minimum sampled gap is

```text
||c_best Z^hat_best - Z^min||_2 = 7.791551e-03,
```

attained at the boundary corner

```text
(tau_transfer = 1e-4, tau_boundary = 4.0, asym_decay = 1e-8, linear_decay = 0.3214).
```

This is an empirical sampled-grid no-go on the listed grid, with a
strictly positive minimum gap and no sampled point inside the box
producing a smaller gap.

## Scope

This note is restricted to:

- the explicit `1440`-point dense grid above;
- the explicit `beta = 6` `spatial_pair` witness family;
- the optimal-scalar fitting routine in `gap_at` of the source runner.

The dense-grid argmin coincides with the stated boundary corner across
all four sampled directions, and the minimum gap reproduces the
original 1D-search result (`7.58e-03`) within rounding / grid
resolution.

## Open derivation gap

The continuous-parameter no-go over the audited parameter box is **not**
established by this note. The auditor verdict was explicit:

> However, the note's stronger no-realization conclusion over the
> audited parameter box is not established by a finite dense grid
> alone, and the note itself admits the dense grid is not a symbolic or
> interval-arithmetic global certificate. Therefore the chain does not
> close for the continuous-family no-go claim, though it does support a
> narrower empirical sampled-grid claim.

Closing the continuous no-go would require one of:

- an interval-arithmetic / Lipschitz-bound certificate on `gap_at`
  showing the minimum gap is bounded below by a strictly positive
  constant on the full continuous parameter box;
- an analytic monotonicity / global-minimum theorem on the box; or
- a certified deterministic optimizer with a numerically rigorous
  global lower-bound output.

That remains genuine open derivation work and is **not** closed by this
note.

## Empirical evidence

Result of the dense-grid certificate run (PASS=3 FAIL=0):

```text
swept 1440 grid points in 0.4 s
min gap                     = 7.791551e-03
median gap                  = 2.039034e-01
max gap                     = 2.856130e-01
fraction below stated gap   = 0.0000
argmin grid point:
  tau_transfer = 1.0000e-04   (lower edge of box)
  tau_boundary = 4.0000        (upper edge of box)
  asym_decay   = 1.0000e-08    (lower edge of box)
  linear_decay = 0.3214        (interior)
```

Allowing the free overall scalar that the evaluator route leaves open,
the best sampled fit on the current `spatial_pair` witness family to
the explicit completed triple comes from the normalized family vector

```text
Z^hat_best = (0.280527830070..., 0.789850309412..., 1.120725632470...)
```

with optimal overall scale `c_best = 0.481383963846...`, so the best
sampled scaled fit is

```text
c_best Z^hat_best = (0.135041598808..., 0.380221272789..., 0.539499347342...)
```

with gap

```text
c_best Z^hat_best - Z^min = (-0.000123680754..., 0.006208392780..., -0.004344511202...).
```

## Meaning

This sharpens the remaining plaquette seam one level further on the
sampled grid:

- the first symmetric seam closes positively to `Z^min`;
- the full framework-point packet is still open;
- the current audited explicit `spatial_pair` witness family does
  **not** realize `Z^min` at any sampled grid point, so on the listed
  grid that family remains only a boundary ansatz rather than the
  missing exact realization.

The continuous-family no-go remains an open derivation gap as recorded
above.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py
```

Expected:

```text
SUMMARY: PASS=3, FAIL=0
```

The three runner checks certify the empirical sampled-grid statement
above; they do not certify the continuous-parameter no-go that the
audit verdict flagged as the load-bearing failure.

The companion runner
[`scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py`](../scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py)
provides the original local-perturbation check at the stated boundary
corner.
