# Scalar-Selector Synthesis

**Date:** 2026-04-19
**Scope:** Publishable synthesis of four Tier-1 Standard Model
scalar-selector gates: Koide `kappa`, Koide doublet-phase (Koide
`theta`), Quark up-amplitude `a_u`, DM A-BCC basin.

**Status.** This note now serves as **route-history and internal synthesis**,
not the current reviewer-facing claim surface. The honest read after the
science review plus the later meta-closure pass is:

- at the **reviewer bar**, MRU, Berry, DPLE, and RPSR/STRC remain
  support/conditional routes rather than full object-derivation closures;
- at the **meta-axiom layer**, the strongest current compression is
  `4 -> 2` via **DIM-UNIQ + STRC**, not `4 -> 0`;
- a named future target (**BACT**, the bimodule amplitude-completeness
  theorem) sharpens the remaining quark-side structural gap but does not erase
  the per-lane object-derivation issue by itself.

**Reading order.** Read
`docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md` first,
then
`docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md`,
then use this note for the branch-local candidate-route logic in §2-§9.

---

## §1 Tier-1 gate landscape

The framework's Tier-1 Standard Model gate closure requires four
scalar selections:

| Gate | Content | Status |
|---|---|---|
| **Koide `kappa`** | Charged-lepton cone normalization `kappa = 2` | Support/candidate principle via **MRU** |
| **Koide `theta`** | Doublet-phase offset `delta = 2/9` (Brannen–Zenczykowski) | Geometric support/candidate via **Berry holonomy** |
| **DM A-BCC basin** | Interior-minimum linear-path Sylvester discriminator `F_4` | Support theorem on the fixed DM chart via **DPLE** |
| **Quark `a_u`** | Up-sector reduced amplitude `a_u = 0.7748865611` | Conditional support via **RPSR** + **STRC observable principle** |

§2 presents the four branch-local routes; §3 presents STRC; §4 records the
later meta-closure compression (`DIM-UNIQ + STRC`); §5 separates
meta-axiom accounting from reviewer-bar accounting; §6 names the future target
BACT.

---

## §2 Four branch-local routes

### §2.1 Moment-Ratio Uniformity (MRU) — candidate route to Koide `kappa`

On the Hermitian circulant algebra `Herm_circ(d)` with Frobenius
metric, the MRU principle requires Frobenius-normalized cyclic
responses to be uniform across Z_d isotypes. At `d = 3` this is a
single equation equivalent to `a^2 = 2|b|^2` on
`H = aI + bC + b^bar C^2`, i.e. `kappa = 2`.

Dimensional uniqueness: MRU has a single non-trivial
singlet-vs-doublet scalar selector iff `|Iso(d)| = 2` with one singlet
+ one complex doublet, which holds iff **`d = 3`**.

See `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=65 FAIL=0.

### §2.2 Berry-phase theorem on `S^2_Koide` — candidate route to Koide `theta`

The projectivized Koide cone `S^2_Koide` carries a natural `C_3`
action. The `n = 2` monopole line bundle `L_doublet` (first Chern
number `= dim(doublet) = d - 1 = 2` at `d = 3`) has Berry holonomy

    gamma(one C_3 period)  =  2 pi (d - 1) / d  =  2 pi Q.

At `d = 3`: `gamma = 4 pi / 3`. Reduction to Brannen units per `C_3`
element:

    delta_d  =  Q / d  =  (d - 1) / d^2    (at d = 3: 2/9 exactly).

This gives `cos(3 arg b_s) = cos(Q)` — the Brannen–Zenczykowski
doublet-phase identity — as a corollary.

See `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`. Runner
PASS=26 FAIL=0. Literature alignment: Brannen 2006, Zenczykowski PRD
2012/2013.

### §2.3 Dim-Parametric log|det| Extremum (DPLE) — support theorem on `F_4`

On the retained linear Hermitian pencil `H(t) = H_0 + t H_1`, the
observable `W(t) = log|det H(t)|` has at most `floor(d/2)` interior
Morse-index-0 critical points. At `d = 3` this is exactly 1 — a clean
binary selector. `F_3` on the retained DM A-BCC pencil
(`H_0 = H_base`, `H_1 = J_*`) reproduces `F_4` on all four basins
`{1, N, P, X}`.

`d = 3` uniqueness: clean binary selector iff `d = 3`; `d = 2`
degenerate; `d >= 4` fragments (explicit `d = 4` example with 2
interior Morse-idx-0 CPs). Uhlig 1982 sign-characteristic
classification provides the dim-parametric backbone.

Same-day source-side tightening: the current branch discriminator on the DM
route is already an exact local scalar of the descended charged Schur block,

```text
Delta_src(dW_e^H) = det(H_e(L_e)),
```

with `H_e(L_e) = Herm(L_e^(-1))`, and that sign is invariant under ambient
Wilson completions once `L_e` is fixed. So the open DM source-side object is
now the finer sign law on `L_e` itself, not a vague chart-choice placeholder.
See
`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`.

See `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=19 FAIL=0.

### §2.4 Reduced Projector-Ray Sum Rule (RPSR) — conditional route to Quark `a_u`

On the 1 (+) 5 CKM projector ray
`p = cos(delta_std) + i sin(delta_std)`,

    a_u / sin(delta_std)  +  a_d  =  1 + a_d * supp * delta_A1  =  1 + rho / 49.

The derivation uses four retained ingredients: unit ray `|p|^2 = 1`,
scalar-tensor bridge `supp = 6/7`, `a_d = rho`, and `delta_A1 = 1/42`.
The NLO excess `rho / 49` is the unique minimal 3-atom contraction on
`{rho, supp, delta_A1}`.

**Conditional on STRC** (§3):

    [LO closure]  a_u + rho * sin(delta_std) = sin(delta_std).

See `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=10 FAIL=0.

---

## §3 STRC observable principle — Koide-analog on CKM

The linear amplitude sum rule on the CKM 1(+)5 projector ray:

    a_u  +  rho * sin(delta_std)  =  sin(delta_std)                    (STRC-LO)

equivalently (geometric form):

    a_u  =  Im(p) * (1 - Re(r))  =  sin(delta_std) * (1 - rho),

where `r = rho + i eta = p / sqrt(7)` is the scalar-comparison ray
collinear with `p`.

**Koide-analog epistemic footing.** STRC is to CKM reduced
amplitudes what the Koide sum rule is to charged-lepton sqrt-masses:
a single linear scalar relation retained as an observable principle
rather than derived from symmetry or quadratic unitarity.

| Principle | Sector | Form |
|:---|:---:|:---:|
| Koide | Charged-lepton sqrt-masses | `(sum m) / (sum sqrt(m))^2 = 2/3` |
| STRC | CKM reduced amplitudes | `a_u + rho * sin_d = sin_d` |

**SM-native derivations surveyed and do not close STRC.** Six named
candidate sources were systematically checked:

1. EW-charge asymmetry — side identity `Q_u^2 + Q_d^2 = (2/3) sin^2_d`
   but not STRC.
2. 1(+)5 block factor — cross-link `6 rho = sqrt(supp)` but no linear
   STRC closure.
3. Row-unitarity NLO — scale mismatch ~1000x.
4. Discrete flavor groups — `a_u` is in framework-block algebra
   `Q[sqrt(5), sqrt(7)]`, not in small-group character rings.
5. Anomaly cancellation — SM anomalies cancel; side identity
   `3/4 + 1/12 = sin^2_d` is a mnemonic.
6. Clifford bimodule (quadratic) — `|p|^2 = 1` is quadratic, does not
   force linear STRC.

A literature survey (QLC, Koide extensions, Froggatt-Nielsen, SO(10)
sum rules) also does not produce STRC. Retention of STRC as an
observable principle is the minimal-cost path.

**Scenario A bundling (recommended).**
`QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` already retains
`a_d = rho`. STRC bundles: the single reduced-amplitude retention is
upgraded to "STRC fixes both `a_u` and `a_d`." Net axiom cost across
the investigation is approximately 1 observable principle.

See `docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`. Runner
PASS=19 FAIL=0.

---

## §4 Meta-structural picture

### §4.1 DIM-UNIQ compresses the MRU/Berry/DPLE routes

The three non-quark routes (MRU, Berry, DPLE) share a common structural
pattern:

- Each states a **dim-parametric principle** at arbitrary `d >= 2`.
- Each reduces at **`d = 3`** to the retained framework content.
- Each has **at most one** non-trivial specialization (MRU:
  1-equation singlet-vs-doublet; Berry: unique Chern class
  `= dim(doublet)`; DPLE: at most one interior Morse-idx-0 CP).
- Each is **non-trivial at other `d`** (fragmentation at `d >= 4`;
  degeneracy at `d = 2`).

This is the **DIM-UNIQ** fingerprint: a single dim-uniqueness pattern
manifested across three independent route constructions. At the
meta-closure layer, these three routes compress to one meta-axiom.

`d = 3` itself is already retained on `main` via several independent
routes:

- `docs/DIMENSION_SELECTION_NOTE.md` (`d >= 3` lower bound);
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` (`d_t = 1`, `d_s` odd);
- `docs/3D_CORRECTION_MASTER_NOTE.md` (`d <= 3` via Bertrand /
  atomic);
- `.claude/science/derivations/cl3-minimality-conditional-support-2026-04-17.md`
  (R1, R2, R3 at SUPPORT);
- `.claude/science/derivations/native-su2-tightness-forces-ds3-2026-04-17.md`
  (alt route).

### §4.2 STRC is the separate quark-side meta-axiom

The fourth gate (Quark `a_u`) is not captured by the dim-uniqueness
pattern above. Instead it is isolated by a **scalar amplitude sum rule
on a retained specific ray** — a linear relation of a structurally
different type from the three dim-parametric routes.

**STRC is the Koide-analog for CKM.** Koide retains a linear scalar
relation on charged-lepton sqrt-masses; STRC retains a linear scalar
relation on CKM reduced amplitudes. Both live on a specific retained
ray in their respective sectors; both are on equal epistemic footing
as observable principles.

---

## §5 Honest accounting: meta-axioms vs reviewer bar

Two different accounting layers must be kept separate.

### §5.1 Meta-axiom accounting

At the branch's internal structural layer, the strongest honest
compression is:

- **DIM-UNIQ** for MRU + Berry + DPLE
- **STRC** for the quark LO balance

So the current meta answer is **`4 -> 2`**, not `4 -> 0`.

| Scenario | Meta-axiom status | Outcome |
|:---|:---|:---|
| A (current honest read) | `DIM-UNIQ + STRC` | `4 -> 2` |
| B (alternate packaging) | standalone route descriptions | `4 -> 4` |
| C (future target) | derive STRC via BACT / ray-saturation | sharper meta-closure than A, but still not reviewer-grade by itself |

### §5.2 Reviewer-bar accounting

At the reviewer's object-derivation bar, the current branch remains a
support/conditional packet:

- MRU restates the missing charged-lepton scalar law but does not derive why
  the physical carrier satisfies it;
- Berry gives a coherent geometric model but does not force the physical
  charged-lepton phase to be that holonomy;
- DPLE upgrades `F_4` to a real theorem on the fixed chart but does not derive
  the physical source-side chart by itself;
- STRC remains an observable principle and RPSR remains conditional on it.

So the current reviewer-grade answer is still: **no full gate is closed on
this branch yet**.

## §6 Future target — BACT / bimodule ray-saturation theorem

If the following target is proven, STRC becomes a derived theorem
at the meta-closure layer. That would improve the branch's axiom
accounting, but it still would not by itself erase the per-lane
object-derivation gap identified in the science review.

**Ray-saturation theorem (target).** On the Clifford bimodule

    M_CKM  =  Cl(3) / Z_3  (x)  Cl_CKM(1 (+) 5),

prove that bimodule unitarity + scalar-tensor support bridge
`supp = 6/7` + democratic center-excess `delta_A1 = 1/42` jointly
force STRC-LO.

**Significance.** If proven, the quark-side linear-amplitude gap is no
longer carried as a separate observable principle. The meta-closure
picture tightens, but reviewer-grade closure still also requires the
lane-specific object derivations.

**Approach directions (not validated).**

1. Frobenius-type scalar-tensor duality using cross-link
   `6 rho = sqrt(supp)`.
2. Anomaly inflow on the bimodule (bimodule-internal, not SM-level).
3. Bimodule unitarity + democratic center-excess saturation at
   `supp * delta_A1 = 1/49`.
4. Representation-theoretic matching at specific bi-isotypes.
5. RG flow fixed point on reduced amplitude space.

See `docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`.

No retention is claimed for this target.

---

## §7 Literature alignment

- **MRU**: Maschke decomposition for cyclic groups; Frobenius metric
  standard on `M_d(C)`.
- **Berry phase**: Brannen 2006 MASSES2.pdf; Zenczykowski PRD 86
  (2012) 117303; PRD 87 (2013) 077302; Rivero-Gsponer
  hep-ph/0505220. The two-decade phenomenological `delta = 2/9` is
  now derived.
- **DPLE**: Uhlig 1982 (Linear Algebra Appl. 46),
  sign-characteristic classification for Hermitian pencils;
  Mehl–Mehrmann–Ran–Rodman 2016 (Linear Algebra Appl. 511)
  generalization; Milnor Morse Theory 1963. Uhlig 1982 is the
  structural backbone for DPLE at `d = 3`.
- **RPSR**: standard CKM atlas + Schur cascade; Wolfenstein
  parametrization; retained scalar-comparison geometry.
- **STRC**: Koide-analog linear amplitude sum rule; novel on the
  CKM projector ray (not present in QLC, Froggatt-Nielsen, SO(10)
  sum-rule literature).
- **Clifford-algebra ↔ exterior-algebra equivalence** (`Cl ≅ Λ`):
  standard under the retained Z_d-reduced convention used throughout.

---

## §8 Reading order

Start here, then (in order):

1. `SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md` —
   current science verdict on the branch routes.
2. `SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md` —
   later same-day `4 -> 2` meta-closure update.
3. `KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` — shared
   `C_3` isotypic decomposition (scaffolding).
4. `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
   — axiom-native "2" + cone normalization pieces.
5. `KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` — MRU.
6. `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — Berry-phase.
7. `DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
   — DPLE.
8. `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md` — `supp`
   bridge.
9. `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
   — RPSR.
10. `QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md` — STRC.
11. `CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`
   — future target (optional).

### Runners

| Runner | PASS | FAIL |
|---|---|---|
| `frontier_koide_z3_joint_projector_identity.py` | 55 | 0 |
| `frontier_koide_kappa_two_orbit_dimension_factorization.py` | 26 | 0 |
| `frontier_koide_moment_ratio_uniformity_theorem.py` | 65 | 0 |
| `frontier_koide_berry_phase_theorem.py` | 26 | 0 |
| `frontier_dm_dple_theorem.py` | 19 | 0 |
| `frontier_quark_up_amplitude_rpsr_conditional.py` | 10 | 0 |
| `frontier_quark_strc_observable_principle.py` | 19 | 0 |

No retained runner on `main` regresses.

---

## §9 Honest branch claim

> This branch contributes four mathematically meaningful scalar-selector
> routes, but on the current evidence it remains a **support/conditional
> packet**, not a full gate-closure packet. The strongest later same-day
> compression is meta-structural: MRU, Berry, and DPLE fit one
> dim-uniqueness pattern (DIM-UNIQ), while the quark LO balance isolates one
> separate observable principle (STRC), giving an honest `4 -> 2`
> meta-closure. The remaining sharp future target is the bimodule
> amplitude-completeness / ray-saturation theorem (BACT), together with the
> still-open per-lane object-derivation work needed to clear the reviewer's
> bar.
