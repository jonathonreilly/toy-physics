# Propagator Family Unification Note

**Date:** 2026-04-05  
**Status:** narrow review-safe unification note for the proposed_retained wavefield,
complex-action, and electrostatics scalar-sign-law lanes

**Status authority and audit hygiene (2026-05-10):**
This is a cross-note synthesis with `claim_type = meta`. The audit lane has
classified the note `audited_conditional`. Two reasons stand:
(a) at least one cited authority
(`claude_complex_action_grown_companion_note`) is itself
`audited_conditional`, and another (`source_resolved_wavefield_mechanism_note`)
is currently `unaudited`, so retained-grade support does not
propagate through the synthesis; and
(b) the note does not provide a bridge theorem proving the transport
architectures are literally the same across lanes rather than only
analogously described. This note therefore makes no load-bearing
contribution and is not itself eligible for promotion until those
upstream dependencies are first promoted to retained-grade and a
narrow bridge theorem identifying the shared transport scaffold is
added. The "Safe conclusion" below should be read as a status report
on a propagator-family naming convention, not as a derivation. Audit
verdict and effective status are set by the independent audit lane
only; nothing in this rigorization edit promotes status.

## Artifact chain

This note is a synthesis of `main` notes (mixed retained / audited_conditional / unaudited):

- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md) — currently `unaudited`
- [`docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md) — currently `retained_bounded`
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md) — currently `audited_conditional`
- [`docs/ELECTROSTATICS_CARD_NOTE.md`](ELECTROSTATICS_CARD_NOTE.md) — currently `retained`
- [`docs/ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md`](ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md) — currently `retained`

Of the five cited authorities, two block retained-grade propagation
through the synthesis: one is `audited_conditional` and one is
`unaudited`. Statuses listed above are a snapshot at the time of this
edit and may move as the audit lane progresses — the author of any
future re-audit should confirm against `audit_ledger.json` rather than
this static list. The links above are also corrected to relative repo
paths (the original absolute `/Users/jonreilly/...` paths were a stale
local layout from the original draft and pointed outside this checkout).

## One-line read

The common retained structure is a fixed propagator on a causal graph, with a
scalar coupling that changes how edges contribute without changing the basic
path-sum form.

That is the narrow unification claim here.

## Common propagator skeleton

Across the retained lanes, the shared shape is:

- a graph or ordered-lattice family
- a path-sum or stepwise transport rule
- a baseline propagation kernel that remains the same family-to-family
- a scalar coupling that modifies the edge contribution in a controlled way
- a zero-coupling or null-control reduction that must recover the baseline

In symbolic form, the retained lanes all look like a variant of:

```text
amplitude(edge) = baseline_propagator(edge) × scalar_coupling(edge)
```

The exact details differ by lane, but the review-safe common point is that the
coupling is scalar and multiplicative at the edge level, not a change to the
overall transport architecture.

## What each retained lane contributes

### Wavefield lane

The wavefield mechanism keeps the baseline propagator fixed and promotes a
phase-sensitive detector-line observable.

Retained behavior:

- exact zero-source reduction survives
- the detector-line phase ramp is coherent
- the ramp coefficient depends on source depth and source strength
- weak-field `F~M` stays near unity on the exact family

Interpretation:

- the scalar coupling here acts as a phase-sensitive transport control
- the important observable is not raw attenuation, but a stable phase ramp

### Complex-action lane

The complex-action carryover keeps the same ordered transport family and adds
a scalar action deformation:

```text
S = L(1 - f) + iγLf
```

Retained behavior:

- exact `gamma = 0` reduction survives
- Born stays machine-clean on the frozen exact field and the grown-row companion
- increasing `gamma` drives a `TOWARD -> AWAY` crossover
- detector escape falls sharply as the scalar coupling grows

Interpretation:

- the scalar coupling acts like a phase / absorption deformation of the same
  fixed propagator
- the narrow retained claim is structural crossover, not geometry-independence

### Electrostatics scalar-sign lane

The electrostatics card keeps the same ordered-lattice transport family but
changes the source polarity.

Retained behavior:

- sign antisymmetry is clean
- opposite-sign superposition cancels to printed precision
- dipole orientation flips the sign of the response
- the charge response is linear on the tested range
- screening strongly attenuates the response

Interpretation:

- the scalar coupling acts like a sign selector on the same transport skeleton
- the retained claim is electrostatics-like sign structure, not full Maxwell
  theory

## What is actually unified

The narrow unification is:

- same underlying path-sum / transport scaffold
- same requirement for a null or zero-coupling reduction
- same use of a scalar coupling to alter edge-level transport
- same review discipline: the promoted observable must survive the baseline
  check

That is enough to say the project has a **propagator family**, not merely a set
of unrelated cards.

## What is not unified yet

This note does **not** claim:

- geometry-generic transfer from exact lattices to all generated families
- a derivation of the scalar couplings from one principle
- full electromagnetism
- continuum closure
- self-gravity as a retained mechanism
- QNM / BMV / horizon thermodynamics as retained claims
- a single flagship theorem that forces belief on its own

The missing step is still a stronger bridge between families, not a new
taxonomy of existing results.

## Safe conclusion

The narrow review-safe statement is:

- the cited wavefield, complex-action, and electrostatics results share an
  analogous path-sum / transport scaffold at the descriptive level
- the difference between them is captured by a scalar coupling attached at
  the edge level, not by changes to the overall transport architecture
- using these notes as a coordinated "propagator family" is an organizing
  convention; treating the synthesis as a load-bearing bridge theorem is
  not yet supported by the cited material

That is the strongest unification description currently supported on
`main`. It is a naming/organizing claim, not a derivation.

## Audit-aware repair path

The audit lane's stated cheapest repair (see `audit_ledger.json`,
`notes_for_re_audit_if_any` for `propagator_family_unification_note`):

1. close or replace the non-retained dependencies — currently
   `source_resolved_wavefield_mechanism_note` (`unaudited`) and
   `claude_complex_action_grown_companion_note`
   (`audited_conditional`) — with retained-grade authorities; only
   then does retained-grade support propagate into this synthesis;
2. then add a narrow bridge theorem identifying the shared transport
   scaffold across lanes — explicitly establishing that the path-sum
   transport rule is the same operator family in each lane, not merely
   the same descriptive pattern;
3. only after both steps is the synthesis itself eligible for re-audit at
   anything stronger than `audited_conditional`.

Until those steps land, this note must be cited only as a non-load-bearing
organizing description, never as a bridge theorem and never as a chain
closure for any descendant claim.

