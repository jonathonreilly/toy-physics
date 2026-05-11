# Koide BAE Probe Y: Topological Decoupling on the C3 hw=1 Triplet

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py`](../scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py)
**Cache:** [`logs/runner-cache/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.txt`](../logs/runner-cache/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.txt)

## Claim

This bounded note tests one route toward the Brannen amplitude
equipartition condition (BAE), the amplitude-ratio condition
`|b|^2/a^2 = 1/2` for the `C3`-equivariant Hermitian circulant

```text
H(a,b) = a I + b C + conjugate(b) C^2
```

on the `hw=1` BZ-corner triplet. The route tested here is narrow:
whether standard topological or index-theoretic invariants of the
`C3` representation on the triplet, without an additional amplitude
bridge, force the BAE ratio.

**Bounded theorem.** On the `hw=1` triplet with the `C3[111]` action,
the following data are integer, finite-group, or representation-class
data independent of the continuous circulant amplitude `(a,b)`:

1. the `C3` representation-ring class
   `K_C3(pt) = R(C3) = Z[chi_0] + Z[chi_1] + Z[chi_2]`, with the
   regular triplet class `(1,1,1)`;
2. equivariant index data built only from `C3` isotype zero-mode
   counts;
3. the point-base Chern character / anomaly-trace data, which reduces
   to rank and character traces for this finite representation;
4. point and equivariant point cohomology data, such as `H^0(pt,Z)=Z`
   and the usual finite `C3` torsion classes.

Therefore these topological data do not by themselves select the
specific continuous value `|b|^2/a^2 = 1/2`. A theorem that derives BAE
from topology would need a separate bridge mapping one of these
integer or representation-class invariants to the continuous amplitude
ratio. This note does not supply that bridge.

## Dependencies and Imports

Load-bearing repo dependencies:

- [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
  for the `hw=1` BZ-corner triplet and `C3[111]` action.
- [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
  for the `C3`-equivariant Hermitian circulant form.
- [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
  for the algebraic equivalence between Koide `Q=2/3` and the BAE
  ratio in this lane.

Bounded mathematical imports:

- finite-dimensional representation theory of the cyclic group `C3`;
- the elementary identity `K_G(pt)=R(G)` for a finite group `G`;
- point-base Chern character and character-trace bookkeeping;
- point and finite-group cohomology bookkeeping.

These mathematical imports are not new repo-wide axioms. They are also
not a new interpretation of the physical Cl(3) local algebra plus Z^3
spatial substrate baseline.

Context only, not load-bearing dependencies:

- Probe X and the Probe 12-30 operator-level packets are prior BAE
  obstructions, but this note does not require their audit status.
- `MINIMAL_AXIOMS_2026-05-03.md` records the physical Cl(3) local
  algebra plus Z^3 spatial substrate baseline; this note does not
  add to that baseline.

## Proof Sketch

The `C3` action on the triplet is the regular representation. Its
character is `(3,0,0)` on the conjugacy classes `1,C,C^2`, so character
orthogonality gives one copy of each complex irrep:

```text
[V] = (1,1,1) in R(C3).
```

Changing the continuous parameters `(a,b)` in the circulant operator
changes eigenvalues of an operator on the same representation space,
but it does not change the `C3` representation class. Thus the
representation-ring class is constant in `(a,b)`.

Equivariant index data built only from isotype zero-mode counts is
integer-valued. Chern-character and anomaly-trace data on a point reduce
to rank and character traces. Point cohomology and finite `C3`
cohomology are integer or finite torsion data. These objects can change
only when their discrete input changes, not continuously with the
circulant amplitude.

The BAE ratio is a single real value in a continuous amplitude
parameter. Since the topological data above are constant under sampled
changes of `(a,b)` and, by construction, do not include `(a,b)`, they
cannot select `|b|^2/a^2 = 1/2` without an extra bridge theorem.

## Boundaries

This note does not:

- close the BAE condition;
- claim that all possible topological constructions are exhausted;
- promote any parent or companion BAE obstruction;
- assert retained or audited status;
- add a new axiom, new physics primitive, or new repo-wide theory
  language;
- use PDG masses, lattice Monte Carlo values, or fitted constants.

What it does preserve is the bounded negative result for the specific
representation-class, point-index, point-character, and point-cohomology
routes tested here: those routes provide integer or finite data that
are decoupled from the continuous BAE amplitude ratio.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/cl3_koide_y_bae_topological_2026_05_10_probeY_bae_topological.py
```

Expected result:

```text
TOTAL: PASS=33 FAIL=0
```
