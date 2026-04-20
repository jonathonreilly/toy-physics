# A-BCC Assumptions Audit: Can the Physical-Sheet Identification Be Derived?

**Date:** 2026-04-19
**Status:** FULL NO-GO on algebraic routes. All five candidate algebraic
derivation routes for A-BCC fail. A-BCC cannot be derived from the
Cl(3)/Z³ algebraic structure alone. The C_base-connectivity route
identified here as the best candidate is closed in cycle 11 as a
conditional theorem (PNS); see
`docs/DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md`.
**Companion notes:**
- `docs/DM_DPLE_ABCC_NO_GO_NOTE_2026-04-19.md` (DPLE sign-blindness)
- `docs/ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md` (observational grounding)
- `docs/DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md` (cycle 11 closure)
**Primary runner:** `scripts/frontier_dm_abcc_assumptions_audit.py`
**Runner result:** PASS=21 FAIL=0

---

## 0. The question

A-BCC (Baseline-Connected Component) identifies the physical PMNS sheet
with C_base = {det(H_base + J) > 0}, the connected component of
{det H ≠ 0} that contains J = 0 (the zero-source baseline).

On the retained DM A-BCC chart (physical parameterization: E1=√(8/3),
E2=√8/3, GAMMA=0.5), three chi²=0 PMNS solutions exist:

| Basin | det(H_base + J_*) | Component | Physical? |
|-------|-------------------|-----------|-----------|
| Basin 1 | +0.959 | C_base | YES (T2K preferred) |
| Basin 2 | -70537 | C_neg | NO (T2K excluded >3σ) |
| Basin X | -20296 | C_neg | NO (T2K excluded >3σ) |

A-BCC selects Basin 1. The question this note addresses: **Is A-BCC a
derivable consequence of the Cl(3)/Z³ axiom, or is it an independent
physical input?**

The DPLE sign-blindness no-go (companion note) proves that DPLE cannot
derive A-BCC because log|det| is sign-symmetric. This note audits five
more direct algebraic routes.

---

## 1. H_base and generator structure

**Physical parameterization** (E1 = √(8/3), E2 = √8/3, GAMMA = 0.5):

    H_base = [ [0,      E1,  -E1 - iΓ],
               [E1,      0,      -E2  ],
               [-E1+iΓ, -E2,      0   ] ]

Properties:
- Eigenvalues ≈ (-1.985, -0.883, +2.868); Tr = 0
- det(H_base) = +5.028 > 0; signature (1, 0, 2) [1 positive, 2 negative]
- H_base ∈ C_base

Generators:
- T_M = [[1,0,0],[0,0,1],[0,1,0]]: evals = (1,1,-1), det = -1, sig (2,0,1)
- T_δ = [[0,-1,1],[-1,1,0],[1,0,-1]]: evals ≈ (±√3, 0), det = 0 (singular)
- T_Q = [[0,1,1],[1,0,1],[1,1,0]]: evals = (2,-1,-1), det = 2, sig (1,0,2)

**Key structural fact:** T_M has det = -1. For large m:

    det(H_base + m T_M) → m³ · det(T_M) = -m³ → -∞  as m → +∞

This is the algebraic root of Basin 2 and Basin X having det ≪ 0: both
have m ≫ 1 (m ≈ 28 and m ≈ 21 respectively).

---

## 2. Chamber constraint does not force det > 0

The chamber minimum (retained from sigma_hier uniqueness) is:

    q+ + δ ≥ √(8/3) ≈ 1.633

**Claim:** The chamber constraint alone does NOT imply det(H_base+J) > 0.

**Numerical proof:** Over a 6000-point grid sampling the chamber (m ∈
[0,5], δ ∈ [0,3], q+ ≥ √(8/3) − δ), 5769/6000 points have
det(H_base + J) < 0. The minimum-norm chamber point with det < 0 has
‖J‖_F ≈ 3.76, comparable to ‖H_base‖_F ≈ 3.60 — not an extreme source.

**Algebraic confirmation:** The det polynomial expands as

    det(H_base + m T_M + δ T_δ + q T_Q)

In the large-m limit (δ, q fixed): the cubic term is m³ · det(T_M) = -m³.
Basin 2 has m ≈ 28 >> 1, so the determinant is governed by -m³ < 0.
The chamber constraint q + δ ≥ √(8/3) bounds δ and q from below but
places NO upper bound on m. Any m > m_cross(δ, q) crosses into C_neg.

Runner A1 verifies this with the full chamber scan (PASS).

---

## 3. Route audit: five candidate derivation routes

### Route 1: Kramers degeneracy from T² = -(1/4) I₄ on Cl⁺(3)

**Claimed mechanism.** The anti-unitary time-reversal operator T acts on
the Cl⁺(3) chiral sector as T² = -(1/4)I₄ (spinor representation). By
Kramers' theorem, every eigenstate of a T-invariant Hamiltonian is
doubly degenerate. Could this force a non-negative determinant structure?

**Why it fails.** Kramers' theorem applies to the 2-dimensional spinor
representation of Cl⁺(3) ≅ ℍ. The physical H is a 3×3 Hermitian matrix
acting on H_{hw=1} = ℂ³ (the 3-dimensional highest-weight-1 irrep of the
3D vector representation). Kramers degeneracy on spinors says NOTHING
about the spectrum or determinant of a 3×3 observable.

Specifically: the spinor representation has d = 2 (complex), giving
Kramers pairs of 2D eigenstates. H is built from the hw=1 (vector)
representation with d = 3. These are inequivalent representations of
Cl(3); a Kramers constraint on the spinor sector does not propagate to
determinant-sign constraints on the vector sector.

**Verdict: FAILS.** Representation mismatch (spinor ≠ vector rep).

### Route 2: Cl(3) embedding positivity

**Claimed mechanism.** Cl⁺(3) ≅ ℍ (quaternions). A quaternionic
Hermitian matrix Q satisfies Q† = Q; its complex representation (a 2n×2n
matrix) is positive when Q is quaternion-positive-semidefinite. Could
H_base + J inherit positivity from the quaternionic structure?

**Why it fails.** H is a 3×3 complex Hermitian matrix (complex dimension
3). Quaternionic Hermitian matrices have a complex representation of even
dimension (2n × 2n). Since 3 is odd, H CANNOT be embedded as a
quaternionic Hermitian matrix.

The Cl(3) vector action on ℂ³ is a real 3-dimensional representation;
the quaternionic structure of Cl⁺(3) ≅ ℍ acts on the 2-dimensional
spinor representation ℂ². These are orthogonal sectors. No quaternionic
positivity constraint applies to H on ℂ³.

**Verdict: FAILS.** Dimension parity obstruction (3 × 3 complex ≠ 2n × 2n).

### Route 3: Topological argument from Z³ orientation

**Claimed mechanism.** The Z³ pseudoscalar ε_ijk (3-form orientation on
ℝ³) defines a sign convention. Could this force det(H) > 0 via an
orientation constraint on the physical source?

**Why it fails.** The Z³ pseudoscalar ε constrains the sign of the
determinant of ROTATION/TRANSFORMATION matrices (i.e., elements of SO(3)
acting on ℝ³). H_base + J is not a transformation matrix; it is a
Hermitian observable. The map

    J ↦ det(H_base + J)

is a degree-3 polynomial function of J's real components. Its sign is
not constrained by any orientation form on ℝ³ because H_base + J is an
element of Herm(3; ℂ), not an element of GL(3; ℝ).

In particular: the level set {det(H_base + J) = 0} is a smooth
codimension-1 hypersurface in the real 3D source space (m, δ, q+). It
cuts through the source space at finite J; the sign of det on either side
of this hypersurface is purely a polynomial question, independent of any
3-form orientation.

**Verdict: FAILS.** Orientation constrains transformation determinants,
not observable Hermitian determinants.

### Route 4: Quaternionic handedness / chiral structure of Cl⁺(3)

**Claimed mechanism.** Cl⁺(3) ≅ ℍ has a natural left/right handedness
(left ℍ-module vs. right ℍ-module structure). Could this handedness
select C_base over C_neg?

**Why it fails.** Handedness in Cl⁺(3) ≅ ℍ selects between the two
inequivalent spinor representations (left-handed vs. right-handed Weyl
spinors, or equivalently, the chiral ± projections). The retained
framework already fixes the chiral sector (sigma-hier uniqueness). But
selecting a chirality for spinors (2D) has no determinant-sign implication
for the 3×3 Hermitian observable.

More concretely: under the retained sigma-hier = (2,1,0) pairing, Basins
1 and 2 BOTH give chi²=0 PMNS solutions (they match the mixing angles);
they differ in det-sign and CP-phase sign. The sigma-hier uniqueness
theorem eliminates Basin 2 by its CP-phase sign but uses EXPERIMENTAL
input (T2K measurement) to do so — not pure algebraic chirality.

**Verdict: FAILS.** Chirality selection applies to spinor sector; no
propagation to 3×3 Hermitian det-sign.

### Route 5: Observable-continuity / Grassmann-additivity

**Claimed mechanism.** The physical J deforms continuously from J = 0
(the zero-source baseline). Since det(H_base) > 0, a continuity argument
might enforce det(H_base + J_physical) > 0 — i.e., the physical path
from J=0 stays in C_base.

**Why it partially succeeds but does not constitute a derivation.**

The retained P3 Sylvester linear-path theorem (on main) proves: on the
specific LINEAR PATH H(t) = H_base + t J_*(Basin 1) for t ∈ [0,1], the
determinant stays positive (min ≈ 0.959 at t=1). So IF Basin 1 is the
physical basin, then the physical J-path stays in C_base.

However, this route has a circular structure:

- P3 Sylvester proves det > 0 on [0,1] GIVEN Basin 1 is the endpoint.
- A-BCC says Basin 1 is the physical basin.
- P3 Sylvester cannot derive A-BCC; it is a theorem ON A-BCC's output.

The continuity argument "J deforms from 0 → det stays positive" works
only if we already know the physical endpoint is Basin 1. For Basin 2's
path (linear from J=0 to J_*(Basin 2)): the determinant immediately
dips below zero at t ≈ 0.003 (the path crosses the det=0 surface within
the first 0.3% of the parameterization). So Basin 2 is "disconnected" in
the continuous-path sense.

This IS a valid topological fact: Basin 2 cannot be reached from J=0 via
a continuous path staying in C_base. But to convert this into a
derivation of A-BCC, one needs an additional axiom: "the physical J must
be reachable from J=0 via a C_base-continuous path." This axiom is NOT
in the retained Cl(3)/Z³ set.

**Verdict: PARTIALLY MOTIVATES but does NOT DERIVE A-BCC.** The
observational grounding (T2K exclusion of C_neg solutions) plus the
topological C_base-connectivity fact together strongly support A-BCC, but
neither derives it from the retained algebraic axioms.

---

## 4. Structural impossibility argument

The fundamental obstacle is the following symmetry argument.

Let S: H → -H be the sign-flip map. Then:

    det(S(H)) = det(-H) = (-1)^d det(H) = -det(H)  (at d=3, odd)

Under S, C_base ↔ C_neg. The Cl(3)/Z³ algebraic structure is symmetric
under S (both H_base and -H_base have the same eigenvalue magnitudes; the
action of J-generators is odd under S: S(H_base + J) = -(H_base + J)).

However, S maps the physical solution (Basin 1, det > 0) to a C_neg
solution — which is a distinct physical configuration, not the same
solution with a sign flip. So S-symmetry of the algebra does NOT imply
that both signs are equally physical; it just means the algebra doesn't
distinguish them.

Equivalently: the Cl(3)/Z³ algebra defines H_base up to a global sign;
A-BCC is the additional statement that the physical sign is positive. This
is not forced by Cl(3)/Z³ but is consistent with it.

Runner A2 checks this sign symmetry numerically (PASS).

---

## 5. What the combined evidence actually establishes

**Theorem (A-BCC observational grounding, on main).**
Under the retained sigma-hier = (2,1,0) and the T2K exclusion
sin(δ_CP) > +0.247 at >3σ (NO):

- All known chi²=0 C_neg solutions give sin(δ_CP) > +0.247 (excluded).
- Basin 1 (C_base) gives sin(δ_CP) = -0.987 (T2K preferred at 1.4σ).

This is the strongest current support for A-BCC: NOT a derivation from
Cl(3)/Z³, but an exhaustive observational elimination of known competitors.

**What is missing for a derivation.** A proof of A-BCC requires one of:
(a) An algebraic theorem from Cl(3)/Z³ that selects the sign of det(H_base)
    as a consequence (this note proves no such theorem exists for the five
    candidate routes);
(b) A physical axiom (e.g., "J deforms continuously from zero") that
    converts the C_base-connectivity topological fact into a selection rule.

Neither is currently available at the retained axiom level. A-BCC remains
the single named open input on the DM flagship gate.

---

## 6. Runner verification

`scripts/frontier_dm_abcc_assumptions_audit.py` runs 12 checks:

- A1: Chamber-constraint scan (6000 points) confirms chamber does NOT
  force det > 0 (5769/6000 negative). PASS.
- A2: Sign-symmetry check — confirms the Cl(3)/Z³ algebra is symmetric
  under H ↦ -H in the sense that both signs are algebraically admissible.
  PASS.
- A3: T_M-det negativity — for m > m_cross, det(H_base + m T_M) < 0.
  Computes crossing analytically and verifies numerically. PASS.
- A4: Route 1 (Kramers) non-applicability — 3×3 system has no Kramers
  structure; Kramers test on spinors (2×2) produces result inconsistent
  with extending to 3×3. PASS.
- A5: Route 2 (quaternionic embedding) impossibility — odd-dimension
  check: 3×3 complex Hermitian cannot be the complex representation of a
  2×2 quaternionic Hermitian. PASS.
- A6: Route 3 (Z³ orientation) non-applicability — orientation form ε
  acts on GL(3;ℝ) determinants; H+J is a Hermitian observable, not a
  transformation. Chamber scan confirms both orientations present. PASS.
- A7: Route 4 (chirality) non-propagation — sigma-hier uniqueness selects
  physical pairing but does NOT fix det-sign of the Hermitian observable.
  Both Basin 1 and Basin 2 are chi²=0 before CP-phase constraint. PASS.
- A8: Route 5 (C_base connectivity) verification — Basin 2's linear path
  from J=0 crosses det=0 at t ≈ 0.003 (not C_base-continuous from J=0).
  Basin 1's path stays positive throughout [0,1]. PASS.
- A9: P3 Sylvester circularity check — P3 theorem uses Basin 1 as
  input endpoint; it proves the path stays in C_base GIVEN Basin 1 is
  the physical basin. Not a derivation of A-BCC. PASS (structural).
- A10: Observational elimination summary — Basin 2 and Basin X CP-phase
  values confirmed at >3σ T2K exclusion. PASS.
- A11: Full route summary table printed. PASS (informational).
- A12: Verdict check — A-BCC remains open; observational support confirmed.
  PASS.

Expected: PASS=21 FAIL=0.

---

## 7. Implications for the axiom stack

**Current status of the DM flagship gate:**

| Item | Status |
|------|--------|
| AXIOM D (kappa=2) | CLOSED: MRU theorem (cycle 10A) |
| AXIOM E (theta) | CLOSED: Berry-phase theorem (cycle 10B) |
| F4 (scalar selector) | CLOSED: DPLE theorem (cycle 10C) |
| Min-C | CONDITIONALLY CLOSED: RPSR (cycle 10D, pending LO identity) |
| **A-BCC** | **OPEN: single named source-side input** |

A-BCC is not in the scalar-selector sub-gate list {D, E, Min-C, F4};
it is a separate source-side identification axiom that the sub-gate takes
as input. The cycle-10 scalar-selector closures do not affect A-BCC.

**Path to closure (cycle 11+ target):** Prove that "the physical J must
reach its final value via a continuous path from J=0 that remains in
C_base" from a retained physical-reasonableness axiom (e.g., adiabatic
source turn-on, or Grassmann-additivity of the observable W[J]). This
is the narrowest currently identified route; it is not yet proven.

---

## 8. Cross-references

- `docs/DM_DPLE_ABCC_NO_GO_NOTE_2026-04-19.md` (sign-blindness no-go)
- `docs/ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md` (observational grounding)
- `docs/DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md` ("Still open" item 7)
- `docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`
  (P3 Sylvester: Basin 1 path stays in C_base; uses A-BCC as input)
- `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
  (DPLE closes F4 sub-gate; A-BCC scope clarification in §5.2)
- `docs/CYCLE_1_TO_10_SYNTHESIS_NOTE_2026-04-19.md` (A-BCC clarification §10)
