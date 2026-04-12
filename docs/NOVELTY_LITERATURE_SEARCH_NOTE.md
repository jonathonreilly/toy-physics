# Novelty Literature Search: What Is Known vs New

**Date:** 2026-04-12
**Purpose:** Honest assessment of whether three specific claims from our framework
are genuinely novel or already established in the literature.

---

## Question 1: SU(3) from the Cl(3) Taste Algebra Triplet Subspace

**Our claim:** In d=3, the 8-dimensional taste space decomposes as 8 = 3 + 3* + 1 + 1
under total spin. Projecting Cl(3) onto the triplet subspace yields exact su(3)
generators (all 8 Gell-Mann matrices).

### What IS known

**The general idea of deriving SU(3) from Clifford algebras is well-trodden ground:**

1. **Trayling & Baylis (2001)** -- "A geometric basis for the standard-model gauge group,"
   J. Phys. A. They derive the full SM gauge group SU(3)_C x SU(2)_L x U(1)_Y from
   Cl(7), identifying SU(3)_C with "interior" right-sided rotations. Follow-up:
   "The Cl_7 approach to the Standard Model" (2004).

2. **Stoica (2018)** -- "The Standard Model Algebra -- Leptons, Quarks, and Gauge from
   the Complex Clifford Algebra Cl_6," Adv. Appl. Clifford Algebras 28, 52. Shows
   that C-ell_6 contains automatically the leptons, quarks, and electroweak + color
   gauge symmetries of one generation.

3. **Furey (2014-2024)** -- Series of papers deriving SM structure from division algebras.
   Key results: SU(3)_C x U(1)_em from complex octonions (which generate Cl(6)),
   and three generations from Cl(8)/sedenions with S_3 automorphism symmetry.
   Most recent: "Algebraic realisation of three fermion generations with S_3 family
   and unbroken gauge symmetry from Cl(8)" (Eur. Phys. J. C, 2024).

4. **Shirokov (2025)** -- "On SU(3) in Ternary Clifford Algebra," presented at CGI 2024.
   Gives explicit su(3) generators in ternary Clifford algebra with explicit connection
   to Gell-Mann basis.

5. **Lasenby (2024)** -- "Some recent results for SU(3) and octonions within the
   geometric algebra approach to the fundamental forces of nature," Math. Methods
   Appl. Sci.

**The taste symmetry of staggered fermions is also well-established:**

- In d=4 spacetime, the taste group is SU(4). In the free theory on the lattice,
  the internal symmetry is U(2^(D/2)) x U(2^(D/2)).
- The spin-taste structure is encoded via the Clifford algebra SO(2D).
- Adams (2004, hep-lat/0411037) reformulated the Dirac operator using SO(2D) Clifford
  algebra to clarify symmetries in arbitrary dimension.
- Recent work (2411.07780, 2604.02078) studies taste symmetry properties in various
  dimensions, noting that when spatial dimension is odd, conserved charges generate
  chiral flavor symmetries in the continuum limit.

### What appears to be NEW in our claim

The specific combination: (a) working in d=3 spatial dimensions (not the standard d=4),
(b) decomposing the 2^3 = 8 taste doublers under total spin into 3 + 3* + 1 + 1, and
(c) showing that projecting Cl(3) onto the triplet gives all 8 Gell-Mann matrices --
this specific chain does not appear in the literature we found.

**However, the novelty is incremental, not revolutionary.** The Furey/Stoica/Trayling
line of work has already shown that SU(3) lives inside various Clifford algebras.
Our contribution would be connecting this to the taste algebra interpretation in d=3
specifically, which is a new angle but builds on extensive prior art.

**Honest assessment: PARTIALLY NOVEL.** The algebraic fact (SU(3) from Clifford algebra)
is known. The specific taste-decomposition route in d=3 appears new. The connection to
staggered fermion physics in d=3 adds a lattice-QCD interpretation that the pure-algebra
papers lack, but anyone familiar with both literatures could derive it.

**Risk level:** Medium. A referee familiar with Furey's work might say "this is a
special case of known Clifford-to-gauge-group constructions."

---

## Question 2: Self-Consistent Poisson Iteration

**Our claim:** The technique of iterating (propagate wavepacket -> compute density ->
solve Poisson -> use field in next propagation -> iterate to convergence) applied to
test WHICH field equations (Poisson vs biharmonic vs non-local) give self-consistent
attractive gravity.

### What IS known

**The Schrodinger-Poisson / Schrodinger-Newton equation is well-established:**

1. **Schrodinger-Newton equation** (Diosi 1984, Penrose 1996) -- Nonlinear modification
   of Schrodinger equation with Newtonian gravitational self-interaction. The gravitational
   potential emerges from treating |psi|^2 as mass density. Well-studied since the 1990s.

2. **Self-consistent numerical methods** -- The self-consistent Crank-Nicolson method and
   related iterative schemes are standard tools. Giulini & Grossardt demonstrated
   gravitational self-localization numerically. "Patterns of Gravitational Cooling in
   Schrodinger Newton System" (2018, arXiv:1811.09694).

3. **Semiconductor Schrodinger-Poisson solvers** -- Fully mature engineering tools
   (e.g., Aestimo 1D, QCAD). The iterate-to-self-consistency approach is textbook
   material in semiconductor device simulation.

4. **Fully self-consistent semiclassical gravity** -- Recent work (Phys. Rev. D) has
   put forward fully self-consistent frameworks, addressing longstanding questions
   about whether semiclassical gravity is internally consistent.

5. **Astrophysical self-consistent field methods** -- Hernquist & Ostriker (1992,
   ApJ 386, 375) developed SCF methods for galactic dynamics: solve Poisson, compute
   orbits, revise potential, iterate.

### What appears to be NEW in our claim

Using the self-consistent iteration as a **discrimination tool** between competing
field equations (Poisson vs biharmonic vs non-local kernel) appears to be a novel
application. The existing literature takes Poisson/Newton as given and solves for
dynamics. We instead ask: "which field equation is self-consistent?" and use the
iteration as a selection principle.

**Honest assessment: THE APPLICATION IS NOVEL, the technique is not.** The
Schrodinger-Poisson self-consistent iteration is textbook. Using it as a discriminator
between candidate field equations is a new idea. This is a genuine methodological
contribution, though modest in scope.

**Risk level:** Low. This is clearly a new application of a known method. The novelty
claim is defensible as long as we cite the Schrodinger-Newton/Poisson literature
properly and frame our contribution as the discrimination application.

---

## Question 3: Fermion Generations from Z_3 Orbifold of Taste Doublers

**Our claim:** The number of fermion generations (3) arises from the Z_3 cyclic
permutation symmetry of d=3 spatial dimensions acting on the 2^3 = 8 taste doublers,
giving size-3 orbits that are natural triplets.

### What IS known

**The "why three generations?" question is a major open problem:**

1. **No consensus exists.** Wikipedia's article on generations in particle physics
   states plainly that the origin of exactly three generations is unexplained.

2. **Spatial dimensions = generations speculation** -- The coincidence that there are
   3 spatial dimensions and 3 fermion generations has been noted many times, but
   as Big Think (Siegel) notes, this "doesn't provide any obvious connections
   between the two."

3. **Kaplan & Sun (2012)** -- "Spacetime as a Topological Insulator: Mechanism for
   the Origin of the Fermion Generations," Phys. Rev. Lett. 108, 181807. Three
   generations arise as surface modes in a 5D theory via nonlinear fermion
   dispersion, analogous to topological insulator edge states. Uses domain wall
   fermion techniques from lattice gauge theory. This is the closest prior work
   conceptually -- it links lattice fermion physics to generation count.

4. **Furey & Gourlay (2024)** -- "Algebraic realisation of three fermion generations
   with S_3 family and unbroken gauge symmetry from Cl(8)." Three generations from
   S_3 automorphism of sedenion algebra. The S_3 here is the permutation group of
   3 objects, acting on algebraic structure -- but it is S_3 acting on the Cayley-
   Dickson construction, NOT on spatial dimensions.

5. **String theory orbifolds** -- Z_3 orbifolds of heterotic strings (e.g., SO(32))
   and Z_2 x Z_2 orbifolds of 6D tori both produce three-generation models. The
   Z_2 x Z_2 case relates family triplication to three twisted sectors. Fermion
   generations from extra-dimensional orbifold projection is a standard mechanism
   (Nucl. Phys. B, 2003).

6. **Furey (2014)** -- "Generations: Three Prints, in Colour," JHEP. Shows 48 states
   from complex octonions decompose as three generations under su(3) + u(1).

7. **Physics Forums discussion (2025)** -- Direct question asking whether fermion
   doubling connects to three generations. No definitive answer; the connection
   remains speculative.

### What appears to be NEW in our claim

The specific mechanism -- Z_3 cyclic permutation of the 3 spatial dimensions acting
on the 2^3 = 8 taste doublers of staggered fermions to produce size-3 orbits --
appears to be genuinely new. Key distinctions from prior work:

- **vs. Furey:** She uses S_3 on Cayley-Dickson algebraic structure, not on spatial
  dimensions acting on taste doublers.
- **vs. Kaplan & Sun:** They use topological insulator physics in 5D, not taste
  doubling in 3D.
- **vs. String orbifolds:** Those use Z_3 on compactified extra dimensions, not on
  the 3 visible spatial dimensions acting on lattice doublers.
- **vs. "3 dimensions = 3 generations" folklore:** We provide an actual mechanism
  (Z_3 orbits on taste space), not just a numerological coincidence.

**Honest assessment: APPEARS GENUINELY NOVEL.** The specific mechanism connecting
Z_3 spatial permutation -> taste doubler orbits -> three generations has not been
proposed before, as far as this search can determine. This is the most novel of
the three claims.

**Caveats:**
- The idea is speculative and would need to survive scrutiny about whether the
  Z_3 orbits actually produce the correct quantum numbers.
- The connection between d=3 and 8 taste doublers is only valid if one works in
  d=3 spatial dimensions, which is non-standard for QCD (normally d=4 spacetime).
- A referee might ask why Z_3 and not the full S_3, and whether the remaining
  orbits (size-1 and size-2 under Z_3 subgroups) have physical interpretation.

**Risk level:** Low for novelty claims, high for correctness/completeness. This
is new territory but needs careful development.

---

## Bonus: Overall Framework Novelty

**Our framework:** Deriving Standard Model gauge groups + gravity + generations from
a single discrete lattice/graph structure.

### Related programs in the literature

1. **Connes' Noncommutative Geometry (1996-present)** -- The most developed program
   for deriving the SM from a geometric structure. Uses spectral triples; spacetime
   is a product of 4D continuum with a finite discrete space F of KO-dimension 6.
   The spectral action principle yields SM + gravity. This is the gold standard
   for "SM from geometry" programs.

2. **Furey/Stoica/Trayling Clifford algebra program** -- Derives SM gauge groups
   from Clifford algebras (Cl_6, Cl_7, Cl_8). Does not include gravity. Does not
   use lattice/graph structures.

3. **Wen's emergent gauge symmetry (2003-present)** -- String-net condensation
   produces emergent gauge symmetries from lattice models. Produces U(1) and
   SU(N) gauge theories from entangled qubits. Published in PRL, widely cited.
   Most relevant for "gauge from discrete structure" claims.

4. **Graviton emergence from qubit lattice** -- Wen (2012, Nucl. Phys. B) constructed
   quantum qubit models on 3D lattices where gapless helicity +/-2 modes (gravitons)
   emerge as low-energy excitations, with emergent linearized diffeomorphism
   gauge symmetry.

5. **Lattice gauge theory** -- The standard framework puts gauge fields on lattice
   links as group elements. But this is a computational technique, not a claim
   that the lattice is fundamental.

6. **Combinatorial quantum gravity** -- Trugenberger (2023, arXiv:2311.17526) and
   related work on emergent 3D quantum behavior from combinatorial structures.

### Assessment of overall framework

**Our framework is novel in its specific combination** but each individual ingredient
has precursors:
- SU(3) from Clifford algebra: known (Furey, Stoica, Trayling)
- Gravity from lattice qubits: known (Wen)
- Generations from algebraic structure: known (Furey, Kaplan)
- SM from spectral geometry: known (Connes)

**What would be genuinely new** is getting ALL of these from a SINGLE structure
(the grown graph + staggered fermion taste algebra). No existing program achieves
this unification from one discrete starting point:
- Connes needs continuous geometry + discrete internal space (two ingredients)
- Furey gets gauge groups but not gravity
- Wen gets gauge fields but not SM specifically
- String theory gets everything but from a much larger structure

**The overall framework, if it works, would be a genuine advance in unification.**
But the "if it works" is doing a lot of heavy lifting. Each piece needs to be
demonstrated rigorously, and the connections between pieces need to be shown to
be necessary rather than coincidental.

---

## Summary Table

| Claim | Known? | Our novelty | Risk |
|-------|--------|-------------|------|
| SU(3) from Cl(3) taste triplet | Partially | Taste-decomposition route in d=3 | Medium |
| Self-consistent Poisson as discriminator | Method known, application new | Using SCF to select field equations | Low |
| Generations from Z_3 taste orbifold | Genuinely new mechanism | Specific Z_3 spatial -> taste -> 3 families | Low (novelty), High (rigor) |
| Overall unified framework | Novel combination | All from one discrete structure | Medium |

## Recommendations for the Paper

1. **Cite extensively:** Furey, Stoica, Trayling, Connes, Wen, Kaplan & Sun, and the
   Schrodinger-Newton literature. Not citing these would be a fatal error.

2. **Frame contributions carefully:**
   - Q1: "We show that the known Clifford-to-SU(3) correspondence has a natural
     interpretation in terms of staggered fermion taste symmetry in d=3."
   - Q2: "We apply the well-known Schrodinger-Poisson self-consistent technique
     as a novel discriminator between candidate gravitational field equations."
   - Q3: "We propose a new mechanism connecting fermion generations to the Z_3
     cyclic permutation symmetry of spatial dimensions acting on taste doublers."

3. **Be honest about what is incremental vs. what is new.** Overselling kills
   credibility. The generation mechanism (Q3) is the strongest novelty claim.

4. **Acknowledge the "why d=3?" question.** Our framework assumes d=3 spatial
   dimensions. We should address why the taste decomposition in d=3 (rather than
   d=4 spacetime) is physically motivated.

---

## Key References

- Trayling & Baylis, J. Phys. A (2001), hep-th/0103137
- Stoica, Adv. Appl. Clifford Algebras 28, 52 (2018), arXiv:1702.04336
- Furey, JHEP (2014), arXiv:1405.4601
- Furey & Gourlay, Eur. Phys. J. C (2024)
- Shirokov, CGI 2024 proceedings (2025)
- Kaplan & Sun, Phys. Rev. Lett. 108, 181807 (2012), arXiv:1112.0302
- Connes & Chamseddine, spectral action (1997, 2006)
- Wen, Nucl. Phys. B (2012), emergent gravitons from qubits
- Adams, hep-lat/0411037 (2004), staggered fermion symmetries in arbitrary dimension
- Diosi (1984) / Penrose (1996), Schrodinger-Newton equation
