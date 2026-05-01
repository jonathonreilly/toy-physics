# Lane 2 Route Portfolio

**Updated:** 2026-05-01T10:53:48Z  
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
