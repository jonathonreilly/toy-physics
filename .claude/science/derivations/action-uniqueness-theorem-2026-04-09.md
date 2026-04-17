# Derivation: Action Constraint Theorem

## Date
2026-04-09

## Target
Determine how tightly the axioms constrain the action functional
S_edge = L * g(f), where f is the gravitational field and L is the
spatial link length. Is g(f) unique, or is there a family?

NOTE: This result does NOT prove full uniqueness. It constrains
the leading-order action to a one-parameter family (parametrized
by the coupling strength c_2), with unconstrained higher-order
corrections (c_3, c_4, ...). The title "constraint theorem" rather
than "uniqueness theorem" reflects this.

## Axioms

A1. **Linearity of propagator** — amplitude = sum of
     exp(i*k*S) / L^p contributions; S additive along paths.

A2. **Born rule preservation** — follows from A1 (linear
     propagator gives I_3 = 0 for any S).

A3. **Gravity sign** — g'(0) < 0 (mass decreases action,
     creating constructive interference toward mass).

A4. **Weak-field Newtonian limit** — deflection proportional to
     M/b in the continuum limit (verified numerically for the
     valley-linear action).

A5. **Action-reaction symmetry** — F(A->B) = F(B->A),
     which combined with the equivalence principle forces p = 1
     in the mass-coupling exponent.

A6. **Lorentz covariance** — S_edge must be a Lorentz scalar
     (invariant under boost-like frame mixing).

## Derivation

### Step 1: Lorentz covariance selects the building blocks (A6)

On each edge the model has two local quantities:
  - Coordinate delay: dt = L(1+f)
  - Spatial link length: L (= dx in the lattice frame)

Under a Lorentz boost with velocity v:
  dt' = gamma(dt - v*L),  L' = gamma(L - v*dt)

The possible local scalars are:
  (a) dt                        -> NOT invariant (drift ~ v*gamma*L)
  (b) sqrt(dt^2 + L^2)         -> NOT invariant (Euclidean norm)
  (c) sqrt(dt^2 - L^2) = tau   -> INVARIANT (proper time)
  (d) dt - sqrt(dt^2 - L^2)    -> NOT invariant (spent delay)

Proof for (c): dt'^2 - L'^2 = gamma^2[(dt - vL)^2 - (L - vdt)^2]
  = gamma^2[dt^2 - 2v*dt*L + v^2*L^2 - L^2 + 2v*dt*L - v^2*dt^2]
  = gamma^2[(1 - v^2)*dt^2 - (1 - v^2)*L^2]
  = dt^2 - L^2.  QED.

This has been verified numerically in retained_update_symmetry_test():
tau is invariant to machine epsilon; all other candidates drift.

**Conclusion from A6:** The action per edge must be a function of
tau and L alone: S_edge = F(tau, L).

### Step 2: Additivity constrains the functional form (A1)

The total action is S_path = sum_{edges} S_edge. For the path-sum
exp(i*k*S_path) to give meaningful interference, S_edge must be
an extensive quantity (scaling with edge size). The most general
form consistent with dimensional analysis is:

  S_edge = sum_{n=0}^{infty} c_n * tau^n / L^{n-1}

where each term has dimensions of length. Explicitly:
  n=0: c_0 * L
  n=1: c_1 * tau
  n=2: c_2 * tau^2 / L
  n=3: c_3 * tau^3 / L^2
  ...

The simplest (lowest-order) form is the LINEAR combination:

  S_edge = c_0 * L + c_1 * tau                           ... (*)

Higher-order terms (tau^2/L, tau^3/L^2, ...) are suppressed by
powers of (tau/L) which is O(1), so they are NOT automatically
negligible. We will return to them.

### Step 3: Express (*) in terms of the field f

With dt = L(1+f), the proper time is:
  tau = sqrt(dt^2 - L^2)
      = sqrt(L^2(1+f)^2 - L^2)
      = L * sqrt((1+f)^2 - 1)
      = L * sqrt(2f + f^2)

So the linear action (*) becomes:
  S_edge = c_0*L + c_1*L*sqrt(2f + f^2)
         = L * [c_0 + c_1*sqrt(2f + f^2)]

This means:  g(f) = c_0 + c_1*sqrt(2f + f^2).

### Step 4: Gravity sign constrains the signs (A3)

g'(f) = c_1 * (2 + 2f) / (2*sqrt(2f + f^2))
       = c_1 * (1+f) / sqrt(2f + f^2)

At small f > 0:  g'(f) -> c_1 / sqrt(2f), which is positive
if c_1 > 0 and negative if c_1 < 0.

A3 requires g'(0+) < 0, therefore:  **c_1 < 0**.

The sign of c_0 is unconstrained by gravity (it contributes
a field-independent phase that cancels in centroid ratios).

### Step 5: Identify with the known action forms

Setting c_0 = 1, c_1 = -1:
  g(f) = 1 - sqrt(2f + f^2)

This is NOT the valley-linear action g(f) = 1 - f.

Let us check: the proper-time deficit (spent delay) is
  dt - tau = L(1+f) - L*sqrt(2f+f^2)
           = L[1 + f - sqrt(2f+f^2)]

So the spent-delay action is S = dt - tau, which in our
notation is S = L*g(f) with:
  g_spent(f) = 1 + f - sqrt(2f + f^2)

This is NOT of the form c_0 + c_1*sqrt(2f+f^2). Instead it
is c_0 + a*f + c_1*sqrt(2f+f^2) with a = 1, c_1 = -1.
This comes from writing S = dt - tau = L(1+f) - tau, i.e.,
the action includes a dt term (NOT Lorentz-invariant by itself)
minus the invariant tau.

**Key realization:** S = dt - tau is NOT a Lorentz scalar.
As shown in the symmetry test, spent delay has nonzero boost
drift. It transforms as a TIME COMPONENT, not a scalar.

The ONLY Lorentz-scalar actions built from (tau, L) are
combinations of tau^n / L^{n-1} as in Step 2.

### Step 6: The weak-field expansion determines the distance law (A4)

The field-dependent part of g(f) controls the deflection integral.
For any action of the form g(f) = const + c * f^nu + ..., the
phase perturbation per edge is:

  delta_phi = k * L * c * f^nu

The deflection at impact parameter b from a mass M with field
f = s/r (where r = sqrt(x^2 + b^2)) is:

  deflection ~ d/db integral dx * f(r)^nu
             = d/db integral dx * s^nu / (x^2 + b^2)^{nu/2}

For nu = 1 (linear in f):
  integral dx / sqrt(x^2+b^2) = asinh(x/b)
  d/db[asinh(x/b)] ~ 1/b for x >> b
  Therefore: deflection ~ s/b  (Newtonian)

For nu = 1/2 (sqrt of f):
  integral dx / (x^2+b^2)^{1/4} ~ b^{1/2} * const
  d/db ~ b^{-1/2}
  Therefore: deflection ~ s^{1/2} / b^{1/2}  (non-Newtonian)

A4 requires Newtonian deflection (~ M/b), so **nu = 1**.

### Step 7: The Lorentz-covariant action expanded to leading order

From Step 3, the linear Lorentz-scalar action (n=0 and n=1) gives:
  g(f) = c_0 + c_1*sqrt(2f+f^2)
        = c_0 + c_1*sqrt(2f)*(1 + f/4 + ...)   [for small f]
        ~ c_0 + c_1*sqrt(2)*f^{1/2} + ...

This has **nu = 1/2**, which violates A4 (gives non-Newtonian
distance law and F proportional to sqrt(M) instead of M).

The valley-linear action g(f) = 1 - f has nu = 1 (Newtonian),
but 1 - f is NOT expressible as c_0*L + c_1*tau because
tau = L*sqrt(2f+f^2), and there is no combination of L and tau
that gives a term LINEAR in f.

### Step 8: The tension — and its resolution

We have a CONFLICT between two axioms at leading order:

  A6 (Lorentz covariance) + n=1 term -> g(f) ~ c_1*sqrt(f) [nu=1/2]

  A4 (Newtonian limit)               -> g(f) ~ c*f          [nu=1]

These cannot both be satisfied by the simplest (n <= 1) action.

**Resolution:** The action must include the n=2 term from Step 2.
Consider the full tower of Lorentz scalars:

  S_edge = sum_{n=0}^{infty} c_n * tau^n / L^{n-1}
         = c_0*L + c_1*tau + c_2*tau^2/L + c_3*tau^3/L^2 + ...

Substituting tau = L*sqrt(2f+f^2):
  tau^n / L^{n-1} = L * (2f+f^2)^{n/2}

So: g(f) = sum_n c_n * (2f+f^2)^{n/2}

Expanding each term at small f:
  n=0: c_0                              (constant)
  n=1: c_1*(2f+f^2)^{1/2}  ~ c_1*sqrt(2)*f^{1/2}
  n=2: c_2*(2f+f^2)        ~ 2*c_2*f
  n=3: c_3*(2f+f^2)^{3/2}  ~ c_3*(2f)^{3/2}
  ...

The FIRST term linear in f comes from **n=2: tau^2/L**.

Now tau^2/L = (dt^2 - L^2)/L = L[(1+f)^2 - 1] = L(2f + f^2).

So the action with leading Newtonian behavior is:

  **S_edge = c_0*L + c_2*(dt^2 - L^2)/L + higher order**
           = L*[c_0 + c_2*(2f + f^2)]

giving g(f) = c_0 + 2*c_2*f + c_2*f^2.

**But we must also kill the n=1 term.** If c_1 is nonzero,
the sqrt(f) piece from tau dominates the linear-f piece from
tau^2/L at small f (since sqrt(f) >> f for f -> 0). This would
give non-Newtonian scaling at weak field, violating A4.

Therefore: **c_1 = 0** (forced by A4).

### Step 9: Apply gravity sign (A3)

g'(0) = 2*c_2.

A3 requires g'(0) < 0, therefore **c_2 < 0**.

Setting c_0 = 1 (normalization: free-field action = L) and
c_2 = -1/2 (to match the valley-linear convention g = 1-f):

  g(f) = 1 - f - f^2/2

This is the valley-linear action PLUS a correction at order f^2.

### Step 10: Action-reaction provides no additional constraint on g (A5)

The p=1 derivation (from the three-axioms note) shows that
action-reaction forces the mass-coupling exponent to be 1,
i.e., F proportional to M_A * M_B. But this constrains HOW f
couples to masses (linearly), not the FUNCTIONAL FORM of g(f).

Any g(f) with g'(0) < 0 and leading linear term gives p=1
when combined with action-reaction. So A5 is already satisfied
once A4 is imposed.

### Step 11: Identify the physical meaning of tau^2/L

  tau^2/L = (dt^2 - L^2)/L = (delay^2 - length^2)/length

In GR language, tau^2 = ds^2 is the proper-time-squared interval.
The quantity tau^2/L is the proper-time-squared per unit spatial
length — a discretized version of the Lagrangian density for a
relativistic particle:

  L_GR = -m*sqrt(1 - v^2) ~ -m + m*v^2/2 + ...

Our tau^2/L = L*[(1+f)^2 - 1] = L*(2f + f^2), which plays the
role of the gravitational potential energy term in the action.

The GR geodesic action for a static weak-field metric with
g_00 = 1 + 2*Phi gives S ~ integral (1 + Phi) dt. Our term
c_2*tau^2/L ~ c_2*2f*L plays exactly this role: a linear
coupling to the potential f.

## The Constraint Theorem

**Theorem.** Among Lorentz-scalar actions that are:
  (i)   additive along paths (A1),
  (ii)  extensive in L (dimensional consistency),
  (iii) analytic in f at f = 0,
  (iv)  gravity-attracting: g'(0) < 0 (A3),
  (v)   Newtonian at weak field: deflection ~ M/b (A4),

the leading-order action is:

  **S_edge = c_0*L + c_2*tau^2/L = L + c_2*L*(2f + f^2)**

with c_2 < 0. The free parameter is c_2 (the gravitational
coupling strength). Setting c_2 = -1/2 gives the valley-linear
action to leading order.

The n=1 term (c_1*tau) is EXCLUDED by A4: it contributes a
sqrt(f) piece that would dominate the linear piece at small f,
giving non-Newtonian scaling. Therefore **c_1 = 0**.

Higher-order terms (n >= 3) are allowed but suppressed at weak
field. They produce post-Newtonian corrections:
  n=3: c_3*tau^3/L^2 contributes ~ f^{3/2} (sub-leading)
  n=4: c_4*tau^4/L^3 contributes ~ f^2 (same order as c_2*f^2)

After normalization (c_0 = 1), there is a **ONE-PARAMETER FAMILY**
parametrized by c_2 (plus higher-order coefficients that are
unconstrained by the weak-field limit).

## Which axiom does the most work?

| Axiom | What it constrains |
|-------|--------------------|
| A6 (Lorentz) | Building blocks: only tau and L allowed |
| A1 (Linearity) | S must be additive and extensive |
| A4 (Newton) | **Kills the sqrt(f) term (c_1 = 0)** — most powerful |
| A3 (Gravity sign) | c_2 < 0 (sign only) |
| A5 (Action-reaction) | Redundant once A4 is imposed |
| A2 (Born) | Follows from A1 |

**A4 (Newtonian weak-field limit) does the most work.** Without it,
both sqrt(f) and linear-f actions are allowed, giving qualitatively
different physics. A4 selects the linear branch.

## Spent-delay is ruled out as fundamental

The spent-delay action S = dt - tau:
  1. Is NOT a Lorentz scalar (numerically verified).
  2. Has g(f) ~ sqrt(2f) at weak field, giving F proportional to
     sqrt(M) and deflection proportional to 1/sqrt(b).

It is therefore excluded by BOTH A6 and A4. Its utility on noisy
graphs (stronger signal-to-noise per the bridge analysis) is an
operational advantage, not a fundamental property.

## Valley-linear emerges as the leading-order constrained action

With c_0 = 1 and c_2 = -1/2:
  g(f) = 1 - f - f^2/2 = 1 - f + O(f^2)

At weak field this matches valley-linear exactly. The f^2 term
is a POST-NEWTONIAN CORRECTION that is:
  - Required by Lorentz covariance (cannot truncate at linear f
    while keeping tau^2/L as the building block)
  - Numerically small (f ~ 10^{-5} in typical simulations, so
    f^2 ~ 10^{-10} is undetectable)
  - Analogous to the 1PN correction in GR

## Summary of the constrained action

The leading-order Lorentz-covariant, Newtonian, gravity-attracting
action consistent with axioms A1-A6 is:

  **S_edge = L - c_2*(tau^2)/(L) = L - c_2*L*(2f+f^2)**

With c_2 = -1/2 this gives L(1-f) - Lf^2/2, matching valley-linear
at weak field. But c_2 is a FREE parameter (coupling strength), and
higher-order corrections (c_3*tau^3/L^2, ...) are unconstrained.

This is a CONSTRAINT result, not a full derivation. It narrows g(f)
from an arbitrary function to a one-parameter family at leading order.
The valley-linear action S = L(1-f) is the weak-field limit for any
c_2 < 0. The spent-delay action S = dt - tau is excluded by Lorentz
covariance.

## Status
PROPOSED CONSTRAINT — the algebraic argument is clean for the
leading-order form. The key non-trivial step is showing c_1 = 0
(tau term excluded by A4). The result is a constraint to a
one-parameter family, NOT a uniqueness proof: c_2 (coupling
strength, analog of G) is free, and c_3, c_4, ... are
unconstrained by these axioms.

## Open questions
1. Can the higher-order coefficients (c_3, c_4, ...) be
   constrained by post-Newtonian observations or consistency
   conditions?
2. Does the f^2 correction in g(f) produce measurable effects
   in the lattice simulations at larger field strengths?
3. Is there a variational principle (geodesic equation) that
   selects c_2 = -1/2 specifically, or is it truly free?
