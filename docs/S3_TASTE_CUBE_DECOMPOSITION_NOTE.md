# S_3 Taste-Cube Decomposition Note

**Date:** 2026-04-17
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** proposed_retained exact structural theorem on the full taste cube;
audit pending
**Script:** `scripts/frontier_s3_action_taste_cube_decomposition.py`
**Authority role:** canonical representation-theoretic theorem for
axis-permutation symmetry on `C^8 = (C^2)^{\otimes 3}`; not a standalone
physical-flavor theorem

## Safe statement

Let `S_3` act on `C^8 = (C^2)^{\otimes 3}` by permuting tensor positions. Then:

- Hamming weight is preserved, so the computational basis splits as
  `1 + 3 + 3 + 1`
- the `hw = 0` and `hw = 3` sectors are trivial `A_1`
- each of the `hw = 1` and `hw = 2` sectors is the standard permutation
  representation `A_1 + E`
- therefore

```text
C^8 ~= 4 A_1 + 2 E
```

and the sign irrep `A_2` does not occur

This is a full-cube structural theorem. It does not by itself prove any flavor
or mass-hierarchy claim. Its safe retained-grade role is narrower: it fixes the
exact `S_3` carrier content that later generation and flavor tools are allowed
to use as an input.

## Classical results applied

- finite-group character theory for `S_3`
- the permutation-character formula `chi(pi) = |Fix(pi)|`
- standard decomposition of the three-point permutation representation as
  `A_1 + E`

## Framework-specific step

- identification of the `S_3` action as axis permutations on the taste cube
- exact computation of the character on the `8` computational basis states

## Why it matters on `main`

This theorem sharpens the repo's axis-symmetry language into an exact
representation statement. It supplies a canonical structural input for the
retained three-generation lane and for future bounded flavor work built on the
full taste cube rather than only on the retained `hw=1` triplet.

## Verification

Run:

```bash
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
```

The runner checks the `S_3` representation law on `C^8`, Hamming-weight
preservation, the class characters, and the multiplicity calculation
`C^8 ~= 4 A_1 + 2 E`.


## Hypothesis set used (axiom-reset 2026-05-03)

Per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
