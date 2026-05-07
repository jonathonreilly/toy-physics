# PR230 Higher-Shell Schur/Scalar-LSZ Production Contract

Status: bounded support / higher-shell production contract; no physics
closure.

Runner:
`scripts/frontier_yt_pr230_schur_higher_shell_production_contract.py`

Certificate:
`outputs/yt_pr230_schur_higher_shell_production_contract_2026-05-07.json`

## Purpose

The current two-source taste-radial row campaign is a live four-mode
`63`-chunk packet.  It should not be changed midstream.  Its strict
scalar-LSZ/Schur diagnostics have only two ordered `q_hat^2` levels, so
`C_x|s` can pass a first-shell Stieltjes direction but cannot test complete
monotonicity or threshold structure.

This contract defines a separate future higher-shell campaign rather than
mutating chunks037-063.

## Contract

The future mode set is:

```text
0,0,0
1,0,0  0,1,0  0,0,1
1,1,0  1,0,1  0,1,1
1,1,1
2,0,0  0,2,0  0,0,2
```

On `L=12` this supplies five ordered `q_hat^2` levels:

```text
0
0.267949192431123
0.535898384862245
0.803847577293368
1.0
```

The runner emits non-colliding future commands under:

```text
outputs/yt_pr230_schur_higher_shell_rows/
outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/
```

with seed base `2026057000`.  It does not launch jobs and it does not write
measurement rows.

## Current Boundary

The active campaign remains the four-mode `C_ss/C_sx/C_xx` packet and must
finish or be separately checkpointed before any higher-shell campaign is
launched.  The refreshed certificate detects chunks036-037 as active; chunk035
has completed but is not packaged by this support-only contract.  The contract
is infrastructure support only.  It does not supply:

- a complete higher-shell packet;
- complete monotonicity;
- threshold/model-class/pole authority;
- multivolume FV/IR authority;
- canonical `O_H` or source-overlap authority;
- W/Z physical-response authority.

No `y_t` closure proposal is authorized.

## Validation

```bash
python3 scripts/frontier_yt_pr230_schur_higher_shell_production_contract.py
# SUMMARY: PASS=16 FAIL=0
```
