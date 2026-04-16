# Nature-Grade Index — Session Contribution

**Branch:** `claude/main-derived`
**Date:** 2026-04-16 (post-3x-check)
**Bar:** strictly unbounded

## Single surviving claim

### P1. K_R Tensor Carrier Vanishes on A1 Backgrounds

**Theorem:** On the seven-site star support carrying an S_3 representation
that decomposes as 2·A1 + E + T1, the tensor carrier
```
K_R(q) = (u_E(q), u_T(q), δ_A1(q)·u_E(q), δ_A1(q)·u_T(q))
```
with u_E(q) = ⟨E_x, q⟩ and u_T(q) = ⟨T1_x, q⟩ satisfies
```
K_R(q) = 0 for all q ∈ A1 subspace.
```

**Proof:** Schur orthogonality. Distinct S_3 irreps are orthogonal as
submodules. E_x ∈ E irrep and T1_x ∈ T1 irrep, both disjoint from A1.
Therefore u_E(q) = u_T(q) = 0 for any q ∈ A1, which makes all four
components of K_R zero.

**Status:** unbounded pure-math theorem.

**Note:** `KR_A1_VANISHING_DERIVED_NOTE.md`
**Runner:** `frontier_KR_A1_vanishing_proof.py` — 30/30 PASS

## Claims removed during triple-check

### P2 (projector algebra) — REMOVED (trivial)

Rank-1 + rank-(n-1) projector weights = 1/n and (n-1)/n. Pure textbook
linear algebra. Removed because the theorem in isolation provides no
physics content; its value depended on a downstream identification
(with UT CP phase cos²(δ) = 1/6) that was explicitly disclaimed.

### N1 (V_sel-fermion mass matrix) — REMOVED (derivation gap)

Claimed eigenvalue structure {2α, α, 0} for the hw=1 sector from one-
loop δφ self-energy. Error: with diagonal δφ propagators
Π_{ij} = δ_{ij}/m²_i at the EWSB vacuum, off-diagonal contributions
vanish (since S_i² = I gives only diagonal delta_{ab} contributions).
The eigenvalue claim is not rigorously derived from the stated
mechanism.

### N2 (y_t = g_s/√6 not derivable) — REMOVED (scope-bounded)

Claimed no derivation via four standard Ward-identity / CG /
universality methods. Removed because the scope "within four standard
methods" is itself a bridge — a reviewer can always posit a fifth
non-standard approach that might yield √6.

## What this branch is, honestly

One small unbounded lemma. Not a flagship submission.

## What this branch is NOT

- Not a CKM derivation
- Not a Yukawa / mass derivation
- Not a replacement for existing main content
- Not sufficient for Nature-grade submission on its own merit

## Existing main content (not duplicated here)

- CMT partition identity
- V_sel EWSB selector derivation (63/63 PASS on main)
- Anomaly-forced 3+1
- Native SU(2), graph-first SU(3)
- Three-generation observable algebra
- Discrete 3+1 GR + UV-finite QG chain
- CPT, I_3=0, emergent Lorentz
- Recent plaquette work (separate review track)

These stand on their own and are not affected by this branch.

## Reviewer verification

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py  # PASS=30 FAIL=0
```
