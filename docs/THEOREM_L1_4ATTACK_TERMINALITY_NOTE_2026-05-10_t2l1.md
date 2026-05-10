# L1 β_2/β_3 4-Attack Terminality Theorem

**Date:** 2026-05-10
**Claim type:** no_go (bounded structural no-go with named
open-gate residue)
**Scope:** Records a bounded structural no-go for four tested route
families that attempted to close the QCD beta-function scalar channel
weights at 3-loop and 4-loop (`β_2`, `β_3`) from the existing
physical `Cl(3)`/`Z³` framework baseline. The runner separates
positive support content from the unresolved residue and decomposes
that residue into 3 named sub-functor missing ingredients, in line
with the P-L1-D open-gate construction.
**Status authority:** independent audit lane only; effective status
is pipeline-derived. This note is a source-note proposal.
**Source-note proposal disclaimer:** the `claim_type`, scope, named
admissions, and 4-attack terminality classification are
author-proposed. The audit lane has full authority to retag, narrow,
or reject.

**Primary runner:** [`scripts/cl3_theorem_l1_4attack_terminality_2026_05_10_t2l1.py`](../scripts/cl3_theorem_l1_4attack_terminality_2026_05_10_t2l1.py)
**Cached output:** [`logs/runner-cache/cl3_theorem_l1_4attack_terminality_2026_05_10_t2l1.txt`](../logs/runner-cache/cl3_theorem_l1_4attack_terminality_2026_05_10_t2l1.txt)

## Naming convention

In this note:

- **Physical `Cl(3)` local algebra** = the repo baseline local algebra
  used throughout the framework; this note does not introduce or rename
  that baseline.
- **"L1"** = Lane 1 (`alpha_s`); the bridge from the lattice/
  `<P>`-scheme to phenomenological `alpha_s` at standard energy
  scales.
- **"channel weight"** = the scalar coefficient (rational or
  rational + `zeta_k` combination) multiplying a Casimir-tensor
  channel in the beta-function expansion at a given loop order. For
  example, the 3-loop MS-bar beta function has 6 channels with
  scalar weights `2857/54, -1415/54, -205/18, 79/54, 11/9, 1/2`
  (Tarasov-Vladimirov-Zharkov 1980).
- **"period functor"** = an assignment from 1PI Feynman graphs to
  the rationals (or `Q[zeta_n]`) that reproduces the perturbative
  coefficient of a graph's contribution to a coupling-constant
  beta-function in a given renormalization scheme.

## Claim boundary

This note records that four tested route families for constructing
or importing a closed form for `β_2` and/or `β_3` from
`Cl(3)`/`Z³` terminate at named obstacles. It does not prove that all
future framework routes are impossible. It does show that, for the
tested MS-bar dim-reg, quartic-Casimir, resurgence, and topological /
Chern-Simons route families, the scalar channel weights are not
closed by the current inputs and the missing-ingredient decomposition
is sharp and named.

The L1 admission remains. What this note adds is a structural
explanation of WHY four very different attacks all terminate, and a
SHARP sub-functor decomposition (a, b, c) showing what additional
content WOULD close the gate.

## Question

Four tested route families for deriving `β_2` and/or `β_3` on the L1
lane terminated negatively in 2026-05-08 through 2026-05-10:

| Attack | Framework | Source basis used by this note |
|---|---|---|
| 1. MS-bar dim-reg | Tarasov-Vladimirov-Zharkov 3-loop in MS-bar; VVL 1997 4-loop | runner classification and literature comparator |
| 2. Casimir | Quartic Casimir invariants at 4-loop; cubic Casimir at 3-loop | [`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md) |
| 3. Resurgence | Borel-plane / trans-series Stokes structure | runner classification and literature comparator |
| 4. Topological | Chern-Simons on T³ with SU(3); knot polynomials | [`KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md`](KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md) |
| Synthesis | P-L1-D period functor construction attempt | [`PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md`](PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md) |

These four attacks span genuinely orthogonal mathematical content
(scheme-perturbation theory, group-theory invariant theory,
asymptotic-resurgence analysis, topological QFT). Each retains
genuinely new structural content (3-loop / 4-loop Casimir skeletons,
Borel-plane renormalon structure, finite/algebraic CS data). Yet
none closes the rational coefficients of the channel weights.

**Question:** Do these four tested route families close `β_2`, `β_3`
from the existing physical `Cl(3)`/`Z³` baseline, and can their
residual failure be decomposed into a sharp finite list of named
missing sub-functors?

## Answer

**Yes, for the tested surface.** The four route families span the
mathematical surface exercised by this runner for substrate-native
perturbative QCD coupling running:

| Attack | What it produces | What it cannot produce |
|---|---|---|
| MS-bar dim-reg | The full channel skeleton (6 channels at 3-loop, 17+ at 4-loop), scheme dictionary | Scalar weights — they are 3-/4-loop master integrals in dim-reg, FOREIGN to lattice/`<P>`-scheme |
| Casimir | Casimir VALUES (`C_F=4/3, C_A=3, T_F=1/2, d_F·d_F/N_F=5/12`, etc.) | Channel WEIGHTS (rational + `ζ_3` combinations from 4-loop integrals) |
| Resurgence | Borel-plane geometry (`z_*=4π/7`), UV renormalon ladder, asymptotic growth `(β_0/4π)^(n+1)` | Stokes constants `S_IR`, subleading exponent `b`, finite-n corrections at `n=2,3` |
| Topological | CS partition function, Wilson-loop knot polynomials, level shift `k+h^∨` | The specific TVZ/VVL rational + `ζ_3` channel weights (cyclotomic vs rational mismatch) |

Per the P-L1-D open-gate construction, the natural substrate-native
period functor decomposes as `P_Cl(3) = P_Cl(3)^HK × P_Cl(3)^Schnetz`
(heat-kernel × Kirchhoff-point-count). This composition is rank-2,
while the target MS-bar 3-loop channel space is rank-6: there is a
rank deficit of 4 missing rational coefficients. The deficit is
sharp and decomposable into 3 named sub-functor missing
ingredients (a), (b), (c) per P-L1-D §3.

## Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| Cl3Local | Physical `Cl(3)` local algebra | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3Substrate | Physical `Z³` spatial substrate | repo baseline; same source |
| beta_0 | `beta_0 = (11 N_c − 2 N_f) / 3 = 7` at `N_c = 3, N_f = 6` | source dependency; retained universal |
| beta_1 | `beta_1 = (34/3) C_A² − (20/3) C_A T_F N_f − 4 C_F T_F N_f = 26` at SU(3), N_f=6 | source dependency; retained via quadratic Casimirs |
| HK-plaq | `<P>_HK_SU(3)(s_t) = 1 − exp(−(4/3) s_t)` framework-native heat-kernel single-plaquette | source dependency; see [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md) |
| Casimir-values | Quartic Casimir invariants at SU(3): `d_F^abcd d_F^abcd / N_F = 5/12`, `d_F^abcd d_A^abcd / N_F = 5/2`, `d_A^abcd d_A^abcd / N_A = 135/8` | support-only |
| Schnetz-counts | F_q point counts of Kirchhoff polynomials | combinatorial; substrate-native (per P-L1-D) |

### Forbidden imports

- NO PDG values of `alpha_s` at standard energy scales as derivation
  input.
- NO new repo-wide axiom.
- NO new admissions; the L1 admission is unchanged.
- NO promotion of any of the four underlying source notes to a new
  tier.
- NO Brown-Schnetz period evaluation oracle, dim-reg machinery, or
  scheme-conversion integrals as derivation input.

## The structural argument

### Step 1 — Channel-skeleton vs channel-weight distinction

The QCD beta function admits, at each loop order `n`, a
decomposition into a finite linear combination of Casimir-tensor
channels with scalar weights:

```text
beta_2(QCD) = sum_{ch in CH_3} w_3,ch · T_ch                (3-loop)
beta_3(QCD) = sum_{ch in CH_4} w_4,ch · T_ch                (4-loop)
```

where `T_ch` is a Casimir-product channel (e.g., `C_A^3`,
`C_F C_A T_F N_f`, `d_F^abcd d_F^abcd / N_R`, ...) and `w_n,ch` is
its scalar weight (rational at 3-loop, rational + `ζ_3` multiples at
4-loop in MS-bar).

The CHANNEL SKELETON `CH_n` and the values `T_ch(SU(3), N_f=6)` of
the channels at `SU(3)` are pure group theory: they reduce to
combinations of `(C_F, C_A, T_F N_f)` and, at 4-loop, quartic
Casimirs `d_F^abcd, d_A^abcd`. These are all RETAINED or SUPPORTED
from retained content (Casimir values, generator algebra).

The CHANNEL WEIGHTS `w_n,ch` are loop-integral-derived: they are the
rational+irrational combinations that emerge after evaluating the
3-loop or 4-loop master integrals in a specific renormalization
scheme. These are NOT retained from any Cl(3)/Z³ content.

### Step 2 — Attack 1: MS-bar dim-reg

**Framework.** Tarasov-Vladimirov-Zharkov 1980 (3-loop) and van
Ritbergen-Vermaseren-Larin 1997 (4-loop) computed `beta_2, beta_3`
in MS-bar by direct dim-reg evaluation of 3-/4-loop master
integrals. The result is a closed form with explicit rational +
`ζ_3` coefficients.

**Retention boundary.** The channel skeleton (6 channels at 3-loop,
17+ at 4-loop) is framework-retainable from Casimir algebra. The
scalar weights are 3-/4-loop master integrals in dim-reg. Dim-reg is
foreign to a lattice/`<P>`-scheme framework: it relies on analytic
continuation in dimension `d = 4 − 2ε`, which is not native to the
discrete `Z³` substrate. The scheme-conversion integral from the
lattice's `<P>`-scheme to MS-bar is itself a 3-loop computation
(Alles-Feo-Panagopoulos 1996; Bode-Panagopoulos 2002), foreign to
retained content.

**Net.** Attack 1 retains the channel SKELETON; it cannot retain the
channel WEIGHTS. The MS-bar route is structurally a dim-reg native
construction.

### Step 3 — Attack 2: Casimir (quartic + cubic)

**Framework.** At 4-loop, the channel basis extends with quartic
Casimir tensors `d_F^abcd d_F^abcd / N_F = 5/12`,
`d_F^abcd d_A^abcd / N_F = 5/2`, `d_A^abcd d_A^abcd / N_A = 135/8`.
These VALUES are pure group theory, reproducible from explicit
SU(3) generator algebra — and they are reproduced by the V-L1-Quartic
runner from retained content.

**Retention boundary.** The Casimir values are support-only:
reproducible from explicit SU(3) matrix algebra, not retained as
theorem-grade. More critically, the SCALAR COEFFICIENTS multiplying
these channels in `beta_3` (e.g., `c_dFdF · d_F^abcd d_F^abcd / N_F`
where `c_dFdF ~ -64 + 480 ζ_3` in one convention) are 4-loop
ladder/sunrise master integrals in dim-reg, NOT framework-supported.

At 3-loop, the situation is parallel: the 6-channel skeleton uses
cubic products of `(C_F, C_A, T_F N_f)` as VALUES; channel WEIGHTS
remain 3-loop master integrals.

**Net.** Attack 2 retains the Casimir VALUES at all four loops; it
cannot retain the channel WEIGHTS at loop `>= 3`. The conjecture that
"quartic Casimir values bypass the channel-weight obstruction" is
foreclosed: `beta_2` contains NO quartic-Casimir channels at all
(the TVZ closed form is degree 2 in `n_f`, structurally excluding
quartic mixing); `beta_3` does contain them, but their scalar weights
remain loop-integral content.

### Step 4 — Attack 3: Resurgence (trans-series)

**Framework.** Resurgence relates perturbative coefficients
`β_n` to non-perturbative content (instantons, renormalons) via
Stokes phenomena: `β_n ~ (S_IR / 2πi) · (β_0/4π)^(n+1) · Γ(n+1+b)`
where `S_IR` is the IR-renormalon Stokes constant and `b` is the
subleading exponent.

**Retention boundary.** The Borel-plane geometry is retainable from
retained `β_0 = 7`: the IR renormalon at `z_* = 4π/β_0 = 4π/7`, the
UV renormalon ladder at `z = −4π/(β_0 n)`, the asymptotic factorial
growth rate `(β_0/4π)^(n+1) = (7/4π)^(n+1)`. The subleading exponent
has retained leading piece `1 − β_1/β_0² ≈ 23/49`.

However, the Stokes constant `S_IR` closed form is NOT retained: it
requires identifying the QCD instanton moduli with the current
physical `Cl(3)`/`Z³` framework baseline, which is structurally
suggestive (Z_3 center symmetry
analogue) but unproved. The full Borel transform `B[β](z)` and
finite-n subleading corrections at `n=2,3` are not retained;
benchmarking `S_IR=1, b=23/49` gives `β_2^asymp ≈ 0.036`, vs literature
`β_2(MS-bar) = 32.5` — a multiplicative gap of ~900× at `n=2`,
indicating finite-n corrections matter exactly where `β_2/β_3` live.

**Net.** Attack 3 ADDS Borel-plane geometric retentions; it cannot
close the closed-form `β_2/β_3` via resurgence without additional
input on Stokes constants and finite-n corrections.

### Step 5 — Attack 4: Topological (Chern-Simons / knot)

**Framework.** Chern-Simons theory on `T³` with `SU(3)` gauge group
has partition function `Z(T³, SU(3)_k) = (k+1)(k+2)/2`, a single
integer at each level. Wilson-loop expectation values give knot
polynomial outputs in cyclotomic algebraic numbers
`Q[ζ_(k+h^∨)]` with `h^∨(SU(3)) = 3` the dual Coxeter number.

**Retention boundary.** The CS data and knot polynomials are
algebraic in cyclotomic fields. The TVZ 3-loop weights are pure
rationals (`2857/54, ...`), and the VVL 4-loop weights are rationals
plus `ζ_3` multiples. Since `Q` is contained in cyclotomic fields,
bare field membership is not the obstacle. The obstacle is that the
specific CS data does not construct the specific TVZ channel vector,
and there is no derived map from `Z[ζ_(k+3)]` outputs to the `ζ_3`
terms used as comparators. The level shift `k → k + h^∨ = k + 3` is
ONE integer, while `β_n` channel decomposition has many independent
rationals; pure CS topology does not supply the multi-channel
weighting.

**Net.** Attack 4 retains the CS / knot data as substrate-native
topological invariants; it cannot construct the specific TVZ/VVL
channel weights.

### Step 6 — P-L1-D synthesis: rank-2 vs rank-6 deficit

The most natural substrate-native period functor composes two
sub-functors:

```text
P_Cl(3)^HK :     1PI Graph -> Q,         Gamma -> [s_t^n] <P>_HK_SU(3)(s_t)
                                                     = (-1)^(n+1) (4/3)^n / n!
P_Cl(3)^Schnetz: 1PI Graph -> Z[q],     Gamma -> #{alpha in F_q^|E| : Psi_Gamma(alpha) = 0}.
```

The composition `P_Cl(3) := P_Cl(3)^HK × P_Cl(3)^Schnetz` assigns
each graph at loop `n` the pair `(T(n), c_2(Gamma))`. `T(n)` is ONE
rational per loop order. `c_2(Gamma)` is ONE Galois class per graph
(rational / `ζ_3` / etc., not a rational value). To reproduce the
SIX distinct MS-bar rationals in TVZ at 3-loop, the construction
must span a 6-dimensional rational space — which neither sub-functor
nor their composition can:

```text
rank(P_Cl(3))                  =  2
rank(MSbar channel space)      =  6
deficit                        =  4 missing rational coefficients
```

The rank-2 composition reproduces the universal `β_0 = 7` and
`β_1 = 26` at 1-loop and 2-loop (already retained via Casimir
algebra), but fails at 3-loop (`P_Cl(3)^HK` at 3-loop is `32/81`;
`β_2^MSbar` at `N_f = 6` is `-65/2`; ratio ~82×, a structural
scheme-conversion gap).

### Step 7 — The 3 named missing sub-functors

The P-L1-D analysis sharpens the residual open-gate requirement to THREE
structurally independent missing ingredients:

| Sub-functor | What it would do | Why it is not retained |
|---|---|---|
| (a) HK ↔ MSbar 3-loop scheme conversion | Convert `β_2^HK = 32/81` to `β_2^MSbar = -65/2` via the 3-loop plaquette-coupling matching integral | The plaquette-coupling matching integral is a 3-loop computation (Alles-Feo-Panagopoulos 1996; Bode-Panagopoulos 2002), not retained from Cl(3)/Z³ |
| (b) `c_2` ↔ rational-coefficient extraction | Turn `F_q` Galois-class data into rational coefficients (e.g., the "6" in `6 ζ_3` for `K_4`) | Requires full period-evaluation machinery comparable to Brown-Schnetz period theory, not retained |
| (c) per-graph Casimir channel projection | Decompose TOTAL graph period into the 6 TVZ monomial channels | Combinatorial bookkeeping that compounds (a) and (b) |

These three ingredients are independent in the sense that closing
any one does not close the others, and they are exhaustive in the
sense that their joint resolution would close the rank-2-vs-rank-6
deficit at 3-loop (and the analogous deficit at 4-loop).

## Theorem (L1 β_2/β_3 4-Attack Terminality)

**Theorem.** On the existing physical `Cl(3)` local algebra and
`Z³` spatial substrate, together with
`beta_0 = (11 N_c − 2 N_f)/3 = 7`,
`beta_1 = (34/3) C_A² − (20/3) C_A T_F N_f − 4 C_F T_F N_f = 26`,
retained Casimir algebra at SU(3) (including quartic Casimir values),
retained `<P>`-scheme heat-kernel plaquette, and Schnetz F_q point
counts on Kirchhoff polynomials as substrate-native combinatorial
content:

```text
(a) Channel skeleton retention. The QCD beta-function channel skeleton
    (6 channels at 3-loop in MS-bar; 17+ channels at 4-loop) is
    supported by retained Casimir algebra. The channel
    SKELETON / VALUE is positive content from Attacks 1-2.
    [Verified Section 1 of runner.]

(b) Scheme-foreign barrier (MS-bar). The MS-bar channel WEIGHTS
    `w_n,ch` for n >= 3 are 3-/4-loop master integrals in dim-reg.
    Dim-reg is foreign to the lattice/`<P>`-scheme native framework;
    the scheme-conversion integral from `<P>`-scheme to MS-bar at
    3-loop is itself a non-retained 3-loop computation.
    [Verified Section 2 of runner.]

(c) Casimir-value vs channel-weight separation. Casimir VALUES at SU(3)
    (`C_F=4/3, C_A=3, T_F=1/2, d_F^abcd d_F^abcd / N_F = 5/12, ...`)
    are pure group theory, reproducible from retained generator
    algebra. Channel WEIGHTS (the scalar coefficients multiplying
    these in `beta_2, beta_3`) are loop-integral content, NOT
    framework-supported. `beta_2` contains zero quartic-Casimir
    channels (TVZ closed form degree 2 in n_f), so the conjecture
    "β_2 derived from quartic Casimir values" is structurally
    foreclosed.
    [Verified Section 3 of runner.]

(d) Borel-plane geometry retention; Stokes constants admitted.
    Resurgence retains the IR renormalon at `z_* = 4π/7`, the UV
    renormalon ladder at `z = -4π/(7 n)`, and the asymptotic factorial
    growth `(β_0/4π)^(n+1)`. The Stokes constant `S_IR`, the full
    subleading exponent `b`, and finite-n corrections at `n=2, 3`
    are NOT retained. Benchmark `S_IR=1, b=23/49` gives `β_2^asymp ≈
    0.036`, vs `β_2(MS-bar) = 32.5` — a structural ~900× gap.
    [Verified Section 4 of runner.]

(e) Topological mismatch. CS-on-T³ with SU(3) gives finite/algebraic
    cyclotomic data with level shift `k → k + h^∨ = k + 3`; the
    MS-bar 3-loop weights are pure rationals (TVZ closed form), and
    the 4-loop weights are rationals plus `ζ_3` multiples (VVL
    1997). The CS/knot route does not construct the specific TVZ
    channel vector; the level shift `k+3 ≠ β_0 = 7` (at `N_f = 6`)
    so the "k+h^∨ ↔ β_0" identification is numerically falsified.
    [Verified Section 5 of runner.]

(f) P-L1-D rank deficit. The natural substrate-native period functor
    `P_Cl(3) := P_Cl(3)^HK × P_Cl(3)^Schnetz` is rank 2 (one rational
    per loop order from `P_Cl(3)^HK`, one Galois class per graph from
    `P_Cl(3)^Schnetz`). The MS-bar 3-loop channel space is rank 6.
    Rank deficit = 4 missing rational coefficients, decomposable
    into 3 named sub-functor missing ingredients:
       (a) HK ↔ MS-bar 3-loop scheme conversion
       (b) c_2 ↔ rational-coefficient extraction
       (c) per-graph Casimir channel projection
    [Verified Section 6 of runner.]

Therefore: at loop orders `>= 3`, the QCD beta-function scalar
channel weights are not closed by the four tested route families
(MS-bar dim-reg, Casimir, resurgence, topological) from the current
framework inputs. The residual open-gate requirement decomposes to
three structurally independent named sub-functors (a, b, c).
The L1 admission count is UNCHANGED. No new admission. No new axiom.
```

**Proof.** Each item is verified by the runner. Section 1 (channel
skeleton from Casimir algebra); Section 2 (MS-bar scheme-foreign
verification); Section 3 (Casimir-value vs channel-weight
separation and `beta_2` no-quartic verification); Section 4
(Borel-plane retention + benchmark resurgence numerics); Section 5
(CS/knot cyclotomic vs rational mismatch + `k+3 vs β_0` numerical
check); Section 6 (P-L1-D rank deficit and 3 named sub-functors);
Section 7 (cross-validation); Section 8 (verdict synthesis);
Section 9 (does-not-do disclaimers); Section 10 (comparison with
prior L1 probes). ∎

**Corollary (bounded no-go content).** Any future closure of
`β_2` and/or `β_3` within these four tested route families must supply
at least one of the 3 named missing sub-functors (a, b, c). The
tested route families cover:

- the **scheme-perturbation** axis (Attack 1: dim-reg vs lattice),
- the **group-invariant-theory** axis (Attack 2: Casimirs),
- the **asymptotic-resurgence** axis (Attack 3: Borel/Stokes),
- and the **topological-QFT** axis (Attack 4: CS/knot).

A fifth structurally orthogonal axis is not visible from the current
sources used here; any future attempt within this surface that does
not supply at least one of (a), (b), (c) reduces to one of the four
tested axes, hence to one of the four established no-gos.

## What the runner checks

The paired runner verifies:

1. `beta_0 = (11 N_c − 2 N_f)/3 = 7` at `SU(3), N_f = 6` via the
   retained universal formula.
2. `beta_1 = 26` via retained Casimirs at `SU(3), N_f = 6`.
3. Casimir values: `C_F = 4/3, C_A = 3, T_F = 1/2`, and the quartic
   Casimirs `d_F^abcd d_F^abcd / N_F = 5/12`, etc., from explicit
   SU(3) generator algebra (8 generators in the fundamental,
   sufficient products).
4. TVZ `beta_2(N_f = 6) = 2857/2 − (5033/18)(6) + (325/54)(6²) =
   -65/2` reproduced from the closed-form formula (consistency
   check against literature value, not a derivation).
5. Heat-kernel plaquette closed form
   `<P>_HK_SU(3)(s_t) = 1 − exp(−(4/3) s_t)` and its loop-order
   coefficient extraction (giving `4/3, -8/9, 32/81, -32/243` at
   loops 1-4).
6. The ratio `β_2^HK(loop=3) / β_2^MS-bar(N_f=6) = (32/81) / (-65/2) =
   -64/5265 ≈ -0.012`, demonstrating the structural scheme-conversion
   gap.
7. Schnetz Kirchhoff point counts for the 1-loop bubble, 2-loop
   sunset, and 3-loop K_4 = wheel_3 graphs.
8. K_4 c_2 invariant residues: `q=2: ⌊36/4⌋ mod 2 = 1`,
   `q=3: ⌊261/9⌋ mod 3 = 2`, consistent with the known `6 ζ_3`
   period class for K_4 (Broadhurst-Kreimer 1997).
9. Resurgence Borel-plane: `z_* = 4π/7`, UV ladder at
   `z = -4π/(7 n)`, asymptotic growth `(7/4π)^(n+1)` for `n = 1, 2,
   3, 4`. Benchmark resurgence formula at `S_IR = 1, b = 23/49`
   gives `β_2^asymp` ≈ 0.036.
10. CS-on-T³ with SU(3): partition function `Z = (k+1)(k+2)/2` at
    `k = 1, 2, 3`. Numerical check `k + h^∨ = k + 3 ≠ β_0 = 7` at
    `N_f = 6`.
11. P-L1-D rank-deficit count: 2 (period functor composition rank)
    vs 6 (MS-bar 3-loop channel rank); deficit 4.
12. 3 named missing sub-functors documented with their respective
    role definitions.

## What this theorem does NOT claim

1. Does NOT close `β_2` or `β_3`.
2. Does NOT modify the L1 admission count.
3. Does NOT add new repo-wide axioms.
4. Does NOT promote any underlying source note to a new tier.
5. Does NOT promote the Casimir-value supports to retained tier.
6. Does NOT prove `β_2/β_3` are impossible to derive on Cl(3)/Z³:
   only that the four tested attack frameworks are structurally
   inadequate, and that the residual open-gate requirement decomposes to 3
   named sub-functor missing ingredients. A future closure
   supplying at least one of (a, b, c) is not ruled out.
7. Does NOT use PDG values of `alpha_s` or any phenomenological
   matching condition as derivation input.
8. Does NOT import Brown-Schnetz period evaluation, dim-reg, or
   scheme-conversion integrals as derivation input.

## Audit handoff

```yaml
proposed_claim_type: no_go
proposed_claim_scope: |
  Four tested route families for QCD `beta_2/beta_3` closure under
  the current physical Cl(3)/Z^3 framework baseline (MS-bar dim-reg,
  quartic Casimir, resurgence trans-series, topological CS/knot) each
  terminate negatively at the channel-weight layer. The natural
  substrate-native period functor decomposition `P_Cl(3)^HK ×
  P_Cl(3)^Schnetz` is rank 2 vs the MS-bar 3-loop channel space rank
  6, giving a rank deficit of 4 missing rational coefficients. The
  residual open-gate requirement decomposes to 3 named sub-functor missing
  ingredients (HK ↔ MS-bar scheme conversion at 3-loop;
  c_2 ↔ rational-coefficient extraction; per-graph Casimir channel
  projection). The four tested axes (scheme, Casimir, resurgence,
  topological) cover the attack surface exercised by this runner.
status_authority: independent audit lane only
admitted_context_inputs:
  - `beta_2` and `beta_3` closed forms remain admitted at the
    channel-weight layer at loop `>= 3`.
  - Underlying source notes are not promoted or otherwise retagged by
    this note.
  - P-L1-D open-gate source content remains an open-gate input; this
    note records terminality, not closure.
forbidden_imports_used: false
audit_required_before_effective_status_change: true
```

## References

- Tarasov, O. V., Vladimirov, A. A., and Zharkov, A. Yu. (1980).
  *Phys. Lett. B* 93, 429 — 3-loop QCD beta function in MS-bar.
- Larin, S. A. and Vermaseren, J. A. M. (1993). *Phys. Lett. B* 303,
  334 — 3-loop QCD with general gauge group.
- van Ritbergen, T., Vermaseren, J. A. M., and Larin, S. A. (1997).
  *Phys. Lett. B* 400, 379 — 4-loop QCD beta function in MS-bar.
- Alles, B., Feo, A., and Panagopoulos, H. (1996). *Nucl. Phys. B*
  502, 325 — 3-loop lattice-plaquette ↔ MS-bar matching.
- Bode, A. and Panagopoulos, H. (2002). *Nucl. Phys. B* 625, 198 —
  refined lattice-plaquette scheme matching.
- Broadhurst, D. J. and Kreimer, D. (1997). *Phys. Lett. B* 393, 403
  — K_4 wheel period `6 ζ_3`.
- Schnetz, O. (2010). *Commun. Number Theory Phys.* 4, 1 — `c_2`
  arithmetic invariants.
- Brown, F. (2017). Periods and Feynman amplitudes. *Proc. ICM*.
- Marino, M. (2014). *Lectures on non-perturbative effects in large N
  gauge theories, matrix models, and strings*. Fortschr. Phys. 62, 455.

## Cross-references

### Source-note dependencies (per-attack)

- Attack 1 (MS-bar): runner classification and literature comparator
- Attack 2 (Casimir): [`KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md`](KOIDE_V_L1_QUARTIC_CASIMIR_BETA2_NOTE_2026-05-08_probeV_L1_quartic.md)
- Attack 3 (Resurgence): runner classification and literature comparator
- Attack 4 (Topological): [`KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md`](KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md)
- Synthesis: [`PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md`](PRIMITIVE_P_L1_D_PERIOD_FUNCTOR_NOTE_2026-05-10_pPl1_d.md)

### Structural baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- SU(3) NLO closure (heat-kernel plaquette): [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)
- QCD low-energy running bridge: [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this theorem
  derives the rank-2-vs-rank-6 deficit from the P-L1-D construction;
  the conclusion is structural, not a numerical coincidence. The 3
  named sub-functor decomposition is derived from the rank deficit,
  not asserted.
- `feedback_hostile_review_semantics.md`: stress-tests the four
  semantic claims ("MS-bar route closes β_2", "quartic Casimirs
  determine β_2/β_3", "resurgence supplies S_IR closed form",
  "CS/knot constructs the TVZ channel vector"); each is rejected at
  the action-level identification.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion; this note is a bounded no-go theorem with
  sharpened residual open-gate content and no source-note retagging.
- `feedback_physics_loop_corollary_churn.md`: this note adds new
  POSITIVE structural content (the unified 4-attack terminality
  statement and the 3 named sub-functor decomposition) that none
  of the four individual probes states.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (closing `β_2/β_3`) characterized in terms of WHICH sub-functor
  must be supplied (a, b, or c), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  consolidates four independent attacks into a single load-bearing
  terminality statement, with explicit per-attack reduction to one
  of three named sub-functors.
- `feedback_review_loop_source_only_policy.md`: this note is a
  single source-note theorem + paired runner + cached output. No
  synthesis, no lane promotions, no working "Block" notes.

## Validation

```bash
python3 scripts/cl3_theorem_l1_4attack_terminality_2026_05_10_t2l1.py
```

Expected: `=== TOTAL: PASS=N, FAIL=0 ===` where N is the runner's
declared check count.
