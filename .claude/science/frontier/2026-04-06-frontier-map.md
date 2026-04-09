# Frontier Map: 2026-04-06

## Coverage Summary
- Total scripts: 526
- Total log files: 275
- Mechanism families: 20+
- Confirmed results on main: ~10 (including today's merge of 33 commits)
- Branch-side exploratory: ~8 (BMV, area law, EP, binary, ringdown, unitarity, GW speed, cosmology)
- Honest limitations: 5 (strong-field, MI/d_TV h-dep, P_det underflow, gamma unmotivated, distance -1.1)
- Dead ends: 18+

## What Changed Today (merged to main)

### New retained positives
1. **Complex action** S=L(1-f)+i*gamma*L*f: Born holds, F~M=1.0, grown geometry transfer, h-independent transition
2. **h^2 measure** extends continuum to h=0.25: F~M 0.979→0.998
3. **T-normalization** preserves Born (vs data-dependent rescaling which broke it)
4. **Self-consistent Poisson back-reaction**: absorption at G_crit~0.011
5. **Electrostatics**: F~q^0.97 from same propagator
6. **Companion controls**: grown vs fixed agree to 0.1%
7. **QNM control hardening**: k=6.5,9.5 peaks are lattice artifacts (honest correction)

### Branch-side exploratory (NOT yet retained artifact chain)
- BMV entanglement (differential phase grows with G)
- Area law (S is W-independent at G=0.10)
- Equivalence principle (F~g^1.008, amplitude-level only)
- Binary beam attraction (excess 7-18% above baseline)
- GW speed (luminal by construction)
- Cosmological beam expansion (bounded positive)
- Unitarity (P conserved to 0.2%)

## Family Census

| Family | Scripts | Logs | Status |
|--------|---------|------|--------|
| Complex action | 6 | 2 | ACTIVE — strongest new result |
| Continuum limit (h^2+T) | 7 | 2 | ACTIVE — F~M converges |
| Back-reaction/self-gravity | 4 | 0 | ACTIVE — G_crit found |
| Distance law | 4 | 1 | PARTIAL — alpha -0.97 to -1.12 |
| Grown geometry (gate B) | 3 | 1 | RETAINED — transfers confirmed |
| 10-property card | 1 | 0 | RETAINED — 10/10 at h=0.25 |
| Mirror/Z2 DAG | 20+ | 30+ | EXHAUSTED on this branch |
| Lattice 3D dense | 15+ | 20+ | MATURE |
| Random/causal DAG | 30+ | 40+ | EXHAUSTED — ceiling theorem |
| Pocket wrap/taper | 40+ | 50+ | EXHAUSTED |
| NN/continuum | 3 | 0 | DEAD END (beam width → 0) |

## Top 5 Highest-Value Gaps

### 1. Wide h=0.125 continuum family (W=10+)
**Why:** The W=6 h=0.125 bridge resolved negative (P_det underflow). A wider
family (W=10) would test whether the continuum limit extends with controlled
boundary leakage. This is the #1 blocker for the continuum-limit claim.
**Status:** W=10 h=0.125 test RUNNING (6.2M nodes, ~30 min).
**Effort:** Running now. Result determines next move.
**Expected win:** If F~M stays near 1.0 and gravity TOWARD: continuum confirmed.

### 2. Exact-lattice / transfer gap closure
**Why:** All results are on the exact lattice (regular grid with known
coordinates). The grown geometry transfer shows 0.1% agreement on escape,
but the distance law and continuum limit have NOT been tested on grown
geometry. If the distance law works on grown geometry: the model is truly
geometry-independent.
**Feasibility:** Use existing grown geometry code + distance law measurement.
**Effort:** 1-2 hours.
**Expected win:** Geometry-independence of the distance law.

### 3. Persistent-object inertial mass
**Why:** The equivalence principle is confirmed at amplitude level (F~g^1.008)
but NOT at the persistent-object level. The repo's own notes say inertial
mass equality remains open. Getting this would upgrade EP from "amplitude-
level invariance" to "equivalence principle."
**Feasibility:** Needs a persistent-object definition (not just beam centroid).
**Effort:** Conceptual + 2-3 hours computation.
**Expected win:** Would be a genuine physics result, not just a lattice measurement.

### 4. Distance law in the geometric optics limit
**Why:** Current alpha = -0.97 to -1.12 with ~10% wave-optics correction.
Need to demonstrate that the correction vanishes in the geometric optics
limit (k → ∞, or equivalently, b/lambda → ∞). This would change the
distance law from "approximately 1/b" to "exactly 1/b in the continuum."
**Feasibility:** Needs very large lattice (W=40, L=200) at high k.
**Effort:** Multi-hour computation.
**Expected win:** Clean 1/b law would complete the Newton story.

### 5. Non-perturbative strong-field regime
**Why:** Currently, nothing converges at s ≥ 0.1. The model is perturbative.
Understanding WHY the strong field breaks (and whether a different action or
normalization fixes it) would open the GR strong-field regime.
**Feasibility:** Diagnostic (why does it break?) then fix.
**Effort:** 2-4 hours exploration.
**Expected win:** If fixable: opens black hole physics properly.

## Dead Ends (do not revisit)

1. Random DAGs — ceiling theorem (rank-1 transfer matrix)
2. NN-only lattice — beam width → 0
3. Data-dependent rescaling — breaks Born (0.348)
4. Emergent gamma from source motion — doesn't map quantitatively
5. Hawking thermal spectrum — resonance structure, not thermal
6. QNM k=6.5,9.5 peaks — lattice artifacts (control hardening)
7. Cosmological distance-rescaling — beam dynamics dominated by lattice
8. LN decoherence — k-band artifact
9. Quaternion propagator — no qualitative change
10. Soft amplitude penalty — collapses at N=60
