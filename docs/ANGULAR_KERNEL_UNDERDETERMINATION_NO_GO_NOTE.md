# Angular Kernel Underdetermination No-Go (with Phase 4 decoupling)

**Date:** 2026-04-25 (audit-ready hygiene: 2026-05-02)
**Type:** no_go
**Claim type:** no_go
**Claim scope:** Two-part statement on the directional-path-measure
construction (`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`):
(1) Negative result (bounded no-go): the angular kernel `w(theta)` of
the directional path-measure walk is structurally underdetermined by the
four currently retained primitives — Cl(3) trace structure, action
extremization on Z^3, causal-cone kinematics (forward-only edges,
theta in [0, pi/2]), and leading-order continuum-limit SO(3) isotropy.
The runner exhibits seven distinct kernels (`uniform`, `cos`, `cos^2`,
three Gaussian widths `exp(-c theta^2)` for `c ∈ {0.4, 0.8, 1.6}`, and
`linear_falloff`) all of which satisfy primitives 1-4 but produce
measurably distinct transverse-step moments `<r_perp^2>` and `<r_perp^4>`,
hence measurably distinct higher-derivative continuum behaviour. The
empirical `beta = 0.8` choice (gravity-card lead candidate) sits in the
middle of this family with no first-principles selection rule. The
no-go is conditional on the four primitives being all the constraints;
closing positively would require adopting one of three candidate
additional axioms (higher-order isotropy, action-Lagrangian principle,
or direct observable matching), none currently retained.
(2) Positive result (retained routing clarification / Phase 4
decoupling): the boost-covariance program (Phase 4, the retained
LORENTZ_BOOST_COVARIANCE_2D and 3PLUS1D theorems) lives entirely on the
fixed staggered/Laplacian Hamiltonian construction, which has zero
angular-kernel freedom. The empirical `beta = 0.8` of the directional-
measure walk does NOT enter Phase 4 anywhere. The two constructions are
on distinct claim surfaces.
**Status:** branch-local bounded no-go on the directional-path-measure
angular kernel + decoupling theorem for the boost-covariance lane;
runner passing PASS=64/64; classified PASS surface dominant_class=C.
Audit ready. On clean audit: target effective_status = retained_no_go
(the no-go is decisive: the runner exhibits 7 concrete kernels passing
primitives 1-4 with measurably different moments, so the kernel is
structurally underdetermined on the retained primitive surface).
**Runner:** `scripts/frontier_angular_kernel_underdetermination_nogo.py`
(PASS=64, FAIL=0; classified runner counts dominant_class=C; the 64
checks span 10 parts including kernel azimuthal symmetry, forward-causal
nonnegativity, distinct moments, Cl(3) trace blindness, action saddle-
point independence, cone-kinematics-equivalent kernel diversity,
leading-order isotropy automaticity, the staggered/Laplacian zero-
kernel-freedom lemma, the Phase-4 decoupling proof, and the combined
no-go statement)
**Companions / load-bearing inputs:**
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md) (Phase-4 decoupling target — 1+1d theorem),
[LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md) (Phase-4 decoupling target — 3+1d theorem),
[ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md](ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md) (defines the directional path measure and lists kernel derivation as open work),
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md) (proves the dispersion theorem on staggered/Laplacian — input for the decoupling theorem)

## Purpose

This note sharpens the boost-covariance lane in the form of a
**bounded no-go on the angular kernel** plus a **retained routing
clarification**. Together they explain why the boost-covariance theorems
can proceed on the fixed staggered/Laplacian carrier without forcing a
derivation of the empirical `beta = 0.8`.

## The no-go

**No-go (Angular Kernel Underdetermination).**
The angular kernel `w(theta)` of the directional path-measure walk
(`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`) is **not** uniquely determined
by the currently retained primitives:

1. Cl(3) trace structure;
2. action extremization on `Z^3`;
3. causal-cone kinematics (forward-only edges, `theta in [0, pi/2]`);
4. leading-order continuum-limit SO(3) isotropy.

Each retained primitive is satisfied by a multi-parameter family of
kernels. The runner verifies this on seven distinct kernels --
`{uniform, cos, cos^2, exp(-0.4 theta^2), exp(-0.8 theta^2),
exp(-1.6 theta^2), linear_falloff}` -- all of which pass primitives
(1)-(4) but produce **measurably different** transverse-step moments,
and therefore measurably different higher-derivative continuum behaviour:

| kernel               | `<r_perp^2>` | `<r_perp^4>` |
|----------------------|--------------|--------------|
| uniform              | 8.00         | 88.00        |
| cos(theta)           | 6.30         | 62.83        |
| cos^2(theta)         | 4.56         | 39.89        |
| exp(-0.4 theta^2)    | 7.30         | 77.77        |
| **exp(-0.8 theta^2)**| **6.52**     | **66.94**    |
| exp(-1.6 theta^2)    | 4.77         | 44.72        |
| linear_falloff       | 6.03         | 59.71        |

The empirical `beta = 0.8` choice (the gravity-card lead candidate) sits
in the middle of this family with no first-principles selection rule.
`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md` lists the missing derivation
explicitly as open work item #3 ("principled derivation of `beta` from
graph geometry").

Therefore: the angular kernel `w(theta)` is an **additional model
parameter**, not a derived quantity, on the currently retained primitive
surface.

## The missing axiom

The no-go is conditional on the four primitives above being **all** the
constraints. Closing the no-go positively would require adopting one of:

1. **Higher-order isotropy axiom.** Demand that the *sub-leading*
   continuum dispersion is also rotationally isotropic, i.e. the
   fourth-order term in the small-`p` expansion of the continuum
   propagator is `O(p^4)` with isotropic coefficient. This would constrain
   the fourth moment `<r_perp^4>` of `w` and therefore one parameter of
   the kernel family (e.g. the width `beta` if the family is restricted
   to Gaussian-in-theta).
2. **Action-Lagrangian principle.** Promote the angular weight from
   amplitude-only to action-derived: define a continuum Lagrangian whose
   Euler-Lagrange equations include the angular preference, and discretise.
   No such Lagrangian has been written on the retained surface.
3. **Direct observable matching.** Pin `w` by demanding agreement with a
   specific observable (e.g. the gravity-card response). This is the
   current de-facto procedure (`beta = 0.8` minimises decoherence
   saturation), but it is empirical rather than structural.

Each of (1)-(3) is itself a separate axiom that has not been written on
the retained claim surface. The no-go does NOT prove that no such axiom
can be written; it only proves that without one the kernel is
underdetermined.

## The decoupling theorem

**Theorem (Phase 4 Decoupling).**
The boost-covariance Phase 4 program is **independent** of the angular
kernel `w(theta)`. Specifically:

- The retained dispersion-isotropy theorem
  ([EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md))
  operates on the **staggered/Laplacian Hamiltonian** propagator
  construction.
- The staggered/Laplacian Hamiltonian is fully determined by the lattice
  action: nearest-neighbour hopping with staggered phases
  `eta_mu(x) = (-1)^{sum_{nu < mu} x_nu}`. It has **zero** angular-kernel
  freedom -- there is no `w(theta)` to choose.
- Therefore Phase 4, which generalises the
  [Phase 2 1+1D theorem](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md) to
  3+1D on the same dispersion-theorem surface, lives entirely on the
  staggered/Laplacian construction.
- The empirical `beta = 0.8` of the directional-measure walk does NOT
  enter Phase 4 anywhere. The two constructions are on distinct claim
  surfaces.

The runner verifies this by:

- Building the staggered Hamiltonian explicitly (Part 8) and showing it
  has no free parameter.
- Verifying the staggered fermion dispersion `E = |sin(p a)|/a` and the
  Laplacian dispersion `E = (2/a)|sin(p a / 2)|` are both fully fixed by
  the action.
- Confirming the existing 37/37 PASS dispersion theorem uses only the
  staggered/Laplacian surface (Part 9).

## Two propagator constructions, two claim surfaces

| Construction          | Object                       | Free angular parameter | On boost-covariance lane? |
|-----------------------|------------------------------|------------------------|---------------------------|
| Staggered Hamiltonian | discrete Dirac, hopping `1/(2a)` | none               | YES (this lane)           |
| Bosonic Laplacian     | nearest-neighbour 2nd diff   | none                   | YES (this lane)           |
| Directional path measure | `exp(i k S)/L^p * w(theta)` | `beta` (and shape)   | NO (gravity-card lane)    |

The no-go applies to the third row; the decoupling theorem says the third
row is irrelevant to Phase 4.

## What this closes

This note contributes two program-level results:

1. **Negative result (bounded no-go):** the directional-measure angular kernel
   `w(theta)` is underdetermined by retained primitives. Promoting the
   gravity-card empirical `beta = 0.8` to a derived quantity requires an
   additional axiom that has not been written.
2. **Positive result (retained routing clarification):** the retained
   boost-covariance lane does not need (1) to be
   resolved. Phase 4 generalises the Phase 2 theorem to 3+1D on the
   staggered/Laplacian construction, where there is no angular-kernel
   parameter to derive.

Both are useful: (1) prevents over-claiming on the directional-measure
side; (2) clears the path for Phase 4 to proceed without that overhead.

## Relation to the retained Lorentz lane

The retained dispersion theorem and the retained 1+1D / 3+1D correlator
theorems live on the staggered/Laplacian Hamiltonian-lattice surface. This
note makes the routing consequence explicit: the directional-measure kernel
question belongs to a different support-side construction and does not sit
on the fixed carrier used by the retained boost-covariance lane.

## Relation to existing repo notes

This note **complements**:

- `ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md` -- which lists the kernel
  derivation as open ("Next work" item 3) but does not state it as a
  theorem-shaped no-go.
- `EMERGENT_LORENTZ_INVARIANCE_NOTE.md` -- which proves dispersion
  isotropy on the staggered/Laplacian surface and is therefore correctly
  scoped as a separate object from the directional-measure walk.
- `frontier_angular_kernel_investigation.py` and
  `frontier_kernel_derivation.py` -- which both do empirical kernel
  scans but explicitly state that no analytic derivation has been found
  ("STATUS: NOT A DERIVATION" in the kernel-derivation script).

This note **does not supersede** any of the above; it adds the explicit
theorem-shaped no-go and the explicit decoupling for the Phase 4
boost-covariance program.

## Package wording

Safe wording:

> The directional-measure angular kernel `w(theta)` is an empirical model
> parameter, not a derived quantity, on the currently retained primitive
> surface. The boost-covariance program decouples from this no-go by
> living entirely on the staggered/Laplacian construction, which has no
> angular-kernel freedom.

Unsafe wording:

> The angular kernel `exp(-0.8 theta^2)` is derived from first principles.

## Honest claim-status

```yaml
actual_current_surface_status: support
conditional_surface_status: bounded no-go on the directional-path-measure angular kernel + decoupling theorem for the boost-covariance lane
hypothetical_axiom_status: closing positively would require one of three candidate additional axioms (higher-order isotropy axiom, action-Lagrangian principle, direct observable matching) — none currently retained
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Branch-local bounded no-go + decoupling theorem. The no-go is decisive on the retained primitive surface (the runner exhibits 7 concrete kernels passing primitives 1-4 with measurably different transverse-step moments). The decoupling theorem is on the staggered/Laplacian carrier where there is no angular-kernel freedom by construction. Awaiting independent audit per AUDIT_AGENT_PROMPT_TEMPLATE."
audit_required_before_effective_retained: true
bare_retained_allowed: false
target_effective_status_on_clean_audit: retained_no_go
target_effective_status_on_clean_audit_reason: "The no-go is structurally decisive: 7 kernels in 7 distinct moment-classes all pass the four retained primitives, so no derivation of w(theta) from those primitives alone can succeed. Closing the no-go positively would require adopting an additional axiom — that is the audit-ratified scope. Auditor is asked to ratify retained_no_go (negative result) rather than retained or retained_bounded (positive results)."
audit_independence_required: cross_family_or_fresh_context
runner_class_dominant: C
```

## Verification

```bash
python3 scripts/frontier_angular_kernel_underdetermination_nogo.py
# PASS=64  FAIL=0
# Exit code: 0
```

The 64 checks span 10 parts:

| Part | Coverage                                                       | PASS |
|------|----------------------------------------------------------------|------|
| 1    | 7 kernels are azimuthally symmetric                            | 7    |
| 2    | 7 kernels are forward-causal nonnegative                       | 7    |
| 3    | 7 kernels give 7 distinct second & fourth moments              | 3    |
| 4    | Cl(3) trace blind to kernel choice                             | 7    |
| 5    | Action saddle-point independent of kernel                      | 8    |
| 6    | Cone-kinematics-equivalent kernels can have different shapes   | 8    |
| 7    | Leading-order SO(3) isotropy automatic for all 7 kernels       | 7    |
| 8    | Staggered/Laplacian Hamiltonian has no kernel freedom          | 5    |
| 9    | Decoupling: Phase 4 -> staggered/Laplacian, kernel irrelevant  | 6    |
| 10   | Combined no-go statement                                       | 6    |

Total: 64/64 PASS.
