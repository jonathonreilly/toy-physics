# Route Portfolio

| Route | Goal | Outcome | Reason |
|-------|------|---------|--------|
| R1: derive residual environment | close the gate by proving the residual environment data | rejected | belongs in companion notes; out of bounded scope |
| R2: convert to no_go on local-only | flip claim_type to no_go | rejected | misclassifies positive factorization content |
| R3: prose-only narrow | tighten note text but leave open_gate | rejected | does not move effective_status |
| R4 (chosen): tighten + cross-family bounded_theorem audit | flip open_gate -> bounded_theorem with new auditor independence | executed | minimal-edit honest move |

## Selection rationale

R4 alone passes the dramatic-step gate (changes effective_status from
`open_gate` to `retained_bounded`, retiring an open_gate from the repo
and unblocking 246 transitive descendants from gate-induced chain
blocking). The move is honest: the note's load-bearing math is
unchanged, only the audit-classification language is tightened to
match what the proof actually delivers. A cross-family independent
auditor (Anthropic vs prior Codex auditors) is required to ratify the
new claim_type without a self-audit conflict.

Routes R1-R3 are recorded as no-go in `NO_GO_LEDGER.md` so future
campaign cycles do not re-explore them.
