# Atomic Rydberg Gate Factorization Fan-Out

**Date:** 2026-05-01
**Loop:** `lane2-atomic-scale-20260428`
**Science block:** 01
**Status:** exact boundary/support packet for Lane 2 dependency
factorization and stuck fan-out. This is not retained Rydberg closure.
**Runner:** `scripts/frontier_atomic_rydberg_gate_factorization_fanout.py`
**Log:** `.claude/science/physics-loops/lane2-atomic-scale-20260428/logs/atomic_rydberg_gate_factorization_fanout_2026-05-01.log`

## Question

After the QED-threshold firewall and the nonrelativistic Coulomb scale bridge,
does any non-overlapping Lane 2 route close retained atomic/Rydberg scale from
current repo primitives?

## Result

No.

The current branch can honestly state an exact gate-factorization result:
retained Rydberg closure currently requires three independent gates, not one
implicit substitution:

1. retained electron/reduced mass `mu`;
2. retained low-energy Coulomb coupling `alpha(0)`, or threshold-resolved QED
   transport from retained `alpha_EM(M_Z)`;
3. retained framework-native physical-unit nonrelativistic
   Coulomb/Schrodinger map, including the kinetic normalization and length-time
   unit bridge.

The existing scaffold and the new branch-local bridges sharpen the map, but
they do not supply those gates. Lane 2 remains open/scaffold-only.

## Theorem

**Theorem (Lane 2 Rydberg gate factorization).** On the current Lane 2 surface,
including the standard-QM atomic scaffold, the retained high-scale
`alpha_EM(M_Z)` value, the retained structural `b_QED = 32/3` ingredient, the
QED threshold firewall, and the branch-local NR Coulomb scale bridge, a retained
Rydberg claim is blocked unless the branch also supplies retained versions of:

```text
mu / m_e,
alpha(0) or threshold-resolved alpha_EM(M_Z) -> alpha(0) transport,
framework-native physical unit / kinetic normalization map.
```

The proof is by factorization:

```text
E_n = -mu (Z alpha)^2 / (2 n^2)
```

after the physical unit map is admitted, while without that map the
dimensionless companion gives:

```text
lambda_n = -g^2 / (4 n^2),
E_n = lambda_n / (2 mu a^2).
```

Thus `mu`, `alpha(0)`, and the physical map are all load-bearing. A single
Rydberg-scale number constrains only the product `mu alpha^2` after the
standard map has already been supplied; it does not derive the gates.

## Stuck Fan-Out Synthesis

| Frame | Attempt | Result | Next prerequisite |
|---|---|---|---|
| Minimal Coulomb algebra | Factor `E_n = -mu (Z alpha)^2/(2 n^2)` from synthetic inputs | Energy fixes only `mu alpha^2`; `mu` and `alpha` remain separate retained gates | retained `mu/m_e` and retained `alpha(0)` |
| QED running bridge | Use retained `alpha_EM(M_Z)` and `b_QED=32/3` | Same high endpoint and same `b_QED` yield different low-energy couplings under different threshold placements | threshold-resolved QED decoupling with charged thresholds and hadronic handling |
| Charged-lepton mass gate | Treat `m_e` as available to the atomic scaffold | `m_e` is absent from Lane 2 and Lane 6 work is out of scope here | reviewed Lane 6 electron-mass retention or explicit comparator-only admission |
| Physical-unit kinetic map | Map `H_g=-Delta_x-g/r` to physical units | Exact conditional map works only after `a=g/(2 mu Z alpha)` is supplied | retained kinetic normalization / unit theorem |
| Scaffold falsifier | Compare scaffold success to direct high-scale-alpha substitution | Scaffold succeeds with textbook inputs; direct `alpha_EM(M_Z)` misses by order 15 percent | substitute retained upstream gates only after they exist |

No frame supports retained Rydberg closure on current inputs. The strongest
honest movement is exact support for the dependency factorization.

## Comparator-Only Checks

The runner prints textbook constants only after the synthetic theorem checks.
They illustrate the load-bearing nature of hidden fits:

```text
direct alpha_EM(M_Z) substitution shifts E_1 by +15.21%
using alpha_EM(M_Z) would require a hidden m_e shift of -13.20%
the alpha(0) comparator can be hit by choosing an effective threshold
```

These are falsifier/comparator checks, not derivation inputs.

## Claim Boundary

Can claim:

- exact branch-local gate factorization for current Lane 2 Rydberg closure;
- stuck fan-out across five non-overlapping attack frames;
- scaffold success is sharply separated from retained Rydberg closure;
- the next theorem prerequisites are explicit and reviewable.

Cannot claim:

- retained Rydberg constant;
- retained `alpha(0)`;
- retained electron/reduced mass;
- retained physical-unit Schrodinger/Coulomb limit;
- Lamb shift, fine structure, hyperfine, helium, or larger-atom closure.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_atomic_rydberg_gate_factorization_fanout.py
python3 -m py_compile scripts/frontier_atomic_rydberg_gate_factorization_fanout.py
PYTHONPATH=scripts python3 scripts/frontier_atomic_rydberg_dependency_firewall.py
PYTHONPATH=scripts python3 scripts/frontier_atomic_qed_threshold_bridge_firewall.py
PYTHONPATH=scripts python3 scripts/frontier_atomic_nr_coulomb_scale_bridge.py
```

Observed branch-local result:

```text
frontier_atomic_rydberg_gate_factorization_fanout.py -> PASS=43 FAIL=0
```

## Import Roles

| Input | Role | Import class | Disposition |
|---|---|---|---|
| `alpha_EM(M_Z)=1/127.67` | high-scale endpoint for running attempts | framework-derived high-scale input | usable only with a QED transport bridge |
| `b_QED=32/3` | asymptotic QED running ingredient | retained/exact structural support | not sufficient for `alpha(0)` |
| textbook `m_e`, `alpha(0)`, Rydberg value | comparator/falsifier checks | observational comparator / standard context | not used as derivation inputs |
| `E_n=-mu(Z alpha)^2/(2n^2)` | downstream Coulomb spectrum bridge | admitted standard bridge / exact support context | requires retained gates before closure |
| `a=g/(2 mu Z alpha)` | physical unit map in the scale bridge | admitted map in branch-local support theorem | open as framework-native retained theorem |

## Next Exact Action

The next non-overlapping route should target one gate at a time:

1. prove a narrow framework-native kinetic/unit-map theorem, if current action
   surfaces contain enough structure; or
2. prove a sharper no-go that threshold-resolved `alpha(0)` transport cannot
   be retained from current Lane 2 primitives without upstream charged-mass and
   hadronic inputs.

Do not work Lane 4 or Lane 6 in this loop.
