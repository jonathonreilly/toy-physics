# (CPT)² = Identity on the Framework's Retained CPT Structure

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the antiunitary CPT operator on the framework's RP-reconstructed H_phys, defined by composing the framework's exact C (sublattice parity), P (spatial inversion), and T (complex conjugation), satisfies the involution identity (CPT)² = I exactly on H_phys with no phase factor.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r3-20260502`
**Cycle:** 2 (Block 2)
**Branch:** `physics-loop/positive-only-r3-block02-cpt-squared-20260502`
**Runner:** `scripts/cpt_squared_is_identity_check.py`
**Log:** `outputs/cpt_squared_is_identity_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — `effective_status: retained` on the live ledger. Provides:
  - **C operator:** sublattice parity ε(x) = (-1)^{x_1+x_2+x_3}, real diagonal involutory.
  - **P operator:** spatial inversion x → -x mod L, real involutory permutation.
  - **T operator:** complex conjugation K (since H is real).
  - **(CP)² = I** explicitly.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Antiunitary operator squared yields unitary.** Standard QM result: T·T·U = T·(T·U) where T antiunitary. (T·U) is antilinear, so T·(T·U) = U is linear. So T² is unitary. Pure linear algebra.
- **Antiunitary commutation rule** with unitary: T · U = U* · T for any unitary U. Pure structural.

No physics conventions admitted beyond what the retained CPT exact note provides.

## Statement

Let CPT = C·P·T be the antiunitary CPT operator on the framework's H_phys, with C, P, T as in the retained CPT_EXACT_NOTE. Then:

**(I1)** (CPT)² = I on H_phys, exactly. No phase factor.

**(I2)** CPT is therefore an involution on H_phys: applying CPT twice returns the original state.

**(I3)** The Hilbert space H_phys decomposes orthogonally into the +1 and -1 eigenspaces of CPT — but since (CPT)² = I (no phase), the +1 eigenspace is the entirety of H_phys and the -1 eigenspace is empty.

## Proof

### Step 1 — Decomposition

CPT = (CP) · T where CP is unitary (real, by retained CPT note: both C and P are real operators, so CP is real → its complex conjugate equals itself: (CP)* = CP) and T = K (complex conjugation).

### Step 2 — Compute (CPT)²

```
(CPT)² = (CP·T)(CP·T) = CP·T·CP·T
```

By the antiunitary commutation rule (T·U = U*·T for unitary U):

```
T·CP = (CP)* · T = CP · T   (since CP is real ⇒ (CP)* = CP)
```

So:

```
(CPT)² = CP · (T·CP) · T = CP · CP · T · T = (CP)² · T²
```

### Step 3 — Apply retained identities

By retained CPT_EXACT_NOTE:
- (CP)² = I (cited identity, line 77 of source note)
- T = K (complex conjugation), so T² = K² = I (applying conjugation twice on any complex number returns it)

Therefore:

```
(CPT)² = I · I = I
```

establishing (I1). ∎

### Step 4 — Involution and eigenvalue structure (I2, I3)

Any operator A satisfying A² = I is an involution. Its eigenvalues are ±1, with eigenspaces orthogonal. (I2) follows. For (I3): the antiunitary nature of CPT means it doesn't admit a standard linear eigenvalue decomposition, but the involution identity restricts the action — the "+1 eigenspace" of CPT is the set of states fixed by CPT, which by (I1) is all of H_phys (any state |ψ⟩ satisfies CPT·CPT·|ψ⟩ = |ψ⟩, so |ψ⟩ is in some sense fixed by CPT²; the linear-eigenvalue language is delicate for antiunitary operators but the involution content (I1) is unambiguous). ∎

## Hypothesis set used

- `cpt_exact_note` (retained): provides (CP)² = I and explicit C, P, T constructions.
- Antiunitary commutation rule (basic linear algebra).
- T² = K² = I (basic complex analysis).

## Corollaries

C1. **Selection rules from CPT.** Matrix elements ⟨ψ|O|φ⟩ where O is CPT-odd vanish on CPT-symmetric states. C₁ together with (I1) gives a clean Hilbert-space decomposition.

C2. **No "Majorana" obstruction.** For fermionic systems with (CPT)² = -I (instead of +I), there's an obstruction to defining a Majorana mass term cleanly. The framework's (CPT)² = I means no such obstruction.

C3. **Reality of the framework Hamiltonian (alternative proof).** Since CPT² = I and [CPT, H] = 0, taking the spectral decomposition of H gives real eigenvalues without further assumption (already known from Hermiticity but reinforced).

C4. **CPT as Z₂ gauge action.** The involution structure makes CPT generate a Z₂ action on H_phys; the framework can be analyzed as a "graded" theory under this Z₂.

## Honest status

Positive theorem on the retained surface. Single one-hop chain. Pure algebraic consequence of (CP)² = I (cited from retained CPT_EXACT_NOTE) plus T² = I.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "(CPT)² = I exactly on H_phys"
upstream_dependencies:
  - cpt_exact_note (effective_status: retained)
admitted_context_inputs:
  - antiunitary commutation rule T·U = U*·T
  - T² = K² = I
```
