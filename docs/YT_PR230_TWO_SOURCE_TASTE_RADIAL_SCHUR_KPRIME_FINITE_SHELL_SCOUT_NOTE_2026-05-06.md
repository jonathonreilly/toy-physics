# PR230 Two-Source Taste-Radial Schur K-Prime Finite-Shell Scout

**Status:** bounded-support / finite-shell Schur inverse-slope scout from
two-source taste-radial rows; strict `K'(pole)` authority absent
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout.py`
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json`

The completed chunks001-026 contain finite rows for the certified
source/complement block

```text
G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]
```

This scout inverts that measured 2x2 finite correlator block and compares the
zero mode with the first nonzero momentum shell.  For the source-given-
complement inverse preview it computes

```text
Delta_sx = C_ss C_xx - C_sx^2
K_{s|x}(q) = C_xx(q) / Delta_sx(q)
dK_{s|x}/d p_hat^2 ~= (K_shell - K_0) / (p_hat^2_shell - p_hat^2_0)
```

On chunks001-026, the finite-shell `K_{s|x}` slope is finite across all ready
chunks.  The certificate records the chunk-level rows and summary statistics.

This is not closure.  A zero-to-first-shell finite difference is not an
isolated-pole `K'(pole)` derivative.  The scout writes no strict Schur A/B/C
kernel rows, supplies no pole location, no FV/IR/zero-mode limiting authority,
no canonical `O_H` identity, and no `kappa_s`.

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout.py
# SUMMARY: PASS=14 FAIL=0
```
