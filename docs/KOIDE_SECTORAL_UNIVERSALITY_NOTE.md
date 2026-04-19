# Koide Sectoral Universality Note

**Date:** 2026-04-17
**Status:** falsification test of Prediction 3 of the charged-lepton
Koide-cone derivation. Current verdict:
`KOIDE_UNIVERSALITY = CHARGED_LEPTON_ONLY`.
**Script:** `scripts/frontier_koide_sectoral_universality.py`
**Authority role:** honest cross-sector comparator for the Koide invariant
`Q = (sum m) / (sum sqrt m)^2`. Reads `alpha_s(v)` and `y_t(v)` from their
respective authority notes and uses PDG values **for comparison only**.
The note does NOT promote Koide universality to a theorem and in fact
falsifies the strong universality reading of Prediction 3 on the current
PDG observation surface.

## Safe statement

On the retained framework surface, using

- `alpha_s(v) = 0.103303816122` from
  [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md) via
  [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- the bounded down-type mass-ratio lane from
  [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
- `y_t(v) = 0.9176` from
  [YT_FLAGSHIP_BOUNDARY_NOTE.md](./YT_FLAGSHIP_BOUNDARY_NOTE.md) (bounded
  central value with explicit systematic)
- PDG masses (pole-mass lepton values; threshold-local self-scale and
  common-scale MS-bar quark values) used **only** as comparators

the runner symbolically establishes the following facts:

1. The charged-lepton Koide ratio computed at PDG precision is
   `Q_l = 0.666661`, equal to `2/3` within `|dev| < 0.001%`. This
   reproduces the classical Koide observation at the accuracy at which
   the charged-lepton pole masses are known.

2. The framework-native down-type Koide ratio, computed from
   `m_d/m_s = alpha_s(v)/2` and `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)`
   (the bounded CKM-dual lane), evaluates to
   `Q_d (framework) = 0.730582`, deviating from `2/3` by `+9.59%`.

3. The PDG threshold-local self-scale down-type Koide ratio evaluates
   to `Q_d (PDG self) = 0.731428`, deviating from `2/3` by `+9.71%`. The
   framework-native prediction is internally consistent with the PDG
   self-scale value to within 0.12%, so the 9% deviation is a property
   of observation, not an artefact of the framework bridge chain.

4. Running the light masses to the common scale `mu = m_b` using the
   standard one-loop transport factor `(alpha_s(m_b)/alpha_s(2 GeV))^{12/25}`
   gives `Q_d (common, m_b) = 0.744497`, i.e., even further from `2/3`.
   No scheme in the down-type sector brings `Q_d` inside the tight
   1% window set by the charged-lepton anchor.

5. The up-type Koide ratio, computed in the canonical PDG scheme with
   `m_u(2 GeV) = 2.16 MeV`, `m_c(m_c) = 1273 MeV`,
   `m_t(pole) = 172.69 GeV`, evaluates to `Q_u (PDG self) = 0.848838`,
   deviating from `2/3` by `+27.33%`.

6. Running all three up-type masses to `mu = M_Z` (representative PDG
   MS-bar values) gives `Q_u (M_Z) = 0.888373`, deviating from `2/3` by
   `+33.26%`. Common-scale running does NOT rescue up-type Koide; it
   makes the deviation larger.

7. The framework has a bounded anchor for `m_t` via `y_t(v) = 0.9176`
   which gives `m_t(v) = v * y_t / sqrt(2) approx 159.80 GeV`. The
   framework does NOT currently carry a retained or bounded extraction
   of `m_u/m_c` or `m_c/m_t`, so a parallel framework-native up-type
   Koide prediction cannot be computed. This absence is confirmed by a
   `grep` across `docs/` on 2026-04-17 and recorded explicitly in the
   runner.

8. The minimum scheme rescaling of `sqrt(m_t)` required to bring
   `Q_u = 2/3` at fixed PDG `m_u(2 GeV)` and `m_c(m_c)` is the root
   `A = 0.339401`, equivalent to a rescaling of `m_t` by
   `A^2 = 0.1152`, i.e., a required effective `m_t` of `approx 19.89 GeV`.
   No retained framework theorem (plaquette running, canonical `v -> M_Z`
   transport, `(7/8)^{1/4}` selector, or any Ward / Schur bridge on main)
   produces a factor of this size.

## Numerical results table

| Quantity | Value | Scheme | Deviation from 2/3 |
|---|---|---|---|
| Q_l | 0.666661 | PDG pole | -0.001% |
| Q_d framework-native | 0.730582 | `alpha_s(v)` + 5/6 bridge | +9.587% |
| Q_d PDG self-scale | 0.731428 | `m_d,m_s` at 2 GeV, `m_b` at `m_b` | +9.714% |
| Q_d common-scale | 0.744497 | all at `mu = m_b` (1-loop) | +11.675% |
| Q_u PDG self-scale | 0.848838 | `m_u` at 2 GeV, `m_c` at `m_c`, `m_t` pole | +27.326% |
| Q_u M_Z | 0.888373 | MS-bar at `mu = M_Z` | +33.256% |

### Verdict

```
KOIDE_UNIVERSALITY = CHARGED_LEPTON_ONLY
```

Rule applied: Q_l passes PDG precision (< 0.01% of 2/3). Both Q_d and
Q_u deviate from 2/3 by >= 5% on every scheme tested. No scheme
correction derivable from retained theorems closes the gap.

## What this does not claim

This note does **not** claim:

- a falsification of the charged-lepton Koide-cone derivation
  ([CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md)
  and
  [charged-lepton-koide-cone-2026-04-17.md](../.claude/science/derivations/charged-lepton-koide-cone-2026-04-17.md)).
  The charged-lepton sector still sits at `Q_l = 2/3` to PDG precision, and
  the algebraic layer of the cone derivation (Steps 1-5) is untouched;
- a falsification of the bounded down-type mass-ratio lane. The
  framework-native `Q_d` is internally consistent with the PDG self-scale
  reading; the 9% deviation is a property of the data, not of the bridge
  chain;
- that the Koide-cone mechanism is wrong. The result is that if there is a
  framework-native Koide-cone theorem, it is **sector-specific** to
  charged leptons on the current retained surface, not a universal law
  across all three mass sectors;
- a promotion of Koide to retained theorem status in any sector. The
  algebraic cone equivalence is theorem-grade; the cone-forcing step
  remains open even on the charged-lepton surface;
- any new input to PMNS, DM, Z_3 doublet-block-selector, or G1 lanes;
- any claim about up-type mass ratios beyond the exhibited absence of a
  framework-native `m_u/m_c` or `m_c/m_t` extraction on main. Building
  such an extraction is a separate G5 lane task;
- that the observed Q_d value of roughly 0.73 is inconsistent with some
  *future* framework extraction. The honest reading is that the current
  bounded down-type lane itself predicts `Q_d ~ 0.73`, not `2/3`, because
  the framework-native ratios `m_d/m_s = alpha_s(v)/2` and
  `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)` do not land on the Koide cone.

## Relationship to existing notes

- [CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md):
  carries the algebraic Koide-cone equivalence (`Q_l = 2/3` iff
  `a_0^2 = 2 |z|^2` on the retained hw=1 triplet) and flags the
  cone-forcing step as open. The present note is a *transverse* test
  that checks whether the same cone is occupied by the other two mass
  sectors. It concludes that it is not, at PDG-level precision, under
  any scheme checked.
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md):
  supplies the framework-native down-type mass ratios used as input here.
  The 9.6% deviation of `Q_d` from `2/3` is fully consistent with that
  lane's own 3-4% threshold-local mass-ratio deviations; Koide amplifies
  those residual mismatches because it is a quadratic form in the
  mass-square-roots.
- [YT_FLAGSHIP_BOUNDARY_NOTE.md](./YT_FLAGSHIP_BOUNDARY_NOTE.md):
  supplies the `y_t(v) = 0.9176` bounded central value used to exhibit
  the framework `m_t` anchor. Not used as a derivation input to any Koide
  quantity.
- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md),
  [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md):
  supply `alpha_s(v)`, `u_0`, `<P>`, `alpha_LM`, `alpha_bare` via
  `scripts/canonical_plaquette_surface.py`.

## Dependency contract

Before this note is trusted, each reused authority runner must be
re-executed fresh and report its usual PASS:

- `frontier_mass_ratio_ckm_dual.py` expected `PASS=23, FAIL=0`
- `frontier_plaquette_self_consistency.py` expected retained `<P>` closure
- `frontier_yt_exact_interacting_bridge_transport.py` (or equivalent)
  expected to hold `y_t(v) = 0.9176` central value in its bounded window

No retained generation / observable / anomaly theorem is claimed by
this runner, so no broader retained-stack revalidation is required.

PDG masses used as comparators:

- charged-lepton pole: `m_e = 0.5109989461 MeV`, `m_mu = 105.6583745 MeV`,
  `m_tau = 1776.86 MeV`
- down-type threshold-local: `m_d(2 GeV) = 4.67 MeV`,
  `m_s(2 GeV) = 93.4 MeV`, `m_b(m_b) = 4180 MeV`
- up-type threshold-local: `m_u(2 GeV) = 2.16 MeV`, `m_c(m_c) = 1273 MeV`,
  `m_t(pole) = 172.69 GeV`
- up-type at `mu = M_Z` (representative MS-bar): `m_u = 1.27 MeV`,
  `m_c = 619 MeV`, `m_t = 171 GeV`

None of these comparators enters the derivation surface of the runner.

## Paper-safe wording

> Applied to the three charged-fermion mass sectors, the Koide invariant
> `Q = (sum m) / (sum sqrt m)^2` takes sharply different values. On the
> charged-lepton sector, `Q_l = 0.666661` lies at the `2/3` theorem-grade
> target to PDG precision. On the down-type quark sector, both the
> framework-native bounded-lane prediction and the PDG threshold-local
> read give `Q_d approx 0.73`, a 9-10% departure from `2/3` that no
> common-scale running reduces. On the up-type quark sector, the PDG
> self-scale read gives `Q_u approx 0.85` and the MS-bar-at-M_Z read
> gives `Q_u approx 0.89`, neither of which is reduced to `2/3` by any
> scheme correction derivable from the retained framework stack. On the
> present observation surface, the Koide invariant is therefore a
> sector-specific statement of the charged-lepton mass sector, not a
> universal law across the three generations. The charged-lepton
> Koide-cone derivation remains active as a sector-local G5 lane; a
> cross-sector universality theorem would have to be accompanied by an
> explicit sector-dependent spectral correction that the current retained
> stack does not supply.

## Validation

Run:

```bash
python3 scripts/frontier_koide_sectoral_universality.py
```

Current expected result: `PASS=20, FAIL=0`,
`KOIDE_UNIVERSALITY = CHARGED_LEPTON_ONLY`.
