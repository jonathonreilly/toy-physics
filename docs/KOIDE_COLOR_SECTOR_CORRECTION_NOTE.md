# Koide Color Sector Correction Note

**Date:** 2026-04-17
**Status:** structural investigation of a color-theoretic sector correction
to the Koide invariant on the retained Cl(3)/Z^3 framework surface; the
retained SU(3) Casimir algebra supplies the exact identity
`(C_F - T_F)^(-1/4) = (6/5)^(1/4)`, which — assumed as a down-quark hw=1
spectral-amplitude dressing — reproduces `Q_d = (2/3) sqrt(6/5)` and matches
the PDG threshold-local observation to `0.16%`; the DERIVATION that the
hw=1 down-type amplitudes actually carry this factor is OPEN
**Script:** `scripts/frontier_koide_color_sector_correction.py`
**Authority role:** structural support / negative-result note for candidate
5 (color-theoretic sector correction) of the five-agent G5 attack surface
recorded in
[CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).
This note does NOT promote any Koide relation to a retained theorem in
any sector.

## Safe statement

On the retained framework surface, using exclusively the SU(3) Casimirs
already present on `main`:

- `C_F = 4/3` (fundamental quadratic Casimir at `N_c = 3`)
- `T_F = 1/2` (fundamental Dynkin index, standard normalization)
- `C_A = 3` (adjoint quadratic Casimir, `C_A = N_c`)
- `C_F - T_F = 5/6` (retained CKM `5/6` bridge, see
  [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](./CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md))
- `R_conn = (N_c^2 - 1)/N_c^2 = 8/9` (leading-order color-singlet
  projection from
  [RCONN_DERIVED_NOTE.md](./RCONN_DERIVED_NOTE.md))

the runner symbolically establishes the following facts:

1. **Zero-order invariance.** If the square-root mass vector is uniformly
   dressed by a species-independent scalar `f`, the Koide invariant
   `Q = (sum m) / (sum sqrt m)^2` is exactly invariant. Therefore any
   color correction that shifts `Q` between sectors MUST be either
   species-dependent or act as a matrix correction on the circulant
   `(a, b)` parameters of the retained hw=1 character expansion.

2. **Exact retained identity.** Among natural Casimir expressions,
   `(C_F - T_F)^(-1/4)` evaluates to `(6/5)^(1/4) = 1.0466351394...`
   exactly by SU(3) algebra. No heuristic, no tuning: this is a
   four-step consequence of `C_F = 4/3` and `T_F = 1/2`.

3. **Target ratio match.** If the charged-lepton sector is fixed at
   the retained Koide cone `Q_l = 2/3` and the down-sector spectral
   amplitudes are dressed by `f_color(down) = (C_F - T_F)^(-1/4)`, the
   framework predicts

   `Q_d (predicted) = (2/3) * sqrt(6/5) = 2 sqrt(30)/15 = 0.730296743...`

   The PDG threshold-local self-scale observation is `Q_d = 0.731428`,
   so the dressing-hypothesis prediction sits `0.16%` below the
   comparator. The framework-native bounded down-type prediction from
   the retained `5/6` CKM bridge (see
   [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md))
   gives `Q_d = 0.730582`, matching the dressing-hypothesis prediction
   to `0.04%`.

4. **Naive Casimir sums do not help.** The hypothesis that a first-order
   linear Casimir combination directly produces `6/5` is checked and
   FALSIFIED: `(C_A + C_F)/(C_A + T_F) = (13/3)/(7/2) = 26/21`, not
   `6/5`. The `6/5` only appears through the multiplicative
   `C_F - T_F = 5/6` route.

5. **Casimir-ratio scan.** Seventeen natural Casimir-ratio candidates
   were enumerated. Only `(C_F - T_F)^(-1/4)` (and its algebraic
   equivalent `(5/6)^(-1/4)`) reproduce `(6/5)^(1/4)` exactly. The
   nearest unrelated candidate `sqrt(1 + T_F/C_A) = sqrt(7/6)` lies
   `1.4%` from the target.

6. **Up-type sharp failure.** Extending the dressing hypothesis by a
   doubled Casimir insertion `f_color(up) = (C_F - T_F)^(-1/2) =
   sqrt(6/5)` gives `Q_u (predicted) = (2/3)(6/5) = 4/5 = 0.800`,
   versus the PDG threshold-local value `Q_u = 0.849`. The doubled-
   insertion hypothesis misses by `5.75%`. No simple integer or
   half-integer Casimir-power extension of the down-type dressing
   reproduces the observed `Q_u`; the log-ratio `p = 2.65` is not a
   retained Casimir exponent.

7. **Structural audit of the retained surface.** The retained hw=1
   generation algebra (see
   [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md))
   does NOT currently carry a species-dependent color-adjoint projector
   acting on the charged-fermion triplet. The color-singlet projector
   `R_conn = 8/9` is species-democratic and therefore cancels in `Q`.
   So the Casimir expression `(C_F - T_F)^(-1/4)` is ALGEBRAICALLY
   available, but its deployment as a species-dependent spectral-
   amplitude dressing is not forced by any retained theorem.

## Verdict

```
COLOR_CORRECTION_FORCES_SQRT_65 = FALSE_BUT_NEAR
```

Rule applied:

- `TRUE`: retained algebra DERIVES `Q_d / Q_l = sqrt(6/5)` from a
  species-dependent color insertion.
- `FALSE_BUT_NEAR`: retained algebra supplies an EXACT Casimir
  expression equal to `(6/5)^(1/4)`, but no retained theorem forces
  that expression to be the down-type spectral-amplitude dressing.
- `FALSE`: retained algebra does not reach the observed ratio.

The present state is `FALSE_BUT_NEAR`: the numerical identification
is exact by SU(3) algebra, but the structural derivation is open.

## Explicit `f_color` per sector

| Sector | `f_color` | Value | Status |
|---|---|---|---|
| Charged leptons | `1` (color singlet) | `1` | retained baseline |
| Down-type quarks | `(C_F - T_F)^(-1/4) = (6/5)^(1/4)` | `1.046635...` | retained-algebra identity; derivation OPEN |
| Up-type quarks (doubled insertion hypothesis) | `(C_F - T_F)^(-1/2) = sqrt(6/5)` | `1.095445...` | off observation by `5.75%` |

Under this assignment:

- `Q_l = 2/3` (baseline, reproduces PDG pole value to `0.001%`)
- `Q_d (hypothesis) = (2/3) sqrt(6/5) = 2 sqrt(30)/15 = 0.730296...`
  (matches PDG threshold-local self-scale `Q_d = 0.731428` to `0.16%`
  and matches the framework-native bounded down-type read to `0.04%`)
- `Q_u (hypothesis, doubled) = (2/3)(6/5) = 4/5 = 0.800`
  (misses PDG threshold-local self-scale `Q_u = 0.849` by `5.75%`)

## What this does not claim

- A promotion of Koide `Q_l = 2/3` to a retained theorem in the
  charged-lepton sector. The algebraic cone equivalence
  (`Q_l = 2/3` iff `a_0^2 = 2|z|^2`) is theorem-grade; the cone-forcing
  step remains open. See
  [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).
- A derivation that the down-type hw=1 spectral amplitudes ARE dressed
  by `(C_F - T_F)^(-1/4)`. The present note only establishes that
  this dressing, IF imposed, reproduces the observed `Q_d / Q_l`
  ratio to sub-percent precision on the threshold-local self-scale
  observation surface. The dressing itself is not a retained
  operator at this date.
- A universal Koide theorem across all three mass sectors. The up-type
  prediction under the most natural extension (doubled Casimir
  insertion) misses by `5.75%`, confirming the sectoral-universality
  null of Agent 3 (see
  [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md)).
- Any claim that `6/5` arises from a linear Casimir sum. The explicit
  counterexample `(C_A + C_F)/(C_A + T_F) = 26/21` is recorded.
- A refutation of the other four successor candidates listed in the
  G5 status note. The `Z_3` doublet / two-Higgs lane, the `SU(2)_L`
  gauge-exchange lane, the Wilson-improvement lane, and the
  anomaly-forced cross-species lane remain live independent of this
  investigation.
- Any input to PMNS, DM, Z_3 doublet-block-selector, or G1 lanes.
- Any claim about the up-type framework-native extraction; the absence
  of a bounded `m_u/m_c` or `m_c/m_t` lane on `main` is recorded in
  [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md).

## Relationship to existing notes

- [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md):
  supplies the five-agent attack consolidation and explicitly lists a
  "color-theoretic sector correction" (candidate 5) as one concrete
  successor target motivated by the `0.05-0.2%` match
  `Q_d / Q_l ~ sqrt(6/5)`. The present note is the structural
  investigation of that candidate; its conclusion is that the
  retained algebra SUPPLIES the required Casimir expression but does
  NOT force its deployment as a spectral-amplitude dressing.
- [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md):
  establishes the three sector values
  `Q_l ~ 0.667`, `Q_d ~ 0.731`, `Q_u ~ 0.849` on the current PDG
  surface. The ratios `Q_d / Q_l` and `Q_u / Q_l` used here are derived
  from those values. The up-type sharp failure here is consistent with
  Agent 3's `CHARGED_LEPTON_ONLY` verdict.
- [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](./CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md):
  the retained CKM lane exponent `|V_cb| = (m_s/m_b)^{5/6}` uses the
  exact `5/6 = C_F - T_F` identity. The present note uses the same
  Casimir on a fourth-root footing:
  `(C_F - T_F)^(-1/4) = (6/5)^(1/4)`. The two lanes are structurally
  parallel (both lift `5/6` by rational-power Casimir insertions) but
  independent; neither lane forces the other.
- [RCONN_DERIVED_NOTE.md](./RCONN_DERIVED_NOTE.md):
  supplies `R_conn = 8/9` at leading `1/N_c` order as the
  color-singlet projection on gauge-coupling and Yukawa normalizations.
  This is a species-DEMOCRATIC dressing and therefore cancels in `Q`
  (Part B of the runner). The `R_conn` surface cannot by itself
  explain the observed sector-dependent `Q_d / Q_l`.
- [YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md):
  supplies the color-singlet projection chain on the EW coupling lane
  (`g_EW(phys) = g_EW(lattice) / sqrt(R_conn)`). Its species-democratic
  action is the ingredient whose non-cancellation in `Q` would be
  required — and is absent from the retained surface.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  establishes that the retained hw=1 triplet already carries an
  irreducible generation algebra via `C_3[111]` and the three
  translations, with no color-adjoint species projector on the
  retained operator surface. This is the structural statement that
  closes the "species-dependent Casimir insertion" route at the
  current retained level.

## Dependency contract

Before this note is trusted, each reused authority runner should be
re-executed fresh and report its usual PASS:

- `frontier_koide_sectoral_universality.py` expected `PASS=20, FAIL=0`
- `frontier_ckm_five_sixths_bridge_support.py` expected `EXACT PASS=5,
  BOUNDED PASS=7, FAIL=0`
- `frontier_color_projection_mc.py` expected MC `R_conn = 0.887 +/- 0.008`
- `frontier_three_generation_observable_theorem.py` expected
  `PASS=47, FAIL=0`

No retained generation / observable / anomaly theorem is claimed by
this runner beyond those already on `main`.

PDG comparator values used (never as derivation inputs):

- charged-lepton pole: `m_e = 0.5109989461 MeV`,
  `m_mu = 105.6583745 MeV`, `m_tau = 1776.86 MeV`
- down-type threshold-local: `m_d(2 GeV) = 4.67 MeV`,
  `m_s(2 GeV) = 93.4 MeV`, `m_b(m_b) = 4180 MeV`
- up-type threshold-local: `m_u(2 GeV) = 2.16 MeV`,
  `m_c(m_c) = 1273 MeV`, `m_t(pole) = 172690 MeV`

## Paper-safe wording

> On the retained Cl(3)/Z^3 framework surface, the SU(3) Casimir
> identity `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` is exact. If the down-type
> hw=1 spectral amplitudes are dressed by this factor — an assumption
> that the retained surface currently permits but does not force — the
> framework predicts `Q_d = (2/3)\sqrt{6/5}` to `0.16%` of the PDG
> threshold-local self-scale observation and to `0.04%` of the
> framework-native bounded down-type prediction from the retained
> `|V_{cb}| = \alpha_s(v)/\sqrt{6}` and `5/6 = C_F - T_F` chain. The
> same Casimir power-series does NOT reproduce the observed up-type
> Koide ratio under the natural doubled-insertion extension: it
> predicts `Q_u = 4/5`, versus the observed `Q_u \approx 0.849`, a
> `5.75%` deviation. The structural status is therefore that the
> retained Casimir algebra is SUFFICIENT to express the observed
> down-type Koide shift, but not sufficient to DERIVE that shift. The
> derivation requires a new retained primitive supplying a
> species-dependent color-adjoint projector on the hw=1 charged-fermion
> triplet. No such primitive is on `main` at 2026-04-17, and none of
> the four attack nulls closed by the five-agent G5 campaign supplies
> one. The next structurally open attack lane is therefore the
> species-dependent color-insertion mechanism itself — either through
> the `SU(2)_L` gauge-exchange channel (Agent 7 lane), the
> anomaly-forced cross-species propagator (Agent 8 lane), or the
> `Z_3` doublet-block mechanism of the separate G1 thread.

## Validation

Run:

```bash
python3 scripts/frontier_koide_color_sector_correction.py
```

Current expected result on `main`: `PASS=24, FAIL=0`,
`COLOR_CORRECTION_FORCES_SQRT_65 = FALSE_BUT_NEAR`.

The runner checks:

- exact SU(3) Casimir identities (`C_F = 4/3`, `T_F = 1/2`, `C_A = 3`,
  `C_F - T_F = 5/6`, `R_conn = 8/9`)
- species-independent scalar dressing invariance of `Q` (Part B)
- exhaustive Casimir-ratio scan for the target `sqrt(6/5)` (Part C)
- symbolic circulant `(a, b)` structure and Koide cone solutions
  (Part D)
- observed `Q_d / Q_l` vs `sqrt(6/5)` and `Q_u / Q_l` vs `6/5` (Parts
  E and F)
- exact identity `(C_F - T_F)^(-1/4) = (6/5)^(1/4)` (Part G)
- predicted `Q_d` and `Q_u` under the dressing hypothesis (Part H)
- three-outcome verdict logic (Part I)
