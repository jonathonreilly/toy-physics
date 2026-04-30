# PMNS `C3` Character-Mode Reduction

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
