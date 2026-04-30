# Koide `√m` Amplitude Principle Note

**Date:** 2026-04-18
**Status:** candidate extension note — narrows `P1` to a positive-parent /
one-leg-amplitude construction; does not yet derive the charged-lepton masses on
the retained surface
**Runner:** `scripts/frontier_koide_sqrtm_amplitude_principle.py`

## Question

The April 18 circulant note isolated the remaining `P1` ambiguity:

> why should the circulant eigenvalues be identified with `√m`, rather than `m`
> or `m²`?

Can that question be sharpened into a concrete internal construction, rather
than left as a free phenomenological guess?

## Bottom line

Yes.

The repo already uses a consistent **square-root dictionary** from positive
quadratic quantities to linear one-leg amplitudes:

1. In the charged-lepton review note, the second-order return operator `Σ` is a
   quadratic object; under the mass-squared convention, physical Koide lives on
   `√w`, not on `w`.
2. In the Yukawa color-projection theorem, LSZ gives `√Z_φ` per scalar external
   leg, not `Z_φ`.
3. In the positive polar-section theorem, a positive Hermitian parent `H`
   carries the unique positive square-root representative `H^(1/2)`.

So the natural internal route for `P1` is:

```
positive quadratic parent M   --->   one-leg amplitude operator Y = M^(1/2)
                                         with spectrum eig(Y) = √eig(M).
```

Applied to the Koide lane: if the charged-lepton masses arise as the spectrum of
a positive `C_3[111]`-covariant parent operator `M`, then the circulant
operator in the April 18 note should be interpreted as its principal square
root `Y = M^(1/2)`, and `λ_k = √m_k` follows automatically.

This does **not** finish the science. The missing step is now precise:

> derive the positive parent operator `M` on the charged-lepton `hw=1` lane.

And the new
[`KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`](./KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md)
shows an immediate complication: on the current retained charged-lepton
surface, any nontrivial positive `C_3[111]` parent lives in the
eigenvalue/Fourier channel, while the physical readout still uses the
axis-basis diagonal channel (`U_e = I_3`).
The companion
[`KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md`](./KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)
sharpens this further: merely enlarging the carrier beyond bare `hw=1` does not
evade the obstruction if the reduction back to the charged-lepton lane stays in
the current `C_3`-equivariant Schur/effective-operator class.

## Retained inputs

- [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](./CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  §7 convention note:
  `Σ` is quadratic; under Convention B, physical Koide is recovered on `√w`.
- [YUKAWA_COLOR_PROJECTION_THEOREM.md](./YUKAWA_COLOR_PROJECTION_THEOREM.md)
  §3:
  LSZ gives `√Z_φ` for one scalar external leg.
- [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md):
  a positive Hermitian parent has the unique positive square-root representative.
- `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`:
  the candidate circulant operator on the `C_3[111]` orbit.

## Exact square-root dictionary

### 1. Quadratic charged-lepton parent vs linear physical readout

The charged-lepton review note already isolates the convention issue cleanly:

- if `Σ` is read as a linear mass operator, one pins `w ~ m`;
- if `Σ` is read dimensionally as a quadratic parent, one pins `w ~ m²`;
- in the second reading, physical Koide is recovered on `√w ~ m`.

So the repo already distinguishes:

```
quadratic parent quantity   ->   linear physical amplitude / mass readout
```

by a principal square root.

### 2. LSZ gives the same square-root rule

The Yukawa theorem gives the physical Yukawa vertex
```
M_Y = √Z_ψ · √Z_φ · √Z_ψ · Γ_Y,
```
so a single scalar external leg contributes `√Z_φ`, not `Z_φ`.

This is the same structural rule:

```
positive quadratic residue Z   ->   one-leg amplitude factor √Z.
```

### 3. Positive parent operators carry unique square-root amplitudes

If `M` is positive Hermitian, then functional calculus gives the unique positive
square root
```
Y = M^(1/2),
```
with
```
Y² = M,
eig(Y) = √eig(M).
```

This is not extra philosophy; it is exact linear algebra and already used in
the positive polar-section theorem elsewhere in the repo.

### 4. `C_3` covariance is preserved by the square root

If `M` commutes with the retained `C_3[111]` action, then `M` is diagonal in the
same Fourier basis as the shift operator `C`. Therefore `M^(1/2)` is diagonal in
that same basis as well, so it also commutes with `C`.

Hence:

- positive `C_3`-covariant parent `M`  ->  positive `C_3`-covariant square root
  `Y = M^(1/2)`;
- `Y` is again circulant on the `hw=1` orbit;
- the spectral triple of `Y` is exactly `√m`.

So the charged-lepton square-root vector is the natural spectral amplitude of a
positive parent, not an arbitrary coordinate trick.

## Consequence for `P1`

`P1` is no longer best stated as

> “guess that the circulant eigenvalues are `√m`.”

It is better stated as

> “derive a positive `C_3[111]`-covariant parent operator `M` whose principal
> square root `M^(1/2)` is the charged-lepton circulant amplitude operator.”

Then:

```
eig(M) = (m_e, m_μ, m_τ)
eig(M^(1/2)) = (√m_e, √m_μ, √m_τ).
```

This reduces the open science from a dimensional-labeling ambiguity to a
concrete construction problem. The obstruction note sharpens it one step
further:

> derive both the positive parent `M` and the retained reduction/readout
> primitive that makes its nontrivial `C_3` eigenvalue channel physical on the
> charged-lepton lane.

## What this does not claim

- It does **not** derive the parent operator `M`.
- It does **not** prove that the current April 18 circulant `H` is already that
  `M^(1/2)`.
- It does **not** evade the current axis-basis readout obstruction.
- It does **not** upgrade the current retained charged-lepton status, which
  remains the bounded April 17 package.

## Paper-safe wording

> The `√m` readout in the Koide lane is not best viewed as an isolated
> phenomenological guess. The existing framework already uses a square-root
> dictionary from positive quadratic parents to linear one-leg amplitudes: in the
> charged-lepton convention note, physical Koide is recovered on `√w` when the
> second-order return is read as quadratic; in the Yukawa lane, LSZ gives
> `√Z_φ` per scalar external leg; and the positive polar-section theorem gives
> the unique positive representative `M^(1/2)` of a positive Hermitian parent
> `M`. Therefore the natural charged-lepton extension problem is to derive a
> positive `C_3[111]`-covariant parent operator `M` whose principal square root
> carries the Koide spectral amplitudes.
