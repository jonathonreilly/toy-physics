# Assumptions And Imports

| Item | Role | Current status | Notes |
|---|---|---|---|
| `Cl(3)/Z^3` substrate | base surface | accepted framework input | Fixed lattice, not a continuum family by default. |
| `lambda(M_Pl)=0` | Higgs boundary | existing framework authority | Not enough to force beta stationarity. |
| `beta_lambda(M_Pl)=0` | needed selector | open import | Decisive unresolved premise for non-MC criticality closure. |
| SM RGE bridge | running machinery | external/bridge | Needed to run Planck boundary data to `v`. |
| Observed `y_t`, `m_t`, `m_H` | comparators | not proof inputs | Must remain after-the-fact checks only. |
| Old `H_unit` Ward route | forbidden for PR #230 proof | audited_renaming trap | Must not be used as load-bearing input. |
| Direct MC production data | measurement evidence | absent | Strict runner cannot pass without this data. |
| Top mass parameter pin | derivational evidence | absent | A tuned mass is a calibrated readout, not a derivation. |

Current exact obstruction:

```text
beta_lambda^(1)|_{lambda=0}
  = -6 y_t^4 + (3/8) [2 g_2^4 + (g_2^2 + g'^2)^2].
```

This is not identically zero.  It requires a new relation among `y_t`, `g_1`,
and `g_2`.
