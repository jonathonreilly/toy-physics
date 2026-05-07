# Restricted Strong-Field Closure on the Exact `O_h` Shell Class

**Date:** 2026-04-13; derivation closure repair 2026-05-07
**Status:** proposed_retained restricted strong-field theorem; independent audit
required before effective retained status; not full nonlinear GR
**Packet runner:**
[`frontier_restricted_strong_field_closure_packet.py`](../scripts/frontier_restricted_strong_field_closure_packet.py)
**Component runners:**
[`frontier_sewing_shell_source.py`](../scripts/frontier_sewing_shell_source.py),
[`frontier_oh_static_constraint_lift.py`](../scripts/frontier_oh_static_constraint_lift.py),
[`frontier_oh_schur_boundary_action.py`](../scripts/frontier_oh_schur_boundary_action.py),
[`frontier_microscopic_dirichlet_bridge_principle.py`](../scripts/frontier_microscopic_dirichlet_bridge_principle.py)

## Statement

On the exact local `O_h` star-supported source class realized by the current
finite-box source object, the scalar strong-field sector has an exact restricted
closure:

1. the exterior sewing field is represented exactly by the shell source
   `sigma_R = H_0 Pi_R^ext phi` on the band `3 < r <= 5`;
2. the same-charge bridge is the unique common Dirichlet bridge
   `psi = 1 + phi_ext`, `chi = 1 - phi_ext = alpha psi`;
3. the local static conformal source readout is forced pointwise by the two
   conformal constraints:
   `rho = sigma_R / (2 pi psi^5)` and
   `S = 0.5 rho (1/alpha - 1)`;
4. the exact shell trace is the stationary point, and in fact the unique
   minimum, of the microscopic Schur-complement boundary action.

This is a restricted scalar/static-conformal closure. It does not claim a full
pointwise Einstein/Regge tensor theorem.

## Inputs Fixed Inside The Packet

The proof uses the following finite-box objects.

- `H_0`: the nearest-neighbor graph Laplacian on the current `15^3` box,
  positive definite on the zero-boundary potential sector.
- `G_0 = H_0^{-1}` on the interior.
- `S = {0, +/- e_x, +/- e_y, +/- e_z}`: the seven-point star support.
- the exact local `O_h` source object `phi` from
  [`frontier_same_source_metric_ansatz_scan.py`](../scripts/frontier_same_source_metric_ansatz_scan.py),
  with `O_h`-invariant support data.
- cutoff `R = 4`, exterior projector
  `phi_ext = Pi_R^ext phi`, where `Pi_R^ext` sets the field to zero on
  `r <= R`.

Concretely, the source object is the finite-rank star-support field

```text
phi = G_0 P q_eff,
q_eff = (I - W G_S)^(-1) m,
```

where `P` injects the seven star sites into the box, `G_S = P^T G_0 P`,
`m = (m0, ms, ms, ms, ms, ms, ms)` with `m0 = 0.8247`,
`ms = 0.2271`, and `W` is the `O_h`-commutant star operator with adapted-basis
parameters

```text
(x1, x2, mix, lam_e, lam_t)
  = (0.0698, 0.0499, -0.0070, 0.0642, 0.1056).
```

The generated field is rescaled so the maximum support value is `0.35`. These
numbers define the restricted source class used by this note; they are not
fitted to the closure residuals in the derivation below.

The theorem is intentionally conditional on this exact local source class. It
does not attempt to derive the numerical source parameters from the single
axiom alone.

## Derivation

### 1. Exact Shell Source

Define

```text
phi_ext = Pi_R^ext phi,
sigma_R = H_0 phi_ext.
```

Since `G_0` is the inverse of `H_0` on the finite Dirichlet interior,

```text
G_0 sigma_R = G_0 H_0 phi_ext = phi_ext.
```

The projector is the only place where `phi_ext` fails to be lattice-harmonic:
inside the cutoff it is zero, outside the cutoff it is the original exterior
harmonic field, and `H_0` has nearest-neighbor range. Therefore the support of
`sigma_R` is confined to the cells adjacent to the radius-4 interface. On the
current centered lattice this interface is exactly the sewing band
`3 < r <= 5`.

The runner
[`frontier_sewing_shell_source.py`](../scripts/frontier_sewing_shell_source.py)
verifies the finite-box identity directly:

```text
exact local O_h family: ext_err=5.204e-17, full_err=5.204e-17,
Q_total=2.52683051, Q_shell=2.52683051, band=[3.162278, 5.000000]
PASS=9 FAIL=0 TOTAL=9
```

So the shell source is not an inserted shell law. It is the exact image
`H_0 Pi_R^ext phi` of the exterior projector.

### 2. Same-Charge Bridge

Let `u` be the exterior bridge field with the same microscopic shell charge:

```text
H_0 u = sigma_R,    u | outer boundary = 0.
```

The finite Dirichlet operator is positive definite, so this problem has a
unique solution. Since `phi_ext` satisfies the same equation and boundary
condition, uniqueness gives

```text
u = phi_ext.
```

The two scalar bridge factors are therefore fixed as

```text
psi = 1 + u = 1 + phi_ext,
chi = 1 - u = 1 - phi_ext,
alpha = chi / psi.
```

Equivalently, `chi = alpha psi`. If another bridge with the same shell charge
and the same outer boundary existed, its difference from `phi_ext` would be a
homogeneous Dirichlet harmonic function and hence zero.

The microscopic Dirichlet runner checks the same uniqueness through the Schur
action minimizer:

```text
exact local O_h: trace_match=2.637e-16, stationary_grad=6.939e-16
[EXACT] PASS: the exact shell trace is recovered by the boundary-action
minimizer on the exact local O_h class
PASS=6 FAIL=0 TOTAL=6
```

Thus the same-charge bridge is forced by the Dirichlet problem, not chosen as a
post-hoc ansatz.

### 3. Pointwise Shell Orbit Laws

The `O_h` source object is invariant under the cubic group. The centered
projector `Pi_R^ext` and the nearest-neighbor Laplacian `H_0` commute with the
same group action, so `phi_ext`, `sigma_R`, `psi`, `chi`, and `alpha` are
constant on `O_h` orbits. Any pointwise function of these fields is also an
orbit law.

The static-conformal shell readouts derived below are pointwise functions of
those fields, so the shell density and stress readout are exact pointwise
orbit laws on the whole band. The runner reports

```text
shell orbit spreads: O_h (rho,S)=(3.123e-17,1.897e-18)
[PASS (A)] [EXACT] on the exact local O_h class the lifted shell density and
stress are pointwise orbit laws
```

The separate reduced-shell runner also verifies that the seven star-support
point-Green columns have a common normalized reduced shell law and that the
exact local `O_h` family follows it:

```text
c_aniso = 0.081435402995901
max family-vs-reference c_aniso difference = 4.163e-17
PASS=7 FAIL=0 TOTAL=7
```

### 4. Local Static Conformal Lift

The restricted local `3+1` claim is only the static conformal constraint pair

```text
H_0 psi = 2 pi psi^5 rho,
H_0 chi = -2 pi alpha psi^5 (rho + 2S).
```

Once the shell source and bridge are fixed, these equations determine the
readout variables triangularly. For the affine bridge fields, the full-grid
Laplacian has a unit outer layer, so `H_0 1 = 0` in this
static-conformal residual calculation. Since `H_0 phi_ext = sigma_R`,

```text
H_0 psi = sigma_R,
H_0 chi = -sigma_R.
```

The first constraint therefore forces

```text
rho = sigma_R / (2 pi psi^5).
```

Substituting this into the second constraint gives

```text
rho + 2S = sigma_R / (2 pi alpha psi^5)
2S = rho (1/alpha - 1)
S = 0.5 rho (1/alpha - 1).
```

So `rho` and `S` are not free definitions selected after the fact. They are the
unique pointwise solution of the restricted static conformal constraint system
for the independently fixed shell source and bridge.

The runner
[`frontier_oh_static_constraint_lift.py`](../scripts/frontier_oh_static_constraint_lift.py)
then evaluates the residuals:

```text
exact local O_h: shell band=[3.162278, 5.000000],
max residuals=(psi=1.789e-15, chi=1.551e-15)
[PASS (A)] [EXACT] the exact local O_h bridge fields satisfy the first local
static conformal constraint exactly
[PASS (A)] [EXACT] the exact local O_h bridge fields satisfy the second local
static conformal constraint exactly
PASS=8 FAIL=0 TOTAL=8
```

### 5. Schur Boundary Action

Partition the exterior lattice variables into the inner trace `Gamma_R` and
the exterior harmonic bulk. In block form,

```text
H_0 =
[ H_tt  H_tb ]
[ H_bt  H_bb ].
```

Because the finite Dirichlet Laplacian is positive definite, `H_bb` is
positive definite. Eliminating the bulk variables gives the Schur complement

```text
Lambda_R = H_tt - H_tb H_bb^{-1} H_bt.
```

For a trace vector `f`, the discrete harmonic extension has boundary energy

```text
E_R(f) = 0.5 f^T Lambda_R f,
grad E_R(f) = Lambda_R f.
```

Let `f_*` be the trace of the exact exterior shell field and let
`j = Lambda_R f_*` be the microscopic trace flux. The sourced action is

```text
I_R(f; j) = 0.5 f^T Lambda_R f - j^T f.
```

Then

```text
grad I_R(f_*; j) = Lambda_R f_* - j = 0,
I_R(f; j) - I_R(f_*; j)
  = 0.5 (f - f_*)^T Lambda_R (f - f_*).
```

Since `Lambda_R` is positive definite, `f_*` is the unique global minimizer.
This derives the shell trace law from the microscopic lattice boundary action.

The Schur runner verifies the finite-box operator and stationarity:

```text
trace count=1052, bulk count=888, symmetry error=3.331e-16,
min eigenvalue=1.148587e+00
exact local O_h: rebuild_err=2.255e-17, flux_err=9.021e-17,
stationary_grad=9.021e-17
PASS=6 FAIL=0 TOTAL=6
```

The Dirichlet-principle runner verifies the minimizer form:

```text
[EXACT] PASS: the bridge is the unique minimum-energy discrete Dirichlet
extension on the current star-supported strong-field class
PASS=6 FAIL=0 TOTAL=6
```

## Closure Chain

Combining the preceding steps gives the closure chain over independent
finite-box inputs:

```text
exact local O_h source phi
  -> phi_ext = Pi_R^ext phi
  -> sigma_R = H_0 phi_ext
  -> unique Dirichlet bridge u = phi_ext
  -> psi = 1 + u, chi = 1 - u, alpha = chi / psi
  -> unique static-conformal readouts rho and S
  -> zero local static-conformal residuals
  -> Schur action I_R whose unique minimizer is the same shell trace.
```

Each arrow is an algebraic solve, a group-covariance consequence, or a
positive-definite Schur complement computation. The closure package is
therefore derived on the restricted `O_h` shell class rather than declared as
a status assertion.

## Runner Evidence

The stdout captured during this repair lives in
[`outputs/physics_loop/restricted_strong_field_closure/`](../outputs/physics_loop/restricted_strong_field_closure/).

| Runner | Role | Result |
|---|---|---|
| [`frontier_restricted_strong_field_closure_packet.py`](../scripts/frontier_restricted_strong_field_closure_packet.py) | executes all six component runners and fails on any non-clean component summary | [`PASS=41 FAIL=0 TOTAL=41`](../outputs/physics_loop/restricted_strong_field_closure/frontier_restricted_strong_field_closure_packet.stdout.txt) |
| [`frontier_sewing_shell_source.py`](../scripts/frontier_sewing_shell_source.py) | derives `sigma_R = H_0 Pi_R^ext phi`, reconstruction, charge inheritance, shell band | [`PASS=9 FAIL=0 TOTAL=9`](../outputs/physics_loop/restricted_strong_field_closure/frontier_sewing_shell_source.stdout.txt) |
| [`frontier_oh_static_constraint_lift.py`](../scripts/frontier_oh_static_constraint_lift.py) | solves and verifies the local static conformal lift and `O_h` orbit laws | [`PASS=8 FAIL=0 TOTAL=8`](../outputs/physics_loop/restricted_strong_field_closure/frontier_oh_static_constraint_lift.stdout.txt) |
| [`frontier_oh_schur_boundary_action.py`](../scripts/frontier_oh_schur_boundary_action.py) | constructs `Lambda_R`, checks SPD, trace flux, stationarity | [`PASS=6 FAIL=0 TOTAL=6`](../outputs/physics_loop/restricted_strong_field_closure/frontier_oh_schur_boundary_action.stdout.txt) |
| [`frontier_microscopic_dirichlet_bridge_principle.py`](../scripts/frontier_microscopic_dirichlet_bridge_principle.py) | checks unique boundary-action minimizer | [`PASS=6 FAIL=0 TOTAL=6`](../outputs/physics_loop/restricted_strong_field_closure/frontier_microscopic_dirichlet_bridge_principle.stdout.txt) |
| [`frontier_star_supported_bridge_class.py`](../scripts/frontier_star_supported_bridge_class.py) | sampled finite-rank extension sanity check beyond the benchmark `O_h` field | [`PASS=5 FAIL=0 TOTAL=5`](../outputs/physics_loop/restricted_strong_field_closure/frontier_star_supported_bridge_class.stdout.txt) |
| [`frontier_one_parameter_reduced_shell_law.py`](../scripts/frontier_one_parameter_reduced_shell_law.py) | reduced shell-law consistency for the star support and benchmark families | [`PASS=7 FAIL=0 TOTAL=7`](../outputs/physics_loop/restricted_strong_field_closure/frontier_one_parameter_reduced_shell_law.stdout.txt) |

The sampled finite-rank rows are supporting evidence only. The theorem claim in
this note is the exact local `O_h` closure above.

## Broader Bounded Consequence

For the broader exact finite-rank source family already on the branch:

- the same local static conformal constraints hold exactly;
- the same microscopic Schur boundary action reproduces the exact shell trace
  law exactly;
- the remaining non-`O_h` difference is the already-controlled small
  within-orbit shell variation:
  - `rho` about `1.4%`;
  - `S` about `2.7%`.

So the broader-family gap is not a new scalar shell law or scalar boundary
action. It is a small pointwise deformation of the same scalar closure
package, plus the still-open problem of a full tensorial Einstein/Regge law.

## What Is Promotable After Audit

The following is the audit target:

> On the exact local `O_h` strong-field source class, the framework admits an
> exact restricted scalar/static-conformal closure consisting of an exact shell
> source, unique same-charge Dirichlet bridge, exact local static conformal
> constraint lift, and exact microscopic Schur boundary action.

This is stronger than the earlier weak-field-only gravity surface, but it is
restricted to the scalar/static-conformal shell class.

## What Is Not Promotable

This does **not** justify claiming:

1. fully general nonlinear GR;
2. full pointwise Einstein/Regge closure beyond the current static conformal
   bridge;
3. fully general non-`O_h` strong-field closure;
4. no-horizon / no-echo as theorem-level downstream consequences.

The bounded GW-echo companion may cross-reference the separately retained
pair in `EVANESCENT_BARRIER_AMPLITUDE_SUPPRESSION_THEOREM_NOTE.md`, but that
does not promote the Planck-unit astrophysical exponent
`exp[-(R_S/l_P) ln(R_S/R_min)]` to this theorem.

## Practical Conclusion

Gravity is promotable only in this **restricted scalar strong-field** form, not
as a full universal GR derivation.
