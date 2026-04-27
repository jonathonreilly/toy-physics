# Area-Law Primitive-Edge Entropy Selector No-Go Note

**Date:** 2026-04-25
**Status:** proposed_retained residual no-go for Planck Target 2
**Runner:** `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py`

## Purpose

This note attacks the remaining gapped-horizon route to Target 2. The Planck
conditional packet derives the exact primitive trace

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4.
```

The open question is whether this same finite primitive boundary can be read as
an entanglement entropy coefficient. The answer is negative for the canonical
finite-cell entropy constructions. The rank trace is not a von Neumann
entropy, and the standard entropies associated with the same `16`-state
primitive data do not equal `1/4`.

## Safe statement

On the source-free primitive cell

```text
H_cell ~= C^16,    rho_cell = I_16/16,    rank(P_A)=4,
```

the primitive counting trace is

```text
Tr(rho_cell P_A) = 1/4.
```

But the corresponding canonical entropy quantities are:

```text
S(I_16/16)                         = log 16,
S(P_A/rank(P_A))                   = log 4,
-Tr((P_A rho P_A) log(P_A rho P_A)) = (1/4) log 16 = log 2,
H_binary(Tr(rho P_A))              = H_binary(1/4),
log(rank(P_A))/log(16)             = 1/2.
```

None is `1/4` in natural units. Therefore the identity

```text
Tr((I_16/16) P_A) = 1/4
```

is a counting/action coefficient, not already an entanglement-entropy
coefficient.

## Gapped-edge tuning obstruction

A gapped edge carrier can be made to obey a strict area law. For independent
boundary-crossing two-level edge pairs, one face carries entropy

```text
S_edge(p) = -p log p - (1-p) log(1-p).
```

There is a unique `p_* in (0, 1/2)` with

```text
S_edge(p_*) = 1/4,
p_* ~= 0.068599066737.
```

So a gapped edge model can be tuned to the Bekenstein-Hawking coefficient. But
`p_*` is not the primitive rank fraction `4/16`, not a `1/16` cell atom, and
not determined by the rank pair `(16,4)`. It is an additional edge-spectrum
selector.

This is not just a numerical concern. The gap can be kept fixed while the
boundary entropy varies continuously from `0` to `log 2` by changing the local
Schmidt parameter. A mass gap or exponential correlation length gives an area
law; it does not determine the leading ultraviolet coefficient.

## The no-go

Within the finite primitive-edge class whose local data are only:

1. `H_cell ~= C^16`;
2. the source-free state `I_16/16`;
3. the rank-four primitive boundary/event projector `P_A`;
4. locality and finite-face additivity;
5. standard von Neumann or binary measurement entropy;

there is no derivation of an entanglement area coefficient equal to `1/4`.

Any positive gapped Target 2 theorem must add at least one further datum:

- a Schmidt-spectrum selector fixing `p = p_*`;
- an edge-sector Hilbert-space/temperature law whose entropy per face is
  exactly `1/4`;
- or a direct theorem that the entropy functional to use is the primitive
  trace itself, despite it not being von Neumann entanglement entropy.

The last option changes the meaning of "entropy" from entanglement entropy to
primitive boundary count unless a new operational argument is supplied.

## Relation to the action-side `1/4`

The action-side result remains valuable and exact. The finite-boundary density
extension theorem proves that `c_cell = 1/4` extends additively once the
primitive boundary count is accepted as the gravitational boundary/action
carrier.

This note says only that the same arithmetic does not automatically produce
the von Neumann entanglement coefficient required by Target 2. The bridge still
requires a real entropy carrier theorem, not a relabeling of the trace.

## What remains open

The surviving positive Target 2 routes are now sharply specified:

1. derive the multipocket/sector selector needed by a Widom carrier;
2. derive the primitive-edge Schmidt spectrum needed by a gapped carrier;
3. replace von Neumann entropy with a justified operational primitive-boundary
   entropy and state that the result is not ordinary entanglement entropy.

Without one of these, Target 2 remains open.

## Package wording

Safe wording:

> The primitive `4/16` trace is not itself a von Neumann entanglement entropy.
> The canonical finite-cell entropy constructions from the same `16`-state
> data give `log 16`, `log 4`, `log 2`, `H(1/4)`, or `1/2` after rank
> normalization, not `1/4`. A gapped edge carrier can be tuned to entropy
> `1/4`, but the required Schmidt spectrum is an additional selector.

Unsafe wording:

> The Planck primitive trace already proves the entanglement entropy area
> coefficient.

## Verification

Run:

```bash
python3 scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py
```

The runner checks all finite-cell entropy values, the absence of a `1/4`
entropy among the canonical primitive rank constructions, the tuned gapped-edge
Schmidt parameter, and the fact that a fixed gap does not fix the edge entropy.

Current output:

```text
SUMMARY: PASS=26  FAIL=0
```
