# Minimal Tensor Matching/Completion Theorem on the Retained Gravity Stack

**Date:** 2026-04-14 (audit-prep cite-chain rigorize 2026-05-10)
**Script:** `scripts/frontier_tensor_matching_completion_theorem.py`
**Status:** support - structural or confirmatory support note
**Claim type:** bounded_theorem
**Claim scope:** restricted-probe-family theorem that scalar Schur data does
not distinguish vector and traceless-shear channel activations, and that the
tested mixed probe is locally additive in those two channels on the
currently audited restricted class.

## Audit-driven dependency-edge rigorization (2026-05-10)

The 2026-05-05 audit verdict on this row was `audited_conditional` (critical,
load-bearing 9.267) with rationale: "The runner checks imported frontier
modules and imported probe grids rather than deriving the retained scalar
bridge, Schur action, Einstein channels, or restricted classes from the
axiom within the packet. With no cited authorities provided, those upstream
bridge and normalization assumptions remain open dependencies." The named
repair target was: "missing_dependency_edge: provide retained-grade packets
for the imported scalar bridge/Schur action, Einstein-channel readouts,
O_h class, and finite-rank class, or include an axiom-level derivation of
those objects in this audit packet."

This rigorize pass makes the one-hop dependency status explicit so the audit
graph can route directly to the upstream authority surfaces. It does not
derive any of the imported objects within this packet, does not promote any
sibling claim, and does not change this row's `audited_conditional` status.

**Cited authorities (one-hop deps):**

- [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
  — `claim_type: bounded_theorem`, current ledger
  `effective_status: retained_bounded`. Canonical surface for the exact
  scalar Schur boundary action on the local `O_h` class. Strongest leg of
  the input chain; supplies the `I_scalar(f; j)` term whose invariance
  across the four probes is checked by the runner.
- [`SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02.md`](./SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02.md)
  — `claim_type: positive_theorem`, current ledger
  `effective_status: retained`. Canonical surface for Schur-class block
  covariance; supplies the structural framework for inheriting scalar Schur
  invariance across the restricted probe family.
- [`BLOCK_GAUSSIAN_SCHUR_MARGINALIZATION_NARROW_THEOREM_NOTE_2026-05-02.md`](./BLOCK_GAUSSIAN_SCHUR_MARGINALIZATION_NARROW_THEOREM_NOTE_2026-05-02.md)
  — `claim_type: positive_theorem`, current ledger
  `effective_status: retained`. Canonical surface for the block-Gaussian
  Schur marginalization identity; underlies the additivity of channel deltas
  in the bounded local sufficiency result.
- [`DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md`](./DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md)
  — `claim_type: bounded_theorem`, current ledger
  `effective_status: unaudited` (recently `audited_conditional` per
  commit 8cfce7da3). Canonical surface for the restricted discrete
  Einstein/Regge lift; supplies the Einstein-channel readouts `G_{0i}` and
  traceless-shear `G_{ij}` whose independent activation by vector and
  tensor probes is checked by the runner. This is the weakest leg of the
  input chain.
- [`FINITE_RANK_SOURCE_TO_METRIC_THEOREM_NOTE.md`](./FINITE_RANK_SOURCE_TO_METRIC_THEOREM_NOTE.md)
  — `claim_type: bounded_theorem`, current ledger
  `effective_status: audited_conditional`. Canonical surface for the
  finite-rank class; supplies the broader probe class on which the same
  additivity persists with `dG_0i = 6.85e-08, dG_TF = 6.19e-11`.
- [`GR_CLASS_EXPANSION_FINITE_RANK_TARGET_NOTE.md`](./GR_CLASS_EXPANSION_FINITE_RANK_TARGET_NOTE.md)
  — `claim_type: bounded_theorem`, current ledger
  `effective_status: unaudited`. Sister surface for the finite-rank class
  expansion target; sister-status only, not a derivation closure for this
  row.
- [`MINIMAL_AXIOMS_2026-04-11.md`](./MINIMAL_AXIOMS_2026-04-11.md) — `meta`,
  axiom-set authority; supplies the Cl(3) on Z^3 working axiom and the
  3+1 anomaly/selector closure organization referenced in the Purpose
  section. Meta authority only.

**Runner-imported frontier modules (script-level deps):**

The runner consumes three frontier modules via `_frontier_loader`:

- `frontier_tensorial_einstein_regge_completion.py` — supplies the
  `probe_family` Einstein-channel readouts `(dG_0i, dG_TF)` for each probe
  type (base/vector/tensor/mixed). The discrete Einstein/Regge lift
  authority surface is `DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md` (cited above).
- `frontier_same_source_metric_ansatz_scan.py` — supplies the
  `build_best_phi_grid()` exact local `O_h` probe family. The `O_h` class
  authority surface is `OH_SCHUR_BOUNDARY_ACTION_NOTE.md` (cited above).
- `frontier_coarse_grained_exterior_law.py` — supplies the
  `build_finite_rank_phi_grid()` finite-rank probe family. The finite-rank
  class authority surface is `FINITE_RANK_SOURCE_TO_METRIC_THEOREM_NOTE.md`
  (cited above).

**What the cite-chain does NOT close.** Two of the upstream authorities
remain `unaudited` (`discrete_einstein_regge_lift_note`,
`gr_class_expansion_finite_rank_target_note`); one remains
`audited_conditional` (`finite_rank_source_to_metric_theorem_note`). The
"missing_dependency_edge" repair target is therefore not directly satisfied
by this rigorize pass; the chain remains conditional on those parent audits
being upgraded. The runner's PASS=7/0 verifies the load-bearing scalar
invariance and additivity claims on the currently imported probe grids;
this is the bounded scope on which the row stands.

**What this rigorize pass NEVER claims.** It does not derive any of the
imported objects from `Cl(3)` on `Z^3`. It does not close the Schur action,
the Einstein channels, the `O_h` class, or the finite-rank class
within this packet. It does not promote `tensor_matching_completion_theorem_note`
to retained or remove any of the four bullets in the existing
`What remains open` section.

## Purpose

This note treats the gravity problem on the strongest retained surface already
present on the branch, not as a narrow local patch:

- `Cl(3)` on `Z^3` is the working axiom
- anomaly/selector closure already organizes the framework as `3+1`
- the shell/junction law is already exact on the current restricted class
- the microscopic Schur/Dirichlet boundary action is already exact
- the restricted discrete Einstein/Regge lift is already exact
- scalar-only completion is already ruled out

So the remaining question is narrower:

> what is the smallest genuinely tensor-valued boundary data required to extend
> the current scalar shell trace / Schur data toward a full `3+1` completion?

## What the retained stack already forces

The broader retained stack removes several fake degrees of freedom:

1. the completion data must be **shell-local** on the current bridge surface,
   because the restricted lift is already a stationary shell action
2. the completion data must be **observable-level boundary data**, not another
   bulk reparameterization, because the scalar shell trace is already the exact
   boundary observable extracted by the Schur/Dirichlet machinery
3. the completion must respect the already-retained `3+1` split, so the new
   channels must live in the non-scalar lapse/shift/spatial-tensor sector
4. the completion must reduce to the exact scalar package when those new
   channels vanish

That means the missing principle is not an arbitrary new metric ansatz. It must
be a tensor-valued extension of the current shell observable package.

## Exact theorem

On the current restricted probe family already on the branch:

- scalar bridge
- vector shift perturbation
- traceless-shear perturbation
- mixed vector+tensor perturbation

the exact microscopic scalar Schur boundary action is unchanged across all four
probes on both:

- the exact local `O_h` class
- the broader finite-rank class

At the same time:

- the vector perturbation activates an independent `G_{0i}` channel
- the traceless-shear perturbation activates an independent traceless
  `G_{ij}` channel

Therefore the full tensor completion cannot live in the current scalar shell
trace alone. At least **two** additional non-scalar boundary coordinates are
required on the retained restricted class:

1. one shift-like / vector boundary coordinate
2. one traceless-shear boundary coordinate

That lower bound is exact on the current branch.

## Bounded local sufficiency result

The companion verifier then checks the mixed perturbation.

Result:

- on the exact local `O_h` class, the mixed probe is locally additive in the
  two non-scalar channel deltas with errors
  - `dG_0i`: `3.059e-08`
  - `dG_TF`: `8.023e-18`
- on the finite-rank class, the same additivity persists with errors
  - `dG_0i`: `6.850e-08`
  - `dG_TF`: `6.191e-11`

So on the currently audited restricted family, the smallest tensor extension
that closes the tested tangent directions is:

- the exact scalar Schur data
- plus one shift-like tensor coordinate
- plus one traceless-shear tensor coordinate

This is not yet a full GR theorem, because the branch still lacks the
microscopic source-to-channel map and the tensor boundary kernel itself.

## Minimal tensor boundary action forced by the retained stack

The retained shell-action picture now forces the missing object into one narrow
form.

The smallest possible tensor extension compatible with the current stack is a
shell-local quadratic action

`I_tensor(f, a_vec, a_tf ; j, eta) = I_scalar(f ; j)
  + 1/2 [a_vec, a_tf] K_tensor [a_vec, a_tf]^T - eta^T [a_vec, a_tf]`

with:

- `f` the already-exact scalar shell trace
- `a_vec` the shift-like tensor boundary coordinate
- `a_tf` the traceless-shear boundary coordinate
- `K_tensor` a symmetric positive-definite `2 x 2` tensor boundary kernel
- `eta` the microscopic source-to-tensor-channel drive

Everything except `K_tensor` and `eta` is already forced by the retained stack.

## What this closes

This closes the ambiguity in the remaining gravity search space.

The missing gravity principle is no longer:

- a better scalar bridge
- a better scalar shell action
- a more clever static conformal ansatz
- an unspecified “tensor correction”

It is specifically:

> derive the microscopic source-to-`(a_vec, a_tf)` map and the tensor boundary
> kernel `K_tensor` on the current restricted class.

## What remains open

This still does **not** close:

1. the microscopic derivation of `eta`
2. the microscopic derivation of `K_tensor`
3. extension beyond the currently audited restricted class
4. full nonlinear GR in full generality

## Practical conclusion

The positive path to gravity closure is now exact enough to state cleanly:

- the retained stack already forces a shell-local tensor boundary extension
- the missing data are minimally rank-two beyond the scalar shell trace
- the only honest remaining theorem family is the derivation of the tensor
  source map and tensor boundary kernel

That is much tighter than the previous generic “find a tensor completion”
framing.
