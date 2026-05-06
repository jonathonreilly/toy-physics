# PR230 Schur Route Completion

**Status:** exact negative boundary / strict Schur `A/B/C` route not complete;
bounded two-source correlator subblock, finite inverse A/B/C rows,
finite-shell inverse-slope support, and finite-to-pole lift boundary present
**Runner:** `scripts/frontier_yt_pr230_schur_route_completion.py`
**Certificate:** `outputs/yt_pr230_schur_route_completion_2026-05-06.json`

The Schur route is real hard-physics support: if a same-surface neutral scalar
kernel basis and block rows `A`, `B`, `C` plus derivatives are supplied, the
Schur-complement formula computes the source-pole denominator derivative.

Current PR230 now has a bounded two-source correlator subblock witness from the
completed taste-radial rows:
`outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json`.
That witness is not source-only data: it packages finite `C_ss/C_sx/C_xx` rows
for the certified source/complement chart.  It is still not the strict Schur
kernel packet because it has no pole derivatives, isolated-pole/FV/IR
authority, canonical `O_H`, or source-overlap bridge.

The finite Schur A/B/C row certificate adds an explicit inverse-block row
artifact from the same measured subblocks:
`outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json`.
It computes `K(q)=G(q)^(-1)` and records finite `A_f=K_ss`, `B_f=K_sx`, and
`C_f=K_xx` rows with chunk-level inverse-identity checks.  These rows are
still finite inverse-correlator-block rows, not strict neutral-kernel A/B/C
pole rows.

The finite-shell K-prime scout adds the companion bounded diagnostic from the
same rows:
`outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json`.
It inverts the finite 2x2 correlator block and compares the zero mode with the
first nonzero momentum shell.  This supplies a real finite-shell inverse-slope
diagnostic, but it is not an isolated-pole `K'(pole)` derivative.

The finite-to-pole lift gate closes the endpoint-promotion shortcut:
`outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json`.
It proves that two finite endpoint values do not determine the pole derivative:
`f_lambda(x)=f(0)+((f(dp)-f(0))/dp)x+lambda x(x-dp)` preserves both finite
endpoint values while changing `f_lambda'(0)`.  Thus finite `A_f/B_f/C_f`
rows and endpoint secants cannot become strict `K'(pole)` authority without
model-class, pole, and FV/IR authority.

Existing artifacts also prove sufficiency and reject source-only shortcuts,
compressed-denominator bootstraps, finite ladder row extraction, and
outside-math row naming as physical authority.

This is a current-surface boundary only.  The route reopens with a neutral
kernel basis certificate plus Schur `A/B/C` rows or an equivalent theorem.

```bash
python3 scripts/frontier_yt_pr230_schur_route_completion.py
# SUMMARY: PASS=15 FAIL=0
```
