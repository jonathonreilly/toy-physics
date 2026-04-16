# Nature-Grade Index — Session Contribution

**Branch:** `claude/main-derived`
**Date:** 2026-04-16

Only work produced by me this session. Existing framework content on
`origin/main` is not duplicated here.

## Positive airtight derivations

### P1. K_R Tensor Carrier Vanishes on A1 Backgrounds

The tensor carrier K_R defined on the seven-site star support has
components that are inner products with non-A1 S_3 irrep basis vectors
(E and T1). By Schur orthogonality, K_R(q) = 0 identically for any q
in the A1 subspace.

- Note: `KR_A1_VANISHING_DERIVED_NOTE.md`
- Runner: `frontier_KR_A1_vanishing_proof.py`
- Status: PROVED (30/30 PASS)
- Method: explicit construction of the 7-dim S_3 decomposition +
  Schur orthogonality theorem
- Scope: proves K_R(A1) = 0 algebraically; any downstream application
  of this vanishing (e.g., in CKM |V_ub| amplitude selection) is a
  separate claim and is NOT in this note.

### P2. Rank-1 + Rank-(n-1) Projector Algebra

For any n-dim Hilbert space C^n, the rank-1 projector onto a unit
vector and the rank-(n-1) projector onto its complement satisfy
standard completeness, idempotency, and trace identities:
- Tr(P_1) = 1, Tr(P_(n-1)) = n-1
- weight_1 = 1/n, weight_(n-1) = (n-1)/n
- P_1 + P_(n-1) = I_n

- Note: `PROJECTOR_ALGEBRA_DERIVED_NOTE.md`
- Runner: `frontier_projector_algebra.py`
- Status: PROVED (25/25 PASS)
- Scope caveat: the note proves ONLY the algebra. Identification of
  the weight 1/6 with the UT CP phase cos²(δ) = 1/6 is a STRUCTURAL
  claim and is NOT proved here. The note flags this caveat explicitly.

## Clean negative results

### N1. V_sel-Fermion Coupling Gives Wrong Mass Structure

Derive closed-form: the natural coupling L_int = y Σ_i φ_i ψ̄ S_i ψ at
EWSB vacuum (0, 0, v), under the constraint removing the flat axis-3
mode, generates an effective hw=1 mass matrix with eigenvalues
{2α, α, 0} where α = y²/(64v²)². This is a 2+1 pattern with one
massless state, NOT the observed SM three-generation hierarchy.

- Note: `NEGATIVE_VSEL_WRONG_MASS_STRUCTURE.md`
- Method: closed-form algebra (matrix element derivation + eigenvalue
  computation)
- Status: RIGOROUS NEGATIVE — natural minimal V_sel-fermion coupling
  insufficient for SM mass structure

### N2. y_t = g_s/√6 Not Derivable from Standard Ward Identities

Four standard algebraic derivation attempts fail:
1. Gauge Ward identity — doesn't relate y_t to g_s
2. Chiral Ward identity — gives anomaly, not coupling ratio
3. Clebsch-Gordan on Q_L = (2, 3) — gives y_t = g_s/√2, wrong
4. Gauge-Yukawa universality on quark block — gives y_t = 2g_s, wrong

None produces the framework's claimed √6 factor.

- Note: `NEGATIVE_YT_SQRT_6_NOT_DERIVED.md`
- Method: explicit algebraic attempt along four standard routes
- Status: RIGOROUS NEGATIVE within standard machinery; doesn't rule
  out non-standard mechanisms (compositeness, etc.), which would
  require a separate derivation program.

## Reviewer verification

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py       # PASS=30
python3 scripts/frontier_projector_algebra.py           # PASS=25
```

Exit 0 on success, nonzero otherwise.

## Relation to the broader framework

The existing framework on `origin/main` contains many already-airtight
results (CMT partition identity, V_sel EWSB selector, anomaly-forced
3+1, native SU(2), graph-first SU(3), three-generation observable
algebra, physical-lattice invariants, discrete 3+1 GR on the project
route, UV-finite QG chain, CPT, I_3=0, emergent Lorentz, etc.). This
branch does not touch or reference those — they stand on their own.

My contributions add two small theorems (P1, P2) as building blocks
and two clean negatives (N1, N2) that identify where the framework's
Yukawa/mass/CKM sector currently rests on structural identifications
rather than rigorous derivations.

## What this branch is NOT

Not a flagship paper. Not a CKM derivation. Not a fermion mass
derivation. Not a replacement for the main-repo work. A narrow,
reviewer-hardened session contribution.
