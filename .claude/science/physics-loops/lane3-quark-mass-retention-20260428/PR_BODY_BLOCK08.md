# [physics-loop] Lane 3 quark mass retention block08: A1 source bridge no-go

## Scope

Stacked continuation from block07 for
`lane3-quark-mass-retention-20260428`.

This block attacks Lane 3 target 3C, generation-stratified quark Yukawa Ward
identities. It audits whether existing Koide A1 support faces already type the
quark `C3` source ratio. It does not claim retained non-top quark masses.

## Artifacts

- `docs/QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py`
- `logs/2026-04-28-quark-c3-a1-source-domain-bridge-no-go.txt`
- loop-pack updates under
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

The A1 algebra is exact on a `C3` circulant carrier:

```text
|q|^2/a^2 = 1/2
<=> Q = 2/3
<=> E_plus = E_perp.
```

Existing Koide support faces all hit the scalar `1/2`. The current typed-edge
inventory, however, has no path from those A1 support faces to the physical
quark `C3` Ward source ratio `|q_quark|^2/a_quark^2 = 1/2`. Adding exactly
that bridge creates the desired path, so the bridge is new theorem content,
not latent support.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
TOTAL: PASS=50, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_koide_q_bridge_single_primitive.py
PASSED: 10/10

PYTHONPATH=scripts python3 scripts/frontier_koide_a1_lie_theoretic_triple_match.py
PASSED: 10/10

PYTHONPATH=scripts python3 scripts/frontier_koide_circulant_character_bridge.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0
```

## Review Disposition

Review-loop emulation found the artifact honest as an exact current-bank
no-go / support boundary. It excludes observed quark masses, fitted Yukawa
entries, CKM mass input, charged-lepton A1 physical bridge import, and hidden
quark block-extremum assumptions.

## Remaining Blockers

- 3C: typed quark source-domain theorem for A1, alternate source ratio, or a
  P1/readout theorem plus sector phase and scale laws.
- 3A: non-perturbative `5/6` exponentiation plus threshold-local
  scale-selection / RG-covariant transport theorem.
- 3B: typed source-domain theorem or alternate readout primitive for the
  up-type scalar law.
