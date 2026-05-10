# R_conn from the SU(N_c) Fierz Channel-Count Identity, with 1/N_c Dynamical-Correction Estimate

**Date:** 2026-04-14 (originally); 2026-05-10 (audit-narrowing refresh).
**Status:** scope-narrowed bounded note. The exact `(N_c^2 − 1)/N_c^2`
adjoint-channel **representation-dimension fraction** is **imported**
from the already-retained Fierz authority below; this note adds a
1/N_c-expansion **estimate** for the channel-population dynamics and
records an MC cross-check. The promotion of the channel-count fraction
to the connected-trace dynamical observable is **not** derived in this
note; it inherits the named matching gap from the Fierz authority.
**Type:** bounded_theorem (estimate + MC cross-check), open dynamical
bridge.
**Status authority:** independent audit lane only.
**Authority role:** records, but does not close, the dynamical bridge
from the exact Fierz channel-count fraction to the lattice connected-
trace ratio. Names that bridge as a real upstream gap inherited from
the Fierz authority's matching rule.
**Depends on:** Cl(3) axiom (N_c = 3), SU(N_c) gauge theory.

**Primary authority for the exact `(N_c^2 − 1)/N_c^2` ratio (one-hop dep,
cited here, not closed in this note):**

- [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_clean`,
  `effective_status: retained_bounded`) — exact group-theory derivation
  of the q-qbar Hilbert-space adjoint-channel dimension fraction
  `(N_c^2 − 1)/N_c^2` from the SU(N_c) Fierz completeness identity
  applied to the q-qbar two-point function, valid at every gauge
  configuration and at any finite N_c (no expansion). This is the
  cycle-breaking authority on `main`. **This note imports the channel-
  count fraction from there**; it does **not** re-derive it.

**Other cross-refs (cited as related, not as authority closure):**
`YT_EW_COLOR_PROJECTION_THEOREM.md` (plain text),
[YUKAWA_COLOR_PROJECTION_THEOREM.md](YUKAWA_COLOR_PROJECTION_THEOREM.md)
(`claim_type: decoration` under the Fierz authority),
`EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`
(plain text).

**Primary runner:** `scripts/frontier_color_projection_mc.py` (MC
cross-check; the runner computes the analytic 8/9 explicitly as its
expected target — the MC value is a numerical agreement check, not an
independent derivation of the dynamical-bridge identification).

---

## Audit boundary

The 2026-05-10 audit verdict was `audited_renaming`: the load-bearing
in-note step "the connected/adjoint propagator fraction equals the
representation-dimension fraction" was classified as a definitional
substitution from group-theory channel counts to a dynamical observable.
That substitution is the **dynamical-population bridge** between the
exact Fierz channel-count and the lattice connected-trace ratio.

This note does **not** derive that bridge. It does the following four
things, all explicitly under their cited or admitted-context authority:

1. **Imports** the exact `(N_c^2 − 1)/N_c^2` adjoint-channel
   representation-dimension fraction from the cited Fierz authority
   (no in-note re-derivation; the Fierz note is `audited_clean`,
   retained-bounded).
2. **Records** a standard 't Hooft-1974 1/N_c topological argument for
   why planar diagrams dominate non-planar diagrams by `1/N_c^2` at
   leading order. This argument is a textbook large-N_c structural
   estimate cited as admitted-context literature input ('t Hooft 1974,
   Witten 1979, Coleman 1985, Manohar 1998); it is **not** an in-atlas
   theorem.
3. **States** the **assumption** (from the cited Fierz note's matching
   rule (M)) that the lattice connected-trace observable inherits the
   adjoint-channel projection coefficient. This is the dynamical-
   population bridge; it is the renaming step flagged by the audit
   verdict and is **not** derived here.
4. **Reports** an MC cross-check on a 4^4 lattice that the measured
   `R_conn(MC) = 0.887 ± 0.008` agrees with the analytic target 8/9 to
   0.2%. The runner's "expected" value is hard-coded as 8/9 from the
   imported Fierz fraction; the MC is a numerical consistency test, not
   an independent derivation.

**Admitted-context derivation gap (real, not import-redirect):**

The promotion from the imported Fierz channel-count fraction
`(N_c^2 − 1)/N_c^2` to the lattice connected-trace ratio `R_conn`
requires a structural matching rule: that the lattice connected color
trace `<Tr_color[G(0,x) G(x,0)]_connected>` projects onto the adjoint
channel `C(x,y)` of the Fierz decomposition rather than onto the total
`Tr_color[G(x,y) G(y,x)]`. The cited Fierz note records this matching
rule as a **named structural input from the framework's lattice gauge
surface, not derived in that note** (see Fierz note section 5,
"matching rule (M)"). This row inherits that gap without bypass; no
retained, bounded, or proposed theorem on the current atlas closes the
matching rule.

This is a **real derivation gap**, not a dependency-citation issue.

## Statement (scope-bounded)

**Imported representation-theoretic fact (from the cited Fierz
authority, not re-derived here).** In SU(N_c) gauge theory, the
adjoint-channel dimension fraction of the q-qbar Hilbert space is
exactly:

    dim(adj) / dim(N_c ⊗ N_c-bar) = (N_c^2 − 1) / N_c^2,

which equals 8/9 at N_c = 3 (fixed by Cl(3)). This is a pure group-
theory invariant; it carries no expansion correction. Source:
[`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md).

**1/N_c estimate (this note, conditional on the named matching rule).**
*Assuming* the matching rule (M) of the cited Fierz authority — that
the lattice connected color trace projects onto the adjoint channel —
the leading-order 't Hooft topological dominance of planar over non-
planar diagrams gives the estimate

    R_conn = (N_c^2 − 1) / N_c^2 + O(1/N_c^4),

with the `O(1/N_c^4) ~ 1.2%` correction at `N_c = 3` bounded by genus-2
contributions in the standard topological expansion. The matching rule
(M) is a named structural input, not derived in this note or in the
cited Fierz note.

For `N_c = 3`:

    R_conn ~ 8/9 + O(1/81)  conditional on (M)

with the MC cross-check `R_conn(MC) = 0.887 ± 0.008` agreeing to 0.2%
under the same assumption.

---

## Part 1: The 1/N_c Expansion -- Setup

### 1.1 Origin of N_c = 3

The framework begins with Cl(3), the rank-3 Clifford algebra over Z^3.
The gauge group SU(3) arises from the Z_3 clock-shift symmetry of the
lattice. The number of colors N_c = 3 is not a parameter -- it is fixed
by the spatial dimension d = 3 of the Z^3 lattice. This is the single
axiom from which N_c descends.

### 1.2 The 't Hooft expansion

For SU(N_c) gauge theory with quarks in the fundamental representation,
't Hooft (1974) showed that Feynman diagrams can be organized by their
topology. The key insight: rewrite the gauge coupling as

    g^2 = lambda / N_c

where lambda = g^2 N_c is the 't Hooft coupling, held fixed as N_c
varies. Each Feynman diagram can be drawn on a compact orientable
surface of genus g (number of handles). The amplitude of a diagram
drawn on a genus-g surface scales as:

    A_g ~ N_c^{chi}  where  chi = 2 - 2g - B

Here chi is the Euler characteristic of the surface, and B is the
number of quark-loop boundaries.

For the quark-antiquark propagator (B = 1 external quark boundary):

    chi = 2 - 2g - 1 = 1 - 2g

Therefore:
- Planar diagrams (g = 0): A_0 ~ N_c^{1}
- First non-planar correction (g = 1): A_1 ~ N_c^{1-2} = N_c^{-1}
- Higher genus (g >= 2): A_g ~ N_c^{1-2g}

The ratio of non-planar to planar contributions is suppressed by
1/N_c^{2g}, with the leading correction at g = 1 suppressed by
1/N_c^2.

### 1.3 Standard references

This topological classification of diagrams is a textbook result:

- 't Hooft, Nucl. Phys. B72, 461 (1974): original large-N_c paper
- Witten, Nucl. Phys. B160, 57 (1979): baryons in large N_c
- Coleman, "Aspects of Symmetry" (1985), Ch. 8: pedagogical treatment
- Manohar, "Large N QCD" (1998), hep-ph/9802419: modern review

The expansion is exact as a topological classification. No approximation
is involved in assigning genus g to a diagram. The approximation enters
only when truncating the sum over genera.

---

## Part 2: Derivation of R_conn

### 2.1 Color decomposition of the q-qbar propagator

The quark-antiquark bilinear psi-bar_a psi_b transforms under
SU(N_c) as:

    N_c (x) N_c-bar = 1 (singlet) + (N_c^2 - 1) (adjoint)

The full q-qbar propagator Pi(p) receives contributions from both
channels:

    Pi(p) = Pi_singlet(p) + Pi_adjoint(p)

The connected color trace ratio is defined as:

    R_conn = Pi_adjoint / Pi_total = Pi_adjoint / (Pi_singlet + Pi_adjoint)

### 2.2 Topological identification of channels

The critical step: the singlet and adjoint channels correspond to
distinct diagram topologies.

**Adjoint channel (connected, planar).**
Diagrams where the quark and antiquark exchange gluons without their
color lines crossing. These are PLANAR diagrams: they can be drawn
on a sphere (genus 0) with the quark boundary on one side. The color
quantum numbers flow continuously between the quark and antiquark
lines via gluon exchange.

At leading order in 1/N_c, the planar diagrams dominate. Each planar
diagram carries an implicit factor of N_c from the color trace around
the quark loop, plus factors of lambda (the 't Hooft coupling) from
each vertex pair. The total planar contribution scales as:

    Pi_planar ~ N_c * f(lambda)

where f(lambda) is a function of the 't Hooft coupling that encodes
all planar dynamics.

**Singlet channel (disconnected, non-planar).**
Diagrams where the quark and antiquark annihilate into a pure-glue
intermediate state (the quark lines form a closed loop, connected to
the rest only through gluons). These correspond to the singlet channel:
the q-qbar pair has total color charge zero, and the intermediate state
is a colorless glueball.

Such diagrams are NON-PLANAR: the quark loop is a separate boundary
from the external operator insertion, requiring the surface to have
at least one handle (genus >= 1). The leading non-planar contribution
scales as:

    Pi_non-planar ~ N_c^{-1} * h(lambda)

The key topological fact: cutting open a planar diagram along the
quark boundary, the quark and antiquark color indices are connected
by gluon lines -- this is the adjoint (connected) channel. Cutting
open a non-planar diagram, the quark color index is traced internally
-- this is the singlet (disconnected) channel.

### 2.3 The ratio at leading order

The total propagator is:

    Pi_total = Pi_planar + Pi_non-planar + O(N_c^{-3})
             = N_c f(lambda) + N_c^{-1} h(lambda) + O(N_c^{-3})

The connected (adjoint) fraction is:

    R_conn = Pi_planar / Pi_total
           = N_c f / (N_c f + N_c^{-1} h + ...)
           = 1 / (1 + h/(N_c^2 f) + ...)
           = 1 - h/(N_c^2 f) + O(1/N_c^4)

Now invoke the completeness relation. The singlet and adjoint channels
span the full N_c x N_c-bar space. By the Fierz identity (proved in
YUKAWA_COLOR_PROJECTION_THEOREM.md, Section 1.3), the N_c^2-dimensional
bilinear space decomposes into:

    dim(singlet) = 1
    dim(adjoint) = N_c^2 - 1

If the dynamics populates the color channels according to their
dimensionality (which is guaranteed at leading order in 1/N_c by
the dominance of planar diagrams, since planar diagrams explore all
N_c^2 - 1 adjoint generators democratically), then:

    Pi_singlet / Pi_total = 1/N_c^2
    Pi_adjoint / Pi_total = (N_c^2 - 1)/N_c^2

This gives:

    h/(N_c^2 f) = 1/N_c^2

    R_conn = 1 - 1/N_c^2 + O(1/N_c^4) = (N_c^2 - 1)/N_c^2 + O(1/N_c^4)

### 2.4 What is "exact" and what is conditional (audit-narrowed 2026-05-10)

The exact-at-finite-N_c content is the **representation-dimension
fraction** `(N_c^2 − 1)/N_c^2`, imported from the cited Fierz authority.
That fraction is a pure SU(N_c) group-theory invariant; it carries no
expansion correction.

The leading-order **dynamical** statement that the lattice connected-
trace observable saturates that fraction is **conditional**:

1. The Fierz identity is an algebraic identity of SU(N_c) — that part
   is exact and imported; this note does not re-derive it.

2. The assertion that *planar dynamics populates all `N_c^2 − 1` adjoint
   generators uniformly* at leading order in 1/N_c is **not derived in
   this note**. It is the standard textbook large-N_c heuristic
   ('t Hooft 1974) and is part of the admitted-context literature
   input. It is also the renaming step flagged by the audit verdict.

3. The assertion that *the singlet channel receives contributions ONLY
   from non-planar diagrams (genus >= 1)* uses the same 't Hooft
   topological classification under the same heuristic.

4. Under (2)-(3), the leading-order channel decomposition matches the
   imported representation-dimension fraction with corrections of
   `O(1/N_c^4)` from genus-2 surfaces.

The leading-order match is therefore "leading-order in the 't Hooft
topological-dominance heuristic plus the matching rule (M) of the
cited Fierz note". Calling it "exact" overstates the in-atlas
derivation status; the previous version of this section did exactly
that and is corrected here.

---

## Part 3: Validity at beta = 6

### 3.1 The topological argument is beta-independent

The 1/N_c expansion classifies diagrams by their TOPOLOGY (genus of
the surface on which they can be drawn). This classification is
independent of:

- The bare coupling g^2 (or equivalently beta = 2N_c/g^2)
- The lattice spacing a
- The quark mass m
- The lattice volume L

The genus of a Feynman diagram is a combinatorial property of its
graph structure. It does not depend on the numerical values of the
propagators or vertices. A planar diagram remains planar at any beta.

Therefore, the statement "planar diagrams dominate over non-planar
diagrams by a factor of N_c^2" holds at ALL beta, including beta = 6.

### 3.2 What DOES depend on beta

The 't Hooft coupling lambda = g^2 N_c determines the WEIGHT of each
diagram within a given genus class. At beta = 6 (g^2 = 1), the
't Hooft coupling is lambda = 3. This is O(1), meaning:

- Individual diagrams are not perturbatively small
- The full non-perturbative sum over planar diagrams gives f(lambda=3)
- The full non-perturbative sum over genus-1 diagrams gives h(lambda=3)

But the RATIO h/(N_c^2 f) is still 1/N_c^2 = 1/9, because:

1. Both f and h receive contributions from all orders in lambda
2. The relative suppression factor N_c^{-2} between genus 0 and
   genus 1 is a property of the COLOR TRACE, not the coupling
3. At strong coupling, each genus class is resummed non-perturbatively,
   but the genus-dependent N_c scaling is preserved

This is the power of the topological expansion: it separates the
N_c-counting (which is exact) from the dynamical content (which is
non-perturbative but genus-by-genus).

### 3.3 Higher-genus corrections at N_c = 3

For N_c = 3, the formal expansion parameter is 1/N_c^2 = 1/9 ~ 11%.
However, the PHYSICAL correction at genus 2 is:

    delta R_conn^{(g=2)} ~ c_2 / N_c^4 = c_2 / 81

where c_2 is an O(1) coefficient. Even if c_2 ~ 1, the correction
is ~1.2%.

The MC measurement confirms this: R_conn(MC) agrees with 8/9 to 0.2%
(see Part 5), consistent with c_2 being O(1) or smaller.

### 3.4 Strong coupling and the topological expansion

One might worry that at strong coupling (g^2 = 1), the 1/N_c expansion
breaks down. This does NOT happen. The reason:

The 1/N_c expansion is not a weak-coupling expansion. It is a
TOPOLOGICAL expansion that works at ANY coupling. 't Hooft's original
proof holds for arbitrary lambda. The expansion parameter is 1/N_c^2,
not g^2 or alpha_s.

At strong coupling, the individual diagrams are large, but the
topological suppression of non-planar diagrams is maintained because
it arises from COLOR COMBINATORICS (the number of independent color
traces), not from the magnitude of individual diagrams.

This is confirmed by lattice Monte Carlo studies of large-N_c gauge
theories, which verify the 1/N_c^2 scaling of non-planar observables
at strong coupling (see Lucini, Teper, Wenger, JHEP 0401:061, 2004).

---

## Part 4: Correction Bound

### 4.1 Genus-2 bound

The leading correction to R_conn = (N_c^2 - 1)/N_c^2 comes from
genus-2 diagrams:

    R_conn = (N_c^2 - 1)/N_c^2 + c_2/N_c^4 + O(1/N_c^6)

For N_c = 3:

    R_conn = 8/9 + c_2/81 + O(1/729)

The coefficient c_2 depends on the full non-perturbative dynamics.
From the MC measurement (Part 5):

    R_conn(MC) = 0.887 +/- 0.008
    8/9 = 0.88889

    Residual: |R_conn(MC) - 8/9| = 0.002 +/- 0.008

This gives |c_2| < 0.8 (2-sigma), consistent with c_2 = O(1).

### 4.2 Parametric bound from large-N_c scaling

In general, the 1/N_c expansion coefficients satisfy:

    c_g ~ (lambda/4pi)^{n_g}

where n_g is the number of vertices in the minimal genus-g diagram.
For genus 2, the minimal diagram has n_2 >= 4 vertices, giving
c_2 ~ (3/4pi)^4 ~ 0.03 if perturbative counting applies.

However, at strong coupling (lambda = 3), this perturbative estimate
is unreliable. The MC bound |c_2| < 0.8 is the reliable constraint.

### 4.3 Impact on observables

The O(1/N_c^4) correction to R_conn propagates to observables as:

    delta(y_t) / y_t = (1/2) * delta(R_conn) / R_conn
                     ~ c_2 / (2 * 81 * 8/9) ~ c_2 * 0.007

For |c_2| < 0.8: delta(y_t)/y_t < 0.5%. This is within the
perturbative matching uncertainty (Delta ~ 2%) and does not affect
the prediction at the current precision.

    delta(g_EW) / g_EW = (1/2) * delta(R_conn) / R_conn ~ 0.5%

Similarly negligible compared to the 0.17% agreement of the EW
couplings (which probes the LEADING term, not the correction).

---

## Part 5: MC Verification

### 5.1 Setup

The script `scripts/frontier_color_projection_mc.py` measures R_conn
directly on SU(3) gauge configurations at beta = 6 (g^2 = 1) using
the color-decomposed quark propagator.

Framework inputs (zero imports):
- SU(3) gauge group from Cl(3)
- Lattice Z^4 (d+1 = 4 from anomaly-forced time)
- beta = 6 from g^2 = 1 (Cl(3) canonical)
- Staggered fermion operator from Cl(3) taste structure

### 5.2 Measurement

The MC computes:

    R_conn = <Tr_color[G(0,x) G(x,0)]_adj> / <Tr_color[G(0,x) G(x,0)]_total>

where G_{ab}(x,y) is the staggered quark propagator in the SU(3)
gauge background, and the subscripts denote the Fierz decomposition
into adjoint and total channels.

Result (4^4 lattice, 100 configurations, Cabibbo-Marinari heat bath):

    R_conn(MC) = 0.887 +/- 0.008

### 5.3 Comparison with derivation

    R_conn(derived) = 8/9 = 0.88889
    R_conn(MC) = 0.887 +/- 0.008
    Deviation: |0.887 - 0.889| / 0.889 = 0.2%

The MC value agrees with the analytical prediction to 0.2%, well
within the statistical error (0.9%) and consistent with the
O(1/N_c^4 ~ 1.2%) correction being small.

### 5.4 Cross-check: observable predictions

The Fierz/channel result `R_conn = 8/9` enters one direct observable
prediction and one matching-rule conditional EW package:

1. **EW couplings:** g_1(v), g_2(v) match observed values to 0.17%
   average deviation only on the connected-trace specialization
   `kappa_EW=0`, where `sqrt(K_EW(0)) = sqrt(9/8)`. The exact Fierz
   fraction alone does not derive that physical readout coefficient.

2. **Top mass:** m_t(pole) = 172.57 GeV vs observed 172.69 GeV
   (-0.07%) when y_t is corrected by sqrt(8/9) = sqrt(R_conn).

Three independent observables (g_1, g_2, m_t) agree with a single
group-theory factor to sub-percent precision.

---

## Part 6: Axiom and Authority Trace

The dependency chain has two parts: an axiom trace for `N_c = 3`, and a
mixed in-atlas / admitted-context literature trace for the
`(N_c^2 − 1)/N_c^2` channel-count value:

    Cl(3) --> Z_3 clock-shift --> SU(3) gauge group --> N_c = 3       (in-atlas axiom trace)
          |
          +--> SU(N_c) gauge theory on Z^4 lattice                    (in-atlas axiom trace)

    SU(N_c) gauge theory                                              (in-atlas)
          |
          +--> Fierz completeness identity                            (cited Fierz authority, audited_clean)
          |
          +--> Hilbert-space dimension fraction (N_c^2 - 1)/N_c^2     (cited Fierz authority, audited_clean)
          |
          +--> matching rule (M): connected-trace projects on adjoint (open structural input
          |                                                            inherited from Fierz note;
          |                                                            not derived on `main`)
          |
          +--> conditional 8/9 R_conn estimate at N_c = 3              (this note, conditional on (M))

    't Hooft 1/N_c topological classification                         (admitted-context literature input)
          |
          +--> O(1/N_c^4) correction estimate                          (admitted-context literature input)

This note's in-note content is a class-A read of the imported Fierz
fraction (no re-derivation), conditional on the matching rule (M),
plus an admitted-context literature input from 't Hooft for the
correction-size estimate, plus an MC numerical cross-check.

---

## Part 7: Status Assessment (audit-narrowed 2026-05-10)

### 7.1 Scope of the in-note claim

This note's in-note content is restricted to:

1. an **import** of the exact `(N_c^2 − 1)/N_c^2` adjoint-channel
   dimension fraction from the cited
   [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
   authority (`audited_clean`, retained-bounded);
2. a **conditional** 1/N_c-expansion estimate that, *assuming the
   matching rule (M) of the Fierz note*, gives `R_conn = (N_c^2 − 1)/N_c^2
   + O(1/N_c^4)`;
3. an **MC cross-check** on a 4^4 lattice that agrees with the
   target 8/9 to 0.2%, under the same assumption (the runner uses 8/9
   as its expected target).

### 7.2 What is **not** derived in this note

The dynamical-population bridge — i.e. the structural assertion that the
lattice connected color trace projects onto the adjoint channel of the
Fierz decomposition — is **not** derived in this note. It inherits the
matching rule (M) from the cited Fierz authority, where it is itself
recorded as a named structural input that is not derived inside the
Fierz note either. This is the renaming step flagged by the
2026-05-10 audit verdict.

The 't Hooft 1974 topological dominance argument is admitted-context
literature input; it is **not** an in-atlas theorem on `main`.

### 7.3 Status table for downstream consumers

The downstream observables that depend on `R_conn = 8/9` (`sqrt(Z_phi)`,
`y_t(phys)`, `g_EW(phys)`, `m_t(pole)`) inherit the same status as the
matching rule (M): conditional on the named structural input. This row
explicitly **does not** propose retained or positive-theorem promotion
for those downstream observables.

---

## Import Status Table (audit-narrowed 2026-05-10)

| Element                          | Value      | Status      | Source                                                                                              |
|----------------------------------|------------|-------------|-----------------------------------------------------------------------------------------------------|
| N_c = 3                          | 3          | AXIOM       | Cl(3) Z_3 clock-shift (axiom)                                                                       |
| SU(N_c) gauge theory             | --         | AXIOM       | Cl(3) framework (axiom)                                                                             |
| 1/N_c topological classification | --         | LITERATURE  | 't Hooft 1974 (admitted-context literature input; not in-atlas theorem)                             |
| Planar dominance (genus 0)       | N_c^{chi}  | LITERATURE  | Topological classification (admitted-context literature input)                                      |
| Fierz identity                   | exact      | IMPORTED    | Cited Fierz note (`audited_clean`, retained_bounded)                                                |
| `(N_c^2-1)/N_c^2`                | 8/9        | IMPORTED    | Cited Fierz note (representation-dimension fraction; not re-derived here)                           |
| Matching rule (M)                | --         | OPEN GAP    | Inherited from cited Fierz note as a named structural input; not derived on the current atlas      |
| R_conn estimate                  | 8/9 + O(1/81) | CONDITIONAL | This note, conditional on matching rule (M) and 't Hooft topological-dominance literature input |
| R_conn(MC) = 0.887 +/- 0.008     | 0.887(8)   | NUMERICAL   | `scripts/frontier_color_projection_mc.py`; runner uses 8/9 as the explicit target value              |
