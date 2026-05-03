# Higgs Mass + Vacuum Stability — New-Physics Discrimination Tests

**Date:** 2026-05-03
**Type:** bounded_theorem
**Role:** discrimination-test sharpening note
**Claim scope:** identify the framework's specific discriminating predictions
in the Higgs / y_t / vacuum-stability lane, frame them as **falsification
tests vs the SM**, compute current and near-future experimental
discrimination, and identify which precision improvements would
falsify the framework. NOT a closure of the m_H value (which has
documented internal version conflict 119.8/125.1/129.7 GeV reflecting
bounded systematic across derivation routes).
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_higgs_vacuum_stability_new_physics_discrimination.py`

## 0. Question

The framework's prior cycle 11 audit (PR [#271](https://github.com/jonathonreilly/cl3-lattice-framework/pull/271))
demoted `HIGGS_MASS_FROM_AXIOM_NOTE` to support tier with the obstruction:
"lattice curvature ↔ (m_H/v)² matching theorem missing." Rather than
re-attempting the matching theorem (cluster obstruction, multi-month
research), this note **reframes the lane as a discrimination test**:
what does the framework predict that the SM doesn't, and how testable is
that distinction?

## Cited authorities (one hop)

- [`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
  — records the cycle 11 demotion and the missing
  lattice-curvature ↔ `(m_H/v)^2` matching theorem.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — historical Higgs-mass target note being reframed here as bounded
  discrimination rather than exact closure.
- [`HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md`](HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
  — carries the existing vacuum-stability / CW-boundary systematic surface.
- [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md)
  — carries the hierarchy-correction route whose value spread is treated
  here as bounded systematic.
- [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
  — current open-gate parent for the y_t Ward identity surface.
- [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md)
  — prior y_t chain surface used here only as a bounded internal input.
- [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)
  — records the matching-cluster obstruction that prevents exact m_H closure.

External comparators and literature inputs are admitted as comparators, not
framework derivations: PDG-style `m_t`, `m_H`, `α_s` extractions; Buttazzo et
al. 2013 and Bednyakov et al. 2015 SM stability-boundary calculations; and
published/future collider precision targets. These imports are used only to
state falsification thresholds.

## 1. Framework's distinguishing predictions in this lane

| # | Prediction | Framework value | SM/PDG | Distinguishability |
|---|---|---|---|---|
| D1 | Vacuum stability | **absolutely stable** | metastable (with current y_t) | binary YES/NO test |
| D2 | y_t(v) | **0.918** (bounded internal value; no PDG fit for y_t) | 0.94 ± 0.01 (extracted from m_t) | continuous (current ~0.75σ with the stated 3% framework systematic) |
| D3 | m_H value | 119.8–129.7 GeV (bounded systematic) | 125.25 ± 0.17 GeV (PDG free param) | tight central value, framework's range overlaps |
| D4 | λ(M_Pl) | conditionally 0 on the CW-boundary surface | varies by extraction | precision λ at high scale |

## 2. The KEY discrimination: vacuum stability

The strongest single distinguishing claim is **absolute vacuum stability**.

**Standard Model vacuum stability landscape (Buttazzo et al 2013; Bednyakov et al 2015):**
- With y_t = 0.940 ± 0.005 (NNLO extraction from m_t = 172.5 GeV), m_H = 125.25 GeV
- λ(M_Pl) crosses zero at scale Λ_inst ~ 10¹⁰⁻¹² GeV
- Vacuum is **metastable** with tunneling lifetime >> Hubble time (so observationally fine)
- Stability boundary requires y_t ≲ 0.93 (m_t ≲ 171.5 GeV) at fixed m_H = 125.25

**Framework prediction:**
- y_t(v) = 0.918 (below the stability boundary)
- λ(M_Pl) = 0 on the conditional CW-boundary surface (not a fit, but still
  bounded by the open bridge chain listed above)
- Vacuum is **absolutely stable**

**Discrimination test:** any precision measurement whose lower 5σ bound is
above the stability boundary `y_t ≈ 0.93` (or equivalently the corresponding
top-mass boundary at fixed `m_H = 125.25`) would falsify the framework's
stability claim. Current PDG-style y_t extraction sits at ~0.94 ± 0.01,
about 1σ above the stability boundary and about 0.75σ above the framework's
bounded internal value once the stated 3% framework systematic is included.

| Quantity | Framework | SM / PDG | Tension |
|---|---|---|---|
| y_t(v) | 0.918 ± 3% systematic | 0.940 ± 0.010 | ~0.75σ including framework systematic |
| m_t (pole) | 172.57–173.10 GeV (2L–3L) | 172.69 ± 0.30 GeV | <1σ (within bounded systematic) |
| Stability | absolutely stable | metastable (98% confidence per Buttazzo et al) | binary, currently weakly favoring SM |

**Critical experiment:** ATLAS/CMS top mass program at HL-LHC (2030+) targets
δm_t ~ 100 MeV (vs current 300 MeV). FCC-ee threshold measurements would
sharpen the observational side further. Direct resolution of the y_t = 0.918
vs 0.940 distinction at >3σ also requires narrowing the current 3%
framework-side transport systematic.

## 3. The KEY tension: y_t(v) = 0.918 vs 0.940

The framework's y_t(v) = 0.918 is derived from:
- y_t(M_Pl) / g_s(M_Pl) = 1/√6 (existing Ward-identity surface; currently an open-gate / bounded input under the audit ledger)
- Standard SM running from M_Pl to v (admitted bridge)
- Bounded ~3% QFP/RGE-surrogate systematic

The SM extraction y_t = 0.94 ± 0.01 uses:
- m_t pole (PDG, observed)
- αs(M_Z) (PDG, observed)
- Standard Higgs sector

The framework value is an internal framework value rather than a PDG fit for
y_t, but it is not a repo-wide retained theorem here: the comparison is
bounded by the y_t Ward-identity gate, the SM-running bridge, and the 3%
QFP/RGE-surrogate systematic. The SM extraction is observation-driven
(uses `m_t`, `m_H`, and `α_s` inputs).

**Net discrimination:** if precision-LHC + future colliders establish that
`y_t` lies above the stability boundary with a lower 5σ bound above ~0.93,
the framework's stability claim is falsified. A direct falsification of the
central `y_t(v)=0.918` value also requires reducing the current framework-side
3% systematic or replacing it with a narrower audited transport bound.

## 4. Why this is a beyond-SM discrimination surface

The user's net-call required: "anything that distinguishes the framework
from 'the SM, written in lattice notation.'"

The framework's y_t(v) = 0.918 + vacuum stability prediction satisfies this:
- The framework PREDICTS vacuum stability from CW + λ(M_Pl)=0 + Ward chain
- The SM does NOT predict stability — m_H, y_t are free parameters and
  the stability conclusion depends on those input values
- A SM-with-correct-fits matches observation; a FRAMEWORK that predicts
  these values differently (specifically, y_t lower than SM extraction)
  is making a bounded claim beyond SM

**Honest caveat:** the framework's y_t(v) = 0.918 vs SM extraction 0.94 is
only ~0.75σ once the stated 3% framework systematic is included; it is not
currently a smoking-gun discrimination. Future precision can falsify the
stability claim if it pushes the lower error bar above the stability boundary,
but direct y_t discrimination also needs a narrower framework-side transport
systematic.

## 5. Discrimination experiment timeline

| Experiment | Target precision | Discriminates |
|---|---|---|
| HL-LHC (2030+) | δm_t ~ 100 MeV; precision λ_3 H self-coupling at 50% | y_t to <1%; vacuum stability via λ at v |
| FCC-ee (proposed 2040s) | δm_t ~ 25 MeV at threshold scan; m_H to 4 MeV | y_t to ~0.1%; m_H to 0.003% |
| FCC-hh (proposed 2050s) | λ_3 to 5% | direct stability test via λ shape |
| Linear collider (ILC/CLIC, proposed) | δm_t ~ 30 MeV; m_H to 14 MeV | y_t / vacuum stability |

## 6. Honest status

```yaml
actual_current_surface_status: bounded discrimination-test sharpening note + named-obstruction stretch
target_claim_type: bounded_theorem
conditional_surface_status: bounded by HIGGS_MASS_FROM_AXIOM cycle 11 demotion (PR #271)
hypothetical_axiom_status: null
admitted_observation_status: PDG-style m_t/m_H/alpha_s comparators, literature stability-boundary calculations, and standard SM running from M_Pl to v (admitted bridge)
claim_type_reason: |
  This note REFRAMES the m_H lane as a falsification test rather than
  attempting m_H closure (which faces the cluster obstruction documented
  in cycle 13 / PR #274). The framework's distinguishing predictions
  (vacuum stability, y_t(v) = 0.918, λ(M_Pl) = 0) remain conditional on
  prior bridges, open gates, and comparator imports, but they define
  specific falsification thresholds.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Reframing-and-sharpening note; not a derivation of m_H value.
  Audit ratification of underlying y_t/vacuum-stability chain required
  before retained-grade promotion.
```

## 7. What this note closes

- **Reframes** the m_H lane: from "predict m_H exactly" (cluster-obstructed)
  to "predict discriminating signatures vs SM" (testable now and near-term)
- Identifies y_t(v) = 0.918 vs SM 0.940 as a current ~0.75σ discrimination
  once the stated framework systematic is included
- Identifies vacuum stability vs metastability as a binary discrimination
- Connects to specific experiments (HL-LHC, FCC-ee, FCC-hh, linear collider)
- Provides quantitative falsification thresholds

## 8. What this note does NOT close

- The m_H value version conflict (119.8/125.1/129.7) — bounded systematic
- The lattice-curvature ↔ (m_H/v)² matching theorem (cluster obstruction)
- The y_t(v) = 0.918 derivation (carried by existing y_t surfaces; not
  re-ratified here)
- A claim that the framework currently falsifies SM (it doesn't; only
  identifies what would)

## 9. Cross-references

- Parent (demoted cycle 11): [`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
- Parent (audited): [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
- Vacuum stability infrastructure: `HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md`
- Hierarchy correction analysis: `HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`
- y_t lane: `YT_*` notes; `ALPHA_S_DERIVED_NOTE.md`
- Cluster obstruction: [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)
- Standard SM stability references: Buttazzo et al 2013 ([arXiv:1307.3536](https://arxiv.org/abs/1307.3536)); Bednyakov et al 2015 ([arXiv:1502.04404](https://arxiv.org/abs/1502.04404))
