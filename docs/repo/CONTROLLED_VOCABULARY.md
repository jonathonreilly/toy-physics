# Controlled Vocabulary

Use this note as the repo-wide status taxonomy and wording style guide.

Goals:

- keep matrix / ledger / atlas / review / note / runner language aligned
- separate publication-capture decisions from theorem-strength labels
- avoid vague shorthand on live package surfaces
- prefer explicit protocol qualifiers over loose adjectives

## Vocabulary Families

There are four different status families in this repo. Do not mix them
casually.

1. publication-capture dispositions
2. claim-strength / release labels
3. historical lane-board labels
4. historical discovery-log labels

If a file already has separate columns for `Status`, `Qualifier`, `Import
class`, or `Current publication decision`, keep one family per column rather
than collapsing everything into one hybrid phrase.

## Publication-Capture Dispositions

Use these on publication-control-plane surfaces such as
`PUBLICATION_MATRIX.md`.

| Label | Use |
|---|---|
| `retained` | live retained family on the current paper-authority surface |
| `promoted` | flagship-facing publication-core family carried directly in the current paper package |
| `bounded` | live captured family kept outside the flagship core with explicit caveats |
| `open` | live gate / blocker that is not yet closed |
| `frozen-out` | intentionally excluded from the flagship paper while still recorded |

These are package-capture decisions, not generic adjectives.

## Claim-Strength / Release Labels

Use these on notes, claims tables, quantitative tables, and runner summaries.

| Label | Use |
|---|---|
| `retained` | theorem-grade closure on the retained authority surface |
| `derived` | current-main downstream result obtained from retained structure plus named bridge/import assumptions; safe to quote, but not the same as zero-input retained closure |
| `retained corollary` | safe retained consequence of a retained theorem/action surface |
| `retained support theorem` / `retained support` | exact retained support result that is reusable but not itself the manuscript headline |
| `promoted quantitative package` | quantitative package strong enough for the current flagship-facing surface |
| `bounded companion` | live bounded supporting lane outside the flagship core |
| `bounded secondary lane` | live bounded lane worth carrying, but clearly secondary to the main package |
| `conditional / support` | useful positive package whose load-bearing step is still conditional, imposed, or support-only |
| `open flagship gate` | still-open flagship closure target |
| `historical / diagnostic` | preserved for audit/history/instrumentation, not live evidence |
| `negative-result` | useful negative or no-go result |
| `inconclusive` | signal exists but interpretation is not frozen |

Allowed composite forms should be built from the labels above and kept narrow:

- `retained exact theorem`
- `retained corollary`
- `retained support theorem`
- `bounded companion prediction`
- `promoted quantitative package`
- `open flagship gate`

Avoid minting new slash-composites when a nearby qualifier/import column can
carry the caveat instead.

## Historical Lane-Board Labels

Use these only on historical repo-map surfaces such as
`LANE_STATUS_BOARD.md` and the lane registry.

| Label | Use |
|---|---|
| `primary-retained` | current best-supported lane in the historical lane-board sense |
| `retained-companion` | real, replayable companion lane, but not the single default entrypoint |
| `open-blocker` | active blocker limiting the historical lane claim surface |
| `exploratory-reopen` | partially positive lane worth more work, but not promoted |
| `historical-control` | historical comparison/control lane |
| `historical-retained` | older retained major program, no longer the default |
| `historical-bounded` | scientifically useful historical work, no longer the lead lane |
| `historical-blocked` | diagnosed dead-end or mechanism-level blocker |

## Historical Discovery-Log Labels

Use these only on historical discovery / paper-seed ledgers such as
`POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`.

| Label | Use |
|---|---|
| `retained` | historically important retained discovery |
| `bounded-retained` | bounded positive result preserved on `main`, worth paper planning, but not a retained theorem-grade closure |
| `methodological` | important measurement / methodology / audit contribution |
| `negative-result` | strong structural no-go or narrowing result |
| `exploratory-lead` | quantitatively interesting lead worth preserving, not yet frozen |

## Column Rules

- `PUBLICATION_MATRIX.md`
  - use publication-capture dispositions for capture decisions
- `CLAIMS_TABLE.md`, `QUANTITATIVE_SUMMARY_TABLE.md`,
  `FULL_CLAIM_LEDGER.md`, `DERIVATION_ATLAS.md`
  - use claim-strength / release labels
- `LANE_STATUS_BOARD.md`
  - use historical lane-board labels
- `POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`
  - use historical discovery-log labels

Do not use row prose like `Retained ...` when the row status is
`bounded-retained`.

## Evidence Terms

Prefer these nouns:

- `protocol`: a specific constructed experimental/computational setup
- `witness`: a bounded positive signal on a stated protocol
- `diagnostic`: an instrument/readout used for triage or debugging
- `companion`: a bounded supporting lane attached to a stronger package
- `closure`: use only when the load-bearing claim is actually closed

Avoid vague upgrades like:

- `proof` when the surface is only a witness or protocol
- `closure` when the status is really `bounded-retained` or `conditional / support`

## Branch-Entanglement / BMV Language

Preferred terms for the current staggered branch-entanglement lane:

- `branch-mediated entanglement`
- `externally imposed geometry/source-branch protocol`
- `fixed-adjacency two-branch protocol`
- `branch-mediated entanglement witness`

Only call something a `BMV witness` when the surface closes the stronger
mediator-side requirements, including:

- branch/mediator structure is generated by the relevant physical degrees of
  freedom, not inserted externally
- the mediator-null / LOCC-exclusion logic is implemented at the claimed level

For the current live branch-entanglement package, say explicitly:

- `not a self-generated mediator-branch BMV witness`
- `not a mediator-null / LOCC-exclusion closure`

Avoid as the primary descriptor on live package surfaces:

- `toy`
- `toy model`
- `toy witness`
- `BMV-like evidence`

Those are acceptable only in historical commentary where the sentence also says
what the protocol is missing.

## Boundary-Law Language

For the live boundary-law lane, prefer:

- `Dirac-sea boundary-law probe`
- `many-body-style boundary-law result`
- `bounded boundary-law package`

Avoid calling historical transfer-entropy scripts:

- `area law`
- `subsystem entanglement measurement`

unless the measured object actually matches that wording.

## Historical Retirement Language

When an old runner is no longer live evidence, prefer:

- `retired as evidence`
- `historical / diagnostic`
- `historical exploratory predecessor`

Avoid ambiguous phrasing like:

- `still useful`

unless the sentence also states exactly for what it is still useful.
