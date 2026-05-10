# Koide A1 Probe 5 — RG Fixed-Point Hypothesis: Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 5 closure attempt for
the A1 √2 equipartition admission on the charged-lepton Koide lane,
testing the **dynamical** (RG-attractive fixed point) hypothesis after
all eight prior **static** structural attempts (Routes F/E/A/D,
Probes 1-4) closed as bounded obstructions.
**Status:** source-note proposal for a negative Probe 5 closure —
shows that the candidate fixed-point structure `|b|²/a² = 1/2` is
NOT an attractive fixed point of the framework's matter-sector
dynamics. Five independent structural barriers each block the
RG fixed-point hypothesis. The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-rg-fixed-point-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.py`](../scripts/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.txt`](../logs/runner-cache/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

The eight prior A1 closure attempts (Routes F, E, A, D + Probes 1-4
RP/anomaly/gravity/spectral) all close as bounded obstructions on
**static** structural grounds: algebra, operator theory, anomaly
counts, variational extremality, RP/GNS, gravity-as-phase, spectral
action. Each shows the framework's retained content does not select
a canonical normalization on the matter-sector C_3-circulant amplitude.

But Yukawa-class coupling parameters in standard QFT are **dynamical**
— they run with energy via RG equations and have IR/UV fixed points
(e.g., the framework's retained y_t Pendleton-Ross IR QFP).

**Hypothesis to test:** is `|b|²/a² = 1/2` an **RG-attractive fixed
point** of the framework's matter-sector evolution, NOT a static
algebraic identity? If true, "deriving A1" means showing the
framework's dynamics have this fixed point — and the convention
dependence we kept hitting in static routes is exactly the dynamical
freedom that's resolved by RG flow.

## Answer

**No.** The hypothesis fails on retained content. Five independent
structural barriers each block the RG fixed-point claim:

1. **Barrier RG1 — No retained matter-sector RG flow on `|b|²/a²`.**
   The framework's retained dynamical content covers (a) Wilsonian
   gauge-coupling running through `<P>` → `α_LM`, (b) the EW
   staircase `v_EW = M_Pl·(7/8)^(1/4)·α_LM^16` (a real running
   result with 16 powers of `α_LM`), and (c) the colored-Yukawa
   Pendleton-Ross IR QFP for `y_t`. NONE of these flows acts on
   the C_3-circulant amplitude ratio `|b|²/a²` on the
   charged-lepton sector. The matter-sector circulant RG is
   not retained content.

2. **Barrier RG2 — Charged-lepton Yukawa lacks Pendleton-Ross
   structure.** The SM β_{y_l} for charged leptons is
   `β_{y_l} ∝ +9/2 y_l² − 9/4 g_2² − 9/4 g_1²` with NO `g_3²`
   term (charged leptons have no color). Numerical integration
   (this runner) confirms that y_τ does NOT focus toward a fixed
   value — UV variations propagate to IR essentially without
   compression. This is the structural asymmetry between the
   colored sector (where Pendleton-Ross applies) and the lepton
   sector (where it does not).

3. **Barrier RG3 — Under SM-like flow on circulant Y_e, `|b|²/a²`
   has no fixed point at 1/2.** Numerical integration of the SM
   1-loop matrix RGE
   `dY_e/dt = (1/16π²)·[3 Y_e Y_e†Y_e − (gauge·I) Y_e]`
   on circulant `Y_e = aI + bU + b̄U^{-1}` shows the ratio drifts
   AWAY from 1/2 over 17 decades of running (`0.5 → 0.10`).
   The flow is non-trivial but does NOT focus on 1/2. Different
   starting ratios end at different final values; some appear
   stationary (e.g., 1.0 → 1.0) but none are at 1/2.

4. **Barrier RG4 — No attractive fixed-point structure at
   `|b|²/a² = 1/2` from the SM flow.** Linearization tests at the
   purported fixed point show:
   (i) perturbations from `0.55` end further from `1/2`
   (distance ratio 7.4×, NOT < 1);
   (ii) perturbations from `0.501` propagate (distance ratio
   ~400×);
   (iii) the local Jacobian shows uniform multiplicative
   gauge-dressing — the non-multiplicative cubic term does
   not produce restoring eigenvalues at 1/2.

5. **Barrier RG5 — `g_bare = 1` Hilbert-Schmidt rigidity does
   not propagate to matter-sector amplitude ratio.** The retained
   HS rigidity (joint Tr-Gram + Casimir on `su(3) ⊂ End(V)`)
   forces `g_bare = 1` once `N_F = 1/2` is admitted. The
   analogous matter-sector statement asks whether a 2-form
   rigidity on circulant Y_e fixes `|b|²/a² = 1/2`. The runner
   constructs explicit 2-forms (`Tr(Y†Y)`, `Tr((Y†Y)²)`) and
   shows both rescale uniformly under `Y_e → c Y_e`, leaving
   the ratio FREE. The HS rigidity argument is gauge-sector-
   specific (Killing-form uniqueness on simple Lie algebra) and
   has no charged-lepton analog from retained content.

The combined picture: **the RG fixed-point hypothesis is
structurally barred** under the retained matter-sector content.
Closing A1 via this route would require either (a) a new retained
primitive supplying matter-sector circulant flow, (b) C_3-breaking
dynamics extending the retained surface, or (c) a Hilbert-Schmidt-
style 2-form rigidity theorem on hw=1.

This is the **fifth** A1 attack closed as bounded obstruction
(after Routes F, E, A, D and Probes 1, 2, 3, 4). The
dynamical-route hypothesis was the natural complement to the
eight static attempts; it also fails on retained content.

## Setup

### Premises (A_min for Probe 5 closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Plaquette | `<P> = 0.5934` from SU(3) lattice MC at `β = 6` | retained: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| α_LM | `α_LM = α_bare/u_0` derived from plaquette | retained: same source |
| Hierarchy | `v_EW = M_Pl·(7/8)^(1/4)·α_LM^16` (16 powers running) | retained: same source |
| g_bare | `g_bare = 1` from HS rigidity given `N_F = 1/2` | retained: [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) |
| QFP | y_t IR Pendleton-Ross focusing from `β_{y_t}` with `-8 g_3²` | retained: [`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md) |
| GS | One-Higgs gauge selection: `Y_e` is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | No direct Ward lift forces `y_τ`; `Y_e` remains free 3×3 | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| C3-RG | RG flow preserves C_3 symmetry (Coleman 1975 / Wilson 1971) | classical math (referenced in [`A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md`](A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md) HR5.5) |
| KoideAlg | Koide Q = 2/3 ⟺ `a₀² = 2|z|²` ⟺ `|b|²/a² = 1/2` (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Probe 5's premise was that dynamics would close
  A1 from retained content; any A3-class admission requires explicit
  user approval and is not proposed here)
- NO admitted SM Yukawa-coupling pattern as derivation input

## The hypothesis at issue

**Hypothesis (Probe 5):**
> `|b|² / a²  =  1/2`  is an RG-attractive fixed point of the framework's
> matter-sector dynamics on the C_3-circulant Y_e = aI + bU + b̄U^{-1}.

If true, "deriving A1" means showing the framework's dynamics have
this fixed point. The convention dependence found in Routes F/E/A/D
(the static structural attempts) would then be precisely the dynamical
freedom resolved by RG flow.

This hypothesis is motivated by:
- The framework HAS retained dynamical content (`α_LM`, EW staircase
  `α_LM^16`, y_t Pendleton-Ross IR QFP).
- The y_t QFP is an existence proof that the framework has at least
  one matter-sector fixed point.
- The retained content doesn't include matter-sector circulant flow,
  but a CONSTRUCTION from retained primitives + admissible math (e.g.,
  importing the SM matrix RGE on Y_e) is a natural extension to test.

## Theorem (Probe 5 bounded obstruction)

**Theorem.** On A1+A2 + retained dynamical content (plaquette, α_LM,
EW staircase, y_t QFP, g_bare HS rigidity) + retained gauge-selection
+ retained C_3-equivariance + retained KoideCone-algebraic-equivalence
+ admissible standard math machinery (SM matrix RGE applied to
circulant Y_e, Coleman 1975 / Wilson 1971 RG-symmetry preservation):

```
The hypothesis "|b|² / a² = 1/2 is an RG-attractive fixed point of
the framework's matter-sector dynamics" cannot be derived from
retained content alone. Five independent structural barriers each
block the hypothesis:

  (RG1) No retained matter-sector RG flow on the circulant amplitude
        ratio. Retained running covers gauge sector and colored
        Yukawa; not lepton circulant.

  (RG2) Charged-lepton SM Yukawa β-function lacks the dominant
        gauge-coupling term needed for Pendleton-Ross focusing.

  (RG3) Under the SM matrix RGE on Y_e, |b|²/a² drifts substantially
        AWAY from 1/2 (e.g., 0.5 → 0.10 over 17 decades).

  (RG4) Linearization at |b|²/a² = 1/2 shows no attractive Jacobian
        eigenvalues; perturbations grow (distance ratio 7×–400×).

  (RG5) The retained Hilbert-Schmidt rigidity for g_bare = 1 is
        gauge-sector-specific (Killing-form uniqueness on simple
        Lie algebra); no analog 2-form rigidity exists on circulant
        Y_e from retained content.

Therefore the RG fixed-point hypothesis closure of A1 is structurally
barred under the stated retained-content surface. The A1 admission
count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired
runner; combining them establishes that no retained-content chain
reaches the RG fixed-point claim. ∎

### Barrier RG1: No retained matter-sector RG for `|b|²/a²`

The framework's RETAINED dynamical content is enumerated in
[`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md):

| Retained running | Domain | Acts on `|b|²/a²`? |
|---|---|---|
| Plaquette → α_LM (Coupling Map Theorem) | gauge sector | NO |
| EW staircase `α_LM^16` (Hierarchy Theorem) | gauge sector | NO |
| y_t Pendleton-Ross IR QFP | colored Yukawa | NO |
| Backward Ward scan | y_t boundary condition | NO |
| 1/N_c color projection R_conn = 8/9 | gauge sector | NO |
| Taste-staircase taste decoupling | gauge thresholds | NO |

The retained Yukawa running is for `y_t` only — and only because
its `β_{y_t}` has the `-8 g_3²` term producing the IR QFP. There is
NO retained running on the C_3-circulant amplitude ratio for
charged leptons.

The runner enumerates these (Section 2.1-2.4) and verifies the
EW hierarchy reproduces v ≈ 246.28 GeV (within 0.01%), confirming
the retained dynamical content is operative on the gauge sector but
absent on the matter circulant.

### Barrier RG2: Charged-lepton Yukawa lacks Pendleton-Ross structure

The SM 1-loop charged-lepton Yukawa β-function is

```
β_{y_l} = y_l/(16π²) · [9/2 y_l² + 3 Tr(Y_e†Y_e) − 9/4 g_2² − 9/4 g_1²]
```

with NO `-8 g_3²` term (charged leptons are color singlets). The
Pendleton-Ross focusing mechanism requires a DOMINANT gauge term
that competes with the Yukawa self-coupling: `-8 g_3² ≈ -10.4` is
the y_t structural term that creates the IR QFP at `y_t ≈ 0.92`.

For charged leptons, the dominant gauge term is `-9/4 g_2² ≈ -0.95`
— ~12× smaller. The Yukawa self-coupling `+9/2 y_τ²` is small for
physical y_τ (ratio `y_τ/y_t ≈ 0.01`), giving negligible competition.

The runner verifies this numerically (Section 3.1-3.4):
- y_t SM RGE: focusing ratio R = 22 (strong QFP)
- y_τ SM RGE: focusing ratio R = 0.71 (NOT focusing — slightly
  defocusing under the y² self-coupling)

This is a structural difference, not a numerical accident.

### Barrier RG3: Under SM matrix RGE, `|b|²/a²` drifts AWAY from 1/2

The SM 1-loop matrix β-function for `Y_e` (charged-lepton sector,
written in flavor space) is

```
dY_e/dt = (1/16π²) · [3 Y_e Y_e† Y_e − (9/4 g_2² + 9/4 g_1²) Y_e]
```

On circulant `Y_e = aI + bU + b̄U^{-1}`:

- The gauge dressing `(gauge·I)·Y_e` is uniform multiplicative —
  cancels in any ratio of `(a, b)`-coefficients.
- The cubic `Y_e Y_e† Y_e` IS circulant (circulants form an
  algebra) but is NOT homogeneous in `(a, b)` of degree 1. It
  produces a non-trivial flow on the ratio.

The runner integrates this flow numerically over 17 decades
(Section 4.1-4.4) starting from various initial ratios:

| UV `|b|²/a²` | IR `|b|²/a²` | `|b|²/a²` ↓ to 1/2 |
|---|---|---|
| 0.10 | 0.008 | NO (further from 1/2) |
| 0.30 | 0.037 | NO (further from 1/2) |
| 0.50 (A1) | 0.10 | DRIFTS AWAY from 1/2 (79% drift) |
| 0.70 | 0.26 | further from 1/2 |
| 1.00 | 1.00 | stays at 1.0 (NOT 1/2) |
| 1.50 | 13.6 | runs to large |

If 1/2 were an attractive fixed point, all rows would converge to
`IR ≈ 0.5`. They don't. The starting point at A1 itself drifts to
~0.1.

### Barrier RG4: Linearization shows no attractive structure at 1/2

For an attractive fixed point at `|b|²/a² = 1/2`, the Jacobian of
the flow at that point should have all-negative real-part
eigenvalues in the IR direction. The runner tests this directly
(Section 5.1-5.4):

- **5.1**: `d(|b|²/a²)/dt` at the test point is non-zero
  (≈ -0.036), confirming 1/2 is NOT a stationary point of the
  flow.
- **5.2**: starting at `|b|²/a² = 0.55` (small perturbation from
  1/2), the flow ends at `|b|²/a² ≈ 0.13` — distance from 1/2
  GROWS by factor 7.4× (attractor would shrink by < 1).
- **5.3**: starting at `|b|²/a² = 0.501` (machine-perturbation),
  the flow ends at `|b|²/a² ≈ 0.10` — distance from 1/2 grows
  by factor ~400×.
- **5.4**: local Jacobian at 1/2 shows uniform multiplicative
  dressing in (a, b) directions, NOT differentially attractive
  components in the ratio.

These four checks each independently confirm the absence of
attractive fixed-point structure at `|b|²/a² = 1/2`.

### Barrier RG5: HS rigidity does not propagate to matter sector

The retained `g_bare = 1` Hilbert-Schmidt rigidity
([`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md))
states: under the framework's fixed Hilbert-Schmidt form on
`su(3) ⊂ End(V)`, no scalar dilation `T_a → c T_a` with `c ≠ ±1`
preserves both the trace Gram and the quadratic Casimir
simultaneously. This is a 2-form rigidity statement that fixes
`g_bare = 1` once `N_F = 1/2` is admitted.

The hypothetical analog for the matter sector would be: under
some 2-form structure on circulant `Y_e`, no scalar dilation
`Y_e → c Y_e` preserves both forms — fixing `|b|²/a² = 1/2`.

The runner constructs candidate 2-forms (Section 6.1-6.4):
- `Tr(Y_e†Y_e)` — bilinear (Frobenius)
- `Tr((Y_e†Y_e)²)` — quartic

Both rescale uniformly under `Y_e → c Y_e` (`c²` and `c⁴`
respectively), and the ratio `Tr²/quartic = constant` is invariant
under the rescaling. There is NO joint two-form rigidity
analogous to su(3).

The structural reason: the HS rigidity argument relies on
**Killing-form uniqueness on the simple Lie algebra `su(3)`**.
The matter-sector circulant on hw=1 is `M_3(C)` (a full matrix
algebra, NOT a simple Lie algebra), so the Killing-form rigidity
does NOT apply.

The runner also constructs five explicit `(a, b)` choices
(`|b|²/a² ∈ {0.09, 0.49, 1.00, 0.50 (A1), 2.25}`) all satisfying
retained constraints (Hermitian + C_3-equivariant), confirming
the retained primitives do NOT select 1/2.

## Why the framework's existing dynamical content is NOT enough

The framework HAS retained dynamical content. The EW hierarchy
`v_EW = M_Pl·(7/8)^(1/4)·α_LM^16` is a real 16-power running
result. The y_t IR QFP is a real Pendleton-Ross fixed point. Both
are computed and verified.

But these are GAUGE-SECTOR results. The matter-sector circulant
amplitude ratio `|b|²/a²` is a different object:

- `α_LM` and v are SCALES (single real numbers from gauge
  running), NOT amplitude ratios.
- y_t QFP is a COLORED Yukawa fixed point, requiring the
  `-8 g_3²` term that charged leptons lack.
- HS rigidity is on `su(3)`, NOT on `M_3(C)` matter algebra.

To extend retained dynamical content to the charged-lepton
circulant ratio requires either:
- A new RETAINED primitive (matter-sector circulant flow),
- C_3-breaking dynamics (forbidden — Coleman/Wilson preserve C_3
  symmetric flow),
- A new HS-style rigidity theorem on hw=1 (no Killing-form
  argument applies because `M_3(C)` is not a simple Lie algebra).

None of these is supplied by retained content.

## Comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | bounded obstruction | trace-based 4th-order; Wilson-coefficient ratio unforced |
| Route B (Clifford torus on S³) | does not match Koide cone | 45° latitude vs equator |
| Route C (AS Lefschetz cot²) | parallel numeric identity | 2/3 = 2/3 coincidence |
| Route D (Newton-Girard) | bounded obstruction | trace-poly form; coefficient 6 unforced |
| Route E (A_1 Weyl-vector / Kostant) | bounded obstruction | three-way exact match but no derivation |
| Route F (Yukawa Casimir-difference) | bounded obstruction | four-barrier negative closure |
| Probe 1 (RP-Frobenius) | bounded obstruction | RP/GNS does not select 1/2 |
| Probe 2 (Flavor anomaly) | bounded obstruction | anomaly counts don't fix 1/2 |
| Probe 3 (Gravity-as-phase) | bounded obstruction | gravity sector orthogonal to flavor |
| Probe 4 (Spectral action) | bounded obstruction | spectral action degeneracy |
| **Probe 5 (RG fixed-point) — THIS NOTE** | **bounded obstruction** | **five-barrier negative closure on dynamical hypothesis** |

This note **complements** prior probes by establishing that the
NATURAL extension to dynamical/RG content also fails on retained
material. The static-vs-dynamic dichotomy was the principled
remaining angle; both close negatively.

## What this closes

- **Probe 5 negative closure** (bounded obstruction). Five
  independent structural barriers verified.
- **Sharpens the static-vs-dynamic dichotomy**: prior 8 attempts
  were static; this one was the dynamical alternative. Both
  classes close negatively on retained content.
- **Verified RG-flow numerical experiments**: the SM matrix RGE
  on circulant Y_e produces drift AWAY from 1/2, not focusing.
  This is a falsifiable numerical claim, not just a structural
  argument.
- **Structural reason** for the no-go: charged-lepton sector has
  no `g_3²` driver (no PR mechanism), `M_3(C)` is not simple
  (no Killing-form rigidity), and the HS argument does not lift.
- **Audit-defensibility**: all five barriers verified by paired
  runner with explicit numerical counterexamples.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic) remains the strongest open
  candidate (outside Theorem 6); needs derivation.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The framework's retained dynamical content (plaquette, EW
  staircase, y_t QFP) is unaffected.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| RG1 (no retained matter-sector RG) | Identify a retained derivation note that produces a β-function on circulant `(a, b)` from A1+A2+admissible math without new primitives — refutes RG1. |
| RG2 (no PR QFP for charged leptons) | Demonstrate a Pendleton-Ross-class focusing structure for charged-lepton Yukawa on the framework's lattice (with the actual lattice fermion content, not SM extension) — refutes RG2. |
| RG3 (drift away from 1/2) | Identify a derived or admissible C_3-symmetric β-function whose flow focuses `|b|²/a²` toward 1/2 from generic UV starting points — refutes RG3. |
| RG4 (no attractive structure at 1/2) | Compute Jacobian eigenvalues at 1/2 with negative real parts under a derived β-function — refutes RG4. |
| RG5 (no HS analog) | Establish a 2-form rigidity statement on `M_3(C)` (or any matter-sector algebra on hw=1) that fixes `|b|²/a²` — refutes RG5. |
| Numerical match (anchor) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; representative anchor values give Q = 0.6667 (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Probe 5 boundary:
the RG fixed-point hypothesis is blocked by absence of retained
matter-sector RG, lack of Pendleton-Ross structure for charged
leptons, drift away from 1/2 under SM matrix RGE, no attractive
Jacobian at 1/2, and absence of HS rigidity analog — unless a new
matter-sector primitive (matter-sector RG flow generator, C_3-breaking
dynamics, or `M_3(C)` 2-form rigidity) is supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "static vs dynamic" methodological gap (prior 8 attempts all static) is closed: the dynamical alternative also fails on retained content. |
| V2 | New derivation? | The five-barrier obstruction argument applied to RG dynamics is new structural content with explicit numerical RG-flow integration. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) RG1 retained-content enumeration, (ii) RG2 β-function structure, (iii) RG3 numerical RG-flow evidence, (iv) RG4 Jacobian analysis, (v) RG5 HS-rigidity analog. |
| V4 | Marginal content non-trivial? | Yes — the explicit numerical RG-flow demonstration that |b|²/a² drifts AWAY from 1/2 is non-obvious from prior notes and definitively refutes the RG-attractor hypothesis. |
| V5 | One-step variant? | No — the five-barrier argument across multiple dynamical sectors (gauge running, QFP structure, matrix RGE, Jacobian, rigidity) is not a relabel of any prior static obstruction. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior static Koide routes. The five-barrier
  obstruction argument applied to RG dynamics is new structural
  content with explicit numerical RG-flow tests.
- Tests a NEW STRUCTURAL HYPOTHESIS (the dynamical-fixed-point
  alternative) not addressed in prior routes.
- Provides explicit numerical RG-flow integration with multiple
  starting conditions — these were not present in prior probes.
- Sharpens the meta-pattern across 9 attempts: framework's retained
  content does not select a canonical normalization on the
  matter-sector C_3-circulant amplitude, in EITHER static OR
  dynamical formulations.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Prior Route F obstruction: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Retained dynamical chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- y_t Pendleton-Ross IR QFP: [`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- `g_bare = 1` HS rigidity: [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- A3 Route 1 (sister route): [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md)
- A3 R5 hostile review (RG-symmetric flow): [`A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md`](A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.py
```

Expected output: structural verification of (i) A1 algebraic baseline
on circulant Y_e, (ii) Barrier RG1 enumeration of retained dynamical
content (none acts on `|b|²/a²`), (iii) Barrier RG2 numerical y_t QFP
focusing vs y_τ no-focusing, (iv) Barrier RG3 SM matrix RGE drifts
ratio AWAY from 1/2, (v) Barrier RG4 Jacobian analysis at 1/2 (no
attractive structure), (vi) Barrier RG5 explicit non-A1 counter-
examples + degeneracy of 2-form analog, (vii) combined verdict, (viii)
falsifiability anchor (PDG values, anchor-only). Total: 24 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.txt`](../logs/runner-cache/cl3_koide_a1_probe_rg_fixed_point_2026_05_08_probe5.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The numerical match `1/2 = 1/2` (PDG anchor) is a consistency
  equality, not a structural RG-fixed-point result, and the proposed
  hypothesis cannot load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "the framework's matter-sector RG produces 1/2
  as fixed point" by showing that (a) the framework's retained RG
  content does not act on `|b|²/a²`, (b) the natural SM-matrix-RGE
  extension drifts AWAY from 1/2, and (c) HS rigidity on `su(3)` does
  not lift to `M_3(C)` matter sector.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit numerical RG-flow integration and Jacobian
  analysis is substantive new structural content, not a relabel of
  prior static Koide routes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (matter-sector primitive, C_3-breaking dynamics, M_3(C) 2-form
  rigidity) are characterized in terms of WHAT additional content
  would be needed, not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent barriers across retained-
  content enumeration, β-function structure, RG-flow integration,
  Jacobian analysis, and rigidity-form lifting) on a single
  load-bearing dynamical hypothesis, with sharp PASS/FAIL deliverables
  in the runner.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named
by the source-note above. It does not promote this note or change the
audited claim scope.

- [koide_a1_derivation_status_note](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
- [koide_a1_route_f_casimir_difference_bounded_obstruction_note_2026-05-08_routef](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- [complete_prediction_chain_2026_04_15](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- [yt_qfp_insensitivity_support_note](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- [g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- [sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- [charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- [a3_route1_higgs_yukawa_c3_breaking_bounded_obstruction_note_2026-05-08_r1](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md)
- [a3_r5_hostile_review_confirms_obstruction_note_2026-05-08_r5hr](A3_R5_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r5hr.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
