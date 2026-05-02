# Triple-Stack Collapse Scaling Note

**Status:** bounded - bounded or caveated result note
This note records the corrected scaling pilot for the stacked hard-geometry lane:

- linear baseline
- stochastic collapse alone
- `LN + |y|` removal
- `LN + |y| + collapse`

The run used the same 3D hard-geometry setup across `N = 25, 40, 60, 80, 100` with `8` seeds and `10` realizations per seed. The corresponding script is [`scripts/triple_stack_collapse_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/triple_stack_collapse_scaling.py).

## What The Run Shows

The hard-geometry lane is the strongest finite-`N` purity improvement, but the collapse term does **not** reverse the asymptotic direction. All four modes still fit a decay in `1 - purity` with increasing `N`.

### Best retained finite-`N` result

The strongest retained purity floor is the triple stack at small `N`:

- `N = 25`
  - linear: `purity = 0.9472`
  - collapse: `0.9302`
  - `LN + |y|`: `0.7160`
  - `LN + |y| + collapse`: `0.7075`

So the triple stack gives the lowest purity at the smallest `N` tested, but the gain is still bounded.

### Scaling summary

Power-law fits for `(1 - purity)`:

- linear: `1.432e+00 * N^-0.911`, `R^2 = 0.628`
- collapse: `1.095e+00 * N^-0.803`, `R^2 = 0.864`
- `LN + |y|`: `4.277e+00 * N^-0.805`, `R^2 = 0.769`
- `LN + |y| + collapse`: `3.638e+00 * N^-0.754`, `R^2 = 0.788`

Interpretation:

- `LN + |y|` and `LN + |y| + collapse` improve purity at all tested `N` relative to the linear baseline.
- Adding collapse inside the hard-geometry lane gives a small finite-`N` improvement over `LN + |y|` alone.
- The collapse story does **not** survive as a positive-exponent escape from the ceiling in this lane.
- The best read is that collapse is a bounded helper inside the hard-geometry geometry, not a new asymptotic regime.

## Strongest Retained Quantitative Result

The strongest retained quantitative result from this pilot is:

- `LN + |y| + collapse` at `N = 25`: `purity = 0.7075`
- `LN + |y| + collapse` at `N = 100`: `purity = 0.8835`

That is the best triple-stack purity floor in the tested range, but it remains a finite-`N` gain rather than an asymptotic reversal.

## Log

The run output was captured in:

- [`logs/2026-04-02-triple-stack-collapse-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-02-triple-stack-collapse-scaling.txt)
