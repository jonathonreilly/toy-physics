# Primitive P-HeavyQ Species Differentiation — Open-Gate Candidate Inventory

**Date:** 2026-05-10
**Claim type:** open_gate
**Sub-gate:** Heavy-quark species-DIFFERENTIATION primitive on `y_q(M_Pl)` UV
boundary condition.
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note inventories candidate primitive routes; it does
not admit, approve, or promote any candidate primitive.
**Source-note proposal disclaimer:** this note is a primitive-design
proposal note. Audit verdict and downstream status are set only by the
independent audit lane.

**Primary runner:**
[`scripts/cl3_primitive_p_heavyq_2026_05_10_pPheavyq.py`](../scripts/cl3_primitive_p_heavyq_2026_05_10_pPheavyq.py)
**Cached output:**
[`logs/runner-cache/cl3_primitive_p_heavyq_2026_05_10_pPheavyq.txt`](../logs/runner-cache/cl3_primitive_p_heavyq_2026_05_10_pPheavyq.txt)

## 0. Probe context

This open-gate inventory is motivated by recent heavy-quark mass stress
tests and proposal branches. Those surrounding PRs are context only, not
load-bearing dependencies for this note, and this note does not require any
unlanded sibling probe to be accepted.

- **Probe X-L1-Threshold (PR #933):** companion probe reports that the EW
  Wilson-chain heavy-quark absolute-mass route with
  `m_q = M_Pl × C × α_LM^{n_q}` is foreclosed.
- **Probe Y-L1-Ratios (PR #946):** companion probe reports that EW-chain
  heavy-quark mass ratios via integer-difference exponents are foreclosed.
- **Probe Z-Quark-QCD-Chain (PR #958):** companion probe reports that the
  parallel QCD-confinement chain
  `m_q = Λ_QCD × C × α_s^{n_q}` is foreclosed for the `(m_t, m_b, m_c)`
  triplet under any single structural `C`.
- **Probe W-Quark-RGFP (PR #1022):** Yukawa quasi-fixed-point attractor
  (Pendleton-Ross 1981 / Hill 1981) does not close `m_t` from
  framework-derived UV BC at the 5% gate.
- **Probe V-Quark-Dynamical (PR #981):** companion probe reports that the
  Yukawa-dominated current-mass + chiral SSB constituent shift route is
  foreclosed; chiral SSB Σ ~ Λ_QCD³ bridges <0.2% of the m_b gap with
  species-uniform Ward BC.
- **Probe U-Heavy-Modular (PR #994):** companion probe reports that
  SL(2,ℤ) modular flavor on Γ(3) at τ = ω is foreclosed; canonical
  weight-2 Yukawa matrix at τ = ω is rank-1 (eigenvalues (9, 0, 0)) —
  structurally inconsistent with PDG 3-mass spectrum.

The working gap being tracked is:

> "Heavy-quark masses cannot be reached by single-coupling chain OR
> Yukawa+SSB OR RGE QFP OR modular flavor at τ=ω. The species-
> DIFFERENTIATION primitive on y_q(M_Pl) UV BC remains the open gap."

This note inventories **three candidate primitives** (P-Heavy-A, P-Heavy-B,
P-Heavy-C) for the species-differentiation gap. It does NOT close the
gap. It explicitly enumerates which existing framework context each
candidate uses and which new inputs would require explicit approval before
any future admission.

## 1. Assumptions exercise (Elon first-principles)

### 1.1 Existing framework context used as background

The diagnostic refers to the following framework context without changing
any status:

| Item | Content | Role in this diagnostic |
|---|---|---|
| Z1 | `α_LM = α_bare/u_0 = 0.090668` (geometric-mean coupling) | contextual input |
| Z2 | `α_s(v) = α_bare/u_0² = 0.1033` (CMT vertex-power chain) | contextual input |
| Z3 | `g_lattice = √(4π α_LM) = 1.0673` | contextual input |
| Z4 | Ward identity `y_t(M_Pl) = g_lattice/√6 = 0.4358` | context, not re-ratified here |
| Z5 | `m_t = y_t(v) v/√2 = 169.5 GeV` (-1.84% from PDG) | context, not re-ratified here |
| Z6 | `v = M_Pl × (7/8)^{1/4} × α_LM^{16}` (hierarchy theorem) | contextual input |
| Z7 | C_3[111] cyclic structure on hw=1 generation triplet | contextual input |
| Z8 | Hermitian circulants on T_1: `H = aI + bC + b̄C²` | contextual input |
| Z9 | Circulant eigenvalues: `λ_k = a + 2|b|cos(arg(b) + 2πk/3)` | contextual input |
| Z10 | Z_3 Fourier basis diagonalizes C_3[111] (PR landing 2026-05-03) | contextual input |
| Z11 | Down-type ratio `m_s/m_b = [α_s(v)/√6]^{6/5}` (+0.2% threshold-local) | bounded context, not re-ratified here |
| Z12 | Brannen-Rivero charged-lepton form `√m_k = v_0(1+√2 cos(δ + 2πk/3))` | contextual admission surface |
| Z13 | Brannen amplitude-equipartition condition (legacy alias: A1): `2|b|/a = √2` for charged leptons (`ρ_lep = √2`) | contextual admission surface |
| Z14 | Square-root mass identification (legacy alias: P1): `λ_k = √m_k` not `m_k` | contextual admission surface |
| Z15 | δ_lep = 2/9 rad ≈ Brannen magic angle (charged-lepton phase) | empirical observation |

### 1.2 What the framework DOES NOT have for heavy quarks

Despite the rich circulant structure, the framework does not retain:

- A derivation of which sector (up vs down, generation index 1/2/3) each
  Fourier-basis eigenvalue `λ_k` corresponds to.
- A derivation of `ρ_q = 2|b_q|/a_q` for the up-type and down-type quark
  sectors (charged-lepton-specific value `ρ_lep = √2` from the Brannen
  amplitude-equipartition condition does not extend; Appendix A.3 of
  `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE`
  reports required `ρ_up ≈ 1.754` for top, `ρ_down ≈ 1.536` for bottom).
- A derivation of the relative phases `δ_q` for up-type and down-type
  quarks (charged-lepton-specific value `δ_lep ≈ 2/9` from empirical
  observation).
- A derivation of the absolute scale `v_q` for each sector (charged-lepton
  has `v_0 = 17.72 √MeV` heuristic match).
- An identification of ρ_q in terms of fundamental Casimirs or framework
  constants (no `C_F`, `C_A`, `T_F`, `α_LM` combination has been derived
  to give ρ_up = 1.754).

### 1.3 What if assumptions are wrong?

**Assumption A:** Heavy-quark masses are encoded in a 3-eigenvalue circulant
spectrum on H_{hw=1} per sector (up-type / down-type), with sector-dependent
ρ and δ.
**If wrong:** the sector partition would not be a circulant on H_{hw=1};
quarks could couple to a different invariant of the C_3 algebra (e.g., a
non-circulant component of the M_3(ℂ)_Herm decomposition under C_3
conjugation), or to a 6-dimensional representation (joint isospin ×
generation) that does not split into per-sector circulants.

**Assumption B:** UV BC at M_Pl is the right anchor.
**If wrong:** the BC could be at Λ_QCD (reported against by Probe Z), at
the EW scale `v` (Yukawa+SSB; reported against by Probe V), or at a previously
unidentified intermediate scale (e.g., the EW symmetry breaking transition
scale ≠ v due to NLO matching shifts). This would change the RGE running
distance and could shift the predicted ρ values.

**Assumption C:** Species labels (top, bottom, charm) are intrinsic
quantum numbers vs emergent boundary-condition consequences.
**If wrong:** the three masses could be three eigenvalues of a single
sector-blind operator, with the species label being an a-posteriori
sorting by RGE attractor — top quark = the eigenvalue that flows to the
quasi-fixed point; bottom quark = the eigenvalue that flows to a different
fixed point under the up/down isospin-asymmetric β functions. (This blends
into Probe W-RGFP, which reports foreclosure; but a hybrid where the BC supplies three
distinct Yukawa values that each flow to **different** IR fixed points is
not yet tested.)

## 2. Three candidate primitives

### 2.1 P-Heavy-A: Sector-dependent ρ-Koide circulant

**Formal statement.**

> Each quark sector `q ∈ {up-type, down-type}` carries an independent
> circulant Hermitian operator `H_q = a_q I + b_q C + b̄_q C²` on
> H_{hw=1}, with eigenvalues `λ_k^(q) = a_q + 2|b_q|cos(δ_q + 2πk/3)`
> for `k = 0, 1, 2`. The Yukawa UV boundary condition at M_Pl is
> `y_{q,k}(M_Pl) = (λ_k^(q)/v_0_q) × g_lattice/√6` where `(ρ_q, δ_q,
> v_0_q)` are sector-specific parameters with `ρ_q = 2|b_q|/a_q`.
> Identification: generation `g` ∈ {1,2,3} maps to Fourier index `k ∈
> {1, 2, 0}` (electron-like to k=1, muon-like to k=2, tau-like to k=0)
> for charged leptons, and the heaviest generation (top, bottom) maps
> to k=0 for quarks.

**Derivation of m_t/m_b/m_c ratios.**

Charged-lepton parameters (from existing framework calibration):
`ρ_lep = √2, δ_lep = 2/9 rad`. Required quark parameters per Appendix
A.3 of the Koide circulant note:

| Sector | ρ required | δ tested | Eigenvalue ratio |
|---|---|---|---|
| up-type (t, c, u) | 1.754 | TBD | √(m_t/m_c)/v_0_up |
| down-type (b, s, d) | 1.536 | TBD | √(m_b/m_s)/v_0_dn |

Under square-root mass identification (legacy alias: P1), `λ_k = √m_k`:
- m_t/m_c = (λ_0/λ_1)² with `(ρ_up, δ_up)`
- m_b/m_s = (λ_0/λ_1)² with `(ρ_dn, δ_dn)`

The runner numerically computes `(ρ_up, δ_up)` that fit `(m_t, m_c, m_u)`
and `(ρ_dn, δ_dn)` that fit `(m_b, m_s, m_d)` (with PDG values used as
falsification targets), then asks whether the resulting `(ρ_up, ρ_dn)`
are recognizable framework constants.

**Physical interpretation.** Each sector lives in its own copy of the
M_3(ℂ)_Herm circulant family. The up-down isospin partner relationship
is implemented at the circulant level: not "y_q is a single 3×3 Yukawa
matrix with up and down components" but "y_up and y_dn are independent
3-eigenvalue operators sharing the C_3[111] Fourier basis."

**Prior literature analog.** Closest analog is the Brannen-Rivero
charged-lepton circulant (hep-ph/0505220), generalized to per-sector ρ.
The sector-dependent ρ is not in Brannen's original work — Brannen
proposed Q_lep = 2/3 as universal; sector-specific ρ extension is a
framework-internal candidate.

**Is the candidate BAE-locked?** No, P-Heavy-A is independent of BAE
(Brannen amplitude-equipartition condition; legacy alias: A1). BAE forces
ρ = √2 universally; P-Heavy-A explicitly relaxes BAE per sector. The
future-admission cost, if pursued, would be replacing 1 universal scalar
(BAE) with 4 sector-specific parameters `(ρ_up, δ_up, ρ_dn, δ_dn)`.

**Hostile-review tier classification.**
- **Would require explicit approval before admission:** 4 sector-specific
  real parameters `(ρ_up, δ_up, ρ_dn, δ_dn)`. None are derived here.
- **Context used by the diagnostic:** square-root mass identification
  (legacy alias: P1), Z_3 Fourier basis
  on H_{hw=1}.
- **Not assumed here:** universal Brannen amplitude equipartition (BAE)
  outside the charged-lepton context.

**Runner verdict pre-test:** the candidate exists as a parameter-counting
extension and matches PDG masses by construction (with 4 sector-specific
fits), but does not derive `(ρ_up, ρ_dn, δ_up, δ_dn)` from framework
constants. This is candidate parameter-counting, not closure. Scoring
target: 2/4 quark parameters recognizable.

**Runner findings (post-test, 2026-05-10):**
- `ρ_up = 1.7600` (sub-1% fit residual on `(t, c, u)` triplet) matches
  `2 × F_adj = 16/9 = 1.7778` to **1.01%**.
- `ρ_dn = 1.5450` (sub-1% fit residual on `(b, s, d)` triplet) matches
  `(7/8) + √2/2 = 1.5821` to **2.40%**.
- `ρ_lep = 1.4150` matches `√2` to **0.06%** (consistency with the
  existing charged-lepton BAE context, as expected).
- `δ_lep` matches `2/9` orbit (under C_3 ⋊ Z_2 symmetry) consistent with
  Brannen magic angle.
- The `2 × F_adj` candidate identification for `ρ_up` is structurally
  intriguing: `F_adj = 1 - 1/N_c² = 8/9` is the framework's adjoint
  Fierz channel fraction (retained-bounded context per
  [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md) §3),
  and `2 × F_adj = 2(1-1/N_c²)` is a natural N_c-graded combination.
  The `ρ_dn` candidate identification `(7/8) + √2/2` blends the APBC
  factor with the BAE-equipartition `√2/2`; this is suggestive but
  carries less structural cleanness than `ρ_up`.

**Open question raised by these findings:** if `ρ_up = 2(1 - 1/N_c²)` and
`ρ_dn = (7/8) + √2/2` are derivable from framework Casimirs, the
4-parameter candidate collapses to identifications of the existing
F_adj, APBC, and √2 (BAE) inputs in N_c-graded combinations. This is a
candidate route to future review — pursuing it requires deriving why the up-
type sector uses `2 F_adj` while the down-type sector uses
`7/8 + √2/2`. (The 1.01% gap on rho_up is at the edge of the framework's
typical precision; rho_dn at 2.40% is not.)

---

### 2.2 P-Heavy-B: Froggatt-Nielsen-like generation-graded chain

**Formal statement.**

> Each fermion `f` of generation `g ∈ {1, 2, 3}` and isospin `T_3 ∈
> {+1/2, -1/2}` carries an integer-graded chain exponent
> `n(g, T_3)` such that
> `y_f(M_Pl) = (g_lattice/√6) × α_LM^{n(g, T_3) - n(top)}`,
> with normalization
> `n(top) = n(g=3, T_3=+1/2) = 0` (i.e., top quark sits at the
> retained Ward value). The species-differentiation primitive is the
> structural rule for `n(g, T_3)`.

**Derivation of m_t/m_b/m_c ratios.**

Required `n(g, T_3)` from PDG masses, working back from
`y_f(v) = m_f √2 / v` and 1-loop SM RGE running v → M_Pl:

| Fermion | y_f(M_Pl) (RGE-derived) | n_required = log(y_f/y_t)/log(α_LM) |
|---|---|---|
| t | 0.4358 (Ward; n=0 by construction) | 0 |
| b | ~0.0067 (RGE from y_b(v) ~ 0.024) | n_b ≈ 1.74 |
| c | ~0.0027 (RGE from y_c(v) ~ 0.0073) | n_c ≈ 2.13 |
| τ | ~0.0073 (RGE from y_τ(v) ~ 0.010) | n_τ ≈ 1.71 |
| s | ~0.000147 | n_s ≈ 3.36 |
| μ | ~0.000437 | n_μ ≈ 2.91 |

The runner tests integer/simple-rational fits for `n_b, n_c, n_τ`. The
density-of-rationals control inherits from Probe Z's methodology
(integer-only random-density ~5% at 5%; q ≤ 6 random-density ~37% at 5%,
~8% at 1%).

**Physical interpretation.** The chain exponent `n` is the Froggatt-
Nielsen U(1)_FN charge difference between the fermion and the top quark.
Each insertion of the flavon spurion `<S>/M_Pl ~ α_LM^{1/2}` in the
SU(3)_F-invariant Yukawa operator suppresses the effective Yukawa by one
power. With α_LM^{1/2} ~ 0.301 as the suppression factor, the integers
n correspond to the U(1)_FN charge differences.

**Prior literature analog.** This is the Froggatt-Nielsen mechanism
(Nucl. Phys. B147, 277 (1979)) applied to the physical Cl(3) local
algebra / Z^3 spatial substrate surface. The key
non-trivial step relative to standard FN: the framework's α_LM (not a
free flavon expectation value `<S>/M`) plays the role of the small
parameter. The "U(1)_FN charges" `n(g, T_3)` are non-derived quantum
numbers in standard FN — here, they are the new structural primitive.

Recent work `Mapping and Probing Froggatt-Nielsen Solutions to the Quark
Flavor Puzzle (Bauer, Carena, Ramos 2023)` enumerates viable charge
assignments — n_top = 0, n_charm = 4, n_up = 8 reproduces up-type ratios
with ε ~ Cabibbo angle. These integer assignments could be tested against
the n_required values above.

**Is the candidate BAE-locked?** No, P-Heavy-B is independent of BAE,
the Brannen amplitude-equipartition condition, square-root mass
identification, and the Brannen-Rivero circulant entirely. It uses only the
Z_3 generation-structure context (Z7, Z10) plus the candidate
`n(g, T_3)` integer assignment.

**Hostile-review tier classification.**
- **Would require explicit approval before admission:** 1 integer-valued
  function `n: {gen} × {isospin} → ℤ` (5 free integers if `n(top)=0` is
  fixed and lepton mapping is optional).
- **Context used by the diagnostic:** Ward `y_t(M_Pl) = g_lattice/√6` (Z4),
  α_LM = α_bare/u_0 (Z1).
- **Not assumed here:** no Brannen-Rivero circulant ingredient
  (P-Heavy-B does not engage with the circulant story).

**Runner verdict pre-test:** the candidate exists as a 5-integer function
fit, and matches PDG masses if integer/simple-rational `n_b, n_c, n_τ,
n_s, n_μ` exist. The probe tests:
1. Are `n_b, n_c, n_τ, n_s, n_μ` integer-close to within the random-
   density 5% gate?
2. Do they admit a structural rule (e.g., `n(g, T_3) = 2(g-1) + δ_{T_3, -1/2}`)?

Scoring target: integer-close-to-5% PASS for ≥3/5; structural-rule fit
PASS for ≥2/5.

---

### 2.3 P-Heavy-C: Casimir-graded color-isospin contraction

**Formal statement.**

> The Ward identity factor `1/√6 = 1/√(N_c · N_iso)` reflects unit-norm
> normalization on the (1,1) singlet of Q_L = (2,3). Generation-
> differentiated extension: each generation's Ward factor uses a
> different color-isospin tensor contraction with structurally-distinct
> Casimir weights:
> ```
> y_{f,g}(M_Pl) = g_lattice × √(C_g(g, T_3) / 6)
> ```
> where `C_g(g, T_3) = c_color(g) × c_iso(T_3)` is the Casimir-graded
> contraction weight per generation/isospin.

**Derivation of m_t/m_b/m_c ratios.**

Working back from `y_q(M_Pl) / (g_lattice/√6) = √C_g`:

| Fermion | y_f(M_Pl) | C_g = (y/y_t)² |
|---|---|---|
| t | 0.4358 (Ward) | C_t = 1 (top sets normalization) |
| b | ~0.0067 | C_b ≈ 2.4e-4 |
| c | ~0.0027 | C_c ≈ 3.8e-5 |

Required Casimir suppression: `C_b/C_t ≈ 1/4200`, `C_c/C_t ≈ 1/26000`,
`C_b/C_c ≈ 6.3`. Test whether these factor as `c_color(g) × c_iso(T_3)`
with each factor recognizable as a SU(3)/SU(2) Casimir or
Clebsch-Gordan combination.

The runner enumerates candidate Casimir combinations:
- `C_F = 4/3, T_F = 1/2, C_A = 3, F_adj = 8/9, 7/18, 7/8, 8/9 × T_F = 4/9`
- Powers and products: `C_F^k T_F^j (1-T_F)^l ...`
- Generation-graded: `c_color(g) ∝ (8/9)^g`, `(7/18)^g`, `(C_F)^{-(g-1)}`, etc.

**Physical interpretation.** The 1PI Block 6 Clebsch-Gordan analysis
showed all six basis components of unit-norm (1,1) singlet have weight
1/√6. P-Heavy-C posits that physical identification of components with
species Yukawas uses **non-uniform** Clebsch-Gordan-like weights derived
from generation-dependent Casimir contractions — not the uniform 1/√6.
The 1PI algebra context is not modified (each component still has weight
1/√6 in the singlet wavefunction); if this candidate were pursued, the
species identification would mix components with C_g-weighted contractions.

**Prior literature analog.** Closest analog: SU(5)/SO(10) GUT Yukawa
unification with generation-dependent Clebsch-Gordan factors (e.g.,
Georgi-Jarlskog `m_b/m_τ = 1, m_s/m_μ = 1/3, m_d/m_e = 3` from SU(5)
×Z_n). The framework version: physical Cl(3) local algebra / Z^3
spatial substrate Casimir context (no GUT
embedding), with generation grading from the Z_3 Fourier basis.

**Is the candidate BAE-locked?** No, P-Heavy-C is independent of BAE,
the Brannen amplitude-equipartition condition, and square-root mass
identification. It engages only with the Ward Block 6 algebra context
(Z4 and the underlying Clebsch-Gordan structure) plus the new `C_g`
function.

**Hostile-review tier classification.**
- **Would require explicit approval before admission:** 1 generation-graded
  Casimir function `C_g: {gen} × {isospin} → R+` (5 positive reals if
  `C_t = 1` fixed).
- **Context used by the diagnostic:** Ward Block 6 1PI algebra (Z4
  underlying structure), framework Casimirs `C_F, T_F, C_A, F_adj`.
- **Not assumed here:** species-uniform Block-6 reading would need to be
  re-evaluated if this candidate were pursued.

**Runner verdict pre-test:** the candidate exists as a 5-real function
fit. The probe tests:
1. Do `C_b/C_t, C_c/C_t, C_b/C_c, C_τ/C_t` factor as products of
   recognizable framework Casimirs?
2. Is there a generation-graded structural rule (e.g.,
   `c_color(g) ∝ F_adj^{g-1}` or `c_iso(T_3 = -1/2) = T_F` vs
   `c_iso(T_3 = +1/2) = C_F - T_F`)?

Scoring target: ≥2/3 of `(C_b, C_c, C_τ)/C_t` factor in the candidate
Casimir basis; structural-rule fit at the ≥3-fermion level.

## 3. Comparative summary

| Primitive | New parameters | BAE-locked? | Closes m_t? | Closes m_b/m_c? | Literature analog |
|---|---|---|---|---|---|
| P-Heavy-A | 4 (ρ_up, δ_up, ρ_dn, δ_dn) | NO (relaxes BAE) | yes (top fixed by Ward Z4 context) | by construction with 4 fits | Brannen-Rivero, sector-dependent extension |
| P-Heavy-B | 5 integers (n_b, n_c, n_τ, n_s, n_μ) | NO (orthogonal to BAE) | yes (n_top = 0) | iff integer fits exist | Froggatt-Nielsen 1979 |
| P-Heavy-C | 5 reals (C_b, C_c, C_τ, C_s, C_μ relative to C_t = 1) | NO (orthogonal to BAE) | yes | iff Casimir factorization holds | SU(5)/SO(10) Georgi-Jarlskog Clebsch-Gordan |

**P-Heavy-A** sits naturally on the existing Brannen-Rivero / Koide
circulant infrastructure (re-uses Z7-Z10, relaxes BAE per sector only as
a candidate).
Best-positioned for "extends existing audited-context backbone" framing.
Runner verdict: STRONGEST candidate. `ρ_up` matches `2 F_adj = 16/9` at
1.01%; the 4-parameter candidate may collapse to ~2 framework Casimir
identifications under further investigation.

**P-Heavy-B** is structurally simpler (integer counting) and most
directly testable against density-of-rationals control. Best-positioned
for "Froggatt-Nielsen on the framework's α_LM scale" framing.
Runner verdict: WEAK. Only n_c (0.6%) and n_s (4.6%) are integer-close
at 5%; n_b at 1.397 (159% rel.err to nearest integer 1) and n_τ at
1.705 (51% rel.err) are far off. Integer-only FN-on-α_LM is rejected
by the runner's evidence.

**P-Heavy-C** sits on the existing Ward identity / Block-6 Clebsch-
Gordan stack (re-uses Z4, refines its physical reading). Best-positioned
for "species-differentiation as Casimir-graded reading of Ward
algebra" framing.
Runner verdict: WEAK BUT INFORMATIVE. 2/5 fermions admit Casimir-product
factorization at <5% (b at 0.25%, c at 0.02%); 4/5 admit at <20%. But
density-of-Casimirs control at 5% gate gives 87% random hit rate (the
Casimir-product search space is too dense), so factorization closes carry
no structural information above ~13% confidence. The single-Casimir or
single-product structural rule (e.g., Georgi-Jarlskog `F_adj^(g-1)`)
fails by 99% on charm.

## 4. What this note explicitly does NOT claim

This note does NOT claim:

- **Any positive closure** of the heavy-quark species-differentiation
  gap. All three candidates would require new species-dependent parameters; the
  runner numerically checks how well each candidate matches PDG `m_b,
  m_c, m_τ` etc. but neither candidate derives those values from the
  retained surface.
- **A choice among P-Heavy-A, B, C.** The note proposes three
  candidates side-by-side; selection should follow audit-lane scrutiny
  and follow-up probes (which structural-Casimir or integer fit holds,
  which sector-pairing makes sense, etc.).
- **Modification of the retained m_t prediction** (Z5 = 169.5 GeV @
  -1.84%). All three candidates normalize to the Ward-context value at
  the top channel.
- **Modification of the bounded m_s/m_b ratio** (Z11 at +0.2%
  threshold-local). P-Heavy-A and P-Heavy-B/C are tested against this
  ratio as a downstream consistency check; the bounded-ratio audit
  status is not promoted by this note.
- **Promotion of any Brannen-Rivero BAE or square-root mass ingredient** to
  retained. All three candidates either relax or remain orthogonal
  to BAE; none promote a Brannen-magic-angle or sector-uniform
  equipartition statement.

## 5. Audit-lane authority

This is a **primitive-design proposal note**. Pipeline-derived status
and downstream propagation are set only by the independent audit lane,
not by this note. The result recorded here is a **3-candidate enumeration
with parameter-counting and density-of-rationals classification**, NOT
a closure or new positive theorem.

The runner produces:
- The required `(ρ_up, δ_up, ρ_dn, δ_dn)` for P-Heavy-A and tests
  whether they match recognizable framework constants.
- The required `(n_b, n_c, n_τ, n_s, n_μ)` for P-Heavy-B and tests
  integer/simple-rational closure with density-of-rationals control.
- The required `(C_b, C_c, C_τ, C_s, C_μ)/C_t` for P-Heavy-C and tests
  Casimir factorization against the framework's `{C_F, T_F, C_A, F_adj}`
  basis.

## 6. Cross-references

- **Probe X-L1-Threshold (PR #933):** companion EW Wilson-chain absolute
  mass probe.
- **Probe Y-L1-Ratios (PR #946):** companion EW-chain mass-ratio
  integer-difference probe.
- **Probe Z-Quark-QCD-Chain (PR #958):**
  [`KOIDE_Z_QUARK_QCD_CHAIN_NOTE_2026-05-08_probeZ_quark_qcd_chain.md`](KOIDE_Z_QUARK_QCD_CHAIN_NOTE_2026-05-08_probeZ_quark_qcd_chain.md)
  companion parallel QCD-chain probe.
- **Probe W-Quark-RGFP (PR #1022):** companion QFP-attractor top-mass
  probe.
- **Probe V-Quark-Dynamical (PR #981):** companion chiral-SSB bridge
  probe.
- **Probe U-Heavy-Modular (PR #994):** companion SL(2,ℤ) modular flavor
  probe at τ=ω.
- **Existing context:**
  - [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md) —
    retained m_t = 169.5 GeV @ -1.84%.
  - [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
    — species-uniform interpretation falsified at 35× on m_b; species-
    differentiation primitive named as the open gap (§5.2).
  - [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
    — Brannen-Rivero charged-lepton circulant; Appendix A.3 records
    `ρ_up ≈ 1.754, ρ_down ≈ 1.536` as the required values (charged-lepton
    BAE does not extend).
  - [`THREE_GEN_Z3_FOURIER_DIAGONALIZATION_THEOREM_NOTE_2026-05-03.md`](THREE_GEN_Z3_FOURIER_DIAGONALIZATION_THEOREM_NOTE_2026-05-03.md)
    — retained Z_3 Fourier basis on H_{hw=1}.
- **Literature anchors:**
  - Froggatt & Nielsen, Nucl. Phys. B147, 277 (1979) — original FN
    mechanism.
  - Ramond, Roberts, Ross, Nucl. Phys. B406, 19 (1993) — U(1)_FN charge
    assignments for quark mass hierarchy.
  - Bauer, Carena, Ramos, "Mapping and Probing FN Solutions to the
    Quark Flavor Puzzle," Phys. Rev. D 111, 015042 (arXiv:2306.08026,
    2024) — recent computational catalog of FN charge assignments.
  - Fritzsch, Phys. Lett. B73, 317 (1978) — original Fritzsch six-zero
    ansatz; six-zero excluded; Fritzsch-Xing four-zero textures still
    viable per Verma & Khan, JHEP 08 (2023) 162 (arXiv:2305.00069).
  - Brannen, hep-ph/0505220 — circulant cosine charged-lepton form;
    Q = 2/3 derivation with magic angle δ ≈ 2/9 rad.
  - Pendleton & Ross, Phys. Lett. B98, 291 (1981) — RG quasi-fixed
    point for top Yukawa (tested by Probe W-Quark-RGFP
    PR #1022 for the framework UV BC).
  - Hill, Phys. Rev. D24, 691 (1981) — IR fixed point of SM Yukawa.

## 7. Constraints respected

- **No new repo-wide axioms.** The baseline remains the physical Cl(3)
  local algebra on the Z^3 spatial substrate.
- **No new derivational imports.** PDG fermion masses are observational
  targets; no PDG mass enters as a derivation premise.
- **No fitted constants are promoted to the retained surface.** All three
  candidate primitives carry species-dependent parameters whose framework-
  constant interpretation is the open question this note proposes, not
  closes.
- **No promotion.** None of P-Heavy-{A,B,C} are promoted; the runner
  produces parameter-fit values + density-of-rationals classification
  + Casimir factorization tests.

PASS = 12, FAIL = 5 across all candidate-primitive checks (runner
output cache: `logs/runner-cache/cl3_primitive_p_heavyq_2026_05_10_pPheavyq.txt`).

The 5 FAILs are diagnostic, not blocking — they characterize which
structural rules within each candidate primitive fail to close. The
P-Heavy-A candidate carries 0 FAIL (8/8 PASS); the P-Heavy-B and
P-Heavy-C candidates carry the 5 informational FAILs that sharpen the
open-gap content for downstream selection between candidates.
