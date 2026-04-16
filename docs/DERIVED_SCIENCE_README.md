# Derived Science — Session Contribution

**Branch:** `claude/main-derived`
**Date:** 2026-04-16

This branch contains **only the work produced in this session** that passes
a hostile-reviewer bar: pure-math theorems or clean negative results with
no imports, no structural identifications, no crutches.

Existing framework results (CMT, V_sel EWSB, anomaly-forced 3+1, etc.) are
already on `origin/main` with their own authority notes and runners and are
NOT duplicated here.

## Airtight positives (produced this session)

| # | Claim | Authority | Runner | Status |
|---|---|---|---|---|
| 1 | K_R tensor carrier vanishes on A1 backgrounds via Schur S₃ orthogonality | `KR_A1_VANISHING_DERIVED_NOTE.md` | `frontier_KR_A1_vanishing_proof.py` | 30/30 PASS |
| 2 | Rank-1 + rank-(n-1) projector algebra: weights 1/n and (n-1)/n | `PROJECTOR_ALGEBRA_DERIVED_NOTE.md` | `frontier_projector_algebra.py` | 25/25 PASS with scope caveat |

## Clean negative results (produced this session)

| # | Claim | Authority | Method |
|---|---|---|---|
| N1 | V_sel-fermion coupling does NOT produce SM three-generation mass structure | `NEGATIVE_VSEL_WRONG_MASS_STRUCTURE.md` | closed-form eigenvalue derivation |
| N2 | y_t = g_s/√6 not derivable from gauge/chiral Ward identities, CG, or gauge-Yukawa universality | `NEGATIVE_YT_SQRT_6_NOT_DERIVED.md` | four attempted algebraic derivations, all fail |

## Out of scope (not included in this branch)

- Existing framework content already on main (CMT, V_sel EWSB selector,
  anomaly-forced 3+1, native SU(2), graph-first SU(3), three-generation
  observable algebra, CPT, I_3=0, discrete 3+1 GR, UV-finite QG chain, etc.)
- Anything related to the plaquette ⟨P⟩ derivation on main
  (that work is not mine and is currently under separate review)
- CKM numerical predictions (conjectures, not rigorous derivations)
- Yukawa / fermion mass hierarchy predictions
- All structural-identification claims explored during session

## Reviewer verification

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py     # expect PASS=30
python3 scripts/frontier_projector_algebra.py         # expect PASS=25
```

Both scripts terminate with nonzero exit on any failure.

## What this branch establishes

**Positively:**
- Two small but genuinely rigorous theorems: K_R vanishes on A1 (Schur
  orthogonality), and the projector-weight formula for a rank-1+rank-(n-1)
  decomposition (weights 1/n and (n-1)/n).
- Neither is load-bearing for the flagship CKM/mass claims; both are
  clean pure-math building blocks.

**Negatively:**
- The natural V_sel-fermion coupling, analyzed algebraically, gives the
  wrong fermion mass structure (eigenvalues {2α, α, 0} instead of three
  hierarchical masses).
- The "y_t = g_s/√6" Ward identity cited as foundational is not derivable
  from any of the four standard routes (gauge Ward, chiral Ward, Clebsch-
  Gordan on Q_L, gauge-Yukawa universality). Either a non-standard
  mechanism exists or the identity should be labeled as a postulate.

Together these narrow the framework's airtight domain: the gauge/EWSB/
anomaly sector on main remains airtight, but the Yukawa/CKM/fermion-mass
sector needs further research before it can make rigorous claims.

## Scope caveats (important)

- Positive #2 (projector algebra) proves ONLY the weight formula; the
  downstream identification with the Unitarity Triangle CP phase
  cos²(δ) = 1/6 is a separate structural claim and is NOT proved here.
- Negative N2 establishes only that STANDARD Ward-identity routes fail.
  It does not rule out non-standard mechanisms.

## What's NOT claimed

- No claim to derive CKM, fermion masses, Higgs mass, top mass, or any
  quantitative PDG match from first principles.
- No claim about the plaquette ⟨P⟩ value — that work is not mine.
- No claim that the two positive theorems (K_R-A1 vanishing, projector
  algebra) are load-bearing for a full ToE derivation.
