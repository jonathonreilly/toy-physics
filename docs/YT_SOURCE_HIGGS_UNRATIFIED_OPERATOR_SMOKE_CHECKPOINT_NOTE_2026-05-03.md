# PR #230 Source-Higgs Unratified-Operator Smoke Checkpoint

Status: bounded instrumentation support only; closure proposal is not
authorized.

This block exercises the new source-Higgs cross-correlator estimator path in
`scripts/yt_direct_lattice_correlator_production.py` without pretending to
solve the canonical-Higgs identity problem.  The run uses a tiny reduced-scope
`4x8` lattice and an explicitly unratified constant diagonal operator
certificate:

- `outputs/yt_source_higgs_unratified_operator_certificate_2026-05-03.json`
- `outputs/yt_source_higgs_unratified_operator_smoke_run_2026-05-03.json`
- `scripts/frontier_yt_source_higgs_unratified_operator_smoke_checkpoint.py`
- `outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json`

The smoke run emits finite-mode same-ensemble `C_ss`, `C_sH`, and `C_HH`
rows for modes `(0,0,0)` and `(1,0,0)`, including per-configuration time
series.  It also records:

- `canonical_higgs_operator_realization = certificate_supplied_unratified`;
- `canonical_higgs_operator_identity_passed = false`;
- `used_as_physical_yukawa_readout = false`;
- forbidden-import firewall fields all false;
- `pole_residue_rows = []`;
- finite-row Gram diagnostics explicitly marked as not pole residues.

The checkpoint runner passes:

```bash
python3 scripts/frontier_yt_source_higgs_unratified_operator_smoke_checkpoint.py
# SUMMARY: PASS=18 FAIL=0
```

The retained-route and campaign certificates now include this artifact as a
non-evidence row:

```bash
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=115 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=141 FAIL=0
```

This advances the positive source-Higgs route only by proving estimator
reachability and metadata/firewall behavior.  It does not supply an
audit-acceptable `O_H`, source-Higgs pole residues, Gram-purity closure,
FV/IR/model-class control, or retained-route authorization.

Exact next action: replace the unratified smoke operator with an
audit-acceptable same-surface canonical-Higgs operator certificate, run
production source-Higgs cross-correlator rows, extract isolated-pole residues,
then rerun the source-Higgs certificate builder, Gram-purity postprocessor, and
retained-route gate.
