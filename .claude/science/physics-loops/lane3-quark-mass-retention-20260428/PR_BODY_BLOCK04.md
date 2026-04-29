# [physics-loop] Lane 3 quark mass retention block04: open scale boundary

## Scope

Stacked continuation from block03 for
`lane3-quark-mass-retention-20260428`.

This block attacks Lane 3 target 3A, the down-type `5/6` bridge, and records
an exact scale-selection boundary. It does not claim retained `m_d`, `m_s`,
`m_b`, or five-quark mass closure.

## Artifacts

- `docs/QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_five_sixths_scale_selection_boundary.py`
- `logs/2026-04-28-quark-five-sixths-scale-selection-boundary.txt`
- loop-pack updates under
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

Exact `SU(3)` still gives:

```text
C_F - T_F = 5/6.
```

The threshold-local comparator gives:

```text
p_self = log(|V_cb|_atlas) / log(m_s(2 GeV)/m_b(m_b))
       = 0.832890...
```

which is close to `5/6 = 0.833333...`.

The common-scale comparator gives:

```text
p_same = log(|V_cb|_atlas) / log(m_s(m_b)/m_b(m_b))
       = 0.803802...
```

and the same fixed `5/6` prediction misses that surface by `+14.98%`.
Therefore the exact Casimir rational is not a scale-selection theorem.
Retained 3A still requires non-perturbative exponentiation plus
threshold-local scale selection or an RG-covariant transport theorem.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_five_sixths_scale_selection_boundary.py
TOTAL: PASS=34, FAIL=0

python3 -m py_compile scripts/frontier_quark_five_sixths_scale_selection_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_ckm_five_sixths_bridge_support.py
EXACT PASS=5, BOUNDED PASS=7, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_mass_ratios_taste_staircase_support.py
TOTAL: PASS=55, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0
```

## Review Disposition

Review-loop emulation found the artifact honest as an exact negative boundary
/ theorem-target isolation. Comparator values and one-loop transport remain
comparator/admitted-convention context, not proof inputs. Claim status remains
`open`.

## Remaining Blockers

- 3A: non-perturbative `5/6` exponentiation plus threshold-local
  scale-selection / RG-covariant transport theorem.
- 3B: typed source-domain theorem or alternate readout primitive for the
  up-type scalar law.
- 3C: species-differentiated non-top Yukawa Ward primitive.
