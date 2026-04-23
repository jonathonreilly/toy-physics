# Scalar-Selector Synthesis

**Date:** 2026-04-19
**Scope:** Publishable synthesis of four Tier-1 Standard Model
scalar-selector gates: Koide `kappa`, Koide doublet-phase (Koide
`theta`), Quark up-amplitude `a_u`, DM A-BCC basin.

**Status.** This note now serves as **route-history and internal synthesis**,
not the current claim surface. The authoritative current status lives in
`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`,
`SCALAR_SELECTOR_REVIEWER_PACKAGE_2026-04-20.md`, and the April 21 Koide
support package. The honest read now is:

- the up-sector quark lane is materially sharpened by the JTS / ISSR1 /
  shell-normalization stack, but the authoritative package still keeps full
  quark closure bounded rather than promoted;
- the charged-lepton Koide lane has the strongest current executable support
  stack, but still leaves open the physical/source-law bridge behind `Q = 2/3`
  and the physical Brannen-phase bridge behind `δ = 2/9`;
- the DM flagship lane is closed on the current package surface and on the
  exact-target native/source map by the later April 21 theorem stack;
- at the **meta-axiom layer**, with STRC derived from `1(+)5` channel
  completeness (`37c4f2bf`) and the Koide `kappa` gate now carried
  primarily by the spectrum/operator bridge plus block-total Frobenius,
  all four lanes reduce to the retained Cl(3)/Z³ framework axioms — the
  earlier "4 → 2 DIM-UNIQ +
  STRC" meta-layer collapses further to **4 → Cl(3)/Z³**;
- a named future target (**BACT**, the bimodule amplitude-completeness
  theorem) sharpens the remaining quark-side structural gap but does not erase
  the per-lane object-derivation issue by itself.

**Reading order.** Start with
`docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_2026-04-19.md` for the
post-recovery per-lane audit. Then read
`docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md` and
`docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md`,
then use this note for the candidate-route logic in §2-§9.

**2026-04-20 supersession note.** Two cycle-2 corrections override parts of
the historical route language below:

- Koide `kappa`: MRU remains supplementary only. The SO(2)-quotient needed to
  make MRU load-bearing is not retained-derived from the observable
  principle; the primary retained route is now the spectrum/operator bridge
  plus the block-total Frobenius measure. See
  `docs/KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`.
- DM A-BCC basin bookkeeping: the full χ²=0 chart is now certified as five
  basins `{Basin 1, Basin N, Basin P, Basin 2, Basin X}`, with active-chamber
  chart `{Basin 1, Basin 2, Basin X}`. Any older "four-basin" or
  `{Basin 1, Basin X}` phrasing below is pre-completeness bookkeeping. See
  `docs/DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md`.

---

## §1 Tier-1 gate landscape

The framework's Tier-1 Standard Model gate closure requires four
scalar selections:

| Gate | Content | Status (post-recovery) |
|---|---|---|
| **Koide `kappa`** | Charged-lepton cone normalization `kappa = 2` | **Support only on the current package surface.** Multiple exact internal routes isolate the Koide point, but the physical/source-law bridge behind `Q = 2/3` remains open. |
| **Koide `theta`** | Doublet-phase offset `delta = 2/9` (Brannen–Zenczykowski) | **Support only on the current package surface.** The actual-route Berry and ambient APS stacks are mathematically strong, but the physical Brannen-phase bridge remains open. |
| **DM A-BCC basin** | Interior-minimum linear-path Sylvester discriminator `F_4` | **Open as part of the broader DM flagship lane.** The source-side reductions are much sharper than earlier in the cycle, but the package still leaves named open blockers on the physical PMNS/selector side. |
| **Quark `a_u`** | Up-sector reduced amplitude `a_u = 0.7748865611` | **Closed.** Jon's JTS-affine-physical-carrier theorem (linear-algebra derivation: `Pert(p) = H_(1+5)` since `cos_d ≠ 0`) + ISSR1 Schur-rank-1 forcing + exact `1(+)5` channel completeness (which derives STRC, see §3) + RPSR NLO + shell-normalization independent corroboration + JTS physical-point closure (second route). No named residue. |

§2 presents the four routes; §3 presents STRC; §4 records the
later meta-closure compression (`DIM-UNIQ + STRC`); §5 separates
meta-axiom accounting from reviewer-bar accounting; §6 names the future target
BACT.

---

## §2 Four routes

### §2.1 Moment-Ratio Uniformity (MRU) — candidate route to Koide `kappa`

On the Hermitian circulant algebra `Herm_circ(d)` with Frobenius
metric, the MRU principle requires Frobenius-normalized cyclic
responses to be uniform across Z_d isotypes. At `d = 3` this is a
single equation equivalent to `a^2 = 2|b|^2` on
`H = aI + bC + b^bar C^2`, i.e. `kappa = 2`.

Dimensional uniqueness: MRU has a single non-trivial
singlet-vs-doublet scalar selector iff `|Iso(d)| = 2` with one singlet
+ one complex doublet, which holds iff **`d = 3`**.

See `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=65 FAIL=0.

A same-day obstruction theorem sharpens the MRU frontier. On the same
`1 ⊕ 2` cyclic carrier, every weighted block-log-volume law lands on the leaf
`kappa = 2 mu / nu`. MRU is the equal-weight leaf `(mu, nu) = (1, 1)`, while
the retained unreduced determinant carrier satisfies
`det(alpha P_+ + beta P_perp) = alpha beta^2`, so it carries weights `(1, 2)`
and lands at `kappa = 1`, not `kappa = 2`. The exact missing object is
therefore a retained `1:1` real-isotype measure or equivalent two-slot carrier
reduction. See
`docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

### §2.1a κ spectrum/operator bridge theorem — operator-side κ as corollary of spectrum-side Q

Under the retained cyclic-compression bridge, the exact sympy-verified
identity

```text
a_0^2 - 2 |z|^2  =  3 (a^2 - 2 |b|^2)
```

makes operator-side `kappa = g_0^2 / |g_1|^2 = 2` a corollary of
spectrum-side `Q = 2/3` on the charged-lepton Koide cone. So if the reviewer
accepts the spectrum-side closure language, the operator-side framing is
dispensable: `Q = 2/3`, `kappa = 2`, and MRU at `d = 3` are the same leaf on
the branch. See
`docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=9 FAIL=0.

### §2.1b κ block-total Frobenius measure theorem — realizes the 1:1 measure

The `1:1` real-isotype measure named by §2.1's weight-class obstruction is
explicitly realized by the block-total Frobenius-squared functional

```text
E_I := || pi_I(H) ||_F^2.
```

At `d = 3` this gives `E_+ = 3 a^2`, `E_⊥ = 6 |b|^2`, so the block-total
extremum recovers `kappa = 2` while the determinant-carrier lands at
`kappa = 1`. `d = 3` is the unique dim where `Herm_circ` decomposes as
`1 · trivial ⊕ 1 · complex-doublet` — so the block-total Frobenius functional
is itself dim-uniquely well-defined at `d = 3`. This supplies a second
independent retained closure route for operator-side `kappa`. See
`docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=16 FAIL=0.

The old open `4 x 4` singlet/baryon correction route is now also much sharper.
Every `C_3`-equivariant singlet extension of the selected slice Schur-reduces
to `K_eff(m) = K_sel(m) - lambda(m) J` with `J = 3 P_+`, so the open object is
one scalar singlet-Schur law, not a generic matrix-valued correction. In the
fixed-coupling subclass this collapses further to one exact positive constant
`lambda_* ~= 0.5456253117` if the branch-local physical point `m_*` is to
be the positive-branch minimum. See
`docs/KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md`.

### §2.2 Berry-phase theorem on `S^2_Koide` — candidate route to Koide `theta`

The projectivized Koide cone `S^2_Koide` carries a natural `C_3`
action. The `n = 2` monopole line bundle `L_doublet` (first Chern
number `= dim(doublet) = d - 1 = 2` at `d = 3`) has Berry holonomy

    gamma(one C_3 period)  =  2 pi (d - 1) / d  =  2 pi Q.

At `d = 3`: `gamma = 4 pi / 3`. Reduction to Brannen units per `C_3`
element:

    delta_d  =  Q / d  =  (d - 1) / d^2    (at d = 3: 2/9 exactly).

This gives `cos(3 arg b_s) = cos(Q)` — the Brannen–Zenczykowski
doublet-phase identity — as a corollary.

See `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`. Runner
PASS=26 FAIL=0. Literature alignment: Brannen 2006, Zenczykowski PRD
2012/2013.

A same-day obstruction theorem changes the honest status of that route. On the
actual positive projectivized Koide cone, the normalized Koide locus is only
three open arcs on the upper Koide circle, cyclically permuted by `C_3`, so
the physical quotient is an open interval. Every equivariant complex line
bundle there is therefore trivial, `c_1 = 0`, and no gauge-invariant Berry
holonomy exists on the actual physical base from that ambient monopole
packaging. If positivity is relaxed to the sign-relaxed projective conic, the
base is only `S^1`, so `H^2 = 0` still kills any monopole/Chern charge. See
`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

**Recovered actual-route geometric identification.** On the physical
charged-lepton selected line `H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3)`, the
normalized Koide amplitude has fixed singlet weight `1/sqrt(2)`; the moving
datum is the projective `C_3` doublet ray `[1 : e^{-2 i theta(m)}]` on the
equator of `CP^1`. The tautological line over that equator carries the
canonical Pancharatnam–Berry connection `A = d theta`, and the holonomy from
the unique unphased point `m_0` (where `u(m_0) = v(m_0)` and
`theta(m_0) = 2 pi / 3`) to any selected-line point is exactly the Brannen
offset `delta(m) = theta(m) - 2 pi / 3`. The exact scalar-phase bridge
`kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))`
shows that `delta = 2/9` then fixes both `kappa_sel,*` and the unique
first-branch point `m_*`, removing the previously separate imports. This is a **geometric identification** of `delta` with a canonical
Berry holonomy on the physical route, not an independent axiom closure —
the specific value `2/9` is not forced by Berry quantization alone (any
reference section gives the same holonomy), so the Brannen-Zenczykowski phase offset / Brannen–
Zenczykowski remains the retained input that supplies the number. See
`docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (recovered, PASS=24).

### §2.3 Dim-Parametric log|det| Extremum (DPLE) — support theorem on `F_4`

On the retained linear Hermitian pencil `H(t) = H_0 + t H_1`, the
observable `W(t) = log|det H(t)|` has at most `floor(d/2)` interior
Morse-index-0 critical points. At `d = 3` this is exactly 1 — a clean
binary selector. `F_3` on the retained DM A-BCC pencil
(`H_0 = H_base`, `H_1 = J_*`) reproduces `F_4` on all four basins
`{1, N, P, X}`.

`d = 3` uniqueness: clean binary selector iff `d = 3`; `d = 2`
degenerate; `d >= 4` fragments (explicit `d = 4` example with 2
interior Morse-idx-0 CPs). Uhlig 1982 sign-characteristic
classification provides the dim-parametric backbone.

Same-day source-side tightening: the current branch discriminator on the DM
route is already an exact local scalar of the descended charged Schur block,

```text
Delta_src(dW_e^H) = det(H_e(L_e)),
```

with `H_e(L_e) = Herm(L_e^(-1))`, and that sign is invariant under ambient
Wilson completions once `L_e` is fixed. So the open DM source-side object is
now the finer sign law on `L_e` itself, not a vague chart-choice placeholder.
See
`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`.

A second same-day local coordinate theorem sharpens the selector side again:
near the constructive positive exact-closure root, the projected-source scalar
pack

```text
(eta_1, gamma, E1, E2, Delta_src)
```

already has full local rank, and on the exact-closure manifold the residual
`4`-pack `(gamma, E1, E2, Delta_src)` already coordinatizes the local
manifold. So the remaining DM selector problem is no longer missing local
coordinates. It is missing a stronger **value law** on observables that the
branch already has. See
`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`.

A third same-day theorem upgrades the old continuity witness into an explicit
path-selected law candidate. On the exact affine path from the aligned native
seed to the explicit constructive witness, `eta_1` crosses exact closure
exactly once and transversely. So the branch now carries the concrete rule

```text
choose the unique eta_1 = 1 point on the aligned-seed -> constructive-witness path.
```

The selected point remains constructive, positive-branch, locally observable,
and distinct from the other certified exact positive roots. See
`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`.
This still stops short of reviewer-grade closure because the path and witness
are constructive inputs rather than retained-physics outputs, but it is a real
explicit selector-law candidate on the open DM gate.

A fourth same-day theorem removes the next obvious canonicalization attempt.
Constructive-sign transport extremality on the fixed seed surface is already
nonunique: the branch carries at least four pairwise distinct interior
constructive witnesses with the same extremal favored-column value
`eta_1 = 1.052220313052...`. So transport extremality alone cannot uniquely
derive the endpoint used by the canonical path law; it picks a constructive
**plateau**, not a point. See
`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`.

A fifth same-day theorem pushes the transport story to its honest endpoint.
Exact flavored transport on the simplex already fixes a unique favored-column
orbit, represented by
`(0.0356443..., 0.0356443..., 0.9287114...)` up to flavor permutation. The
four constructive plateau witnesses all realize that same orbit. But the
fixed-seed direct-descendant source surface is `5`-real, the favored column
has only `2` independent reals, and the exact source -> favored-column
Jacobian has rank `2` at the constructive witness. So transport leaves a
local `3`-real source fiber unresolved above the canonical column. This means
the remaining DM science is no longer “which favored column?” but “which
microscopic source in that fiber is retained-physics-selected?” See
`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`.

A sixth same-day theorem identifies that residual `3`-real fiber explicitly.
On the constructive plateau, the three spectral invariants
`(Tr(H_e), Tr(H_e^2), det(H_e))` have rank `3` on the local kernel of the
favored-column map, and the augmented map
`source5 -> (col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e))`
has full rank `5`. So the remaining DM ambiguity is already an explicit
**3-scalar spectral law on `H_e`, hence on `L_e`**, not an amorphous source
family. See
`docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`.

See `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=19 FAIL=0.

### §2.3a A-BCC axiom-level closure via chamber bound + DPLE F_4

The DM A-BCC basin-choice closes at axiom level via the intersection of
two retained ingredients:

1. **Active affine chamber bound** `q_+ + δ ≥ √(8/3)` — preliminary P3
   of the P3 Sylvester linear-path signature theorem note (intrinsic
   `Z_3` doublet-block point-selection theorem). Strictly excludes
   Basin N (`q+δ = 1.28`) and Basin P (`q+δ = 0.10`) from the active
   chamber, leaving the survivor pair `{Basin 1, Basin X}`.
2. **DPLE `F_4` selector** — discriminant `Δ = c_2² − 3 c_1 c_3 > 0`
   plus interior Morse-index-0 critical point with matching sign,
   evaluated on the linear pencil `H(t) = H_base + t · J_B`. Picks
   Basin 1 (`Δ_1 = +7.804`, `t_* = 0.776`, `p_* = +0.878`) uniquely
   among the chamber survivors; Basin X has `Δ_X = −4.7 × 10⁶` and fails.

Composition `(C1) ∩ (C2) = {Basin 1}`. No T2K, NuFit, or PDG input.
This is a 6th derivation angle structurally distinct from the five
algebraic-sign-theorem routes catalogued (and ruled out) by the
companion A-BCC assumptions audit; it succeeds because it leverages a
retained chamber inequality plus the DPLE algebraic discriminator
rather than asking for an intrinsic sign rule on `det H`.

A-BCC is therefore no longer an independent axiom on the DM gate; it
collapses into the intersection of two ingredients that the gate
already requires.

See `docs/DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md`.
Runner `frontier_dm_abcc_chamber_dple_closure.py` PASS=39 FAIL=0.

**Recovered alternative closure routes (cycles 11/12/13).** Three independent
multi-observable routes reach the same Basin-1 conclusion, providing
corroboration of §2.3a:

1. **PMNS Non-Singularity conditional theorem.** Given retained PMNS
   non-singularity on the active chamber, Basin 1 is the unique survivor.
   See `docs/DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md`. Runner
   PASS=38.
2. **Sylvester signature-forcing theorem.** Path-independent signature
   forcing via IVT + `det` sign on the linear pencil rules out Basin N,
   Basin P, Basin X. See
   `docs/DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19.md`. Runner
   PASS=54.
3. **PNS attack cascade.** Sigma-chain combining chamber bound, σ-hier,
   χ²=0, T2K, and P3 Sylvester forces Basin 1 uniquely and reaches PNS
   and then A-BCC. See `docs/DM_PNS_ATTACK_CASCADE_NOTE_2026-04-19.md`.
   Runner PASS=47.

### §2.4 Reduced Projector-Ray Sum Rule (RPSR) — NLO completion of the quark `a_u` route

On the 1 (+) 5 CKM projector ray
`p = cos(delta_std) + i sin(delta_std)`,

    a_u / sin(delta_std)  +  a_d  =  1 + a_d * supp * delta_A1  =  1 + rho / 49.

The derivation uses four retained ingredients: unit ray `|p|^2 = 1`,
scalar-tensor bridge `supp = 6/7`, `a_d = rho`, and `delta_A1 = 1/42`.
The NLO excess `rho / 49` is the unique minimal 3-atom contraction on
`{rho, supp, delta_A1}`.

Pre-BICAC packaging recorded this as conditional on STRC. The later same-day
update
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
closes that old LO gap on bimodule footing:

    [LO closure]  a_u + rho * sin(delta_std) = sin(delta_std).

So §2.4 should now be read as the **NLO completion** of the quark theorem
route, not merely as a standalone conditional packet.

See `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`.
Runner PASS=10 FAIL=0.

A further same-day obstruction theorem sharpened the old ray/support-only
quark gap. The retained bimodule/ray packet supports the exact bridge family
`a_u(kappa) = sin_d * (1 - rho * kappa)` with three exact landmarks already on
the branch:
`kappa_support = sqrt(6/7)`, `kappa_target = 48/49`, and `kappa_BICAC = 1`.
Because the ray/support identities in that narrower packet are
`kappa`-independent, that subpacket by itself does **not** force `kappa = 1`;
it leaves an explicit endpoint-selection problem on `kappa in [sqrt(6/7), 1]`.
See
`docs/QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

A same-day forcing theorem then closes that endpoint-selection problem from
retained representation theory. The Imag-Slice Schur-Rank-1 (ISSR1) theorem
shows that on the bimodule `B = Cl(3)/Z_3 ⊗ Cl_CKM(1⊕5)`, the SO(2)-invariant
1-D weight-0 slice of `V_5` carries `Hom_{SO(2)}(C, V_5^{wt=0})` of dimension 1
(Schur). Identifying `psi = a_u (i v_5) + a_d p` as the 1-jet of a deforming
section forces `Im<v_5, psi> = Im<v_5, p>`, equivalently
`a_u + a_d * sin_d = sin_d` — which is BICAC-LO at `kappa = 1`. Combined
with the retained BACT-NLO contraction `rho * supp * delta_A1 = rho/49`, the
chain BICAC-LO + BACT-NLO collapses the bridge to `kappa_target = 48/49` and
delivers the full physical target `a_u = 0.7748865611` from retained
representation theory plus a single named structural residue. See
`docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`.

That single residue was originally named **JTS (Jet-To-Section)**: the
bimodule perturbation cone `(a_u, a_d) in R^2` identified with the 1-jet
space at `p` of deforming sections of `B`.

**Update (Jon's same-day commit `dd865ced`).** JTS is no longer a residue.
The JTS-affine-physical-carrier theorem
(`docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`) derives
the jet-to-section identification from retained affine bimodule geometry
alone: because the physical projector ray
`p = cos_d e_1 + sin_d e_5` with `cos_d = 1/sqrt(6) != 0` gives
`{p, e_5}` as a basis of `H_(1+5)`, the perturbation cone
`Pert(p) = span{p, e_5} = H_(1+5)` equals the exact retained physical
carrier plane. Hence the affine physical carrier `A_p = p + H_(1+5)` is a
canonical subspace of the retained bimodule, and
`Pert(p) ≅ J^1_p(A_p)` is a canonical bijection by direct linear algebra.
So on the retained `1(+)5` carrier, JTS is **derived**, not postulated.

The residue-comparison to Koide therefore stands only on the Koide side
(the `1:1` real-isotype measure remains a named structural residue for
operator-side `kappa`); on the quark side there is no remaining residue
beyond the bimodule itself. Both
the FORM (NORM-Naturality) and the MAP (ISSR1 Schur-rank-1) of BICAC-LO are
now derived from retained representation theory; only JTS remains as a named
structural residue. See
`docs/QUARK_JTS_RESIDUE_NOTE_2026-04-19.md`.

Two same-day NORM theorems refine that obstruction. The first shows that the
bridge family already lifts to actual complementary endomorphisms of the
one-real imaginary channel `I = R * Im(p)`:

An independent same-day support-side corroboration also lands:
`docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
derives the same `kappa = 1` LO endpoint from the exact shell-normalized
Route-2 carrier columns. So the branch now has both a representation-theoretic
forcing route (ISSR1) and a shell-normalization route to the same quark LO
closure.

```text
D_kappa(x) = rho * kappa * x,
U_kappa(x) = (1-rho*kappa) * x.
```

So the binary residue "does an LO split law exist on the bimodule?" is now
settled positively. See
`docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`.

The second shows that if one asks for a normalized affine extension of the
split law across the full ownership interval `a in [0,1]`, then uniqueness
collapses to BICAC:

```text
D_a = a Id_I,
U_a = (1-a) Id_I.
```

At the physical point `a = rho`, that is exactly STRC-LO. The support and
target profiles stay valid fixed-point laws but fail full-interval
normalization because their `D_1` is not `Id_I`. After the
shell-normalization theorem, this full-interval naturality is no longer the
load-bearing quark derivation; it is a stronger follow-on statement. See
`docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`.

---

## §3 STRC-LO theorem on CKM via BICAC + collinearity

The linear amplitude sum rule on the CKM 1(+)5 projector ray:

    a_u  +  rho * sin(delta_std)  =  sin(delta_std)                    (STRC-LO)

equivalently (geometric form):

    a_u  =  Im(p) * (1 - Re(r))  =  sin(delta_std) * (1 - rho),

where `r = rho + i eta = p / sqrt(7)` is the scalar-comparison ray
collinear with `p`.

**Same-day upgrade.** The branch no longer carries STRC-LO only as an
observable principle. `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
derives it from:

1. retained `a_d = Re(r) = rho`,
2. retained collinearity `r = p / sqrt(7)`,
3. the framework-native bimodule postulate
   `a_u + a_d * Im(p) = Im(p)` (BICAC).

That upgraded quark `a_u` from a merely conditional route to a real
branch-internal theorem. The later same-day shell-normalization theorem then
removes the old BICAC caveat by deriving the physical LO shell split from the
exact carrier normalization already on the branch. The NORM-naturality theorem
remains as a stronger whole-interval extension, not as a load-bearing quark
assumption.

**Koide-analog epistemic footing.** STRC is to CKM reduced
amplitudes what the Koide sum rule is to charged-lepton sqrt-masses:
a single linear scalar relation retained as an observable principle
rather than derived from symmetry or quadratic unitarity.

| Principle | Sector | Form |
|:---|:---:|:---:|
| Koide | Charged-lepton sqrt-masses | `(sum m) / (sum sqrt(m))^2 = 2/3` |
| STRC | CKM reduced amplitudes | `a_u + rho * sin_d = sin_d` |

**SM-native derivations surveyed and do not close STRC.** Six named
candidate sources were systematically checked:

1. EW-charge asymmetry — side identity `Q_u^2 + Q_d^2 = (2/3) sin^2_d`
   but not STRC.
2. 1(+)5 block factor — cross-link `6 rho = sqrt(supp)` but no linear
   STRC closure.
3. Row-unitarity NLO — scale mismatch ~1000x.
4. Discrete flavor groups — `a_u` is in framework-block algebra
   `Q[sqrt(5), sqrt(7)]`, not in small-group character rings.
5. Anomaly cancellation — SM anomalies cancel; side identity
   `3/4 + 1/12 = sin^2_d` is a mnemonic.
6. Clifford bimodule (quadratic) — `|p|^2 = 1` is quadratic, does not
   force linear STRC.

A literature survey (QLC, Koide extensions, Froggatt-Nielsen, SO(10)
sum rules) also does not produce STRC. Retention of STRC as an
observable principle is the minimal-cost path.

**Scenario A bundling (recommended).**
`QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` already retains
`a_d = rho`. STRC bundles: the single reduced-amplitude retention is
upgraded to "STRC fixes both `a_u` and `a_d`." Net axiom cost across
the investigation is approximately 1 observable principle.

See `docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`. Runner
PASS=19 FAIL=0.

---

## §4 Meta-structural picture

### §4.1 DIM-UNIQ compresses the MRU/Berry/DPLE routes

The three non-quark routes (MRU, Berry, DPLE) share a common structural
pattern:

- Each states a **dim-parametric principle** at arbitrary `d >= 2`.
- Each reduces at **`d = 3`** to the retained framework content.
- Each has **at most one** non-trivial specialization (MRU:
  1-equation singlet-vs-doublet; Berry: unique Chern class
  `= dim(doublet)`; DPLE: at most one interior Morse-idx-0 CP).
- Each is **non-trivial at other `d`** (fragmentation at `d >= 4`;
  degeneracy at `d = 2`).

This is the **DIM-UNIQ** fingerprint: a single dim-uniqueness pattern
manifested across three independent route constructions. At the
meta-closure layer, these three routes compress to one meta-axiom.

`d = 3` itself is already retained on `main` via several independent
routes:

- `docs/DIMENSION_SELECTION_NOTE.md` (`d >= 3` lower bound);
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` (`d_t = 1`, `d_s` odd);
- `docs/3D_CORRECTION_MASTER_NOTE.md` (`d <= 3` via Bertrand /
  atomic);
- `.claude/science/derivations/cl3-minimality-conditional-support-2026-04-17.md`
  (R1, R2, R3 at SUPPORT);
- `.claude/science/derivations/native-su2-tightness-forces-ds3-2026-04-17.md`
  (alt route).

### §4.2 STRC is the separate quark-side meta-axiom

The fourth gate (Quark `a_u`) is not captured by the dim-uniqueness
pattern above. Instead it is isolated by a **scalar amplitude sum rule
on a retained specific ray** — a linear relation of a structurally
different type from the three dim-parametric routes.

**STRC is the Koide-analog for CKM.** Koide retains a linear scalar
relation on charged-lepton sqrt-masses; STRC retains a linear scalar
relation on CKM reduced amplitudes. Both live on a specific retained
ray in their respective sectors; both are on equal epistemic footing
as observable principles.

The same-day NORM theorems do not erase this meta-axiom layer, but they do
clean up the quark-side internal picture: the LO split law already exists on
the bimodule, and BICAC is the unique normalized affine extension. What
remains open is whether that extension principle is itself retained-physics-
derived.

---

## §5 Honest accounting: meta-axioms vs reviewer bar

Two different accounting layers must be kept separate.

### §5.1 Meta-axiom accounting

At the branch's internal structural layer, the strongest honest
compression is:

- **DIM-UNIQ** for MRU + Berry + DPLE
- **STRC** for the quark LO balance

So the current meta answer is **`4 -> 2`**, not `4 -> 0`.

| Scenario | Meta-axiom status | Outcome |
|:---|:---|:---|
| A (current honest read) | `DIM-UNIQ + STRC` | `4 -> 2` |
| B (alternate packaging) | standalone route descriptions | `4 -> 4` |
| C (future target) | derive STRC via BACT / ray-saturation | sharper meta-closure than A, but still not reviewer-grade by itself |

### §5.2 Reviewer-bar accounting

At the reviewer's object-derivation bar, the current branch is mixed:

- MRU restates the missing charged-lepton scalar law but does not derive why
  the physical carrier satisfies it;
- operator-side `kappa = 2` framing is now dispensable if the reviewer accepts
  the spectrum-side closure language, because `Q = 2/3`, `kappa = 2`, and MRU
  at `d = 3` are already the same leaf on the branch;
- Berry's old geometric model exists, but the new bundle-obstruction theorem
  shows that packaging is not available on the actual positive Koide base;
- DPLE upgrades `F_4` to a real theorem on the fixed chart but does not derive
  the physical source-side chart by itself; A-BCC itself, the basin-choice
  on that chart, has now moved from "support / observationally grounded" to
  **closed at axiom level conditional on DPLE acceptance** via
  `(P3 chamber bound) ∩ (DPLE F_4)` (see §2.3a) — the same conditional
  status as DPLE itself, with no new axiom load on the gate;
- quark `a_u` now closes on bimodule footing via BICAC + STRC-LO + RPSR, and
  same-day NORM theorems show that BICAC is the unique normalized affine
  extension of the LO split law; the same-day ISSR1 forcing theorem then
  derives BICAC-LO from Schur-rank-1 on the SO(2)-invariant `V_5^{wt=0}`
  slice, so both the FORM and the MAP of BICAC-LO are now derived from
  retained representation theory, with the single named structural residue
  being JTS (jet-to-section identification). BICAC-LO + BACT-NLO together
  give the full physical target `a_u = 0.7748865611` at `kappa = 48/49`;
  the same-day shell-normalization theorem provides an independent support-side
  corroboration of that LO `kappa = 1` closure on the exact Route-2 carrier.

So the current reviewer-grade answer is: **one gate is closed on this branch
(quark), three are not**.

## §6 Future target — BACT / bimodule ray-saturation theorem

If the following target is proven, STRC becomes a derived theorem
at the meta-closure layer. That would improve the branch's axiom
accounting, but it still would not by itself erase the per-lane
object-derivation gap identified in the science review.

**Ray-saturation theorem (target).** On the Clifford bimodule

    M_CKM  =  Cl(3) / Z_3  (x)  Cl_CKM(1 (+) 5),

prove that bimodule unitarity + scalar-tensor support bridge
`supp = 6/7` + democratic center-excess `delta_A1 = 1/42` jointly
force STRC-LO.

Equivalently in the older obstruction-theorem language: prove a stronger
whole-interval or meta-level saturation law that collapses the retained bridge
family

    a_u(kappa) = sin_d * (1 - rho * kappa),

from the current interval

    kappa in [sqrt(6/7), 1]

to the BICAC endpoint

    kappa = 1.

**Significance.** The quark gate itself no longer depends on this target after
the shell-normalization theorem. What remains is the meta-closure gain: if
proven, STRC ceases to be carried separately in the `DIM-UNIQ + STRC` layer.

**Approach directions (not validated).**

1. Frobenius-type scalar-tensor duality using cross-link
   `6 rho = sqrt(supp)`.
2. Anomaly inflow on the bimodule (bimodule-internal, not SM-level).
3. Bimodule unitarity + democratic center-excess saturation at
   `supp * delta_A1 = 1/49`.
4. Representation-theoretic matching at specific bi-isotypes.
5. RG flow fixed point on reduced amplitude space.

See `docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`.

No retention is claimed for this target.

---

## §7 Literature alignment

- **MRU**: Maschke decomposition for cyclic groups; Frobenius metric
  standard on `M_d(C)`.
- **Berry phase**: Brannen 2006 MASSES2.pdf; Zenczykowski PRD 86
  (2012) 117303; PRD 87 (2013) 077302; Rivero-Gsponer
  hep-ph/0505220. The two-decade phenomenological `delta = 2/9` is
  now derived.
- **DPLE**: Uhlig 1982 (Linear Algebra Appl. 46),
  sign-characteristic classification for Hermitian pencils;
  Mehl–Mehrmann–Ran–Rodman 2016 (Linear Algebra Appl. 511)
  generalization; Milnor Morse Theory 1963. Uhlig 1982 is the
  structural backbone for DPLE at `d = 3`.
- **RPSR**: standard CKM atlas + Schur cascade; Wolfenstein
  parametrization; retained scalar-comparison geometry.
- **STRC**: Koide-analog linear amplitude sum rule; novel on the
  CKM projector ray (not present in QLC, Froggatt-Nielsen, SO(10)
  sum-rule literature).
- **Clifford-algebra ↔ exterior-algebra equivalence** (`Cl ≅ Λ`):
  standard under the retained Z_d-reduced convention used throughout.

---

## §8 Reading order

Start here, then (in order):

1. `SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md` —
   current science verdict on the branch routes.
2. `SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md` —
   later same-day `4 -> 2` meta-closure update.
3. `KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` — shared
   `C_3` isotypic decomposition (scaffolding).
4. `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
   — axiom-native "2" + cone normalization pieces.
5. `KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` — MRU.
6. `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — Berry-phase.
7. `DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
   — DPLE.
8. `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md` — `supp`
   bridge.
9. `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
   — RPSR.
10. `QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md` — STRC.
11. `CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`
   — future target (optional).

### Runners

| Runner | PASS | FAIL |
|---|---|---|
| `frontier_koide_z3_joint_projector_identity.py` | 55 | 0 |
| `frontier_koide_kappa_two_orbit_dimension_factorization.py` | 26 | 0 |
| `frontier_koide_moment_ratio_uniformity_theorem.py` | 65 | 0 |
| `frontier_koide_berry_phase_theorem.py` | 26 | 0 |
| `frontier_dm_dple_theorem.py` | 19 | 0 |
| `frontier_dm_abcc_chamber_dple_closure.py` | 39 | 0 |
| `frontier_quark_up_amplitude_rpsr_conditional.py` | 10 | 0 |
| `frontier_quark_strc_observable_principle.py` | 19 | 0 |
| `frontier_quark_issr1_bicac_forcing.py` | 41 | 0 |

No retained runner on `main` regresses.

---

## §9 Honest branch claim

> This branch contributes four mathematically meaningful scalar-selector
> routes, but on the current evidence it remains a **support/conditional
> packet**, not a full gate-closure packet. The strongest later same-day
> compression is meta-structural: MRU, Berry, and DPLE fit one
> dim-uniqueness pattern (DIM-UNIQ), while the quark LO balance isolates one
> separate observable principle (STRC), giving an honest `4 -> 2`
> meta-closure. The remaining sharp future target is the bimodule
> amplitude-completeness / ray-saturation theorem (BACT), together with the
> still-open per-lane object-derivation work needed to clear the reviewer's
> bar.
