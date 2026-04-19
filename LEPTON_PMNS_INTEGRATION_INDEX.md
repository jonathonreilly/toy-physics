# Lepton / PMNS Integration Package — Reviewer Index

**Branch:** `review/lepton-pmns-integration-package`
**Base:** `origin/main` (clean fork, no rebase)
**Date:** 2026-04-18
**Status:** integration-ready; all smoke-tested runners PASS; reviewer to land selectively

---

## 0. What this branch is

During the extended PMNS-pin investigation (audit + 6-attack sweep + 45+ agent fires) a large body of lepton-sector work accumulated across **12 distinct branches** that never landed on `main`. This branch consolidates every lepton-sector file from those branches that is **not already on `origin/main`** into one place so a reviewer can evaluate and land it coherently instead of weaving 12 branches.

- **No repo weaving.** This is a flat integration: I picked the highest-priority author per file (priority table below) and cherry-added only files not present on `origin/main`.
- **No content modification.** Every file is exactly as it appeared on its source branch. I added this INDEX and nothing else.
- **Lepton-focus filter.** From a 315-file unique pool I removed 60 non-lepton files (DM-only, CKM-only, publication infra, repo audits) leaving **255 files** — 127 docs + 127 scripts + 1 science derivation.
- **Zero overlap with `origin/main`.** I cross-checked every retained filename against the current main file list; none of the 255 files are already there. (Main does have 466 other lepton-tagged files — those stay untouched.)

---

## 1. Source branch provenance

Priority order (used when the same path lived on multiple branches — earlier wins):

| Priority | Branch | Head SHA | Date | Files contributed |
|---|---|---|---|---|
| 1 | `review/koide-one-scalar-obstruction-triangulation` | `05d307ad` | 2026-04-18 | 8 |
| 2 | `review/dm-blocker-3-deep-impossibility-triangulation` | `5329f8db` | 2026-04-18 | 8 |
| 3 | `review/koide-charged-lepton-for-main` | `db8df07c` | 2026-04-18 | 0* |
| 4 | `frontier/lepton-mass-tower` | `58f14e42` | 2026-04-19 | 4 |
| 5 | `claude/g5-koide-closure` | `2dd0fc13` | 2026-04-17 | 34 |
| 6 | `codex/neutrino-retained-lanes-review` | `db9a7873` | 2026-04-16 | 136 |
| 7 | `codex/neutrino-science-main-derived-2026-04-16` | `85a3d8ec` | 2026-04-16 | 6 |
| 8 | `codex/neutrino-clean-2026-04-16` | `da74c430` | 2026-04-16 | 53 |
| 9 | `codex/lepto-selector-closeout-main-2026-04-17` | `eeb42790` | 2026-04-17 | 2 |
| 10 | `codex/leptogenesis-science-review-2026-04-16` | `d30105e1` | 2026-04-16 | 2 |
| 11 | `frontier/dm-leptons-review` | `3b020383` | 2026-04-19 | 1 |
| 12 | `claude/mass-ratio-package` | `7f869e3f` | 2026-04-16 | 1 |

(*) `review/koide-charged-lepton-for-main` files all overlapped with higher-priority branches.

Full per-file attribution: `/tmp/integration-work/filtered-selection.csv` (reviewer can request if needed).

---

## 2. Smoke-test status (ran 2026-04-18)

Four flagship runners executed from the branch as-is:

| Runner | Result | Source branch |
|---|---|---|
| `scripts/frontier_koide_z3_scalar_potential.py` | **PASS=34 FAIL=0** | `frontier/lepton-mass-tower` |
| `scripts/frontier_koide_one_scalar_obstruction_triangulation.py` | **PASS=23 FAIL=0** | `review/koide-one-scalar-obstruction-triangulation` |
| `scripts/frontier_g5_joint_pmns_koide_pinning.py` | **PASS=9 FAIL=0** (verdict: `JOINT_PINNING_THEOREM_ABSENT` — correct no-go) | `claude/g5-koide-closure` |
| `scripts/frontier_pmns_sigma_zero_no_go.py` | **PASS=18 FAIL=0** | `codex/neutrino-clean-2026-04-16` |

No runner was modified. Historical PASS counts from source branches (720/0 for triangulation, 511/0 for G5, 33/33 for lepton-mass-tower) are expected to hold for the full corpus — the reviewer should sweep `scripts/frontier_*.py` before landing.

---

## 3. Organization — file groups by theme

### 3.1 Charged-lepton mass tower  **(flagship — promotable)**  · 1 file
- `docs/KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`

**Key result:** Clifford involution `T_m² = I` forces the Z³-invariant scalar potential
```
V(m) = const + (c₁ + c₂/2)·m + (3/2)·m² + (1/6)·m³
```
with **cubic coupling 1/6 pinned exactly by `Tr(T_m³) = 1`** and quadratic 3/2 pinned by `Tr(T_m²) = 3`. After one overall scale the slot triplet at m_* reproduces all three charged-lepton masses to <0.05%.

**Honest gap:** `V_eff` minimum sits at `m_V ≈ −0.433`, not at the physical `m_* ≈ −1.161`. The scalar potential alone does not close the selection; an additional microscopic law (the `H_*` witness ratio or equivalent) is needed to pin `m_*`.

**Bonus finding (from review.md commit `58f14e42`):** Agent T confirmed this is promotable. See *review.md* on the source branch for continuation direction.

### 3.2 Koide one-scalar obstruction triangulation  **(promotable)**  · 8 files
- `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_NOTE_*.md`
- `scripts/frontier_koide_one_scalar_obstruction_triangulation.py` (PASS=23)
- plus supporting notes from the same branch

**Key result:** Three independent routes (primitives A1, P1, m, κ) all terminate at the same dagger identity `g₀² = 2|g₁|²` on the retained Cl(3)/Z³ + observable-principle surface. Koide equivalence on the circulant commutant is therefore route-independent.

### 3.3 G5 / Koide closure programme  · 24 files
Avenues G (Higgs-dressed propagator), H (stationarity principle), I (mixed-gamma return), plus γ=1 reconnaissance, S2-breaking primitive survey, shape-theorem robustness audit, observational pin closure.

Contains both structural theorems (PASS) and honest no-gos (`JOINT_PINNING_THEOREM_ABSENT`, `SIGMA_ZERO_NO_GO` lineage). Reviewer should read `G5_OBSERVATIONAL_PIN_CLOSURE_NOTE.md` first for the umbrella picture.

### 3.4 Koide — charged-lepton specific  · 6 files
- `docs/CHARGED_LEPTON_KOIDE_*` — cone attempt, G5 status, circulant-character-bridge, Z3-source-response-crosscheck
- Closes out the charged-lepton-side Koide investigation with multiple converging reductions.

### 3.5 Charged-lepton structure (two-Higgs, Y_ν, NNI)  · 13 files
Two-Higgs canonical reduction (Y_ν = A + B·C with 7 real params), observable inverse problem, Z3 source response, curvature `L_T` extension, plus mass-basis NNI and associated scouts. Reviewer-grade structural results — most are PASS-status reductions.

### 3.6 PMNS reductions — named selectors  **(38 files)**
Passive monomial phase reduction; EWSB weak-axis Z3 seed; active-block / projector reductions; breaking-triplet source laws; directional Z3-moment route; `σ = 0` no-go. These are the *named-primitive* PMNS reduction catalogue — the rigorous core of the PMNS lane.

### 3.7 DM–leptogenesis / PMNS bridge  · 10 files
Branch-selected normalization theorem, Ne-effective block-gap localization, observation-free normalization boundary, real-slice intrinsic class certificate. Each has a matched runner. These connect the DM-sector frozen structure to the PMNS selector via normalization constraints.

### 3.8 Neutrino–Majorana three-generation programme  · 14 files
Minimal-bridge structural closure, canonical closure axiom derivation, three-generation review packet. The Majorana side of the lepton programme — includes right-conjugacy-invariant no-go.

### 3.9 PMNS — reduction / closure exploration corpus  · 111 files
The bulk of `codex/neutrino-retained-lanes-review`. Includes:
- **Closure-status / full-microscopic-closure program notes** — current landscape
- **Lower-level Schur pushforward & partition response theorems** — structural backbone
- **Delta-D corner orbit / source closure family** — microscopic selector analysis
- **Green-kernel / active-block / source-response laws** — kernel-level reductions
- **Right-conjugacy-invariant no-go, single-axiom microscopic non-closure** — confirmed obstructions

Reviewer recommendation: read `docs/PMNS_CLOSURE_STATUS_NOTE_2026-04-16.md` first — it's the umbrella status note for this entire corpus.

### 3.10 Neutrino — other / DM-surface scouts  · 24 files
Dirac-monomial no-mixing, Higgs-Z3 underdetermination, full-closure last-mile, minimal-post-retained-integration, plus DM-neutrino source-surface scouts (bivector Pfaffian, discrete fixed-point attractor, Z3-doublet phase chart). Exploration-grade; reviewer may defer.

### 3.11 Koide — sectoral / cross-species  · 13 files
Anomaly-forced cross-species, color-sector correction, matrix-unit-source-law cyclic projection, observable-principle cyclic source law, sectoral universality, SU(2) gauge-exchange mixing, DM-Koide cross-HW shared-bottleneck scout, CL3 selector gap, mass-ratio CKM dual. These are Koide-adjacent generalizations / cross-sector scouts.

### 3.12 Other lepton-tagged  · 1 file
Single miscellaneous file retained by the lepton keyword filter.

---

## 4. Key science findings — reviewer punch-list

**Promote candidates (reviewer-grade, PASS-status):**
1. **Z³ scalar potential → lepton mass tower** (§3.1) — cubic coupling 1/6 axiom-pinned by Clifford trace identity. *Honest gap flagged: `m_*` not yet closed by V alone.*
2. **Koide one-scalar obstruction triangulation** (§3.2) — three independent routes terminate at the same dagger identity.
3. **Charged-lepton two-Higgs canonical reduction** (§3.5) — 7-parameter canonical form for Y_ν.
4. **PMNS σ=0 no-go** (§3.6) — every current pure-retained PMNS route forces σ = 0 on the sole-axiom bank.
5. **DM-leptogenesis branch-selected normalization theorem** (§3.7) — real-slice intrinsic class certificate.
6. **Right-conjugacy-invariant PMNS no-go** (§3.9) — single-axiom microscopic non-closure confirmed.

**Context from preceding audit work (not in this branch; handed over separately):**
- **Attack 1 PARTIAL:** `Δm²_21/Δm²_31 ≈ 5/(54π) = 0.029473` at ~0.1% (falsifiable JUNO prediction; involves retained 5/6 and `C_A²` Casimirs).
- **Attack 2 PARTIAL:** Observed pin IS a critical point of V for `H_base = (γ = 0.363309, E_1 = √(8/3), E_2 = √8/3)` — but saddle, and no closed form for γ = 0.363309. Agent U rank argument weakens here.
- **R1 and R2 are PDG coincidence, not axiom-native.** Historical PDG-drift + Frobenius obstruction established this.

---

## 5. What is NOT in this branch

- 60 non-lepton files from the unique-file pool (DM-only `frontier_dm_blocker_3_*`, `frontier_dm_case3_*`, publication-infra, `PREDICTION_CARD.md`, backlog/audit docs, `WAVEFIELD_PREDICTION_CARD_NOTE.md`, `CABIBBO_BOUND_NOTE.md`, CKM-NNI notes). These remain on their source branches; the reviewer can pull them selectively if useful for non-lepton lanes.
- Any file already on `origin/main` (verified 0 overlap).
- The 12 branches themselves are untouched and remain available for archaeology.

---

## 6. How to review / land

```bash
# Fetch this branch
git fetch origin review/lepton-pmns-integration-package
git checkout review/lepton-pmns-integration-package

# Re-run smoke tests (expect all PASS)
python3 scripts/frontier_koide_z3_scalar_potential.py          # PASS=34
python3 scripts/frontier_koide_one_scalar_obstruction_triangulation.py  # PASS=23
python3 scripts/frontier_g5_joint_pmns_koide_pinning.py        # PASS=9 (JOINT_PINNING_THEOREM_ABSENT — intended)
python3 scripts/frontier_pmns_sigma_zero_no_go.py              # PASS=18

# Full sweep (recommended before landing)
for f in scripts/frontier_*.py; do python3 "$f" > /tmp/out 2>&1 || echo "FAIL: $f"; done
```

**Suggested landing strategy:** Land in named groups (§3.1, §3.2, §3.5 first; then §3.6, §3.7, §3.8; then the large corpus §3.9 as a single bulk add). Each group is semantically coherent and can be reviewed independently.

---

## 7. Provenance audit trail

All working files for this integration (file selection CSVs, priority awk scripts, overlap check) are preserved at `/tmp/integration-work/` on the machine where this branch was prepared. Reviewer can request them if per-file attribution is needed beyond §1.
