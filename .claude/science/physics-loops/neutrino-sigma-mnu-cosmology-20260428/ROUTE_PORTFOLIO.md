# Route Portfolio for Lane 4F Σm_ν

## Primary entry: matter-budget split

```text
Ω_m,0  =  Ω_b  +  Ω_DM  +  Ω_ν                                    (4F-1)
Ω_ν h²  =  Σm_ν / (93.14 eV)                                        (4F-2)
1 - L - R  =  Ω_b  +  Ω_DM  +  Σm_ν / (93.14 eV h²)                 (4F-3)
```

(4F-3) follows from the retained open-number-reduction surface
`Ω_m,0 = 1 - L - R` plus standard cosmology bookkeeping.

## Routes

### R1 — Direct algebraic retention via fully-retained inputs

**Premise:** if all of `(L, R, h, Ω_b, Ω_DM)` are retained, then
`Σm_ν` retains directly via (4F-3).

**Status:** blocked. `(h, Ω_b, Ω_DM)` are admitted observational
layer numbers. `h` is research-level distant per Lane 5
two-gate dependency.

### R2 — Bounded-envelope retention

**Premise:** under bounded `(h, Ω_b, Ω_DM)` (e.g., from retained
absolute-scale gate or cosmology constraint envelope), retain
`Σm_ν` as a bounded interval.

**Status:** depends on Lane 5 (C1) gate closure for bounded `h`.
Currently scaffold.

### R3 — Structural functional form (theorem-plan)

**Premise:** without retaining numerical bound, retain the **exact
functional form** of `Σm_ν` as a function of admitted/retained inputs.
Analog of the cosmology open-number reduction theorem's "S as
closed-form function of (H_0, L)".

**Status:** Phase-1 attemptable. Single-cycle.

### R4 — N_eff cross-validation as upper-envelope

**Premise:** retained `N_eff = 3.046` plus retained neutrino
observable bounds may give a **structural lower bound** on `Σm_ν`
(via mass-splitting + lightest constraint).

**Status:** depends on neutrino mass-splitting retention; Δm² values
not yet retained per Lane 4 4B/4C status. Currently scaffold.

### R5 — Cross-sector tie via retained PMNS structure

**Premise:** retained PMNS selector zero law + retained `δ_CP`/`θ_23`
structure may constrain mass-spectrum direction, anchoring `Σm_ν`
via the `(m_lightest, Δm²_21, Δm²_31)` reduction.

**Status:** distant; would require 4B+4C+4E closure.

## Recommended Cycle 1: R3 (structural functional form)

Build a branch-local theorem-plan note that:

1. States the matter-budget identity (4F-3).
2. Identifies the retained inputs `(L, R)`.
3. Identifies the admitted inputs `(h, Ω_b, Ω_DM)`.
4. Audits which would unblock single-cycle `Σm_ν` retention.
5. Outputs the structural functional form
   `Σm_ν = (1 - L - R - Ω_b - Ω_DM) × 93.14 eV × h²`
   as a retained algebraic identity given the structural inputs.

This isolates the load-bearing dependencies and produces a clean
Phase-1 deliverable (analog of Lane 5's open-number reduction
theorem and Lane 6's theorem plan).
