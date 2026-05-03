# Source-Higgs Cross-Correlator Harness Extension

**Status:** bounded-support / harness instrumentation
**Runner:** `scripts/frontier_yt_source_higgs_cross_correlator_harness_extension.py`
**Certificate:** `outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json`

## Purpose

PR #230's selected retention route needs same-ensemble source-Higgs pole data:

```text
C_ss(q), C_sH(q), C_HH(q)
```

The production harness now has an optional, default-off measurement path for
those finite-mode rows.  It requires a separate source-Higgs operator
certificate through `--source-higgs-operator-certificate`; without that
certificate the harness remains guarded and emits no `C_sH/C_HH` rows.

## Harness Surface

The new flags are:

- `--source-higgs-cross-modes`
- `--source-higgs-cross-noises`
- `--source-higgs-operator-certificate`

The estimator measures diagonal-vertex stochastic traces on the same gauge
ensemble:

```text
C_AB(q) = Tr[S V_A(q) S V_B(-q)]
```

for `A,B` in `{source, H}`.  The resulting finite-mode rows are stored under
`source_higgs_cross_correlator_analysis` in each ensemble artifact.

## Claim Boundary

This is not retained closure.  The harness does not prove that the supplied
operator is canonical `O_H`; that burden remains on the operator certificate
and audit.  Finite-mode rows are also not pole residues.  Positive retention
still requires isolated-pole residues, Gram purity, FV/IR/zero-mode control,
and retained-route authorization.

The extension does not use `H_unit`, static EW algebra, observed targets,
`yt_ward_identity`, `alpha_LM`, plaquette, or `u0`, and does not set
`kappa_s = 1` or `cos(theta) = 1`.

## Next Action

Supply or derive an audit-acceptable canonical-Higgs operator certificate, run
the harness with source-Higgs modes/noises, then build pole-residue rows for
the source-Higgs certificate builder and Gram-purity postprocessor.
