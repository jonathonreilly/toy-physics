# Assumptions, Imports, and Forbidden Surfaces

## A_min (retained framework foundation)

`MINIMAL_AXIOMS_2026-04-11.md`:
1. Local Cl(3) algebra
2. Z³ spatial substrate
3. Finite local Grassmann/staggered-Dirac partition (current normal grammar)
4. `g_bare = 1` (gauge-coupling normalization rigidity)

## Retained cosmology surface (used as derivation inputs)

| Identity | Authority |
|---|---|
| `Lambda = 3 / R_Lambda^2` | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| `H_inf = c / R_Lambda` | `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` |
| `w_Lambda = -1` | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` |
| `Omega_Lambda = (H_inf/H_0)^2` | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` |
| FRW kinematic forward reduction | `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md` |
| Open-number reduction (2 dof at fixed R) | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` |
| `H_0(z)` constancy at late times | `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` |
| `N_eff = 3.046` | `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` |

## Admitted observational layer numbers (admitted convention, NOT retained)

Per `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`:
- `T_CMB` (CMB temperature)
- `eta` (baryon-photon ratio)
- `alpha_GUT` (some GUT-scale anchor)
- `R_Lambda`-anchor (cosmological-constant scale anchor)

These enter via `(Omega_r, Omega_b, Omega_DM, scale)` but are not in
the retained variable set `S`.

## Open / unretained inputs relevant to 4F

- **`h = H_0 / (100 km/s/Mpc)`** — currently open in Lane 5;
  depends on (C1) absolute-scale gate + (C2)/(C3) cosmic-L gate.
- **`Ω_b`** — admitted observational layer number.
- **`Ω_DM`** — admitted observational layer number.
- **`Σm_ν`** — primary target; currently unretained.

## Forbidden imports (not used as derivation input)

- Direct PDG observed `Σm_ν` upper bound (cosmological surveys) —
  NOT a derivation input; can be cited as falsifier consistency check
  only.
- Specific Planck `Ω_b h² = 0.02236` value — NOT a derivation input
  (admitted observational layer).
- Specific Planck `Ω_DM h² = 0.1200` value — NOT a derivation input.
- Lane 5 specific `H_0` numerical values — NOT a derivation input
  (Lane 5 closure not yet landed).
- Charged-lepton scale `V_0` — NOT a derivation input
  (research-level distant per Lane 6 closure).

## Status posture

This loop's posture is theorem-plan + gate-audit + Phase-1 stretch
attempt for `Σm_ν` retention. It does not propose to retain a numerical
`Σm_ν` value without parallel-lane progress (Lane 5 h closure).
