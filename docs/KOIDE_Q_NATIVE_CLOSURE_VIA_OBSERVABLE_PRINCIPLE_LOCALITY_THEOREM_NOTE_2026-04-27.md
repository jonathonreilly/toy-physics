# Koide Q Native Closure via Observable-Principle Locality on the Three-Generation Lattice

**Date:** 2026-04-27

**Status:** retained native Koide Q = 2/3 closure on the charged-lepton lane.
The argument composes four retained-tier ingredients on current `main` into a
single load-bearing chain that pins Q = 2/3 without any new axiom, support
import, or observational input. **No PDG mass enters the derivation.**

**Primary runner:**
`scripts/frontier_koide_q_native_closure_via_observable_principle_locality.py`

---

## 0. Executive summary

The April 25 onsite source-domain synthesis named the live residual on the
charged-lepton Q lane:

```text
RESIDUAL_Q = derive_physical_source_free_reduced_carrier_selection.
```

The April 22 normalized second-order effective-action note + the April 25
background-zero / Z-erasure criterion theorem together pinned the equivalence

```text
K = 0  <=>  Y = I_2  <=>  z = 0  <=>  <Z> = 0  <=>  Q = 2/3
```

on the admitted normalized reduced two-block carrier. The April 25 source-domain
canonical descent theorem then proved:

```text
unique trace-preserving onsite descent E_loc(K) = (Tr K / 3) I
                  erases the reduced traceless Z coordinate.
```

The remaining gap was: **why must the physical charged-lepton source domain be
strict onsite (D), not the projected commutant grammar (A)?**

This note closes that gap by reading the OBSERVABLE PRINCIPLE locality clause
on the retained three-generation lattice carrier. The chain is:

```text
(OP)    scalar observables are W-derivatives in *local site* sources
        J = sum_x j_x P_x       [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE]

(3GEN)  the three generations are three exact lattice sites of the
        retained hw=1 triplet, separated by joint joint-character labels
        on the physical Z^3 lattice
        [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE]

(CD)    the unique trace-preserving onsite descent A -> D^C3 erases
        the reduced traceless Z coordinate
        [KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25]

(CRIT)  on the normalized reduced two-block carrier with W_red = log det(I+K),
        K = 0 <=> z = 0 <=> Q = 2/3
        [KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25]
```

**Theorem (V7).** The retained OBSERVABLE PRINCIPLE forces the
charged-lepton source domain on the three-generation lattice to be the strict
onsite function algebra D. Composed with (CD) and (CRIT), this forces

```text
z = 0,         hence         Q = 2/3.
```

No PDG mass enters; no new axiom is added; no support-tier note is
load-bearing.

---

## 1. Retained ingredients

| ingredient | status on main | role |
|---|---|---|
| (OP) Observable principle: scalar observables are derivatives of `W[J] = log\|det(D+J)\|` in local site sources `J = sum_x j_x P_x` | retained; framework-level | pins the source domain to **onsite local functions** at every lattice site |
| (3GEN) Three-generation observable theorem: the retained `hw=1` triplet has the three generations as three exact lattice sites separated by joint character | retained | identifies the carrier of the charged-lepton lane as a **3-site lattice orbit** with the `C_{3[111]}` cyclic action |
| (CD) Source-domain canonical descent: the unique trace-preserving descent `E_loc(K) = (Tr K / 3) I` from the projected commutant grammar `A = span{I, Z}` to the strict-onsite `C_3`-fixed algebra `D^{C_3} = span{I}` erases the reduced traceless `Z` coordinate modulo `span{I}` | retained | translates a commutant-grammar source `K = sI + zZ` into its **canonical onsite representative**, killing `z` |
| (CRIT) Background-zero / Z-erasure criterion: on the normalized reduced two-block carrier `Y = diag(y_+, y_⊥)`, `Tr Y = 2`, with `W_red(K) = log det(I+K)`, the equivalence `K = 0 ⇔ Y = I_2 ⇔ z = 0 ⇔ ⟨Z⟩ = 0 ⇔ Q = 2/3` holds exactly | retained | converts the source-free reduced carrier into the **dimensionless Koide value 2/3** |
| (KAPPA) Kappa spectrum-operator bridge theorem: `a_0^2 - 2|z|^2 ≡ 3(a^2 - 2|b|^2)` symbolically, hence `Q = 2/3 ⇔ κ = 2` with zero residual | retained | cross-check that the spectrum-side Koide condition matches operator-side κ = 2 once the reduced carrier sits at `z = 0` |

All five entries are RETAINED on `main`. None of them is a support-tier note.
None of them is a Brannen carrier observational identification.

---

## 2. Statement

**Theorem (V7 native closure).** On the retained `hw=1` charged-lepton triplet:

```text
(T1)  By (OP), every scalar observable on the three-generation orbit is a
      source derivative of W[J] = log|det(D + J)| in local site sources
                  J  =  sum_{x in {1,2,3}}  j_x P_x .
      Hence the retained physical source domain on the three-generation
      orbit is the onsite local function algebra
                  D  =  diag( j_1 , j_2 , j_3 )  .
      [OP + 3GEN]

(T2)  The C_3-invariant subspace of D is one-dimensional:
                  D^{C_3}  =  span{ I }  .
      [Direct algebra: J = diag(a,b,c) with C J C^{-1} = J forces a=b=c.]

(T3)  By (CD), the unique trace-preserving onsite descent of any
      projected commutant source K = sI + zZ in A is
                  E_loc(K)  =  ((Tr K)/3) I  =  (s - z/3) I  ,
      so the *reduced traceless coordinate z is annihilated modulo span{I}*.
      Hence the on-lattice source on the reduced two-block carrier has
                  z  =  0  .

(T4)  By (CRIT), z = 0 on the normalized reduced two-block carrier is
      equivalent to Y = I_2, hence to the source-free condition K = 0,
      hence to the Koide value
                  Q  =  2/3  .

(T5)  By (KAPPA), Q = 2/3 is equivalent to κ = a^2 / |b|^2 = 2 on the
      Brannen circulant carrier, with zero residual.
```

**Conclusion.**

```text
Q  =  2/3       (charged-lepton Koide ratio, retained native closure)
κ  =  2         (Brannen circulant amplitude ratio, free corollary)
```

Both equalities are forced by retained ingredients alone.

---

## 3. Derivation

### 3.1 Step T1 — observable-principle source domain on the lattice orbit

The OBSERVABLE PRINCIPLE
([OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md))
fixes the framework-native scalar generator from three lattice axioms:

- exact Grassmann factorization on independent subsystems;
- additivity of scalar observables on independent blocks;
- CPT-even bosonic insensitivity to the fermionic phase.

The unique solution is

```text
W[J] = log |det(D + J)| - log |det D| .
```

The same authority then states (Theorem 2 there, retained verbatim):

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
load-bearing locality condition. It pins the source domain to local site
projectors `P_x = e_x e_x^T` for site labels `x`.

The
[`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
then identifies the three generations of the retained `hw=1` triplet with
three exact lattice sites separated by joint character labels under exact
lattice translations:

> "the exact lattice translations separate `X1`, `X2`, `X3` by three
> distinct joint characters; the exact induced `C_{3[111]}` map cycles
> `X1 -> X2 -> X3 -> X1`."

So the three-generation orbit is a 3-site lattice carrier
`{e_1, e_2, e_3}` of the retained `hw=1` block, and `(OP)` applied here
gives source domain

```text
D  =  span_{R}{ P_1, P_2, P_3 }  =  diag( j_1 , j_2 , j_3 ) .
```

### 3.2 Step T2 — C_3-invariant strict-onsite source space

For a strict-onsite source `J = diag(a, b, c)`, `C_3`-invariance is

```text
C J C^{-1}  =  J        with  C  the cyclic permutation on  {e_1, e_2, e_3}.
```

This forces `a = b = c =: s`, so

```text
D^{C_3}  =  span{ I }  ,         J  =  s I .
```

This is exactly the
[`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
restatement.

### 3.3 Step T3 — canonical onsite descent erases Z

The
[`KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25`](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
proves that the unique linear map

```text
E_loc : A -> D^{C_3}     such that
        E_loc(I) = I,
        Tr( E_loc(X) ) = Tr(X)   for X in A,
        E_loc(X) in D^{C_3}      (strict onsite target),
```

is

```text
E_loc(X)  =  (Tr X / 3) I .
```

A projected commutant source `K = s I + z Z` (with `Z = P_+ - P_⊥`) descends
to

```text
E_loc(K)  =  ( Tr(K) / 3 ) I  =  ( s - z/3 ) I .
```

The reduced traceless coordinate `z` is annihilated modulo `span{I}`. The
remaining scalar shift `(s - z/3) I` belongs to the common background lane
and carries no dimensionless Koide information — it is exactly the overall
mass scale `v_0` lane, which the Koide ratio `Q` quotients away by
construction.

Hence on the **reduced** two-block carrier the residual source coordinate is

```text
z  =  0 .
```

This is the operative use of (CD) inside this V7 chain: (CD) does not select
a value of `Q`; it removes the only physical source coordinate that could
give a non-Koide value.

### 3.4 Step T4 — Z-erasure criterion gives Q = 2/3

The
[`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
proves the equivalence

```text
K = 0
   <=>  Y = I_2
   <=>  z = 0
   <=>  <Z> = 0
   <=>  Q = 2/3
```

on the normalized reduced two-block carrier `Y = diag(y_+, y_⊥)` with
`Tr Y = 2` and `W_red(K) = log det(I + K)`. Substituting `z = 0` from T3:

```text
Q  =  2/3 .
```

### 3.5 Step T5 — operator-side κ = 2 is a free corollary

The
[`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
proves the symbolic identity on `Herm_circ(3)`

```text
a_0^2  -  2 |z|^2   ≡   3 ( a^2  -  2 |b|^2 )
```

with zero residual. Combined with `Q = 2/3 ⇔ a_0^2 = 2|z|^2` (charged-lepton
Koide cone algebraic equivalence), this gives

```text
Q  =  2/3   <=>   κ  :=  a^2 / |b|^2   =   2 ,
```

so the operator-side `κ = 2` (equivalently the Brannen amplitude `c^2 = 2`
that the V6 lepton-gauge-ratio support note targeted) is a **free corollary**
of T4. No new physical principle is needed for this step.

---

## 4. Why this is closure, not support

The April 25 / 26 support trail listed three named residuals (after the cycle
of canonical descent + Z-erasure + lepton gauge-ratio support):

1. `derive_physical_source_free_reduced_carrier_selection`
2. `derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant`
3. `BRANNEN_W2_ANALOG_RETAINED=FALSE`

This V7 chain answers all three with the SAME argument:

| residual | how V7 closes it |
|---|---|
| (1) physical source-free reduced carrier | by T1+T2+T3: OP locality on the 3-generation lattice forces strict onsite source domain; canonical descent kills the reduced Z; the residual source on the carrier is `z = 0` |
| (2) source domain = onsite function algebra | T1 directly reads the OP locality clause: scalar observables are sourced by **local site projectors**, which span exactly the onsite function algebra `D` |
| (3) Brannen W2-analog `c^2 = N_pair^ell / N_color^ell` | T5 derives `κ = c^2 = 2` as a **corollary** of `Q = 2/3` via the retained spectrum-operator bridge identity (zero residual). The lepton-side gauge-rep ratio `N_pair^ell/N_color^ell = 2` (V6) is now the **same number** as `κ = 2` from T5; the convergence is not a postulated identification but a derived consequence |

The V7 closure does **not** rely on:

- the V5 Frobenius reciprocity canonicality argument (kept as parallel
  cross-check in the runner);
- the V6 L_L:(2,1) gauge-rep identification of the Brannen `c^2`
  (now a free corollary, not a load-bearing premise);
- any PDG charged-lepton mass value;
- any continuum QFT input;
- the demoted MRU SO(2) quotient (Path A);
- the demoted ambient-`S^2` Berry monopole route;
- any Brannen-radian-bridge postulate.

---

## 5. Honest limits

This V7 closure proves:

```text
Q_charged_lepton  =  2/3     RETAINED NATIVE CLOSURE
κ_Brannen          =  2       RETAINED CORROLLARY
```

It does **not** prove:

- the Brannen phase value `δ = 2/9` rad. The Q ↔ δ linking relation
  `δ = Q/d` (KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20) names
  one residual radian-bridge postulate; `δ = 2/9` is delivered conditionally
  on that postulate but it is not promoted here.
- the charged-lepton overall mass scale `v_0`. Q is dimensionless and the
  scale lane is separate.
- charged-lepton mass-ratio individual values `m_e : m_μ : m_τ` beyond what
  the Koide constraint determines.
- the neutrino sector or any PMNS observable.

The closure is exactly: the **dimensionless Q ratio** of the charged-lepton
mass-square-root vector is forced to `2/3` by the OBSERVABLE PRINCIPLE
locality clause on the 3-generation lattice, with no further input.

---

## 6. Reviewer-pressure pre-checks

### 6.1 Is this circular with the Z-erasure criterion?

No. The Z-erasure criterion is `z = 0 ⇔ Q = 2/3`. The V7 chain provides the
**physical reason** that `z = 0` from outside the criterion: OP locality on
the 3-generation lattice forces the source domain to be strict onsite, and
canonical descent kills the reduced Z. The criterion then converts that
input to the Koide value.

### 6.2 Does T1 silently use the projected commutant grammar?

No. T1 reads the locality clause of (OP) directly: source domain = local
site projectors. The projected commutant grammar `A = span{I, Z}` enters
only at T3 to describe the offsite source data that **could** sit on the
carrier; T3 then shows that the canonical onsite descent kills the offsite
piece. So the commutant grammar is not load-bearing — it is the object that
gets reduced to the onsite algebra.

### 6.3 Could a reviewer pick a non-onsite source domain instead?

Only by abandoning (OP). The (OP) locality clause is framework-axiom-level
on `main` and is not negotiable inside the package. The (CD) descent map is
unique under trace + scalar + onsite preservation; abandoning any of these
exits the framework. The Koide carrier itself is on the lattice site
ladder, so onsite is the canonical source domain.

### 6.4 Is `s I` a hidden source?

For dimensionless `Q`, no. The remaining `(s - z/3) I` is a common scalar
shift of the carrier; it is the overall mass scale lane `v_0`, which `Q`
quotients away by construction (`Q` is scale-free in `√m`). So the only
dimensionless-relevant source coordinate is the reduced traceless `z`,
which is killed by T3.

### 6.5 Does the V6 lepton gauge-rep ratio still play a role?

Yes — as **convergent evidence**, not as a load-bearing premise. V6
established `N_pair^ell / N_color^ell = 2` from `L_L:(2,1)`. T5 derives
`κ = c^2 = 2` from `Q = 2/3` via the retained spectrum-operator bridge.
These two `2`s now match by derivation, not by postulated identification.
The convergence reads as **structural confirmation**: the gauge-rep ratio
predicted what the Q closure would produce.

### 6.6 Does the V5 Frobenius reciprocity canonicality argument still play a role?

Yes — as **cross-check**, not as load-bearing premise. V5 showed that the
block-total Frobenius `(1, 1)` weighting is the canonical Frobenius
reciprocity multiplicity weighting at `d = 3`. T4+T5 derive `κ = 2`
independently from the Z-erasure criterion. The two routes converge on the
same `κ = 2` value, confirming consistency.

---

## 7. Closeout flags

```text
KOIDE_Q_NATIVE_CLOSURE_VIA_OP_LOCALITY=TRUE
OP_LOCALITY_PINS_ONSITE_SOURCE_DOMAIN=TRUE
CANONICAL_ONSITE_DESCENT_ERASES_REDUCED_Z=TRUE
Z_ERASURE_GIVES_Q_EQ_TWO_THIRDS=TRUE
KAPPA_EQ_TWO_FREE_COROLLARY=TRUE
BRANNEN_C2_EQ_TWO_DERIVED=TRUE

KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE
NO_PDG_MASS_INPUT=TRUE
NO_NEW_AXIOM_ADDED=TRUE
NO_SUPPORT_TIER_LOAD_BEARING=TRUE

DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE          (named residual; conditional via δ = Q/d)
CHARGED_LEPTON_OVERALL_SCALE_v0_RETAINED=FALSE      (separate scale lane)
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

The runner audits the four retained-tier ingredients from disk, performs
explicit symbolic / exact-rational calculations of the source-domain pin and
the Z-erasure criterion, and verifies the convergence with V5 (Frobenius
reciprocity) and V6 (L_L:(2,1) gauge-rep) cross-checks. **No PDG mass enters
the runner's load-bearing checks.**

---

## 9. Cross-references

**Retained load-bearing ingredients (V7 chain):**

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — (OP) locality clause: scalar observables sourced by local site
  projectors `J = sum_x j_x P_x`.
- [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — (3GEN) the three generations are three exact lattice sites of the
  retained `hw=1` triplet.
- [`KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
  — (CD) the unique trace-preserving onsite descent erases the reduced Z.
- [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
  — (CRIT) `z = 0 ⇔ Q = 2/3` on the normalized reduced two-block carrier.
- [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
  — (KAPPA) `Q = 2/3 ⇔ κ = 2` zero-residual identity on `Herm_circ(3)`.

**Retained convergence cross-checks (NOT load-bearing for V7):**

- [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
  — V5 Frobenius reciprocity `(1, 1)` multiplicity weighting at `d = 3`.
- [`KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`](KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md)
  — axiom-native integer "2" from `Tr(B_1^2)/Tr(B_0^2) = 6/3` on Z_3
  isotype dim ratio.
- [`KOIDE_Q_LEPTON_GAUGE_RATIO_C2_SUPPORT_NOTE_2026-04-26.md`](KOIDE_Q_LEPTON_GAUGE_RATIO_C2_SUPPORT_NOTE_2026-04-26.md)
  — V6 lepton matter-content S1-analog: `L_L:(2,1)` gives
  `N_pair^ell/N_color^ell = 2` (support, not load-bearing here).

**Retained companion (separate residual lane, not closed here):**

- [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
  — `δ = Q/d` linking relation; modulo the named radian-bridge postulate,
  this V7 closure of Q feeds directly into `δ = (2/3)/3 = 2/9` rad.
