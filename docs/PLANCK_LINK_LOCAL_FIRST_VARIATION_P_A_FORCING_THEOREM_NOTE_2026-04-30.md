# Planck Link-Local First-Variation P_A Forcing Theorem

**Date:** 2026-04-30
**Status:** intrinsic proposed_retained candidate; current audit graph effective
status is conditional until upstream action/time/CPT authority rows are clean
**Runner:** `scripts/frontier_planck_link_local_first_variation_p_a_forcing.py`
**Loop:** `physics-loop/planck-pa-retention-block01-20260430`

## Purpose

PR #228's positive primitive Clifford-Majorana construction was audited as
`audited_renaming` because it matched the rank-four packet

```text
P_A H_cell ~= C^4
```

to the irreducible complex `Cl_4(C)` module without proving that retained
substrate content forces that active packet.

Two follow-up no-gos then showed:

```text
stated substrate symmetries -/-> unique P_A
stated substrate symmetries -/-> first-order P_1 over Hodge-dual P_3
```

The boundary-incidence stretch no-go sharpened the same obstruction:
oriented faces and normal covectors are Hodge-dual, so boundary orientation
alone still does not select `P_1`.

This note records the new path that does distinguish them. It uses the
microscopic action surface itself. The accepted `A_min` dynamics are the finite
Grassmann / staggered-Dirac partition with lattice operators built from
one-link nearest-neighbor terms. On the time-completed primitive local star,
the fundamental action-source variables are one-link / one-axis variables.
The primitive active response is the first variation of that retained action
with respect to those variables. Its support is exactly the Hamming-weight-one
packet:

```text
P_A = P_1.
```

The Hodge-dual `P_3` remains a valid flux/face representation, but it is not a
fundamental one-link action variation. It appears only after applying Hodge
duality or after taking higher composite/third-variation data.

## Inputs

The theorem uses:

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md): local
  `Cl(3)`, cubic `Z^3`, finite Grassmann / staggered-Dirac partition, and
  lattice operators built on that surface;
- [NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md): staggered
  hopping and `Cl(3)` bivector / spatial spin-lift context;
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md):
  retained graph-first gauge-substrate closure context;
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md): the
  single time axis completing the primitive `(t,x,y,z)` local star;
- [I3_ZERO_EXACT_THEOREM_NOTE.md](./I3_ZERO_EXACT_THEOREM_NOTE.md): the
  retained complex/Born-rule quantum structure for treating the selected
  packet as a complex Hilbert block;
- [CPT_EXACT_NOTE.md](./CPT_EXACT_NOTE.md): the substrate CPT grading checked
  by the runner;
- the finite event-cell algebra used in PR #228:

  ```text
  H_cell ~= Lambda^* span(t,x,y,z) ~= (C^2)^4.
  ```

The proof does not use `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, or any `alpha_LM` decoration chain.

## Audit-Pressure Boundary

The load-bearing selector is not the phrase "first-order boundary response."
That phrase was already isolated as circular by the earlier no-gos.

The selector here is narrower and action-native:

```text
image of the algebraic differential of the retained link-local microscopic
action with respect to its fundamental local link/source variables.
```

Those variables are present because the minimal input stack already contains
the finite Grassmann / staggered-Dirac partition and lattice operators on
`Z^3`. A Hodge-dual face/flux variable is a valid dual representation, but it
is not an automorphism of that source domain: it sends a one-link source to a
three-link composite. If an audit does not accept the minimal action source
domain as retained substrate content, this note demotes to conditional support
rather than retained-grade closure.

## Theorem Statement

Let

```text
W = span(t,x,y,z),        H_cell ~= Lambda^* W.
```

Let `u_a` denote the fundamental local link/source variable for the primitive
axis `a` in the time-completed staggered/Dirac local star. The retained
microscopic action is link-local: each primitive local term carries exactly
one such axis label,

```text
S_link = sum_{a in {t,x,y,z}} u_a J_a,
```

where the coefficients and staggered signs in `J_a` are irrelevant to support
degree.

Then the primitive first variation

```text
dS_link / du_a
```

has support on exactly the four one-axis basis states:

```text
{t}, {x}, {y}, {z}.
```

Therefore the active primitive action-response projector is

```text
P_1 = sum_a P_{ {a} } = P_A.
```

Among the 17 local rank-four equivariant projector classes admitted by the
spin/time/CPT/local symmetry package, `P_A` is the unique class satisfying the
additional retained-action criterion:

```text
support = support of the fundamental link-local first variation.
```

Thus:

```text
A_min link-local first variation + anomaly-forced time
  -> unique active P_A block.
```

## Derivation

### 1. The Retained Action Variables Are One-Link Variables

The minimal accepted dynamics are not an arbitrary exterior-algebra response
on `H_cell`. They are the finite Grassmann / staggered-Dirac partition and
the lattice operators built on that surface. Locally, the staggered/Dirac
operator is a nearest-neighbor hop operator. After the anomaly-forced time
completion, the primitive local star has four axis labels:

```text
t, x, y, z.
```

Each primitive local source term is one-link:

```text
u_t J_t,  u_x J_x,  u_y J_y,  u_z J_z.
```

The runner represents only this support fact; it does not need the numeric
values of the staggered eta signs.

### 2. The Action Differential Has Hamming Weight One

Let the local source space be

```text
U = span(u_t,u_x,u_y,u_z).
```

The link-local action restricts to the affine-linear source map

```text
S_link : U -> H_cell,
S_link(u) = sum_a u_a J_a,
support(J_a) = {a}.
```

The algebraic differential is therefore

```text
dS_link(du_a) = J_a.
```

In the Boolean event-cell dictionary,

```text
J_a <-> P_{ {a} }.
```

So the total support of the retained source differential is

```text
span({t}, {x}, {y}, {z}) = P_1 H_cell.
```

The runner constructs the four derivative images `dS_link(du_a)` and verifies
that their support projector is exactly `P_1`, with rank four. This is a
derivative of the retained microscopic source map, not an adopted observable
readout principle.

### 3. P_3 Is A Flux/Composite Sector, Not A Fundamental First Variation

The Hodge-dual sector is

```text
P_3 = span({x,y,z}, {t,y,z}, {t,x,z}, {t,x,y}).
```

It is the oriented face / flux representation dual to one-link normal data.
It is also the support of third-degree composite monomials

```text
product_{b != a} u_b.
```

But this is not a first variation of the link-local action. It is a Hodge
image or higher composite response. The runner verifies:

```text
* P_1 *^{-1} = P_3,
P_1 P_3 = 0,
degree(P_1 source) = 1,
degree(P_3 source) = 3.
```

This is the step that resolves the previous Hodge obstruction. Hodge duality
is still exact on exterior algebra, but it is not an automorphism of the
fundamental action-source domain because it maps one-link variables to
three-link face/flux composites.

### 4. Uniqueness Among Rank-Four Equivariant Projectors

The symmetry-only substrate-to-`P_A` no-go enumerated 17 local rank-four
equivariant projector classes. That no-go remains correct on its stated
surface.

The present theorem adds a criterion not present in the symmetry-only
surface, and derives it from the retained action:

```text
the active primitive response must be the support of the link-local first
variation of the microscopic action.
```

The runner re-enumerates the 17 classes and applies this criterion. Exactly
one class matches:

```text
E_t + E_V = P_1 = P_A.
```

All other classes, including `P_3`, fail the first-variation support criterion.

### 5. Clifford-Majorana Carrier After P_A Is Forced

Once the active packet is forced to be rank four, the PR #228 algebraic
construction applies without using rank equality as the selector. The retained
spatial `Cl(3)` bivector content plus the anomaly-forced time axis construct
four primitive coframe axes. The unique irreducible complex `Cl_4` module has
dimension four:

```text
Cl_4(C) ~= M_4(C),        dim K = 4.
```

The runner constructs Hermitian generators on the selected rank-four packet,
verifies the Clifford anticommutator, verifies span `M_4(C)`, and verifies the
two-mode CAR pairing.

The theorem therefore supplies the missing selector:

```text
retained link-local action response -> P_A H_cell,
retained Cl(3)+time coframe -> Cl_4(C) carrier on that selected packet.
```

## Relation To The Existing No-Gos

This theorem does not overturn the no-gos. It changes the premise surface.

| Prior result | Still valid? | What changes here |
|---|---:|---|
| symmetry-only substrate-to-`P_A` no-go | yes | link-local first variation is extra retained action structure, not pure symmetry |
| first-order coframe unconditionality no-go | yes | "first-order" is not assumed abstractly; it is the first variation of the retained link-local action |
| boundary-incidence no-go | yes | normal/face incidence is Hodge-dual, but only the normal link variable is fundamental in the action source domain |
| full-cell odd coframe restriction obstruction | yes | the active `Cl_4` carrier is intrinsic after `P_A` is selected; it is not a compression of odd full-cell generators |
| bilinear active-block support boundary | yes | bilinears show capacity; the present theorem supplies the missing block selector, not a dimensional action unit |

## Claim Boundary

This theorem claims:

- the active primitive action-response block is forced to be `P_A` by the
  retained link-local first variation;
- the Hodge-dual `P_3` is excluded as a fundamental first variation, though it
  remains a valid flux/face representation;
- after `P_A` is selected, the rank-four `Cl_4(C)` / two-mode CAR carrier is
  the unique irreducible complex Clifford module up to automorphism.

This theorem does not claim:

- the SI decimal value of `hbar`;
- a physical-units derivation of `G_Newton`;
- strong-field continuum gravity;
- a black-hole interior statement;
- that boundary incidence alone selects `P_A`;
- that the gravitational Wald/area carrier identification is closed by this
  note alone.

The theorem is intended to repair the PR #228 renaming failure at the
substrate-to-active-packet step. Audit ratification is still required before
any downstream Planck cascade can be promoted. On the current audit graph, the
intrinsic theorem is a `proposed_retained` candidate but the effective lane
remains conditional until the upstream action/time/CPT authority rows are
clean or the auditor accepts those facts as base substrate content for this
restricted theorem.

## Verification

Run:

```bash
python3 scripts/frontier_planck_link_local_first_variation_p_a_forcing.py
```

Current output:

```text
Summary: PASS=8  FAIL=0
Verdict: PASS.
```

The eight checks are:

1. construct the retained local action support as one-link / one-axis source
   terms;
2. verify first-variation support is exactly `P_1`;
3. verify `P_3` is third-composite / flux support, not first variation;
4. verify Hodge duality is not an automorphism of the fundamental link-source
   domain;
5. enumerate rank-four equivariant projectors and show the first-variation
   support criterion selects one class;
6. verify the selected projector remains spin/time/CPT equivariant and
   tensor-local;
7. verify the selected rank-four packet supports the irreducible `Cl_4(C)` /
   CAR carrier;
8. verify the forbidden-input boundary.
