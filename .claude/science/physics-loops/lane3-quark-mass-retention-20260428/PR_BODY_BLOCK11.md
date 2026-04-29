# [physics-loop] Lane 3 quark mass retention block11: RPSR readout underdetermination

## Summary

Block 11 continues the Lane 3 3B RPSR route from block 10.

Block 10 established exact retained support for the reduced RPSR up-amplitude:

```text
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42))) = 0.7748865611...
```

This block tests the next load-bearing step: whether that single scalar plus
top-scale normalization can determine both physical up-type ratios
`y_u/y_c` and `y_c/y_t`.

## Artifacts

- `docs/QUARK_RPSR_SINGLE_SCALAR_READOUT_UNDERDETERMINATION_NOTE_2026-04-28.md`
- `scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py`
- `logs/2026-04-28-quark-rpsr-single-scalar-readout-underdetermination.txt`
- loop-pack updates under `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

The exact RPSR scalar remains valuable support, but a single scalar does not
determine a two-ratio up-type Yukawa readout.

Within the admissible scale-covariant power class:

```text
R_{p,q}(a_u; y_t) = y_t * (a_u^(p+q), a_u^q, 1),
```

the same exact `a_u` supports a continuum of ordered ratio pairs:

```text
y_u/y_c = a_u^p,
y_c/y_t = a_u^q.
```

Choosing `p` and `q`, or an equivalent pair of readout functions and
generation-gap assignment, is new theorem content. The block does not claim
retained `m_u`, `m_c`, `m_u/m_c`, or `m_c/m_t`.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
TOTAL: PASS=80, FAIL=0

python3 -m py_compile scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
TOTAL: PASS=50, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_conditional.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0
```

## Honest Claim Status

Lane 3 remains open.

This block closes the shortcut:

```text
RPSR reduced amplitude a_u
+ top Ward scale
=> retained up-type ratio pair.
```

The next hard residual is a derived two-ratio readout law, generation/source
assignment, and top-compatible sector/scale bridge.
