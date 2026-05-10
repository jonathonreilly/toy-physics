# Primitive P-L1-D --- Cl(3)/Z³-Native Period Functor Construction Attempt

**Date:** 2026-05-10
**Claim type:** primitive_construction_attempt (bounded_theorem on closure)
**Sub-gate:** Lane 1 (alpha_s) --- terminal admission on QCD beta_2 / beta_3
scalar channel weights at 3-loop and 4-loop.
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note proposes a construction for review; it
does not claim retention of any new content.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane. No primitive proposed here is admitted into the retained
A1 + A2 + retained-theorem stack on the basis of this note alone.

**Primary runner:** [`scripts/cl3_primitive_p_l1_d_2026_05_10_pPl1_d.py`](../scripts/cl3_primitive_p_l1_d_2026_05_10_pPl1_d.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_l1_d_2026_05_10_pPl1_d.txt`](../logs/runner-cache/cl3_primitive_p_l1_d_2026_05_10_pPl1_d.txt)

**Companion design proposal:**
[`PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md`](PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md)
(PR #1045), which left P_L1-D as an open design problem:

> **P_L1-D (OPEN DESIGN PROBLEM):** A Cl(3)/Z³-native period functor
> `P_Cl(3) : 1PI Graph → Q[ζ_n]` reproducing TVZ/VVL values from the
> lattice substrate alone, without dim-reg or Brown-Schnetz period
> theory. **No such functor is currently known.**

This note attempts that construction explicitly.

## 0. Context --- what is being attempted?

The P-L1 design probe stress-tested three candidate primitives (P_L1-A
Connes-Kreimer Hopf, P_L1-B `⟨P⟩`-scheme bootstrap, P_L1-C combinatorial
sum-rule) and found all NEGATIVE on closure. The remaining hypothetical
P_L1-D was left as the genuine open NEW-MATH question: does a
Cl(3)/Z³-native period functor exist that derives the missing
beta_2/beta_3 channel weights?

This note takes the most natural substrate-native route to constructing
P_Cl(3), composes two sub-functors, runs them explicitly on 1-loop, 2-loop,
and 3-loop primitive QCD graphs, and reports the honest result.

## 1. Construction definitions

### 1.1 P_Cl(3)^HK : 1PI Graph → Q (heat-kernel-scheme period functor)

**Definition.** For a 1PI Feynman graph Γ at loop order n = L(Γ), set

```
P_Cl(3)^HK (Γ) := [s_t^n] ⟨P⟩_HK_SU(3) (s_t)
                = (−1)^(n+1) (4/3)^n / n!
```

where `⟨P⟩_HK_SU(3) (s_t) = 1 − exp(−(4/3) s_t)` is the framework-native
heat-kernel single-plaquette retained by
[`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md).

This is well-defined as a functor (assigns a single rational to every
graph based only on its loop number), substrate-native (only retained
heat-kernel content is used), and computable at every loop order.

The values it produces are:

| n (loop order)         | T(n) = `P_Cl(3)^HK` rational value |
|------------------------|------------------------------------|
| 1                      | `4/3`                              |
| 2                      | `−8/9`                             |
| 3                      | `32/81`                            |
| 4                      | `−32/243`                          |

### 1.2 P_Cl(3)^Schnetz : 1PI Graph → Z[q] (point-counting functor)

**Definition.** For a 1PI Feynman graph Γ with edges E(Γ), vertices
V(Γ), let `Ψ_Γ` denote the first Symanzik (Kirchhoff) polynomial:

```
Ψ_Γ (α) = Σ_{T ∈ Sp.Tr.(Γ)} ∏_{e ∉ T} α_e
```

(sum over spanning trees of Γ, product over edges not in the tree).
Note that Ψ_Γ has integer coefficients, derived purely combinatorially
(spanning-tree enumeration) without any integration.

Set

```
P_Cl(3)^Schnetz (Γ)(q) := #{α ∈ F_q^{|E|} : Ψ_Γ (α) = 0}
```

for q a prime power. This is the affine F_q-point count of the
Kirchhoff hypersurface --- a purely arithmetic invariant. By
**Kontsevich's conjecture** (1997), for many small graphs this is a
polynomial in q; by **Brown-Yeats denominator conjecture** (2011),
the coefficient of q² in `[Γ]_q` (the c_2 invariant) is identically
0 mod q iff the underlying Feynman period of Γ is rational; otherwise
the non-trivial c_2 signature encodes the Galois class of the
transcendentals in the period.

This functor is well-defined, substrate-native (Z-coefficient polynomial
arithmetic + F_p counting; no Brown-Schnetz period oracle imported),
and computable explicitly for small graphs.

## 2. Empirical loop-by-loop test

### 2.1 1-loop bubble (V=2, E=2)

**Kirchhoff polynomial.** `Ψ_bubble = α_0 + α_1` (two spanning trees,
each leaving the OTHER edge as the monomial).

**Point count.** `[bubble]_q = q` for all prime q (linear polynomial
in 2 variables; count = q solutions).

**c_2 invariant.** Polynomial degree in q is 1; c_2 (coefficient of q²)
is 0. ⇒ bubble period is rational. ✓ (true; 1-loop bubble period
is 1 in suitable normalization)

**Beta_0 closure.** Universal: scheme-independent. `P_Cl(3)^HK` value at
1-loop is 4/3; together with retained S1 group-theory (which gives
`(11 N_color − 2 N_quark)/3 = 7` at retained `N_color = 3, N_quark = 6`),
reproduces `β_0 = 7` at any scheme --- but only by universality, not
because the functor genuinely evaluates the bubble period.

### 2.2 2-loop sunset (V=2, E=3)

**Kirchhoff polynomial.** `Ψ_sunset = α_0 α_1 + α_0 α_2 + α_1 α_2`
(three spanning trees; each leaves the other two edges as the monomial).

**Point count.** Directly computed:

| q | `[sunset]_q` |
|---|--------------|
| 2 | 4            |
| 3 | 9            |
| 5 | 25           |
| 7 | 49           |

By Lagrange interpolation through q ∈ {3, 5, 7}, the polynomial form
is `[sunset]_q = q²` (leading coef = 1, b = 0, c = 0). Prediction at
q = 2 is 4, matching measurement. ✓ Polynomial of degree 2 in q.

**c_2 invariant.** Leading coefficient (q²) is 1; c_2 in the
Brown-Yeats sense is mixed-Tate trivial. ⇒ sunset period is rational.
✓ (true)

**Beta_1 closure.** Universal: scheme-independent. `P_Cl(3)^HK` value at
2-loop is −8/9; together with retained group theory (quadratic Casimir
algebra giving `β_1 = (34/3) C_A² − (20/3) C_A T_F n_f − 4 C_F T_F n_f =
26` at SU(3), N_f=6), reproduces `β_1 = 26` --- but again only by
universality.

### 2.3 3-loop K_4 = wheel_3 (V=4, E=6)

**Kirchhoff polynomial.** 16 monomials of degree 3 (Cayley's theorem:
K_n has `n^(n−2)` spanning trees; K_4 has 16).

**Point count.** Directly computed:

| q | `[K_4]_q` |
|---|-----------|
| 2 | 36        |
| 3 | 261       |

The Stembridge / Brown polynomial form for K_4 is documented in
[Schnetz 2011 *QFT over Fq*] as a degree-5 polynomial in q; our q=2,3
data is consistent with the K_4 hypersurface being a polynomial-class
graph (Kontsevich-conjecture-positive class for graphs with ≤12 edges).

**c_2 invariant (signature only).** Floor-residues:

| q | `⌊[K_4]_q / q²⌋ mod q` |
|---|-----------------------|
| 2 | 1                     |
| 3 | 2                     |

These residues encode the c_2 class signature. For K_4 = wheel_3 the
known Feynman period is `6 ζ_3` (Broadhurst-Kreimer 1997 in suitable
normalization). The c_2 invariant correctly distinguishes this as a
non-rational (ζ_3-class) period --- but it does NOT recover the
rational coefficient 6 of ζ_3 from the F_p counts alone. This is
the structural limit.

**Beta_2 closure --- FAILED.** `P_Cl(3)^HK` at 3-loop is `32/81 ≈ 0.395`;
`β_2^MSbar` at N_f = 6 is `−65/2 = −32.5`. Ratio ~ 82×. These do not
agree; the heat-kernel scheme value differs structurally from the
MSbar value by a 3-loop scheme-conversion integral (Alles-Feo-
Panagopoulos 1996, Bode-Panagopoulos 2002) --- which is the
X-L1-MSbar missing primitive, unchanged.

## 3. Sharpened admission shape

The construction attempt SHARPENS the open admission from "no Cl(3)/Z³-
native period functor known" to "three structurally independent missing
sub-functors":

### Missing ingredient (a) --- HK ↔ MSbar scheme conversion at 3-loop

The heat-kernel scheme is framework-native; the MSbar scheme is not.
Converting `β_2^HK = 32/81` to `β_2^MSbar = −65/2` requires the 3-loop
plaquette-coupling matching integral, which is exactly the
X-L1-MSbar missing primitive. Computed in the literature by
**Alles-Feo-Panagopoulos** (Nucl. Phys. B 502, 325, 1997) and by
**Bode-Panagopoulos** (Nucl. Phys. B 625, 198, 2002).

### Missing ingredient (b) --- c_2 → rational-coefficient extraction

The Schnetz F_q functor produces the c_2 invariant, which gives the
Galois class of the period (rational / ζ_3 / ζ_5 / mixed Tate type /
modular form / etc.) by the Brown-Yeats denominator conjecture. It
does NOT produce the rational coefficient. For K_4 the c_2 invariant
tells us "the period is in `Q ⊕ Q · ζ_3`" but doesn't recover the
specific coefficient 6 in `6 ζ_3`. The inverse map class → coefficient
requires **Brown-Schnetz period theory** --- the same primitive
P_L1-C identified as comparable in strength to the original missing
primitive.

### Missing ingredient (c) --- per-graph Casimir channel projection

Casimir-tensor decomposition `T(Γ)` of QCD primitive graphs is
group-theory and IS retained (X-L1-MSbar Section 3 channel skeleton).
But the channel-by-channel rational decomposition of the TOTAL period
into the 6 TVZ monomial weights (`2857/54, −1415/54, −205/18, 79/54,
11/9, 1/2`) requires per-graph period evaluation per channel --- a
combinatorial bookkeeping operation that compounds (a) and (b).

## 4. Composition is rank-deficient

The natural composition

```
P_Cl(3) := P_Cl(3)^HK × P_Cl(3)^Schnetz
```

assigns to each graph at loop n the pair

```
(  T(n)  ,   c_2(Γ)  ).
```

`T(n)` is **one rational per loop order** (not per graph). `c_2(Γ)`
is **one Galois class per graph** (rational / ζ_3 / etc., not a
rational value). To reproduce the **6 distinct MSbar rationals** in
TVZ at 3-loop, the construction would have to span a 6-dimensional
space of rationals, which neither sub-functor + their composition can.

Structurally:

```
       rank(P_Cl(3))                =  2
       rank(MSbar channel space)    =  6
       deficit                      =  4 missing rational coefficients
```

The deficit is exactly what the three missing ingredients (a, b, c)
above would close, jointly, if they could be constructed.

## 5. Honest verdict

| Question | Answer |
|----------|--------|
| Can `P_Cl(3)^HK` be constructed substrate-natively? | YES |
| Can `P_Cl(3)^Schnetz` be constructed substrate-natively? | YES |
| Do these jointly reproduce TVZ MSbar values? | NO |
| Is the L1 channel-weight closure achieved? | NO |
| Has the open admission shape been sharpened? | YES (3 missing pieces) |
| Has X-L1-MSbar bounded admission been lowered? | NO |

**Tier classification:** `bounded_theorem` on closure. Two well-defined
substrate-native sub-functors constructed; their composition does NOT
reproduce TVZ rationals; three independent missing structural
ingredients identified.

This is consistent with and EXTENDS the design proposal in
[`PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md`](PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md)
(PR #1045): the open P_L1-D problem is not solved, but its shape is
now sharpened from "one missing functor" to "three independent missing
sub-functors". The sharpening is the positive result.

## 6. What if A1, A2, A3, A4 from the construction's assumptions were wrong?

### A1: P_L1-D must EXIST mathematically

**What if wrong?** Maybe β-function coefficients in any QFT are
FUNDAMENTALLY tied to dim-reg / Brown-Schnetz periods --- i.e., they
are determined by the ANALYTIC structure of Feynman integrals, not by
any combinatorial encoding. If so, P_L1-D cannot exist purely on
substrate-native primitives.

**This probe's finding.** Consistent with this. `P_Cl(3)^HK` exists
but produces wrong-scheme values; `P_Cl(3)^Schnetz` exists but
produces only class-not-coefficient. Neither route, nor their
composition, recovers the analytic period value. Suggests that the
"analytic" content of the period (the rational coefficient extraction
step in particular) is genuinely not combinatorial.

### A2: Functor must be NATURAL (no arbitrary look-up)

**What if wrong?** Maybe a functor exists but is highly non-natural,
e.g., a 1-parameter family parameterized by a scheme-conversion
constant. This would make P_L1-D a multi-admission construct
rather than a single primitive.

**This probe's finding.** Confirms this: the missing ingredient (a)
HK ↔ MSbar scheme conversion is a non-trivial 3-loop integral
constant; admitting it would make the resulting functor "natural up
to scheme choice" but still depend on an externally-imported constant.

### A3: Cl(3)/Z³ substrate provides enough machinery

**What if wrong?** Maybe the substrate lacks essential structural
content (e.g., a discrete analogue of motivic Galois group action,
or a moduli space of instantons / monopoles).

**This probe's finding.** Confirms this in the specific form: the
substrate has (i) heat-kernel via Casimirs (gives `P_Cl(3)^HK`), and
(ii) finite-field counting on Kirchhoff polynomials (gives
`P_Cl(3)^Schnetz`). It does NOT have a natural rational-coefficient-
extraction primitive composing these, nor a per-graph scheme-conversion
primitive. So the substrate is rich enough for the "class signature"
but not for the "value signature".

### A4: TVZ rationals reflect specific algebraic structure

**What if wrong?** Maybe `65/2`, `ζ_3`, etc. are not accidental ---
they DO reflect specific algebraic structure, but the structure is the
analytic structure of Feynman master integrals, not the combinatorial
structure of graph hypersurfaces.

**This probe's finding.** Confirms: rationals in TVZ come from
combining the master-integral analytic values with the symmetry-factor
combinatorics and Casimir contractions. The combinatorial pieces ARE
retained; the master-integral analytic values ARE the structural gap.

## 7. Conditional admissions inherited

This note inherits the conditional admissions of the existing retained
substrate (identical to PR #1045 P-L1-Channel-Weight design):

- A1 + A2 ([`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)).
- S1 Identification Source Theorem
  ([`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md))
  for `β_0 = (11 N_color − 2 N_quark)/3 = 7`.
- SU(3) quadratic Casimirs `(C_F = 4/3, C_A = 3, T_F = 1/2)`
  ([`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md),
   [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)).
- `⟨P⟩_HK_SU(3)(s_t) = 1 − exp(−(4/3) s_t)` framework-native closed form
  ([`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)).
- X-L1-MSbar bounded admission
  ([`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)).
- P-L1-Channel-Weight design proposal
  ([`PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md`](PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md)).

This note proposes no new retained primitive. The sub-functors
`P_Cl(3)^HK` and `P_Cl(3)^Schnetz` are constructed from already-retained
content (heat-kernel single-plaquette; Kirchhoff polynomial spanning-tree
enumeration; F_p arithmetic). Neither is admitted as a new retained
primitive; both are documented as "constructible but non-load-bearing
for L1 closure" sub-functors.

**Imported authorities (numerical comparators only, NOT load-bearing):**

- TVZ 1980 (Phys. Lett. B 93, 429): MSbar 3-loop six-channel rationals.
- van Ritbergen-Vermaseren-Larin 1997 (Phys. Lett. B 400, 379): MSbar
  4-loop rationals + ζ_3.
- Czakon 2005 (Nucl. Phys. B 710, 485): MSbar 4-loop verification.
- Schnetz 2011 (Electron. J. Combin. 18, P102): QFT over F_q
  point-counting framework.
- Brown-Yeats 2011 (Comm. Math. Phys. 301, 357): denominator conjecture
  for graph periods.
- Brown-Schnetz 2012 (Duke Math. J. 161, 1817): K3 in φ^4 (Kontsevich-
  conjecture counter-examples).
- Bloch-Esnault-Kreimer 2006 (Comm. Math. Phys. 267, 181): graph
  motives.
- Alles-Feo-Panagopoulos 1997 (Nucl. Phys. B 502, 325): lattice 3-loop
  matching coefficients.
- Bode-Panagopoulos 2002 (Nucl. Phys. B 625, 198): 3-loop β-function
  with clover action.
- Broadhurst-Kreimer 1997: K_4 = wheel_3 period = 6 ζ_3.
- Cayley's theorem (n^(n−2) spanning trees of K_n).

## 8. Falsifiable structural claims

1. The 1-loop bubble Kirchhoff polynomial is `α_0 + α_1` with 2 terms
   (Cayley count: 2 spanning trees of K_2 doubled edge).
2. `[bubble]_q = q` for any prime q (count of solutions to linear
   equation in 2 variables over F_q).
3. The 2-loop sunset Kirchhoff polynomial is `α_0 α_1 + α_0 α_2 +
   α_1 α_2` with 3 terms.
4. `[sunset]_q = q²` for prime q (verified explicitly for q ∈ {2,3,5,7}).
5. K_4 has 16 spanning trees (Cayley).
6. K_4 Kirchhoff polynomial has 16 monomials each of degree 3.
7. `[K_4]_2 = 36, [K_4]_3 = 261` (direct enumeration over F_q^6).
8. `P_Cl(3)^HK` at 3-loop = 32/81 ≠ −65/2 = `β_2^MSbar(N_f=6)`.

## 9. Boundaries

This note does NOT claim:

- **A framework-native closed form for β_2 or β_3 in MSbar.**
  X-L1-MSbar bounded admission stands unchanged. `P_Cl(3)` produces a
  ⟨P⟩-scheme-native rational (`32/81` at 3-loop, etc.) which is not
  the MSbar value.
- **The Brown-Yeats denominator conjecture is a theorem.** It is
  treated here as a conjecture (Brown-Yeats 2011 conjecture); the
  construction USES the Kirchhoff polynomial F_p counts as a substrate-
  native primitive, but does NOT rely on the denominator conjecture
  for the negative conclusion.
- **Promotion of any sub-functor (P_Cl(3)^HK, P_Cl(3)^Schnetz, or
  their composition) to retained status.** Each is documented as
  constructible but non-load-bearing for L1 closure.
- **Closure of the L1 strong-coupling chain.** β_2, β_3 continue to
  be imported from QCD literature.
- **Lane 1 alpha_s(M_Z) status change.** Unchanged.

## 10. Status summary

| Sub-functor | Constructed? | Substrate-native? | Closes L1 admission? |
|-------------|--------------|-------------------|----------------------|
| `P_Cl(3)^HK` (heat-kernel scheme) | YES | YES | NO (wrong scheme value) |
| `P_Cl(3)^Schnetz` (F_q point counting) | YES | YES | NO (class only, not coefficient) |
| `P_Cl(3) = HK × Schnetz` | YES | YES | NO (rank-deficient by factor 3) |
| Full P_L1-D recovering TVZ | NO | -- | OPEN (3 missing ingredients) |

| Quantity | Retention status (after this note) | Source |
|----------|------------------------------------|--------|
| `β_0 = 7, β_1 = 26` at N_f=6 | RETAINED (universal) | X-L1-MSbar |
| 9-channel 3-loop Casimir skeleton | RETAINED (group theory) | X-L1-MSbar |
| `⟨P⟩_HK_SU(3) = 1 − exp(−(4/3) s_t)` | RETAINED (closed form) | C_ISO SU(3) NLO |
| Kirchhoff polynomial spanning-tree formula | RETAINED (combinatorial) | this note |
| F_q point-counting of Kirchhoff hypersurfaces | RETAINED (arithmetic) | this note |
| 6-channel 3-loop scalar weights | NOT DERIVABLE | imported TVZ 1980 |
| 14+-channel 4-loop scalar weights | NOT DERIVABLE | imported VVL 1997 |
| HK ↔ MSbar 3-loop scheme conversion | structural primitive (missing) | -- |
| c_2 → rational coefficient extraction | structural primitive (missing) | -- |
| Per-graph Casimir channel projection | structural primitive (missing) | -- |

## 11. Reproduction

```bash
python3 scripts/cl3_primitive_p_l1_d_2026_05_10_pPl1_d.py
```

Expected output:
- Section 1: heat-kernel Taylor coefficients (4/3, −8/9, 32/81, −32/243)
  reproduced; β_0, β_1 universal values cross-checked.
- Section 2: `P_Cl(3)^HK` constructed and tested on 1-loop, 2-loop, 3-loop.
  At 3-loop, value 32/81 documented to differ from MSbar −65/2.
- Section 3: `P_Cl(3)^Schnetz` constructed; Kirchhoff polynomials for
  bubble, sunset, K_4 computed explicitly; F_q point counts at q ∈
  {2, 3, 5, 7} for bubble/sunset, q ∈ {2, 3} for K_4. c_2 invariant
  signature extracted.
- Section 4: composition is rank-deficient (2 vs 6).
- Section 5: 1L, 2L universal pass; 3L explicit failure.
- Section 6: 3 missing structural ingredients sharpened.
- Section 7: hostile-review self-audit.
- Section 8: final summary --- `primitive_construction_attempt`, BOUNDED
  on closure.

## 12. References

- Tarasov O.V., Vladimirov A.A., Zharkov A.Yu. (1980), *The Gell-Mann-Low
  function of QCD in the three-loop approximation*, Phys. Lett. B 93, 429.
  [TVZ; MSbar 3-loop closed form.]
- Larin S.A., Vermaseren J.A.M. (1993), Phys. Lett. B 303, 334.
- van Ritbergen T., Vermaseren J.A.M., Larin S.A. (1997), *The four-loop
  β function in quantum chromodynamics*, Phys. Lett. B 400, 379,
  hep-ph/9701390. [VVL; MSbar 4-loop with ζ_3.]
- Czakon M. (2005), Nucl. Phys. B 710, 485.
- Schnetz O. (2011), *Quantum field theory over F_q*, Electron. J.
  Combin. 18, no. 1, P102.
- Brown F., Yeats K. (2011), *Spanning forest polynomials and the
  transcendental weight of Feynman graphs*, Comm. Math. Phys. 301,
  357.
- Brown F. (2012), *Mixed Tate motives over Z*, Ann. Math. 175, 949.
- Brown F., Schnetz O. (2012), *A K3 in φ⁴*, Duke Math. J. 161, 1817.
- Bloch S., Esnault H., Kreimer D. (2006), *On motives associated to
  graph polynomials*, Comm. Math. Phys. 267, 181.
- Kontsevich M. (1997), informal conjecture on graph hypersurface
  point counts.
- Broadhurst D.J., Kreimer D. (1997), *Association of multiple zeta
  values with positive knots via Feynman diagrams up to 9 loops*,
  Phys. Lett. B 393, 403, hep-th/9609128. [K_4 period = 6 ζ_3.]
- Stembridge J.R. (1998), *Counting points on varieties over finite
  fields related to a conjecture of Kontsevich*, Ann. Combin. 2, 365.
- Alles B., Feo A., Panagopoulos H. (1997), *The three-loop beta
  function in SU(N) lattice gauge theories*, Nucl. Phys. B 502, 325,
  hep-lat/9609025.
- Bode A., Panagopoulos H. (2002), *The three-loop β-function of QCD
  with the clover action*, Nucl. Phys. B 625, 198, hep-lat/0110211.
- Lüscher M., Weisz P. (1995), Phys. Lett. B 349, 165.
- Connes A., Kreimer D. (2000), Comm. Math. Phys. 216, 215,
  hep-th/0003188.
- Panzer E., Schnetz O. (2019), Comm. Math. Phys. 365, 121.
- Cayley A. (1889), *A theorem on trees*, Quart. J. Math. 23, 376.
  [`n^(n−2)` spanning trees of K_n.]

## 13. New-math elements actually constructed

This note is one of the project's relatively rare instances where
substrate-native new-math construction was attempted in full-blast scope.
The new-math elements actually delivered are:

1. **Explicit formulation of `P_Cl(3)^HK`** as a functor on 1PI Feynman
   graphs given by `Γ ↦ T(L(Γ))` where T is the heat-kernel single-
   plaquette Taylor coefficient. This is a one-line definition and is
   provably well-defined. (Modest.)
2. **Explicit formulation of `P_Cl(3)^Schnetz`** as a functor on 1PI
   Feynman graphs given by F_q point-counting of the Kirchhoff
   hypersurface. (More substantial; standard in arithmetic-geometry
   QFT but here re-derived purely from substrate-native combinatorial
   + F_p arithmetic content.)
3. **Sharpened admission decomposition** of the missing P_L1-D into
   THREE independent sub-functors (scheme conversion, coefficient
   extraction, Casimir channel projection). Each of (a), (b), (c)
   could in principle be the subject of its own separate construction
   attempt; this decomposition is the most concrete sharpening of the
   L1 admission produced so far.

What this note did NOT deliver:

- A successful P_L1-D closing the L1 admission. The honest negative
  result.
- A new axiom or new retained primitive. None.
- A claim that any of the three missing ingredients is more or less
  reachable than the others. All three remain structurally open.

This is the campaign-discipline "clean negative result" pattern from
the bridge-gap fragmentation 2026-05-07 lesson: the L1 channel-weight
admission is no longer a single open problem but a clean three-piece
decomposition, each of which can be independently stress-tested in
future campaigns.
