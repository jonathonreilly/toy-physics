# Universal GR Tensor Action Blocker Note

**Status:** bounded blocker note. The note records, as a bounded blocker
statement (not as a derivation), that the direct universal GR route is
incomplete because no retained-grade tensor-valued localization primitive
yet identifies the scalar-generator Hessian with Einstein/Regge dynamics on
the full metric space. The "missing primitive" is named here as a label for
the blocker; the note does **not** derive its existence, non-existence, or
uniqueness.
**Date:** 2026-04-14 (audit-narrowing refresh: 2026-05-10)  
**Branch:** `codex/review-active`  
**Role:** direct universal route / bounded blocker label  
**Claim type:** bounded_blocker_label
**Status authority:** independent audit lane only.
**Purpose:** name the blocker so downstream notes can target a sharp object;
this is not a uniqueness or non-existence theorem.

## Audit boundary

This note classifies the direct universal route as blocked. The classification
rests on inventorying retained-grade objects on the current branch:

- **What is imported here as already-exact (not re-derived in this note):**
  the scalar observable generator, the `3+1` kinematic lift on `PL S^3 x R`,
  the tensor-valued variational candidate, the symmetric quotient kernel,
  and the exact rank-2 `A1` invariant projector `Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

- **What is named (not derived) as the blocker label:**
  a covariant `3+1` polarization-frame / projector bundle with a distinguished
  connection extending `Pi_A1` to the complementary `E ⊕ T1` channels, plus
  the induced curvature-localization map `Pi_curv`. This note **introduces
  the name** for the missing primitive and stops there. It does not prove
  existence, non-existence, or uniqueness of such a primitive.

If a future packet supplies a retained projector-bundle/localization theorem
or runner that independently derives the Einstein/Regge identification, this
row becomes obsolete and should be re-audited. Until then the row remains a
blocker label.

## Verdict (scope-bounded)

The direct universal GR route is recorded here as **blocked** because no
retained-grade object on the current branch identifies the scalar-generator
Hessian with full Einstein/Regge metric dynamics. This is a structural-
inventory statement at the route level; it is **not** a uniqueness or
non-existence result.

## What is exact already

### Scalar observable generator

The axiom-side observable principle gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`

This is the unique additive CPT-even scalar generator on the exact Grassmann
Gaussian surface. It is exact, but it is scalar.

### Route-2 kinematic lift

The retained spacetime side gives an exact kinematic background predicate:

`O_lift = 1[S^3 closed] * 1[d_t = 1]`

That is exact on the current atlas. It selects the clean `PL S^3 x R`
background scaffold.

This is a kinematic statement, not a metric carrier.

### Tensor variational candidate

The scalar generator can be lifted into a tensor-valued quadratic form by
taking its metric-source Hessian on the lifted background:

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`

This is the first exact tensor-valued variational candidate on the direct
route. It is exact as a construction, but not yet identified with
Einstein/Regge dynamics.

### Symmetric quotient kernel

The strongest current identification result is that the Hessian kernel is the
unique symmetric bilinear lift of the scalar generator on the `3+1`
perturbation quotient. On the finite prototype used by the current runner, that
quotient kernel is nondegenerate, so the route has no extra tensor bilinear
freedom hiding in the scalar observable principle.

### Exact invariant selector

The current tensor candidate also contains an exact rank-2 `A1` projector
onto lapse and spatial trace:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

This is the strongest exact selector latent in the current construction. It is
canonical on the invariant block, but it does not resolve the complementary
`E \oplus T1` channels needed for the full tensor action.

## What is missing

The direct universal route still lacks the first exact tensor-valued object
that could upgrade the scalar generator into a full `3+1` metric law.

The remaining missing primitive can now be stated more sharply:

1. a covariant `3+1` polarization-frame / projector bundle with a
   distinguished connection that extends the exact `Pi_A1` selector on lapse
   and spatial trace to the complementary `E \oplus T1` channels before
   localization
2. the induced curvature-localization map `Pi_curv` that identifies the
   unique symmetric `3+1` Hessian kernel with the Einstein/Regge tensor law
   on the full metric space

Without one of those, the observable principle remains scalar-only at the
closure level and the direct universal route cannot close full GR.

## Why the current route survey points here

The route survey already ranks the observable-principle effective-action route
first, with the discrete `3+1` variational action as the concrete theorem
form.

That remains the right architecture.

What the survey now makes explicit is the failure mode:

- the scalar generator is exact
- the `3+1` kinematic lift is exact
- but the Einstein/Regge identification of the tensor Hessian has not yet been
  made exact

So the universal route is not wrong. It is incomplete at exactly one
localization primitive.

## Blocker label (named, not derived)

The smallest honest missing object is **labelled here**, for downstream
targeting, as:

> a covariant `3+1` polarization-frame / projector bundle with a
> distinguished connection, together with the induced curvature-localization
> map `Pi_curv` on `PL S^3 x R`

This name is a **target label**, not a derivation. The note does not prove
that any object satisfying this label exists, is unique if it exists, or
that no other primitive could discharge the same blocker. Whether this label
is the right shape for a future retained derivation is an independent
question.

If a future packet derives or axiomatizes a primitive answering this label
(or a different but route-discharging primitive), the direct universal route
can advance from scalar observable principle plus `3+1` kinematics to a
genuine metric dynamics law. Until that happens, this row records only the
inventory-level blocker classification.

## Honest status

The current direct universal route is:

- imported as exact at the scalar observable level
- imported as exact at the `3+1` kinematic lift level
- recorded here as **blocked at the tensor-valued action / uniqueness level**,
  in the bounded inventory sense above (no derivation, no uniqueness or
  non-existence claim about the named missing primitive).

This is a structural-inventory blocker statement on the current atlas, not a
theorem about the missing primitive itself.
