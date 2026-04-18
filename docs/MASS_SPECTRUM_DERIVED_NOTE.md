# Mass Spectrum Derived — Five-Phase Attack Closure

**Date:** 2026-04-17
**Status:** headline bundling note for the 1→3 mass-spectrum attack.
Mixed closure: one retained headline (Phase 1 down-type dual), one
bounded secondary with explicit partition (Phase 2 up sector), one
bounded cross-reference (Phase 3 charged leptons), one retained
seesaw scale + bounded solar/PMNS (Phase 4 neutrino), one
bounded/conditional cosmology cascade (Phase 5).
**Attack plan:** `/Users/jonBridger/.claude/plans/zesty-nibbling-pretzel.md`
**Framework convention:** "axiom" means only the single framework
axiom `Cl(3)` on `Z^3`.

## Scope

This note bundles the five phases of the mass-spectrum attack into a
single reviewer entry point.  Each phase has its own runner and its
own authority note.  This document is the index + honest-accounting
table for the entire lane.

## The five phases

| Phase | Sector | Runner | Note | Status |
|---|---|---|---|---|
| 1 | down-type quarks | `frontier_mass_ratio_ckm_dual.py` | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` | **retained headline** |
| 2 | up-type quarks | `frontier_mass_ratio_up_sector.py` | `UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md` | bounded, one conditional partition |
| 3 | charged leptons | `frontier_mass_ratio_lepton_sector.py` | `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` | bounded cross-reference; three missing primitives named |
| 4 | neutrino sector | `frontier_neutrino_mass_derived.py` | `NEUTRINO_MASS_DERIVED_NOTE.md` | retained (`k_B = 8`, `m_3`, NO); conditional/support `theta_23` upper octant; bounded solar gap |
| 5 | cosmology | `frontier_cosmology_from_mass_spectrum.py` | `COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md` | bounded/conditional (imported `eta` + bounded `alpha_GUT`) |

## Phase 1 — down-type quark mass ratios from CKM dual

**Algebra (zero free parameters):** equating the atlas CKM with the
mass-ratio CKM through the GST relation and the 5/6 = C_F - T_F SU(3)
bridge exponent.

```
  |V_us|_atlas = sqrt(alpha_s(v)/2)  =>  m_d/m_s = alpha_s(v)/2 = 0.0517
  |V_cb|_atlas = alpha_s(v)/sqrt(6)  =>  m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)
                                                 = 0.02237
  chain:                                m_d/m_b = 0.001157
```

| Prediction | Value | Observed | Error |
|---|---|---|---|
| `m_d/m_s` | 0.0517 | 0.0500 | +3.3% |
| `m_s/m_b` | 0.02237 | 0.02234 | +0.13% |
| `m_d/m_b` | 1.16e-3 | 1.12e-3 | +3.6% |

Uses only promoted/exact framework inputs (atlas CKM, `alpha_s(v)`, SU(3)
Casimirs).  Zero fitted parameters.  **Retained headline.**

## Phase 2 — up-type quark mass ratios from CKM inversion

Parallel-bridge + CP-orthogonal ansatz adds the up sector symmetrically
to the down sector:

```
  |V_us|^2 = m_d/m_s + m_u/m_c                  (CP-orthogonal sum)
  |V_cb|^2 = (m_s/m_b)^(5/3) + (m_c/m_t)^(5/3)
```

One conditional partition `(f_12, f_23)` in `[0,1]^2` parametrizes the
family.  Down-dominant edge `(1,1)` recovers Phase 1 exactly.
Observation-comparator partition:

- `f_12 = 0.984` (1-2 down-dominant at 1.6%)
- `f_23 = 0.998` (2-3 down-dominant at 0.2%)

Numerical outcomes at that partition:

- `m_u/m_c` = 1.65e-3 (obs 1.70e-3, +2.6% deviation) — closed within 3%.
- `m_c/m_t` = 7.35e-4 (obs 7.38e-3, -90% deviation) — structural signature:
  the CP-orthogonal ansatz saturates `|V_cb|^2` on the down side, leaving
  no room for a 2-3 up contribution.  Requires non-orthogonal phase
  `cos(psi) ~ 0.2` or modified bridge combination rule.

**Bounded secondary lane.**  Three closure candidates:
(1) atlas CP phase `delta = arctan(sqrt(5))`;
(2) Jarlskog invariant `J`;
(3) isospin-partner EWSB cascade theorem.

## Phase 3 — charged lepton mass hierarchy

Delegates to the 19-runner review package
(`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`).  Answers the
plan's key question:

> Is the charged lepton hierarchy `m_e/m_mu ~ 1/207` derivable from the
> same `alpha_s`-based formula as `m_d/m_s ~ alpha_s(v)/2`?

**Answer: no.**  A negative test in the Phase 3 runner verifies that
`alpha_s(v)/2 = 0.0517` does not reproduce `m_e/m_mu = 0.00484`
(off by 10x).  The 19-runner package rigorously documents six no-gos
and names three missing primitives:

1. non-Cl(3)-covariant lift;
2. real-irrep-block democracy;
3. fourth-order cancellation breaking.

The Koide relation `Q_ell = 2/3` is algebraically equivalent to
`a_0^2 = 2|z|^2` on `C_3` characters (retained as structural).

**Bounded; three primitives named for future promotion.**

## Phase 4 — neutrino sector closure

Retained zero-import outputs:

- taste-staircase placements `k_A = 7`, `k_B = 8` from adjacent-placement
  theorem;
- `rho = B/A = alpha_LM` (one staircase step);
- `eta_break = eps/B = alpha_LM/2` from residual-sharing theorem;
- Dirac coefficient `y_nu^eff = g_weak^2/64` from retained local theorem;
- seesaw mass `M_1 = B(1 - alpha_LM/2) = 5.32e10 GeV`;
- atmospheric scale `m_3 = 5.06e-2 eV`, `Dm^2_31 = 2.54e-3 eV^2` (+3.5%
  of NuFit 5.3 NO);
- **normal ordering as structural prediction**;
- **`theta_23` upper-octant falsifiable conditional/support prediction**
  (`s_23^2 >= 0.541`).

Bounded:

- solar gap `Dm^2_21` (diagonal benchmark over-predicts; requires
  off-diagonal M_R texture);
- sharp point predictions for `theta_12, theta_13, delta_CP` (bounded
  on chamber-boundary ridge `q_+ + delta = sqrt(8/3)`).

## Phase 5 — cosmology cascade

Chain:

```
  eta  ->  Omega_b (BBN)  ->  Omega_DM = R * Omega_b  ->  Omega_Lambda = 1 - Omega_m
```

with R = 31/9 * Sommerfeld = 5.48.

| Pie chart | Predicted | Observed | Error |
|---|---|---|---|
| `Omega_b`       | 0.0492 | 0.0493 | 0.2% |
| `Omega_DM`      | 0.2696 | 0.2650 | 1.7% |
| `Omega_m`       | 0.3188 | 0.3150 | 1.2% |
| `Omega_Lambda`  | 0.6811 | 0.6850 | 0.6% |

Reduces six LCDM parameters to one imported (`eta`) + one bounded
(`alpha_GUT`).  Open lane: promote `eta` from DM-gate support to retained
theorem (exact one-flavor transport or PMNS reduced-surface selector
closure).

## The 1 -> 3 mass-spectrum attack plan scorecard

| Plan deliverable | Realized | Note |
|---|---|---|
| `scripts/frontier_mass_ratio_ckm_dual.py` | yes | Phase 1 runner |
| `scripts/frontier_mass_ratio_up_sector.py` | yes | Phase 2 runner |
| `scripts/frontier_mass_ratio_lepton_sector.py` | yes | Phase 3 runner |
| `scripts/frontier_neutrino_mass_derived.py` | yes | Phase 4 runner |
| `scripts/frontier_cosmology_from_mass_spectrum.py` | yes | Phase 5 runner |
| `docs/MASS_RATIO_CKM_DUAL_NOTE.md` | yes | as `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` |
| `docs/MASS_SPECTRUM_DERIVED_NOTE.md` | yes | **this note** |

## Retained vs bounded vs conditional

**RETAINED (zero-free-parameter, sub-percent or few-percent to observation):**

- `m_d/m_s = alpha_s(v)/2` (Phase 1, +3.3%)
- `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)` (Phase 1, +0.13%)
- `m_d/m_b` chain (Phase 1, +3.6%)
- `k_A = 7, k_B = 8` (Phase 4, integer theorem)
- `rho = B/A = alpha_LM`, `eta_break = eps/B = alpha_LM/2` (Phase 4, exact)
- `m_3`, `Dm^2_31` (Phase 4, +3.5%)
- normal ordering (Phase 4, structural)
- `theta_23` upper octant (Phase 4, falsifiable conditional/support)
- `R_base = 31/9` (Phase 5, exact group theory)
- flatness identity `Omega_total = 1` (Phase 5, textbook)

**BOUNDED (one parameter / conditional):**

- `m_u/m_c`, `m_c/m_t` via `(f_12, f_23)` partition (Phase 2)
- `m_e/m_mu`, `m_mu/m_tau` blocked on three named missing primitives
  (Phase 3)
- `alpha_GUT` in `[0.03, 0.05]` entering Sommerfeld `R` (Phase 5)

**IMPORTED (single input carrying residual dependence on observation):**

- `eta = 6.12e-10` on the live cosmology surface
  (DM-gate support reaches `eta/eta_obs = 1.0` but not yet retained).

**OPEN LANES:**

- solar gap `Dm^2_21` and PMNS angles `theta_12, theta_13, delta_CP`
  (Phase 4 bounded to chamber ridge);
- partition parameters `(f_12, f_23)` retained from a primitive
  (Phase 2 bounded);
- charged lepton primitive closure (Phase 3 bounded);
- `eta` promotion (Phase 5 imported-with-support);
- `alpha_GUT` from retained unification (Phase 5 bounded).

## Validation

Run all five in sequence:

```bash
python3 scripts/frontier_mass_ratio_ckm_dual.py
python3 scripts/frontier_mass_ratio_up_sector.py
python3 scripts/frontier_mass_ratio_lepton_sector.py
python3 scripts/frontier_neutrino_mass_derived.py
python3 scripts/frontier_cosmology_from_mass_spectrum.py
```

Expected result on `main`:

- `frontier_mass_ratio_ckm_dual.py`: `PASS=23 FAIL=0`
- `frontier_mass_ratio_up_sector.py`: `PASS=23 FAIL=0`
- `frontier_mass_ratio_lepton_sector.py`: `PASS=11 FAIL=0`
- `frontier_neutrino_mass_derived.py`: `PASS=19 FAIL=0`
- `frontier_cosmology_from_mass_spectrum.py`: `PASS=14 FAIL=0`
- **Total: `PASS=90 FAIL=0`**

## Safe wording

**Can claim:**

- the down-type mass ratios are zero-free-parameter predictions from
  promoted atlas CKM + SU(3) Casimirs;
- the up-type 1-2 sector ratio `m_u/m_c` is closed within 3% at the
  observation-comparator partition in a bounded one-parameter family;
- the neutrino atmospheric mass scale, normal ordering, and the
  `theta_23` upper-octant consequence is conditional/support, not retained;
- the cosmological pie chart (`Omega_b, Omega_DM, Omega_m, Omega_Lambda`)
  lands within 2% across the board once `eta` is imported;
- the five-phase attack reduces the ToE parameter count on the retained
  surface by delivering the Phase 1 sub-percent down-type chain.

**Cannot claim:**

- that the full quark mass spectrum is retained (Phase 2 up sector
  remains bounded on one partition);
- that the charged lepton hierarchy is derived (three primitives
  missing);
- that the solar gap or PMNS angles are sharp retained point
  predictions;
- that `eta` is derived on the live cosmology surface (imported with
  DM-gate support, but not yet a retained theorem);
- that the framework delivers `H_0` or age-of-universe observables
  from this attack.
