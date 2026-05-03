# Conditional EWSB Q = T_3 + Y/2 on Derived SM Rep + Named Obstruction

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **conditional derivation** that, given the
framework's derived SM matter representation (cycles 01+02+04+06) and
admitting a scalar field Φ in the (2, +1)_Y representation of
SU(2)_L × U(1)_Y with non-zero vacuum expectation value (VEV) in its
lower (T_3 = -1/2) component, the unbroken U(1) generator of the
residual symmetry SU(2)_L × U(1)_Y → U(1)_em is uniquely

```text
Q = T_3 + Y/2     (doubled-Y convention),
```

and the Q-eigenvalues on the framework's derived SM matter form the
spectrum {0, ±1/3, ±2/3, ±1}. The result is **universal**: any
(2, +1)_Y scalar with VEV in the lower component triggers the same
Q = T_3 + Y/2 unbroken combination, independent of which framework
primitive plays the Higgs role.

This PR closes the verdict-identified obstruction on
`HIGGS_MECHANISM_NOTE.md` (audit-clean non-circular mechanism theorem)
in CONDITIONAL form. The unconditional version (deriving the Higgs
candidate from framework primitives) is documented as a **named
obstruction** for future work.

**Status:** audit pending. Audit-lane ratification is required before
any retained-grade status applies. Under the scope-aware
classification framework, `effective_status` is computed by the audit
pipeline; no author-side tier is asserted in source.

**Runner:** [`scripts/frontier_conditional_ewsb_q_formula_derivation.py`](./../scripts/frontier_conditional_ewsb_q_formula_derivation.py)

**Authority role:** closing derivation for the parent's class-B
load-bearing step (audit-clean non-circular mechanism theorem) +
explicit named-obstruction documentation for the unconditional
Higgs identification.

## Verdict-identified obstruction (quoted)

From `higgs_mechanism_note`'s `verdict_rationale`:

> Issue: the load-bearing authority rule points from
> HIGGS_MECHANISM_NOTE.md to HIGGS_MASS_DERIVED_NOTE.md, while the
> cited authority is itself audited-conditional and depends back on
> higgs_mechanism_note. ... Repair target: split the mechanism-only
> CW/naturalness runner from the exact-mass checks, and provide an
> audit-clean non-circular mechanism theorem or authority note for
> the scalar order-parameter/Higgs identification.

This PR provides the audit-clean non-circular mechanism theorem in
**conditional form** (Theorem T1) and documents the unconditional
Higgs identification as the **named obstruction** (§ Named Obstruction
below).

## Statement

Let:

- (P1, sister-derivations cycles 01+02+04+06) The framework's derived
  SM one-generation matter representation:

  ```text
  Q_L : (2, 3)_{+1/3}
  L_L : (2, 1)_{-1}
  u_R : (1, 3)_{+4/3}
  d_R : (1, 3)_{-2/3}
  e_R : (1, 1)_{-2}
  ```

  ([`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md)
  cycle 06 [PR #405](https://github.com/jonathonreilly/cl3-lattice-framework/pull/405)).
  Optionally extends to include `ν_R : (1, 1)_0`.

- (P2, retained) `NATIVE_GAUGE_CLOSURE_NOTE.md` — gauge structure
  SU(3)_c × SU(2)_L × U(1)_Y on the framework's chiral surface.

- (P3, admitted) A scalar field Φ in the (2, +1)_Y representation of
  SU(2)_L × U(1)_Y, with non-zero VEV ⟨Φ⟩ = (0, v/√2)^T (lower
  component), triggers EWSB from SU(2)_L × U(1)_Y to a residual
  U(1)_em. **The identification of Φ with a specific framework
  primitive is the named obstruction below; T1 is conditional on this
  admission.**

- (P4, admitted-context external) Standard SM EWSB algebra: SU(2)
  generators T_a in the fundamental rep, U(1)_Y generator Y acting as
  a number, doubled-Y convention `Q = T_3 + Y/2`. Peskin-Schroeder
  1995 ch. 20, or any standard QFT text.

**Conclusion (T1) (conditional EWSB direction).** Under P1+P2+P3+P4,
the unbroken U(1) generator of the residual symmetry SU(2)_L × U(1)_Y
→ U(1)_em is uniquely

```text
Q = T_3 + Y/2.
```

The other linearly independent generators of SU(2)_L × U(1)_Y (i.e.,
T_1, T_2, and T_3 - Y/2) all have non-zero action on ⟨Φ⟩ and are
broken.

**Conclusion (T2) (Q-spectrum on derived rep).** Applying T1 to the
framework's derived SM matter representation (P1):

```text
Q(Q_L^upper, Q_L^lower) = (+2/3, -1/3)
Q(L_L^upper, L_L^lower) = (0, -1)
Q(u_R) = +2/3
Q(d_R) = -1/3
Q(e_R) = -1
[Q(ν_R) = 0   if included]
```

Q-spectrum: **{0, ±1/3, ±2/3, ±1}**, denominators in {1, 3} (matches
SM electric-charge spectrum exactly).

**Conclusion (T3) (universality).** T1's Q = T_3 + Y/2 result depends
ONLY on Φ's quantum numbers (2, +1)_Y and the lower-component VEV
choice. It is **independent** of which framework primitive (Z3 scalar,
Wilson scalar, EW current Fierz channel, or other) plays the Higgs
role, IF any such primitive is identified.

## Proof

### Step 1: SU(2)_L generators on (2, +1)_Y doublet

The SU(2)_L generators in the fundamental rep are T_a = σ_a / 2 with
σ_a Pauli matrices:

```text
T_1 = (1/2) ((0, 1), (1, 0))
T_2 = (1/2) ((0, -i), (i, 0))
T_3 = (1/2) ((1, 0), (0, -1))
```

The (2, +1)_Y doublet Φ has T_3-eigenvalues ±1/2 (upper, lower) and
Y-eigenvalue +1.

### Step 2: VEV ⟨Φ⟩ in the lower component

```text
⟨Φ⟩ = (0, v/√2)^T,   v ≠ 0.
```

### Step 3: Action of generators on ⟨Φ⟩

Compute T_a · ⟨Φ⟩ for each generator:

```text
T_1 · ⟨Φ⟩ = (1/2) (v/√2, 0)^T   ≠ 0   (broken)
T_2 · ⟨Φ⟩ = (-i/2) (v/√2, 0)^T  ≠ 0   (broken)
T_3 · ⟨Φ⟩ = (1/2) (0, -v/√2)^T = (0, -v/(2√2))^T  ≠ 0
Y · ⟨Φ⟩  = +1 · (0, v/√2)^T = (0, v/√2)^T          ≠ 0
```

T_1 and T_2 are clearly broken (they don't fix ⟨Φ⟩ — they rotate it).
T_3 and Y individually don't annihilate ⟨Φ⟩ either.

### Step 4: Linear combinations T_3 + a · Y/2

Try `(T_3 + a · Y/2) · ⟨Φ⟩`:

```text
(T_3 + a · Y/2) · ⟨Φ⟩ = (0, -v/(2√2)) + a · (0, v/(2√2))
                       = (0, (a - 1) · v/(2√2)).
```

This vanishes iff `a = 1`, giving Q = T_3 + Y/2.

### Step 5: Uniqueness

For other coefficients `a ≠ 1`, the combination is broken. Hence the
unbroken generator is **uniquely** (up to overall normalization)

```text
Q = T_3 + Y/2.
```

### Step 6: Q-spectrum on derived SM matter

For each species in the derived rep (P1):

- **Q_L** (Y = +1/3, T_3 = ±1/2):
  - upper: Q = +1/2 + (1/3)/2 = +1/2 + 1/6 = +2/3 (up quark)
  - lower: Q = -1/2 + 1/6 = -1/3 (down quark)
- **L_L** (Y = -1, T_3 = ±1/2):
  - upper: Q = +1/2 + (-1)/2 = +1/2 - 1/2 = 0 (neutrino)
  - lower: Q = -1/2 - 1/2 = -1 (electron)
- **u_R** (Y = +4/3, T_3 = 0): Q = 0 + (4/3)/2 = +2/3
- **d_R** (Y = -2/3, T_3 = 0): Q = 0 + (-2/3)/2 = -1/3
- **e_R** (Y = -2, T_3 = 0): Q = 0 + (-2)/2 = -1
- (optional) **ν_R** (Y = 0, T_3 = 0): Q = 0 + 0 = 0

Q-spectrum: **{0, ±1/3, ±2/3, ±1}**, denominators in {1, 3} ✓.

### Step 7: Universality

The derivation (Steps 1-5) uses ONLY:
- SU(2) generators in the fundamental rep (universal),
- Φ's hypercharge value Y(Φ) = +1 (universal definition of (2, +1)_Y),
- VEV in the lower (T_3 = -1/2) component (universal choice).

It does NOT use any specific framework primitive's properties.
**Therefore T1's Q = T_3 + Y/2 result is universal across any
framework Higgs identification.** ∎

## Named obstruction (unconditional version)

The unconditional version of T1+T2 — i.e., deriving Q = T_3 + Y/2
from framework primitives ALONE without admitting a (2, +1)_Y Higgs
candidate — requires identifying a specific framework primitive as
the Higgs.

The framework's existing scalar primitives:

- **Z3 scalar potential** (`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19`):
  provides scalar dynamics on the Koide selected slice, but is not
  naturally in the (2, +1)_Y representation of SU(2)_L × U(1)_Y.
- **Wilson scalar / staggered scalar** (cycle 05 parity coupling):
  carries gravity coupling but no SU(2)_L × U(1)_Y quantum numbers.
- **EW current Fierz channel** ([PR #249](https://github.com/jonathonreilly/cl3-lattice-framework/pull/249) `EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01`):
  4-fermion structure (q-qbar adjoint channel), not a scalar field.

**None of these currently has a retained identification as a (2, +1)_Y
SU(2) doublet scalar.** This is the **named obstruction** for the
unconditional version.

### Specific future targets

To close the named obstruction, future work would need to either:

(a) Identify a framework primitive (perhaps a composite of existing
    primitives) with the quantum numbers (2, +1)_Y and demonstrate
    it acquires a non-zero VEV in the lower component;
(b) Provide a non-Higgs EWSB mechanism (e.g., dynamical condensation
    of fermion bilinears) that breaks SU(2)_L × U(1)_Y → U(1)_em
    and verify the unbroken combination matches Q = T_3 + Y/2;
(c) Demonstrate that the framework's EW symmetry is unbroken at the
    scales considered, and the SM-like behavior emerges only via a
    different mechanism.

## What this claims

- `(T1)` Conditional EWSB direction: GIVEN a (2, +1)_Y Higgs candidate
  with VEV ⟨Φ⟩ = (0, v/√2)^T, the unbroken U(1) generator is uniquely
  Q = T_3 + Y/2.
- `(T2)` Q-spectrum on the framework's DERIVED SM matter rep
  (cycles 01+02+04+06) is exactly {0, ±1/3, ±2/3, ±1}, matching
  observed SM charges.
- `(T3)` Universality: T1 depends only on (2, +1)_Y quantum numbers,
  not on any specific Higgs identity.

## What this does NOT claim

- Does NOT identify a specific framework primitive as the
  (2, +1)_Y Higgs. That IS the named obstruction.
- Does NOT address Higgs mass — separate question downstream of
  identification.
- Does NOT prove the scalar potential mechanism (CW, dynamical
  condensation, etc.) generates the VEV. P3 admits a non-zero VEV;
  the mechanism is not derived.
- Does NOT close the unconditional version of T1 — that requires
  closing the named obstruction.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1) [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md) (cycle 06, [PR #405](https://github.com/jonathonreilly/cl3-lattice-framework/pull/405))
  — synthesizes cycles 01+02+04 derivation of SM rep.
- (P2) [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained gauge structure.
- (P3) Admitted (2, +1)_Y Higgs candidate with non-zero VEV in lower
  component. **NOT identified with any framework primitive.**
- (P4) Peskin-Schroeder 1995 ch. 20 — admitted-context external SM
  EWSB algebra.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Peskin-Schroeder is
  admitted-context external machinery, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y convention.
- No same-surface family arguments.
- No load-bearing dependency on the demoted
  `HYPERCHARGE_IDENTIFICATION_NOTE` (cycle 04's decoupling carries
  through).

## Validation

Primary runner: [`scripts/frontier_conditional_ewsb_q_formula_derivation.py`](./../scripts/frontier_conditional_ewsb_q_formula_derivation.py)
verifies (PASS=34/0, exact rational + numerical SU(2) generator algebra):

1. SU(2) generators T_a in fundamental rep (Pauli σ_a / 2).
2. Action of T_1, T_2, T_3 on ⟨Φ⟩ = (0, v/√2)^T: all non-zero
   (broken).
3. Action of Y on ⟨Φ⟩: Y · ⟨Φ⟩ = ⟨Φ⟩ (Y(Φ) = +1).
4. Q = T_3 + Y/2 annihilates ⟨Φ⟩: (T_3 + Y/2) · ⟨Φ⟩ = 0.
5. Counterfactual: Q' = T_3 - Y/2 does NOT annihilate ⟨Φ⟩.
6. Counterfactual: Q'' = T_3 + 0.5 · Y/2 (a ≠ 1) does NOT annihilate
   ⟨Φ⟩.
7. Q-spectrum on derived rep matches SM exactly:
   - Q_L: {+2/3, -1/3}
   - L_L: {0, -1}
   - u_R: +2/3, d_R: -1/3, e_R: -1
   - (with ν_R: 0)
8. Q-spectrum denominators ⊆ {1, 3}.
9. Universality check: Q-formula is independent of v's value (any
   v ≠ 0 gives the same unbroken combination).

## Cross-references

- [`HIGGS_MECHANISM_NOTE.md`](HIGGS_MECHANISM_NOTE.md) — parent row
  whose verdict-identified obstruction is closed (in conditional
  form) by this derivation.
- [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md) —
  cycle 06 sister: provides the derived SM rep that this cycle uses.
- [`SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`](SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md) —
  cycle 04 sister: provides Y values used in the Q-spectrum check.
- [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md) —
  candidate framework scalar primitive (not (2, +1)_Y).
- [`STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md`](STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md) —
  cycle 05 sister: candidate framework scalar (not (2, +1)_Y).
- [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md) —
  candidate framework structure (4-fermion, not scalar).
- Peskin-Schroeder 1995 ch. 20 — admitted-context external SM EWSB
  algebra.
