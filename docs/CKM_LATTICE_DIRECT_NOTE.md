# CKM from Direct Inter-Valley Scattering on the Staggered Lattice

**Date:** 2026-04-12
**Script:** `scripts/frontier_ckm_lattice_direct.py`
**Exit code:** 0 (PASS=17, FAIL=0)

## Status

**BOUNDED negative result.**

The direct lattice computation shows that inter-valley scattering amplitudes
on the staggered lattice with Wilson term do NOT produce the CKM hierarchy
|V_us| >> |V_cb| >> |V_ub|. This is a clean route-pruning result.

## Theorem / Claim

**Claim (bounded, negative):** On Z^3_L with SU(3) gauge links and
Wilson taste-breaking term, the inter-valley scattering amplitudes T_ij
between the three hw=1 BZ corners X_1, X_2, X_3 do not exhibit a
systematic magnitude hierarchy. The CKM hierarchy cannot emerge from
this mechanism alone.

## Assumptions

1. Staggered fermion Hamiltonian on Z^3_L (L=6) with SU(3) gauge links
2. Wilson taste-breaking term with parameter r
3. Bloch wave packets centered at hw=1 BZ corners
4. Quenched gauge configurations (near-identity SU(3) links, epsilon=0.3)

## What Is Actually Proved

### Exact results

1. **Free-field C3 symmetry:** With unit gauge links, all off-diagonal
   T_ij are equal in magnitude (C3 exact to machine precision).

2. **Free-field simultaneous diagonalizability:** M_u and M_d commute
   in the free field (||[M_u, M_d]|| < 1e-10), so V_CKM is trivially
   identity. No CKM mixing without gauge fluctuations.

3. **Wilson term scales linearly:** The off-diagonal amplitudes scale
   linearly with the Wilson parameter r (verified at r = 0.5, 1.0, 2.0),
   preserving the same magnitude ratios.

### Computed (bounded) results

4. **Gauge fluctuations break C3:** With random SU(3) gauge links,
   the off-diagonal |T_ij| develop configuration-dependent differences.
   Typical C3 breaking ~ O(1) on a single configuration.

5. **No systematic hierarchy:** The ensemble average over 5 gauge
   configurations restores C3 symmetry (spread/mean = 0.12). There is
   no structural mechanism selecting |T_12| >> |T_23|.

6. **V_CKM != I with gauge links:** Gauge fluctuations break the
   simultaneous diagonalizability of M_u and M_d, producing non-trivial
   mixing. But the mixing pattern is random, not hierarchical.

### Negative result (the key finding)

7. **The inter-valley scattering route is blocked.** On the staggered
   lattice, the three BZ corners X_1 = (pi,0,0), X_2 = (0,pi,0),
   X_3 = (0,0,pi) are related by C3[111] symmetry. The Wilson term
   treats all three inter-valley transitions equally. Gauge fluctuations
   break this symmetry randomly, not hierarchically. The CKM hierarchy
   |V_us| >> |V_cb| >> |V_ub| does not emerge from this mechanism.

## What Remains Open

The CKM lane remains bounded. Possible routes forward:

1. **Radiative hierarchy:** The CKM hierarchy may arise from loop
   corrections that distinguish BZ corners through their coupling to
   the Higgs/EW sector (taste-dependent radiative corrections).

2. **Yukawa-taste interplay:** The interplay between the Yukawa sector
   and taste splitting may produce the hierarchy at the level of the
   mass matrix diagonalization, not the inter-valley scattering amplitude.

3. **Additional structure:** The CKM hierarchy may require structure
   beyond the staggered lattice + Wilson term (e.g., the full Higgs Z_3
   mechanism, if it becomes L-independent).

## How This Changes The Paper

This is a useful route-pruning result:

- **Narrows the CKM derivation space:** The direct inter-valley scattering
  mechanism is now excluded as a source of the CKM hierarchy.
- **Confirms the blocker:** The CKM lane remains bounded, consistent with
  `review.md` status.
- **Does not change gate count:** The four live gates remain:
  S^3, DM relic mapping, renormalized y_t, CKM.

The note may be cited as: "Direct lattice computation excludes
inter-valley scattering as the source of CKM hierarchy."

## Commands Run

```
python3 scripts/frontier_ckm_lattice_direct.py
```

Exit code: 0. PASS=17, FAIL=0.
