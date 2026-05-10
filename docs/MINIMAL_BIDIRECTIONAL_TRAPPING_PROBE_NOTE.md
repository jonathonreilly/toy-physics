# Minimal Bidirectional Trapping Probe

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical observation on the runner-defined no-restore
grown geometry family at `h = 0.5`, `W = 10`, `NL = 25`, seeds `0..3`,
`z = {3, 4, 5}`, `drift = 0.2`. Frozen on disk.
**Status authority:** independent audit lane only.
**Claim scope:** at `alpha = 0` the runner reproduces the runner-defined
weak-field readout (3/3 TOWARD, `F~M = 1.00` on both exact grid and
sector stencil). At `alpha >= 0.10` on the same scope the runner-
computed escape fraction drops below `50%` and at `alpha >= 0.5` the
escape fraction is `~ 0.02`. The claim is explicitly bounded to this
runner-defined harness and does not derive a no-return threshold,
a black-hole observable, or a strong-field trapping law from accepted
framework primitives.

## Audit boundary (2026-05-10)

The independent audit verdict on this row's most recent active hash
was `audited_failed`. The audit rationale named two issues: the
referenced frozen log path was absent at the time of audit, and the
note's branch verdict overstated the proxy as producing a "retained
threshold" while the load-bearing observable is a hand-added `alpha`
trapping proxy with no derivation from retained dynamics. The audit's
repair target was: "restore or regenerate the frozen log, correct the
Status/source status to bounded/proposed_bounded, or derive the
trapping parameter from retained dynamics."

This 2026-05-10 rigorize pass selects **PATH B** of the audit's
repair target: explicitly scope the load-bearing claim to the bounded
numerical statement on the runner-defined harness, with the trapping
parameter `alpha` recorded as a hand-added proxy (not derived from
A_min primitives). The earlier 2026-05-01 frozen log regeneration is
not currently visible in the working tree at the cited path; the live
runner reproduces the table on 2026-05-10. PATH A (deriving the
trapping law from retained dynamics) is deferred to future work as a
separate retained promotion.

## Hand-added proxy (NOT derived in this packet)

The following modeling input is a hand-added proxy used in the runner;
it is NOT derived from A_min primitives in this note:

- **Trapping parameter `alpha`** — applied as a uniform per-step
  damping on the propagated amplitude. There is no field-theoretic
  source law, no no-return condition, and no constraint from accepted
  primitives that picks the values `alpha in {0.0, 0.1, 0.3, 0.5, 2.0, 10.0}`.
  The bounded numerical observation here is purely about the runner-
  computed escape fraction at these chosen `alpha` values on the
  declared scope.

## Cluster note (2026-05-10): duplicate harness with absorbing-horizon probe

This probe and
[`MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md`](MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md)
share the identical runner harness and produce identical output (escape
fraction `1.0002` at `alpha=0`, `0.4353` at `alpha=0.10`, `0.0903` at
`alpha=0.30`, `0.0202` at `alpha=0.50`, `0.0000` at `alpha in {2.0, 10.0}`).
The two notes differ only in framing (bidirectional/no-return language
here versus absorbing-horizon language in the sibling). They are not
two independent probes; they are the same bounded numerical harness
read in two ways. Treat the cluster as one bounded numerical
observation with two framings.

## Upstream one-hop dependencies (audit-disclosed)

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`).
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md)
  (`audit_status: audited_conditional`).
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md)
  (`audit_status: audited_conditional`).
- [`docs/GATE_B_FARFIELD_NOTE.md`](GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — upstream Gate B far-field
  reference whose primitive-to-physical-gravity bridge is itself
  flagged in the cluster rigorize pass (PR #58a471d23).

## Artifact chain

- [`scripts/minimal_bidirectional_trapping_probe.py`](../scripts/minimal_bidirectional_trapping_probe.py)
- [`logs/2026-04-05-minimal-bidirectional-trapping-probe.txt`](../logs/2026-04-05-minimal-bidirectional-trapping-probe.txt)
  (file may be absent in working tree; runner reproduces it on demand)

## Question

Can a minimal trapping extension create a genuine no-return threshold on the
retained generated-geometry family while still reducing back to the weak-field
lane at `alpha = 0`?

This note is intentionally narrow:

- one trapping parameter `alpha`
- one observable: escape fraction versus `alpha`
- one weak-field recovery check at `alpha = 0`

## Frozen result

The frozen log is on the retained no-restore grown geometry family with the
geometry-sector stencil connectivity, `h = 0.5`, `W = 10`, `NL = 25`,
`seeds = 4`, and `z = [3, 4, 5]`.

Weak-field recovery check:

- exact grid: `3/3` TOWARD, `F~M = 1.00`
- sector stencil: `3/3` TOWARD, `F~M = 1.00`

Escape fraction versus absorption:

| alpha | escape | no-return |
| --- | ---: | ---: |
| `0.00` | `1.0002` | `-0.0002` |
| `0.10` | `0.4353` | `0.5647` |
| `0.30` | `0.0903` | `0.9097` |
| `0.50` | `0.0202` | `0.9798` |
| `2.00` | `0.0000` | `1.0000` |
| `10.00` | `0.0000` | `1.0000` |

## Safe read

The strongest bounded numerical statement, on the declared
runner-defined scope, is:

- the runner-computed escape fraction falls below `50%` at `alpha ≈ 0.10`
- the weak-field reduction check at `alpha = 0` matches the
  runner-defined retained-lane signature (`3/3` TOWARD on both exact
  grid and sector stencil)

The bounded honest limitation:

- the trapping parameter `alpha` is a hand-added proxy, not a
  derivation of a no-return law from A_min primitives
- "no-return threshold" language refers to the runner-computed escape
  fraction crossing 50%, not to a black-hole horizon observable
- the upstream Gate B one-hop deps are themselves
  `audited_conditional` (see "Upstream one-hop dependencies" above),
  so the runner-defined "retained-lane" reduction is itself currently
  conditional

## Relation to the retained lane (cross-references)

Read this together with the audit-disclosed upstream dependencies
listed above:

- [`GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`).
- [`GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md)
  (`audit_status: audited_conditional`).
- [`GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md)
  (`audit_status: audited_conditional`).
- [`GATE_B_FARFIELD_NOTE.md`](GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`).

The runner-defined weak-field readout reduction (at `alpha = 0`) is
recorded as a bounded numerical companion to the upstream Gate B
cluster, conditional on those one-hop dependencies; the trapping
branch is recorded as a runner-defined bounded threshold readout, not
a derived strong-field observable.

## Branch verdict

The runner-defined harness produces a **bounded numerical observation**
on the declared scope. It is not a full black-hole theory, the
trapping parameter `alpha` is hand-added (not derived from A_min
primitives), and the broader "retained no-return threshold" reading
is recorded only as a moonshot framing — not as a closed theorem. The
bounded numerical statement is: at `alpha = 0` the weak-field readout
matches the runner-defined retained lane; at `alpha >= 0.10` the
escape fraction drops below `50%`; at large `alpha` the escape
fraction is `~ 0`. PATH A (deriving the trapping law from retained
dynamics with audited dependencies) is deferred to future work as a
separate retained promotion.
