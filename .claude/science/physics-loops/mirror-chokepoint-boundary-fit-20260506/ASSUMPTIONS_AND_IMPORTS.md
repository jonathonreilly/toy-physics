# Assumptions And Imports

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Dense boundary card: `NPL_HALF=60`, `connect_radius=5.0`, `layer2_prob=0.0`, `k=5.0`, 16 seeds | Defines the finite card being certified | admitted boundary condition | `docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`; certificate runner command | yes | yes | Keep as explicit finite-card scope; do not use as family theorem selector | disclosed |
| Mirror chokepoint generator and readout | Produces the finite rows | computed lattice input | `scripts/mirror_chokepoint_joint.py` | yes | yes | Replay from primary certificate runner | registered |
| Retention gates | Separate retained rows from wall before fitting | framework-local audit criterion | `scripts/mirror_chokepoint_boundary_fit_certificate.py` | yes | yes | Hard assertions in certificate runner | retired |
| Exponent fit | Descriptive summary after row retention | computed lattice input | primary certificate runner | yes, for fit only | yes | Recomputed from retained rows | retired |
| `N=120` wall | Bounds the finite card | computed lattice input | primary certificate runner | yes | yes | Hard zero-gravity assertion | retired |
| Any asymptotic/family law | Not part of claim | unsupported import if asserted | none | no | no | Excluded in note and certificate | blocked by scope |
