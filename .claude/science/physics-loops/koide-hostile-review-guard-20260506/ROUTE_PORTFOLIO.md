# Route Portfolio

| Route | Score | Disposition |
|---|---:|---|
| Execute every target no-go script and parse captured stdout labels | 5/5 | Already present in the runner; kept as the main closure path. |
| Add a guard self-test that executes temporary scripts with dead/comment literals | 5/5 | Chosen. Directly targets the archived auditor's failure mode. |
| AST-parse print paths instead of executing scripts | 2/5 | Rejected for this turn because execution is simpler and proves the emitted surface. |
| Demote the note to shallow source scan | 1/5 | Rejected because the existing runner can support the stronger meta claim. |

Chosen route: keep live script execution and add an executable regression mode
that fails if source-only literals can satisfy the emitted-output predicates.
