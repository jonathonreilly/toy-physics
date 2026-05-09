# DM Candidate Mass Window Theorem

**Date:** 2026-04-19
**Status:** **bounded support theorem on the open DM gate** - framework `M_N`
is in the leptogenesis-viable window; the current one-flavor transport gap
corresponds to a non-integer `ALPHA_LM` power shift not closeable by a single
power-law step
**Runner:** `scripts/frontier_dm_candidate_mass_window_theorem.py` ([scripts/frontier_dm_candidate_mass_window_theorem.py](../scripts/frontier_dm_candidate_mass_window_theorem.py))
**Runner result:** `PASS = 15, FAIL = 0`

## Inputs (cited authorities)

The framework mass values `(M1, M2, M3)` and the one-flavor transport
ratio `η/η_obs = 0.189` are imported from the upstream DM neutrino lane;
this note does **not** re-derive the `ALPHA_LM` power-law generator or
the exact-kernel closure. The cited authorities are:

- [`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)
  — the exact source-and-CP-channel package and the consistent
  benchmark `η/η_obs ≈ 0.558` heavy-basis number; this note's
  one-flavor `0.189` is the radiation-branch projection.
- [`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
  and [`DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md)
  — the upstream `ALPHA_LM` power-law `(k_A, k_B)` generators that
  fix the `(M1, M2, M3)` spectrum entries.
- [`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md)
  — the upstream cosmology-side mass-spectrum reading on the same
  `ALPHA_LM` ladder.

The Davidson-Ibarra bound `M_DI ≈ 2.4 × 10^8 GeV` is a literature input
(Davidson-Ibarra 2002), not a framework derivation; this note imports it
to characterise viability and does not claim its derivation. The
transport-gap factor and the `M_N_target = 4.002 × M1` ratio are
characterisations of the imported numbers, not new first-principles
derivations from physical `Cl(3)` on `Z^3`. The bounded scope is the
power-law-position characterisation `k_target ≈ 7.44`, which is
arithmetic over the imported values.

## What this theorem establishes

The framework derives the heavy right-handed neutrino (DM candidate) mass
spectrum from the `ALPHA_LM` running-coupling power laws:

| Field | Power | Mass (GeV) | Role |
|-------|-------|-----------|------|
| M1 | k_B = 8 | 5.323 × 10¹⁰ | Lightest RHN — leptogenesis source |
| M2 | k_B = 8 | 5.829 × 10¹⁰ | Quasi-degenerate with M1 |
| M3 | k_A = 7 | 6.150 × 10¹¹ | Heaviest RHN |

The theorem characterises four properties of this spectrum:

**(a) Davidson-Ibarra viability.** M1/M_DI = 222, where M_DI ≈ 2.4 × 10⁸ GeV
is the Davidson-Ibarra lower bound on M_N for successful leptogenesis with a
hierarchical spectrum. The entire spectrum is above this bound. Leptogenesis
is viable.

**(b) Transport gap.** The exact one-flavor radiation-branch transport chain
gives η/η_obs = 0.189 at M1. The factor-5.30 deficit below observation is a
structural result of the current framework transport law.

**(c) Transport-implied target mass.** The unique M_N_target at which
η/η_obs = 1 (under fixed CP structure, with all other transport factors held
constant) is:

```
M_N_target = 2.130 × 10¹¹ GeV = 4.002 × M1_framework
```

**(d) Non-integer power-law position.** M_N_target corresponds to the
non-integer ALPHA_LM power k_target ≈ 7.44, which lies between the integer
lattice nodes k = 7 (M3 scale, 6.15 × 10¹¹ GeV) and k = 8 (M1 scale,
5.58 × 10¹⁰ GeV). The gap is NOT closeable by a single integer power step.

## Proof structure

### Transport chain factorisation

The baryon asymmetry formula on the one-flavor radiation branch is:

```
η = (s/n_γ) × C_sph × d_N × ε_1 × κ_axiom(k_decay)
```

where:
- `(s/n_γ) = 7.039`, `C_sph = 28/79`, `d_N = 0.003901` — pure cosmology
- `ε_1 = 2.458 × 10⁻⁶` — CP asymmetry from framework-derived Yukawa structure
- `κ_axiom(k_decay) = 0.004830` — washout efficiency at k_decay = 47.24
- `k_decay = m̃/m★` where `m̃ ∝ 1/M1`

The prefactor A = (s/n_γ) × C_sph × d_N × ε_1 / η_obs = 39.09 is
**constant in M1** (ε_1 depends only on mass ratios and fixed Yukawa
structure). Therefore:

```
η/η_obs = A × κ_axiom(k_decay(M1))
```

The only M1-dependence is through `k_decay ∝ 1/M1`. Since `κ_axiom` is a
monotone decreasing function of k_decay (more washout at larger k_decay), a
larger M1 gives smaller k_decay and larger κ_axiom — approaching the
observational target.

### Target mass computation

Setting η/η_obs = 1 requires κ_axiom(k_target) = 1/A = 0.02558. Solving the
Boltzmann transport integral:

```
k_target = 11.80  (from numerical inversion of κ_axiom)
M_N_target = M1 × (k_decay_fw / k_target) = 5.323 × 10¹⁰ × (47.24 / 11.80)
           = 2.130 × 10¹¹ GeV
```

### Power-law bracket

```
M_PL × ALPHA_LM^7 = 6.150 × 10¹¹ GeV  (k=7, overshoots by factor 2.89)
M_N_target         = 2.130 × 10¹¹ GeV  (k_target = 7.44, non-integer)
M_PL × ALPHA_LM^8 = 5.576 × 10¹⁰ GeV  (k=8, undershoots by factor 0.26)
```

M_N_target requires a non-integer power k ≈ 7.44. This is not at an integer
ALPHA_LM lattice node.

## Structural interpretation

The transport gap is a genuine structural feature:

1. **Not a viability failure.** The framework M1 is 222× above the
   Davidson-Ibarra bound, so leptogenesis is kinematically viable. The
   factor-5.3 deficit is not a sign that leptogenesis fails but that the
   one-flavor radiation-branch chain undershoots observation.

2. **Not closeable by a simple power step.** k = 7 (M3 scale) would
   overshoot by a factor ~2.9; k = 8 (M1 scale) undershoots by a factor
   ~3.8. The target sits between two consecutive integer lattice nodes.

3. **Gap signals either multi-flavor correction or non-power-law prescription.**
   Closing the gap could require: (a) multi-flavor washout contributions not
   included in the one-flavor chain; (b) a non-power-law selection of M_N
   from the framework; or (c) additional CP phase contributions.

4. **DM candidate mass scale is fixed on the current route.** Regardless of
   the transport gap, the framework derives `M_N = M1 = 5.32 × 10^10 GeV` as
   the current DM-candidate (lightest right-handed neutrino) mass scale on the
   live `ALPHA_LM` power-law route.

## Summary table

| Quantity | Value | Status |
|----------|-------|--------|
| M_N = M1 (framework) | 5.323 × 10¹⁰ GeV | DERIVED from k_B=8 power law |
| M_N / M_DI | 221.8 | PASS: leptogenesis viable |
| η/η_obs at M_N | 0.1888 | SUPPORT: undershoots by 5.30× |
| M_N_target | 2.130 × 10¹¹ GeV | COMPUTED: k_decay inversion |
| k_target | 7.44 | NON-INTEGER: gap is structural |

## What this theorem does NOT claim

- Does not close the transport gap (that remains an open structural deficit).
- Does not derive the leptogenesis washout from the Cl(3)/Z³ axiom directly
  (the one-flavor radiation-branch formula is an established approximation).
- Does not determine whether multi-flavor corrections would close the gap.
- Does not pin the absolute neutrino mass scale (different carrier).

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_candidate_mass_window_theorem.py
```

Expected: `PASS = 15, FAIL = 0`.
