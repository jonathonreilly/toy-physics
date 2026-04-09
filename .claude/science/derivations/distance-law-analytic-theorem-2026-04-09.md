# Distance Law Analytic Theorem

**Date:** 2026-04-09
**Status:** New derivation — unifies distance and mass law anomalies

## Summary

The gravitational deflection on a 2D lattice with Laplacian field is **analytically determined** by the action's dependence on the field strength f. For any action of the form delta_S ~ f^alpha, the deflection at impact parameter b is:

    delta(b) = k * s^alpha * C_alpha / b^alpha

where C_alpha = sqrt(pi) * Gamma((alpha+1)/2) / Gamma((alpha+2)/2).

**The action power alpha simultaneously determines both the distance law AND the mass law.** This is the root cause of all observed anomalies.

## Setup

Consider a point mass at origin on a 2D lattice. The Laplacian field satisfies nabla^2 f = -rho, giving (in continuum limit):

    f(r) = s / r    (2D Coulomb, s = coupling strength proportional to mass M)

A beam at impact parameter b propagates along x, accumulating phase:

    Phi(b) = k * integral_{-W}^{W} g(f(x,b)) dx

where g(f) is the action's dependence on field strength, and f(x,b) = s / sqrt(x^2 + b^2).

The gravitational deflection is the transverse phase gradient:

    delta(b) = dPhi/db = k * integral g'(f) * (df/db) dx

Since df/db = -s*b / (x^2 + b^2)^{3/2}:

    delta(b) = k * s * b * integral |g'(f)| / (x^2 + b^2)^{3/2} dx

## Case 1: Valley-Linear Action (S = L(1-f))

Here g(f) = -f, so g'(f) = -1 (constant).

    delta_VL(b) = k * s * b * integral dx / (x^2 + b^2)^{3/2}

The standard integral gives 2/b^2 for W >> b, so:

    **delta_VL(b) = 2ks / b**

This is exact Newtonian 1/b.

## Case 2: Spent-Delay Action

The spent-delay action is S = L(1+f) - sqrt(L^2(1+f)^2 - L^2).

For small f: S approx L(1+f) - L*sqrt(2f + f^2) approx L(1+f) - L*sqrt(2f)(1 + f/4 + ...)

The leading field-dependent term is: delta_S approx -L*sqrt(2f)

So g(f) ~ -sqrt(f), giving g'(f) = -1/(2*sqrt(f)).

Substituting f(x,b) = s/sqrt(x^2+b^2):

    g'(f) = -(x^2+b^2)^{1/4} / (2*sqrt(s))

The deflection integral becomes:

    delta_SD(b) = k*sqrt(s/2) * b * integral dx / (x^2 + b^2)^{5/4}

Scaling x = b*u: the integral gives C / b^{3/2}, so:

    **delta_SD(b) = const / sqrt(b)**

This is the b^{-1/2} law observed numerically.

## General Rule

| Action form | alpha | delta(b) | F ~ M dependence |
|---|---|---|---|
| S ~ f (valley-linear) | 1 | 1/b | F ~ M |
| S ~ sqrt(f) (spent-delay) | 1/2 | 1/sqrt(b) | F ~ sqrt(M) |
| S ~ f^2 | 2 | 1/b^2 | F ~ M^2 |

## The Unification

**Key insight:** The action power alpha controls both anomalies simultaneously:
- Distance law: delta ~ 1/b^alpha
- Mass law: delta ~ M^alpha (since s ~ M, and delta ~ s^alpha)

The numerical measurements:
- Distance exponent: b^{-0.5} to b^{-0.9} (expected: 0.5 in continuum limit for spent-delay)
- Mass exponent: M^{0.82} (intermediate — finite-size corrections push alpha from 0.5 toward 1)

The spread arises because at small b (where f is large), the spent-delay transitions from sqrt(f) to linear-f behavior, inflating the effective exponent.

## The Minimal Fix: Action Phase Linearity

**Axiom (Action Phase Linearity):** The phase per edge is Phi_edge = k * L * (1 - c*f).

This single axiom:
- Gives Newtonian distance law: delta ~ 1/b
- Gives linear mass dependence: F ~ M
- IS the valley-linear action S = L(1-f)
- No modification to the field equation or kernel is needed

## Why This Matters

The distance law closure was previously treated as a structural negative. This derivation shows:

1. The anomaly is NOT a lattice artifact or finite-size effect — it's the expected continuum behavior of the spent-delay action
2. The fix is a single axiom (phase linearity) that also fixes the mass law
3. Valley-linear was already tested and shown to work numerically — now we know WHY

## Open Questions

1. Can phase linearity be derived from deeper principles (Lorentz covariance + additivity)?
2. Is there a physical argument for why the action should be linear in f rather than sqrt(f)?
3. Does this connect to the action uniqueness theorem (Frontier #3)?

## Weakest Link

The assumption that the Laplacian field gives f ~ 1/r in 2D. On discrete graphs, deviations from 1/r field are the second-order correction. But this derivation shows the primary effect is from the action nonlinearity, not the field shape.
