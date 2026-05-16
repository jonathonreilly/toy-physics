# No-Go Ledger

**Date:** 2026-05-16
**Loop:** koide-l5-spectral-triple-20260516

Routes already excluded by prior negative evidence. Agents must NOT
re-explore these unless a NEW premise is named.

## NG-1: Cl(3) bivectors via (R − R^T)/i

**Source:** §6.1 of `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10.md`

**Claim:** Cl(3) has three bivectors {γ_2γ_3, γ_3γ_1, γ_1γ_2}. The
antisymmetric "circulator" combination `H = (R − R^T)/i` (which is the
anti-Hermitian commutator part of the Z_3 3-cycle generator R) has:

- Eigenvalues `0` on the singlet direction (1,1,1)
- Eigenvalues `±√3` on the doublet subspace
- Both non-zero eigenvectors are entirely in the doublet
- Therefore (R−R^T)/i **COMMUTES** with Γ_χ (not anti-commutes)

**Status:** EXCLUDED. Cl(3) bivectors alone do not provide the needed H.

**Re-open condition:** a new construction that USES Cl(3) bivectors as
PART of a larger algebra (e.g., Cl(3) ⊗ extra) where the tensored
operator anti-commutes with Γ_χ ⊗ I would be a new premise. Bare Cl(3)
bivectors alone are dead.

## NG-2: Real Hermitian anti-commuting H always has zero eigenvalue

**Source:** §3.3 of the same note

**Claim:** Every Hermitian H of the form `(1/3)(1⊗h + h⊗1)` with Σh = 0,
h ≠ 0, has spectrum {−λ, 0, +λ} — there is ALWAYS a zero eigenvalue.

**Status:** Theorem (not a no-go). The non-zero-eigenvalue eigenvectors
of H satisfy LCC.

**Implication:** any framework realization must produce an H whose
non-zero-eigenvalue eigenvectors contain v (the lepton mass-square-root
vector). The zero-eigenvalue direction is the singlet (parallel to
(1,1,1) — see §3.2: "H (1,1,1)^T = h, so the all-ones vector is NOT
an eigenvector of H unless h ∝ (1,1,1), which Σh=0 rules out").

Wait — the note says h is NOT an eigenvector but `H · 1 = h`. The
zero-eigenvector and 0-eigenvalue are distinct directions. Let me re-check
on Cycle 1 — this is a subtlety that the agent fan-out should clarify.

## NG-3: Staggered Dirac taste operators on Z³

**Source:** §6.2 of the same note

**Claim:** The staggered Dirac on Z³ acts on the 2³ = 8 taste cube.
Specific generators of taste shifts (mixing the 8 taste states across
generation candidates) "MIGHT produce H of the required form when
restricted to the 3-generation subspace."

**Status:** Research-level open. NOT a no-go, but no concrete
construction exists yet.

**Re-open condition:** any new attempt must produce a specific embedding
of the 3-generation triplet into the 8-taste cube, then check the
restriction.

## Prior no-go context (from memory / project context)

These are general framework no-gos that may interact with the
spectral-triple route:

- **Brannen CH closure** (memory): Gaps 1-3 closed; runner 16/16. The
  Berry=CH equivalence and Ω=1 derivation are retained. This is the
  closest sister-structure to the Koide chain.
- **Bridge gap fragmentation 2026-05-07** (memory): Bridge gap was a
  bundle of hidden admissions. L3a trace-surface, L3b overall scalar,
  C-iso a_τ=a_s, W1.exact engineering frontier remain. Cl(3)/Z³
  spectral-triple route was named as "non-trivial structural
  construction — bigger than a single push."

## What agents should NOT do

- Re-derive that `(R − R^T)/i` commutes with Γ_χ — already known
- Claim Cl(3) bivectors alone give the answer — excluded
- Use PDG lepton masses as load-bearing proof inputs — non-negotiable
- Add new axioms — per no-new-axiom rule
- Produce one-step relabelings of the retained Level 4 theorem — churn

## What agents SHOULD do

- Construct concrete spectral triples (A, H, D, γ, J) with stated
  axioms and check whether D (or its decomposition) realizes H of the
  required form
- Either produce a positive existence proof (with framework derivation
  of h) or a rigorous no-go (proving no such D exists with stated
  Connes axioms on Cl(3)/Z³)
- Use the 5 counterfactual directions from ASSUMPTIONS_AND_IMPORTS.md
  as independent attack frames
