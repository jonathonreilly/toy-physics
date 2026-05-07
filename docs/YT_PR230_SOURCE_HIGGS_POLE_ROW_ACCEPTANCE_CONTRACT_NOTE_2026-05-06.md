# PR #230 Source-Higgs Pole-Row Acceptance Contract Note

Status: open / strict acceptance contract only; proposal_allowed=false.

This note defines the landing pad for the missing PR #230 bridge.  The accepted
future artifact must be a same-surface canonical-Higgs pole-row certificate
containing `C_ss/C_sH/C_HH` residues, uncertainties, Gram purity, isolated-pole
control, FV/IR control, scalar-LSZ/model-class authority, and a clean
forbidden-input firewall.

Current status: the strict row file is absent.  The existing taste-radial row
campaign emits `C_sx/C_xx` support rows and alias metadata; those rows are not
canonical-Higgs `C_sH/C_HH` pole rows and do not determine source-Higgs overlap.
The FMS composite expansion gives a useful conditional operator form, but it
does not by itself supply `Res C_sH` or exclude orthogonal neutral top
couplings.

Verifier:

```bash
python3 scripts/frontier_yt_pr230_source_higgs_pole_row_acceptance_contract.py
```

Output:

```text
outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json
```

The contract rejects closure unless all of the following are present:

- Same-surface canonical `O_H` identity and normalization certificate.
- Same-ensemble pole rows with `Res_C_ss`, `Res_C_sH`, and `Res_C_HH` plus
  uncertainties.
- No `C_sx/C_xx` aliasing in the accepted row labels.
- Gram purity/positivity with uncertainty control.
- Isolated scalar pole, FV/IR, and scalar-LSZ/model-class certificates.
- No `H_unit`, `yt_ward_identity`, observed selector, `alpha_LM`,
  plaquette/`u0`, `kappa_s=1`, `c2=1`, or `Z_match=1` shortcut.
