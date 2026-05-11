# Tensor Network Connection Note

**Status:** support - structural or confirmatory support note
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-05-02):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "The
registered runner reproduces the four computational gates, but the
note's broader bridge to AdS/CFT, Ryu-Takayanagi, and holographic-
principle language is interpretive and not derived by the runner."
This rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported content
of this note is the four computational gates reproduced live by the
registered runner
[`scripts/frontier_tensor_network_connection.py`](../scripts/frontier_tensor_network_connection.py):
Test 1 (propagator-as-MPO bond dimension equals Ny on tested 2D
lattices), Test 2 (CFT scaling `S = (c/6) ln(L), c=1.09, R^2=0.9997`;
2D area law `S = 0.82 * boundary - 0.47, R^2=0.9996`; mutual
information `~d^{-0.86}`), Test 3 (gravitational bond dimension drop
8 → 7 at f=20), and Test 4 (entropy decreases monotonically with
gravitational coupling, approximately linear `S ~ -0.36 g + 5.77,
R^2=0.975`). The §"Interpretation" bridge to AdS/CFT, Swingle 2012,
Pastawski et al. 2015, Ryu-Takayanagi, and holographic-principle
language is **interpretive** and is not derived by the runner; the
supported perimeter is just the four computational gates, not the
holographic narrative around them.

## Result

The path-sum propagator on a layered graph is formally a Matrix Product
Operator (MPO). Gravity modifies the singular value spectrum of the
transfer matrices, reducing the effective bond dimension near
gravitational sources. All four gates pass.

## Key findings

### Test 1: Propagator as MPO (PASS)
On a 2D lattice (Nx x Ny), the propagator from layer 0 to Nx-1
decomposes as a product of Ny x Ny transfer matrices. Bond dimension
equals Ny for all lattice sizes tested (4, 6, 8). Gravity changes
matrix elements but not the formal bond dimension.

### Test 2: Entanglement structure (PASS)
- 1D CFT scaling confirmed: S = (c/6) ln(L) with c = 1.09 (expect 1.0
  for free fermion CFT with open boundaries). R^2 = 0.9997.
- 2D area law: S = 0.82 * boundary - 0.47, R^2 = 0.9996.
- Mutual information decays as d^{-0.86} between separated regions.

### Test 3: Gravitational bond dimension (PASS)
At strong gravity (f=20), the effective bond dimension at the center
drops from 8 to 7 and the singular value condition number grows from
112 to 641507. Gravity concentrates information into fewer modes --
the holographic principle in tensor network language.

### Test 4: Ryu-Takayanagi (PASS)
Entropy decreases monotonically with gravitational coupling: from
S=6.07 at g=0 to S=2.43 at g=10. The relationship is approximately
linear (S ~ -0.36*g + 5.77, R^2 = 0.975) rather than S ~ 1/g.
This suggests an exponential suppression of entanglement by the
gravitational field, consistent with the transfer matrix structure
where field enters as exp(-f).

## Interpretation

The propagator-as-MPO result connects the path-sum framework to the
AdS/CFT tensor network program (Swingle 2012, Pastawski et al. 2015).
The area-law entropy (R^2=0.9996) and CFT central charge (c=1.09)
emerge naturally. Gravity acts by modifying the singular value spectrum
of transfer matrices, effectively reducing the bond dimension -- a
discrete realization of the holographic principle.

## Script
`scripts/frontier_tensor_network_connection.py`
