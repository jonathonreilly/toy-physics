# YT Schur Compressed-Denominator Row-Bootstrap No-Go

```yaml
actual_current_surface_status: exact negative boundary / Schur compressed-denominator row-bootstrap no-go
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_schur_compressed_denominator_row_bootstrap_no_go.py`
**Certificate:** `outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json`

## Purpose

Cycle 7 tests the remaining Schur shortcut that is not covered by the finite
ladder/Feshbach row-extraction no-go: reconstructing the missing same-surface
`A/B/C` kernel rows from an already-compressed scalar denominator
`D_eff(x)`, or from `D_eff'(x_pole)`.

The accepted Schur route still needs actual rows:

```text
K(x) = [[A(x), B(x)^T],
        [B(x), C(x)]]
```

with the source/orthogonal partition, pole control, and row-firewall metadata.

## Result

The runner constructs two explicit one-orthogonal-mode Schur partitions.  They
share the same pole, the same compressed denominator over the test grid, and
the same pole derivative:

```text
D_eff(x) = A(x) - B(x)^2 / C(x).
```

Their `A/B/C` rows and row derivatives differ.  Therefore the compressed
denominator and its pole derivative do not reconstruct the missing kernel
rows, even before any physical-readout bridge is considered.

Verification:

```bash
python3 scripts/frontier_yt_schur_compressed_denominator_row_bootstrap_no_go.py
# SUMMARY: PASS=11 FAIL=0
```

## Boundary

This block does not produce `A/B/C` rows and does not close PR #230.  It only
closes the shortcut that tries to bootstrap those rows from the Schur-compressed
denominator.  The Schur route remains viable only through genuine same-surface
kernel rows from a neutral scalar kernel theorem or measurement.

Next positive actions remain: real Schur kernel rows, certified
`O_H/C_sH/C_HH` pole rows, same-source W/Z response rows with identities and
covariance authority, scalar-LSZ moment/threshold/FV authority, or a
neutral-sector irreducibility certificate.
