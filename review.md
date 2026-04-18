# Review: `codex/pf-science-review-2026-04-18`

## Verdict

Still reject for `main` at the current tip (`29fb7282`).

This round is a real scientific improvement over the earlier PF packet. The
branch now states the honest negative current-bank claim rather than
overclaiming a positive global sole-axiom PF selector. But it is still not
ready to land as science on `main`.

I am **not** treating lack of repo weaving as a blocker here. If the science
were clean, I would do the landing/package work myself. The remaining blockers
are scientific evidence-surface blockers.

## Current Replay

- `frontier_perron_frobenius_selection_axiom_boundary.py`
  → `PASS = 126, FAIL = 0, SUPPORT = 63`
- `frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`
  → `THEOREM PASS = 4, SUPPORT = 1, FAIL = 0`
- `frontier_perron_frobenius_wilson_current_bank_complete_closure_2026_04_18.py`
  → `THEOREM PASS = 3, SUPPORT = 1, FAIL = 1`
- `frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py`
  → `THEOREM PASS = 4, SUPPORT = 1, FAIL = 0`
- `frontier_pmns_graph_first_fixed_slice_scalar_production_discriminant_2026_04_18.py`
  → `THEOREM PASS = 4, SUPPORT = 1, FAIL = 0`
- `frontier_gauge_vacuum_plaquette_beta6_first_hankel_certificate_2026_04_18.py`
  → `THEOREM PASS = 4, SUPPORT = 1, FAIL = 0`

So this is no longer just the old “overclaimed positive PF” problem. The new
packet is closer. But the current negative-closure evidence layer still does
not clear review.

## Live Blockers

### 1. One of the branch's own headline Wilson validators currently fails

`scripts/frontier_perron_frobenius_wilson_current_bank_complete_closure_2026_04_18.py`
does **not** replay cleanly at the current tip. It fails on its support check
against
`docs/PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md`, because the
audit note no longer contains the exact wording the runner expects about Wilson
being the “only/main positive reopening lever.”

That means the branch's claimed “clean current-bank closure validator stack” is
still internally inconsistent on its own terms.

This is not the deepest scientific issue, but it is a real blocker: the branch
cannot be called clean while one of its top-level exact-closure validators is
red locally.

### 2. The new negative-closure layer is still certified mainly by note-audit and generic certificate-shape runners

The central current-bank closure runner
`scripts/frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`
still only:

- reads the Wilson / PMNS / plaquette closure notes,
- checks for expected phrases,
- and then declares that all three frontier certificates are negatively closed.

That is prose-consistency auditing, not a theorem-grade primary verifier for
the branch-wide statement
“the present exact bank has no live positive PF route remaining.”

The same issue persists one level down in the representative new frontier
certificate runners:

- `frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py`
  proves a generic Hermitian `3x3` trace/characteristic-polynomial identity on
  a hand-built toy matrix with `b = h.copy()`, then checks whether the notes
  say the Wilson route has been reduced to a local `1 + 1` certificate.
- `frontier_pmns_graph_first_fixed_slice_scalar_production_discriminant_2026_04_18.py`
  proves a generic `2x2` Gram-positivity / scalar-discriminant lemma for a toy
  holonomy map, then checks whether the note says the fixed-slice PMNS frontier
  has been scalarized.
- `frontier_gauge_vacuum_plaquette_beta6_first_hankel_certificate_2026_04_18.py`
  proves generic first-moment / Hankel facts for toy witness matrices, then
  checks whether the note says the plaquette frontier now fails at the first
  Hankel layer.

These are good **certificate-shape** sanity checks. They are not yet direct
object-level verifiers that the **current exact bank** itself forces those
three frontier reductions/nonrealizations.

So the scientific gap is now narrower and clearer than before, but it is still
real: the branch lacks a theorem-grade primary verification layer for the exact
negative current-bank closure it now claims.

## Practical Call

The science is closer than the previous PF review, but it is still not ready
to land.

The next honest step is:

1. fix the broken Wilson complete-closure validator so the branch is at least
   internally self-consistent again;
2. replace the current note-audit / generic-certificate runners with
   object-level current-bank verifiers for the three live frontier closures;
3. then resubmit the negative current-bank PF theorem packet.

If that happens, this could plausibly become landable as a **science-only exact
boundary result** on `main`. It is not there yet.
