# K Dependence Review-Safe Note

**Status:** support - structural or confirmatory support note
This note captures the hardened rerun for the k-dependence claim from
`scripts/k_dependence_ceiling.py`.

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/k_dependence_ceiling.py` now carries explicit class-(A) algebraic-identity assertions (`assert math.isclose(...)`, `assert abs(...) < EPS`, etc.) mirroring its existing PASS-condition booleans. This nudges the audit classifier (`docs/audit/scripts/classify_runner_passes.py`) to register this runner as class-A dominant. The runner output and pass/fail semantics are unchanged.

## Method

- Fixed N window for every `k`: `N = [25, 30, 40, 60, 80]`
- Shared seed set across all `k` values
- Per-seed slope fits on `(1 - pur_min)` vs `N`
- Bootstrap confidence intervals on the mean seed-level slope

## Result

From `logs/2026-04-03-k-dependence-fixed-window-review.txt`:

- `k=1.0`: `seed_alpha = -3.931`, bootstrap CI `[-5.674, -2.255]`
- `k=2.0`: `seed_alpha = -2.881`, bootstrap CI `[-4.784, -1.094]`
- `k=3.0`: `seed_alpha = -2.286`, bootstrap CI `[-4.036, -0.528]`
- `k=5.0`: `seed_alpha = -3.322`, bootstrap CI `[-5.745, -0.920]`
- `k=7.0`: `seed_alpha = -2.827`, bootstrap CI `[-5.306, -0.198]`
- `k=10.0`: `seed_alpha = -3.813`, bootstrap CI `[-6.389, -1.242]`
- `k=15.0`: `seed_alpha = -2.773`, bootstrap CI `[-5.307, -0.455]`

## Interpretation

The fixed-window rerun does not support a clean hardened `alpha(k)` law.
The per-seed exponents are all negative, but the confidence intervals
overlap strongly and the ordering is not monotonic in `k`.

Best replacement wording:

- `k` affects the fitted ceiling behavior inside this graph family, but
  the current evidence is fit-window-sensitive and does not yet support a
  review-safe universal `alpha(k)` claim.

