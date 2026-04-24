# Planck-Scale Primitive Weyl Hbar Representation Theorem

**Date:** 2026-04-24
**Status:** structural textbook-appearance closure on the coherent realified representation surface
**Verifier:** `scripts/frontier_planck_primitive_weyl_hbar_representation_theorem_2026_04_24.py`

## Question

After the action-phase theorem gives

`S(H)/hbar = Phi(H)`,

can the usual appearances of `hbar` in quantum mechanics be derived rather
than imported separately?

## Result

Yes, on the coherent-history plus realified regular-representation surface.

The result is not a prediction of the SI decimal value of `hbar`. It is a
representation theorem: once the primitive action count is the universal-cover
phase generator, the same unit appears in

1. `E = hbar omega`;
2. `p = hbar k`;
3. `[X,P] = i hbar`;
4. `Delta X Delta P >= hbar/2`;
5. angular-momentum generators measured in units of `hbar`.

The finite cell supplies the exact Weyl character law. The textbook
commutator is obtained only after passing to the realified regular
representation envelope. This distinction is load-bearing: an exact
finite-dimensional canonical commutator `[X,P]=i hbar I` is impossible because
the trace of a commutator is zero.

## Theorem 1: retained translations force the Weyl character pair

The physical `Z^3` support supplies primitive translation histories. For a
one-axis submodule, write the translation count as `n in Z`. Its characters are

`chi_k(n) = exp(i k n)`.

Let `T_m` be translation by `m`, and let `M_k` be multiplication by the
character `chi_k`. Then

`T_m M_k T_m^{-1} = exp(i k m) M_k`.

Equivalently,

`T_m M_k = exp(i k m) M_k T_m`.

This is the Weyl relation. It is not an extra quantum postulate; it is the
character pairing of the retained translation group and its dual.

On a finite cyclic regulator, the same statement is the exact clock/shift law

`S C = omega C S`,

with `omega = exp(2 pi i/N)`. This finite law is exact, but it is not the
canonical commutator. The commutator belongs to the realified regular
representation envelope.

## Theorem 2: action-phase identification gives `p = hbar k`

The action-phase theorem gives

`U(H) = exp(i Phi(H)) = exp(i S(H)/hbar)`.

For a spatial character over physical displacement `x`, the phase is

`Phi = k x`.

The conventional action phase of a momentum eigenhistory is

`Phi = p x / hbar`.

Therefore

`p = hbar k`.

No dimensional constant is fitted here: `hbar` is the physical action assigned
to one primitive phase-count unit by the action-phase representation theorem.

## Theorem 3: time characters give `E = hbar omega`

The same argument applies to the retained time direction. A stationary
history has phase

`Phi = omega t`.

The conventional action phase is

`Phi = E t / hbar`.

Therefore

`E = hbar omega`.

## Theorem 4: the realified Weyl envelope gives `[X,P]=i hbar`

On the realified regular representation, define

`(T(u) psi)(x) = psi(x-u)`,

and

`(M(k) psi)(x) = exp(i k x) psi(x)`.

Then

`T(u) M(k) = exp(-i u k) M(k) T(u)`.

By Stone's theorem,

`T(u) = exp(-i u P/hbar)`,

and the character operator is

`M(k) = exp(i k X)`.

Differentiating the Weyl relation at `u=0` and `k=0` gives

`[X,P] = i hbar I`.

The finite cyclic clock/shift pair is therefore the exact finite Weyl shadow;
the canonical commutator is the infinitesimal realified representation
corollary.

## Theorem 5: uncertainty follows without a new constant

For any state in the domain of `X` and `P`, the Robertson inequality gives

`Delta X Delta P >= (1/2) |<[X,P]>|`.

Using Theorem 4,

`Delta X Delta P >= hbar/2`.

Thus the uncertainty floor uses the same action-phase unit. No separate
uncertainty constant is imported.

## Theorem 6: angular momentum is measured in the same unit

A rotation history is represented coherently as

`R(phi) = exp(-i phi J/hbar)`.

Since `hbar` is already the action unit converting phase to physical action,
the generator `J` is measured in units of `hbar`.

For orbital rotations,

`L = X x P`,

so the same `P = hbar k` result fixes orbital angular momentum units.

For the retained Clifford spin representation, the even Clifford algebra gives
the usual `su(2)` generators. With Pauli normalization,

`J_i = (hbar/2) sigma_i`,

and

`[J_i,J_j] = i hbar epsilon_ijk J_k`.

Thus half-integer spin units are also downstream representations of the same
primitive action-phase unit, not independent constants.

## Strongest Endpoint Claim

Use:

> Bare physical `Cl(3)` / `Z^3`, once first-order realified response and
> coherent histories are derived as native semantics, forces Planck spacing,
> the structural action quantum `S/hbar=Phi`, and the standard Weyl,
> commutator, uncertainty, energy-frequency, momentum-wavenumber, and
> angular-momentum appearances of `hbar`.

Do not use:

> Finite automorphisms alone give the exact canonical commutator.

Do not use:

> The SI decimal value of `hbar` is predicted.

Do not use:

> The gravitational and coherent-history representation surfaces are optional
> presentation choices.

