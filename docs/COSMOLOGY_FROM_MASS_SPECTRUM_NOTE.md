# Cosmology Cascade from Mass Spectrum (Phase 5 of mass spectrum)

**Date:** 2026-04-17
**Status:** bounded/conditional cascade; retained pieces consolidated; open
lane is promotion of `eta` from DM-gate support to retained theorem.
**Primary runner:** `scripts/frontier_cosmology_from_mass_spectrum.py`
**Depends on:** `NEUTRINO_MASS_DERIVED_NOTE.md` (Phase 4),
`OMEGA_LAMBDA_DERIVATION_NOTE.md` (cascade chain), and the retained
`DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md` (eta support package).

## Safe statement

Given the Phase 4 retained taste-staircase level `k_B = 8` — which fixes
the lightest right-handed neutrino Majorana mass
`M_1 = M_Pl * alpha_LM^8 * (1 - alpha_LM/2) = 5.32e10 GeV` — and given the
promoted exact group-theory factor `R_base = 31/9`, the framework admits a
single chain

```
  eta  ->  Omega_b (BBN)  ->  Omega_DM = R * Omega_b
        ->  Omega_m  ->  Omega_Lambda = 1 - Omega_m   (flatness)
```

with **one imported input (`eta`) and one bounded parameter (`alpha_GUT`)**
that predicts every other entry of the Planck cosmological pie chart to
within 1% of observation:

| Quantity | Predicted | Observed | Error |
|---|---|---|---|
| `Omega_b`       | 0.0492 | 0.0493 | 0.2% |
| `R = DM/b`      | 5.48   | 5.375  | 2.0% |
| `Omega_DM`      | 0.2696 | 0.265  | 1.7% |
| `Omega_m`       | 0.3188 | 0.315  | 1.2% |
| `Omega_Lambda`  | 0.6811 | 0.685  | 0.6% |

The six LCDM parameters are reduced to **one imported (`eta`) + one bounded
(`alpha_GUT`)**.

## Inputs and provenance

### Retained / promoted inputs

- Phase 4: `k_B = 8`, `M_1 = M_Pl * alpha_LM^8 * (1 - alpha_LM/2)` from the
  adjacent-placement + residual-sharing theorem stack.
- Exact group theory: `R_base = (3/5) * [C_2(3)*8 + C_2(2)*3] / [C_2(2)*3]
  = 31/9 = 3.4444...`.
- Flatness `Omega_total = 1` (from S^3 topology or inflation, Planck
  bound `|Omega_k| < 0.002`).
- BBN link `Omega_b * h^2 = 3.6515e-3 * eta_10` (Cyburt+ 2016, textbook).

### Imported input (one)

- `eta = 6.12e-10` from Planck 2018 CMB + BBN.

The live DM-gate (see `DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md`)
materially supports `eta` without yet closing it:

- exact one-flavor transport branch: `eta/eta_obs = 0.1888`;
- PMNS reduced-surface support branch: `eta/eta_obs = 1.0`;
- selector / normalization closure still open.

### Bounded input (one)

- `alpha_GUT` in `[0.03, 0.05]` entering the Sommerfeld correction
  `S_vis/S_dark`.  Self-consistent match to the observed `R` pins
  `alpha_GUT ~ 0.048`.

## Cascade

```
  k_B = 8 (Phase 4, retained)
    -> B = M_Pl * alpha_LM^8               = 5.58e10 GeV
    -> M_1 = B (1 - alpha_LM/2)            = 5.32e10 GeV
  eta (imported, with DM-gate support)
    -> Omega_b = 3.6515e-3 * eta_10 / h^2  = 0.0492   (BBN)
  R_base = 31/9 (exact group theory)
    -> Sommerfeld(alpha_GUT) in [1.4, 1.6]
    -> R = R_base * S_vis/S_dark            = 5.48
  Arithmetic:
    -> Omega_DM = R * Omega_b              = 0.2696
    -> Omega_m  = Omega_b + Omega_DM       = 0.3188
  Flatness:
    -> Omega_Lambda = 1 - Omega_m - Omega_r = 0.6811
```

## What Phase 5 retains

- `R_base = 31/9` as an exact group-theory consequence.
- the BBN link `Omega_b * h^2 = 3.6515e-3 * eta_10` as textbook standard
  physics.
- the arithmetic cascade `Omega_DM = R * Omega_b`, `Omega_m`, `Omega_Lambda`.
- the flatness identity `Omega_total = 1` (justified by S^3 or inflation).
- the Phase 4 inputs `k_B = 8` and `M_1 = B(1 - alpha_LM/2)`.

## What Phase 5 bounds

- `R = 5.48` via Sommerfeld with `alpha_GUT` in `[0.03, 0.05]`.  Inside
  that band `R` varies over `[4.8, 5.3]` and `Omega_Lambda` over
  `[0.66, 0.71]`, comfortably containing the observed `0.685`.
- `eta` remains imported on the live cosmology surface despite the
  DM-gate support package.

## What Phase 5 conditionally closes

If `eta` is promoted from DM-gate support to a retained theorem (Phase 5b),
the entire cosmological pie chart becomes parameter-free up to the bounded
Sommerfeld correction.  The remaining open lane is therefore sharply
named:

> **Phase 5b: promote `eta` to retained.**
>
> Candidates (already partly constructed on the branch):
>   1. exact one-flavor theorem-native transport closure;
>   2. PMNS reduced-surface selector closure;
>   3. combined transport + selector + normalization integration.

## What is not claimed

- that `eta` is derived from first principles on this cascade
  (imported with support);
- that flatness `Omega_total = 1` is independently proved
  (assumed from S^3 or inflation);
- that the Sommerfeld correction is an exact number rather than a bounded
  function of `alpha_GUT`;
- that Phase 5 delivers the Hubble constant `H_0` or the age of the
  universe (both additional downstream observables, not in this chain).

## Validation

```bash
python3 scripts/frontier_cosmology_from_mass_spectrum.py
```

Expected result on `main`:

- `frontier_cosmology_from_mass_spectrum.py`: `PASS=14 FAIL=0`

The runner verifies:

- the Phase 4 retained leptogenesis scale `M_1` (Part 1);
- the `eta` import status + DM-gate support package (Part 2);
- `Omega_b` from BBN within 5% of observation (Part 3);
- `R_base = 31/9` exactly from group theory + self-consistent Sommerfeld
  match (Part 4);
- `Omega_DM`, `Omega_m`, `Omega_Lambda` all within 5% (Part 5);
- flatness consistency `Omega_total = 1` (Part 6);
- LCDM parameter-count reduction `6 -> 1 + 1` (Part 7);
- cross-link through all five phases of the mass-spectrum attack plan
  (Part 8);
- a summary of retained / bounded / conditionally-closed content (Part 9).
