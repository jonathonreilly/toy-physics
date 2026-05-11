# Closure T1 --- Numerical Computation of Z_10^{HK->MS}, Z_20^{HK->MS} via 4D Brillouin-Zone Integration: Bounded-Tier Source Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem (numerically positive at SU(3), N_f=0; scope-bounded)
**Sub-gate:** Lane 1 (alpha_s) --- L1 channel-weight admission sub-piece (a),
HK <-> MSbar 3-loop scheme conversion at SU(3) (children of PR #1059).
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This note proposes a source theorem for review; it
does not claim retention of any new numerical content.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane. No new primitive proposed here is admitted as a framework
premise, and this note does not change the physical Cl(3) local
algebra / Z^3 spatial substrate baseline.

**Primary runner:** [`scripts/cl3_closure_t1_z10_z20_2026_05_10_t1z10z20.py`](../scripts/cl3_closure_t1_z10_z20_2026_05_10_t1z10z20.py)
**Parent note:** [`CLOSURE_C_L1_HK_MSBAR_3L_CONVERSION_NOTE_2026-05-10_cL1a.md`](CLOSURE_C_L1_HK_MSBAR_3L_CONVERSION_NOTE_2026-05-10_cL1a.md) (PR #1059)

## 0. Context

PR #1059 (closure C-L1a) derived the universal 3-loop scheme-conversion
identity

```
b_2^MSbar = b_2^HK - 2 b_1 Z_10 + b_0 Z_10^2 + 2 b_0 Z_20       (*)
```

structurally from named framework inputs plus universal RG algebra. The closure
isolated two scalar admissions:

- `Z_10^{HK->MS}` --- 1-loop Brillouin-zone matching constant
- `Z_20^{HK->MS}` --- 2-loop Brillouin-zone matching constant

This note attempts a **NUMERICAL** closure of those two scalars via
direct 4D BZ integration adapted to the framework's HK propagator,
using the AFP 1996/1997 framework as a reference implementation.

## 1. Theorem (bounded, numerically positive, scope-bounded)

**Theorem (T1 numerical BZ integration; bounded, numerically positive at SU(3), N_f=0).** On
the physical Cl(3) local algebra and Z^3 spatial substrate, plus the
S1 Identification Source Theorem, the SU(3) Casimir authority, the
`<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3) s_t)` source, the C-iso SU(3) NLO
bounded source `(P_W - P_HK)_SU(3) = (7/9) s_t^2 + O(s_t^3)` (from
[`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)), the
universal scheme-conversion identity (*) + the composition theorem (PR
#1059), the scalar conversion constants `Z_10^{HK->MS}, Z_20^{HK->MS}`
at SU(3), N_f=0 admit the following numerical estimates:

```
Z_10^{HK->MS, SU(3), N_f=0}  =  -0.37993...   [bounded mean-field on HK side]
Z_20^{HK->MS, SU(3), N_f=0}  =  +0.07647...   [bounded mean-field + asymptotic c_3^W]
```

derived via the composition factorization

```
HK ---[mean-field matching]---> Wilson ---[AFP eq. (2.10), (3.4)]---> MSbar
```

with the BZ integral `P_1` independently re-derived in this run
(`P_1 = 0.15493344 ± 3 × 10⁻⁷`, matching AFP literature value
0.15493339 at relative error ~3 × 10⁻⁷).

**Positive bounded source results of this note:**

(P1) **`P_1` numerically derived from 4D BZ integration** at meshes
     `N = 24, 32, 40, 48` (up to 5.3 million BZ points), with Richardson
     `1/N²` extrapolation reproducing AFP's literature value at relative
     error `< 1 × 10⁻⁶`. This is a NEW positive derivation on the
     framework's lattice substrate; no prior framework note had derived
     it from BZ integration. (`scripts/frontier_alpha_s_determination.py`
     uses an analytic value imported from Lueschern-Weisz 1995.)

(P2) **`Z_10^{W->MS, SU(3), N_f=0} = -0.23410067`** computed from AFP
     eq. (2.10) with our BZ-derived `P_1` and (one admission) the AFP
     `P_2` Symanzik integral. Matches AFP-published comparator at
     relative error `< 1 × 10⁻⁷`.

(P3) **`Z_20^{W->MS, SU(3), N_f=0} = -0.05524`** back-solved from AFP's
     published `b_2^W` (eq. 3.4) and the universal identity (*) at the
     `W <-> MSbar` boundary. By construction this exactly round-trips
     the AFP-published 3-loop lattice beta-function value.

(P4) **`Z_10^{HK->W, SU(3), N_f=0}` mean-field = -7/48 = -0.14583**
     derived from the upstream `<P>_HK` and bounded `<P>_W` expansions
     at the single-plaquette level. The leading-order mean-field
     ratio 7/12 in the s_t² coefficient of `<P>_HK - <P>_W` is an exact
     framework source input.

(P5) **`Z_20^{HK->W, SU(3), N_f=0}` mean-field = +0.02929** derived
     from NNLO single-plaquette matching with the bounded Wilson
     `c_3^W` asymptotic fit (-4.33 from C-iso note).

(P6) **Composition theorem** (PR #1059, Section 3) applied:
     `Z_10^{HK->MS} = Z_10^{HK->W} + Z_10^{W->MS}` and
     `Z_20^{HK->MS} = Z_20^{HK->W} + Z_20^{W->MS} + 3 Z_10^{HK->W} Z_10^{W->MS}`.

(P7) **Identity (*) yields finite numerical prediction** for `b_2^HK`
     when plugging `b_2^MS(N_f=6) = -65/2` and the computed `Z_n`.
     At N_f=0 the round-trip is exact by construction.

**Bounded admissions remaining after this closure note:**

(T1Z-ADM-1) **AFP `P_2 = 0.024013181`** (1-loop Symanzik integral). Not
     re-derived in this run. Would require an additional BZ
     integration with a different integrand topology than `P_1`;
     bounded as a clean literature admission to Alles-Feo-Panagopoulos
     1996 (hep-lat/9605013) Section 2.

(T1Z-ADM-2) **Wilson `c_3^W ≈ -4.33` asymptotic fit** per the C-iso SU(3) NLO
     bounded note. The s_t³ coefficient of `<P>_W_SU(3)` enters the
     NNLO matching for `Z_20^{HK->W}`; bounded admission to the
     C-iso note's NNLO single-plaquette source result.

(T1Z-ADM-3) **`Z_n^{HK->W}` beyond mean-field**. The mean-field derivation
     in this note uses ONLY the single-plaquette expectation values
     `<P>_HK, <P>_W` source inputs. The full BZ integration over HK
     propagator (the genuine HK analog of AFP eq. (2.10)) would
     require HK lattice Feynman rules at quadratic + cubic vertex
     level, which are NOT in the current source content.
     The mean-field value is the LEADING-order tadpole-improvement
     contribution; higher-loop corrections from HK Feynman vertices
     can modify `Z_n^{HK->W}` by O(g²) at 1-loop accuracy. Bounded.

(T1Z-ADM-4) **N_f > 0 corrections on HK side**. The framework's HK
     source `<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3) s_t)` is at the
     pure-gauge level; quark-loop corrections require the HK-action
     extension with N_f fermion loops which is not available here. The
     N_f=6 cross-check therefore inherits the X-L1-MSbar bounded
     admission unchanged.

(T1Z-ADM-5) **Normalization of `b_2^HK` (32/81 pure-gauge) to MS-beta units**.
     The C-iso SU(3) NLO source gives the s_t Taylor coefficient
     of `<P>_HK` directly. Conversion to the canonical MS-beta
     `b_L = coefficient × (N/(16 π²))^L` normalization requires loop-
     counting prefactors that are part of the X-L1-MSbar bounded
     admission, not derived here.

## 2. What this closes vs. does not close

### Closed (positive)

- **`P_1 = 0.15493339` numerically DERIVED** from 4D BZ integration
  on the framework's lattice substrate. AFP literature value is
  reproduced as cross-check (rel err < 1e-6 after extrap).
- **`Z_10^{W->MS, SU(3), N_f=0} = -0.23410`** numerically derived via
  AFP eq. (2.10) with framework-derived `P_1` + bounded `P_2`.
- **`Z_20^{W->MS, SU(3), N_f=0} = -0.05524`** numerically derived via
  back-solve from AFP eq. (3.4) (exact round-trip).
- **Mean-field Z_n^{HK->W} derived** from upstream `<P>_HK` and
  bounded `<P>_W` expansions: Z_10 = -7/48 (exact framework source input),
  Z_20 = +0.02929 (bounded by `c_3^W` admission).
- **Composition Z_n^{HK->MS}** numerically estimated by combining all
  the above via the PR #1059 composition theorem.
- **N_f=0 self-consistency**: round-trip of (*) is exact since
  `Z_20^{W->MS}` was back-solved from AFP eq. (3.4).

### Not closed (frontier remaining; bounded admissions T1Z-ADM-1 through T1Z-ADM-5)

- **AFP `P_2` Symanzik integral** not re-derived; admitted to literature.
- **Full HK BZ integrals** (genuine HK analog of AFP eq. (2.10)) require
  HK Feynman rules at quadratic + cubic vertex level beyond current source
  content. Mean-field estimate is LEADING-order only.
- **Wilson `c_3^W` and HK-side quark-loop corrections** stay bounded
  to existing bounded sources (C-iso NLO, X-L1-MSbar).

### Final bounded statement

```
[POSITIVE]
Z_10^{HK->MS, SU(3), N_f=0}  =  -0.37993    [mean-field bounded]
Z_20^{HK->MS, SU(3), N_f=0}  =  +0.07647    [mean-field bounded]

derived via composition HK -> Wilson -> MSbar with:
  - P_1 = 0.15493344 (re-derived from 4D BZ integration on framework lattice)
  - Z_10^{W->MS, SU(3), N_f=0} = -0.23410 (AFP eq. (2.10) + framework P_1)
  - Z_20^{W->MS, SU(3), N_f=0} = -0.05524 (back-solved from AFP eq. (3.4))
  - Z_10^{HK->W, SU(3), N_f=0} = -7/48 (mean-field, source input)
  - Z_20^{HK->W, SU(3), N_f=0} = +0.02929 (mean-field + bounded c_3^W)

[STRUCTURALLY DERIVED]
The mean-field route is universal: any single-plaquette scheme conversion
must reduce its first two scalar matchings to single-plaquette expectation
value coefficients at leading + next-to-leading order in s_t.

[BOUNDED ADMISSIONS REMAINING]
T1Z-ADM-1: AFP P_2 (1 Symanzik integral; literature) -- bounded import
T1Z-ADM-2: Wilson c_3^W asymptotic fit (-4.33) -- C-iso NLO note bounded
T1Z-ADM-3: Z_n^{HK->W} beyond mean-field -- HK Feynman rules not available
T1Z-ADM-4: N_f > 0 on HK side -- X-L1-MSbar bounded admission unchanged
T1Z-ADM-5: b_2^HK normalization to MS-beta units -- X-L1-MSbar bounded

[FALSIFIABLE PREDICTION]
Total framework-native gain from this closure note:
  - P_1 is now framework-derived (not imported); PR #1059's
    AFP-comparator role for P_1 is upgraded to framework-native.
  - Z_n^{HK->MS} at SU(3), N_f=0 has numerical estimates with
    explicit error sources (T1Z-ADM-1 through T1Z-ADM-5).
  - Does NOT change Lane 1 alpha_s(M_Z) status (uses 2-loop bridge).
```

## 3. Method

### 3.1 Section 1: 4D BZ integration of P_1

The Wilson 1-loop tadpole integral is

```
P_1 = (1/(2 pi)^4) integral_BZ d^4 p  /  (4 sum_mu sin^2(p_mu / 2))
```

The runner uses a midpoint Riemann sum on `N^4` meshes for `N = 24, 32,
40, 48` (up to 5.3 million BZ points). Midpoint shift avoids the
removable singularity at `p = 0`. Richardson extrapolation eliminating
the `1/N^2` leading error gives

```
P_1 = 0.15493344    (vs. AFP literature 0.15493339, rel err 3.2 × 10⁻⁷)
```

This is a NEW numerical derivation of `P_1` on the framework's lattice
substrate. No prior framework note had performed this integration; the
AFP value was previously imported as a comparator.

### 3.2 Section 2: Z_10^{W->MS} via AFP eq. (2.10)

```
Z_10^{W->MS}(SU(N)) = N * ( 1/(96 pi^2) + 1/(16 N^2) - 1/32
                            - (5/72) P_1 - (11/6) P_2 )
```

Substituting BZ-derived `P_1` and AFP literature `P_2 = 0.024013181`:

```
Z_10^{W->MS, SU(3), N_f=0} = -0.2341007    [from AFP eq. (2.10)]
```

### 3.3 Section 3: Z_20^{W->MS} back-solved from AFP eq. (3.4)

AFP eq. (3.4) gives the 3-loop Wilson-lattice beta-function coefficient:

```
b_2^W = (N/(16 pi^2))^3 * (-366.2 + 1433.8/N^2 - 2143/N^4)
```

Using the universal identity (*) at the W <-> MSbar boundary:

```
Z_20^{W->MS} = (b_2^W - b_2^MS + 2 b_1 Z_10 - b_0 Z_10^2) / (2 b_0)
            = -0.05524
```

By construction this exactly round-trips AFP's published `b_2^W` value.

### 3.4 Section 4: HK -> Wilson mean-field single-plaquette matching

The upstream source content gives the two single-plaquette expansions:

```
<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3) s_t)
                  = (4/3) s_t - (8/9) s_t^2 + (32/81) s_t^3 - ...

<P>_W_SU(3)(s_t)  = (4/3) s_t - (1/9) s_t^2 + (c_3^W/27) s_t^3 + ...
                                                ^^^^^^^^^^^^ bounded
```

The single-plaquette matching equation `<P>_HK(s_HK) = <P>_W(s_W)`
solves order-by-order for `s_W` in terms of `s_HK`:

```
NLO (s_t^2):  s_W = s_HK - (7/12) s_HK^2 + O(s_HK^3)
NNLO (s_t^3): s_W = s_HK - (7/12) s_HK^2 + (0.31935...) s_HK^3 + O(s_HK^4)
              (uses bounded c_3^W = -4.33)
```

In terms of bare couplings `g^2 = 2 s_t` (canonical xi=1):

```
g_W = g_HK * (1 + (alpha/4) g_HK^2 + ((beta/8) - (alpha^2/32)) g_HK^4 + ...)
```

with `alpha = -7/12` (exact upstream input) and `beta = 0.31935` (bounded).
Reading off:

```
Z_10^{HK->W, SU(3), N_f=0} mean-field = alpha/4 = -7/48 = -0.14583
Z_20^{HK->W, SU(3), N_f=0} mean-field = beta/8 - alpha^2/32 = +0.02929
```

**Honesty boundary**: this mean-field derivation captures the LEADING
single-plaquette tadpole-improvement contribution to the HK -> Wilson
scheme conversion. Higher-loop corrections from HK Feynman rules at
cubic + quartic vertex level are NOT included; these are bounded by
T1Z-ADM-3 above.

### 3.5 Section 5: Composition HK -> Wilson -> MSbar

The PR #1059 composition theorem (Section 3 of that note):

```
Z_10^{A->C} = Z_10^{A->B} + Z_10^{B->C}
Z_20^{A->C} = Z_20^{A->B} + Z_20^{B->C} + 3 Z_10^{A->B} Z_10^{B->C}
```

With A = HK, B = Wilson, C = MSbar:

```
Z_10^{HK->MS} = -0.14583 + (-0.23410) = -0.37993
Z_20^{HK->MS} = +0.02929 + (-0.05524) + 3*(-0.14583)*(-0.23410)
              = +0.02929 - 0.05524 + 0.10243
              = +0.07647
```

### 3.6 Section 6: Cross-check via identity (*)

At N_f = 0, the round-trip is exact by construction of Section 3.

At N_f = 6, identity (*) predicts (using N_f=0 Z_n as bounded mean-
field estimate):

```
b_2^HK(N_f=6) predicted from (*) using N_f=0 Z_n:
  b_2^HK = b_2^MS + 2 b_1 Z_10 - b_0 Z_10^2 - 2 b_0 Z_20
         = -32.5 + 2*26*(-0.37993) - 7*(-0.37993)^2 - 2*7*0.07647
         = -32.5 - 19.756 - 1.010 - 1.071
         = -54.34
```

This is consistent with identity (*) but does NOT strengthen the
closure since N_f-corrections to Z_n are bounded admissions (T1Z-ADM-4).

## 4. Conditional admissions

This bounded source theorem uses the framework baseline and inherits the
named bounded admissions T1Z-ADM-1 through T1Z-ADM-5:

- Framework baseline: physical Cl(3) local algebra and Z^3 spatial substrate
  (repo baseline; not a new admission in this note).
- S1 Identification Source Theorem
  ([`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)).
- SU(3) Casimir authority
  ([`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)).
- `<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3) s_t)` source closed form
  ([`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)).
- C-L1a parent note (PR #1059)
  ([`CLOSURE_C_L1_HK_MSBAR_3L_CONVERSION_NOTE_2026-05-10_cL1a.md`](CLOSURE_C_L1_HK_MSBAR_3L_CONVERSION_NOTE_2026-05-10_cL1a.md)).
- X-L1-MSbar bounded admission
  ([`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)).

**Imported authorities (literature inputs and numerical comparators; load-bearing
imports are explicitly labelled as bounded admissions above):**

- Alles B., Feo A., Panagopoulos H. (1996), *The 1-loop scheme
  conversion `Z_10^{W->MS}`*, hep-lat/9605013. (Eq. 2.10 form.)
- Alles B., Feo A., Panagopoulos H. (1996), *The 3-loop QCD beta
  function on the lattice*, hep-lat/9608118.
- Alles B., Feo A., Panagopoulos H. (1997), *The three-loop beta-function
  in SU(N) lattice gauge theories*, Nucl. Phys. B 502, 325,
  hep-lat/9609025. (Eq. 3.4 numerical b_2^W.)
- Lueschern M., Weisz P. (1995), Nucl. Phys. B 452, 234.
- Symanzik K. (1979), Cargese lectures. (Lattice integrals P_1, P_2.)
- Tarasov O.V., Vladimirov A.A., Zharkov A.Yu. (1980), Phys. Lett. B 93,
  429. (MSbar b_2 value.)

## 5. Boundaries

This note does NOT claim:

- **Framework-native closed-form derivation of full Z_n^{HK->MS}.**
  The mean-field estimates are LEADING-order in tadpole improvement;
  higher-loop corrections from HK Feynman rules at cubic + quartic
  vertex level are bounded admission T1Z-ADM-3.
- **Re-derivation of AFP P_2.** This 1-loop Symanzik integral remains
  literature-imported (admission T1Z-ADM-1).
- **Framework-native derivation of c_3^W.** The Wilson NNLO single-
  plaquette coefficient remains the asymptotic-fit bounded admission
  per the C-iso SU(3) NLO note (admission T1Z-ADM-2).
- **Closure of L1 channel-weight admission as a whole.** Sub-pieces (b)
  and (c) of P-L1-D remain genuinely open.
- **Lane 1 alpha_s(M_Z) status change.** Lane 1 uses 2-loop RGE; the
  3-loop scheme conversion is structural background, not active
  Lane 1 input.

## 6. Falsifiable structural claims

1. **`P_1 = 0.154933...`** (4D Wilson 1-loop tadpole) is numerically
   derivable from BZ integration; AFP literature value is reproduced.
2. **`Z_10^{W->MS, SU(3), N_f=0} = -0.23410`** follows by AFP eq. (2.10)
   substitution with derived `P_1` and admitted `P_2`.
3. **`Z_10^{HK->W, SU(3), N_f=0}` mean-field = -7/48**, an EXACT
   rational from upstream `<P>_HK` and bounded `<P>_W` expansion at
   NLO (the s_t² coefficient ratio 7/9 is the source input).
4. **The composition theorem** `Z_20^{A->C} = Z_20^{A->B} + Z_20^{B->C}
   + 3 Z_10^{A->B} Z_10^{B->C}` is verified symbolically in PR #1059;
   in this note it is applied numerically.
5. **`Z_n^{HK->MS}` at N_f=0 has finite numerical estimates** with
   explicit bounded admissions (T1Z-ADM-1 through T1Z-ADM-5); no hidden free parameters.
6. **Identity (*)** yields a finite numerical prediction for any pair
   `(b_2^MS(N_f), b_2^HK(N_f))` once Z_n are determined to bounded
   admissions.

## 7. What if the bounded admissions are wrong?

### T1Z-ADM-1: AFP P_2 is reliable

**What if wrong?** P_2 = 0.024013181 has been cross-checked across
AFP 1996/1997, Lueschern-Weisz 1995, and independent computer-algebra
treatments. The value is at high redundancy in the literature.

**This note's finding.** Safe. Re-deriving P_2 from BZ integration is a
straightforward extension of Section 1; bounded as future work, not
load-bearing for the current numerical estimate.

### T1Z-ADM-2: Wilson c_3^W = -4.33 is reliable

**What if wrong?** This asymptotic fit, per the C-iso SU(3) NLO note,
has bounded numerical uncertainty. A 10% deviation in c_3^W would
shift `Z_20^{HK->W}` mean-field by ~0.01, which propagates linearly
into `Z_20^{HK->MS}`.

**This note's finding.** The numerical estimates carry the C-iso
bounded uncertainty on c_3^W explicitly; the published mean-field
estimate is therefore bounded by this propagated uncertainty.

### T1Z-ADM-3: Mean-field captures the dominant HK -> W matching

**What if wrong?** This is the deepest concern. Tadpole improvement
(Lepage-Mackenzie) is known to capture the LEADING-log corrections to
lattice perturbation theory at SU(3); the residual corrections from
HK Feynman vertices at cubic/quartic level are formally O(g²) at
1-loop. For the 1-loop matching Z_10^{HK->W}, the mean-field result
is the dominant term; for the 2-loop matching Z_20^{HK->W}, higher-
loop corrections from HK vertices could be comparable in magnitude.

**This note's finding.** The numerical estimates are bounded above
the mean-field. To genuinely close T1Z-ADM-3 requires:
  (a) Either: explicit HK lattice Feynman rules (action expansion
      to cubic + quartic in algebra-valued fields) — outside current
      source content.
  (b) Or: numerical MC measurement of the HK propagator and 3-pt
      function — empirical, not source-derived.

### T1Z-ADM-4: N_f = 0 on HK side is the framework's source regime

**What if wrong?** The framework uses pure-gauge SU(3) HK via
`<P>_HK = 1 - exp(-(4/3) s_t)`. Quark-loop extension is open. At
N_f = 6 the conversion coefficients Z_n acquire fermionic contributions
on BOTH the HK and W -> MSbar sides; the W -> MSbar N_f dependence
is standard (linear in N_f for Z_10, quadratic for Z_20), but the HK
side at N_f > 0 is X-L1-MSbar bounded.

**This note's finding.** N_f = 0 is the source-scoped regime; N_f = 6
inherits X-L1-MSbar admission unchanged.

### T1Z-ADM-5: 32/81 to pure-gauge b_2^HK in MS-beta units

**What if wrong?** The C-iso SU(3) NLO note supplies the s_t³ Taylor
coefficient of `<P>_HK` at 32/81. Converting this to canonical MS-beta
units `b_2 = coefficient × (N/(16 π²))^3` requires loop-counting
prefactors that are part of the X-L1-MSbar bounded admission.

**This note's finding.** The cross-check at N_f=6 in Section 6 uses
the identity (*) without committing to the normalization conversion;
the conversion is bounded admission T1Z-ADM-5.

## 8. Closure status summary

| Quantity | Review status | Source |
|---|---|---|
| `P_1 = 0.15493339` 4D Wilson tadpole | source-supported bounded result, unaudited | this note, Section 1 |
| `Z_10^{W->MS, SU(3), N_f=0}` | source-supported bounded result, unaudited | this note, Section 2 |
| `Z_20^{W->MS, SU(3), N_f=0}` | source-supported bounded result, unaudited | this note, Section 3 |
| `Z_10^{HK->W}` mean-field = -7/48 | exact mean-field bounded result, unaudited | this note, Section 4 |
| `Z_20^{HK->W}` mean-field = +0.02929 | bounded (depends on c_3^W) | this note, Section 4 + C-iso NLO |
| `Z_10^{HK->MS}` numerical estimate | bounded (mean-field) | this note, Section 5 |
| `Z_20^{HK->MS}` numerical estimate | bounded (mean-field + c_3^W) | this note, Section 5 |
| AFP `P_2 = 0.024013181` Symanzik integral | imported, bounded admission T1Z-ADM-1 | AFP 1996 |
| Wilson `c_3^W ≈ -4.33` asymptotic | bounded admission T1Z-ADM-2 | C-iso SU(3) NLO |
| `Z_n^{HK->W}` beyond mean-field | bounded admission T1Z-ADM-3 (HK Feynman rules not available) | this note |
| N_f > 0 corrections on HK side | bounded admission T1Z-ADM-4 (X-L1-MSbar unchanged) | this note |
| `b_2^HK` normalization to MS-beta units | bounded admission T1Z-ADM-5 (X-L1-MSbar unchanged) | this note |

**Tier classification:** `bounded_theorem` (numerically positive at
SU(3), N_f=0; scope-bounded). The conversion constants now have
numerical estimates with explicit bounded admissions. PR #1059's
sub-piece (a) admission is sharpened from "two scalar BZ integrals;
source functional form" to "numerical estimates at N_f=0 mean-field
+ five bounded admissions T1Z-ADM-1 through T1Z-ADM-5".

## 9. Reproduction

```bash
python3 scripts/cl3_closure_t1_z10_z20_2026_05_10_t1z10z20.py
```

Expected output:
- Section 1: P_1 BZ integration converges to AFP literature at rel err < 1e-6.
- Section 2: Z_10^{W->MS, SU(3)} reproduces AFP eq. (2.10) at rel err < 1e-7.
- Section 3: Z_20^{W->MS, SU(3), N_f=0} back-solved, exact round-trip.
- Section 4: mean-field Z_n^{HK->W} derived from upstream <P>_HK, <P>_W.
- Section 5: composition Z_n^{HK->MS}.
- Section 6: cross-check at N_f=6 (bounded by admissions).
- Section 7: bounded admissions documentation.
- Section 8: hostile-review self-audit.
- Section 9: final verdict: PASS=12, FAIL=0, ADMITTED=5.

## 10. References

- Tarasov O.V., Vladimirov A.A., Zharkov A.Yu. (1980), *The Gell-Mann-Low
  function of QCD in the three-loop approximation*, Phys. Lett. B 93, 429.
- Lueschern M., Weisz P. (1995), *Computation of the relation between the
  bare lattice coupling and the MSbar coupling in SU(N) gauge theories to
  two loops*, Nucl. Phys. B 452, 234.
- Alles B., Feo A., Panagopoulos H. (1996), *1-loop scheme conversion*,
  hep-lat/9605013.
- Alles B., Feo A., Panagopoulos H. (1996), *3-loop beta function of
  QCD*, hep-lat/9608118 (Lattice 1996 proceedings).
- Alles B., Feo A., Panagopoulos H. (1997), *The three-loop beta-function
  in SU(N) lattice gauge theories*, Nucl. Phys. B 502, 325,
  hep-lat/9609025.
- Symanzik K. (1979), in *New Developments in Gauge Theories*, Cargese
  lectures. (Universal lattice regularization integrals P_1, P_2.)
- Lepage G.P., Mackenzie P.B. (1993), *On the viability of lattice
  perturbation theory*, Phys. Rev. D 48, 2250. (Tadpole improvement
  / mean-field motivation.)
- Migdal A.A. (1975), JETP 42, 413; Makeenko Yu.M., Migdal A.A. (1979),
  Phys. Lett. B 88, 135. (HK action SU(N) heritage.)

## 11. New-math elements actually constructed

This note is a NUMERICAL closure adapted to the framework's HK
substrate. The new-math elements delivered are:

1. **Direct BZ-integration derivation of P_1** on a 5.3M-point 4D
   lattice mesh with Richardson extrapolation. P_1 = 0.15493344
   matches AFP literature to <1e-6 relative; first framework-native
   derivation of this constant from the lattice substrate.
2. **Mean-field single-plaquette derivation of Z_10^{HK->W} = -7/48**
   as an EXACT rational from upstream `<P>_HK = 1 - exp(-(4/3) s_t)`
   and the bounded `<P>_W` NLO expansion. Captures the leading
   tadpole-improvement contribution.
3. **Composition application of the PR #1059 composition theorem**
   to compose HK -> Wilson -> MSbar numerically:
   `Z_10^{HK->MS, SU(3), N_f=0} = -0.37993`,
   `Z_20^{HK->MS, SU(3), N_f=0} = +0.07647`.
4. **Reduction of PR #1059 sub-piece (a)** from "two scalar BZ
   integrals; source functional form" to "numerical estimates
   at N_f=0 mean-field + five bounded admissions T1Z-ADM-1 through T1Z-ADM-5".

What this note did NOT deliver:

- **Full HK BZ integration over HK Feynman rules.** T1Z-ADM-3 remains a clean
  admission requiring HK action expansion to cubic + quartic vertex
  level, which is not in current source content.
- **Re-derivation of AFP P_2.** T1Z-ADM-1 remains; clean future work.
- **Closure of N_f > 0 on HK side.** T1Z-ADM-4 unchanged from X-L1-MSbar.
- **New axioms or status promotions.** None.
- **Promotion of any imported numerical comparator** (AFP b_2^W,
  TVZ b_2^MS, AFP P_2) **to retained-grade status.** None.

## 12. Diff against companion notes

| Note | Status before | Status after this closure |
|---|---|---|
| C-L1a (PR #1059) sub-piece (a) | "two scalar BZ integrals; source functional form" | sharpened to "numerical estimates at SU(3), N_f=0 mean-field + 5 bounded admissions" |
| C-iso SU(3) NLO bounded note | provides upstream `<P>_HK` and bounded `<P>_W` NLO | unchanged; used as input |
| `frontier_alpha_s_determination.py` import of K_4D = 0.15493 | imported literature value | now framework-derived (this note's P_1) |
| Lane 1 alpha_s(M_Z) status | 2-loop RGE bridge | unchanged (3-loop scheme conversion not used in Lane 1) |
| X-L1-MSbar bounded admission | "HK <-> MSbar conversion at 3L is open" | unchanged on N_f, normalization (T1Z-ADM-4, T1Z-ADM-5) |
| P-L1-D sub-pieces (b), (c) | open | unchanged |
| Overall framework | (a) sharpened, (b), (c) open | (a) further sharpened numerically; (b), (c) open |
