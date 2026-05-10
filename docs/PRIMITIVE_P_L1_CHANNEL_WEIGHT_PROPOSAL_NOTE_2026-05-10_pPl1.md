# L1 Channel-Weight Open Gate — Negative Candidate-Primitive Probe for QCD β_2/β_3 Scalar Weights

**Date:** 2026-05-10
**Claim type:** open_gate
**Sub-gate:** Lane 1 (alpha_s) — open gate on β_2 / β_3 scalar
channel weights at 3-loop and 4-loop QCD running.
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note records candidate inputs for review; it does
not claim retention of any new content.
**Source-note boundary:** this is an open-gate source note. Audit verdict
and downstream status are set only by the independent audit lane. No
candidate primitive proposed here is admitted, and no repo-wide axiom or
retained surface changes on the basis of this note. The framework baseline
is the physical Cl(3) local algebra on the Z^3 spatial substrate.

**Primary runner:** [`scripts/cl3_primitive_p_l1_2026_05_10_pPl1.py`](../scripts/cl3_primitive_p_l1_2026_05_10_pPl1.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_l1_2026_05_10_pPl1.txt`](../logs/runner-cache/cl3_primitive_p_l1_2026_05_10_pPl1.txt)

## 0. Context — what is the open gate?

The Lane 1 strong-coupling running chain currently relies on the standard
SM RGE with `β_0 = 7, β_1 = 26` as existing repo context at `N_f = 6`, and
literature-imported `β_2, β_3` (TVZ 1980; van Ritbergen-Vermaseren-Larin
1997 in MSbar). Companion L1 probes give the following context; they
motivate this note but are not authority for admitting a new primitive:

- **MSbar-native route context** — neither MSbar dimensional regularization
  nor lattice perturbation theory
  (LPT) primitives are not established as framework-native; the framework carries the 9-channel
  3-loop Casimir-tensor SKELETON and the 17+-channel 4-loop quartic
  Casimir extension as group theory, but NOT the scalar coefficients
  multiplying each channel.
- **V-L1-Quartic** ([`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md),
  PR #972) — quartic-Casimir values (`5/12`, `5/2`, `135/8`) are
  available at SU(3); β_2 has no quartic-Casimir channels; β_3 has
  them but their scalar weights are 4-loop master integrals.
- **U-L1-Resurgence** (PR #989) — Borel-plane renormalon ladder at
  `z* = 4π/β_0 = 4π/7` is available as structural context; Stokes constant `S_IR` and finite
  parts of trans-series are non-perturbative QCD instanton primitives,
  not derived here.
- **S-L1-Topological** ([`KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md`](KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md),
  PR #1009) — Chern-Simons output field is `Q(ζ_(k+h^∨))`; β_n weight
  field is `Q + Q·ζ_3`. Number-theoretic mismatch; CS level shift
  reproduces only the existing Casimir skeleton at classical
  limit.

The open gate, restated cleanly, is:

```
For the 9-channel 3-loop QCD Casimir-tensor skeleton
(C_F^3, C_F^2 C_A, C_F C_A^2, C_A^3, C_F^2 T_F N_f, C_F C_A T_F N_f,
 C_A^2 T_F N_f, C_F (T_F N_f)^2, C_A (T_F N_f)^2),
whose TVZ MSbar n_f-polynomial reduction has six nonzero scalar weights,
and for each of the 14+ independent 4-loop channels, the scalar rational
weight (resp. rational + ζ_3 weight) is not framework-derived here.
```

This open gate is what THIS NOTE is asked to either (a) probe with a
candidate primitive, or (b) honestly conclude that no clean candidate
primitive exists.

## 1. What a candidate primitive must provide

A candidate input that would close this gate must, by definition, supply a
**function**

```
W : Channel  →  Q   (3-loop)
W : Channel  →  Q + Q · ζ_3   (4-loop)
```

mapping each Casimir-tensor channel to its scalar weight, where
"Channel" is the space of ordered Casimir-tensor monomials in the
quadratic / cubic / quartic Casimirs of SU(3) at `N_f = 6`. The
specific 3-loop target values (TVZ 1980 in MSbar) are:

| Channel | TVZ MSbar weight |
|---|---|
| `C_A^3` | `2857/54` |
| `C_A^2 (T_F n_f)` | `-1415/54` |
| `C_F C_A (T_F n_f)` | `-205/18` |
| `C_A (T_F n_f)^2` | `79/54` |
| `C_F (T_F n_f)^2` | `11/9` |
| `C_F^2 (T_F n_f)` | `1/2` |

(Note: in MSbar the full 3-loop function is degree 2 in `n_f`,
collapsing the 9-channel skeleton to 6 nonzero channels at
`N_f = 6`. The remaining `C_F^3, C_F C_A^2, C_F^2 C_A` are present
in the skeleton but have weight 0 at the `(T_F N_f)^k` cuts that
TVZ tabulates because the polynomial reduction is degree-2 in `n_f`.
The full 9-channel decomposition is recovered before the
`n_f`-polynomial reduction; see TVZ 1980 Eq. (11) and VVL 1997
Appendix A for the unreduced form.)

The TVZ closed-form polynomial gives `β_2 = 2857/2 − (5033/18) n_f
+ (325/54) n_f²`, which at `N_f = 6` evaluates to `−65/2 = −32.5`.

A candidate closes the gate **strictly** if it derives ALL six
non-trivial weights jointly from existing framework context plus the
candidate input. A candidate **partially** closes the gate if it derives some
subset (e.g., the pure-gauge `c_AAA = 2857/54` only). A candidate
**weakly** closes the gate if it derives one structural
relation (e.g., `c_AAA + c_FAA + c_FFA + c_FFF = ?`) that is not
already implied by existing context.

## 2. Three candidate primitives

This note designs and stress-tests three candidate primitives. None
are admitted by this note; each is presented with candidate statement,
assumptions inventory, what-if-wrong analysis, and explicit
honest finding (positive / partial / negative).

### Primitive P_L1-A — Connes-Kreimer Hopf-Subdivergence Primitive

**Candidate statement.** *Consider the Connes-Kreimer Hopf algebra
`H_CK^{QCD}` of 1-particle-irreducible Feynman graphs of QCD as a
candidate combinatorial input. Specifically:*

  1. *The set of vertices of `H_CK^{QCD}` is the set of 1PI
     Feynman graphs `Γ` constructible from the QCD Lagrangian
     (`A_μ^a, ψ, c^a, c̄^a` with the standard quartic and cubic
     interaction vertices). Each `Γ` carries:
     - a set of internal edges `E(Γ)`,
     - an integer loop number `ℓ(Γ) = |E(Γ)| − |V(Γ)| + 1`,
     - a Casimir-tensor evaluation `T(Γ) ∈ {Casimir-monomials}`,
     - a finite-period evaluation `R(Γ) ∈ Q + Q·ζ_3 + Q·ζ_5 + ...`.*
  2. *The coproduct
     `ΔΓ = Σ_{γ ⊆ Γ, γ divergent 1PI} γ ⊗ (Γ/γ)`
     encodes the BPHZ recursive subtraction of subdivergences.*
  3. *The β-function coefficients `β_n` are computed by
     `β_n = Σ_{Γ : ℓ(Γ) = n+1, primitive} (sym(Γ))^{-1} T(Γ) R(Γ)`
     where the sum runs over primitive (no proper divergent
     1PI subgraph) graphs at loop order `n+1`, weighted by their
     symmetry factor.*

**Derivation of β_2 under the candidate.** With P_L1-A assumed as a
candidate input, β_2 is computed by
enumerating 3-loop 1PI primitive graphs of QCD (gluon self-energy,
gluon-fermion vertex, gluon-ghost vertex, etc.), assigning
each a Casimir tensor `T(Γ)` and a finite period `R(Γ)`, summing
with symmetry factors. For 3-loop QCD this enumeration is
~100 graphs; for 4-loop QCD this is ~50,000 graphs (van Ritbergen-
Vermaseren-Larin 1997 count).

**Assumptions inventory.**

  1. *1PI Feynman graphs of QCD* form a well-defined combinatorial
     species (assumes the QCD Lagrangian and its standard vertex set
     are themselves derived or explicitly imported).
  2. *Period evaluation `R(Γ)`* admits a well-defined rational +
     `ζ_n` decomposition. Assumes BPHZ regularization is applicable
     to the framework baseline, but the baseline spatial substrate is
     `Z^3`, not 4D Minkowski plus dimensional regularization.
  3. *Symmetry factors `sym(Γ)`* are determined by graph
     automorphisms — pure combinatorics, no scheme dependence.
  4. *The β_n formula* assumes Gell-Mann–Low evolution applies to
     the framework's running coupling. This is itself an unproved bridge:
     the physical Cl(3) local algebra on the Z^3 spatial substrate has
     a discrete spatial structure, NOT a continuous renormalization-group flow.

**What-if-wrong analysis.**

  - *Wrong-Assumption 1 (1PI Feynman graphs).* If QCD's 1PI graph
    species is not available from framework-native inputs, the candidate cannot be applied. Currently
    the framework carries an `S^P` plaquette action (lattice gauge
    theory at `N_f = 6` quark sector), not a continuum 1PI graph
    expansion. **Open obstruction**: lattice plaquette → continuum 1PI
    requires a Wilsonian → BPHZ matching that is itself a 3-loop
    coefficient.
  - *Wrong-Assumption 2 (BPHZ-applicable).* If BPHZ is applicable to
    Z^3 lattice Feynman expansions only modulo a regulator translation,
    then `R(Γ)` would carry lattice spacing-dependence that is
    NOT pure rational. **Open obstruction**: this is exactly the
    regulator dependence the MSbar-native route context identifies.
  - *Wrong-Assumption 3 (β_n via primitive graphs).* The
    Connes-Kreimer formula relates β_n to PRIMITIVE graph residues
    via the BCH-like expansion of the Hopf-algebraic renormalization
    group. If the framework's running coupling is NOT a Hopf-algebra
    homomorphism into the diffeomorphism group of `Q[[g]]`, the formula
    fails. **Hostile-review reading**: this is essentially the QCD
    perturbative expansion in algebraic clothing — the primitive
    promises closure but actually IMPORTS dim-reg + BPHZ + period
    evaluation under a single name.

**Mathematical/physical interpretation.**
Connes-Kreimer is the *categorification* of perturbative QCD
renormalization. As mathematical structure it is genuine and elegant
(Birkhoff decomposition, Riemann-Hilbert correspondence). As a
*candidate closure input*, it imports the entire QCD perturbative
machinery in three lines.

**Prior literature analog.**
Connes-Kreimer (Comm. Math. Phys. 199, 203, 1998–2000); Connes-Marcolli
"Noncommutative Geometry, Quantum Fields and Motives" (2008);
Brown-Schnetz "Single-valued multiple polylogarithms" (2012) for
period structure. **Critical observation**: in the Connes-Kreimer
framework, the β-function still requires evaluating master integrals
to obtain the rational + `ζ_n` weights; the Hopf algebra organizes
the subtraction structure but does NOT compute the periods themselves.

**Honest finding.** **NEGATIVE on closure.** P_L1-A as stated provides
the algebraic framework but DOES NOT supply the period evaluation
function `R : Γ → Q + Q·ζ_3 + ...`. The latter is exactly the
master-integral evaluation step the MSbar-native route context identifies as
the missing primitive. Adding P_L1-A without an independent
period-evaluation primitive amounts to a notational rewrap of
the existing open gate.

**Sub-finding (positive structural).** P_L1-A *does* organize the
6-channel decomposition cleanly: each primitive 3-loop QCD graph
contributes to exactly one Casimir-tensor channel by its `T(Γ)`
projection, and the channel-weight scalars are exactly the sums
of `(sym(Γ))^{-1} R(Γ)` over graphs with the same `T(Γ)`. This
sharpens the *structure* of the open gate but does not
close it.

### Primitive P_L1-B — Lattice-<P>-Period Bootstrap Primitive

**Candidate statement.** *Consider a single candidate structural input
denoted `B_⟨P⟩`: at canonical operating point `g² = 1, ξ_*` with
`s_t = g²/(2ξ) = 1/(2ξ)`, the framework-native heat-kernel single-
plaquette `⟨P⟩_HK_SU(3)(s_t) = 1 − exp(−(4/3) s_t)` extends to ALL
loop orders by the bootstrap*

```
β_n^⟨P⟩  =  R^{(n+1)}_HK [ ⟨P⟩_HK_SU(3) ]
```

*where `R^{(n+1)}_HK` is the (n+1)-loop residue extraction operator
defined recursively by*

```
R^{(1)}_HK [Q] := lim_{s_t → 0} d/ds_t Q(s_t) = (4/3)  for Q = ⟨P⟩_HK,
R^{(n+1)}_HK [Q] := residue of (Q − Σ_{k≤n} R^{(k)}_HK [Q] s_t^k) / s_t^{n+1}
                                at s_t = 0.
```

*The structural claim is that `β_2^⟨P⟩, β_3^⟨P⟩` are derived from
the closed-form `⟨P⟩_HK` Taylor coefficients alone, in a `⟨P⟩`-scheme.*

**Derivation of β_2.** Computing the ⟨P⟩_HK Taylor coefficients:
`⟨P⟩_HK_SU(3)(s_t) = (4/3) s_t − (8/9) s_t² + (32/81) s_t³ − ...`
and applying the bootstrap definition gives (in this candidate's
convention):
- `R^{(1)}_HK = 4/3`
- `R^{(2)}_HK = −8/9`
- `R^{(3)}_HK = 32/81`

These are clean rational numbers, not requiring scheme conversion.

**Assumptions inventory.**

  1. *⟨P⟩_HK_SU(3) Taylor coefficients ARE the running-coupling
     β-function coefficients in the ⟨P⟩-scheme*. This is the
     load-bearing structural assumption of P_L1-B.
  2. *The ⟨P⟩-scheme is a valid renormalization scheme* in which
     β_2, β_3 are well-defined. (`⟨P⟩` IS framework-native via
     [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md);
     the scheme distinction from MSbar is structurally real in the
     MSbar-native route context.)
  3. *No scheme conversion is needed to compare to MSbar β_2, β_3*.
     This assumption is **almost certainly false**: the ⟨P⟩-scheme β_2
     differs from MSbar β_2 by a finite scheme-conversion factor
     involving 3-loop integrals computed in BOTH schemes.

**What-if-wrong analysis.**

  - *Wrong-Assumption 1.* If ⟨P⟩_HK Taylor coefficients are NOT
    the β_n^⟨P⟩, the bootstrap fails. In fact: ⟨P⟩_HK is the
    plaquette EXPECTATION VALUE in the heat-kernel limit, not the
    β-function coefficient. The β-function in ⟨P⟩-scheme is
    defined by `β^⟨P⟩(α^⟨P⟩) = dα^⟨P⟩/d log Λ^⟨P⟩`, which involves
    cross-correlators of plaquettes at different lattice scales, NOT
    a single-plaquette expansion. The bootstrap conflates *probe
    expectation value* with *running-coupling derivative*.
  - *Wrong-Assumption 2.* In the ⟨P⟩-scheme, `α^⟨P⟩(β_W)` is
    defined via the plaquette inversion `α^⟨P⟩ = α_bare / ⟨P⟩(β_W)`
    (Lüscher-Weisz scheme, 1995 form). The running involves the
    lattice spacing `a` and the Wilson coupling `β_W = 6/g²`, not
    the heat-kernel parameter `s_t` directly. Equating the two
    expansions requires an additional `β_W ↔ s_t` matching that is
    itself a non-trivial scheme conversion. **Open obstruction**:
    this matching is the same lattice-PT computation identified by the
    MSbar-native route context.
  - *Wrong-Assumption 3.* Even if we assume the bootstrap formula,
    it would predict β_2^⟨P⟩ = 32/81 ≈ 0.395. The MSbar value at
    `N_f = 6` is `β_2^MSbar ≈ −32.5`. These differ by ~82×; to
    match them via scheme conversion would itself require 3-loop
    LPT integrals — circling back to the MSbar-native open gate.

**Mathematical/physical interpretation.** P_L1-B promises a clean
"new science" closed form: the framework-native heat-kernel plaquette
literally IS the β-function. The structural objection: the
β-function is defined by a *flow equation*, not a single-point
expectation value. Identifying the two requires the flow equation
to reduce to single-plaquette expansion — which it does at
1-loop and 2-loop (universal coefficients), but NOT beyond.

**Prior literature analog.** Lüscher-Weisz "Two-loop relation between
the bare lattice coupling and the MS coupling" (Phys. Lett. B 349,
165, 1995); Bode-Panagopoulos "The three-loop β-function of QCD with
the clover action" (Nucl. Phys. B 625, 198, 2002); Christou-
Panagopoulos "The three-loop beta-function of SU(N) lattice gauge
theories" (Phys. Lett. B 387, 587, 1996, hep-lat/9609025). All
require explicit 3-loop lattice integrals, not single-plaquette
expansions.

**Honest finding.** **NEGATIVE on closure.** P_L1-B as stated
conflates the ⟨P⟩-scheme single-plaquette expectation value with the
β-function coefficient. The structural identification at orders 1, 2
is universal (β_0, β_1 are scheme-independent), but at order ≥ 3
the β-function coefficient genuinely depends on cross-plaquette
correlators and lattice integral structure that is not captured by
single-point expansion of `⟨P⟩_HK`.

**Sub-finding (positive structural).** The ⟨P⟩-scheme IS framework-
native; the *scheme distinction* between ⟨P⟩ and MSbar IS structurally
real. What P_L1-B fails to provide is the
flow-to-flow conversion, not the scheme context.

### Primitive P_L1-C — Combinatorial Symmetry-Factor Sum-Rule Primitive

**Candidate statement.** *Consider the following structural sum-rule for
β-function channel weights at any loop order `n ≥ 3`:*

```
For each Casimir-tensor channel T_α at loop order n,
  c_α  =  Σ_{Γ ∈ G_n^{T_α}}  (sym(Γ))^{-1}  ·  P_α^{rational}(Γ)
```

*where `G_n^{T_α}` is the species of n-loop QCD primitive 1PI graphs
projecting onto channel T_α under Casimir contraction, `sym(Γ)` is
the graph automorphism order, and `P_α^{rational}(Γ)` is a
graph-period-class invariant taking values in `Q` (3-loop) or
`Q + Q·ζ_3` (4-loop). The species `G_n^{T_α}` and symmetry counts are
treated as candidate combinatorial inputs derivable from QCD vertex rules;
the period classes `P_α^{rational}(Γ)` require a candidate input that
would need explicit approval before admission — a function from primitive
graph cohomology classes to
rational/ζ-extension values.*

**Derivation of β_2.** P_L1-C reduces β_2 channel-weight derivation
to:
  1. Enumerate 3-loop primitive 1PI QCD graphs (combinatorial,
     ~100 graphs).
  2. Compute each graph's Casimir tensor (Lie-algebra primitive,
     existing context — this is the channel-skeleton result carried by the MSbar-native route
     already established).
  3. Compute each graph's symmetry factor (combinatorial).
  4. Compute each graph's *period class* (candidate input requiring explicit approval).

The per-channel rational weight is then a sum of `(sym × period)`
over graphs in that channel.

**Assumptions inventory.**

  1. *The graph period class IS a finite rational + ζ_3 value*.
     This is true for primitive 3-loop QCD graphs (Brown-Schnetz
     period theory, 2012); for 4-loop QCD it is true modulo
     conjectured single-valuedness (Brown 2009).
  2. *Period classes are computable from graph cohomology alone*
     — i.e., they admit a presentation by graph polynomial Symanzik
     determinants without explicit dim-reg subtraction. This is the
     **Schwinger-period viewpoint** (Bloch-Esnault-Kreimer 2006).
  3. *The species `G_n^{T_α}` is finite and combinatorially specifiable*
     — true for QCD at fixed loop order `n`.

**What-if-wrong analysis.**

  - *Wrong-Assumption 1 (period-class field).* For 4-loop QCD, the
    full period class is conjectured to be `Q + Q·ζ_3 + Q·ζ_5`
    (with `ζ_5` first appearing at 5-loop in BPHZ; possibly already
    at 4-loop in some conventions). If `ζ_5` enters β_3 in the
    framework's natural scheme, P_L1-C's `Q + Q·ζ_3` assumption is
    incomplete. **Open obstruction**.
  - *Wrong-Assumption 2 (period-class computability).* The "graph
    period" is, in practice, the value of a Feynman integral with
    all external momenta nullified — i.e., a master integral. As
    of 2026, period evaluation for 4-loop QCD primitives still
    requires computer-algebra reduction to known multiple zeta values
    (Schnetz HyperInt, 2014). The combinatorial candidate therefore
    imports a NON-TRIVIAL computational primitive
    (period evaluation = master integral computation). **Critical
    objection**: this is the same primitive the MSbar-native route identifies
    as foreign.
  - *Wrong-Assumption 3 (symmetry-factor canonicity).* If `sym(Γ)`
    is not uniquely defined for a given primitive graph (e.g.,
    different normalizations for ghost orientation), the channel
    weight formula is ambiguous up to integer rescaling. This is
    a soluble book-keeping question, not a real obstruction.

**Mathematical/physical interpretation.** P_L1-C tries to factor
the obstruction into two parts:
  - the *combinatorial* part (graph enumeration + symmetry
    factors + Casimir contraction), which is available as existing context;
  - the *number-theoretic* part (period class), which is the candidate
    input requiring explicit approval before admission.

If the period-class part is supplied as a "Brown-Schnetz oracle"
returning the Q[ζ_n] value of any primitive graph period, then
β_2, β_3 are determined. But this candidate input is essentially
"supply a Feynman period evaluation function," which is what the
MSbar-native bounded open gate already names as the missing primitive.

**Prior literature analog.** Bloch-Esnault-Kreimer "On motives
associated to graph polynomials" (Comm. Math. Phys. 267, 181, 2006);
Brown-Schnetz "A K3 in φ^4" (Duke Math. J. 161, 1817, 2012);
Brown "Mixed Tate motives over Z" (Ann. Math. 175, 949, 2012);
Panzer-Schnetz "The Galois coaction on φ^4 periods" (Comm. Math.
Phys. 365, 121, 2019). These works develop the period-class
machinery exactly along the lines P_L1-C admits.

**Honest finding.** **NEGATIVE on closure.** P_L1-C's "graph period
class" candidate input is NOT structurally weaker than the MSbar-native
"3-loop master integral" gap — they are the SAME primitive in different
mathematical clothing (Schwinger-parameter Symanzik determinants vs.
dim-reg integrals). P_L1-C would formally close the open gate only by
adding a primitive of comparable strength to the original missing one.

**Sub-finding (positive structural).** P_L1-C *does* sharpen the
*shape* of the open gate: the missing primitive is a
function `P : Primitive 1PI Graphs / (1PI iso) → Q[ζ_n]`, NOT a
miscellaneous "scheme" or "regulator." This is the cleanest known
formulation of the gap.

## 3. What this note provides vs. does not provide

### Closed (positive findings)

- **Sharper formulation of the missing primitive.** The open gate
  can be cleanly stated as: "a function from primitive
  1PI Feynman graph cohomology classes to `Q + Q·ζ_3 + Q·ζ_5 + ...`
  is not framework-derived." This is structurally a NUMBER-THEORETIC
  function, not a scheme choice. (P_L1-C sub-finding.)
- **Hopf-algebra organization is non-load-bearing.** Connes-Kreimer's
  algebraic structure (P_L1-A) cleanly factorizes the renormalization
  procedure but does NOT supply the missing period-evaluation
  function. (P_L1-A sub-finding.)
- **`⟨P⟩`-scheme is framework-native at ⟨P⟩-expectation level but
  NOT at β-function level.** The single-plaquette ⟨P⟩_HK is a probe
  expectation value, not a flow-equation derivative. (P_L1-B
  sub-finding.)

### Closed (negative findings on the candidate primitives)

- **P_L1-A does not close the open gate** — Connes-Kreimer
  organizes BPHZ but does not evaluate periods.
- **P_L1-B does not close the open gate** — the
  ⟨P⟩-scheme single-plaquette expansion is not the flow-equation
  derivative beyond 1-loop / 2-loop universality.
- **P_L1-C does not close the open gate** — it formally
  reduces it to a Brown-Schnetz period-evaluation primitive of
  comparable strength.

### Honest verdict

**No clean candidate primitive closes the L1 channel-weight open gate**
without adding a new primitive of comparable mathematical strength
to the original missing one. The unresolved status of β_2, β_3 scalar
channel weights is genuine; the "best" candidate (P_L1-C)
sharpens the *shape* of the gap to a "Feynman period oracle"
but does not eliminate it.

This conclusion is consistent with the 4-attack-type campaign:
β_2, β_3 channel weights at 3-loop+ are not derived
from existing framework content. The L1 strong-coupling chain must
continue to import β_2, β_3 from QCD literature (TVZ 1980; VVL 1997)
as "imported authority for a bounded-tier theorem" — exactly the
status currently in place.

### What WOULD constitute a positive primitive

A candidate input that *would* close the gate:

- **Hypothetical P_L1-D (physical Cl(3) local algebra / Z^3-native period functor)** — an
  algorithmically specifiable function `P_Cl(3) : 1PI Graph → Q[ζ_n]`
  that:
  1. Reproduces the 3-loop TVZ values `2857/54, ..., 1/2` from
     the physical Cl(3) local algebra on the Z^3 spatial substrate alone,
     *without* importing dim-reg
     master integrals or Brown-Schnetz period theory.
  2. Reproduces the 4-loop VVL `Q + ζ_3` weights similarly.

  No such functor is currently known. The framework's `Z^3` lattice
  substrate carries no canonical period extension to graphs that
  reproduces continuum perturbative Q[ζ_n] periods — establishing
  one would itself be a major result. **This is the concrete shape of
  the open primitive design problem.**

## 4. Context and imports

This note uses the following context and imports. It does not admit any
candidate primitive, and it does not re-ratify any upstream row:

- Physical Cl(3) local algebra and Z^3 spatial substrate baseline
  ([`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)).
- S1 Identification Source Theorem
  ([`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md))
  for `β_0 = (11 N_color − 2 N_quark)/3 = 7`.
- SU(3) quadratic Casimirs `(C_F = 4/3, C_A = 3, T_F = 1/2)`
  ([`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md),
   [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)).
- SU(3) quartic Casimirs `(5/12, 5/2, 135/8)`
  ([`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md)).
- `⟨P⟩_HK_SU(3)(s_t) = 1 − exp(−(4/3) s_t)` framework-native
  closed form
  ([`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)).
This note proposes no new retained primitive. The candidate
primitives P_L1-A, B, C are stress-tested and documented as
non-load-bearing (each fails to close the open gate cleanly).

**Imported authorities (numerical comparators only, NOT load-bearing):**

- TVZ 1980 (Phys. Lett. B 93, 429): `β_2^MSbar` 6-channel rationals.
- Larin-Vermaseren 1993 (Phys. Lett. B 303, 334): `β_2^MSbar`
  refinement.
- van Ritbergen-Vermaseren-Larin 1997 (Phys. Lett. B 400, 379,
  hep-ph/9701390): `β_3^MSbar` 14+-channel rationals + ζ_3.
- Czakon 2005 (Nucl. Phys. B 710, 485): `β_3^MSbar` verification.
- Connes-Kreimer 1998 (Comm. Math. Phys. 199, 203): Hopf algebra
  of graphs.
- Connes-Kreimer 2000 (Comm. Math. Phys. 210, 249, hep-th/0003188):
  Riemann-Hilbert and the β-function.
- Bloch-Esnault-Kreimer 2006 (Comm. Math. Phys. 267, 181):
  graph polynomials and motives.
- Brown-Schnetz 2012 (Duke Math. J. 161, 1817): K3 in φ^4 periods.
- Lüscher-Weisz 1995 (Phys. Lett. B 349, 165): bare-to-MSbar
  matching at 2-loop.
- Bode-Panagopoulos 2002 (Nucl. Phys. B 625, 198): 3-loop
  lattice β-function with clover action.
- Christou-Panagopoulos 1996 (Phys. Lett. B 387, 587,
  hep-lat/9609025): 3-loop β-function in SU(N) lattice gauge theory.

These are imported authorities for an open-gate probe;
the runner verifies them at the level of identity-check and
structural-decomposition cross-check, NOT framework-native
derivation of channel weights.

## 5. Implementation overview

The runner [`scripts/cl3_primitive_p_l1_2026_05_10_pPl1.py`](../scripts/cl3_primitive_p_l1_2026_05_10_pPl1.py)
implements:

1. **PASS Section 1**: Document the open-gate shape (9-channel
   3-loop skeleton, six nonzero TVZ rational weights; 14+ 4-loop
   channels with VVL rationals + ζ_3) for reference.
2. **PASS Section 2**: Verify the existing `β_0, β_1` reductions
   at `N_f = 6` from S1 + Casimir algebra.
3. **PASS Section 3 (P_L1-A)**: Construct the P_L1-A Hopf algebra
   abstractly (3-loop QCD primitive graphs ↦ Casimir-tensor channels)
   and demonstrate that without an independent period-evaluation
   function, the channel weights remain free. Verify via a
   3-loop "minimal example" (1 graph → 1 channel, weight free).
4. **PASS Section 4 (P_L1-B)**: Reproduce the `⟨P⟩_HK_SU(3)` Taylor
   coefficients `4/3, −8/9, 32/81` and demonstrate that they do NOT
   match the MSbar β-function values `−65/2 = −32.5` (off by ~82×
   at 3-loop). Document the conflation between probe expectation and
   flow derivative.
5. **PASS Section 5 (P_L1-C)**: Demonstrate the species
   factorization: enumerate the 6 3-loop QCD primitive Casimir-tensor
   channels at `N_f = 6` and show that the channel weights are
   determined by per-graph period values multiplied by sym factors.
   Document that the period evaluation function is the missing
   primitive.
6. **OPEN Section 6**: The open gate stands; no candidate primitive
   closes it cleanly. Document the hypothetical P_L1-D shape as a
   physical Cl(3) local algebra / Z^3-native period functor design problem.
7. **HONEST verdict**: open_gate; NEGATIVE on closure; positive on
   sharpening the *shape* of the open gate.

## 6. Dependencies

- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) —
  physical Cl(3) local algebra and Z^3 spatial substrate baseline.
- [`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md)
  for the V probe foreclosure.
- [`KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md`](KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md)
  for the S probe foreclosure.
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
  for the `C_F = 4/3` value.
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
  for the `C_A = 3` value.
- [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)
  for `⟨P⟩_HK_SU(3) = 1 − exp(−(4/3) s_t)` framework-native form.

## 7. Boundaries

This note does NOT claim:

- **A framework-native closed form for β_2 or β_3 in any scheme.**
  The honest verdict is that the MSbar-native bounded open gate stands
  unchanged; no candidate primitive proposed here closes it.
- **Promotion of any candidate primitive (P_L1-A, B, C) to retained
  status.** Each is stress-tested and documented as non-load-bearing.
- **A new axiom.** The framework baseline remains the physical Cl(3)
  local algebra on the Z^3 spatial substrate. The candidates test whether
  well-known mathematical structures (Hopf algebra of graphs;
  ⟨P⟩-scheme bootstrap; combinatorial symmetry-factor sum-rule) can close
  the gate without adding a new admitted primitive; all three fail that test.
- **Closure of the L1 strong-coupling chain.** β_2, β_3 continue to
  be imported from QCD literature.
- **Lane 1 alpha_s(M_Z) status change.** Unchanged.

## 8. Context summary

| Candidate primitive | Type | Closure verdict | Fail mode |
|---|---|---|---|
| **P_L1-A** Hopf-Subdivergence | algebraic organization | NEGATIVE | period evaluation function still missing |
| **P_L1-B** ⟨P⟩-scheme bootstrap | scheme-native expansion | NEGATIVE | conflates probe expectation with flow derivative |
| **P_L1-C** Combinatorial sum-rule | structural decomposition | NEGATIVE | "graph period oracle" = master-integral primitive |
| **P_L1-D** (hypothetical) physical Cl(3) local algebra / Z^3-native period functor | candidate input requiring explicit approval before admission | OPEN DESIGN PROBLEM | not yet known to exist |

| Quantity | Contextual role after this note | Source |
|---|---|---|
| `β_0 = 7, β_1 = 26` at N_f = 6 | existing repo context; not re-ratified here | S1 + Casimir algebra |
| 9-channel 3-loop Casimir skeleton | existing group-theory context; not re-ratified here | MSbar-native route context |
| 14+-channel 4-loop quartic Casimir extension | existing group-theory context; not re-ratified here | V-L1-Quartic + MSbar-native route context |
| `⟨P⟩_HK_SU(3) = 1 − exp(−(4/3) s_t)` | existing closed-form context; not re-ratified here | C_ISO SU(3) NLO |
| 6-channel 3-loop scalar weights `2857/54, ..., 1/2` | NOT DERIVABLE | imported (TVZ 1980) |
| 14+-channel 4-loop scalar weights | NOT DERIVABLE | imported (VVL 1997) |
| Hopf-algebra organization of BPHZ | structural primitive (not load-bearing) | Connes-Kreimer 2000 |
| ⟨P⟩-scheme expansion bootstrap | non-bootstrap-equivalent to flow | this probe |
| Combinatorial sum-rule species factorization | sharpened open-gate shape | this probe |

## 9. Falsifiable structural claims

1. The Connes-Kreimer Hopf algebra of QCD 1PI graphs admits a
   subdivergence coproduct that organizes BPHZ recursively. This is
   imported standard mathematics; the runner verifies the structure
   via a simple 3-vertex toy graph example.
2. The ⟨P⟩_HK_SU(3) Taylor expansion `4/3 s_t − 8/9 s_t² + 32/81 s_t³`
   reproduces the closed-form heat-kernel single-plaquette expectation
   at small `s_t`. The runner cross-checks the expansion against
   direct evaluation of `1 − exp(−(4/3) s_t)`.
3. The 3-loop QCD β-function at `N_f = 6` evaluates to
   `−65/2` from the TVZ closed-form polynomial
   `2857/2 − (5033/18) n_f + (325/54) n_f²` at `n_f = 6`. The
   runner reproduces this value to confirm the comparator.
4. Each of the 6 independent 3-loop Casimir-tensor channels at
   SU(3), `N_f = 6` evaluates to the standard value (`64/27, 16/3,
   12, 27, 12, 27`, etc.) — the runner re-checks these values
   from the existing `(C_F, C_A, T_F)` Casimirs (parallel to
   standard SU(3) Casimir algebra).
5. None of the three candidate primitives (P_L1-A, P_L1-B, P_L1-C)
   provides the missing period-evaluation function. The runner
   demonstrates each failure mode explicitly.

## 10. Reproduction

```bash
python3 scripts/cl3_primitive_p_l1_2026_05_10_pPl1.py
```

Expected: a sequence of PASS lines for the support context checks
(`β_0`, `β_1`, Casimir channel values, `⟨P⟩_HK` Taylor coefficients,
TVZ polynomial value at `N_f = 6`), followed by structural-failure
documentation lines for each of the three candidate primitives,
and a final summary classifying the verdict as
`open_gate` with NEGATIVE-on-closure and POSITIVE-on-shape-sharpening
sub-findings.

## 11. References

- Tarasov O.V., Vladimirov A.A., Zharkov A.Yu. (1980), *The
  Gell-Mann-Low function of QCD in the three-loop approximation*,
  Phys. Lett. B 93, 429. [TVZ 1980]
- Larin S.A., Vermaseren J.A.M. (1993), *The three-loop QCD
  β-function and anomalous dimensions*, Phys. Lett. B 303, 334.
- van Ritbergen T., Vermaseren J.A.M., Larin S.A. (1997), *The
  four-loop β function in quantum chromodynamics*, Phys. Lett. B 400,
  379, hep-ph/9701390. [VVL 1997]
- Czakon M. (2005), *The four-loop QCD β-function and anomalous
  dimensions*, Nucl. Phys. B 710, 485.
- Baikov P.A., Chetyrkin K.G., Kühn J.H. (2017), *Five-Loop Running
  of the QCD coupling constant*, Phys. Rev. Lett. 118, 082002.
- Connes A., Kreimer D. (1998), *Hopf algebras, renormalization and
  noncommutative geometry*, Comm. Math. Phys. 199, 203.
- Connes A., Kreimer D. (2000), *Renormalization in QFT and the
  Riemann-Hilbert problem II: the β-function*, Comm. Math. Phys.
  216, 215, hep-th/0003188.
- Bloch S., Esnault H., Kreimer D. (2006), *On motives associated
  to graph polynomials*, Comm. Math. Phys. 267, 181.
- Brown F., Schnetz O. (2012), *A K3 in φ⁴*, Duke Math. J. 161,
  1817.
- Brown F. (2012), *Mixed Tate motives over Z*, Ann. Math. 175, 949.
- Panzer E., Schnetz O. (2019), *The Galois coaction on φ⁴ periods*,
  Comm. Math. Phys. 365, 121.
- Lüscher M., Weisz P. (1995), *Two-loop relation between the bare
  lattice coupling and the MS coupling in pure SU(N) gauge theories*,
  Phys. Lett. B 349, 165.
- Christou C., Panagopoulos H. (1996), *The three-loop β-function in
  SU(N) lattice gauge theories*, Phys. Lett. B 387, 587,
  hep-lat/9609025.
- Bode A., Panagopoulos H. (2002), *The three-loop β-function of
  QCD with the clover action*, Nucl. Phys. B 625, 198.
- van Baalen G., Kreimer D., Uminsky D., Yeats K. (2009), *The QCD
  β-function from global solutions to Dyson-Schwinger equations*,
  Annals Phys. 325, 300.
- Banks T., Zaks A. (1982), *On the phase structure of vector-like
  gauge theories with massless fermions*, Nucl. Phys. B 196, 189.
- Reshetikhin N., Turaev V.G. (1991), *Invariants of 3-manifolds via
  link polynomials and quantum groups*, Invent. Math. 103, 547.
