# YT Schur Kernel Row Contract Gate

```yaml
actual_current_surface_status: open / Schur kernel row contract gate not passed; current rows absent
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_schur_kernel_row_contract_gate.py`
**Certificate:** `outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json`

## Purpose

The Schur-complement K-prime theorem makes `K'(pole)` computable once the
same-surface neutral scalar kernel rows are known.  This block turns that
statement into an executable input contract for future rows instead of leaving
the next action as an informal theorem request.

The future row file is:

```text
outputs/yt_schur_scalar_kernel_rows_2026-05-03.json
```

The accepted row contract requires a same-surface Cl(3)/Z^3 scalar kernel
partition, pole-control certificate, firewall metadata, and either one-mode
Schur rows

```text
A(pole), B(pole), C(pole), A'(pole), B'(pole), C'(pole)
```

or precontracted matrix Schur rows sufficient to compute
`D_eff(pole)` and `D_eff'(pole)`.

## Result

The runner validates an in-memory positive witness for the contract and rejects
source-only shortcuts:

```bash
python3 scripts/frontier_yt_schur_kernel_row_contract_gate.py
# SUMMARY: PASS=12 FAIL=0
```

Current PR #230 has no Schur scalar kernel row file, so the executable gate is
not passed.

## Boundary

This is not retained or proposed-retained top-Yukawa closure.  It does not
derive the missing rows, it does not identify the source pole with the
canonical Higgs radial mode, and it does not turn source-only `C_ss` data into
physical `y_t`.

The next positive closure action is to produce the same-surface Schur rows or
precontracted matrix rows with partition, pole-control, and firewall
certificates, then rerun this gate and the retained-closure certificate.

This block does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`, and it does not set `kappa_s`, `c2`, `Z_match`,
or `cos(theta)` to one.
