# Graph Laplacian KG Core Card Note

**Date:** 2026-04-10  
**Harnesses:**  
- [`scripts/frontier_graph_kg_16card.py`](../scripts/frontier_graph_kg_16card.py)  
- [`scripts/frontier_graph_laplacian_kg.py`](../scripts/frontier_graph_laplacian_kg.py)  
- [`scripts/frontier_geometric_gravity_v2.py`](../scripts/frontier_geometric_gravity_v2.py)

This note freezes the audited branch read for the graph-Laplacian lane after
rerunning the checked-in scripts and correcting the most important card logic
errors.

## Summary

The graph-Laplacian lane is **promising, but not a perfect card**.

- the checked-in graph core card now reruns to **13/16**
- the free regular-lattice operator really does derive the exact lattice KG law
  from nearest-neighbor connectivity
- local potential gravity on that operator is clean on the gravity rows
- the claimed `16/16` was inflated by miswired tests

## Audited Core-Card Result

Current audited score from
[`scripts/frontier_graph_kg_16card.py`](../scripts/frontier_graph_kg_16card.py):

- **13/16**

Passes:

- `C2` slit distinguishability `d_TV = 0.6934`
- `C3` null control exact
- `C4` weak-field linearity `R^2 = 1.000000`
- `C5` operating-point gravity TOWARD `+1.1885e-03`
- `C6` decoherence proxy reduces coherence (`0.9806 -> 0.0480`)
- `C7` mutual information positive
- `C8` purity stability `CV = 0.3679`
- `C9` gravity growth with propagation is all-TOWARD and monotone on the tested `N` row
- `C10` distance row is `4/4` TOWARD on the retained offsets
- `C11` exact graph-lattice KG isotropy passes: `R^2 = 0.999809`, `iso = 1.0309`
- `C12` two-path flux **proxy** gives `V = 1.0000`
- `C15` periodic/open sign agreement is `5/5`
- `C16` centroid/peak/shell panel agrees `3/3`

Fails:

- `C1` Born barrier / slit: `|I3|/P = 1.9943`
- `C13` carrier-`k` achromaticity: `CV = 1.0786`, with sign flips by `k ≈ 0.45`
- `C14` split mass vs gravity susceptibility: response is highly linear in `g`
  and nearly rank-1, but the sign flips at large mass (`m = 0.8`), so the row
  is not cleanly retained

## Important Audit Corrections

The earlier `16/16` story was not acceptable as written. The main corrections:

1. `C1` Born had the pass condition reversed.
   - The script had been treating **large** `|I3|/P` as a pass.
   - The corrected card now requires Born interference to be small.

2. `C13` achromaticity was tautological.
   - The script looped over `k0`, but always used the same zero-carrier packet.
   - The corrected row now uses actual carrier packets and matched travel depth.

3. `C14` equivalence/split coupling was tautological.
   - The script computed `F/m` directly from a potential already proportional to `m`,
     so the row could only report a trivial pass.
   - The corrected row now checks whether the response separates into an
     independent mass profile and an independent gravity-coupling profile, while
     keeping the sign stable.

4. `C15` boundary robustness was misnamed.
   - The original row compared two periodic lattices of different size.
   - The corrected row compares periodic vs open boundaries on the same geometry.

5. `C11` was checked against the wrong sign in the prototype script.
   - The prototype had treated the spectrum of `-L` as the graph-Laplacian
     eigenvalue story.
   - The corrected prototype now checks the exact graph-lattice dispersion
     `omega^2 = m^2 + lambda_L(k)` and its low-`k` isotropy.

## Interpretation

This lane still matters.

- It is the cleanest **local, no-coin, no-FFT** route on the branch that derives
  the free lattice KG law from the graph operator itself.
- It shows that several gravity positives survive without coin-mediated mixing.
- But it is not yet a replacement for the retained lanes because:
  - Born barrier behavior is bad
  - carrier-`k` sensitivity is still strong
  - the mass/gravity split is not clean at larger mass
  - the current gauge row is only a two-path flux proxy, not yet a full retained
    3D gauge-loop closure

## Carry-Forward

The next graph-Laplacian attacks should be narrow:

1. fix or explain the Born barrier failure under local blocking
2. redesign the gauge row from a proxy into a genuine 3D loop/flux harness
3. map the `k`-sign flip boundary in the local leapfrog lane
4. determine whether the `m=0.8` split-row sign flip is a continuum-breakdown
   artifact or a deeper coupling problem
