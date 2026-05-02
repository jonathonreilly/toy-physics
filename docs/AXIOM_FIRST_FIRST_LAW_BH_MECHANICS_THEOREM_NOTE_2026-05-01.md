# Axiom-First First Law of Black Hole Mechanics

**Date:** 2026-05-01
**Status:** support — branch-local theorem note on retained framework GR + retained BH 1/4 carrier + Block 02 Hawking T_H support; runner passing; audit-pending. Honest status: derived support theorem. `proposal_allowed: false` because upstream Hawking T_H block is itself audit-pending support.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 5 (Block 05; stacked on Block 02 (Hawking))
**Branch:** `physics-loop/24h-axiom-first-block05-firstlaw-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Runner:** `scripts/axiom_first_first_law_bh_mechanics_check.py`
**Log:** `outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt`

## Scope

This note proves the **first law of black hole mechanics** on the
framework's retained discrete GR action surface plus retained BH 1/4
carrier composition plus Block 02 Hawking temperature. The result is

```text
    dM  =  T_H  dS_BH  +  Ω_H dJ  +  Φ_H dQ                                  (BCH 1973)
```

for stationary, axially-symmetric solutions of the framework's GR
action with a non-degenerate Killing horizon, where:

- `M` = asymptotic ADM mass,
- `T_H = κ/(2π)` = Hawking temperature (Block 02),
- `S_BH = A/(4G)` = Bekenstein-Hawking entropy (retained BH 1/4 carrier),
- `J` = total angular momentum,
- `Q` = total electric charge (when matter content includes a U(1)
  gauge field),
- `Ω_H` = angular velocity of the horizon,
- `Φ_H` = electric potential at the horizon.

For the Schwarzschild family (`J = 0`, `Q = 0`) the law reduces to

```text
    dM  =  T_H · dS_BH  =  (κ / 8π G) dA                                    (1)
```

This is the **gravitational analog of the first law of
thermodynamics** and confirms that `(M, T_H, S_BH)` form a
thermodynamically consistent triple on the framework's retained
gravity surface.

## Retained inputs

- **Framework GR action surface.** Stationary axially-symmetric
  solutions exist via the canonical Einstein-Hilbert equivalence
  (`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`).
  We use only the Schwarzschild family explicitly; rotating Kerr and
  charged Reissner-Nordström extensions are corollaries.
- **BH 1/4 carrier composition.** From the retained
  `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`,
  `S_BH = A · c_cell = A / (4 G_Newton,lat)`.
- **Wald-Noether identity** (already admitted by upstream BH 1/4
  carrier): for a stationary Killing horizon with Killing vector `ξ`,
  the Noether charge `Q_ξ` integrated over a horizon cross-section
  equals `(κ / 2π) S_Wald + Ω_H J + Φ_H Q + ...`.
- **Block 02 Hawking temperature.** From the Block 02 support
  theorem, `T_H = κ/(2π)` for any non-degenerate Killing horizon on
  the framework's GR surface.
- **Smarr formula prerequisite.** Standard relation
  `M = 2 T_H S_BH + 2 Ω_H J + Φ_H Q` for the Schwarzschild + Kerr +
  RN family follows from the same retained Wald-Noether composition
  by Komar-style integration.

## Admitted-context inputs

- **ADM mass identification.** Asymptotic mass of a stationary
  asymptotically-flat solution = ADM mass = M (admitted-context, same
  level as Block 02).
- **Bardeen-Carter-Hawking 1973** integrability argument: the Killing
  vector at the horizon plus the Wald-Noether form-identity give
  exact differentials.

These are the same inputs already paid for by the retained
Wald-Noether composition.

## Statement

Let `(M, g)` be a one-parameter family of stationary, axisymmetric
solutions of the framework's GR action, parametrized by `(M, J, Q)`
with non-degenerate Killing horizons. Then:

**(F1) First law (Schwarzschild specialization).** For
Schwarzschild family `(J = 0, Q = 0)`,

```text
    dM  =  T_H  dS_BH                                                       (2)
```

with `T_H = κ/(2π)` and `S_BH = A/(4G)`. Substituting `T_H` and
`dS_BH = dA/(4G)`:

```text
    dM  =  (κ / 2π) · (dA / 4G)  =  κ dA / (8π G)                          (3)
```

**(F2) First law (general Kerr-Newman family).** For the general
stationary axisymmetric family `(M, J, Q)` on the framework smooth-
limit equivalence surface,

```text
    dM  =  T_H · dS_BH  +  Ω_H · dJ  +  Φ_H · dQ                          (4)
```

**(F3) Smarr-type relation.** For the same family, the Smarr-Komar
mass formula reads

```text
    M  =  2 T_H S_BH  +  2 Ω_H J  +  Φ_H Q                                  (5)
```

**(F4) Schwarzschild explicit check.** For Schwarzschild with
`r_s = 2GM`, `A = 4π r_s² = 16π G² M²`, `S_BH = A/4G = 4π G M²`, and
`T_H = 1/(8π G M)`, the first law (F1) reads

```text
    dM  =  (1 / 8π G M) · d(4π G M²)  =  (1 / 8π G M) · 8π G M dM  =  dM    (6)
```

an identity, confirming consistency.

**(F5) Universal thermodynamic interpretation.** (F1)-(F4) imply
that on the framework's retained GR surface, BHs satisfy the
standard four laws of thermodynamics (zeroth, first, second, third)
with the identifications `T ↔ T_H`, `S ↔ S_BH`. This is the
"Black Holes are thermodynamic" statement of Bardeen-Carter-Hawking
1973 / Hawking 1975, now derived (modulo the upstream chain) on the
framework's GR surface.

## Proof

### Step 1 — Wald-Noether form identity

By the Wald-Noether identity (already admitted by retained BH 1/4
carrier composition), the variation of the Iyer-Wald Noether charge
`Q_ξ[g]` on a horizon cross-section `Σ_H` for a stationary Killing
vector `ξ` satisfies

```text
    δQ_ξ  -  ξ · θ[g, δg]  =  d(...)                                        (7)
```

Integrating (7) between the horizon `Σ_H` and spatial infinity gives

```text
    δH_∞[ξ]  -  δH_H[ξ]  =  0                                                (8)
```

where `H_∞[ξ]` is the asymptotic Hamiltonian (= ADM mass for the
asymptotic time translation) and `H_H[ξ]` is the horizon Hamiltonian.
This is the **Iyer-Wald identity**.

For the asymptotic time-translation Killing vector `ξ_t` normalized
at infinity:

```text
    H_∞[ξ_t]  =  M  (ADM mass)                                              (9)
```

For the horizon Killing vector `ξ_H = ξ_t + Ω_H ϕ + ...`:

```text
    H_H[ξ_H]  =  T_H · S_BH  +  Ω_H · J  +  Φ_H · Q                        (10)
```

(this is the form computed by Wald 1993; the temperature factor comes
from the surface gravity `κ` via Block 02's `T_H = κ/(2π)` and the
entropy from the retained BH 1/4 carrier).

### Step 2 — First law

Differentiating (8) along the family parameter `(M, J, Q)` and using
(9), (10):

```text
    dM  =  d(T_H S_BH)  +  d(Ω_H J)  +  d(Φ_H Q)                           (11)
```

But the family is parameterized by `(M, J, Q)` with Killing-horizon
preservation, so the parameters `T_H, Ω_H, Φ_H` are themselves
functions of `(M, J, Q)`. The Bardeen-Carter-Hawking integrability
argument shows the differential simplifies:

```text
    dM  =  T_H  dS_BH  +  Ω_H dJ  +  Φ_H dQ                               (12)
```

establishing (F2) and hence (F1) as the `J = Q = 0` specialization. ∎

### Step 3 — Smarr formula by Euler scaling

By Euler's theorem on homogeneous functions: `M(λ²S_BH, λ²J, λQ) =
λ M(S_BH, J, Q)` (since `M, S_BH, J` scale as length squared and `Q`
as length, in natural units). Differentiating in `λ` at `λ = 1`:

```text
    M  =  2 (∂M/∂S_BH) S_BH  +  2 (∂M/∂J) J  +  (∂M/∂Q) Q                (13)
       =  2 T_H S_BH  +  2 Ω_H J  +  Φ_H Q                                 (14)
```

using `∂M/∂S_BH = T_H` etc. from (F2). This proves (F3). ∎

### Step 4 — Schwarzschild explicit check (proves F4)

For Schwarzschild: `M = M`, `r_s = 2 G M`, `A = 16 π G² M²`,
`S_BH = A/4G = 4 π G M²`, `T_H = 1/(8 π G M)`. Then

```text
    T_H · dS_BH  =  (1/8 π G M) · d(4 π G M²)  =  (1/8 π G M) · 8 π G M dM  =  dM    (15)
```

confirming (F4). Smarr (F3) for Schwarzschild: `M = 2 T_H S_BH =
2 · (1/8 π G M) · 4 π G M² = M` ✓. ∎

## Hypothesis set used

- Retained framework GR action surface and canonical Einstein-Hilbert
  equivalence.
- Retained BH 1/4 carrier composition (Wald-Noether admitted).
- Block 02 Hawking temperature support theorem (T_H = κ/(2π)).
- Wald-Noether identity (admitted-context, same as upstream).
- ADM mass identification (admitted-context).
- Bardeen-Carter-Hawking 1973 integrability argument
  (admitted-context, theorem-grade reference).

No fitted parameters. No observed values used as proof inputs.

## Corollaries

C1. **Universal BH thermodynamics.** With the zeroth law (`κ`
constant on Killing horizon), first law (F2), second law (`δA ≥ 0`,
Hawking 1971), and third law (no `T_H = 0` extremal limit reachable
in finite steps), BHs on the framework retained surface satisfy all
four laws of thermodynamics.

C2. **Smarr formula.** (F3) is a useful diagnostic: any candidate
solution that violates `M = 2 T_H S_BH + 2 Ω_H J + Φ_H Q` cannot be
a member of the stationary axially-symmetric family.

C3. **Negative specific heat for Schwarzschild.** From (6),
`dT_H/dM = -1/(8π G M²) < 0`, so Schwarzschild has negative specific
heat — adding mass *cools* the BH. This is the standard result and
is consistent with thermodynamic instability of asymptotically flat
Schwarzschild.

C4. **GSL cornerstone.** Combined with Block 01 KMS monotonicity
and the second law `δA ≥ 0`, (F1) gives the Generalized Second Law
`δ(S_BH + S_matter) ≥ 0` (Block 09).

## Honest status

**Branch-local theorem on retained framework GR + retained BH 1/4
carrier + Block 02 Hawking T_H support.** (F1)–(F5) are derived from
the upstream chain plus the standard Wald-Noether form identity and
Bardeen-Carter-Hawking 1973 integrability argument.

The runner verifies the Schwarzschild specialization (F4) numerically
across a sweep of `M` values: `dM = T_H dS_BH` holds at machine
precision. It also verifies the Smarr formula `M = 2 T_H S_BH` for
Schwarzschild and the negative specific heat corollary.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 carrier + Block 02 Hawking T_H support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits upstream support classification: depends on Block 02 Hawking T_H support theorem which is itself audit-pending support (depends on Block 01 KMS support which depends on retained-but-audit-pending RP and spectrum-condition support notes). Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until the entire upstream chain is ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Full Iyer-Wald 1994 derivation of the form identity (we admit it
  as standard Wald-Noether input, same as upstream).
- Promotion to retained / Nature-grade in the canonical paper
  package. Independent audit + upstream ratification required.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained framework GR action: `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
- retained BH 1/4 carrier: `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- Block 02 Hawking T_H support: `docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md`
- standard external references (theorem-grade, no numerical input):
  Bardeen-Carter-Hawking (1973) *Comm. Math. Phys.* 31, 161 (BCH 1973);
  Bekenstein (1973) *Phys. Rev. D* 7, 2333;
  Hawking (1975) *Comm. Math. Phys.* 43, 199;
  Wald (1993) *Phys. Rev. D* 48, R3427 (Noether-charge entropy);
  Iyer-Wald (1994) *Phys. Rev. D* 50, 846.
