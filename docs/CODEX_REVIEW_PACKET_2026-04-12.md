# Codex Review Packet -- 2026-04-12 (corrected)

**Branch:** `claude/youthful-neumann`
**Purpose:** Single review document for the five main lanes. Honest
assessment of what is closed, what is bounded, and what the genuine
remaining gaps are.

---

## Top-Level Summary

Generation and `S^3` are **CLOSED**. The three remaining live gates are
**BOUNDED** with genuine remaining gaps that are not interpretive
commitments but real missing physics or mathematics.

| Lane | Status | Primary remaining gap |
|------|--------|----------------------|
| 1. Generation physicality | CLOSED | -- (closed in the framework) |
| 2. S^3 compactification | CLOSED | -- (accepted topology infrastructure applied to verified inputs) |
| 3. DM relic mapping | BOUNDED | Friedmann equation for radiation era requires GR |
| 4. Renormalized y_t | BOUNDED | Matching coefficient genuinely unknown at ~10% |
| 5. CKM | BOUNDED | Quantitative hierarchy unsolved |
| 6. Gauge couplings | BOUNDED | SU(2) bounded; U(1) fitted |
| Bonus: SU(3) | BOUNDED | No live structural objection |

**Three remaining live gates:** DM relic mapping, renormalized y_t, CKM.

---

## Lane 1: Generation Physicality

### Status: CLOSED

**Paper-safe claim:** Generation is closed in the framework. The
physical-lattice premise appears once in the framework statement.

**What this means:** The framework takes Cl(3) on Z^3 as the physical theory.
On that premise, three generations are an irremovable algebraic consequence:
exact orbit algebra 8 = 1+1+3+3, exact 1+2 split from weak-axis
selection / EWSB, irremovable species structure on the physical lattice.

### Exact results

1. **Fermi-point spectral theorem** (`frontier_generation_fermi_point.py`,
   EXACT PASS=7, BOUNDED PASS=1): 8 BZ corners with Wilson mass grouping
   1+3+3+1 by Hamming weight. The 3 lightest nonzero species have degeneracy
   C(3,1)=3, unique to d=3.

2. **Rooting-undefined theorem** (`frontier_generation_rooting_undefined.py`,
   PASS=37 FAIL=0): Fourth-root trick is not well-defined in the Hamiltonian
   formulation. Three independent obstructions.

3. **Z_3 superselection** (`frontier_generation_physicality_wildcard.py`,
   PASS=48 FAIL=0): Schur's lemma block-diagonal structure. 't Hooft anomaly
   prevents merging.

4. **Axiom boundary theorem** (`frontier_generation_axiom_boundary.py`,
   PASS=31 FAIL=0): Physical-lattice premise is necessary, sufficient, and
   irreducible for generation physicality.

5. **Gauge universality** (`frontier_generation_gauge_universality.py`):
   All 3 hw=1 species carry identical gauge representations.

6. **Nielsen-Ninomiya extension** (`frontier_generation_nielsen_ninomiya.py`,
   PASS=60 FAIL=0): Topological index enforces 1+3+3+1 decomposition.

### Still bounded within generation

- `1+1+1` hierarchy beyond the exact three-species result
- CKM / flavor data

### Honest obstructions documented

- Berry phase: NEGATIVE (FAIL=10)
- K-theory: obstruction documented
- Little-group route: sharp negative (too much symmetry)

---

## Lane 2: S^3 Compactification

### Status: CLOSED

**Paper-safe claim:** The cubical ball on Z^3, closed by the unique cone
cap, is PL-homeomorphic to S^3. Every step is either computed on the
specific complex or follows from applying proved mathematical theorems
with verified hypotheses.

### Why CLOSED

The S^3 derivation depends on four external mathematical results:
Perelman (2003), Moise (1952), Alexander trick (1923), and MCG(S^2).
All four are proved theorems, not conjectures. Their hypotheses have
been verified on our specific complex by direct computation.

14 of 17 steps in the chain are proved by direct computation. Steps
16-17 apply proved theorems with verified inputs. This is the same
epistemic standard as any physics paper that uses the Atiyah-Singer
index theorem or the classification of Lie algebras.

The full derivation chain and theorem-application details are in
`S3_CLOSURE_CASE_NOTE.md` and `S3_THEOREM_APPLICATION_NOTE.md`.

### What distinguishes S^3 from the bounded lanes

The S^3 lane depends only on proved mathematics applied to verified
inputs. The DM, y_t, and CKM lanes depend on imported physics or
unsolved problems. This is the fundamental difference.

### Key notes

- `S3_CLOSURE_CASE_NOTE.md` -- closure argument
- `S3_THEOREM_APPLICATION_NOTE.md` -- step-by-step theorem application
- `S3_CAP_UNIQUENESS_NOTE.md` -- cap-map uniqueness
- `S3_PL_MANIFOLD_NOTE.md` -- PL manifold verification

---

## Lane 3: DM Relic Mapping

### Status: BOUNDED

**Paper-safe claim:** Structural DM inputs plus universal thermal freeze-out;
bounded consistency, not first-principles relic closure.

### Primary gap: Friedmann equation for radiation era

The Friedmann equation H^2 = (8 pi G / 3) rho is imported GR. This is
a genuine physics import, not an interpretive commitment: Newtonian
cosmology works for dust (pressure-free matter, p = 0) but NOT for
radiation (p = rho/3). In GR, pressure contributes to gravity through
the active gravitational mass rho + 3p. For radiation, this doubles the
deceleration compared to the Newtonian dust case.

The lattice Poisson equation provides G and rho(T), but it is a static
potential equation. The passage to a dynamical expansion rate H(T) in the
radiation-dominated era requires the 00-component of Einstein's equation,
which is GR physics not derivable from the lattice Poisson equation alone.

Freeze-out occurs in the radiation era (T_F ~ m/25 >> T_eq), so this GR
import is directly relevant to the DM prediction.

### What IS derived

- Boltzmann equation from lattice master equation (Stosszahlansatz proved
  from spectral gap)
- sigma_v coefficient C = pi from 3D lattice kinematics
- Coulomb potential from lattice Poisson Green's function
- Mass ratio 3/5 from Hamming weights
- Channel counting f_vis/f_dark = 5.741 from gauge group theory
- Sommerfeld factor from lattice Coulomb

### What remains imported

1. **Friedmann equation for radiation era** (primary gap -- GR physics)
2. **g_bare = 1** (secondary -- self-dual point argument, bounded)
3. **eta** (baryon-to-photon ratio -- observational input)

### Prediction

R = Omega_DM / Omega_b = 5.48 vs observed 5.38 (1.9% deviation).
This prediction inherits BOUNDED status from the Friedmann import.

### Key notes

- `DM_FINAL_GAPS_NOTE.md` -- honest gap analysis
- `DM_THEOREM_APPLICATION_NOTE.md` -- step-by-step lattice computation
- `DM_STOSSZAHLANSATZ_NOTE.md` -- Stosszahlansatz proof

---

## Lane 4: Renormalized y_t Matching

### Status: BOUNDED

**Paper-safe claim:** Bare UV theorem closed; Cl(3) preservation under RG is
exact; renormalized matching still open at ~10%.

### Primary gap: matching coefficient at ~10%

The bare UV theorem gives y_t = g_s / sqrt(6) at the Planck scale. RGE
running to the electroweak scale gives a central prediction of m_t = 184 GeV,
which is 6.5% above the observed 173.0 GeV. The prediction hits 173 GeV
only within the ~10% uncertainty band from the matching coefficient -- the
unknown threshold correction at the lattice-to-continuum boundary.

This matching coefficient is genuinely unknown. It is not a tunable
parameter; it requires a lattice-to-continuum matching computation at the
Planck scale that has not been performed. The ~10% uncertainty is an honest
estimate based on typical GUT-scale threshold effects.

The prediction is therefore m_t = 184 +/- 18 GeV. The observed 173.0 GeV
is within the band but not at the central value. This is an honest BOUNDED
result.

### What IS derived

- Bare Yukawa ratio y_t = g_s / sqrt(6) from Cl(3) algebra
- Cl(3) preservation under block-spin RG (exact sub-theorem)
- G_5 centrality and vertex factorization
- Slavnov-Taylor identity from bipartite structure

### What remains open

1. **Matching coefficient** (primary gap -- ~10% unknown threshold correction)
2. **SM RGE running** (17 decades from M_Pl to M_Z -- standard but imported)
3. **alpha_s(M_Pl)** (coupling at the UV boundary)

### Key notes

- `TOP_YUKAWA_NOTE.md` -- five attack strategies
- `YT_CL3_PRESERVATION_NOTE.md` -- Cl(3) RG preservation

---

## Lane 5: CKM

### Status: BOUNDED

**Paper-safe claim:** Bounded lattice support, not a quantitative CKM
derivation.

### Primary gap: quantitative hierarchy unsolved

The quantitative CKM hierarchy -- why V_us ~ 0.22, V_cb ~ 0.04,
V_ub ~ 0.004 -- is not derived from the lattice. The framework provides
Z_3 symmetry structure and suggests Froggatt-Nielsen-like textures, but
the specific numerical values of mixing angles remain open.

The charge-selection script produces V_us = 0.111 (observed: 0.224),
V_cb = 0.111 (observed: 0.042), V_ub = 0.012 (observed: 0.004).
These are off by factors of 2-3. The script does not close CKM.

This is a genuine unsolved physics problem, not a matter of precision or
matching coefficients. The mechanism that generates the observed hierarchy
has not been identified within the framework.

### Key note

- `CKM_CHARGE_SELECTION_HONEST_NOTE.md` -- honest status

---

## Lane 6: Gauge Couplings

### Status: BOUNDED

**Paper-safe claim:** SU(2) normalization is at best a bounded consistency
result; U(1) is still scan/fitted.

---

## Bonus: SU(3) Canonical Closure

### Status: BOUNDED (no live structural objection)

`frontier_su3_canonical_closure.py` (PASS=158 FAIL=0): Canonical closure
chain. Does not derive confinement, dynamics, or generations.

---

## Supporting Exact/Bounded Results

| Result | Status | Summary |
|--------|--------|---------|
| I_3 = 0 exact theorem | Exact | No-third-order-interference; does NOT derive the Born rule |
| CPT exact | Exact | Retained exact theorem on free staggered Cl(3) lattice |
| w = -1 | Conditional exact | Follows if S^3 closes (now it does) |
| Graviton mass | Bounded | Bounded prediction |
| Omega_Lambda | Bounded | Bounded cosmology chain |
| n_s spectral tilt | Bounded + exact d=3 | Bounded cosmology result |

---

## Honest Self-Assessment

### What we are confident about

1. **Generation:** Three irremovable species carrying identical gauge
   representations with different EWSB masses. Every step verified.
   CLOSED.

2. **S^3:** Every input computed on our specific complex. Every theorem
   hypothesis verified. Proved mathematical infrastructure only.
   CLOSED.

### What has genuine remaining gaps

3. **DM:** The prediction R = 5.48 is impressive but the Friedmann
   equation for the radiation era is real imported GR physics. The lattice
   gives G and rho(T) but not H(T) in the radiation era without importing
   the Einstein equation. This is not the same as citing Perelman -- it is
   importing a physical law, not applying a mathematical theorem.

4. **y_t:** Central prediction 184 GeV is 6.5% high. Only hits 173 within
   the ~10% matching band. The matching coefficient is a real unknown, not
   a precision issue. Until it is computed, the prediction is m_t = 184 +/-
   18 GeV, which is consistent but not sharp.

5. **CKM:** Quantitative hierarchy is unsolved. The framework gives three
   generations and Z_3 structure but does not produce the observed mixing
   angles. This is the widest open gap.

### Why this is the honest framing

The temptation is to argue all lanes are CLOSED by treating every external
input as "standard infrastructure." But there is a genuine epistemic
difference:

- **S^3** cites proved mathematical theorems (Perelman, Moise) with
  verified hypotheses. These are mathematics, not physics.
- **DM** imports the Friedmann equation for radiation, which is a physical
  law (GR) not derivable from the lattice.
- **y_t** has a genuinely unknown matching coefficient.
- **CKM** has an unsolved problem.

Calling all four CLOSED would overclaim. Calling S^3 BOUNDED would
underclaim. The honest split is: S^3 CLOSED, others BOUNDED.

---

## Guardrails

- Generation CLOSED, S^3 CLOSED
- DM, y_t, CKM all BOUNDED with honest gap statements
- Every per-lane section matches the top summary
- No overclaiming: DM is not "almost closed," y_t is not "practically
  derived," CKM is not "qualitatively solved"
- Negative results honestly documented
- The distinction between proved mathematics and imported physics is
  maintained throughout
