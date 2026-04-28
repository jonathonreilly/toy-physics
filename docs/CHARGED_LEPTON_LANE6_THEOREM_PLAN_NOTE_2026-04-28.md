# Lane 6 Charged-Lepton Theorem Plan: Closure Roadmap with Phase Ordering

**Date:** 2026-04-28
**Status:** retained branch-local theorem-plan note on
`frontier/charged-lepton-pickup-20260428`. Reduces Lane 6 (charged-
lepton mass retirement) to a sharp `m_e, m_μ, m_τ` closure roadmap
using retained gauge content + retained electroweak hierarchy `v` +
retained `y_t / g_s = 1/sqrt(6)` analog template + the Koide flagship
lane's in-flight Q/δ closures.
**Lane:** 6 — Charged-lepton mass retention (full closure)
**Loop:** `charged-lepton-pickup-20260428`

---

## 0. Statement

Lane 6 closure (retained absolute `m_e`, `m_μ`, `m_τ` derived from one
axiom — no PDG observational pin) decomposes into three orthogonal
sub-targets:

- **6A** Koide ratios closure (Q = 2/3, δ = 2/9): pins `m_e/m_μ/m_τ`
  ratios = direction of `v = (sqrt(m_e), sqrt(m_μ), sqrt(m_τ))` in
  R³, modulo overall scale. **In flight on Koide flagship lane.**
- **6B** Absolute lepton scale `V_0` via `y_τ` Ward identity (analog
  of retained `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)`). **Phase-1 priority
  of this loop.**
- **6C** Combined retention: 6A × 6B = retained absolute
  `m_e, m_μ, m_τ` from one axiom, retiring the 3-real PDG pin.

Per the lane file, 6A + 6B = 6C is automatic once both inputs land.
Lane 6's load-bearing single open number after 6A is `V_0` —
equivalently `y_τ` — equivalently `m_τ` retained.

This plan does not derive any charged-lepton mass; it produces the
structural roadmap.

## 1. Retained framework structure used

| Identity | Authority | Role in plan |
|---|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` | substrate |
| Three-generation matter structure (anomaly-forced + hw=1) | three-generation cluster | structural lift basis |
| `v = 246.282818290129 GeV` electroweak hierarchy | `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` | EW scale (ambient) |
| `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6)` exact lattice-scale Ward identity | YT theorem cluster | **analog template** for 6B |
| `m_t (pole) = 172.57 GeV` retained | YT/top transport lane | precedent for retained quantum-mass closure |
| `Cl(3)` bivector → `SU(2)` native gauge structure | retained gauge cluster | candidate `y_τ` anchor (R6) |
| Generation-color and EW A4 bridges (2026-04-25) | recent retained landing | structural support |
| `alpha_LM` geometric-mean identity | retained quantitative | cross-coupling structure |
| Recent SM gauge-cluster proofs (`SM_*_PROOF_2026-04-26`) | SM cluster | gauge-anomaly content |

## 2. The four derivation targets

### 2.1 Target 6A — Koide ratios `Q = 2/3` and `δ = 2/9`

**Identity:** the Koide formula

```text
Q := (m_e + m_μ + m_τ)² / [3 (m_e² + m_μ² + m_τ²)]   =   2/3      (Koide)
```

is the well-known dimensionless ratio. The framework's retention path
adds the structural δ = 2/9 companion identity. Together these pin
the direction of `v = (√m_e, √m_μ, √m_τ)` in R³ modulo overall scale.

**In flight.** The Koide flagship lane has substantial activity:
- April 21 package as authoritative support
- April 22 batch: A1 landscape audit; APS value `|η| = 2/9`
  Lefschetz/spectral-flow support; selected-line Brannen geometry;
  Callan-Harvey anomaly-descent candidate; Yukawa Casimir + BZ
  cross-check
- April 24 native-dimensionless packet + Round-10 fractional-topology
  no-go probes
- April 27 OP-locality / C3-fixed source route landed as conditional
  support

**Approachability per lane file:** Tier A-B; Q closure proceeds via
source-domain selector theorem; δ closure via period convention /
Euclidean rotation interpretation.

### 2.2 Target 6B — `y_τ` Ward identity (Phase-1 priority)

**Goal:** construct a structural Ward identity for the τ-Yukawa,
analogous to the retained YT-lane identity `y_t(M_Pl)/g_s(M_Pl) =
1/sqrt(6)`.

**Anchor candidates** (per route portfolio):
- (R6) `SU(2)` weak coupling `g_2`: tau is in the lepton doublet
  `L_L = (ν_L, τ_L)^T`. Try `y_τ / g_2 = const` structural identity.
  **Most promising single-cycle attack** (next cycle target).
- (R7) `U(1)_Y` hypercharge `g_1`: `τ_R` has hypercharge -1.
  Try `y_τ / g_1 = const`. Plausible but YT-lane analogy weakest.
- (R8) Combined SU(2)×U(1) doublet structural anchor.
- Koide-structural anchor: use the Q=2/3 combinatorial structure
  to anchor `y_τ` via the lepton mass ratio + ambient `v` scale.
- Non-gauge structural anchor (representation-theoretic).

**Approachability per lane file:** Tier A-B; "1-3 months of focused
work on existing Ward-identity scaffolding".

### 2.3 Target 6C — Absolute lepton scale `V_0`

**Identity:** once 6B lands, with retained `y_τ` and retained `v`:

```text
V_0  :=  v / sqrt(2) × y_τ      ⇒      m_τ = V_0                  (V_0)
```

i.e., `m_τ` retained. With Koide ratios retained (6A), all three
`m_e, m_μ, m_τ` retained, and the 3-real PDG pin is retired.

**Approachability:** Tier A. Automatic chain once 6A and 6B land.

### 2.4 Target 6D — Cross-lane impact

If 6B lands, what's the cross-lane impact? Three potential
extensions:

- **4A neutrino Route A:** the neutrino-Yukawa Ward identity
  attempted by analogy. Per neutrino loop's Cycle 10 stretch-attempt
  finding, `ν_R` is gauge-singlet so direct YT-anchor analog doesn't
  extend; but if `y_τ` Ward identity is anchored on a **non-gauge**
  structural element (e.g., Koide-structural), an analog might
  extend to ν.
- **Lane 2 atomic-scale:** atomic-scale predictions per Lane 2 lane
  file gate on absolute lepton scale `V_0`. With 6B landed, Lane 2
  unblocks Phase-1.
- **Hadron mass sector (Lane 1):** charged-lepton structural
  identity may inform analog quark-lepton symmetry constraints.

**Approachability:** Tier A audits.

## 3. Closed-route inventory (extensive)

The recent (2026-04-26/27) cluster + older Koide (2026-04-15 through
2026-04-24) cluster establish ~15+ closed routes (per
`NO_GO_LEDGER.md`):

- direct Ward-free Yukawa (April 26 audited_clean)
- type-B radian readout generation selectors
- selected-line generation selectors
- Koide-ratio source-selector firewall
- radiative tau selector firewall
- A1 fractional topology / Cheeger-Simons / RZ
- Wilson selected-eigenline delta
- marked relative cobordism delta
- readout-retention split / residual-cohomology obstruction
- onsite source-domain
- Q23 Oh covariance
- selected-line local radian bridge
- selected-slice spectral completion / minimal-local-spectral-law
- transport gap constant
- Z3 qubit radian bridge

**Implication for this loop:** new cycles must avoid all of these.
Specifically: the "direct Ward-free Yukawa" no-go closes the easy
route 6B (= "just write down a Ward identity for `y_τ`"). The
surviving 6B route must explicitly leverage the gauge structure
(`g_2` or `g_1` anchor) — that's what distinguishes it from the
closed direct-Ward-free attempt.

## 4. Phase ordering

### Phase 1 (now, parallel work)

1. **6A Koide ratios closure** — flagship lane, in flight.
   This loop watches but does not duplicate.
2. **6B y_τ Ward identity construction** — this loop's Phase-1
   priority. Cycle 2 = stretch attempt, anchor on `g_2` (R6).

### Phase 2 (after Phase 1)

3. **6C V_0 absolute scale** — automatic chain once 6A + 6B land.
4. **6D cross-lane impact study** — audit-grade, can run in parallel.

### Phase 3 (after Phase 2)

5. **Manuscript-grade consolidation** of 6A + 6B + 6C → retained
   absolute `m_e, m_μ, m_τ` from one axiom.
6. **Atlas integration** — retire the 3-real PDG pin from
   `INPUTS_AND_QUALIFIERS_NOTE`; update `CLAIMS_TABLE`.

## 5. Stretch-attempt candidates (per Deep Work Rules)

If audit-quota threshold hits:
- **(SA-A) y_τ Ward identity from g_2 anchor:** Cycle 2 primary
  attempt.
- **(SA-B) y_τ Ward identity from g_1 anchor:** fallback.
- **(SA-C) Koide-structural y_τ anchor:** use Q=2/3 combinatorial
  structure to construct the identity without a gauge coupling.
- **(SA-D) Lepton-quark cross-sector y_τ identity:** leverage
  recent retained generation-color and EW A4 bridges.

## 6. What this plan closes and does not close

**Closes (claim-state movement):**

- Lane 6 closure roadmap with phase ordering.
- Cleanest Phase-1 single-cycle target identified as 6B (R6 g_2
  anchor first).
- Stretch-attempt candidate inventory (SA-A through SA-D).
- Closed-route inventory cross-referenced.
- Cross-lane impact map (4A neutrino, Lane 2 atomic, Lane 1 hadron).

**Does not close:**

- Any charged-lepton mass numerically.
- 6A Koide ratios (flagship lane in flight; not duplicated here).
- 6B y_τ Ward identity (Cycle 2 attempt).
- The cross-lane impact studies.

## 7. Falsifier

This plan is structural; not a numerical claim. Falsified if a
Phase-2 derivation succeeds without retaining one of the listed
prerequisites, or if Lane 6 lands via a different methodology not
enumerated here.

## 8. Cross-references

- `docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md`
  — Lane 6 lane file (primary authority).
- `docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md` — Koide
  flagship lane authority.
- YT theorem cluster (analog template for 6B).
- `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
  (direct Ward-free Yukawa closed; 6B route must use gauge anchor).
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — `A_min`.
- `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
  — neutrino lane (4A Route A is potential cross-lane extension of 6B).
- Loop pack at
  `.claude/science/physics-loops/charged-lepton-pickup-20260428/`.

## 9. Boundary

This is a structural plan, not a theorem. It does not retire any
input, does not promote any claim, and does not duplicate the
in-flight Koide flagship lane. It produces the loop's Phase-1
roadmap focused on 6B `y_τ` Ward identity construction.

A runner is not authored.
