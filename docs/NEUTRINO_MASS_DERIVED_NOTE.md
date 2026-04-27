# Neutrino Sector Closure (Phase 4 of mass spectrum)

**Date:** 2026-04-17
**Status:** proposed_retained atmospheric scale + rho + eta_break + k_B; bounded solar gap;
conditional/support `theta_23` upper-octant lane.
**Primary runner:** `scripts/frontier_neutrino_mass_derived.py`
**Depends on:** retained atmospheric-scale + adjacent-placement + residual-sharing
staircase theorem package; Phase 1-2 of mass spectrum.

## Safe statement

The zero-import Cl(3) on Z^3 framework, combined with the retained staircase
theorem package on the current branch, fixes the Z_3 breaking parameters
`(rho, eta_break)` of the neutrino sector and predicts the atmospheric
neutrino mass scale and ordering without fitting any neutrino observable:

| Quantity | Derived expression | Numerical |
|---|---|---|
| `k_A` | adjacent-placement theorem | `7` |
| `k_B` | adjacent-placement theorem | `8` |
| `rho = B/A` | one staircase step | `alpha_LM = 0.0907` |
| `eta_break = eps/B` | residual-sharing theorem | `alpha_LM/2 = 0.0453` |
| `y_nu^eff` | retained local Dirac theorem | `g_weak^2/64 = 6.66e-3` |
| `v_EW` | hierarchy theorem | `M_Pl * (7/8)^(1/4) * alpha_LM^16 = 246.3 GeV` |
| `M_1` | seesaw on fixed bridge | `5.32e+10 GeV` |
| `m_3` | `y^2 v^2 / M_1` | `5.06e-2 eV` |
| `Dm^2_31` | `m_3^2 - m_1^2` (diag) | `2.54e-3 eV^2` (+3.5% of NuFit) |

**No observed neutrino masses, splittings, or mixing angles are used as
derivation inputs.**

In addition the conditional/support
`PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION` note gives a
falsifiable upper-octant consequence `s_23^2 >= 0.541` at PDG-2024 central
`(s_12^2, s_13^2)`, testable at JUNO/DUNE/Hyper-Kamiokande, given the same
imposed branch-choice rule used by the G1 chamber pin.

This closes the Phase 4 deliverable of the mass-spectrum attack plan:

> "Map the quark mass ratios to the Z_3 breaking parameters... Once `rho`
>  and `eta_break` are determined, the mass-squared splittings are
>  predictions."

## Inputs and provenance

### Promoted / retained inputs

- [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md):
  `m_3 = y_nu^2 v^2 / M_1 = 5.058e-2 eV` and `Dm^2_31 = 2.539e-3 eV^2`
  on the fixed `k_A=7, k_B=8` bridge.
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md):
  `k_B - k_A = 1`.
- [NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md):
  `eps/B = alpha_LM / 2`.
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md):
  Phase 1 quark 2-3 splitting `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)`.
- [UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md](./UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md):
  Phase 2 up-sector parallel-bridge ansatz.
- [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md):
  conditional/support θ_23 upper-octant chamber-threshold consequence.

### No observational input

The runner uses PDG/NuFit values only as comparator benchmarks after
running the derivation. None appear in the predictive chain.

## Closure chain

```
  Cl(3) on Z^3 axiom
   → canonical plaquette surface P_MC, u_0, alpha_bare, alpha_LM, alpha_s(v)
   → retained local Dirac theorem          → y_nu^eff = g_weak^2 / 64
   → adjacent-placement theorem             → k_A = 7, k_B = 8
   → residual-sharing theorem               → eps/B = alpha_LM / 2
   → hierarchy theorem                      → v_EW = M_Pl * (7/8)^(1/4) * alpha_LM^16
   → seesaw on the fixed k_A=7, k_B=8 bridge:
        A = M_Pl * alpha_LM^7
        B = M_Pl * alpha_LM^8
        M_1 = B(1 - eps/B)
        M_2 = B(1 + eps/B)
        M_3 = A
        m_i = y_nu^2 v^2 / M_{sigma(i)}
   → atmospheric-scale theorem              → m_3 = 5.058e-2 eV
                                            → Dm^2_31 = 2.539e-3 eV^2
```

The plan's named parameters `rho` and `eta_break` are realized as

- `rho = B/A = alpha_LM` (one staircase step),
- `eta_break = eps/B = alpha_LM/2` (residual sharing).

Both are **exact integer / simple-algebraic** expressions in the
already-promoted staircase coupling `alpha_LM`.

## What Phase 4 retains

- the Majorana heavy spectrum `(M_1, M_2, M_3)` on the fixed bridge;
- the atmospheric mass scale `m_3 ~ 5.06e-2 eV` and
  `Dm^2_31 ~ 2.54e-3 eV^2` (within 5% of NuFit 5.3 NO);
- the **normal ordering** as a structural prediction (`m_3 > m_2 > m_1`);
- the **θ_23 upper-octant** conditional/support chamber-threshold consequence
  (`s_23^2 >= 0.541` at PDG-2024 central);
- `k_B = 8` as the taste-staircase level for the lightest RH neutrino —
  the input required by Phase 5 leptogenesis.

## What Phase 4 bounds but does not retain

- **Solar gap** `Dm^2_21`: the diagonal benchmark over-predicts
  `Dm^2_21 ~ 2.1e-3 eV^2` vs the observed `7.4e-5 eV^2`. This is a
  known open lane requiring full-matrix flavor texture (off-diagonal
  mixing in `M_R`) that is not yet derived from the retained core.
- **Point predictions for `theta_12, theta_13, delta_CP`**: the retained
  PMNS-chamber closure bounds these to a 1-parameter chamber-boundary
  ridge `q_+ + delta = sqrt(8/3)`; no sharp derivation pins specific
  values. Complex Z_3 breaking suggests `delta_CP ~ -103°` but this is
  not yet retained.

These are exactly the lanes flagged as "remaining blockers" in the
atmospheric-scale theorem note and are consistent with the plan's
expectation that "the remaining uncertainty... may also resolve" via
downstream closure.

## Cross-link to Phase 1-2 (shared alpha_LM building block)

The plan hypothesizes: "The same α_s-based hierarchy that gives m_d/m_s
should determine ε/B."

The numerical realization is structural rather than algebraically
identical:

- Phase 1 quark 2-3: `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5) = 0.02239`.
- Phase 4 neutrino 2-3: `eps/B = alpha_LM/2 = 0.04533`.

Both ratios are monomials in the plaquette-surface coupling (with
`alpha_s(v) = alpha_LM/u_0`), but the exponents differ: the quark
splitting carries the SU(3) 5/6 bridge exponent and the `sqrt(6)`
CKM normalization, while the neutrino splitting carries the
self-dual + residual-sharing combinatorial factor of 1/2.

The structural hypothesis "shared `alpha_LM` building block" is therefore
retained; the stronger hypothesis "identical ratio" is **not** retained
and is **not** required by the framework — the quark and neutrino
sectors have different group-theoretic fingerprints (SU(3) 5/6 bridge vs
SU(2)_L + self-dual Majorana lift), and the retained residual-sharing
theorem already explains why.

## What closes next (Phase 4b path)

Three candidates for the remaining solar / PMNS lanes:

1. **Off-diagonal M_R texture**: derive the `(1,2)` and `(1,3)` entries
   of the right-handed Majorana matrix from the full Z_3 selection rule
   package, not just the diagonal benchmark. This would fix `Dm^2_21`.
2. **PMNS angle pinning via Schur-Q coincidence**: the retained
   `PMNS_THETA23_UPPER_OCTANT` note observed that the Schur-Q
   variational symmetric minimum and the PMNS-pinning threshold point
   lie on the same chamber-boundary line. A theorem promoting this
   coincidence to a derivation would give point predictions for the
   remaining PMNS angles.
3. **Complex Z_3 breaking δ_CP derivation**: promote the current
   `delta_CP ~ -103°` suggestion from complex Z_3 breaking to a
   retained theorem.

Any one of these would move a Phase 4 bounded item into the retained
tier.

## Validation

```bash
python3 scripts/frontier_neutrino_mass_derived.py
```

Expected result on `main`:

- `frontier_neutrino_mass_derived.py`: `PASS=19 FAIL=0`

The runner verifies:

- the retained staircase + Dirac inputs (Part 1);
- `rho = B/A = alpha_LM` and `eta_break = eps/B = alpha_LM/2` from the
  staircase and residual-sharing theorems (Part 2);
- Majorana eigenvalues and light-neutrino masses + `Dm^2_31` within 5%
  of NuFit 5.3 NO central, with normal ordering structural; also that
  the diagonal `Dm^2_21` benchmark is NOT a closure (honestly flagged
  as open lane) (Part 3);
- the conditional/support `theta_23` upper-octant chamber-threshold consequence (Part 4);
- `k_B = 8` and `M_1` as the Phase 5 leptogenesis input (Part 5);
- the shared `alpha_LM` building-block between quark 2-3 and neutrino
  2-3 splittings (Part 6);
- a summary of what Phase 4 retains, what it bounds, and what it
  delivers to Phase 5 (Part 7).
