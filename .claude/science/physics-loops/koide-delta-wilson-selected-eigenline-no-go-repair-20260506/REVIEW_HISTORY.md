# Review History

- Starting audit status: `audited_failed`.
- Blocking issue: the source note and expected closeout claimed an ambient
  eta-proxy residual, while the runner computed `2/9` and returned one failed
  check.
- Repair: remove that residual from the claim boundary and turn it into a
  positive comparator check.
- Local verification: selected runner `14/14`, hostile-review guard `8/8`,
  Koide lane regression `381/381`.
- Audit pipeline: source-note hash was re-seeded, the prior failed audit was
  archived, and the current row is `unaudited` pending independent re-audit.
