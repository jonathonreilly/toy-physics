## Summary

Science block 01 for `lane2-atomic-scale-20260428` packages Lane 2 atomic-scale work as open with exact support/no-go boundaries. It does not claim retained Rydberg or atomic-scale closure.

The block separates scaffold success from retained closure and adds six branch-local artifacts:

- QED threshold bridge firewall: `alpha_EM(M_Z) + b_QED=32/3` does not determine `alpha(0)`.
- NR Coulomb scale bridge: the dimensionless lattice companion maps to the Bohr formula only after `mu`, `alpha(0)`, and a physical unit map are supplied.
- Rydberg gate factorization and stuck fan-out: current routes preserve independent mass, coupling, and unit/kinetic gates.
- Planck-unit map firewall: Planck/source-unit support is not an atomic coupling/unit-map closure.
- `alpha(0)` threshold-moment no-go: retained weights and `b_QED` do not fix `T_EM` or finite/hadronic matching.
- Massive NR kinetic bridge: Lorentz/dispersion support gives `p^2/(2m)` only after a retained massive one-particle sector and mass are supplied.

## Review Links

- Handoff: `.claude/science/physics-loops/lane2-atomic-scale-20260428/HANDOFF.md`
- State: `.claude/science/physics-loops/lane2-atomic-scale-20260428/STATE.yaml`
- Review history: `.claude/science/physics-loops/lane2-atomic-scale-20260428/REVIEW_HISTORY.md`
- Assumptions/imports: `.claude/science/physics-loops/lane2-atomic-scale-20260428/ASSUMPTIONS_AND_IMPORTS.md`
- No-go ledger: `.claude/science/physics-loops/lane2-atomic-scale-20260428/NO_GO_LEDGER.md`
- Route portfolio: `.claude/science/physics-loops/lane2-atomic-scale-20260428/ROUTE_PORTFOLIO.md`

## Runners And Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_atomic_qed_threshold_bridge_firewall.py -> PASS=17 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_atomic_nr_coulomb_scale_bridge.py -> SUMMARY: PASS=42 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_atomic_rydberg_gate_factorization_fanout.py -> PASS=43 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_atomic_planck_unit_firewall.py -> SUMMARY: PASS=31 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_atomic_alpha0_threshold_moment_no_go.py -> SUMMARY: PASS=25 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_atomic_massive_nr_limit_bridge.py -> SUMMARY: PASS=22 FAIL=0
python3 -m py_compile scripts/frontier_atomic_massive_nr_limit_bridge.py -> pass
python3 -c 'import pathlib, yaml; yaml.safe_load(pathlib.Path(".claude/science/physics-loops/lane2-atomic-scale-20260428/STATE.yaml").read_text()); print("STATE.yaml ok")' -> STATE.yaml ok
git diff --check -> pass
```

## Imports Exposed

- Retained electron mass / reduced mass.
- Retained low-energy `alpha(0)`.
- Threshold moment `T_EM = sum_f N_c Q_f^2 log(M_Z/m_f^eff)`.
- Finite/hadronic matching for `alpha(0)` transport.
- Framework-native physical unit map and low-energy Schrodinger/Coulomb sector.
- Retained Coulomb potential/coupling in the same low-energy one-particle sector.

## Remaining Blockers

Lane 2 remains open/scaffold-only. Future retained closure needs independent retained premises for the mass/reduced-mass gate, `alpha(0)` threshold/matching gate, and physical-unit Schrodinger/Coulomb gate. No Lane 4 or Lane 6 work was performed in this block.
