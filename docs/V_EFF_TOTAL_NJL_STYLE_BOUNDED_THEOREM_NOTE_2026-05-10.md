# V_eff Total (NJL-Style) with Tree σ²/(2 G_eff) Term and Gap Equation — Bounded Theorem

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_v_eff_total_njl_style.py`](../scripts/frontier_v_eff_total_njl_style.py)

## 0. Audit context and scope

The framework's bare logarithmic potential
`V_taste(σ) = -8 log(σ² + 4 u_0²)` (parent
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) Step 4)
is **monotonically decreasing for σ > 0** and therefore has
**no interior minimum** by itself. Standard NJL-style composite-Higgs
analyses include a tree-level σ²/(2 G_eff) term that, together with
the fermion-loop log-determinant, yields a stable broken-phase saddle
when the four-fermion coupling exceeds a critical value. Without that
tree term the framework's V_taste alone cannot give an interior EWSB
minimum; with it, the question of whether the framework's lattice
action is above or below the NJL critical coupling becomes a precise,
decidable algebraic statement.

This note (i) identifies a candidate σ²/(2 G_eff) tree term natural
to the framework's lattice action via integrating out gauge fields at
strong coupling; (ii) derives the resulting NJL-style gap equation
analytically; (iii) computes the framework's critical coupling
`G_critical = u_0²/4`; (iv) reports leading-order strong-coupling
estimate of `G_eff = 1/(2 N_c)` from Kawamoto–Smit (1981); (v) compares
`G_eff` to `G_critical` and finds the framework lattice in the
**symmetric phase** at leading order — i.e., the lattice-gauge-only
sector does not by itself drive chiral SSB, so EWSB would have to come
from additional structure such as the SU(2)_L × U(1)_Y electroweak
gauge structure (which is not part of the lattice gauge action this
note examines). This is a precise bounded statement consistent with
the framework's existing admitted-context inputs and does NOT close
any gap. It records the
NJL-style gap equation structure and locates the framework's
position in the NJL phase diagram.

The result is **structurally interesting**: at the canonical operating
point (β = 6, N_c = 3, u_0 ≈ 0.8776), `G_eff/G_critical ≈ 0.866` —
near-critical, in the weakly attractive regime, but on the
**symmetric** side of the chiral-SSB threshold. The conclusion is
sensitive to sub-leading corrections to `G_eff` at the O(1) level
(this is the bounded-theorem named admission); the leading-order
Kawamoto–Smit result drives the qualitative outcome.

## 1. Claim scope

> **Theorem (V_eff total NJL-style structure on framework's lattice).**
> Define
>
> ```text
> V_total(σ)  =  σ² / (2 G_eff)  −  8 log(σ² + 4 u_0²)              (1)
> ```
>
> on the canonical physical Cl(3) local algebra plus Z³ spatial-substrate
> Wilson-plaquette + staggered-Dirac
> mean-field surface (HIGGS_MASS_FROM_AXIOM Step 2, mean-field
> factorization `U_{ab} → u_0 δ_{ab}`, minimal APBC L_s = 2 block,
> N_sites = N_taste = 16). Then
>
> 1. **Gap equation.** `dV_total/dσ = 0` reduces to
>
>    ```text
>    σ · [1/G_eff  −  16/(σ² + 4 u_0²)]  =  0.                       (2)
>    ```
>
>    The trivial root `σ = 0` is always a critical point. The
>    nontrivial root is
>
>    ```text
>    σ_min²  =  16 G_eff  −  4 u_0²,                                  (3)
>    ```
>
>    which exists (`σ_min² > 0`) iff
>
>    ```text
>    G_eff  >  G_critical  :=  u_0² / 4.                              (4)
>    ```
>
> 2. **Phase identification.** At `σ = 0`,
>    `d² V_total / dσ²|_{σ=0} = 1/G_eff − 4/u_0²`, which is positive
>    (`σ = 0` stable) iff `G_eff < G_critical`. At the nontrivial
>    minimum (when it exists),
>
>    ```text
>    d² V_total / dσ²|_{σ_min}  =  σ_min² / (8 G_eff²)
>                              =  (4 G_eff − u_0²) / (2 G_eff²).      (5)
>    ```
>
> 3. **Framework-side leading-order numerical position.** With the
>    Kawamoto–Smit leading-order strong-coupling lattice estimate
>    `G_eff_LO = 1/(2 N_c)`, at framework values `N_c = 3` and
>    `u_0 ≈ 0.8776`:
>
>    ```text
>    G_eff_LO  =  1/6  ≈  0.1667
>    G_critical  =  u_0²/4  ≈  0.1925
>    G_eff_LO / G_critical  ≈  0.866
>    ```
>
>    so `G_eff_LO < G_critical` and the lattice gauge sector alone is
>    on the **symmetric side** of the NJL chiral-SSB threshold — the
>    nontrivial root (3) does not exist at leading order, and the only
>    extremum is the trivial `σ = 0`.

The bounded theorem **explicitly does NOT** claim:

- a derivation of EWSB from the framework's lattice action alone
  (the leading-order strong-coupling result puts the lattice in the
  symmetric phase; EWSB driver must come from additional structure,
  e.g. SU(2)_L × U(1)_Y gauge bosons + top-Yukawa, which are NOT
  part of the lattice action examined here);
- a definitive G_eff value (the leading-order Kawamoto–Smit
  `1/(2 N_c)` is the canonical leading-order estimate; sub-leading
  corrections in `1/g²` and `u_0` dressing can shift `G_eff` by
  O(1) factors — see §6.2 sensitivity analysis);
- an identification of the candidate four-fermion structure with
  the actual framework action (the framework's Wilson-plaquette
  action does NOT contain a manifest four-fermion term; the
  candidate `(σ²/(2 G_eff))` arises from integrating out gauge
  fields at strong coupling, which is a standard but admitted
  derivation step — see §3 named admissions);
- a closure of Gate #3 (Morse / convexity for V_taste). The Gap #3
  probe established that V_taste alone has no interior minimum; this
  note shows that the **standard NJL tree term** + V_taste **would**
  give a minimum if `G_eff > G_critical`, but the framework's
  leading-order `G_eff_LO < G_critical`, so the lattice action alone
  remains insufficient to drive a Higgs minimum. Closing Gate #3
  requires either (a) sub-leading G_eff corrections that flip the
  ratio, or (b) coupling to the EW gauge sector;
- a Higgs mass prediction. Since the framework is in the symmetric
  phase at leading order, no `m_H_pole` extraction from (5) is
  performed (`σ_min` does not exist there); we record what the
  formula **would** give in a hypothetical broken-phase scenario as
  a structural ingredient for downstream work, not as a derived
  prediction.

## 2. Counterfactual Pass — implicit assumptions

| # | Assumption | Forced or imported? | If wrong, what changes? |
|---|---|---|---|
| 1 | A four-fermion contact term is generated at lattice strong coupling | Imported from Kawamoto–Smit (1981); standard lattice strong-coupling expansion | If no four-fermion term is generated, V_total reduces to V_taste alone (no interior minimum, gap #3 unclosed). |
| 2 | The dominant scalar channel of that four-fermion term is `(ψ̄ψ)²` (after Fierz) | Standard NJL-channel Fierz decomposition; admitted | If a different channel dominates (vector / tensor), the candidate σ²/(2 G_eff) tree term has different parametric form. |
| 3 | Mean-field factorization of the bilinear `(ψ̄ψ)² → σ ψ̄ψ + σ²/(2 G_eff)` (Hubbard–Stratonovich) | Standard composite-Higgs auxiliary-field trick | If mean-field is invalid (strong fluctuations), the gap equation is shifted at sub-leading order. |
| 4 | `G_eff = 1/(2 N_c)` at leading order in 1/g² (Kawamoto–Smit form) | Imported from Kawamoto–Smit (1981) leading-order result | Other forms (1/(g² N_c), Casimir-corrected, u_0-dressed) shift G_eff by O(1) factors; phase outcome flips for some forms (see §6.2). |
| 5 | The framework's u_0 = 0.8776 is the canonical mean-field link | Engineering frontier (Gate #7 / C-iso convention) | Numerical position shifts but structural form (3),(4) unchanged. |
| 6 | V_taste prefactor `-8` is correct | Imported from HIGGS_MASS_FROM_AXIOM Step 2 | If prefactor is different (e.g., due to N_taste channel choice), `G_critical = u_0²/4` rescales by the prefactor ratio. |
| 7 | The L_s = 2 minimal APBC block is the right surface | Standard framework convention; admitted | Different blocks shift V_taste prefactor (see #6). |

The load-bearing assumptions are (1), (2), (4): **whether** a
four-fermion term is generated, **what channel** dominates after
Fierz, and **what numerical value** of G_eff results at leading
order. Assumptions (1) and (2) are textbook lattice-strong-coupling
results (Kawamoto–Smit 1981, Münster); assumption (4) inherits its
O(1) uncertainty from the leading-order truncation, and §6.2 records
the sensitivity. The structural NJL-style gap equation (2)–(5) holds
for **any** G_eff > 0; only the phase diagnosis depends on the
G_eff numerical value.

**Negate each:**

- **Negate (1):** if no four-fermion is generated, V_total = V_taste,
  and Gap #3 (Morse / convexity) remains unclosed by **any**
  variation of this style. The note's claim is bounded **conditional
  on (1)**.
- **Negate (2):** if a non-scalar channel dominates, V_total has a
  different parametric form; the σ-channel analysis becomes one of
  several parallel channel analyses, and the framework would need
  channel-by-channel analysis. Not the scope of this note.
- **Negate (4):** if G_eff scales differently with N_c, beta, or u_0,
  the leading-order phase outcome can flip. §6.2 sensitivity table
  shows that some plausible forms put the system in the broken phase.
  This is the **bounded admission** of this note.

## 3. Elon first-principles — what is V_total, really?

**Stripping all framework conventions, what does fundamental
composite-Higgs theory say?**

Standard NJL Lagrangian:

```text
L_NJL  =  ψ̄ (i ∂̸) ψ  +  (g²/Λ²) (ψ̄ ψ)²                              (*)
```

with Λ a UV cutoff (in lattice context, Λ ~ 1/a with a the lattice
spacing). Hubbard–Stratonovich auxiliary scalar `σ`:

```text
(g²/Λ²) (ψ̄ ψ)²  =  -σ ψ̄ ψ  -  σ² / (2 G)
                with G  =  g² / Λ².                                   (**)
```

Integrating out fermions (mean-field):

```text
V_eff(σ)  =  σ² / (2 G)  -  Tr log(D + σ)
          =  σ² / (2 G)  -  N_c · [Λ²σ²/(8π²)  +  σ⁴/(16π²) log(Λ²/σ²)  + ...]
```

(standard NJL textbook result, e.g. Hatsuda–Kunihiro hep-ph/9401310
Section 2). The gap equation `dV_eff/dσ = 0` gives a non-trivial
chiral-symmetry-breaking solution iff

```text
G · Λ²  >  G_critical · Λ²  =  2π² / N_c                              (***)
```

(critical coupling for chiral SSB in 4D NJL with hard cutoff;
equivalent in spirit to the lattice `G_critical = u_0²/4` derived
below for the framework's specific eigenvalue structure).

**Now: what is V_total in the framework?**

The framework's mean-field log-determinant from
HIGGS_MASS_FROM_AXIOM Step 2 is NOT the continuum Tr log;
instead the staggered-Dirac eigenvalue spectrum is degenerate
(`|λ_k| = 2 u_0` for all N_taste = 16 eigenvalues) by the Clifford
identity D_taste² = d · I. This collapses the continuum integral

```text
Tr log(D + σ)  =  ∫ d⁴p/(2π)⁴ log(p² + σ²)  →  Λ-cutoff integral
```

into the discrete sum

```text
W(J=σ)  =  Σ_k (1/2) log(σ² + |λ_k|²)
        =  (N_tot/2) log(σ² + 4 u_0²),                                (****)
```

which is exact on the L_s = 2 minimal block (no IR/UV subtractions
needed — the framework's spectrum is finite and degenerate). After
factoring N_c out and per-site normalization, this gives the
framework's V_taste(σ) = -8 log(σ² + 4 u_0²) (eight = N_taste/2).

**The gap equation (2) is the framework's lattice-discretized analog
of NJL's continuum gap equation.** The critical coupling
`G_critical = u_0²/4` is the framework's lattice analog of the
continuum `2π²/N_c`. Both have the same physical content: dimensional
analysis forces `G · (UV scale)² ~ O(1)` at the chiral-SSB threshold;
the specific numerical factor depends on the spectral structure of
the regulator.

**This is honest first-principles physics.** The framework's V_taste
plus an admitted NJL-style tree term σ²/(2 G_eff) yields the
**standard composite-Higgs gap equation structure** with the
framework-specific spectral input giving `G_critical = u_0²/4`. The
load-bearing question is whether the framework's `G_eff` is above or
below this threshold.

## 4. Computing G_eff from lattice strong-coupling expansion

**Standard result (Kawamoto–Smit 1981, Nucl. Phys. B192 100;
Münster textbook).** Integrating out gauge link variables `U_{ab}` at
strong coupling (large `g²`, equivalently small β) on a hypercubic
lattice with staggered fermions generates color-singlet four-fermion
contact terms. At leading order in 1/g², the dominant (scalar-channel
after Fierz) coefficient is

```text
G_eff_LO  =  1 / (2 N_c · g²)              (lattice units, a = 1).    (5)
```

For framework operating point (`β = 2 N_c / g² = 6`, `N_c = 3`):

```text
g²  =  2 N_c / β  =  6/6  =  1                                        (6)
G_eff_LO  =  1 / (2 N_c · 1)  =  1 / 6  ≈  0.1667                     (7)
```

**Comparison to G_critical:**

```text
G_critical  =  u_0² / 4  =  (0.8776)² / 4  ≈  0.1925                  (8)
G_eff_LO / G_critical  ≈  0.1667 / 0.1925  ≈  0.866                   (9)
```

**Result:** the framework lattice gauge sector at leading order in
1/g² is **below the NJL critical coupling**, in the **symmetric
phase**. The lattice action alone does not drive chiral SSB.

This is consistent with the established framework picture:
EWSB is driven by the **electroweak** gauge structure (SU(2)_L ×
U(1)_Y) coupled to the top quark Yukawa and the Higgs scalar — none
of which are part of the **strong-coupling lattice gauge action**
analyzed here. The framework's prediction `m_H_tree = v/(2 u_0) =
140.3 GeV` (HIGGS_MASS_FROM_AXIOM) is read off the
**symmetric-point curvature** of V_taste, not at a broken-phase
minimum (the parent note explicitly admits this in Step 5(b): the
identification of symmetric-point curvature with broken-phase pole
becomes exact in a limit "(i) all N_taste taste channels degenerate,
(ii) gauge corrections vanish, (iii) EWSB saddle aligns with
symmetric-point curvature. None of (i)-(iii) is exactly true").
**This note explains, from first principles, why (iii) cannot be
exactly true at the level of the lattice gauge sector alone:** the
broken-phase saddle does not exist there.

## 5. Load-bearing step (class A)

```text
Setup:
  V_total(σ)  =  σ² / (2 G_eff)  −  8 log(σ² + 4 u_0²)               [from (1)]

Step A.1 — first derivative:
  dV_total/dσ  =  σ/G_eff  −  16 σ / (σ² + 4 u_0²)
              =  σ · [1/G_eff − 16/(σ² + 4 u_0²)]                     [factor σ]

Step A.2 — gap equation roots:
  σ = 0  is always a critical point.
  Nontrivial root from 1/G_eff = 16/(σ² + 4 u_0²):
    σ² + 4 u_0² = 16 G_eff  ⇒  σ_min² = 16 G_eff − 4 u_0²            [from (3)]

Step A.3 — existence of nontrivial root:
  σ_min² > 0  ⇔  16 G_eff > 4 u_0²  ⇔  G_eff > G_critical = u_0²/4    [from (4)]

Step A.4 — second derivative:
  d²V_total/dσ²  =  1/G_eff
                  + 16 · [-(σ² + 4 u_0²) + 2 σ²] / (σ² + 4 u_0²)²
                =  1/G_eff  +  16 · (σ² − 4 u_0²) / (σ² + 4 u_0²)²
                =  1/G_eff  +  16 σ²/(σ² + 4 u_0²)²
                              −  64 u_0² / (σ² + 4 u_0²)²              [explicit form]

Step A.5 — at σ = 0:
  d²V_total/dσ²|_{σ=0}  =  1/G_eff  −  64 u_0² / (4 u_0²)²
                       =  1/G_eff  −  4/u_0²                          [trivial root curvature]

  Stable (positive) iff G_eff < u_0²/4 = G_critical. ✓ matches (4).

Step A.6 — at σ = σ_min (when broken phase exists):
  Use σ_min² + 4 u_0² = 16 G_eff:
    1/G_eff  =  16/(σ² + 4 u_0²)  =  16/(16 G_eff)  =  1/G_eff (self-consistent)
    16 σ²/(σ² + 4 u_0²)²  =  16 σ_min² / (16 G_eff)²  =  σ_min²/(16 G_eff²)
    64 u_0²/(σ² + 4 u_0²)²  =  64 u_0² / (256 G_eff²)  =  u_0²/(4 G_eff²)

  d²V_total/dσ²|_{σ_min}
    =  1/G_eff  +  σ_min²/(16 G_eff²)  −  u_0²/(4 G_eff²)
    =  [16 G_eff + σ_min² − 4 u_0²] / (16 G_eff²)
    =  [16 G_eff + (16 G_eff − 4 u_0²) − 4 u_0²] / (16 G_eff²)
    =  [32 G_eff − 8 u_0²] / (16 G_eff²)
    =  (4 G_eff − u_0²) / (2 G_eff²)                                 [from (5)]

  Equivalently, σ_min² / (8 G_eff²)  =  (16 G_eff − 4 u_0²) / (8 G_eff²)
                                     =  (4 G_eff − u_0²) / (2 G_eff²) ✓

  Positive iff G_eff > u_0²/4 = G_critical. ✓ Stable broken-phase saddle.
```

Class (A) algebraic substitution on V_total = σ²/(2 G_eff) − 8 log(σ² + 4 u_0²)
plus the gap-equation root from Step A.2. ∎

## 6. Structural implications (named, not derived)

### 6.1 Numerical phase diagnosis at framework values

At `u_0 ≈ 0.8776`, `N_c = 3`, `β = 6`:

```text
G_eff_LO  =  1/(2 N_c)  =  0.16667    [Kawamoto–Smit leading-order]
G_critical  =  u_0²/4   =  0.19255

  G_eff_LO / G_critical  =  0.866          ← symmetric phase
  σ_min² (formal)  =  16 G_eff_LO − 4 u_0² ≈  -0.4561  < 0   (does NOT exist)
```

The framework lattice gauge sector is **on the symmetric side** of
the NJL chiral-SSB threshold at leading order. No σ_min exists; no
m_H_pole extraction from the broken-phase formula (5) can be made.

### 6.2 Sensitivity to G_eff form (bounded admission)

The leading-order `G_eff = 1/(2 N_c)` is the canonical Kawamoto–Smit
result, but sub-leading corrections (1/g² expansion, u_0 dressing,
Casimir variants) can shift G_eff by O(1) factors. Sensitivity table:

| G_eff form | Source | Numerical | G/G_crit | Phase |
|---|---|---|---|---|
| `1/(2 N_c)` | Kawamoto–Smit LO | 0.16667 | 0.866 | **SYMMETRIC** |
| `1/(g² N_c)` | strong-coupling alt | 0.33333 | 1.731 | broken |
| `1/(g² (N_c²−1))` | Casimir variant | 0.12500 | 0.649 | symmetric |
| `(N_c²−1)/(2 N_c² g²)` | color-trace | 0.44444 | 2.308 | broken |
| `u_0²/(2 N_c)` | u_0²-dressed | 0.12836 | 0.667 | symmetric |
| `u_0⁴/(2 N_c)` | u_0⁴-dressed | 0.09886 | 0.513 | symmetric |

**Four of six plausible forms put the framework in the SYMMETRIC
phase**, with G_eff / G_critical ≈ 0.5–0.9. Two forms (with
different group-theory dressings) give the broken phase. The
**leading-order Kawamoto–Smit form** is the one with the strongest
literature backing for the staggered-fermion strong-coupling
expansion; this drives the bounded conclusion.

The **named bounded admission** of this theorem is: the precise
parametric form of G_eff at sub-leading orders in 1/g² and u_0
dressing is not derived here. The leading-order Kawamoto–Smit form
is admitted as the canonical reference; alternative forms are
recorded for sensitivity.

### 6.3 Implication: lattice action alone insufficient for EWSB

The framework's leading-order strong-coupling lattice gauge sector is
**below the NJL critical coupling**. EWSB therefore requires
additional structure beyond what is examined in this analysis:

- **SU(2)_L × U(1)_Y electroweak gauge bosons** (which are not part
  of the lattice gauge action this note examines);
- **Top quark Yukawa coupling** y_t (which provides the dominant
  attractive channel in Bardeen–Hill–Lindner top-condensation);
- **Wilson term taste-breaking** corrections (which lift the
  N_taste = 16 degeneracy and can shift the effective `8` prefactor
  in V_taste — see WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R notes).

These additional structures are admitted-context inputs from
sister authorities; their detailed contribution to V_total is
**out of scope** for this note. This note **records the lattice
gauge sector's NJL-style structural ingredient** and **identifies
its leading-order phase**.

### 6.4 Hypothetical broken-phase pole mass (formal, not predictive)

If `G_eff > G_critical` (broken phase, NOT the framework's leading-
order outcome but recorded for downstream comparison work):

```text
m_H_pole²(formal)  =  d² V_total/dσ²|_{σ_min}  =  (4 G_eff − u_0²)/(2 G_eff²)
                                             =  σ_min²/(8 G_eff²)        [lattice mass²]
```

In **lattice units** (a = 1, so all masses are dimensionless). To
compare to PDG `m_H_pole = 125.10 GeV`, a lattice-to-physical
conversion via `M_Pl` (or equivalently the framework's hierarchy
theorem `v = M_Pl · α_LM^16`) would be needed. Since the leading-
order phase outcome is **symmetric**, this comparison is **not
made here** — `σ_min` does not exist at leading order. Recording
the formal expression for downstream broken-phase scenario work.

### 6.5 Relation to Gate #3 (Morse / convexity)

The Gap #3 probe established `V_taste(σ) = -8 log(σ² + 4 u_0²)`
alone has no interior minimum. This note shows:

- **Gap #3 in current form is unclosed by V_total of style (1).**
  At leading-order Kawamoto–Smit G_eff_LO = 1/(2 N_c) ≈ 0.167 <
  G_critical ≈ 0.193, the V_total gap equation has only the trivial
  root σ = 0; no interior minimum exists.
- **Gap #3 closure requires either** (a) sub-leading G_eff
  corrections that flip G_eff > G_critical (sensitivity §6.2 shows
  this is possible with non-canonical forms but not with the
  leading-order strong-coupling form); (b) coupling to additional
  EW gauge / Yukawa structure that provides EWSB independent of
  the lattice gauge sector.

Gap #3 is **not closed** by this note. It is **structurally located
in the NJL phase diagram**: the framework's lattice gauge sector
sits at G_eff_LO/G_critical ≈ 0.866 — near-critical but on the
symmetric side. This is a **precise bounded statement**, not a
closure.

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_v_eff_total_njl_style.py
```

Verifies:

1. V_total(σ) form is correct: `σ²/(2 G_eff) − 8 log(σ² + 4 u_0²)`.
2. Gap equation factors as `σ · [1/G_eff − 16/(σ² + 4 u_0²)]`
   symbolically via SymPy.
3. Nontrivial root `σ_min² = 16 G_eff − 4 u_0²` from gap equation.
4. Critical coupling `G_critical = u_0²/4` from `σ_min² > 0`.
5. Trivial-root second derivative `d²V/dσ²|_{σ=0} = 1/G_eff − 4/u_0²`.
6. Broken-phase second derivative `d²V/dσ²|_{σ_min} = (4 G_eff − u_0²)/(2 G_eff²)`
   verified by direct substitution.
7. Numerical evaluation at framework values (u_0 = 0.8776, N_c = 3,
   β = 6, g² = 1): G_eff_LO = 1/6 ≈ 0.1667, G_critical ≈ 0.1925,
   ratio ≈ 0.866, **symmetric phase**.
8. Sensitivity sweep over six G_eff forms (§6.2 table) reproduced
   numerically.
9. Structural property: NJL phase boundary is `G·u_0² = 4` (lattice
   units), agreeing with the `G·Λ² ~ 2π²/N_c` continuum NJL critical
   condition up to an O(1) numerical coefficient that depends on
   spectral structure.
10. Note structure / scope discipline.

The runner does **not** verify EWSB (the framework is in the
symmetric phase), does not extract `m_H_pole` (no `σ_min`), and
does not close Gate #3.

## 8. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  NJL-style total effective potential V_total(σ) = σ²/(2 G_eff) - 8 log(σ² + 4 u_0²)
  on the framework's L_s=2 mean-field surface. Derives gap equation
  σ_min² = 16 G_eff - 4 u_0², critical coupling G_critical = u_0²/4,
  and second-derivative formulas. At leading-order Kawamoto-Smit
  G_eff = 1/(2 N_c) and framework u_0 ≈ 0.8776, locates the lattice
  gauge sector in the SYMMETRIC phase (G_eff/G_critical ≈ 0.866).
  EXPLICITLY DOES NOT close Gate #3 (Morse/convexity), does NOT
  derive EWSB from lattice action alone, does NOT extract m_H_pole
  (no broken-phase σ_min exists at leading order). Records the
  framework's structural position in NJL phase diagram and names
  the bounded admission (G_eff form at sub-leading orders).

proposed_load_bearing_step_class: A   # algebraic gap equation + critical coupling derivation
proposed_definitional_step_class: D   # σ²/(2 G_eff) tree-term identification (Hubbard-Stratonovich)
status_authority: independent audit lane only

declared_one_hop_deps:
  - higgs_mass_from_axiom_note   # V_taste form Step 2
  - staggered_dirac_realization_gate_note_2026-05-03   # N_taste = 16
  - minimal_axioms_2026-05-03   # physical Cl(3) local algebra + Z^3 spatial substrate
  - c_iso_su3_nnlo_closure_bounded_note_2026-05-10_su3nnlo   # u_0 frontier

admitted_context_inputs:
  - V_taste form V(m) = -8 log(m² + 4 u_0²) (HIGGS_MASS_FROM_AXIOM Step 2)
  - N_taste = 16 = 2^D (staggered-Dirac realization open gate)
  - u_0 ≈ 0.8776 (Gate #7 engineering frontier)
  - σ²/(2 G_eff) Hubbard-Stratonovich auxiliary scalar
    (standard NJL trick; admitted from Hatsuda-Kunihiro hep-ph/9401310)
  - G_eff = 1/(2 N_c) leading-order strong-coupling
    (Kawamoto-Smit 1981 / Münster 1994; admitted as canonical leading-order
    form, with O(1) sub-leading uncertainty named in §6.2)

bounded_admissions:
  - G_eff parametric form at sub-leading orders in 1/g² and u_0 dressing
    not derived here; leading-order Kawamoto-Smit form admitted
  - Hubbard-Stratonovich mean-field validity at strong coupling assumed
  - Scalar-channel dominance after Fierz assumed (other channels not
    analyzed)
  - lattice → continuum matching for G_eff·Λ² with Λ ~ 1/a not derived;
    framework's u_0² plays the analog role of the continuum cutoff Λ²
    in the critical condition

forbidden_imports_used: false    # no PDG values are derivation inputs;
                                 # observed m_H_pole appears only as an
                                 # audit comparator that is NOT used
                                 # (framework is in symmetric phase)
source_proposal_submitted_for_audit: true
audit_required_before_effective_status_change: true

named_open_bridge:
  bridge_id: njl_gap_3_phase_location
  description: |
    Gap #3 (Morse/convexity for V_taste) is NOT closed by this note.
    The framework's leading-order lattice gauge sector is in the
    SYMMETRIC phase of the NJL gap equation (G_eff_LO/G_critical ≈
    0.866). Closure of Gap #3 requires either (a) sub-leading G_eff
    corrections that flip the phase, or (b) coupling to additional
    EW gauge / Yukawa structure providing EWSB independent of the
    lattice gauge sector. Both routes are open.
```

## 9. What this theorem establishes

- **NJL-style structural ingredient supplied.** The framework's
  V_taste plus a candidate σ²/(2 G_eff) tree term yields the
  standard composite-Higgs gap equation; the framework-specific
  spectral structure gives `G_critical = u_0²/4`.
- **Phase identification.** At leading-order Kawamoto–Smit G_eff,
  the framework is on the **symmetric side** of the NJL chiral-SSB
  threshold, with `G_eff/G_critical ≈ 0.866`.
- **Gap #3 located, not closed.** The framework's lattice gauge
  sector sits near-critical but in the symmetric phase; Gap #3
  requires additional structure for closure.
- **Honest scope discipline.** No EWSB derivation, no `m_H_pole`
  extraction (no `σ_min` at leading order), no Gate #3 closure
  claimed.

## 10. What this theorem does NOT close

- **Gate #3 (Morse / convexity).** Located, not closed; framework
  is in symmetric phase at leading order.
- **EWSB from lattice action alone.** Lattice gauge sector is below
  the chiral-SSB threshold at leading order.
- **m_H_pole prediction from broken-phase formula.** No `σ_min`
  exists at leading order; the broken-phase d²V/dσ² formula (5) is
  recorded for downstream broken-phase scenario work, not derived
  as a prediction.
- **G_eff form at sub-leading orders.** Bounded admission;
  leading-order Kawamoto–Smit form admitted from literature.
- **Hubbard–Stratonovich mean-field validity at strong coupling.**
  Standard NJL admission, named.
- **Scalar-channel dominance after Fierz.** Other channels not
  analyzed.
- **Lattice → continuum matching for G_eff·Λ².** Bounded; framework's
  `u_0²` plays the analog role of continuum `Λ²`.
- **The numerical u_0 (Gate #7).** Admitted engineering frontier.
- **The staggered-Dirac realization gate.** Admitted open gate.

## 11. Cross-references

### Parent / structural
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — provides V_taste form (Step 2); Step 5(b) names the +12% gap
  whose lattice-side structural ingredient is identified here.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — N_taste = 16 = 2^D origin (open gate).
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  — physical Cl(3) local algebra plus Z^3 spatial substrate baseline.

### Context (parallel-track, not load-bearing)
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)
  — assumption-derivation ledger; CW analysis context.
- [`HIGGS_LATTICE_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](HIGGS_LATTICE_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
  — symmetric-point lattice ratio R_lattice = 1/(4 u_0²).
- [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  — Wilson-corrected V_taste extremum at leading order in r.
- [`C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`](C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md)
  — Gate #7 / C-iso engineering frontier; provides u_0 numerical
  context.

### Standard physics references (admitted-context literature, not load-bearing)
- Hatsuda & Kunihiro (1994), Phys. Rep. 247, 221, hep-ph/9401310 —
  NJL model gap equation, critical coupling, mean-field effective
  potential.
- Kawamoto & Smit (1981), Nucl. Phys. B192, 100 — strong-coupling
  expansion of lattice gauge theories with staggered fermions;
  source of leading-order `G_eff = 1/(2 N_c)` form.
- Bardeen, Hill, Lindner (1990), Phys. Rev. D41, 1647 — top-quark
  condensation NJL framework; structural template.
- Münster (1994), Quantum Fields on a Lattice (CUP) — textbook
  treatment of lattice strong-coupling expansion.
