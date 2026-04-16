# Nature-Grade Index: Derived Science

**Branch:** `claude/main-derived`
**Last updated:** 2026-04-16

## Positive airtight derivations

### P1. Coupling Map Theorem (CMT)

α_s(v) = α_bare / u_0² as partition-function identity.

- Authority: `YT_VERTEX_POWER_DERIVATION.md` (existing on main)
- Runner: `frontier_vertex_power.py` (existing)
- Status: PROVED (algebraic path-integral identity)

### P2. EWSB Selector Derivation

V_sel(φ) = 32 Σ_{i<j} φ_i² φ_j² from trace identities on cube-shift
operators S_i.

- Authority: `GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md` (existing)
- Runner: `frontier_graph_first_selector_derivation.py` — 63/63 PASS
- Status: PROVED (zero free parameters, S_3 → Z_2 cascade forced)

### P3. K_R Vanishes on A1 Backgrounds

Pure S_3 representation theory.

- Authority: `KR_A1_VANISHING_DERIVED_NOTE.md`
- Runner: `frontier_KR_A1_vanishing_proof.py` — 30/30 PASS
- Status: PROVED (Schur orthogonality)

### P4. Rank-1 + Rank-(n-1) Projector Algebra

Weights 1/n and (n-1)/n for C^n decomposition.

- Authority: `PROJECTOR_ALGEBRA_DERIVED_NOTE.md`
- Runner: `frontier_projector_algebra.py` — 25/25 PASS
- Status: PROVED (algebra only; UT identification caveat documented)

### P5. Single-Plaquette SU(3) ⟨P⟩_1(β) Exact

⟨P⟩_1(β=6) = 0.78185 via Haar integration (all β).

- Authority: `PLAQUETTE_SINGLE_EXACT_NOTE.md`
- Runner: `frontier_plaquette_single_exact.py`
- Status: PROVED (numerical quadrature of closed-form integral;
  leading β/6 and 4/(3β) verified)

### P6. Gauge-Vacuum Plaquette Scalar-Bridge Theorem

⟨P⟩(β) = ⟨P⟩_1plaq(β_eff) with β_eff = β · (3/2) · (2/√3)^(1/4), on
the chosen 3+1 scalar-bridge route.

- Authority: `GAUGE_VACUUM_PLAQUETTE_BRIDGE_THEOREM_NOTE.md` (on main)
- Supplement: `PLAQUETTE_ANALYTIC_DERIVATION_NOTE.md` (in this branch)
- Runners: `frontier_scalar_3plus1_temporal_ratio.py` (EXACT 4/4 + 1)
  and `frontier_gauge_vacuum_plaquette_bridge_theorem.py` (THEOREM 8/8 + COMPUTE 1/1)
- Status: theorem closed on main; numeric migration across downstream
  lanes pending.

## Clean negative results

### N2. V_sel-Fermion Coupling Gives Wrong Mass Structure

- Authority: `NEGATIVE_VSEL_WRONG_MASS_STRUCTURE.md`
- Method: closed-form eigenvalue computation: {2α, α, 0}
- Status: RIGOROUS NEGATIVE (2+1 pattern, not 1+1+1 hierarchy)

### N3. y_t = g_s/√6 Not Derivable from Standard Ward Identities

- Authority: `NEGATIVE_YT_SQRT_6_NOT_DERIVED.md`
- Method: four algebraic derivation attempts (gauge Ward, chiral
  Ward, Clebsch-Gordan, gauge-Yukawa universality) all fail
- Status: RIGOROUS NEGATIVE within standard machinery; open to
  non-standard mechanisms

## Standing on main (already airtight, not duplicated)

- Anomaly-forced 3+1 dimensionality theorem
- Native SU(2) bivector closure
- Graph-first structural SU(3) (selector + commutant)
- Three-generation observable algebra theorem
- Physical-lattice invariant theorems
- Exact discrete 3+1 Einstein-Regge GR on PL S³ × ℝ
- UV-finite partition-density chain + canonical continuum closure
- Exact CPT on free staggered lattice
- Exact I_3 = 0 / no third-order interference
- Emergent Lorentz invariance (dim-6 cubic-harmonic ℓ=4 signature)

## What is NOT on this branch (and why)

### Not airtight — depends on structural identifications:

- CKM magnitude formulas |V_us|² = α_s/2, |V_cb| = α_s/√6, |V_ub|
  → depend on y_t = g_s/√6 (conjecture, N3) and the UT-projector
    identification (caveat in P4)

- CP phase δ = arctan(√5) → depends on UT identification (caveat in P4)

- Fermion mass ratios m_d/m_s = α_s/2, m_u/m_c = α_s²/(2π), etc.
  → depend on GST relation (imported SM) + H1 hypothesis
    (cos α_12 = α_LM, no derivation)

- y_t, m_t, m_H quantitative predictions → depend on N3 conjecture

### Open research directions (flagged for future programs):

- Attempt to derive √6 from non-standard mechanisms (compositeness,
  framework-specific spin-taste, etc.)
- Extend any successful √6 derivation to y_b, y_c, y_u, y_s, y_d,
  y_τ, y_μ, y_e
- Derive fermion mass matrix structure (beyond V_sel insufficiency)
- Derive CKM magnitudes rigorously (not via GST/Fritzsch imports)
- Derive CP phase rigorously (beyond the projector-weight identification)

## Reviewer workflow

To verify the airtight claims on this branch:

```bash
# EWSB selector (already on main)
python3 scripts/frontier_graph_first_selector_derivation.py    # expect PASS=63

# Tensor carrier A1 vanishing
python3 scripts/frontier_KR_A1_vanishing_proof.py              # expect PASS=30

# Projector algebra
python3 scripts/frontier_projector_algebra.py                  # expect PASS=25

# Single-plaquette exact (slower; ~minute)
python3 scripts/frontier_plaquette_single_exact.py
```

Each runner exits with PASS/FAIL summary and nonzero status on failure.

## Scientific posture

This branch is the **airtight, reviewer-facing core** of the framework.
It is deliberately NARROWER than the flagship paper claims. It trades
breadth for rigor.

Full research program (including the conjectural CKM/mass/Higgs
sector) lives on `claude/stoic-almeida` with the full audit trail
and honest identification of gaps.

## Session artifacts preserved elsewhere

For the multi-session rigorous attack that produced these verdicts,
see commits on `claude/stoic-almeida`:
- Sessions A, B, C, C-deep.1 through C-deep.4
- Adversarial reviews
- Fermion mass program exploration
- Hierarchical diagonalization attempts
