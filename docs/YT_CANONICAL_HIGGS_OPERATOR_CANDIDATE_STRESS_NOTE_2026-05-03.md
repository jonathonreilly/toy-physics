# PR #230 Canonical-Higgs Operator Candidate Stress

Status: exact negative boundary for current substitutes; closure proposal is
not authorized.

This block stress-tests the current tempting `O_H` substitutes against the
canonical-Higgs operator certificate schema:

- the raw unratified source-Higgs smoke operator;
- a schema-padded version of that smoke operator;
- static electroweak gauge-mass algebra used as an operator;
- `H_unit` by fiat;
- an observed-target selector.

The runner is:

```bash
python3 scripts/frontier_yt_canonical_higgs_operator_candidate_stress.py
# SUMMARY: PASS=6 FAIL=0
```

It writes:

```text
outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json
```

All five current candidates are rejected.  The schema-padded unratified smoke
operator still fails because the canonical identity and local identity /
normalization certificate references are absent.  Static electroweak algebra,
`H_unit` by fiat, and observed-target selection fail their explicit firewall
checks.

As part of this block,
`scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py` was hardened
so `identity_certificate` and `normalization_certificate` must reference
existing local `docs/`, `outputs/`, or `scripts/` artifacts.  Arbitrary strings
such as an "absent" or "unratified" label no longer satisfy the reference
check.

Global gates:

```bash
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=116 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=142 FAIL=0
```

This does not derive `O_H`.  It closes a loophole in the positive
source-Higgs lane by proving that the currently available diagonal
instrumentation and known shortcuts cannot pass the operator-certificate gate.

Exact next action: supply a genuinely derived same-surface canonical-Higgs
operator identity and normalization certificate backed by local audit
artifacts, then rerun the operator certificate gate before treating any
production `C_sH/C_HH` rows as source-Higgs evidence.
