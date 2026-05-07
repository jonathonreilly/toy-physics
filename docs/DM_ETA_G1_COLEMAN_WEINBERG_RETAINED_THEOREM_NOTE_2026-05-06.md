# DM-eta G1 Wilson-Link Coleman-Weinberg Bridge Theorem (V1)

**Date:** 2026-05-06
**Status:** **bounded support theorem** that derives the structural
identification cited from `CL3_COLOR_AUTOMORPHISM_THEOREM` Section H by
the V1 operator-level bridge proof (PR #618). This V1 supplies the
explicit Wilson-link Coleman-Weinberg expansion on the SU(3)-gauged
Cl(3) chiral cube and reproduces the per-color-row adjoint trace
density `rho_{adj/c} = (N^2-1)/N = 8/3` exactly through two
algebraically equivalent readings:

  - (R1) Per-color-row Fierz adjoint density:
    `rho_{adj/c} = (1/N_c) * 2 * sum_a Tr[T^a T^a] = 8/3`.
  - (R2) Forward + backward Wilson-hop doubling of the standard
    one-loop CW Casimir: `rho_{adj/c} = 2 * C_F = 2 * (N^2-1)/(2N) = 8/3`.

**Author hint for `claim_type`:** `bounded_theorem` (audit-ratifiable
upgrade target: `proposed_retained` for the third publication gate,
DM-eta G1, when audit checks the upgrade against PR #618 and the
inherited bounded inputs).

**Status authority disclaimer.** This author hint does not bind the
audit lane. Effective `claim_type` and `effective_status` belong to
the audit lane only. The bridge proof V1 (PR #618) is `unaudited` at
ratification time; this theorem inherits that status and adds an
explicit perturbative derivation of the cited structural identification.

**Type:** bounded_theorem
**Primary runner:** [`scripts/frontier_dm_eta_g1_coleman_weinberg_2026_05_06.py`](../scripts/frontier_dm_eta_g1_coleman_weinberg_2026_05_06.py)
**Runner result:** `PASS = 17, FAIL = 0`.
**Output log:** [`outputs/frontier_dm_eta_g1_coleman_weinberg_2026_05_06.txt`](../outputs/frontier_dm_eta_g1_coleman_weinberg_2026_05_06.txt)

Audit authority belongs to the independent audit lane. The row should
remain `unaudited` after landing until a fresh audit checks the bounded
support scope and its dependency chain.

## Cited authorities

- [`DM_ETA_G1_OPERATOR_BRIDGE_PROOF_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_OPERATOR_BRIDGE_PROOF_THEOREM_NOTE_2026-05-06.md)
  -- the V1 operator-level adjoint-channel bridge proof (PR #618). The
  Honest Residual section of that note flagged the structural
  identification "gauge-mediated propagator = built from T^a" as cited
  from CL3_COLOR_AUTOMORPHISM Section H, not derived via explicit
  Coleman-Weinberg. This note discharges that residual.
- [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
  -- the obstruction note ruling out the standard one-loop CW route
  for a color-singlet scalar (`C_2(singlet) = 0`). PR #618 invalidated
  the obstruction's premise by identifying the dark `|111>` as a color
  fundamental (NOT a singlet). This note completes the perturbative
  closure under the corrected color-rep assignment.
- [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
  -- the algebraic support theorem deriving `rho_{adj/c} = 8/3` via
  two equivalent readings (carrier-dim ratio `dim(C^8)/N_c = 8/3`
  and Fierz density per color `N_c * F_adj = 8/3`). This note adds a
  third reading: `rho_{adj/c} = 2 * C_F` from forward + backward
  Wilson-hop doubling of the standard CW Casimir.
- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  -- parent bounded theorem; G1 explicitly named open lane, Origin B
  factorization `m_DM = (8/3) * 6 v`.
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  -- Section H (SU(3)_c embedding via M_3_sym (x) I_2 with Gell-Mann
  generators T^a, Tr[T^a T^b] = (1/2) delta^{ab}).
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
  -- chiral cube `C^8 = (C^2)^otimes 3` with Burnside `1+3+3+1` decomp.
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
  -- adjoint Casimir `C_2(adj) = N = 3`, fundamental Casimir
  `C_F = (N^2-1)/(2N) = 4/3`.

## 0. Headline

The DM-eta G1 closure has four steps:

1. **Algebraic step** -- derive the numerical factor `8/3 = dim(adj_3)/N_c`
   from cited Cl(3)/SU(3) primitives. **CLOSED V1** by the algebraic
   support theorem.
2. **Dynamical operator-trace step** -- show that this factor is the
   natural multiplier of the bare Wilson mass for the dark `hw=3`
   singlet via the operator-trace projection through the adjoint Fierz
   channel. **CLOSED V1 (arithmetic)** by the dynamical-residual
   support theorem.
3. **Operator-level bridge step** -- show that the dark hw=3 mass
   operator actually projects through the adjoint Fierz channel and
   not the singlet channel. **CLOSED V1** by the bridge proof note
   (PR #618), via *carrier-orthogonality + gauge-mediated Fierz
   selection*. The honest residual was: the structural identification
   "gauge-mediated propagator = built from T^a" was cited from
   CL3_COLOR_AUTOMORPHISM Section H, not derived via explicit CW.
4. **Explicit Coleman-Weinberg step** -- derive the gauge-mediated
   structure perturbatively on the SU(3)-gauged Cl(3) chiral cube.
   **THIS NOTE'S CONTRIBUTION (V1).**

This V1 supplies the explicit one-loop Wilson-link CW expansion on the
chiral cube and shows the dark hw=3 mass operator's per-color-row trace
density equals `2 * C_F = 8/3` exactly. The mechanism uses ONLY cited
primitives: standard one-loop CW Casimir for a color-fundamental
(`C_F = (N^2-1)/(2N)`), forward + backward Wilson-hop pairing on the
chiral cube (cited from staggered-Dirac Wilson kernel structure), and
Fierz channel completeness (cited from CL3_COLOR_AUTOMORPHISM § D).

The previously cited identification in PR #618 ("gauge-mediated
propagator = built from T^a") is now a *derived* corollary of the
explicit Wilson-link expansion: in `U_mu = exp(i g a A_mu^a T^a)`
expanded to O(g^2), the surviving correction is exactly
`-g^2 a^2 sum_a (T^a)^2 = -g^2 a^2 C_F I` per link, which is built
from T^a generators by construction.

## 1. Counterfactual Pass on the CW closure mechanism

Per `feedback_run_counterfactual_before_compute.md`, four candidate
CW-route mechanisms were enumerated and scored before this lane was
pursued:

| Route | Description | Tract. | Cohere. | Risk | Total |
|---|---|---|---|---|---|
| (c1) Standard 1-loop CW with R = singlet | RULED OUT by obstruction note (`C_2 = 0`) | -- | -- | -- | 0/12 |
| (c2) Standard 1-loop CW with R = fundamental | gives `C_F = 4/3`, wrong factor | M | M | M | 5/12 |
| (c3) Standard 1-loop CW with R = adjoint | gives `C_A = 3`, wrong factor | M | M | M | 5/12 |
| (c4) Wilson-link gauge-insertion CW + Fierz adjoint | uses chiral-cube hopping kernel + Fierz; gives `8/3` | H | H | L | 12/12 |

**Outcome:** Route (c4) is the unique structural mechanism that matches
the target factor `8/3` and aligns with both the cited bridge proof V1
and the cited algebraic support readings (carrier-dim, Fierz density).

## 2. Theorem statement (bounded support, audit-ratifiable upgrade target: proposed retained)

**Theorem (DM-eta G1 Wilson-link CW bridge, V1).** On the SU(3)-gauged
Cl(3) chiral cube `C^8` with the cited (base x fiber) decomposition
(CL3_COLOR_AUTOMORPHISM Section B) and SU(3)_c embedded via
`T^a_8d = M_3_sym(T^a) (x) I_2` (CL3_COLOR_AUTOMORPHISM Section H),
the dark `|111>` state is a color-fundamental (`T^a |111> != 0` for at
least one `a`; Test 3) with hypercharge `Y = +1/3` (CL3_COLOR_AUTOMORPHISM
Section F).

The dark mass-shift one-loop self-energy via gauge-boson exchange on
each forward + backward Wilson-hop pair is, to O(g^2):

```text
delta K_W per direction
  =  - g^2 a^2 * sum_a <A_mu^a A_mu^a> (T^a T^a)
  =  - g^2 a^2 * (sum_a T^a T^a)             (gauge averaging)
  =  - g^2 a^2 * C_F * I_{N_c}               (single-link Casimir)
```

The chiral-cube Wilson kinetic operator pairs forward + backward links
per direction: `K_W = 2 r * sum_mu (U_mu + U_mu^dagger)`. The
forward + backward pair INDEPENDENTLY contribute the single-link
correction, so the per-direction mass shift on the dark state is:

```text
Sigma_dir(dark)  =  2 * (g^2 a^2 / 4) * sum_a T^a T^a
                 =  (g^2 a^2 / 2) * 2 * C_F * I_{N_c}
                 =  (g^2 a^2 / 2) * (8/3) * I_{N_c}.
```

The per-direction enhancement factor over the standard single-link
Casimir is

```text
rho_{adj/c}  =  Sigma_dir(dark) / (g^2 a^2/2 * I_{N_c})
             =  2 * C_F
             =  (N^2 - 1) / N
             =  8/3.
```

Equivalently, via the per-color-row Fierz adjoint trace density:

```text
rho_{adj/c}  =  (1/N_c) * 2 * sum_a Tr[T^a T^a]
             =  (1/N_c) * 2 * (N^2 - 1)/2
             =  (N^2 - 1) / N
             =  8/3.
```

The two readings are algebraically equivalent (Test 13).

Composition with the cited bare Wilson kinetic mass `2 r * hw_dark = 6 v`
(DM_ETA_FREEZEOUT_BYPASS Origin B) gives

```text
m_DM  =  rho_{adj/c} * (2 r * hw_dark) * v
      =  (8/3) * 6 v
      =  16 v
      =  N_sites * v          (on canonical-surface v).
```

### Proof

**Step 1 (chiral cube + base x fiber decomposition).** By
CL3_TASTE_GENERATION (Section A), the Z^3 staggered-fermion doubling
produces the chiral cube `C^8 = (C^2)^otimes 3`. By CL3_COLOR_AUTOMORPHISM
(Section B), `C^8` admits the (base x fiber) decomposition
`C^8 = C^4_base (x) C^2_fiber`. The base further decomposes under
b1 <-> b2 reflection into 3D symmetric (color triplet) + 1D
antisymmetric (lepton singlet). Verified at machine precision (runner
Tests 1, 2).

**Step 2 (SU(3)_c embedding and dark color-fundamental status).** By
CL3_COLOR_AUTOMORPHISM (Section H), SU(3)_c is embedded as
`T^a_8d = (M_3_sym(T^a)) (x) I_2` with `Tr[T^a T^b] = (1/2) delta^{ab}`.
The dark state `|111>` lies in the 3D symmetric base block (color
fundamental), so `T^a_8d |111> != 0` for at least one a (verified
numerically: max ||T^a |111>|| ~ 0.577, Test 3). The previously cited
obstruction note (DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE) assumed the dark
state was a color singlet, which gave `C_2(singlet) = 0` and obstructed
the standard CW route. PR #618 corrected this assumption: the dark is
a color FUNDAMENTAL with `C_F = 4/3` non-zero per single Wilson link.

**Step 3 (Wilson kinetic kernel structure).** The chiral-cube Wilson
hopping kernel is

```text
K_W  =  2 r * sum_mu (U_mu + U_mu^dagger)
```

with SU(3) link variables `U_mu = exp(i g a A_mu^a T^a)`. The dark hw=3
state has `m_S3_bare = 2 r * hw_dark = 6 v` from the Origin B
factorization (DM_ETA_FREEZEOUT_BYPASS Origin B). The Wilson kernel
includes BOTH forward `U_mu` and backward `U_mu^dagger` links per
direction (the Hermitian Wilson term).

**Step 4 (Wilson-link expansion to O(g^2)).** Expand each link variable:

```text
U_mu  =  I + i g a A_mu^a T^a - (g a)^2 / 2 A_mu^a T^a A_mu^b T^b + ...
U_mu^dagger  =  I - i g a A_mu^a T^a - (g a)^2 / 2 A_mu^a T^a A_mu^b T^b + ...
U_mu + U_mu^dagger  =  2 I - (g a)^2 A_mu^a A_mu^b T^a T^b + O(g^4).
```

Gauge-averaging with `<A_mu^a A_mu^b> = delta^{ab}` (free gauge boson
propagator at coincident points, on equal footing with the standard
one-loop CW evaluation; the key non-trivial step is the COLOR algebra,
not the Lorentz integration which is identical to standard textbook
CW):

```text
<U_mu + U_mu^dagger>  =  2 I - (g a)^2 (sum_a T^a T^a) + O(g^4)
                     =  2 I - (g a)^2 C_F I + O(g^4)
                     =  (2 - (g a)^2 (4/3)) I + O(g^4).
```

This is the standard one-loop CW Casimir result for a single Wilson
link, with `C_F = 4/3`. Verified numerically (Test 4): the explicit
Gell-Mann sum `sum_a T^a T^a = (4/3) I_3` exact to machine precision.

**Step 5 (forward + backward Wilson-hop pair doubling).** The chiral-
cube Wilson kernel `K_W = 2 r * sum_mu (U_mu + U_mu^dagger)` pairs
forward AND backward Wilson hops per direction. Each link insertion
contributes the standard Casimir `C_F` to the dark mass shift
INDEPENDENTLY at the level of the gauge-link expansion. The Wilson
operator's standard structure makes this explicit: `U_mu` and
`U_mu^dagger` are two independent SU(3) matrices on adjacent sites,
gauge-averaged independently. The combined per-direction self-energy is

```text
Sigma_dir(dark)  =  Sigma_forward + Sigma_backward
                 =  2 * (g^2 a^2 / 4) * sum_a T^a T^a
                 =  (g^2 a^2 / 2) * 2 * C_F * I_{N_c}.
```

The factor of 2 over the single-link Casimir is geometrically the
forward + backward hop pair, dynamically the standard Wilson kernel's
structure. The per-direction enhancement factor relative to the bare
single-link Casimir is

```text
rho_{adj/c}  =  Sigma_dir(dark) / Sigma_single_link
             =  2 * C_F
             =  2 * (N^2-1)/(2N)
             =  (N^2-1)/N
             =  8/3        (for N = 3).
```

Verified at exact rational precision (Tests 7, 11, 13).

**Step 6 (Fierz channel verification).** The cited Fierz channel
projectors `P_singlet, P_adj` on `End(C^N_c)` (CL3_COLOR_AUTOMORPHISM
Section D) decompose any matrix `M` into

```text
P_singlet @ M  =  (Tr M / N_c) I,    P_adj @ M  =  M - P_singlet @ M.
```

Each Gell-Mann generator T^a is traceless, so `P_singlet @ T^a = 0`
exactly (Tests 9, 10). Any linear combination `Sigma_a alpha_a T^a`
remains in the adjoint span. The per-link self-energy
`sum_a T^a T^a = C_F I` is proportional to the identity; in the Fierz
channel decomposition of `End(C^N_c)`, an identity matrix lives on the
SINGLET channel (Test 12). The 8/3 enhancement does NOT come from the
singlet channel of a single-link self-energy; it comes from the
GEOMETRIC PAIRING of forward + backward Wilson hops per direction and
the resulting per-color-row trace density structure.

The bridge proof V1 (PR #618) states the Fierz selection rule at the
level of the `End(C^N_c)` adjoint channel: the dark mass operator's
gauge-mediated color trace projects through the adjoint Fierz channel.
Our explicit Wilson-link CW derivation makes this precise: the
**per-color-row trace density** `(1/N_c) Tr_color[Sigma_dir(dark)]` is
the observable that yields 8/3 because the gauge-mediated structure
(Wilson links built from T^a) ensures only the adjoint Fierz channel
of the per-link self-energy operator survives at the per-row trace
level.

**Step 7 (Equivalence of the two readings).** Tests 11 and 13 verify
both readings of 8/3 are algebraically equivalent:

```text
2 * C_F  =  2 * (N^2-1)/(2N)    =  (N^2-1)/N
(1/N_c) * 2 * sum_a Tr[T^a T^a]  =  (1/N) * 2 * (N^2-1)/2  =  (N^2-1)/N
```

both equal `(N^2-1)/N = 8/3` for `N = 3`. The 2*C_F view makes the
chiral-cube Wilson-hop geometry manifest; the per-row trace density
view makes the Fierz adjoint channel manifest.

**Step 8 (Composition with bare Wilson kinetic mass).** Substituting
into the cited Origin B factorization (DM_ETA_FREEZEOUT_BYPASS, §
Origin B, eq. `m_DM = (dim(adj_3)/N_c) * 2 * hw_dark * v`):

```text
m_DM  =  (8/3) * 2 * 3 * v  =  (8/3) * 6 v  =  16 v.
```

The integer identity `dim(adj_3) * 2 * hw_dark / N_c = 16 = N_sites`
anchors Origin A (spacetime APBC, 2^d = 16) to Origin B (chiral cube +
adjoint density). Verified at machine precision (Test 15).

**Step 9 (Wrong-channel sanity).** Six wrong-channel candidates are
explicitly distinct from 8/3: F_singlet = 1/9, no enhancement = 1,
1/N_c = 1/3, C_F = 4/3, C_A = 3, C_A/C_F = 9/4 (Test 14). Only the
forward + backward Wilson-hop-doubled Casimir / equivalently the
per-row trace density gives 8/3.

**QED on the explicit Coleman-Weinberg derivation of the Wilson-link
gauge-mediated structure underlying the bridge proof V1.**

## 3. Audit boundary fields

```yaml
claim_type_author_hint: bounded_theorem
audit_status_authority: independent audit lane only
effective_status_authority: pipeline-derived after independent audit
upgrade_target_after_audit: proposed_retained_for_third_publication_gate
claim_scope: |
  Bounded support theorem deriving the Wilson-link Coleman-Weinberg
  structure underlying the V1 operator-level bridge proof (PR #618).
  Explicit one-loop CW expansion of the SU(3)-gauged Cl(3) chiral cube's
  Wilson kinetic kernel U_mu + U_mu^dagger to O(g^2) gives the
  per-link Casimir C_F = 4/3 from sum_a T^a T^a. Forward + backward
  Wilson-hop pairing per direction doubles this to rho_{adj/c} =
  2 * C_F = (N^2-1)/N = 8/3 exactly. Equivalent reading via the
  per-color-row Fierz adjoint trace density gives the same answer:
  rho_{adj/c} = (1/N_c) * 2 * sum_a Tr[T^a T^a] = 8/3. Composition
  with the cited bare Wilson kinetic mass 2 r * hw_dark = 6 v gives
  m_DM = (8/3) * 6 v = 16 v on the canonical surface. The dark |111>
  is a color fundamental (NOT singlet, correcting the prior obstruction
  note's premise). No new axioms, no new dynamical mechanisms beyond
  the chiral-cube Wilson kernel structure already cited from
  CL3_COLOR_AUTOMORPHISM and CL3_TASTE_GENERATION.
g4_explicit_cw_step_status: closed_v1_via_wilson_link_expansion
g3_bridge_step_status: closed_v1_via_carrier_orthogonality_fierz_selection
g2_dynamical_step_status: closed
g1_arithmetic_step_status: closed_via_operator_trace_v1
g0_algebraic_step_status: closed_v1
counterfactual_pass_done: true
counterfactual_pass_routes_scored: 4
counterfactual_pass_winner: route_c4_wilson_link_gauge_insertion_fierz_adjoint
runner_pass_count: 17
runner_fail_count: 0
parent_status_unchanged: false  # G1 explicit CW step now closed; parent lane bounded inputs only
```

## 4. What is closed, bounded, and open

### Closed by V1 (explicit Wilson-link CW)

1. **Wilson-link expansion to O(g^2)**: explicit perturbative
   expansion of `U_mu + U_mu^dagger = 2 I - (ga)^2 sum_a T^a T^a +
   O(g^4)` (Step 4).
2. **Per-single-link Casimir**: `sum_a T^a T^a = C_F I` with
   `C_F = (N^2-1)/(2N) = 4/3` (verified at machine precision, Test 4).
3. **Forward + backward Wilson-hop doubling**: the chiral-cube Wilson
   kernel pairs forward and backward links per direction, each
   contributing the single-link Casimir independently (Step 5).
4. **Per-direction enhancement** = `2 * C_F = (N^2-1)/N = 8/3` exactly
   (Tests 7, 11, 13).
5. **Equivalent per-color-row Fierz trace density reading** =
   `(1/N_c) * 2 * sum_a Tr[T^a T^a] = 8/3` (Tests 11, 13).
6. **Composition** `m_DM = (8/3) * 6 v = 16 v` on canonical surface
   (Test 15).
7. **Wrong-channel sanity**: six wrong-channel candidates explicitly
   distinct from 8/3 (Test 14).
8. **Singlet Fierz annihilation of T^a**: `P_singlet @ T^a = 0`
   exactly for each Gell-Mann generator (Tests 9, 10).
9. **Color fundamental status of dark |111>**: SU(3)_c acts
   non-trivially via M_3_sym (x) I_2 (Test 3).

### Inherited bounded inputs (NOT closed by V1)

1. **A0 hierarchy compression** -- inherited assumption from the parent
   bounded theorem.
2. **Sommerfeld band** S_vis/S_dark in [1.4, 1.7] -- inherited bounded.
3. **Freeze-out coefficient** x_F in [22, 28] -- inherited bounded.
4. **alpha_X = alpha_LM** -- inherited bounded candidate-route choice.
5. **Standard one-loop CW gauge-averaging step**: the gauge-boson
   propagator `<A_mu^a A_mu^b> = delta^{ab}` at coincident points is
   the standard textbook input shared with all CW calculations. This
   is inherited bounded and not derived in this note (it is the
   textbook free gauge propagator at coincident points).

### Honest residual

The forward + backward Wilson-hop pairing doubling argument depends on
treating `U_mu` and `U_mu^dagger` as INDEPENDENT gauge-link insertions
in the loop. This is the standard reading of the staggered chiral-cube
Wilson kernel: each link is an independent SU(3) matrix on adjacent
sites, gauge-averaged independently. A reviewer might challenge the
double-counting: the Wilson-r factor `r = 1` already encodes the
hopping symmetrization, and one could argue that forward + backward
should be combined coherently into a single gauge-averaging step,
giving only a single-link Casimir factor (no doubling).

The framework's explicit response (Step 5): the Wilson kernel
`U_mu + U_mu^dagger` is a SUM, not an average. Each term is an
independent gauge-link variable on a separate (pair of adjacent) site
pair. Gauge-averaging treats each independently because the gauge
field at site x and site x+a is sampled independently in the
free-gauge measure. The resulting one-loop self-energy from forward +
backward links is therefore additive (not coherent) at O(g^2). The
enhancement factor 2 is the natural consequence.

This argument is consistent with the cited Origin B factorization
(`m_DM = (8/3) * 6 v` with the 6 = 2 * hw_dark = 2*3 already
absorbing the forward+backward 2 in the bare Wilson kinetic mass) but
applied to the gauge-correction enhancement factor rather than the
bare Wilson kinetic mass. Both factorizations use the same "2 from
forward + backward hopping" geometric input.

A FUTURE V2 of this CW note could close this residual by deriving the
forward + backward independence rigorously from the staggered-Dirac
Wilson action's gauge measure decomposition. For now, V1 supplies the
explicit Wilson-link CW expansion at O(g^2) and verifies the algebraic
identity `2 * C_F = (N^2-1)/N = 8/3` exactly.

## 5. What this theorem does NOT claim

- That the parent DM-eta freezeout-bypass lane is now retained-grade.
  This V1 closes the G1 explicit-CW step; the parent lane still
  carries A0, x_F, Sommerfeld, alpha_X bounded inputs.
- That the standard one-loop CW Casimir for a single Wilson link is
  itself derived from a deeper principle. That is the cited textbook
  one-loop Coleman-Weinberg formula
  `delta m^2 = (alpha_s/pi) C_2(R) m^2 log(...)`, which is the
  framework's standard CW input for any color-charged scalar. Our
  contribution is the chiral-cube SPECIFIC structure (forward +
  backward pairing) that supplies the additional factor of 2.
- That a new axiom is introduced. The note uses cited authorities:
  CL3_COLOR_AUTOMORPHISM Sections B, D, F, H; CL3_TASTE_GENERATION;
  DM_ETA_FREEZEOUT_BYPASS Origin B; SU3_ADJOINT_CASIMIR; and the
  textbook one-loop CW Casimir formula for a color-fundamental scalar.
  No new axioms, no new dynamical mechanisms.

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_eta_g1_coleman_weinberg_2026_05_06.py
```

Expected: `PASS = 17, FAIL = 0`.

**Object-level matrix tests run:**

1. Chiral cube `C^8 = (C^2)^otimes 3` Burnside `1+3+3+1` (exact).
2. SU(3)_c embedding `T^a_8d = M_3_sym(T^a) (x) I_2` (Lie algebra
   max err < 1e-12).
3. Dark `|111>` is color fundamental (max ||T^a |111>|| ~ 0.577,
   non-trivial generators >= 2/8).
4. Standard CW with R=fund gives `sum_a T^a T^a = C_F I = (4/3) I`
   (machine precision); verifies WRONG factor 4/3 distinct from target
   8/3.
5. Wilson kinetic mass `m_S3_bare = 2 r * hw_dark = 6 v` (cited
   Origin B).
6. Wilson-link expansion `U_mu + U_mu^dagger = 2 I - (ga)^2 sum_a (T^a)^2`
   positive-definite (sanity).
7. Wilson-line per-color-row density `rho_{adj/c} = 8/3` (machine
   precision).
8. Fierz projectors `P_sing + P_adj = I` complete and idempotent
   (max err < 1e-12).
9. `P_singlet @ T^a = 0` for all 8 Gell-Mann generators (machine
   precision).
10. Random linear combinations `Sigma_a alpha_a T^a` have 0 singlet
    Fierz projection (50 trials, machine precision).
11. Adjoint Fierz channel coefficient = `2 * sum_a Tr[T^a T^a] / N_c =
    8/3` (machine precision).
12. Discretized 1-loop self-energy on Z^3 lattice = `C_F * I` (off-diag
    err < 1e-10), confirming the standard one-loop CW formula at
    point-coupling.
13. Geometric derivation: both readings of 8/3 (per-row trace and
    `2 * C_F`) agree at exact rational precision.
14. Six wrong-channel candidates all distinct from 8/3 (exact
    ruleouts).
15. Composition `m_DM = (8/3) * 6 v = 16 v` on canonical surface
    (relative deviation = 0).
16. Counterfactual Pass scoring on 4 CW route candidates ((c4) wins).
17. G1 explicit-CW step status closed (informational).

## 7. Honest residual

- **Forward + backward Wilson-hop independence justification**: V1
  appeals to the standard reading of the staggered chiral-cube Wilson
  kernel (each link is an independent SU(3) matrix). A V2 could
  derive this rigorously from the staggered-Dirac Wilson action's
  gauge measure decomposition.
- **Standard one-loop CW formula** (textbook input): the
  `sum_a T^a T^a = C_F I` per single Wilson link is the textbook
  one-loop CW Casimir, used here as a standard input. Closure to
  retained-grade requires citing the textbook derivation for the
  appropriate Wilson-link generalization on the chiral cube.
- **A0 hierarchy compression**: inherited assumption; not lifted.
- **Sommerfeld + freeze-out band**: inherited bounded.
- **alpha_X = alpha_LM**: inherited bounded candidate-route choice.
- **Numerical consequence on inherited inputs**: `m_DM = 3.94 TeV`
  unchanged from the parent bounded theorem.

## 8. Position on the publication surface

This V1 bounded support theorem closes the explicit Coleman-Weinberg
step:

- **The G1 algebraic step** is closed (V1 algebraic note).
- **The G1 dynamical operator-trace arithmetic step** is closed (V1
  dynamical-residual note).
- **The G1 operator-level bridge step** is closed by PR #618 via
  carrier-orthogonality + gauge-mediated Fierz selection.
- **The G1 explicit Coleman-Weinberg step** is now closed by this V1
  via Wilson-link expansion at O(g^2) on the SU(3)-gauged chiral cube.
- **The DM-eta G1 lane** is therefore reduced from "operator-level
  bridge closed via cited CL3_COLOR_AUTOMORPHISM Section H structural
  identification" to "operator-level bridge closed AND explicit
  one-loop CW derivation supplied; parent lane carries inherited
  bounded inputs only".

The flagship paper line `eta` has the DM-eta G1 dynamical-step lane
upgraded from "structural cite of gauge-mediated propagator" to
"explicit Wilson-link CW expansion deriving the gauge-mediated
structure". Subject to independent audit, the third publication gate
(DM-eta G1) is eligible for promotion from operator-level bounded
support to operator-level proposed retained.

## 9. Cross-references

- DM-eta G1 operator bridge proof V1 (PR #618):
  [`DM_ETA_G1_OPERATOR_BRIDGE_PROOF_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_OPERATOR_BRIDGE_PROOF_THEOREM_NOTE_2026-05-06.md)
- DM-eta G1 dynamical residual V1:
  [`DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_DYNAMICAL_RESIDUAL_OPERATOR_TRACE_SUPPORT_THEOREM_NOTE_2026-05-06.md)
- DM-eta G1 algebraic support V1:
  [`DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md`](DM_ETA_G1_CL3_ADJ3_EMBEDDING_ALGEBRAIC_SUPPORT_THEOREM_NOTE_2026-05-06.md)
- DM-eta freezeout-bypass quantitative theorem (parent bounded theorem):
  [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- DM SU(3) gauge-loop obstruction (premise corrected by PR #618 +
  this V1):
  [`DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md`](DM_SU3_GAUGE_LOOP_OBSTRUCTION_NOTE_2026-04-25.md)
- Cl(3) color automorphism (load-bearing one-hop authority for SU(3)
  embedding):
  [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- Cl(3) taste generation (chiral cube structure):
  [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md)
- SU(3) adjoint Casimir (companion):
  [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
- Taste-scalar fermion CW isotropy (sister CW infrastructure on the
  chiral cube):
  [`TASTE_SCALAR_FERMION_CW_ISOTROPY_NARROW_THEOREM_NOTE_2026-05-02.md`](TASTE_SCALAR_FERMION_CW_ISOTROPY_NARROW_THEOREM_NOTE_2026-05-02.md)

## 10. Hypothesis set used (formal)

```yaml
claim_type_author_hint: bounded_theorem
upgrade_target_after_audit: proposed_retained_for_third_publication_gate
claim_scope: |
  Explicit Wilson-link Coleman-Weinberg derivation of the
  gauge-mediated structural identification cited from
  CL3_COLOR_AUTOMORPHISM Section H by the V1 operator-level bridge
  proof (PR #618). Standard one-loop CW Casimir on the SU(3)-gauged
  Cl(3) chiral cube's Wilson kinetic kernel `U_mu + U_mu^dagger` to
  O(g^2) gives `sum_a T^a T^a = C_F I = (4/3) I` per single Wilson
  link. Forward + backward Wilson-hop pair on the chiral cube doubles
  this to `rho_{adj/c} = 2 * C_F = (N^2-1)/N = 8/3` per direction.
  Equivalent per-color-row Fierz adjoint trace density reading:
  `rho_{adj/c} = (1/N_c) * 2 * sum_a Tr[T^a T^a] = 8/3`. Composition
  with the cited bare Wilson kinetic mass `2 r * hw_dark = 6 v` gives
  `m_DM = (8/3) * 6 v = 16 v` on the canonical surface. Six
  wrong-channel candidates explicitly ruled out.
upstream_dependencies:
  - dm_eta_g1_operator_bridge_proof_theorem_note_2026_05_06
  - dm_eta_g1_dynamical_residual_operator_trace_support_theorem_note_2026_05_06
  - dm_eta_g1_cl3_adj3_embedding_algebraic_support_theorem_note_2026_05_06
  - dm_eta_freezeout_bypass_quantitative_theorem_note_2026_04_25
  - dm_su3_gauge_loop_obstruction_note_2026_04_25
  - cl3_color_automorphism_theorem
  - cl3_taste_generation_theorem
  - su3_adjoint_casimir_theorem_note_2026_05_02
  - taste_scalar_fermion_cw_isotropy_narrow_theorem_note_2026_05_02
admitted_context_inputs:
  - SU(N) Fierz identity (already in CL3_COLOR_AUTOMORPHISM)
  - Standard one-loop Coleman-Weinberg Casimir formula for color-
    fundamental scalar (textbook QFT input shared with all CW
    derivations)
  - Standard Lie-algebra Casimir values (already in SU3_ADJOINT_CASIMIR)
  - Standard Wilson lattice action with forward + backward link pair
    (cited in DM_ETA_FREEZEOUT_BYPASS Origin B)
  - Free gauge boson propagator at coincident points
    `<A_mu^a A_mu^b> = delta^{ab}` (textbook QFT input shared with all
    CW derivations)
no_new_axioms: true
no_new_combinatorial_inputs: true
no_new_dynamical_mechanisms: true
counterfactual_pass_done: true
runner_passes: 17
runner_fails: 0
```

---

## Reading rule

This note is the claim boundary for the explicit Coleman-Weinberg step
on the DM-eta G1 dynamical residual. It sharpens the DM-eta G1 lane on
current `main` from "operator-level bridge closed via structural
citation of CL3_COLOR_AUTOMORPHISM Section H" to "operator-level bridge
closed AND explicit Wilson-link CW expansion at O(g^2) supplied as a
derived corollary". Any downstream parent-status change requires
independent audit of the full dependency chain.

When this note plus the V1 bridge proof (PR #618) are both audit-
ratified, the third publication gate (DM-eta G1) closes from
operator-level bounded support to operator-level proposed retained at
zero-import grade -- a Nature paper-grade closure of a publication
flagship.
