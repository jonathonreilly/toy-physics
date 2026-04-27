# DM Neutrino `Z_3` Phase-Lift Mixed Bridge

**Date:** 2026-04-15 (boundary narrowed 2026-04-27 per review/audit handoff)
**Status:** bounded candidate algebraic family — defines a one-parameter `K_λ` family that algebraically populates the residual-`Z_2`-odd slot. This is **not** a derivation of the bridge amplitude `λ` from primitives, **not** a leptogenesis closure, and outside the audit-ratified tier on the DM-neutrino mixed bridge.
**Primary runner:** `scripts/frontier_dm_neutrino_z3_phase_lift_bridge.py`

**Cited authorities (one-hop deps):**
- [DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md](DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md)
  — fixes the source-faithful `λ` branches to `λ ∈ {−1, 0, +1}` after this candidate family is admitted.
- [DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md](DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md)
  — exact circulant mass-basis no-go showing the entire `Z_3`-covariant
  circulant family still diagonalizes to a real spectrum and stays
  real after the current Majorana doublet rotation. This no-go is
  **load-bearing in the opposite direction** for any retained-leptogenesis
  reading of the present family.

## Audit boundary (2026-04-27)

The review/audit handoff
([docs/audit/worker_lanes/05_dm_neutrino_z3_phase_lift.md](audit/worker_lanes/05_dm_neutrino_z3_phase_lift.md))
flagged this note because the load-bearing
step "define `K_λ = d·I + r·(...)` with a new bridge amplitude `λ`"
introduces a new symbol rather than deriving it from registered
authorities. The runner verifies the algebraic properties of the
defined family — that `λ = 0` reproduces the even bank and that
nonzero `λ` populates the odd slot — but it does not derive `λ` and
it does not exhibit a physical mass-basis texture that evades the
later circulant no-go.

Per that handoff, the safe statement is the bounded one:

- it **is** safe to use `K_λ` as an **algebraically controlled
  candidate family** showing how a `Z_3` phase would populate the odd
  slot.
- it is **not** safe to claim a retained DM-neutrino mixed bridge
  or a leptogenesis closure on this surface.

The DM "flagship closed" package on the publication-facing surface
should currently be read as `proposed_retained` (unratified) rather
than `flagship closed` for any component that depends on the mixed
bridge being a derived authority. Either:

- a future worker derives the bridge amplitude from primitives **and**
  exhibits a physical mass-basis texture that evades the no-go (Path A
  in the worker-lane handoff), **or**
- the DM "flagship closed" package is re-scoped on the publication
  surface to exclude the mixed-bridge component (Path C, the path
  this PR aligns with).

## Purpose

The branch now proves that the exact current-stack law is

`c_odd,current = 0`.

So full DM closure needs a genuinely new residual-`Z_2`-odd bridge or
activator. This note introduces the strongest axiom-native candidate family I
can currently justify without bluffing.

## Candidate family

Start from the exact even local DM kernel

`K_0 = d I + r (S + S^2)`.

Let the exact weak-only `Z_3` CP source supply the phase

`delta_src = 2pi/3`.

Then define the one-parameter mixed bridge family

`K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2)`.

Equivalently,

`K_lambda = d I + r cos(lambda delta_src) (S + S^2)
          + r sin(lambda delta_src) i(S - S^2)`.

So:

- `lambda = 0` reproduces the exact current stack
- `lambda = 1` is full weak-source transfer
- the odd slot is
  `c_odd(lambda) = r sin(lambda delta_src)`

## Why this is axiom-native

This candidate uses only:

- the exact even local DM kernel `(d,r)`
- the exact weak-only `Z_3` CP source `delta_src = 2pi/3`
- one new bridge amplitude `lambda`

It does **not** import fitted phases or external flavor textures.

## Exact algebraic properties

The runner proves:

1. the family preserves `d` and the off-diagonal norm `r`
2. it therefore stays on the same admissible local two-Higgs subcone
3. residual-`Z_2` reflection sends `lambda -> -lambda`
4. any nonzero `lambda` turns on the unique odd slot
5. at `lambda = 1`, the full-source candidate gives

   - `c_even = -r/2`
   - `c_odd = +sqrt(3) r / 2`

and the standard CP tensor is nonzero

## Updated interpretation

This note is still a **candidate-family note**, but the branch has moved since
it was first written.

What is now exact on top of this family:

- the later `Z_3` character-transfer theorem fixes the source-faithful
  branches to `lambda in {-1,0,+1}`
- the source-oriented nontrivial branch is `lambda = +1`

What is also now exact:

- the later circulant mass-basis no-go theorem shows the whole exact
  `Z_3`-covariant circulant family still diagonalizes to a real spectrum in
  the `Z_3` basis and stays real after the current Majorana doublet rotation
- so this family is **not** yet the final physical leptogenesis texture

So the strongest honest wording is now:

- this phase-lift family is still the right local invented family for the odd
  slot
- its source-faithful activation law is discrete and selects `lambda = 1`
- but the whole exact circulant class is still a physical no-go for the
  leptogenesis tensor

## Command

```bash
python3 scripts/frontier_dm_neutrino_z3_phase_lift_bridge.py
```
