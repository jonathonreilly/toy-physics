# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-03
**Status:** corrected checkpoint

## Current architecture read

The repo now supports a narrower but much cleaner story than the older
"gravity law + scalable decoherence" synthesis.

- **Retained unitary core:** the best current propagator remains
  `exp(i k S_spent) / L^p × exp(-0.8 theta^2)`.
- **Gravity signal is real:** statistically positive deflection exists on the
  retained families, but the exact force law is still unresolved.
- **The linear-path ceiling is real:** on the tested path-sum families,
  decoherence capacity decays roughly like `1/N`.
- **Regulation and hard geometry help a lot, but boundedly:** layer
  normalization, modular gap structure, and central-band removal all shift the
  finite-`N` window substantially.
- **Collapse is not an asymptotic rescue:** the earlier positive-exponent
  collapse story was an artifact. Inside the retained hard-geometry lanes,
  collapse behaves like a bounded helper, not a new scaling regime.

## Locked quantitative results

### 1. Gravity signal

On the retained uniform-DAG benchmark family, gravity-like deflection is
statistically real, peaking at:

- `N = 30`: `5.1 SE`

What is **retained** after cleanup:

- controlled fixed-geometry distance response has a real peak and falling tail
- best controlled tail fit:
  - `delta ~= C * b^-1.545`
  - `R^2 = 0.943`
- controlled fixed-anchor mass window is positive and sublinear:
  - `delta ~= 0.2872 * M^0.678`
  - `R^2 = 0.954`

What is **not retained**:

- exact `1/b^2` as a locked law
- exact `F ∝ M` as a locked law

Reference:
- [GRAVITY_LAW_CLEANUP_NOTE.md](/Users/jonreilly/Projects/Physics/docs/GRAVITY_LAW_CLEANUP_NOTE.md)

### 2. Linear decoherence ceiling

For the linear path-sum / CL-bath lane:

- `(1 - pur_min) = 1.64 × N^-1.01`
- `R^2 = 0.83`

So the clean current read is:

- decoherence capacity decays roughly like `1/N`
- the ceiling is a property of the path-sum architecture, not just a weak bath

### 3. Born-clean regulated propagator

Per-layer normalization survives the corrected Sorkin harness on the retained
unitary lanes and materially improves the finite-`N` decoherence floor.

Representative row:

- `N = 80`
  - linear: `pur_min = 0.982`, `|I3|/P ≈ 1e-15`
  - layer norm: `pur_min = 0.948`, `|I3|/P ≈ 4e-16`

This is a real prefactor/window gain, not an asymptotic escape.

### 4. Strongest bounded unitary stack

The strongest current bounded unitary lane is still modular hard geometry
plus layer norm.

Retained combined fit:

- `(1 - pur_min) = 5.88 × N^-0.88`
- `R^2 = 0.946`

Representative rows:

- `N = 25`: `pur_min = 0.603`
- `N = 100`: `pur_min = 0.892`

The effect is large and very clean, but it still decays.

### 5. Dense central-band hard-geometry pocket

The central-band `|y| < 2` lane is now a real dense, corrected-Born-safe
pocket.

On the corrected chokepoint Sorkin harness at `npl = 60`:

- `N = 80`, `LN + |y|`: `|I3|/P = 3.70e-17`, max `3.33e-16`
- `N = 80`, `LN + |y| + collapse`: `4.32e-17`, max `6.66e-16`
- `N = 100`, retained seed rows also stay at machine precision

This is density-sensitive and should be read as a bounded pocket, not a
universal law.

References:
- [CENTRAL_BAND_BORN_DENSE_SWEEP_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_BORN_DENSE_SWEEP_NOTE.md)
- [CENTRAL_BAND_BORN_LARGEN_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_BORN_LARGEN_NOTE.md)

### 6. Dense same-graph joint coexistence

The strongest clean same-graph hard-geometry coexistence row currently is:

- `N = 60`, dense central-band pocket
  - `LN + |y|`: Born `0`, `pur_min = 0.875 ± 0.125`, gravity `+0.455 ± 0.384`
  - `LN + |y| + collapse`: Born `0`, purity `0.550 ± 0.082`, gravity `+0.454 ± 0.385`

This is a real bounded coexistence result:

- corrected Born survives
- the decoherence floor improves
- gravity stays positive on the same graph family

Reference:
- [CENTRAL_BAND_DENSE_JOINT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_DENSE_JOINT_NOTE.md)

### 7. Gravity-side mass window inside hard geometry

Hard geometry also improves the gravity-side mass window on the denser slice.

Best retained row:

- `N = 100`, pruned LN:
  - `delta ~= 0.4704 * M^0.595`
  - `R^2 = 0.828`

This is useful and real, but still a bounded window, not a final law.

Reference:
- [CENTRAL_BAND_MASS_WINDOW_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_MASS_WINDOW_NOTE.md)

### 8. Generated asymmetry-persistence lane

The generated asymmetry-persistence lane remains alive, but more narrowly.

Retained pieces:

- it improves the unitary decoherence lane on dense generated graphs
- a narrow dense corrected-Born probe at `N = 100`, `npl = 60`,
  thresholds `0.10` and `0.20` keeps
  `persistence`, `persistence + LN`, and `persistence + LN + collapse`
  at machine precision

This is enough to keep the lane live, but not enough yet to promote it as a
full asymptotic answer.

Reference:
- [ASYMMETRY_PERSISTENCE_BORN_NOTE.md](/Users/jonreilly/Projects/Physics/docs/ASYMMETRY_PERSISTENCE_BORN_NOTE.md)

## What closed

These earlier claims are no longer retained:

- exact `1/b^2` as a locked gravity law
- exact `F ∝ M` as a locked mass law
- collapse positive exponent / asymptotic escape
- generic statement that plain layer norm is always Born-clean independent of
  geometry

The collapse correction is especially important:

- the apparent positive exponent was dominated by averaging artifacts
- inside the retained hard-geometry lanes, collapse helps finitely but still
  trends back toward the same ceiling

## Best current interpretation

The strongest current picture is:

1. **hard geometry is the shared enabler**
2. **layer norm is the best clean regulator**
3. **collapse can help inside the right geometry, but does not rescue the
   asymptotics**

So the project is now best read as:

- a strong bounded emergence program with multiple clean coexistence lanes
- a sharpened gravity signal with unresolved exact force law
- a universal path-sum ceiling that future mechanisms must either derive or
  genuinely break

## Main frontier

The next serious questions are:

1. can the generated asymmetry-persistence lane be promoted from a narrow
   dense Born probe to a broader retained pocket?
2. can the dense same-graph central-band lane be extended cleanly beyond the
   current `N = 60` coexistence row?
3. is the `1/N`-style ceiling provable from the path-sum structure, or is
   there still one architecture left that can truly change the exponent?
