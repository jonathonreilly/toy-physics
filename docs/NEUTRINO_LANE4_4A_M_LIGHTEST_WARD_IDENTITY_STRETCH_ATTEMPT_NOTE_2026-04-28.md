# 4A `m_lightest` via Neutrino-Yukawa Ward Identity — Stretch Attempt

**Date:** 2026-04-28
**Status:** retained branch-local **stretch-attempt** note on
`frontier/neutrino-quantitative-20260428`. Cycle 10 of the loop:
mandatory stretch attempt per Deep Work Rules audit-quota threshold.
Attempts 4A `m_lightest` absolute scale via a neutrino-Yukawa Ward
identity analogous to the retained YT-lane `y_t / g_s = 1/sqrt(6)`.
**Result:** no clean structural path on the current axiom set; the
neutrino sector lacks the gauge-coupling anchor that the YT-lane
identity rests on. Identifies two candidate alternative routes and
the structural premise each would require.
**Lane:** 4 — Neutrino quantitative closure (route 4A)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. First-principles reset (per Deep Work Rules)

### 0.1 `A_min`

Standard axioms 1-4 of `MINIMAL_AXIOMS_2026-04-11.md`:
1. `Cl(3)` local algebra
2. `Z^3` substrate
3. finite local Grassmann / staggered-Dirac partition
4. canonical normalization `g_bare = 1` + plaquette/u_0 + APBC

Plus the no-fitted-parameter posture (per Cycle 7 reasoning).

### 0.2 Forbidden imports

- no observed neutrino mass values (PDG / KATRIN / cosmological bounds)
- no oscillation-derived splittings
- no Schechter-Valle as derivation premise
- no fitted Yukawa coefficients

### 0.3 Goal

Derive `m_lightest` (the smallest active neutrino mass, equivalently
`m_1` in normal ordering) from `A_min` plus the retained Lane-4
content via a neutrino-Yukawa Ward identity, analogous to the
retained top-sector identity:

```text
y_t / g_s = 1/sqrt(6)   at lattice scale (M_Pl pin)              (YT)
```

per the YT theorem cluster.

`(YT)` plus retained `g_s` value gives `y_t` retained, hence
retained `m_t = y_t v / sqrt(2)` after running.

The neutrino analog would be:

```text
y_ν,1 / [some retained coupling]  =  [some structural constant]
```

with an analogous derivation pathway.

## 1. The retained YT-lane Ward identity structure

The YT-lane Ward identity rests on:

1. **Top-sector gauge content:** the top quark is `(3, 2, 1/3)`
   under `SU(3) × SU(2) × U(1)`, so couples to `g_s` (strong),
   `g_2` (weak), `g_1` (hypercharge).
2. **Yukawa coupling structure:** `y_t` couples the right-handed
   top to the left-handed quark doublet via the Higgs.
3. **Specific Ward identity:** `y_t / g_s = 1/sqrt(6)` arises from
   a specific combinatorial / representation-theoretic structure
   related to the color projection in the top sector.

The **anchor** is `g_s`: the identity expresses `y_t` as a
structural ratio relative to a separately-retained gauge coupling.

## 2. What the neutrino sector has — and lacks

The right-handed neutrino `ν_R`:

| Gauge content | `(1, 1, 0)` |
|---|---|
| `SU(3)` | trivial (color singlet) |
| `SU(2)` | trivial (weak singlet) |
| `U(1)_Y` | trivial (zero hypercharge) |

So `ν_R` carries **no gauge charges**. Consequently, **there is no
gauge coupling for `ν_R` to anchor a Ward identity to**.

This is qualitatively different from the top sector. The YT-lane
structure does not extend to the neutrino sector by analogy —
the neutrino simply doesn't have the gauge couplings the top has.

## 3. Three candidate alternative routes

### Route A — Lepton-sector y_τ analog with neutrino extension

**Premise:** if Lane 6 closes the `y_τ` Ward identity (the analog
target identified in `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md`
Lane 6 row: "full closure requires the absolute lepton scale `V_0`
via a `y_τ` Ward identity (analog of retained `y_t/g_s = 1/sqrt(6)`)"),
then the lepton-doublet structure shared between `τ_L` and `ν_L`
might extend to a neutrino-side identity.

**Why this might work:** `τ_L` and `ν_L` are both members of
`L_L = (ν_L, τ_L)^T`, the same lepton doublet. A `y_τ` Ward
identity that couples `τ_R`'s Yukawa to retained gauge couplings
could in principle generalize to `y_ν`'s Yukawa via the doublet
structure.

**Why it might not:** `τ_R` and `ν_R` are different right-handed
fields with different gauge content. `τ_R` has hypercharge `-1`,
`ν_R` has hypercharge `0`. The YT-lane identity rests on the
right-handed top's color triplet structure; the analog for `τ_R`
would rest on hypercharge structure; the analog for `ν_R` has
no analog gauge structure.

**Status:** depends on Lane 6's `y_τ` closure path, which is itself
open. If Lane 6 closes via a hypercharge-anchored identity, the
neutrino sector still lacks the anchor.

### Route B — Lepton-quark cross-sector identity

**Premise:** the framework's retained content already includes
the cross-sector CKM-Koide bridge identities (e.g.,
`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE`, etc.). A
similar cross-sector identity might exist between charged-lepton
Koide structure and neutrino-mass structure.

**What's available:** the charged-lepton Koide work (Lane 6) has
substantial recent activity. A retained Koide-style identity
`Q_l = 2/3` and `delta_l = 2/9` for the charged leptons would
constrain charged-lepton mass ratios; if a similar structure
applies to neutrinos, it could give mass ratios but not absolute
scales.

**Why mass ratios alone don't give `m_lightest`:** Koide-type
identities give ratios `m_e : m_μ : m_τ`. The absolute scale
requires a separate retention. So even a retained neutrino-Koide
analog would only give `m_1 : m_2 : m_3`, not `m_lightest`.

**Status:** would close 4B/4C splittings (which are mass ratios
through the seesaw or Dirac structure), not 4A absolute scale.

### Route C — Direct cosmological back-extraction from `Σm_ν`

**Premise:** the Cycle-9 Σm_ν cosmology bridge gives an explicit
structural relation:

```text
Ω_b (1 + R_base × S_corr) + Σm_ν / (93.14 eV h²) = 1 - L - R    (eq.10)
```

If `Ω_b`, `S_corr`, `L`, `R`, `h` are all retained, this gives a
single retained number `Σm_ν`. Combined with retained mass ratios
(Route B) and retained ordering (`Δm²_31 > 0` from oscillation
data — but observation, not retention), one could solve for
individual masses.

**What it requires:** retain `Ω_b` (= retain `eta` via DM-leptogenesis
lane), retain `S_corr` (= retain `α_GUT` via gauge-coupling
unification), retain `L` and `H_0` (= close Lane 5 itself per the
two-gate firewall), AND retain neutrino mass ratios.

This is essentially "retain everything else first, then `m_lightest`
follows arithmetically". It's a downstream cycle, not a primary 4A
attack.

**Status:** depends on retaining many other lanes first. Not a
stand-alone 4A route.

## 4. Synthesis: 4A is structurally distant from `A_min`

After this stretch attempt, the picture is:

| 4A route | Anchored on | Currently retained? | Distance to closure |
|---|---|---|---|
| Direct Ward identity (analog of YT-lane) | `g_s` (strong coupling) | n/a — `ν_R` has no gauge charges | NO ROUTE |
| Lepton-sector `y_τ` analog (Route A) | `y_τ` Ward identity from Lane 6 | open | 2+ lanes deep |
| Cross-sector Koide-type ratio (Route B) | charged-lepton Koide structure | open | 1+ lane deep, gives ratios only |
| Cosmological back-extraction (Route C) | `Ω_b` + `S_corr` + Lane 5 closure | open | 3+ lanes deep |

**Conclusion:** 4A `m_lightest` is the **most distant** Lane-4
sub-target from `A_min` retention. Direct attack via the YT-lane
analog fails because `ν_R` is gauge-singlet. Indirect attacks
(Routes A, B, C) all require closing other open lanes first.

## 5. What this stretch attempt closes and does not close

**Closes:**

- The direct YT-lane-analog attack on 4A is excluded — `ν_R`
  has no gauge charges, so no analog `y_ν / g = const` identity
  exists.
- 4A is structurally distant from `A_min`; 4A closure requires
  closing other open lanes first (Lane 6, gauge-coupling
  unification, Lane 5).
- Three alternative-route candidates (A, B, C) named with their
  specific premise dependencies.

**Does not close:**

- 4A itself.
- Any neutrino mass numerically.
- The alternative routes (A/B/C) — each remains a hypothetical
  research target dependent on other lanes.

## 6. Implications for the Lane-4 closure pathway

After Cycle 10:

- **4D Dirac global lift:** RETAINED on current axiom set
  (Cycles 2 + 6 + 7 + 8).
- **4F Σm_ν cosmology bridge:** structural coupling mapped
  (Cycle 9); numerical closure depends on `Ω_b` retention.
- **4A m_lightest:** structurally distant; requires closing other
  lanes first (this cycle's finding).
- **4E Dirac mass mechanism without seesaw:** open; smallness
  of `m_ν` without seesaw suppression is the structural question.
- **4B/C splittings:** would follow arithmetically from 4A + 4E.
- **4G cross-validation:** depends on having mass content to
  cross-check against retained `δ_CP`, `θ_23`.

So Lane 4's near-term productive work is **4D extensions**, not
4A pursuit. The remaining 4A/4E/4B/4C work depends on other
lanes' progress.

## 7. Recommendation: pivot the loop

Lane 4's natural Lane-4-internal claim-state movement is now
exhausted on the current axiom set:

- 4D landed (Cycles 2-8)
- 4F bridge mapped (Cycle 9)
- 4A structurally distant (this cycle, Cycle 10)
- 4B/C/E follow from 4A
- 4G is a downstream consistency check

Per the user's 10h plan in the loop prompt, the next iteration
should pivot to a fresh **Lane 6 charged-lepton mass retirement**
workstream. Lane 6 has overnight upstream progress and concrete
near-term targets (Koide closure with `Q = 2/3`, `δ = 2/9`; `y_τ`
Ward identity; absolute lepton scale `V_0`).

Lane 6 also has the strongest **cross-lane impact**: closing `y_τ`
opens Route A for 4A, and closing the absolute lepton scale opens
the analog for the neutrino carrier.

Recommended Cycle 11 actions:
1. Honest close-out of the neutrino loop (workstream-status note +
   updated PR_BACKLOG).
2. PR #113 already open; final commits land via the existing PR
   thread.
3. Open a fresh physics-loop on `frontier/charged-lepton-pickup-20260428`
   from current `origin/main` per the loop prompt's pivot
   instructions.

## 8. Cross-references

- Cycle 9 4F bridge:
  `NEUTRINO_LANE4_SIGMA_M_NU_COSMOLOGY_BRIDGE_NOTE_2026-04-28.md`.
- Cycle 8 manuscript-grade theorem:
  `NEUTRINO_DIRAC_GLOBAL_LIFT_CURRENT_AXIOM_SET_THEOREM_NOTE_2026-04-28.md`.
- YT-lane retained Ward identity:
  YT theorem cluster (e.g.,
  `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`).
- Lane 6 `y_τ` Ward identity target:
  `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md` Lane 6 row.
- Charged-lepton Koide work:
  `docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md` and
  cluster.
- Loop pack:
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.

## 9. Boundary

This is a stretch-attempt artifact under Deep Work Rules. It
**produces** an honest finding that 4A is structurally distant
from `A_min` via the direct YT-lane analog, with three named
alternative routes each depending on other open lanes. This is
valid stretch output per the no-churn exception.

A runner is not authored: the attempt is structural case-analysis
on the gauge-content of `ν_R` and on candidate alternative
identity paths. No new symbolic or numerical content is introduced.
