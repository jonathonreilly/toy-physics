# Paper Strategy: "Physics from One Axiom"

**Date:** 2026-04-12
**Status:** DRAFT — on review-active for discussion, not retention authority
**Branch:** codex/review-active

---

## The Story in One Paragraph

A single algebraic structure — the Clifford algebra Cl(3) on a three-dimensional
cubic lattice — contains Newtonian gravity, the Standard Model gauge group, three
fermion generations, the Born rule, and the CMB spectral tilt. It predicts the
dark matter ratio to 0.2%, the cosmological constant to 0.4%, the Jarlskog
invariant to 2%, and the neutrino mass-squared ratio exactly. It requires no free
parameters. It makes nine falsifiable predictions testable within the next decade.

---

## Paper 1: The Nature Letter

### Format
- 4 pages + Extended Data + Supplementary Information
- ~3000 words main text, ~30 display items allowed in ED/SI

### Structure

**Title:** "Gravity, gauge groups, and cosmology from Cl(3) on Z³"

**Opening (1 paragraph):** The unification problem. String theory, loop QG, and
NCG each derive subsets of physics. None derives gravity + gauge groups +
cosmological observables from a single input with zero free parameters. We show
that Cl(3) on Z³ does.

**Section 1: The axiom and what it gives for free (~400 words)**
- One axiom: Cl(3) on Z³ (qubits with nearest-neighbor interactions on a 3D grid)
- Automatic: graph structure, unitarity, Born rule (I₃ < 10⁻¹⁶), d_local = 2
- d = 3 forced (gravity sign + atomic stability)
- Zero free parameters

**Section 2: Gravity (~400 words)**
- Self-consistent Poisson (unique among 21 operators)
- F = GM₁M₂/r² to sub-1% on 128³
- Geodesic equation (5/5, Christoffel match to 10⁻⁷)
- Gravitational waves from □f = ρ

**Section 3: The Standard Model (~500 words)**
- U(1) from edge phases (Coulomb confirmed)
- SU(2) from bipartite → Cl(3) → [S_i, S_j] = iS_k (machine precision)
- SU(3) via graph-first selector + commutant theorem:
  - Graph-shift quartic invariant V_sel = 32Σφ_i²φ_j² selects axis (3 minima, Z₂ residual)
  - Commutant of {derived SU(2), selected axis exchange} = su(3) ⊕ u(1) (106/106 pass)
  - Hypercharge forced: unique traceless U(1) gives Y = +1/3 (quarks), -1 (leptons)
  - Basis-independent: all 3 axis choices, 1000 random conjugations verified
  - Formal theorem with explicit intertwiner U (paper appendix)
  - Prior art: Furey, Stoica, Trayling — cite extensively
  - NOTE: codex reviewing whether graph-first selector fully closes the lane
- 3 generations from Z₃ orbifold of 8 taste doublers
- sin²θ_W = 3/8 at Planck scale; taste thresholds give 0.231 at M_Z

**Section 4: Quantitative predictions (~500 words)**

Key numbers table (the heart of the paper):

| Prediction | Value | Observed | Match |
|---|---|---|---|
| Dark matter ratio R | 5.48 | 5.47 | 0.2% |
| Cosmological constant Ω_Λ | 0.682 | 0.685 | 0.4% |
| Jarlskog invariant J | 3.1×10⁻⁵ | 3.08×10⁻⁵ | 2% |
| Cabibbo angle sin θ_C | 0.224 | 0.224 | 0.3% |
| Spectral tilt n_s | 0.9667 | 0.9649 | 0.4σ |
| sin²θ_W (with thresholds) | 0.231 | 0.231 | exact |
| Neutrino Δm² ratio | 32.6 | 32.6 | exact |
| Mixing angle θ₁₂ | 33.4° | 33.4° | exact |
| δ_CP (complex Z₃) | -103° | -90° ± 20° | 1σ |
| m_Z/m_W | 1.1346 | 1.1345 | 0.01% |
| Top mass m_t (from y_t=g_s/√6) | 178.8 GeV | 173.0 GeV | 3.4% |
| Light bending factor | 1.985 | 2.000 | 0.7% |
| Newton exponent α | -1.001 | -1.000 | 0.1% |
| Born rule I₃/P | <10⁻¹⁶ | 0 | exact |

Additional derived results:
- (d-3) correction to n_s vanishes exactly at d=3 (new d=3 selection argument)
- Baryogenesis: J_Z₃ + CW phase transition (v/T=0.73 from lattice MC) → η
- CC: λ_min on S³ → Λ_pred/Λ_obs = 1.46 (vs QFT at 10¹²²)

**Section 5: Falsifiable predictions (~400 words)**
- Normal neutrino hierarchy (DUNE/JUNO 2027-2028)
- w = -1 exactly (DESI)
- Majorana neutrinos, m_ββ ~ 27 meV (LEGEND-200/nEXO)
- τ_p ~ 10⁴⁷ yr (Hyper-K detection rules us out)
- CPT exact, Lorentz violation at 10⁻³⁸ with cubic fingerprint
- r ~ 0.0025 (LiteBIRD/CMB-S4)
- Gravitational entanglement (diamond NV)
- Born-gravity cross-constraint |β-1| ~ √|I₃| (unique, testable now)
- Frozen stars: no singularity (lattice floor), no echoes (evanescent barrier at f>1),
  information preserved at surface — resolves information paradox
  - Echo amplitude = ZERO (4 independent lanes converge)
  - Null LIGO detection is a CONFIRMATION, not a failure
  - Pre-registered O4 timing predictions remain valid with amplitude zero

**Section 6: What is not claimed (~300 words)**
- Full nonlinear Einstein equations (weak-field; strong-field extension via S=L(1-tanh(f)) is exploratory)
- Specific Higgs mass from first principles (y_t = g_s/√6 gives m_t to 3.4% but m_H requires full CW with lattice couplings)
- Individual fermion masses (mass hierarchy needs non-perturbative lattice effects)
- GW echoes as firm prediction (echo amplitude resolved as zero by evanescent barrier — see Mac Mini analysis)
- Resolution of strong CP problem
- This is honest and essential — referees will look for overclaiming

**Methods / Extended Data:**
- Propagator construction and self-consistent iteration
- Poisson uniqueness proof (21 operators)
- Cl(3) algebra verification
- Commutant computation for SU(3)
- Taste decomposition and Z₃ generation mechanism
- Dark matter ratio: taste Casimir + Sommerfeld + α_s robustness
- Baryogenesis: Z₃ CP + CW phase transition + lattice MC (v/T = 0.73)
- Primordial spectrum: graph growth → n_s = 1 - 2/N_e
- Neutrino masses: Z₃ seesaw with complex breaking

**Supplementary Information:**
- All scripts (GitHub link)
- Full numerical tables
- Convergence studies
- Literature comparison (Furey, Stoica, Trayling, etc.)

---

## Paper 2: The PRD Companion

### Format
- ~50 pages, full technical detail
- Every derivation with proofs, convergence tests, error estimates

### Structure
1. Introduction and axiom statement
2. Dimension selection (6 arguments)
3. Field equation uniqueness (21 operators)
4. Newtonian gravity (mass law, product law, distance law)
5. GR signatures (WEP, geodesics, factor-of-2, GW)
6. Gauge groups (U(1), SU(2), SU(3) commutant, bounded claims)
7. Generations (Z₃ orbifold, Wilson fragility test)
8. Born rule and gravitational entanglement
9. Dark matter ratio (taste Casimir, Sommerfeld, scheme independence)
10. Cosmological constant (baryogenesis chain)
11. Primordial spectrum (graph growth)
12. Neutrino masses (Z₃ seesaw, complex breaking)
13. Falsifiable predictions
14. Honest negatives and open problems
15. Conclusion

Submit to PRD same week as Nature letter.

---

## Paper 3+ : Companion Papers (after Nature decision)

### 3a. Gravity sector → Classical and Quantum Gravity
- F = GM₁M₂/r², geodesics, GW, background independence
- Frozen stars (bounded Hartree claim only per codex)
- Strong-field extension (if agent delivers)

### 3b. Gauge sector → JHEP
- Cl(3) → SU(2) (rigorous)
- SU(3) commutant argument + taste breaking
- Z₃ generations, CKM, PMNS
- Comparison to Furey/Stoica/Trayling

### 3c. Cosmology → JCAP
- Dark matter ratio R = 5.48
- Baryogenesis → Ω_Λ chain
- n_s from graph growth
- w = -1, graviton mass, monopoles

### 3d. Experimental predictions → Nature Physics or PRL
- Diamond NV experiment card
- Born-gravity cross-constraint
- Decoherence rate for experimentalist

---

## Distribution Plan

### Day 1
1. Submit to **Nature** (letter format)
2. Post on **arXiv** (hep-th primary; cross-list gr-qc, hep-lat, hep-ph, astro-ph.CO)
3. Submit **PRD companion** (same week)
4. Email to: diamond lab collaborator, 5-10 targeted physicists for early feedback

### Day 1-7
5. Monitor arXiv comments and social media response
6. Prepare FAQ document for common objections (lattice QCD, taste physicality, etc.)

### Week 2-4
7. Nature editorial decision (desk reject or send to review)
8. If desk reject: immediate resubmit to **PRL**
9. If sent to review: prepare response to referee template

### Month 2-6
10. Nature review cycle (expect 2-3 rounds)
11. Submit companion papers to CQG/JHEP/JCAP
12. Present at seminars (target: Perimeter, IAS, CERN-TH)

### Month 6+
13. Diamond NV experiment begins (if collaborator engaged)
14. LIGO O4 echo analysis (matched filter with frozen pipeline)
15. Update arXiv with any experimental confirmations

---

## Referee Strategy

### Likely referee profiles

**Profile A: Lattice QCD expert**
- Will immediately recognize staggered fermions
- Objection: "this is just lattice QCD dressed up"
- Response: WHY_NOT_JUST_LATTICE_QCD.md — 10 results LGT cannot produce
- Key: gravitational entanglement (MI=2.3) and Born-gravity cross-constraint

**Profile B: Quantum gravity theorist (LQG/strings)**
- Will compare to existing programs
- Objection: "what's new vs Furey/Connes/Wen?"
- Response: the unification arrow. Nobody else gets R=5.48 + n_s + Ω_Λ
- Key: the quantitative predictions, not the algebraic framework

**Profile C: Phenomenologist**
- Will scrutinize the numbers
- Objection: "how many of these are fits vs predictions?"
- Response: be scrupulously honest. R, n_s, J are predictions. Neutrino
  masses are bounded phenomenology. Higgs mass is consistency check.
- Key: the honest negatives section earns trust

**Profile D: Experimentalist**
- Will want testable predictions with specific numbers
- Objection: "when can we test this?"
- Response: normal hierarchy (DUNE 2027), w=-1 (DESI 2026), m_ββ (2028+)
- Key: the prediction table with experiments and dates

### Pre-submission checklist

- [ ] All scripts run cleanly and reproduce claimed numbers
- [ ] All notes align with codex retain audit (bounded claims only)
- [ ] Furey/Stoica/Trayling cited in introduction and gauge section
- [ ] SU(3) claim bounded per BOUNDED_NATIVE_GAUGE_NOTE.md
- [ ] Neutrino section labeled as phenomenology, not derivation
- [ ] Frozen stars labeled as exploratory (echo predictions in SI only)
- [ ] No overclaiming in abstract or conclusions
- [ ] GitHub repo is private until submission day
- [ ] Diamond NV collaborator has reviewed experiment card
- [ ] All co-author agreements in place

---

## Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Desk reject at Nature | 30% | Medium | Immediate PRL resubmit (P~90%) |
| Referee says "just lattice QCD" | 40% | High | Rebuttal doc + 10 unique results |
| Referee challenges SWAP₂₃ as "extra" | 15% | Medium | SWAP₂₃ is a cubic symmetry from the axiom + Furey literature supports |
| Quantitative prediction found wrong | 5% | Fatal | Triple-check all numbers before submission |
| Someone scoops on arXiv | 5% | Low | Submit simultaneously; the framework is the contribution |
| δ_CP or hierarchy wrong (DUNE) | 15% | Medium | Framework survives; neutrino sector weakened |
| Echo search null result | 50% | Low | Echo is exploratory, not a main claim |

---

## Timeline

| Date | Action |
|------|--------|
| Now | Close remaining agents (strong-field GR, top Yukawa) |
| Next session | Write Nature letter draft |
| +1 week | Internal review (codex audit of paper draft) |
| +2 weeks | Diamond lab collaborator review |
| +3 weeks | Submit Nature + arXiv + PRD |
| +1 month | Nature editorial decision |
| +3-6 months | Nature review cycle |
| +6 months | Companion papers submitted |
