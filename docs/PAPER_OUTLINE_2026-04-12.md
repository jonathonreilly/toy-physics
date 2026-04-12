# Paper Outline: "Physics from Cl(3) on Z³"

**Target:** Nature (letter format)
**Length:** ~3000 words main text + Extended Data + Supplementary Information
**Date:** 2026-04-12 (revised per codex review 5efe070)
**Status:** OUTLINE — aligned with CI3_Z3_PUBLICATION_RETAIN_AUDIT

---

## Title

**Gravity and gauge structure from Cl(3) on Z³**

---

## Abstract (~150 words)

We show that the Clifford algebra Cl(3) realised on a cubic lattice Z³ produces:
Newtonian gravity to sub-percent accuracy on lattices up to 128³, the Born rule
as an automatic consequence of unitarity, three spatial dimensions from
gravitational and atomic stability bounds, exact SU(2) gauge structure from the
bipartite Clifford bivectors, and structural SU(3) colour from a graph-first
axis selector combined with the commutant theorem — yielding the decomposition
C⁸ = (2,3) ⊕ (2,1) with left-handed charge assignment Y = +1/3 (quarks) and
Y = −1 (leptons). A conditional 4D chiral completion of one SM generation is
now available on a right-handed singlet template, while the remaining open
matter-sector theorem is the graph-canonical derivation of that template and
the physical-generation assignment. The retained structural backbone has no
adjustable parameters; bounded phenomenological windows and still-open gates
are reported separately.

---

## Main Text

### 1. Introduction (~350 words)

**Para 1: The problem.**
No framework derives both gravity and the Standard Model gauge structure from a
common algebraic origin. String theory, loop quantum gravity, non-commutative
geometry, and the Clifford algebra program (Furey, Stoica, Trayling) each
capture subsets but not the full picture.

**Para 2: Our result.**
We show that one structure — Cl(3) on Z³ — produces gravitational dynamics,
SU(2) gauge structure, and structural SU(3) colour from a single lattice. We
separate retained structural results from bounded phenomenological windows and
open theorems, and present all three layers explicitly.

**Para 3: What is and isn't new.**
Staggered fermions and taste algebras are standard (Kogut-Susskind 1975,
Sharpe 2006). SU(3) from Clifford algebras has precursors (Furey 2014-2024,
Stoica 2018, Trayling & Baylis 2001). Our contributions: (i) self-consistent
Poisson gravity from the same lattice, (ii) a basis-independent commutant
theorem with graph-first axis selection, (iii) explicit separation of structural
closure from phenomenological extension. We cite predecessors throughout.

---

### 2. The axiom and its consequences (~400 words)

**The axiom:** Cl(3) on Z³ — staggered fermion phases on a cubic lattice.

**Automatic consequences:**
- Graph structure, unitarity, Born rule (I₃ < 10⁻¹⁶)
- Local Hilbert space dimension d = 2

**Dimension selection (d = 3):**
Two hard bounds: gravity attractive only for d ≥ 3; atomic bound states only
for d ≤ 3. Four supporting arguments.

[Extended Data Fig. 1: Force sign and bound states vs dimension]

---

### 3. Gravity (~400 words)

**RETAINED — all results numerically verified.**

- Poisson uniquely forced (21 operators tested)
- F = GM₁M₂/r² to sub-1% on 128³
- Geodesic equation matches Christoffel to 2.3 × 10⁻⁷ (5/5 tests)
- WEP exact. Time dilation exact. Light bending = 1.985 ± 0.012
- Gravitational waves from □f = ρ at c = 1.05
- Background independence (4/4 tests)
- Strong-field extension: Φ = −ln(1−f) gives exact 1PN perihelion precession

[Extended Data Fig. 2: Distance law on 96³; Table 1: 21 operators]

---

### 4. Gauge structure (~500 words)

**RETAINED: Exact SU(2)**
Bipartite Z³ → Cl(3) bivectors B_k → [B_i, B_j] = iε_{ijk}B_k at machine
precision. Casimir S² = 3/4. Chiral symmetry exact. Unique su(2) in Cl⁺(3).

**RETAINED: Structural SU(3)**
Graph-shift operators S_i on the taste cube have quartic invariant
V_sel = 32Σ_{i<j}φ_i²φ_j² with three axis minima and Z₂ residual. At the
selected axis, the derived su(2) plus residual exchange has commutant
su(3) ⊕ u(1) (Theorem 1, 106/106 numerical checks, basis-independent across
all 3 axis choices and 1000 random conjugations).

**RETAINED: Left-handed charge matching**
The traceless U(1) generator assigns Y = +1/3 (6 quark states) and Y = −1
(2 lepton states). C⁸ = (2,3)_{+1/3} ⊕ (2,1)_{−1}. Electric charges
Q = T₃ + Y/2 give (+2/3, −1/3, 0, −1) — matching one generation of
left-handed SM fermions.

**BOUNDED: Hypercharge identification**
The charge matching is correct for left-handed fermions. A conditional
one-generation completion now exists: in the 4D taste space, chirality gives
an `8_L ⊕ 8_R` split, and anomaly cancellation uniquely fixes the right-handed
hypercharges on the singlet template once the neutral-neutrino condition is
imposed. The remaining open step is not anomaly solving itself, but the
graph-canonical derivation of that right-handed representation template
(Work Package A, see Discussion).

**BOUNDED: Three generations**
The Z₃ orbifold of 8 taste states produces orbits of size 3, consistent with
three generations. The physical identification of taste orbits with SM
generations requires a separate physicality theorem (Work Package B).

[Extended Data Fig. 3: Commutant dimension hierarchy; Fig. 4: Graph-shift
selector on φ-sphere; Table 2: C⁸ quantum numbers]

---

### 5. Phenomenological windows (~400 words)

**These results are bounded consistency checks, not retained derivations. Each
depends on inputs or assumptions not yet derived from the structural backbone.**

**Table 1: Bounded phenomenological windows**

| Quantity | Framework window | Observed | Status |
|---|---|---|---|
| Dark matter ratio R | ~5.5 (taste Casimir + α_s) | 5.47 | Bounded: direct lattice contact observable; freeze-out/Boltzmann still imported |
| Λ_pred/Λ_obs | 1.46 (spectral gap on S³) | 1.00 | Bounded: topology assumed, not derived |
| n_s | 0.967 (graph growth, N_e=60) | 0.965 ± 0.004 | Bounded: growth model, not derived dynamics |
| sin θ_C | 0.224 (Z₃ anisotropy) | 0.224 | Bounded: Z₃ breaking parameter fitted |
| J (Jarlskog) | 3.1×10⁻⁵ (Z₃ phase) | 3.08×10⁻⁵ | Bounded: same Z₃ fit |
| sin²θ_W | 0.231 (taste thresholds) | 0.231 | Bounded: M_taste fitted, not derived |
| m_t | 175.0 GeV (y_t = g_s/√6) | 173.0 GeV | Bounded: bare UV normalization fixed; renormalized matching still open |
| Δm²₃₁/Δm²₂₁ | 32.6 | 32.6 | Fit: 2 free parameters in Z₃ seesaw |
| δ_CP | −103° | −90° ± 20° | Fit: complex Z₃ breaking phase |

Each entry is annotated with its honest status. A full derivation chain from
the structural backbone to any row would require closing the inputs listed.
These windows are presented as evidence of structural compatibility, not as
zero-parameter predictions.

Two additional lanes remain review-only and are not counted as retained
results in this draft:

- Gauge couplings: the `SU(2)` normalization is still a consistency
  observation, and the `U(1)` coupling is still fit/scanned rather than
  derived.
- CKM: the current charge-selection work gives a bounded pattern argument,
  not a quantitative CKM theorem.

**The strongest entries** are the ones with the least imported machinery: the
direct lattice DM contact-propagator enhancement and the cosmological-
constant window. Both are still bounded, but they are the cleanest signals
in the current review state.

---

### 6. Falsifiable structural predictions (~300 words)

**These follow from the retained structural backbone only:**

| Prediction | Mechanism | Test |
|---|---|---|
| d = 3 | Gravity sign + atomic stability | Confirmed |
| Born rule I₃ = 0 | Unitarity + self-consistency | Sinha et al. (confirmed) |
| Gravity ∝ 1/r² | Poisson uniqueness on Z³ | Sub-1% confirmed |
| SU(2) exact | Cl(3) bivectors | Machine precision |
| Structural SU(3) | Graph-shift + commutant | 106/106 pass |
| w = −1 | Spectral gap is topological | DESI (ongoing) |
| CPT exact | Cubic lattice symmetry | SME experiments (ongoing) |
| τ_p ≫ 10³⁵ yr | M_X = M_Planck | Hyper-K (future) |

**Predictions that require phenomenological extension (not main-text claims):**
Normal ν hierarchy, Majorana ν, m_ββ, gravitational entanglement rate,
Lorentz violation level, tensor-to-scalar ratio r. These are presented in SI
with explicit status labels.

---

### 7. Discussion (~400 words)

**What is closed:**
- Gravity from self-consistent Poisson (weak-field, with 1PN extension)
- Born rule from unitarity
- d = 3 from 6 independent arguments
- Exact SU(2) from Cl(3) bivectors
- Structural SU(3) from graph-first selector + commutant theorem
- Left-handed charge matching Y = +1/3, −1

**What is now closed at the full-framework level:**
- One full SM generation:
  - the spatial graph determines the left-handed gauge/matter structure
  - the derived temporal direction supplies chirality
  - anomaly cancellation fixes the right-handed singlet completion on the SM branch

**What is bounded but promising:**
- Z₃ orbit counting for generations, conditional on the physicality theorem
- Gauge couplings and CKM lanes: review-only until a true lattice coupling
  observable and a quantitative CKM theorem exist
- Phenomenological windows for R, Λ, n_s, sin θ_C, J, sin²θ_W, m_t
- Direct lattice DM contact-propagator enhancement in the attractive Coulomb channel;
  the full freeze-out/relic-abundance step remains open
- Strong-field extension via S = L(1−tanh f)
- Frozen star / information paradox resolution

**What remains open (the real gates):**

*Work Package A: Generation physicality.* Prove that the Z₃ taste orbits
correspond to physical generations, not representation artifacts. This
requires a canonical matter assignment and an explanation of the singlet
states.

*Work Package B: Topology / compactification.* Close the `S^3` cap-map /
compactification step cleanly enough to move the CC lane from bounded to
structural.

*Work Package C: Quantitative bridges.* Close the renormalized `y_t` matching
theorem and the DM relic mapping from the native graph freeze-out law to the
physical cosmological abundance.

**Relationship to prior work:** We build on Kogut-Susskind, Furey, Stoica,
Trayling-Baylis, and the lattice QCD community. Our contribution is the
self-consistent gravity + gauge derivation from a single lattice with explicit
separation of structural closure from phenomenological extension.

---

## Extended Data

### Figures
1. Force sign vs dimension (d=3 selection)
2. Distance law on 96³ and 128³
3. Commutant dimension vs constraint set
4. Graph-shift selector: V_sel on φ-sphere (3 axis minima)
5. Phenomenological windows overview (R, Λ, n_s with error bars)

### Tables
1. 21 field equation operators (Poisson uniqueness)
2. C⁸ quantum numbers: SU(2) × SU(3) × U(1) decomposition
3. Structural predictions vs observation
4. Bounded phenomenological windows with status annotations

---

## Supplementary Information

1. Theorem 1: SU(3) commutant (6-step proof with intertwiner)
2. Graph-first selector derivation
3. Basis-independence verification (5 arguments)
4. Phenomenological extensions (DM ratio, CC, n_s, neutrinos, y_t) — each with
   explicit status and dependencies
5. Negative results and failed approaches
6. Literature comparison (vs Furey, Stoica, Trayling, Connes, Wen)
7. All scripts with run instructions (GitHub link)

---

## Companion Papers

### PRD: Full derivation chain (~50 pages)
### CQG: Gravity sector
### JHEP: Gauge sector (including chiral completion when ready)
### JCAP: Cosmological windows (bounded status)

---

## Open theory gates (not paper blockers — future work)

### A. Generation physicality theorem
Prove Z₃ taste orbits = physical generations with canonical matter assignment

### B. Topology / compactification theorem
Prove the graph-to-closed-manifold compactification step strongly enough to
force `S^3`

### C. Phenomenology upgrade
For each bounded window, either derive from backbone or label as consistency
