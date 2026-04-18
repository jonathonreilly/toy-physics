# Observable-Bank Exhaustion — Atlas Exhaustion Theorem (Obstruction + New-Gap)

**Date:** 2026-04-17
**Status:** OBSTRUCTION + NEW-GAP at this note's scope. Names the three promotion lanes (P1 / P2 / P3) that can close the selector gate; integrated closure is the downstream PMNS-as-f(H) closure via P3.
**Script:** `scripts/frontier_dm_neutrino_observable_bank_exhaustion_theorem.py`
**Runner:** `PASS = 36, FAIL = 0`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

This note attempts to close the selector law on the `Z_3` doublet block by
**extending the observable bank** beyond the currently-exhausted
transport/source/slot/CP bank. Specifically: the runner searches the
retained DM/neutrino/flavor/PMNS/cosmology atlas for a physical
observable that

- (a) is **retained** (atlas-grade; not post-axiom invented),
- (b) is expressible as `f(H(m, delta, q_+))` on the live source-oriented sheet,
- (c) **genuinely varies** across the chamber `q_+ >= sqrt(8/3) - delta`,
- (d) has a **specific observational target** recorded on the retained atlas.

If any one observable satisfies all four, the chamber function can be
level-set against its observational value and the selector gate closes (CASE 1/2). If
some observable satisfies (a)+(b)+(c) but fails (d), that is CASE 3
(new gap). If none of the surveyed observables satisfies all four, that
is CASE 4 (obstruction) — the observable bank is exhausted on the
current retained atlas, and closure requires promoting a new object.

**This note records the negative outcome.** It is a structurally strong
**CASE 4 OBSTRUCTION** on observables O1–O8, plus a **CASE 3 NEW-GAP**
on pure `H`-reader invariants.

## Structural theorem (retained-atlas-native)

**Theorem (Observable-bank exhaustion).** Every atlas-retained
physical observable that possesses an observational target value in the
retained atlas factors through the **frozen** current-bank signature

```
B_frozen = (gamma, E1, E2, cp1, cp2, K00, a_*, b_*, T_slot)
```

on the live DM-neutrino source-oriented sheet. By the retained theorem
`DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM`,
every entry of `B_frozen` is exact-constant on the chamber. Therefore
every retained physical observable with an atlas-retained observational
value is **chamber-blind**.

Consequently, no observable in the retained atlas bank can uniquely
pin `(delta_*, q_+*)` on the chamber.

**Proof sketch.** The retained downstream observables split into three
families:

1. **Gauge-sector observables** (e.g. `R = Omega_DM/Omega_B ~ 5.48` via
 `alpha_plaq` from the `Cl(3)` normalization `g_bare = 1`, and all
 `Omega_X` quantities derived from it). None reads the neutrino
 doublet block.

2. **Leptogenesis/neutrino observables via the source package**
 (`eta/eta_obs`, `m_3 = y_nu_eff^2 v^2 / M_1`, atmospheric
 `Dm^2_31 = 2.539e-3 eV^2`). All factor through
 `(gamma, E1, E2, K00) in B_frozen`. Chamber-blind by the retained
 blindness theorem.

3. **CP / slot observables** (`cp1, cp2, a_*, b_*, T_slot`). All frozen
 on the active sheet by the intrinsic-slot and CP theorems.

Items not yet closed on the atlas (PMNS angles `theta_ij`, solar gap
`Dm^2_21`, muon `g-2`, LFV) have **no atlas-retained observational
target as `f(H)`**; they fail criterion (d) by absence of the retained
derivation. QED.

## Observable-by-observable survey

| # | Observable | retained? | `f(H)`? | varies on chamber? | obs target? | closes? |
|---|------------|-----------|---------|--------------------|-------------|---------|
| O1 | `R = Omega_DM/Omega_B` (5.48 vs 5.47) | Y | **N** | N | Y | no |
| O2 | `m_DM` (DM particle mass) | Y | **N** | N | Y | no |
| O3 | Atmospheric `Dm^2_31` via `m_3` | Y | **N** | N | Y | no |
| O4 | PMNS `θ_12, θ_13, θ_23` | **N** | Y | Y | **N** | no |
| O5 | DM direct/indirect `sigma` | Y | **N** | N | Y | no |
| O6 | Muon `g-2`, LFV | N | N | N | Y | no |
| O7 | Neutrino mass scale (see-saw) | Y | **N** | N | Y | no |
| O8 | `eta/eta_obs` on PMNS-assisted route | Y | Y | **N (on chamber)** | Y | no |

**Joint intersection (retained & `f(H)` & varies & observational) is
EMPTY.** This is the CASE 4 obstruction.

### Per-observable rationale

**O1. `R = Omega_DM/Omega_B`.** Retained (0.25% agreement with
`R_obs = 5.47` at the `g_bare = 1` Cl(3) normalization). Routes through
`alpha_plaq` (gauge sector), not through the neutrino active doublet
block. Provenance: `G_BARE_DERIVATION_NOTE.md`,
`OMEGA_LAMBDA_DERIVATION_NOTE.md`. **Not a function of `H(m, delta, q_+)`.**
Chamber-blind.

**O2. `m_DM`.** Retained DM provenance uses imported perturbative QFT
(`sigma_v = pi alpha_s^2 / m_DM^2`) plus `alpha_s`/`alpha_plaq`; does
not read the neutrino doublet block.

**O3. Atmospheric `Dm^2_31` via `m_3`.** On the retained diagonal
benchmark,
```
m_3 = y_nu_eff^2 v^2 / M_1,
y_nu_eff = g_weak^2 / 64,
v = M_Pl C alpha_LM^16,
M_1 = M_Pl alpha_LM^8 (1 - alpha_LM/2),
```
giving `m_3 = 5.058e-2 eV` and `Dm^2_31 = 2.539e-3 eV^2`. Authority:
`DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md`. **None of
`y_nu_eff, v, M_1` depend on `(delta, q_+)`.** Chamber-blind.

**O4. PMNS angles.** `DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE`
explicitly records: *"This note still does not derive: the solar gap
`Dm^2_21`; the full PMNS / non-universal Yukawa texture."* The
`NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE` likewise defers
*"full PMNS / solar-splitting closure"*. Hence PMNS `theta_ij` are
atlas-**open**, not atlas-retained. Closure via PMNS observables would
require first promoting PMNS to the retained surface.

**O5. DM direct/indirect-detection `sigma`.** Imported QFT cross-section;
not a function of `H`.

**O6. Muon `g-2`, LFV.** Not on the retained atlas as `f(H)`.

**O7. See-saw mass scale.** Same as O3.

**O8. `eta/eta_obs` on the PMNS-assisted route.** The PMNS-assisted
transport-extremal witness
(`DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16`)
achieves `eta/eta_obs = 1` on a 5-real parameter space
`(xbar, ybar, x_close, y_close, delta_PMNS)`, not on the 2-real
`(delta, q_+)` chamber. The image of the PMNS route on the active sheet
projects through the frozen `B_frozen` bank and is chamber-blind. The
transport chamber-blindness runner already verifies this.

## The CASE 3 new-gap: pure `H`-reader invariants

The invariants `{det(H), Tr(H^2), ||K_doublet||_F^2}` are retained
(axiom-grade), are functions of `H(m, delta, q_+)`, and vary across the
chamber. The runner verifies, at the five retained candidate points
(A = Schur-Q, B = det-crit, C = Tr(H²)-bdy, D = K_12 char-match,
E = parity-mixing F1-min):

| Candidate | `(m, δ, q_+)` | `det(H)` | `Tr(H^2)` | `‖K_dbl‖_F^2` |
|-----------|-------------|----------|-----------|----------------|
| A | `(0.5, √6/3, √6/3)` | `+1.5700` | `7.6960` | `1.1486` |
| B | `(0.613, 0.964, 1.552)` | `+7.0765` | `17.1560` | `3.3258` |
| C | `(0.385, 1.268, 0.365)` | `-0.2743` | `5.0040` | `0.4830` |
| D | `(0.0, 0.800, 1.000)` | `+2.5006` | `8.5621` | `2.3972` |
| E | `(4√2/9, √6/2−√2/18, √6/6+√2/18)` | `-0.0445` | `5.4780` | `0.2461` |

The spread across A..E for each invariant exceeds machine precision —
these ARE right-sensitive in `(delta, q_+)`.

**But no retained-atlas experiment reads `det(H)`, `Tr(H^2)`, or
`||K_doublet||_F^2` as a physical observable** (with an atlas-retained
observational value). These are axiom-grade algebraic invariants of the
neutrino source-oriented `H` matrix; they are not directly measurable
at present on the atlas.

This is the CASE 3 new-gap: chamber-varying retained invariants with no
observational target.

## Narrower-gap statement

**Before this note:** selector was known to be open by the obstruction
theorems (info-geom, cubic variational, holonomy,
parity-mixing functional-selection ambiguity) and by the Physics-
Validation chamber-constancy of `eta/eta_obs`. The remaining open object
was described as "a selector that couples to a bank-unblinded observable
on the chamber", without further stratification.

**After this note:** The open object is strictly narrower — it is ONE of
exactly three explicit promotion lanes:

- **(P1) Observable-bank promotion.** Add a NEW retained atlas
 observable that reads `H(m, delta, q_+)` and admits an atlas-grade
 observational target. This would directly close selector via level-set on
 that observable. Candidates: a retained measurement bridge for
 `det(H)`, `Tr(H^2)`, `||K_doublet||_F^2`, `K_12` phase, or another
 chamber-varying `H`-reader. None is currently retained.

- **(P2) Selector-principle promotion.** Add a NEW sole-axiom variational
 / canonical-functional selection principle that picks one chamber-
 varying `H`-reader invariant as the physical selector objective, and
 whose chamber minimum (or critical point) is the physical
 `(delta_*, q_+*)`. This is the (G-Var) / functional-selection
 ambiguity track already flagged in the info-geometric selection obstruction and the parity-mixing selection obstruction.

- **(P3) Atlas extension of neutrino phenomenology.** Promote PMNS
 angles `θ_12, θ_13, θ_23` and/or the solar gap
 `Dm^2_21` to retained, and derive their atlas form as a function of
 `H(m, delta, q_+)` — after which the observed values of those PMNS
 quantities level-set `(delta_*, q_+*)`. This is the largest-scope
 lane; it simultaneously closes selector and the PMNS / solar-splitting
 open objects.

No other lane closes selector on the current retained atlas.

## What this note establishes positively

1. **Atlas-exhaustion theorem (retained-atlas-native).** Every
 observable in the retained atlas with an atlas-grade observational
 value factors through the frozen-on-chamber bank `B_frozen`. Chamber-
 blind by the blindness theorem.

2. **Observable-by-observable survey (O1..O8).** Each of the eight
 candidate observable classes is classified against the four criteria
 (retained, `f(H)`, varies, observational). Joint intersection is
 EMPTY.

3. **Pure `H`-reader scalars classified.** The axiom-grade invariants
 `{det(H), Tr(H^2), ||K_doublet||_F^2}` are chamber-varying but lack
 atlas-retained observational targets. Explicit CASE 3 new-gap.

4. **Three explicit promotion lanes (P1, P2, P3).** The selector gate open object
 is now stratified. Any future selector attempt must choose one.

## Runner-verified content

The runner executes 36 PASS / 0 FAIL checks across five parts:

- **Part 1 (O1..O8 survey).** For each observable, the runner records
 the four criteria and asserts the joint intersection is EMPTY.
- **Part 2 (chamber-blindness at five candidates).** Re-verifies the
 retained current-bank blindness theorem at A, B, C, D, E; extracts
 `|gamma|, |E1|, |cp1|, |cp2|` from the positive representative of
 `H(m, delta, q_+)` and matches the exact-package values (modulo the
 known lift branch on `|E1|` at large `|delta|`, documented in the
 Physics-Validation note).
- **Part 3 (eta/eta_obs chamber-constancy).** Confirms
 `eta/eta_obs = 0.188785929502` at every candidate; the level set
 `eta/eta_obs = 1` is empty on the chamber.
- **Part 4 (pure `H`-reader variation).** Prints the candidate table
 above and asserts each of `det(H), Tr(H^2), ||K_doublet||_F^2` has
 chamber-spread greater than `1e-3`.
- **Part 5 (verdict).** Records the CASE 3 + CASE 4 outcome and the
 three promotion lanes.

## Atlas inputs used

All retained / theorem-grade:

- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md)
 — frozen bank on the chamber.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_FULL_CLOSURE_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_FULL_CLOSURE_BOUNDARY_NOTE_2026-04-16.md)
 — explicit current-bank closure boundary.
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
 — affine chart `H(m, delta, q_+)` and generators.
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
 — chamber `q_+ >= sqrt(8/3) - delta`.
- [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md)
 — `m_3`, `Dm^2_31` derivation (O3/O7 chamber-blindness).
- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
 — local post-EWSB Dirac operator `Gamma_1`; no `(delta, q_+)` dependence.
- [G_BARE_DERIVATION_NOTE.md](./G_BARE_DERIVATION_NOTE.md)
 — `R = Omega_DM/Omega_B` via `alpha_plaq` and `g_bare = 1` (O1 chamber-blindness).
- [OMEGA_LAMBDA_DERIVATION_NOTE.md](./OMEGA_LAMBDA_DERIVATION_NOTE.md)
 — cosmology chain downstream of `R`.
- [DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md)
 — PMNS-side selector bank CP-sheet blindness (O8).
- [DM_NEUTRINO_TRANSPORT_CHAMBER_BLINDNESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_TRANSPORT_CHAMBER_BLINDNESS_THEOREM_NOTE_2026-04-17.md)
 — prior chamber-blindness at A..D (this note extends to E = parity-mixing F1).
- [DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md)
 — candidate E and functional-selection ambiguity.

No new axioms. No invented observable. No selector promotion.

## Position on publication surface

This note is **not** flagship publication-grade on its own. It is a
**structural obstruction + narrower-gap stratification** of the selector gate open
object:

- atlas obstruction row in
 [DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md)
 under the DM neutrino source-surface family, sibling to the
 info-geometric / cubic-variational / parity-split obstructions, the
 parity-mixing F1 candidate, and the transport chamber-blindness
 theorem.
- This note does not close the DM flagship gate on its own. It names
 the three promotion lanes (P1, P2, P3) that can close it. The
 integrated closure is the downstream PMNS-as-f(H) closure, which
 realises P3 explicitly.
- The observable-bank-extension lane is classified as CASE 3 + CASE 4.
 Any future selector attempt along observable-bank lines must cite one
 of P1 / P2 / P3 and supply the missing promotion; P3 is realised by
 the PMNS-as-f(H) closure.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_observable_bank_exhaustion_theorem.py
```

Current expected: `PASS = 36, FAIL = 0`.

## What this file must never say

- that selector is closed;
- that the DM flagship gate is closed;
- that PMNS angles are on the retained atlas as `f(H(m, delta, q_+))`
 (they are not — PMNS closure is atlas-open);
- that the pure `H`-reader invariants have an atlas-retained
 observational target (they do not — CASE 3 new-gap);
- that any chamber candidate (A..E) is physics-selected by an
 observable in the retained atlas (all are chamber-blind);
- that the PMNS-assisted `eta/eta_obs = 1` witness lives on the
 chamber (it does not);
- that P1/P2/P3 have been supplied (none has been).

If any future revision of this note tightens those boundaries, it must
cite a new source on the live retained/promoted surface. Until then,
the safe read is: **observable-bank exhausted by retained theorem;
the selector gate open with three explicit promotion lanes (P1/P2/P3) now documented**.
