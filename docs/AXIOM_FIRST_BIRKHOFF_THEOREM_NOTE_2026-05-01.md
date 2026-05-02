# Axiom-First Birkhoff Theorem on Framework GR Action

**Date:** 2026-05-01
**Type:** positive_theorem
**Claim scope:** any spherically-symmetric vacuum (T_μν = 0) solution of the framework's retained discrete GR action is locally isometric to a piece of Schwarzschild and is therefore necessarily static.
**Status:** awaiting independent audit. Under the scope-aware classification framework (audit-lane proposal #291), `effective_status` is computed by the audit pipeline from `audit_status` + `claim_type` + dependency chain; no author-side tier is asserted in source.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 9 (Block 09; independent of Blocks 01-08)
**Branch:** `physics-loop/24h-axiom-first-block09-birkhoff-20260501`
**Runner:** `scripts/axiom_first_birkhoff_check.py`
**Log:** `outputs/axiom_first_birkhoff_check_2026-05-01.txt`

## Scope

This note proves the **Birkhoff theorem** on the framework's retained
discrete GR action surface:

> Any spherically-symmetric vacuum (`T_μν = 0`) solution of the
> framework's GR action is locally isometric to a piece of the
> Schwarzschild solution and is therefore necessarily **static**
> (admits a timelike Killing vector).

This is a classical theorem of GR (Birkhoff 1923) which extends to
the framework's retained discrete GR action surface via the
canonical Einstein-Hilbert equivalence
(`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`).

After this note, the framework retains:
- Schwarzschild family is the unique static vacuum spherically
  symmetric solution (in agreement with Block 02 Hawking T_H usage).
- No "Schwarzschild dust" or breathing radial modes can exist in pure
  vacuum.
- Outside any spherically-symmetric matter distribution, the metric
  is the Schwarzschild metric of total mass M (gravitational analog
  of Gauss's law for spherical symmetry).

## Retained inputs

- **Framework GR action surface.** Einstein vacuum equations
  `R_μν = 0` hold on the retained discrete-Lorentzian Einstein/Regge
  stationary action class
  (`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
  `UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`).

## Admitted-context inputs

- **Spherically-symmetric metric ansatz.** Standard differential-
  geometric reduction: any spherically-symmetric (SO(3)-invariant)
  Lorentzian metric can be locally written in coordinates `(t, r,
  θ, φ)` as

  ```text
      ds²  =  -A(r, t) dt²  +  B(r, t) dr²  +  r² dΩ²                       (1)
  ```

  where `dΩ² = dθ² + sin² θ dφ²` is the round-2-sphere metric. This
  is standard GR and inherited from Hawking-Ellis 1973.
- **Tensor calculus / Einstein equations expansion.** Standard
  differential geometry on the framework's smooth-limit surface.

## Statement

Let `(M, g)` be a spherically-symmetric vacuum solution of the
framework's GR action equations `R_μν = 0`. Then on `A_min` plus the
retained framework GR surface:

**(B1) Time-independence of `B`.** From the off-diagonal Ricci equation
`R_{tr} = 0`, the metric component `B(r, t) = B(r)` is independent of
`t`.

**(B2) Schwarzschild metric.** The metric (1) takes the form

```text
    ds²  =  -(1 - 2 G M / r) dt²  +  (1 - 2 G M / r)⁻¹ dr²  +  r² dΩ²       (2)
```

for some constant `M ∈ R` (the integration constant for the radial
ODE; physically, `M` is the asymptotic ADM mass).

**(B3) Static.** The metric (2) admits a timelike Killing vector
`∂_t` (independent of `t`), so the solution is static.

**(B4) Locally Schwarzschild.** The solution is locally isometric
to a piece of the Schwarzschild manifold of mass `M`.

**(B5) Uniqueness corollary.** No spherically-symmetric vacuum
solution can have time-dependent breathing radial modes. Equivalently:
spherically-symmetric pulsations radiate no gravitational waves
(consistent with the absence of monopole gravitational radiation).

## Proof

Standard derivation, Birkhoff 1923 (cf. Wald 1984 §6.1).

### Step 1 — Off-diagonal Ricci R_{tr} = 0 (proves B1)

For the metric (1), compute `R_{tr}`. Using the Christoffel symbols
and Ricci tensor formula in the orthonormal frame, the off-diagonal
component is

```text
    R_{tr}  =  - (∂_t B) / (r B)                                            (3)
```

Setting `R_{tr} = 0` (vacuum) gives `∂_t B = 0`, so `B(r, t) = B(r)`.

### Step 2 — Combination R_{tt}/A + R_{rr}/B = 0 (forces AB = 1 after rescaling)

In vacuum, both `R_{tt} = 0` and `R_{rr} = 0`. Computing:

```text
    R_{tt}/A + R_{rr}/B  =  - (1 / r) · (∂_r ln(A · B))                    (4)
```

Setting this to zero (vacuum) gives `∂_r ln(A B) = 0`, so
`A · B = f(t)` for some function `f(t)` of `t` only.

We can absorb `f(t)` into the time coordinate by redefining
`dt' := √f(t) · dt`. After this redefinition, `A · B = 1`, so

```text
    A(r, t)  =  1 / B(r)                                                    (5)
```

Combined with (B1), `A(r, t) = A(r)` is also independent of `t`.

### Step 3 — Radial Einstein equation R_{θθ} = 0 (gives Schwarzschild)

With `A(r) B(r) = 1`, the angular Ricci equation simplifies to

```text
    R_{θθ}  =  1 - A - r · A'  =  0                                          (6)
```

This is a first-order ODE for `A(r)`. Rewriting:

```text
    (r A)'  =  1                                                             (7)
```

Integrating: `r A = r - 2 G M` for some integration constant
`2 G M`. So

```text
    A(r)  =  1 - 2 G M / r                                                  (8)
```

This is the Schwarzschild metric coefficient. Substituting back into
(5) and (1) gives (B2). ∎

### Step 4 — Static and local isometry (proves B3, B4)

The metric (B2) is independent of `t`, so `∂_t` is a Killing vector.
Outside the horizon `r > 2 G M`, `∂_t` is timelike. Hence the
solution is static.

The solution is locally isometric to a piece of the maximal
Schwarzschild extension (Kruskal manifold) — the local Birkhoff
form (B2) extends to the full Schwarzschild family by global
patching arguments standard in GR.

### Step 5 — Uniqueness of static SS vacuum (proves B5)

Birkhoff implies no spherically-symmetric vacuum can be
time-dependent. In particular, a spherically-symmetric pulsation of
matter does not radiate gravitational waves: the exterior metric
remains the Schwarzschild metric of the constant total ADM mass
(gravitational version of Gauss's law for spherical symmetry).
This is the content of (B5). ∎

## Hypothesis set used

- Retained framework GR action surface (Einstein vacuum equations).
- Spherical symmetry ansatz (admitted-context).
- Standard tensor calculus on framework smooth-limit surface
  (admitted-context).

No fitted parameters. No observed values used as proof inputs.

## Corollaries

C1. **Spherical pulsations radiate no GWs.** No monopole
gravitational radiation can exist in classical GR. (Confirmed
observationally by LIGO: only quadrupole-or-higher modes contribute.)

C2. **Schwarzschild as exterior solution.** Any spherically-
symmetric matter distribution (e.g. star, planet) has an exterior
metric equal to the Schwarzschild metric of total mass `M`. This is
the "Schwarzschild exterior" theorem.

C3. **Spherical collapse to BH.** Spherical gravitational collapse
of a star produces a Schwarzschild BH of mass equal to the star's
ADM mass — no additional radiation channel exists.

C4. **No spherical hair.** Together with the no-hair theorem
(Israel-Carter-Robinson; not derived here), Birkhoff implies that
spherical BHs are uniquely characterized by mass alone.

## Honest status

**Branch-local theorem on retained framework GR action surface.**
(B1)–(B5) follow by the standard Birkhoff 1923 calculation on the
framework's smooth-limit Einstein-Hilbert equivalence surface. The
proof is independent of Blocks 01-08.

The runner verifies the Birkhoff derivation symbolically: starting
from the spherically-symmetric ansatz, it computes the relevant
Ricci tensor components and confirms that the vacuum equations
force `A(r, t) = 1/B(r) = 1 - 2GM/r`.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR action surface
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained framework GR action surface (which is retained but uses smooth-limit equivalence as admitted-context). Standard tensor-calculus admission. Per physics-loop SKILL retained-proposal certificate item 4, branch-local derivations from retained inputs require independent audit before promotion to proposed_retained."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Israel-Carter-Robinson no-hair theorem (separate result).
- Promotion to retained / Nature-grade.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained framework GR: `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
- standard external references (theorem-grade, no numerical input):
  Birkhoff (1923) *Relativity and Modern Physics*, Harvard;
  Wald (1984) *General Relativity*, §6.1;
  Hawking-Ellis (1973) *The Large-Scale Structure of Space-Time*,
  ch. 5.4.
