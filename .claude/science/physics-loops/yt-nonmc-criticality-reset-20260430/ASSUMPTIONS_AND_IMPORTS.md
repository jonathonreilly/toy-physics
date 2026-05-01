# Assumptions And Imports

| Item | Role | Status | Notes |
|---|---|---|---|
| `lambda(M_Pl)=0` | Higgs high-scale boundary | framework Higgs input | Already used by the Higgs runner. |
| `beta_lambda(M_Pl)=0` | new selector | open import | Decisive unresolved premise. |
| `g_1(v)=0.464`, `g_2(v)=0.648` | gauge boundary inputs | imported framework values | Must remain separately audited. |
| `alpha_s(v)=0.1033` | gauge boundary input | imported framework value | Used only as gauge input, not through a YT Ward identity. |
| SM RGE to 3-loop | running bridge | external/theory bridge | Reuses `frontier_higgs_mass_full_3loop.py`. |
| accepted `y_t(v)=0.9176` | comparator | not proof input | Used only after the boundary solve. |
| observed `m_H=125.25 GeV` | comparator | not proof input | Used only after the boundary solve. |
| top pole mass | comparator | not proof input | Pole conversion is not claimed as closed. |

Forbidden proof inputs:

- `H_unit` matrix element;
- old `yt_ward_identity_derivation_theorem`;
- `y_t_bare`;
- observed top mass target;
- `y_t/g_s=1/sqrt(6)` as a defining condition.

