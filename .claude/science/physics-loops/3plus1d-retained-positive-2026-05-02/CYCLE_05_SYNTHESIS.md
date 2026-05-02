# Cycle 05 — Synthesis: per-admission outcomes and rewrite plan

**Date:** 2026-05-02
**Goal:** Synthesize Cycles 1-4. Decide the honest claim_type for the row.
Plan the theorem note rewrite.

## Per-admission summary

| # | Admission | Outcome | Status |
|---|---|---|---|
| 1 | ABJ inconsistency | Still requires literature import | Open |
| 2 | Singlet completion is unique | Re-classified as Cl(3)/Z^3 + retained gauge structure (bounded) | Closed-bounded |
| 3 | Clifford-volume chirality | Re-classified as sublattice parity ε(x) on Z^3 | Closed (retained-clean) |
| 4 | Ultrahyperbolic Cauchy obstruction | Dispensable; subsumed by single-clock unitarity | Closed |

**Net result:**
- 3 of 4 admissions close on retained-clean / Cl(3)/Z^3 structural inputs.
- 1 admission remains a literature import: the standard QFT statement
  "ABJ axial anomaly with nonzero traces ⇒ chiral gauge theory is
  inconsistent in 3+1d."
- The bounded scope is now sharply narrowed: only one well-named
  literature import remains, and a path to its derivation is sketched
  (lattice Wess-Zumino consistency, requiring upstream re-audit of
  reflection positivity / microcausality).

## Claim_type decision

The honest claim_type for the rewritten theorem is:
**`bounded_theorem`**, with the bounded scope narrowed from "four
admissions" to "one admission" (the standard ABJ inconsistency
implication for chiral gauge theories in 3+1d).

This is a substantial narrowing of the bounded scope and a
strengthening of the framework-internal coherence.

## Why not `positive_theorem`?

Promoting to `positive_theorem` would require admission #1 to also
close on retained-clean inputs. This requires:

(i) lattice Wess-Zumino / Fujikawa derivation on Z^3 — does not exist
    in the repo;
(ii) retained-clean reflection positivity / microcausality / spectrum
     condition — these primitives exist as `unaudited` in the repo,
     not retained-clean.

These are tractable upstream re-audits but not in scope for one
physics-loop cycle.

## Rewrite plan

Modify `docs/ANOMALY_FORCES_TIME_THEOREM.md`:

(R1) **Step 1 (anomaly traces):** keep the algebraic catalog. **Add an
honest framing** that "ABJ inconsistency for chiral gauge theories in
3+1d" is the single remaining literature import, and that the framework's
own anomaly arithmetic is exact and retained-clean.

(R2) **Step 2 (RH completion):** **rewrite** to use the Cl(3)/Z^3 +
native gauge closure argument from Cycle 4. State that within the
retained-clean framework (Cl(3)/Z^3 + native gauge closure +
sublattice-parity chirality grading), the only allowed cancellation
route is SU(2)-singlet RH completion. Cite the supporting retained
notes explicitly.

(R3) **Step 3 (chirality grading):** **rewrite** to use the sublattice
parity argument from Cycle 1. State that the framework's chirality
grading is ε(x) on Z^3, retained-clean via CPT note + Cl(3) per-site
uniqueness. Drop the Cl(p,q) volume-element appeal (Lawson-Michelsohn
[3]) and the "d_total even" implication.

(R4) **Step 4 (d_t = 1):** **rewrite** to use the single-clock argument
from Cycle 2. State that assumption 1 (single strongly continuous
unitary one-parameter group) directly forces d_t = 1, with no need for
the ultrahyperbolic Cauchy obstruction. Drop references [4]
(Craig-Weinstein) and [5] (Tegmark) from load-bearing position; keep
them only as historical/comparative remarks.

(R5) **Step 5 (conclusion):** update to reflect the cleaner chain.

(R6) **Status / claim_type:** change to `bounded_theorem` with narrowed
scope. The single remaining bounded admission is "ABJ inconsistency for
chiral gauge theories in 3+1d", and a roadmap to its retained-positive
closure is documented.

## Updated chain

```text
Cl(3) on Z^3
  ⇒ SU(2) × SU(3) × U(1) gauge sector with LH (2,3)_{+1/3} + (2,1)_{-1}
     [`native_gauge_closure_note` retained-bounded, retained-clean]
  ⇒ Anomaly trace catalog (Tr[Y]=0, Tr[Y^3]=-16/9, Tr[SU(3)^2 Y]=1/3, ...)
     [`lh_anomaly_trace_catalog_theorem_note_2026-04-25`, internally
      verified arithmetic]
  ⇒ Bounded literature import: ABJ inconsistency for chiral gauge
     theories in 3+1d ⇒ anomaly cancellation is mandatory
     [residual literature import, single]
  ⇒ Anomaly cancellation requires opposite-chirality SU(2)-singlet
     completion [Cycle 4 — Cl(3)/Z^3 + retained gauge structure]
     {only allowed route given the retained gauge closure +
      sublattice parity chirality grading}
  ⇒ Existence of γ_5 = sublattice parity ε(x) on Z^3 [Cycle 1 — CPT note +
     Cl(3) per-site uniqueness; structural fact about Z^3]
  ⇒ Single-clock unitary one-parameter group U(t)=exp(-itH)
     [assumption 1] forces d_t = 1 [Cycle 2 — direct]
  ⇒ Spacetime is 3 + 1 dimensional. QED.
```

The chain now has **one** literature import (ABJ inconsistency), down
from four. The sole bounded scope is much more precise.

## What this would look like as a `claim_scope`

> Conditional derivation that Cl(3) gauge content plus single-clock
> unitarity forces 3+1 spacetime, modulo the standard ABJ inconsistency
> implication for chiral gauge theories in 3+1d.

## Effective_status implications

After rewrite:
- claim_type = `bounded_theorem`
- audit_status: re-audit needed to ratify the new structure
- effective_status: `audited_conditional` until re-audit, then likely
  `retained_bounded` if the upstream retained-clean primitives hold.

The 299 transitive descendants are partially shielded: anything that
relies only on "3+1d is forced from Cl(3)/Z^3" continues to inherit
the bounded result. The rewrite does not narrow what the row implies
*downstream*, only how cleanly it is supported *upstream*.

## Roadmap to full retained-positive

For the row to fully close as `retained_positive`, the lattice
Wess-Zumino / Fujikawa story for ABJ inconsistency on Z^3 must close.
This requires:

(a) a retained-clean reflection positivity theorem on Z^3;
(b) a retained-clean microcausality / Lieb-Robinson theorem on Z^3;
(c) a retained-clean lattice Fujikawa or Wess-Zumino consistency
    theorem on Z^3;
(d) a retained-clean gauge invariance / Ward identity theorem on
    the framework's surface.

(a)-(c) exist as `unaudited` in the repo. They are tractable upstream
re-audits but require independent audit cycles.
