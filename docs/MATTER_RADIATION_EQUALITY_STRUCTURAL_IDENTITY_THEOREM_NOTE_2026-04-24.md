# Matter–Radiation Equality Redshift Structural Identity Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Companion / extension to [`COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md), which covers the **late-time** kinematic identities (K1–K5) involving matter and Λ. The present theorem packages the **early-time** matter–radiation equality redshift identity, which is also a clean structural identity on retained flat FRW + standard matter/radiation EOS but is not currently named on `main`.
**Primary runner:** `scripts/frontier_matter_radiation_equality_structural_identity.py`

---

## 0. Statement

**Theorem (matter–radiation equality redshift).** Under the retained flat FRW cosmology with the standard matter EOS (`w_m = 0`) and radiation EOS (`w_r = 1/3`), the redshift of matter–radiation equality is the exact structural identity

```text
(MR)   1 + z_{mr}  =  Ω_{m,0} / Ω_{r,0}
```

equivalently `a_{mr} = Ω_{r,0} / Ω_{m,0}`, where `Ω_{m,0}` and `Ω_{r,0}` are the present-day matter and radiation density fractions.

The identity is a pure ratio of present-day density fractions; it does not depend on `H_0`, `Ω_Λ`, or the cosmological constant. It is α_s-independent, baryon-physics-independent, and atomic-physics-independent.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Flat FRW cosmology | standard cosmology / [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| Matter EOS `w_m = 0`, `ρ_m(a) ∝ a^{-3}` | textbook |
| Radiation EOS `w_r = 1/3`, `ρ_r(a) ∝ a^{-4}` | textbook |
| FRW continuity equation | [`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md) |

The retained `Λ = 3/R²` and `w_Λ = -1` are not needed for this identity (radiation-matter equality is decoupled from Λ).

## 2. Derivation

The matter and radiation density fractions evolve as

```text
Ω_m(a)  =  (Ω_{m,0} / a³) / E²(a),         Ω_r(a)  =  (Ω_{r,0} / a⁴) / E²(a),
```

where `E(a) = H(a)/H_0`. The ratio `Ω_m(a) / Ω_r(a)` cancels the common `1/E²(a)` factor:

```text
Ω_m(a) / Ω_r(a)  =  (Ω_{m,0} / Ω_{r,0}) · a.                          (R)
```

Matter–radiation equality is `Ω_m(a_{mr}) = Ω_r(a_{mr})`, equivalently the LHS of (R) = 1:

```text
(Ω_{m,0} / Ω_{r,0}) · a_{mr}  =  1
a_{mr}                        =  Ω_{r,0} / Ω_{m,0}
1 + z_{mr}                    =  1 / a_{mr}  =  Ω_{m,0} / Ω_{r,0}.    (MR)
```

The identity holds independently of `H_0`, `Ω_Λ`, the spatial curvature (here flat-FRW is used but any `Ω_k` cancels in the ratio), and any other cosmology parameter beyond `Ω_{m,0}` and `Ω_{r,0}`. ∎

## 3. Numerical verification (retained Ω_{r,0} + observed Ω_{m,0})

Standard cosmology values:

```text
Ω_{r,0}  ≈  9.2 × 10⁻⁵       (CMB photons + 3 species of relativistic neutrinos)
Ω_{m,0}  ≈  0.315             (Planck 2018, retained matter content from cosmology cascade)
```

Framework prediction:

```text
1 + z_{mr}  =  0.315 / 9.2 × 10⁻⁵  =  3424
z_{mr}     ≈  3423
```

Observational anchor (CMB-derived from acoustic peak structure):

```text
z_{mr}^{CMB}  =  3387 ± 21      (Planck 2018 inferred)
```

Framework deviation: `(3423 − 3387) / 3387 ≈ +1.1%`, within ~2σ of observed.

## 4. Joint with retained late-time kinematics

Combined with the late-time identities (K1–K5) from [`COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md), the FRW redshift hierarchy on the retained surface is structurally:

| Cosmic event | Retained identity | At observed Ω's |
|--------------|---------------------|-----------------|
| matter–radiation equality | `1 + z_{mr} = Ω_m,0/Ω_r,0` (this theorem) | `z_{mr} ≈ 3423` |
| photon decoupling (CMB) | atomic-physics dependent | `z_{rec} ≈ 1090` (not structural) |
| matter–Λ equality | `1 + z_{mΛ} = (Ω_Λ,0/Ω_m,0)^{1/3}` (K3) | `z_{mΛ} ≈ 0.296` |
| deceleration→acceleration | `1 + z_* = (2 Ω_Λ,0/Ω_m,0)^{1/3}` (K2) | `z_* ≈ 0.632` |

The structural identities sandwich the observational `z_{rec} ≈ 1090` (which depends on baryon and atomic physics, not on this theorem):

```text
z_{mr}  >  z_{rec}  >  z_*  >  z_{mΛ}  >  0.
```

with framework structural prediction of the OUTER three timestamps in the cosmic-history sequence.

## 5. Structural observations

- **The identity is α_s-independent and Λ-independent.** It depends only on the matter/radiation density ratio at the present epoch.
- **It is a "ratio identity"**, like the cosmology matter-bridge `Ω_Λ = (H_inf/H_0)²` and the late-time K1–K5: the LHS is a single observable (`z_{mr}`) and the RHS is a structural function of one or two density fractions.
- **The "1 + z" form makes the structural form algebraic** — `(Ω_{m,0}/Ω_{r,0})` is a pure ratio with `Ω_{r,0}` known precisely from CMB photon temperature `T_CMB = 2.725 K`.
- **The radiation count `Ω_{r,0}` includes neutrinos.** Specifically `Ω_{r,0} = Ω_γ,0 (1 + N_eff (7/8) (4/11)^{4/3})` with `N_eff = 3.046`. This is observationally determined; the framework retains 3 generations (giving 3 SM neutrino flavours), so `N_eff = 3` is structurally consistent.
- **Comparison to K3:** the matter-Λ equality redshift `1 + z_{mΛ} = (Ω_Λ/Ω_m)^{1/3}` involves a cube-root because matter scales as `a^{-3}`. The matter-radiation equality has no cube-root because both matter (a^{-3}) and radiation (a^{-4}) scaling differ by a single power of `a`, giving a linear ratio identity.

## 6. Falsifiability

Sharp:

- A confirmed `z_{mr}` outside framework's `Ω_{m,0}/Ω_{r,0}` band falsifies one of:
  - Standard matter EOS (`w_m = 0`) — would require massive dark-matter candidate with non-trivial pressure
  - Standard radiation EOS (`w_r = 1/3`) — would require modified relativistic species
  - Three-generation retained structure (changing N_eff and hence Ω_r,0)
- Current Planck 2018 z_{mr} = 3387 ± 21 is consistent with framework prediction 3423 at ~2σ.
- LiteBIRD / CMB-S4 will sharpen the constraint to `~1%` precision on z_{mr} by 2030.

The framework prediction's small (1%) deviation from observed could be sharpened if the retained Ω_{m,0} is itself derived from the cascade chain (`R_base × Sommerfeld`) rather than imported. That would test the joint consistency of:
- Ω_{m,0} from cosmology cascade
- Ω_{r,0} from CMB + neutrinos (and 3 generations)
- z_{mr} from this identity

## 7. Scope and boundary

**Claims:**

- (MR) `1 + z_{mr} = Ω_{m,0}/Ω_{r,0}` exactly on retained flat FRW + standard matter/radiation EOS.
- α_s-independent, Λ-independent, baryon-physics-independent.
- Numerical match within ~1% to Planck 2018 inferred z_{mr}.

**Does NOT claim:**

- A native-axiom derivation of `Ω_{m,0}` (separately bounded via cascade chain).
- A native-axiom derivation of `Ω_{r,0}` (depends on `T_CMB` observational input).
- Photon decoupling redshift `z_{rec} ≈ 1090` (depends on atomic recombination physics, not retained at native-axiom).
- BBN, sound horizon, or other baryon-dependent epochs.
- Modifications from non-standard matter/radiation (warm dark matter, modified radiation EOS, etc.).

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_matter_radiation_equality_structural_identity.py
```

Expected: all checks pass.

The runner:

1. Verifies (MR) via direct computation of `Ω_m(a)/Ω_r(a)`.
2. Computes `z_{mr}` using observed `Ω_{m,0}` and `Ω_{r,0}`.
3. Compares to CMB-inferred `z_{mr} = 3387 ± 21` (Planck 2018).
4. Symbolic (sympy) verification of the structural identity.
5. Cross-check with retained late-time kinematic identities (K1–K5 from FRW kinematic theorem).
6. Confirms ordering `z_{mr} > z_{rec} > z_* > z_{mΛ}`.

## 9. Cross-references

- [`COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md) — late-time kinematic identities K1-K5; this theorem is the early-time companion
- [`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md) — Ω_m,0 cascade (bounded)
- [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) — Λ identity (not used in this theorem)
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) — 3 retained generations giving N_eff = 3
- Weinberg, *Cosmology* (2008) — standard cosmology reference for FRW kinematics
- Planck Collaboration 2018, "Planck 2018 results. VI. Cosmological parameters", A&A 641, A6 — observational z_{mr}
