# The Case for DM Closure: Zero Bounded Inputs

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Purpose:** Strongest honest case that the two remaining "bounded" inputs
(g_bare = 1 and k = 0) are framework consequences, not independent
assumptions, reducing the DM chain to zero bounded inputs.

---

## Status

**ARGUMENT** -- not claimed as theorem. This note presents the strongest
honest case. A skeptic can reject either argument on foundational grounds.
But if both hold, R = 5.48 is fully derived from A1-A5 plus observation
(eta) alone.

---

## Current Ledger (Before This Argument)

The 13-step DM chain (DM_CLEAN_DERIVATION_NOTE.md) has:

- 4 EXACT (taste decomposition, dark sector, mass ratio, channel weighting)
- 7 DERIVED (alpha_s, Sommerfeld, sigma_v, Boltzmann, x_F, H(T), rho(T))
- 2 BOUNDED (g_bare = 1 and k = 0)
- 1 observational input (eta = 6.12 x 10^{-10}, enters Omega_b only)

This note argues both BOUNDED items are framework consequences.

---

## Argument 1: g_bare = 1 Is Part of the Framework Definition

### The operator argument

The KS staggered Hamiltonian on Z^3 is:

    H = sum_{x, mu} eta_mu(x) [psi^dag(x+e_mu) U_mu(x) psi(x) + h.c.]

This operator has NO free coupling constant. The hopping coefficient is 1
by construction of the Kawamoto-Smit staggered fermion. This is not a
choice -- it is the operator that realizes Cl(3) on Z^3.

In continuum gauge theory, the holonomy is U = exp(i g A_mu T^a dx).
The coupling g appears because A_mu is independently normalized. But on
the lattice with a = l_Pl (axiom A5), the link variable U_mu(x) IS the
fundamental degree of freedom. There is no independent field A_mu to
renormalize. The holonomy U is unitary by construction, and its appearance
in H with unit coefficient is the definition of the staggered action.

### The self-consistency argument

The gravity lane establishes (GRAVITY_CLEAN_DERIVATION_NOTE.md, 12/12
EXACT):

    L = G_0^{-1} = H = -Delta_lat

The field equation IS the Hamiltonian. The Hamiltonian has unit hopping
coefficient. Therefore the field equation has unit coupling. This is not
a coincidence -- self-consistency FORCES L = H, and H has no free
parameter.

### The no-running argument

With a = l_Pl as the unique physical scale (A5) and no continuum limit,
the coupling cannot run. There is no ratio of scales to generate a
beta function. The coupling is a pure number determined by algebraic
structure: g_bare = 1.

### The computational chain (not a choice)

From g_bare = 1:

    alpha_bare = g^2 / (4 pi) = 1 / (4 pi) = 0.0796
    beta = 2 N_c / g^2 = 6
    <P>_1-loop = 1 - (pi^2/3) alpha_bare
    alpha_plaq = -ln(<P>) / (pi^2/3) = 0.0923

Every step is algebraic computation on the defined Hamiltonian. The value
alpha_s = 0.092 is a COMPUTATION, not a parameter selection.

### Codex precedent

Codex accepted the entire generation lane on the basis that "the framework
says Cl(3) on Z^3 is the physical theory" (axiom A5). The framework
DEFINES the Hamiltonian. The Hamiltonian HAS unit coupling. If A5 is
accepted (as it is for the generation count), then g = 1 is already
accepted as part of the framework definition.

The question "is g_bare = 1 a constraint or a convention?" becomes: "is
the normalization of the Cl(3) generators part of the framework axioms?"
The answer is yes -- {Gamma_mu, Gamma_nu} = 2 delta_{mu,nu} IS axiom A1.
The factor 2 on the right-hand side fixes the generator normalization.
The gauge coupling is determined by the same normalization.

### Honest residual

A pure mathematician can always define a rescaled Hamiltonian H' = lambda H
and absorb lambda into the coupling. The defense: axiom A5 (a = l_Pl is
the unique physical scale) together with A1 (Cl(3) normalization) leaves
no freedom for lambda. The lattice spacing sets the energy scale, and the
Clifford algebra sets the dimensionless normalization. Together they fix
g = 1.

This is a foundational commitment, not a dynamical derivation. But it is
the SAME kind of foundational commitment as A5 itself, which Codex has
already accepted.

---

## Argument 2: k = 0 Is Irrelevant to R

### The numerical argument

The full Friedmann equation is:

    H^2 = (8 pi G / 3) rho - k / a^2

At freeze-out (T_F ~ m/25 ~ M_Pl/25):

    rho_rad = (pi^2/30) g_* T_F^4

    (8 pi G / 3) rho ~ T_F^4 / M_Pl^2 ~ M_Pl^2 / (25^4)

The curvature term for k = +/-1:

    k / a_F^2

where a_F is the scale factor at freeze-out. In Planck units with
T_F ~ 10^{18} GeV, the scale factor satisfies a_F T_F ~ 1 (radiation
era), so a_F ~ 1/T_F ~ 10^{-18} in natural units. But what matters is
the RATIO of the curvature term to the radiation term.

The curvature contribution to H^2 scales as:

    |k / a^2| / [(8 pi G / 3) rho] = |Omega_k(T_F)|

During radiation domination, Omega_k scales as (a H_0)^2 / (a^2 H^2).
At freeze-out temperatures T ~ 10^{18} GeV, with T_0 ~ 10^{-4} eV:

    T_F / T_0 ~ 10^{22}

    |Omega_k(T_F)| ~ |Omega_k(T_0)| x (T_0 / T_F)^2
                    < 0.001 x 10^{-44}
                    ~ 10^{-47}

The curvature term is suppressed by a factor of 10^{-47} relative to the
radiation term at freeze-out. This is not "small" -- it is functionally
zero. The value of k does not affect H(T_F) to any physically
meaningful precision.

### The structural argument

The freeze-out condition is:

    Gamma_ann(T_F) = H(T_F)

where Gamma = n_eq <sigma v> and H = sqrt(8 pi G rho / 3). The curvature
correction to H is:

    delta H / H = -(k / a^2) / (2 H^2) = -Omega_k / 2 ~ 10^{-47}

This shifts x_F = m/T_F by:

    delta x_F / x_F ~ delta H / H ~ 10^{-47}

which shifts R by:

    delta R / R ~ (1 / x_F) (delta x_F) ~ 10^{-48}

For comparison, the 0.25% agreement of R = 5.48 with observation
corresponds to delta R / R ~ 0.003. The curvature contribution is
10^{45} times smaller than the current theoretical precision.

### Even on S^3 (k = +1)

The S^3 compactification (bounded lane) gives k = +1. But on S^3, the
curvature radius R_curv >> l_Pl at freeze-out. The curvature term k/a^2
is still suppressed by the same factor of 10^{-47}. Whether the spatial
geometry is S^3, R^3, or H^3, the curvature is irrelevant at freeze-out.

### k does not enter R

The ratio R = Omega_DM / Omega_b depends on H(T) only through x_F (the
freeze-out temperature). Since x_F is logarithmically sensitive to H,
and H receives a 10^{-47} correction from k, the value of k propagates
into R at the level of 10^{-48}. This is not an approximation -- it is
exact to any precision that could ever matter.

**k does not need to be assumed. It drops out.**

### Honest residual

The argument requires that the universe was radiation-dominated at
freeze-out, i.e., that rho ~ T^4 >> k/a^2 at the relevant epoch.
This is a consequence of the framework's spectrum (g_* = 106.75 gives
radiation domination) and the scale hierarchy (T_F << M_Pl). No
assumption about the global topology is needed.

---

## Combined Result: If Both Arguments Hold

| Input | Before | After | Justification |
|-------|--------|-------|---------------|
| g_bare = 1 | BOUNDED | FRAMEWORK (same status as A5) | Unit coupling is the Hamiltonian's definition |
| k = 0 | BOUNDED | IRRELEVANT (drops out at 10^{-47}) | Curvature negligible at freeze-out |

The DM chain then has:

- 4 EXACT steps
- 9 DERIVED steps (including g_bare = 1 as framework-derived)
- 0 BOUNDED steps
- 1 observational input (eta for Omega_b)

R = 5.48 is DERIVED from the framework axioms A1-A5 plus the observed
baryon-to-photon ratio eta.

---

## Strength Assessment: How a Skeptic Would Attack

### Attack on g_bare = 1

**Strongest objection:** "You can always rescale A -> A/g. The coupling
is a convention, not a prediction."

**Defense:** On the Planck lattice, there is no independent continuum
field A. The link variable U is fundamental. Its appearance in H with
unit coefficient is the operator definition. The rescaling freedom
A -> A/g exists in the continuum, where A and g are independently
defined. On the lattice, they are not independent -- U = exp(i A a)
and the lattice action depends on U alone.

**Strength:** 7/10. Compelling within the framework. A skeptic who
accepts A5 (Planck lattice is fundamental) should accept g = 1. But the
argument is algebraic/definitional, not dynamical. It will convince
lattice practitioners (who recognize that beta = 6/g^2 defines the
theory, and beta = 6 means g = 1) but may not convince continuum
theorists (who view g as a free parameter).

### Attack on k = 0

**Strongest objection:** "k = 0 is assumed in the Newtonian derivation.
Even if it's numerically irrelevant, you need it for the derivation to be
valid."

**Defense:** No. The full equation H^2 = (8piG/3)rho - k/a^2 is valid
for any k. The freeze-out calculation uses H(T_F), and at T_F the
curvature term is 10^{-47} times the radiation term. The derivation is
valid for ANY k -- the answer is the same. Saying "k = 0" is not an
assumption; it is the statement that a 10^{-47} correction does not
matter.

**Strength:** 9/10. This is essentially unassailable. The curvature
is numerically irrelevant by 45 orders of magnitude. The only residual
is the assumption of radiation domination at freeze-out, which follows
from the framework's particle content.

---

## What This Changes for the Paper

### If the referee accepts both arguments

The paper can state:

> The dark-matter-to-baryon ratio R = Omega_DM / Omega_b = 5.48 is
> derived from axioms A1-A5 in a 13-step chain with zero free parameters.
> The bare coupling g = 1 is the unit-normalized hopping coefficient
> of the staggered Hamiltonian, determined by the Cl(3) algebraic
> structure (A1) on the Planck lattice (A5). Spatial curvature k enters
> the Friedmann equation but is suppressed by a factor of 10^{-47}
> relative to the radiation density at freeze-out, making R independent
> of k to any meaningful precision. The only observational input is
> the baryon-to-photon ratio eta = 6.1 x 10^{-10}, which enters the
> baryon abundance Omega_b but not the ratio R.

### If the referee does not accept g_bare = 1

Fall back to the current BOUNDED status: two bounded inputs (g_bare = 1
and k = 0), with full sensitivity analysis showing R in [5.22, 5.78] for
g in [0.95, 1.05]. The 0.25% agreement at g = 1 is then a "prediction
conditional on the Cl(3) normalization."

### What NOT to claim

- "Zero-parameter theory" -- eta is still an observational input.
- "g = 1 is proved from dynamics" -- it is not. It follows from the
  algebraic structure of the framework, not from a dynamical calculation.
- "k = 0 is derived" -- it is not derived; it is irrelevant. The
  distinction matters: we do not prove k = 0, we prove k does not matter.
- "The DM lane is CLOSED" -- use DERIVED, not CLOSED, since the
  foundational status of the g_bare argument remains debatable.

---

## The Honest Bottom Line

The DM chain has two items previously classified as BOUNDED. One of them
(k = 0) is not really an assumption at all -- it is a 10^{-47} irrelevance.
The other (g_bare = 1) is part of the same foundational package as axiom
A5, which Codex has already accepted for other lanes. If the framework
defines the Hamiltonian (which everyone agrees it does), and the
Hamiltonian has unit coupling (which is a mathematical fact about the KS
staggered operator), then g = 1 is not an input -- it is a consequence
of the framework definition.

The strongest version of the claim: R = 5.48 follows from the same axiom
surface (A1-A5) that gives the generation count, gauge group, and Newton's
law, with no additional assumptions. The only external input is the
observed baryon-to-photon ratio eta.

---

## Cross-References

- `DM_CLEAN_DERIVATION_NOTE.md` -- the 13-step chain (current BOUNDED status)
- `G_BARE_DERIVATION_NOTE.md` -- detailed g_bare = 1 argument
- `DM_FRIEDMANN_FROM_NEWTON_NOTE.md` -- Newtonian Friedmann derivation
- `GRAVITY_CLEAN_DERIVATION_NOTE.md` -- self-consistency L = H = -Delta (12/12)
- `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` -- full operator-level argument
- `DM_FLAGSHIP_CLOSURE_NOTE.md` -- current bounded status with Codex objections
- `ALPHA_S_SELF_CONSISTENCY_NOTE.md` -- alpha_s computation chain
