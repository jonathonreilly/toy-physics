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
| `retained support batch` | coherent retained batch of support theorems/tools carried together for atlas, reviewer, or support-package reuse |
| `retained exact theorem` / `retained exact companion` | exact retained theorem/companion variant used when exactness itself is part of the safe statement |
| `retained structural theorem` / `retained exact structural theorem` | retained exact structural law on the framework/package surface |
| `retained support tool` | reusable retained tool/subderivation that supports other lanes without itself being the manuscript headline |
| `retained framework statement` / `retained positioning` / `retained quantitative lane` | retained package-authority framing labels for front-door/control-plane use |
| `retained action-surface closure` / `retained restricted theorem` / `retained restricted support` / `retained evaluated theorem` | retained exact-result variants where the constrained surface/class/evaluation matters |
| `retained positive` / `retained partial positive` | retained positive lane result used mainly on atlas/toolbox surfaces rather than as the headline theorem |
| `exact support theorem` / `exact support` | accepted exact-support variant when exactness itself is material to the safe statement; use with the same non-headline semantics as retained support, and keep bridge/import qualifiers explicit |
| `exact support batch` | coherent exact batch of support theorems/tools carried together for atlas or reviewer reuse |
| `exact structural theorem` / `exact algebraic identity` / `exact subderivation` | accepted exact-result specializations for atlas / theorem-bank rows when the mathematical role matters |
| `exact boundary theorem` / `exact reduction theorem` | accepted exact-result specializations for atlas / theorem-bank rows when the mathematical role is an open-lane boundary or a compression/reduction statement |
| `exact current-stack theorem` / `exact current-bank theorem` / `exact current-bank reduction` / `exact current-bank no-go theorem` | accepted exact-result specializations for current-stack/current-bank closeout rows on atlas and reviewer surfaces |
| `exact negative boundary` / `exact negative closeout` / `exact post-selector reduction` | accepted exact-result specializations for explicit no-go/closeout/post-selector roles on atlas and reviewer surfaces |
| `exact support/boundary theorem` | accepted mixed exact-role label when a row simultaneously contributes a reusable exact support input and an exact open-lane boundary statement |
| `exact support tool` | reusable exact tool/subderivation that supports other lanes without being the headline claim |
| `bounded support theorem` / `bounded support note` / `bounded support tool` | bounded supporting result/tool carried for atlas, reviewer, or secondary-lane use; not a flagship closure claim |
| `bounded support batch` | coherent bounded batch of support tools/calculations carried for atlas or reviewer reuse |
| `promoted quantitative package` | quantitative package strong enough for the current flagship-facing surface |
| `bounded companion` | live bounded supporting lane outside the flagship core |
| `bounded secondary lane` | live bounded lane worth carrying, but clearly secondary to the main package |
| `bounded frontier` / `bounded negative boundary` / `bounded Route 2 build candidate` | bounded frontier/result classes kept for ongoing design work rather than current-package promotion |
| `flagship closure package` | package-level flagship-facing closure claim on the current review/package surface; stronger than support, but not automatically the retained quantitative paper core |
| `conditional / support` | useful positive package whose load-bearing step is still conditional, imposed, or support-only |
| `open flagship gate` | still-open flagship closure target |
| `historical / diagnostic` | preserved for audit/history/instrumentation, not live evidence |
| `historical support / provenance` / `exact transport provenance` | provenance-only rows kept for route history, reviewer handoff, or closure bookkeeping rather than live promotion |
| `negative-result` | useful negative or no-go result |
| `negative-result / support` | negative/no-go result that is also a reusable support/pruning surface |
| `inconclusive` | signal exists but interpretation is not frozen |

Allowed composite forms should be built from the labels above and kept narrow:

- `retained exact theorem`
- `retained exact companion`
- `retained structural theorem`
- `retained exact structural theorem`
- `retained corollary`
- `retained support theorem`
- `retained support batch`
- `retained support tool`
- `exact support theorem`
- `exact support batch`
- `exact structural theorem`
- `exact algebraic identity`
- `exact subderivation`
- `exact boundary theorem`
- `exact reduction theorem`
- `exact current-stack theorem`
- `exact current-bank theorem`
- `exact current-bank reduction`
- `exact current-bank no-go theorem`
- `exact negative boundary`
- `exact negative closeout`
- `exact post-selector reduction`
- `exact support/boundary theorem`
- `exact support tool`
- `bounded support theorem`
- `bounded support note`
- `bounded support tool`
- `bounded support batch`
- `bounded companion prediction`
- `bounded frontier`
- `bounded negative boundary`
- `bounded Route 2 build candidate`
- `flagship closure package`
- `promoted quantitative package`
- `open flagship gate`

Avoid minting new slash-composites when a nearby qualifier/import column can
carry the caveat instead.

Role-specialized variants are acceptable when the cell begins with one of the
accepted base labels above and the trailing noun names the mathematical role
or control-plane role of the row, for example:

- `retained framework statement`
- `retained quantitative lane`
- `retained action-surface closure`
- `retained restricted theorem`
- `exact structural theorem`
- `exact algebraic identity`
- `exact subderivation`
- `retained support tool`
- `retained support batch`
- `exact support tool`
- `exact support batch`
- `exact boundary theorem`
- `exact reduction theorem`
- `exact current-stack theorem`
- `exact current-bank theorem`
- `exact current-bank no-go theorem`
- `exact negative boundary`
- `exact negative closeout`
- `exact post-selector reduction`
- `historical support / provenance`

Do not mix a publication-capture disposition with a claim-strength label in
the same cell unless the file explicitly allows hybrid narrative decisions.

Short scope qualifiers may follow an accepted label when they state where the
claim lives, for example:

- `exact boundary theorem on open gate`
- `exact reduction theorem outside flagship core`
- `exact support theorem on the bounded charged-lepton package`
- `exact support theorem with bounded downstream reuse`
- `retained support theorem on the current package surface`

Do not use `reviewed` or `reviewer-tested` as status labels. Those are review
process adjectives, not controlled-vocabulary claim-strength labels. Carry
review context in prose, placement, or authority notes instead.

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
  - `Current publication decision` cells should begin with one of
    `retained`, `promoted`, `bounded`, `open`, `frozen-out`; a short
    placement note may follow after a semicolon
- `CLAIMS_TABLE.md`, `QUANTITATIVE_SUMMARY_TABLE.md`,
  `DERIVATION_ATLAS.md`
  - use claim-strength / release labels
  - accepted role-specialized variants may be used when they begin with the
    primary claim-strength label
- `FULL_CLAIM_LEDGER.md`
  - may begin with either a publication-capture disposition or a
    claim-strength label because it narrates package decisions row-by-row
  - avoid ad hoc hybrids; if a row begins with one family, keep any
    second-family qualifier short and explanatory
  - on mixed audit rows, the cell should begin with the primary label from
    the family being used; a short explanatory qualifier may follow after a
    semicolon
  - accepted ledger-style hybrids include forms such as
    `promoted exact companion`, `promoted restricted theorem`,
    `promoted retained closure`, `promoted retained support batch`, and
    `promoted retained action-surface closure`
- `LANE_STATUS_BOARD.md`
  - use historical lane-board labels
- `POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`
  - use historical discovery-log labels

Do not use row prose like `Retained ...` when the row status is
`bounded-retained`.

## Protocol Qualifiers

These are qualifiers, not standalone status labels:

- `review surface`
- `current package grade`
- `strict/native map`
- `exact-target strict/native map`

They can appear in prose or qualifier/import columns, but they should not
replace the primary status label.

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

## Hyphenation

- prefer `observational-pin` as a compound adjective
- use `observational pin` only as a noun phrase

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
