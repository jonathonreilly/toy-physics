# SU(2) Witten Z_2 Global Anomaly Cancellation Theorem

**Date:** 2026-04-24
**Type:** positive_theorem
**Primary runner:** [`scripts/frontier_su2_witten_z2_anomaly.py`](../scripts/frontier_su2_witten_z2_anomaly.py) (PASS=35/0)
**Claim type:** structural-anomaly cancellation theorem (binary parity arithmetic on retained chiral fermion content)
**Claim scope:** for the retained SM left-handed chiral fermion content `Q_L : (2,3)_{+1/3}` (3 colour copies) plus `L_L : (2,1)_{-1}` (1 colour copy) replicated across the retained three generations, the count of fundamental SU(2) Weyl doublets is `N_D = n_gen * (N_c + 1) = 12`, even, so the Witten Z_2 global anomaly cancels. Conditional on retained native SU(2) gauge structure, retained N_c = 3 colour count, and retained three-generation structure as upstream inputs.
**Status:** awaiting independent audit. Under the scope-aware classification framework, ratified status is computed by the audit pipeline from audit-lane data; no author-side retained tier is asserted in source.

## Statement

The fourth homotopy group of `SU(2)` is

```text
pi_4(SU(2)) = Z_2.
```

For an `SU(2)` gauge theory whose chiral Weyl fermion content contains
`N_D` fundamental weak doublets, counted with color multiplicity and across
all generations, the Witten global anomaly cancels iff

```text
N_D = 0 mod 2.
```

On the retained one-generation content,

```text
Q_L: 3 color copies of one SU(2) doublet
L_L: 1 lepton SU(2) doublet
```

so

```text
N_D(one generation) = N_c + 1 = 3 + 1 = 4 = 0 mod 2.
```

Across the retained three generations,

```text
N_D(three generations) = 3 * 4 = 12 = 0 mod 2.
```

Thus the retained `SU(2)` matter content is globally anomaly-free at the
nonperturbative Witten `Z_2` level.

## Retained Inputs

| Input | Authority |
|---|---|
| Native `SU(2)` gauge structure | [NATIVE_GAUGE_CLOSURE_NOTE.md](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Retained left-handed `Q_L`, `L_L` doublet content | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), `ANOMALY_FORCES_TIME_THEOREM.md` |
| Retained `N_c = 3` color count | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained three-generation structure | [THREE_GENERATION_STRUCTURE_NOTE.md](THREE_GENERATION_STRUCTURE_NOTE.md) |
| Singlet right-handed completion | `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`, `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md` |

The homotopy fact `pi_4(SU(2)) = Z_2` and the associated sign obstruction are
standard Witten-anomaly input. The repo theorem here packages the count on the
retained matter surface.

## Proof On Retained Content

The Witten anomaly is not a perturbative triangle anomaly. A large gauge
transformation representing the nontrivial element of `pi_4(SU(2))` changes
the sign of the fermion Pfaffian for one chiral Weyl doublet. For `N_D`
doublets, the sign is

```text
(-1)^(N_D).
```

Gauge consistency therefore requires this sign to be `+1`, i.e.
`N_D` even.

The retained one-generation content contributes:

| Field | `SU(2)` rep | color multiplicity | Witten doublet count |
|---|---:|---:|---:|
| `Q_L` | doublet | 3 | 3 |
| `L_L` | doublet | 1 | 1 |
| `u_R` | singlet | 3 | 0 |
| `d_R` | singlet | 3 | 0 |
| `e_R` | singlet | 1 | 0 |
| `nu_R` | singlet | 1 | 0 |

Therefore:

```text
N_D(one generation) = 3 + 1 = 4.
```

The anomaly cancels per generation. Replicating the retained generation three
times preserves cancellation:

```text
N_D(total) = 3 * 4 = 12.
```

## Parity Structure

For the retained one-generation pattern with one lepton doublet and `N_c`
quark-color copies,

```text
N_D(per generation) = N_c + 1.
```

Per-generation Witten cancellation holds iff `N_c` is odd. The retained
`N_c = 3` therefore gives the stronger local result that each generation is
already Witten-safe.

The global condition is slightly broader:

```text
N_D(total) = n_gen * (N_c + 1)
```

must be even. This note does not claim a native-axiom derivation of
`N_c = 3`; it only records that the retained `N_c = 3` matter surface passes
the nonperturbative `SU(2)` global-anomaly test.

## Falsification And Extension Surface

The count is binary. Starting from the retained three-generation total
`N_D = 12`:

| Extension | Added chiral weak doublets | New total parity | Witten status |
|---|---:|---:|---|
| Add one extra lepton-like chiral doublet | 1 | odd | anomalous |
| Add one quark-like chiral doublet with three colors | 3 | odd | anomalous |
| Add one full retained-style generation | 4 | even | allowed by Witten |
| Add one vectorlike weak-doublet pair | 2 | even | allowed by Witten |
| Add a full mirror retained-style generation | 4 | even | allowed by Witten |

Right-handed weak doublets would still count after conversion to left-handed
conjugate Weyl fields; the `SU(2)` fundamental is pseudoreal.

## Higgs Boundary

The Higgs is an `SU(2)` doublet, but it is bosonic. The Witten anomaly is a
fermion-measure obstruction, so scalar doublets do not contribute to `N_D`.
Consequently, the Witten count does not constrain the number of Higgs
doublets.

## Scope

This theorem covers the Witten global anomaly for fundamental `SU(2)` Weyl
doublets on the retained matter content.

It does not reprove the perturbative anomaly equations in
`ANOMALY_FORCES_TIME_THEOREM.md`.

It does not replace the SM hypercharge uniqueness theorem or the `B-L`
anomaly-freedom theorem.

It does not classify possible higher-isospin `SU(2)` representations outside
the retained content.

It does not claim that `B-L` is gauged, that new weak-doublet matter exists, or
that `N_c = 3` is derived here.

## Reproduction

Run:

```bash
python3 scripts/frontier_su2_witten_z2_anomaly.py
```

The runner enumerates the retained doublet content, checks per-generation and
three-generation parity, scans `N_c` and `n_gen`, verifies extension scenarios,
and confirms that bosonic Higgs doublets are excluded from the Witten count.

## Honest claim-status

```yaml
proposed_claim_type: positive_theorem
status_authority: independent audit lane only
audit_required_before_effective_retained: true
actual_current_surface_status: structural-anomaly cancellation theorem on retained left-handed chiral SU(2) doublet content
conditional_surface_status: Witten Z_2 cancellation on retained N_c = 3, n_gen = 3 surface; the per-generation arithmetic N_D = N_c + 1 = 4 is even (Witten-safe) iff N_c is odd, and the retained N_c = 3 is supplied by the graph-first SU(3) integration upstream
hypothetical_axiom_status: null
admitted_observation_status: "Standard Witten (1982) homotopy fact pi_4(SU(2)) = Z_2 admitted as universal QFT input; the fermion-Pfaffian sign rule (-1)^N_D admitted as standard nonperturbative anomaly machinery."
proposal_allowed: false
proposal_allowed_reason: "Source note records the structural cancellation theorem. Effective retained tier is set by the independent audit lane based on retained-grade upstream availability of NATIVE_GAUGE_CLOSURE_NOTE (SU(2) gauge structure), GRAPH_FIRST_SU3_INTEGRATION_NOTE (N_c = 3), and THREE_GENERATION_STRUCTURE_NOTE (n_gen = 3); not asserted by author."
bare_retained_allowed: false
```
