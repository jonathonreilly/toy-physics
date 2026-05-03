# Angular Kernel Underdetermination No-Go (with Phase 4 decoupling)

**Date:** 2026-04-25
**Status:** bounded no-go on the directional-path-measure kernel +
retained routing clarification/support note for the boost-covariance program
**Type:** no_go proposal (with bundled positive routing-clarification
corollary). Audit status is assigned only by the independent audit
lane; this note does not set or predict an audit verdict. Effective
status is `unaudited` until Codex GPT-5.5 audits it independently.
**Claim type:** no_go
**Claim scope:** Bounded no-go on the angular kernel `w(theta)` of
the directional path-measure walk
(`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`): the four currently
retained primitives (Cl(3) trace, action extremization on `Z^3`,
forward-only causal-cone kinematics, leading-order continuum-limit
SO(3) isotropy) are ALL satisfied by a multi-parameter family of
distinct kernels with measurably different transverse-step moments,
so `w(theta)` is NOT uniquely determined by retained primitives
alone. The empirical `beta = 0.8` Gaussian-in-theta selection has
no first-principles derivation on the retained surface. Bundled
positive corollary: the boost-covariance theorems
(`LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md`,
`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`) live entirely
on the staggered/Laplacian Hamiltonian carrier, which has no
angular-kernel parameter, so the no-go is decoupled from the
boost-covariance lane. Bounded scope: (a) the no-go is conditional
on the four retained primitives being all the constraints --
adding a higher-order isotropy axiom, an action-Lagrangian
principle, or direct observable matching could close the
underdetermination, and the no-go does NOT prove no such axiom can
be written; (b) the seven kernels exhibited in the runner are an
existence demonstration, not an exhaustive parameterization;
(c) the decoupling corollary is exact for the staggered/Laplacian
construction used by the boost-covariance theorems and does not
extend to other lanes that may use the directional measure.
Runner `scripts/frontier_angular_kernel_underdetermination_nogo.py`
PASS=64, FAIL=0.
**Runner:** `scripts/frontier_angular_kernel_underdetermination_nogo.py`
(PASS=64, FAIL=0)
**Companions:**
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md),
[LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md),
[ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md](ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md),
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)

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

## Honest claim-status block

```yaml
proposed_claim_type: no_go
proposed_claim_scope: |
  Bounded no-go on the angular kernel w(theta) of the directional
  path-measure walk (ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md): the
  four currently retained primitives -- (1) Cl(3) trace structure,
  (2) action extremization on Z^3, (3) causal-cone kinematics
  (forward-only edges, theta in [0, pi/2]), (4) leading-order
  continuum-limit SO(3) isotropy -- are simultaneously satisfied
  by a multi-parameter family of kernels (uniform, cos, cos^2,
  three Gaussian-in-theta widths including the empirical
  beta = 0.8, and linear_falloff) that produce measurably different
  transverse-step moments <r_perp^2> and <r_perp^4>. The empirical
  beta = 0.8 has no first-principles selection rule on the
  retained primitive surface. Bundled positive corollary
  (decoupling theorem): the boost-covariance Phase 2 / Phase 4
  program lives entirely on the staggered/Laplacian Hamiltonian
  carrier (nearest-neighbour hopping with staggered phases
  eta_mu(x) = (-1)^{sum_{nu < mu} x_nu} and bosonic Laplacian
  dispersion), which has zero angular-kernel freedom; therefore
  the no-go does not block the boost-covariance theorems.

  Bounded scope: (a) the no-go is conditional on the four retained
  primitives being all the constraints; closing the no-go
  positively would require adopting one additional axiom
  (higher-order isotropy, action-Lagrangian principle, or direct
  observable matching), and this note does NOT prove that no such
  axiom can be written; (b) the seven exhibited kernels are an
  existence demonstration of underdetermination, not an exhaustive
  parameterization of the kernel space; (c) the decoupling
  corollary applies exactly to the staggered/Laplacian construction
  used by the boost-covariance theorems and does not extend to
  other lanes that may use the directional measure (e.g. the
  gravity-card lane, where beta = 0.8 remains an empirical model
  parameter on the retained surface).

  This note does NOT touch any existing audit row, and does NOT
  propose flipping any other note's claim_type or effective_status.
  It enters as a STANDALONE unaudited source claim awaiting
  independent audit.

status_authority: independent audit lane only
audit_required_before_effective_retained: true
bare_retained_allowed: false
```
