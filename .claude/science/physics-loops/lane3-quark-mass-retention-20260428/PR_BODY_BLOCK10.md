# [physics-loop] Lane 3 quark mass retention block10: RPSR mass boundary

## Scope

Stacked continuation from block09 for
`lane3-quark-mass-retention-20260428`.

This block attacks Lane 3 target 3B. It records the existing STRC/RPSR
up-amplitude theorem as exact support, and separates it from retained
up-quark mass closure.

## Artifacts

- `docs/QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py`
- `logs/2026-04-28-quark-up-amplitude-rpsr-mass-retention-boundary.txt`
- loop-pack updates under
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

STRC/RPSR gives an exact retained reduced amplitude:

```text
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42))) = 0.7748865611...
```

This is valuable 3B support, but it is not retained `m_u/m_c`, `m_c/m_t`, or
absolute non-top mass closure. The missing item is a typed
amplitude-to-Yukawa readout theorem plus a sector/scale bridge compatible with
the top Ward anchor.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
TOTAL: PASS=50, FAIL=0

python3 -m py_compile scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_strc_lo_collinearity_theorem.py
PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_conditional.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_projector_parameter_audit.py
TOTAL: PASS=6, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py
PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0
```

## Review Disposition

Review-loop emulation found the artifact honest as exact 3B support/boundary,
not retained non-top quark mass closure. It excludes observed quark masses,
fitted Yukawa entries, CKM mass input, amplitude-as-mass shortcut, and
species-uniform top Ward import.

## Remaining Blockers

- 3B: amplitude-to-Yukawa readout theorem and sector/scale bridge.
- 3C: source/readout theorem for generation-stratified Ward identities.
- 3A: non-perturbative `5/6` exponentiation plus threshold-local
  scale-selection / RG-covariant transport theorem.
