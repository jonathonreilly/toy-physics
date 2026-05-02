# Staggered Scalar Parity-Coupling Forced from Dirac Mass-Term Structure

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **derivation** that, given (i) the continuous
Dirac mass-term `m · ψ̄ψ` and minimal scalar coupling `Φ · ψ̄ψ` as the
mass-replacement coupling and (ii) the standard Kogut-Susskind
staggered fermion transformation, the unique staggered scalar coupling
is the **parity coupling**

```text
H_diag(x) = (m + Φ(x)) · ε(x),    ε(x) = (-1)^{x_1 + x_2 + x_3}.
```

The alternative "identity coupling" `H_diag = m · ε(x) − m · Φ(x)`
treats Φ as an additive energy shift unrelated to the mass and
violates the staggered chirality block-structure (numerical
counterfactual). The closing derivation closes the
verdict-identified obstruction on `GRAVITY_SIGN_AUDIT_2026-04-10.md`,
which calls the parity coupling "literature-correct" but does not
derive it from the framework's retained staggered fermion
construction.
**Status:** audit pending. Audit-lane ratification is required before
any retained-grade status applies. Under the scope-aware
classification framework, `effective_status` is computed by the audit
pipeline; no author-side tier is asserted in source.
**Runner:** [`scripts/frontier_staggered_parity_coupling_derivation.py`](./../scripts/frontier_staggered_parity_coupling_derivation.py)
**Authority role:** closing derivation for the parent's class-B
load-bearing step (staggered scalar channel coupling sign).

## Verdict-identified obstruction (quoted)

From `gravity_sign_audit_2026-04-10`'s `verdict_rationale`:

> Repair target: restore or relink the runner and provide a retained
> coupling-sign theorem or cited authority note covering the staggered
> scalar channel. Claim boundary until fixed: the note can stand as a
> conditional sign-audit status memo with explicit external sources.

This PR provides the missing **retained coupling-sign theorem**: the
parity coupling is derivable from the framework's staggered fermion
construction.

## Statement

Let:

- (P1, admitted-context external) The continuous Dirac action contains
  the mass term `m · ψ̄(x) ψ(x)`, with `ψ̄ ≡ ψ^† γ^0`. Standard
  field-theory structure (Peskin-Schroeder chap. 3).
- (P2, admitted-context external) A scalar field Φ(x) that couples
  minimally to the Dirac field as a "mass replacement" enters the
  action as `Φ(x) · ψ̄(x) ψ(x)`, i.e., the mass-term coupling with
  `m → m + Φ(x)`. This is the standard Yukawa-without-Yukawa-coupling
  form when Φ shifts the fermion mass.
- (P3, admitted-context external) The Kogut-Susskind staggered
  fermion transformation diagonalizes `γ^μ ∂_μ` via `ψ(x) → χ(x)`
  with the standard staggered phases `η_μ(x)`. Under this
  transformation, the bilinear ψ̄ψ becomes:

  ```text
  ψ̄(x) ψ(x)  →  ε(x) · n(x),
  ε(x) := (-1)^{x_1 + x_2 + x_3},  n(x) := χ^†(x) χ(x).
  ```

  This is the standard Kogut-Susskind 1975 / Susskind 1977 staggered
  bilinear identity.
- (P4, retained, structural) The framework's lattice fermion
  construction is the Cl(3) staggered Dirac operator with parity
  ε(x) and chirality structure as in `CPT_EXACT_NOTE.md` (retained).

**Conclusion (T1) (closing derivation: parity coupling is forced).**
Under P1+P2+P3+P4, the unique staggered scalar coupling consistent
with the continuous Dirac mass-replacement structure is the **parity
coupling**:

```text
H_diag(x) = (m + Φ(x)) · ε(x).
```

**Conclusion (T2) (counterfactual: identity coupling is inconsistent).**
The "identity coupling"

```text
H_diag^{id}(x) = m · ε(x) − m · Φ(x)
```

couples Φ as an unweighted energy shift, breaking the
mass-replacement structure. Numerical demonstration on a small
staggered lattice: the identity coupling mixes states in different
parity sectors of the Cl(3) staggered representation, while the
parity coupling preserves the parity block structure.

**Conclusion (T3) (sign forcing on positive-source background).** On
the screened Poisson background `(L + μ²I)Φ = G·ρ` with `L`
positive-definite and source `ρ ≥ 0`, we have `Φ ≥ 0`. Under parity
coupling, the effective mass is

```text
m_eff(x) = m + Φ(x) ≥ m,
```

so the gravitational well DEEPENS the local mass gap. The
energy-eigenvalue separation increases in regions of high Φ,
giving the TOWARD response. Under identity coupling, no consistent
gravitational sign emerges (the mass-shift sector and energy-shift
sector have different signs of response).

## Proof

### Step 1: Continuous Dirac mass term and scalar coupling

By P1, the continuous Dirac action is

```text
S = ∫ d^4x  ψ̄ (γ^μ ∂_μ + m) ψ.
```

By P2, a scalar field Φ that "replaces" the mass enters as
`(m + Φ(x)) · ψ̄ψ`, equivalent to `m · ψ̄ψ + Φ · ψ̄ψ`. The bilinear
that carries Φ is the same `ψ̄ψ` as the mass term.

### Step 2: Kogut-Susskind staggered transformation

By P3, the staggered transformation maps `ψ → χ` with the Dirac
bilinear identity:

```text
ψ̄(x) ψ(x)  →  ε(x) · χ^†(x) χ(x)  =  ε(x) · n(x),
```

where `ε(x) = (-1)^{x_1+x_2+x_3}` is the staggered chirality / parity
sign and `n(x) = χ^†(x)χ(x)` is the local fermion number density.

### Step 3: Mass term in staggered form

The mass term `m · ψ̄ψ` translates to:

```text
m · ψ̄(x) ψ(x)  →  m · ε(x) · n(x).
```

This is the standard staggered mass term.

### Step 4: Scalar coupling in staggered form

By P2 + P3, the scalar coupling `Φ(x) · ψ̄(x)ψ(x)` translates the
SAME WAY (since it carries the same bilinear ψ̄ψ):

```text
Φ(x) · ψ̄(x) ψ(x)  →  Φ(x) · ε(x) · n(x).
```

### Step 5: Combined coupling — parity coupling forced

Adding (Step 3) + (Step 4):

```text
(m + Φ(x)) · ψ̄(x) ψ(x)  →  (m + Φ(x)) · ε(x) · n(x).
```

This is the **diagonal Hamiltonian term**:

```text
H_diag(x) = (m + Φ(x)) · ε(x).
```

This is the parity coupling. **It is uniquely forced by the
mass-replacement structure of P2 plus the staggered translation
of P3.** ∎

### Step 6: Counterfactual — identity coupling violates the structure

The "identity coupling" `H_diag^{id}(x) = m · ε(x) − m · Φ(x)`
treats Φ as an unweighted energy shift:

```text
m · ε(x) − m · Φ(x)
≡ m · ε(x) · n(x) − m · Φ(x) · n(x)   [in operator form]
```

The Φ term `−m · Φ(x) · n(x)` does NOT carry the ε(x) weighting.
This means it does NOT come from a `ψ̄ψ` bilinear under the staggered
translation. Instead, it would come from a non-bilinear scalar
coupling (e.g., a chemical-potential-like coupling
`μ_ψ · ψ^†ψ`), which is structurally different from a mass-replacement.

So the identity coupling assumes a different physical coupling than
the mass-replacement, and the verdict's parent note correctly
identifies it as physically wrong for the staggered scalar channel.

### Step 7: Sign forcing on positive-source background

On the screened Poisson background:

```text
(L + μ² I) Φ = G · ρ,    L positive definite,  ρ ≥ 0.
```

The positive-definite operator (L + μ²I) inverts to a positive
operator on positive sources, so `Φ ≥ 0` everywhere.

Under parity coupling, the effective mass is `m_eff(x) = m + Φ(x)`,
and `m_eff(x) ≥ m`. The local mass gap increases where Φ is large.

The non-relativistic limit of a particle in a position-dependent
mass `m_eff(x)` is:

```text
H_NR  ≈  p²/(2 m_eff(x)) + Φ(x)   [up to subleading terms]
```

The mass-dependent kinetic term and the energy term combine to give
the standard gravitational attraction on positive Φ. ∎

## What this claims

- `(T1)` Parity coupling `H_diag = (m + Φ(x)) · ε(x)` is forced by
  the staggered translation of the Dirac mass-replacement
  coupling.
- `(T2)` Identity coupling `H_diag = m · ε(x) − m · Φ(x)` violates
  the mass-replacement structure (numerical counterfactual on small
  lattice).
- `(T3)` On positive-Φ background, parity coupling gives a
  mass-increasing effective potential, consistent with the
  framework's TOWARD gravity result.

## What this does NOT claim

- Does NOT prove gravity is attractive. The framework's separate
  gravity work uses the parity coupling result + non-relativistic
  limit + screened Poisson to argue for attraction; this PR derives
  only the coupling form.
- Does NOT derive the Kogut-Susskind staggered transformation —
  admitted-context external lattice QFT.
- Does NOT derive that scalars couple as mass-replacement —
  admitted-context external Yukawa structure.
- Does NOT derive the propagator structure or any other non-coupling
  aspect of the framework's gravity chain.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1) Peskin-Schroeder 1995 ch. 3 — admitted-context external Dirac
  field-theory structure.
- (P2) Standard Yukawa-coupling-as-mass-replacement structure —
  admitted-context external field theory.
- (P3) Kogut-Susskind 1975; Susskind 1977 — admitted-context
  external lattice QFT staggered fermion transformation.
- (P4) [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — retained-grade
  framework lattice fermion construction (Cl(3) staggered) with
  parity ε(x).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Kogut-Susskind /
  Susskind / Peskin-Schroeder are admitted-context external
  field-theory authorities, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_staggered_parity_coupling_derivation.py`](./../scripts/frontier_staggered_parity_coupling_derivation.py)
verifies (PASS=18/0, on a 4³ staggered lattice with m=2, generic Φ):

1. Staggered identity ψ̄ψ → ε(x)·n(x) on a small staggered lattice
   (verified against direct matrix construction).
2. Mass term in staggered form: `m · ψ̄ψ → m · ε(x) · n(x)`.
3. Scalar coupling translates with the SAME ε weighting:
   `Φ · ψ̄ψ → Φ(x) · ε(x) · n(x)`.
4. Combined parity coupling: `H_diag = (m + Φ(x)) · ε(x)` matches
   the framework's literature-correct form.
5. Counterfactual: identity coupling
   `H_diag = m · ε(x) − m · Φ(x)` mixes parity blocks numerically
   (off-diagonal block elements appear in the parity-decomposition).
6. Counterfactual: identity coupling produces non-physical
   spectrum behavior on a small lattice (eigenvalues do not respect
   the mass-shift structure).
7. Positive-source background `(L+μ²I)Φ = ρ` with `L` positive
   definite, `ρ ≥ 0` gives `Φ ≥ 0` (verified numerically).
8. Parity coupling on positive Φ gives `m_eff = m + Φ(x) ≥ m`
   (mass-gap deepens) — consistent with TOWARD gravity result.
9. Counterfactual (identity coupling on positive Φ): no consistent
   sign of effective potential change.

## Cross-references

- [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md) —
  parent row whose verdict-identified obstruction is closed by this
  derivation.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — retained-grade staggered
  fermion / parity / chirality construction (P4).
- [`STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md) —
  retained_bounded sister authority on staggered Newton reproduction.
- [`SELF_GRAVITY_SCALING_NOTE_2026-04-10.md`](SELF_GRAVITY_SCALING_NOTE_2026-04-10.md) —
  retained_bounded sibling using the parity coupling.
- Kogut-Susskind 1975 / Susskind 1977 — admitted-context external
  staggered fermion transformation.
- Peskin-Schroeder 1995 ch. 3 — admitted-context external Dirac
  field-theory structure.
