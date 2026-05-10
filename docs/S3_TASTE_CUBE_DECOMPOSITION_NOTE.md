# S_3 Taste-Cube Decomposition Note

**Date:** 2026-04-17 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`, `claim_type: open_gate`, `audit_status: audited_clean` as a meta-parent identity, not as a derivation closure).
**Status:** bounded class-A representation-theoretic theorem on the eight-state
taste cube `C^8 = (C^2)^{\otimes 3}` under tensor-position permutations.
**Status authority:** independent audit lane only.
**Script:** `scripts/frontier_s3_action_taste_cube_decomposition.py` (PASS=57)
**Authority role:** canonical representation-theoretic theorem for
axis-permutation symmetry on `C^8 = (C^2)^{\otimes 3}`; **not** a standalone
physical-flavor, generation, mass-hierarchy, or framework-carrier theorem.

## Audit boundary

This note proves a single class-A finite-group representation theorem:

> Under tensor-position permutations of `S_3` on `C^8 = (C^2)^{\otimes 3}`,
> the class character is `chi(e) = 8`, `chi(2-cycle) = 4`, `chi(3-cycle) = 2`,
> giving `C^8 ~= 4 A_1 + 2 E` with no `A_2` summand.

That statement is closed in-note from finite-group character theory and is
verified by the runner (PASS=57) on the explicit `S_3` permutation matrices.

The earlier framing in this note also identified the eight-state cube as the
**framework's** taste cube and identified the `S_3` action as the **framework's**
axis-permutation symmetry. That framework-carrier identification is **not**
closed in this note. It depends on the staggered-Dirac realization derivation
target, which is the canonical open gate
`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`.
This row's load-bearing claim is therefore narrowed to the abstract
representation-theoretic theorem; the framework-carrier reading is recorded
only as an admitted-context label, not as a load-bearing conclusion of this row.

**Cited authorities (one-hop deps):**

- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  (`claim_type: open_gate`) — canonical parent for the framework-carrier
  identification of `C^8 = (C^2)^{\otimes 3}` as the staggered-Dirac BZ-corner
  taste cube. Cited but **not closed** by this note.
- `MINIMAL_AXIOMS_2026-05-03.md` (meta) —
  records that the staggered-Dirac realization is currently an open gate, not
  an axiom; this note inherits that open status for any framework-carrier
  reading.

**Admitted-context literature input:** standard finite-group character theory
for `S_3` (permutation-character formula `chi(pi) = |Fix(pi)|`, decomposition
of the 3-point permutation representation as `A_1 + E`) — this is universal
mathematics input, not framework-derived.

## Safe statement (scope-bounded)

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

and the sign irrep `A_2` does not occur.

This is an abstract finite-dimensional representation-theoretic theorem. It
does not by itself prove any flavor, generation, or mass-hierarchy claim,
and it does not by itself identify `C^8` as the framework's taste cube.
Its safe role is narrower: it fixes the exact abstract `S_3` carrier content
on `C^8 = (C^2)^{\otimes 3}` that later framework tools — *conditional on the
staggered-Dirac realization gate closing* — are allowed to import as an
abstract structural input.

## Classical results applied

- finite-group character theory for `S_3`
- the permutation-character formula `chi(pi) = |Fix(pi)|`
- standard decomposition of the three-point permutation representation as
  `A_1 + E`

## Framework-specific step

- identification of the `S_3` action as axis permutations on the taste cube
- exact computation of the character on the `8` computational basis states

## Why it matters on `main`

This theorem sharpens an abstract `S_3`-on-`C^8` representation-theoretic
identity into an exact bounded statement. It supplies an abstract structural
input that the three-generation lane and future bounded flavor work *may
import as an abstract input*, conditional on the framework-carrier
identification (staggered-Dirac realization gate) closing.

This row is not a physical-flavor closure on its own.

## Verification

Run:

```bash
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
```

The runner checks the `S_3` representation law on `C^8`, Hamming-weight
preservation, the class characters, and the multiplicity calculation
`C^8 ~= 4 A_1 + 2 E`.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
