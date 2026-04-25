# CKM Atlas/Axiom Closure Note

**Date:** 2026-04-15  
**Status:** promoted no-import quantitative package on the canonical tensor/projector surface
**Script:** `scripts/frontier_ckm_atlas_axiom_closure.py`
**Named subtheorems:** [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md),
[`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md),
[`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md),
[`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md),
[`CKM_SIN_2_BETA_BAR_NLO_N_QUARK_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_SIN_2_BETA_BAR_NLO_N_QUARK_RATIO_THEOREM_NOTE_2026-04-25.md),
[`CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md),
[`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md),
[`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md),
[`CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md),
[`CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md`](CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md),
[`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md),
[`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md),
[`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md),
[`CKM_A_RHO_MULTIPLICATIVE_IDENTITIES_THEOREM_NOTE_2026-04-25.md`](CKM_A_RHO_MULTIPLICATIVE_IDENTITIES_THEOREM_NOTE_2026-04-25.md),
[`CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md`](CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md)

## Claim

The mainline package carries a promoted algebraic CKM atlas/axiom package on
the canonical tensor/projector surface without importing quark masses or
fitted CKM observables. It combines only branch-local exact or derived
ingredients:

1. canonical `alpha_s(v)` from the coupling-map theorem on the plaquette
   surface
2. the exact EWSB `1+2` split
3. the exact quark-block dimension `dim(Q_L) = 2 x 3 = 6`
4. the exact `Z_3` CP source
5. the exact support-side center-excess scalar on the six-state quark block
6. the exact bilinear tensor carrier `K_R` on `A1 x {E_x, T1x}`
7. the exact Schur-complement cascade

The old scalar-closed versus tensor-open split is no longer the right framing.
The theorem package is unique. The democratic seven-site support point remains
an exact scalar comparison surface, but it is not the leading `1 -> 3` CKM
amplitude.

## Canonical Input Surface

The canonical coupling input is

- `alpha_s(v) = alpha_bare / u_0^2`

with

- `<P> = 0.5934`
- `u_0 = <P>^(1/4)`
- `alpha_bare = 1/(4*pi)`.

This is the coupling-map theorem input. It is the actual CKM coupling used in
the runner.

The current hierarchy-pinned `v` surface is only a consistency check:

- `alpha_s(v)_hier = 4*pi (v/(C M_Pl))^(1/8)`
- current main-branch `v = 246.282818290129 GeV`
- relative gap from the canonical CMT coupling: `0` to numerical precision

So the review-safe statement is:

- canonical CKM coupling: same-surface plaquette / CMT route
- hierarchy `v` route: consistency surface, not a second averaged theorem

## Exact Constants

Let

- `n_pair = 2` from the exact EWSB residual pair
- `n_color = 3` from structural `SU(3)`
- `n_quark = 2 x 3 = 6` from `Q_L = (2,3)`

Then

- `lambda = sqrt(alpha_s(v) / n_pair) = sqrt(alpha_s(v)/2)`
- `A = sqrt(n_pair / n_color) = sqrt(2/3)`
- raw quark-block CP radius `= 1/sqrt(n_quark) = 1/sqrt(6)`

The phase chain is unchanged:

- source phase `delta_source = 2*pi/3`
- quark-block projector weights `1 + 5`
- `cos^2(delta_std) = 1/6`
- `sin^2(delta_std) = 5/6`
- `delta_std = arctan(sqrt(5)) = arccos(1/sqrt(6)) = 65.905157... deg`

## Exact Tensor-Slot Theorem

The exact support-side scalar law on the canonical `A1` family is

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

and at the democratic point `r = sqrt(6)` gives

- `delta_A1(q_dem) = 1/42`
- noncentral support fraction `= 6/7`.

That remains an exact scalar support datum.

The decisive new input is the exact bilinear tensor carrier on the microscopic
support block:

- `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

from [S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
and [S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md](S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md).

Two exact facts matter:

1. `K_R` vanishes on pure `A1` backgrounds, including the democratic
   seven-site background.
2. On that same democratic background, the bright columns are exact:
   - `E_x`: `(1, delta_A1)`
   - `T1x`: `(1, delta_A1)`

So the scalar democratic support contraction does **not** suppress the leading
bright/tensor amplitude. It only contributes the lower-row bilinear dressing.

That is the exact reason the `1 -> 3` CKM slot keeps the raw quark-block
radius:

- `sqrt(rho^2 + eta^2) = 1/sqrt(6)`
- `rho = 1/6`
- `eta = sqrt(5)/6`

The scalar democratic contraction `1/sqrt(7)` is still an exact scalar support
comparison surface, but it is not the theorem value for the bright/tensor
`1 -> 3` amplitude.

## Closure Formulas

The theorem package is therefore:

- `lambda^2 = alpha_s(v)/2`
- `A^2 = 2/3`
- `|V_us|_0^2 = alpha_s(v)/2` on the atlas-leading first row
- `|V_ub|_0^2 = alpha_s(v)^3/72` on the atlas-leading first row
- `|V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72`
- `|V_cd|_0^2 = alpha_s(v)/2` on the atlas-leading second row
- `|V_cs|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^2/6`
- `|V_cb| = A lambda^2 = alpha_s(v)/sqrt(6)`
- `|V_ub|_0 = A lambda^3 / sqrt(6) = alpha_s(v)^(3/2)/(6 sqrt(2))`
- `|V_td|_0^2 = 5 alpha_s(v)^3/72` on the atlas-leading third row
- `|V_ts|_0^2 = alpha_s(v)^2/6` on the atlas-leading third row
- `|V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2`
- `rho = 1/6`
- `eta = sqrt(5)/6`
- NLO barred-apex guardrail: `rho_bar=(4-alpha_s(v))/24`,
  `eta_bar=sqrt(5)(4-alpha_s(v))/24`, and protected
  `gamma_bar=gamma_0=arctan(sqrt(5))` through the NLO multiplicative
  barred-apex map
- retained NLO beta-ratio corollary:
  `sin(2 beta_bar)/sin(2 beta_0) = 1 - alpha_s(v)/(n_quark-1)
  = 1 - alpha_s(v)/5 + O(alpha_s(v)^2)`
- retained exact barred-apex-angle closure on the protected-`gamma_bar`
  surface: `tan(alpha_bar) = -4 sqrt(5)/alpha_s(v)`,
  `alpha_bar = pi/2 + arctan((sqrt(5)/20) alpha_s(v))`, and
  `sin(2 alpha_bar) = -8 sqrt(5) alpha_s(v)/(80 + alpha_s(v)^2)`
- retained exact barred-triangle center/Euler-line closure on the
  protected-`gamma_bar` surface:
  `H = (rho_bar, (20 + alpha_s(v))/(24 sqrt(5)))`,
  `H - V_3 = (0, alpha_s(v) sqrt(5)/20)`,
  `G = ((28 - alpha_s(v))/72, sqrt(5)(4 - alpha_s(v))/72)`,
  `O = (1/2, -alpha_s(v) sqrt(5)/40)`, and exact Euler relation
  `H = 3G - 2O`
- atlas-leading B_s phase: `phi_s,0=-alpha_s(v)sqrt(5)/6`
- atlas-leading kaon epsilon_K CKM-bracket factorization:
  `Im(lambda_c^2)=+2J_0`, `Im(lambda_c lambda_t)=-J_0`, and
  `Im(lambda_t^2)=-(5 alpha_s(v)^2/18)J_0`, where
  `lambda_q=V_qs^* V_qd`

The row-level subscript `0` marks the leading atlas/Wolfenstein surface. The
finite-`lambda` exact standard-matrix row readouts and the NLO barred-triangle
closed forms remain guarded parent-atlas calculations, not all-orders
monomial or exact barred-angle promotions. The kaon epsilon_K row is a
CKM-bracket factorization only; standard Inami-Lim, QCD-running, bag, decay
constant, mass, and absolute `|epsilon_K|` inputs remain external.

The retained scalar comparison package is:

- `|V_ub|_scalar = A lambda^3 / sqrt(7) = alpha_s(v)^(3/2)/(2 sqrt(21))`
- `rho_scalar = 1/sqrt(42)`
- `eta_scalar = sqrt(5/42)`

## Numerical Read

Using the canonical plaquette/CMT coupling gives the theorem package:

- atlas-leading `|V_us|_0 = 0.227269`
- `|V_cb| = 0.042174`
- atlas-leading `|V_ub|_0 = 0.003913`
- atlas-leading `|V_ud|_0 = 0.973824`
- atlas-leading `|V_td|_0 = 0.008750`
- atlas-leading `|V_ts|_0 = 0.042174`
- atlas-leading `|V_tb|_0 = 0.999072`
- `J = 3.331e-5`
- atlas-leading kaon factors: `Im(lambda_c^2)=+2J_0`,
  `Im(lambda_c lambda_t)=-J_0`, and
  `Im(lambda_t^2)=-(5 alpha_s(v)^2/18)J_0`
- `delta_std = 65.905 deg`

Against the current branch-local angle-facing comparator package:

- atlas-leading `|V_us|_0`: about `+1.3%`
- `|V_cb|`: about `-0.1%`
- atlas-leading `|V_ub|_0`: about `-0.7%`
- `J` versus angle-reconstructed `J`: about `+0.8%`
- `delta_std`: about `+0.6%`

The retained scalar comparison surface gives:

- `|V_ub|_scalar = 0.003623`
- `J_scalar = 3.084e-5`

which is close to the standalone scalar `J` comparator but weakens `|V_ub|`.

## Observation Comparator Split

There is a real observation-side split on this branch:

- standalone scalar comparator: `J = 3.08e-5`
- reconstructed from the listed comparator angles and phase:
  `J_recon = 3.304e-5`

So the angle-reconstructed comparator sits about `+7.3%` above the standalone
scalar comparator.

That is why the review-safe comparison rule is:

- theorem package compared to the coherent angle package
- scalar-support comparison kept only as a secondary scalar readout

## Why This Is Different From The Imported Bounded Routes

The imported routes remained bounded because they depended on at least one of:

- observed mass inputs
- reference-mass conventions
- matching factors
- finite-volume normalization
- an explicitly bounded decisive step

This route avoids that entire surface. The quantitative CKM entries come from:

- one canonical derived coupling
- exact atlas counts
- the exact `1/6` projector
- the exact bilinear tensor carrier `K_R`
- the exact `Z_3` source
- the exact Schur cascade

No observed quark masses appear anywhere in the derivation.

## Scope

This is the **promoted main-branch CKM authority note**. It supersedes the
older bounded Cabibbo / mass-basis NNI / Jarlskog presentation as the
controlling CKM authority surface.

The review-safe theorem statement is now:

- canonical coupling from the same-surface CMT plaquette derivation
- exact phase dressing from the `1 + 5` projector
- exact `1 -> 3` tensor-slot theorem from `K_R`

The older bounded CKM notes remain useful as route history and comparison
surfaces, but not as the controlling publication authority.
