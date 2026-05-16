# Constructive UV-Localized Bridge Class for `y_t`

**Date:** 2026-04-15 (demoted 2026-05-16)
**Status:** bounded numerical-match note (tuned fit to imported endpoint)
**Audit class:** G — load-bearing step is a numerical match, not a derivation
**Primary runner:** `scripts/frontier_yt_constructive_uv_bridge.py`

## Scope (honest framing)

This note is **not** a derivation that the interacting lattice bridge belongs
to a UV-localized class. It is a bounded *consistency check*: given an
imported physical endpoint `y_t(v) = 0.9176`, three endpoint-preserving
profile families (logistic, error-function, smoothstep) can each be tuned
within a narrow UV-localized window so that their best fit reproduces the
imported endpoint with cross-family spread `<= 0.0252%`.

The endpoint `y_t(v) = 0.9176` is imported, not derived. The runner's best
rows are explicitly chosen by minimizing deviation from that imported target.
Tunable parameters are the bridge center fraction and width; both are scanned
on a 9x9 grid inside a pre-selected UV-localized window.

This is therefore an `audited_numerical_match` result in the project's audit
taxonomy, not a closed first-principles derivation. The remaining structural
gap is recorded below in "What remains open".

## Previous-scan context (informational)

Earlier scans established:

- broad / diffuse bridges fail to reproduce the imported endpoint
- only a narrow UV-localized window admits any fit
- subleading EW-side deformations do not rescue diffuse bridges

These results are taken as background; this note does not re-derive them.

## Numerical result

The runner builds three independent endpoint-preserving bridge families:

1. logistic
2. error-function
3. smoothstep

Each family scans the UV-localized window and selects its best fit to the
imported endpoint `y_t(v)=0.9176`.

After best-fit selection per family:

- each best fit stays within `0.0252%` of the imported endpoint
- the best-fit center fractions lie in `[0.965, 0.975]`
- the best-fit widths lie in `[0.017, 0.020]`
- the normalized bridge area is stable across families (spread `9.65%`)

The honest interpretation of this is that, **conditional on** the imported
endpoint and **conditional on** restricting to the pre-selected UV-localized
window and these three profile families, the per-family best fit is not very
sensitive to the choice of profile family. It does not establish that the
imported endpoint is shape-independent in a non-tuned sense.

## Meaning (bounded)

The bounded claim this note licenses is narrow:

> *Conditional on* the imported endpoint `y_t(v)=0.9176` and *conditional on*
> restricting to a pre-selected UV-localized window with three chosen
> endpoint-preserving profile families, the per-family best fit reproduces the
> imported endpoint with cross-family spread `<= 0.0252%`.

It does not establish that the interacting lattice bridge actually belongs to
the UV-localized class, nor that the UV-localized class is uniquely selected
by any axiom in the framework. The result is a tuned-fit consistency check,
not a derivation.

## What remains open (load-bearing gaps)

To upgrade this row from `audited_numerical_match` to `audited_clean`, the
following structural gaps must be closed, none of which the present runner
addresses:

1. derive the endpoint `y_t(v) = 0.9176` from the framework axioms rather
   than importing it as a target;
2. derive why the interacting lattice bridge must lie in the chosen
   UV-localized window, rather than asserting this window from prior scans;
3. derive why the three profile families chosen here exhaust (or fairly
   sample) the admissible bridge class, rather than treating them as
   convenient analytic placeholders.

All three are operator/theorem problems and are out of scope for this note.
The note therefore stops at the bounded numerical-match claim and does not
attempt to upgrade beyond it.

## Audit history

The 2026-05-04 audit recorded this row as `audited_numerical_match` with
Class-G load-bearing step. The 2026-05-16 demotion edit (this revision)
rewrites the "Scope", "Result", and "Meaning" sections of this note so the
headline framing matches the auditor verdict instead of relying on a
trailing addendum. No runner, audit-data, or publication file is changed by
the demotion; the bounded numerical-match status is preserved.

## Audit dependency repair links

This graph-bookkeeping section records load-bearing upstream notes as
Markdown links so the audit citation graph can track them. Backticked
filenames in this section are preserved see-also context only and do
not emit citation-graph edges. This section does not promote this note
or change the audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
- [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md)
- `YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md` (see-also cross-reference,
  not a load-bearing dependency — backticked to break cycle-0005 in the
  citation graph. The rearrangement note explains the UV-localization
  structurally and is downstream of this constructive-class note; this
  note's three-family endpoint-stability runner does not consume the
  rearrangement-kernel result, so the dependency arrow runs from
  rearrangement back to this note, not vice versa.)
- `YT_BOUNDARY_THEOREM.md` (see-also cross-reference, not a load-bearing
  dependency — backticked to break the residual yt cluster cycle in the
  citation graph. The boundary theorem establishes that `v` is the
  physical crossover endpoint; this constructive bridge note's
  three-family runner targets that endpoint empirically but does not
  consume the boundary theorem's domain-separation proof as a logical
  premise of the three-family endpoint-stability result.)
