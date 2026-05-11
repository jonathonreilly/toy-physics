# Tree-Level Gluon Masslessness from Retained SU(3) Gauge Invariance

**Date:** 2026-05-02
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Claim scope:** at the tree level on the framework's retained SU(3) gauge action surface, no Lorentz-invariant Hermitian gauge-singlet quadratic-in-A_μ^a operator exists that is also SU(3) gauge-invariant; therefore the only quadratic-in-A operator allowed by retained SU(3) gauge invariance is the kinetic term -(1/4) F^a_μν F^{aμν}, and the gluon propagator pole is at p² = 0 (massless).
**Status:** awaiting independent audit. Under scope-aware classification (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Claim type:** positive_theorem
**Loop:** `positive-only-retained-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-block01-gluon-massless-20260502`
**Runner:** `scripts/gluon_tree_level_massless_check.py`
**Log:** `outputs/gluon_tree_level_massless_check_2026-05-02.txt`

**Audit-conditional perimeter (2026-05-02):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "The
cited dependencies retain bounded structural su(3) closure on graph-
first/cubic surfaces, but they do not themselves construct a local
Lorentz-covariant Yang-Mills connection, gauge action, or propagator
for framework gluons. The runner verifies the standard Yang-Mills
algebra after assuming that bridge, not the bridge from the retained
framework structure." This rigorization edit only sharpens the
boundary of the conditional perimeter; nothing here promotes audit
status. The supported content of this note is the standard Yang-
Mills algebra theorem (G1)–(G3): given a local Lorentz-covariant
SU(3) gauge connection `A_μ^a` with the standard non-abelian
transformation law, no quadratic-in-A gauge-invariant mass term
exists, so the tree-level gluon propagator pole is at p² = 0. The
conditional gap is the bridge from the framework's retained graph-
first / cubic structural SU(3) closure (cited authorities) to a local
Lorentz-covariant Yang-Mills connection on the framework surface;
this note's "Admitted-context inputs" already lists this bridge as
admitted-context. A future bridge-theorem note would close the
conditional perimeter; this note remains a tree-level theorem on the
admitted Yang-Mills surface, not a bridge from the retained graph-
first structure.

## Cited authorities (one hop)

- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — current ledger effective status `retained_bounded` (the SU(2) and structural SU(3) parts; the bounded-only piece is the abelian hypercharge-like surface, which this note does not depend on).
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — current ledger effective status `retained_bounded`. Provides the canonical structural SU(3) on the graph-first selected-axis surface.

Both deps are in the chain-clean set `{retained, retained_no_go, retained_bounded}` per the propagation rule.

## Admitted-context inputs

- **Standard non-abelian gauge transformation law** for an SU(3) connection
  `A_μ^a` (taking values in the Lie algebra `su(3)`), namely

  ```text
      A_μ^a → A_μ^a + (1/g) ∂_μ ω^a + f^{abc} A_μ^b ω^c                       (1)
  ```

  for an infinitesimal local gauge parameter `ω^a(x)`. This is the
  definition of a non-abelian gauge field — it is not a physics
  admission but a structural definition.

- **Lorentz invariance of bilinear-in-A operators in 3+1 dimensions**.
  The framework's emergent Lorentz invariance is a separate retained
  surface; for this theorem we use only the elementary fact that the
  only Lorentz scalar quadratic-in-A_μ^a contractions are
  `A_μ^a A^{aμ}` and `(∂_μ A^{aμ})²` (the latter is a total derivative
  modulo gauge transformations and reduces to a tree-level no-op for the
  on-shell propagator pole question).

- **Color-singlet constraint**. The mass term must be color singlet (no
  open `a` index). Standard requirement of a Lagrangian density for a
  gauge theory.

No physics conventions admitted beyond these structural / mathematical
items.

## Statement

Let `A_μ^a` (with `a = 1, …, 8`) be the SU(3) gauge connection on the
framework's retained SU(3) gauge action surface
(`NATIVE_GAUGE_CLOSURE_NOTE` + `GRAPH_FIRST_SU3_INTEGRATION_NOTE`). Then
on the live retained-grade chain:

**(G1) No SU(3)-invariant quadratic mass term exists.** The candidate
"gluon mass" Lagrangian density

```text
    L_mass  =  (1/2) m² A_μ^a A^{aμ}                                          (2)
```

is **not** invariant under the infinitesimal SU(3) gauge transformation
(1). Specifically,

```text
    δL_mass  =  m² A_μ^a · ((1/g) ∂^μ ω^a + f^{abc} A^{bμ} ω^c)                (3)
            =  (m² / g) A_μ^a ∂^μ ω^a  +  m² f^{abc} A_μ^a A^{bμ} ω^c          (4)
```

The second term `m² f^{abc} A_μ^a A^{bμ} ω^c` vanishes pointwise by
antisymmetry of `f^{abc}` paired with the symmetric `A_μ^a A^{bμ}` (the
swap `a ↔ b` flips `f^{abc}` sign but leaves `A_μ^a A^{bμ}` invariant
after relabeling), so `f^{abc} A_μ^a A^{bμ} = 0`. The first term
`(m² / g) A_μ^a ∂^μ ω^a` integrates by parts to
`-(m²/g) (∂_μ A^{μa}) ω^a`, which does **not** vanish for arbitrary
`ω^a` unless `m = 0` or `∂_μ A^{μa} = 0` is imposed by hand (which it
cannot be at the level of the unconstrained gauge action).

Hence `L_mass = (1/2) m² A_μ^a A^{aμ}` is gauge invariant **iff** `m = 0`.

**(G2) Uniqueness of the kinetic term up to total derivative.** The only
SU(3) gauge-invariant Lorentz-scalar quadratic-in-A_μ^a operator (up to a
total derivative and modulo color singlet constraint) is

```text
    L_kin  =  -(1/4) F^a_μν F^{aμν}                                            (5)
```

with `F^a_μν = ∂_μ A^a_ν - ∂_ν A^a_μ + g f^{abc} A^b_μ A^c_ν`. Other
candidates fail one of the three constraints (gauge invariance, Lorentz
scalar, color singlet).

**(G3) Tree-level propagator pole at p² = 0.** The kinetic-term
inverse-propagator (in covariant Lorenz gauge with parameter ξ) is

```text
    Γ^{(2)}_{μν, ab}(p)  =  i δ^{ab} · ( -p² g_{μν} + (1 - 1/ξ) p_μ p_ν )      (6)
```

The on-shell propagator pole is at `p² = 0`. Equivalently, the tree-level
gluon dispersion relation is `ω = |p|` (light-cone), which is the
massless dispersion. There is no `m²` term to add to the inverse propagator
because no gauge-invariant `m²` term exists in the Lagrangian by (G1)–(G2).

(G1)–(G3) constitute the **tree-level gluon masslessness theorem** on the
retained SU(3) gauge action surface.

## Proof

The proof is a one-screen calculation that already appears compactly in
the **Statement** section above. The structure is:

1. **Step 1 (G1):** verify that `L_mass = (1/2) m² A_μ^a A^{aμ}` is not
   gauge invariant unless `m = 0`. Calculation: substitute (1) into
   `L_mass`, expand to first order in `ω^a`, simplify using
   antisymmetry of `f^{abc}`. Residual term `(m²/g) A_μ^a ∂^μ ω^a`
   integrates to a non-vanishing surface-plus-bulk contribution that is
   not killed by any algebraic identity. (See Peskin-Schroeder §15.1
   for the abelian case which is the same calculation specialised to
   `f^{abc} = 0`; the non-abelian generalisation is direct.)

2. **Step 2 (G2):** enumerate all Lorentz-scalar quadratic-in-A
   color-singlet operators. There are exactly three classes:
   - `A_μ^a A^{aμ}` — fails gauge invariance by Step 1.
   - `(∂_μ A^{aμ})²` — gauge non-invariant: under (1) the term `∂_μ ω^a / g`
     contributes `(2/g) ∂_μ A^{aμ} ∂_ν ∂^ν ω^a`, which is not zero off
     the EOM. So this operator is also non-invariant.
   - `F^a_μν F^{aμν}` — gauge invariant by direct calculation: `F^a_μν`
     transforms covariantly as `F^a_μν → F^a_μν + f^{abc} F^b_μν ω^c`,
     so `F^a_μν F^{aμν} → F^a_μν F^{aμν} + 2 f^{abc} F^a_μν F^{bμν} ω^c`.
     The cross-term vanishes by antisymmetry of `f^{abc}` paired with
     symmetric `F^{a}_{μν} F^{b\,μν}`.

   So `F² /4` (up to overall sign and normalization) is the unique
   gauge-invariant quadratic-in-A operator up to a total derivative.

3. **Step 3 (G3):** invert the kinetic operator `δ²L_kin / δA δA` in the
   Lorenz gauge to read the propagator. Pole at `p² = 0`. Standard
   textbook calculation (Peskin-Schroeder §16.2).

The proof uses only:

- the SU(3) gauge transformation law (1) — definition of SU(3) gauge
  field;
- antisymmetry of structure constants `f^{abc}` — Lie-algebra structure
  property of `su(3)`;
- standard Lorentz-scalar enumeration of bilinears in 3+1 dimensions;
- elementary integration by parts;
- standard inverse-of-quadratic-form propagator identity.

No physics admission, no fitted value, no observed input.

## Hypothesis set used

- `NATIVE_GAUGE_CLOSURE_NOTE` (retained_bounded): provides the SU(3)
  connection `A_μ^a` with `a = 1, …, 8` and the structure constants
  `f^{abc}`.
- `GRAPH_FIRST_SU3_INTEGRATION_NOTE` (retained_bounded): provides that
  the framework's structural SU(3) closure includes the kinetic term
  `-(1/4) F²` as the gauge-action backbone.

No fitted parameters. No observed values. No physics conventions
admitted beyond the structural definition of an SU(3) gauge field.

## Corollaries

C1. **No spin-1 color-octet mass spectrum at tree level.** The eight
gluons are degenerate at zero mass at tree level on the retained
surface.

C2. **Goldstone non-applicability.** Because there is no spontaneous
breaking of SU(3)_color in the retained gauge action, there are no
"would-be" longitudinal Goldstone modes that could be eaten to give a
gluon mass via the Higgs mechanism. (The retained content has no
color-non-singlet scalar in the Higgs sector.)

C3. **Gluon condensate caveat.** At the non-perturbative / quantum level,
QCD develops a non-vanishing gluon condensate `<F²> ≠ 0` (Shifman-
Vainshtein-Zakharov 1979). This is a separate dynamical statement and
is **not** in scope for this tree-level theorem. Confinement-related
mass-gap statements are also separate (and bounded on the framework
surface).

C4. **Photon analogue.** The same argument with `f^{abc} → 0` gives the
abelian U(1) result that `(1/2) m² A_μ A^μ` is not U(1) gauge invariant
unless `m = 0`. However this depends on the U(1) hypercharge surface
which is `bounded` (per `NATIVE_GAUGE_CLOSURE_NOTE`, the abelian factor
is "bounded to the left-handed +1/3 / -1 eigenvalue surface, not a full
anomaly-complete U(1)_Y theorem"). So the photon analogue is *not* a
clean retained corollary today; it would land at retained_bounded.

## Honest status

**Tree-level positive theorem on the retained SU(3) gauge action
surface.** Steps 1–3 close from `(NATIVE_GAUGE_CLOSURE_NOTE,
GRAPH_FIRST_SU3_INTEGRATION_NOTE)` plus standard structural definition
of an SU(3) gauge field. No physics admission.

The runner verifies (G1)–(G3) by:

- explicitly computing the gauge variation of `A_μ^a A^{aμ}` under (1)
  and confirming the residual term `(m²/g) A_μ^a ∂^μ ω^a` is non-zero
  for generic `ω^a`;
- enumerating quadratic-in-A bilinears and confirming `F² /4` is the
  unique gauge-invariant choice;
- inverting the Lorenz-gauge kinetic operator and reading off the
  pole at `p² = 0`.

**Honest classification fields:**

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Tree-level on the framework's retained SU(3) gauge action surface, no Lorentz-invariant Hermitian gauge-singlet quadratic-in-A_μ^a operator other than -(1/4) F^a_μν F^{aμν} is SU(3) gauge invariant; the gluon tree-level propagator has its pole at p² = 0."
admitted_context_inputs:
  - SU(3) gauge transformation law (definition)
  - antisymmetry of f^{abc} (Lie algebra structure)
  - standard Lorentz-scalar enumeration of quadratic-in-A operators
upstream_dependencies:
  - native_gauge_closure_note
  - graph_first_su3_integration_note
audit_required_before_effective_retained: true
```

These are author-side hints only. The independent audit lane sets the audit
verdict, and the pipeline computes any retained-family effective status after
that verdict and dependency closure.

**Not in scope.**

- Non-perturbative gluon mass-gap / dynamical mass generation.
- Confinement.
- Photon masslessness (abelian U(1) analogue is bounded, not retained,
  on the live ledger).

## Citations

- retained inputs: `docs/NATIVE_GAUGE_CLOSURE_NOTE.md`,
  `docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`
- standard external references (theorem-grade, no numerical input):
  Yang-Mills (1954) *Phys. Rev.* 96, 191;
  Peskin-Schroeder (1995) *An Introduction to Quantum Field Theory*,
  ch. 15-16.
