# Lane 4 Neutrino — Literature Bridges

**Loop:** `neutrino-quantitative-20260428`
**Literature mode:** not enabled in user invocation; can be requested
per cycle if needed.

## Conventions admitted

- **Standard PMNS oscillation framework** (textbook neutrino physics).
  References: Pontecorvo 1957; Maki-Nakagawa-Sakata 1962; PDG (2024).
  Role: admitted convention — substrate for δ_CP, θ_*, Δm² parameter
  definitions.
- **Standard type-I seesaw formalism.** References: Minkowski 1977;
  Yanagida 1979; Gell-Mann-Ramond-Slansky 1979; Mohapatra-Senjanovic
  1980. Role: admitted convention — light-neutrino mass via heavy
  Majorana right-handed neutrinos. (Type-II / Type-III not in initial
  scope.)
- **Majorana mass insertion / 0νββ amplitude formalism.** References:
  Schechter-Valle 1982; PDG. Role: admitted convention — only used to
  state the falsifier of the R2 Dirac global lift.

## Comparators (used by runners; never derivation inputs)

- **PDG / NuFIT global oscillation values:**
  - `Delta m^2_21 = 7.42 × 10^-5 eV^2`
  - `Delta m^2_31 = 2.515 × 10^-3 eV^2` (normal ordering)
  - `theta_12 = 33.45°`
  - `theta_23 = 49.0°` (best-fit; ranges to 51.7°)
  - `theta_13 = 8.62°`
  - `delta_CP = 197°` (best-fit; consistent with framework's `-81°`
    via mod 360°)
  Role: numerical comparator only. Verification phase of any runner.
- **KATRIN absolute mass bound:** `m_β < 0.8 eV` (90% CL).
- **Cosmological Σm_ν bound:** `< 0.12 eV` (Planck + BAO).
- **0νββ effective mass bound (KamLAND-Zen):** `m_ββ < (28-122) meV`.

## Theorems imported

None for Cycle 1.

For Cycle 2 (R2 Dirac global lift): the proof will cite the **Schechter-
Valle theorem** (any positive 0νββ rate implies Majorana mass for at
least one neutrino) only as the falsifier statement, not as a
derivation input.

## Boundary statement

No literature value is a derivation input on the retained surface.
Comparators are used in runners' verification phase only.
