# Omega_Lambda Investigation: Can We Remove the Observational Input?

**Script:** `scripts/frontier_omega_lambda_derivation.py`
**Date:** 2026-04-12
**Status:** Honest negative -- Omega_Lambda cannot be derived; cosmic coincidence explained

## The Problem

The CC prediction Lambda = 3*H_0^2*Omega_Lambda/c^2 matches observation to 1.3%,
but uses Omega_Lambda = 0.685 as input. Can we derive Omega_Lambda from the framework,
or at least explain why Omega_Lambda ~ Omega_m right now (the "cosmic coincidence")?

## Seven Investigations

### (1) De Sitter attractor

Omega_Lambda(a) evolves from ~0 at early times to ~1 at late times.
Key epochs:

| Epoch | a | z | Omega_Lambda | Cosmic time |
|-------|---|---|-------------|-------------|
| BBN | 0.001 | 999 | 1.7e-9 | -- |
| Matter-Lambda equality | 0.772 | 0.30 | 0.50 | 10.3 Gyr |
| Today | 1.000 | 0 | 0.685 | 13.8 Gyr |
| Far future | 10 | -- | 0.9995 | 53.0 Gyr |

The transition takes ~30x in scale factor. We observe near the midpoint.

### (2) Coincidence window

The window 0.3 < Omega_Lambda < 0.9 spans:
- 1.0 e-foldings in ln(a), out of ~90 total (BBN to a=10^30)
- Only ~1% of cosmic history in log-scale
- In cosmic time: 7.2 to 21.2 Gyr (extends into de Sitter future)

This is narrow in log(a), but wide in cosmic time.

### (3) Graph growth models

| Model | Lambda behavior | w | Verdict |
|-------|----------------|---|---------|
| N ~ a^3 (volume growth) | Lambda ~ 1/a^2 | -1/3 | RULED OUT |
| N fixed (one-time formation) | Lambda = const | -1 | Needs R_f tuned |
| R = c/H (Hubble horizon) | Lambda = 3*H^2/c^2 | -1 (de Sitter) | Gives Omega_L = 1 |

None of the graph growth models independently determine Omega_Lambda.
The Hubble horizon model gives Lambda = 3*H^2/c^2, which is the pure
de Sitter equation (Omega_Lambda = 1). Adding matter reduces Omega_Lambda
but requires knowing the matter content.

### (4) Taste structure to Omega_m

To derive Omega_Lambda = 1 - Omega_m, we need Omega_m, which requires:
- Baryon asymmetry eta ~ 6e-10 (from baryogenesis, not yet derived)
- DM/baryon ratio R ~ 5.4 (partially addressed by taste singlets)
- Number of species (8 taste states: 6 visible + 2 dark)

Even with R derived from taste structure, eta remains an external input.

### (5) Honest accounting: what IS vs what IS NOT predicted

**Predicted (no free parameters):**
1. Lambda = lambda_min(graph Laplacian) [R^2 = 0.999]
2. Lambda ~ 1/L^2 scaling [exact]
3. S^3 topology [forced by C=3 self-consistency]
4. Lambda = 3*H^2/c^2 in de Sitter limit

**Not predicted:**
- Omega_Lambda = 0.685 (matter content)
- H_0 = 67.4 km/s/Mpc (graph size)
- Baryon asymmetry eta
- Dark matter abundance

### (6) The cosmic coincidence explained

The coincidence (Omega_Lambda ~ Omega_m today) is explained by:

1. **The framework guarantees Lambda ~ rho_crit** (not Lambda ~ M_Pl^4).
   Lambda = 3/R_H^2 means Lambda is always comparable to the critical density.
   This reduces the problem from 10^122 fine-tuning to O(1).

2. **Observer selection.** During the structure formation epoch (z ~ 10 to 0),
   Omega_Lambda ranges from 0.002 to 0.685. Any observer in this window
   sees Omega_Lambda ~ O(1). The specific value 0.685 requires Omega_m = 0.315.

3. **The window is wide.** |ln(Omega_L/Omega_m)| < 1 for z in [-0.07, 0.81],
   spanning a factor ~2 in scale factor. Structure-forming observers
   naturally find themselves in this range.

### (7) Comparison to other approaches

| Approach | Prediction | Accuracy |
|----------|-----------|----------|
| QFT vacuum energy | Lambda ~ M_Pl^4 | 10^122 off |
| SUSY cancellation | Lambda ~ M_SUSY^4 | ~10^60 off |
| Anthropic (Weinberg) | Lambda < 10*rho_m | O(1), not sharp |
| Holographic (CKN) | Lambda ~ 1/R_H^2 | Scaling only |
| Causal set | Lambda ~ 1/sqrt(V_4) | Order of magnitude |
| **This framework** | Lambda = 3/R_H^2 | **1.3% (given H_0, Omega_L)** |

## Quantitative Improvement

| Level | Ratio | log10 |
|-------|-------|-------|
| QFT vacuum energy | 10^122 | 122 |
| Framework (T^3 periodic) | 19.0 | 1.28 |
| Framework (S^3) | 1.44 | 0.16 |
| Framework (+ Friedmann) | 1.013 | 0.006 |

## The Correct Statement

The framework's CC prediction should be stated as:

> Lambda = 3*H^2/c^2 (the de Sitter value), with coefficient C=3 uniquely
> determined by self-consistency of the spectral gap equation on S^3.
> This solves the cosmological constant problem (why Lambda << M_Pl^4)
> by identifying Lambda with the IR spectral gap. The observed fraction
> Omega_Lambda = 0.685 requires additionally specifying the matter content,
> which is a particle physics question (baryon asymmetry + DM abundance).

This is analogous to GR: H^2 = 8*pi*G*rho/3 does not predict rho.
Our Lambda = 3/R^2 does not predict R independently of H and Omega_Lambda.
But it DOES predict Lambda is an IR quantity, resolving the 122-order problem.

## Scorecard

| Test | Result | Verdict |
|------|--------|---------|
| De Sitter attractor | Omega_L -> 1 as a -> inf | KNOWN |
| Coincidence window | ~1% of log(a) history | MODEST |
| Graph growth (volume) | w = -1/3, ruled out | NEGATIVE |
| Graph growth (Hubble) | Omega_L = 1 (de Sitter) | TOO STRONG |
| Taste -> Omega_m | Needs baryon asymmetry | INCOMPLETE |
| Cosmic coincidence | O(1) from observer selection | QUALITATIVE |
| Reframing: Lambda=3/R^2 | Solves CC problem, not Omega_L | STRONG |

## Bottom Line

Omega_Lambda = 0.685 cannot be derived from the framework alone. It depends on
the matter content (Omega_m = 0.315), which requires baryon asymmetry and DM
abundance from particle physics. However, the framework makes the cosmic coincidence
natural: Lambda = 3/R_H^2 guarantees Lambda ~ rho_crit, reducing the problem from
10^122 fine-tuning to an O(1) question about matter content. Observer selection
during structure formation explains why we see Omega_Lambda ~ 0.7.
