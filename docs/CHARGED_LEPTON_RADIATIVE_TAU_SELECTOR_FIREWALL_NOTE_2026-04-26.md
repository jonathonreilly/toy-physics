# Charged-Lepton Radiative Tau Selector Firewall

**Date:** 2026-04-26

**Status:** proposed_retained exact negative boundary for standalone tau
selection.

**Primary runner:**
`scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py`

## 1. Claim

The support relation

```text
y_tau ?= alpha_LM / (4pi)
```

is numerically strong when assigned to the tau comparator. It is not, by
itself, a retained tau-generation theorem.

The reason is exact: the electroweak charged-lepton Casimir used by the
radiative support stack is generation-blind. The same calculation applies to
`e`, `mu`, and `tau`. Therefore it cannot select the tau eigenvalue without an
additional generation-selection, ratio, or source-domain primitive.

## 2. What The Support Stack Does Establish

The existing support scripts establish a coherent scale lane:

- `alpha_LM` is a retained lattice coupling on the repo surface.
- `1/(4pi)` is the one-loop phase-space factor used by the retained
  perturbative stack.
- The charged-lepton electroweak Casimir is

```text
C_l = 3/4 + 1/4 = 1.
```

This yields the generation-blind support scale

```text
y_l^rad = alpha_LM / (4pi).
```

Assigned to the tau comparator with the retained electroweak scale, this
matches the observed tau mass closely. That is useful support.

## 3. What It Does Not Establish

The calculation does not contain a tau selector. The three charged leptons
have the same Standard Model electroweak quantum numbers generation by
generation:

```text
L_i : (1, 2)_{-1},
e_i : (1, 1)_{-2}.
```

So the radiative Casimir vector is

```text
(C_e, C_mu, C_tau) = (1, 1, 1).
```

Any generation relabeling leaves this vector invariant. A rule that is
invariant under `U(3)` generation relabeling cannot, by itself, identify the
third charged-lepton eigenvalue.

Naively applying the same scale to all three charged leptons would produce a
degenerate charged-lepton spectrum near the tau scale, not the observed
electron/muon/tau hierarchy. Using the observed fact that tau is the heavy
charged lepton would import the selector from data.

## 4. Comparator Firewall

The runner prints PDG charged-lepton masses only as comparators. They are not
proof inputs. The key audit point is that the prior support scripts contain
PDG-match checks such as `M_TAU_PDG`, and those checks are appropriate only as
observational comparisons.

They cannot promote the relation to retained closure unless the tau selection
and the charged-lepton ratios are derived without observed charged-lepton
masses.

## 5. Consequence

This firewall does not kill the radiative scale. It demotes its role precisely:

```text
alpha_LM/(4pi) can remain a candidate charged-lepton scale,
but it is not a standalone retained y_tau theorem.
```

To promote it, the workstream still needs a retained primitive that identifies
which charged-lepton eigenvalue receives that scale, or a retained full ratio
law that makes the assignment unavoidable.

## 6. Safe Downstream Wording

Safe:

```text
The radiative alpha_LM/(4pi) lane supplies a strong tau-scale comparator, but
the electroweak Casimir is generation-blind. A separate generation/source law
is still required.
```

Unsafe:

```text
alpha_LM/(4pi) derives y_tau by itself.
```
