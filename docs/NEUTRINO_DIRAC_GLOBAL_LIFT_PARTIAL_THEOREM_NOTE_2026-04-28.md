# Neutrino Dirac Global Lift — Partial Theorem with Named Obstruction

**Date:** 2026-04-28
**Status:** support conditional theorem for Lane 4 gate isolation; no
unconditional Dirac closure and no numerical neutrino-mass claim. Lifts the
current-stack Majorana zero law (`mu_current = 0`) to a conditional global
statement on the current framework content and identifies the **single
load-bearing premise** that would make the lift unconditional: a **charge-2
primitive class exhaustion theorem** showing that no admissible framework
extension can introduce a fermionic charge-`±2` carrier outside the current
class.
**Lane:** 4 — Neutrino quantitative closure (route 4D)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. Statement

**Theorem (Conditional Dirac Global Lift).** Adopt:

- (P1) the retained current-stack Majorana zero law:
  `mu_current = 0` for the canonical one-generation Majorana block
  `A_M(mu) = mu * J_2`
  (`NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`);
- (P2) the retained three-generation lift:
  `M_R,current = 0_(3 x 3)` on the retained three-generation surface
  (`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` §1);
- (P3) the retained finite normal grammar's exact fermion-number
  `U(1)` symmetry (which kills the charge-`±2` Majorana coefficient
  on the current grammar)
  (`NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`);
- (P4) the retained current-atlas non-realization: no atlas-listed
  beyond-scalar primitive on `main` is a fermionic charge-`±2`
  carrier
  (`NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md`);
- (P5) the Pfaffian-no-forcing theorem: nothing built only from
  current retained normal data can force `mu != 0` behind the scenes
  (`NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md`);
- (P6) the retained mass-reduction-to-Dirac on the admitted Higgs /
  CW electroweak-scalar lane: with `M_R = 0`, the remaining mass-
  closing object is the Dirac Yukawa `Y_nu`
  (`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`);
- **(Conditional premise C2-X) Charge-2 primitive class exhaustion:**
  no admissible extension of the framework on `Cl(3)/Z^3` can
  introduce a fermionic charge-`±2` primitive outside the retained
  class.

Then on **all framework extensions consistent with (C2-X)**, the
neutrino sector is **globally Dirac**: `mu = 0` everywhere, no
Majorana mass amplitude is admissible, and the Majorana phases
`alpha_21`, `alpha_31` are vacuous.

**Corollary (current-stack reading):** without the conditional premise
(C2-X), the lift remains current-stack only: the framework currently
exhibits Dirac-only behavior, but the framework could in principle
admit a charge-2 primitive that breaks the zero law in a future
extension.

**Falsifier of the conditional theorem:** a positive 0νββ signal at
any experimental precision falsifies (C2-X) (per Schechter-Valle: any
positive 0νββ rate implies Majorana mass for at least one neutrino).

## 1. Retained inputs (all on `main`)

| Identity | Authority |
|---|---|
| One-gen canonical local Majorana block `A_M(mu) = mu * J_2` | `NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md` |
| `mu_current = 0` (current-stack zero law) | `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` |
| Three-gen lift `M_R,current = 0_(3x3)` | `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` |
| Fermion-number `U(1)` on current normal grammar | `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` |
| Current-atlas non-realization | `NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md` |
| Pfaffian no-forcing | `NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md` |
| Mass reduction to Dirac (on admitted Higgs / CW lane) | `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` |
| Closed Majorana construction classes (Native-Gaussian, Lower-Level-Pairing) | `NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md`, `NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md` |

## 2. Proof of the conditional theorem

### 2.1 Step 1 — Current-stack zero is exact

By (P1), the canonical local Majorana block is `A_M = 0 * J_2` on the
current retained stack. By (P2), the three-generation lift is
`M_R,current = 0_(3x3)`.

By (P3), the retained finite normal grammar carries exact fermion-
number `U(1)`, which forbids any charge-`±2` Majorana coefficient.

By (P4)+(P5), the current atlas contains no charge-`±2` primitive,
and nothing built only from current retained normal data can force
`mu != 0`.

So **on the current retained stack, the Dirac lane is exact.** This
is what (P1)-(P5) jointly establish.

### 2.2 Step 2 — Globalization step (where (C2-X) enters)

A future framework extension could in principle introduce a new
admissible charge-`±2` primitive that:
- generates a nonzero Majorana coefficient `mu != 0`, or
- breaks the fermion-number `U(1)` of the retained finite normal
  grammar, or
- realizes a `nu_R` primitive with charge-`±2` content that the
  current atlas non-realization theorem does not yet rule out
  globally.

(C2-X) is precisely the assumption that no such extension exists
within the framework's admissibility constraints. **Under (C2-X)**,
the retained charge-`0` normal grammar is the **complete**
fermion-number-carrying class, and the zero law extends from
"current-stack" to "globally on every admissible extension".

By (P6), with `M_R = 0` globally and the admitted Higgs / CW lane,
the remaining mass-closing object is `Y_nu`. The framework's neutrino
sector is therefore globally Dirac under (C2-X).

This proves the conditional theorem. `QED`

## 3. The single load-bearing premise (C2-X)

The "charge-2 primitive class exhaustion" is the only premise the
proof requires beyond the retained content (P1)-(P6). It is **not
currently retained**. The source notes explicitly preserve this
openness:

> [Current-stack zero law §6 "What this does not close"]
> "This note does NOT prove that no future extension can ever
> generate `mu != 0`."

> [Mass reduction to Dirac §10 "Cannot claim"]
> "The framework has already chosen Dirac neutrinos over Majorana
> neutrinos in nature."

So (C2-X) is the explicit open obstruction.

## 4. Candidate routes to retain (C2-X)

The lift becomes unconditional if (C2-X) is retained on the framework
surface. Candidate routes:

### (R-X1) Anomaly-cancellation exhaustion

The retained SM gauge-anomaly cluster (e.g., recent
`SM_ACCIDENTAL_BL_PROOF`, `SM_GIM_NEUTRAL_CURRENT_PROOF`,
`SM_MAJORANA_PMNS_COUNT_PROOF`, `SM_QUARK_FLAVOR_COUNT_PROOF`)
constrains admissible matter content via anomaly cancellation.
A direct proof that adding any charge-`±2` fermionic primitive to
the retained content breaks anomaly cancellation would close (C2-X).

**Route state:** the anomaly-cancellation work focuses on the
SM matter content as already retained. An exhaustion direction
("no admissible additional matter content has charge-`±2`") has
not been articulated as a separate theorem. **Open structural
target.**

### (R-X2) Representation-theory constraint on `Cl(3)/Z^3` carriers

The minimal axiom stack `Cl(3)` algebra + `Z^3` substrate may
bound the admissible representation content of fermion primitives
to charge-0 or charge-`±1`. A direct rep-theory argument that
charge-`±2` representations are not realizable as primitives on
this substrate would close (C2-X).

**Route state:** not currently articulated. Would require an explicit
representation classification on `Cl(3)/Z^3`'s admissible carrier
class.

### (R-X3) Finite-normal-grammar fermion-number `U(1)` rigidity

(P3) establishes fermion-number `U(1)` on the **current** normal
grammar. A rigidity theorem showing that any normal-grammar
extension consistent with `Cl(3)` algebra **must preserve**
fermion-number `U(1)` would extend (P3) globally and close (C2-X).

**Route state:** the current normal-grammar finite-normal-grammar no-go
gives the local result. A rigidity-style globalization is the
natural extension. **Most direct candidate path.**

### (R-X4) Schechter-Valle-side falsifier as empirical proxy

A null result on 0νββ at next-generation precision (KamLAND-Zen,
LEGEND, nEXO) progressively tightens the empirical bound on
admissible Majorana mass. While not a structural proof of (C2-X),
it sharpens the conditional theorem's empirical falsifier.

**Route state:** experimental program; not a Lane-4-internal closure
route.

## 5. What this theorem closes and does not close

**Closes (this cycle):**

- A sharp **conditional Dirac global lift** on the retained content
  + (C2-X).
- An explicit identification of (C2-X) as the load-bearing premise.
- Four candidate retention routes for (C2-X), with (R-X3) flagged
  as the most direct.
- Mirror of the hubble-h0 `(C1)` and `(C2)` gate-isolation pattern:
  a single residual premise named on a primitive algebraic block.

**Does not close:**

- The unconditional global lift. (C2-X) remains an open premise.
- (R-X1), (R-X2), (R-X3), (R-X4). All four are hypothetical routes;
  none is currently active as a Lane-4-internal cycle.
- Any neutrino mass numerically.

## 6. Falsifier (operational, conditional)

The conditional theorem predicts: on every admissible framework
extension, the neutrino sector is Dirac, with no Majorana phases.
This is operationally falsified by:

- **Direct (empirical):** any positive 0νββ signal at any precision
  (Schechter-Valle implies Majorana mass).
- **Structural (theoretical):** a worked admissible framework
  extension that introduces a charge-`±2` primitive consistent with
  retained anomaly cancellations and `Cl(3)/Z^3` substrate.

The first falsifier acts on the conditional theorem's empirical
content. The second falsifier acts on (C2-X) directly — exhibiting
such an extension would refute (C2-X) and reduce the theorem back to
current-stack only.

## 7. How this advances Lane 4

Before this cycle, Lane 4 was framed with seven derivation targets
(per `NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md`). Target 4D
(Dirac vs Majorana global lift) was the cleanest Phase-1 candidate.

After this cycle, target 4D reduces to a single open premise (C2-X)
plus four candidate retention routes. The cycle output is:

- the conditional theorem (support structure;
  unconditional under (C2-X));
- the named obstruction (C2-X);
- the candidate routes (R-X1, R-X2, R-X3, R-X4).

Cycle 3 candidate per Deep Work Rules: **stretch attempt on the
audit-quota counter trigger.** With Cycles 1 and 2 both closing as
audit-grade / blocker-isolation outputs, Cycle 3 must be a stretch
attempt on a named hard residual. **(C2-X)** is the natural
candidate, and **(R-X3) finite-normal-grammar `U(1)` rigidity** is
the most direct attack.

## 8. Cross-references

- `docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` (P1)
- `docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`
- `docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` (P3)
- `docs/NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md` (P4)
- `docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md` (P5)
- `docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` (P2, P6)
- `docs/NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md` (closed
  construction class)
- `docs/NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md` (closed
  construction class)
- `docs/NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md` (Cycle 1)
- Loop pack at
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.
- Schechter-Valle (1982) — admitted convention for the falsifier
  statement.

## 9. Boundary

This is a **conditional structural theorem** on a support/open Lane 4
surface. It does not promote any input to retired status, does not retain any
neutrino mass numerically, and does not unconditionally close 4D.
It produces the conditional lift + the named obstruction (C2-X) +
candidate routes for retaining (C2-X).

A runner is not authored: the proof is structural case-analysis on
the retained Majorana cluster + the named open premise. No new
symbolic or numerical content is introduced.

The output is honest first-principles work with a named obstruction
— valid under the new physics-loop skill's Deep Work no-churn
exception:

> An honest first-principles attempt with named obstructions is valid
> progress even without closure.
