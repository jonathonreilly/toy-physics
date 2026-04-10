# Chiral Split-Mass / Split-Gravity Note

This note captures the bottleneck experiment for the chiral walk:

- Baseline overload hypothesis: the same `theta_m` sets the free dispersion gap and the local gravity response.
- Split hypothesis: `theta_m` sets the free gap, while `g` independently scales the local field coupling.

Why this matters:

- The current matrix has already shown that 1D and 2D chiral transport can preserve norm, Born-style complementarity, and linear field scaling.
- The remaining question is whether the gravity response is being artificially tied to the inertial parameter through a single coin-angle control.
- If the split model flattens the `theta_m` sweep while preserving KG and `F ∝ M`, then overloading `theta_m` is a genuine bottleneck.

Recommended early-warning tests for the 10-card:

1. `theta_m`-sweep at fixed `g`
   - Measure the gravity-induced centroid shift across several `theta_m` values.
   - Fail if the response slope changes sharply when only inertial mass changes.

2. `g`-sweep at fixed `theta_m`
   - Keep the free gap fixed and vary only susceptibility.
   - Pass if the deflection stays linear in `g` and free dispersion stays unchanged.

3. `k`-sweep at fixed `theta_m`
   - Use a fixed carrier `k` set and compare baseline vs split `CV`.
   - This catches whether the model is still chromatic at the operating point.

4. Observable-consistency row
   - Compare centroid, peak, and first-arrival observables on the same run.
   - This catches torus-wrapping and recurrence artifacts early.

5. Coupled-coin leakage row
   - In 3D, check whether a factorized coin leaks into axis-pair separability.
   - This is the earliest warning for the 3D KG / gauge failures.

6. Torus-aware recurrence row
   - Sweep `L/n` and `offset/n` on periodic lattices.
   - This catches the sign-window issue before it is mistaken for a physics law.
