# YT PR230 Same-Source EW/Higgs Action Ansatz Gate Note

Status: conditional support only.  No top-Yukawa closure proposal is
authorized.

This block records the cleanest action-first candidate without promoting it to
the current PR230 authority surface.  The runner
`scripts/frontier_yt_pr230_same_source_ew_higgs_action_ansatz_gate.py` defines
a concrete lattice action-extension shape:

- keep the existing PR230 top FH/LSZ scalar source coordinate `s`;
- add dynamic `SU(2)_L`, `U(1)_Y`, and Higgs-doublet fields on the same
  lattice sites;
- couple the same scalar source to the centered gauge-invariant composite
  `O_H = Phi^dagger Phi - <Phi^dagger Phi>`;
- check that `dS/ds` contains `sum_x O_H(x)`;
- check the local FMS expansion
  `Phi^dagger Phi - v^2/2 = v h + (h^2 + pi^2)/2`.

The output certificate is
`outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json`
with `PASS=15 FAIL=0`.

The block intentionally does not write any accepted future certificate path:

- `outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json`;
- `outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json`;
- `outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json`;
- `outputs/yt_top_wz_matched_response_rows_2026-05-04.json`.

Claim boundary:

- The ansatz is not an adopted PR230 same-surface action.
- It does not supply canonical `O_H` authority on the actual current surface.
- It does not supply `C_sH/C_HH` pole rows, W/Z response rows, Gram purity,
  scalar-LSZ/FV/IR authority, matching/running authority, or `kappa_s = 1`.
- It does not use `H_unit`, `yt_ward_identity`, observed masses/couplings,
  `alpha_LM`, plaquette, `u0`, reduced pilots, or unit `c2`/`Z_match`/`kappa_s`
  as proof inputs.

Exact next action:

Either promote this ansatz through a same-surface adoption theorem and then
produce canonical `O_H/C_sH/C_HH` pole rows, or implement genuine same-source
W/Z response rows with identity, covariance, strict non-observed `g2`, and
`delta_perp` authority.
