# Handoff

The PR #230 direct-correlator path remains honest but computationally too
large for quick closure.  The new route to pursue is Planck double-criticality:

```text
lambda(M_Pl)=0
beta_lambda(M_Pl)=0
```

The runner solves the resulting boundary-value problem and gets:

```text
y_t(v) = 0.9208739295
m_H    = 126.333488 GeV
```

These are comparators, not fitted targets.  The solve uses gauge inputs and
the RGE bridge, not the top mass, not `H_unit`, and not `y_t/g_s=1/sqrt(6)`.

The exact next hard problem is to prove or rule out:

```text
Cl(3)/Z^3 Planck boundary stationarity => beta_lambda(M_Pl)=0
```

If that implication is proved, this route becomes a plausible non-MC
replacement candidate for the month-scale production lattice campaign.  If it
fails, the result should be recorded as a bounded no-go for the criticality
selector.

