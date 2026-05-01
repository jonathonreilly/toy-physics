# Atomic QED Threshold Bridge Firewall

**Date:** 2026-05-01  
**Loop:** `lane2-atomic-scale-20260428`  
**Science block:** 01  
**Status:** branch-local exact negative boundary / support theorem for Lane 2 dependency accounting. This is not an atomic-scale framework prediction and not a retained Rydberg theorem.  
**Runner:** `scripts/frontier_atomic_qed_threshold_bridge_firewall.py`

## Question

Can the current repo determine the atomic low-energy Coulomb coupling
`alpha(0)` from:

```text
retained alpha_EM(M_Z) = 1/127.67
+ retained structural asymptotic b_QED = 32/3
```

without adding new charged-threshold or hadronic inputs?

## Result

No.

The repo now has a real structural QED-running ingredient:

```text
b_QED = (2/3)(N_color + 1)^2 = 32/3
```

on the retained charge/count surface. But this coefficient is explicitly an
asymptotic or above-threshold ingredient. It does not by itself determine the
low-energy zero-momentum coupling used in the Rydberg formula.

At one loop, running downward across an active interval changes the inverse
coupling as:

```text
1/alpha(Q_low)
  = 1/alpha(Q_high) + (b_active / 2 pi) log(Q_high / Q_low).
```

Thresholds decide the active intervals. With only the high-scale value and the
asymptotic coefficient, the threshold locations are unconstrained, so the
low-energy `1/alpha` is underdetermined.

## Theorem

**Theorem (Lane 2 QED threshold bridge firewall).** On the current Lane 2
surface, `alpha_EM(M_Z)` and the retained structural QED coefficient
`b_QED = 32/3` do not determine `alpha(0)`. A retained or exact-support
atomic `alpha(0)` bridge also requires a threshold-resolved QED transport
theorem, including charged thresholds and hadronic/vacuum-polarization
handling, or a proof that those threshold data are irrelevant at the target
status.

**Proof sketch.**

Fix the same high-scale inverse coupling `1/alpha_high = 127.67` and the same
asymptotic coefficient `b_QED = 32/3`. Consider three models that differ only
in effective active interval length over a dimensionless log interval of 10:

| Active interval | `1/alpha_low` |
|---:|---:|
| 0 | 127.670000 |
| 5 | 136.158264 |
| 10 | 144.646527 |

All three share the same high endpoint and the same asymptotic QED
coefficient. They differ only by threshold placement. Therefore the low-energy
coupling is not a function of `alpha(M_Z)` and `b_QED` alone.

This underdetermination proof does not use the observed `alpha(0)` or Rydberg
energy as an input.

## Physical-Scale Illustration

Using comparator-only values already standard on the repo surface:

```text
M_Z = 91.1876 GeV
m_e = 0.00051099895 GeV
1/alpha(0) comparator = 137.035999084
```

two invalid extremes bracket the comparator:

| Transport assumption | `1/alpha` |
|---|---:|
| no transport from `M_Z` | 127.670000 |
| all-threshold `b_QED = 32/3` active down to `m_e` | 148.198122 |
| comparator `alpha(0)` | 137.035999 |

The active log interval required to hit the comparator is an internal selector:

```text
log_active = 5.517029
effective threshold = 0.366371 GeV
```

That number is not derived by the current framework; it is what would be
chosen if the observed comparator were silently used to set an effective
threshold. This is exactly the hidden-fit failure mode the firewall is meant
to block.

## What This Retires

This retires the tempting upgrade:

```text
retained alpha_EM(M_Z) + retained b_QED
  => retained alpha(0)
  => retained Rydberg
```

The first implication is false without threshold-resolved QED transport.

## What Remains Open

Lane 2 still needs all three gates before Rydberg closure:

1. retained electron mass or charged-lepton activation law;
2. retained threshold-resolved `alpha_EM(M_Z) -> alpha(0)` transport, including
   charged thresholds and hadronic/vacuum-polarization handling;
3. retained physical-unit nonrelativistic Coulomb/Schrodinger limit.

This artifact improves the second gate by making the theorem prerequisite
more precise. It does not close the lane.

## Inputs And Import Roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `1/alpha_EM(M_Z)=127.67` | high-scale endpoint tested for transport | framework-derived | `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md` |
| retained charge spectrum `Q_u=2/3`, `Q_d=-1/3`, `Q_e=-1` | computes the asymptotic QED coefficient | retained support / exact structural | `docs/FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md`, `docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md` |
| `b_QED=32/3` | asymptotic QED running ingredient | retained/exact structural support | `docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md` |
| one-loop running form | proof bridge for threshold sensitivity | admitted standard QFT bridge | same convention used in the retained beta-coefficient note |
| `M_Z`, `m_e`, `alpha(0)` comparator | physical-scale illustration only | comparator / non-derivation context | existing repo conventions and standard physical labels |

No observed Rydberg value or `alpha(0)` value is used to derive a framework
quantity. Comparator values appear only after the abstract underdetermination
proof.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_atomic_qed_threshold_bridge_firewall.py
python3 -m py_compile scripts/frontier_atomic_qed_threshold_bridge_firewall.py
```

Expected:

```text
PASS=17 FAIL=0
```

## Safe Wording

Can claim:

- current Lane 2 has a sharper QED-running dependency firewall;
- retained structural `b_QED = 32/3` is necessary support, not an `alpha(0)`
  bridge;
- any retained Rydberg theorem must supply threshold-resolved QED transport.

Cannot claim:

- `alpha(0)` is derived;
- the Rydberg constant or hydrogen ground-state energy is retained;
- the existing hydrogen/helium scaffold is framework evidence;
- hadronic vacuum polarization or charged thresholds have been retired.
