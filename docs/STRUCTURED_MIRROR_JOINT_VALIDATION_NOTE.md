**Status:** structured mirror linear joint check saved

Artifacts:
- [`scripts/structured_mirror_joint_validation.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_joint_validation.py)
- [`logs/2026-04-03-structured-mirror-joint-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-structured-mirror-joint-validation.txt)

What this does:
- keeps the structured mirror geometry from
  [`scripts/structured_mirror_growth.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_growth.py)
- replaces the old layer-normalized propagation with a fully linear propagator
- measures the same core bounded observables on that geometry:
  - `d_TV`
  - `pur_cl`
  - gravity
  - Born `|I3|/P`
  - `k=0`

Default saved run:
- `npl_half = 20`
- `d_growth = 2`
- `N = 25, 30, 40`
- `16` seeds
- `connect_radius = 4.5`

Main readout:
- `N=25`: `pur_cl = 0.833±0.013`, gravity `+3.863±0.225`, Born `2.51e-01±9.56e-02`
- `N=30`: `pur_cl = 0.878±0.015`, gravity `+4.904±0.282`, Born `1.71e-01±2.69e-02`
- `N=40`: `pur_cl = 0.932±0.009`, gravity `+6.620±0.181`, Born `1.71e-01±2.47e-02`
- `k=0` stays numerically zero in the saved run

Interpretation:
- The structured mirror geometry is still physically interesting under a linear
  propagator.
- It keeps a positive gravity signal and nontrivial decoherence-side effect.
- But it is **not** Born-clean in this validator, so it should not replace the
  exact mirror or `Z2 x Z2` lanes as the main synthesis headline.

Bottom line:
- structured mirror remains a live geometry idea
- the strongest immediate unification target is still a Born-safe structured
  variant, not the current linearized validator as-is
