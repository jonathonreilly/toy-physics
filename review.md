# Review: `codex/pf-science-review-2026-04-18`

## Verdict

Still reject for `main` at the current tip (`6d2cf065`).

The latest update improves some note-consistency language, but it does not
change the load-bearing blockers from the previous review:

1. the umbrella PF closure runner is still a note-audit script rather than an
   object-level theorem verifier,
2. the representative frontier-certificate runners still prove toy generic
   lemmas and then promote note conclusions, and
3. the branch still creates a large root-level authority stack without any
   package-surface wiring.

## Current Replay

The branch still replays cleanly:

- `frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`
  → `THEOREM PASS=4 SUPPORT=1 FAIL=0`
- `frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py`
  → `THEOREM PASS=4 SUPPORT=1 FAIL=0`

So this remains an evidence-surface rejection, not a runtime one.

## Live Blockers

### 1. The top closure runner is still only checking note phrases

`scripts/frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`
still just reads the Wilson / PMNS / plaquette notes and passes if they contain
the expected closure sentences. It does **not** verify the branch-wide closure
claim directly on the underlying branch objects.

That is enough for a prose-consistency audit. It is not enough for claims like:

- “all three frontier certificates are negatively closed”
- “no remaining positive PF route is left open”
- “current-bank global PF is fully closed negatively”

Those remain theorem-grade statements without a theorem-grade primary runner.

### 2. The Wilson representative certificate is still toy-lemma plus note audit

`scripts/frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py`
still proves only the generic Hermitian `3x3` equivalence using a hand-built
matrix `h` with `b = h.copy()`, then checks whether the notes say the Wilson
route has been compressed to a local `1 + 1` certificate.

That is still not a certification of the actual Wilson objects or the concrete
branch route. The same general issue remains at the PMNS and plaquette frontier
certificate layer.

### 3. The branch still bypasses the repo truth surfaces

This tip still does **not** update any of the package control-plane files:

- `PUBLICATION_MATRIX.md`
- `DERIVATION_ATLAS.md`
- `DERIVATION_VALIDATION_MAP.md`
- `CLAIMS_TABLE.md`
- `RESULTS_INDEX.md`
- `EXTERNAL_REVIEWER_GUIDE.md`
- package / root `README` surfaces

So even if some subset of the science were acceptable, the branch is still not
packaged for `main`. It remains a competing root-level authority stack rather
than a package-captured landing.

## Practical Call

The latest edits are not enough to make this branch merge-ready.

The honest next step is still:

1. keep this as a salvage / review branch,
2. promote lower-level notes only where the runner certifies actual branch
   objects rather than note text,
3. replace the umbrella closure layer with real object-level verifiers, and
4. only then wire any accepted subset through the repo publication surfaces.
