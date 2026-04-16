# PMNS Microscopic Pair Reconstruction Interface

## Question

If the selector outputs `(tau, q)` and the projected active/passive kernels are
independently supplied, do they recover the full PMNS-relevant microscopic
triplet pair `(D_0^trip, D_-^trip)`?

## Exact Result

Yes.

The combined interface is:

- supplied selector outputs `(tau, q)`
- the active projected Green kernel
- the passive projected Green kernel

Together these reconstruct the PMNS-relevant microscopic pair exactly:

`(tau, q, G_act, G_pass) -> (D_0^trip, D_-^trip)`.

Once that pair is known, the existing downstream solver is exact and automatic:

- branch
- passive monomial data
- active two-Higgs data
- sheet
- `H_nu`, `H_e`
- masses and PMNS

## Boundary

This note does not derive `tau`, `q`, or either projected kernel from the sole
axiom inside the same theorem. It proves a reconstruction interface only. It
also does not claim a global statement about degrees of freedom outside the
retained PMNS lepton supports.
