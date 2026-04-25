# Koide Q Dynamical Z-Linear / Plus-Perp Mixer No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_dynamical_z_linear_mixer_no_go.py`  
**Status:** executable no-go; Q remains open

## Purpose

Attack the next strongest live route:

```text
derive a retained charged-lepton dynamical law that either forbids the linear
Z=P_plus-P_perp source term or supplies a genuine plus/perp mixer.
```

If retained dynamics supplied either input, the traceless source coefficient
would be forced to zero and the known conditional chain would give:

```text
K_TL = 0
Y = I_2
E_+ = E_perp
kappa = 2
Q = 2/3.
```

## Theorem Attempt

Maybe the physical charged-lepton dynamics is strong enough to do one of two
things:

```text
1. forbid ell*z in the effective source potential, or
2. mix P_plus and P_perp so that bZ is not a conserved source charge.
```

Either would turn zero-background from a coordinate choice into a retained
theorem.

## Result

The audit rejects the route under current retained structure.

The retained `C3` dynamical commutant has the form:

```text
H_ret = alpha P_plus + beta P_perp + gamma(C-C^2).
```

It has no plus/perp cross block:

```text
P_plus H_ret P_perp = 0
P_perp H_ret P_plus = 0
```

and it conserves `Z`:

```text
[H_ret, Z] = 0.
```

A genuine mixer does kill the `Z` source coefficient conditionally, but that
mixer is not `C3`-retained.  Likewise, a `Z -> -Z` parity forbids the linear
term conditionally, but that parity is the same missing exchange/quotient law.

The exact counterbackground remains:

```text
V(z) = ell*z + m*z^2
ell = 2/3
m = 1
z* = -1/3
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR=derive_retained_dynamical_law_forbidding_linear_Z_or_supplying_plus_perp_mixer
RESIDUAL_SOURCE=C3_commutant_preserves_Z_and_allows_linear_Z_potential
COUNTERBACKGROUND=z_minus_1_over_3_from_linear_term_ell_2_over_3_m_1
```

## Hostile Review

This no-go does not promote conditional support as closure.  A mixer or parity
would close the Q source bridge only after being derived as retained
charged-lepton dynamics.  The current retained `C3` commutant supplies neither.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_dynamical_z_linear_mixer_no_go.py
python3 -m py_compile scripts/frontier_koide_q_dynamical_z_linear_mixer_no_go.py
```

Expected closeout:

```text
KOIDE_Q_DYNAMICAL_Z_LINEAR_MIXER_NO_GO=TRUE
Q_DYNAMICAL_Z_LINEAR_MIXER_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_RETAINED_Z_PARITY_OR_PLUS_PERP_MIXER=TRUE
```
