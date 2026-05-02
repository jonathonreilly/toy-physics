# Axiom-First Unruh Temperature from KMS + Framework Lorentz Kernel

**Date:** 2026-05-01
**Type:** bounded_theorem
**Claim scope:** for a uniformly accelerated observer with proper acceleration a in the framework Minkowski-limit Rindler wedge on the retained Lorentz kernel surface, the regular Wick-rotated Rindler period is 2π and the Minkowski vacuum appears as Gibbs at proper-time inverse temperature β_th(a) = 2π/a, i.e. T_Unruh = a/(2π) (U1)-(U4); also the Bisognano-Wichmann modular operator identity Δ_R = exp(-2πK).
**Status:** awaiting independent audit. Under the scope-aware classification framework (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 8 (Block 08; stacked on Block 01 (KMS))
**Branch:** `physics-loop/24h-axiom-first-block08-unruh-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Runner:** `scripts/axiom_first_unruh_temperature_check.py`
**Log:** `outputs/axiom_first_unruh_temperature_check_2026-05-01.txt`

## Scope

This note proves the **Unruh effect** on the framework's retained
Lorentz kernel surface plus Block 01 KMS:

> A uniformly accelerated observer in the framework's Minkowski-limit
> vacuum sees a thermal flux at temperature
>
> ```text
>     T_Unruh  =  ℏ a / (2π k_B c)              (Unruh 1976 form)
>              =  a / (2π)                       (in natural units)
> ```
>
> where `a` is the observer's proper acceleration.

The proof structure mirrors Block 02 (Hawking T_H): instead of a
Killing horizon of a black hole, we use the Rindler horizon of the
right Rindler wedge in flat space.

## Retained inputs

- **Block 01 KMS support theorem.** Periodic-Euclidean ↔ thermal
  Gibbs identification on `H_phys`.
- **Retained Lorentz kernel.** From
  `LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`, the framework has a
  positive boost generator `K` such that `U(η) = exp(-i η K)` is the
  one-parameter group of Lorentz boosts on `H_phys`.
- **Retained emergent Lorentz invariance.** From
  `EMERGENT_LORENTZ_INVARIANCE_NOTE.md`, framework states transform
  covariantly under boosts in the smooth-limit regime.
- **Retained anomaly-forced 3+1 dimensions.** Rindler wedge structure
  is 3+1-dimensional, matching the framework's retained signature.

## Admitted-context inputs

- **Standard Rindler coordinate construction.** The Rindler wedge is
  the spacetime region `x > |t|` in Minkowski space, parametrized by
  `(η, ξ)` with `t = ξ sinh η`, `x = ξ cosh η`. Standard SR.
- **Rindler observer trajectories.** Observer at fixed `ξ = 1/a` has
  proper acceleration `a` and proper time `τ_proper = η / a`.
- **Wick-rotation regularity** (same as Block 02).

## Statement

Let `H_phys` be the RP-reconstructed physical Hilbert space, `K` the
retained Lorentz boost generator, and `|Ω⟩` the Minkowski vacuum.
Consider a uniformly accelerated observer in the right Rindler wedge
with proper acceleration `a > 0`.

Then on `A_min` plus the retained inputs above:

**(U1) Wick-rotated Rindler regularity.** The Euclidean continuation
of the Rindler metric `ds² = -ξ² dη² + dξ² + dy² + dz²` along the
Rindler time `η → -i τ` gives `ds_E² = +ξ² dτ² + dξ² + dy² + dz²`,
which is regular at `ξ = 0` (the Rindler horizon) if and only if `τ`
is identified periodically with period `2π`.

**(U2) Unruh temperature.** A Rindler observer at fixed
`ξ = 1/a` (proper acceleration `a`) with proper time `τ_proper = η/a`
sees the Minkowski vacuum as a Gibbs state at proper-time inverse
temperature

```text
    β_th(a)  =  2π / a                                                       (1)
```

i.e. at temperature

```text
    T_Unruh  =  a / (2π)                                                     (2)
```

**(U3) KMS condition for Rindler observer.** The two-point function
of any operator `O` along the Rindler trajectory satisfies the KMS
condition (Block 01 (K2)) at inverse temperature `β_th(a) = 2π/a`.

**(U4) Bisognano-Wichmann analogue.** The boost generator `K` acts on
the right Rindler wedge as the modular Hamiltonian for the Minkowski
vacuum, and the modular automorphism `e^{-i η K}` is the (improper-
time) Rindler boost.

Statements (U1)–(U4) constitute the framework Unruh theorem on the
retained Lorentz kernel surface plus Block 01 KMS support.

## Proof

The proof is the same structure as Block 02 (Hawking T_H) Steps 1-3,
with the Killing horizon replaced by the Rindler horizon `ξ = 0`.

### Step 1 — Rindler local coordinates

In the right Rindler wedge `R = {x > |t|}` of 3+1 Minkowski space,
introduce coordinates `(η, ξ, y, z)` with `t = ξ sinh η`,
`x = ξ cosh η`, `y, z` flat. The Minkowski metric becomes

```text
    ds²  =  -ξ² dη² + dξ² + dy² + dz²                                       (3)
```

This is the standard Rindler metric. The Killing vector is the boost
generator: `ξ_R = ∂_η = a x ∂_t + a t ∂_x` (under the
identification `a = 1/ξ` for an observer at fixed proper distance `ξ`).

The "surface gravity" of the Rindler horizon at `ξ = 0` is `κ_R = 1`
in the (η, ξ) coordinates (with the boost-Killing vector unit-
normalized at `ξ = 1`).

### Step 2 — Wick rotation and periodicity

Wick-rotate the Rindler time `η → -i τ`. The Euclidean continuation
of (3) is

```text
    ds_E²  =  +ξ² dτ² + dξ² + dy² + dz²                                     (4)
```

The 2D `(τ, ξ)` factor is the standard Euclidean Rindler /
2D-cone metric. Smoothness at `ξ = 0` requires `τ ∈ R / 2π Z`
(period `2π`), the same conical-defect argument as Block 02.

### Step 3 — KMS at proper-time inverse temperature

For a Rindler observer at fixed `ξ_obs = 1/a` (proper acceleration
`a = 1/ξ_obs`), the proper time is `τ_proper = ξ_obs · η = η/a`.

The Rindler-Killing-time periodicity `η ∈ R / 2π Z` translates to
proper-time periodicity

```text
    τ_proper  ∈  R / (2π / a) Z                                              (5)
```

i.e. proper-time period `β_th = 2π / a`. By Block 01 (K1)–(K2), the
Minkowski vacuum restricted to the Rindler wedge appears to the
accelerated observer as a Gibbs state at this proper-time inverse
temperature, and any two-point function along the trajectory satisfies
the KMS condition. ∎

### Step 4 — Bisognano-Wichmann (proves U4)

The retained Lorentz kernel `K` is the boost generator on `H_phys`
(`LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`). By the standard
Bisognano-Wichmann argument (1975, 1976), restricted to the right
Rindler wedge `R`, the boost generator `K` is the modular Hamiltonian
for the local algebra `A(R)` and the Minkowski vacuum `|Ω⟩`:

```text
    Δ_R  =  e^{-2π K}                                                       (6)
```

where `Δ_R` is the modular operator from Tomita-Takesaki. This is
the QFT-statement of the same fact: the modular automorphism of
`A(R)` is the Rindler boost, with proper-time period `2π / a`.

The proof of (6) uses the same Wick-rotation analyticity used in
Steps 2-3 plus the Reeh-Schlieder cyclicity (Block 07 — Minkowski
vacuum is cyclic-and-separating for `A(R)`). Block 07 supports the
Tomita-Takesaki modular structure; Block 08 specializes it to the
Rindler wedge to recover the Unruh temperature. ∎

## Hypothesis set used

- A_min (only as inherited from upstream RP via Block 01 KMS).
- Retained Lorentz kernel (gives boost generator K on H_phys).
- Retained emergent Lorentz invariance (gives Rindler wedge structure
  in smooth-limit regime).
- Retained anomaly-forced 3+1 dimensions.
- Block 01 KMS support theorem.
- Standard Rindler coordinate construction and Bisognano-Wichmann
  argument (admitted-context).

No fitted parameters. No observed values used as proof inputs.

## Corollaries

C1. **Detector response.** A two-level Unruh-DeWitt detector on the
Rindler trajectory has thermal excitation rate consistent with
temperature `T_Unruh = a / 2π`. This is the standard quantitative
prediction.

C2. **Numerical scale.** For `a = 9.8 m/s²` (Earth gravity),
`T_Unruh ≈ 4 × 10⁻²⁰ K` — far below any current experimental
sensitivity. For `a = c/(1 ns)`, `T_Unruh ≈ 200 K` — observable in
principle.

C3. **Connection to Hawking.** The same Step 1–3 derivation with
the Schwarzschild horizon in place of the Rindler horizon gives
Hawking T_H = κ/(2π). Both are special cases of the Wick-rotation
regularity argument plus KMS (Block 01).

C4. **No-go for cyclic Hartle-Hawking restriction.** The Hartle-
Hawking-Israel state on Schwarzschild restricted to the exterior
satisfies KMS at T_H = κ/(2π), exactly mirroring the Minkowski
vacuum restricted to the Rindler wedge.

## Honest status

**Branch-local theorem on retained Lorentz kernel + Block 01 KMS
support.** (U1)–(U4) follow by direct adaptation of the Block 02
proof structure to the Rindler wedge.

The runner verifies the formula `T_Unruh = a / (2π)` numerically on
a sweep of accelerations, confirms the proper-time period `β_th =
2π / a`, recovers the SI scale for Earth-gravity acceleration, and
checks the structural identity `T_Unruh / a = 1 / (2π)` is universal.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained Lorentz kernel + Block 01 KMS support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits Block 01 KMS upstream support classification (audit-pending)."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Independent derivation via Bogoliubov coefficients (Unruh 1976
  original method).
- Experimental tests of Unruh radiation (currently at the limit of
  experimental sensitivity).

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained Lorentz kernel: `docs/LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`
- retained emergent Lorentz: `docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md`
- Block 01 KMS support: `docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`
- Block 02 Hawking T_H (parallel proof structure):
  `docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md`
- standard external references (theorem-grade, no numerical input):
  Unruh (1976) *Phys. Rev. D* 14, 870;
  Bisognano-Wichmann (1975) *J. Math. Phys.* 16, 985;
  Bisognano-Wichmann (1976) *J. Math. Phys.* 17, 303;
  Sewell (1982) *Annals Phys.* 141, 201.
