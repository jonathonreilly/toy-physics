# Handoff

This block closes the missing artifact chain identified by the failed audit:
the note now points to a repo-relative primary runner and a SHA-pinned cache,
the audit ledger registers the runner, and the note explains where the
deterministic `spacing / sqrt(3)` schedule enters the computation.

Verification commands:

```bash
python3 scripts/cached_runner_output.py scripts/lattice_nn_deterministic_rescale.py --check-only
python3 -c "import scripts.canonical_regression_gate as g; g.check_nn_deterministic_rescale()"
```

Exact next action: run the audit loop for
`lattice_nn_deterministic_rescale_note`.
