# Koide BAE Probe 24 — Brannen Magic Angle `φ = 2/9` from Z_3-Character / Berry-Phase / Plancherel-Frobenius Content (Sharpened, Partial Closure)

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction with partial positive closure)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 24 of the Koide Brannen Amplitude
Equipartition (BAE) closure campaign. Tests whether the newly-named
admission `φ = 2/9` (Probe 19, separate from BAE) can be derived from
retained Z_3-character / Berry-phase / Plancherel-Frobenius content on
the Cl(3)/Z³ lattice in the framework's **native angular unit**, NOT by
admitting the radian primitive that the Probe 19 statement imports.
**Authority role:** source-note proposal; effective status set only by
the independent audit lane.
**Loop:** koide-bae-probe24-phi-from-z3-character-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.py`](../scripts/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.txt`](../logs/runner-cache/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"BAE-condition"** = Brannen Amplitude Equipartition: the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the `C_3`-equivariant
  Hermitian circulant `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³` (legacy
  alias: "A1-condition" in PRs #727, #730–#740, #751, #755, #763,
  #784, #787, #788, #789).
- **"`φ = 2/9` admission"** = the Brannen "magic angle" admission
  newly named by Probe 19
  ([`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md))
  as a structural admission **separate from BAE**: the angular phase
  `φ = arg(b) = 2/9` (in radians, per Probe 19) on top of which the
  Brannen circulant `λ_k = a + 2|b| cos(φ + 2πk/3)` reproduces the
  PDG charged-lepton triplet to `~10⁻⁴`.

Framework axiom A1 is retained and untouched. This probe concerns
**only** the `φ = 2/9` admission newly named by Probe 19. BAE is not
attacked here.

## Constraint (per user 2026-05-09 directives)

**No new axioms. No new imports.** Any closure must come from already
cited source-stack content (`C_3`-Plancherel decomposition, character-algebra
dimension counts, conjugate-pair forcing per Brannen-phase reduction
theorem, retained selected-line Berry holonomy on CP¹).

**No PDG-input as derivation step.** The PDG charged-lepton triplet
appears only as a falsifiability comparator, never as derivation
input.

## Distinct angle (vs Probe 19 and the four prior radian-bridge probes)

Probe 19 named the `φ = 2/9` admission for the first time but stated
it in **radian units**: `φ = 2/9 ≈ 0.2222 rad ≈ 12.73°`. Per the
retained
[`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
and
[`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md),
the **radian primitive itself is not retained on Cl(3)/Z³**: every
retained periodic-phase source produces angles of the form `(rational)
× π`, every retained dimensionless ratio is a pure rational, and the
two sets meet only at zero.

This probe asks the **distinct** question:

> Is there a **native angular unit** retained on Cl(3)/Z³ — fractional
> Z_3-cycle, fractional Z_3-step, fractional `χ_ω`-character cycle,
> Plancherel-step, Bargmann-triangle unit, or any other character-algebra-
> derived unit — in which `φ = 2/9` is the **correct numerical value**
> for the Brannen circulant `cos(φ + 2πk/d)` formula to reproduce the
> PDG charged-lepton triplet?

Equivalently: can the radian primitive be **replaced** by some other
retained native unit, recovering the empirical PDG match without
admitting the radian as primitive?

## Question

Does the retained Cl(3)/Z³ character-algebra surface admit a native
angular unit in which `φ = 2/9` is the structural Brannen-phase value
that reproduces the PDG charged-lepton triplet via the retained
Brannen circulant `λ_k = a + 2|b| cos(φ + 2πk/d)`?

## Answer

**Partial positive closure with sharpened obstruction:**

1. **POSITIVE FINDING (dimensionless retained value):** The
   dimensionless rational `2/9 = n_eff/d² = 2/d²` IS exact retained
   content. It derives from:

   - `n_eff = 2`: doublet conjugate-pair winding, derived structurally
     in
     [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
     §1.3 from `L_ω̄ = conj(L_ω)`, forcing the projective doublet
     ratio `e^{-2iθ}` with winding number 2;
   - `d² = 9`: from `d = 3 = |C_3|` (retained, three-generation
     observable theorem) squared, equivalently the 9 real dimensions
     of `Herm_3` (R3 of
     [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md))
     or the `3 × 3` C_3-character × C_3-character pairing matrix
     (Plancherel surface).

   Therefore: **as a dimensionless character-algebra ratio, `2/9` is
   retained** as `(real DOF of b) / (real dim Herm_3) = 2/9 =
   n_eff/d²`. This is the same content the retained
   [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
   already isolates as I2 (dimensional-ratio identity).

2. **STRUCTURAL OBSTRUCTION (no native angular unit replaces the
   radian primitive):** The PDG-matching Brannen circulant
   `λ_k = a + 2|b| cos(φ + 2πk/3)` REQUIRES `φ` measured in radians
   for the empirical match to hold. Six native angular units
   inventoried below (cycle, Z_3-step, character-step, Plancherel-step,
   Bargmann-triangle, period-1-rad convention) all FAIL to give a
   rational fractional value of the magic angle in PDG-matching units.

   The framework's retained native angle measures are:

   - **Z_3-character units**: angles of the form `2πk/d, k ∈ Z_d`,
     i.e. rational multiples of `π`;
   - **Closed-orbit Bargmann units**: the closed three-step Bargmann
     phase on the equator equals `π` (rational multiple of `π`);
   - **Plancherel-weight units**: pure rationals (`1/3` per character)
     with no canonical angular conversion;
   - **Dimensional-ratio units**: pure rationals with no angle
     interpretation (e.g. `2/d²`, `(d-1)/d`).

   Every one of these gives the empirical PDG-matching `φ` as a
   **transcendental** in its own native unit. Specifically:

   | Native unit | `φ_native` for PDG match | Type |
   |---|---|---|
   | Radian (PDG match) | `2/9` (rational) | (NOT native) |
   | Cycle (`2π` rad = 1 cycle) | `2/(9·2π) = 1/(9π)` | transcendental |
   | Z_3-step (`2π/3` rad = 1 step) | `(2/9)/(2π/3) = 1/(3π)` | transcendental |
   | Bargmann-triangle (`π` rad = 1) | `(2/9)/π = 2/(9π)` | transcendental |
   | Plancherel-step (`2π/d²` rad = 1) | `(2/9)/(2π/9) = 1/π` | transcendental |
   | Character-step (per `χ_ω` increment, `2π/d` rad) | `(2/9)/(2π/3) = 1/(3π)` | transcendental |

   Therefore: **no retained native angular unit on Cl(3)/Z³ supplies
   the dimensional radian primitive that converts the dimensionless
   character-algebra ratio `2/d² = 2/9` into the PDG-matching radian
   value `φ = 2/9 rad`.**

3. **NEW SHARPENING:** The Probe 19 admission `φ = 2/9 rad` is
   precisely the **literal-rational-as-radian identification** that
   the Probe-20 (KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE) and the
   April-24 KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT identified as
   the residual primitive `P` (radian-bridge) in its sharpest form.
   Probe 19's `φ = 2/9` IS the same residual postulate `P`, restated
   at the BAE level. The "magic angle" framing of Probe 19 imports
   the radian primitive identically to how the `δ = 2/9` of the linking
   theorem imports it.

   **In particular, the Probe 19 admission "`φ = 2/9 rad ≈ 12.73°`" is
   not a new admission distinct from the prior radian-bridge `P`; it is
   the same primitive `P` re-named at the BAE / Brannen-circulant level.**

## What this DOES close

**Partial positive closure (dimensionless retained value of the
Brannen offset):**

`φ_dimensionless = n_eff / d² = 2/9` is a **derived dimensionless
character-algebra rational** under cited source-stack content alone. Specifically:

- `n_eff = 2` derives from C_3 conjugate-pair forcing (no new
  primitive).
- `d² = 9` derives from `d = 3` and the `3 × 3` Plancherel pairing
  surface or the 9 real dimensions of `Herm_3`.
- The ratio `n_eff/d² = 2/9` is therefore derived as a pure rational
  in retained Plancherel/Frobenius dimensional-counting units.

This recovers the linking theorem's I2 input
([`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
§3.2) at the BAE level: the dimensionless `2/d² = 2/9` is structural
character-algebra cited source-stack content.

## What this DOES NOT close

**Structural obstruction (radian-bridge primitive remains
load-bearing):**

The PDG-matching value of `φ` is `2/9 rad`, which uses the **radian as
unit of measurement**. The radian unit is structurally distinct from
all retained native angle units on Cl(3)/Z³: Z_3-character units
(`2πk/d`), Bargmann-triangle units (`π`), Plancherel-step units
(`2π/d²`), and character-step units (`2π/d`) all give the same
dimensional radian value `2/9` rad as a transcendental in their own
native rational ratio. Equivalently, in any native angle unit of
Cl(3)/Z³ — all of which take the form `(rational) × π` rad — the
PDG-matching `φ` is an irrational fraction.

**Equivalent compact statement:** the residual primitive needed is
exactly the bridge

> "the dimensionless Plancherel-Frobenius character-algebra ratio `2/d² =
> 2/9` numerically equals the PDG-matching Brannen magic angle measured
> in radians (i.e., `2/9 rad`)."

This is the same residual postulate `P` named in
[`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
§4 and reconfirmed by Probe 20
[`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
to require one of three specific structural inputs (lattice
propagator radian quantum, 4×4 hw=1+baryon non-uniform Wilson
holonomy, or Z_3-orbit Wilson-line `d²`-power quantization), none
currently retained.

The Probe 19 `φ = 2/9` admission is the SAME primitive `P`, restated
at the Brannen-circulant level. It is not a separate independent
admission distinct from the prior radian-bridge.

## Setup

### Retained C_3 / Brannen-circulant content

| Item | Origin | Retained content |
|---|---|---|
| `C_3[111]` cyclic shift `C` on `hw=1 ≅ ℂ³` | THREE_GENERATION_OBSERVABLE_THEOREM | order-3 unitary, eigenvalues `{1, ω, ω̄}` |
| Hermitian circulant family `H = aI + bC + b̄C²` | KOIDE_CIRCULANT_CHARACTER_DERIVATION R1 | 3 real DOF: `(a, |b|, arg(b))` |
| C_3-character decomposition `ℂ³ = L_1 ⊕ L_ω ⊕ L_ω̄` | KOIDE_CIRCULANT_CHARACTER_DERIVATION R2 | Plancherel-uniform |
| Brannen eigenvalue formula `λ_k = a + 2|b|cos(arg(b) + 2πk/d)` | KOIDE_CIRCULANT_CHARACTER_DERIVATION R3 | structural |
| Selected-line CP¹ Berry connection `A = dθ` | KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19 §4 | tautological |
| Bundle-obstruction (no `c_1`-forced Chern class) | KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19 | physical Koide base is interval |
| Conjugate-pair forcing `n_eff = 2` | KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20 §1.3 | `L_ω̄ = conj(L_ω)` ⇒ `arg(zeta) = -2θ` |

### Retained no-go content (radian-bridge primitive)

| Note | Statement |
|---|---|
| KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_2026-04-24 | every retained radian source = `(rational) × π`; pure rational `2/9` not supplied |
| KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_2026-04-20 | per-Z_3-element PB phase = `π/3`; closed-orbit Bargmann = `π`; neither equals `2/9 rad` |
| KOIDE_Q_DELTA_LINKING_RELATION_2026-04-20 §4 | postulate `P` named: `(2 DOF of b)/(real dim Herm_d) = 2/d² = δ` (radians) |

### Retained Brannen-phase reduction content (positive)

From
[`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
§1–2:

```
n_eff = 2     (conjugate-pair forcing, derived)
d = 3         (|C_3|, retained)
δ = n_eff / d² = 2/9    (dimensionless rational, derived)
```

This is a positive theorem **in dimensionless units**. The radian
identification step is what fails.

## Derivation chain

### Step 1 (positive theorem): `2/9` as a retained dimensionless ratio

By
[`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
§1.3, the projective doublet ratio on the selected line is
`zeta(θ) = e^{-2iθ}`, with winding number `n_eff = |d(arg ζ)/dθ| = 2`
forced by the conjugate-pair structure `L_ω̄ = conj(L_ω)`.

Per the C_3 step holonomy normalization (§2.2), the doublet projective
phase advance per C_3 step in **dimensionless Brannen units**
(advance per step divided by full C_3 period) is

```
δ_per_step = n_eff / d² = 2 / 9.
```

This is a **derived dimensionless rational**. Step 1 closes positively
in dimensionless retained units.

### Step 2 (admission required): radian-bridge primitive `P`

To convert the dimensionless `2/9` into a radian value usable in the
Brannen circulant formula `λ_k = a + 2|b| cos(φ + 2πk/3)`, one must
posit:

```
P:  φ_radians = δ_dimensionless,   i.e.   φ = 2/9 rad.
```

The radian-bridge no-go (Probe 20) proves `P` is not derivable from
retained Cl(3)/Z³ + selected-line CP¹ Berry content alone. Its minimal
inputs are (a), (b), or (c) named in the no-go note §4. None
currently retained.

### Step 3 (numerical exhaustion of native angle units)

For each retained or candidate native angle unit `U` (rad-equivalence
factor `α_U`), the PDG-matching `φ` in unit `U` is computed:

| Unit `U` | `α_U` (rad / `U`) | `φ_U = (2/9)/α_U` | Rational? |
|---|---|---|---|
| Cycle | `2π` | `1/(9π)` | No |
| Z_3-step | `2π/3` | `1/(3π)` | No |
| Bargmann-triangle | `π` | `2/(9π)` | No |
| Plancherel-step | `2π/d² = 2π/9` | `1/π` | No |
| Character-step | `2π/d = 2π/3` | `1/(3π)` | No |
| Selected-line CP¹ Berry holonomy per step | `π/3` (Probe 20) | `(2/9)/(π/3) = 2/(3π)` | No |
| Period-1-rad convention | `1` (literal-rational-as-radian) | `2/9` | Yes (only this one) |

**Only the period-1-rad convention** gives `φ` as a rational. This
convention IS the radian primitive (per the irreducibility audit's
sharpened formulation: "period-1-rad vs canonical period-2π-rad
convention choice"). It is not retained.

### Step 4 (verification): the Brannen formula match requires radian unit

Compute `cos(φ + 2πk/3)` for `k = 0, 1, 2` at:

```
φ_radian = 2/9  (PDG match):   cos values = (0.97541, -0.67861, -0.29679)
                                PDG observed = (0.97540, -0.67857, -0.29683)
                                relative deviation ~ 1e-4 ✓ (PDG match)

φ_cycle = 2/9 (cycles, ⇒ 4π/9 rad):
                                cos values = (0.17365, -0.93969, 0.76604)
                                NO MATCH to PDG charged-lepton cones

φ_Z3step = 2/9 (Z_3-step fraction, ⇒ 4π/27 rad):
                                cos values = (0.89363, -0.96126, 0.06763)
                                NO MATCH to PDG charged-lepton cones
```

Only the radian-unit reading of `φ = 2/9` reproduces the PDG match.
Native units fail.

## Why this probe is structurally rigorous

### Three independent verifications

1. **Numerical exhaustion of seven native angle units.** Cycle,
   Z_3-step, Bargmann-triangle, Plancherel-step, character-step,
   selected-line Berry-per-step, and period-1-rad. Six fail; only
   period-1-rad matches, and that is the radian primitive `P`
   re-named.

2. **Brannen-formula PDG-match requires radian.** Direct verification
   that `cos(φ + 2πk/3)` reproduces the PDG cone values
   `((m_τ-cos), (m_e-cos), (m_μ-cos))` only when `φ` is read as
   literal radians.

3. **Connection to retained no-go content.** The named admission of
   Probe 19 (`φ = 2/9`) is structurally identical to the residual
   postulate `P` named in
   [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
   §4 and reconfirmed by Probe 20
   [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md).
   This probe sharpens the BAE-program admission count: Probe 19's
   "magic angle" is **not** an independent third admission distinct
   from BAE and the radian-bridge `P` — it IS `P`, identified at the
   Brannen-circulant level.

### Sharpened residue

Probe 19 named "BAE + φ-magic" as two admissions on top of the Wilson
chain. This probe sharpens that count:

- **(BAE)**: `|b|²/a² = 1/2`. Independent admission. Eighteen-probe
  bounded obstruction. UNCHANGED.
- **(φ-magic, Probe 19)**: `φ = 2/9 rad`. **Identified with the
  radian-bridge `P`** by this probe. NOT a separate independent
  admission; the same residual primitive at the Brannen-circulant
  level.

The BAE-campaign admission count is therefore:

- **Pre-Probe 24**: BAE + φ-magic = 2 admissions (per Probe 19).
- **Post-Probe 24**: BAE + radian-bridge `P` = 2 admissions, where
  `P` and φ-magic are the same primitive.

The total admission count is unchanged at 2; this probe identifies the
relationship between them.

## What is positively closed

The retained Brannen-phase reduction theorem already supplies:

```
φ_dimensionless = n_eff / d² = 2/9    [retained, derived]
```

This probe confirms this and extends with: **no retained native
angular unit on Cl(3)/Z³ recovers the PDG-matching Brannen circulant
match without admitting the radian-bridge primitive `P`.** The
dimensionless `2/9` is exact cited source-stack content; the radian
identification is the precisely-named missing primitive.

## What remains bounded

The radian-bridge primitive `P` remains the load-bearing missing
input. The Probe 19 statement `φ = 2/9 rad` IS the primitive `P`
restated. To close `P`, one of the three structural inputs from
[`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
§4 must be supplied:

- **Input (a):** Lattice propagator radian quantum
  `G_{C_3}(1) = exp(i · 2/d²) · G_0`.
- **Input (b):** 4×4 hw=1+baryon non-uniform Wilson holonomy where the
  baryon-projected line gives Wilson phase `2/d²` rad.
- **Input (c):** Z_3-orbit Wilson-line `d²`-power quantization
  `W_{Z_3}^{d²} = exp(2i) · 𝟙`.

None currently retained. The Wilson-chain extension of Probe 19
(`m_τ` scale) does not supply any of these (it provides only the
absolute mass scale, not the radian-bridge).

## Strategic options

This probe **does not select** an option; that authority is the
user's. The post-Probe-24 status of the φ = 2/9 admission is:

1. **Re-classify Probe 19's φ = 2/9 admission as the existing
   radian-bridge primitive `P`.** No new admission added by Probe 19's
   "magic angle" naming; it is the same `P` already documented since
   2026-04-20. This reduces the visible admission count from "BAE +
   φ-magic" to "BAE + `P`" without increasing the framework's actual
   open-import budget.

2. **Continue radian-bridge closure hunt.** The minimal inputs (a),
   (b), (c) from Probe 20 §4 remain candidate routes. Wilson-chain
   structure (per Probe 19's positive `m_τ` finding) hints toward
   input (a) or (c), but neither is currently realized.

3. **Pivot to the dimensionless-only readout law.** Reformulate the
   Brannen-circulant `λ_k = a + 2|b|cos(φ + 2πk/d)` formula to take
   its dimensionless input `δ_dimensionless = 2/d²` directly,
   bypassing the radian unit. This requires re-deriving the Brannen
   formula to take dimensionless arguments — a non-trivial
   re-formulation of the entire Brannen-Rivero parameterization.
   Probability of closure unclear.

## What this DOES NOT do

This note explicitly does **NOT**:

1. **Close the radian-bridge primitive `P`.** `P` remains a named
   bounded admission. This probe identifies Probe 19's `φ = 2/9` as
   the same primitive (sharpening, not closure).
2. **Promote any retained theorem.** No retained theorem is modified.
3. **Add a new axiom.** A1+A2 still suffice on the retained stack.
4. **Use PDG values as derivation input.** PDG charged-lepton masses
   appear ONLY as falsifiability comparators in Step 4.
5. **Modify the BAE admission status.** BAE remains independently
   bounded (the eighteen-probe campaign is unchanged).
6. **Resolve any sister bridge gap** (L3a, L3b, C-iso, W1.exact engineering frontier).

## Forbidden imports check

- No PDG observed values consumed (PDG appears only as falsifiability
  comparator in Step 4).
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention (this probe
  EXPLICITLY ANALYZES which conventions enter; the radian convention
  is identified as the residual primitive `P`, not admitted).
- No same-surface family arguments.

## Validation

Primary runner:
[`scripts/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.py`](../scripts/cl3_koide_bae_probe_phi_from_z3_character_2026_05_09_probe24.py)

Verifies:

1. **Retained C_3 character algebra.** `C³ = I`, eigenvalues
   `{1, ω, ω̄}`, Hermitian circulant family on `hw=1 ≅ ℂ³`.
2. **`n_eff = 2` from conjugate-pair forcing.** Projective doublet ratio
   `arg(zeta(θ)) = -2θ`, winding number 2.
3. **`d = 3, d² = 9` from C_3 order.** Plancherel-uniform.
4. **Step 1 dimensionless closure.** `2/d² = 2/9` is derived character-
   algebra rational.
5. **Brannen-circulant PDG-match in radians.** `cos(2/9 + 2πk/3)`
   reproduces PDG charged-lepton triplet to `~10⁻⁴`.
6. **Cycle interpretation FAILS.** `cos(2π·(2/9) + 2πk/3)` does NOT
   match PDG.
7. **Z_3-step interpretation FAILS.** `cos((2π/3)·(2/9) + 2πk/3)` does
   NOT match PDG.
8. **Bargmann-triangle interpretation FAILS.** `cos(π·(2/9) + 2πk/3)`
   does NOT match PDG.
9. **Plancherel-step interpretation FAILS.** `cos((2π/9)·(2/9) +
   2πk/3)` does NOT match PDG.
10. **Character-step interpretation FAILS.** Same as Z_3-step.
11. **Selected-line Berry-per-step interpretation FAILS.** `(π/3)`
    radian-step, `(2/9)·(π/3)` rad does NOT match PDG.
12. **Only period-1-rad convention matches.** Identical to literal
    radian, which is the named primitive `P`.
13. **All native angle units give `φ` as transcendental.** `1/(9π)`,
    `1/(3π)`, `2/(9π)`, `1/π`, `2/(3π)` — all irrational.
14. **Radian primitive is NOT in the retained inventory.**
    Z_3-character periods `2πk/d`, Bargmann `π`, Plancherel `2π/d²` —
    all rationals × π, none equals 1 rad.
15. **Conditional triplet closure (under `P`).** PDG triplet emerges to
    `~10⁻⁴` precision once `P` (radian-bridge) is admitted.
16. **PDG-input firewall.** All Step-1-through-Step-3 verifications use
    only retained framework constants; PDG values appear only in
    Step 4 / Step 11 falsifiability comparator.
17. **Probe 19 `φ = 2/9` admission identified with radian-bridge `P`.**
    Same primitive; not a new independent admission.

Target: `=== TOTAL: PASS=N, FAIL=0 ===`.

## Cross-references

- [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
  — names `φ = 2/9` as new admission alongside BAE
- [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  — `δ = n_eff/d² = 2/9` dimensionless theorem (Step 1 here)
- [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
  §4 — names primitive `P` (radian-bridge)
- [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
  — proves `P` requires inputs (a), (b), or (c)
- [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
  — sharpens `P` to "period-1-rad vs canonical period-2π-rad convention choice"
- [`KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`](KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md)
  — selected-line CP¹ Berry connection `A = dθ`
- [`KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
  — bundle triviality on physical Koide base
- [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
  — `H = aI + bC + b̄C²` family, R1–R3
- [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
  — `a_0 = √3·a, z = √3·b, a_0² − 2|z|² = 3a² − 6|b|²` algebraic identities
- `MINIMAL_AXIOMS_2026-05-03.md` —
  framework axiom A1 (distinct from BAE-condition)

## Cited dependencies

The following cited source-stack content is load-bearing for Step 1 (positive
closure):

1. **C_3 conjugate-pair forcing**:
   `KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20` §1.3.
2. **C_3 order `d = 3`**:
   `THREE_GENERATION_OBSERVABLE_THEOREM` (retained).
3. **Plancherel character decomposition `ℂ³ = L_1 ⊕ L_ω ⊕ L_ω̄`**:
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18` R2.
4. **Real-dim count `dim_ℝ Herm_3 = 9`**:
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18` R3 / A.2.

The following cited source-stack content is load-bearing for Step 2 (named
obstruction):

5. **Radian-bridge no-go**:
   `KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20`.
6. **Radian-bridge irreducibility audit**:
   `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24`.
7. **Q-δ linking relation (names primitive P)**:
   `KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20` §4.

## Bottom line

**Verdict: SHARPENED bounded obstruction with partial positive closure.**

Step 1 closes positively: the **dimensionless** structural value
`φ_dimensionless = n_eff/d² = 2/9` is retained character-algebra
content, derived from C_3 conjugate-pair forcing (n_eff = 2) and
Plancherel-Frobenius dimension counting (d² = 9). This is exact
cited source-stack content, not a new admission.

Step 2 sharpens the obstruction: the PDG-matching Brannen circulant
formula requires `φ` as a literal radian value `2/9 rad`. No retained
native angle unit on Cl(3)/Z³ recovers the PDG match without admitting
the radian-bridge primitive `P` as load-bearing. Six native units
(cycle, Z_3-step, Bargmann-triangle, Plancherel-step, character-step,
selected-line Berry-per-step) all give `φ` as a transcendental in
their own native rational ratio.

Step 3 identifies Probe 19's `φ = 2/9 rad` admission with the
existing radian-bridge primitive `P`. The Probe 19 "magic angle" is
**not** an independent third admission distinct from BAE and `P`; it
is `P` re-named at the Brannen-circulant level.

The framework's open-import count for the BAE-campaign closure is
therefore unchanged at 2: `BAE + P`. The Probe 19 naming sharpens
visibility but does not add a new primitive.

The radian-bridge `P` remains the load-bearing structural primitive
for closing `φ`. Its minimal inputs (a), (b), (c) per Probe 20 §4
remain the candidate routes; none currently retained.
