# PR230 Block69 Strict K-Prime Pole-Residue Certificate

```yaml
actual_current_surface_status: open / strict K-prime pole-residue certificate rows missing
status: missing_rows
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_pr230_block69_strict_kprime_pole_residue_certificate_builder.py`  
**Certificate:** `outputs/yt_pr230_strict_kprime_pole_residue_certificate_2026-05-12.json`

## Purpose

This Block69 artifact is the strict positive path for the Schur/Feshbach
`K'(pole)` residue route.  It tries to build the source-pole residue
certificate from an explicit same-surface row artifact, not from finite-shell
source-only correlator rows.

The accepted row artifact must provide the pole coordinate and pole-fit window,
the source projection numerator, Schur/Feshbach `A/B/C` rows or an exactly
signed transfer-kernel derivative row, finite-volume/IR/contact-term checks,
and explicit false fields for the forbidden-import firewall.

## Theorem Boundary

For a certified source/orthogonal neutral scalar partition

```text
K(x) = [[A(x), B(x)^T],
        [B(x), C(x)]],
```

the same-source denominator after eliminating the orthogonal block is

```text
D_eff(x) = A(x) - B(x)^T C(x)^-1 B(x).
```

The pole residue is then strict-support computable from

```text
Res C_ss(pole) = N_source(pole) / D_eff'(pole),
```

where `N_source(pole)` is the source row/projection numerator.  For one
orthogonal direction,

```text
D_eff'(pole) =
  A'(pole)
  - 2 B(pole) B'(pole) / C(pole)
  + B(pole)^2 C'(pole) / C(pole)^2.
```

The runner also accepts the equivalent precontracted matrix form or a
transfer-kernel row `<l,K'(pole)r>` only when the denominator derivative sign
convention is emitted explicitly.

## Current Result

Running the builder produces:

```bash
python3 scripts/frontier_yt_pr230_block69_strict_kprime_pole_residue_certificate_builder.py
# status: missing_rows
# SUMMARY: PASS=3 FAIL=0
```

No accepted strict row artifact exists at the explicit Block69 paths, including
`outputs/yt_schur_scalar_kernel_rows_2026-05-03.json`.  The certificate records
the finite-shell polefit8x8 diagnostic pole only as non-strict context; it is
not used as `K'(pole)` evidence.

## Required Emissions

The next chunk/combiner/theorem emission must provide one accepted strict row
artifact with:

- `pole_coordinate` and `pole_fit_window` with provenance;
- `source_projection_numerator_interval`;
- either `A/B/C` pole rows and derivatives, precontracted Schur rows, or a
  signed `<l,K'(pole)r>` denominator-derivative equivalent;
- `finite_volume_passed`, `ir_zero_mode_order_passed`,
  `contact_terms_subtracted_or_bounded`, and
  `model_class_or_analytic_continuation_passed`;
- explicit `false` firewall fields for `H_unit`, `yt_ward_identity`,
  `y_t_bare`, `alpha_LM`, plaquette/u0, observed target selectors, and alias
  imports.

Until those rows exist, this route remains open and no proposed retained-status
wording is authorized by this artifact.
