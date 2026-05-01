# Lane 2 No-Go Ledger

**Updated:** 2026-05-01T10:53:48Z  
**Loop:** `lane2-atomic-scale-20260428`

| Route | Prior / current artifact | Verdict | Why it is blocked | Reopen condition |
|---|---|---|---|---|
| Directly substitute `alpha_EM(M_Z)` for atomic `alpha(0)` in the hydrogen formula | `docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`, `scripts/frontier_atomic_rydberg_dependency_firewall.py` | no-go / exact negative boundary | With textbook `m_e`, direct substitution gives `E_1 = -15.68 eV`, about 15% away from the Rydberg value; alpha transport is load-bearing. | Provide retained alpha(M_Z) -> alpha(0) transport or a retained low-energy Coulomb coupling. |
| Treat the standard-QM hydrogen/helium scaffold as framework evidence | `docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` | no-go for retained closure | The harness imports textbook `m_e`, `e`, `hbar`, Coulomb Hamiltonian, and physical units. | Substitute retained framework inputs and prove the physical-unit nonrelativistic limit. |
| Promote Lane 2 through Lane 6 electron-mass closure during this run | User collision-avoidance constraint | out of scope | Lane 6/Koide/V0 is active elsewhere and must not be worked here. | Only record dependency; do not modify Lane 6 artifacts or branches. |
| Use asymptotic gauge beta coefficients as a complete low-energy atomic bridge | Candidate under test in this block | suspected no-go | `b_QED` is above-threshold structural support; alpha(0) needs threshold-resolved decoupling and charged-mass/hadronic inputs. | A runner/note must show either a retained threshold theorem or exact insensitivity to missing thresholds. |
| Promote `alpha_EM(M_Z) + b_QED=32/3` to `alpha(0)` | `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_QED_THRESHOLD_BRIDGE_FIREWALL_NOTE_2026-05-01.md`, `scripts/frontier_atomic_qed_threshold_bridge_firewall.py` | no-go / exact negative boundary | The same high endpoint and same asymptotic coefficient yield different low-energy inverse couplings when threshold placement changes; comparator `alpha(0)` can be hit only by choosing a hidden effective threshold. | Provide retained threshold-resolved QED transport or prove threshold insensitivity at the target status. |
