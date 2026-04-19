# Charged-Lepton Curvature Kernel — Pure-APBC L_t Extension Note

**Date:** 2026-04-17
**Status:** exact structural no-go for the pure-APBC route — b = 0 holds
independently of L_t on the retained hw=1 triplet
**Script:** `scripts/frontier_charged_lepton_curvature_lt_extension.py`
**Authority role:** negative structural theorem extending Agent 1's
`CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md`. Rigorously establishes that
the off-diagonal source-response curvature `b = K_{12}` of the observable-
principle kernel on the retained hw=1 triplet vanishes for every pure-APBC
temporal block length `L_t`, not just the minimal `L_t = 4` anchor. The
Koide cone `a_0^2 = 2 |z|^2` is therefore unreachable by pure-APBC L_t
extension alone, and the attack surface must move to one of the four
mixing mechanisms enumerated in Part B.

## Safe statement

On the retained `Cl(3)` on `Z^3` framework surface, the runner
`frontier_charged_lepton_curvature_lt_extension.py` **symbolically
establishes** the following facts on every pure-APBC temporal block with
`L_t ∈ {4, 6, 8, 12, 16, 24}`, evaluated with the framework-native
staggered Dirac operator and species-diagonal sources restricted to the
retained hw=1 triplet:

1. **Diagonal kernel closed form (EXACT).** The species-diagonal
   observable-principle curvature is
   ```
   K_{ii}^{(spec)}(L_t) = 4 * sum_{n=0..L_t-1}  1 / (m_i^2 + u_0^2 (3 + sin^2 omega_n))
   ```
   with `omega_n = (2n+1) pi / L_t` the APBC Matsubara frequencies.

2. **Single-pole degeneracy at L_t = 4 only.** The sum collapses to
   `(4 L_t) / (m_i^2 + c(L_t) u_0^2)` iff all `sin^2(omega_n)` coincide,
   which holds only at `L_t = 4` (`sin^2 = 1/2`) giving the retained
   anchor `c(4) = 7/2`. For every `L_t ∈ {6, 8, 12, 16, 24}`, the sum is
   a genuine multi-pole expression in `m_i^2`, and the *effective*
   denominator constant
   ```
   c_eff(L_t) := L_t / sum_{n=0..L_t-1} 1 / (3 + sin^2 omega_n)
   ```
   (the harmonic mean of `3 + sin^2 omega_n`) is the natural
   generalization of `c(4) = 7/2`, reducing to the anchor at `L_t = 4`.

3. **Off-diagonal kernel vanishes identically (EXACT).** For every
   pair `i ≠ j` and every `L_t`,
   ```
   K_{ij}(L_t) = 0
   ```
   by translation-character orthogonality: the three hw=1 species
   `X_1, X_2, X_3` carry distinct joint characters
   `(-1,+1,+1), (+1,-1,+1), (+1,+1,-1)` under the three commuting lattice
   translations `(T_x, T_y, T_z)`, and each species pair disagrees on
   exactly two of those three translation generators. Pure-APBC `D`
   commutes with each `T_k`, so `(D+J)^{-1}` does as well whenever `J` is
   species-diagonal on the hw=1 triplet, and `P_i · (D+J)^{-1} · P_j`
   carries no cross-character matrix element at quadratic source-response
   order.

4. **Structural no-go theorem (EXACT).** The circulant `(a, b)` parameter
   form of `K` on the hw=1 triplet reduces to `K = a · I_3` on every
   pure-APBC `L_t` block. The spectral-amplitude vector therefore lies on
   the trivial C_3 character (`|z| = 0`), so the Koide cone
   `a_0^2 = 2 |z|^2` with `|z| > 0` is **not reachable by pure-APBC L_t
   extension alone**.

5. **Bulk L_t → ∞ limit (EXACT).** The effective denominator converges to
   ```
   lim_{L_t → ∞} c_eff(L_t) = 2 sqrt(3) ≈ 3.4641016151…
   ```
   the inverse of `(1/(2π)) ∫_0^{2π} dω / (3 + sin^2 ω) = 1 / (2 sqrt(3))`.
   This is strictly larger than 3 and strictly smaller than `7/2`, so the
   naive continuum-limit reading `c → 3` is *not* the correct asymptotic.
   The retained `c(4) = 7/2` sits 1% above the bulk value; the sequence
   `c(L_t)` is non-increasing in `L_t` and has converged to the bulk
   value to ~10 digits by `L_t = 24`.

## Table of c(L_t) and b(L_t) on pure-APBC blocks

| `L_t` | `c(L_t)` symbolic         | `c(L_t)` decimal     | `b = K_{12}` |
|------:|:--------------------------|:---------------------|:-------------|
|   4   | `7/2`                     | `3.500000000000`     | `0` (EXACT)  |
|   6   | `52/15`                   | `3.466666666667`     | `0` (EXACT)  |
|   8   | `97/28`                   | `3.464285714286`     | `0` (EXACT)  |
|  12   | `1351/390`                | `3.464102564103`     | `0` (EXACT)  |
|  16   | `18817/5432`              | `3.464101620029`     | `0` (EXACT)  |
|  24   | `3650401/1053780`         | `3.464101615138`     | `0` (EXACT)  |
|   ∞   | `2 sqrt(3)`               | `3.464101615138…`    | `0` (EXACT)  |

The `c(L_t)` column for `L_t ≥ 6` reports the harmonic-mean effective
constant `c_eff(L_t)` extracted at the massless limit; the single-pole
rewrite `K_{ii} = 4 L_t / (m_i^2 + c u_0^2)` is exact only at `L_t = 4`
where the Matsubara frequencies degenerate to a single `sin^2` value.

## Structural no-go theorem (EXACT)

> **Theorem (pure-APBC hw=1 curvature no-go).** Let `K_{ij}(L_t)` denote
> the observable-principle source-response curvature on the retained
> hw=1 triplet evaluated on any pure-APBC temporal block of length `L_t`,
> with species-diagonal sources and the framework-native staggered Dirac
> operator. Then for every pair `i ≠ j` and every `L_t ≥ 2`,
> `K_{ij}(L_t) = 0`. Consequently no pure-APBC extension of the
> observable-principle curvature kernel on the hw=1 triplet carries
> cross-species mixing; `b = 0` holds independently of `L_t`, and the
> Koide cone `a_0^2 = 2 |z|^2` (equivalently `Q = 2/3` with `|z| > 0`)
> is unreachable on the pure-APBC surface.

Proof sketch (fully symbolic in the runner): the three hw=1 species
`X_1, X_2, X_3` are joint eigenvectors of the three commuting lattice
translations `T_x, T_y, T_z` with the distinct character triples
`(-1,+1,+1), (+1,-1,+1), (+1,+1,-1)`. For any pair `i ≠ j`, at least one
translation generator `T_k` assigns `X_i` and `X_j` opposite characters
(in fact exactly two of the three do). Pure-APBC `D` and species-diagonal
`J` on the hw=1 triplet both commute with every `T_k`, so `(D+J)^{-1}`
does as well. The trace
`Tr[(D+J)^{-1} P_i (D+J)^{-1} P_j]` decomposes over translation-character
eigenspaces; with `P_i` projecting onto `chi_i` and `P_j` onto `chi_j`
and the propagator `T_k`-invariant, only `chi_i = chi_j` matrix elements
survive, which is empty for `i ≠ j`. QED.

## What this does not claim

This note does **not** claim:

- that `b = 0` in the full framework. The statement is restricted to
  **pure-APBC temporal blocks with species-diagonal sources and the
  framework-native staggered Dirac operator**. Any of the four mechanisms
  in Part B below can and will produce `b ≠ 0`, each in a specific way;

- that the Koide cone is unreachable in the full framework. The statement
  is that the cone is unreachable **by pure-APBC L_t extension alone**.
  The cone can still be reached by adding a mixing channel (two-Higgs,
  gauge exchange, Wilson/improvement, or non-APBC temporal mixing);

- any numerical match to observed charged-lepton masses, Koide Q, or
  residual mass ratios. The runner imports only framework-native
  canonical values and tests no observational quantity;

- that the Two-Higgs mechanism (Part B, Mechanism 1) succeeds or fails.
  That is the natural next attack surface for the Koide cone and is
  under active work in a separate G1 Z_3 doublet-block selector thread;
  this runner only *identifies* it as the natural extension and
  cross-references the retained atlas entries;

- that the L_t → ∞ limit of `c_eff(L_t)` is 3. The correct bulk value is
  `2 sqrt(3)`, and the runner exhibits this explicitly as a contradiction
  of the naive `c → 3` reading;

- that the bulk value `2 sqrt(3)` or the retained anchor `c(4) = 7/2`
  carries additional physical content beyond what is in the existing
  observable-principle authority. They are computed consequences of the
  Matsubara structure, not independent axioms;

- absorption of the physical-lattice axiom boundary. That remains on its
  retained note and is unaffected by this extension.

## Part B: mixing mechanisms that could produce b ≠ 0

The pure-APBC no-go in Part A identifies **translation-character
orthogonality** as the structural obstruction. Any mechanism that
produces `b ≠ 0` must either (i) break the `T`-invariance of the
resolvent, or (ii) insert a channel carrying cross-character matrix
elements between the hw=1 species. The minimal candidates, paired with
their leading-order coupling scaling, are:

**[MECH 1] Two-Higgs insertion.** Adds a scalar bilinear coupling the
hw=1 species through the Higgs sector. Leading-order off-diagonal
curvature:
```
b_Higgs  ~  y_i y_j  * <Phi_{ij}^dag Phi_{ij}>  /  (Higgs mass gap)^2    ~  y_i y_j.
```
Related to the ongoing G1 Z_3 doublet-block selector work. **Not
attacked in this runner** — see
`docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md` and
`docs/NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md`.

**[MECH 2] Retained SU(2)_L gauge-boson exchange.** The weak isospin
gauge interaction acts on the hw=1 triplet via the covariant derivative
`D_mu`. At one-gauge-boson-exchange:
```
b_gauge  ~  g_2^2  * <J_W^mu(P_i -> P_j) . J_{W mu}>  /  M_W^2       ~  g_2^2.
```
The cross-species matrix element is carried by off-diagonal isospin
currents that couple the three hw=1 Z_3 charges `(0, +1, -1)` in the
left-handed sector. Structure identified; end-to-end evaluation out of
scope of this runner.

**[MECH 3] Higher-derivative lattice operators (Wilson / improvement).**
A Wilson term `r a D^2` or clover improvement does not commute with the
individual `T_k` in general: the second-derivative structure mixes
adjacent Brillouin corners. Leading-order scaling:
```
b_Wilson  ~  r * (a / L_t)^2
```
vanishing in the continuum limit. A lattice-artifact channel, typically
tuned away in the retained framework.

**[MECH 4] Non-APBC temporal structure.** Anti-periodic boundary
conditions combined with either (a) a non-diagonal temporal hopping
matrix `M_{ij}` on the hw=1 triplet, or (b) a thermal-field-theory
modification (Matsubara plus imaginary chemical potential `mu_i` per
species), produces a cross-species propagator at quadratic order:
```
b_M   ~  M_{ij} / (m_i m_j + u_0^2 c_eff(L_t))
b_mu  ~  (mu_i - mu_j)^2 / (m^2 + u_0^2 c_eff(L_t))^2.
```
This is the closest-to-the-kernel deformation: it preserves the
source-response structure but breaks `T`-invariance of `D`.

## Cross-references

- `docs/CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md` — Agent 1's minimal-
  block first-results authority note that this extension directly
  sharpens.
- `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — retained hw=1
  algebra `M_3(C) = <P_1, P_2, P_3, C_{3[111]}>`, translation characters,
  cycle structure.
- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — unique additive
  CPT-even generator `W[J] = log|det(D+J)| - log|det D|` and the APBC
  Matsubara structure used in the diagonal kernel.
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — retained `3+1` surface on
  which every APBC block in this runner is defined.
- `docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md` — atlas
  support for Mechanism 1 (two-Higgs insertion).
- `docs/NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md` — adjacent
  two-Higgs canonical reduction structure in the neutrino sector.

## Dependency contract

This runner is self-contained at the structural level and depends on the
following retained authorities (their runners must pass before this
runner is trusted; this runner does not re-execute them, matching the
lightweight-extension scope):

- `frontier_three_generation_observable_theorem.py` — retained hw=1
  algebra, translation characters, cycle structure.
- `frontier_hierarchy_observable_principle_from_axiom.py` — unique
  additive CPT-even generator and APBC Matsubara structure.
- `frontier_anomaly_forces_time.py` — retained `3+1` surface on which
  the APBC block is defined.
- `frontier_plaquette_self_consistency.py` — canonical `u_0`,
  `<P>`, `alpha_LM` values are *not* numerically consumed here (the
  extension is symbolic in `m_i, u_0, L_t`), but the runner's
  interpretation inherits these as the retained physical scales.

No observed charged-lepton masses, quark masses, Yukawa couplings,
gauge couplings, or any fitted values are imported. All symbolic output
is framework-native.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the observable-principle
> source-response curvature on the retained hw=1 triplet, evaluated on
> any pure-APBC temporal block with species-diagonal sources, has
> vanishing off-diagonal component `K_{ij} = 0` for every `i ≠ j` and
> every block length `L_t`. The diagonal component retains a clean
> closed form `K_{ii}^{(spec)}(L_t) = 4 \sum_n 1/(m_i^2 + u_0^2
> (3 + \sin^2 \omega_n))` with APBC frequencies `\omega_n = (2n+1)\pi/L_t`,
> specializing to the retained anchor `K_{ii} = 16/(m_i^2 + (7/2) u_0^2)`
> at `L_t = 4`. In the bulk limit the effective denominator converges to
> `2\sqrt{3}` (not 3). The circulant `(a, b)` form of the kernel on the
> hw=1 triplet therefore collapses to `a \cdot I_3` on every pure-APBC
> block, and the Koide cone `a_0^2 = 2|z|^2` is unreachable by pure-APBC
> `L_t` extension alone. This is a theorem-grade negative result that
> sharpens the G5 attack surface: any mechanism producing `b \neq 0`
> must either break `T`-invariance of the resolvent or insert a
> cross-species channel (two-Higgs, SU(2)_L gauge exchange,
> Wilson/improvement, or non-APBC temporal mixing), each of which is
> identified with its leading coupling scaling but not attacked here.

## Validation

- `scripts/frontier_charged_lepton_curvature_lt_extension.py`

Current state:

- `frontier_charged_lepton_curvature_lt_extension.py`: `PASS=44`, `FAIL=0`
- `NO_GO_PURE_APBC=TRUE`

## Status

**PROPOSED** — structural no-go for the pure-APBC route recorded. The
Koide-cone attack now shifts to one of the four mixing mechanisms
enumerated in Part B. The natural next step is Mechanism 1 (two-Higgs
insertion), already under active work in the separate G1 Z_3
doublet-block selector thread; closure there would simultaneously
unblock this lane.
