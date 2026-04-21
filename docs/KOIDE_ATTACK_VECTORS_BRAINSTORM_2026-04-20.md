# Koide I1 / I2-P Creative Attack Vectors Brainstorm

**Date:** 2026-04-20 (evening)
**Status:** Brainstorm — new attack vectors to go after I1 (native Cl(3)/Z³
forcing law for Koide cone) and I2/P (physical-base radian bridge for δ = 2/9).
**Context:** Six converging paths to 2/3 and 2/9 via qubit-lattice-dim +
anomaly + SELECTOR² are reviewer-facing conditional support. Need a
genuine native forcing law. Every assumption is on the table.

---

## Assumptions to question

### For I1 (Koide Q = 2/3)

| # | Assumption | Why might be wrong |
|---|---|---|
| A1 | Q is defined on the circulant `aI + bC + b̄C²` via `Σλ²/(Σλ)²` | Maybe Q is primarily a TENSOR-PRODUCT ratio, not a circulant trace ratio |
| A2 | κ = 2 is the unique selector | Maybe κ = 2 is shorthand for a deeper SELECTION RULE |
| A3 | H_sel(m) parametrizes a 1-dim line of physical points | Maybe the physical "point" is a 2-dim surface or a specific topological class |
| A4 | Observable principle = `log|det|` | Maybe the retained observable is NON-POLYNOMIAL |
| A5 | The relevant operator is 3×3 on hw=1 | Maybe it's 4×4, 8×8, or INFINITE-dim |
| A6 | Q emerges from operator-side only | Maybe Q is a FLOW fixed-point, not a stationary-action selector |
| A7 | MRU / Frobenius equipartition is THE extremum principle | Maybe a DIFFERENT entropy / functional forces κ = 2 |
| A8 | The cone condition is quadratic in amplitudes | Maybe it's CUBIC via an anomaly-like structure |

### For I2/P (Brannen δ = 2/9)

| # | Assumption | Why might be wrong |
|---|---|---|
| B1 | δ is fundamentally in RADIANS | Maybe the cosine parametrization is a DISGUISED dimensionless form |
| B2 | δ = 2/9 is a BARE rational that needs a radian bridge | Maybe it IS `rational × π` in natural units: `2/9 = (π · 2)/(9π)` |
| B3 | Berry on CP¹ projective doublet ray is THE topological carrier | Maybe a DIFFERENT base (4-torus, S³, Klein quartic) is the right carrier |
| B4 | "Every retained radian is (rational) × π" | This rules out 4 specific mechanisms, but is it an exhaustive no-go? |
| B5 | The first-branch physical m_* is a SINGLE POINT | Maybe m_* is a TOPOLOGICAL INVARIANT (winding number) |
| B6 | δ = Q/d from Zenczykowski is a DEPENDENT chain | Maybe δ is INDEPENDENT and Q = d·δ is the derived side |
| B7 | δ lives on the "physical Koide locus" (interval) | Maybe δ lives on the UNIVERSAL COVER (circle) of that interval |
| B8 | δ and Q are dimensionless | Maybe they carry hidden units from Cl(3) scaling |

---

## Attack Vector 1: Gradient flow on `Herm_circ(3)`

**Concept:** Not a stationary-action selector (which MRU is) but a GRADIENT FLOW whose unique attractor is Koide cone.

**Concrete candidate:** Consider the flow on Herm_circ(3) parametrized by
`(a, |b|)`:

```text
da/dτ   = -∂V/∂a,      d|b|/dτ = -∂V/∂|b|,
V(a, |b|) = F(a, |b|; Cl(3)/Z³ data)
```

where `F` is a Cl(3)/Z³-native potential (not log-det, not Frobenius
log). Candidates for F:

- **Ricci-flow analog:** use the "curvature" of the circulant moduli as a
  3-manifold with metric `diag(3, 6, 6)`. Ricci flow → Einstein metric
  which might sit at κ = 2.
- **Yamabe-flow analog:** fixed scalar curvature on the moduli.
- **Entropy-gradient flow:** Fisher-information or relative-entropy
  gradient. The Fisher metric on the Koide manifold is typically
  NON-Frobenius and might select κ = 2 uniquely.

**What would close I1:** show the retained Cl(3)/Z³ dynamics (e.g.,
from the observable principle integrated against a Cl(3) Haar measure)
induces a gradient flow whose asymptotic attractor is the Koide cone.

### Why this might work

- Gradient flows have UNIQUE attractors (under mild conditions).
- The Koide cone Q = 2/3 is a codim-1 submanifold; if it's an ATTRACTOR,
  that's a native forcing.
- All six no-gos ruled out STATIC selectors; a DYNAMIC flow is
  structurally different.

### Why this might fail

- Need to identify the CANONICAL flow generator from retained Cl(3)/Z³
  content (not just invent one).
- The flow might have multiple attractors, not just Koide.

---

## Attack Vector 2: Three-qubit tensor product irrep count

**Concept:** `(C²)^⊗3` under diagonal SU(2) decomposes as
`spin-3/2 ⊕ 2·(spin-1/2)`. The count ratio
`#(spin-1/2 irrep copies) / #(total irrep copies) = 2/3 = Q`.

**Retained content needed:**

- Three sites, each carrying a Cl(3) spinor (qubit) — NATURAL from
  Cl(3)/Z³ with 3 physical sites.
- Diagonal SU(2) action (the retained Spin(3) = SU(2) group action on
  Cl(3) spinor, pulled back to all three sites simultaneously).

**Decomposition:**

```text
(C²)^⊗3 = (spin-3/2, 4-dim, trivial S_3)
         ⊕ (spin-1/2, 2-dim, standard S_3)
         ⊕ (spin-1/2, 2-dim, standard S_3)

Irrep copy count: 1 + 1 + 1 = 3 total sectors
                  ^-- spin-3/2 | spin-1/2 × 2

Q_irrep := |{spin-1/2 copies}| / |{total copies}| = 2/3.
```

### What would close I1

**Claim:** the Koide charged-lepton ratio Q is the irrep-count ratio
`Q = 2/3` in the retained 3-qubit tensor product, because:

1. Charged leptons are AT HW=1 (one excitation out of three sites).
2. HW=1 states span the "mixed-symmetry" spin-1/2 sector of `(C²)^⊗3`.
3. The Koide amplitude triple (√m_e, √m_μ, √m_τ) is the component of the
   retained lattice wavefunction in this spin-1/2 sector.
4. Σm / (Σ√m)² for the spin-1/2 subspace evaluates to 2/3 by combinatorics
   of S_3 mixed symmetry.

**The bridge** "irrep count = Koide Q" is a clean combinatorial statement
(no SO(2) postulate, no MRU log-law, no tracelessness — just dimension
counting in the tensor product).

### Proof sketch

Consider the 3-qubit Hilbert space `H = (C²)^⊗3`. Under `SU(2)_diag × S_3`:

```text
H = (spin-3/2 ⊗ triv_S3) ⊕ (spin-1/2 ⊗ std_S3).
```

For a specific "Koide-like" observable `O` on H that respects both
structures (e.g., the total magnetic moment operator), the Koide ratio
of eigenvalues on each sector is determined by irrep counting.

**Anticipated result:** Q(charged-lepton sector) = 2/3 by combinatorics.

### Why this is structurally different from qubit-lattice-dim

- Qubit-lattice-dim: `2 = dim(spinor)`, `3 = dim(lattice)`, ratio 2/3.
- 3-qubit tensor: `2 = #(spin-1/2 copies)`, `3 = #(total irrep copies)`,
  ratio 2/3.

These are the SAME 2/3 numerically but arise from DIFFERENT counting.
If both arise at d = 3 uniquely, Koide is DOUBLY structurally forced.

---

## Attack Vector 3: Stereographic re-parametrization kills the radian problem

**Concept:** The Brannen formula `√m_k = A(1 + √2 cos(δ + 2πk/3))` uses
δ in the cosine argument → radians. But if we change variables to
stereographic coordinates σ = tan(δ/2), the Brannen formula becomes:

```text
cos(δ) = (1 - σ²)/(1 + σ²),  sin(δ) = 2σ/(1 + σ²).
```

At δ = 2/9: σ = tan(1/9) ≈ 0.1116 (not obviously clean).

BUT: what if the RIGHT reparametrization is different? Candidates:

**(a) Projective:** `ζ = e^{iδ}` on the unit circle. At δ = 2/9:
`ζ = cos(2/9) + i sin(2/9)` (transcendental).

**(b) Rational stereographic with radius R:** `σ_R = R tan(δ/2)`. Pick
R = 2π/3 (Z_3 unit): `σ = (2π/3) tan(1/9)`. Still transcendental.

**(c) Pseudoscalar rotor:** `ψ = e^{I·δ/2}` where `I = γ_1 γ_2 γ_3` is
the Cl(3) pseudoscalar. `I² = -1`, so `e^{I·δ/2}` is a Cl(3) rotor of
angle δ/2. The specific value δ = 2/9 gives `e^{I/9}` — a Cl(3)-native
object.

### What would close I2/P

If the "correct" statement of δ is `ψ = e^{I·δ/2}` with δ in NATURAL CL(3)
ROTOR UNITS (where the pseudoscalar I is the angle generator), then
δ = 2/9 is a dimensionless rotor parameter, NOT a radian.

**Radian-bridge no-go defeated by assumption B1:** δ wasn't a radian in
the first place — it was a Cl(3) rotor parameter. The "2/9" is naturally
in pseudoscalar units.

### Concrete check

Verify: does the Brannen form `A(1 + √2 cos(δ + 2πk/3))` arise naturally
from a Cl(3) rotor `ψ_k = e^{I(δ + 2πk/3)/2}` applied to some reference
state? If yes, then δ is a ROTOR parameter, not a radian, and the no-go
doesn't apply.

---

## Attack Vector 4: Universal cover of Koide arcs → closed loop

**Concept:** The bundle-obstruction theorem says the physical base is
an interval (3 positive arcs on the unit circle). No closed-loop Berry
quantization on an interval.

BUT: three positive arcs under Z_3 cyclic action → lift to a
FUNDAMENTAL DOMAIN of the universal cover. The universal cover of the
Koide locus IS a closed circle.

On this closed circle, Berry phases ARE quantized (closed-loop integrals).

### What would close I2/P

Show:

1. The universal cover of the Koide positive chamber is `S¹`.
2. The retained Berry connection lifts to a U(1) bundle on `S¹` with a
   specific Chern class.
3. The Z_3 deck transformations of the cover act by `θ → θ + 2π/3`.
4. The BRANNEN δ is the `ONE-DOMAIN` integrated Berry phase MOD the
   deck transformation period.
5. Chern-class quantization forces `δ = Q/d` in radians.

### Why this might work

- Universal cover turns an interval into a circle → enables closed-loop
  holonomy quantization.
- The "rational × π" obstruction of the no-go note comes from closed
  loops on CP¹; on the universal cover, the Chern class is different.
- Specifically: the Chern number on the Z_3-reduced cover could be a
  FRACTIONAL Chern number in units that differ from π.

### Key step to prove

**Lemma:** On the Z_3 universal cover of the Koide positive locus, the
retained Berry U(1) bundle has first Chern class `c_1 = Q` (dimensionless),
integrated against the Z_3 action gives Chern-Simons level `Q/d`, which
equals δ in the natural "per-element" radian unit.

---

## Attack Vector 5: The Lepton-Baryon asymmetry angle

**Concept:** The SM has `B − L` conserved and `B + L` violated by
electroweak sphaleron anomaly. The sphaleron generates a phase
associated with the Chern-Simons level of the SU(2)_L gauge bundle.

**Sphaleron angle:** `θ_sphaleron = N_CS · 2π/N_gen` where `N_CS` is the
Chern-Simons level, `N_gen = 3` (generations).

At `N_CS = 1/d = 1/3`: `θ_sphaleron = 2π/(3·3) = 2π/9`.

**Hmm** — `2π/9 ≈ 0.698 rad`, not `2/9 ≈ 0.222 rad`. Different by factor
of π.

But the ratio `θ_sphaleron / (2π) = 1/9` matches `δ/(2π) = 1/(9π)`. Not
same.

**Alternative:** `θ_sphaleron` in a FRACTIONAL sphaleron event.
Consider `θ_sphaleron = N_CS · 2` (in units of π/3 per N_CS=1):
`θ = 2 · (1/9) = 2/9` in "per-generation-squared" units.

This is speculative but the number 2/9 naturally appears in sphaleron
charge distribution across 3 generations.

### What would close I2/P

Identify `δ_Brannen` with a SPHALERON-like fractional Chern-Simons level
that comes from the retained SU(2)_L × U(1)_Y anomaly on Cl(3)/Z³.
Since anomaly cancellation forces specific hypercharges, it might also
force a specific sphaleron angle.

---

## Attack Vector 6: CM point of elliptic curve

**Concept:** The elliptic curve `y² = x³ + 1` has complex multiplication
(CM) by `Z[ω]` where `ω = e^{2πi/3}`. Its period ratio `τ = e^{2πi/3}` is
a CM POINT of the modular `j`-function, and `j(ω) = 0`.

**Koide structure correspondence:**

- Z_3 cyclic group on Koide triplet ↔ CM action on elliptic curve.
- Circulant Hermitian on Z_3 triplet ↔ Hecke operator on CM elliptic
  curve.
- Koide cone ↔ modular fixed-point condition.

**Specific numerical conjecture:** The Koide Q = 2/3 corresponds to a
natural "modular weight" ratio at the CM point:

```text
weight(modular form of weight 2 on Γ(3)) / weight(level 3) = 2/3.
```

If this checks out, Koide is a MODULAR FORM IDENTITY, not an operator-
algebra identity.

### Why this might work

- Modular forms on `Γ_0(3)` are well-studied; the j-function restricted
  to CM points gives specific rationals.
- The Z_3 CM structure is EXACTLY the Cl(3)/Z³ action when interpreted
  geometrically.
- Modular identities often have both a representation-theoretic and a
  geometric face.

### What would close I1 AND I2/P simultaneously

Show: the Koide ratio Q and Brannen phase δ are BOTH evaluations of a
specific modular form at the CM point `τ = e^{2πi/3}`.

- Q = `f(τ=ω)/g(τ=ω)` for specific modular forms f, g.
- δ = arg of an Eisenstein series at the CM point.

---

## Attack Vector 7: Pseudoscalar rotor quantization

**Concept:** In Cl(3), the pseudoscalar `I = γ_1 γ_2 γ_3` satisfies
`I² = -1` and COMMUTES with all even-grade elements. So `I` acts like
an imaginary unit specifically for the even subalgebra `Cl⁺(3) ≅ ℍ`
(quaternions).

**Rotor angle in Cl(3):** any rotation is `R = e^{Iφ/2}` for some
bivector-pseudoscalar combination. The pseudoscalar-rotor angle is
intrinsically defined modulo `4π` (spinor periodicity).

**Claim:** The Brannen phase δ is the pseudoscalar-rotor angle of a
specific retained Cl(3) operation on the charged-lepton hw=1 triplet.

### What would close I2/P

If δ = (pseudoscalar-rotor parameter of a retained Cl(3) operation), then
δ has NATURAL CL(3) UNITS, not radians. The no-go's "rational × π" rule
applies to radians, not to pseudoscalar rotor parameters.

**Concrete target:** Identify the retained Cl(3) rotor whose parameter
is 2/9 on the selected line.

Candidate: the "generation shifter" rotor `R = e^{I·(δ/2)}` that maps the
first-generation state to the second-generation state on the selected
line. Its angle parameter should be derivable from the retained Z_3
action structure.

---

## Attack Vector 8: Graph Green's function resonance

**Concept:** On the Z³ lattice graph (3 sites in a cycle), the Green's
function `G(z) = (z·I - Δ)^{-1}` has poles at the graph Laplacian
eigenvalues.

**Z_3 Laplacian:** `Δ = I - (C + C²)/2` has eigenvalues `0, 3/2, 3/2`
(singlet at 0, doublet degenerate at 3/2).

**Retained Green's function:** `G(z) = 1/(z) · P_+ + 1/(z - 3/2) · P_d`
where P_d is the doublet projector.

**Conjecture:** The Koide Q and Brannen δ are RESIDUES of G at specific
z-values tied to Cl(3) structure:

```text
Res(G, z=0) · Res(G, z=3/2) / Tr(G^2 at physical z_*) = 2/3 or similar.
```

### What would close I1

If the retained lattice Green's function has a specific residue identity
that forces Q = 2/3 as a function of Cl(3)/Z³ graph structure, we have
a direct forcing law.

### Why this might work

Graph theory gives EXACT residue identities. The Cl(3)/Z³ graph has
specific spectral structure (eigenvalues 0, 3/2 with multiplicities 1,
2). Any natural physical quantity derived from this graph spectrum
should be a rational function of these eigenvalues.

Q = 2/3 = 1 - 1/3 = 1 - 1/d is natural on a d-cycle graph.

δ = 2/9 = 2/d² = 1/d · 2/d = (eigenvalue ratio 1/d) × (doublet multiplicity 2/d)
  = specific residue combination.

**Target identity:** Koide = (multiplicity of doublet eigenvalue) · (inverse of
spectral gap) / (dim of lattice) at the unique "physical" residue point.

---

## Attack Vector 9: Entropy maximization with CONSTRAINED normalization

**Concept:** The MRU log-extremum was demoted because SO(2) invariance
(I6) is not retained. But a DIFFERENT entropy extremum might force
κ = 2 without SO(2).

**Candidate entropies on Herm_circ(3):**

- **Shannon entropy of eigenvalue distribution.** Maximum at uniform →
  Q = 1/d. Not Koide.
- **Rényi-2 entropy:** `-log Σ p_k²`. Extremum at Q = 2/3? Let me check.
- **Bregman divergence from a reference.** If the reference is the
  retained A-select point, the divergence-minimum might be the Koide
  point.
- **Relative entropy `D(p||q)` between two distributions.** If q is the
  uniform-3 distribution and p is parametrized by κ, the minimum of
  `D(p||q)` subject to fixed `Σp_k² = 2/3` fixes κ = 2.

### What would close I1

Identify a Cl(3)/Z³-NATIVE entropy or divergence functional whose
extremum is Q = 2/3 WITHOUT the SO(2) postulate.

### Specific candidate: Wehrl entropy

The Wehrl entropy on spin-1/2 coherent states is `S_Wehrl = 1 + log π`.
For spin-1, `S_Wehrl = 2 + log(4π/3) = 2 - (2/3) log(3/(4π)) · ...`.
The number 2/3 appears naturally in Wehrl entropy of spin-1.

If Koide Q is a Wehrl-entropy ratio on the retained spin-1/2 × spin-1
structure of Cl(3), it's forced by coherent-state geometry.

---

## Attack Vector 10: Chern-Simons level matching on topological boundary

**Concept:** 3d Chern-Simons at level k has ground-state degeneracy =
k+1 on torus. For k=2, GSD = 3 → matches 3 generations.

**CS level = 2 on Z_3 gauge theory:** gives level-2 affine SU(3) at the
boundary. Its characters include specific rationals related to 2/3.

### What would close I1

If the retained framework has a hidden 3d Chern-Simons TQFT whose
boundary is the SM at the Cl(3)/Z³ scale, the CS level-2 structure
could force Koide Q = 2/3 as the UNIQUE ground state ratio on the
Z_3-valued Wilson lines.

### Specific target

Find a retained CS-like action in the Cl(3)/Z³ lattice, compute its
boundary Hilbert space, and show the Koide triplet is exactly the
spin-1/2 representation of the boundary affine algebra at level 2.

---

## Attack Vector 11: The `2 out of 3` spinor parity

**Concept:** On three Cl(3) spinors (one per site), the PARITY EIGENVALUES
under the pseudoscalar `I` give a 3-bit string. The `I`-even and
`I`-odd states have specific counts:

- Total states: `2³ = 8` (3 qubits).
- Even under total pseudoscalar (product of all three I's): `4` states.
- Odd: `4` states.

Ratio even/total = 1/2. Not 2/3.

BUT: under `I` on EACH SPINOR individually (not the product):

- All three even (`+++`): 1 state.
- Two even, one odd (`++−` permutations): 3 states.
- One even, two odd: 3 states.
- All odd (`−−−`): 1 state.

Totals: 1 + 3 + 3 + 1 = 8 ✓.

The "mixed" states (`++−` or `+−−`) count: 6/8 = 3/4. Not 2/3.

Hmm. Doesn't directly give 2/3.

### Alternative: sign-PATTERN mod S_3

Under S_3 permutation of qubits, `++−` states form a 2-dim standard rep.
Under Z_3 rotation only: `++−` has 3 cyclic variants.

Specifically: pattern `(+,+,−)` and its 2 cyclic rotations form a Z_3 orbit.
That's 3 states.

`(+, −, +)` is the SAME as `(+, +, −)` cyclically rotated. So orbit size = 3
in both cases.

Similarly `(−, −, +)`: orbit size 3.

Total orbit structure: `(+++)` × 1 orbit (size 1), `(+ + −)` × 1 orbit (size 3),
`(+ − −)` × 1 orbit (size 3), `(−−−)` × 1 orbit (size 1).

Number of ORBITS: 4. Number of "doublet orbits": 2. Ratio: 2/4 = 1/2. Not 2/3.

### Another: spinor parity as Koide weight

Assign each 3-spinor state a Koide "weight" based on its parity signature.
Weighted sum gives an expectation value. Maybe this equals 2/3 for the
retained measure.

Not obvious but could be explored.

---

## Top-3 priority attacks (ranked by feasibility and novelty)

### 🏆 Priority 1: Attack Vector 2 (3-qubit tensor product irrep count)

**Why priority:** CLEAN COMBINATORIAL statement, directly from Cl(3)
spinor structure. Distinct from qubit-lattice-dim (different counting).
Verifiable quickly.

**Action:** Prove the identity `Q = #(spin-1/2 irrep copies)/#(total irrep copies) = 2/3`
matches the Koide ratio via a specific observable on the 3-qubit hw=1
space.

### 🏆 Priority 2: Attack Vector 7 (Pseudoscalar rotor quantization)

**Why priority:** Kills the radian assumption B1 directly. Cl(3)-native
units.

**Action:** Express Brannen form via Cl(3) pseudoscalar rotor `e^{Iδ/2}`,
show δ = 2/9 is the natural rotor parameter (not radian).

### 🏆 Priority 3: Attack Vector 8 (Graph Green's function resonance)

**Why priority:** Exact spectral-theory statement on the retained
Cl(3)/Z³ lattice graph. Gives Q = 2/3 as a residue identity.

**Action:** Compute Green's function on Z_3 cyclic graph, find the
spectral identity that equals 2/3.

---

## Secondary: combined-attack vectors

### Vector 12: Irrep count + rotor quantization together

If Priority 1 (irrep count = 2/3) AND Priority 2 (rotor δ = 2/9)
both work, together they give DUAL closure: Q from count, δ from rotor.
This is structurally analogous to the anomaly + time argument in
ANOMALY_FORCES_TIME.

### Vector 13: Use ALL the observational data

The Koide cone holds with Q = 0.666661 at PDG (< 10⁻⁴ off from 2/3).
Brannen phase is δ ≈ 0.22227 (< 10⁻⁴ off from 2/9).

**If we admit the OBSERVATION as a POSTULATE:** "the framework RETAINS
the experimental Koide identity as a structural input," then Q = 2/3
and δ = 2/9 are EMPIRICAL. This is less satisfying but might be the
right scientific answer.

**But:** the whole point of Cl(3)/Z³ is to DERIVE these, not postulate.

---

## Meta-observation

**All 10 attack vectors above share one theme:** they look for a DIFFERENT
structural carrier (flow, tensor product, rotor, graph, modular form)
where 2/3 and 2/9 arise NATIVELY, rather than via the contested
qubit-lattice-dim or SELECTOR² = Q bridges.

If ANY single one works, we have a native forcing law.

The most promising (by rough feasibility): **Attack Vector 2 (irrep count)**
and **Attack Vector 8 (graph Green's function)**. Both are clean
combinatorial/spectral statements on the retained Cl(3)/Z³ content.

---

## Next steps

1. Test Attack Vector 2 symbolically: verify the 3-qubit tensor product
   gives Koide Q = 2/3 via irrep counting on a specific observable.
2. Test Attack Vector 8 symbolically: compute the Z_3 graph Green's
   function residues and check for a natural 2/3 identity.
3. Test Attack Vector 7 numerically: express Brannen δ as a Cl(3)
   pseudoscalar rotor and verify 2/9 is the natural parameter value.
4. If any succeeds, write up as a new closure note and verify runner.
5. If multiple succeed, they provide INDEPENDENT structural bridges,
   strengthening the case.

---

## Initial probe results (2026-04-20 evening probe)

First pass computational probe of priority attacks:

### Attack Vector 2 (3-qubit tensor product): PARTIAL

- `#(spin-1/2 copies) / #(total copies) = 2/3` ✓ exact count ratio.
- BUT: `dim(spin-1/2 sector) / dim(total) = 4/8 = 1/2`, NOT 2/3.
- Koide Q on Casimir masses `{15/4, 3/4, 3/4}` gives ≈ 0.56, NOT 2/3.
- Koide Q on dim masses `{4, 2, 2}` gives ≈ 0.34, NOT 2/3.
- **Status:** irrep-count 2/3 is numerical but NOT an observable Koide
  ratio on this structure. Need to find the "right" observable or admit
  this is just restating qubit-lattice-dim.

### Attack Vector 7 (pseudoscalar rotor): NEGATIVE

- `δ/(4π) = 1/(18π)` transcendental. Not a clean rotor fraction.
- `δ/(2π/3) = 1/(3π)` transcendental. Not a clean Z_3 unit fraction.
- **Status:** δ = 2/9 is specifically a RADIAN rational, not a
  Cl(3)-rotor-natural parameter. This attack doesn't kill the radian
  assumption.

### Attack Vector 8 (graph Green's function): PROMISING BUT REDUCES

- Z_3 cyclic Laplacian has spectrum `{0, 3/2, 3/2}` — 2 distinct
  eigenvalues (one singlet, one degenerate-doublet).
- `#(distinct eigenvalues) / dim(lattice) = 2/3` ✓ exact.
- BUT: this is structurally the same as qubit-lattice-dim
  (# of distinct eigenvalues = # of isotypes = 2).
- **Status:** gives 2/3 natively but reduces to existing bridge, not a
  new forcing law.

### What the probe rules in / rules out

**Ruled in as candidates:** Attack Vectors 1 (gradient flow), 4 (universal
cover closed loop), 5 (lepton-baryon sphaleron), 6 (CM point modular),
9 (alternative entropy), 10 (Chern-Simons TQFT).

**Ruled out (probe-level):** Attack Vector 7 (pseudoscalar rotor), mostly
Attack Vector 2 (reduces to count, no observable match).

### Honest remaining frontier

The creative vectors that haven't been probe-eliminated are still open:

- Gradient flow (need to identify canonical generator).
- Universal cover quantization (need to prove Chern class on cover).
- CFT/modular form interpretation (need to identify the right modular
  form).
- Sphaleron anomaly (need to check the factor-of-π issue).

Each is a multi-week physics project. None is a quick win.

### Bottom line

**No immediate quick-win native forcing law has emerged from the first
probe pass.** The qubit-lattice-dim + anomaly arithmetic closure remains
the best available route, with the honest conditional status as stated
in `KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md` §1.2a.

The promising creative directions (1, 4, 5, 6, 9, 10) require deeper
mathematical work to evaluate. Setting them up as explicit candidate
theorems with target runners is the natural next step for a full
pass.
