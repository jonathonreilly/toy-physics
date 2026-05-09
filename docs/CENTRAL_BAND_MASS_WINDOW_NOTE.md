# Central-Band Mass Window Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_mass_window_summary.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

This note records the gravity-side follow-up to the central-band hard-geometry
lane. The question is narrower than the full joint card:

- does the best retained hard-geometry row give a cleaner mass-response window
  than the plain baseline?

The new summary script is:

- [`scripts/central_band_mass_window_summary.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_mass_window_summary.py)

The intended comparison is on the same graphs and matched seeds:

- plain baseline
- baseline layernorm
- central-band pruned linear
- central-band pruned layernorm

The script keeps the comparison review-safe by:

- using fixed-graph matched seeds
- fixing one mass anchor on the gravity layer
- varying only the mass count `M`
- fitting only the declared positive window

This is a gravity-side summary only. Collapse is handled elsewhere by the
joint card, because including it here would mix a stochastic control into the
mass-law fit.

## What The Summary Shows

The bounded sweep was run at `N = 60` and `N = 100` with `8` matched seeds,
`y_cut = 2.0`, `anchor_b = 5.0`, and the mass counts `M = 1, 2, 3, 5, 8`.

The plain baseline is not a clean mass law on this slice:

- `N = 60`
  - linear: not enough positive points for a stable fit
  - LN: not enough positive points for a stable fit
- `N = 100`
  - linear: `delta ~= 1.7995 * M^-0.522` with `R^2 = 0.559`
  - LN: `delta ~= 1.2016 * M^0.006` with `R^2 = 0.001`

The pruned hard-geometry rows are cleaner:

- `N = 60`
  - pruned linear: `delta ~= 2.0814 * M^-0.412` with `R^2 = 0.726`
  - pruned LN: `delta ~= 1.2087 * M^-0.535` with `R^2 = 0.272`
- `N = 100`
  - pruned linear: `delta ~= 0.6207 * M^0.642` with `R^2 = 0.649`
  - pruned LN: `delta ~= 0.4704 * M^0.595` with `R^2 = 0.828`

## Narrow Conclusion

The gravity-side answer is mixed but useful:

- the central-band hard-geometry row does improve the mass-response window
  relative to the plain baseline on the densest slice we tested
- the cleanest retained mass fit in this sweep is the pruned LN row at
  `N = 100`, which has the best `R^2` of the four modes
- this is still a bounded window, not a full gravity-law rescue

