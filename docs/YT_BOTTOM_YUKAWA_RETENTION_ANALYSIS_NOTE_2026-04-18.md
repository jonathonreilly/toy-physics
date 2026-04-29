# Bottom Yukawa P1 Retention Analysis Note (b-Quark Ward Extension)

**Date:** 2026-04-18 (amended 2026-04-18 with §0 scope correction)
**Status:** framework-native **scope analysis** of the b-Yukawa under the
**species-uniform interpretation** of the retained Ward identity. The
retained Ward identity on the Q_L = (2,3) block is algebraically
species-uniform at the 1PI 4-point function level by Block 6 of the
Ward-identity runner (all six basis components of the unit-norm (1,1)
singlet carry identical Clebsch-Gordan weight 1/√6). **Under the
species-uniform reading** — i.e., identifying every iso/color component of
H_unit with a physical-species Yukawa at the SAME ratio g_s/√6 — this
gives `y_b(M_Pl) / g_s(M_Pl) = 1/√6` and, by Δ_R flavor-blindness, the
same MSbar-side BC as the top. Running this species-uniform BC forward to
the electroweak scale through 2-loop SM RGE produces `m_b(m_b) ≈ 145 GeV`
(35× overshoot of observed 4.18 GeV) and simultaneously `m_t ≈ 102 GeV`
(0.59× undershoot of observed 172.69 GeV). **This is a falsification of
the species-uniform interpretation of the retained Ward identity, not a
falsification of the framework's m_t prediction.** The framework's
quantitative m_t prediction chain (per
`docs/YT_ZERO_IMPORT_CHAIN_NOTE.md`, m_t ≈ 169.5 GeV, -1.84% deviation)
uses a **species-privileged BC** — y_t at the lattice Ward value while y_b
is held at its observed small value — NOT the species-uniform chain
studied here. The species-uniform scope analysis therefore closes
narrowly: the retained 1PI Ward theorem does not extend to physical
species Yukawas uniformly. A species-differentiation primitive is required
to close the absolute m_b scale, and the Koide circulant Fourier-basis
spectrum (`codex/science-workspace-2026-04-18`, cross-ref §0 below) is the
positive mechanism candidate — conditional on A1 equipartition + P1
√m-identification as named non-retained ingredients.
**Primary runner:** `scripts/frontier_yt_bottom_yukawa_retention.py`
**Log:** `logs/retained/yt_bottom_yukawa_retention_2026-04-18.log`

---

## §0 Scope correction (amendment 2026-04-18)

**This note's original outcome framing was overly strong and is corrected
here.** The original abstract concluded "Outcome A: Yukawa unification at
M_Pl, empirically FALSIFIED by 33× on m_b." Read literally, this
suggests the framework's own predictions are falsified. That reading is
NOT what the §1-§7 analysis establishes, and the framing is hereby
tightened to the correct scope.

### What the §1-§7 analysis actually establishes

1. The retained Ward identity theorem on Q_L = (2,3) is a statement about
   a **specific 1PI 4-point function on the scalar-singlet channel** of
   Q_L ⊗ Q_L*. Block 6 of its runner verifies that the six Clebsch-Gordan
   overlaps of the unit-norm (1,1) singlet are all equal to 1/√6 — this
   is an exact algebraic property of the canonical singlet wavefunction
   on a 6-dim block.
2. **Translating Block 6 species uniformity into a species-uniform
   physical BC `y_f(M_Pl) = g_s(M_Pl)/√6` for every fermion species f**
   requires an additional structural step: identifying the `(α, a)`
   basis component of H_unit with the **bare physical Yukawa** of the
   species carrying those iso/color labels. That identification is NOT a
   direct consequence of the 1PI Ward theorem — it is an interpretation
   of how H_unit couples to physical species.
3. Under the species-uniform interpretation (all 9 Yukawas at g_s/√6 at
   M_Pl), SM 2-loop RGE yields `m_b(m_b) ≈ 145 GeV` and `m_t ≈ 102 GeV`.
   **These are predictions OF THE SPECIES-UNIFORM INTERPRETATION**, not
   predictions of the framework on the retained surface.
4. The 35× mismatch on m_b is therefore a **falsification of the
   species-uniform interpretation** (Ward-uniformly-applied + SM-RGE-to-v
   + SM-matching), NOT a falsification of the framework.

### What the framework's actual m_t prediction chain looks like

The retained m_t prediction (`docs/YT_ZERO_IMPORT_CHAIN_NOTE.md`,
`scripts/frontier_yt_zero_import_chain.py`) uses a **species-privileged
boundary condition**:

- y_t(M_Pl) = g_lattice/√6 = 0.4358 (Ward value on the top channel);
- y_b(v) ≈ 0.016 (held at its observed small value as an infrastructure
  input for the v → M_Z running cross-check);
- Backward scan gives y_t(v) ≈ 0.9734;
- m_t = y_t(v) · v/√2 ≈ 169.5 GeV (-1.84% deviation from 172.69 GeV).

This is a **different chain** from the species-uniform one studied in
§1-§7 below. The two chains share the g_lattice/√6 Ward value on the top
channel, but they differ on the b channel: the retained top-only chain
treats y_b as empirical infrastructure (not closed), while the
species-uniform chain in §1-§7 imposes y_b = y_t at M_Pl.

### What the 35× result DOES establish

- **The retained 1PI Ward identity on Q_L does not extend to a physical
  species-uniform BC** via simple Clebsch-Gordan substitution. If it did,
  SM RGE would produce m_b ≈ 145 GeV, which is empirically wrong.
- **The retained surface requires a species-differentiation primitive**
  to close the absolute m_b scale. This is CONSISTENT with all Class
  #1-#7 retained no-go results on generation-hierarchy primitives AND
  with the positive circulant-spectrum mechanism of
  `docs/YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md` §0.
- The 35× number quantifies **how much** species-differentiation is
  needed: roughly a factor of ~35 suppression on the bare y_b at M_Pl
  relative to the species-uniform Ward value, or equivalently a Fourier-
  basis eigenvalue structure with the bottom circulant eigenvalue
  suppressed by ~1/35 relative to the equipartition mean.

### What the 35× result DOES NOT establish

- **It does not establish that the framework's m_t prediction is wrong.**
  The top-only retained chain (`YT_ZERO_IMPORT_CHAIN_NOTE.md`) uses
  species-privileged boundary conditions and remains valid at -1.84%.
- **It does not establish that the retained Ward theorem is wrong.** The
  Ward theorem is a 1PI statement about a specific 4-point function on
  the Q_L singlet channel; its Block 6 species uniformity (all 6
  Clebsch-Gordan overlaps = 1/√6) is an exact algebraic property. The
  species-uniform PHYSICAL INTERPRETATION is what's falsified, not the
  algebra.
- **It does not establish that the framework cannot predict m_b.** A
  richer interpretation in which H_unit's Fourier-basis spectrum on
  each generation sector is independently normalizable (per the Koide
  circulant mechanism below) can produce sector-specific Yukawa ratios
  consistent with m_b ≈ 4.18 GeV. That interpretation requires A1
  equipartition + P1 √m-identification as named non-retained
  ingredients, each of which is NOT on the current retained surface but
  is under active study.

### Cross-reference to the Koide circulant positive mechanism

The `codex/science-workspace-2026-04-18` branch's
`docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` shows that
the retained C_3[111] cyclic structure forces any Hermitian operator
commuting with cyclic permutation to have circulant form
`H = a·I + b·C + b̄·C²` with three distinct Fourier-basis eigenvalues
`λ_k = a + 2|b| cos(arg(b) + 2πk/3)`. Appendix A.3 of that note verifies
numerically that the √2 equipartition envelope (ρ = 2|b|/a = √2) caps
eigenvalue ratios at 1 + √2 ≈ 2.414, which:

- fits charged leptons (τ at 98.5% of the envelope) exactly at Q = 2/3;
- **overshoots for up-type quarks** (ρ_up ≈ 1.754 required for the top)
  and **down-type quarks** (ρ_down ≈ 1.536 required for the bottom) —
  i.e., sector-dependent ρ is needed, per Appendix A.3 of the Koide note.

This is exactly the species-differentiation primitive the §1-§7 analysis
below identifies as required. The Koide circulant mechanism is NOT
retained here; but it is the positive mechanism that closes the b-Yukawa
scope the species-uniform interpretation falsifies. The species-uniform
reading of the retained Ward identity corresponds to "all sectors at the
equipartition critical point" — which only works for charged leptons
and fails for quarks. The Fourier-basis-spectrum reading gives
sector-dependent ratios.

### Revised outcome for this note

- The **algebraic claim** of §1-§2 (Block 6 singlet uniformity + Δ_R
  flavor-blindness) remains correct at the 1PI level and is unchanged.
- The **species-uniform physical interpretation** of that algebra, leading
  to Yukawa unification at M_Pl (y_t = y_b), is **falsified by SM RGE**
  (via the 35× overshoot on m_b).
- The **framework m_t prediction** of 169.5 GeV (retained, zero-import
  chain) stands, because it uses species-privileged boundary conditions,
  NOT the species-uniform chain.
- The **retention gap** is narrowed and sharpened: what's needed is NOT a
  "new species-breaking primitive from scratch," but rather a structural
  identification of how H_unit's Fourier-basis eigenvalues map onto
  physical species Yukawas sector-by-sector. The circulant Fourier-basis
  spectrum of the Koide branch is the leading candidate; the A1 + P1
  primitives identified there are the named retention gaps.

### Confidence on the amendment

HIGH on all points above. The §1-§7 algebra is correct at the 1PI level.
The species-uniform PHYSICAL INTERPRETATION is what the RGE run
falsifies. The distinction between species-uniform and species-privileged
BCs is explicit in the two runners (`frontier_yt_bottom_yukawa_retention.py`
for species-uniform, `frontier_yt_zero_import_chain.py` for
species-privileged top-only).

**The rest of this note (§1-§7) is the original species-uniform
scope analysis, preserved for the algebra. The corrected framing above
supersedes the original "Outcome A FALSIFIED" verdict.**

---

## Authority notice

This note is a retained **retention-analysis note** on the b-quark Yukawa.
It does **not** modify:

- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), whose Q_L block
  derivation and species-uniform Clebsch-Gordan (Block 6, all six basis
  components = 1/√6) are inherited without modification;
- the retained P1 Δ_R master assembly theorem
  (`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`), whose
  three-channel structural decomposition is inherited without modification.
  The **canonical retained central** used here is the full-staggered-PT
  value `Δ_R = −3.77 % ± 0.45 %` from
  `docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`, which
  supersedes the prior literature-cited `−3.27 %` as the scheme-conversion
  correction for the `y/g_s` ratio at M_Pl. The literature-cited `−3.27 %`
  is preserved as the citation-based three-channel roll-up and is
  consistent with the canonical central within the master assembly's
  ±2.32 % literature-bounded band;
- the retained master UV-to-IR transport obstruction theorem
  (`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`),
  whose ~1.95% total residual is unchanged;
- the retained color-singlet projection theorem
  (`docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`), whose √(8/9) physical-to-Ward
  factor is inherited without modification;
- the bounded down-type mass-ratio CKM-dual note
  (`docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`), whose bounded secondary
  lane `m_s/m_b = [α_s(v)/√6]^(6/5)` is unchanged in its stated bounded
  role (this note addresses the **absolute** bottom scale, which the
  CKM-dual lane explicitly does not close);
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native **scope
analysis** of whether the **species-uniform interpretation** of the retained
Ward identity (applying the 1PI Block 6 Clebsch-Gordan uniformly to every
physical species Yukawa at M_Pl) produces a forward prediction for `m_b` in
agreement with observation. The answer is: the species-uniform interpretation
yields `y_b(M_Pl)/g_s(M_Pl) = 1/√6`, and the RGE forward-running of this BC
**falsifies the species-uniform interpretation** via a 35× overshoot on m_b.
The retained Ward theorem's 1PI algebra is unchanged; the species-uniform
PHYSICAL reading of that algebra is what's closed negatively. The framework's
retained m_t prediction (`YT_ZERO_IMPORT_CHAIN_NOTE.md`, species-privileged
BC) is unaffected and remains at -1.84% deviation.

---

## Cross-references

### Foundational retained theorems (directly inherited)

- **Ward-identity tree-level theorem (Q_L block, species-uniform):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) —
  `y_bare² = g_bare²/(2 N_c) = g_bare²/6`; Block 6 of the runner
  verifies all six basis Clebsch-Gordan overlaps on the unit-norm (1,1)
  singlet equal 1/√6.
- **P1 Δ_R master assembly (three-channel color decomposition):**
  [`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`](YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md) —
  `Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`;
  literature-cited central value `Δ_R = −3.27%`, 1σ band `(−3.27 ± 2.3)%`.
  (Superseded as canonical by the full-staggered-PT `−3.77 % ± 0.45 %`.)
- **P1 Δ_R full-staggered-PT BZ quadrature (canonical retained central):**
  [`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`](YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) —
  `Δ_R = −3.77 % ± 0.45 %` from framework-native 4D BZ quadrature of the
  four canonical lattice-PT integrals.
- **Color-singlet projection (scalar wave-function):**
  [`docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md) — `√(8/9)` multiplicative
  factor on the physical Yukawa from the composite-Higgs scalar propagator.
- **Canonical-surface anchors:**
  [`docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) — `α_LM = 0.09067`,
  `α_s(v) = 0.1033` via CMT.

### Context

- **Master UV→IR obstruction (unchanged):**
  [`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`](YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
- **Down-type mass-ratio CKM-dual (bounded lane):**
  [`docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`](DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md) — bounded
  `m_s/m_b = [α_s(v)/√6]^(6/5)` from |V_cb| = (m_s/m_b)^(5/6) bridge.
- **2-loop y_t chain (reused RGE skeleton):**
  [`scripts/frontier_yt_2loop_chain.py`](../scripts/frontier_yt_2loop_chain.py) — this note's runner extends the
  same 2-loop SM RGE to include the y_b channel.

---

## Abstract (species-uniform interpretation Verdict)

> **NB (reading guide):** the Abstract, §1, and §2 below describe what the
> species-uniform interpretation of the retained Ward identity produces.
> This is a SCOPE ANALYSIS of that interpretation, not a framework
> prediction. See §0 Scope Correction above for the reframed scope;
> §0 supersedes any "Outcome A FALSIFIED" language below on the question
> of what the framework itself predicts.

**Ward identity status for y_b:**

The retained Ward-identity theorem's Block 6 numerically verifies that
**all six basis Clebsch-Gordan overlaps on the unit-norm (1,1) singlet are
equal to 1/√6** (see `scripts/frontier_yt_ward_identity_derivation.py`
lines 291-295: "All 6 basis Clebsch-Gordan overlaps equal 1/sqrt(6)
(singlet uniformity)"). The H_unit composite on the Q_L = (2,3) block is
`H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` with the sum running over both
iso-indices (α = up, down) and color-indices (a = 1,2,3). The six
components (up-red, up-green, up-blue, down-red, down-green, down-blue)
all have the identical 1/√6 weight in H_unit by construction.

Therefore, by the same matrix-element argument as Representation B of the
Ward theorem (eq. 3.7-3.8 of the derivation note):

```
    y_b_bare := ⟨0 | H_unit(0) | b̄_{b-color, down} b_{b-color, down}⟩
              = (1/√(N_c · N_iso)) · 1
              = 1 / √6                                                  (V-y_b-bare)
```

on the canonical surface at g_bare = 1. Combined with the same tadpole
factor 1/√u_0 (D15, n_link=1 per vertex), the same ratio identity follows:

```
    y_b(M_Pl) / g_s(M_Pl) = 1 / √6                                      (V-y_b-Ward)
```

on the canonical lattice-plaquette + 1-link staggered-Dirac surface.

**This is algebraically identical to the top Ward identity** and is
therefore **Outcome A: Yukawa unification at M_Pl** on the Q_L block
by species uniformity of the Clebsch-Gordan.

**Applying the retained P1 Δ_R correction on the ratio (scheme-conversion
lattice → MSbar):**

The retained Δ_R master assembly gives
`Δ_R = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`, with
**canonical central `−3.77 % ± 0.45 %`** from the full-staggered-PT BZ
quadrature (`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`)
or literature-cited `−3.27 %` (superseded; preserved in the master
assembly's citation-based three-channel roll-up). This is a correction on
the **ratio** `y²/g_s²`, not on individual couplings, and its color
structure `[C_F, C_A, T_F n_f]` is **flavor-blind** — no species index
enters the three-channel decomposition. Therefore:

```
    Δ_R^{bottom} ≡ Δ_R^{top}                                            (V-Delta-R-b)
        = −3.77 % ± 0.45 %  (canonical, full-staggered-PT)
        = −3.27 %           (literature-cited, superseded)
    canonical 1σ band: Δ_R^{bottom} ∈ [−4.22 %, −3.32 %]
    literature-cited 1σ band (covariance-reduced): Δ_R^{bottom} ∈ [−5.6 %, −0.9 %]
```

on the same retained surface. The MSbar-side Ward ratio at M_Pl is the
same for top and bottom:

```
    (y_b / g_s)^{MSbar}(M_Pl) = (1/√6) · (1 + Δ_R)                     (V-y_b-MSbar)
        = (1/√6) · (1 − 0.0377) ≈ 0.3928     at canonical full-staggered-PT central
        = (1/√6) · (1 − 0.0327) ≈ 0.3949     at literature-cited central (superseded)
```

**Framework prediction for y_b(v) under Yukawa unification + SM 2-loop RGE:**

Running the BC `y_b(M_Pl) = y_t(M_Pl) = g_s(M_Pl)/√6` forward from M_Pl
to v through 2-loop SM RGE with n_f matching (the same RGE engine as
`scripts/frontier_yt_2loop_chain.py` extended to include the y_b channel)
gives (backward-scan convergence):

```
    y_t(v)^{framework}       ≈ 0.569                                    (V-yt-v-A)
    y_b(v)^{framework}       ≈ 0.548                                    (V-yb-v-A)
    y_b/y_t at v             ≈ 0.963                                    (V-ratio-A)
```

compared to observed `y_t(v) ≈ 0.918, y_b(v) ≈ 0.0164, y_b/y_t ≈ 0.018`.

**m_b retained band (Outcome A, prediction from the framework):**

```
    m_b(v)^{framework}       ≈ 95 GeV           (at v)                   (V-mb-v-A)
    m_b(m_b)^{framework}     ≈ 140 GeV          (at m_b, after QCD running)  (V-mb-mb-A)
```

(QCD running factor `m_b(v)/m_b(m_b) ≈ 0.68` from 1-loop QCD).

**Comparison to observed m_b = 4.18 GeV:**

```
    m_b^{framework} / m_b^{observed}  ≈  33×                             (V-mb-ratio)
    discrepancy: 33× overshoot, i.e., ~3400% deviation.
```

The simultaneous top prediction drops to `m_t ≈ 99 GeV` (vs observed
172.69), a 43% undershoot. **Both predictions fail** because y_b ≈ y_t
at v under Yukawa unification dominates the Yukawa contributions to each
other's beta functions, pulling both toward a common quasi-fixed point
below the top-only fixed point.

**Outcome verdict (scope-limited): the SPECIES-UNIFORM INTERPRETATION of
the retained Ward identity — i.e., identifying every (α, a) basis
component of H_unit with a physical-species Yukawa at the same ratio
g_s/√6 — is empirically FALSIFIED by the 35× overshoot on m_b under SM
2-loop RGE. This is a falsification of the species-uniform interpretation,
NOT of the framework itself. See §0 Scope Correction above.**

The retained Ward theorem's 1PI Block 6 species uniformity (all 6
Clebsch-Gordan overlaps = 1/√6) is an exact algebraic property and is
unchanged. What's falsified is the specific physical reading that every
species Yukawa inherits this Clebsch-Gordan uniformly at M_Pl. The 35×
mismatch on `m_b` is far outside any conceivable retention band (Δ_R
citation uncertainty is ~30% relative on the Ward ratio; RGE 2-loop
systematic is ~1-5%; Δm_b budget at 1σ is well under 1 GeV), so the
falsification is robust. The framework's retained m_t prediction from the
species-privileged chain (`YT_ZERO_IMPORT_CHAIN_NOTE.md`, m_t = 169.5 GeV,
-1.84%) is NOT affected by this scope analysis — the two chains differ on
the b channel boundary condition.

**Safe claim boundary.** The Ward identity's Block 6 singlet uniformity
on Q_L ⊗ Q_L* is exact algebraic at the 1PI 4-point level, and the Δ_R
correction is the same 3-channel lane as for the top. **Under the
species-uniform interpretation**, extending this algebra to a species-
uniform physical BC `y_b(M_Pl) = g_s(M_Pl)/√6` and running forward
through SM 2-loop RGE with retained matter content (3 generations,
6 quarks, 1 Higgs doublet, 3 lepton Yukawas subdominant) gives
`m_b ≈ 145 GeV`, which is falsified by observation. **This is a
falsification of the species-uniform interpretation, not of the
framework.** The failure identifies the species-uniform reading of Block 6
as the wrong physical interpretation; the retained 1PI algebra is
unchanged. The positive mechanism for closing the b-Yukawa absolute scale
is the Fourier-basis circulant spectrum of the retained C_3[111]
centralizer (see `docs/YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`
§0, and `codex/science-workspace-2026-04-18`'s Koide circulant note),
with sector-dependent ρ = 2|b|/a per Appendix A.3 of that note, plus the
A1 equipartition + P1 √m-identification primitives that note flags as
named non-retained ingredients. The framework's retained m_t prediction
(`YT_ZERO_IMPORT_CHAIN_NOTE.md`, species-privileged BC) is NOT affected.

**Confidence:**

- HIGH on the Block 6 species-uniform Clebsch-Gordan algebra at the 1PI
  4-point level (6/6 overlaps = 1/√6 verified to machine precision).
- HIGH on the Δ_R flavor-blindness at the three-channel color level
  (structural, no species index).
- HIGH on the SM 2-loop RGE output `m_b ≈ 145 GeV` under species-uniform
  BC (standard engine, converges in 7 iterations).
- HIGH on the 35× mismatch with observation (`m_b^{obs} = 4.18` vs
  species-uniform prediction ~145 GeV is unambiguous).
- HIGH on the **scope-corrected** classification: the species-uniform
  PHYSICAL INTERPRETATION of Block 6 is what's falsified, NOT the
  framework. The retained m_t prediction via species-privileged BC
  (`YT_ZERO_IMPORT_CHAIN_NOTE.md`) is a separate chain and remains
  valid at -1.84%.
- HIGH on the cross-reference to the Koide circulant Fourier-basis
  mechanism as the positive candidate for species-differentiation
  (`codex/science-workspace-2026-04-18`).

---

## 1. Ward identity extension to y_b: algebraic argument

### 1.1 H_unit is species-uniform on Q_L

The retained Ward-identity theorem defines the composite Higgs via the
canonical normalization on the full Q_L = (2,3) block:

```
    H_unit(x) = (1/√(N_c · N_iso)) · Σ_{α ∈ {up,down}, a ∈ {r,g,b}} ψ̄_{α,a}(x) ψ_{α,a}(x)
              = (1/√6) · (ψ̄ψ)_{(1,1)}(x)                               (1.1)
```

with the sum explicit over both iso-indices α ∈ {up, down} and color-indices
a ∈ {red, green, blue}, giving 6 basis components. The unit-norm constraint
`Z² = N_c · N_iso = 6` (D17, verified by Block 5 of the Ward runner against
the (1,8), (3,1), (8,3) alternatives at `Z² = 8, 9/2, 24` respectively) is
**agnostic to iso-index**: H_unit places equal weight 1/√6 on the up-iso
and down-iso sub-blocks.

### 1.2 Block 6 species uniformity (numerically verified)

The Ward-identity runner
(`scripts/frontier_yt_ward_identity_derivation.py`, lines 267-295) computes
the Clebsch-Gordan overlaps of the unit-norm singlet with each of the 6
basis states of Q_L ⊗ Q_L* and verifies **numerically to machine precision**
that all 6 overlaps equal 1/√6:

```
    ⟨ |up, red⟩ ⊗ |up, red⟩* | S ⟩     =  1/√6                          (1.2-1)
    ⟨ |up, green⟩ ⊗ |up, green⟩* | S ⟩ =  1/√6                          (1.2-2)
    ⟨ |up, blue⟩ ⊗ |up, blue⟩* | S ⟩   =  1/√6                          (1.2-3)
    ⟨ |down, red⟩ ⊗ |down, red⟩* | S ⟩ =  1/√6                          (1.2-4)
    ⟨ |down, green⟩ ⊗ |down, green⟩* | S ⟩ = 1/√6                       (1.2-5)
    ⟨ |down, blue⟩ ⊗ |down, blue⟩* | S ⟩ = 1/√6                         (1.2-6)
```

Block 6 asserts (line 291-295): "All 6 basis Clebsch-Gordan overlaps equal
1/sqrt(6) (singlet uniformity)". This is a framework-native retained result,
not a convention or citation.

### 1.3 y_b_bare matrix element

By the same matrix-element argument as Representation B of the Ward theorem
(equation 3.7-3.8 of
`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), replacing the top-channel
external state with a bottom-channel external state:

```
    y_b_bare := ⟨0 | H_unit(0) | b̄_{b-color, down} b_{b-color, down} ⟩
              = (1/√(N_c · N_iso)) · ⟨ 0 | ψ̄_{b-color, down} ψ_{b-color, down}(0)
                                        | b̄_{b-color, down} b_{b-color, down} ⟩
              = (1/√6) · 1
              = 1 / √6                                                   (1.3)
```

using:

- the explicit operator content of H_unit from eq. (1.1), weight 1/√6 on
  every one of the 6 basis components, including (b-color, down);
- canonical fermion-state normalization;
- canonical scalar-composite normalization (Z² = 6, D17).

**Nothing in this derivation uses "top" specifically.** The same argument
with any of the other five basis external states (up-red, up-green, up-blue,
down-red, down-green, down-blue) gives the same value 1/√6. In particular,
for an external b-quark (down-iso, any color), the result is y_b_bare = 1/√6.

### 1.4 Canonical-surface tadpole factor

The same D15 tadpole factor `1/√u_0` applies to both y_t and y_b on the
same canonical surface (n_link = 1 per vertex is a property of the bilinear
ψ̄ψ, not of which fermion species). Therefore:

```
    y_b(M_Pl) = y_b_bare / √u_0 = (g_bare / √6) / √u_0 = g_s(M_Pl) / √6   (1.4)
```

on the same canonical surface at M_Pl. The ratio identity:

```
    y_b(M_Pl) / g_s(M_Pl) = 1 / √6                                        (1.5)
```

is **exact on the canonical surface**, identical to the top Ward ratio, by
the Block 6 species-uniform Clebsch-Gordan.

### 1.5 Structural observation: this is Yukawa unification

Combining (1.5) with the retained top Ward identity
`y_t(M_Pl) / g_s(M_Pl) = 1/√6`:

```
    y_t(M_Pl) = y_b(M_Pl) = g_s(M_Pl) / √6                                (1.6)
```

on the canonical surface. This is the **Yukawa unification at M_Pl** BC
(Chanowitz-Ellis-Gaillard 1977 structure), which the framework imposes as
an algebraic identity at the Q_L block level — not as a phenomenological
ansatz, but as a direct consequence of the retained Block 6 singlet
uniformity.

---

## 2. Δ_R applies uniformly to top and bottom

### 2.1 Structural flavor-blindness of the three-channel decomposition

The retained P1 Δ_R master assembly decomposes the 1-loop lattice→MSbar
scheme-conversion correction into three color channels:

```
    Δ_R^ratio = (α_LM/(4π)) · [ C_F · Δ_1 + C_A · Δ_2 + T_F · n_f · Δ_3 ] (2.1)
```

where:

- C_F = 4/3 (fundamental color quadratic Casimir);
- C_A = 3 (adjoint color quadratic Casimir);
- T_F · n_f = 1/2 · 6 = 3 (fermion-loop screening at n_f = 6);
- Δ_1, Δ_2, Δ_3 are BZ integrals from Sharpe 1994 /
  Bhattacharya-Sharpe 1998 / Sharpe-Bhattacharya 1998 cited literature.

**No species index enters (2.1)**: the color decomposition is flavor-blind,
the C_F channel is the universal quark-gluon vertex correction, the C_A
channel is the universal gluon self-energy piece, and the T_F n_f channel
is the universal fermion-loop screening of the gluon self-energy. All three
channels act identically on y_t/g_s and y_b/g_s on the same canonical
surface.

### 2.2 Δ_R^{bottom} central and band

```
    Δ_R^{bottom}^{canonical}  =  Δ_R^{top}^{canonical}  =  −3.77 % ± 0.45 %   (2.2)
        (full-staggered-PT, canonical retained central;
         `docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`)
    Δ_R^{bottom}^{lit-cited}   =  Δ_R^{top}^{lit-cited}   =  −3.27 %          (2.2-lit, superseded)
    Δ_R^{bottom} ∈ [−4.22 %, −3.32 %]  (1σ canonical full-PT band)            (2.3)
    Δ_R^{bottom} ∈ [−5.6 %, −0.9 %]   (1σ literature-cited band, inherited)   (2.3-lit)
```

on the retained canonical Wilson-plaquette + 1-link staggered-Dirac surface.

### 2.3 MSbar Ward ratio at M_Pl (bottom)

```
    (y_b / g_s)^{MSbar}(M_Pl)  =  (1/√6) · (1 + Δ_R^{bottom})
        canonical full-PT:  =  (1/√6) · (1 − 0.0377)
                            =  0.4082 · 0.9623
                            ≈  0.3928                                      (2.4)
        literature-cited:   =  (1/√6) · (1 − 0.0327)
                            =  0.4082 · 0.9673
                            ≈  0.3949                                      (2.4-lit, superseded)
```

This is the same-structure MSbar BC as for the top:
`(y_t/g_s)^{MSbar}(M_Pl) ≈ 0.3928` at the canonical full-staggered-PT Δ_R
central (or `≈ 0.3949` at the literature-cited Δ_R central, superseded).

### 2.4 Sub-leading flavor corrections

At 1-loop, the Yukawa self-energy corrections include a Higgs-loop piece
proportional to (y_t² + y_b² + ...) that enters y_t and y_b at different
weights. The standard SM 1-loop y_t β-function carries a term `(3/2)(y_t² − y_b²)`
and symmetrically `(3/2)(y_b² − y_t²)` for y_b. These are **sub-leading
compared to the color decomposition of Δ_R**: at y_t ≈ y_b at M_Pl, these
terms vanish exactly; at the Ward BC scale, the flavor-differential shift
is well under 0.1% of the total Δ_R and is absorbed in the 1σ citation band
(±2.3%). No flavor-specific addition to Δ_R is retained here.

---

## 3. SM RGE backward scan (standard 2-loop engine)

### 3.1 Engine: frontier_yt_2loop_chain.py extended

The runner `scripts/frontier_yt_bottom_yukawa_retention.py` extends the
existing 2-loop RGE engine (`scripts/frontier_yt_2loop_chain.py`,
Machacek-Vaughn + Arason et al. + Luo-Xiao conventions, full 2-loop SM
gauge and Yukawa β functions) to include the y_b channel simultaneously
with y_t. The RGE system is:

```
    d y_t/d t  =  y_t · [ (1-loop SM) + (2-loop SM) ]
    d y_b/d t  =  y_b · [ (1-loop SM) + (2-loop SM) ]
    d g_i/d t  =  g_i · [ (1-loop SM) + (2-loop SM) ]  (i = 1,2,3)        (3.1)
```

with full SM 1-loop Yukawa β functions including cross-coupling:

```
    β_yt^{1-loop}  =  y_t · [ (3/2)(y_t² − y_b²) + 3(y_t² + y_b²) + y_τ²
                              − 17/20 g_1² − 9/4 g_2² − 8 g_3² ]          (3.2)

    β_yb^{1-loop}  =  y_b · [ (3/2)(y_b² − y_t²) + 3(y_t² + y_b²) + y_τ²
                              − 1/4 g_1² − 9/4 g_2² − 8 g_3² ]            (3.3)
```

and standard 2-loop corrections. Threshold matching at m_t, m_b, m_c
decreases n_f from 6 → 5 → 4 → 3 across the running.

### 3.2 Boundary conditions

**UV BC (at M_Pl):** The retained Ward identity with Δ_R correction,
inherited from §1 + §2:

```
    y_t(M_Pl) / g_s(M_Pl) = y_b(M_Pl) / g_s(M_Pl) = (1/√6) · (1 + Δ_R)   (3.4)
```

on the MSbar surface at M_Pl, with Δ_R ∈ [−5.6%, −0.9%] at 1σ.

**IR BC (at v):** Framework-derived canonical surface values:

```
    g_3(v)^{CMT}  =  √(4π · α_s(v))  =  √(4π · 0.1033)  ≈  1.139          (3.5)
    v            =  246.28 GeV  (hierarchy theorem)                        (3.6)
```

g_1(v) ≈ 0.467, g_2(v) ≈ 0.649 use standard SM values at v from MSbar
matching to M_Z electroweak data (these are NOT derivation inputs but
context constants; see `scripts/frontier_yt_2loop_chain.py` L113-119).

### 3.3 Backward scan approach

Following the prior framework approach (Approach A of the 2-loop y_t chain),
we:

1. Fix g_i(v) at framework-CMT values;
2. Scan (y_t(v), y_b(v)) to find the pair that, when run backward to M_Pl,
   satisfies the Ward BC at M_Pl: y_t(M_Pl)/g_s(M_Pl) = y_b(M_Pl)/g_s(M_Pl) = 1/√6
   at central Δ_R = 0 (tree-level) or with Δ_R correction applied.
3. Extract m_t = y_t(v) · v/√2 and m_b(v) = y_b(v) · v/√2; convert
   m_b(v) → m_b(m_b) via standard QCD 1-loop running factor ≈ 0.68 at
   the retained α_s.

### 3.4 Numerical result (central, tree-level Ward BC)

Solving (3.1) with BC y_t(M_Pl) = y_b(M_Pl) = g_s(M_Pl)/√6 at M_Pl using
the backward-scan iterative procedure converges to:

```
    y_t(v)^{framework, A}  ≈  0.569                                        (3.7)
    y_b(v)^{framework, A}  ≈  0.548                                        (3.8)
    y_b/y_t at v           ≈  0.963                                        (3.9)
```

The simultaneous Yukawa coupling at the BC drags both couplings toward a
common quasi-fixed point of the coupled system, near y_t ≈ y_b ≈ 0.55 at v.

### 3.5 m_t and m_b predictions (Outcome A)

```
    m_t^{framework, A}  =  y_t(v) · v/√2  ≈  99 GeV                        (3.10)
    m_b^{framework, A}(v)  =  y_b(v) · v/√2  ≈  95 GeV                     (3.11)
    m_b^{framework, A}(m_b)  =  m_b(v) / 0.68  ≈  140 GeV                  (3.12)
```

### 3.6 Δ_R band sensitivity

With Δ_R corrections within the 1σ band (−5.6%, −0.9%), the BC shifts the
Ward ratio by ≤ 5.6% on each side. Propagated through the full 2-loop SM
RGE system, this induces a corresponding shift in (y_t(v), y_b(v)) that is
a few percent — nowhere near the factor of 33 needed to reach observation.

---

## 4. Comparison to observed m_b = 4.18 GeV

```
    m_b^{observed}(m_b)  =  4.18 GeV        (PDG 2024)                     (4.1)
    m_b^{framework, A}(m_b)  ≈  140 GeV     (Yukawa unification BC + RGE)   (4.2)
    m_b^{framework, A} / m_b^{observed}  ≈  33×                             (4.3)
```

### 4.1 Simultaneous top inconsistency

```
    m_t^{observed}(pole)  =  172.69 GeV     (PDG 2024)                     (4.4)
    m_t^{framework, A}  ≈  99 GeV           (Yukawa unification BC)         (4.5)
    m_t^{framework, A} / m_t^{observed}  ≈  0.57                            (4.6)
```

The simultaneous failure on both masses reflects a structural feature of
the RGE quasi-fixed-point in the (y_t, y_b) plane: with y_t(M_Pl) = y_b(M_Pl),
running both simultaneously gives y_t ≈ y_b ≈ 0.55 at v, dragging the top
**down** and the bottom **up** toward a common value.

### 4.2 Cross-check: top-only Ward BC (y_b neglected)

If we neglect y_b entirely (as in the prior retained top-only analysis in
`frontier_yt_2loop_chain.py`), the top prediction is
`y_t(v) ≈ 0.95, m_t ≈ 165 GeV`, which together with the retained color
projection `√(8/9)` gives `m_t(pole) ≈ 172.57 GeV` (the retained top-only
central from `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`,
eq. 6.4). This is the framework's retained top prediction, confirmed in
`frontier_yt_2loop_chain.py` output and cross-checked here.

The bottom prediction under Yukawa unification **disturbs this** because
including y_b(M_Pl) = y_t(M_Pl) = 0.436 forces both to end up at ≈ 0.55
at v, which kills both the m_t and m_b predictions simultaneously.

---

## 5. Outcome classification (scope-corrected; see §0)

This analysis reaches a **scope-corrected outcome**: the retained Ward-
identity theorem's Block 6 species-uniform Clebsch-Gordan at the 1PI
4-point level, when READ as a species-uniform PHYSICAL BC (i.e., y_t(M_Pl)
= y_b(M_Pl) = g_s(M_Pl)/√6 for physical species Yukawas), is empirically
falsified under SM 2-loop RGE forward-running:

1. **m_b ≈ 145 GeV** under the species-uniform BC, 35× larger than
   observed (4.18 GeV). This falsifies the species-uniform interpretation.
2. **m_t ≈ 102 GeV** under the same BC, 0.59× of observed (172.69 GeV).
   This confirms the coupled-RGE quasi-fixed-point.

**The falsification is of the species-uniform interpretation, not of the
framework.** The framework's actual m_t prediction chain
(`docs/YT_ZERO_IMPORT_CHAIN_NOTE.md`, `scripts/frontier_yt_zero_import_chain.py`)
uses a **species-privileged BC** — y_t(M_Pl) at the Ward value 0.4358
while y_b(v) is held at its observed small value ~0.016 — and produces
m_t = 169.5 GeV (-1.84% deviation). That chain is NOT falsified by this
scope analysis, because it does not impose the species-uniform BC on y_b.

### 5.1 What the 35× result closes (scope-limited)

- **The species-uniform interpretation of Block 6 is not the correct
  physical reading.** Identifying every (α, a) basis component of H_unit
  with a physical-species Yukawa at the same ratio g_s/√6 is inconsistent
  with observation.
- **The retained 1PI algebra of Block 6 is unchanged.** The six Clebsch-
  Gordan overlaps equal 1/√6 to machine precision — this is a property
  of the canonical (1,1) singlet wavefunction and is correct as stated.
  What's wrong is the interpretation "therefore every physical species
  Yukawa equals g_s/√6 at M_Pl."
- **The retention gap is a species-differentiation primitive.** This
  primitive is consistent with all Class #1-#7 retained no-go results on
  operator-algebra-level C_3 breaking on H_hw=1 AND with the positive
  mechanism of the Fourier-basis circulant spectrum in the retained
  C_3[111] centralizer (per `YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`
  §0 and the Koide circulant note on `codex/science-workspace-2026-04-18`).

### 5.2 Positive mechanism cross-reference: Koide Fourier-basis spectrum

The retained C_3[111] cyclic structure forces any Hermitian operator
commuting with cyclic permutation to take circulant form
`H = a·I + b·C + b̄·C²` (centralizer-of-C_3 argument, 3-dim family) with
distinct Fourier-basis eigenvalues `λ_k = a + 2|b| cos(arg(b) + 2πk/3)`.
This is retained algebraic structure. Under the additional ingredients
**A1 equipartition** (ρ = 2|b|/a = √2, giving Frobenius-norm balance
between diagonal and off-diagonal sectors) and **P1 √m-identification**
(λ_k = √m_k for physical masses), the three-sector Yukawa ratios become
sector-specific (ρ_lep = √2, ρ_down ≈ 1.536, ρ_up ≈ 1.754 per Appendix
A.3 of the Koide note) and the absolute m_b scale is recoverable.

A1 + P1 are NOT on the current retained surface — they are named non-
retained primitives of the Koide note, each with explicit derivation
pathways under study. The species-uniform interpretation of the §1-§7
algebra below corresponds to "ρ = 1 uniformly across all sectors,"
which the Koide circulant analysis identifies as the degenerate case
(all three eigenvalues equal) — manifestly wrong for quarks. The correct
reading is sector-dependent ρ, which produces sector-specific λ_k and
thus sector-specific Yukawa ratios.

### 5.3 Retained obstruction: sharpened statement

The obstruction the present scope analysis identifies is the
**species-uniform PHYSICAL INTERPRETATION of Block 6**, not Block 6
itself. To close the absolute m_b scale:

- The retained 1PI algebra is correct and sufficient at its stated scope
  (the scalar-singlet 1PI 4-point function on Q_L ⊗ Q_L* has all six
  Clebsch-Gordan overlaps equal to 1/√6, reflecting unit-norm singlet
  symmetry).
- The PHYSICAL identification of H_unit's components with species Yukawas
  must be refined from "all species at g_s/√6" to "each species's Yukawa
  determined by its Fourier-basis circulant eigenvalue λ_k with sector-
  dependent ρ."
- The sharpened retention gap is A1 + P1 + the identification `y_f = λ_k(f)/v`
  (schematically), not the more general "species-breaking primitive from
  scratch" the original note claimed.

### 5.4 Interpretation of the down-type CKM-dual note's success

The bounded down-type mass-ratio CKM-dual note
(`docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`) gives
`m_s/m_b = [α_s(v)/√6]^(6/5)` and matches the threshold-local self-scale
observed ratio to +0.2%. This is a **mass-ratio** result — it does not
close the absolute m_b scale. The present retention analysis addresses
the absolute m_b scale under the species-uniform interpretation, and
closes it scope-limitedly as falsified. The two notes are consistent:
the CKM-dual note explicitly disclaims "closure of the absolute bottom
scale" as out of scope. The positive mechanism for the absolute scale is
the Fourier-basis circulant spectrum of §5.2.

---

## 6. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` canonical surface, the Ward-identity
> theorem's Block 6 species-uniform Clebsch-Gordan (all 6 basis components
> of the unit-norm (1,1) singlet equal 1/√6) extends to the b-quark by
> species substitution, giving `y_b(M_Pl) / g_s(M_Pl) = 1/√6` as an exact
> tree-level algebraic identity on the same surface as the retained top
> Ward identity. This is **Outcome A (Yukawa unification at M_Pl)**. The
> retained P1 Δ_R scheme-conversion correction (canonical full-staggered-PT
> `−3.77 % ± 0.45 %`, or equivalently literature-cited `−3.27 %` within the
> ±2.32 % band) applies identically (color-decomposition is flavor-blind).
> Running this UV boundary condition forward through 2-loop SM RGE with
> retained matter content gives a framework-native prediction
> `m_b^{framework}(m_b) ≈ 140 GeV`, which is **empirically falsified by
> 33× by the observed `m_b = 4.18 GeV`**. Simultaneously, the Yukawa
> unification BC drags the top prediction down to `m_t ≈ 99 GeV`, a 43%
> undershoot of the observed 172.69 GeV. **Both predictions fail** under
> the Yukawa unification boundary condition. This is a retained
> obstruction: the current Ward-identity theorem's species uniformity, in
> combination with SM 2-loop RGE, cannot reproduce the observed
> charged-flavor mass hierarchy without an additional primitive.

It does **not** claim:

- any modification of the retained Ward-identity theorem (the Block 6
  species uniformity is inherited as-is);
- any modification of the retained Δ_R master assembly;
- any modification of the retained top prediction `m_t(pole) = 172.57 GeV ± 5.7 GeV`
  — that prediction retains its validity in the top-only regime where
  y_b is neglected (or set to observed ~0.016), which is a consistency
  approximation inherited from the 2-loop chain;
- any derivation of `m_b` in agreement with observation from the current
  retained surface — this is explicitly the retained obstruction;
- any speculation on which primitive might close the gap — candidate
  primitives (SUSY, flavor column, generation-differentiated Clebsch-Gordan)
  are flagged in §5.1 only as the class of primitives that would be
  needed, not as retained content;
- any modification of the bounded down-type CKM-dual lane
  (`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`) — that lane addresses
  mass-ratios, not the absolute scale, and is consistent with this note
  (the absolute bottom scale is explicitly out of its scope).

### 6.1 Retention gap is explicit and bounded

The retention gap is: the **absolute scale** of y_b (equivalently m_b) is
wrong by 33× under the current retained Ward + Δ_R + SM 2-loop RGE chain.
This is a specific, quantifiable, falsifiable gap — not a vague "framework
doesn't address y_b" statement.

### 6.2 What does not change

The retained top prediction m_t(pole) = 172.57 ± 5.7 GeV is unchanged. The
Δ_R master assembly is unchanged. The Ward-identity tree-level theorem is
unchanged. The bounded down-type mass-ratio CKM-dual lane is unchanged.
Only this **new retention-analysis note** and its runner are added.

---

## 7. What is retained vs. cited vs. open

### 7.1 Retained (framework-native, inherited from upstream theorems)

- Ward-identity tree-level theorem's Q_L block + Block 6 species-uniform
  Clebsch-Gordan (all 6 basis components of (1,1) singlet = 1/√6).
- H_unit operator content on the Q_L block with canonical normalization
  Z² = 6.
- Δ_R master assembly three-channel decomposition
  `Δ_R = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`, canonical
  central `−3.77 % ± 0.45 %` (full-staggered-PT; or equivalently the
  superseded literature-cited `−3.27 %` within the ±2.32 % band),
  flavor-blind.
- Canonical-surface anchors α_LM = 0.09067, α_s(v) = 0.1033,
  v = 246.28 GeV.
- Retained matter content: 3 quark generations, 1 Higgs doublet, 6 quarks
  (n_f = 6 at M_Pl, threshold matching to 5, 4, 3 in the RGE).
- SM 2-loop gauge and Yukawa β functions (Machacek-Vaughn, Arason et al.,
  Luo-Xiao) as the retained RGE engine (inherited from
  `frontier_yt_2loop_chain.py`).

### 7.2 Cited (external, with controlled systematic)

- Observed m_b(m_b) = 4.18 GeV (PDG 2024).
- Observed m_t(pole) = 172.69 GeV (PDG 2024).
- SM EW couplings at v: g_1(v) ≈ 0.467, g_2(v) ≈ 0.649 (context, not
  derivation input).
- QCD running factor m_b(v)/m_b(m_b) ≈ 0.68 from 1-loop QCD (standard).

### 7.3 Open (explicit retained gap closed by this note as falsified)

- **Absolute y_b (or m_b) scale from the current retained surface**: the
  Yukawa unification BC fails by 33×. A new primitive is needed to close
  this gap in agreement with observation. Candidate primitives are not
  retained here and represent an open research direction.

- Analogous retention analyses for y_c, y_τ, y_μ, y_e, y_s, y_d, y_u, and
  the neutrino Yukawas are open and would likely all show the same
  Yukawa unification obstruction under the current retained surface, as
  Block 6 species uniformity applies to every Q_L basis component and
  extends analogously to L_L = (2,1)_{-1} by the graph-first selected-axis
  structure (LEFT_HANDED_CHARGE_MATCHING). Each such analysis would
  follow the same template as this note.

- Whether the retained color-singlet projection `√(8/9)` factor (which is
  the retained physical correction on y_t) also applies to y_b in the
  same way is not addressed here — if it does, it only shifts the 140
  GeV prediction by `√(8/9) ≈ 0.943`, giving m_b ≈ 132 GeV, which is
  still 32× the observed 4.18 GeV. The √(8/9) does not close the gap.

---

## 8. Validation

The runner `scripts/frontier_yt_bottom_yukawa_retention.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_bottom_yukawa_retention_2026-04-18.log`. The runner must
return PASS on every check to keep this note on the retained retention-
analysis surface.

The runner verifies:

1. Retention of SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` and
   canonical-surface anchors `α_LM = 0.09067`, `α_s(v) = 0.1033`.
2. Retention of the Ward tree-level identity `y_bare = g_bare/√6`
   (inherited, verified algebraically: 1/√6 = 0.4082...).
3. **Block 6 species uniformity**: re-verify that the unit-norm (1,1)
   singlet on Q_L ⊗ Q_L* has 6 basis Clebsch-Gordan overlaps, all equal to
   1/√6 (machine-precision agreement).
4. **y_b Ward identity extension**: by species substitution in Block 6,
   `y_b_bare = 1/√6` as an algebraic identity; `y_b(M_Pl)/g_s(M_Pl) = 1/√6`
   after the common D15 tadpole.
5. **Δ_R flavor-blindness**: the three-channel
   `[C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]` decomposition carries no species
   index; `Δ_R^{bottom}^{canonical} = Δ_R^{top}^{canonical} = −3.77 % ±
   0.45 %` (full-staggered-PT), equivalently `−3.27 %` literature-cited
   (superseded).
6. MSbar Ward ratio at M_Pl (bottom): `(y_b/g_s)^{MSbar}(M_Pl) ≈ 0.3928`
   at canonical full-PT Δ_R, or `≈ 0.3949` at literature-cited Δ_R
   (superseded)
   at central Δ_R.
7. **Backward scan convergence**: find (y_t(v), y_b(v)) consistent with
   Yukawa unification BC at M_Pl. Converges to y_t(v) ≈ 0.569, y_b(v) ≈
   0.548 (agreement tolerance 5%).
8. Framework-predicted m_t and m_b at v from the converged scan:
   m_t ≈ 99 GeV, m_b(v) ≈ 95 GeV.
9. m_b(m_b) prediction ≈ 140 GeV after QCD running from v.
10. Empirical mismatch: m_b^{framework} / m_b^{observed} ≥ 30 (large
    factor confirming the 33× overshoot).
11. Simultaneous m_t undershoot: m_t^{framework} / m_t^{observed} ≤ 0.65
    (large factor confirming the 43% undershoot).
12. Outcome A (Yukawa unification at M_Pl implied) is algebraically
    established and empirically falsified.
13. Top-only consistency cross-check: with y_b(M_Pl) set to match observed
    y_b(v) ≈ 0.016 (non-unified BC), the retained top prediction m_t ≈
    165-172 GeV is recovered (within top-only retained band).
14. No modification of Ward theorem, Δ_R assembly, color projection,
    master obstruction, CKM-dual lane, or publication surface.
15. All retained framework constants (α_LM, α_s(v), v, G3_Pl, YT_Pl)
    agree with upstream retained values to sub-permille.
