# DM Neutrino `Z_3` Phase-Lift Discrete-Quantized Bridge

**Date:** 2026-04-15 (upgraded 2026-04-27 per audit-lane verdict)
**Status:** proposed_retained discrete-quantized phase-lift family. The bridge amplitude `λ` is **not** a free parameter; it is derived by the registered character-transfer theorem to take values `λ ∈ {−1, 0, +1}`, with `λ = +1` selected by the retained source orientation `δ_src = +2π/3`. The K_λ family carries the unique source-faithful odd slot for the residual-`Z_2`-odd channel.
**Primary runner:** `scripts/frontier_dm_neutrino_z3_phase_lift_bridge.py`

**Cited authorities (one-hop deps):**
- [DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md](DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md)
  — exact theorem deriving `λ ∈ Z` from `Z_3`-source faithfulness
  (`χ(λ)³ = 1`), with `λ = +1` selected by source orientation. This
  is the load-bearing derivation of the bridge amplitude.
- [DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md](DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md)
  — separate exact no-go showing the entire `Z_3`-covariant circulant
  class diagonalizes to a real spectrum and stays real after the
  current Majorana doublet rotation. **Bounds the leptogenesis
  consequence, not the bridge derivation.**

## Audit boundary (2026-04-27)

The audit-lane verdict
([docs/audit/worker_lanes/05_dm_neutrino_z3_phase_lift.md](audit/worker_lanes/05_dm_neutrino_z3_phase_lift.md))
classified an earlier version of this note as `audited_renaming`
because the front matter introduced `λ` as if it were a free
parameter ("define `K_λ` ... with a new bridge amplitude `λ`"). At
the time of that audit, the character-transfer theorem existed but
was not registered as a one-hop dependency, so the auditor could not
see that `λ` is in fact derived.

This PR closes that gap. With the character-transfer theorem
registered above, the bridge amplitude is no longer free: it is
discretely quantized by exact `Z_3`-source faithfulness to
`λ ∈ {−1, 0, +1}`, and the retained source orientation
`δ_src = +2π/3` selects `λ = +1` as the unique physical nontrivial
branch.

The earlier "renaming" classification was correct against the older
front matter framing; it is no longer correct against the current
chain. The audit should re-evaluate against the registered chain.

## Two distinct claims in this note

The note carries **two distinct claims** that the audit lane should
evaluate separately:

**Claim 1 (proposed_retained discrete-quantized bridge):**
The phase-lift family `K_λ = d·I + r·(e^{iλδ_src} S + e^{−iλδ_src} S²)`
is the unique algebraic candidate populating the residual-`Z_2`-odd
slot from the exact even local DM kernel `(d, r)` plus the exact
weak-only `Z_3` CP source. The amplitude `λ` is **derived** by the
character-transfer theorem to be `+1` on the physical branch.

**Claim 2 (bounded — limited by no-go):**
The resulting `K_{λ=1}` populates the odd slot algebraically, but
the **circulant mass-basis no-go theorem** shows the entire
`Z_3`-covariant circulant family diagonalizes to a real spectrum in
the `Z_3` basis and stays real after the Majorana doublet rotation.
So this bridge family is **not** the final physical leptogenesis
texture; the no-go bounds the lane's leptogenesis consequence
independently of whether the bridge family itself is derived.

This separation matters: the audit's "renaming" complaint was about
Claim 1 (the bridge derivation), and Claim 1 is now closed via the
character-transfer theorem. Claim 2 (the leptogenesis result) was
always bounded by the no-go and remains so.

## Purpose

The branch already proves that the exact current-stack law is

`c_odd,current = 0`.

So full DM closure needs a residual-`Z_2`-odd bridge or activator.
This note packages the unique axiom-native phase-lift family that
does this, with the bridge amplitude derived (not free) by the
character-transfer theorem.

## Bridge family (with derived amplitude)

Start from the exact even local DM kernel

`K_0 = d I + r (S + S^2)`.

Let the exact weak-only `Z_3` CP source supply the phase

`δ_src = 2π/3`.

Define the phase-lift family

`K_λ = d I + r (e^{i λ δ_src} S + e^{−i λ δ_src} S^2)`.

Equivalently,

`K_λ = d I + r cos(λ δ_src) (S + S^2) + r sin(λ δ_src) i(S − S^2)`.

By the registered character-transfer theorem, exact `Z_3` source
faithfulness requires `χ(λ) = exp(i λ δ_src)` to be a one-dimensional
`Z_3` character (`χ³ = 1`). This forces `λ ∈ Z`. On the local
continuity strip `|λ| ≤ 1`, the only source-faithful branches are
`λ ∈ {−1, 0, +1}`. The retained source orientation
`δ_src = +2π/3` selects the **physical** nontrivial branch:

    λ = +1   (derived; selected by source orientation)

So:

- `λ = 0` reproduces the exact current stack (zero odd slot)
- `λ = +1` is the source-oriented full-transfer branch (physical)
- `λ = −1` is the conjugate / reflected companion (non-physical
  under the retained orientation)
- the odd slot at `λ = +1` is `c_odd = +√3 r / 2`

## Why this is axiom-native

The chain uses only registered authorities:

- the exact even local DM kernel `(d, r)`
- the exact weak-only `Z_3` CP source `δ_src = 2π/3`
- the registered character-transfer theorem deriving `λ ∈ Z`
- the retained source orientation selecting `λ = +1`

It does **not** import fitted phases or external flavor textures, and
it does **not** introduce free parameters: the previously-named
"bridge amplitude `λ`" is fully determined by the registered chain.

## Exact algebraic properties

The runner proves:

1. the family preserves `d` and the off-diagonal norm `r`
2. it therefore stays on the same admissible local two-Higgs subcone
3. residual-`Z_2` reflection sends `λ → −λ`
4. any nonzero `λ` turns on the unique odd slot
5. at `λ = +1` (the derived physical branch), the source-faithful
   candidate gives
   - `c_even = −r/2`
   - `c_odd = +√3 r / 2`
6. the standard CP tensor is nonzero on the bridge family

## Boundary on the leptogenesis consequence

The registered circulant mass-basis no-go theorem is **load-bearing
in the opposite direction** for any retained-leptogenesis reading:
the entire exact `Z_3`-covariant circulant class still diagonalizes
to a real spectrum in the `Z_3` basis and stays real after the
current Majorana doublet rotation.

Therefore Claim 2 above is **bounded** independently of whether the
bridge family itself is derived. Closing Claim 2 requires either:

- a separate texture that exits the circulant class (e.g., a
  non-circulant deformation that respects source faithfulness),
  **or**
- an honest publication-side downgrade of the DM "flagship closed"
  package's leptogenesis component, since the present bridge does
  not supply a physical leptogenesis tensor.

This PR does not attempt to close Claim 2. It closes Claim 1 (the
bridge derivation) via the registered character-transfer theorem,
which directly addresses the audit's "renaming" verdict.

## Command

```bash
python3 scripts/frontier_dm_neutrino_z3_phase_lift_bridge.py
```
