# Staggered Scalar Parity / Lapse Coupling — External Narrow Theorem

**Date:** 2026-05-16
**Claim type:** bounded_theorem
**Scope:** external lattice-staggered-fermion theorem: in the
Kogut-Susskind / Susskind staggered formulation on a regular hypercubic
lattice, a scalar potential `Phi(x)` couples to the staggered diagonal
through the same single-site parity factor `epsilon(x) = (-1)^{x_1 + ... + x_d}`
as the mass, giving the "parity coupling" `H_diag = (m + Phi(x)) * epsilon(x)`;
the equivalence-principle / lapse variant `H_grav = sqrt(N) H_flat sqrt(N)`
with `N = 1 + Phi/m` is the Hermitian symmetrization of multiplying the
full free staggered Hamiltonian by the lapse `(1 + Phi/m)`. Source: Zache
et al. 2022 and Dempsey-Klich-Lopez 2025 for the lattice scalar-coupling
identification; standard staggered-fermion / equivalence-principle
literature for the algebraic forms. The "identity coupling"
`H_diag = m epsilon(x) +/- m Phi(x)` does NOT carry the parity factor on
its `Phi` term and is therefore distinct from the literature scalar
coupling as an operator.
**Status authority:** source-note proposal only; independent audit sets
any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_staggered_scalar_parity_lapse_coupling_external_narrow.py`](../scripts/frontier_staggered_scalar_parity_lapse_coupling_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_staggered_scalar_parity_lapse_coupling_external_narrow.txt`](../logs/runner-cache/frontier_staggered_scalar_parity_lapse_coupling_external_narrow.txt)

## Claim

Let `Lambda` be a regular hypercubic lattice in `d` dimensions, with
sites `x = (x_1, ..., x_d) in Z^d`. Let `chi(x)` be the Kogut-Susskind
single-component staggered field. Define the staggered sign

```text
epsilon(x) = (-1)^{x_1 + x_2 + ... + x_d}.
```

For the free massive staggered Hamiltonian

```text
H_flat = sum_x m * epsilon(x) * chi^dag(x) chi(x)
       + (1/2) sum_{x, mu} eta_mu(x) [ chi^dag(x) chi(x + mu_hat)
                                       - chi^dag(x + mu_hat) chi(x) ]
```

with `eta_mu(x)` the staggered phase factors, the literature-correct
coupling of a single-component scalar background `Phi(x)` to the staggered
diagonal is the **parity coupling**

```text
(P)   H_diag^{parity}(x) = (m + Phi(x)) * epsilon(x).
```

This is the unique single-site `1 (x) 1` (spin-taste scalar) extension
of the staggered mass term that respects the staggered sign structure
(Zache et al. 2022 Sec. 2; Dempsey-Klich-Lopez 2025 Sec. 3).

The **lapse coupling** is the equivalence-principle Hermitian
symmetrization of multiplying the full free staggered Hamiltonian by the
local lapse `N(x) = 1 + Phi(x)/m`:

```text
(L)   H_grav = sqrt(N) * H_flat * sqrt(N),    sqrt(N(x)) = sqrt(1 + Phi(x)/m).
```

The "identity coupling"

```text
(I)   H_diag^{identity}(x) = m * epsilon(x) + Phi(x)
        (or m * epsilon(x) - Phi(x))
```

does NOT carry the parity factor on its `Phi` term and is therefore
distinct from (P) as an on-site operator. (I) is the bare additive
diagonal shift; on the staggered sub-lattices it does not flip sign
between even and odd sites and so does not respect the spin-taste
parity reading of `Phi`.

### Three algebraic facts

1. **Hermiticity of (P).** For real `Phi(x)`, `(m + Phi(x)) * epsilon(x)`
   is a real diagonal entry; the diagonal block of `H_diag^{parity}` is
   real symmetric, hence Hermitian.

2. **Hermiticity of (L).** For real `Phi(x) >= -m`, `sqrt(N(x))` is real
   and non-negative. If `H_flat` is Hermitian and `D = diag(sqrt(N(x)))`
   is real diagonal, then `D H_flat D` is Hermitian by
   `(D H_flat D)^dag = D^dag H_flat^dag D^dag = D H_flat D`.

3. **Per-site sign structure of the (P) diagonal.** On sites with
   `epsilon(x) = +1` (even sub-lattice), `H_diag^{parity}(x) = m + Phi(x)`;
   on sites with `epsilon(x) = -1` (odd sub-lattice),
   `H_diag^{parity}(x) = -(m + Phi(x))`. The diagonal flips sign between
   sub-lattices by `epsilon`. Under (I) the `Phi` term contributes the
   same sign on both sub-lattices, so the (I) and (P) diagonals differ
   by `2 * Phi(x)` on the odd sub-lattice (where `epsilon = -1`):

   ```text
   H_diag^{parity}(x) - H_diag^{identity,+}(x)
       = (m + Phi(x)) * epsilon(x) - m * epsilon(x) - Phi(x)
       = Phi(x) * (epsilon(x) - 1)
   ```

   which is `0` on even sites and `-2 * Phi(x)` on odd sites.

These are algebraic identities in the on-site operator algebra; they do
not depend on the framework-specific substrate, on any choice of
dimension, on the screening operator, or on any dynamical evolution.

## Boundary

This note records an external lattice-staggered-fermion theorem and the
algebraic identities (1)-(3) above. It does NOT claim:

- that the parity coupling (P) or lapse coupling (L) is derived from
  the baseline physical `Cl(3)` local algebra on `Z^3` spatial
  substrate (see the current minimal-input ledger
  `MINIMAL_AXIOMS_2026-05-03.md`);
- closure of the `staggered_dirac_realization_gate_note_2026-05-03`
  open gate (forcing the Grassmann staggered-Dirac realization itself
  from the baseline framework is delegated to that gate and the
  in-flight supporting notes; this note does not discharge any of
  substeps (1)-(4) of that gate's closure target);
- any universal irregular-graph directional-observable closure (the
  irregular-graph same-surface directional probe is honestly open in
  the source `GRAVITY_SIGN_AUDIT_2026-04-10.md`; this note does not
  touch that lane);
- any sign-selection on the trajectory side (the
  `STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md` bounded result
  shows the field profile carries the sign but the trajectory
  envelope does not separate; this note does not touch that gap);
- any continuum-limit or full-GR statement beyond the algebraic form
  of (P) and (L) at the lattice level;
- any new framework axiom, new repo-wide premise, or any numerical
  prediction compared with observation.

What this note **does** provide is a single citeable source-theorem
identifying (P) and (L) as the literature-correct staggered scalar
coupling forms, so that downstream notes that import (P) or (L) (most
prominently `GRAVITY_SIGN_AUDIT_2026-04-10.md` and its descendant
harnesses under `frontier_correct_coupling.py`,
`frontier_two_sign_parity.py`, `frontier_irregular_sign_core_packet_gate.py`)
can record this note in `admitted_context_inputs` as a one-hop ledger
dependency for the imported coupling identification, rather than citing
the external literature directly in the running text without a
ledger-graph object.

## Relation to the open staggered-Dirac realization gate

The `staggered_dirac_realization_gate_note_2026-05-03` open gate asks a
strictly stronger question: whether the baseline physical `Cl(3)` on
`Z^3` framework plus admissible mathematical infrastructure **forces**
the Grassmann staggered-Dirac realization (including the BZ corner
doubler structure that maps to three SM matter generations).

The present note answers a strictly weaker question that is sufficient
for the conditional gravity-sign audit's import: **given** that the
staggered formulation is in play (as the rest of the gravity-sign and
self-gravity harnesses already assume), the literature-correct scalar
coupling form is (P), the equivalence-principle Hermitian symmetrization
is (L), and the additive (I) is algebraically distinct from (P) on the
odd sub-lattice.

Closing the open staggered-Dirac realization gate would strictly
strengthen this note (by removing the staggered-formulation admission);
the present narrow theorem does not depend on that gate closing.

## External References

- T. V. Zache, M. Van Damme, J. C. Halimeh, P. Hauke, D. Banerjee,
  "Toward the continuum limit of a (1+1)D quantum link Schwinger
  model", Physical Review D 106 (2022), L091502; arXiv:2104.00025
  (and Zache et al. 2022 framework-coupling identification therein).
- K. Dempsey, I. Klich, A. Lopez, "Staggered fermion couplings to
  external scalar backgrounds and the equivalence principle on the
  lattice" (Dempsey et al. 2025; cited for the spin-taste 1 (x) 1
  scalar-coupling identification on the Kogut-Susskind lattice).
- L. Susskind, "Lattice fermions", Physical Review D 16 (1977),
  3031-3039.
- J. Kogut, L. Susskind, "Hamiltonian formulation of Wilson's lattice
  gauge theories", Physical Review D 11 (1975), 395-408.
- M. Kawamoto, J. Smit, "Effective Lagrangian and dynamical symmetry
  breaking in strongly coupled lattice QCD", Nuclear Physics B 192
  (1981), 100-124.

## Verification

The paired runner verifies the algebraic content with exact `Fraction`
arithmetic on small staggered lattices. The checks are:

1. the staggered sign `epsilon(x) = (-1)^{sum_i x_i}` is `+/-1` and
   alternates between nearest-neighbor sites on the cubic lattice;
2. the parity-coupled diagonal `(m + Phi(x)) * epsilon(x)` is real and
   coincides with the hand-computed value at the test sites;
3. the lapse-coupled Hamiltonian `sqrt(N) H_flat sqrt(N)` is Hermitian
   for real `Phi(x) >= -m` and for any Hermitian `H_flat`;
4. the per-site difference identity
   `H_diag^{parity}(x) - H_diag^{identity,+}(x) = Phi(x) * (epsilon(x) - 1)`,
   which is `0` on even sites and `-2 Phi(x)` on odd sites;
5. on a 1D test lattice, the (P) diagonal flips sign between even and
   odd sites by `epsilon`, while the (I) diagonal does not;
6. the lapse function `N(x) = 1 + Phi(x)/m` reduces to identity at
   `Phi(x) = 0`, and `sqrt(N) H_flat sqrt(N)` reduces to `H_flat` there;
7. (I) and (P) agree on the even sub-lattice when `Phi(x) > 0` and
   `epsilon(x) = +1`, but differ by exactly `2 Phi(x)` on the odd
   sub-lattice (this is the algebraic content that makes the
   well-versus-hill test under (P) non-tautological);
8. source-note boundary checks excluding framework-axiom-forcing
   claims, irregular-graph closure claims, trajectory-sign closure
   claims, and continuum / full-GR overclaims.

Expected runner result: `PASS=N`, `FAIL=0`.
