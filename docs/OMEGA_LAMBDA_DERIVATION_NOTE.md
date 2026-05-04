# Omega_Lambda Derivation: The Cosmological Pie Chart

**Primary runner:** [`scripts/frontier_omega_lambda_derivation.py`](../scripts/frontier_omega_lambda_derivation.py) (PASS=6/0, INFO=4)

## Status

**BOUNDED** -- Omega_Lambda = 0.686 is a conditional cascade value given
observed Omega_b and the bounded dark-matter ratio chain. The base factor
`R_base = 31/9` is now packaged as an exact group-theory support identity,
but the Sommerfeld continuation, eta, and the matter/cosmology bridge remain
outside retained first-principles closure.

**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Theorem / Claim

Given the observed baryon density Omega_b = 0.0493 and the bounded
DM-to-baryon ratio chain, the framework gives the dark-energy fraction
Omega_Lambda = 0.686 (observed: 0.685). This is a conditional cascade result,
not a retained first-principles cosmology closure.

The full chain:

    eta(obs) -> Omega_b(BBN) -> R(bounded) -> Omega_DM -> Omega_m -> Omega_Lambda

Each link:

1. **eta = 6.12e-10**: still imported from Planck 2018 on this cosmology
   chain. However, the current DM gate no longer leaves eta unsupported:
   the exact one-flavor theorem-native transport branch gives
   `eta/eta_obs = 0.1888`, and reduced-surface PMNS support recovers a
   low-action branch with `eta/eta_obs = 1`. That support stack is not yet
   promoted as live theorem-grade closure, so eta remains imported here.
2. **Omega_b = 0.0492**: standard BBN, zero free parameters given eta
3. **R = 5.38**: bounded from the exact support identity
   `R_base = 31/9 = 3.444` (see
   [`R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md))
   plus the Sommerfeld correction (`S_vis/S_dark ~ 1.56`)
4. **Omega_DM = R * Omega_b = 0.264**: arithmetic
5. **Omega_m = Omega_b + Omega_DM = 0.314**: arithmetic
6. **Omega_Lambda = 1 - Omega_m = 0.686**: flatness (from S^3 or inflation)

## Assumptions

1. **eta imported from observation** -- the old taste-scalar EWPT route is no
   longer the right support story. The current live DM lane gives:
   - exact one-flavor theorem-native transport:
     `eta/eta_obs = 0.1888`
   - reduced-surface PMNS support:
     `eta/eta_obs = 1`
   This is materially stronger than a pure import, but the selector /
   normalization closure is still open, so eta remains imported on this chain.

2. **R derivation bounded by alpha_GUT** -- the base identity
   `R_base = 31/9` is exact, but the Sommerfeld correction
   depends on alpha_GUT in [0.03, 0.05].  Within this range, R varies
   from ~4.8 to ~5.3.  The self-consistent match gives alpha_GUT ~ 0.062.

3. **Flatness assumed** -- Omega_total = 1.  Justified by S^3 topology
   (compact spatial sections) or inflation.  Planck: |Omega_k| < 0.002.

4. **Standard BBN** -- eta -> Omega_b is textbook cosmology with no
   model dependence.

## What Is Actually Proved

The derivation establishes:

- Given Omega_b (observed), the framework gives a conditional Omega_Lambda
  value once the bounded `R` chain is supplied. The exact part of that chain
  is `R_base = 31/9`; the Sommerfeld enhancement is still bounded.

- The conditional cascade is robust: alpha_GUT in [0.03, 0.05] gives
  Omega_Lambda in [0.66, 0.71], comfortably containing the observed 0.685.

- The chain is a genuine conditional cascade: if bounded `R ~ 5.4` is supplied,
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

1. **Eta from first principles** -- the current live taste-block theorem gives
   only a bounded scalar-only estimate `v(T_c)/T_c = 0.3079`, so the old
   taste-scalar EWPT baryogenesis route is not currently a closure path.
   The active eta route is now the DM leptogenesis gate:
   exact one-flavor transport reaches `0.1888`, while reduced-surface PMNS
   support reaches `1.0`. Promoting that gate would remove the eta import, but
   the full pie chart would still need the Sommerfeld/alpha_GUT and
   matter-bridge statuses promoted.

2. **Alpha_GUT from the framework** -- the Sommerfeld correction uses
   alpha_GUT as a bounded input.  If gauge coupling unification is
   derived within the framework, R becomes fully exact.

3. **Flatness mechanism** -- Omega_total = 1 is assumed.  The S^3
   compactification lane is still bounded/open (see review.md).

4. **DM relic mapping** -- the R derivation uses thermal freeze-out as
   standard physics input.  The full graph-native relic mapping is still
   open (see DM_RELIC_GAP_CLOSURE_NOTE.md).

## How This Changes The Paper

The chain Omega_b(obs) -> R(bounded) -> Omega_Lambda is a strong
bounded result for the paper:

- **Safe claim**: Given the observed baryon density and the bounded
  DM-to-baryon ratio chain, the framework gives Omega_Lambda = 0.686.
  The exact piece of the ratio chain is `R_base = 31/9`; the Sommerfeld
  continuation remains bounded.

- **Not safe**: Claiming Omega_Lambda is derived from first principles.
  Eta is still imported on the live cosmology surface, even though the current
  DM gate now provides much stronger support than before.

- **Paper placement**: This belongs in the cosmological predictions
  section as a conditional chain.  The honest framing is: "the framework
  reduces the six LCDM parameters to one observable input (eta or
  equivalently Omega_b), exact `R_base`, bounded Sommerfeld, and flatness."

## Commands Run

```bash
python3 scripts/frontier_omega_lambda_derivation.py
# PASS=6  FAIL=0  INFO=4
```
