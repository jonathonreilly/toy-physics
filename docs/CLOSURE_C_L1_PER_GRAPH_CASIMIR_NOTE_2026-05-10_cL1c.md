# Closure C-L1c --- Six-Channel Casimir Span and Assignment/Weight Split

**Date:** 2026-05-10
**Claim type:** bounded_theorem (scoped six-channel span plus
assignment/weight split; no retained-grade theorem status change)
**Sub-gate:** Lane 1 (alpha_s) --- narrows one sub-admission named by
[`PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md`](PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md)
on QCD beta_2 channel-weight admission. Specifically targets
sub-admission (c): per-graph Casimir channel projection. Sub-admissions
(a) HK <-> MSbar scheme conversion and (b) c_2 invariant -> rational
coefficient extraction are NOT closed here.
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note proposes a closure for review; it does not
claim retention of any new content beyond what is named.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_closure_c_l1c_2026_05_10_cL1c.py`](../scripts/cl3_closure_c_l1c_2026_05_10_cL1c.py)
**Cached output:** [`logs/runner-cache/cl3_closure_c_l1c_2026_05_10_cL1c.txt`](../logs/runner-cache/cl3_closure_c_l1c_2026_05_10_cL1c.txt)

## 0. Context --- the (c) admission

[Probe P-L1-D --- Period Functor Construction](PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md)
decomposed the L1 channel-weight admission into three structurally
independent sub-admissions:

> **Missing ingredient (a)** --- HK <-> MSbar scheme conversion at 3-loop
> [`Alles-Feo-Panagopoulos 1996, Bode-Panagopoulos 2002`]
>
> **Missing ingredient (b)** --- c_2 invariant -> rational coefficient
> extraction [`Brown-Schnetz period theory`]
>
> **Missing ingredient (c)** --- per-graph Casimir channel projection,
> i.e., the channel-by-channel rational decomposition of the TOTAL
> period into the 6 TVZ monomial weights (`2857/54, -1415/54, -205/18,
> 79/54, 11/9, 1/2`) requires per-graph period evaluation per channel
> --- a combinatorial bookkeeping operation that compounds (a) and (b).

This note examines (c) and SEPARATES it into:

- **(c.1) Channel ASSIGNMENT** --- for a specified 3-loop 1PI color
  skeleton Γ contributing to the gluon self-energy, what is its
  Casimir-product channel inside the 6-channel beta_2 span? This is
  algebraic: it depends on the graph topology and the stated SU(3)
  birdtrack identities, NOT on integration. This note does not enumerate
  the full 3-loop graph catalogue.

- **(c.2) Channel WEIGHT** --- what is the scalar rational coefficient
  multiplying that channel? This requires (a) the period value of the
  graph and (b) the symmetry factor `1 / |Aut(Γ)|`. Weight extraction
  IS coupled to (a) and (b) admissions.

The split is the substantive content of this closure note: it shows
that the six-channel span and a deterministic assignment procedure are
available from the stated source dependencies, while (c.2) inherits the
X-L1-MSbar bounded/open weight boundary unchanged.

## 1. Bounded Theorem (Span and Split)

**Theorem (C-L1c; six-channel span and assignment/weight split).** Let
Γ be a specified 3-loop 1PI color skeleton contributing to the QCD gluon
self-energy with external gauge field A^a_µ. Then:

**(K1) Channel span is source-dependency-derivable.** The possible
Casimir-product channels of Γ lie in {C_A^3, C_A^2 (T_F n_f),
C_F C_A (T_F n_f), C_A (T_F n_f)^2, C_F (T_F n_f)^2, C_F^2 (T_F n_f)},
as determined by:
- the graph topology Top(Γ)
- the number L_q(Γ) of closed fermion loops
- the standard SU(3) birdtrack reduction using the stated source identities

**(K2) Channel projection is purely algebraic.** The color factor C(Γ)
of Γ is computable by birdtrack reduction using only:
- [T^a, T^b] = i f^{abc} T^c        (SU(3) Lie algebra)
- Tr[T^a T^b] = T_F · δ^{ab}        (trace normalization)
- f^{acd} f^{bcd} = C_A · δ^{ab}    (adjoint Casimir)
- T^a T^a = C_F · 1                 (fundamental Casimir on |R|=N_F)

No 3-loop integral, no master integral, no period information enters
the channel projection.

**(K3) Channel assignment is deterministic for a specified color
skeleton.** Birdtrack reduction gives a deterministic reduced color
polynomial for a specified graph skeleton. This note verifies
representative reductions and the full six-channel span; it does not
claim an exhaustive per-graph catalogue of all 3-loop 1PI graphs. The
assignment procedure does NOT depend on (a) scheme conversion or (b)
period rationality. Hence the projection map

```
Ch : {3-loop 1PI gluon SE graphs}  →  {6 Casimir channels of beta_2}
```

is the bounded target supplied by this note, with full catalogue
enumeration left to downstream audit or tooling if needed.

**(K4) Channel WEIGHT is NOT closed here.** The scalar rational
coefficient `w(Γ) ∈ Q` weighting graph Γ's contribution within its
channel Ch(Γ) requires:
- the period value `Per(Γ) ∈ Q[ζ_n]` from analytic integration --- this
  is (a)+(b) compound
- the symmetry factor `1 / |Aut(Γ)|` --- graph-theoretic

So `w(Γ)` factorizes as `Per(Γ) / |Aut(Γ)|`; only the second factor is
graph-theoretic. Channel WEIGHT closure inherits the X-L1-MSbar
bounded/open boundary UNCHANGED.

**(K5) Six TVZ channels are exhausted by the bounded projection span.** The
image of `Ch` is the full 6-channel basis of beta_2 (TVZ 1980; Larin-
Vermaseren 1993; Czakon 2005). No 3-loop 1PI graph contributes outside
this 6-channel span. Hence the SPAN of the channel projection is
source-dependency determined, with TVZ used as a literature comparator.

## 2. Constructive birdtrack algorithm for Ch(Γ)

The algorithm to assign a graph Γ to its Casimir channel uses only the
four stated identities listed in (K2) above. We describe it explicitly.

### 2.1 Vertex Catalog (Color Level)

A 1PI gluon-self-energy graph at 3-loop has internal vertices of three
types, with color factors:

| Vertex type        | Color factor             | Source                |
|--------------------|--------------------------|-----------------------|
| 3-gluon            | `f^{abc}`               | gauge sector          |
| 4-gluon            | sum of `f^{abe} f^{cde}` over pairings | gauge sector |
| quark-gluon-quark  | `(T^a)_{ij}`            | matter sector         |
| ghost-ghost-gluon  | `f^{abc}` (anti)         | gauge fixing          |

All four are standard color-level inputs in the upstream SU(3) source
chain (see [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md),
[`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md),
and [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)).

### 2.2 Topology -> color factor (per-graph)

Given Γ with vertices V(Γ) and internal lines E(Γ):

1. Label each gluon internal line with adjoint index a_i ∈ {1, ..., 8}.
2. Label each fermion internal line with fundamental indices i, j ∈ {1, ..., 3}.
3. Replace each vertex with its color factor (from Section 2.1).
4. Sum/integrate over all internal color indices.
5. **External gluon legs:** Γ has two external gluons (gluon self-energy).
   Their color indices are matched against an outer `δ^{ab}` (the
   color-singlet projector on the self-energy basis).

The result is a rational multiple of `δ^{ab}`; the rational coefficient
is C(Γ).

### 2.3 Reduction to Casimir channels

After steps 1-5, repeatedly apply the four retained identities of (K2)
to reduce C(Γ) to a polynomial in `C_F, C_A, T_F·n_f`. Each application
is a graph-rewriting move on the color skeleton. By the standard
birdtrack reduction theorem (Cvitanovic 2008), this terminates in a
unique polynomial.

**Loop counting argument for channel structure.** A 3-loop graph Γ has
L(Γ) = 3 loops. After color-factor reduction:

- The number of `T_F` factors equals the number of closed quark loops
  L_q(Γ).
- Each quark loop contributes one `n_f` factor (sum over flavors).
- Hence the channel of Γ contains `(T_F n_f)^{L_q(Γ)}` factor.
- The remaining factor is in `Q[C_F, C_A]` of total degree `3 - L_q(Γ)`
  (where degree counts factors of quadratic Casimir).
- **C_F-source rule:** A `C_F` factor can arise ONLY through
  the contraction `T^a T^a = C_F · 1` on a fundamental-rep line. In
  1PI gluon-self-energy graphs the only fundamental-rep lines are the
  closed quark loops, so `C_F` requires `L_q(Γ) ≥ 1`. If `L_q = 0`,
  the only Casimir available is `C_A` (from `f^{acd} f^{bcd}` adjoint
  contractions), giving the single pure-gauge channel `C_A^3`.

The 3-loop 1PI gluon-self-energy graphs fall into three classes by
L_q(Γ):

| L_q | (T_F n_f)^k | Remaining Casimir degree | Channels reached         |
|-----|-------------|--------------------------|--------------------------|
| 0   | (T_F n_f)^0 | 3 (pure gauge, C_F forbidden) | C_A^3 (1 channel)    |
| 1   | (T_F n_f)^1 | 2                        | C_A^2, C_F C_A, C_F^2 (3 ch.) |
| 2   | (T_F n_f)^2 | 1                        | C_A, C_F (2 channels)    |

Total: 1 + 3 + 2 = 6 channels. This exhausts the TVZ 6-channel basis
of beta_2 EXACTLY.

The structural argument:

- **For L_q = 0:** no quark loops, no fundamental-rep line for
  `T^a T^a -> C_F · 1` contraction; only `f`-vertex contractions
  reducing via `f^{acd} f^{bcd} = C_A δ^{ab}`. At 3-loop the only
  possible reduction is `C_A^3` (Jacobi closure on the gauge sector).
- **For L_q = 1:** one quark loop closes a `Tr[T^{a_1} ... T^{a_n}]`
  factor; the trace contracts to a polynomial in `C_F, C_A` of degree
  2. Possible reductions include `C_F^2` (via two `T^a T^a` within
  the trace), `C_F C_A` (one `T^a T^a` and one `f f`), or `C_A^2`
  (no `C_F` factors, just `f f` reductions).
- **For L_q = 2:** two disjoint quark loops, each contributing a
  trace, plus exactly one remaining gauge attachment between them.
  The pair contracts via either a `f^{abc} f^{abd} = C_A δ^{cd}` link
  (giving `C_A` total) or a `T^a` insertion on one loop closing back
  through `T^a T^a = C_F` (giving `C_F` total). The 2 channels are
  `C_A (T_F n_f)^2` and `C_F (T_F n_f)^2`.

This is a structural enumeration; no 3-loop integral enters.

### 2.4 Worked example: 3-loop "kite" graph (sunset with 1 quark loop)

Consider the 3-loop graph: two gluon lines forming a quark-loop with
self-energy insertion. Topology:

```
gluon_in --[3g]-- quark_loop --[3g]-- gluon_out
                      |
                  (gluon self-energy bubble)
```

L_q = 1 (one quark loop); two 3-gluon vertices at the external legs;
one closed gluon-self-energy bubble (with another internal quark or
gluon loop --- depending on subgraph topology).

Color factor by birdtracks: `Tr[T^a T^b] · (gauge bubble color)`. The
trace contracts to `T_F · δ^{ab}`; the gauge bubble color is either
`C_A · δ^{ab}` (gluon bubble) or `T_F n_f · δ^{ab}` (quark bubble).

So Ch(this graph) is either:
- `T_F · C_A · δ^{ab}` -> `C_A · T_F n_f` channel (after external factor)
- `T_F · T_F n_f · δ^{ab}` -> `(T_F n_f)^2` channel

Each topology variant is unambiguously assigned to one channel by birdtrack
reduction --- no integration needed.

## 3. Why (c.1) Narrows But (c.2) Does Not Close

### Narrows (c.1) Channel Assignment

The projection target `Ch : Γ -> {6 channels}` is well-defined under the
stated source dependencies. The sufficient source inputs are:

1. Graph topology (combinatorial)
2. SU(3) Lie algebra
   ([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md),
   [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md),
   [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md))
3. Birdtrack reduction algorithm as standard SU(N) color algebra
4. Loop-counting `(L_q, L_g)`

The "what channel is graph Γ in?" question is answered by the algorithm
of Section 2 without any reference to 3-loop integrals, periods, or
scheme conversion.

**This is a non-trivial finding.** The (c) admission of P-L1-D was
phrased as "channel-by-channel rational decomposition...requires per-
graph period evaluation per channel." Re-reading this, the load-bearing
phrase is "per-graph period evaluation": the channel ASSIGNMENT is
algebraic and source-local, while the channel WEIGHT requires period
evaluation. This note formalizes the split without changing audit status
for the upstream chain.

### Does not close (c.2) channel WEIGHT

The scalar rational `w(Γ) = Per(Γ) / |Aut(Γ)|` requires:

- `Per(Γ)` --- analytic period from integration; needs (a) HK -> MSbar
  scheme conversion if working in MSbar, AND (b) c_2 -> rational
  coefficient extraction if the period has transcendental class
  (e.g., K_4 = 6·zeta_3 needs the coefficient 6 extracted from c_2).
- `|Aut(Γ)|` --- graph automorphism count (combinatorial).

Only the `|Aut(Γ)|` factor is graph-theoretic. Period evaluation is the
compound (a)+(b) frontier.

**Hence channel WEIGHTS for beta_2 remain bounded/open; the
assignment-span side is narrowed but not elevated to retained status.**

## 4. Verification --- TVZ channel structure matches 6-channel span

The standard TVZ 1980 polynomial form of beta_2 is

```
beta_2 = 2857/2 - (5033/18) n_f + (325/54) n_f^2
```

This is degree 2 in `n_f`, equivalent to expansion in `(T_F n_f)` of
degree 2. After substituting `T_F = 1/2`:

```
n_f^0 coefficient -> pure-gauge channels (no T_F n_f)        -> 1 channel
n_f^1 coefficient -> 1 quark-loop channels (factor T_F n_f)  -> 3 channels
n_f^2 coefficient -> 2 quark-loop channels (factor (T_F n_f)^2)-> 2 channels
```

Total: 1 + 3 + 2 = 6 channels. Matches Section 2.3 enumeration EXACTLY.

This is the **verification** that the source-dependency channel-span
algorithm (Section 2) yields the SAME 6-channel span as TVZ 1980.

The 6-channel SPAN is determined; the per-channel WEIGHTS still require
integration. This is the precise statement that the closure note
establishes:

```
[BOUNDED (c.1) per-graph channel assignment/span]
Algorithm Ch in Section 2 is defined from stated source dependencies.
Image of Ch is the 6-channel TVZ basis of beta_2.

[BOUNDED (c.2) per-channel weight]
w(Γ) = Per(Γ) / |Aut(Γ)|, where Per(Γ) requires (a)+(b) closure.

[INHERITED open/bounded boundary]
beta_2 / beta_3 channel WEIGHTS in MSbar: NOT framework-derivable.
The X-L1-MSbar bounded admission stands unchanged on weights.
```

## 5. Three structural verification tests (in the runner)

The runner `cl3_closure_c_l1c_2026_05_10_cL1c.py` executes three
structural tests:

### 5.1 Test 1 --- Channel-projection algorithm produces 6 channels

Apply the Section 2.3 enumeration to L_q ∈ {0, 1, 2} and check that
the channel basis is exactly the 6-channel TVZ basis:
`{C_A^3, C_A^2 (T_F n_f), C_F C_A (T_F n_f), C_F^2 (T_F n_f),
   C_A (T_F n_f)^2, C_F (T_F n_f)^2}`.

This is a structural test: enumerate 3 quark-loop classes, count
distinct Casimir products with total degree 3, get 6.

### 5.2 Test 2 --- Birdtrack reduction gives unique channel per graph

For each of three representative 3-loop graph topologies (the sunset-
with-quark-loop, the triangle-of-bubbles, the ladder-with-quark-loop),
explicitly compute the color factor by birdtrack reduction and verify
deterministic channel assignment for those representatives.

### 5.3 Test 3 --- TVZ polynomial degree-in-n_f matches enumeration

Verify that TVZ closed form `beta_2(n_f)` is degree 2 in `n_f`, and that
the channel enumeration of Section 2.3 produces exactly `(T_F n_f)^0`,
`(T_F n_f)^1`, `(T_F n_f)^2` channels. This is the cross-check that
the channel SPAN matches the literature value's polynomial structure.

### 5.4 Test 4 --- Inherited bounded admission unchanged

Verify that the X-L1-MSbar bounded/open boundary on channel WEIGHTS is
NOT contradicted by this closure: the per-channel weights `2857/54,
-1415/54, -205/18, 79/54, 11/9, 1/2` are NOT derived here and remain
outside the source-derived result.

## 6. Honest verdict

| Question                                          | Answer       |
|---------------------------------------------------|--------------|
| Is the six-channel assignment span source-derived? | YES (bounded) |
| Is the algorithm `Ch` framework-dependency-derived? | YES (Section 2)|
| Does the channel SPAN match TVZ (6 channels)?     | YES (Section 4)|
| Is per-channel WEIGHT closed by this note?        | NO (bounded/open boundary)|
| Does X-L1-MSbar bounded admission still stand?    | YES (unchanged) |
| Is one of the three P-L1-D sub-admissions narrowed? | YES (narrow (c.1))|

**Tier classification:** `bounded_theorem` overall. It narrows the
(c.1) channel-assignment/span claim but does not elevate it to a
retained-grade theorem. The (c.2) channel-weight and (a) scheme
conversion and (b) period extraction frontiers stand unchanged.

## 7. Probe-Assumption Stress Tests

### Probe Assumption 1: Each specified 3-loop color skeleton has a deterministic channel

**Status:** BOUNDED. The birdtrack reduction theorem (Cvitanovic 2008)
gives a deterministic polynomial in `C_F, C_A, T_F n_f` after
reduction. The runner verifies representative color skeletons and the
six-channel span. An exhaustive graph catalogue is not claimed here.

### Probe Assumption 2: The channel can be read off the graph structure without integration

**Status:** CONFIRMED. Loop-counting (L_q vs. L_g) plus the algebraic
identity `f^{acd} f^{bcd} = C_A δ^{ab}` (and `T^a T^a = C_F · 1`)
suffice; no momentum integration.

### Probe Assumption 3: SU(3) Casimirs + graph topology + standard 't Hooft double-line counting suffice

**Status:** BOUNDED. The source dependencies (SU(3) Lie algebra +
trace normalization + adjoint Casimir + fundamental Casimir) is exactly
the standard birdtrack algebra. 't Hooft double-line is one diagrammatic
realization; the underlying algebra is identical.

### Probe Assumption 4: There exist explicit closed-form rules for assigning channels

**Status:** CONFIRMED. The algorithm of Section 2 is closed-form.
Verified against TVZ 1980 channel structure.

### Stress-test: what if channel assignment requires diagram coloring beyond what's retained?

**Investigation.** Are there 3-loop graphs requiring quartic Casimir
contributions that aren't in the 6-channel basis? The
[`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md)
source note and TVZ polynomial both report no beta_2 quartic Casimirs;
the TVZ closed-form
polynomial is degree 2 in `n_f`, structurally excluding higher Casimir
products. Hence no extension beyond the 6 channels of Section 2.3 is
needed.

### Stress-test: what if some channels have AMBIGUOUS graph contributions?

**Investigation.** Could two distinct graph topologies map to the same
channel? YES, multiple graphs can map to one channel (different
analytic periods, same color factor). This is NOT ambiguous channel
assignment --- it means MANY graphs contribute to ONE channel, each
with its own weight `w(Γ)`. The sum `Σ_Γ in Ch^{-1}(channel) w(Γ)`
equals the TVZ rational coefficient. The MAP `Ch` is well-defined and
many-to-one. This does not weaken (c.1) closure.

## 8. Source Dependencies and Imports

This bounded theorem uses the following source dependencies and imports:

- physical Cl(3) local algebra and Z^3 spatial substrate
  ([`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md))
- S1 Identification Source Theorem ([`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md))
  for `beta_0 = (11 N_color - 2 N_quark)/3 = 7`
- SU(3) quadratic Casimirs `(C_F = 4/3, C_A = 3, T_F = 1/2)`
  ([`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md),
   [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md))
- `<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3) s_t)` framework-native closed form
  ([`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md))
- P-L1-D primitive construction attempt ([`PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md`](PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md))
- V-L1-Quartic beta_2/quartic-Casimir boundary
  ([`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md))

This note proposes no new retained primitive. The channel-projection
algorithm uses only the named source dependencies and standard SU(N)
color algebra. It is a bounded structural clarification of the P-L1-D
(c) sub-admission.

**Imported authorities (numerical comparators only, NOT load-bearing):**

- TVZ 1980 (Phys. Lett. B 93, 429): MSbar 3-loop six-channel rationals
- Larin-Vermaseren 1993 (Phys. Lett. B 303, 334): explicit channel weights
- Czakon 2005 (Nucl. Phys. B 710, 485): MSbar 4-loop verification
- Cvitanovic 2008 (Princeton UP): *Group Theory: Birdtracks, Lie's, and
  Exceptional Groups*. The birdtrack reduction theorem for SU(N) color
  algebras.
- van Ritbergen-Vermaseren-Larin 1997 (Phys. Lett. B 400, 379): explicit
  4-loop color-tensor decomposition (for context on the 6-channel limit)

## 9. Falsifiable structural claims

1. The 6-channel span of beta_2 is exhausted by L_q ∈ {0, 1, 2} graphs
   at 3-loop, giving 1 + 3 + 2 = 6 distinct Casimir products of total
   degree 3.
2. The TVZ closed form `beta_2 = 2857/2 - (5033/18) n_f + (325/54) n_f^2`
   has polynomial degree exactly 2 in `n_f` (confirmed; no `n_f^3`).
3. For a specified 3-loop 1PI gluon-self-energy color skeleton, the
   birdtrack reduction algorithm deterministically places its reduced
   color factor in the six-channel span. This note does not enumerate
   every 3-loop graph.
4. The SU(3) algebraic identities (4 listed in Section 2.2)
   are sufficient for channel projection at 3-loop.
5. No 3-loop graph contributes to any quartic-Casimir channel
   (`d_F^abcd`, `d_A^abcd`); these first appear at 4-loop in the cited
   V-L1-Quartic source note and standard QCD color decomposition.

## 10. Boundaries

This note does NOT claim:

- **Per-channel WEIGHT closure.** w(Γ) = Per(Γ) / |Aut(Γ)| still
  requires the period Per(Γ), which is the (a)+(b) compound frontier.
- **Resolution of P-L1-D as a whole.** Only sub-admission (c.1) is
  narrowed; (c.2), (a), (b) stand unchanged.
- **A new retained primitive.** The birdtrack reduction algorithm uses
  only the named source dependencies; it is a structural clarification,
  not a new primitive proposal.
- **Beta_3 closure.** The 4-loop case has 12+ channels (including
  quartic Casimirs from V-L1-Quartic). Channel ASSIGNMENT at 4-loop
  is more complex and not addressed here.

## 11. Hostile-review self-audit Q1-Q7

**Q1.** Is the algorithm `Ch` truly framework-dependency-derived, or
does it require imports beyond the named source dependencies?

> *A.* The four identities in (K2) are the named source dependencies.
> Birdtrack reduction is the application of these identities iteratively;
> no further primitive is introduced by this note.

**Q2.** Does this closure load-bear any 3-loop integral primitive?

> *A.* No. Channel assignment is purely algebraic; no momentum integration,
> no master integral, no period information enters. Period information
> is needed for the WEIGHT, not the channel.

**Q3.** Is the 6-channel basis a literature import that's being
"verified" or framework-derived?

> *A.* The 6-channel span is derived in Section 2.3 by
> structural enumeration (3 quark-loop classes × 1+3+2 channels =
> 6 channels). The TVZ-1980 polynomial form is a literature comparator
> verifying the same span.

**Q4.** Could there be 3-loop graphs producing color factors outside
the 6 channels?

> *A.* No beta_2 quartic channel is needed in this model. The
> [`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md)
> source note and TVZ degree check both support no beta_2
> quartic-Casimir contributions, and by birdtrack reduction every
> 3-loop diagram reduces to a polynomial of total Casimir degree 3,
> spanning exactly the 6 channels of Section 2.3.

**Q5.** Is channel projection ambiguous for any graph (i.e., does any
graph map to multiple channels)?

> *A.* For a specified color skeleton, birdtrack reduction gives a
> deterministic polynomial in `C_F, C_A, T_F n_f`. The runner verifies
> representative reductions and the full six-channel span. An exhaustive
> per-graph catalogue is not claimed by this note.

**Q6.** Could the "channel WEIGHT not closed" finding be a relabeling
of work already supplied by the named source dependencies?

> *A.* No. Period extraction (a, b admissions) requires:
> - dim-reg-style integration to extract analytic value (a)
> - Brown-Schnetz period theory to extract rational coefficient from c_2 (b)
> Neither is produced by the stated source dependencies. The
> V-L1-Quartic source note supports the same boundary: Casimir values do
> NOT determine channel WEIGHTS.

**Q7.** Does this closure narrow the P-L1-D admission to TWO sub-
admissions instead of three?

> *A.* Yes, in effect. The (c) sub-admission was "per-graph Casimir
> channel projection" which P-L1-D treated as compounding (a)+(b). This
> note shows that the (c.1) assignment/span problem is independent of
> (a)+(b), while (c.2) channel WEIGHT compounds (a)+(b). The sharpened
> admission shape is therefore: { (a), (b), (c.2)=Per(Γ)/|Aut(Γ)| },
> where (c.2) is effectively a wrapper around (a)+(b), so the remaining
> independent period-weight frontiers are scheme conversion (a) and
> rational-coefficient extraction (b).

This is the substantive sharpening claim of this closure: the 3
independent frontiers named by P-L1-D are sharpened after (c) is split
into algebraic assignment/span (c.1) and analytic weight (c.2, equals
(a)+(b)) pieces.
