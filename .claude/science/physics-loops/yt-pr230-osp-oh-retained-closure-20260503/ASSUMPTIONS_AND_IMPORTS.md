# Assumptions And Imports

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Cl(3)/Z3 substrate and uniform scalar source `s` | Defines `O_s` and source functional | zero-input structural | `MINIMAL_AXIOMS_2026-04-11.md`, PR230 harness | yes | yes | none needed | allowed |
| Legendre/LSZ `O_sp` | Normalized source-pole operator | exact support | `YT_LEGENDRE_SOURCE_POLE_OPERATOR_CONSTRUCTION_NOTE_2026-05-03.md` | yes | yes | already derived | support only, not `O_H` |
| Canonical Higgs radial `O_H` | Physical field whose VEV defines `v` | unsupported bridge on PR230 surface | EW/Higgs notes after `H` supplied | yes | yes | source-Higgs Gram purity, W/Z response, or rank-one theorem | open blocker |
| `O_sp/O_H` overlap | Converts source-pole readout to physical `y_t` | unsupported import if assumed | no accepted certificate | yes | yes | derive identity or measure overlap | open blocker |
| Taste-scalar isotropy | Scalar/taste support | retained/exact support | `TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md` | no, not enough | no by itself | use as support only | does not select source axis |
| One-Higgs gauge monomial selection | SM operator pattern after `H` supplied | exact support | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | no, not enough | no by itself | use after `O_H` exists | does not prove source-pole purity |
| `H_unit` matrix-element readout | Tempting shortcut | audited_renaming / forbidden | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md` audit | no | no | none | forbidden |
| Observed `m_t` / `y_t` | Comparator | observational comparator | PDG / external | no | no | comparator only | forbidden as selector |
| `kappa_s = 1`, `cos(theta)=1` | Would close bridge by assertion | unsupported import | none | yes if assumed | yes | derive or measure | forbidden unless derived |
