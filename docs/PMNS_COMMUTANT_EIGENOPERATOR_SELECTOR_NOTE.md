# PMNS Commutant Eigenoperator Selector

**Date:** 2026-04-16  
**Status:** bounded - bounded or caveated result note
**Script:** `scripts/frontier_pmns_commutant_eigenoperator_selector.py`

## Question

Can a non-`Cl(3)` projected commutant eigenoperator on the `hw=1` triplet
produce a corner-distinguishing C3 Fourier-mode decomposition with a
C3-trivial-rep (even) and C3-fundamental-rep (odd) split, with a derivable
one-way Cl(3)-span vanishing check and a demonstrated nonzero odd example?

## Bottom line

Yes. This note's bounded scope covers exactly the C3-representation-theoretic
decomposition of the corner-trace profile of a projected non-`Cl(3)`
commutant generator. It does **not** close a bridge from this Fourier
decomposition to physical PMNS observables (the τ branch bit, the q passive
offset class label, or any other PMNS reduced-class readout). That bridge is
**not** in the load-bearing chain of this note (see "Claim scope" below).

The projected commutant route produces an exact decomposition law on the
`hw=1` corner orbit:

- the C3-trivial-rep Fourier mode of the corner-trace profile is the orbit
  average (even mode)
- the C3-fundamental-rep Fourier modes are the corner-distinguishing
  conjugate pair (odd modes)
- every projected `Cl(3)`-span element has vanishing odd modes
- the demonstrated projected non-`Cl(3)` commutant generator has nonzero odd
  modes

So the bounded claim is purely an algebraic-representation-theoretic content
identity: it gives a canonical even + odd decomposition of any C3-orbit
3-vector, a one-way `Cl(3)`-span vanishing certificate, and one explicit
non-`Cl(3)` corner-distinguishing example.

## Claim scope (narrowed)

> **Bounded algebraic statement.** On the `hw=1` corner orbit `{X1, X2, X3}`,
> the corner-trace profile `v = (tr P_i^* M P_i)_{i=1,2,3}` of any operator
> `M` (literal complex trace, no Hermitianization) admits the canonical
> decomposition into C3 irreps:
>
> ```
> v_0 = (v_1 + v_2 + v_3) / 3                           (C3-trivial rep)
> v_+ = (v_1 + ω v_2 + ω^2 v_3) / 3                     (C3-fundamental rep, +)
> v_- = (v_1 + ω^2 v_2 + ω v_3) / 3                     (C3-fundamental rep, -)
> ```
> with `ω = exp(2πi/3)`. For Hermitian `M`, `v_i` is real for each `i`, and
> the two odd modes satisfy `v_- = conj(v_+)`. The runner verifies, on the
> literal complex profile `v_i = tr(P_i^* M P_i)`, that the odd modes
> `(v_+, v_-)` vanish on the projected `Cl(3)` basis (hence on its span by
> linearity), and that they are nonzero on the demonstrated Hermitian
> projected non-`Cl(3)` commutant generator. The demonstrated generator is
> chosen to be Hermitian so the literal complex profile is real and the
> conjugate-pair relation holds on the example; the choice is consistent
> because the commutant of a Hermitian gamma set is closed under Hermitian
> conjugation, so the projected commutant always admits a Hermitian
> representative outside the projected `Cl(3)` span.

This is a one-way scope statement. Nonzero odd mode certifies that a generator
is outside the projected `Cl(3)` span, but zero odd mode is not claimed to
certify membership in that span.

**This note explicitly does NOT claim:**

- that `v_0` IS the PMNS passive-offset class label `q`;
- that `Re(v_+)` IS the PMNS branch / orientation selector bit `τ`;
- that the q/τ extraction maps `q := argmax(...)` and `τ := sign(Re(v_+))`
  used by the runner are the canonical PMNS-observable readouts;
- any axiom-native PMNS selector value law beyond the algebraic
  decomposition itself.

The bridge from `(v_0, v_+)` to PMNS-observable selector labels (`q`, `τ`)
is the parent's previously load-bearing renaming; under this narrowing it is
**reframed as an operational definition**, not a derived readout, and is
explicitly excluded from the load-bearing chain. Any downstream cite of this
note for a PMNS-physical readout must supply that bridge separately.

## Exact construction

Start from the exact `Cl(3)` on `Z^3` generation boundary:

- build the projected commutant on each `hw=1` corner
- pick a Hermitian projected commutant generator outside the projected
  `Cl(3)` span (such a representative exists because the commutant of a
  Hermitian gamma set is closed under Hermitian conjugation)
- lift that projected eigenoperator back to the ambient taste space
- compute the literal complex corner-trace profile
  `v = (tr P_i^* M P_i)_{i=1,2,3}` on `X_1, X_2, X_3` (no Hermitianization
  of the projected operator; the Hermiticity of `M` makes each `v_i`
  numerically real on the example)
- decompose `v` into the C3 Fourier modes `(v_0, v_+, v_-)`

For the corner profile `v = (v_1, v_2, v_3)`, define

`v_0 = (v_1 + v_2 + v_3) / 3`

`v_+ = (v_1 + ω v_2 + ω^2 v_3) / 3`

`v_- = (v_1 + ω^2 v_2 + ω v_3) / 3`

with `ω = exp(2πi/3)`.

Then:

- `v_0` is the C3-trivial-rep (even) mode = orbit average
- `(v_+, v_-)` are the C3-fundamental-rep (odd) modes = conjugate pair on
  real profiles
- `(v_+, v_-)` are zero on the projected `Cl(3)` basis and nonzero on the
  demonstrated projected non-`Cl(3)` generator

## Exact theorem statement (narrowed)

**Theorem (C3 Fourier decomposition of the projected commutant
corner-trace profile).** On the `hw=1` triplet, the corner-trace profile of
the lifted projected non-`Cl(3)` commutant generator admits an exact C3
representation-theoretic decomposition:

1. the C3-trivial-rep (even) Fourier mode equals the corner-orbit average
2. the C3-fundamental-rep (odd) Fourier modes form a conjugate pair on real
   profiles
3. the odd modes vanish on the projected `Cl(3)` span and are nonzero on the
   demonstrated projected non-`Cl(3)` commutant generator

This is a finite-dimensional representation-theoretic identity. It does not
constitute a PMNS microscopic closure theorem and it does not derive a
bridge from the Fourier modes to the PMNS τ/q observable labels.

## Operational reduction (q, τ): scope-only

For an operational tag on the canonical projected generator used by the
runner, the reduced labels (computed by the operational maps `q :=
argmax(v_0, v_0 - Re v_+, v_0 + Re v_+)` and `τ := 0 if Re(v_+) >= 0 else
1`) take the values:

- branch bit `τ = 0`
- passive offset label `q = 2`

These are stated **as operational definitions** on the demonstrated
projected eigenoperator: under this narrowing they are not asserted to
equal physical PMNS observables, but only to be a canonical operational
readout of the C3 Fourier decomposition. The theorem-level content is the
existence of the canonical even + odd Fourier split and the derivable
one-way vanishing certificate for the odd mode.

## Consequence

Within the bounded scope, this note closes the C3
representation-theoretic content of the projected non-`Cl(3)` commutant
eigenoperator's corner-trace decomposition. The PMNS-observable readout
bridge (τ, q ↔ Fourier modes) is removed from the load-bearing chain and
must be supplied separately by any downstream use that needs a physical
selector value law.

## Command

```bash
python3 scripts/frontier_pmns_commutant_eigenoperator_selector.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by
a prior conditional audit so the audit citation graph can track them. It
does not promote this note or change the audited claim scope.

- The narrowed claim depends only on:
  - the exact `Cl(3)` on `Z^3` generation boundary geometry
  - the projected commutant construction on each `hw=1` corner
  - the C3 cyclic group representation theory (finite-dimensional
    character decomposition)
- It does **not** claim the converse that every zero-odd projected commutant
  direction lies in the projected `Cl(3)` span.
- It does **not** depend on, and does not derive, any PMNS observable
  bridge: `τ`, `q`, or any reduced-class-space PMNS selector value law.
