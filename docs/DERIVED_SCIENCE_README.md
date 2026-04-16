# Derived Science — Session Contribution (Post-3x-Check)

**Branch:** `claude/main-derived`
**Date:** 2026-04-16
**Bar:** strictly unbounded — no bridges, no scope qualifiers, no downstream
structural identifications required for the claim to hold.

After triple-checking, only one result from my session work survives the
strict unbounded bar.

## Single airtight claim

### P1. K_R vanishes on A1 backgrounds (Schur orthogonality)

- Statement: the tensor carrier K_R(q) = (u_E(q), u_T(q), δ_A1(q)·u_E(q),
  δ_A1(q)·u_T(q)) with u_E = ⟨E_x, q⟩ and u_T = ⟨T1_x, q⟩ vanishes
  identically on the A1 subspace of the seven-site star.
- Proof: distinct S_3 irreps are orthogonal (Schur's theorem). E_x ∈ E
  irrep, T1_x ∈ T1 irrep, q ∈ A1 irrep. Therefore u_E = u_T = 0, so K_R = 0.
- Status: unbounded pure-math theorem.
- Note: `KR_A1_VANISHING_DERIVED_NOTE.md`
- Runner: `frontier_KR_A1_vanishing_proof.py` — 30/30 PASS

## What was removed after triple-check

### P2 (projector algebra) — REMOVED

Pure linear algebra (weights 1/n and (n-1)/n for rank-1 + rank-(n-1)
decomposition). The theorem is trivially true but provides no content
without the downstream identification with the UT CP phase cos²(δ) = 1/6,
which was explicitly disclaimed. Removed because the theorem in isolation
is too trivial to be a submission.

### N1 (V_sel-fermion wrong mass structure) — REMOVED

My derivation claimed off-diagonal mass matrix elements from
⟨X_a|S_i S_j|X_b⟩ matrix elements via one-loop δφ exchange. But with
diagonal δφ propagators Π_{ij} = δ_{ij}/m²_i (correct for mass
eigenstates at the EWSB vacuum), the formula reduces to diagonal only:
M_eff(a,b) = y² Σ_i ⟨X_a|S_i²|X_b⟩/m²_i = y² Σ_i δ_{ab}/m²_i. The off-
diagonal structure I claimed doesn't arise from this diagram. Removed
for logical gap.

### N2 (y_t = g_s/√6 not derivable) — REMOVED

The claim "four standard derivation methods fail" is scoped to four
specific methods; a reviewer can always posit a non-standard approach.
Removed because the scope constitutes a bridge (a non-standard mechanism
could exist that I haven't examined).

## Honest assessment

This branch now contains ONE small unbounded pure-math theorem (P1).

P1 is:
- Genuinely rigorous (textbook Schur orthogonality applied to a specific
  S_3 representation).
- Small in scope — a single lemma about a specific tensor structure.
- Not load-bearing for any flagship physics claim in isolation.
- Would be a building block in a larger CKM derivation, but the
  downstream application is NOT claimed here.

This branch is NOT a flagship-level submission. It is a single clean
lemma that survives the strictest "unbounded only" filter after
triple-checking my session work.

## What remains on main (existing, not duplicated here)

The existing framework on origin/main contains substantial airtight
content not produced by me this session:
- CMT (Coupling Map Theorem) partition identity
- V_sel EWSB selector (63/63 PASS on main)
- Anomaly-forced 3+1 theorem
- Native SU(2), graph-first SU(3)
- Three-generation observable algebra
- Discrete 3+1 Einstein-Regge GR + UV-finite QG chain
- CPT, I_3=0, emergent Lorentz
- Recent plaquette work (under separate review)

My session contribution (P1) is one small addition to that existing body.

## Reviewer verification

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py
# Expected: TOTAL: PASS=30, FAIL=0
```

## Submission readiness (honest)

**Not ready for flagship submission.** P1 alone is too small.

The work done this session is better characterized as:
1. P1: one small clean lemma produced.
2. Audit findings: several framework claims previously labeled as
   "derived" on main rely on structural identifications rather than
   rigorous derivations. These findings are preserved on
   `claude/stoic-almeida` as session work but are not promoted here
   because they don't meet the strict unbounded bar.

If a flagship submission is desired, it should lean on the framework's
larger existing main-repo results (gauge/EWSB/GR sector), not on my
session contribution.
