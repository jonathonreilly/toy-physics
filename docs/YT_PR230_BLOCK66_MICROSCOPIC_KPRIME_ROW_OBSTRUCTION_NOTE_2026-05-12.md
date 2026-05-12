# PR230 Block66 Microscopic K-Prime Row Obstruction

**Status:** no-go / exact negative boundary for the current PR230 surface:
microscopic source/transfer/Feshbach formalism reduces `K'(pole)` or pole
residue to a missing same-surface derivative/projection row
**Runner:** `scripts/frontier_yt_pr230_block66_microscopic_kprime_row_obstruction.py`
**Certificate:** `outputs/yt_pr230_block66_microscopic_kprime_row_obstruction_2026-05-12.json`

## Claim Tested

This probe tests the direct microscopic route left open by Blocks57-64:

```text
compact Cl(3)/Z3 scalar source functional
+ transfer operator / Schur complement / Feshbach denominator
=> K'(pole) or pole residue
```

The formal theorem is clean.  If the same surface supplies an analytic inverse
kernel `K(x)`, a simple isolated pole at `x_*`, source vector `u`, and
right/left pole vectors `r,l`, then

```text
Res_x <u, K(x)^(-1) u> = <u,r><l,u> / <l,K'(x_*)r>.
```

In the self-adjoint case this is

```text
Res_x = |<u,psi>|^2 / <psi,K'(x_*)psi>.
```

In a transfer-resolvent form,

```text
<u,(1-zT)^(-1)u>
```

has a simple-pole residue fixed by the isolated transfer spectral projection
`P_*` and the source overlap `<u,P_*u>`.  In a Schur/Feshbach source/orthogonal
split,

```text
D_eff = P K P - P K Q (Q K Q)^(-1) Q K P,
```

so

```text
D_eff' =
  P K' P
  - P K' Q R Q K P
  - P K Q R Q K' P
  + P K Q R Q K' Q R Q K P,
```

with `R=(QKQ)^(-1)` at the pole.

Thus the attempted theorem reduces the route to one precise missing object:
the same-surface pole derivative/projection row.  Current PR230 artifacts do
not provide it.

## Exercises Required Before Conclusion

### Assumptions

| Assumption | Needed for | If wrong |
|---|---|---|
| Same-surface analytic inverse kernel `K(x)` exists near the scalar pole | Meromorphic residue theorem for the source two-point function | `K'(pole)` is only formal; source functional derivatives do not define the row |
| The pole is isolated and simple after FVIR/thermodynamic limiting | Rank-one Laurent term | A threshold or multipole continuum replaces scalar LSZ residue data |
| Pole vectors or spectral projection are same-surface objects | Numerator and derivative sandwich | A denominator zero has no normalization |
| Additive Cl(3)/Z3 source carrier is the source coordinate in `K` | Prevents moving factors between source coordinate and operator | Source residue is rescalable |
| Feshbach `P/Q` split is a certified neutral scalar kernel split | Gives meaning to `A/B/C` and derivative rows | Schur algebra is correct but row labels are unauthoritative |
| Contact subtraction is fixed before pole differentiation | Separates analytic contact curvature from the pole | Contact choices can change inverse-curvature reads |
| Euclidean-to-pole analytic continuation is authorized | Identifies the derivative variable | Transfer energies/moments do not define the required `p^2` derivative |
| FVIR/toron limits commute with pole isolation/residue extraction | Promotes finite-volume support to a scalar pole row | Atomless soft-continuum limits can erase finite-volume pole weights |
| Canonical `O_H`/source-overlap or strict physical response is supplied | Converts source-pole normalization to PR230 Higgs normalization | The result normalizes `O_sp`, not canonical `O_H` |

### First-Principles Minimal Driver

The route has only three mathematical drivers:

- denominator zero: `D(x_*)=0`;
- derivative at the zero: `D'(x_*)=<l,K'(x_*)r>` or the Feshbach derivative
  above;
- source numerator: `<u,r><l,u>`, or `1` only after a certified
  source-coordinate Schur normalization.

Blocks57-64 give support around the source functional, finite spectral
positivity, fixed source carrier, and finite moments.  They do not give
`K'(pole)`, the transfer spectral projection overlap, the Feshbach block
derivative rows, FVIR pole isolation, or canonical `O_H` authority.

## Executable Witness

The runner checks a self-adjoint `2x2` analytic kernel family

```text
K_alpha(x) = [[g^2/M + alpha*x, g],
              [g,                 M]]
```

with fixed `g=0.3`, `M=2`, fixed source vector `e_s`, and fixed pole at
`x=0`.  Every family member has the same `K(0)`, the same source vector, the
same nullvector, and the same Feshbach denominator zero.  But

```text
D_eff,alpha'(0) = alpha,
Res_alpha = 1/alpha.
```

The checked `alpha` rows vary the residue by `8x` while preserving the
same-pole operator data at `x=0`.  Therefore the derivative row is genuinely
load-bearing; it cannot be inferred from the denominator zero, source carrier,
or same operator value at the pole.

## Literature And Mathematics Search

Targeted references used as context, not as imported PR230 proof rows:

- Feshbach projection/operator formalism: H. Feshbach, *Unified Theory of
  Nuclear Reactions*, Annals of Physics 5 (1958), doi:10.1016/0003-4916(58)90007-1,
  https://www.osti.gov/biblio/4272316.
- Feshbach projection flexibility and the need for explicit projection
  representations in quantitative calculations: H. Feshbach, *A Unified Theory
  of Nuclear Reactions. Part II*, Annals of Physics 19 (1962),
  doi:10.1016/0003-4916(62)90221-X, https://www.osti.gov/biblio/4796566.
- Lattice reflection positivity and transfer matrices: K. Osterwalder and
  E. Seiler, *Gauge field theories on a lattice*, Annals of Physics 110 (1978),
  doi:10.1016/0003-4916(78)90039-8,
  https://oamonitor.ireland.openaire.eu/rpo/rcsi/search/publication?pid=10.1016%2F0003-4916%2878%2990039-8.
- Analytic perturbation / spectral projection standard reference: T. Kato,
  *Perturbation theory for linear operators*, Springer (1966),
  doi:10.1007/978-3-662-12678-3.
- Analytic Fredholm theorem: used only as meromorphic inverse-family context.
- Lattice correlator spectral matrix context: A. C. Lichtl, *The Spectral
  Structure of Correlator Matrices*, PoS LAT2007 (2007), arXiv:0711.4072.
- Kallen-Lehmann/Stieltjes scalar correlator context: D. Dudal, O. Oliveira,
  M. Roelfs, *Kallen-Lehmann Spectral Representation of the Scalar SU(2)
  Glueball*, EPJC 82 (2022), arXiv:2103.11846.
- Krein/Birman-Schwinger/Fredholm determinant formulas: useful mathematical
  analogies for reduced determinants, but they still require derivative and
  projection data at the zero.

## Boundary

This block preserves the Schur-complement K-prime sufficiency theorem: if a
future artifact supplies same-surface `A/B/C` kernel rows and pole derivatives,
then `D_eff'(pole)` is computable.  It also preserves the source-pole operator
construction: once a source pole and inverse derivative exist, an `O_sp` with
unit source-pole residue can be defined.

Neither is current PR230 closure.  The current surface lacks:

- direct row `<l_*, K'(x_*) r_*>`;
- transfer overlap row `<O_s Omega, P_* O_s Omega>` with isolated-pole/FVIR
  authority;
- Feshbach derivative rows `P K' P`, `P K' Q`, `Q K' P`, and `Q K' Q` in a
  certified neutral scalar split;
- canonical `O_H`/source-overlap or strict physical W/Z response authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use finite-prefix moments, Pade rows, or finite endpoint secants
as residue authority.  It does not infer Schur `A/B/C` rows from source-only
`C_ss` data.  It does not identify `O_s` or `O_sp` with canonical `O_H`.

It does not use `H_unit`, Ward, `y_t_bare`, observed targets, `alpha_LM`,
plaquette/`u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block66_microscopic_kprime_row_obstruction.py
python3 scripts/frontier_yt_pr230_block66_microscopic_kprime_row_obstruction.py
# SUMMARY: PASS=14 FAIL=0
```
