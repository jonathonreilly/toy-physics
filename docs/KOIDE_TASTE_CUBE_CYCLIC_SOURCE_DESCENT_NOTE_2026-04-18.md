# Koide Taste-Cube Cyclic-Source Descent Note

**Date:** 2026-04-18  
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** support - structural or confirmatory support note
**Runner:** `scripts/frontier_koide_taste_cube_cyclic_source_descent.py`

## Question

The charged-lepton Koide lane should not assume too early that the bare
`hw=1` / `T_1` triplet is the whole physical lepton story. The physical lattice
starts on the full `8`-corner taste cube, and the right positive-path question
is therefore:

> if we work on the full taste cube first, then apply exact `C_3[111]`
> averaging and a Schur-compatible charged-sector reduction, what exact source
> bundle survives on the charged-lepton lane?

Does the full `C^8` carrier produce a genuinely larger Koide source bank, or
does it descend to the same cyclic `3`-response bundle already isolated on the
`T_1` triplet?

## Bottom line

It descends to the same bundle exactly.

Let
```
V = C^8 = O_0 ⊕ T_1 ⊕ T_2 ⊕ O_3
```
with basis ordered as
```
000 | 100,010,001 | 110,011,101 | 111,
```
and let `U` be the spatial `C_3[111]` cycle. Then `T_1` is invariant and the
restricted action is the retained `3 x 3` cycle
```
C = U|_{T_1}.
```

Define the full-cube averaging map
```
A_8(X) = (1/3) Σ_{k=0}^2 U^k X U^{-k},
```
and the `T_1` cyclic projector
```
A_3(Y) = (1/3) Σ_{k=0}^2 C^k Y C^{-k}.
```

If `P_1` denotes the projector onto `T_1`, then for every full-cube source
operator `X`
```
P_1 A_8(X) P_1 = A_3(P_1 X P_1).
```

So exact full-cube averaging and charged-sector compression commute.

Therefore every averaged full-cube source lands, after compression to `T_1`,
in the same cyclic Hermitian image
```
span_R{B0, B1, B2},
```
where
```
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2).
```

That is the same `3`-response Koide bundle already found on the smaller
carrier. The full taste cube does not enlarge the response target; it only
provides a more physical starting point for deriving it.

## Why this is the right positive path

This is exactly the clean version of the full-lattice caution:

- do **not** identify bare `hw=1` with the whole lepton story too early;
- do start on the physical `8`-corner carrier;
- but then compute honestly what exact `C_3[111]` averaging and charged-sector
  reduction actually leave behind.

The answer is positive and small:

> the full physical carrier still descends to the same cyclic `3`-response
> Koide target.

So the next science step is not “guess a new larger source bank.” It is:

1. derive the microscopic full-cube source law on the physical carrier,
2. push it through the exact descent map,
3. derive the selector on the resulting three responses.

## Exact descent identity

Let `P_1` be the projector onto `T_1`. Because `T_1` is invariant under the
full spatial cycle, `P_1` commutes with `U`, and `U|_{T_1} = C`. Therefore
```
P_1 A_8(X) P_1
  = (1/3) Σ_{k=0}^2 P_1 U^k X U^{-k} P_1
  = (1/3) Σ_{k=0}^2 C^k (P_1 X P_1) C^{-k}
  = A_3(P_1 X P_1).
```

This is exact. It is not a heuristic projection.

The runner verifies this identity on all `64` matrix-unit sources of `End(C^8)`.

## Canonical full-cube orbit channels

The descent is not only abstract. There are explicit full-cube orbit sources
whose reduced images are exactly the Koide channels.

Using the one-hot taste corners `100,010,001`, define
```
Q0 = 3 A_8(E_{100,100}),
Qf = 3 A_8(E_{010,100}),
Qb = 3 A_8(E_{100,010}).
```

Then on `T_1`
```
P_1 Q0 P_1 = B0,
P_1 Qf P_1 = C,
P_1 Qb P_1 = C^2.
```

Hence the Hermitian full-cube orbit channels
```
Q1 = Qf + Qb,
Q2 = i(Qf - Qb)
```
reduce exactly to
```
P_1 Q1 P_1 = B1,
P_1 Q2 P_1 = B2.
```

So the full physical carrier already contains canonical averaged source
channels that descend to the Koide basis without any ad hoc ansatz.

## Schur-compatible charged-sector reduction

Now let the full-cube parent operator split as
```
M = [[A,  B ],
     [B†, D ]]
```
under `V = T_1 ⊕ W`, and assume:

- `M` is positive Hermitian;
- `M` is `U`-covariant;
- the charged-sector effective operator is the Schur-compatible reduction
  ```
  S(M) = A - B D^(-1) B†.
  ```

Then the usual block argument gives
```
C S(M) = S(M) C.
```
So the reduced charged-sector operator is circulant:
```
S(M) in span_R{B0, B1, B2}.
```

Write
```
S(M) = (r0/3) B0 + (r1/6) B1 + (r2/6) B2,
```
where
```
r0 = Re Tr(S(M) B0),
r1 = Re Tr(S(M) B1),
r2 = Re Tr(S(M) B2).
```

Those are the same three cyclic responses as in the smaller Koide note. The
full taste cube changes where the law should be derived, but not the exact size
of the charged-sector target.

## Exact factorization of any Schur-compatible source response

For any full-cube Hermitian source `X`, set
```
Y(X) = P_1 A_8(X) P_1.
```
By the descent theorem,
```
Y(X) = u0(X) B0 + u1(X) B1 + u2(X) B2
```
for unique real coefficients `u0,u1,u2`.

Therefore any Schur-compatible charged response of the form
```
R_M(X) = Re Tr(S(M) Y(X))
```
factors exactly as
```
R_M(X) = u0(X) r0 + u1(X) r1 + u2(X) r2.
```

So the physical-lattice source bank collapses exactly to the same three Koide
responses once the charged sector is read through exact `C_3[111]` averaging
and Schur-compatible reduction.

This is the precise constructive statement we needed.

## What is exact now

This note proves exactly:

1. the full taste-cube `C_3[111]` average descends to the same `T_1` cyclic
   projector;
2. the physical carrier contains explicit averaged orbit channels descending to
   `B0,B1,B2`;
3. every positive `U`-covariant full-cube parent reduced by a Schur-compatible
   charged-sector map lands in the same cyclic `3`-response family;
4. every Schur-compatible full-cube source response factors through the same
   three response numbers `(r0,r1,r2)`.

The runner verifies all of this directly.

## What remains open

This note does **not** yet derive:

- the microscopic full-cube source law that determines the functions
  `u0(X), u1(X), u2(X)` from the retained axioms alone;
- the microscopic dynamics that determine the reduced responses
  `(r0, r1, r2)`;
- the selector law
  ```
  2 r0^2 = r1^2 + r2^2,
  ```
  i.e. the actual Koide-closing step;
- the final mass/amplitude readout primitive.

So this is not a premature closure claim. It is a clean reduction of the
physical-lattice problem to the same exact `3`-response target.

## Consequence

The physical-lattice caution and the Koide cyclic law are now aligned.

We do **not** need to choose between:

- “stay honest to the full taste cube,” and
- “work with the small exact Koide bundle.”

Both statements are true simultaneously:

> start on the full `8`-corner carrier, and the exact `C_3[111]` /
> Schur-compatible descent still lands on the same cyclic `3`-response Koide
> bundle.

That makes the next positive move sharp:

> derive the microscopic full-cube source law whose descent produces the three
> cyclic responses, then derive the selector on those responses.

## Bottom line

The full taste cube does not force a larger charged-lepton Koide target.

Under exact `C_3[111]` averaging and Schur-compatible charged-sector reduction,
the physical `8`-corner carrier descends to the same cyclic `3`-response bundle
`(B0,B1,B2)` and therefore to the same response coordinates `(r0,r1,r2)`.

That is the constructive full-lattice positive-path target.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
