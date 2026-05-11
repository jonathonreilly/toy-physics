# Koide Full-Lattice Schur-Inheritance Note

**Date:** 2026-04-18
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** exact scope theorem for the positive-parent obstruction
**Runner:** `scripts/frontier_koide_full_lattice_schur_inheritance.py`

## Question

The previous positive-parent obstruction was stated directly on the retained
`hw=1` triplet. That is useful, but not yet the whole science question, because
the framework is not supposed to stop at a bare `hw=1` identification:

- the full taste-cube / BZ-corner carrier is physical input, and
- the anomaly-forced `3+1` completion may matter before one accepts a no-go.

So the real question is narrower and better:

> if one enlarges the carrier beyond bare `hw=1`, but still reduces back to the
> charged-lepton observable lane by the current effective-operator / Schur class,
> does the old obstruction survive?

## Safe answer

Yes.

The old obstruction is **not** just a small-carrier artifact. It extends to any
larger carrier of the form
```
V = T_1 ⊕ W,
```
where:

- `T_1` is the retained `hw=1` triplet carrying the regular `C_3[111]` action,
- `W` is any additional sector: `O_0 ⊕ T_2 ⊕ O_3`, full taste-cube
  completion, or extra spectator/internal factors from a `3+1` extension,
- the full parent operator is `C_3[111]`-covariant, and
- the physical charged-lepton effective operator is obtained by the standard
  block reduction / Schur complement onto `T_1`.

Under those hypotheses, the reduced operator on `T_1` is still
`C_3[111]`-covariant, hence still circulant. Therefore the current
axis-diagonal charged-lepton readout (`U_e = I_3`) gives the same conclusion as
before:

> any axis-diagonal reduced operator on `T_1` is scalar, so a nondegenerate
> charged-lepton hierarchy still cannot come from this reduction class alone.

So the previous obstruction should be read as a **reduction-class theorem**, not
as a claim that bare `hw=1` is the whole physical story.

## Why this matters

This sharpens the science in exactly the direction the full-lattice caution
demands.

The [site-phase / cube-shift intertwiner note](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
already warns that one should **not** identify the retained `hw=1` triplet with
physical generations by itself. That warning is correct.

But the right conclusion is not "therefore the old obstruction is probably a
projection artifact." The right conclusion is:

> enlarging the carrier is not enough by itself. One must also change the
> reduction or readout architecture if one wants to evade the obstruction.

## The theorem

Let the spatial `C_3[111]` action on the larger carrier be
```
U = C ⊕ R
```
with:

- `C` the retained `3 x 3` cycle on `T_1`,
- `R` any unitary representation on the complement `W`.

Let a positive Hermitian full-carrier parent be written in block form
```
M = [[A,  B ],
     [B†, D ]],
```
where the blocks refer to the splitting `V = T_1 ⊕ W`, and assume
```
U M U† = M.
```

If `D` is invertible and the effective charged-lepton operator is the Schur
complement
```
S = A - B D^(-1) B†
```
on `T_1`, then
```
C S = S C.
```

So `S` lies in the commutant of the regular `C_3` action on `T_1`, i.e. `S` is
circulant.

### Proof

From `U M U† = M`, block comparison gives
```
C A = A C,
C B = B R,
R D = D R.
```
Since `D` commutes with `R`, so does `D^(-1)`. Also `C B = B R` implies
```
R B† = B† C.
```
Then
```
S C
  = A C - B D^(-1) B† C
  = A C - B D^(-1) R B†
  = A C - B R D^(-1) B†
  = A C - C B D^(-1) B†
  = C S.
```
Therefore `S` is `C_3[111]`-covariant on `T_1`. On the retained `hw=1`
triplet, that means `S` is circulant. □

## Full taste-cube reading

This is not an abstract representation-theory trick detached from the lattice.
On the full taste cube `C^8`, the spatial `C_3[111]` cycle preserves the
splitting
```
C^8 = O_0 ⊕ T_1 ⊕ T_2 ⊕ O_3,
```
with:

- `O_0` and `O_3` fixed singlets,
- `T_1` carrying the retained regular `3`-cycle,
- `T_2` carrying the same regular `3`-cycle.

So integrating out `O_0 ⊕ T_2 ⊕ O_3` by a standard Schur/effective reduction
still returns a circulant operator on `T_1`.

The runner verifies this explicitly on random positive `C_3`-covariant full
`C^8` parents.

## Extra internal / `3+1` factors

The same inheritance statement survives arbitrary additional internal sectors.
If one tensors the spatial carrier with a spectator/internal space and the
spatial `C_3[111]` action acts as
```
U_ext = U_spatial ⊗ I_int,
```
then exactly the same block argument applies. So merely appending a `3+1`,
chirality, or other spectator factor does **not** by itself break the induced
`C_3` symmetry on the reduced charged-lepton block.

This does **not** mean `3+1` completion is irrelevant. It means:

> `3+1` completion helps the Koide lane only if it changes the physical carrier,
> the reduction map, or the readout primitive, rather than only enlarging the
> ambient Hilbert space.

## Consequence for the obstruction

The earlier obstruction should now be read in the following stronger but more
careful form:

> Any positive full-carrier `C_3[111]` parent that is reduced to the
> charged-lepton observable lane by the standard `C_3`-equivariant Schur /
> effective-operator map still gives a circulant operator on `T_1`. If masses
> are then read in the current axis basis (`U_e = I_3`), nondegenerate
> hierarchy is still impossible.

So the actual remaining blocker is:

- not "you assumed bare `hw=1` too early";
- but "you kept the same reduction and readout class."

## What still escapes the theorem

This note does **not** rule out a future charged-lepton closure. It leaves open
exactly the escape hatches that now matter scientifically:

1. a new physical carrier where the charged leptons are not read as an isolated
   `T_1` target;
2. a non-Schur or non-`C_3`-equivariant reduction map from the full lattice to
   the charged sector;
3. a new readout primitive replacing the current axis-diagonal `U_e = I_3`
   evaluation;
4. a controlled charged-lepton-specific breaking of strict `C_3[111]`
   covariance.

Those are now the honest next science targets.

## Bottom line

The positive-parent obstruction survives the full-lattice caution in the
following precise sense:

- it is **not** a theorem that bare `hw=1` is the whole physical lepton story;
- it **is** a theorem that every current-style full-carrier completion with the
  same equivariant Schur reduction inherits the same obstruction.

So the next leptons work should not be "just make the carrier bigger." It
should be "derive the new reduction/readout primitive, if one exists."


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
