# Route Portfolio

## R1: External Static-Energy / Static-Force Bridge

**Status:** cycle-2 complete; bounded support, not retained closure.

Import modern `N_f=2+1` or `N_f=2+1+1` lattice-QCD static-energy data,
but only after choosing the observable:

- `r0`, `r1`, or `r2` force scale;
- pre-breaking `sigma_eff`;
- finite-window static-energy fit `sigma`.

This can produce a retained-with-budget interim statement if the residual
table is clean and B5 is declared honestly.

Cycle 2 result: the bridge is real but bounded. TUMQCD finite-window
`sigma` has a static-potential convention split; CLS `N_f=2+1` `r0`/`r1`
force scales are clean but do not uniquely map back to `sqrt(sigma)`.

## R2: Direct Framework Dynamical Ensemble

**Status:** live but compute-heavy.

Run a `N_f=2+1` dynamical-fermion ensemble at `beta = 6.0` on the
framework substrate with an operator basis that can see both the
unbroken string and broken two-meson channels.

This is conceptually clean but outside a single local cycle.

## R3: B5 First

**Status:** live next science route.

Large-volume pure-gauge Wilson-loop or plaquette scaling can tighten
the framework-to-standard-QCD identification. It does not close B2 by
itself, but it improves any external bridge route.

## Closed Routes

- Rough x0.96 promotion.
- PDG/comparator backsolve.
- Literal asymptotic full-QCD string tension as the target observable.
