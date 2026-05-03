# Gauge-Vacuum Plaquette First-Sector Completed Triple Current Transfer-Family Boundary

**Date:** 2026-04-19  
**Status:** support - structural or confirmatory support note
completion; on the audited current explicit `beta = 6`
`spatial_pair` witness family, even the best scaled fit still does not realize
the completed triple `Z^min` exactly  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py` (**MISSING — flagged for re-audit**)

> **Missing primary runner (2026-05-03 audit-repair scan):**
> The script above is referenced as this note's primary runner but does not
> exist in the current `scripts/` tree. Sibling notes in the same lane were
> archived to `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`;
> this note is left active pending a runner-rewrite decision. The audit
> verdict on this note will be redone once a working runner is registered
> or the note is moved to archive.

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
