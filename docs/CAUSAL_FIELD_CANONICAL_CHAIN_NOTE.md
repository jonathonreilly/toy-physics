# Causal Field: Canonical Retained Chain

**Date:** 2026-04-06
**Status:** retained package — six observables, honest mimic control

## What this chain contains

The causal propagating field lane has six retained observables, three
honest controls, and one honest mimic correction. All are portable
across three independent grown families.

## Retained observables

### 1. Shapiro phase delay (primary lab-facing observable)
- Phase lag at c=0.5: +0.062 rad, scaling as s^1.000 (linear in mass)
- Portable: 0.4% agreement across 3 families
- Chromatic: proportional to k (wavenumber)
- NO static field reproduces a c-dependent phase shift
- **This is the strongest unique causal discriminator**

### 2. Gravitomagnetic correction
- Moving source produces antisymmetric phase shift: +0.003 at v=+0.2
- Portable: 3 families agree within 12%
- Antisymmetry residual < 10% of signal

### 3. Causal-escape window
- At eta=20, s=0.004: inst trapped (0.39), dyn escapes (0.97)
- Portable: 3 families, 0.2% agreement
- **BUT**: exposure-matched static mimic ALSO escapes (0.987)
- The escape mechanism is average-exposure reduction, not cone geometry

### 4. Boundary law
- eta_max(c) where dyn drops to 0.85: scales as ~1/c^2
- S-dependence: protection ratio 1.3 (s=0.001) to 33 (s=0.016)

### 5. Causal cone deflection ratio
- Dynamic(c=0.5)/instantaneous = 0.45 (stable across families)
- Theoretical prediction (NL-gl)/NL = 0.667 for forward-only

### 6. Complex action coexistence
- Shapiro delay amplified 10% by gamma=0.5 (complex action)
- The two observables are weakly coupled but independent

## Honest controls

1. **Zero field**: all observables = 0 or 1.0 (exact null)
2. **Seed robustness**: 4 seeds agree to 2%
3. **Family portability**: 3 families agree to 0.4% (Shapiro)

## Honest mimic correction

The exposure-matched static proxy (uniform per-layer field with same
average as the dynamic cone) reproduces the causal-escape window.
The escape mechanism is quantitative exposure reduction, not qualitative
cone geometry.

The Shapiro phase lag is NOT reproducible by any static field. It remains
the strongest unique causal discriminator.

## Lab bridge

The Shapiro phase delay is the most experimentally accessible observable:
- It's a phase shift proportional to GM
- It depends on the field propagation speed c
- It could be measured in a matter-wave interferometer where the two
  paths differ in gravitational exposure
- The model predicts: phase = k * s * geometric_factor / c_function

The diamond sensor / tabletop gravity experiment lane (Codex's brainstorm)
could target this specific observable.

## Artifact chain

| Observable | Script | Log | Note |
| --- | --- | --- | --- |
| Shapiro delay | shapiro_delay_portable.py | 2026-04-06-shapiro-delay-portable.txt | SHAPIRO_DELAY_NOTE.md |
| Gravitomagnetic | gravitomagnetic_portable.py | 2026-04-06-gravitomagnetic-portable.txt | GRAVITOMAGNETIC_NOTE.md |
| Causal escape | causal_escape_window.py | — | CAUSAL_ESCAPE_WINDOW_NOTE.md |
| Boundary law | causal_escape_boundary_law.py | — | (in escape note) |
| Causal cone | causal_propagating_field.py | — | CAUSAL_PROPAGATING_FIELD_NOTE.md |
| Kernel vs gravity | complex_action_kernel_vs_gravity.py | 2026-04-06-kernel-vs-gravity.txt | KERNEL_VS_GRAVITY_NOTE.md |
