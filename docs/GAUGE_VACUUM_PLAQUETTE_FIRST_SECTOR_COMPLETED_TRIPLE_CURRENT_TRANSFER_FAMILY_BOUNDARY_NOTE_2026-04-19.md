# Gauge-Vacuum Plaquette First-Sector Completed Triple Current Transfer-Family Boundary

**Date:** 2026-04-19 (originally); 2026-05-03 (dense-grid global certificate added)
**Status:** support — on the audited current explicit `beta = 6` `spatial_pair` witness family, dense-grid global search confirms even the best scaled fit does not realize the completed triple `Z^min` exactly
**Original runner:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py`
**Dense-grid global certificate (2026-05-03 audit repair):** `scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py`

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (fresh-agent-gauge-triple-transfer-boundary)
flagged that the original runner fixes the boundary corner
(`tau_transfer = 10^-4, tau_boundary = 4.0, asym_decay = 10^-8`) and
checks only local inward perturbations: "a positive residual at one
preselected boundary corner does not rule out an exact or smaller-gap
realization elsewhere in the audited parameter box."

This repair adds a **dense parameter-box global gap certificate**
[`scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py`](../scripts/gauge_vacuum_completed_triple_dense_box_certificate_2026_05_03.py)
that sweeps a `6 × 6 × 5 × 8 = 1440`-point structured grid across
the full audited parameter box (`tau_transfer × tau_boundary ×
asym_decay × linear_decay`) and reports the global minimum gap.

Result of the certificate run (PASS=3/3):

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

The dense-grid argmin coincides with the stated boundary corner
(lower `tau_transfer`, upper `tau_boundary`, lower `asym_decay`),
the minimum gap `7.79e-03` reproduces the original 1D-search result
`7.58e-03` within rounding/grid-resolution, and **no grid point
yields a smaller gap**. The "boundary corner is globally minimizing"
claim is now backed by a 1440-point dense-grid empirical certificate,
not just a local-perturbation check.

The dense grid is **not** a symbolic / interval-arithmetic global
certificate (which would be a stronger guarantee); that remains
genuine open work. The empirical confidence is: dense-grid argmin
coincides with the stated boundary corner across 4 dimensions of
the parameter box, and the minimum gap is strictly positive
(`> 1e-6 ≫ 0`).

## Question

Once the first symmetric three-sample seam is closed positively to the explicit
completed triple `Z^min`, does the current explicit spatial-environment
transfer witness family already realize that triple?

## Bottom line

Not on the audited current `spatial_pair` family.

Allowing the free overall scalar left open by the evaluator route, the best
audited fit on the current `spatial_pair` witness family to the explicit
completed triple

`Z^min = (0.135165279562..., 0.374012880009..., 0.543843858544...)`

is still far:

comes from the normalized family vector

`Z^hat_best = (0.280527830070..., 0.789850309412..., 1.120725632470...)`

with optimal overall scale

`c_best = 0.481383963846...`,

so the best audited scaled fit is

`c_best Z^hat_best = (0.135041598808..., 0.380221272789..., 0.539499347342...)`,

with gap

`c_best Z^hat_best - Z^min = (-0.000123680754..., 0.006208392780..., -0.004344511202...)`

and Euclidean norm

`||c_best Z^hat_best - Z^min||_2 = 0.007578536496...`.

Moreover the best audited fit is driven to the parameter-box boundary:

- `tau_transfer = 10^(-4)` (lower audited edge),
- `tau_boundary = 4.0` (upper audited edge),
- `asym_decay = 10^(-8)` (lower audited edge).

So the completed triple is still not realized exactly inside the audited
current explicit witness family.

## Meaning

This sharpens the remaining plaquette seam one level further.

The branch no longer only knows:

- the first symmetric seam closes positively to `Z^min`,
- and the full framework-point packet is still open.

It now also knows:

- the current audited explicit spatial-environment witness family still does
  **not** realize `Z^min` exactly,
- so that family remains only a boundary ansatz rather than the missing exact
  realization itself.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py
```
