# Universal θ-Induced EDM Vanishing Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-corollary theorem** on `main`. Generalises the retained [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md) — which packages only the neutron EDM corollary `d_n(QCD) = 0` — to a universal statement covering **all** θ-induced electric dipole moments and θ-induced CP-violating QCD operators. The generalization is a clean structural consequence of the retained [`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md) `θ_eff = 0` surface, but is not currently named as a standalone theorem.
**Primary runner:** `scripts/frontier_universal_theta_induced_edm_vanishing.py`

---

## 0. Statement

**Theorem (universal θ-induced EDM vanishing).** On the retained `θ_eff = 0` action-surface ([`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md)), all θ-induced contributions to electric-dipole-moment-class observables vanish exactly:

```text
(E1)  d_n^θ        =  0          (neutron EDM, retained: CKM_NEUTRON_EDM_BOUND_NOTE)
(E2)  d_p^θ        =  0          (proton EDM)
(E3)  d_e^θ        =  0          (electron EDM, trivially: no QCD coupling)
(E4)  d_μ^θ, d_τ^θ =  0          (muon, tau EDMs, similarly trivial)
(E5)  d_d^θ        =  0          (deuteron EDM = sum of nucleon EDMs)
(E6)  d_He³^θ, d_He⁴^θ =  0      (helium nuclei EDMs)
(E7)  S^θ_atom     =  0          (Schiff moments for any atomic species)
(E8)  d_atom^θ     =  0          (Hg-199, Xe-129, Ra-225, Tl-205, ...)

(O1)  c_θ G G̃     =  0          (QCD topological term coefficient)
(O2)  d_q^c, ✓ d̃_q^c =  0       (chromo-EDM and chromo-electric-dipole quark operators)
(O3)  c_W G G G̃    =  0          (Weinberg three-gluon operator coefficient)
(O4)  c_4F^θ      =  0          (four-fermion CP-odd θ-induced operators)
```

Surviving CP-violating EDM contributions on the retained surface are exclusively from the **CKM weak sector** (`d_n^CKM ~ 10⁻³² e·cm` and similarly suppressed for other particles). All currently-measured EDM upper bounds satisfy these CKM-weak predictions by many orders of magnitude.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Retained `θ_eff = 0` on Wilson-staggered action surface | [`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md) |
| Retained CKM-only neutron EDM corollary | [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md) |
| Retained CPT exact theorem | [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) |
| Retained graph-first SU(3) confinement | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md), [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md) |
| Standard Adler–Bell–Jackiw / Crewther–Wilczek QCD-EDM relation | textbook (Crewther 1979) |

## 2. Derivation

### 2.1 The retained `θ_eff = 0` action surface

The retained `STRONG_CP_THETA_ZERO_NOTE` establishes that on the retained Wilson-plus-staggered action surface:

```text
θ_eff  =  θ_QCD + arg det(M_u M_d)  =  0
```

with **four closure legs** (fermion phase, axial non-generation, instanton-measure positivity, zero-θ minimum). This holds at all orders in the retained framework's perturbative expansion.

### 2.2 Step 1: θ-induced gluon operator coefficients vanish (O1, O3)

The QCD topological term `θ G^a_{μν} G̃^{a,μν}` has coefficient `θ_eff` directly. Since `θ_eff = 0`:

```text
c_θ G G̃  =  θ_eff × [normalisation]  =  0.                                    (O1)
```

The Weinberg three-gluon operator (G G G̃) is induced at higher loops by θ × heavy-quark propagator integrals. With `θ_eff = 0`:

```text
c_W^θ  =  θ_eff × [loop function]  =  0.                                       (O3)
```

(There remains a CKM-weak contribution to Weinberg-operator coefficient, `c_W^CKM ~ 10⁻¹⁰` in canonical units; this is an independent — and tiny — source.)

### 2.3 Step 2: θ-induced quark CP-odd operators vanish (O2, O4)

Quark chromo-EDM operators `q̄ σ^{μν} γ_5 G_{μν} q` are induced by θ × heavy-quark loops. With `θ_eff = 0`, all θ-induced chromo-EDM coefficients vanish:

```text
d_q^c (chromo-EDM, θ-induced)        =  0
d̃_q^c (chromo-electric, θ-induced)    =  0                                   (O2)
```

Similarly, four-quark CP-odd operators induced by θ all vanish (O4). (CKM-weak induced contributions are non-zero but tiny.)

### 2.4 Step 3: Hadronic EDMs from θ vanish (E1, E2, E5, E6)

The neutron EDM from θ is the famous Crewther-Wilczek-Weinberg result:

```text
d_n^θ  ≈  +e × 10⁻¹⁶ × θ_eff   cm.
```

With `θ_eff = 0`:

```text
d_n^θ  =  0.                                                                  (E1)
```

(Already retained as [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md).)

Proton EDM follows the same Crewther-Wilczek mechanism with opposite sign:

```text
d_p^θ  ≈  −e × 10⁻¹⁶ × θ_eff   cm  =  0.                                       (E2)
```

Composite-nucleus EDMs (deuteron, helium-3, helium-4) are linear sums of nucleon EDMs at leading order, so they inherit the same vanishing:

```text
d_d^θ      =  d_n^θ + d_p^θ  =  0                                              (E5)
d_He³^θ, d_He⁴^θ  =  similar nucleon-sum  =  0                                 (E6)
```

### 2.5 Step 4: Lepton EDMs from QCD-θ trivially vanish (E3, E4)

Charged leptons (e, μ, τ) have no direct strong-sector coupling. The only θ → lepton-EDM channel is via heavy-quark loops mediating CP violation through electroweak boson exchange. Since `θ_eff = 0` removes the θ source:

```text
d_e^θ, d_μ^θ, d_τ^θ  =  0.                                                     (E3, E4)
```

The CKM-weak induced electron EDM is `d_e^CKM ~ 10⁻³⁸ e·cm` (Khriplovich-Pospelov estimate), far below all experimental bounds.

### 2.6 Step 5: Atomic EDMs from QCD-θ vanish (E7, E8)

Atomic EDMs are dominated by:
- Electron EDM `d_e` weighted by atomic enhancement factors
- Nuclear Schiff moment `S` (T-violating nuclear charge distribution)

The Schiff moment from QCD-θ vanishes since it inherits the nucleon EDM vanishing:

```text
S^θ_nucleus  =  Σ_i {nucleon-EDM_i contribution} × {nuclear-structure factor}  =  0
                                                                              (E7)
```

Atomic EDMs (Hg-199, Xe-129, Ra-225, Tl-205, etc.) are linear combinations of `d_e`, `S`, and nucleon EDMs. With all θ-induced contributions zero:

```text
d_Hg-199^θ, d_Xe-129^θ, d_Ra-225^θ, ...  =  0.                                 (E8)
```

### 2.7 Step 6: Surviving CKM-weak contributions

After all θ-induced vanishings, the surviving EDM sources are CKM-weak induced (CP violation from the CKM phase via 3+ loop processes). Standard predictions:

```text
d_n^CKM    ~  10⁻³² e·cm    (retained-bounded, CKM_NEUTRON_EDM_BOUND)
d_e^CKM    ~  10⁻³⁸ e·cm
d_atom^CKM ~  10⁻³⁵ e·cm
```

These are far below all current experimental bounds, so any future positive EDM detection would falsify the retained `θ_eff = 0` surface — which is exactly the predictive content of this theorem.

## 3. Comparison with experimental bounds

| Observable | Framework θ contribution | Framework CKM-weak | Experimental upper bound |
|------------|---------------------------|---------------------|----------------------------|
| `d_n` | 0 (E1) | ~10⁻³² e·cm | 1.8×10⁻²⁶ e·cm (Abel et al. 2020) |
| `d_p` | 0 (E2) | ~10⁻³² e·cm | (no direct bound) |
| `d_e` | 0 (E3) | ~10⁻³⁸ e·cm | 4.1×10⁻³⁰ e·cm (ACME II 2018) |
| `d_μ` | 0 (E4) | ~10⁻³⁶ e·cm | 1.9×10⁻¹⁹ e·cm (BNL 2009) |
| `d_τ` | 0 (E4) | – | ~10⁻¹⁷ e·cm (LEP) |
| `d_Hg-199` | 0 (E8) | ~10⁻³⁴ e·cm | 7.4×10⁻³⁰ e·cm (Graner et al. 2016) |
| `d_Xe-129` | 0 (E8) | ~10⁻³⁵ e·cm | 1.5×10⁻²⁸ e·cm (Sachdeva et al. 2019) |
| `d_Ra-225` | 0 (E8) | ~10⁻³³ e·cm | 1.4×10⁻²³ e·cm (Bishof et al. 2016) |
| `d_d` (deuteron) | 0 (E5) | ~10⁻³² e·cm | (storage ring proposal) |

All current experimental bounds are satisfied by many orders of magnitude.

## 4. Falsification

Sharp:

- A confirmed positive EDM detection at significance > 5σ at any sensitivity above `~10⁻³² e·cm` for nucleon-class observables, or `~10⁻³⁸ e·cm` for lepton-class observables, would require either:
  - Falsification of `θ_eff = 0` (this theorem)
  - Beyond-SM physics (separate from retained framework)
- Any θ-attributable EDM signal (i.e., not consistent with CKM-weak prediction) directly falsifies retained `θ_eff = 0`.

Future experiments:
- **n2EDM** (Paul Scherrer Institute): targeting `d_n` at `~10⁻²⁸ e·cm` precision by 2030.
- **ACME III**: targeting `d_e` at `~10⁻³² e·cm` precision.
- **EDM³** (electron EDM in molecules): similar precision.
- **Storage ring EDM** (proton, deuteron): `~10⁻²⁹ e·cm` proposed.

If any of these detect a positive signal incompatible with CKM-weak, the retained `θ_eff = 0` is in tension; if signal is at or above ~10⁻²⁹ e·cm for the most sensitive species, framework is **falsified**.

## 5. Joint with retained Strong-CP closure

This theorem extends the existing retained chain:

```text
STRONG_CP_THETA_ZERO_NOTE          (θ_eff = 0 on action surface)
            ↓
CKM_NEUTRON_EDM_BOUND               (d_n^θ = 0, d_n bounded ~10⁻³²)
            ↓
THIS THEOREM                        (universal θ-induced EDM vanishing
                                      across n, p, e, μ, τ, atomic, Schiff,
                                      chromo-EDM, Weinberg-op, four-fermion)
```

Each successive theorem widens the scope of "what θ-induced CP violation produces" from "the neutron EDM only" to "any EDM-class observable."

## 6. Scope and boundary

**Claims:**

- (E1)–(E8) all θ-induced EDMs and Schiff moments vanish on retained surface.
- (O1)–(O4) all θ-induced QCD CP-odd operator coefficients vanish.
- The framework predicts surviving CKM-weak EDMs that are far below all current experimental bounds.

**Does NOT claim:**

- BSM EDM contributions (axions, supersymmetry, leptoquarks, etc.) — these are separate, beyond retained framework.
- Quantitative CKM-weak EDM values (referencing standard QCD calculations, not derived here).
- Beyond standard hadronic-EDM mechanisms (e.g. chiral effective theory at high precision).

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_universal_theta_induced_edm_vanishing.py
```

Expected: all checks pass.

The runner:

1. Catalogues retained `θ_eff = 0` and verifies each EDM contribution starts at θ × loop-function form.
2. Confirms each E_i and O_i vanishes when `θ_eff = 0`.
3. Lists CKM-weak surviving contributions with order-of-magnitude estimates.
4. Compares all framework predictions to experimental bounds (n2EDM, ACME, etc.).
5. Verifies framework satisfies all current bounds with at least 4 orders of magnitude margin.

## 8. Cross-references

- [`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md) — retained θ_eff = 0 theorem
- [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md) — neutron-EDM corollary (this theorem extends to all particles)
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — CPT exact preservation
- [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md) — graph-first SU(3) confinement
- Crewther et al. 1979 "Chiral estimate of the electric dipole moment of the neutron in QCD", Phys. Lett. B 88, 123 — original QCD-EDM relation
- Pospelov & Ritz 2005 "Electric dipole moments as probes of new physics", Annals Phys. 318, 119 — review
- Khriplovich & Pospelov 1991 — CKM-weak EDM estimates
