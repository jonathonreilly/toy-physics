# SU(3)^3 Cubic Gauge Anomaly Cancellation Theorem

Date: 2026-04-24

**Status:** bounded_theorem on the retained graph-first SU(3) gauge surface,
conditional on the assumed one-generation color-matter completion (Q_L
SU(3) fundamental at weak multiplicity 2, plus u_R^c and d_R^c as SU(3)
anti-fundamentals). The matter-content premise is an admitted external
input; this theorem does not derive the right-handed anti-triplet
completion. Given the premise, the cubic-index sum
`+2 - 1 - 1 = 0` is exact.

**Type:** bounded_theorem (cubic SU(3) gauge anomaly arithmetic on the
assumed one-generation color matter table; see `## Scope` for the
explicit not-claimed boundary).

**Claim type:** bounded_theorem

**Primary runner:** `scripts/frontier_su3_cubic_anomaly_cancellation.py`

## Statement

For chiral Weyl fermions coupled to `SU(3)`, the pure cubic gauge anomaly is
proportional to

```text
sum_i m_i A(R_i),
```

where `m_i` is the multiplicity from non-color indices and `A(R_i)` is the
`SU(3)` cubic anomaly index of the color representation:

```text
A(1) = 0,  A(3) = +1,  A(3bar) = -1,  A(8) = 0,
A(6) = +7, A(6bar) = -7.
```

On the retained one-generation content written in the left-handed conjugate
frame,

| field | `SU(3)` rep | weak multiplicity | contribution |
|---|---:|---:|---:|
| `Q_L` | `3` | 2 | `+2` |
| `u_R^c` | `3bar` | 1 | `-1` |
| `d_R^c` | `3bar` | 1 | `-1` |
| `L_L`, `e_R^c`, `nu_R^c` | `1` | any | `0` |

so

```text
sum_i m_i A(R_i) = +2 - 1 - 1 = 0.
```

Thus the retained color-charged matter content cancels the pure `SU(3)^3`
cubic gauge anomaly exactly.

## Retained Inputs

| Input | Authority |
|---|---|
| Retained graph-first `SU(3)` gauge sector and `N_c = 3` color count | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained left-handed `Q_L`, `L_L` content | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), `ANOMALY_FORCES_TIME_THEOREM.md` |
| Retained one-generation right-handed completion | `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`, `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md` |
| Standard `SU(3)` cubic anomaly indices | Lie-algebra input for chiral gauge anomalies |

## Proof On Retained Content

Use the left-handed conjugate frame. The right-handed color triplets are
represented as left-handed anti-triplets:

```text
u_R  ->  u_R^c in 3bar,
d_R  ->  d_R^c in 3bar.
```

The only `SU(3)`-charged retained fields are `Q_L`, `u_R^c`, and `d_R^c`.
Leptons are color singlets and do not contribute.

The retained quark doublet contributes two color fundamentals because it has
two weak components:

```text
Q_L: 2 * A(3) = 2.
```

The retained right-handed colored singlets contribute two anti-fundamentals:

```text
u_R^c: A(3bar) = -1,
d_R^c: A(3bar) = -1.
```

Therefore:

```text
SU(3)^3 anomaly index = 2 - 1 - 1 = 0.
```

Equivalently, the retained one-generation content is vector-like with respect
to net color fundamentals:

```text
2 copies of 3  -  2 copies of 3bar  = 0.
```

This is not automatic for `SU(3)`. It is a real matter-content condition.

## Relation To Other Anomaly Rows

This theorem is separate from:

- the hypercharge and mixed-gauge anomaly equations used in
  `ANOMALY_FORCES_TIME_THEOREM.md`;
- the SM hypercharge uniqueness theorem;
- the nonperturbative `SU(2)` Witten `Z_2` global anomaly;
- `B-L` anomaly freedom as a gaugeable option.

The pure `SU(2)^3` cubic gauge anomaly is different: it vanishes
group-theoretically because the symmetric `d^{abc}` tensor for `SU(2)` is
zero. The pure `SU(3)^3` anomaly does not vanish group-theoretically; it
vanishes here because the retained matter content has balanced `3` and
`3bar` contributions.

## Extension Surface

Starting from the retained one-generation value `0`:

| Extension | Change in `SU(3)^3` index | Status |
|---|---:|---|
| Add one chiral color fundamental with no partner | `+1` | anomalous |
| Add one chiral color anti-fundamental with no partner | `-1` | anomalous |
| Add a vectorlike `3 + 3bar` pair | `0` | allowed by this anomaly |
| Remove `u_R^c` or `d_R^c` | `+1` | anomalous |
| Add one full retained-style generation | `0` | allowed by this anomaly |
| Add one `6` with no `6bar` | `+7` | anomalous |
| Add one adjoint `8` | `0` | allowed by this anomaly |

Thus any extension with chiral color charge must preserve
`sum_i m_i A(R_i) = 0`.

## Scope

### What this bounded theorem claims

Given the one-generation color-matter premise

```text
Q_L : SU(3) fundamental, weak multiplicity 2,
u_R^c : SU(3) anti-fundamental, weak multiplicity 1,
d_R^c : SU(3) anti-fundamental, weak multiplicity 1,
all leptonic and color-singlet fields contribute zero,
```

and given the standard SU(3) cubic anomaly indices
`A(3) = +1, A(3bar) = -1`, this theorem proves the exact rational
identity

```text
sum_i m_i A(R_i) = 2 (+1) + 1 (-1) + 1 (-1) = 0.
```

The theorem is a structural cubic-index arithmetic identity *given*
the matter-content premise. The runner verifies the cubic-index sum on
the named matter table and the extension boundaries.

### What this theorem does NOT claim

- It does not derive the right-handed anti-triplet completion
  `u_R^c, d_R^c in 3bar`. That input is admitted from
  `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` (currently
  `audited_conditional`) and
  `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
  (currently `unaudited`). The closing derivation of the
  anti-fundamental completion is pursued in a separate physics-loop
  block (`physics-loop/su3-anomaly-forced-3bar-completion-derivation-2026-05-02`,
  PR #382), which, if it lands at retained-grade, would lift the
  conditional and could re-audit this row to positive_theorem.
- It does not prove the full right-handed lepton sector; leptons are
  color singlets and are invisible to `SU(3)^3`.
- It does not derive `N_c = 3`; that input comes from the graph-first
  color lane.
- It does not claim the retained completion is the only possible
  `SU(3)^3`-anomaly-free completion, since vectorlike and other
  balanced extensions can also cancel this anomaly.
- It does not replace the perturbative hypercharge anomaly equations,
  the Witten `SU(2)` anomaly theorem, or the `B-L` anomaly-freedom
  theorem.

### Audit-readiness boundary

The audit verdict on this row (`audited_conditional` per Codex
2026-05-02) explicitly identifies the right-handed matter completion
as the conditional surface and prescribes the boundary:
"if the stated one-generation SU(3) representations are assumed, the
standard cubic-index arithmetic cancels exactly." By narrowing the
claim type from `positive_theorem` to `bounded_theorem` (with the
matter-content premise made explicit), the bounded scope matches what
the runner actually verifies and is audit-ready as
`bounded_theorem` -> `retained_bounded`.

## Reproduction

Run:

```bash
python3 scripts/frontier_su3_cubic_anomaly_cancellation.py
```

The runner checks the retained content, the exact `+2 - 1 - 1 = 0` anomaly
sum, extension scenarios, the `SU(2)^3` zero tensor, and the nonzero
`SU(3)` symmetric tensor that makes the color anomaly a genuine matter-content
condition.
