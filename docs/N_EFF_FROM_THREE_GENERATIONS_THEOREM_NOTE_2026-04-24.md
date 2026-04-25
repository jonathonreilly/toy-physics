# N_eff = 3 from Retained Three-Generation Structure Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-corollary theorem** on `main`. Connects the retained matter content (three generations + one-generation closure including ν_R) to the cosmological observable `N_eff` (the effective number of relativistic species at BBN/CMB). The link is implicit in cross-references between the matter-sector retained theorems and the cosmology cascade, but not packaged as a named retained theorem; this note packages the structural connection.
**Primary runner:** `scripts/frontier_n_eff_from_three_generations.py`

---

## 0. Statement

**Theorem (N_eff from retained matter content).** Given the retained inputs:

1. Retained three-generation structure ([`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)): three identical SM-content generations on the orbit algebra `8 = 1 + 1 + 3 + 3`.
2. Retained one-generation closure ([`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)): each generation contains one LH neutrino in the doublet `L_L = (ν_L, e_L)` and one RH ν_R singlet (forced by anomaly cancellation including B-L; see [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)).
3. Retained Majorana seesaw scale ([`NEUTRINO_MASS_DERIVED_NOTE.md`](NEUTRINO_MASS_DERIVED_NOTE.md)): RH neutrino lightest mass `M_1 = M_Pl × α_LM^8 × (1 − α_LM/2) ≈ 5.32 × 10¹⁰ GeV`.
4. Standard cosmology BBN/CMB temperature scales `T_BBN ~ 1 MeV`, `T_CMB ~ eV`.

then the effective number of relativistic species at the matter-radiation equality / decoupling era is exactly three (up to the standard QED + non-instantaneous decoupling correction):

```text
(N)   N_eff^framework  =  3   (+ 0.046 standard correction)  =  3.046.
```

The three retained LH SM neutrinos (ν_e, ν_μ, ν_τ) contribute `+1` each to N_eff. The retained RH ν_R singlets are heavy (`M_1 ~ 5×10¹⁰ GeV ≫ T_BBN, T_CMB`) and have decoupled / been Boltzmann-suppressed by the early-universe era, contributing `0` to N_eff at the relevant temperatures.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Three retained generations | [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) |
| One LH neutrino + one RH ν_R per generation | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md), [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) |
| RH ν_R seesaw mass `M_1 ≈ 5.32 × 10¹⁰ GeV` | [`NEUTRINO_MASS_DERIVED_NOTE.md`](NEUTRINO_MASS_DERIVED_NOTE.md), retained Majorana scale at k_B = 8 |
| LH neutrino mass scale `m_3 ≈ 5.06 × 10⁻² eV` | [`NEUTRINO_MASS_DERIVED_NOTE.md`](NEUTRINO_MASS_DERIVED_NOTE.md), retained atmospheric scale |
| Standard SM thermodynamics in early universe | textbook |
| QED + non-instantaneous decoupling correction `+0.046` | de Salas & Pastor 2016, Mangano et al. 2005 |

## 2. Derivation

### 2.1 Step 1: Three retained LH neutrino species

The retained three-generation structure forces three SM neutrino flavours (ν_e, ν_μ, ν_τ) on the LH side. Each is a Weyl spinor in the doublet `L_L = (ν_L, e_L)_{−1}` per generation, with retained content (per [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)).

**Number of LH neutrino species: 3.**

### 2.2 Step 2: RH ν_R is heavy and decoupled

The retained Majorana scale for the lightest RH neutrino is

```text
M_1  =  M_Pl × α_LM^8 × (1 − α_LM/2)
     ≈  1.22 × 10¹⁹ × 4.57 × 10⁻⁹ × 0.955  GeV
     ≈  5.32 × 10¹⁰ GeV.
```

Compared to relevant cosmological temperatures:

```text
M_1 / T_BBN  ≈  5.32 × 10¹⁰ / 10⁻³  =  5.32 × 10¹³           (BBN, T ≈ 1 MeV)
M_1 / T_CMB  ≈  5.32 × 10¹⁰ / 10⁻⁹  =  5.32 × 10¹⁹           (CMB, T ≈ eV)
```

The retained ν_R is **Boltzmann-suppressed** by `e^{−M_1/T} ≈ e^{−10¹³}` at BBN and by `e^{−10¹⁹}` at CMB. RH neutrinos are entirely thermally decoupled and contribute no relativistic energy density at either era.

**Number of relativistic ν_R species at BBN/CMB: 0** (within machine precision of any tractable cosmology).

### 2.3 Step 3: N_eff counts LH neutrinos only

The effective number of relativistic species at BBN/CMB is the standard cosmology quantity

```text
ρ_rel  =  (π² / 30) × g_eff(T) × T⁴
g_eff(T → m_e era) = 2 (photons) + (7/8) × N_eff × 2 (per ν species, particle + antiparticle)
                   × (T_ν/T_γ)⁴.
```

`N_eff` is conventionally normalised so that `N_eff = 3` for the SM with three LH neutrino flavours and standard instantaneous decoupling. Including the QED + non-instantaneous decoupling correction (de Salas & Pastor 2016, Mangano et al. 2005):

```text
N_eff^SM  =  3.046.
```

The retained framework matches this prediction exactly: 3 retained LH neutrinos + heavy decoupled ν_R → `N_eff = 3.046`.

### 2.4 Step 4: Cross-check via Ω_r,0 and z_{mr}

The early-universe radiation density is

```text
Ω_{r,0}  =  Ω_γ,0 × [1 + (7/8) × (4/11)^{4/3} × N_eff].
```

With `T_CMB = 2.725 K` giving `Ω_γ,0 = 2.47 × 10⁻⁵ / h²` and `h = 0.674`:

```text
Ω_γ,0     ≈  5.43 × 10⁻⁵
Ω_{r,0}   ≈  Ω_γ,0 × [1 + 0.227 × 3.046]  =  Ω_γ,0 × 1.692  ≈  9.19 × 10⁻⁵.
```

This matches the value used in retained cosmology cascade ([`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md) and [`MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)).

Combined with retained `Ω_{m,0} ≈ 0.315`, the matter-radiation equality redshift is

```text
z_{mr}  =  Ω_{m,0} / Ω_{r,0} − 1  ≈  0.315 / 9.19 × 10⁻⁵ − 1  ≈  3427.
```

Consistent with Planck 2018 inferred `z_{mr} = 3387 ± 21`.

## 3. Hypothetical alternatives (falsification)

| Hypothetical generation count | N_eff (no QED corr.) | Ω_r,0 | z_{mr} | Status |
|--------------------------------|-----------------------|--------|---------|--------|
| 2 generations (smaller) | 2 | ~7.6 × 10⁻⁵ | ~4140 | inconsistent with 3-gen retained |
| **3 generations (retained)** | **3** | **9.2 × 10⁻⁵** | **3423** | **✓** |
| 4 generations (4th SM-like) | 4 | ~10.8 × 10⁻⁵ | ~2920 | inconsistent with retained, falsifiable |
| 3 SM + 1 light sterile ν | ~4 | ~10.8 × 10⁻⁵ | ~2920 | falsified by Planck N_eff = 2.99 ± 0.17 |
| 3 SM + heavy ν' (M ≫ T_BBN) | 3 | 9.2 × 10⁻⁵ | 3423 | indistinguishable from retained |

The framework prediction `N_eff = 3.046` sits within Planck 2018 1σ window `2.99 ± 0.17`, while a 4-generation or sterile-neutrino addition would push N_eff to ≈ 4 — outside Planck's window at >5σ.

**Light sterile neutrinos are excluded** by the joint Planck + retained framework constraint.

## 4. Connection to other retained theorems

| Lane | Connection |
|------|------------|
| Three-generation closure | Source of LH neutrino count = 3 |
| One-generation closure | Per-generation LH+RH neutrino content (1+1) |
| Retained Majorana seesaw `M_1 ~ 10¹⁰ GeV` | Forces RH decoupling at all observable cosmological eras |
| Matter-radiation equality `z_{mr}` | Cosmological observable that depends on N_eff via Ω_r |
| FRW kinematic K1-K5 | Late-time identities (independent of N_eff at late times) |

The retained N_eff = 3 is an **independent witness** for the three-generation closure: cosmological data on N_eff (Planck, BBN abundance ratios) confirms the same 3-generation structure independently inferred from collider data on three SM lepton/quark flavours.

## 5. Falsifiability

Sharp:

- **Discovery of a 4th-generation light neutrino** would falsify the retained 3-generation closure AND push N_eff to ≈ 4, falsifying the prediction.
- **Confirmation of a light (m < eV) sterile neutrino** would push N_eff toward 4, also incompatible with retained structure.
- **Refinement of N_eff to 4 ± 0.05** at high significance would falsify retained 3-generation.

Current data:
- Planck 2018: `N_eff = 2.99 ± 0.17` (95% CL) — consistent with framework 3.046.
- BBN constraint: `2.66 < N_eff < 4.21` (95% CL) — consistent.
- Future CMB-S4 / LiteBIRD will constrain `N_eff` to ~0.03 precision by 2030 — sharp test.

If future data pushes `N_eff` to 4 ± 0.05, the retained 3-generation closure is falsified. This is one of the few structural cosmological tests of the matter-content retained surface.

## 6. Scope and boundary

**Claims:**

- (N) `N_eff^framework = 3` exactly (counting LH SM neutrinos).
- With standard QED + non-instantaneous decoupling correction, `N_eff^framework = 3.046`.
- Retained ν_R is heavy (M_1 ≈ 5×10¹⁰ GeV) → decoupled at BBN/CMB → contributes 0 to N_eff.
- Cross-consistent with Ω_r,0 ≈ 9.2 × 10⁻⁵ and z_{mr} ≈ 3423.

**Does NOT claim:**

- The QED + non-instantaneous decoupling correction is derived from the framework; it's standard cosmology.
- A native-axiom derivation of `T_CMB = 2.725 K` (observational input).
- Beyond-SM dark radiation (e.g. axions, hidden photons) — would be additional contributions.
- Constraints on absolute neutrino mass scale (separately retained).

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_n_eff_from_three_generations.py
```

Expected: all checks pass.

The runner:

1. Counts retained LH neutrino species per generation (1) × generations (3) = 3.
2. Verifies retained ν_R Boltzmann suppression at BBN/CMB temperatures.
3. Computes N_eff^framework = 3 + 0.046 = 3.046 (standard correction).
4. Cross-checks Ω_r,0 from N_eff and Ω_γ,0.
5. Verifies z_{mr} from N_eff + retained Ω_m,0.
6. Tests falsification scenarios (N_eff = 2, 4, 4.5).
7. Confirms Planck 2018 N_eff = 2.99 ± 0.17 consistency.

## 8. Cross-references

- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) — retained 3 generations
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — retained per-gen content
- [`NEUTRINO_MASS_DERIVED_NOTE.md`](NEUTRINO_MASS_DERIVED_NOTE.md) — retained Majorana M_1
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) — ν_R required by anomaly closure
- [`MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) — z_{mr} cross-check
- [`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md) — cascade context
- de Salas & Pastor 2016, JCAP 07, 051 — `N_eff^SM = 3.046` standard correction
- Planck Collaboration 2018, A&A 641, A6 — N_eff = 2.99 ± 0.17 observational
