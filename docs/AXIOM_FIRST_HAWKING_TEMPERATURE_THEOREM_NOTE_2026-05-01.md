# Axiom-First Hawking Temperature from Wick-Rotated Killing Horizon + KMS

**Date:** 2026-05-01
**Type:** bounded_theorem
**Claim scope:** for any non-degenerate Killing horizon of surface gravity κ on the framework's retained discrete GR action surface, the regular Wick-rotated Euclidean continuation has period β_th = 2π/κ; equivalently the asymptotic state is Hartle-Hawking-Israel Gibbs at T_H = κ/(2π) (H1)-(H4). Conditional on admitted-context Killing-vector / surface-gravity / Wick-rotation-regularity vocabulary already paid for by the retained Wald-Noether composition.
**Status:** awaiting independent audit. Under the scope-aware classification framework (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 1 (Block 02; stacked on Block 01)
**Branch:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Runner:** `scripts/axiom_first_hawking_temperature_check.py`
**Log:** `outputs/axiom_first_hawking_temperature_check_2026-05-01.txt`

## Scope

This note proves, on the framework's retained discrete GR action surface
(`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`,
`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`)
plus the Block 01 KMS support theorem
(`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`), that any
stationary solution of the framework's GR action with a non-degenerate
Killing horizon of surface gravity `κ > 0` carries a Hawking
temperature

```text
    T_H  =  ℏ κ / (2π k_B c)              (Hawking 1975 form)
         =  κ / (2π)                       (in framework natural units ℏ = c = k_B = 1)
```

This is the **gravity-temperature corollary** of KMS applied to the
unique regular Wick rotation of the Killing horizon, and it provides
the load-bearing input for:

- Block 05 (first law of BH mechanics: dM = T_H dA / (8π G));
- Block 09 (generalized second law: δ(S_BH + S_matter) ≥ 0).

After this note, the package can quote a branch-local Hawking
temperature theorem on the framework's retained GR action surface
instead of treating it as a continuum-QFT-only result.

## Retained inputs

- **Framework GR action on PL S³ × R.** The retained discrete-global
  Lorentzian Einstein/Regge stationary action family
  (`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`) gives an exact
  stationary problem on every nondegenerate Lorentzian background in
  the route. Stationary backgrounds with Killing horizons (e.g., the
  Schwarzschild family on the framework's smooth-limit equivalence
  surface) lie inside that class.
- **Canonical Einstein-Hilbert equivalence.** On the smooth surface
  the framework's gravitational action equals the canonical
  Einstein-Hilbert action up to a closed boundary term
  (`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`),
  so the differential-geometric vocabulary of Killing vector fields,
  surface gravity, and bifurcate horizons applies on the framework's
  GR action surface.
- **BH 1/4 carrier composition.** The retained
  `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
  composes the framework primitive coframe `c_cell = 1/4` with the
  Wald-Noether entropy formula to yield `S_BH = A / (4 G_Newton,lat)`.
  We do not redo that composition; we use only the
  Killing-horizon definition that lives in the same retained
  vocabulary.
- **Block 01 KMS support theorem.** Periodic-Euclidean ↔ thermal
  correspondence on the RP-reconstructed Hilbert space. The relevant
  theorem is (K1) ↔ (K2) of Block 01.

## Admitted-context inputs

- **Surface gravity κ.** Standard differential-geometric definition:
  on a stationary Killing horizon `H` with future-pointing Killing
  vector `ξ^a` normalized at infinity (`ξ^a ξ_a = -1` at spatial
  infinity for asymptotically flat solutions), `κ` is the constant on
  `H` defined by `ξ^a ∇_a ξ^b = κ ξ^b`. Equivalently
  `κ² = -(1/2) (∇_a ξ_b)(∇^a ξ^b)|_H`.
- **Wick rotation regularity.** Standard observation that the
  Euclidean continuation of a stationary metric near a Killing horizon
  has the local form `ds² = κ² ρ² dτ² + dρ² + (transverse)`, which is
  smooth at `ρ = 0` if and only if `τ ∈ R / (2π / κ) Z` is identified
  with period `2π / κ`. This is "no conical-defect at the bolt".
- **Asymptotic-time identification.** The Euclidean Killing time `τ`
  asymptotically (away from the horizon) coincides with the Killing
  parameter generating asymptotic time translations, so the period
  `β_th := 2π / κ` *is* the asymptotic inverse temperature seen by an
  observer at infinity.

These three are the same admitted-context inputs already paid for by
the retained Wald-Noether composition in
`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
(which uses both the Killing-horizon vocabulary and the smooth
gravitational action surface). We do not introduce new admitted
inputs.

## Statement

Let `(M, g)` be any stationary solution of the framework's GR action
with a non-degenerate (`κ ≠ 0`) bifurcate Killing horizon `H` and
surface gravity `κ`. Let `α_t := e^{i t H_grav}` denote the
asymptotic time-translation evolution generated by the corresponding
asymptotic Killing vector field. Then on `A_min` plus retained
framework GR plus Block 01 KMS:

**(H1) Wick-rotated horizon regularity.** The Euclidean continuation
`(M_E, g_E)` of `(M, g)` along the Killing parameter `t → -i τ` has a
metric that is regular at `ρ = 0` if and only if `τ` is identified
periodically with period

```text
    β_th  :=  2π / κ                                                        (1)
```

(in natural units; restoring `ℏ` and `c` gives `β_th = 2π c / (ℏ κ)`).

**(H2) Hawking temperature.** The physical state on `H_phys`
asymptotically reproduced by the Wick-rotated regular Euclidean
manifold is the Gibbs state (in the sense of Block 01 (K1)) at
asymptotic inverse temperature `β_th = 2π / κ`. Equivalently, an
asymptotic observer sees a thermal flux at temperature

```text
    T_H  =  1 / β_th  =  κ / (2π)                                            (2)
```

This is the **Hawking temperature** of the horizon.

**(H3) KMS condition for the Hartle-Hawking-Israel state.** Any
two-point function of asymptotic operators `A, B` constructed on
`H_phys` from the Wick-rotated regular Euclidean path integral
satisfies the KMS condition (Block 01 (K2)) at inverse temperature
`β_th = 2π / κ`:

```text
    < A · α_t(B) >_{HH}  =  < α_t(B) · A · e^{- β_th H_grav} · e^{β_th H_grav} >_{HH}
                         (KMS form (5) of Block 01 with β_th = 2π / κ)         (3)
```

so the Hartle-Hawking-Israel vacuum is the unique `α_t`-invariant
KMS state at `T_H = κ / (2π)` on the asymptotic algebra (using Block
01 (K4) equilibrium uniqueness on the finite-block algebra).

**(H4) Composition with retained BH 1/4 carrier.** Combined with the
retained `S_BH = A / (4 G_Newton,lat)` composition from
`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`,
the pair `(T_H, S_BH) = (κ / 2π, A / 4 G_N)` already satisfies the
Bekenstein-Hawking entropy-temperature relation, opening the bridge to
the first law of BH mechanics (Block 05).

Statements (H1)–(H4) constitute the Hawking temperature theorem on
the framework's retained GR surface plus the Block 01 KMS support
theorem.

## Proof

The proof has three explicit steps. Steps 1–2 are pure
differential geometry on the framework's retained GR action surface;
Step 3 is direct application of Block 01 KMS.

### Step 1 — Local Rindler form near a Killing horizon

Let `(M, g)` be a stationary solution of the framework's discrete
GR action on PL S³ × R, in the smooth-limit regime where the
canonical-textbook Einstein-Hilbert equivalence
(`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`)
holds. Let `ξ^a` be the asymptotic time-translation Killing vector,
`H` its bifurcate Killing horizon, and `κ` the surface gravity defined
by `ξ^a ∇_a ξ^b = κ ξ^b` on `H`.

Choose Gaussian normal coordinates near `H` adapted to `ξ^a`. By the
standard near-horizon expansion (a basic theorem in stationary GR;
see Wald, "General Relativity", §12), there exists a coordinate
neighborhood `U` of any horizon point on which the metric takes the
**local Rindler form**

```text
    ds² |_U  =  -κ² ρ² dt² + dρ² + dΩ²(transverse)                          (4)
```

to leading order in `ρ`, where `ρ` is the proper-distance coordinate
from the horizon (`ρ = 0` on `H`) and `t` is the Killing parameter.
The surface gravity `κ` is constant on `H` (zeroth law of BH
mechanics, which holds for any Killing horizon).

### Step 2 — Wick rotation periodicity

Wick-rotate the Killing parameter `t → -i τ`. The Euclidean
continuation of (4) is

```text
    ds_E² |_U  =  +κ² ρ² dτ² + dρ² + dΩ²(transverse)                        (5)
```

The 2D `(τ, ρ)` factor is the standard Euclidean Rindler / 2D-cone
metric. It can be rewritten as `dρ² + ρ² d(κ τ)²`, which is the flat
metric on `R²` in polar coordinates `(ρ, ϕ)` with angular coordinate
`ϕ := κ τ`.

Smoothness at `ρ = 0` requires the angular coordinate `ϕ` to be
identified periodically with period `2π`. Translating back to `τ`,
this gives the periodicity

```text
    τ  ∈  R / (2π / κ) Z                                                    (6)
```

with period `β_th := 2π / κ`. Any other periodicity produces a
conical defect at `ρ = 0`, which violates the regularity of the
Euclidean manifold (a defect of total angle `2π - δ` on the bolt
costs an action contribution proportional to `δ`, breaking
stationarity of the Euclidean action).

### Step 3 — KMS at β_th = 2π / κ

By the regularity argument of Step 2, the Wick-rotated path integral
on the framework's retained GR action surface is well-defined (no
conical defect, hence no spurious boundary term). The Euclidean
manifold is a fiber bundle over the asymptotic spatial geometry with
fiber `S¹` of circumference `β_th = 2π / κ` (in units where the
asymptotic Killing vector is normalized at infinity, `ξ² = -1`).

For asymptotic operators `A, B` constructed on the RP-reconstructed
`H_phys` (asymptotic region), the path integral on this Euclidean
fiber-bundle gives correlators of the form

```text
    < A · α_τ(B) >_{Euclidean}
       =  (1 / Z_E) · ∫ Dg DA exp(-S_E[g, A]) · A · B(τ)                    (7)
```

with the standard transfer-matrix identification `A → Â`,
`B(τ) → α_τ(B̂)` on `H_phys` (the same construction used by the
retained RP and spectrum-condition support notes).

Since the Euclidean time is periodic with period `β_th = 2π / κ`,
this is exactly the periodic-Euclidean path integral covered by
Block 01 (K1):

```text
    Z_E  =  tr_{H_phys}( T̂^{L_τ_grav} )  =  tr_{H_phys}( e^{- β_th H_grav} )    (8)
```

with `H_grav` the asymptotic gravitational Hamiltonian generated by
`ξ^a`. By Block 01 (K1)–(K2), the asymptotic state is the Gibbs
state at inverse temperature `β_th = 2π / κ`, and the asymptotic
two-point function satisfies the KMS condition (3). This proves
(H1)–(H3). ∎

### Step 4 — Composition with retained S_BH = A/(4 G) (proves H4)

The retained `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE`
composition gives `S_BH = A · c_cell = A / 4` in lattice units (and
matching to standard `S_BH = A / (4 G_N)` forces `G_Newton,lat = 1`).
With `T_H = κ / (2π)` from (H2), the pair satisfies

```text
    T_H · dS_BH  =  (κ / 2π) · (dA / 4)
                 =  κ · dA / (8π)                                            (9)
```

which is the standard Smarr / first-law differential. In Block 05 we
will use the Wald-Noether identity to identify `T_H · dS_BH` with the
energy increment `dM` (minus rotational and gauge work terms).
Equation (9) is the load-bearing input. ∎

## Hypothesis set used

- A_min (only as inherited from upstream RP and spectrum-condition
  notes via Block 01 KMS).
- Retained framework GR action surface
  (`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md` and family).
- Retained canonical Einstein-Hilbert equivalence
  (`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`).
- Retained primitive coframe `c_cell = 1/4` and Wald-Noether
  composition (used only in (H4); the core T_H derivation H1-H3 does
  not need the entropy expression).
- Block 01 KMS support theorem
  (`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`).
- Standard Killing-vector / surface-gravity / Wick-rotation-regularity
  vocabulary (admitted-context inputs already paid for by the retained
  Wald-Noether composition).

No fitted parameters. No observed values used as proof inputs. No
imports beyond the explicit admitted-context list.

## Corollaries

C1. **Hawking flux temperature for any retained framework BH solution.**
For Schwarzschild on the framework smooth-limit equivalence surface,
`κ_Schw = 1 / (4 G M)`, giving `T_H = 1 / (8π G M)`. This is the
standard Hawking 1975 result, now derived (modulo the Killing-horizon
admission) on the framework GR surface.

C2. **First law differential.** From (H4), the differential
`κ dA / (8π) = T_H dS_BH` is set up for direct identification with
`dM` in Block 05 via the Wald-Noether identity.

C3. **Generalized second law cornerstone.** Combined with Block 01
KMS-monotonicity, (H2) opens the route to GSL (Block 09):
`δ(S_BH + S_matter) ≥ 0` follows from BH 1/4 + Hawking T_H + KMS
H-theorem.

C4. **Unruh-temperature analogue.** The same Step 1–3 argument
applied to the Rindler wedge in flat space (where κ becomes the
proper acceleration `a` of the Rindler observer) yields
`T_U = a / (2π)` (Unruh 1976). This is the Block 07 derivation.

## Honest status

**Branch-local theorem on retained framework GR + Block 01 KMS
support.** (H1)–(H4) are derived from:

- the retained framework GR action surface (which provides
  stationary backgrounds with Killing horizons via the canonical
  Einstein-Hilbert equivalence);
- standard differential geometry of Killing horizons (admitted
  context, same as upstream Wald-Noether composition);
- Block 01 KMS support theorem (which provides the Euclidean ↔
  thermal Gibbs identification).

The runner verifies the Wick-rotation-regularity periodicity
numerically by computing the conical-defect angle as a function of
the trial period `β` and confirming the unique smooth value at
`β = 2π / κ`. It also verifies the resulting `T_H = κ / (2π)`
formula on a Schwarzschild benchmark `κ_Schw = 1 / (4GM)` and
recovers `T_H = 1 / (8π G M)`.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 carrier (admitted Wald-Noether) + Block 01 KMS support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits upstream support classification: depends on Block 01 KMS support theorem which is itself audit-pending support (depends on retained-but-audit-pending RP and spectrum-condition support notes). Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until all dependencies are ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Continuum QFT-on-curved-spacetime derivation of Hawking radiation
  via Bogoliubov coefficients (Hawking 1975 original method). We
  prove the Wick-rotation / KMS form, which is the cleaner
  derivation given the framework's RP-based foundation.
- Promotion to retained / Nature-grade in the canonical paper
  package. That requires upstream RP, spectrum-condition, and Block
  01 KMS to be ratified first, plus independent audit.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained framework GR action: `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
- retained BH 1/4 carrier composition:
  `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- retained primitive coframe carrier:
  `docs/PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
- Block 01 KMS support theorem:
  `docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`
- standard external references (theorem-grade, no numerical input):
  Hawking (1975) *Comm. Math. Phys.* 43, 199;
  Gibbons-Hawking (1977) *Phys. Rev. D* 15, 2752;
  Wald (1984) *General Relativity*, ch. 12 (surface gravity);
  Bardeen-Carter-Hawking (1973) *Comm. Math. Phys.* 31, 161
  (zeroth law: κ constant on Killing horizon).
