# EW Current Traceless-Generator Selector No-Go Proposal Note

**Date:** 2026-05-03
**Claim type:** no_go
**Status:** route-specific exact blocker for a tempting positive closure of the
EW current matching gate. This note does not replace the existing no-go proposal
in [`EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md`](EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md);
it records why one proposed positive route is not a positive closure.
**Primary runner:** `scripts/frontier_ew_current_traceless_generator_selector_no_go.py`

## Claim

The tracelessness of the electroweak current generator,

```text
Tr_internal(Q_EW) = 0,
```

does not derive the connected-trace EW readout

```text
kappa_EW = 0.
```

It only removes ordinary Wick-disconnected one-current loops. The missing EW
matching coefficient is attached to the **color Fierz singlet** channel inside
the connected two-current fermion-line contraction, and that channel is weighted
by `Tr_internal(Q_EW^2)`, not by `Tr_internal(Q_EW)^2`.

Therefore the route

```text
Tr_internal(Q_EW) = 0  =>  disconnected-current coefficient = 0
```

targets the wrong disconnected object and cannot close the EW current matching
rule positively.

## Setup

The lattice Noether current has the point-split bilinear form

```text
J^{mu,A}_x ~ bar(psi)_x Q_EW^A U_mu(x) psi_{x+mu} + ...
```

where `Q_EW^A` acts on the weak/hypercharge/internal fiber and the color link
is the SU(`N_c`) parallel transporter. For an EW current, the external
generator is color-blind: the color structure at the current insertion is
`I_color`, not an SU(3) generator.

The Fierz-channel authority decomposes the color matrix `M = G(x,y)` as

```text
Tr_color[M^\dagger M]
  = (1/N_c) |Tr_color M|^2
    + 2 sum_A |Tr_color[M t^A]|^2
  = S(M) + C(M).
```

Here `S(M)` is the color Fierz singlet and `C(M)` is the color adjoint channel.
The matching-rule proposal names the physical readout coefficient as

```text
Pi_EW^phys(kappa_EW) = C + kappa_EW S.
```

The required positive theorem would have to derive `kappa_EW = 0`.

## The tempting route and why it fails

For many EW generators, including SU(2) generators and the full-generation
hypercharge/gravitational-anomaly trace, the one-current internal trace is zero.
That gives

```text
Tr_internal(Q_EW)^2 = 0.
```

This is enough to kill a Wick-disconnected product of two one-current loops:

```text
<J_EW(x)> <J_EW(y)>.
```

But the EW current matching gate is not asking about that ordinary
Wick-disconnected product. Its missing `kappa_EW` multiplies the color Fierz
singlet inside the connected two-current contraction:

```text
<J_EW(x) J_EW(y)>_same fermion line
  ~ Tr_internal(Q_EW^2) [ S(M) + C(M) ].
```

The color Fierz singlet is therefore weighted by `Tr_internal(Q_EW^2)`. For a
nonzero generator this quadratic trace is nonzero even when the linear trace
vanishes.

## Exact counterexample

Take `N_c = 3`, `Q_EW = T_3 = diag(1/2, -1/2)`, and a color-diagonal matrix
`M = I_color`. Then

```text
Tr_internal(T_3)   = 0,
Tr_internal(T_3^2) = 1/2.
```

The Wick-disconnected internal factor vanishes:

```text
Tr_internal(T_3)^2 = 0.
```

But the color channel decomposition of `M = I_color` is purely singlet:

```text
S(I_color) = (1/N_c) |Tr_color I|^2 = 3,
C(I_color) = 0.
```

So the connected two-current contraction is nonzero and entirely singlet:

```text
Tr_internal(T_3^2) S(I_color) = (1/2) * 3 = 3/2,
Tr_internal(T_3^2) C(I_color) = 0.
```

Thus `Tr_internal(Q_EW) = 0` can coexist with a nonzero color Fierz singlet
contribution. It cannot imply `kappa_EW = 0`.

## Boundary

This no-go is narrow. It does not say a positive EW current matching theorem is
impossible in all frameworks. It says the specific trace-based route fails:
tracelessness of the internal EW generator removes the wrong term.

The remaining positive routes are still exactly the ones named in the gate:

1. derive an explicit framework-native lattice EW current construction whose
   two-current contraction mechanically projects onto the color adjoint channel;
2. compute the color Fierz singlet/disconnected coefficient exactly and show it
   is zero for the physical EW readout.

The current Noether/current surface is color-blind at the EW insertion,
so it supplies `I_color` at the vertex rather than an adjoint color projector.
That leaves `kappa_EW` unmatched.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_current_traceless_generator_selector_no_go.py
```

The runner verifies the exact rational counterexample, distinguishes
`Tr_internal(Q_EW)^2` from `Tr_internal(Q_EW^2)`, and confirms that the
route cannot distinguish the connected selector `K_EW(0)=9/8` from the
full-trace readout `K_EW(1)=1`.

## Cited authority

- [`EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md`](EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md)
  names `kappa_EW` and proves the current retained Fierz/CMT/OZI packet does
  not fix it.
- [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  supplies the exact color singlet/adjoint Fierz decomposition.
- [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
  is used here only as bounded current-form context for the point-split
  bilinear; this branch does not promote it to repo-wide axiom authority.
