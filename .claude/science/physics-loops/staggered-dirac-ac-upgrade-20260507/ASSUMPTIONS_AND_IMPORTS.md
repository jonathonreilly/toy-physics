# Assumption / Import Ledger — AC Upgrade Research Loop

**Date:** 2026-05-07
**Loop:** staggered-dirac-ac-upgrade-20260507

## A1+A2 — Retained framework axioms

| ID | Statement | Status |
|---|---|---|
| A1 | Cl(3) local algebra | retained per `MINIMAL_AXIOMS_2026-05-03` |
| A2 | Z³ spatial substrate | retained |

## Retained primitives directly relevant to AC upgrade

| Primitive | Statement | Authority |
|---|---|---|
| RP A11 | Reflection positivity → OS reconstruction → H_phys with unique vacuum |Ω⟩ | `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29` |
| Reeh-Schlieder | A(O)|Ω⟩ dense in H_phys for any open region O; vacuum cyclic + separating | `AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01` |
| Spectrum condition | H ≥ 0, |Ω⟩ unique ground state with energy 0 | `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29` (cited via RS) |
| Cluster decomposition | Connected correlators decay exponentially; vacuum unique on canonical surface; **NO superselection sectors** | `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29` |
| Lieb-Robinson | Local-operator microcausality v_LR = 2eJR_int Z_lat | `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01` |
| Lattice Noether | fermion-number Q̂ on H_phys (conserved Noether charge) | `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29` |
| Single-clock evolution | Unitary one-parameter group on H_phys | `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03` |
| M_3(C) on hw=1 | Three corners with translations + C_3[111] generate M_3(C) algebra; distinct joint translation characters | `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE` retained |
| No-proper-quotient | M_3(C) on hw=1 has no proper exact quotient | `THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02` retained |
| Physical-lattice necessity | Substrate-level Hilbert/locality/info reading | `PHYSICAL_LATTICE_NECESSITY_NOTE` retained narrowed |

## Open gates (admitted-context only, not load-bearing for derivation)

| Item | Class |
|---|---|
| Staggered-Dirac realization (A3) | substantially closed by prior campaign (PRs #631-#637) |
| g_bare = 1 normalization (A4) | open gate per `MINIMAL_AXIOMS_2026-05-03` |

## Standard mathematical infrastructure (admissible non-derivation)

| Item | Role |
|---|---|
| GNS construction | Standard QFT |
| Schur orthogonality + Lie-algebra rep theory | Standard math |
| Edge-of-the-wedge / Schwarz reflection | Standard complex analysis |
| Translation algebra on Z³ APBC (BZ corners) | Standard lattice analysis |

## Forbidden imports

- NO PDG observed values
- NO lattice MC values as derivation inputs
- NO fitted selectors
- NO same-surface family arguments
- NO new axioms

## Strategic insight from preflight

**Reeh-Schlieder + cluster decomposition retained → H_phys has UNIQUE vacuum, NO DHR superselection sectors on canonical surface.**

This means:
- Block 05's "three DHR superselection sectors" framing was WRONG
- Three matter generations cannot be DHR sectors (since none exist on canonical surface)
- Three matter generations must be three quantum-mechanically DISTINCT STATES within one H_phys, separated by retained translation characters and connected by C_3[111] cyclic generator within the M_3(C) algebra

This INSIGHT closes substep 4 directly without admitted-context AC, by reformulating the "physical species bridge" as observable-separation + spectral-distinctness within H_phys (all retained), rather than DHR superselection (admitted standard QFT machinery).

## A_min for AC upgrade

```
A_min(AC upgrade) = {
  A1, A2,
  RP A11 + OS reconstruction → H_phys (retained),
  Reeh-Schlieder cyclicity (retained),
  Cluster decomposition + unique vacuum (retained),
  Lieb-Robinson microcausality (retained),
  Lattice Noether fermion-number (retained),
  Single-clock evolution (retained),
  M_3(C) algebra on hw=1 (retained),
  Three-generation no-proper-quotient (retained),
  Physical-lattice necessity (retained),
  Standard math machinery (admissible: GNS, Schur, Lie rep theory)
}
```
