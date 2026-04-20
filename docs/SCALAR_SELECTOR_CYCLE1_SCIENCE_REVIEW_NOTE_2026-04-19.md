# Scalar-Selector Cycle 1-10 Science Review Note

**Date:** 2026-04-19
**Scope:** Science audit of the cycle-1 to cycle-10 scalar-selector branch.
This note is intentionally **not** a claim-surface audit. The question here is
whether the new logic paths themselves actually close the targeted open gates.

**Later update.** A same-day meta-closure pass tightened the structural read to
`4 -> 2` at the meta-axiom layer via DIM-UNIQ + STRC, but it did **not**
change the per-gate scientific verdict below: the branch still does not clear
the reviewer's object-derivation bar on any of the four gates. See
`docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md`.

**Later same-day quark update.** The old quark LO gap is now closed on
branch-internal bimodule footing by
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`, which derives
STRC-LO from retained `a_d = Re(r)`, the retained scalar/tensor collinearity,
and the framework-native BICAC postulate. That strengthens the quark lane
substantially, but it still does not remove the reviewer-bar issue because
BICAC is an added bimodule structural postulate rather than a derivation from
the previously retained quark physics alone.

## Executive decision table

| Path | Target gate | Science result | Does it close the gate? | Review decision |
|---|---|---|---|---|
| MRU | Koide `kappa = 2` | exact equivalence theorem plus weight-class obstruction | **No** | support theorem with explicit missing measure law |
| Berry holonomy | Koide `delta = 2/9` | old geometric route plus bundle obstruction on the actual base | **No** | obstruction theorem against current Berry closure route |
| DPLE | DM `A-BCC` / F4 lane | useful exact matrix-analysis theorem; reproduces F4 on fixed basin chart | **No** | support theorem on the open DM gate |
| STRC-LO + RPSR | quark `a_u` / Min-C lane | quark theorem on bimodule footing; old LO gap closed by BICAC | **Qualified** | branch-internal theorem, reviewer-bar caveat remains |

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

A same-day obstruction theorem now makes the remaining quark gap precise:

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

All retained ray/support identities are `kappa`-independent, so the current
packet does **not** force the BICAC endpoint `kappa = 1`. The missing quark
math is therefore not just “derive BICAC somehow,” but the sharper task:

```text
prove the endpoint-selection law collapsing kappa in [sqrt(6/7), 1] to
kappa = 1.
```

### Why it still does **not** clear the reviewer bar

The old conditional gap is no longer the issue. The issue is now the status of
**BICAC** itself.

`STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md` is explicit that BICAC is a
framework-native bimodule postulate, not a new SM axiom. That is a meaningful
scientific advance over the old "assume STRC" packaging. But it is still an
added structural principle rather than a derivation from the previously
retained quark-side physics alone.

So the quark lane is now stronger than a conditional support theorem, but it
still does not meet the strict reviewer request for object derivation from the
retained package without new load-bearing postulates.

### Science decision

The honest current read is:

- **branch-internal theorem:** yes, via BICAC + STRC-LO + RPSR;
- **reviewer-bar retained derivation:** not yet.

So this lane should now be treated as a **real quark theorem on bimodule
footing**, not merely a conditional route, but with an explicit reviewer-bar
caveat attached to BICAC.

## 5. Net science conclusion

This branch does contain meaningful science. The new logic paths do **not**
all collapse under scrutiny. But they also do **not** yet close the key open
gates.

The right scientific read is:

1. **MRU**: exact restatement of the remaining Koide scalar law, not a closure.
2. **Berry**: the old geometric support model exists, but the current physical
   Berry-bundle packaging is obstructed on the actual positive Koide base.
3. **DPLE**: real support theorem that upgrades the old F4 selector story, but
   does not eliminate the remaining DM source-side open input, now sharpened
   to a 3-scalar spectral law on `H_e/L_e`.
4. **STRC-LO + RPSR**: quark `a_u` now closes on bimodule footing via BICAC,
   but still imports one additional framework-native structural postulate,
   now isolated as an endpoint-selection law on `kappa`.

So the branch is **not** a clean "remaining open gates are now closed"
science packet.

It is a **mixed support packet** containing:

- one strong DM support theorem (DPLE),
- one quark theorem on bimodule footing (STRC-LO + RPSR),
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
  plus `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  plus `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  as a bimodule-theorem quark packet with an explicit BICAC caveat;
- `KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  and `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
  as infrastructure/support notes if their closure language is demoted.

What is **not** justified by this branch:

- claiming the charged-lepton Koide gate is now scientifically closed;
- claiming the DM flagship gate is now closed through DPLE;
- claiming total scalar-selector axiom cost is now zero.
