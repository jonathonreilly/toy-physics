# Scalar-Selector this cycle-10 Science Review Note

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-19
**Scope:** Science audit of the this cycle to this cycle scalar-selector branch.
This note is intentionally **not** a claim-surface audit. The question here is
whether the new logic paths themselves actually close the targeted open gates.

**Later update.** A same-day meta-closure pass tightened the structural read to
`4 -> 2` at the meta-axiom layer via DIM-UNIQ + STRC. The per-gate verdict
below also changed once on the quark side: the branch still does not clear the
reviewer's object-derivation bar on three of the four gates, but the quark
lane now does. See
`docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md`.

**Later same-day quark update.** The old quark LO gap first closed on
branch-internal bimodule footing by
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`, which derived
STRC-LO from retained `a_d = Re(r)`, retained scalar/tensor collinearity, and
the framework-native BICAC split law.

**Later same-day quark closure.** The physical LO split is now derived on the
branch in two independent ways.

First, the exact `1(+)5` channel-completeness / ISSR1 route:

- `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
- `docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`

derives BICAC-LO from the exact physical `1(+)5` carrier and then sharpens
that with the ISSR1 Schur-rank-1 forcing theorem on the SO(2)-invariant
weight-0 slice.

Second, an independent support-side shell-normalization theorem:

- `docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py`

It proves that the exact bilinear carrier has unit-normalized shell columns,
that the old readout ambiguity lives only in the lower-row center dressing,
and therefore that the retained down amplitude `a_d = rho` forces the
physical LO shell law `D_LO(x) = rho x`, i.e. `kappa = 1` at LO. So
BICAC / STRC-LO is now derived from retained quark carrier normalization
rather than left as an added postulate.

**Later same-day quark strengthening.** The NORM theorems remain useful as
full-interval strengthening results:

- `docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`
- `docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`

They show that the branch already carries actual LO split laws on the
one-real imaginary channel (`NORM` existence) and that BICAC is the unique
normalized affine extension across the full ownership interval (`NORM`
naturality). But after the shell-normalization theorem, that full-interval
generality is no longer load-bearing for quark `a_u`; it is a stronger
follow-on statement, not the remaining reviewer-bar blocker.

## Executive decision table

| Path | Target gate | Science result | Does it close the gate? | Review decision |
|---|---|---|---|---|
| MRU | Koide `kappa = 2` | exact equivalence theorem plus weight-class obstruction | **No** | support theorem with explicit missing measure law |
| Berry holonomy | Koide `delta = 2/9` | old geometric route plus bundle obstruction on the actual base | **No** | obstruction theorem against current Berry closure route |
| DPLE | DM `A-BCC` / F4 lane | useful exact matrix-analysis theorem; reproduces F4 on fixed basin chart | **No** | support theorem on the open DM gate |
| STRC-LO + RPSR | quark `a_u` / Min-C lane | retained quark theorem; LO shell split now derived from exact carrier normalization | **Yes** | quark gate closed on current branch |

## 1. MRU on `Herm_circ(d)` -- Koide `kappa`

**Primary files**

- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_moment_ratio_uniformity_theorem.py`

### What scientifically holds

The note proves an exact statement:

- define the isotype moments on the Hermitian circulant algebra
  `Herm_circ(d)` using the Frobenius metric;
- impose Moment-Ratio Uniformity (MRU), meaning those moments are equal across
  `Z_d` isotypes;
- at `d = 3`, MRU is exactly equivalent to `a^2 = 2 |b|^2`, i.e.
  `kappa = 2`.

This is mathematically coherent. The runner verifies the algebraic equivalence,
the per-`d` equation counts, and the `d = 3` singlet-vs-doublet uniqueness
pattern.

A later same-day obstruction theorem sharpens the open MRU gap substantially:

- `docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_mru_weight_class_obstruction_theorem.py`

It classifies the whole weighted block-log-volume family on the same `1 ⊕ 2`
cyclic carrier and proves that every weighted leaf lands at

```text
kappa = 2 mu / nu.
```

MRU is exactly the equal-weight leaf `(mu, nu) = (1, 1)`. But the retained
unreduced determinant carrier satisfies

```text
det(alpha P_+ + beta P_perp) = alpha beta^2,
```

so it carries weights `(1, 2)` and lands at `kappa = 1`, not MRU's
`kappa = 2`. That means the current branch no longer merely “fails to derive
MRU.” It now identifies the exact missing object:

```text
a retained 1:1 real-isotype measure, or an equivalent two-slot carrier
reduction that counts the whole doublet block once.
```

### Why it does **not** close the gate

The charged-lepton gate is not merely "find any principle equivalent to
`kappa = 2`." The scientific burden is to show why the physical charged-lepton
carrier should satisfy that principle.

This branch does **not** derive MRU from:

- the retained charged-lepton carrier dynamics,
- a variational law on the physical selected line,
- a previously established operator identity,
- or an independent microscopic mechanism that forces isotype moment equality.

So the branch has not removed the missing scalar selector law. It has
**repackaged** it as MRU.

### Science decision

MRU is scientifically useful as a **support/candidate principle**:

- it gives a clean exact restatement of the remaining scalar condition;
- it shows strong `d = 3` representation-theoretic uniqueness;
- it sharpens what kind of law would be sufficient.

But it does **not** by itself close the Koide `kappa` gate.

### Operator-side framing

The operator-side `kappa = 2` primitive is now physically redundant on the
branch. Once the reviewer accepts spectrum-side closure language, the
load-bearing content is already the single Koide / MRU leaf

```text
Q = 2/3  <=>  kappa = 2  <=>  MRU at d = 3.
```

So no separate operator-side IDCS-style primitive is needed in the current
charged-lepton packet. What remains open is the measure law selecting that
leaf, not another independent operator identity.

A new same-branch reduction theorem sharpens the old open `4 x 4`
singlet/baryon route under the selected-slice scalar potential. Every
`C_3`-equivariant singlet extension Schur-reduces exactly to
`K_eff(m) = K_sel(m) - lambda(m) J` on the trivial Fourier projector
`J = 3 P_+`, so the route is no longer a generic matrix-valued correction.
It is one scalar singlet-Schur law. In the fixed-coupling subclass
(`lambda` constant), requiring the branch-local physical point `m_*` to be the
positive-branch minimum fixes one unique positive number
`lambda_* ~= 0.5456253117`. See
`docs/KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md`.

## 2. Berry holonomy on `S^2_Koide` -- Koide `delta = 2/9`

**Primary files**

- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_berry_phase_theorem.py`

### What scientifically holds

The note constructs a geometric model:

- projectivize the Koide cone to `S^2_Koide`;
- attach a nontrivial line bundle / monopole connection to the doublet sector;
- compute the holonomy over one `C_3` period;
- obtain
  `delta_d = (d - 1) / d^2`, hence `delta_3 = 2/9`.

As a geometric construction, this is coherent and the runner reproduces the
holonomy arithmetic and the `2/9` value.

A later same-day obstruction theorem changes the honest status of this lane:

- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_berry_bundle_obstruction_theorem.py`

It proves that on the **actual positive** projectivized Koide cone, the
normalized Koide locus is one-dimensional: three open arcs on the upper Koide
circle, cyclically permuted by `C_3`, so the physical quotient is an open
interval. Therefore every `C_3`-equivariant complex line bundle there is
trivial, `c_1 = 0`, and there is no gauge-invariant Berry holonomy on the
physical base.

If positivity is relaxed to the sign-relaxed projective conic, the base is
only `S^1`, so `H^2 = 0` still kills any monopole/Chern charge. The only
surviving datum there is a flat-holonomy parameter `t`, with `delta(t) = t/3`,
so `delta = 2/9` is realizable by choice (`t = 2/3`) but not forced.

### Why it does **not** close the gate

The critical scientific step is not the holonomy calculation. It is the
identification of the physical charged-lepton phase with the Berry holonomy of
this particular bundle.

The branch still assumes the load-bearing geometric input:

- a "natural" equivariant line bundle on `S^2_Koide`,
- with the relevant first Chern number `n = d - 1 = 2`,
- and with the physical charged-lepton phase read off from that holonomy.

Those are added geometric choices. They are not independently forced by the
existing charged-lepton package, and the note itself still records an open point
around the Chern-class packaging.

The new obstruction theorem goes further: on the actual positive projectivized
Koide base, the old monopole / `c_1 = 2` packaging is not merely underived. It
is **topologically unavailable**.

### Verification weakness

The companion runner is weaker than the note:

- several theorem-adjacent items are recorded as `PASS` using hard-coded `True`
  values or narrative placeholders rather than actual checks;
- in particular, equivariance, cross-lane compatibility, minimality
  compatibility, and the uniqueness of `n = 2` are not numerically or
  symbolically certified in the same way as the core holonomy arithmetic.

### Science decision

The honest read is now:

- the old Berry note is a geometric support construction on an auxiliary
  enlarged surface;
- the new bundle-obstruction theorem shows that construction does **not** live
  on the actual physical positive Koide base.

So this lane is not a closure route. It is now an **obstruction theorem
against the current Berry closure packaging** on the physical base.

## 3. DPLE on the DM pencil -- F4 / `A-BCC`

**Primary files**

- `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md`
- `scripts/frontier_dm_dple_theorem.py`

### What scientifically holds

This is the strongest new theorem in the branch.

The note establishes a genuine matrix-analysis statement:

- for a Hermitian pencil `H(t) = H_0 + t H_1`,
- `W(t) = log|det H(t)|` has at most `floor(d/2)` interior Morse-index-0
  critical points;
- at `d = 3`, that gives a clean binary selector structure;
- on the tested DM chart `(H_base, J_*)`, the `d = 3` specialization reproduces
  the previously named F4 condition on the four basins `{1, N, P, X}`.

This is real science. The runner shows:

- the degree-`d` determinant structure,
- the `floor(d/2)` upper bound numerically on sampled Hermitian pairs,
- explicit `d = 4` fragmentation,
- exact agreement with F4 on the four named basins.

### Why it does **not** close the gate

The live DM gate is not only "is F4 mathematically respectable?" The real
question is whether the physical source-side branch / chart is fixed.

DPLE acts **after** the following are already fixed:

- the use of the linear pencil `H_base + t J_*`,
- the specific basin chart `{1, N, P, X}`,
- the retained source-side ingredients that identify `H_base` and `J_*`.

So DPLE does not derive the physical source-side branch by itself. It shows
that **within that fixed chart**, the old F4 selector is the `d = 3`
specialization of a genuine theorem.

That is valuable, but it is not the same as discharging the remaining `A-BCC`
source-side input.

### Same-day source-side improvement

A later same-day theorem does tighten the DM object-derivation picture even
though it still stops short of closure:

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_local_schur_branch_discriminant_theorem_2026_04_19.py`

That theorem proves the current branch discriminator is already an exact local
scalar of the descended charged Schur block:

```text
Delta_src(dW_e^H) = det(H_e(L_e)),
```

with `H_e(L_e) = Herm(L_e^(-1))`, and shows ambient Wilson completions cannot
change the branch sign once `L_e` is fixed.

So the remaining DM gap is no longer "some unspecified source-side chart
choice." It is the finer sign law on `L_e` itself. That is real progress on
the source-side object, but the positive sign law is still not derived from
retained physics, so the gate remains open at the reviewer's bar.

An additional same-day local coordinate theorem sharpens this one step further:

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19.py`

At the constructive positive exact-closure root, the projected-source scalar
pack

```text
(eta_1, gamma, E1, E2, Delta_src)
```

already has full local rank, and on the exact-closure manifold
`eta_1 = 1` the residual `4`-pack `(gamma, E1, E2, Delta_src)` already gives
local coordinates.

So the remaining DM selector gap is now sharper still:

- not missing local observable coordinates,
- but missing a stronger **value law** on observables that already exist.

That matters because it kills the loophole that the open DM gap might still be
just a repackaging problem. The branch now knows the local projected-source
coordinates it has, and what it lacks is stronger selection content.

A third same-day theorem now upgrades the old continuity witness into an
explicit selector-law candidate:

- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py`

On the exact affine path from the aligned native seed to the explicit
constructive witness, the favored column `eta_1` crosses exact closure exactly
once and transversely. So the branch now carries a concrete path law:

```text
choose the unique eta_1 = 1 point on the aligned-seed -> constructive-witness path.
```

That selected point is constructive, positive-branch, locally observable, and
distinct from the other already-certified exact positive roots.

This is real selector science. But it is still not the reviewer's requested
object-derivation standard, because the constructive witness and the path are
explicit constructive inputs, not retained-physics outputs. So the law is now
explicit, but it is still path-chosen rather than reviewer-grade.

A fourth same-day theorem sharpens that limitation further:

- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19.py`

It proves that constructive-sign transport extremality does **not** uniquely
canonicalize the path endpoint. The branch now has at least four pairwise
distinct interior constructive witnesses with the same extremal favored-column
value

```text
eta_1 = 1.052220313052...
```

while carrying different other transport values and different projected-source
triplets. So transport extremality on the constructive sign chamber already
picks a **plateau**, not a point.

That matters because it closes the next obvious rescue route for the new path
law: even after transport is brought in, the endpoint is still not uniquely
derived. The remaining selector problem is finer than constructive transport
extremality.

A fifth same-day theorem now pushes the transport side as far as the current
branch seems to support:

- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19.py`

It proves that exact flavored transport already fixes a **canonical favored
column orbit** on the simplex,

```text
(0.0356443..., 0.0356443..., 0.9287114...)
```

up to flavor permutation. The four constructive plateau witnesses all realize
that same favored-column orbit. But the fixed native seed surface is `5`-real,
the favored column carries only `2` independent reals, and the exact
source -> favored-column Jacobian has rank `2` at the constructive witness.
So transport still leaves a local **`3`-real source fiber** unresolved above
that canonical column orbit.

That is the cleanest current-branch statement of what science remains on the
DM side. The branch no longer lacks a transport law or a transport-selected
column. It lacks the finer microscopic law on `L_e` or an equivalent retained-
physics selector that picks one source in that `3`-real fiber.

A sixth same-day theorem sharpens that residual DM object one step further:

- `docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_2026_04_19.py`

It proves that the remaining local `3`-real transport fiber is already an
explicit **spectral-invariant fiber** of the descended Hermitian response
`H_e`, hence of `L_e`. On the known constructive plateau witnesses, the two
independent favored-column coordinates carry rank `2`, while the three spectral
invariants

```text
(Tr(H_e), Tr(H_e^2), det(H_e))
```

carry rank `3` on the transport-fiber kernel, and the augmented map

```text
(col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e))
```

has full rank `5`.

So the open DM object is now sharper than “pick one source in a 3-real
family.” It is the specific task:

```text
derive a 3-scalar microscopic spectral law on H_e, equivalently on L_e.
```

### Science decision

DPLE should be treated as a **support theorem on the open DM gate**:

- stronger than a mere heuristic,
- worth preserving,
- but not a full closure of the DM selector problem.

## 4. STRC-LO + RPSR on the projector ray -- quark `a_u`

**Primary files**

- `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_strc_lo_collinearity_theorem.py`
- `docs/QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py`
- `docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bimodule_norm_existence_theorem.py`
- `docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bimodule_norm_naturality_theorem.py`
- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
- `docs/QUARK_UP_AMPLITUDE_RETAINED_NATIVE_CANDIDATE_NOTE_2026-04-19.md`
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
- `scripts/frontier_quark_up_amplitude_rpsr_conditional.py`

### What scientifically holds

This route is scientifically stronger than the earlier conditional read.

The branch isolates:

- a real structural identity for the scalar/tensor ray-magnitude bridge
  `supp = 6/7`;
- a framework-native bimodule split law **BICAC**
  (`a_u + a_d * Im(p) = Im(p)`);
- a derived LO identity
  `a_u + rho * sin(delta_std) = sin(delta_std)` from BICAC + retained
  `a_d = Re(r)` + scalar/tensor collinearity;
- a clear NLO correction `rho / 49`;
- an exact target identity for the preferred `a_u`;
- and a clean uniqueness separation among the eight Pareto candidates.

The same-day STRC-LO runner demonstrates that the old LO gap is now closed on
the branch's bimodule footing, and the RPSR runner then supplies the NLO lift:

```text
a_u / sin(delta_std) + a_d = 1 + rho / 49
```

So the branch now has a real quark theorem route to the target
`a_u = 0.7748865611`.

A same-day obstruction theorem first sharpened the old ray/support-only gap:

- `docs/QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py`

It proves that the retained packet supports the exact bridge family

```text
a_u(kappa) = sin(delta_std) * (1 - rho * kappa),
```

with three exact distinguished points already on the branch:

- `kappa_support = sqrt(6/7)`,
- `kappa_target = 48/49`,
- `kappa_BICAC = 1`.

All retained ray/support identities in that narrower packet are
`kappa`-independent, so the ray/support packet by itself does **not** force
the BICAC endpoint `kappa = 1`.

A same-day forcing theorem then closes that endpoint-selection problem on the
physical `1(+)5` carrier from retained representation theory:

- `docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_issr1_bicac_forcing.py`

It proves that Schur-rank-1 on the SO(2)-invariant weight-0 slice of `V_5`
forces

```text
a_u + a_d * sin_d = sin_d
```

at `kappa = 1`, modulo the single named JTS residue. So the route is no
longer an endpoint guess: the exact `1(+)5` carrier now has a direct forcing
theorem.

The later same-day shell-normalization theorem then adds an independent exact
carrier corroboration from the support-side route:

- `docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py`

It proves:

- exact shell columns are already the unit bright basis vectors;
- exact center columns keep the same leading slot with only lower-row
  `1/6` dressing;
- distinct admissible readout maps agree on the shell and split only on the
  center `E` lift.

So the old `kappa` ambiguity lives only in lower-row / center data, not in the
physical LO shell slot. Since the retained down amplitude is

```text
a_d = rho,
```

the physical LO down action on the shell-normalized one-real imaginary channel
must be

```text
D_LO(x) = rho x,
```

so `kappa = 1` at LO follows directly. BICAC / STRC-LO is therefore now
derived from retained quark carrier normalization, and the old endpoint
obstruction remains true only for the narrower ray/support-only subpacket.

The NORM theorems then strengthen the result rather than rescue it:

- `docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`
- `docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`

They show that LO split laws exist on the whole one-real imaginary channel and
that BICAC is the unique normalized affine extension across the full ownership
interval. But quark `a_u` no longer depends on that full-interval naturality.

### Why it now **does** clear the reviewer bar

The earlier reviewer-bar quark caveat was:

```text
derive the physical LO split without adding BICAC as a postulate.
```

The quark branch now resolves exactly that point twice. The load-bearing
closure package is:

1. exact `1(+)5` carrier completeness / ISSR1 forcing at LO;
2. independent exact shell-normalized bright-carrier corroboration;
3. retained `a_d = rho` on the common projector ray;
4. exact NLO dressing `supp * delta_A1 = 1/49`.

That is enough to derive:

```text
a_u + rho * sin(delta_std) = sin(delta_std),
a_u / sin(delta_std) + a_d = 1 + rho / 49.
```

So quark `a_u` is no longer sitting behind a reviewer-bar caveat on this
branch. What remains open on the quark side is only the stronger full-interval
NORM story and the broader bimodule amplitude-completeness target, not the
gate itself.

### Science decision

The honest current read is:

- **retained quark theorem:** yes, via exact shell-normalized LO split plus
  RPSR NLO dressing;
- **same-day strengthening:** BICAC is also the unique normalized affine
  extension of the LO split law on the full ownership interval;
- **reviewer-bar retained derivation:** yes on the quark lane.

So this lane should now be treated as a **real retained quark theorem**, not
merely a conditional or bimodule-postulate route.

## 5. Net science conclusion

This branch does contain meaningful science. The new logic paths do **not**
all collapse under scrutiny. But three of the four gates remain open.

The right scientific read is:

1. **MRU**: exact restatement of the remaining Koide scalar law, not a closure.
2. **Berry**: the old geometric support model exists, but the current physical
   Berry-bundle packaging is obstructed on the actual positive Koide base.
3. **DPLE**: real support theorem that upgrades the old F4 selector story, but
   does not eliminate the remaining DM source-side open input, now sharpened
   to a 3-scalar spectral law on `H_e/L_e`.
4. **STRC-LO + RPSR**: quark `a_u` is now a retained theorem. The exact
   shell-normalized carrier fixes `kappa = 1` at LO, and the retained
   `rho/49` dressing supplies the NLO target.

So the branch is **not** a clean "all four gates are closed" science packet.
It is a mixed packet with one genuine retained closure and three still-open
gates.

It is a **mixed packet** containing:

- one strong DM support theorem (DPLE),
- one retained quark theorem (shell-normalized LO split + STRC-LO + RPSR),
- one charged-lepton support theorem with an explicit missing measure law
  (MRU),
- and one charged-lepton obstruction theorem against the current Berry closure
  packaging.

## 6. Salvage recommendation

If this branch is mined selectively, the scientifically worth-preserving pieces
are:

- `DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
  as a support theorem on the open DM gate;
- `STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
  plus `QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
  plus `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  plus `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  as the retained quark packet;
- `KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  and `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
  as infrastructure/support notes if their closure language is demoted.

What is **not** justified by this branch:

- claiming the charged-lepton Koide gate is now scientifically closed;
- claiming the DM flagship lane is now closed through DPLE;
- claiming total scalar-selector axiom cost is now zero.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_berry_phase_theorem_note_2026-04-19](KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md)
- [dm_dple_dimension_parametric_extremum_theorem_note_2026-04-19](DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md)
- [strc_lo_collinearity_theorem_note_2026-04-19](STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md)
- [quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19](QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md)
