# Action Universality: F∝M exponent = power of f in the action

**Date:** 2026-04-04
**Status:** bounded fixed-family universality-class result

## Primary artifact chain

- Script: [`scripts/action_universality_probe.py`](/Users/jonreilly/Projects/Physics/scripts/action_universality_probe.py)
- Log: [`logs/2026-04-04-action-universality-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-universality-probe.txt)
- Companion sweep: [`docs/ACTION_POWER_SCALING_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_POWER_SCALING_SWEEP_NOTE.md)

This is a bounded replay on one fixed retained family:

- 3D ordered dense lattice
- `h = 0.5`, `W = 8`, `L = 12`
- kernel `1/L^2` with `h^2` measure
- field `s/r`

It should be read as a universality-class probe on that family, not as a
universal theorem over all architectures.

## Frozen replay finding

On this fixed family, the mass-scaling exponent tracks the weak-field power of
`f` in the action:

| Action | f-power | F∝M | Born |
|--------|---------|-----|------|
| `S = L(1-f^0.5)` | `0.5` | `0.50` | `2.50e-15` |
| `S = L(1-f)` | `1.0` | `1.00` | `2.50e-15` |
| `S = L(1-f^2)` | `2.0` | `2.00` | `2.50e-15` |

Companion fixed-family rows from the same replay:

- `S = L` gives no gravity
- `S = L(1+f)` gives AWAY
- `S = -Lf` gives AWAY
- `S = L exp(-f)` gives `F~M = 1.00`
- `S = L/(1+f)` gives `F~M = 1.00`

Born stays machine-clean for every tested action on this family.

## Newtonian gravity requires f-linear action

Any action that's linear in f at weak field gives F∝M = 1.0:
  S = L(1-f), S = L·exp(-f), S = L/(1+f)

These all expand to S ≈ L(1-f) + O(f²) at weak field.
The Newtonian distance law 1/b follows from the f-linear
phase integral (derived analytically).

## Phase valley is necessary

Phase HILL actions (S increasing with f) give AWAY:
  S = L(1+f): AWAY
  S = -Lf: AWAY

Phase VALLEY (S decreasing with f) is required for TOWARD gravity.
No coupling (S = L): no gravity.

## The bounded selection rule

**Newtonian gravity = phase valley + f-linear at weak field.**

This is a two-condition selection from the model's axioms:
1. Gravity is TOWARD → action must create a phase valley (S decreases near mass)
2. F ∝ M (Newtonian) → action must be linear in f at weak field

Together: `S = L × g(f)` where `g(0)=1`, `g'(0)<0`, and `g(f)` is
approximately `1-f` near `f=0`. On the frozen ordered-lattice family, the
specific form of `g` (exponential, reciprocal, linear) matters less than the
weak-field linear behavior.

## What this means

The valley-linear action is **not unique**. It is the simplest member of a
bounded universality class: on the frozen ordered-lattice family, all tested
weak-field-linear phase valleys give Newtonian mass scaling.

The spent-delay (sqrt) and quadratic actions sit in different observed
universality classes, giving different mass-scaling laws.

## What this does not prove

- It does **not** prove a universal theorem across all graph families.
- It does **not** prove that distance-law exponents are equally universal.
- It does **not** settle the irregular-geometry spent-delay lane.
- It does **not** derive the action law uniquely from the axioms.

The strongest safe read is:

- the clean theorem-candidate here is about `F~M`
- the relevant object is a weak-field-linear phase-valley universality class
- that claim is now artifact-backed on one retained ordered-lattice family

## Frozen fixed-family classes

The retained probe also separates the tested actions into clear fixed-family
classes:

| Class | Representative actions | Frozen read on this family |
|-------|-------------------------|----------------------------|
| no coupling / hill | `S=L`, `S=L(1+f)`, `S=-Lf` | no desired TOWARD response |
| sublinear valley | `S=L(1-f^0.5)` | TOWARD, `F~M = 0.50`, shallower tail |
| weak-field-linear valley | `S=L(1-f)`, `S=L exp(-f)`, `S=L/(1+f)` | TOWARD, `F~M = 1.00`, matching tail on this family |
| superlinear valley | `S=L(1-f^2)` | TOWARD, `F~M = 2.00`, steeper tail on this family |

The clean retained statement is:

- weak-field-linear phase valleys share a Newtonian-like mass-scaling class on
  the fixed ordered-lattice family
- the mass-law statement is cleaner than the distance-law statement
- broader tail universality across powers is now bounded by the companion
  fixed-family sweep, but still not promoted to a universal theorem
