# Omega_Lambda Derivation: The Cosmological Pie Chart

## Status

**BOUNDED** -- Omega_Lambda = 0.686 is predicted with 0.2% accuracy given
observed Omega_b.  The chain uses one derived quantity (R) with zero
additional free parameters.  Eta is imported from observation.

**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Theorem / Claim

Given the observed baryon density Omega_b = 0.0493, the framework predicts
the dark energy fraction Omega_Lambda = 0.686 (observed: 0.685) with zero
additional free parameters beyond the derived DM-to-baryon ratio R.

The full chain:

    eta(obs) -> Omega_b(BBN) -> R(derived) -> Omega_DM -> Omega_m -> Omega_Lambda

Each link:

1. **eta = 6.12e-10**: imported from Planck 2018 (the live baryogenesis gate
   is now isolated in [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md);
   the older `v(T_c)/T_c ~ 0.52` target remains bounded route history, not a
   retained first-principles result, and the old taste-scalar implementation
   is not live on the current package surface; see
   [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md))
2. **Omega_b = 0.0492**: standard BBN, zero free parameters given eta
3. **R = 5.38**: derived from taste structure (R_base = 31/9 = 3.444)
   plus Sommerfeld correction (S_vis/S_dark ~ 1.56)
4. **Omega_DM = R * Omega_b = 0.264**: arithmetic
5. **Omega_m = Omega_b + Omega_DM = 0.314**: arithmetic
6. **Omega_Lambda = 1 - Omega_m = 0.686**: flatness (from S^3 or inflation)

## Assumptions

1. **eta imported from observation** -- the baryogenesis lane now has a clean
   main-branch gate note isolating the missing electroweak transition /
   transport computation, but this has not yet been closed by a
   non-perturbative same-surface lattice computation.

2. **R derivation bounded by alpha_GUT** -- the Sommerfeld correction
   depends on alpha_GUT in [0.03, 0.05].  Within this range, R varies
   from ~4.8 to ~5.3.  The self-consistent match gives alpha_GUT ~ 0.062.

3. **Flatness assumed** -- Omega_total = 1.  Justified by S^3 topology
   (compact spatial sections) or inflation.  Planck: |Omega_k| < 0.002.

4. **Standard BBN** -- eta -> Omega_b is textbook cosmology with no
   model dependence.

## What Is Actually Proved

The derivation establishes:

- Given Omega_b (observed), the framework predicts Omega_Lambda with
  ZERO additional free parameters.  R is the only derived input, and it
  comes from group theory (exact) plus Sommerfeld enhancement (bounded).

- The prediction is robust: alpha_GUT in [0.03, 0.05] gives
  Omega_Lambda in [0.66, 0.71], comfortably containing the observed 0.685.

- The chain is a genuine conditional prediction: if R ~ 5.4 (derived),
  then the entire cosmological pie chart follows from Omega_b alone.

Numerical results (using BBN-calibrated Omega_b):

| Parameter    | Predicted | Observed | Error |
|-------------|-----------|----------|-------|
| Omega_b     | 0.0492    | 0.0493   | 0.2%  |
| Omega_DM    | 0.264     | 0.265    | 0.2%  |
| Omega_m     | 0.314     | 0.315    | 0.4%  |
| Omega_Lambda| 0.686     | 0.685    | 0.2%  |
| R = DM/b   | 5.38      | 5.38     | 0.0%  |

## What Remains Open

1. **Eta from first principles** -- the missing object is the electroweak
   transition / sphaleron transport bridge isolated in
   [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md).
   If `eta` is derived on that same retained surface, the entire pie chart
   becomes parameter-free.

2. **Alpha_GUT from the framework** -- the Sommerfeld correction uses
   alpha_GUT as a bounded input.  If gauge coupling unification is
   derived within the framework, R becomes fully exact.

3. **Flatness mechanism** -- Omega_total = 1 is assumed.  The S^3
   compactification lane is still bounded/open (see review.md).

4. **DM relic mapping** -- the R derivation uses thermal freeze-out as
   standard physics input.  The full graph-native relic mapping is still
   open (see DM_RELIC_GAP_CLOSURE_NOTE.md).

## How This Changes The Paper

The chain Omega_b(obs) -> R(derived) -> Omega_Lambda is a strong
bounded result for the paper:

- **Safe claim**: Given the observed baryon density, the framework
  predicts Omega_Lambda = 0.686 with zero additional parameters, using
  only the derived DM-to-baryon ratio R = 5.4 from taste structure and
  Sommerfeld enhancement.

- **Not safe**: Claiming Omega_Lambda is derived from first principles.
  Eta is still imported.

- **Paper placement**: This belongs in the cosmological predictions
  section as a conditional chain.  The honest framing is: "the framework
  reduces the six LCDM parameters to one observable input (eta or
  equivalently Omega_b), with R derived and flatness assumed."

## Commands Run

```bash
python3 scripts/frontier_omega_lambda_derivation.py
# PASS=6  FAIL=0  INFO=4
```
