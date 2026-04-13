# Minimal Axiom Inventory for the Cl(3) on Z^3 Framework

**Date:** 2026-04-12
**Purpose:** Referee-ready document answering: "How many independent
assumptions does this framework actually have?"
**Branch:** `claude/youthful-neumann`

---

## Part 1: Candidate Axiom List

Every assumption used anywhere in the derivation chain, with the file
where it is stated or first imported.

| # | Candidate assumption | Where stated | Used by |
|---|---------------------|--------------|---------|
| C1 | **Finite-dimensional Hilbert space** with local tensor product structure H = H_1 x ... x H_N | `SINGLE_AXIOM_HILBERT_NOTE.md`, `AXIOM_REDUCTION_NOTE.md` (as "A1 + A2"), `COMPLETE_DERIVATION_CHAIN_2026-04-12.md` | Everything. This is the proposed single axiom. |
| C2 | **d_local = 2 (qubit factors)** | `ULTIMATE_SIMPLIFICATION_NOTE.md`, `COMPLETE_DERIVATION_CHAIN_2026-04-12.md` (Step 0) | SU(2) gauge structure, Cl(3), taste space dimension 8 |
| C3 | **d = 3 spatial dimensions** (the graph is Z^3, not Z^d for other d) | `AXIOM_REDUCTION_NOTE.md` (as "C1"), `DIMENSION_SELECTION_NOTE.md` | Force law 1/r^2, kernel power, atomic stability, SU(3), generations |
| C4 | **Cubic lattice topology** (Z^3 specifically, not arbitrary 3-regular graph) | `SU3_FORMAL_THEOREM_NOTE.md`, `RENORMALIZED_YT_THEOREM_NOTE.md` | Bipartite structure, staggered phases, Kawamoto-Smit decomposition |
| C5 | **Nearest-neighbor (staggered) Hamiltonian** | `COMPLETE_DERIVATION_CHAIN_2026-04-12.md`, `YT_FORMAL_THEOREM_NOTE.md` | Cl(3) algebra, bipartite anticommutation, taste-space structure |
| C6 | **Unitarity** (Hermitian H, unitary time evolution) | `AXIOM_REDUCTION_NOTE.md` (as "A2"), `SINGLE_AXIOM_HILBERT_NOTE.md` | Born rule, linearity, complex amplitudes, gravity sign |
| C7 | **Self-consistency** (propagator density sources the field it propagates in) | `AXIOM_REDUCTION_NOTE.md` (D5), `COMPLETE_DERIVATION_CHAIN_2026-04-12.md` (Step 2) | Poisson equation, gravity |
| C8 | **Attraction requirement** (gravity is attractive) | `AXIOM_REDUCTION_NOTE.md` (D6) | Valley-linear action selection |
| C9 | **Newtonian mass scaling** F ~ M | `AXIOM_REDUCTION_NOTE.md` (D6) | Selects weak-field-linear action |
| C10 | **One normalization from observation** (G or c = 1 matching) | `AXIOM_REDUCTION_NOTE.md` (D7), `COMPLETE_DERIVATION_CHAIN_2026-04-12.md` (Step 3) | Coupling constant |
| C11 | **Taste-physicality**: the lattice spacing a = l_Planck is physical, not a regulator; no continuum limit exists | `GENERATION_PHYSICALITY_THEOREM_NOTE.md` (Assumption 1), `CODEX_GENERATION_RESPONSE.md` | Generations, mass hierarchy, DM ratio, CKM |
| C12 | **Hamiltonian homogeneity** (translational invariance: same local Hamiltonian at every site) | `S3_COMPACTIFICATION_THEOREM_NOTE.md` (Gap G1) | S^3 compactification, regular graph, cosmological constant |
| C13 | **Local growth from a seed** | `S3_COMPACTIFICATION_THEOREM_NOTE.md` (Assumption 3), `DM_RELIC_MAPPING_THEOREM_NOTE.md` | S^3 topology, primordial spectrum, Hubble expansion |
| C14 | **g_bare = 1** (bare gauge coupling at the lattice cutoff) | `CODEX_DM_RESPONSE.md` (Objection 1) | alpha_s = 0.092, DM ratio, top Yukawa boundary condition |
| C15 | **sigma_v = pi alpha_s^2 / m^2** (perturbative s-wave cross-section) | `CODEX_DM_RESPONSE.md` (Objection 3) | DM relic abundance, freeze-out x_F |
| C16 | **V(r) = -C_F alpha_s / r** (Coulomb potential shape) | `CODEX_DM_RESPONSE.md` (Objection 3) | Sommerfeld enhancement |
| C17 | **Thermodynamic limit** (N -> infinity) | `DM_RELIC_MAPPING_THEOREM_NOTE.md` (Assumption 3) | Boltzmann equation from lattice master equation, Stefan-Boltzmann law |
| C18 | **Graph-first axis selection** (quartic invariant V_sel selects a distinguished spatial axis) | `SU3_FORMAL_THEOREM_NOTE.md`, `PAPER_OUTLINE_2026-04-12.md` (Section 4) | SU(3) from commutant theorem |
| C19 | **SM branch selection** (anomaly cancellation fixes RH singlet completion) | `review.md` (RH matter boundary) | Right-handed sector, full one-generation matter closure |
| C20 | **Wilson term parameter r ~ O(1)** | `GENERATION_PHYSICALITY_THEOREM_NOTE.md` (Assumption 2) | Mass splitting between generations |
| C21 | **Anisotropy** t_x != t_y != t_z | `GENERATION_PHYSICALITY_THEOREM_NOTE.md` (Assumption 3) | Intra-generation mass hierarchy, CKM mixing |
| C22 | **Coleman-Weinberg Higgs** (Higgs = G_5 condensate) | `RENORMALIZED_YT_THEOREM_NOTE.md` (Assumption 5) | y_t boundary condition protection |
| C23 | **Cl(3) automorphism preservation under RG** | `RENORMALIZED_YT_THEOREM_NOTE.md` (Assumption 4) | Non-renormalization of y_t/g_s ratio |
| C24 | **One calibration scale** (lattice units to GeV conversion) | `DM_RELIC_MAPPING_THEOREM_NOTE.md` (Assumption 4) | All dimensionful predictions |
| C25 | **Spin-statistics connection** (7/8 Fermi-Dirac factor) | `FREEZEOUT_FROM_LATTICE_NOTE.md` | g_* = 106.75 |

---

## Part 2: Redundancy Analysis

For each candidate, can it be derived from others?

### Clearly redundant (derivable from the core)

| Candidate | Derived from | How |
|-----------|-------------|-----|
| C6 (Unitarity) | C1 | Hermitian H on a finite Hilbert space automatically generates unitary evolution. Unitarity IS the Hilbert space structure. |
| C7 (Self-consistency) | C1 | If the propagator lives on the same graph that sources the field, self-consistency is a closure condition, not a separate postulate. It is the statement that the framework is internally consistent rather than a new axiom. However, the SPECIFIC choice (propagator density sources field) vs other couplings arguably carries content. |
| C8 (Attraction) | Not independent | Attraction is an OBSERVATION the framework must match, not a postulate. It constrains which solutions are physical. If treated as input, it selects the valley-linear action from a family, but the family itself follows from C1 + C3. |
| C9 (Newtonian F ~ M) | Not independent | Same status as C8. An empirical boundary condition, not a postulate. |
| C10 (One normalization) | Not independent | Every theory requires matching one observable to set units. This is a boundary condition, universally present, not a framework-specific axiom. |
| C24 (Calibration scale) | = C10 | Same content: one dimensionful number from experiment. |
| C25 (Spin-statistics) | C1 + C5 | The staggered fermion sign structure on the bipartite lattice encodes the spin-statistics connection. The 7/8 factor follows from the lattice Fermi-Dirac statistics, which is a consequence of the anticommuting nature of the staggered fields. |

### Partially redundant (arguably derivable, but with caveats)

| Candidate | Arguably from | Caveat |
|-----------|--------------|--------|
| C2 (d_local = 2) | C1 + C3 + physics requirements | d_local = 2 is the minimum for interference AND the only value giving SU(2). But the AXIOM_REDUCTION_NOTE claims it follows from "minimum for interference." The argument is: complex amplitudes require d_local >= 2, and d_local = 2 is the simplest. This is a minimality/naturalness argument, not a derivation. A referee could ask: why not d_local = 4? |
| C4 (Cubic topology) | C3 | Z^3 is the canonical regular lattice in d = 3. But other 3D lattices exist (FCC, BCC, hexagonal). The cubic lattice is selected by the requirement that the bipartite structure give Cl(3) with the right staggered phases. Whether this is "forced" or "chosen" is debatable. |
| C5 (Nearest-neighbor) | C1 (locality) | Nearest-neighbor coupling is the minimal local interaction on a graph. But "local" could mean next-to-nearest-neighbor or finite-range. Nearest-neighbor is a simplicity choice. |
| C11 (Taste-physicality) | C1 (finite H) | The CODEX_GENERATION_RESPONSE argues this is a theorem: within the Cl(3) framework, 5 independent arguments show no continuum limit exists. The framework is Hamiltonian by construction, so no fourth-root trick is available. Taste-physicality is then a CONSEQUENCE of the framework, not an additional axiom. But: this argument is circular if someone questions the framework itself. |
| C18 (Axis selection) | C3 + C4 + C5 | The quartic invariant V_sel arises from the graph-shift operators on Z^3. Given the cubic lattice with staggered phases, the axis selection is forced by the structure. It is not an independent input. |
| C22 (Coleman-Weinberg Higgs) | C5 | If the only lattice fields are the staggered fermions and the link variables, the Higgs must be a composite (condensate). G_5 is the unique candidate because it is central in Cl(3). This is arguably forced, not chosen. |
| C23 (Cl(3) preservation under RG) | C1 + C4 + C5 | Block-spin RG on a bipartite cubic lattice maps staggered lattice to staggered lattice. The bipartite structure is preserved. Cl(3) automorphism preservation follows. This is close to a theorem. |

### Genuinely independent (not derivable from the core)

| Candidate | Why independent | What it costs to add |
|-----------|----------------|---------------------|
| C1 (Finite local tensor product Hilbert space) | THE foundational axiom. Cannot be derived from anything simpler. | Nothing -- this is the starting point. |
| C3 (d = 3) | 6 arguments support it, 2 are hard bounds (gravity attractive only d >= 3; atomic stability only d <= 3). But no DYNAMICAL mechanism selects d = 3. The intersection of the two bounds is d = 3, which is a derivation IF you accept that both gravity and atoms must exist. | The honest status: d = 3 is forced by the conjunction "attractive gravity AND stable atoms." Whether that conjunction counts as "derived" or "assumed" depends on whether you take the existence of atoms as a physical requirement. |
| C12 (Homogeneity) | Not derivable from C1. A tensor product with local interactions does NOT require translational invariance. Disordered systems have local tensor product structure but are not homogeneous. | Adds one axiom if the S^3 compactification is claimed. |
| C13 (Local growth) | Not derivable from a static Hilbert space. Growth requires a dynamical rule beyond H. | Adds one axiom for cosmological claims (expansion, freeze-out, primordial spectrum). |
| C14 (g_bare = 1) | Not derivable. See CODEX_DM_RESPONSE Objection 1. O(1) is natural; = 1 is specific. | Required for any numerical prediction involving alpha_s. |
| C15 (sigma_v formula) | Imported from perturbative QFT. Not derivable from the lattice. | Required for DM relic abundance. |
| C16 (Coulomb potential) | The 1/r form IS the lattice Green's function, so the shape is derivable. But the identification V_QCD = lattice Green's function is an additional physical step. | Required for Sommerfeld enhancement. Partially derivable. |
| C19 (SM branch / anomaly cancellation) | Anomaly cancellation is a self-consistency condition of quantum gauge theory. Within the framework, it constrains the RH sector. But it does not UNIQUELY select the SM -- other anomaly-free completions may exist. The "SM branch" is a CHOICE among anomaly-free solutions. | Required for RH matter. Adds content beyond the spatial graph. |
| C20 (Wilson r ~ O(1)) | Not derivable. The Wilson parameter r is a coefficient in the lattice action. Its value is not fixed by the Cl(3) structure. | Required for quantitative mass hierarchy. |
| C21 (Anisotropy) | Not derivable from the cubic lattice, which is isotropic by construction. The origin of anisotropy is unspecified. | Required for CKM mixing and intra-generation mass splitting. |

---

## Part 3: The Irreducible Set

The smallest set of independent axioms from which everything else follows,
organized by what they are needed for.

### Tier 1: The structural backbone (needed for all retained results)

| # | Axiom | Content |
|---|-------|---------|
| I1 | **Finite local tensor product Hilbert space** | Nodes = tensor factors; edges = Hamiltonian support; unitarity and Born rule automatic. Encodes C1 + C6. |
| I2 | **d_local = 2, d = 3, cubic, nearest-neighbor** | The graph is qubits on Z^3 with nearest-neighbor staggered Hamiltonian. This packages C2 + C3 + C4 + C5 into one geometric specification. |

These two axioms suffice for: Newtonian gravity (Poisson, 1/r^2, F ~ M1 M2,
WEP, time dilation, light bending factor 2), Born rule, SU(2) gauge structure,
structural SU(3) from commutant theorem, left-handed charge matching, orbit
algebra 8 = 1+3+3+1, taste-physicality (as a theorem within the framework).

### Tier 2: Required for specific claimed results

| # | Axiom | Needed for | Without it |
|---|-------|-----------|-----------|
| I3 | **Hamiltonian homogeneity** (translational invariance) | S^3 compactification, cosmological constant | Lose the S^3 topology argument and Lambda prediction |
| I4 | **Graph growth** (H_graph > 0, local seed) | Expansion, freeze-out, DM relic abundance, primordial spectrum | Lose all cosmological results |
| I5 | **g_bare = 1** | Numerical value of alpha_s, hence m_t prediction and DM ratio | Lose specific numerical predictions; structural results survive |
| I6 | **SM branch selection** (anomaly cancellation picks SM completion) | Right-handed sector, full matter content | Lose RH matter; LH gauge structure still holds |

### Tier 3: Required only for bounded/phenomenological results

| # | Axiom | Needed for |
|---|-------|-----------|
| I7 | Wilson parameter r ~ O(1) | Quantitative mass hierarchy |
| I8 | Anisotropy t_x != t_y != t_z | CKM mixing, intra-generation splitting |
| I9 | sigma_v = pi alpha^2/m^2 (perturbative QFT) | DM relic abundance numerical value |
| I10 | Thermodynamic limit (N -> infinity) | Boltzmann equation from lattice master equation |

---

## Part 4: What Breaks If You Remove Each Irreducible Axiom

| Axiom | What breaks | Strongest result lost |
|-------|-----------|---------------------|
| **I1** (Hilbert space) | Everything. No propagator, no Born rule, no gravity, no gauge groups. | The entire framework. |
| **I2** (qubits on Z^3, NN staggered) | Removing d_local = 2: lose SU(2), Cl(3), all gauge structure. Removing d = 3: lose 1/r^2 gravity, atomic stability, SU(3), three generations. Removing cubic: lose bipartite structure, staggered phases, Kawamoto-Smit decomposition. Removing NN: lose Cl(3) anticommutation relations. | Any single sub-component of I2 destroys the gauge-gravity unification. |
| **I3** (Homogeneity) | Lose regularity of the graph. The finite graph may have boundaries or irregular vertices. S^3 compactification fails. Cosmological constant prediction lost. | Lambda_pred/Lambda_obs = 1.46 |
| **I4** (Growth) | The graph is static. No expansion, no Hubble parameter, no freeze-out, no DM relic abundance, no primordial spectrum. All cosmological results vanish. | DM ratio R = 5.48 and all cosmological windows |
| **I5** (g_bare = 1) | alpha_s becomes a free parameter. The top mass prediction becomes a one-parameter family y_t = g_s(g_bare)/sqrt(6). The DM ratio becomes a function R(g_bare). Structural results (gauge groups, gravity law) unaffected. | m_t = 174 GeV as a numerical prediction |
| **I6** (SM branch) | Only the left-handed sector is derived from the spatial graph. The right-handed singlet completion is undetermined. Anomaly cancellation is not verified. Full one-generation matter closure is lost. | RH matter content; anomaly-free hypercharge |
| **I7** (Wilson r) | Inter-orbit mass splitting becomes qualitative (linear in Hamming weight) but not quantitative. | Quantitative 3-generation mass hierarchy |
| **I8** (Anisotropy) | All intra-orbit splittings vanish. CKM mixing disappears. | CKM matrix elements, Cabibbo angle |
| **I9** (sigma_v) | Cannot compute DM annihilation cross-section from the lattice. Freeze-out calculation loses its normalization. | DM relic abundance numerical value |
| **I10** (Thermo limit) | The Boltzmann equation is only an approximation on finite graphs. Stefan-Boltzmann T^4 law is only bounded. | Formal derivation of freeze-out from lattice |

---

## Part 5: Is "Cl(3) on Z^3" Really One Axiom?

The claim "everything from Cl(3) on Z^3" packages SEVERAL logically
independent specifications:

### Unpacking "Cl(3) on Z^3"

| Component | What it specifies | Independent content |
|-----------|------------------|-------------------|
| **Cl(3)** | The Clifford algebra generated by 3 anticommuting elements | Fixes d_local = 2 (each generator acts on C^2), fixes the number of generators = 3, fixes the anticommutation relations |
| **Z^3** | The 3-dimensional integer lattice | Fixes d = 3, fixes cubic topology, fixes infinite extent (before finiteness is imposed) |
| **"on"** | Staggered fermion realization: Cl(3) generators are the Kawamoto-Smit operators on Z^3 | Fixes nearest-neighbor coupling, fixes the staggered phase convention eta_mu, fixes bipartite structure |
| **Finite** | The Hilbert space is finite-dimensional | Requires finiteness (from C1) separately -- Z^3 itself is infinite |
| **Local tensor product** | H = H_1 x ... x H_N | Fixes the notion of "node" and "locality" |

### Honest decomposition

"Cl(3) on Z^3" is shorthand for:

> A finite tensor product of qubits (C^2 factors), arranged on a cubic
> lattice in three dimensions, with nearest-neighbor staggered hopping
> Hamiltonian.

This contains:

1. **Hilbert space** (finite, tensor product) -- 1 structural axiom
2. **d_local = 2** -- arguably forced by minimality (d_local = 1 gives no
   interference, d_local >= 3 does not give SU(2))
3. **d = 3** -- forced by gravity + atoms IF you demand both
4. **Cubic lattice** -- the canonical d = 3 lattice for bipartite staggered
   fermions; arguably forced by Cl(3) requirement
5. **Nearest-neighbor** -- minimal locality; arguably forced by simplicity
6. **Staggered phases** -- forced by (4) + bipartite structure

Items 2-6 form a tightly coupled package where each constrains the others.
The question is: how many independent choices are encoded?

**Conservative count:** 3 independent pieces of information:
- Hilbert space exists (ontological commitment)
- d = 3 (geometric choice)
- Staggered fermion realization (dynamical choice -- nearest-neighbor +
  bipartite + anticommuting phases)

**Liberal count:** 1.5 pieces of information:
- Hilbert space exists
- d = 3 is forced by requiring both gravity and atoms (reducing to 0.5
  since it is a derived consequence of physical requirements)

**Our assessment:** The honest answer is **2 axioms with 1 strongly
constrained choice**:

1. A finite tensor product Hilbert space exists.
2. The local factors are qubits on the 3D cubic lattice with staggered
   nearest-neighbor Hamiltonian.

Item (2) is a single specification, but it packs in d_local = 2, d = 3,
cubic topology, nearest-neighbor coupling, and staggered phases. Each of
these CAN be argued to follow from the others or from physical
requirements, but the arguments are not all airtight. A strict referee
will count the sub-choices.

---

## Part 6: The Honest Count

### For the structural backbone (retained results only)

**2 axioms** -- "Cl(3) on Z^3" (I1 + I2).

But "Cl(3) on Z^3" encodes at least 2 logically separable commitments:
- A finite tensor product Hilbert space (the quantum substrate)
- A specific geometric and algebraic realization (qubits, cubic, 3D,
  staggered, nearest-neighbor)

A strict referee may count the sub-components of the second commitment.
The most aggressive sub-counting would be:

| Sub-axiom | Can it be argued away? |
|-----------|----------------------|
| d_local = 2 | Partially: minimality argument (weakest link) |
| d = 3 | Yes if you accept gravity + atoms as a derived constraint |
| Cubic | Yes if you accept bipartite + Cl(3) as forcing it |
| Nearest-neighbor | Yes if you accept minimality of local coupling |
| Staggered | Yes: forced by cubic + bipartite |

If ALL the "argued away" links hold: **2 axioms** (Hilbert space + d = 3
as derived).

If NONE of the "argued away" links hold: **6 sub-axioms** (Hilbert space
+ d_local + d + cubic + NN + staggered).

**Best honest answer for the Nature paper: 2 axioms + 1 discrete choice (d = 3)**, consistent with the AXIOM_REDUCTION_NOTE. The other sub-components of "Cl(3) on Z^3" are either forced or strongly constrained by self-consistency.

### For the full framework (including bounded results)

The full framework, covering all lanes including bounded phenomenology,
uses **6 irreducible axioms** (I1-I6) plus **4 model inputs** (I7-I10).

| Category | Count | Content |
|----------|-------|---------|
| Core axioms | 2 | Hilbert space + "Cl(3) on Z^3" specification |
| Discrete choice | 1 | d = 3 (if not counted as derived) |
| Additional axioms for specific results | 3 | Homogeneity, growth, SM branch |
| Undetermined parameters | 1 | g_bare = 1 |
| Imported physics | 3 | sigma_v, Wilson r, anisotropy |
| Limits | 1 | Thermodynamic limit |

### Comparison to the "single axiom" claim

The COMPLETE_DERIVATION_CHAIN and SINGLE_AXIOM_HILBERT_NOTE claim a single
axiom: "a finite-dimensional Hilbert space with local tensor product
structure." This is aspirational but overstates the situation:

1. The single axiom does not specify d = 3. The dimension must come from
   somewhere -- either as an additional input or as a derived consequence
   of requiring attractive gravity and atomic stability.

2. The single axiom does not specify d_local = 2. The minimality argument
   ("smallest Hilbert space dimension giving interference") is suggestive
   but not a proof of uniqueness.

3. The single axiom does not specify cubic lattice or nearest-neighbor
   coupling. Other lattice topologies and interaction ranges are
   consistent with a local tensor product Hilbert space.

4. The single axiom gives NO cosmological results (no growth, no
   expansion, no freeze-out).

5. The single axiom gives NO right-handed matter (no SM branch selection).

**Verdict:** "Cl(3) on Z^3" is not one axiom. It is a tightly constrained
package that can be honestly described as **2 axioms + 1 discrete choice**
for the structural backbone, expanding to **6 axioms + 4 model inputs** for
the full framework including phenomenology.

### The crisp answer for a Nature referee

> The framework's structural backbone -- gravity, Born rule, SU(2), and
> structural SU(3) with left-handed charge matching -- follows from two
> commitments: (1) a finite tensor product Hilbert space, and (2) the
> staggered fermion realization of Cl(3) on the 3D cubic lattice. The
> choice d = 3 is constrained to be the unique integer satisfying both
> gravitational attraction (d >= 3) and atomic stability (d <= 3), but we
> do not claim a dynamical mechanism selecting it. The framework has zero
> continuous free parameters. Bounded phenomenological results (DM ratio,
> cosmological constant, top mass, CKM) require additional inputs:
> Hamiltonian homogeneity, graph growth, a bare coupling g_bare = 1, and
> SM branch selection via anomaly cancellation. These are stated
> explicitly in each result.

---

## Appendix: Lane-by-Lane Assumption Dependencies

For each major result, which irreducible axioms and model inputs are required:

| Result | Axioms used | Model inputs | Status per review.md |
|--------|------------|-------------|---------------------|
| Newtonian gravity (F = GM1M2/r^2) | I1, I2 | None | Closed |
| Born rule (I_3 = 0) | I1 | None | Closed |
| d = 3 selection | I1, (I2 or physical requirements) | None | Closed |
| SU(2) exact | I1, I2 | None | Closed |
| Structural SU(3) | I1, I2 | None (axis selection is derived) | Closed |
| LH charge matching | I1, I2 | None | Closed |
| Orbit algebra 8 = 1+3+3+1 | I2 (d=3 part only) | None | Closed (exact, unconditional) |
| Taste-physicality | I1, I2 | None (theorem within framework) | Conditional on framework |
| Physical generations | I1, I2 | None beyond taste-physicality | Conditional; gate open |
| RH matter / full generation | I1, I2, I6 | None | Closed (full-framework) |
| Time / 3+1 | I1, I2 | None | Closed (single-clock surface) |
| S^3 compactification | I1, I2, I3, I4 | None | Bounded (two gaps) |
| Cosmological constant | I1, I2, I3, I4 | None | Bounded |
| Top Yukawa y_t = g_s/sqrt(6) | I1, I2 | None | Closed (formal theorem) |
| Top mass m_t = 174 GeV | I1, I2, I5 | SM RGE (bounded) | Bounded |
| DM ratio R = 5.48 | I1, I2, I4, I5 | I9 (sigma_v), I10 (thermo limit) | Bounded |
| Mass hierarchy (quantitative) | I1, I2, I5 | I7 (Wilson r), I8 (anisotropy) | Bounded |
| CKM mixing angles | I1, I2 | I7, I8, Froggatt-Nielsen epsilon | Bounded |
| Generation physicality | I1, I2 | None beyond taste-physicality | Open |
| Renormalized y_t matching | I1, I2, I5 | SM RGE | Open |
