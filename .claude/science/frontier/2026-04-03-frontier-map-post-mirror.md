# Frontier Map: 2026-04-03 (post-mirror update)

## Coverage Summary
- Total scripts: ~500 (473 in worktree + ~25 on main-only)
- Total log files: 270
- Mechanism families: 20+
- Confirmed results: 8 (5 prior + ceiling theorem + mirror Z₂ + S4 joint)
- Unvalidated observations: ~5
- Dead ends: 15+
- New lanes opened this session: 4 (mirror, spectral, dynamical, quaternion)

## New Confirmed Results (this session)

6. **Ceiling theorem:** Transfer matrix product is rank-1 on random DAGs.
   Lindeberg condition passes. Spectral no-go for all downstream mechanisms.

7. **Z₂ mirror symmetry:** Decoherence exponent -0.27 (vs -1.0 random).
   N_half = 4.7M. Born: machine precision. d_TV stable 0.2-0.8 through N=100.

8. **S4 mirror joint coexistence:** Born=2.5e-15, gravity=6.5 SE,
   decoherence=25% at N=60. All four phenomena on same graph/propagator.

## New Dead Ends (this session)

13. LN creates zero genuine decoherence (k-band artifact, single-k pur=1.0)
14. Quaternion propagator — magnitudes still sum like reals, no qualitative change
15. Cumulative specificity weights — S_norm saturates at 1.0, purity doesn't improve
16. Soft amplitude penalty — collapses at N=60, kills throughput
17. Cross-channel edge penalty — S_norm unchanged, edges not the mechanism
18. Collapse on 3D — Born=0.03 (marginal), positive exponent was artifact

## Updated Top 5 Highest-Value Gaps

### 1. Mirror gravity quantitative laws
**Why:** S4 mirror gives gravity at 6.5 SE but mass scaling alpha=0.26
(vs 0.82 on standard) and near-field distance only. The mirror geometry
creates a different gravity regime. Need to understand whether this is
fundamental or tunable. If tunable: a single architecture achieves
everything. If fundamental: the project has two complementary families.
**Feasibility:** Needs mass placement strategy exploration on mirror
graphs (controlled y-offset, variable field strength, larger graphs).
**Effort:** 2-3 hours computation.
**Expected win:** Clarity on whether unification is complete or structural.

### 2. Mirror + higher dimensions (3D→4D mirror)
**Why:** 3D mirror gives exponent -0.27. The 3D synthesis showed
higher dimension delays the ceiling. Does 4D mirror give an even
better exponent? If the mirror exponent improves with dimension,
4D mirror could be the ultimate architecture.
**Feasibility:** Needs 4D mirror generator (straightforward extension).
**Effort:** 2 hours (new generator + scaling test).
**Expected win:** If 4D mirror exponent < -0.27: new best scaling.

### 3. Symmetry-broken mirror (controlled Z₂ breaking)
**Why:** Exact Z₂ is essential (approximate doesn't work). But what
about WEAK explicit breaking? If we add a small asymmetry parameter ε
(e.g., edge weights 1±ε across the mirror), does decoherence degrade
gradually or collapse? This maps the sensitivity of the symmetry
protection and determines how robust the mechanism is.
**Feasibility:** Easy modification of S4 generator.
**Effort:** 1-2 hours.
**Expected win:** Robustness curve for the symmetry mechanism.

### 4. Born rule on standard (non-mirror) DAGs with controlled mass
**Why:** The other thread's standard DAG gravity results (1/b², F∝M)
used uncontrolled mass placement. Our fixed-position controls caught
3 confounds. Need to verify the quantitative laws survive on standard
DAGs with proper controls.
**Feasibility:** Existing scripts, new control methodology.
**Effort:** 2 hours.
**Expected win:** Clean quantitative gravity laws or another retraction.

### 5. Entanglement entropy / mutual information
**Why:** Purity measures total mixedness. But the PHYSICALLY relevant
quantity is how much which-slit information reaches the detector.
Mutual information I(slit; detector_bin) measures this directly.
On mirror DAGs with S_norm=1.0, the MI should be maximal.
**Feasibility:** Needs new computation (conditional distributions).
**Effort:** 1-2 hours.
**Expected win:** New observable that may show different scaling.

## Previously Identified Gaps — Status Update

- Gap 1 (analytical ceiling derivation): **DONE** — ceiling theorem
  proved via transfer matrix rank-1 analysis.
- Gap 2 (4D decoherence escape): Partially addressed — 4D results
  exist on main but need mirror extension.
- Gap 3 (k-dependence): Still open but lower priority since the
  k-band artifact was caught and single-k is now standard.
- Gap 4 (LN + modular + 4D triple): **PARTIALLY CLOSED** — LN
  creates zero genuine decoherence (artifact). The triple doesn't
  stack because LN is cosmetic.
- Gap 5 (mutual information): Still open and promoted to #5.
