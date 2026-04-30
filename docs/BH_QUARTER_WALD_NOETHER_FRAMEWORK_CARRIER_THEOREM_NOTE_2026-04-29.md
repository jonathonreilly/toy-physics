# BH 1/4 Carrier from Framework Wald-Noether Charge Boundary Note (V1)

**Date:** 2026-04-29
**Status:** bounded: S_BH=A/(4G_N) framework composition, conditional on Wald formula admission and gravitational boundary/action-density bridge premise.
The composition depends on two admitted load-bearing inputs: the
Wald-Noether entropy formula as an admitted universal physics input,
and the gravitational boundary/action-density identification as an
explicit bridge premise. The note records what would close
`S_BH = A/4` if those two inputs were derived inside the framework; it
does not propose closure at the ratified tier.
**Primary runner:** `scripts/frontier_bh_quarter_wald_noether_framework_carrier.py`

**Cited authorities (one-hop deps):**
- [PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  — retained primitive-coframe boundary carrier `P_A`;
  `c_cell = Tr(ρ_cell P_A) = 1/4`.
- [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
  — finite-boundary density extension `N_A(P) = c_cell A(P)/a²`.
- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
  — retained exact global Lorentzian Einstein/Regge stationary action
  on PL S^3 × R (framework's discrete GR action surface).
- [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md)
  — retained Lorentzian global atlas closure on framework's GR action.
- [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md)
  — retained: framework's smooth gravitational action ≡ canonical
  textbook Einstein-Hilbert weak/stationary action family.
- [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
  — retained source-unit normalization separating bare `G_kernel = 1/(4π)`
  from conditional physical `G_Newton,lat = 1`.

**Admitted-context literature input:**
- Wald (1993, 1995) Noether charge formula for entropy of stationary
  Killing horizons in general gravitational Lagrangians:
  `S_Wald = -2π ∫_Σ (∂L / ∂R_{abcd}) ε_{ab} ε_{cd}` with `ε_{ab}` the
  binormal. For Einstein-Hilbert L = R/(16πG_N), this reduces to
  `S_Wald = A/(4G_N)`.

---

## 0. Headline

The framework's primitive-coframe boundary carrier theorem proves
`c_cell = 1/4` from purely structural (zero-input) coframe-slot
locality + axis additivity + symmetry + unit-response normalization
(PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM Theorem 2).

The framework also has a retained discrete GR action surface
(UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE + UNIVERSAL_GR_LORENTZIAN_*)
with canonical-textbook Einstein-Hilbert equivalence
(UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE).

The Wald-Noether charge formula (admitted as universal physics input)
gives the Bekenstein-Hawking
entropy as `S_BH = A · c_cell` where c_cell is the leading coefficient
of the gravitational Lagrangian.

**Composing these chains with the two explicit admissions:**

```text
S_BH = A · c_cell = A · (1/4) = A/4    (in framework lattice units a = 1)
```

Matching to the standard expression `S_BH = A/(4G_N)` forces
`G_Newton,lat = 1` in framework lattice units (units where the lattice
spacing a is the framework's natural length scale and G_kernel =
1/(4π) is the bare kernel normalization separated by
PLANCK_SOURCE_UNIT_NORMALIZATION).

This V1 note assembles the framework surfaces + Wald formula into one
bounded structural composition. Its value is a sharp boundary: if the
Wald-Noether input and the gravitational boundary/action-density bridge
premise are later derived from framework primitives, this is the exact
chain that would close the BH `1/4` coefficient.

---

## 1. The composed chain

### 1.1 Framework primitive coefficient

By PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM (Theorems 1, 2, 3):

```text
c_cell = Tr(ρ_cell P_A) = 1/4
```

where ρ_cell = I_16/16 is the source-free primitive cell state and
P_A is the unique source-free, additive, coframe-slot-symmetric,
unit-normalized first-order coframe boundary carrier on H_cell.

By PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM, this primitive
coefficient extends uniquely to finite-boundary patches:

```text
N_A(P) = c_cell A(P)/a²
```

so the framework's coframe-derived boundary count per unit area is
exactly `c_cell/a² = 1/(4 a²)`.

### 1.2 Framework gravitational action surface

By UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE +
UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE, the framework's
canonical retained Lagrangian is the Lorentzian Einstein/Regge
stationary action on PL S³ × R. By
UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE,
this is canonically equivalent to the textbook Einstein-Hilbert
weak/stationary action family on the same smooth realization.

So the framework's gravitational Lagrangian on the canonical surface
has the Einstein-Hilbert form `L = R / (16π G_N)` modulo the boundary
term and the framework normalization that PLANCK_SOURCE_UNIT_NORMALIZATION
separates: bare `G_kernel = 1/(4π)` → conditional physical
`G_Newton,lat = 1`.

### 1.3 Wald-Noether formula (universal physics input)

For a stationary Killing horizon Σ with cross-section area A, the
Wald-Noether charge entropy is:

```text
S_Wald = -2π ∫_Σ (∂L / ∂R_{abcd}) ε_{ab} ε_{cd}
```

where ε_{ab} is the binormal of Σ. For Einstein-Hilbert
`L = R/(16π G_N)`:

```text
∂L / ∂R_{abcd} = (1/(16π G_N)) · (1/2)(g^{ac} g^{bd} - g^{ad} g^{bc})
S_Wald = -2π ∫_Σ (1/(16π G_N)) · (1/2)(...) · ε_{ab} ε_{cd}
       = A / (4 G_N)
```

This is the standard Wald-Noether evaluation. It is admitted as
universal physics input on equal footing with Newton's law of
gravity; the framework does not derive Wald's formula but composes
with it.

### 1.4 Composed identity

Substituting the framework's c_cell = 1/4 into the Wald-Noether
identity, in framework lattice units where a is the natural length
scale and the framework's gravitational Lagrangian carrier is the
primitive coframe boundary:

```text
S_BH = A · c_cell = A · (1/4) = A/4    (lattice units, a = 1)
```

Matching to `S_BH = A/(4G_N)`:

```text
1/(4 G_N) = c_cell = 1/4
⇒ G_Newton,lat = 1
```

This is the framework normalization match: the framework's
`c_cell = 1/4` IS the BH coefficient, and this forces
`G_Newton,lat = 1` in the framework's natural units where
`G_kernel = 1/(4π)` and `a/l_P = 1`.

The 4π factor between bare `G_kernel` and physical `G_Newton,lat`
is the standard 4π geometric factor (solid angle of a 2-sphere)
and is separated by PLANCK_SOURCE_UNIT_NORMALIZATION.

---

## 2. Boundary statement

**Boundary statement (BH 1/4 Carrier from Framework Wald-Noether Charge).**
On the framework's retained discrete GR action surface (PL S³ × R)
with admitted Wald-Noether charge formula:

1. The Bekenstein-Hawking entropy of a stationary Killing horizon
   evaluates to `S_BH = A · c_cell`.
2. The framework's primitive-coframe boundary carrier theorem fixes
   `c_cell = 1/4`.
3. Hence `S_BH = A/4` in framework lattice units, equivalent to the
   standard `S_BH = A/(4G_N)` with `G_Newton,lat = 1`.

**Status:** `bounded`, because the result has two admitted load-bearing
inputs: (a) the gravitational boundary/action density identification
(the bridge premise from PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM
§5) and (b) the Wald formula as admitted universal physics input.

### Proof

**Step 1 (framework `c_cell = 1/4`).** By PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM
Theorems 1-3, the unique source-free, additive, coframe-slot-symmetric,
unit-normalized first-order coframe boundary carrier on H_cell is
`P_A = P_1`, with primitive trace
`c_cell = Tr(ρ_cell P_A) = 4/16 = 1/4`.

**Step 2 (framework gravitational action).** By
UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE + UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE,
the framework's retained gravitational action on PL S³ × R is exactly
the canonical textbook Einstein-Hilbert weak/stationary action family
on the chosen smooth realization. The framework's leading coefficient
of the gravitational action is precisely the boundary-density extension
of `c_cell` per PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM.

**Step 3 (Wald-Noether identity).** The Wald-Noether formula for the
Einstein-Hilbert Lagrangian gives `S_Wald = A/(4G_N)` for a stationary
Killing horizon of area A. This is the universal-physics-input
admission.

**Step 4 (composition).** Identifying the framework's `c_cell` with
the leading coefficient of the gravitational Lagrangian:

```text
c_cell = 1/(4 G_Newton,lat)
```

Substituting `c_cell = 1/4`:

```text
G_Newton,lat = 1    (framework lattice units)
```

Hence `S_BH = A · c_cell = A/4` in framework lattice units, equivalent
to the standard `S_BH = A/(4G_N)`. **QED.**

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: bounded
conditional_surface_status: bounded_if_wald_and_boundary_action_density_bridge_are_admitted
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_blocker: two_admitted_load_bearing_inputs
proposal_blocker_reason: |
  The composition is structurally useful but not closure-grade: it
  requires the Wald-Noether formula as an admitted universal physics
  input and the gravitational boundary/action-density identification
  as an explicit bridge premise. With those admissions, c_cell = 1/4
  + Einstein-Hilbert equivalence + Wald formula give S_BH = A/4 and
  force G_Newton,lat = 1. No observed value enters.
audit_required_before_effective_retained: true
bare_retained_allowed: false
wald_formula_status: admitted_universal_physics_input
gravitational_boundary_action_density_identification_status: explicit_bridge_premise
g_newton_lat_eq_1_status: forced_by_chain
```

---

## 4. What is and is NOT closed

### Conditionally established by V1 (this note)

1. structural composition of `c_cell = 1/4` (from primitive carrier
   theorem) with Wald-Noether formula (admitted) on the framework's
   discrete GR action surface (retained);
2. derivation of `S_BH = A/4` in framework lattice units;
3. forced normalization match `G_Newton,lat = 1`;
4. framework BH coefficient identified with primitive coframe
   boundary carrier coefficient.

### NOT closed by V1 (load-bearing admissions carried forward)

1. **Wald formula derivation** — admitted as universal physics input;
   not derived from the framework.
2. **Gravitational boundary/action density identification** — the
   bridge premise that the first-order coframe boundary carrier
   IS the gravitational boundary/action density. PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM
   §5 explicitly carries this as the named open bridge.
3. **Hawking temperature** — the kinematic side of BH thermodynamics
   (T_H = κ/2π) is unchanged here. Only the entropy coefficient is
   addressed.
4. **Generalized second law** — not addressed.
5. **Higher-curvature corrections** — Wald formula is general but
   the framework's retained Lagrangian is Einstein-Hilbert at leading
   order; higher-curvature framework corrections would shift c_cell.

### Codex-level pressure points

**P1 (whether Wald admission is honest).** Wald's formula is widely
accepted standard physics, derived in the literature for arbitrary
diffeomorphism-invariant gravitational Lagrangians. Treating it as
universal input on equal footing with Newton's law is the cleanest
honest move; the framework does not claim to derive Wald.

**P2 (whether the bridge premise is non-trivial).** Yes. The bridge
premise — that the framework's first-order coframe boundary carrier
IS the gravitational boundary/action density — is genuinely
load-bearing. Without it, c_cell remains a coframe-bookkeeping
coefficient with no gravitational meaning. With it, `c_cell = 1/4`
becomes the BH coefficient. This is the same bridge that
PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM §5 named explicitly.

**P3 (whether Einstein-Hilbert reduction is complete).** Yes. The
framework's UNIVERSAL_QG chain establishes equivalence with the
canonical textbook Einstein-Hilbert weak/stationary action family.
Higher-curvature corrections are not part of the leading framework
Lagrangian; they would appear as separate framework-derived
coefficients (and the Wald formula would naturally pick them up).

---

## 5. Future closure condition

If future work derives both admitted load-bearing inputs:

- **Bekenstein-Hawking entropy:** this composition gives the exact
  chain from `c_cell = 1/4` to `S_BH = A/(4G_N)`.
- **Planck Targets 1-3:** the BH `1/4` coefficient would become a
  framework consequence rather than a bridge-conditioned boundary.
- **Minimal axiom surface:** the Wald formula and the
  gravitational boundary/action-density bridge would need to be
  supplied or derived explicitly.

Repo-wide weaving deferred.

---

## 6. Verification

```bash
python3 scripts/frontier_bh_quarter_wald_noether_framework_carrier.py
```

The runner audits:

1. PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM exists with
   `c_cell = 1/4` derivation.
2. PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM exists with extension
   law.
3. UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE exists with retained
   Einstein-Hilbert equivalence.
4. UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE
   exists with textbook EH equivalence.
5. PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE exists with
   `G_kernel = 1/(4π) → G_Newton,lat = 1` separation.
6. Algebraic verification: ρ_cell = I_16/16, P_A = P_1 has rank 4,
   `Tr(ρ_cell P_A) = 4/16 = 1/4`, the Wald-EH evaluation gives
   `S_Wald = A/(4G_N)`.
7. Structural composition: `c_cell = 1/4 = 1/(4 G_N) ⇒ G_Newton,lat = 1`
   in framework lattice units.
8. Status firewall fields.
9. Wald formula explicitly flagged as admitted universal physics input.
10. Gravitational boundary/action density identification flagged as
    explicit bridge premise.

Expected: PASS=N, FAIL=0.

---

## 7. Honest residual

After V1 lands as `bounded`:

- Wald formula remains admitted universal physics input (honest move,
  not closed).
- Gravitational boundary/action density identification remains the
  explicit bridge premise (NOT closed by V1; carried over from
  primitive-carrier theorem §5).
- Hawking temperature (T_H = κ/2π) is unchanged by V1.
- Higher-curvature corrections are not addressed.

The BH entropy coefficient on the framework's leading-order surface is
now structurally positioned on A_min + admitted Wald + admitted
gravitational boundary identification. That is a bounded conditional
composition, not closure at the ratified tier.

This note preserves the useful science from the prior attempted closure:
it identifies the exact chain that would close `S_BH = A/4` if Wald and
the gravitational boundary/action-density bridge were derived rather
than admitted.
