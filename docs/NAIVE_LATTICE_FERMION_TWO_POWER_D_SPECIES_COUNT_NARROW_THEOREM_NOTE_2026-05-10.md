# Naive Lattice Fermion 2^d Species Count — Narrow Theorem

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Scope:** exact zero-locus/species-count theorem for the standard
naive lattice Dirac operator on a hypercubic lattice. At `d = 4`, the
count is `2^4 = 16`.
**Status authority:** source-note proposal only; independent audit
sets any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_naive_lattice_fermion_two_power_d_species_count_narrow.py`](../scripts/frontier_naive_lattice_fermion_two_power_d_species_count_narrow.py)
**Cache:** [`logs/runner-cache/frontier_naive_lattice_fermion_two_power_d_species_count_narrow.txt`](../logs/runner-cache/frontier_naive_lattice_fermion_two_power_d_species_count_narrow.txt)

## Claim

Let `d >= 1` and consider the standard naive lattice Dirac operator
on the hypercubic lattice `Z^d`:

```text
D_naive(k) = (i/a) * sum_{mu=1..d} gamma_mu sin(k_mu a),
             k_mu a in (-pi, pi].
```

Using `{gamma_mu, gamma_nu} = 2 delta_mu_nu`, the squared operator
reduces to

```text
(-i a D_naive(k))^2 = (sum_mu sin^2(k_mu a)) * I.
```

Therefore `D_naive(k) = 0` iff `sin(k_mu a) = 0` for every `mu`,
so the zero locus inside the Brillouin zone is exactly
`{0, pi/a}^d`, of cardinality `2^d`. Each corner gives the usual
continuum expansion of one naive fermion species. Thus the standard
naive lattice action realizes exactly `2^d` species; at `d = 4`,
this is `16`.

## Boundary

This is a narrow lattice-field-theory theorem about a defined naive
operator. It is not a framework axiom and it consumes no framework
authority. It does not claim:

- regulator-independence of the `2^d` count;
- that the framework realizes the naive regulator rather than Wilson,
  staggered, overlap, domain-wall, or another regulator;
- that the `16` at `d = 4` is the same load-bearing `16` appearing in
  any framework hierarchy formula;
- Wilsonian transport composition of the doublers;
- closure of any hierarchy, CKM, lepton, or gravity lane.

The result is useful as an external lattice-field-theory anchor for a
standard `16` count at `d = 4`, but any project-specific use of that
integer needs a separate bridge.

## Literature Context

Nielsen and Ninomiya prove the standard species-doubling obstruction:
a local, translation-invariant, chirally symmetric lattice fermion
cannot isolate a single chiral species under the theorem's hypotheses.
This note cites that result only as context for why doublers are a
structural lattice issue. It does **not** use Nielsen-Ninomiya as a
numerical `2^d` lower-bound statement for every regulator/operator; the
`2^d` count proved here is the exact count for the naive operator above.

Karsten and Karsten-Smit are cited as published lattice-field-theory
anchors for the same naive-action species-doubling calculation and
its anomaly context.

External references:

- H. B. Nielsen and M. Ninomiya, "Absence of neutrinos on a lattice
  (I): Proof by homotopy theory", Nuclear Physics B 185 (1981) 20-40.
- H. B. Nielsen and M. Ninomiya, "Absence of neutrinos on a lattice
  (II): Intuitive topological proof", Nuclear Physics B 193 (1981)
  173-194.
- L. H. Karsten, "Lattice fermions in Euclidean space-time",
  Physics Letters B 104 (1981) 315-318.
- L. H. Karsten and J. Smit, "Lattice fermions: species doubling,
  chiral invariance and the triangle anomaly", Nuclear Physics B 183
  (1981) 103-140.

## Verification

The runner checks:

1. At `d = 4`, all `16` Brillouin-zone corners `{0, pi}^4` make
   `sum_mu sin^2(k_mu a) = 0`.
2. For `d in {1, 2, 3, 4, 5, 6}`, the count of corners is exactly
   `2^d`.
3. The gamma-matrix anticommutator reduction makes the zero condition
   equivalent to all components satisfying `sin(k_mu a) = 0`.
4. Wilson lifting, staggered reduction, and other regulator counts are
   recorded as non-load-bearing context to prevent regulator-independent
   overclaims.
5. The source note avoids framework-bridge, hierarchy, and
   regulator-independence claims.

Expected runner result: `PASS=8`, `FAIL=0`.
