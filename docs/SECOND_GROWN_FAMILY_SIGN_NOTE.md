# Second Grown Family Signed-Source Note

**Status:** bounded - bounded or caveated result note
This note records a genuinely different grown-family slice from the retained drift/restore neighborhood:

- family: no-restore Gate B grown geometry
- connectivity: geometry-sector stencil
- controls: exact zero-source baseline, exact neutral `+1/-1` cancellation
- observables: sign orientation, weak charge scaling

The question was whether the signed-source fixed-field package survives on a second independent grown family, not just another nearby row of the retained drift/restore basin.

## Result

The sweep passed on all tested rows:

- drift values: `0.0, 0.1, 0.2, 0.3, 0.5`
- seeds: `0, 1, 2`
- total: `15/15` rows passed

Key retained behavior:

- zero-source baseline stayed exactly zero
- neutral `+1/-1` cancellation stayed exact
- `+q` and `-q` had opposite sign response
- the weak charge exponent stayed near linear

Summary statistics:

- mean charge exponent over passing rows: `1.000072`
- drift coverage among passes: `[0.0, 0.1, 0.2, 0.3, 0.5]`

## Interpretation

This is a real second grown-family basin candidate.
It is structurally distinct from the retained drift/restore neighborhood because it fixes `restore = 0` and varies drift instead.

The result is still narrow:

- it supports the signed-source fixed-field package on this second family slice
- it does not yet claim geometry-generic closure
- it does not by itself imply the same family carries the complex-action companion or other retained mechanisms

The honest retained claim is therefore:

- the signed-source package now survives on a second independent grown family
- this second family is the no-restore geometry-sector slice
- the result is positive, but not yet broad enough to generalize beyond the tested family
