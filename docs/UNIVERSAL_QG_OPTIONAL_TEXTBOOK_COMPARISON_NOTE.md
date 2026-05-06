# Universal QG Optional Textbook Comparison Note

**Date:** 2026-04-15 (originally); 2026-05-05 (meta retag for re-seed);
2026-05-06 (zero-authority runner closure)
**Type:** meta
**Status:** audit-checkable packaging hub for optional textbook-comparison
crosswalks against the universal-QG canonical textbook closure target.
**Not** a theorem, claim, or new authority surface.
**Authority role:** zero — this row exists only to anchor a citation hub
for downstream universal-QG notes that need a stable target for "optional
textbook comparison" callouts.
**Primary runner:** `scripts/universal_qg_optional_textbook_comparison_meta_check.py`
(metadata invariant check only; no physics derivation).

## 0. Scope retag (2026-05-05)

This rewrite adds an explicit `**Type:** meta` header and removes theorem-like
section names from the body. The note is a packaging row only: it gives
downstream universal-QG notes a stable place to cite optional textbook
comparison callouts, but it does not assert a theorem, introduce a physics
runner, or provide authority for any physics step. The 2026-05-06 runner added
above checks only the metadata boundary.

## 1. Auditable zero-authority invariant

The auditable item in this row is the following repository metadata
invariant, not a continuum theorem:

- `Z0`: the source row is typed as `meta`.
- `Z1`: the status line explicitly negates theorem, claim, and new authority
  roles.
- `Z2`: the authority role is `zero`.
- `Z3`: this note has no markdown links to other docs, so it registers no
  upstream theorem dependency edge for itself; cross-references below are
  code-span filenames for navigation only.
- `Z4`: every substantive textbook-comparison result is forced out to its
  own claim row with its own load-bearing step, runner, and audit.
- `Z5`: current inbound mentions of this filename are guarded as optional
  packaging callouts rather than load-bearing theorem authority.

The primary runner replays `Z0`-`Z5` directly against the repository text. A
passing run certifies only this zero-authority metadata guard. It does not
certify, import, or strengthen any universal-QG continuum, weak-measure,
geometric-action, or textbook-equivalence theorem.

## 2. What this note is for

The canonical textbook continuum target for the universal-QG family is
already handled on the project route by the theorem chain listed in §4 below.
This note is a packaging hub providing a stable citation target for downstream
universal-QG notes that need a named row to attach optional-comparison callouts
to:

- public convention comparison;
- manuscript appendix packaging;
- notation / normalization crosswalks against alternate textbook packages.

It carries **no** derivation, **no** new claim, **no** physics runner, and
**no** authority. Its only runner is the metadata invariant check named
above. It is infrastructure metadata for the universal-QG citation graph.

## 3. What this note is *not* for

This note **must not** be used to:

- reopen, weaken, or extend the closed universal-QG theorem stack;
- introduce a new "comparison" claim that the audit lane would have to
  ratify;
- act as a one-hop authority for any downstream theorem;
- substitute for the actual closed canonical textbook continuum closure
  parent.

If a universal-QG downstream note needs a *substantive* textbook-comparison
result, that must live in its own claim row with its own load-bearing
step, runner, and independent audit review — not here.

## 4. Cross-references (informational only)

The universal-QG canonical textbook closure parent and sibling theorems are
not load-bearing for this meta packaging note. They are listed here only so a
reader landing on this row by citation can navigate to the actual derivations:

- `UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`
- `UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md`
- `UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
- `UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md`
- `UNIVERSAL_QG_CONTINUUM_BRIDGE_REDUCTION_NOTE.md`

These are the actual claim rows. This note is *not* one of them.
