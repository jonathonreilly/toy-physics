# Hierarchy-Scale Identification Theorem: a = ℓ_Planck (Conditional)

**Date:** 2026-05-02
**Type:** bounded_theorem
**Status:** proposed_retained bounded conditional identification corollary;
audit pending. Bridge dependency for
[EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md).
**Runner:** `scripts/frontier_hierarchy_scale_a_equals_planck_length.py`

## Purpose

Provide a registered audit-clean dependency note for the hierarchy-scale
identification `a ~ 1/M_Planck` used as an IF-condition in
[EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md).

This note **does not** claim a fresh first-principles derivation of the
absolute lattice spacing. It is a **graph-registration note** that records
the conditional algebraic identification

```
a / l_P = 1
```

as a corollary of the existing retained
[PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24](PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md)
and the
[PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
finite-patch extension, on the same conditional carrier surface those notes
already use.

## Theorem (Conditional identification)

**Theorem.** On the staggered `Cl(3)/Z^3` framework, given:

(P1) the primitive cell coefficient `c_cell = Tr(rho_cell P_A) = 1/4` of the
     [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24](PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md),

(P2) the gravitational area/action carrier identification: the primitive
     boundary count is the microscopic carrier of the standard gravitational
     area/action density,

(P3) the source-unit normalization fixing `lambda = 1`, hence
     `G_Newton,lat = 1`,

the absolute lattice spacing satisfies

```
a^2 = 4 * c_cell * l_P^2  =  l_P^2,
a / l_P = 1.
```

## Proof

The proof is the same algebraic step as
[PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24](PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md)
Section 2, repeated here for self-containment of this dependency note.

(P2) supplies the carrier matching

```
S_cell / k_B  =  c_cell A / a^2,        (lattice carrier on cell A)
S_grav / k_B  =  A / (4 l_P^2).         (Bekenstein-Hawking area density)
```

Equating the two same-surface densities on the gravitational carrier surface
gives

```
c_cell / a^2  =  1 / (4 l_P^2),        (P2)
a^2  =  4 c_cell l_P^2.                (algebra)
```

Substituting (P1)'s `c_cell = 1/4`:

```
a^2  =  4 * (1/4) * l_P^2  =  l_P^2,
a / l_P  =  1.                         QED
```

(P3) is the source-unit choice that makes the carrier identification
internally consistent (it removes the bare-source `2 sqrt(pi)` ambiguity).

## Scope (what this note proves and what it does NOT)

**Proves (conditional):**

- Given the registered conditional Planck-completion premise (P1)-(P3), the
  staggered Cl(3)/Z^3 absolute lattice spacing is exactly the Planck length.
- Hence the leading dim-6 LV correction in
  [EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
  is suppressed by `(E/M_Planck)^2` rather than some other scale.

**Does NOT prove:**

- An unconditional first-principles derivation of the absolute Planck scale
  from the bare finite Cl(3)/Z^3 stack alone — that route remains closed
  negatively in
  [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24](PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md).
- A removal of the carrier-identification premise (P2). The same hostile
  auditor who rejected the Planck-completion note's retained absolute
  derivation can still reject this corollary on the same grounds. This note
  inherits, not weakens, that premise.
- A claim that `hbar` or other SI Planck constants are predicted from the
  framework alone — those are unit-convention statements once SI is chosen.

The honest claim is therefore:

> Conditional on the same carrier premise that the
> Planck-completion packet already retains, the dimensional identification
> `a = l_P` follows by direct algebra from `c_cell = 1/4`. The
> Lorentz-emergence note can rely on this identification as a registered
> bridge dependency rather than as a plain-text assertion.

## Assumptions (registered)

(A1) Staggered Cl(3)/Z^3 framework with periodic boundary conditions and even
     `L`. Inherited from
     [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md).
(A2) Primitive cell-coefficient retained algebra `c_cell = 1/4`. Inherited
     from
     [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24](PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md)
     Section 1.
(A3) Gravitational area/action carrier identification. Conditional premise
     of the Planck-completion packet; not promoted here.
(A4) Source-unit normalization `lambda = 1`. Inherited from
     [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md).

## Runner

`scripts/frontier_hierarchy_scale_a_equals_planck_length.py`

The runner:

1. Computes `c_cell = Tr(rho_cell P_A)` directly on the time-locked primitive
   event cell `H_cell ~= C^{16}` with `rho_cell = I_16 / 16` and
   `P_A = P_t + P_x + P_y + P_z` of rank 4.
2. Verifies `c_cell = 1/4` to machine precision.
3. Computes the algebraic identification `a^2 / l_P^2 = 4 c_cell` for
   the conditional carrier matching.
4. Reports the closed-form ratio `a / l_P = 1` for the registered premise.
5. Verifies that the same primitive count under the bare-source convention
   (no source-unit normalization fix) reproduces the failure mode
   `a / l_P = 2 sqrt(pi)` documented in the Planck-completion note, so
   the source-unit fix is a load-bearing premise.

## Honest status

This is a **graph-registration corollary**, not a new physics result.

- It registers an explicit one-hop dep for the hierarchy-scale IF-condition
  of [EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md).
- It inherits the conditional carrier premise of the Planck-completion
  packet exactly as that note specifies.
- A hostile auditor can now follow the `a ~ l_P` claim to a registered
  derivation that bottoms out in a retained algebraic step plus an
  explicit, separately registered, conditional carrier premise.

The Lorentz-emergence note's experimental-precision phenomenological
table remains a calculation on this assumed scale surface, not a
ratified prediction. Promoting that table to retained physics still
requires either:

(i) ratifying the carrier-identification premise (P2) into a retained
    derivation, or

(ii) measuring an `(E/M_Planck)^2` LV signal whose angular structure
     matches the framework's cubic harmonic.

This note does not attempt either. It only closes the dep-graph hole.

## Relation to existing notes

- **Inherits:**
  [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24](PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md),
  [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md),
  [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md).
- **Cross-checked against (no-go boundary):**
  [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24](PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
  (this note does not violate the finite-only no-go because it explicitly
  uses the realified carrier premise).
- **Used by:**
  [EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
  (as a one-hop bridge dep for the `a ~ 1/M_Planck` IF-condition).
