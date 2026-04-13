# I_3 = 0 Exact Theorem (No Third-Order Interference)

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_born_rule_derived.py` (historical filename)

**Note:** This file was previously named `BORN_RULE_DERIVED_NOTE.md`. Per
Codex finding 21, the retained exact result is I_3 = 0 given linear
amplitudes and P = |A|^2. The note does NOT derive P = |A|^2 (the Born rule)
from I1 alone. The title has been corrected accordingly.

---

## Status

**Exact theorem.** I_3 = 0 (no third-order interference) is an algebraic
identity that follows from linear amplitude composition and P = |A|^2.
No lattice-specific details enter. This does NOT derive the Born rule itself;
it assumes P = |A|^2 and proves the Sorkin parameter vanishes.

---

## Theorem / Claim

**Theorem.** Let H be a finite-dimensional Hilbert space with unitary
propagator U = exp(-iHt). Let A_X denote the amplitude for a particle
to pass through slit X, satisfying linearity:
A_{S1 union S2} = A_{S1} + A_{S2} for disjoint slit sets. Let
P_S = |A_S|^2 (Born rule). Then the Sorkin parameter

  I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C - P_empty

vanishes identically for any amplitudes A, B, C. More generally,
I_n = 0 for all n >= 3.

---

## Assumptions

1. **Axiom I1:** Finite-dimensional Hilbert space with local tensor
   product structure. This gives:
   - Complex amplitudes
   - Unitary evolution (from Hermitian Hamiltonian)
   - Born rule P = |A|^2 (unique p-norm preserved by all unitaries)
   - Linear amplitude composition

No additional axioms (I2, I3, I4, ...) are used. The result is
independent of:
- The lattice dimension d
- The lattice topology (cubic, FCC, etc.)
- The staggered phase structure
- The Cl(3) algebra
- The specific form of the Hamiltonian H
- The system size L

---

## What Is Actually Proved

**Algebraic identity.** For any complex numbers A, B, C:

  |A+B+C|^2 - |A+B|^2 - |A+C|^2 - |B+C|^2 + |A|^2 + |B|^2 + |C|^2 = 0

**Proof.** Expand |X+Y|^2 = |X|^2 + |Y|^2 + 2 Re(X conj(Y)).
The |A+B+C|^2 expansion contains:
- Three squared terms: |A|^2, |B|^2, |C|^2
- Three cross-terms: 2Re(A conj(B)), 2Re(A conj(C)), 2Re(B conj(C))

Each squared term |X|^2 appears with coefficient 1 - 1 - 1 + 1 = 0
(once in P_ABC, subtracted in two pair terms, added back in P_X).

Each cross-term 2Re(X conj(Y)) appears with coefficient 1 - 1 = 0
(once in P_ABC, subtracted once in P_XY).

All coefficients vanish. I_3 = 0 identically. QED.

**Generalization to I_n.** For n slits, |sum A_i|^2 expands into
degree-1 terms (|A_i|^2) and degree-2 terms (cross products).
The inclusion-exclusion sum assigns each term a coefficient that
sums to zero by the binomial identity. Since |sum A_i|^2 never
produces terms of degree >= 3 in the amplitudes, I_n = 0 for
all n >= 3.

**Converse.** If probabilities were P = |A|^p with p != 2, then
|X+Y|^p generates terms of order > 2 in the real and imaginary
parts of the amplitudes. These higher-order terms do not cancel
under inclusion-exclusion, giving I_3 != 0 generically. The Born
rule (p = 2) is the unique probability rule compatible with
I_3 = 0 and linear amplitude composition.

---

## What Remains Open

Nothing remains open for this specific result. I_3 = 0 is a closed
algebraic identity.

The deeper question -- WHY does the framework use P = |A|^2 -- is not
addressed here. That is the foundational ontological commitment (axiom I1
gives a Hilbert space; the unique unitary-invariant probability measure is
|A|^2). This note shows that once P = |A|^2 and linear amplitudes are
accepted, zero third-order interference is an automatic consequence.

---

## How This Changes The Paper

This result belongs in the framework foundations section. It establishes:

1. Given linear amplitude composition and P = |A|^2, the Sorkin parameter
   I_3 vanishes identically. All multi-path interference is pairwise.
2. The converse also holds: P = |A|^2 is the unique probability rule
   compatible with I_3 = 0 and linear amplitudes.
3. This does NOT derive P = |A|^2 from I1 alone. The Born rule is an
   assumption (via the Hilbert space axiom), not a derived consequence.

**Paper-safe wording:**

> Given the Hilbert-space axiom (I1) and the resulting Born rule P = |A|^2,
> the Sorkin parameter I_3 vanishes identically for any complex amplitudes
> satisfying linear composition. All multi-path interference is pairwise.
> This is an algebraic identity independent of the lattice structure.

---

## Commands Run

```bash
python scripts/frontier_born_rule_derived.py
```

Expected output: `COMPUTED_PASS=6 ASSERTION=2 FAIL=0`
