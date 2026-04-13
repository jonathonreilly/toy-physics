# Alpha_s Self-Consistency: Can the Lattice Constrain alpha_s?

## Status

**BOUNDED.** alpha_s(M_Pl) = 0.092 is NOT derived from first principles. It is computed from the lattice plaquette action with g_bare = 1 and Lepage-Mackenzie log resummation. The chain (g = 1 -> alpha_bare = 1/(4pi) -> plaquette improvement -> alpha_V = 0.092) is algebraic with no free parameters, but the CHOICE of g = 1 and V-scheme is a framework assumption, not a theorem.

**Script:** `scripts/frontier_alpha_s_self_consistency.py` (17/17 PASS, 8 exact, 9 bounded)

---

## Theorem / Claim

**Claim (bounded).** The V-scheme coupling alpha_V(M_Pl) = 0.092 is the unique output of the chain:

1. g_bare = 1 (unit hopping on staggered lattice)
2. alpha_bare = g^2/(4*pi) = 1/(4*pi) = 0.07958
3. c_1 = pi^2/3 = 3.290 (1-loop plaquette coefficient, SU(3))
4. alpha_V = -ln(1 - c_1 * alpha_bare) / c_1 = 0.0923

This chain has no free parameters once g = 1 and the log-resummation prescription are adopted. The numerical value 0.092 is then uniquely determined by lattice geometry and SU(3) group theory.

**Not a theorem:** The value g = 1 is the natural normalization (unit hopping, minimal phase per edge) but is not selected by a dynamical mechanism (no free energy extremum, no phase transition at beta = 6 for SU(3)).

---

## Assumptions

1. **Unit hopping normalization.** The bare gauge coupling g = 1 because the link variable U = exp(i*g*A*a) has unit phase per edge when a = 1 in lattice units.

2. **Lepage-Mackenzie log resummation.** The V-scheme coupling is defined by alpha_V = -ln(<P>) / c_1, not the simpler alpha_V = alpha_bare / <P>. The two definitions differ at O(alpha^2): mean-field gives 0.108, log gives 0.092.

3. **4D SU(3) plaquette coefficient.** c_1 = pi^2/3 is the standard 1-loop coefficient for the Wilson plaquette action in 4D SU(3). The framework uses a 3D spatial lattice; the 4D coefficient is used because the plaquette lives in the 4D spacetime including the derived temporal direction.

4. **V-scheme is the correct lattice scheme.** The V-scheme resums tadpole contributions and is natural for lattice calculations. Other schemes (MS-bar, MOM) would give different values.

---

## What Is Actually Proved

### Exact results (8 PASS):

1. **alpha_bare = 1/(4*pi)** from g = 1 unit hopping.
2. **alpha_V (mean-field) > alpha_V (log)** -- mean-field includes O(alpha^2) tadpole corrections that the log definition resums differently.
3. **alpha_V increases monotonically with g_bare** -- no fixed point or special value.
4. **Z^3 lattice has coordination number 6** and 3 plaquette orientations per site.
5. **V-scheme/MS-bar ratio = 4.82** at M_Pl -- confirms large scheme dependence.
6. **c_1 uniquely determines alpha_V** given g = 1.
7. **Scheme gap diagnostic:** 1/alpha_V < b_0*ln(M_Pl/M_Z)/(2pi), so the V-scheme coupling hits a Landau pole under perturbative QCD running. This confirms alpha_V is NOT an MS-bar coupling.
8. **Final status:** alpha_s = 0.092 is BOUNDED.

### Bounded results (9 PASS):

1. **alpha_V (log) = 0.0923 in [0.088, 0.098]** -- the plaquette-improved coupling is in the expected range.
2. **g = 1 gives alpha_V within 0.3% of 0.092** -- the unit hopping normalization naturally produces the value used in the y_t chain.
3. **MS-bar alpha_s(M_Pl) ~ 0.019** from 1-loop SM extrapolation -- consistent with standard asymptotic freedom.
4. **MS-bar inversion is self-consistent** -- running from observed alpha_s(M_Z) to M_Pl gives the same 0.019.
5. **m_t = 174.2 GeV** from V-scheme BC + MS-bar RGE (0.7% from observed) -- the y_t prediction chain works.
6. **K_4D = 0.155** numerical integral matches the exact value 0.15493.
7. **alpha_V from m_t inversion = 0.089** -- within 3.3% of the lattice value 0.092.
8. **alpha_s = 0.092 is inside the m_t-allowed range** [0.078, 0.103].
9. **Spread of determinations = 0.019** (< 0.02) -- V-scheme values and m_t inversion are mutually consistent.

---

## What Remains Open

### 1. Why g = 1?

The bare coupling g = 1 is the natural normalization for unit hopping but is not forced by:
- A variational principle (no free energy minimum at beta = 6)
- A phase transition (SU(3) in 4D has no bulk transition at beta = 6)
- A fixed point of the RG (g = 1 is in the crossover regime, not at a critical point)

The strongest argument: in the framework, the lattice IS the Planck-scale structure. The gauge field lives on graph edges with U = exp(i*A). Setting g = 1 means each edge carries exactly one unit of gauge phase -- the minimal, canonical coupling. This is a naturalness argument, not a derivation.

### 2. Why V-scheme (log resummation)?

Two V-scheme definitions exist:
- Mean-field: alpha_V = alpha_bare / <P> = 0.108
- Log resum: alpha_V = -ln(<P>) / c_1 = 0.092

The log definition is the standard Lepage-Mackenzie prescription and is used throughout the y_t chain. But the CHOICE of log vs mean-field vs some other resummation is a convention. The two differ by 17%, and the y_t prediction (m_t = 174 GeV) uses the log value.

### 3. Scheme matching at M_Pl

The V-scheme coupling (0.092) and MS-bar coupling (0.019) differ by a factor of 4.8 at M_Pl. This is not an inconsistency -- they are different renormalization schemes and are expected to differ at strong coupling. But the lack of a non-perturbative scheme-matching calculation means we cannot derive one from the other.

The y_t chain avoids this problem: it uses g_V to set y_t(M_Pl) = g_V/sqrt(6), then runs y_t down with MS-bar gauge couplings. The gauge couplings in the RGE come from observed alpha_s(M_Z) run up to M_Pl in MS-bar, NOT from the V-scheme. Only the y_t boundary condition uses V-scheme.

---

## How This Changes The Paper

### Before this work:

- alpha_s(M_Pl) = 0.092 was stated as "from the plaquette action" without systematic analysis of whether this is derived or assumed.

### After this work:

- alpha_s(M_Pl) = 0.092 is precisely characterized as the output of: g=1 + c_1 + log resummation. This is algebraic with no free parameters.
- The scheme gap (V-scheme vs MS-bar factor ~5) is documented and shown to be compatible with the y_t prediction chain.
- The m_t inversion gives alpha_V ~ 0.089, within 3.3% of the lattice value, providing a bounded consistency check.
- The honest status is: BOUNDED. The chain has no free parameters but the starting assumptions (g=1, V-scheme) are not derived.

### Paper-safe wording:

> The V-scheme coupling alpha_V(M_Pl) = 0.092 is computed from the unit-normalized staggered lattice (g_bare = 1) with Lepage-Mackenzie log resummation. This enters the top-mass prediction as a bounded input from the gauge couplings lane. The value is framework-natural but not derived from first principles.

### What would close this lane:

A derivation that g_bare = 1 is the unique self-consistent bare coupling (e.g., from a lattice partition function extremum, a gauge-gravity consistency condition, or a uniqueness theorem for the coupling normalization).

---

## Answers to the Four Original Questions

### Q1: Is g = 1 the unique self-consistent value?

**No.** g = 1 is natural but not unique. The Wilson free energy is monotonically decreasing in beta = 2N_c/g^2 -- no extremum at beta = 6. There is no phase transition at this value for SU(3). The argument is: g = 1 means one unit of gauge phase per edge, which is the canonical/minimal coupling for a lattice gauge theory where the lattice spacing sets the only scale.

### Q2: Is the match to alpha_s(M_Z) = 0.1179 a nontrivial consistency check?

**Yes, but not in the naive way.** The V-scheme alpha_V = 0.092 CANNOT be directly run down to M_Z with perturbative QCD RGEs (it hits a Landau pole at 1/alpha_V ~ 11 < b_0*ln(M_Pl/M_Z)/(2pi) ~ 44). Instead, the consistency check is: the MS-bar alpha_s(M_Pl) = 0.019 (from observed alpha_s(M_Z) run up) is used for the gauge couplings in the RGE, while the V-scheme g_V enters only through y_t = g_V/sqrt(6). The resulting m_t = 174.2 GeV is within 0.7% of observed, which IS a nontrivial check of the V-scheme value.

### Q3: Are the strong-coupling expansion coefficients uniquely determined by lattice geometry?

**Yes.** The 1-loop plaquette coefficient c_1 = pi^2/3 is uniquely determined by (dimension, gauge group, lattice type). For Z^d lattices, the free gluon propagator integral K_d (which determines c_1) is a purely geometric quantity: K_2D = 0.811, K_3D = 0.250, K_4D = 0.155. Given c_1 and alpha_bare = 1/(4*pi), the V-scheme coupling is algebraically fixed.

### Q4: Does the match to m_t = 173.0 GeV constrain alpha_s retroactively?

**Yes, weakly.** Inverting the y_t prediction chain: m_t = 173.0 GeV requires alpha_V(M_Pl) = 0.089 (3.3% below the lattice value 0.092). With a ~5% theory band from RGE and threshold uncertainties, the allowed range is alpha_V in [0.078, 0.103]. The lattice value 0.092 is comfortably inside. The sensitivity is d(m_t)/d(alpha_V) ~ 385 GeV, so delta(alpha_V) = 0.003 produces delta(m_t) = 1.2 GeV.

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_alpha_s_self_consistency.py
```

**Output:** PASS=17 FAIL=0 (exact: 8P/0F, bounded: 9P/0F)

**Test classification:**
- 8 exact checks: algebraic identities, lattice geometry, scheme diagnostics
- 9 bounded checks: numerical consistency, RGE running, m_t prediction
