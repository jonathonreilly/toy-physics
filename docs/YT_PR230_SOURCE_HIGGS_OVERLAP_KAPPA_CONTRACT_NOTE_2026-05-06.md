# PR230 Source-Higgs Overlap/Kappa Contract

**Status:** exact-support / source-Higgs overlap-kappa row contract; current row packet absent

This block makes the remaining source-to-canonical-Higgs normalization object
explicit.  It does not close PR #230.

The genuine source-pole artifact already fixes the source side:

```text
O_sp = O_s / sqrt(Res C_ss) = sqrt(Dprime_ss at pole) O_s
Res C_sp,sp = 1
```

If a future same-surface certified Higgs operator supplies pole rows
`Res C_ss`, `Res C_sH`, and `Res C_HH` at the same nondegenerate isolated
scalar pole, then the source-Higgs overlap is

```text
kappa_spH = Res(C_sp,H) / sqrt(Res(C_HH))
           = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH)).
```

This is the measured overlap coefficient.  It is not the forbidden shortcut
`kappa_s = 1`.  In the pure one-pole case, `|kappa_spH| = 1` and the
`O_sp`-Higgs Gram determinant vanishes.  If `|kappa_spH| < 1`, the source-pole
response can still be held fixed while the canonical Higgs Yukawa changes by
adjusting an orthogonal neutral coupling.  Therefore source-only rows, FMS
`C_HH` support, and `C_sx/C_xx` taste-radial chunks still do not determine
canonical `y_t`.

The executable runner is
`scripts/frontier_yt_pr230_source_higgs_overlap_kappa_contract.py`; it writes
`outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json` with
`PASS=13 FAIL=0`.

Current blockers remain:

- no same-surface certified canonical `O_H` row packet;
- no production `C_sH/C_HH` pole residues;
- the `O_sp`-Higgs Gram postprocessor is awaiting production rows;
- the full retained/campaign gates still have `proposal_allowed=false`.

No closure claim is made.  The next exact action is to produce a same-surface
certified `O_H/C_sH/C_HH` pole-row packet, compute `kappa_spH` from the
normalized cross residue, then rerun the source-Higgs builder, Gram
postprocessor, full assembly, retained-route, and campaign gates.
