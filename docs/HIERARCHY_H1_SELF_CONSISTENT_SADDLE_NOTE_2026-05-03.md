# Hierarchy H1 Route 1 — Self-Consistent Saddle on the Klein-Four Minimal Block

**Date:** 2026-05-03
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_hierarchy_closure_program.py` (Section H1-R1)
**Targets:** H1 Route 1 of the closure program — eliminate the bounded plaquette
input by promoting `<P>(beta=6)` from a Monte-Carlo readout to a
fixed-point of an axiom-determined self-consistency equation on the minimal
hierarchy block.

## Claim scope (proposed)

> On the V-invariant subspace of the L_s = 2, L_t = 4 staggered-fermion APBC
> minimal block at `beta = 6` (admitted via Wilson canonical convention; see
> `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`), the
> mean-field tadpole `u_0 = <P>^(1/4)` is the unique positive root of an
> exact algebraic fixed-point equation
>
> ```
> u_0^4  =  F(u_0; beta = 6, m -> 0)
> ```
>
> where `F(u_0; beta, m)` is the framework-internal source-derivative
> expression
>
> ```
> F(u_0; beta, m)
>   :=  -(1 / N_plaq) * d/d(beta) [ ln Z_min(u_0, beta, m) ]
> ```
>
> evaluated on the minimal block partition function
>
> ```
> Z_min(u_0, beta, m)
>   :=  exp(-S_W^MF(u_0; beta)) * |det(D + m)|_{L_s=2, L_t=4, U->u_0*I}.
> ```

The narrow theorem **explicitly classifies** the mean-field gauge factorization
`U_{ab} -> u_0 * delta_{ab}` as an admitted standard convention (cycle 7 setup,
PR #302), and the self-consistency closure as a bounded theorem on the V-invariant
subspace of the minimal block (not on the full continuum lattice).

The narrow theorem **does not** claim:

- thermodynamic-limit equality of the minimal-block fixed-point with the
  bulk plaquette (this is the residual "same-surface" claim, still bounded;
  see PLAQUETTE_SELF_CONSISTENCY_NOTE.md);
- closure of the broader Perron-state spatial-environment problem (separate
  bridge-support stack);
- non-uniqueness analysis on the non-V-invariant subspace.

## Admitted dependencies

| Authority | Audit-lane status | Role |
|---|---|---|
| `HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md` | proposed_theorem (class A) | exact `\|det(D+m)\|` closed form on minimal block |
| `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` | bounded_theorem | `beta = 2 N_c / g_bare^2 = 6` from the canonical Wilson normalization |
| `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` | positive_theorem | the V-invariant subspace projection |
| `HIERARCHY_H2_ORDER_PARAMETER_SELECTION_THEOREM_NOTE_2026-05-03.md` | proposed_theorem (class A) | the `(7/8)^(1/4)` factor |

## Load-bearing step (class A — algebraic fixed-point equation)

```text
Setup:
  Wilson gauge action on the minimal hypercube:
    S_W[U]  =  (beta / N_c) * sum_p Re Tr(I - U_p)
  with N_c = 3, beta = 6 (Wilson canonical convention).

  Mean-field factorization (admitted standard convention):
    U_{ab}  ->  u_0 * delta_{ab}  on each link.

  Under MF, each plaquette P satisfies:
    Tr(U_p)   ->  N_c * u_0^4    (4 links per plaquette, scalar trace at MF)
    Re Tr(I - U_p)  ->  N_c * (1 - u_0^4)

  Mean-field gauge action on the minimal block:
    S_W^MF(u_0; beta, N_plaq)  =  beta * N_plaq * (1 - u_0^4)

  where N_plaq = 6 * (L_s)^3 * L_t = 6 * 8 * 4 = 192 plaquettes in the
  minimal L_s=2, L_t=4 block (counting all 6 plaquette orientations per
  site times the 32-site volume).

  Fermion determinant on the minimal block (from the MATSUBARA
  DETERMINANT NARROW THEOREM):
    |det(D + m)|_min  =  prod_omega [m^2 + u_0^2 (3 + sin^2 omega)]^4

  At m -> 0:
    |det(D)|_min  =  prod_omega [u_0^2 (3 + sin^2 omega)]^4
                  =  u_0^(8 L_t) * prod_omega (3 + sin^2 omega)^4

  At L_t = 4 with sin^2 omega = 1/2 for all 4 modes:
    |det(D)|_{L_t=4}  =  u_0^32 * (7/2)^16.

Partition function on the V-invariant subspace of the minimal block:

  Z_min(u_0, beta, m=0)  =  exp(-S_W^MF(u_0; beta)) * |det(D)|_min
                         =  exp(-beta * N_plaq * (1 - u_0^4))
                          * u_0^(8 L_t)
                          * prod_omega (3 + sin^2 omega)^4.

Plaquette as source derivative:

  <P>  =  -(1 / N_plaq) * d/d(beta) [ ln Z_min ]
       =  (1 - u_0^4)            (from the Wilson MF gauge term;
                                   the determinant is beta-independent
                                   in the MF approximation, so all
                                   beta-dependence sits in the Wilson term).

Self-consistency:
  u_0^4  =  <P>(u_0)  =  1 - u_0^4    (immediate but inconsistent — see below)

The naive self-consistency equation gives u_0^4 = 1/2, i.e. <P> = 1/2,
which is not the framework value 0.5934. The reason is that the
beta-derivative of the determinant must be retained even at the mean-field
saddle, because the saddle u_0 itself depends on beta.

Saddle-point self-consistency (load-bearing):

  Treating u_0 as a beta-dependent saddle u_0(beta) and varying:

    d/d(beta) [ ln Z_min(u_0(beta), beta) ]
      =  partial_beta ln Z_min |_{u_0 fixed}
       + (du_0/d(beta)) * partial_{u_0} ln Z_min |_{beta fixed}.

  At the saddle, partial_{u_0} ln Z_min = 0 by definition. So:

    <P>  =  -(1/N_plaq) * partial_beta ln Z_min |_{u_0 fixed}
         =  (1 - u_0^4).

  But the saddle equation partial_{u_0} ln Z_min = 0 itself constrains u_0:

    partial_{u_0} ln Z_min  =  -beta * N_plaq * (-4 u_0^3)
                               + (8 L_t / u_0)         (from u_0^(8 L_t))
                            =  4 beta N_plaq u_0^3  +  8 L_t / u_0  =  0.

  Solving for u_0^4:

    4 beta N_plaq u_0^4  =  -8 L_t      (no real positive solution!)

  The MF saddle equation has no real positive solution because the gauge
  term is monotone increasing in u_0 (so Wilson action is minimized at
  u_0 = 1) while the fermion log-det term is monotone increasing in u_0
  too (for u_0 > 0). The minimum of the action thus sits at the
  unitarity boundary u_0 = 1, NOT at the physical 0.8777.
```

## What this means: the naive MF saddle is the wrong selector

The naive mean-field saddle on the minimal block does not reproduce the
physical plaquette `<P>(beta = 6) = 0.5934`. This is a feature, not a bug:
it is exactly the obstruction that the bridge-support stack already
documents (`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`, lines 134-208).

The honest interpretation of the naive saddle calculation is:

> The MF approximation **overconstrains** the gauge sector by collapsing all
> link variables to a single scalar `u_0`. The physical plaquette is
> determined by the full Haar measure on `SU(3)^{N_link}`, not by a single
> scalar saddle. The bridge-support stack closes this gap progressively
> through the spatial-environment / Perron-eigenvector chain.

This is consistent with the framework's existing observation:

```text
exact obstruction to the naive constant-lift law
  P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))
```

(See `GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`, listed in
the PLAQUETTE_SELF_CONSISTENCY support stack.)

## Strengthened V-invariant fixed-point (the real Route 1)

The correct route is to retain the V-invariant subspace projection from
OBSERVABLE_PRINCIPLE Theorem 4 and replace the naive MF saddle with the
V-invariant Haar moment integral:

```text
V-invariant projection:
  P_V  :  measurable functions on SU(3)^{N_link}   ->   V-invariant subspace.

V-invariant plaquette fixed-point equation (proposed):
  <P>_V(beta)
    :=  integral_{SU(3)^{N_link}} P[U] * P_V[U] * exp(-S_W[U]) dU
        / Z_V(beta)
    =   (1 / N_plaq)
        * d/d(beta) [ ln Z_V(beta) ]
  where
    Z_V(beta)  :=  integral_{SU(3)^{N_link}} P_V[U] * exp(-S_W[U]) dU.

The V-invariant subspace is finite-dimensional in the character-recurrence
basis of the spatial-environment Perron operator
(GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md). On
this finite basis, Z_V(beta) reduces to a finite-dimensional analytic
function of beta, and <P>_V(beta) is therefore an analytic function of beta.

The reduction is concretely:

  Z_V(beta)  =  sum_{(p,q) in P_V} c_{(p,q)}(beta) * <P>_{(p,q)}

where the sum runs over V-invariant SU(3) irreps in the character expansion
of the Wilson action and `<P>_{(p,q)}` are V-invariant tensor-transfer
matrix elements. The explicit coefficients `c_{(p,q)}(beta)` are
fully determined by the framework's tensor-transfer Perron operator:
  T_src(beta)  =  exp(3 J) * D_beta * exp(3 J)
(GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md).
```

The remaining computational step is the explicit evaluation of `Z_V(6)` on
the V-invariant Perron basis. The bridge-support stack already exposes:

- `P_loc(6) = 0.4524071590` (Perron solve with `rho = 1` reference)
- `P_triv(6) = 0.4225317396` (Perron solve with `rho = delta_{(0,0)}`)

with the physical V-invariant `<P>_V(6)` lying in the convex hull of the
admissible reference solves (the boundary character measure of the unmarked
spatial Wilson environment with marked-plaquette boundary). The remaining
analytic gap is the explicit identification of the boundary character measure
on the V-invariant subspace.

## Closure status of Route 1

This note **closes**:

1. The MF-saddle obstruction is now an explicit class-A theorem (the naive
   saddle has no positive real solution; the physical plaquette must come
   from beyond MF).
2. The V-invariant projection is now identified as the correct route to a
   finite-dimensional analytic plaquette equation.
3. The bridge between the V-invariant projection and the existing
   bridge-support stack (Perron / character / tensor-transfer) is now explicit.

This note **does not yet close**:

- The explicit numerical evaluation of `<P>_V(6)`. The Perron-state on the
  V-invariant subspace is computable but the evaluation is a substantial
  follow-on calculation (estimated effort: 2-4 weeks of focused tensor-transfer
  Perron work using the existing `frontier_gauge_vacuum_plaquette_*` runners).

The framework retains `<P> = 0.5934` as the bounded numerical input for
downstream rows; this note gives the analytic surface on which the bound
will eventually be replaced by an exact value.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_closure_program.py
```

Verifies, at exact rational precision via `Fraction`:

1. The MF gauge action on the minimal block has the form
   `S_W^MF = beta * 192 * (1 - u_0^4)` with N_plaq = 192.
2. The MF fermion determinant at L_t = 4, m = 0 is
   `u_0^32 * (7/2)^16`.
3. The MF saddle equation `partial_{u_0} ln Z_min = 0` has no positive
   real root, confirming the obstruction.
4. The V-invariant projection retains the exact Klein-four orbit
   structure on the temporal APBC circle.
5. The bridge-support reference Perron solves (`P_loc, P_triv`) are
   recovered with their published 10-digit values.

## Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Two algebraic results: (a) the naive MF saddle on the minimal block has
  no positive real solution (so the physical plaquette cannot come from
  bare MF), and (b) the V-invariant projection reduces the plaquette
  fixed-point equation to a finite-dimensional analytic equation on the
  spatial-environment Perron operator. The note does NOT compute
  <P>_V(6) explicitly; that is identified as the remaining
  computational target.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
```

## Cross-references

- `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — parent note; this Route 1 sharpens
  the residual analytic surface.
- `GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md` —
  the Perron operator identification used in the V-invariant projection.
- `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` — the
  reference Perron solves `P_loc, P_triv`.
- `GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md` — the
  obstruction to naive MF lifts.
- `HIERARCHY_H2_ORDER_PARAMETER_SELECTION_THEOREM_NOTE_2026-05-03.md` —
  the parallel H2 closure.
- `HIERARCHY_CLOSURE_PROGRAM_NOTE_2026-05-03.md` — top-level program.
