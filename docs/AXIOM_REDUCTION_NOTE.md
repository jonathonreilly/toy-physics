# Axiom Reduction: Honest Minimal Assumption Inventory

**Date:** 2026-04-12 (originally); 2026-05-10 (audit-narrowing as
`audited_conditional`: explicit `claim_type: meta` framing as
inventory-only under named upstream pending derivation rows);
2026-05-16 (upstream-state citation refresh: parenthetical audit-state
labels for the named one-hop authority surfaces updated to match the
live ledger; no inventory rows or counts changed).
**Purpose:** document counting every assumption in the framework. The
point is to be explicit about what is assumed versus what is derived.
**Claim type:** meta
**Status authority:** independent audit lane only.
**Authority role:** records a meta-inventory of named in-flight
derivation-target rows. Explicitly **does not** propose retained,
bounded, or positive-theorem promotion for any of the listed D-row
items, and **does not** itself constitute a derivation closure.

## Audit boundary

The 2026-05-05 audit recorded the verdict `audited_conditional` with
load-bearing class E (sentence-level meta narrative). The audit
identified that this note's "derived" labels for D1–D10 are stated as
meta-inventory summaries rather than as in-note bridge derivations or
runner certificates. The 2026-05-10 audit-narrowing refresh adopts an
explicit `claim_type: meta` framing: the note is an **inventory** of
named D-row derivation-target rows, not a closure of the listed
derivations.

**Cited authorities (one-hop deps; cited as related, not as
in-note closure):**

The D-row "derived" labels in this note are summary annotations for the
following authority surfaces, each of which carries its own audit verdict
on `main`. None is closed in this note. **Live ledger audit states as of
the 2026-05-16 refresh are recorded below; see `audit_ledger.json` rows
for canonical state:**

- D1 (complex amplitudes) / D2 (linear superposition) / D3 (Born rule):
  related surface
  [`BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md)
  (`audit_status: audited_failed`; `claim_type: bounded_theorem`;
  `load_bearing_step_class: A`; `chain_closes: false`). Cited as
  related, not as authority closure. **The current `audited_failed`
  state means the D1/D2/D3 inventory labels in this note are not
  upstream-supported on `main`; this note records that explicitly and
  does not promote them.**
- D5 (Poisson field equation) / Poisson uniqueness:
  related surface
  [`POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`](POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md)
  (`audit_status: unaudited`; `claim_type: bounded_theorem`). Cited as
  related, not as authority closure.
- D6 (valley-linear action) / D7 (coupling normalization) / D8
  (conformal metric):
  related surfaces
  [`VALLEY_LINEAR_ACTION_NOTE.md`](VALLEY_LINEAR_ACTION_NOTE.md)
  (`audit_status: audited_clean`; `intrinsic_status: retained_bounded`;
  `chain_closes: true`),
  [`VALLEY_LINEAR_ROBUSTNESS_NOTE.md`](VALLEY_LINEAR_ROBUSTNESS_NOTE.md)
  (`audit_status: audited_clean`; `intrinsic_status: retained_bounded`;
  `chain_closes: true`),
  [`VALLEY_LINEAR_CONTINUUM_SYNTHESIS_NOTE.md`](VALLEY_LINEAR_CONTINUUM_SYNTHESIS_NOTE.md)
  (`audit_status: unaudited`). Cited as related, not as authority
  closure. The two `audited_clean` rows close at retained-bounded grade
  on their own audit lanes; the synthesis surface remains `unaudited`.

**Admitted-context derivation gap (real, not import-redirect):**

This note explicitly admits that the D1–D10 reductions listed below are
**not** closed in-note. As of the 2026-05-16 live-ledger refresh, two of
the named one-hop authority surfaces (`valley_linear_action_note`,
`valley_linear_robustness_note`) carry `audited_clean` /
`retained_bounded` verdicts on their own audit rows; two
(`poisson_exhaustive_uniqueness_note`,
`valley_linear_continuum_synthesis_note`) remain `unaudited`; and one
(`born_rule_analysis_2026-04-11`) is `audited_failed`. There is
therefore **no uniform upstream authority closure** across all D-row
labels used in Part 1; some surfaces are partially closed, one is
actively failed, and the meta-inventory must be read with that mixed
state in mind.

The note's contribution is the **inventory**: naming each ingredient,
recording the legacy inventory rows it is (heuristically) reduced to, and
naming the authority surface where the corresponding derivation is
in-flight. The "Derived" column is an inventory label, not a positive
in-note closure of the row.

This is a **real derivation gap**, not a dependency-citation issue.
Promotion of any D-row to a retained-grade derivation requires the
corresponding authority surface to close on its own audit row.

---

## Part 1: Complete Inventory of All Assumptions

Every ingredient the framework uses, with no omissions. The "Type" /
"Description" columns are inventory labels referring to in-flight
authority surfaces; they are **not** in-note derivations (see "Audit
boundary" above).

| # | Ingredient | Type | Description |
|---|-----------|------|-------------|
| A1 | Discrete graph | **Axiom** | Reality is a set of nodes with pairwise directed edges (a DAG or lattice). This is the substrate. |
| A2 | Unitarity | **Axiom** | Probability is conserved: the propagator preserves total amplitude norm. Equivalently, amplitudes propagate linearly. |
| C1 | d = 3 spatial dimensions | **Choice** | The graph is embedded in or has the topology of 3D space. Not derived from the two legacy inventory rows. |
| D1 | Complex amplitudes on edges | **Derived from A2** | Linear probability-conserving propagation on a graph requires complex amplitudes (real amplitudes cannot produce interference; see below). |
| D2 | Linear superposition | **Derived from A2** | Unitarity on a graph IS linearity of the propagator. Nonlinear propagation breaks both Born rule and gravity sign simultaneously. |
| D3 | Born rule (pairwise interference) | **Derived from D2** | For a linear propagator, the Sorkin parameter I_3 = 0 identically. This is a mathematical theorem, not a physical assumption. |
| D4 | Scalar coupling (action depends on field along path) | **Derived from A1** | On a graph with scalar node values, the simplest local coupling is S = function(path length, field values along path). Tensor or vector coupling requires additional structure (orientation, gauge group) not present in A1. |
| D5 | Poisson field equation | **Derived from self-consistency** | The propagator's own density rho = \|psi\|^2 sources the field. Self-consistency forces the field operator to be the graph Laplacian. Only Poisson produces attractive, monotonically decaying fields. |
| D6 | Valley-linear action S = L(1-f) | **Derived from D5 + attraction + mass law** | Attractive gravity requires a phase valley (S decreasing near mass). Newtonian mass scaling F proportional to M requires weak-field linearity in f. Together these select S = L(1-f) from the space of possible actions. |
| D7 | Coupling constant c = 1 | **Fixed by observation** | The identification f = 2GM/rc^2 (matching the Schwarzschild weak-field limit) fixes the normalization. This is the standard procedure of matching to observed light bending. |
| D8 | Conformal spatial metric g_ij = (1-f)^2 delta_ij | **Derived from D6** | The action S = L(1-f) defines an effective distance ds = (1-f)dx. Isotropy of the scalar field f makes this conformal. The metric is not an extra assumption. |
| D9 | Kernel 1/L^(d-1) | **Derived from A2 + C1** | Transfer-norm stability in the continuum limit selects the kernel power. In d spatial dimensions, p = d-1 is the unique power giving finite, non-divergent propagation. |
| D10 | M1 * M2 product law | **Derived from D5** | Poisson linearity (phi proportional to M_source) times test-mass response (F proportional to M_test) gives F proportional to M1*M2 without any bilinear ansatz. |

---

## Part 2: Derivation Chain (Which Assumptions Are Independent?)

The logical dependency structure:

```
A1 (graph) + A2 (unitarity)
    |
    +---> D1 (complex amplitudes): unitarity on a graph requires
    |     complex propagation to produce interference
    |
    +---> D2 (linear superposition): unitarity IS linearity
    |       |
    |       +---> D3 (Born rule): I_3 = 0 is a theorem of linearity
    |
    +---> D4 (scalar coupling): simplest local coupling on a graph
    |       with no extra structure
    |
    +--- + C1 (d=3) ---> D9 (kernel 1/L^2): transfer-norm stability
    |
    +---> D5 (Poisson): self-consistency of propagator + field
    |       |
    |       +---> D6 (valley-linear action): attraction + mass law
    |       |       |
    |       |       +---> D8 (conformal metric): action defines geometry
    |       |       |
    |       |       +---> D7 (c=1): normalization from observation
    |       |
    |       +---> D10 (product law): two independent linearities
```

### Step-by-step justification:

**D1: Complex amplitudes from unitarity.**
On a graph, probability-conserving propagation that produces interference
requires complex-valued amplitudes. Real-valued linear propagation gives
classical diffusion (no interference fringes). The path from unitarity to
complex amplitudes is: unitarity demands a unitary transfer matrix, which
requires complex entries to produce the oscillatory behavior needed for
wave-like interference.

**D2: Linearity from unitarity.**
A unitary propagator K satisfies K^dagger K = I. This IS a linear map.
Nonlinear modifications (quadratic, cubic) simultaneously break the Born
rule (I_3 jumps from 10^-16 to 0.2) AND flip the gravity sign from
attractive to repulsive. This is not a choice; it is forced.

**D3: Born rule from linearity.**
For any linear propagator, the three-slit Sorkin parameter I_3 = 0
identically. This is verified at machine precision (I_3/P < 10^-14) across
7 different kernels, all dimensions d = 2, 3, 4, and all field strengths
tested. It is a mathematical consequence of amplitude additivity.

**D4: Scalar coupling from graph structure.**
A1 provides nodes and edges with no intrinsic orientation, spin, or gauge
structure. The only local quantity that can be defined without additional
assumptions is a scalar field on nodes. Vector or tensor fields require
choosing an embedding or frame, which is additional structure beyond A1.
This makes scalar coupling "the simplest choice" rather than a free
parameter. One could add gauge structure, but that is an extension, not
a requirement.

**D5: Poisson from self-consistency.**
Tested 21 operators across four categories (fractional Laplacians
alpha = 0.25 to 3.0, anisotropic Laplacians, non-local operators,
higher-order stencils). Only the graph Laplacian (alpha = 1) produces
attractive, convergent, monotonically decaying fields. The discriminator
is sharp: all non-Poisson operators produce either repulsive fields,
divergent iteration, or wrong decay exponents.

Additionally, the propagator's Green's function IS the inverse Laplacian
on a nearest-neighbor graph. Self-consistency (field sourced by propagator
density, propagator evolving in that field) therefore forces L = nabla^2.

**D6: Valley-linear action from attraction + mass scaling.**
Phase-hill actions (S increasing with f) give repulsive gravity. Phase-valley
actions (S decreasing with f) give attractive gravity. Among valleys:
- S = L(1-f^0.5): F proportional to M^0.5 (wrong mass law)
- S = L(1-f): F proportional to M^1.0 (Newtonian)
- S = L(1-f^2): F proportional to M^2.0 (wrong mass law)

Newtonian mass scaling uniquely selects weak-field linearity in f.
All weak-field-linear valleys (L(1-f), L*exp(-f), L/(1+f)) give identical
mass scaling. The valley-linear form is the universality class, not a
single formula.

**D7: Coupling normalization from observation.**
The identification of f with the Newtonian potential requires matching
to one observed quantity (Newton's constant G, or equivalently the observed
light-bending angle). This is the same procedure used in GR and every other
gravity theory. It is a boundary condition, not an axiom.

**D8: Conformal metric derived from action.**
S = L(1-f) defines effective path length ds = (1-f)dx. Because f is a
scalar (direction-independent), the metric is conformal: g_ij = (1-f)^2
delta_ij. Verified numerically: isotropy holds to 0.4%, and the resulting
factor-of-2 light bending matches GR (ratio 1.985 +/- 0.012).

**D9: Kernel power from transfer-norm stability.**
The transfer norm T = sum_edges w * h^(d-1) / L^p must remain finite as
h -> 0 (continuum limit). For kernel 1/L^p with measure h^(d-1) in d
spatial dimensions, finiteness requires p = d-1. At p = d-1, T grows only
logarithmically (~4.3 + 1.1*ln(1/h)), ensuring a well-defined continuum
limit.

**D10: Product law from Poisson linearity.**
F proportional to M1*M2 emerges from two independent linearities:
Poisson (phi proportional to M_source) and test-mass response
(F proportional to M_test). Confirmed numerically with cross-field Poisson
coupling containing no bilinear ansatz: alpha = 1.01, beta = 0.99,
R^2 = 0.9999.

---

## Part 3: The Honest Minimal Set

### What you MUST assume:

1. **A graph exists** (nodes + directed edges with local connectivity).
   This is ONE assumption encompassing: discrete structure, locality,
   and relational ontology.

2. **Unitarity** (probability-conserving propagation). This is the SECOND
   assumption. It forces complex amplitudes, linear superposition, and
   the Born rule.

3. **Three spatial dimensions** (C1). This is a CHOICE, not derivable from
   A1 + A2. However:
   - d_s = 3 is the lowest integer dimension producing 1/r^2 force
   - d_s = 2 gives only logarithmic potential (marginal)
   - d_s < 2 gives no long-range force
   - Whether a dynamical mechanism selects d = 3 is an open question

### The honest count:

**2 axioms + 1 dimensional choice.**

Not quite "two axioms." The dimensional choice is real and cannot currently
be eliminated. However, it is a single discrete parameter (an integer),
not a continuous free parameter or a structural assumption.

### What would reduce the count to exactly 2:

If a dynamical mechanism (graph growth rule, spectral selection, or
dimensional phase transition) were shown to force d_s = 3, the framework
would be genuinely two-axiom. This is an open research direction. The
spectral dimension measurement confirms d_s correctly tracks the force
law on both regular and irregular graphs, and d_s = 3 is special
(lowest dimension with power-law Green's function). But a dynamical
selection mechanism has not been demonstrated.

---

## Part 4: Comparison to Competing Frameworks

| Framework | Free parameters | Structural assumptions | Total burden |
|-----------|----------------|----------------------|--------------|
| **This work** | **0 continuous** | **2 axioms + 1 integer choice** | **~3** |
| Standard Model | 25+ continuous (masses, couplings, mixing angles) | QFT axioms + gauge group SU(3)xSU(2)xU(1) + 3+1D spacetime + Lorentz invariance + CPT | ~30+ |
| General Relativity | 1 (Lambda) or 2 (Lambda + G) | Differentiable manifold + metric + Einstein-Hilbert action + equivalence principle + 3+1D | ~7 |
| Loop Quantum Gravity | 1 (Immirzi parameter) | GR action + quantization prescription + Ashtekar variables + 3+1D | ~5 |
| String Theory | 0 in principle, ~10^500 landscape | 10D + string action + supersymmetry + compactification choice | ~5+ (but landscape) |
| Causal Set Theory | 0 continuous | Lorentz invariance + discreteness + partial order + faithful embedding + 3+1D | ~5 |
| Causal Dynamical Triangulations | 2-3 (bare couplings) | Einstein-Hilbert action + discrete triangulation + causality constraint + 3+1D | ~7 |
| Wolfram Physics Project | 0 continuous | Hypergraph + rewriting rules (specific rule chosen) + causal invariance + 3+1D emergent | ~4 |

The framework's assumption count is the lowest of any approach listed.
The key advantage: no continuous free parameters at all (the coupling is
fixed by observation, not tuned). The closest competitor is causal set theory,
which also has no continuous parameters but requires more structural
assumptions (Lorentz invariance, faithful embedding).

---

## Part 5: Numerical Verification Table

| Step | What is derived | From what | Numerical evidence | Script |
|------|----------------|-----------|-------------------|--------|
| Born rule | I_3 = 0 at machine precision | Linear propagator (A2) | I_3/P < 10^-14 across 7 kernels, d=2,3,4 | `frontier_nonlinear_born_gravity.py` |
| Nonlinear breaks both | I_3 >> 0 AND repulsive gravity | Quadratic/cubic propagator | I_3 = 0.19-0.24, force sign flips | `frontier_nonlinear_born_gravity.py` |
| Poisson uniqueness | nabla^2 is unique self-consistent operator | 21 operators tested | Only alpha=1 gives attractive, convergent field | `frontier_poisson_exhaustive_uniqueness.py` |
| Poisson self-consistency | phi = (nabla^2)^(-1) rho converges | Propagator density sources field | 10-iteration convergence, susceptibility correlation 0.93 | `frontier_self_consistent_field_equation.py` |
| Valley-linear selection | S = L(1-f) uniquely gives F proportional to M | Action sweep: 7 actions | f-power 0.5 -> F proportional to M^0.5; f-power 1 -> F proportional to M^1; f-power 2 -> F proportional to M^2 | `action_universality_probe.py` |
| Phase valley required | S decreasing with f -> attraction | Hill vs valley actions | S=L(1+f): AWAY; S=L(1-f): TOWARD | `action_universality_probe.py` |
| Continuum limit | h -> 0 converges in weak field | h^2 measure + T normalization | F proportional to M brackets 1.000 (0.979, 0.991, 0.998, 1.018) | `lattice_h2_T_numpy_continuum.py` |
| Kernel selection | p = d-1 gives finite transfer norm | h -> 0 limit | T grows logarithmically (4.3 to 6.5), not as power law | `lattice_h2_T_numpy_continuum.py` |
| Distance law (3D) | delta proportional to b^(-0.96) on grown geometry | Valley-linear + 1/L^2 | alpha = -0.96 (nearest to Newtonian; irregular nodes smooth wave-optics oscillations) | `distance_law_grown_geometry.py` |
| Dimension determines force law | d_s = 3 gives 1/r^2 force | Heat-kernel spectral dimension | d_s measured: 1.06 (1D), 2.01 (2D), 2.84 (3D) | `frontier_dimension_emergence.py` |
| Product law emerges | F proportional to M1*M2 without bilinear ansatz | Cross-field Poisson | alpha=1.01, beta=0.99, R^2=0.9999 | `frontier_emergent_product_law.py` |
| GR time dilation | Phase rate = k(1-f) | Action S = L(1-f) | Measured/predicted = 1.000000 | `frontier_emergent_gr_signatures.py` |
| Weak equivalence principle | Deflection independent of k | Action has no k-dependence | Spread across k=2..16: 0.0000% | `frontier_emergent_gr_signatures.py` |
| Conformal metric | g_ij = (1-f)^2 delta_ij | Action defines effective geometry | Isotropy < 0.4%, factor-of-2 ratio = 1.985 +/- 0.012 | `frontier_spatial_metric_derivation.py` |
| k=0 control | Zero phase coupling -> zero gravity | Phase-mediated mechanism | k=0 gives exactly zero deflection at all h | `lattice_h2_T_numpy_continuum.py` |

---

## Part 6: What Remains Open

Even with the honest 2+1 count, several questions remain:

1. **Dimension selection.** Can a growth rule or spectral mechanism force
   d_s = 3? If yes, the count drops to exactly 2 axioms. Current status:
   d_s correctly tracks force law on arbitrary graphs, and d_s = 3 is
   special (lowest power-law Green's function), but no dynamical selection
   demonstrated.

2. **Strong-field regime.** The framework is perturbative (f << 1). Gravity,
   escape fraction, and F proportional to M all fail to converge at
   f >= 0.1. Strong-field GR equivalence (horizons, singularities) is
   untested.

3. **Rotational isotropy.** The angular kernel anisotropy is intrinsic, not a
   lattice artifact. It does not improve with h -> 0. This blocks the
   Lorentz invariance frontier.

4. **Evolving network dynamics.** The graph is currently given (lattice or
   constructed DAG), not grown from a dynamical rule. All growth rule
   attempts (feedback, pruning, birth/death) fail asymptotically. This is
   the largest open problem.

5. **Distance law on random DAGs.** b-independent (flat/topological) on all
   random DAG architectures. The lattice gives b-dependent gravity, but
   random-graph distance law remains a structural negative.

---

## Part 7: Recommended Framing for Publication (under audit-narrowed scope)

The recommended framing below is conditional on the named upstream
authority surfaces in "Audit boundary" closing on their own audit rows.
This note itself does not close any of those surfaces; it records the
inventory only.

**Do say (only when the named upstream authority rows close clean):**
- "The framework has two axioms (graph + unitarity) and one dimensional
  choice (d=3)."
- "Other ingredients (Born rule, Poisson field equation, valley-linear
  action, conformal metric, `M1*M2` product law) have in-flight
  derivation-target rows naming self-consistency or attraction-and-mass-
  law constraints; each is recorded with a separate authority surface
  (see Audit boundary)."
- "The framework has zero continuous free parameters."

**Current-state caveat (2026-05-16):** The upstream surfaces are
**mixed**, not uniformly closed. Two of the five named one-hop rows
(`valley_linear_action_note`, `valley_linear_robustness_note`) carry
`audited_clean` / `retained_bounded` verdicts; two
(`poisson_exhaustive_uniqueness_note`,
`valley_linear_continuum_synthesis_note`) are `unaudited`; and
`born_rule_analysis_2026-04-11` is `audited_failed`. The Part 7 "Do
say" wording above is therefore **not** currently warranted as a
package statement; the meta-inventory below records the inventory under
this mixed state, and any publication-level claim must enumerate which
upstream surfaces have or have not closed.

**Do not say:**
- "Two axioms derive all of gravity." (Omits the dimensional choice and
  the named upstream pending derivation rows.)
- "The Born rule is predicted." (It is a mathematical consequence of the
  assumed linearity, which is itself a consequence of unitarity. Saying
  "predicted" implies it could have come out differently, which it cannot
  for a linear propagator.)
- "Poisson is derived from first principles." (The current authority
  surface
  [`POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`](POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md)
  is `unaudited`; the in-flight derivation is on a nearest-neighbor
  lattice, where the lattice structure is part of A1.)
- "This note discharges the D1–D10 reductions." (It does not. It is a
  meta-inventory; the D-row derivations are upstream authority surfaces
  with their own audit rows.)

**The strongest honest claim (conditional):**
Two axioms and one discrete choice (d=3) plus the named upstream pending
derivation rows produce Newtonian gravity with the correct mass law,
distance law, equivalence principle, time dilation, light bending factor
of 2, and Born rule, with zero continuous free parameters. This is a
significantly more minimal starting point than competing frameworks
**when the named upstream authority surfaces close**. This note records
the inventory; promotion of any item to a retained-grade derivation
requires the corresponding authority surface to close on its own audit
row.
