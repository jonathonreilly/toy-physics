# Derived Science: Nature-Grade Airtight Results

**Branch:** `claude/main-derived` (derived from origin/main)
**Date:** 2026-04-16
**Bar:** every item here is either a pure-math theorem, a partition-function
identity, or a rigorous negative result that has been tested against
adversarial review.

This is NOT the full research program. It is the subset that currently
passes the Nature-grade bar — things that would survive a hostile
reviewer who demands proofs without imports or structural identifications.

## What this branch contains

### AIRTIGHT POSITIVES

| # | Claim | Authority | Runner | Status |
|---|---|---|---|---|
| 1 | Coupling Map Theorem α_s(v) = α_bare/u₀² | `YT_VERTEX_POWER_DERIVATION.md` | `frontier_vertex_power.py` | existing on main |
| 2 | EWSB selector V_sel = 32 Σ_{i<j} φ_i² φ_j² derived from trace identities | `GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md` | `frontier_graph_first_selector_derivation.py` | 63/63 PASS |
| 3 | K_R tensor carrier vanishes on A1 backgrounds via Schur S_3 orthogonality | `KR_A1_VANISHING_DERIVED_NOTE.md` | `frontier_KR_A1_vanishing_proof.py` | 30/30 PASS |
| 4 | Z₃ rank-1+rank-(n-1) projector algebra: weights 1/n and (n-1)/n | `PROJECTOR_ALGEBRA_DERIVED_NOTE.md` | `frontier_projector_algebra.py` | 25/25 PASS with scope caveats |
| 5 | Single-plaquette SU(3) ⟨P⟩ at β=6 exact: 0.78185 via Haar integration | `PLAQUETTE_SINGLE_EXACT_NOTE.md` | `frontier_plaquette_single_exact.py` | rigorous |

### AIRTIGHT NEGATIVES (clean obstructions)

| # | Claim | Authority | Status |
|---|---|---|---|
| N1 | ⟨P⟩ = 0.5934 at β=6 on 4D lattice cannot be derived analytically | `NEGATIVE_PLAQUETTE_NO_ANALYTIC.md` | three methods, all fail |
| N2 | V_sel-fermion coupling does NOT produce SM three-generation mass structure | `NEGATIVE_VSEL_WRONG_MASS_STRUCTURE.md` | eigenvalues {2α, α, 0} |
| N3 | y_t = g_s/√6 not derivable from gauge/chiral Ward identities, CG, or universality | `NEGATIVE_YT_SQRT_6_NOT_DERIVED.md` | four derivation attempts fail |

### FROM EXISTING MAIN (already airtight, not duplicated here)

These are already on main at Nature grade:
- Anomaly-forced 3+1 dimensionality theorem
- Native SU(2) bivector closure
- Graph-first structural SU(3) selector closure
- Three-generation observable algebra theorem
- Physical-lattice invariant theorems
- Full discrete 3+1 GR on project route
- UV-finite QG chain
- Exact native gauge closures
- CPT, I_3=0, emergent Lorentz theorems

## What this branch does NOT contain

Not included (fails the bar):

1. **CKM atlas numerical predictions** (|V_us|=√(α_s/2), |V_cb|=α_s/√6, etc.)
   — these use y_t = g_s/√6 (conjecture) + structural identifications.
2. **Fermion mass hierarchy predictions** (m_u/m_c = α_s²/(2π), etc.)
   — these depend on Fritzsch relation (imported from SM) + H1 hypothesis.
3. **Higgs mass / top mass predictions** — inherit the y_t conjecture.
4. **"Cabibbo angle from lattice" and related structural-identification notes**.
5. **H1 phase identification cos(α_12) = α_LM** — explicit hypothesis.
6. **Wolfenstein A from color projector** — by-analogy argument.
7. **NNI texture as consequence** — uses imported GST relation.

All of the above have strong numerical agreement with PDG, but none
is rigorously derived from Cl(3) on Z³ axioms alone. They are available
for future research but should not be promoted without derivation.

## How to read this branch

Start with `NATURE_GRADE_INDEX.md` for the structured entry point.

For reviewers:
- Each positive claim has a runner that verifies it
- Each negative claim has a proof of obstruction
- No claim here depends on "structural identification," "by analogy,"
  "natural normalization," or imported SM formulas

## Where the framework sits (honest assessment)

**Airtight domain (Nature-grade):**
- Gauge/algebraic structure (SU(2), SU(3), anomaly-forced 3+1)
- EWSB mechanism (V_sel with zero free parameters)
- Partition-function identities (CMT)
- Specific exact theorems (CPT, I_3, K_R A1, projector algebra)

**Open research domain (not in this branch):**
- Quantitative CKM magnitudes
- Fermion mass spectrum (all generations)
- Higgs/top mass predictions with rigorous chain
- Phase structure (CP, mixing phases)

**Session work preserved on:** `claude/stoic-almeida` branch (includes
all investigation, structural identifications, failed derivations, and
the full audit trail). That branch is where further research builds;
this branch is what gets reviewed.
