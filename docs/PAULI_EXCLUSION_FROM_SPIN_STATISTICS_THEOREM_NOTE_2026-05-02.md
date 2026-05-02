# Pauli Exclusion Principle from Retained Spin-Statistics Theorem

**Date:** 2026-05-02
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Claim scope:** for any single-particle fermionic mode |φ⟩ on the framework's retained matter content, the two-fermion Fock state with both particles in mode |φ⟩ is identically the zero vector; equivalently, the squared creation operator (a^†_φ)² = 0 and there is no normalizable physical state with multiplicity > 1 in any single fermionic mode (Pauli exclusion principle).
**Status:** awaiting independent audit. Under scope-aware classification (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `positive-only-retained-20260502`
**Cycle:** 2 (Block 2)
**Branch:** `physics-loop/positive-only-block02-pauli-exclusion-20260502`
**Runner:** `scripts/pauli_exclusion_check.py`
**Log:** `outputs/pauli_exclusion_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md) — declared audit dependency; its live effective status is pipeline-derived and may be audit-pending after dependency-graph strengthening. Provides: any half-integer-spin Cl(3) representation field anticommutes with itself and with a like field at a distinct site. Equivalently, the canonical staggered-Dirac fermion creation operator algebra is

  ```text
      {a_φ, a_ψ}      = 0
      {a^†_φ, a^†_ψ}  = 0
      {a_φ, a^†_ψ}    = ⟨φ|ψ⟩
  ```

  for any pair of single-particle modes φ, ψ on the retained matter content.

This is the **only** load-bearing one-hop dependency.

## Admitted-context inputs

- **Vacuum state |0⟩.** Standard QFT vacuum on H_phys, defined as the
  unique state annihilated by every annihilation operator: a_φ |0⟩ = 0
  for all φ. This is a basic structural definition, not a physics
  admission.
- **Linear algebra on H_phys.** Standard finite-dimensional inner-product
  space identities.

No physics conventions beyond what the retained spin-statistics theorem
already provides.

## Statement

Let `a^†_φ` be the creation operator for the single-particle fermionic
mode `|φ⟩` on the framework's matter content covered by the declared
spin-statistics dependency. Then, conditional on that dependency:

**(P1) Squared creation operator vanishes.** From the retained
fermion anticommutator `{a^†_φ, a^†_φ} = 2 (a^†_φ)² = 0`, we have

```text
    (a^†_φ)²  =  0                                                            (1)
```

as an operator identity on H_phys.

**(P2) Two-fermion same-mode state is the zero vector.** For any
single-particle mode `|φ⟩`, the candidate two-fermion state

```text
    |φ, φ⟩  :=  a^†_φ a^†_φ |0⟩  =  (a^†_φ)² |0⟩                              (2)
```

is, by (P1), the **zero vector** in H_phys. It is therefore not a
normalizable physical state.

**(P3) Pauli exclusion principle.** No two identical fermions on the
framework's retained matter content can simultaneously occupy the same
single-particle mode. Equivalently, the occupation number `n_φ := a^†_φ a_φ`
of any fermionic mode satisfies `n_φ ∈ {0, 1}`.

(P1)–(P3) constitute the Pauli exclusion principle on the framework's
retained matter surface.

## Proof

The proof is a two-line application of the retained spin-statistics
theorem:

### Step 1 — Squared creation operator (proves P1)

The retained spin-statistics theorem
([`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md))
gives, for any half-integer-spin Cl(3) field on the canonical retained
matter content, the anticommutation relation

```text
    {a^†_φ, a^†_ψ}  =  a^†_φ a^†_ψ + a^†_ψ a^†_φ  =  0                        (3)
```

for arbitrary modes `φ, ψ`. Specialise (3) to the case `φ = ψ`:

```text
    {a^†_φ, a^†_φ}  =  2 (a^†_φ)²  =  0  ⇒  (a^†_φ)²  =  0                    (4)
```

This is (P1). ∎

### Step 2 — Same-mode two-fermion state (proves P2)

Apply (P1) to the vacuum state `|0⟩`:

```text
    a^†_φ a^†_φ |0⟩  =  (a^†_φ)² |0⟩  =  0 · |0⟩  =  0                       (5)
```

The candidate two-fermion same-mode state is the zero vector. ∎

### Step 3 — Occupation number n_φ ∈ {0, 1} (proves P3)

Define the occupation operator `n_φ := a^†_φ a_φ`. From the retained
anticommutator `{a_φ, a^†_φ} = 1` (mode-orthonormal basis):

```text
    n_φ²  =  a^†_φ a_φ a^†_φ a_φ
          =  a^†_φ ({a_φ, a^†_φ} - a^†_φ a_φ) a_φ
          =  a^†_φ a_φ - (a^†_φ)² (a_φ)²
          =  a^†_φ a_φ - 0                                                   (6)
          =  n_φ
```

using `(a^†_φ)² = 0` from (P1). So `n_φ²  =  n_φ`, i.e. `n_φ` is a
projection operator. Its eigenvalues are therefore in `{0, 1}`. ∎

This completes the proof of (P1)–(P3) on the retained surface.

## Hypothesis set used

- `axiom_first_spin_statistics_theorem_note_2026-04-29` (declared audit
  dependency; live status is pipeline-derived):
  provides Grassmann anticommutation `{a^†_φ, a^†_ψ} = 0` for fermionic
  fields on the retained matter content.
- Standard QFT vacuum definition `a_φ |0⟩ = 0` (admitted-context,
  structural).
- Standard finite-dim inner-product space identities (admitted-context,
  basic linear algebra).

No fitted parameters. No observed values. No physics conventions
admitted beyond what the retained spin-statistics theorem already
provides.

## Corollaries

C1. **Anti-symmetric multi-fermion states.** For `N` identical
fermions in distinct modes `|φ_1⟩, …, |φ_N⟩`, the joint state

```text
    |φ_1, …, φ_N⟩  =  a^†_{φ_1} … a^†_{φ_N} |0⟩
```

is automatically antisymmetric under any permutation of the modes
(since the creation operators anticommute). This is the Slater-
determinant structure of multi-fermion wavefunctions.

C2. **Atomic shell structure (qualitative).** The Pauli principle on
the framework's retained matter content forces the qualitative
shell-filling pattern of multi-electron atoms: each spatial orbital
holds at most 2 electrons (one each spin), so closed shells form at
2, 10, 18, 36, … electrons. The quantitative spectrum is a separate
calculation outside this note.

C3. **Stability of bulk matter.** The Lieb-Dyson stability of bulk
matter (Lieb-Dyson 1968, Lieb-Thirring 1975) requires Pauli exclusion
as load-bearing input. This corollary is recorded for future work; the
bulk-stability theorem itself depends on additional retained matter
structure (Coulomb potential bounds, etc.) that is not yet at retained-
grade on the live ledger.

C4. **Classical-statistics impossibility for fermionic matter.**
Fermions cannot be described by Maxwell-Boltzmann statistics. They
follow Fermi-Dirac statistics with occupation `⟨n_φ⟩ = 1/(e^{β(E_φ - μ)} + 1) ≤ 1`,
which is bounded above by 1 — direct corollary of (P3) and standard
ensemble averaging.

## Honest status

**Positive theorem candidate on the declared spin-statistics surface.** Steps
1–3 close from the spin-statistics dependency alone, plus the basic vacuum
definition. No physics admission. The chain is single-hop; retained-family
status is not asserted by this source note.

The runner verifies (P1)–(P3) by:

- explicitly constructing the fermionic creation/annihilation operator
  algebra on a small toy fock space (2 modes, Hilbert dim = 4) and
  numerically confirming `{a^†_φ, a^†_φ} = 0`, `(a^†_φ)² = 0`,
  `n_φ² = n_φ`;
- attempting to construct `(a^†_φ)² |0⟩` and confirming it is the zero
  vector;
- enumerating the full 4-dim Hilbert basis and confirming no state has
  any single-mode occupation > 1.

**Honest classification fields:**

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "(a^†_φ)² = 0 on H_phys for any fermionic mode |φ⟩; equivalently the two-fermion same-mode state is the zero vector; occupation number n_φ ∈ {0, 1}."
admitted_context_inputs:
  - QFT vacuum definition a_φ |0⟩ = 0
  - basic finite-dim linear algebra
upstream_dependencies:
  - axiom_first_spin_statistics_theorem_note_2026-04-29
audit_required_before_effective_retained: true
```

These are author-side hints only. The independent audit lane sets the audit
verdict, and the pipeline computes any retained-family effective status after
that verdict and dependency closure.

## Citations

- retained input: `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
- standard external references (theorem-grade, no numerical input):
  Pauli (1925) *Z. Phys.* 31, 765 (original Pauli principle);
  Pauli (1940) *Phys. Rev.* 58, 716 (spin-statistics);
  Streater-Wightman (1964) *PCT, Spin and Statistics, and All That*,
  ch. 4.
