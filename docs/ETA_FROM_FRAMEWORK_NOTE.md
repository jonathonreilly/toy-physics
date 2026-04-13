# Eta From Framework: Input Provenance and Derivability Analysis

## Status: OPEN (transport parameters imported)

## Summary

The baryon-to-photon ratio eta = n_B / n_gamma ~ 6e-10 is computed via
electroweak baryogenesis from six inputs.  Three are framework-derived;
three are imported phenomenological estimates.  The prediction is
dominated by the exponential washout factor, which depends only on
framework-derived v/T.  The imported parameters enter as a linear
prefactor and shift the eta = eta_obs crossing point by only ~0.05 in
v/T even under 100x variation.

## Input Classification

| Input | Value | Status | How it enters |
|-------|-------|--------|---------------|
| J_Z3 (Jarlskog) | 3.1e-5 | DERIVED | linear prefactor |
| v(T_c)/T_c | 0.56 +/- 0.05 | DERIVED | exponential washout + linear |
| Gamma_sph/T^4 | ~9e-7 | DERIVED | linear + exponential |
| v_w (wall velocity) | 0.05 | IMPORTED | linear (1/v_w) |
| L_w*T (wall thickness) | 15 | IMPORTED | linear (1/L_w*T) |
| D_q*T (quark diffusion) | 6 | IMPORTED | linear (D_q*T) |

### Derived inputs

1. **J_Z3**: The Z_3 cyclic permutation assigns phases {1, omega, omega^2}
   to three generations.  sin(delta_Z3) = sin(2*pi/3) = sqrt(3)/2.
   Combined with framework-derived mixing angles, J = 3.1e-5.

2. **v(T_c)/T_c**: Gauge-effective scalar MC with SU(2) corrections
   computed from first principles.  Three independent attacks all give
   v/T >= 0.52.  Best value: 0.56 +/- 0.05.
   Source: `frontier_ewpt_gauge_closure.py`.

3. **Gamma_sph/T^4**: Parametric form alpha_w^5 from Arnold-Son-Yaffe.
   alpha_w = g^2/(4*pi) where g is the SU(2) coupling from Cl(3).
   Coefficient kappa ~ 20 from d'Onofrio et al. lattice measurement
   (pure SU(2) gauge, framework-independent).

### Imported inputs

4. **v_w ~ 0.05**: Bubble wall velocity.  Balance of driving force (Delta V)
   and friction from particle scattering.  Standard range: 0.01-0.5.
   Derivable in principle from framework potential + hydrodynamics.
   Effort: LARGE (coupled Boltzmann + fluid equations).

5. **L_w*T ~ 15**: Wall thickness.  Determined by V_eff(phi, T) barrier shape.
   Derivable from bounce equation with existing MC potential.
   Effort: SMALL (1D ODE, ~50 lines added to existing code).
   Parametric estimate: L_w*T ~ sqrt(lambda)/E ~ 15-25 (consistent).

6. **D_q*T ~ 6**: Quark diffusion coefficient.  Parametric form
   D_q*T ~ 1/(C_F * alpha_s) from framework-derived alpha_s.
   Full NLO result requires kinetic theory calculation.
   Effort: MODERATE.

## Key Finding: Logarithmic Sensitivity

The transport parameters enter only as a linear prefactor P = D_q*T / (v_w * L_w*T).
The prediction is dominated by the double-exponential washout:

    eta = A * P * (v/T) * exp(-K * exp(-36 * v/T))

where A and 36 are framework-derived.  The double-exponential makes eta
EXTREMELY insensitive to P:

| Transport variation | P/P_ref | v/T crossing shift |
|--------------------|---------|--------------------|
| All params 3x favorable | 27x | ~+0.03 |
| Reference | 1x | 0 |
| All params 3x unfavorable | 1/27x | ~-0.03 |

Changing the transport prefactor by a factor of 100 shifts v/T* by only ~0.05.

## Chain Status

```
Cl(3) on Z^3 (axiom)
    |
    v
SU(2) gauge structure ----[CLOSED]
    |
    v
Sphalerons ----[CLOSED]
    |
    v
Gamma_sph ~ alpha_w^5 T^4 ----[CLOSED]
    |
    v
Z_3 CP: J = 3.1e-5 ----[CLOSED]
    |
    v
CW phase transition ----[CLOSED]
    |
    v
v(T_c)/T_c = 0.56 ----[CLOSED]
    |
    v
Transport: v_w, L_w*T, D_q*T ----[IMPORTED, low sensitivity]
    |
    v
eta ~ 6e-10 ----[CONDITIONAL on transport, robust]
    |
    v
Omega_b, Omega_DM, Omega_Lambda ----[follows from eta + R=5.47]
```

## Claim Guidance

**Safe claim**: The framework predicts eta ~ 6e-10 from three structural
inputs (Z_3 CP phase, CW phase transition strength v/T = 0.56, SU(2)
sphaleron rate).  The prediction is dominated by the exponential washout
factor which depends only on framework-derived v/T.  Three transport
parameters (wall velocity, wall thickness, quark diffusion) enter as a
linear prefactor and are in principle derivable from the same framework.

**Not safe to claim**: eta is fully derived from first principles.
The transport parameters are still imported estimates.

## Roadmap to Full Closure

1. **L_w*T from bounce equation** (SMALL effort)
   - Solve d^2 phi/dz^2 = dV/dphi with V_eff from existing MC
   - Extract wall width from kink profile
   - Add ~50 lines to frontier_ewpt_gauge_closure.py

2. **D_q*T from kinetic theory** (MODERATE effort)
   - Use framework-derived alpha_s(T_EW)
   - Compute collision integrals for quark scattering
   - Apply Kubo relation or Boltzmann equation

3. **v_w from hydrodynamics** (LARGE effort)
   - Compute Delta V from framework potential
   - Calculate friction coefficients from framework couplings
   - Solve deflagration/detonation equations

Steps 1 and 2 would reduce the imported count from 3 to 1.
Step 3 would close the gate entirely.

## Files

- Script: `scripts/frontier_eta_from_framework.py`
- Log: `logs/YYYY-MM-DD-eta_from_framework.txt`
- Dependencies: `scripts/frontier_baryogenesis.py`,
  `scripts/frontier_ewpt_gauge_closure.py`
