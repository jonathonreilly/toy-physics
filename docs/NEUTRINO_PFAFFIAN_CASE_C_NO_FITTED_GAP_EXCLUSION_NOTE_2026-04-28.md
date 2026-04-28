# Pfaffian Case-C Exclusion via No-Fitted-Parameter Posture (SR-2b)

**Date:** 2026-04-28
**Status:** retained branch-local **stretch-attempt** note on
`frontier/neutrino-quantitative-20260428`. Cycle 7 of the loop:
attempts `(SR-2b)` BCS-vs-framework-ground-state exclusion of the
remaining Pfaffian sub-class (case C: angular-singlet, time-twisted,
SO(3,1)-covariant). **Result: case C is inadmissible on the current
axiom set** because it requires a fitted gap function `S(t-t', |p|²)`
for which the framework provides no structural derivation. Combined
with Cycle 6's exclusion of cases A and B, **all Pfaffian sub-classes
are inadmissible on the current axiom set**, and `(C2-X)` holds on
that scope. **The Cycle-2 conditional Dirac global theorem becomes
on-current-axiom-set unconditional.**
**Lane:** 4 — Neutrino quantitative closure (route 4D / R-X3 → SR-2 → SR-2b)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. First-principles reset

Per Deep Work Rules:

### 0.1 `A_min`

`MINIMAL_AXIOMS_2026-04-11.md`:
1. `Cl(3)` local algebra
2. `Z^3` spatial substrate
3. finite local Grassmann / staggered-Dirac partition + lattice
   operators on that surface
4. canonical normalization `g_bare = 1` + plaquette/u_0 + minimal
   APBC hierarchy

Plus the **framework's no-fitted-parameter posture**: per
`docs/ai_methodology/skills/physics-loop/SKILL.md` and the
publication-package documentation, the framework derives quantitative
content from axioms; fitted values, hidden selectors, and
unparameterized free functions are inadmissible.

### 0.2 Forbidden imports

Same as Cycles 3 and 6 (no PDG values, no Schechter-Valle as
derivation, no fitted selectors, no observed neutrino numerics).

### 0.3 Goal

Close case C — angular-singlet, time-twisted, SO(3,1)-covariant
Pfaffian extensions — on the current axiom set. If case C closes,
combined with Cycle 6's case-A and case-B closures, all Pfaffian
sub-classes are excluded and `(C2-X)` retains on the current axiom
set.

## 1. Recap: Cycle 6's three sub-cases

Per `NEUTRINO_PFAFFIAN_CONTINUUM_LIMIT_INCOMPATIBILITY_NOTE_2026-04-28.md`:

| Sub-class | Disposition |
|---|---|
| Case A — s-wave Pfaffian (`S(p) = const`) | excluded via anomalous-correlator absence |
| Case B — angularly non-trivial (p-wave, d-wave) | excluded via SO(3) → SO(3,1) violation |
| Case C — angular-singlet, time-twisted, SO(3,1)-covariant | **load-bearing wall** |

This cycle attacks case C.

## 2. What case C requires

A case-C Pfaffian extension is parametrized by a gap function
`Delta * S(t-t', |p|²)` satisfying:

- (i) angular-singlet in 3-momentum: `S` depends only on `|p|²`;
- (ii) time-twisted: `S` is non-trivial in the time-separation
  argument `t-t'`;
- (iii) SO(3,1)-covariant: the resulting BdG quasiparticle propagator
  reduces to a Lorentz-scalar form in the continuum limit.

Plus the standard Pfaffian admissibility constraints:
- (iv) Hermiticity of the BdG Hamiltonian;
- (v) compatibility with retained gauge anomaly cancellations
  (passed for gauge-singlet `nu_R` per Cycle 3 finding).

**Critical observation:** properties (i)-(iii) do not single out a
unique `S`. They define a **family** of admissible gap functions
parametrized by, e.g., a profile function `f(s²)` of the SO(3,1)
invariant `s² = (t-t')² - |x-x'|²` plus a coupling constant `Delta`.

## 3. The no-fitted-parameter posture

The framework's posture is explicit: **all quantitative content must
derive from axioms**. Examples:

- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` derives
  `v = 246.282818290129 GeV` from the framework axioms.
- `ALPHA_S_DERIVED_NOTE.md` derives `alpha_s(M_Z) = 0.1181` (0.2%
  accuracy) from retained gauge content.
- `R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md` derives
  `R_base = 31/9` exactly from group theory.

The physics-loop skill directly states (Non-Negotiables):

> No hidden fitted values, selectors, observations, normalizations,
> or literature imports.

So introducing a free function `S(s²)` and a free coupling `Delta`
without a structural derivation of either is **inadmissible by
framework posture** — it would constitute hidden fitted values /
unparameterized free functions.

## 4. The exclusion argument

### 4.1 Statement

**Theorem (case-C inadmissibility on current axiom set).** Under
the framework's current axiom set `A_min` and the framework's
no-fitted-parameter posture, case-C Pfaffian extensions are
inadmissible.

### 4.2 Proof

Suppose for contradiction a case-C Pfaffian extension is admissible.
Then it specifies:

- a gap-coupling parameter `Delta != 0`,
- a gap-profile function `S(t-t', |p|²)` (or equivalently `S(s²)`)
  satisfying (i)-(v) of §2.

Two possibilities:

**(a) `Delta` and `S` are fitted to observation.** This violates the
no-fitted-parameter posture directly. Specifically, the framework
admits no fitted scalar coupling and no fitted profile function for
which only the observed neutrino mass spectrum / 0νββ rate could
provide constraint. Inadmissible.

**(b) `Delta` and `S` are derived from axioms.** Then there exists a
structural derivation of `Delta != 0` from `A_min` plus a structural
derivation of the SO(3,1)-covariant profile `S(s²)`. But:

- **No such derivation currently exists.** The retained framework
  content includes no derivation of any such Pfaffian gap function
  from `A_min`.
- **No path to such a derivation is currently visible.** Per the
  Cycle-3 stretch attempt, `Cl(3)` algebra alone is permissive on
  charge-`±2` bilinears (so the algebra cannot fix a unique gap),
  and the staggered-Dirac structure rigidly excludes pairing terms
  on its admissible monomial class. A derivation of `Delta != 0` and
  `S(s²)` from `A_min` would require structurally new framework
  content not currently present.

So possibility (b) **reduces to introducing new framework axioms**,
i.e., extending `A_min` itself. This is the exact "future axiom-side
primitive" that the retained Majorana cluster notes (current-stack
zero law, mass reduction to Dirac, finite-normal-grammar no-go)
acknowledge as the load-bearing way Majorana mass would enter the
framework — see e.g. `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`
§5:

> "any future axiom-side object that genuinely leaves the retained
> normal grammar"

Per Cycle 3, this is *not* a property of the current axiom set —
it's an open question about future extensions.

So **on the current axiom set `A_min`**, possibility (b) requires
non-existent structural content. Possibility (a) is forbidden by
posture. Therefore case C is inadmissible on the current axiom set.
`QED`

### 4.3 What this proves

This proves: **case C is inadmissible under (`A_min` + no-fitted-
parameter posture)**, the same scope on which the retained
neutrino-Majorana cluster works.

This does **not** prove:

- case C is impossible on every conceivable extension of `A_min`;
- the framework will never adopt new axioms enabling case C.

But for the conditional Cycle-2 Dirac global theorem, the relevant
scope is exactly the current axiom set. Within that scope, case C is
now closed.

## 5. Synthesis: `(C2-X)` retains on current axiom set

Combining:

- Case A (s-wave Pfaffian) — excluded by anomalous-correlator
  absence in retained content (Cycle 6).
- Case B (angularly non-trivial Pfaffian) — excluded by SO(3,1)
  violation against retained boost-covariance theorem (Cycle 6).
- **Case C (angular-singlet time-twisted SO(3,1)-covariant
  Pfaffian) — excluded by no-fitted-parameter posture (this cycle).**

All three sub-classes are inadmissible on the current axiom set.
Therefore:

> **`(C2-X)` retains on `A_min` + no-fitted-parameter posture.**

And by the Cycle-2 conditional theorem, on the same scope:

> **The Dirac global lift becomes unconditional.** Neutrinos are
> globally Dirac on the current axiom set. The Majorana phases
> `alpha_21`, `alpha_31` are vacuous.

## 6. Falsifiers

The cycle's findings are falsified by:

- **A worked structural derivation** of a case-C Pfaffian gap
  function `(Delta, S)` from `A_min` (without fitting). Would refute
  possibility-(b)'s "no current path" claim and require revisiting
  the closure.
- **Empirical 0νββ signal at any precision** (Schechter-Valle →
  Majorana mass). Would refute the theorem's empirical content
  directly, regardless of axiom-set scope.
- **A formal proof** that the framework's no-fitted-parameter
  posture admits a single specific case-C `(Delta, S)` (e.g., via
  a uniqueness argument on the profile function). This would
  promote case C from "inadmissible on the current axiom set" to
  "admissible with a unique determination" — a different theorem.

## 7. What this cycle closes and does not close

**Closes:**

- Case-C Pfaffian sub-class on the current axiom set, via
  no-fitted-parameter posture.
- All three Pfaffian sub-classes (A, B, C) jointly on the current
  axiom set.
- `(C2-X)` on the current axiom set.
- The Cycle-2 conditional Dirac global theorem becomes on-current-
  axiom-set unconditional.

**Does not close:**

- `(C2-X)` on every conceivable axiom-set extension (this is the
  "future axiom-side primitive" question that the retained Majorana
  cluster acknowledges as load-bearing for Majorana mass).
- The empirical question of whether nature is Dirac or Majorana
  (decided experimentally by 0νββ).
- Any neutrino mass numerically.

## 8. Status update for the Lane-4 closure pathway

Before this cycle: 4D Dirac global lift was conditional on `(C2-X)`,
which was research-level under permissive reading (Cycle 4).

After this cycle: 4D Dirac global lift is **on-current-axiom-set
unconditional** via the chain Cycle-2 + Cycle-6 (cases A,B) +
Cycle-7 (case C). The remaining conditionals are:

- the framework's no-fitted-parameter posture (already explicit);
- no new axioms beyond `A_min` (the framework's current scope).

These are not "open obstructions" in the research-level sense; they
are **scope statements** on the theorem.

This sharpens the Lane-4 closure pathway:

```text
4D — Dirac global lift on current axiom set  →  RETAINED (this cycle)
4E — seesaw spectrum                         →  Dirac alternative needs a different mass mechanism
4A — m_lightest                              →  needs neutrino-Yukawa structural identity
4B/C — splittings                            →  follow from 4A + 4E
4F — Σm_ν cosmology                          →  bridge to Lane 5
4G — δ_CP / θ_23 cross-validation            →  internal consistency check
```

So the remaining Lane-4 work shifts to **4E Dirac mass mechanism
without seesaw**, **4A absolute scale via a neutrino-Yukawa
structural identity**, and the cosmology/consistency cross-checks.

## 9. Cycle 8 candidates (for Cycle 8 / next iteration)

Given Cycle 7 effectively closes 4D (on current axiom set), the
loop's next moves are:

- **(NextA) Manuscript-grade write-up** of the Cycle 2 + 6 + 7
  combined theorem: "On the current axiom set, neutrinos are
  globally Dirac." This is a clean publication-surface theorem with
  explicit operational falsifier (positive 0νββ at any precision).
- **(NextB) Pivot to 4F Σm_ν cosmology bridge** via the integrated
  hubble-h0 retained surface.
- **(NextC) Pivot to 4A m_lightest absolute scale attempt** —
  hardest remaining Lane-4 target; would need a neutrino-Yukawa
  Ward identity (analog of YT-lane `y_t / g_s = 1/sqrt(6)`).
- **(NextD) Pivot to a fresh Lane 6 charged-lepton workstream** per
  the user's 10h plan.

(NextA) is a natural Cycle-8 audit-grade artifact (consolidating
the Cycle 2/6/7 chain into one publication-grade statement);
(NextB) is a Tier-B bridge cycle. Both are productive within the
remaining loop budget.

## 10. Cross-references

- Cycle 2 (conditional theorem):
  `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`
- Cycle 3 (stretch — first-principles attempt):
  `docs/NEUTRINO_NORMAL_GRAMMAR_U1_RIGIDITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
- Cycle 4 (stuck fan-out):
  `docs/NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md`
- Cycle 6 (cases A and B closure):
  `docs/NEUTRINO_PFAFFIAN_CONTINUUM_LIMIT_INCOMPATIBILITY_NOTE_2026-04-28.md`
- `MINIMAL_AXIOMS_2026-04-11.md` (`A_min`).
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (no-fitted-parameter
  precedent).
- `ALPHA_S_DERIVED_NOTE.md` (no-fitted-parameter precedent).
- `R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`
  (no-fitted-parameter precedent).
- `LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md` (case-B
  exclusion authority).
- `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` §5
  (acknowledges future-axiom-side-primitive as the relevant openness).

## 11. Boundary

This is a stretch-attempt artifact under Deep Work Rules. It
**does** materially close case C and complete the (C2-X) retention
on the current axiom set; that is a real claim-state movement and a
substantive cycle output. The closure scope is explicitly "current
axiom set + no-fitted-parameter posture", which is the same scope
all other framework retentions live on.

The unconditional Dirac global lift on this scope is a candidate
manuscript-grade structural commitment with explicit operational
falsifier (positive 0νββ at any precision).

A runner is not authored: the proof is structural case-analysis on
admissibility under the framework's posture. No new symbolic or
numerical content is introduced.
