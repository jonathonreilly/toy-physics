# SCIENCE_FIX_DECLINED — axiom_first_lattice_noether_theorem_note_2026-04-29

**Date:** 2026-05-16
**Worktree branch:** `claude/science-fix/axiom-first-lattice-noether-theorem-note-2026-04-2-2026-05-16-b2`
**Claim:** `axiom_first_lattice_noether_theorem_note_2026-04-29`
**Category:** `audited_conditional_missing_bridge_theorem` (Class A, descendants: 703)

## Auditor's repair target

> `missing_bridge_theorem`: package and audit the staggered-Dirac realization
> derivation target, then re-audit whether this bounded theorem can be retagged
> clean on closed inputs.

## Why a single-row fix is not available

The auditor's `verdict_rationale` is explicit:

> The internal Noether manipulation and runner exhibits are algebraic checks on
> the admitted staggered carrier, so class A is appropriate. However the
> restricted packet explicitly says the staggered-Dirac/Grassmann carrier is an
> open gate and is imported as an admitted context input rather than derived
> from the provided axioms. Under the rubric, an explicit unclosed carrier
> import requires `audited_conditional` even if the bounded identity closes on
> that carrier.

The bounded identity (N1)+(N2)+(N3) is already closed on the admitted carrier:
runner `axiom_first_lattice_noether_check.py` shows 6/6 PASS across exhibits
E1–E6. The audit verdict is therefore not a defect of the algebra — it is the
rubric's correct flag that the **carrier itself** is admitted, not derived.

Three repair routes were considered:

1. **Package and audit the staggered-Dirac derivation.** The canonical parent
   note `docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` is itself
   `audited_clean` only at `open_gate` tier and explicitly states it does
   "NOT close the gate." It enumerates four substeps that must be discharged:
   (1) Grassmann fermion realization on A1+A2, (2) staggered-Dirac kinetic
   structure forced from A1+A2, (3) BZ-corner doubler structure, (4)
   physical-species reading. Six in-flight supporting notes
   (`STAGGERED_DIRAC_*_THEOREM_NOTE_2026-05-07/10.md`) carry the in-flight
   derivation work and are all currently `unaudited` in this ledger snapshot.
   This is a multi-substep research-grade campaign across ~6 notes and a
   coordinated re-audit; far beyond a single-row 30-min repair budget. The
   work is being addressed in a separate PR series, not in this slot.

2. **Add a retained sister-theorem dep edge.** A ledger sweep of
   `audited_clean` + `effective_status == retained` rows with "staggered" /
   "dirac" / "grassmann" / "kogut" in title, scope, or key returns eight
   candidates; none derives the staggered-Dirac/Grassmann **carrier** itself.
   They either sit on the carrier (e.g. `bmv_threebody_note_2026-04-11`,
   `staggered_graph_gauge_closure_note`) or address an adjacent piece
   (`dm_neutrino_dirac_bridge_theorem_note_2026-04-15`,
   `three_generation_observable_m3c_burnside_narrow_theorem_note_2026-05-10`).
   No edge would discharge the open carrier import.

3. **Narrow the claim further.** The note has already been narrowed three
   times: 2026-05-03 sublattice repair (cut to `(2Z)^3` sublattice momentum),
   2026-05-10 gate-recategorization repair (admit `staggered_dirac_realization_gate`
   and admit a separate g_bare gate), 2026-05-10 g_bare-removal repair (drop
   non-load-bearing `g_bare` admission). It is now at its minimal honest scope:
   "bounded lattice Noether identity on the admitted staggered/Grassmann
   carrier." Further narrowing would either drop a sub-claim that genuinely
   closes algebraically on the carrier (a regression, not a repair) or
   misrepresent the imported carrier as derived.

The note correctly identifies and explicitly admits its load-bearing import.
That is what the audit rubric flags as `audited_conditional`. The fix is
upstream (close the gate), not at this row.

## What is and is not in this PR

This PR contains only this `SCIENCE_FIX_DECLINED.md` file at the worktree root.
No `docs/`, `scripts/`, or `docs/audit/**` files are touched. No audit verdict
is claimed and no audit-data file is modified. The author-declared scope and
the auditor's conditional verdict on this row are unchanged.

## Recommended next action (out of scope for this single-row attempt)

Pursue the multi-substep staggered-Dirac realization gate closure via the
existing in-flight supporting-note chain
(`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` plus six supporting
notes listed in its "In-flight supporting work" section). When that gate's
parent note becomes retained-grade and the underlying substep notes are
audited clean, re-audit this row per the auditor's explicit re-audit guidance.
