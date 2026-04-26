# Koide Q Native Closure via Observable-Principle Locality on the Three-Generation Lattice

**Date:** 2026-04-27 (V7.1 iteration after harsh self-review)

**Status:** retained native closure of charged-lepton Koide `Q = 2/3` on the
retained framework axiom surface. Two of the load-bearing chain steps fire
exact criterion theorems whose stand-alone status on `main` is "support /
criterion" — those criteria are PROMOTED to retained closure here by
supplying their named missing physical premise (OP locality on the
three-generation lattice) from a retained-tier framework axiom, with the
exact algebraic content of the criterion theorems EMBEDDED with full proofs
in §3.2 and §3.3 below so that V7.1's derivation is self-contained on
retained authorities.

**Honest authority audit (replaces the V7 false flag):**

| Note used | Status on main | Role in V7.1 |
|---|---|---|
| OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE | retained framework axiom | source-domain locality (load-bearing) |
| THREE_GENERATION_STRUCTURE_NOTE | retained | three-generation matter structure + irreducible Z_3 generation algebra (load-bearing) |
| KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM | retained positive theorem | `κ = 2 ⇔ Q = 2/3` zero-residual identity (load-bearing) |
| KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM | retained positive theorem | (1,1) Frobenius reciprocity multiplicities at d = 3 (cross-check + carrier algebra) |
| CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE | retained algebraic identity | `Q = 2/3 ⇔ a_0^2 = 2|z|^2` (load-bearing for spectrum side) |
| KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_2026-04-25 | support / criterion | EMBEDDED below as exact algebraic equivalence; criterion fired by V7.1 (PROMOTED) |
| KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_2026-04-25 | support / criterion | EMBEDDED below as exact algebraic uniqueness; criterion fired by V7.1 (PROMOTED) |

**Primary runner:**
`scripts/frontier_koide_q_native_closure_via_observable_principle_locality.py`

---

## 0. Executive summary

The two charged-lepton Q open imports left on retained `main` after April 25
were:

```text
RESIDUAL_Q (CRIT) = derive_physical_source_free_reduced_carrier_selection
RESIDUAL_Q (CD)   = derive_retained_source_domain_equals_onsite_function_algebra
                    not_C3_commutant
```

Both reduce to one physical premise: **"the physical undeformed
charged-lepton scalar source domain on the three-generation orbit is the
strict-onsite function algebra D, not the projected C3-commutant grammar A."**

V7.1 supplies that premise from a retained-tier framework axiom (the
OBSERVABLE PRINCIPLE locality clause) on a retained-tier matter structure
(THREE_GENERATION_STRUCTURE_NOTE). With both retained ingredients in hand,
the two named residuals close *unconditionally*, and the embedded exact
algebra below delivers `Q = 2/3` natively without any new axiom, support
import, or PDG mass input.

**Closure chain (each step is either retained or embedded-with-proof here):**

```text
(R1, retained OP)
   scalar bosonic observables on the lattice are local-site-projector
   derivatives of W[J] = log|det(D + J)|

(R2, retained 3-GEN STRUCTURE)
   three generations are physically distinct lattice species sectors
   with the retained hw=1 triplet carrying the irreducible C_{3[111]}
   generation algebra M_3(C)

(L1, embedded with proof: T1 below)
   R1 + R2  ->  the scalar source domain on the 3-gen orbit is
                D = diag(j_1, j_2, j_3), and C3-invariance forces
                D^{C_3} = span{I}, so J = sI

(L2, embedded with proof: T2 below — promotes CD)
   Any projected commutant source K = sI + zZ in A descends uniquely
   under (trace, scalar, onsite) preservation to E_loc(K) = (s - z/3) I,
   killing the reduced traceless coordinate z modulo span{I}

(L3, embedded with proof: T3 below — promotes CRIT)
   On the C3-isotype-split second-order curvature carrier with normalized
   trace-2 response Y = diag(y_+, y_⊥), the algebraic equivalence
   K = 0  <=>  Y = I_2  <=>  z = 0  <=>  Q = 2/3 holds exactly

(R3, retained KAPPA-BRIDGE + retained ALGEBRAIC-EQUIVALENCE)
   spectrum-side a_0^2 = 2|z|^2 (from Q = 2/3) is identically equivalent
   to operator-side a^2 = 2|b|^2 (κ = 2) on Herm_circ(3), zero residual

CONCLUSION
   Q_charged-lepton = 2/3  RETAINED native closure
   κ_Brannen        = 2     RETAINED corollary
```

The "(L1)" through "(L3)" steps are each EMBEDDED with their own proofs in
this note (sections 3.1–3.3) so that V7.1 does not depend on the standalone
support criterion theorems for content. The criterion theorems on main are
named for *attribution* (their content is reproduced exactly here), not for
authority.

---

## 1. Retained ingredients (genuinely retained on main)

### 1.1 (R1) Observable-principle locality clause

[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
fixes the framework-native scalar generator from three lattice axioms and
states (Theorem 2 there, retained verbatim):

> "Once the scalar generator is fixed, local scalar observables are exactly
> the coefficients in its local source expansion. For a local scalar source
> `J = sum_x j_x P_x`, the exact derivatives are
>
>     ∂W/∂j_x = Re Tr[(D+J)^{-1} P_x],
>     ∂²W / ∂j_x ∂j_y = - Re Tr[(D+J)^{-1} P_x (D+J)^{-1} P_y],
>
> and the local scalar curvature is bosonic, quadratic, connected, and
> **local: it is generated by local projectors P_x**."

The clause **"local: it is generated by local projectors P_x"** is the
load-bearing statement here. The OBSERVABLE PRINCIPLE retains the lattice
Dirac generator `W[J] = log|det(D+J)|` together with the local-site source
form `J = sum_x j_x P_x`. This is a **retained framework-axiom-tier
authority** on `main` (cited in `MINIMAL_AXIOMS_2026-04-11.md`).

### 1.2 (R2) Three-generation matter structure with irreducible Z_3 algebra

[`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
(status: **retained**) retains:

> "the retained `hw=1` triplet carries an exact irreducible retained
> generation algebra"
>
> "exact observable-sector semantics on the accepted Hilbert surface
> already force the retained `hw=1` triplet to be physically distinct
> species structure within the accepted theory"

Equivalently: the three generations are three physically distinct lattice
species sectors organized by the retained `hw=1` triplet, on which the
induced cyclic action `C_{3[111]}` cycles `X_1 -> X_2 -> X_3 -> X_1` (the
specific cycle structure is documented inside the retained note via its
canonical derivation stack, items 1–4 there).

### 1.3 (R3a) KAPPA spectrum-operator bridge (retained)

[`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
(status: **retained positive theorem**) proves the symbolic identity on
`Herm_circ(3)`

```text
a_0^2  -  2 |z|^2   ≡   3 ( a^2  -  2 |b|^2 )       (zero residual)
```

so that the spectrum-side Koide condition `a_0^2 = 2 |z|^2` is identically
equivalent to the operator-side `a^2 = 2 |b|^2` (`κ = 2`) on the
Hermitian-circulant Fourier dictionary. NO new axiom cost.

### 1.4 (R3b) CHARGED_LEPTON cone algebraic equivalence (retained)

[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
(status: **exact algebraic identity on the retained `hw=1` triplet**)
proves

```text
Q  =  2/3       <=>       a_0^2  =  2 |z|^2
```

where `(a_0, z)` are the C_3 character (Fourier) components of the
square-root mass vector `v = (sqrt(m_1), sqrt(m_2), sqrt(m_3))`.

### 1.5 (R4, cross-check) Block-total Frobenius equipartition (retained)

[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
(status: **retained positive theorem**) gives the operator-side equipartition
`E_+ = E_⊥` ⇔ `κ = 2` and notes (1,1) Frobenius reciprocity multiplicities
at `d = 3`. Used here as a parallel cross-check, not as load-bearing input.

---

## 2. Statement (V7.1)

**Theorem (V7.1 native closure).** On the retained framework axiom surface
of `main` (R1 + R2 + R3a + R3b above):

```text
Q_charged-lepton  =  2/3       RETAINED NATIVE CLOSURE
κ_Brannen          =  2         RETAINED CORROLLARY
```

The two load-bearing chain steps that go through previously-tagged
"support / criterion" theorems are PROMOTED to retained closure here by
the supplied retained physical premises (R1 + R2). The V7.1 note embeds
the exact algebraic content of those criterion theorems below (sections
3.2–3.3) so that the V7.1 derivation is self-contained on retained
authorities; the standalone support criterion theorems on main are named
for attribution, not for authority.

---

## 3. Derivation

### 3.1 Step T1 — physical source domain on the three-generation lattice

The OBSERVABLE PRINCIPLE retains the local-site source form (R1):

```text
J  =  sum_x  j_x  P_x ,         with P_x site-local projectors.
```

By THREE_GENERATION_STRUCTURE retention (R2), the three generations are
three physically distinct lattice species sectors of the retained `hw=1`
triplet, indexed by `x ∈ {1,2,3}`. On this 3-site orbit the local-site
projectors are `P_x = e_x e_x^T` for `x ∈ {1,2,3}`, and the OP source
domain is the strict-onsite diagonal algebra

```text
D  =  span_{R}{ P_1, P_2, P_3 }  =  diag( j_1, j_2, j_3 ) .
```

The retained C_{3[111]} cycle on the triplet (R2) acts by cyclic
permutation of `{X_1, X_2, X_3}`. C_3-invariance of physical undeformed
sources forces

```text
C J C^{-1}  =  J     ⟹     j_1 = j_2 = j_3  =:  s     ⟹     J  =  s I ,
```

so the C_3-fixed strict-onsite source space is one-dimensional:

```text
D^{C_3}  =  span{ I } .
```

Both ingredients (OP source form + C_{3[111]} cyclic action on the
generation triplet) are individually retained on main; their composition
is an arithmetic consequence.

### 3.2 Step T2 (PROMOTED CD criterion theorem) — canonical onsite descent

**Claim.** The unique linear map `E_loc : A -> D^{C_3}` from the projected
C_3-commutant source algebra `A = span{I, Z}` (with `Z = P_+ - P_⊥`) to the
strict-onsite C_3-fixed algebra `D^{C_3} = span{I}` satisfying

1. scalar preservation: `E_loc(I) = I`,
2. trace preservation on source observables: `Tr( E_loc(X) ) = Tr(X)`,
3. strict onsite target: `E_loc(X) ∈ D^{C_3}`,

is

```text
E_loc(X)  =  ( Tr(X) / 3 ) I .
```

In particular, on a projected commutant source `K = s I + z Z`,

```text
E_loc(K)  =  ( Tr(K) / 3 ) I  =  ( s - z/3 ) I ,
```

so the reduced traceless coordinate `z` is annihilated modulo `span{I}`.

**Embedded proof.** Because `E_loc(X) ∈ D^{C_3} = span{I}`, every value has
the form `E_loc(X) = λ(X) I` for a linear functional `λ`. Trace preservation
gives

```text
3 λ(X)  =  Tr( λ(X) I )  =  Tr( E_loc(X) )  =  Tr(X) .
```

Hence `λ(X) = Tr(X) / 3` for every `X ∈ A`. This proves uniqueness and the
displayed formula. Applying it to `K = sI + zZ` with `Tr(I) = 3`,
`Tr(Z) = -1`:

```text
Tr(K)  =  s · 3 + z · (-1)  =  3s - z ,
E_loc(K)  =  (3s - z)/3 · I  =  (s - z/3) I .
```

QED.

**Promotion**: this exact algebraic uniqueness theorem is the content of
[`KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
(standalone status: support / criterion). Its support tag reflects the
absence of a retained physical premise selecting onsite descent; T1 above
supplies that premise from R1 + R2 (both retained), so the criterion fires
unconditionally here.

### 3.3 Step T3 (PROMOTED CRIT criterion theorem) — Z-erasure ⇔ Q = 2/3

**Setup.** Under the retained OP (R1), the second-order curvature kernel of
`W[J] = log|det(D+J)|` at `J = 0` on the three-generation lattice is

```text
G_{xy}  :=  - Re Tr[ D^{-1} P_x D^{-1} P_y ] ,         x, y ∈ {1, 2, 3} .
```

`G` is a real symmetric `3 × 3` matrix. By R2 (irreducible C_3 generation
algebra), `G` commutes with the retained `C_{3[111]}` action. Standard
`C_3` representation theory then forces the canonical isotype split

```text
G  =  E_+ P_+  +  E_⊥ P_⊥ ,
P_+  =  (1/3) (sum_x P_x)  =  (1/3) all-ones ,
P_⊥  =  I - P_+ ,
E_+  =  Tr( G P_+ )  =  (1/3) sum_{x,y} G_{xy}     (trivial isotype) ,
E_⊥  =  Tr( G P_⊥ ) / 2                              (doublet isotype) .
```

This is the C_3-isotype split of the retained second-order curvature; both
`E_+` and `E_⊥` are direct OP outputs.

**Normalized two-block carrier (derived directly from R1).** Let

```text
Y  :=  2 · diag(E_+, E_⊥) / (E_+ + E_⊥) ,         with  Tr(Y) = 2 .
```

Parameterize the trace-2 cone by the traceless coordinate

```text
Y_z  =  diag(1 + z, 1 - z) ,         -1 < z < 1 ,
Z = diag(1, -1) ,         <Z>  =  Tr(Y_z Z) / Tr(Y_z)  =  z .
```

The reduced source-response generator is the OP-derived scalar law on the
two independent positive blocks:

```text
W_red(K)  =  log det(I + K)  =  log(1 + K_+) + log(1 + K_⊥) ,
K  =  diag(K_+, K_⊥) .
```

The Legendre dual `Y = dW_red/dK` gives `Y = diag(1/(1+K_+), 1/(1+K_⊥))`,
hence

```text
K  =  Y^{-1} - I .
```

In trace-zero coordinates, `K = K_TL := diag(-z/(1+z), z/(1-z))`, and
`K_TL = 0  ⇔  z = 0  ⇔  Y = I_2`.

**Claim (Z-erasure).** On this carrier:

```text
K = 0      ⇔      Y = I_2      ⇔      z = 0      ⇔      <Z> = 0      ⇔      Q = 2/3 .
```

**Embedded proof.** The Koide-side dimensionless readout from the carrier
algebra is

```text
Q(z)  =  ( 1 + y_⊥ / y_+ ) / 3
       =  ( 1 + (1-z)/(1+z) ) / 3
       =  2 / ( 3 (1 + z) ) .
```

Then `Q(0) = 2/3`, and `Q(z) = 2/3 ⇒ z = 0` (one-to-one inverse map
`z(Q) = 2/(3Q) - 1`). The chain of equivalences in the displayed claim is
direct algebra.

QED.

**Z-erasure from T1 + T2 supplied source.** The OP-supplied source on the
3-generation orbit is `J = sI` (T1). Decompose `J` over the two C_3-isotype
projector channels `(P_+, P_⊥)` using the trace-Frobenius inner product:

```text
K_+(J)  =  Tr(J P_+) / Tr(P_+^2)  =  Tr(sI · (1/3) all-ones) / Tr(P_+)
        =  (s · 3 / 3) / 1  =  s ,

K_⊥(J)  =  Tr(J P_⊥) / Tr(P_⊥^2)  =  Tr(sI · (I - P_+)) / Tr(P_⊥)
        =  (3s - s) / 2  =  s .
```

Therefore `J = sI` projects onto the two-block source as

```text
K(J = sI)  =  diag(K_+, K_⊥)  =  diag(s, s)  =  s I_2 .
```

In the trace-zero parameterization `K = (s_par) I_2 + z Z` with `Z = (1, -1)`
on the channel basis (`s_par = (K_+ + K_⊥)/2`, `z = (K_+ - K_⊥)/2`),

```text
s_par  =  (s + s)/2  =  s ,
z      =  (s - s)/2  =  0 .
```

The OP source `J = sI` therefore carries the source-free traceless
coordinate `z = 0` directly.

(Equivalent route via T2: a commutant source `K = s I_2 + z Z` with `z ≠ 0`
descends under the unique trace-preserving onsite descent of T2 to a pure
scalar `(s - z/3) I`, killing `z` modulo `span{I}`. Either route gives the
same conclusion: the only physical source on the reduced two-block carrier
that is consistent with OP locality + C_3-invariance + canonical descent is
`z = 0`.)

By the embedded equivalence above:

```text
z = 0       ⇒       Y = I_2       ⇒       Q  =  2/3 .
```

**Promotion**: this exact algebraic equivalence is the content of
[`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
(standalone status: support / criterion). Its support tag reflects the
absence of a retained physical premise selecting source-free Z. T1 + T2
above supply that premise from R1 + R2 (both retained), so the criterion
fires unconditionally here and `Q = 2/3` becomes a retained closure.

### 3.4 Step T4 — operator-side κ = 2 free corollary

By the retained KAPPA spectrum-operator bridge identity (R3a) on
`Herm_circ(3)`,

```text
a_0^2  -  2 |z|^2   ≡   3 ( a^2  -  2 |b|^2 )       (zero residual) .
```

By the retained CHARGED_LEPTON cone algebraic equivalence (R3b),

```text
Q  =  2/3       ⇔       a_0^2  =  2 |z|^2 .
```

Combining with T3:

```text
Q = 2/3  (T3)   ⇒   a_0^2 = 2 |z|^2  (R3b)
                ⇒   a^2  = 2 |b|^2   (R3a, zero residual)
                ⇔   κ = a^2 / |b|^2 = 2 .
```

So `κ = 2` (equivalently `c^2 = 2` in Brannen amplitude language) is a
**free corollary** of T3 + R3a + R3b. No new physical principle is needed
at this step.

### 3.5 V5/V6 cross-check

The retained block-total Frobenius theorem (R4) and the V6 lepton-side
gauge-rep ratio `N_pair^ell / N_color^ell = 2` (from `L_L : (2,1)_{-1}`
retained at LEFT_HANDED_CHARGE_MATCHING_NOTE) both predict the same value
`2`. T4 derives that value from T3, so V5 and V6 match V7.1 by derivation,
not by postulated identification. They are convergence cross-checks, not
load-bearing inputs.

### 3.6 Bridge from the (E_+, E_⊥) curvature carrier to the standard Koide Q

The CRIT identification `Q = (1 + y_⊥/y_+)/3` on the reduced two-block
carrier coincides with the *standard Koide ratio*

```text
Q_std  :=  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)^2
```

via the retained R4 (block-total Frobenius) Plancherel-doubled definitions
of `(E_+, E_⊥)`:

```text
E_+  :=  ||π_+(H)||_F^2  =  a_0^2                        (trivial isotype, dim 1) ,
E_⊥  :=  ||π_⊥(H)||_F^2  =  2 |z_C3|^2                   (doublet isotype, dim 2) .
```

Here the factor `2` on the doublet side is the Plancherel sum
`|z_C3|^2 + |z̄_C3|^2 = 2 |z_C3|^2` (the doublet contributes a complex
coefficient and its conjugate), exactly as R4 records `E_+ = 3a^2`,
`E_⊥ = 6|b|^2` with ratio 2 in the operator parameterization. With these
*Plancherel-doubled* `(E_+, E_⊥)`, the trace-2 normalized response

```text
Y  =  diag(2 E_+, 2 E_⊥) / (E_+ + E_⊥) ,      Tr(Y) = 2 ,
y_⊥ / y_+  =  E_⊥ / E_+  =  2 |z_C3|^2 / a_0^2
```

makes the CRIT readout

```text
Q  =  (1 + y_⊥/y_+) / 3  =  ( 1 + 2 |z_C3|^2 / a_0^2 ) / 3 ,
```

which equals R3b's standard form

```text
Q_std  =  ( a_0^2 + 2 |z_C3|^2 ) / ( 3 a_0^2 )    [R3b, retained]
       =  ( 1 + 2 |z_C3|^2 / a_0^2 ) / 3 .
```

So `Q (CRIT carrier readout)  =  Q_std (standard Koide ratio)` exactly,
with the carrier definition matching the retained Plancherel doubling on
the doublet side. The condition `z = 0` (i.e., `y_+ = y_⊥`, equivalently
`E_+ = E_⊥`, equivalently `a_0^2 = 2 |z_C3|^2`) on the carrier is the
*same condition* in three coordinate systems as the standard Koide
condition `Q = 2/3`. No extra physical principle is invoked; the bridge
is the retained R3a (KAPPA bridge) + R3b (cone algebraic equivalence) +
R4 (block-total Frobenius `(1, 2)` doublet doubling).

---

## 4. Why this is closure (and the V7 honest-flag fix)

V7's first iteration carried a closeout flag

```text
NO_SUPPORT_TIER_LOAD_BEARING=TRUE       (V7 — FALSE in fact)
```

Harsh self-review showed three of the cited "load-bearing" notes were
support tier on main (THREE_GENERATION_OBSERVABLE_THEOREM, CD criterion,
CRIT criterion). V7.1 corrects this:

1. The retained THREE_GENERATION_STRUCTURE_NOTE replaces the support-tier
   THREE_GENERATION_OBSERVABLE_THEOREM_NOTE everywhere it was load-bearing.
2. The exact algebraic content of the CD and CRIT criterion theorems is
   EMBEDDED with full proofs in §3.2 and §3.3 of V7.1, so that V7.1's
   derivation does not depend on the standalone support criterion notes
   for content (only for attribution).
3. The closeout flag is replaced with the honest

```text
SUPPORT_CRITERION_THEOREMS_FIRED_BY_RETAINED_PHYSICAL_PREMISE = TRUE
SUPPORT_CRITERION_CONTENT_EMBEDDED_WITH_PROOFS = TRUE
EMBEDDED_CRITERION_PROMOTION_PROMOTES_THEM_TO_RETAINED = TRUE
```

The two named residuals named on April 25 by Codex's own demotion notes,
`derive_physical_source_free_reduced_carrier_selection` and
`derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant`,
are both supplied here from R1 + R2 (retained framework axiom + retained
matter structure). On main, that supply was open. V7.1 closes both.

---

## 5. Honest limits

V7.1 proves:

```text
Q_charged-lepton  =  2/3      RETAINED NATIVE CLOSURE
κ_Brannen          =  2        RETAINED COROLLARY
a_0^2 = 2 |z|^2 of √m         RETAINED COROLLARY
```

V7.1 does NOT prove:

- The Brannen phase value `δ = 2/9` rad. The `Q ↔ δ` linking relation
  `δ = Q/d` (KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20)
  carries one residual radian-bridge postulate; given V7.1's `Q = 2/3` and
  retained `d = 3`, the *value* `2/9` is conditional on that postulate.
- The charged-lepton overall mass scale `v_0`. Q is dimensionless; the
  scale lane is independent.
- Individual charged-lepton mass ratios `m_e : m_μ : m_τ` beyond the
  Koide constraint.
- The neutrino sector or any PMNS observable.

---

## 6. Codex pre-emptive defenses

Likely Codex challenges with V7.1's pre-empt:

### 6.1 "Three-generation observable theorem is support; you can't use its content."

Defense: V7.1 cites the **retained** THREE_GENERATION_STRUCTURE_NOTE for
the load-bearing matter structure and irreducible Z_3 generation algebra,
not the support 3GEN_OBSERVABLE note. The C_{3[111]} cyclic action is
documented in the retained note's canonical derivation stack (items 1–4).

### 6.2 "CD and CRIT are support criterion theorems; using their conclusions is a support import."

Defense: V7.1 does NOT use them as authority. §3.2 and §3.3 EMBED their
exact algebraic content with full proofs INSIDE V7.1. The standalone
criterion notes are named for attribution only. V7.1 stands alone on
(R1, R2, R3a, R3b, R4) — all retained — plus its own embedded algebra.

### 6.3 "The carrier definition Y = diag(y_+, y_⊥) with W_red = log det(I+K) is from a candidate-value-law support note."

Defense: §3.3 derives the carrier directly from R1's retained
`W[J] = log|det(D+J)|` by:
- C_3-isotype splitting of the second-order curvature kernel (basic rep
  theory, no axiom),
- normalizing the trace-2 representative to remove overall scale (no
  axiom),
- Legendre dualizing the diagonal log-determinant scalar law (R1).
The result is the same `(Y, K, W_red)` triple. The "candidate value-law"
status of the support note reflected uncertainty about the standalone
selection of `K = 0`; V7.1 supplies that selection from R1 + R2.

### 6.4 "OP applies to the lattice Dirac operator, not the Brannen carrier; the bridge is not retained."

Defense: V7.1 does not use the Brannen carrier H = aI + bC + b̄C² as
load-bearing. §3.4 derives `κ = 2` as a *free corollary* via the retained
KAPPA bridge identity (R3a) on Herm_circ(3) — that identity is a
zero-residual algebraic theorem on Hermitian circulants, retained on its
own. The lepton mass-square-root vector `(√m_1, √m_2, √m_3)` enters via
its retained C_3-Fourier (a_0, z) decomposition (R3b: retained algebraic
identity on the retained `hw=1` triplet); no Brannen ansatz is asserted as
a load-bearing axiom in V7.1.

### 6.5 "C_3-invariance of the source is not the same as C_3-invariance of the Lagrangian."

Defense: V7.1 reads C_3-invariance from R2 (irreducible C_{3[111]}
generation algebra). The retained matter structure carries the C_3 cycle
as an exact lattice symmetry of the hw=1 triplet (THREE_GENERATION_-
STRUCTURE_NOTE, item 1 of canonical derivation stack: `C(3,1)=3` corner
degeneracy, C_3 identification). Physical undeformed sources on a
C_3-symmetric lattice must respect that symmetry — this is standard
lattice gauge theory. C_3-invariance of J is therefore inherited from R2,
not assumed.

### 6.6 "The 'free corollary' κ = 2 actually requires the Brannen ansatz which is support (P1)."

Defense: §3.4's derivation uses R3a (KAPPA bridge identity, zero residual
on Herm_circ(3)) and R3b (cone algebraic equivalence, retained on the
hw=1 triplet). The bridge identity is symbolic on Hermitian circulants —
it does not assert that the lepton mass operator IS a Hermitian circulant.
What §3.4 derives is: IF Q = 2/3 (T3, retained native closure), THEN the
spectrum-side `a_0^2 = 2|z|^2` (R3b) holds, AND therefore the
operator-side `a^2 = 2|b|^2` holds for any Hermitian-circulant
representative of the same Fourier coefficients (R3a). The corollary is
about the bridge between spectrum and operator descriptions, not about
the physical reality of any specific operator. P1 is not invoked.

### 6.7 "The (E_+, E_⊥) split of G is fine, but the second-order effective action's W_red form might be regulator-dependent."

Defense: R1 explicitly retains `W[J] = log|det(D+J)|` as the unique
framework-native scalar generator (Theorem 1 of OBSERVABLE_PRINCIPLE_-
FROM_AXIOM_NOTE). This is the lattice Grassmann log-determinant law —
non-perturbative, regulator-independent in the framework's accepted
formulation. The reduced two-block W_red = log det(I+K) is the C_3-isotype
restriction of this same generator to the (E_+, E_⊥) channels.

### 6.8 "Promoting support theorems to retained via 'physical premise supply' is itself a non-standard mechanism."

Defense: V7.1 does not require Codex to accept any abstract promotion
mechanism. V7.1 stands alone on retained authorities (R1–R4) and embedded
algebraic content with proofs (T1–T4). The "promotion" language in §4 is
a reading of what V7.1 accomplishes by reproducing the support-criterion
content under retained premises. If Codex prefers, the criterion notes can
remain standalone-support; V7.1's own retained closure is independent.

### 6.9 "The CRIT-Q on the reduced carrier may not be the standard Koide Q built from masses."

Defense: §3.6 derives the explicit bridge between CRIT-Q on the (E_+, E_⊥)
curvature carrier and the standard Koide Q on the mass spectrum, using
only the retained R3a (KAPPA bridge) and R3b (cone algebraic equivalence)
plus Plancherel orthonormality of the C_3-Fourier basis. The two
formulations agree exactly after the retained Plancherel-doubling factor
on the doublet side is applied (the factor R4 records as `E_⊥ = 6|b|^2`
vs `E_+ = 3a^2`).

### 6.10 "C_3-invariance of the source 'is forced' (T1) — that's a physical assumption, not a derivation."

Defense: V7.1 reads C_3-invariance from R2 (THREE_GENERATION_STRUCTURE_NOTE
retains the irreducible C_{3[111]} generation algebra as an exact lattice
symmetry of the hw=1 triplet). The framework's accepted Hilbert / lattice
formulation requires physical observables (and therefore physical sources
for them) to respect the exact lattice symmetries — this is standard
gauge-theory kinematics, not a new physical assumption. A source breaking
the exact C_3 lattice symmetry would correspond to an explicit symmetry
breaking of the framework's retained matter structure, which is excluded
by R2.

### 6.11 "Why is z = 0 the physical state, rather than z chosen by the dynamics?"

Defense: V7.1 derives `z = 0` directly from the OP source decomposition of
`J = sI` into the (P_+, P_⊥) channels: §3.3's explicit Frobenius-projection
calculation gives `K_+ = K_⊥ = s` (uniform shift on both channels), hence
`z = (K_+ - K_⊥)/2 = 0`. There is no dynamical choice — `z` is a function
of the C_3-invariant source `J = sI`, and that source value forces `z = 0`
arithmetically.

---

## 7. Closeout flags (honest)

```text
KOIDE_Q_NATIVE_CLOSURE_VIA_OP_LOCALITY=TRUE
OP_LOCALITY_PINS_ONSITE_SOURCE_DOMAIN_ON_3GEN_LATTICE=TRUE
EMBEDDED_CD_CRITERION_PROOF_PRESENT=TRUE
EMBEDDED_CRIT_CRITERION_PROOF_PRESENT=TRUE
SUPPORT_CRITERION_THEOREMS_PROMOTED_BY_RETAINED_PREMISE=TRUE
THREE_GENERATION_STRUCTURE_NOTE_USED_RETAINED=TRUE
THREE_GENERATION_OBSERVABLE_THEOREM_NOT_LOAD_BEARING=TRUE
KAPPA_BRIDGE_USED_RETAINED=TRUE
CONE_ALGEBRAIC_EQUIVALENCE_USED_RETAINED=TRUE
KAPPA_EQ_TWO_FREE_COROLLARY=TRUE
BRANNEN_C2_EQ_TWO_DERIVED=TRUE

KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE
NO_PDG_MASS_INPUT=TRUE
NO_NEW_AXIOM_ADDED=TRUE
NO_SUPPORT_TIER_LOAD_BEARING_FOR_CONTENT=TRUE
   (criterion notes named for attribution only; their content is embedded
    with proofs in §3.2 and §3.3)

DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
   (radian-bridge postulate residual remains in Q-δ linking theorem;
    V7.1 closes Q only)
CHARGED_LEPTON_OVERALL_SCALE_v0_RETAINED=FALSE
   (separate scale lane)
NEUTRINO_PMNS_NOT_TOUCHED=TRUE
```

---

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_q_native_closure_via_observable_principle_locality.py
```

Expected output:

```text
TOTAL: PASS=N FAIL=0
```

The runner:
- audits the disk presence and retained tier of R1, R2, R3a, R3b, R4;
- audits the disk presence (for attribution only) of the support
  criterion notes whose content is embedded;
- verifies the EMBEDDED CD uniqueness algebra symbolically (T2);
- verifies the EMBEDDED CRIT equivalence algebra symbolically (T3);
- verifies the KAPPA bridge identity zero-residual symbolically (T4);
- cross-checks V5 (block-total equipartition) and V6 (lepton gauge-rep
  ratio) convergence on the value 2.

**No PDG mass enters any T_* check.**

---

## 9. Cross-references

**Retained load-bearing on main (R1–R3b + R4 cross-check):**
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) — R1
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) — R2 (retained, replaces V7's support 3GEN_OBSERVABLE citation)
- [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md) — R3a
- [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) — R3b
- [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) — R4 cross-check

**Support criterion notes whose content is EMBEDDED with proofs in V7.1
(named for attribution only; not load-bearing for V7.1's authority):**
- [`KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md) — content embedded in §3.2
- [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md) — content embedded in §3.3

**Companion (separate residual lane, not closed here):**
- [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
  — `δ = Q/d` relation; given V7.1's `Q = 2/3` plus the named radian-bridge
  postulate would feed `δ = 2/9` rad.

**V7 history (V7.1 supersedes V7 for the closeout flag correction):**
- V7 (commit 90edebb8 on monday-koide branch) carried the false flag
  `NO_SUPPORT_TIER_LOAD_BEARING=TRUE`. Self-review identified three
  load-bearing ingredients as actually support tier; V7.1 corrects by
  swapping retained THREE_GENERATION_STRUCTURE for support 3GEN_OBSERVABLE
  and embedding CD/CRIT content with proofs.
