# Lane 2 Route Portfolio

**Updated:** 2026-05-01T11:10:40Z
**Loop:** `lane2-atomic-scale-20260428`  
**Selection policy:** choose the route most likely to move claim state without touching Lane 4 or Lane 6.

Scoring: 0-3 for claim-state movement, import retirement, review-blocker value,
artifactability, novelty, hard-residual pressure, and overclaim risk.

| Route | Type | Claim-state potential | Import retirement | Review value | Artifactability | Hard-residual pressure | Overclaim risk | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| QED threshold bridge firewall: test whether retained `b_QED=32/3` can determine `alpha(0)` from `alpha(M_Z)` | exact runner + no-go/support | 2 | 2 | 3 | 3 | 2 | -1 | selected |
| Physical-unit nonrelativistic Coulomb/Schrodinger limit from existing lattice Hamiltonian notes | constructive theorem / stretch | 3 | 3 | 3 | 1 | 3 | -2 | later stretch if time; larger proof surface |
| Atomic dependency firewall refinement only, without a runner | audit | 1 | 1 | 2 | 3 | 0 | 0 | too shallow unless paired with executable test |
| Search retained lattice atomic companion for direct Rydberg ratio closure | atlas reuse | 1 | 1 | 2 | 2 | 1 | -1 | useful background, but existing lane lacks continuum/volume control |
| Post-Koide electron-mass substitution into hydrogen scaffold | substitution runner | 3 | 3 | 3 | 1 | 1 | -3 | blocked by Lane 6 collision and missing retained `m_e` |

## Selected Block-01 Route

Build an exact threshold-dependency artifact for the QED running bridge:

```text
retained alpha_EM(M_Z) + retained asymptotic b_QED
  does not by itself determine alpha(0)
```

The intended claim-state movement is not Rydberg closure. It is a sharper
Lane 2 prerequisite: any future retained Rydberg claim must supply a
threshold-resolved QED transport theorem, including charged thresholds and
hadronic/vacuum-polarization handling, rather than citing the structural
`b_QED` coefficient alone.

## Block 01 Result

Completed. The paired runner/note landed the exact negative boundary:

```text
alpha_EM(M_Z) + b_QED(asymptotic) does not determine alpha(0).
```

The next high-value routes are:

1. stretch attempt on the physical-unit nonrelativistic Coulomb/Schrodinger
   limit from minimal repo primitives;
2. deeper threshold-resolved QED transport theorem if the route can avoid
   charged-lepton/hadronic closure overlap;
3. stuck fan-out if both routes are blocked.

## Block 01 Stretch Result

Completed route: physical-unit nonrelativistic Coulomb scale bridge.

The stretch produced an exact conditional support theorem plus a no-go
boundary:

```text
H_g = -Delta_x - g/|x|
g = 2 mu a Z alpha
E = lambda / (2 mu a^2)
=> E_n = -mu (Z alpha)^2 / (2 n^2)
```

This means the dimensionless lattice companion has the right scaling bridge
once `mu/m_e`, `alpha(0)`, and the physical unit map are supplied. It also
proves that without the physical unit map `a`, the same dimensionless
eigenvalue maps to different eV energies. The route therefore moves Lane 2 by
isolating the exact scale identity and keeping absolute Rydberg closure open.

Next candidate routes:

1. threshold-resolved QED fan-out: try to prove whether threshold data can be
   made insensitive enough for a bounded `alpha(0)` support statement without
   touching Lane 6/Lane 1 closure;
2. framework-native kinetic normalization route: search retained action/unit
   surfaces for a derivation of the physical map `a = g/(2 mu Z alpha)`;
3. stuck fan-out across algebraic, atlas-reuse, variational, no-go, and
   falsifier frames if neither route passes the dramatic-step gate.
