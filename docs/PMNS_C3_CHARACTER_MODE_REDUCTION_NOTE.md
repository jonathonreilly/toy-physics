# PMNS `C3` Character-Mode Reduction
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).

**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_pmns_c3_character_mode_reduction.py`

## Question

Once the native `C3`-character holonomy family is closed, what is the exact
remaining sole-axiom PMNS value-selection problem on the retained `hw=1`
triplet?

## Answer

It is smaller than the raw `3`-real reduced-cycle family.

On the graph-first reduced forward-cycle channel

\[
A_{\mathrm{fwd}}(u,v,w)
=
(u+i v)E_{12}+wE_{23}+(u-i v)E_{31},
\]

the exact native `C3`-character holonomy triple has discrete Fourier modes

\[
z_0 = w,\qquad
z_1 = u-i v,\qquad
z_2 = u+i v.
\]

So the remaining PMNS value problem is exactly:

- one real trivial-character amplitude `w`
- one complex nontrivial character amplitude `chi := z_2 = u + i v`

with

\[
z_1=\overline{\chi}
\]

on the residual graph-first antiunitary slice.

## Stronger Boundary

The current sole-axiom routes do **not** fail on an unspecified `3`-real
family. They fail because they annihilate the nontrivial character amplitude
exactly:

\[
\chi = 0
\]

on each of:

- the sole-axiom free route
- the sole-axiom `hw=1` source/transfer route
- the retained scalar route

So the exact missing source is now explicit:

> a sole-axiom law that produces nonzero `C3`-nontrivial character amplitude on
> the retained `hw=1` response family.

## Meaning

This sharpens the remaining blocker further than the previous
nonselection/holonomy notes:

- the native readout family is already closed
- the graph-first reduced channel is already fixed
- the unresolved object is not a generic PMNS value law
- it is only the production of nonzero nontrivial `C3` character amplitude

## Verification

```bash
python3 scripts/frontier_pmns_c3_character_mode_reduction.py
```

Expected:

```text
PASS=15 FAIL=0
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
