# Stuck Fan-Out: Strict vs Permissive Reading of `A_min` Axiom 3

**Date:** 2026-04-28
**Status:** bounded stuck-fan-out / no-go inventory for Lane 4; synthesis and
route triage only, no claim promotion and no axiom amendment. Per
`docs/audit/AXIOM_MINIMALITY_POLICY.md`, `A_min` remains fixed through the
repo audit, so the strict/permissive axiom-3 fork is recorded as a boundary
inventory rather than a closure decision. Generates five framework-internal
arguments for each reading of `A_min` axiom 3 ("finite local Grassmann /
staggered-Dirac partition") and preserves the named `(C2-X)` attack frames.
**Lane:** 4 — Neutrino quantitative closure
**Loop:** `neutrino-quantitative-20260428`

---

## 0. Setup

Cycle 3
(`NEUTRINO_NORMAL_GRAMMAR_U1_RIGIDITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`)
reformulated the `(C2-X)` charge-2 primitive class exhaustion
obstruction from research-level to decision-level: the unconditional
Dirac global lift hinges on which reading of `A_min` axiom 3 the
framework adopts.

### 0.1 The two readings

- **`(C2-X)-strict`:** axiom 3 is read as "the package works with the
  finite local Grassmann / staggered-Dirac partition **exclusively**;
  Pfaffian / pairing / `Delta L != 0` substrate extensions are not
  admissible."
- **`(C2-X)-permissive`:** axiom 3 is read as "the package works with
  the finite local Grassmann / staggered-Dirac partition
  **canonically**; admissible extensions may include Pfaffian /
  pairing terms consistent with retained gauge anomaly cancellations."

### 0.2 Stuck fan-out method

Per the new physics-loop skill:

> **Stuck fan-out:** before declaring "no route passes the gate",
> generate 3-5 orthogonal premises/attack frames. ... Synthesize
> agreements, contradictions, and the best remaining attack.

Sequential emulation here (no parallel sub-agents). 5 strict-reading
arguments + 5 permissive-reading arguments + synthesis.

## 1. Five arguments for the strict reading

### S1 — Literal axiom text names a specific partition

`MINIMAL_AXIOMS_2026-04-11.md` axiom 3 reads:

> "Microscopic dynamics: the package works with the finite local
> Grassmann / staggered-Dirac partition and the lattice operators
> built on that surface."

The phrasing names a specific partition class. "Pfaffian / pairing
extensions" are a *different* partition class — they extend the
fermion bilinear structure to allow `chi^T S chi`-type insertions.
A literal reading of axiom 3 excludes these.

**Strength:** straightforward textual reading. **Weakness:** "works
with" is mild language; could read as "uses canonically" rather than
"is exclusively restricted to".

### S2 — `g_bare = 1` evaluation surface depends on bilinear partition

Axiom 4 specifies the canonical normalization `g_bare = 1` on the
plaquette / `u_0` surface. This surface is well-defined on the
staggered-Dirac (bilinear) partition. Extending to a Pfaffian-type
partition would require re-deriving `g_bare = 1` on the extended
surface. The two retained `g_bare = 1` derivation paths
(operator-algebra + 1PI amplitude routes per
`G_BARE_DERIVATION_NOTE.md`) are bilinear-specific.

**Strength:** axiom 4 is implicitly bilinear. **Weakness:** this is
conditional — extending the partition would break the existing
proofs but might admit different proofs.

### S3 — Retained SM gauge-anomaly cancellations rely on bilinear matter

The recent SM gauge-cluster proofs (`SM_ACCIDENTAL_BL_PROOF`,
`SM_GIM_NEUTRAL_CURRENT_PROOF`, `SM_MAJORANA_PMNS_COUNT_PROOF`,
`SM_QUARK_FLAVOR_COUNT_PROOF`) all assume a fixed matter content
structure that is bilinear. A pairing extension would change the
fermion content from "single-component Weyl spinors" to "Bogoliubov
quasiparticles" with mixed `c`/`c^dag` content, and would shift the
B-L cancellation accounting.

**Strength:** integration argument — the retained anomaly work
implicitly fixes the partition class. **Weakness:** Cycle 3 falsified
`(R-X1)`: gauge-singlet `nu_R` Majorana mass passes anomaly
cancellations. So this argument is partially undermined.

### S4 — Physical-lattice reading and Planck-scale lane assume bilinear

The conditional Planck-lane completion
(`PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md` and the
2026-04-25 packet) defines `c_cell = 1/4` and the physical-lattice
reading on the bilinear primitive boundary block `P_A H_cell`.
Extending the partition to Pfaffian would change the rank-4 primitive
block's structure (Bogoliubov mixing changes the boundary carrier).

**Strength:** another integration constraint. **Weakness:** the
Planck lane is itself conditional, so this is "two conditionals lean
on each other" — not load-bearing rigidity.

### S5 — Historical / contextual reading

Every retained framework theorem to date uses the bilinear surface.
No retained theorem cites or admits a Pfaffian extension. The
framework's published-package surface
(`docs/publication/ci3_z3/`) treats bilinear staggered-Dirac as the
operating surface throughout.

**Strength:** the framework's *de facto* practice is strict.
**Weakness:** "what we've done so far" doesn't determine "what's
admissible"; this is an inductive argument from past practice.

### S1-S5 summary

The strict-reading arguments are strongest when read as **integration
constraints**: changing axiom 3 to admit Pfaffian extensions would
require re-deriving `g_bare = 1`, re-checking SM anomaly cancellations,
and re-evaluating the Planck-lane carrier identification. None of
these *strictly forbids* the permissive reading, but they do impose a
substantial cost on it.

## 2. Five arguments for the permissive reading

### P1 — Source notes explicitly preserve openness

The retained Majorana cluster notes uniformly preserve the openness
of future Majorana mass via "future axiom-side primitive":

> [Current-stack zero law §6 "What this does not close"]
> "This note does NOT prove that no future extension can ever
> generate `mu != 0`."

> [Mass reduction to Dirac §10 "Cannot claim"]
> "The framework has already chosen Dirac neutrinos over Majorana
> neutrinos in nature."

> [Finite-normal-grammar no-go §5 "What this does not close"]
> "any future axiom-side object that genuinely leaves the retained
> normal grammar"

This language is **explicit authorial intent** that the framework
admits (in principle) extensions outside the retained normal grammar.
The strict reading would contradict this.

**Strength:** strongest single argument for permissive. The framework's
authors have, repeatedly and explicitly, declined to close the
question.

### P2 — Pfaffian extension notes exist as live framework artifacts

`NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md` and
`NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md` are framework
notes that *consider* Pfaffian extensions as objects of study. Their
existence as exact construction/no-forcing artifacts means the framework
treats Pfaffian extensions as **valid objects to analyze**, even though
the physical Pfaffian sector is not currently retained as realized.

**Strength:** the framework's own corpus treats Pfaffian extensions as
discussable framework objects, not as already-forbidden syntax.

### P3 — Phenomenological openness to Majorana neutrinos

Type-I seesaw (with Majorana right-handed neutrinos) is the most
common neutrino mass mechanism in the literature. A strict reading
of axiom 3 would force the framework to **commit a priori** to Dirac
neutrinos, which is a strong empirical claim before any 0νββ
experimental result. The framework's general posture (per the
Majorana cluster) is to keep both mass mechanisms admissible until
data decides.

**Strength:** consistent with how the framework treats other
empirically-decidable questions (e.g., the framework retains
`delta_CP ≈ -81°` from the DM closed package as a *prediction* with
falsifier, not as an axiom).

**Weakness:** this is a methodological argument, not structural
rigidity.

### P4 — "Works with" is canonical-not-exclusive language

Compare axiom 3's "the package works with..." vs hypothetical
alternative axioms phrased "...consists of...", "...is...",
"...is exclusively..." The chosen phrasing is mild canonical
language ("uses as the canonical surface"), not restrictive
language ("is exclusively this").

The other axioms phrase strict claims more directly: axiom 1 says
"the physical local algebra **is** `Cl(3)`"; axiom 2 says "the
physical spatial substrate **is** the cubic lattice `Z^3`". Both use
copula. Axiom 3 uses "works with". The asymmetry is suggestive.

**Strength:** linguistic / structural argument from the axiom set
itself. **Weakness:** could be stylistic variation rather than
intentional permissiveness.

### P5 — The MINIMAL_AXIOMS note's own scope statement

`MINIMAL_AXIOMS_2026-04-11.md` says (verbatim):

> "These are the framework inputs. Everything else in the current
> publication package is either retained, bounded, or still open
> relative to that stack."

The phrasing "still open relative to that stack" implies axiom-side
extensions are explicitly anticipated and characterized in three
classes (retained, bounded, still open). This is a permissive-reading
posture: the framework treats its axiom set as **stable but open to
admissible extensions**, not as **closed and exclusive**.

**Strength:** direct textual support from the axioms note itself.

### P1-P5 summary

The permissive-reading arguments are dominated by **explicit authorial
intent** (P1, P2, P5) and **methodological consistency** (P3). The
strict reading would require contradicting language the framework's
authors deliberately chose, throughout the Majorana cluster and the
axioms note itself.

## 3. Synthesis

### 3.1 The source-reading inventory

As a source-reading exercise, the permissive-reading arguments are the
stronger historical/posture evidence. The relevant source signals are:

- P1 quotes from three independent notes preserve the openness of
  future Majorana extensions.
- P2 establishes that Pfaffian extensions are framework-discussable
  objects.
- P5 directly states that axiom-side extensions are anticipated.
- P4 supports this via the axiom's own phrasing.

Conversely, the strict-reading arguments (S1-S5) are mostly integration
constraints. They show what would be required to globalize the current-stack
Dirac result, but they do not derive `(C2-X)` from fixed `A_min`.

### 3.2 Implication for `(C2-X)`

Under the audit-policy resolution:

- `(C2-X)` is **not** closed by an axiom-clarification.
- The Cycle-2 Dirac global lift remains a **bounded conditional theorem**.
- No amendment to `MINIMAL_AXIOMS_2026-04-11.md` is used to close the lane.
- The unconditional global lift requires either:
  - a first-principles derivation from fixed `A_min` that **all**
    admissible Pfaffian extensions consistent with retained anomaly
    cancellations + retained gauge structure must still preserve `U(1)_V`,
    or
  - empirical falsification of admissible Pfaffian extensions via
    null 0νββ at experimental precision (`(R-X4)`-type sharpener).

The decision-level reformulation Cycle 3 proposed is **rejected** as an
audit-lane closure move: the framework does not amend `A_min` in order to
close `(C2-X)`.

### 3.3 What this fan-out closes and opens

**Closes:**

- The decision-level reformulation. `(C2-X)` is a research-level
  obstruction under fixed `A_min`.
- The axiom-3 amendment route for this workstream. It is replaced by
  `AXIOM_MINIMALITY_POLICY.md`.

**Opens / re-opens:**

- The research-level question of `(C2-X)` closure under fixed `A_min`.
- The new active hard residual: a structural rigidity theorem on
  `U(1)_V` preservation under all admissible Pfaffian extensions
  consistent with retained framework structure.

## 4. No-go ledger for `(C2-X)` attack frames

### 4.1 The reformulated target

Define **admissible Pfaffian extensions** as: extensions of the
staggered-Dirac partition by `chi^T S chi`-type pairing terms `S` that
preserve all retained:

- gauge anomaly cancellations (SM gauge cluster proofs);
- emergent-Lorentz dimension-6 onset and continuum-limit
  free-scalar 2-point closure;
- canonical normalization `g_bare = 1`;
- Planck-scale conditional completion premises.

The new target: **show that every admissible Pfaffian extension
preserves `U(1)_V`** (i.e., `S` cannot generate a charge-`±2`
amplitude consistent with the retained constraints).

### 4.2 Why this is genuinely hard

The Pfaffian extension companion notes
(`NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md`,
`NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md`) already do
substantial work in this direction. The "Pfaffian no-forcing"
theorem is a specific statement that nothing in the *current*
retained data forces a nonzero Pfaffian amplitude. The harder
direction — that *no admissible extension* can introduce one — is
the load-bearing target.

### 4.3 Concrete sub-targets

Three concrete sub-attacks on `(C2-X)` remain ledgered as candidate attack
frames:

- **(SR-1) Lorentz-onset incompatibility:** show that any nonzero
  Pfaffian pairing `S` breaks the retained emergent-Lorentz
  dimension-6 onset (e.g., by introducing a Lorentz-non-invariant
  rest frame at the lattice level).
- **(SR-2) Continuum-limit scalar 2-point incompatibility:** show
  that the retained continuum-limit 1+1D / 3+1D boost-covariant
  free-scalar 2-point closure constrains the Pfaffian pairing to be
  trivial.
- **(SR-3) Stronger SM anomaly cluster:** sharpen the existing SM
  gauge-cluster proofs to a stronger statement that admissible
  matter content has only bilinear-canonical insertions. This would
  effectively force `(C2-X)`-strict via the gauge-anomaly side.

Of these, **(SR-2)** was the cleanest single-cycle attempt because the
continuum-limit closure is already retained as a theorem-grade result (per
the framework's emergent-Lorentz cluster), and sharpening it to "constrains
pairing extensions" is a self-contained structural step. It remains a
bounded attack frame unless such a derivation is supplied from fixed `A_min`.

## 5. Loop status after this fan-out

### 5.1 Deep Work Rules compliance

Per the new physics-loop skill, this stuck fan-out satisfies the
"stuck fan-out before any honest stop" requirement:

- ≥3 orthogonal attack frames generated (5+5 here).
- Synthesis recorded with named best remaining attack.
- Identifies a bounded no-go ledger of candidate attack frames
  (SR-1 / SR-2 / SR-3).

### 5.2 Honest stop vs continue

After this cycle, the loop has recorded:

- 1 audit-grade dependency audit (Cycle 1)
- 1 audit-grade conditional theorem (Cycle 2)
- 1 stretch attempt (Cycle 3) — exercised Deep Work Rules
- 1 stuck fan-out (Cycle 4) — this note

Both Deep Work Rules requirements (≥1 stretch + ≥1 fan-out) are met.
The loop may now stop honestly OR continue with one more substantive
cycle attacking SR-2 (continuum-limit scalar 2-point incompatibility).

Given:
- 4h runtime budget; ~3-3.5h consumed across cycles 1-4;
- ~30-90 min remains;
- SR-2 is a Tier-B-or-harder structural attempt (likely 90+ min);
- the next cycle's output would be either substantive or "no clean
  attack within budget";

**recommendation: stop honestly at Cycle 4.** Hand off SR-1 / SR-2 /
SR-3 as candidate attack frames for a future loop session. Open the
review PR per skill's PR policy.

## 6. Best remaining attack — handoff to future cycle/session

The cleanest single-cycle continuation, when picked up by a future
session, is:

**(SR-2) Continuum-limit scalar 2-point incompatibility with
Pfaffian extensions.**

Premise: retained continuum-limit `1+1D / 3+1D` boost-covariant
free-scalar 2-point closure on the bilinear staggered-Dirac surface.

Target: show that adding any nonzero Pfaffian pairing `S` to the
staggered partition breaks this closure (e.g., by introducing a
Bogoliubov mixing that is Lorentz-non-invariant in any frame).

If `(SR-2)` lands as a first-principles derivation from fixed `A_min`, the
bounded conditional Dirac theorem (Cycle 2) would discharge `(C2-X)`.

## 7. Cross-references

- `docs/MINIMAL_AXIOMS_2026-04-11.md` — primary text under
  interpretation.
- `docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` (P1
  evidence).
- `docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` (P1 evidence).
- `docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` (P1
  evidence).
- `docs/NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md` (P2 evidence).
- `docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md` (existing
  Pfaffian work).
- `docs/G_BARE_DERIVATION_NOTE.md` (S2 integration constraint).
- SM gauge-cluster proofs (S3, partially undermined per Cycle 3).
- `docs/PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md` (S4).
- `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`
  (Cycle 2; this fan-out reverts the (C2-X)-strict reformulation).
- `docs/NEUTRINO_NORMAL_GRAMMAR_U1_RIGIDITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
  (Cycle 3; this fan-out re-evaluates its conclusion).
- Loop pack at
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.

## 8. Boundary

This is a bounded stuck-fan-out artifact. It does not retain any input, does
not introduce a numerical claim, does not promote any cycle's content, and
does not amend `A_min`. It synthesizes 5+5 framework-internal arguments and
preserves the SR-1 / SR-2 / SR-3 attack-frame ledger for `(C2-X)`.

The fan-out **revises** Cycle 3's conclusion: the decision-level
reformulation `(C2-X)`-strict is **rejected** as inconsistent with the
fixed-`A_min` audit policy. `(C2-X)` remains a bounded obstruction with a
sharpened set of attack frames (SR-1, SR-2, SR-3).

This revision is itself substantive output — Cycle 3 may have
over-stated the closure path, and the fan-out catches that
over-claim before it propagates further.

A runner is not authored: the fan-out is editorial / structural; no
new symbolic or numerical content is introduced.
