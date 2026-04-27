# Hubble H_0 — Literature Bridges

**Workstream:** `hubble-h0-20260426`
**Literature mode:** `--literature` enabled (per user invocation).

This file records every external literature value, theorem, or convention used
in the workstream, with its role.

## Conventions admitted

- **Standard textbook FRW cosmology** (Friedmann equations, density scalings,
  flat-curvature decomposition, late-time geodesic / distance-redshift
  relations). Reference: Weinberg, *Cosmology* (2008); Dodelson, *Modern
  Cosmology* (2nd ed.).
  Role: admitted convention. Used as the structural surface on which the
  retained `Lambda = 3/R_Lambda^2` and matter-bridge identities are read.

- **Big-Bang Nucleosynthesis (BBN)** mapping `eta -> Omega_b` at percent level.
  Reference: Cyburt, Fields, Olive, Yeh, *Rev. Mod. Phys.* 88, 015004 (2016).
  Role: admitted convention. Used in the bounded `Omega_b` cascade only;
  not used by the Cycle-1 structural lock theorem.

- **Sommerfeld enhancement formula** for DM annihilation cross-section.
  Reference: textbook (e.g., Hisano et al., *Phys. Rev. D* 67, 075014, 2003).
  Role: bridge for the bounded DM relic cascade only; not used by Cycle-1.

## Comparators (used by runners; never derivation inputs)

- **Planck 2018 cosmology results** (Aghanim et al., *Astron. Astrophys.* 641,
  A6, 2020):
  `H_0 = 67.4 ± 0.5 km/s/Mpc`, `Omega_m = 0.315 ± 0.007`,
  `Omega_Lambda = 0.685 ± 0.007`, `Omega_b h^2 = 0.0224`,
  `Omega_r,0 ≈ 9.2 × 10^-5`.
  Role: numerical comparator only. The Cycle-1 runner uses these to verify
  observational consistency of the structural lock; theorem premises are
  framework-internal.

- **SH0ES distance-ladder `H_0`** (Riess et al., *Astrophys. J. Lett.* 934,
  L7, 2022): `H_0 = 73.04 ± 1.04 km/s/Mpc`. Role: comparator for the tension
  framing in the theorem note's discussion section. Never a derivation input.

## Theorems imported

None for Cycle 1. The structural lock theorem rests entirely on retained
framework identities (`w = -1`, `Lambda = 3/R_Lambda^2`, matter-bridge,
inverse reconstruction) plus textbook FRW.

If later cycles need imported theorems, they are recorded here with role:
**bridge**, **comparator**, **admitted convention**, or **non-derivation
context**.

## Boundary statement

No literature value is a derivation input on the retained surface.
Comparators are used in runners' verification phase only. Admitted
conventions sit at the FRW bridge layer between the retained core and the
paper surface; they are flagged on `INPUTS_AND_QUALIFIERS_NOTE.md`.
