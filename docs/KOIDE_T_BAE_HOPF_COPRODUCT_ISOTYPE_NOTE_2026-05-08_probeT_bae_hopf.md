# Koide BAE Probe T — Canonical Hopf-Coproduct Obstruction

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py`](../scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py)
**Cached output:** [`logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt`](../logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt)

## Claim Boundary

This note tests one specific attack vector for deriving the Brannen
Amplitude Equipartition condition

```text
|b|^2 / a^2 = 1/2
```

from the `C_3`-equivariant Hermitian circulant

```text
H_circ = a I + b C + conjugate(b) C^2.
```

The tested vector is the **canonical group-ring Hopf coproduct** on
`C[C_3]`:

```text
Delta(C^p) = C^p tensor C^p,
epsilon(C^p) = 1,
S(C^p) = C^{-p}.
```

The bounded result is negative:

> Under the canonical group-ring Hopf coproduct, `Delta(H_circ)` lives
> on the three diagonal tensor-basis components
> `(0,0)`, `(1,1)`, and `(2,2)`. Its `(i,j)` isotype eigenvalues depend
> only on `(i+j) mod 3`, so the nine coproduct isotypes collapse to the
> three original `H_circ` eigenvalues, each with multiplicity three.
> Natural symmetric balance/minimality functionals on this coproduct
> therefore reduce to symmetric functionals of the original eigenvalue
> multiset and do not force the BAE ratio. In the tested balance
> criteria, the extremum is `b = 0`, not `|b|/a = 1/sqrt(2)`.

This does **not** prove that every possible Hopf-algebraic, categorical,
or tensor-structure route to BAE is impossible. It only closes the
canonical group-ring coproduct route tested here.

## Repo Language And Inputs

The repo baseline is the physical `Cl(3)` local algebra on the `Z^3`
spatial substrate; this note does not add a new repo-wide axiom.
The following linked inputs are source/audit-lineage dependencies, not
status promotions by this note:

| Input | Role in this note |
|---|---|
| [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | baseline physical `Cl(3)` local algebra and `Z^3` spatial substrate |
| [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) | source lineage for the `hw=1` `C_3[111]` triplet |
| [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) | source lineage for the `C_3`-equivariant circulant form and eigenvalue formula |
| [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) | source lineage for the algebraic BAE target |
| [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) | related bounded obstruction for the operator-level route |

External mathematics used here is standard finite-group-ring Hopf
algebra and character theory: the canonical group-ring construction,
tensor-product algebra, and the one-dimensional character decomposition
of `C_3 x C_3`. These are mathematical tools used on the scoped
objects above, not new physical primitives.

## Computation

Let `A = C[C_3]` with basis `{1, C, C^2}` and `C^3 = 1`. For the
canonical group-ring Hopf coproduct,

```text
Delta(H_circ)
  = a (I tensor I)
    + b (C tensor C)
    + conjugate(b) (C^2 tensor C^2).
```

So `Delta(H_circ)` is supported only on the three diagonal basis
vectors of the nine-dimensional tensor algebra `A tensor A`.

For characters of `C_3 x C_3`,

```text
chi_ij(C^p, C^q) = omega^(i p + j q),
```

the isotype eigenvalue is

```text
mu_ij(a,b)
  = a + b omega^(i+j) + conjugate(b) omega^-(i+j)
  = a + 2 |b| cos(arg(b) + 2 pi (i+j)/3).
```

Thus `mu_ij` depends only on `(i+j) mod 3`. The nine isotypes form
three classes, each of multiplicity three, with representatives equal
to the original `H_circ` eigenvalues:

```text
spec(Delta(H_circ)) = {lambda_0, lambda_0, lambda_0,
                       lambda_1, lambda_1, lambda_1,
                       lambda_2, lambda_2, lambda_2}.
```

Consequently,

```text
Tr(Delta(H)^n) = 3 Tr(H^n)
```

for the checked powers `n = 1, 2, 3, 4`.

## What The Runner Checks

The paired runner verifies:

1. The `C_3` cycle and circulant eigenvalue formula.
2. The canonical group-ring Hopf structure on the chosen basis:
   coproduct, counit, antipode, coassociativity, and antipode
   involution.
3. The explicit support of `Delta(H_circ)` on only the diagonal tensor
   components.
4. The collapse of `(i,j)` isotype eigenvalues to the original
   `H_circ` eigenvalues with multiplicity three.
5. `Var(mu_ij) = 0` only at `b = 0`, while BAE is not stationary for
   that balance functional.
6. Frobenius central-spread, spectral entropy, and spectral range
   extremize at `b = 0`, not BAE.
7. The power-sum relation `Tr(Delta(H)^n) = 3 Tr(H^n)` for
   `n = 1..4`.
8. Antipode, convolution, counit, higher-coproduct, and convention
   checks do not introduce a BAE-pinning constraint.

## What This Does Not Claim

- Does not close BAE.
- Does not reduce the BAE admission count.
- Does not add a new repo-wide axiom.
- Does not promote Hopf algebra to a physical primitive.
- Does not promote any parent dependency or sibling probe to retained
  status.
- Does not prove all tensor-structure routes impossible; it only tests
  the canonical group-ring coproduct route.
- Does not import observed lepton masses, fitted coefficients, or
  lattice Monte Carlo measurements.

## Audit Handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Canonical group-ring Hopf coproduct on C[C_3] sends the scoped
  C_3-equivariant circulant H_circ to a three-component diagonal
  tensor-algebra element whose C_3 x C_3 isotype eigenvalues collapse
  to the original H_circ eigenvalues with multiplicity three. Natural
  symmetric balance/minimality functionals tested on this coproduct do
  not force |b|^2/a^2 = 1/2; their extrema occur at b = 0.
status_authority: independent audit lane only
admitted_context_inputs:
  - BAE target |b|^2/a^2 = 1/2 remains an admitted target condition.
  - canonical group-ring Hopf algebra on C[C_3] used as standard
    mathematical toolkit, not as a physical axiom.
forbidden_imports_used: false
audit_required_before_effective_status_change: true
```

## References

- Sweedler M.E. (1969). *Hopf Algebras*. Benjamin.
- Kassel C. (1995). *Quantum Groups*. Graduate Texts in Mathematics 155.
- Majid S. (1995). *Foundations of Quantum Group Theory*.
