# PMNS Selector Three-Identity Support Note

**Date:** 2026-04-21
**Status:** Support proposal on the affine Hermitian PMNS chart. Not a proposed_retained
closure theorem.

## Statement

Consider the retained affine Hermitian chart

```text
H(m, delta, q_+) = H_base + m T_M + delta T_Delta + q_+ T_Q
```

with the existing chart constants

```text
gamma = 1/2
E1 = sqrt(8/3)
E2 = sqrt(8)/3
Q_Koide = 2/3
SELECTOR = sqrt(6)/3
```

The support proposal is the three-equation system

```text
Tr(H)       = Q_Koide
delta * q_+ = Q_Koide
det(H)      = E2
```

On the current active-chamber working surface, that system has a numerically
recovered interior solution

```text
(m_*, delta_*, q_+*) = (2/3, 0.9330511..., 0.7145018...)
```

and the PMNS observables extracted from `H(m_*, delta_*, q_+*)` lie in the
runner's current NuFit 5.3 normal-ordering `1 sigma` bands.

## Retained inputs vs proposed inputs

### Retained/chart-side inputs used directly

- the affine Hermitian chart `H_base, T_M, T_Delta, T_Q`;
- the chart constants `gamma, E1, E2`;
- the scalar identity `SELECTOR^2 = Q_Koide = 2/3`;
- the trace identity `Tr(H) = m`.

### Proposed inputs, not yet promoted

- `delta * q_+ = Q_Koide`;
- `det(H) = E2`.

These two equations are the live candidate selector laws. The support package
keeps them explicit as proposals rather than hiding them under retained
language.

## Executable content

The runner verifies four kinds of facts:

1. exact scalar/chart identities already present on the retained chart:

```text
SELECTOR^2 = Q_Koide
2 * SELECTOR / sqrt(3) = E2
Tr(H) = m
```

2. numerical solution of the proposed three-equation system;
3. chamber/signature/PMNS checks at the recovered point;
4. heuristic multi-start evidence that the audited search box returns one
   chamber cluster.

## Recovered point and observables

At the recovered point, the runner reports

```text
m     = 0.666666666666667
delta = 0.933051059...
q_+   = 0.714501805...
```

with

```text
sin^2(theta_12) = 0.306178
sin^2(theta_13) = 0.022139
sin^2(theta_23) = 0.543623
sin(delta_CP)   = -0.990477
|Jarlskog|      = 0.033084
```

## Why this is support, not closure

Three scientific gaps remain explicit:

1. The second and third equations are proposed selector laws, not retained
   derivations.
2. The uniqueness statement is based on a bounded multi-start search, not an
   analytic uniqueness theorem.
3. The broader PMNS/DM flagship lane remains open on the current package
   surface; this proposal gives one compact candidate law on the current chart
   but does not settle the remaining selector-side or sheet-choice obligations.

## What would promote this package

Promotion would require at least:

1. a retained derivation of `delta * q_+ = Q_Koide`;
2. a retained derivation of `det(H) = E2`;
3. a theorem-grade basin uniqueness argument;
4. integration with the remaining open PMNS/DM gate without overstating what is
   already closed elsewhere on the current package surface.

## Review-safe takeaway

The honest value of this package is narrow and useful:

```text
compact candidate law
+ strong numerical fit
+ clear open obligations
= worth retaining as support
```

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_selector_three_identity_support_2026_04_21.py
```

Last run (2026-05-10): `PASS=19 FAIL=0` on the present worktree. The
runner exercises four parts: (Part A) exact scalar/chart identities
already present on the cited chart (`SELECTOR^2 = Q_Koide`,
`2 * SELECTOR / sqrt(3) = E2`, `Tr(H) = m`); (Part B) numerical
solution of the proposed three-equation system using the affine
Hermitian chart; (Part C) chamber/signature/PMNS checks at the
recovered point against NuFit 5.3 normal-ordering 1 sigma bands;
(Part D) heuristic multi-start evidence that the audited search box
returns one chamber cluster. The runner does not derive the proposed
selector laws `delta * q_+ = Q_Koide` and `det(H) = E2`; those remain
imported as proposals.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing selector premise relies on, in response to
the 2026-05-05 audit verdict's `missing_bridge_theorem` repair target
(audit row: `pmns_selector_three_identity_support_note_2026-04-21`).
It does not promote this note or change the audited claim scope, which
remains the support proposal that the three-equation system has the
reported recovered point and PMNS-band fit conditional on the two
proposed selector laws.

One-hop authority candidates cited:

- [`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_PROPOSAL_README_2026-04-21.md`](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_PROPOSAL_README_2026-04-21.md)
  — currently `unaudited` (audit row:
  `pmns_selector_three_identity_support_proposal_readme_2026-04-21`).
  Sibling proposal-package README that frames the same three-equation
  system, names the open scientific obligations, and points to the
  same runner artifact. Because this sibling is `unaudited`, it
  cannot lift the present note's effective status; it is cited as
  graph-bookkeeping for the proposal scope.
- [`PMNS_THREE_IDENTITY_Q_KOIDE_FROM_V8_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md`](PMNS_THREE_IDENTITY_Q_KOIDE_FROM_V8_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md)
  — currently `unaudited` (audit row:
  `pmns_three_identity_q_koide_from_v8_support_lift_theorem_note_2026-04-29`).
  Downstream support lift composing the V8 chart-constant surface
  (`Q_Koide = 2/3` on `A_min`) with the present three-identity package
  to upgrade the chart
  constant `Q_Koide = 2/3` from imported numeric to V8-derived
  structural value. It does not close the two proposed selector laws
  or basin uniqueness, but it removes one chart-constant import.
  Because this lift is itself `unaudited` and conditional on V8
  chart-constant ratification, it does not promote the present note's
  effective status under the cite-chain rule.
- [`KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md`](KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md)
  — currently `unaudited` (audit row:
  `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20`).
  Adjacent transport-side scalar-root note that imports `M_STAR` as
  one of the pins documented (in the
  `rigorize: pin provenance for koide_higgs_dressed_resolvent_root_theorem_note`
  triage commit `06b30907a`) as candidate-derivable from the present
  PMNS three-identity support note's recovered point. Cited here as
  the load-bearing downstream pin chain whose retention currently
  depends on the present note's promotion.

Open class D registration targets named by the 2026-05-05 audit
verdict as `missing_bridge_theorem`:

- The proposed selector law `delta * q_+ = Q_Koide` is imported as a
  candidate law, not derived inside the present note's restricted
  packet. Closing it would require a retained-grade derivation of
  `delta * q_+ = Q_Koide` from framework structure (the
  affine Hermitian chart plus cited source/transfer or
  observable-principle inputs), as named in the 2026-05-05 audit
  verdict's `notes_for_re_audit_if_any` field:
  `missing_bridge_theorem: provide retained-grade derivations of delta * q_+
  = Q_Koide and det(H) = E2`.
- The proposed selector law `det(H) = E2` is imported as a candidate
  law, not derived inside the present note. Closing it would require
  a retained-grade derivation of `det(H) = E2` from the cited chart
  primitives.
- The bounded multi-start uniqueness evidence is class C numerical,
  not theorem-grade. Promotion requires a basin-uniqueness theorem on
  the relevant active chamber (per Section "What would promote this
  package" item 3).

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
`chain_closes=False`, observing that the
package's exact chart identities (`SELECTOR^2 = Q_Koide`,
`2 * SELECTOR / sqrt(3) = E2`, `Tr(H) = m`) close on the retained
chart but the two equations `delta * q_+ = Q_Koide` and `det(H) = E2`
are explicitly proposed selector laws rather than retained
derivations, and the audit packet did not include the runner.
The runner `scripts/frontier_pmns_selector_three_identity_support_2026_04_21.py`
exists in the repository and verifies the conditional readout
(`PASS=19 FAIL=0` on 2026-05-10), but its checks are class A finite-
dimensional algebra plus class C numerical chamber-clustering
evidence, not first-principles derivations of the proposed selector
laws. The cite chain above wires the adjacent proposal README and
V8-derived chart-constant lift, and explicitly registers the three
missing-bridge-theorem and basin-uniqueness targets named by the
verdict's `notes_for_re_audit_if_any` field. Because this source note
is being edited, the audit lane must re-ratify it from the regenerated
ledger; this addendum does not apply an `audit_status` or promote
effective status.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the audit verdict expected, the runner
that exercises the conditional support, and the missing-bridge-theorem
targets named by the verdict's `notes_for_re_audit_if_any` field. It
mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`) and the PMNS active-source cluster (commit
`be5a06dbf`).
