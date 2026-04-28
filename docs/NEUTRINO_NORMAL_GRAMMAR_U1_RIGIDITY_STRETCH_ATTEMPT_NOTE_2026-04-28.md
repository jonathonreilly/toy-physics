# Normal-Grammar `U(1)` Rigidity Stretch Attempt — First-Principles Work From `A_min`

**Date:** 2026-04-28
**Status:** retained branch-local **stretch-attempt** note on
`frontier/neutrino-quantitative-20260428`. First-principles attempt to
retain `(C2-X)` (charge-2 primitive class exhaustion) via route
`(R-X3)` finite-normal-grammar `U(1)` rigidity globalization. Per the
new physics-loop skill's Deep Work Rules audit-quota threshold (Cycles
1, 2 both audit-grade), this cycle is mandatory. Output: **partial
structure** + **sharper obstruction** identified at substrate-class
admissibility, plus a worked failed derivation with the load-bearing
wall named.
**Lane:** 4 — Neutrino quantitative closure (route 4D / R-X3)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. First-principles reset (per Deep Work Rules)

### 0.1 Minimal allowed premises (`A_min`)

Per `MINIMAL_AXIOMS_2026-04-11.md`:

1. **Local algebra:** physical local algebra is `Cl(3)`.
2. **Spatial substrate:** physical spatial substrate is the cubic
   lattice `Z^3`.
3. **Microscopic dynamics:** finite local Grassmann / staggered-Dirac
   partition with lattice operators built on that surface.
4. **Canonical normalization and evaluation surface:**
   `g_bare = 1` + accepted plaquette / `u_0` + minimal APBC hierarchy
   block.

### 0.2 Forbidden imports (this attempt)

The attempt may **not** rely on:

- observed neutrino masses, splittings, mixing angles;
- PDG / global-fit values for any physical observable as derivation
  input;
- the Schechter-Valle theorem (admissible only as **falsifier**
  statement of the conditional theorem, not as derivation premise);
- any inflated retained surface beyond `A_min` (e.g., the YT-lane
  Ward identity or the hubble-h0 cosmology surface);
- any fitted selector or hidden coefficient.

### 0.3 Goal

Attempt to prove: **every framework extension consistent with `A_min`
preserves the fermion-number `U(1)_V` symmetry on the matter sector.**

If proved, this retains `(C2-X)` and unconditionally lifts the partial
Dirac global theorem (Cycle 2) to globally Dirac.

If not proved, identify the load-bearing wall.

## 1. The local result restated

`NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` establishes:

> On the **current** retained finite microscopic grammar, every
> admitted monomial has equal counts of `c` and `c^dag`. Therefore
> the global fermion-number `U(1)`
> `c -> e^(i theta) c, c^dag -> e^(-i theta) c^dag`
> is exact, and any charge-`±2` operator (e.g., the same-chirality
> Majorana bilinear `nu_R^T C P_R nu_R`) has zero expectation.

The local result rests on the **grammar rule**: admitted monomials are
charge-zero. This rule is not derived from `A_min` directly; it is a
property of the *current* normal grammar.

The rigidity question is whether this grammar rule is itself **forced**
by `A_min` on every admissible extension.

## 2. Attempt 1 — `Cl(3)` algebra rigidity

### 2.1 The angle

`Cl(3)` has a graded structure with even and odd subspaces. Fermion
bilinears decompose into `Cl(3)`-equivariant operators. **If**
`Cl(3)` admits no irreducible representation that carries fermion-
number charge `±2` as a primary local operator, then the grammar
rule is forced.

### 2.2 What's true

`Cl(3)` is the eight-dimensional Clifford algebra `Cl_3(R) ~= M_2(C)`.
On a single fermion site the fermion modes carry the spinor
representation. Bilinears `c^dag c` (charge 0) live in the even
subalgebra; bilinears `c c` (charge `-2`) and `c^dag c^dag` (charge
`+2`) span the odd subalgebra under fermion-parity.

### 2.3 What's not yet proved

`Cl(3)` algebra structure **does not** by itself forbid bilinears in
its odd subalgebra. The odd subalgebra is dimensionally non-empty
(half of `Cl(3)` by grading). So `Cl(3)` admits charge-`±2` bilinears
as algebra elements; they are not group-theoretically excluded.

### 2.4 First obstruction

`Cl(3)` algebra rigidity alone does not force the grammar rule.
Rigidity must come from somewhere else. **Naming the wall:** the
representation-theoretic admissibility of charge-`±2` operators is
*open* on `Cl(3)`; the algebra by itself is permissive.

## 3. Attempt 2 — Staggered-Dirac structure rigidity

### 3.1 The angle

The Kogut-Susskind staggered fermion on `Z^3` (or its 4D Euclidean
extension `Z^4 = Z^3 × Z`) carries a residual **`U(1)_V × U(1)_A`**
symmetry at zero bare mass:

- `U(1)_V`: total fermion number; `chi -> e^(i theta) chi`.
- `U(1)_A`: residual axial; `chi -> e^(i theta epsilon(x)) chi`
  where `epsilon(x) = (-1)^(x_1 + x_2 + x_3 + x_4)`.

A charge-`±2` operator that preserves both `U(1)_V` and `U(1)_A`
would be a chiral-condensate-type bilinear; but charge-`±2` bilinears
fail `U(1)_V` invariance by definition.

### 3.2 What's true

For the **massless staggered action** on `Z^d` (d ≥ 2),
`U(1)_V` is exact at the level of the action. The action has the
form `S = sum_{x,y} chi(x)^bar M(x,y) chi(y)`, and the bilinear
operator content is exclusively `chi^bar chi`-type — i.e.,
charge-zero in fermion number.

This is a **stronger statement** than the local grammar rule
because it derives from the action's bilinear structure, not from a
"grammar rule" stipulated separately.

### 3.3 What's not yet proved

The action's bilinear-only structure rests on the substrate choice
(Wilson or staggered fermion action on `Z^4`). A *different* substrate
choice — e.g., introducing a Pfaffian-type pairing term `chi^T S chi`
in the action — would break `U(1)_V` while remaining a "lattice fermion
action" in some broader sense. Whether such alternatives are
admissible under `A_min` is the open question.

`A_min` axiom 3 says: "the package works with the **finite local
Grassmann / staggered-Dirac partition**". This phrasing is restrictive
(it specifies staggered-Dirac, which is bilinear). Under a strict
reading, `A_min` itself excludes Pfaffian-type pairing terms.

### 3.4 Sharper finding

**Key observation:** if `A_min` axiom 3 is interpreted strictly
(staggered-Dirac partition exclusively, no Pfaffian extensions),
then `(R-X3)` follows as a corollary:

> **Corollary (Strict-A_min Dirac globality).** If `A_min` axiom 3
> is interpreted strictly as the staggered-Dirac partition without
> Pfaffian extensions, then the bilinear charge-zero structure of
> the staggered action forces `U(1)_V` globally on every extension
> consistent with `A_min`. Therefore `(C2-X)` holds, and the
> conditional Dirac global lift (Cycle 2) becomes unconditional.

But if `A_min` axiom 3 is interpreted permissively (allowing
"staggered-Dirac plus admissible additions" where additions could
include Pfaffian / pairing terms), the rigidity fails. The rigidity
of `(R-X3)` therefore reduces to:

> **The substrate-class admissibility question: does `A_min` axiom 3
> admit Pfaffian / pairing extensions of the staggered-Dirac
> partition?**

### 3.5 Second obstruction

Substrate-class admissibility is not currently retained. The
`MINIMAL_AXIOMS_2026-04-11.md` text does not explicitly forbid
Pfaffian extensions — it just specifies "staggered-Dirac partition"
and treats that as the canonical surface.

**Naming the wall:** `A_min` axiom 3 is *under-specified* on the
admissibility of Pfaffian / charge-`±2` substrate extensions. The
strict reading closes `(C2-X)`; the permissive reading does not.
The framework's own axiom-set has not made this choice explicit.

## 4. Attempt 3 — Anomaly-cancellation exhaustion

### 4.1 The angle

The retained SM gauge-anomaly cluster (`SM_ACCIDENTAL_BL_PROOF`,
`SM_GIM_NEUTRAL_CURRENT_PROOF`, `SM_MAJORANA_PMNS_COUNT_PROOF`,
`SM_QUARK_FLAVOR_COUNT_PROOF` series) constrains the admissible
matter content via anomaly cancellation. **If** a charge-`±2`
primitive cannot be added without breaking some retained anomaly
cancellation, then `(C2-X)` is closed via `(R-X1)`.

### 4.2 What's likely true

A right-handed neutrino with Majorana mass introduces lepton-number
violation `Delta L = 2`. In the SM, lepton number is an accidental
global symmetry (per `SM_ACCIDENTAL_BL_PROOF`); breaking it with a
Majorana mass for `nu_R` does not break gauge anomalies because
`nu_R` is gauge singlet.

So **SM gauge anomaly cancellation does not directly forbid a
Majorana mass for `nu_R`.** This is well-known textbook physics.

### 4.3 First obstruction (R-X1 angle)

`(R-X1)` cannot close `(C2-X)` via direct anomaly-cancellation
exhaustion: a gauge-singlet Majorana mass passes all SM gauge anomaly
checks. The retained anomaly-cancellation work focuses on gauge
content, not on `Delta L = 2` operators.

So `(R-X1)` is **not the closure route**. Cross out `(R-X1)`.

## 5. Synthesis: what this stretch attempt found

After three angles of attack:

1. **`Cl(3)` algebra rigidity** — does NOT close `(R-X3)` alone.
   Algebra is permissive on charge-`±2` bilinears.
2. **Staggered-Dirac structure rigidity** — closes `(R-X3)` *under
   strict reading of `A_min` axiom 3*. Open under permissive
   reading. **Identifies the substrate-class admissibility question
   as the load-bearing wall.**
3. **Anomaly-cancellation exhaustion (R-X1 angle)** — does NOT
   close. Gauge-singlet Majorana mass passes anomaly cancellation.

### 5.1 New result: `(C2-X)` reduces to substrate-class admissibility

The stretch attempt **converts** `(C2-X)` from a vague "no charge-2
primitive" exhaustion premise into a sharp axiom-interpretation
question:

> **`(C2-X)-strict`**: `A_min` axiom 3 is interpreted strictly as
> the staggered-Dirac partition without Pfaffian / pairing extensions.

If the framework adopts `(C2-X)-strict` as the canonical reading of
its own axiom 3, then by §3.4's corollary the conditional Dirac
global lift becomes **unconditional**.

This is a **sharper obstruction** than (C2-X) was at the start of the
cycle. It is also a **decision-level obstruction** (about how to
read an existing axiom) rather than a research-level obstruction
(requiring new framework content).

### 5.2 Recommended axiom-clarification path

The framework's `MINIMAL_AXIOMS_2026-04-11.md` should be amended /
clarified to explicitly state which reading of axiom 3 it adopts:

- **(strict reading):** "the package works with the finite local
  Grassmann / staggered-Dirac partition **exclusively**; Pfaffian /
  pairing / `Delta L != 0` substrate extensions are not admissible."
- **(permissive reading):** "the package works with the finite local
  Grassmann / staggered-Dirac partition **canonically**; admissible
  extensions may include Pfaffian / pairing terms consistent with
  retained gauge anomaly cancellations."

The strict reading closes `(C2-X)` and globalizes Dirac. The
permissive reading leaves `(C2-X)` open as a research question on
substrate extensions.

### 5.3 Falsified angles

- **(R-X1)** anomaly-cancellation exhaustion: falsified as a closure
  route. A gauge-singlet `nu_R` Majorana mass passes all retained
  anomaly cancellations. `(R-X1)` from the route portfolio is
  effectively a **dead route**.

### 5.4 Surviving angles

- **(R-X2)** representation-theory classification: still open.
  `Cl(3)` algebra alone is permissive (per §2.3); a *combined*
  argument using `Cl(3)` + `Z^3` substrate + staggered structure
  may yield rigidity, but the staggered-structure leg of that
  combination is the §3.4 corollary, which reduces to substrate-
  class admissibility (= `(C2-X)-strict`).
- **(R-X3-strict)** as the new sharper formulation.
- **(R-X4)** experimental sharpener: unchanged; outside Lane-4-
  internal closure path.

## 6. What this cycle closes and does not close

**Closes:**

- A worked failed derivation of unconditional `(C2-X)` retention
  via three independent attempts.
- Identification of the load-bearing wall: substrate-class
  admissibility of `A_min` axiom 3.
- A precise reformulation: `(C2-X)` ⇔ strict reading of
  `A_min` axiom 3 (which is a **decision-level**, not research-
  level, obstruction).
- Falsification of `(R-X1)` (anomaly-cancellation exhaustion)
  as a closure route.
- A recommended axiom-clarification path with two explicit
  readings (strict vs permissive) and their consequences.

**Does not close:**

- `(C2-X)` unconditionally — but the obstruction is now sharply
  decision-level, not research-level.
- The unconditional Dirac global lift — but it is now a one-line
  corollary of the strict reading of axiom 3.
- The substrate-class admissibility question itself.
- Any neutrino mass numerically.

## 7. Falsifiers

The stretch-attempt findings are falsified by:

- a worked extension of `A_min` axiom 3 with Pfaffian / pairing
  terms that *is* admissible under retained framework content
  (would refute the strict-reading closure);
- a `Cl(3)` representation-theoretic argument that forbids
  charge-`±2` bilinears as primary local operators (would close
  `(R-X3)` via algebra-only, sharper than this attempt);
- a positive 0νββ signal at experimental precision (Schechter-Valle
  → Majorana mass; falsifies the conditional theorem's empirical
  content directly, regardless of axiom interpretation).

## 8. How this advances Lane 4

After this stretch attempt, the closure path for the unconditional
Dirac global lift reduces to **a single decision-level question**:
how is `A_min` axiom 3 to be read?

This is a substantially **sharper** state than where Cycle 2 left
us. Cycle 2 said "needs an exhaustion theorem on charge-2 primitives"
(research-level). Cycle 3 says "needs an axiom-clarification on
admissible substrate extensions" (decision-level).

Recommended next-step paths:

- **Cycle 4 candidate A:** Stuck fan-out on the strict-vs-permissive
  reading. Generate 3-5 framework-internal arguments for each
  reading; synthesize.
- **Cycle 4 candidate B:** Search the existing retained framework
  content (anomaly cluster, gauge-cluster proofs, recent SM
  retentions) for evidence pointing to one reading or the other.
- **Cycle 4 candidate C:** Pivot to Lane-4 work that doesn't depend
  on `(C2-X)` resolution — e.g., 4F `Sigma m_nu` cosmological bridge
  via the hubble-h0 retained surface (Lane-bridge work).

## 9. Cross-references

- `docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`
  (primary source — local U(1) argument).
- `docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` (Cycle 2
  premise P1).
- `docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` (Cycle 2 premise
  P6).
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — A_min, the axiom-3
  ambiguity surfaced here.
- `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`
  (Cycle 2; this stretch attempt sharpens its (C2-X) obstruction).
- `docs/NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md` (Cycle 1;
  this stretch attempt is SA2 from §5).
- Loop pack at
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.

## 10. Boundary

This is a stretch-attempt artifact under the new physics-loop skill's
Deep Work Rules. It does **not** retain any input, does not
unconditionally close the Dirac global lift, and does not prove
substrate-class admissibility either way. It produces:

- a worked first-principles attempt across three angles;
- one falsified angle (`(R-X1)`);
- a sharper obstruction reformulation (decision-level vs research-
  level);
- a recommended axiom-clarification path.

This is honest first-principles progress with a named obstruction
— valid output per Deep Work Rules' no-churn exception. The output
is structural and carries no fitted parameters or hidden derivation
inputs.

A runner is not authored: the attempt is structural case-analysis
on `A_min` and the existing Majorana cluster. No new symbolic or
numerical content is introduced.
