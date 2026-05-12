# PR230 Block70 Schur/Feshbach K-Prime Residue Theorem

```yaml
actual_current_surface_status: exact-support / Block70 Schur-Feshbach K-prime residue theorem; physical rows absent
conditional_surface_status: conditional-support if future same-surface Cl(3)/Z3 Schur/Feshbach rows supply the listed hypotheses
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The theorem reduces the source-Higgs residue to concrete same-surface rows, but those physical rows and the canonical-Higgs bridge are not present on the current PR230 surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_pr230_block70_schur_feshbach_kprime_residue_theorem.py`  
**Certificate:** `outputs/yt_pr230_block70_schur_feshbach_kprime_residue_theorem_2026-05-12.json`

## Purpose

This block sharpens the PR230 Schur/K-prime route.  Existing PR230 gates already
say that the scalar pole location is not enough: the LSZ residue depends on the
derivative row at the pole.  The current Schur row contract asks for same-surface
`A/B/C` kernel rows and derivatives, while the source-Higgs builder asks for
pole residues `Res_C_ss`, `Res_C_sH`, and `Res_C_HH`.

The theorem below supplies the missing algebraic bridge between those two
contracts.  It proves, on the same Cl(3)/Z3 source surface and after analytic
contact terms are separated, that a strict Schur/Feshbach K-prime row fixes the
pole residue:

```text
Res C_ab = (a r) (l b) / (l K_prime(x_pole) r).
```

For the source-Higgs row this is the source projection numerator divided by the
K-prime derivative denominator.  With PR230's one-source-coordinate Schur
partition,

```text
K(x) = [[A(x), B(x)],
        [D(x), C(x)]],

D_eff(x) = A(x) - B(x) C(x)^(-1) D(x),

Res C_sH = (h_s - B C^(-1) h_Q) / D_eff_prime(x_pole).
```

No extra minus sign appears under the row convention used here:

```text
C_ab(x) = a K(x)^(-1) b + analytic contact,
Res C_ab = lim_{x -> x_pole} (x - x_pole) C_ab(x).
```

If a production row instead defines the pole variable as `p_pole^2 - p^2`, or
uses `C = -K^(-1)`, that row must carry the corresponding sign convention.

## A_min And Forbidden Inputs

Allowed premise set for this theorem:

- same-surface Cl(3)/Z3 scalar source kernel family `K(x)`;
- analytic dependence on the declared scalar-pole variable `x`;
- a strict Schur/Feshbach partition of the neutral scalar kernel;
- a simple isolated pole;
- left/right null vectors at the pole;
- analytic contact-term separation.

Forbidden as load-bearing inputs:

- `H_unit`;
- `yt_ward_identity`;
- `y_t_bare`;
- `alpha_LM`;
- plaquette or `u0`;
- observed target selectors;
- alias imports.

The runner records all forbidden-firewall flags as false and loads no physical
row data.

## First-Principles Derivation

Let `K(x)` be the inverse connected scalar kernel after analytic contact terms
are separated.  Assume `K(x)` is analytic near `x_pole`, and that `K(x_pole)`
has a simple zero eigenvalue with right and left null vectors

```text
K(x_pole) r = 0,
l K(x_pole) = 0,
l K_prime(x_pole) r != 0.
```

For a simple analytic eigenvalue branch, the singular spectral projector is
rank one.  The derivative of that eigenvalue at the crossing is

```text
lambda_prime(x_pole) = (l K_prime(x_pole) r) / (l r).
```

Therefore the inverse kernel has Laurent singular part

```text
K(x)^(-1) = r l / ((x - x_pole) l K_prime(x_pole) r) + analytic.
```

Multiplying by any source/probe covector `a` and probe vector `b` gives

```text
C_ab(x) = a K(x)^(-1) b + analytic contact
        = ((a r) (l b)) / ((x - x_pole) l K_prime(x_pole) r) + analytic,
```

so

```text
Res C_ab = (a r) (l b) / (l K_prime(x_pole) r).
```

The expression is independent of the normalization of `l` and `r`, since the
same rescalings multiply numerator and denominator.

## Schur/Feshbach Row Form

Use the PR230 row contract's source-plus-orthogonal partition:

```text
K = [[A, B],
     [D, C]],
```

where `C(x_pole)` is invertible.  The Feshbach row is

```text
D_eff = A - B C^(-1) D.
```

At a one-source-coordinate pole, `D_eff(x_pole) = 0`, and the right/left null
vectors can be chosen as

```text
r = [1, -C^(-1) D]^T,
l = [1, -B C^(-1)].
```

Direct differentiation gives

```text
D_eff_prime =
  A_prime
  - B_prime C^(-1) D
  - B C^(-1) D_prime
  + B C^(-1) C_prime C^(-1) D
  = l K_prime r.
```

For source-source:

```text
Res C_ss = 1 / D_eff_prime.
```

For source-Higgs, write the certified Higgs probe in the same partition as
`h = [h_s, h_Q]^T`.  Then

```text
Res C_sH = (h_s - B C^(-1) h_Q) / D_eff_prime.
```

That numerator is exactly the Feshbach-projected source-Higgs overlap.  It is
not allowed to be set to one, and it is not an `O_sp = O_H` certificate by
itself.

## LSZ Convention

If `Res C_ss = Z_s` in the declared pole variable, the Legendre source-pole
operator is

```text
O_sp = sqrt(dGamma_ss/dx | pole) O_s,
dGamma_ss/dx | pole = 1 / Z_s.
```

For the one-source Schur row above, `Z_s = 1 / D_eff_prime`, so the row supplies
the LSZ source-side normalization.  In a positive Euclidean scalar channel the
production row should choose the pole variable/sign so `Z_s > 0`.  If the
certified row is non-Hermitian or uses a signed convention, the sign/phase must
be explicit in the certificate before a source-Higgs builder consumes it.

Analytic contact terms do not change the residue:

```text
lim_{x -> x_pole} (x - x_pole) analytic_contact(x) = 0.
```

Contact separation is still a required certificate field, because finite-shell
fits can otherwise confuse regular terms with pole terms.

## Certificate Fields Required

| Hypothesis | Future certificate fields that discharge it |
|---|---|
| Same surface | `same_surface_cl3_z3`, `phase` |
| Analytic kernel family | `kernel_family_variable`, `schur_form`, `partition_certificate` |
| Simple isolated pole | `pole_control.isolated_scalar_pole_passed`, `pole_control.pole_location_x` |
| Left/right null vectors | `left_null_covector`, `right_null_vector`, `left_right_normalization_convention` |
| K-prime derivative row | `K_prime_at_pole` or `D_eff_prime_at_pole`, `kprime_denominator` |
| Source-Higgs numerator | `source_projection_numerator`, `source_coordinate`, `canonical_higgs_operator.operator_id` |
| Contact separation | `analytic_contact_terms_separated`, `pole_residue_rows` |
| LSZ convention | `Dprime_ss_at_pole`, `Res_C_ss`, `selected_source_side_normalization` |
| Forbidden-import firewall | false flags for `used_hunit_matrix_element_readout`, `used_yt_ward_identity`, `used_y_t_bare`, `used_alpha_lm`, `used_plaquette_or_u0`, `used_observed_target_selectors`, `used_alias_imports` |

These fields are deliberately aligned with the existing Schur row contract and
source-Higgs certificate builder.  A future row can populate
`Res_C_ss`, `Res_C_sH`, and `Res_C_HH` only after the operator/projection side
is certified on the same surface.

## Toy Exact Check

The runner constructs a four-dimensional analytic kernel

```text
K(x) = K0 + (x - x_pole) K1 + (x - x_pole)^2 K2
```

with an exact Schur zero at `x_pole = 0.37` and invertible orthogonal block
`C`.  It verifies:

- `K0 r = 0` and `l K0 = 0`;
- the smallest singular value is numerical zero while the other singular
  values are separated;
- `D_eff_prime = l K1 r = 0.41849338680585607`;
- `Res C_sH = 1.0159108117176803`;
- the Laurent limit with analytic contact terms converges to that residue;
- the formula is invariant under a general similarity basis change;
- the Schur derivative row is invariant under a block-preserving reparametrized
  orthogonal sector.

Validation:

```text
python3 scripts/frontier_yt_pr230_block70_schur_feshbach_kprime_residue_theorem.py
# SUMMARY: PASS=16 FAIL=0
```

## Targeted Math Check

The proof above is self-contained in finite dimension.  I used a narrow
math-literature check only to verify that the ingredients match standard names:
analytic simple-eigenvalue perturbation, the Schur complement inverse formula,
and Feshbach/Schur isospectral reduction.  No literature value or physical
normalization is imported as proof input.

References used for terminology sanity checks:

- Andrew V. Knyazev and Merico E. Argentati, ["First-order Perturbation Theory
  for Eigenvalues and Eigenvectors"](https://arxiv.org/abs/1903.00785),
  arXiv:1903.00785.
- John A. Gubner, ["Block Matrix
  Formulas"](https://gubner.ece.wisc.edu/notes/BlockMatrixFormulas.pdf),
  University of Wisconsin-Madison.
- Bach, Chen, Froehlich, and Sigal, ["Smooth Feshbach map and
  operator-theoretic renormalization group
  methods"](https://www.sciencedirect.com/science/article/pii/S0022123603000570),
  Journal of Functional Analysis 203 (2003).

## Claim Boundary

This is exact support, not physical PR230 closure.  It proves that the
source-Higgs pole residue is computable from strict same-surface Schur/Feshbach
rows if those rows exist.  It does not assert that current PR230 physical
Schur rows exist, does not identify `O_sp` with `O_H`, and does not authorize
retained or `proposed_retained` wording.

The current surface remains open because the required physical rows are absent:
same-surface Schur/Feshbach `A/B/C` rows, certified `O_H/C_sH/C_HH` pole rows,
or an equivalent same-source W/Z response identity must still be produced and
passed through the existing builder, Gram-purity postprocessor, assembly gate,
and campaign status gate.
