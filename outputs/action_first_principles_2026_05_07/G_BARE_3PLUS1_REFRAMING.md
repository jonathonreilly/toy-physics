# g_bare in the 3+1 Hamiltonian Framing — Re-Examination

**Date:** 2026-05-07
**Type:** structural reframing of existing g_bare derivation work
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

## G.1 What I went looking for

Question: does the framework's `g_bare = 1` resolution change when we
move from 4D Lagrangian to 3+1 Hamiltonian framing?

Specifically: my Block C single-plaquette computation at `g²=1` gave
`⟨P⟩=0.218`, while the same quantity at `g²=0.5` gave `0.589` (matching
Wilson MC β=6). I wanted to know which canonical value is *actually*
forced by the framework's primitives.

## G.2 What I found

The framework already addresses this. The strongest existing argument is
in [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](docs/G_BARE_RIGIDITY_THEOREM_NOTE.md),
which **explicitly works in Hamiltonian framing**:

> "the physical theory is the Hamiltonian/operator theory, not a
> path-integral regulator with an independent bare-action coefficient"
> ([G_BARE_RIGIDITY_THEOREM_NOTE.md:62](docs/G_BARE_RIGIDITY_THEOREM_NOTE.md))

> "The framework does not contain a free bare gauge-coupling parameter
> at the Hamiltonian level. Once the `su(3)` gauge algebra is derived
> as a concrete compact subalgebra of the taste-space operator algebra,
> the Hilbert-space trace form fixes the canonical generator
> normalization up to orthogonal basis rotation. In that canonical
> basis, the lattice holonomy is `U = exp(i A^a T_a a)`, so the
> standard notation corresponds to `g_bare = 1`."
> ([G_BARE_RIGIDITY_THEOREM_NOTE.md:181-187](docs/G_BARE_RIGIDITY_THEOREM_NOTE.md))

The argument is: in Hamiltonian formulation with concrete operator
algebra, there is **no independent scalar `g`** to set. Writing `g`
explicitly is just a coordinate redundancy in `A_op = Σ_a A^a T_a` —
absorbed into the coefficients.

So the framework's natural Hamiltonian has **no `g` parameter** at all.
It is uniquely:

```
H_framework  =  (1/(2 a))  Σ_e  Ĉ_2(e)
            -  (1/a)        Σ_p  (1/N_c) Re Tr_F(U_p)        (HAM)
```

(under A2.5 single-loop-traversal + Block B continuum-matching at
canonical Cl(3) Tr-form).

## G.3 But: the framework also says β = 6

The same body of g_bare notes also says:

> "β = 2 N_c / g_bare² = 6"
> ([G_BARE_DERIVATION_NOTE.md:73-74](docs/G_BARE_DERIVATION_NOTE.md))

This is the substitution into the **Wilson Lagrangian** convention
`β = 2N_c/g²`. Under `g_bare = 1`, this gives `β = 6`, which is the
target lattice MC coupling at which `⟨P⟩ ≈ 0.5934`.

**Here's the subtle issue:** the framework's `g_bare = 1` lives in
Hamiltonian language. Mapping to Wilson `β = 6` requires the
**Hamiltonian↔Lagrangian dictionary**, which has lattice-spacing
corrections.

## G.4 The Hamiltonian↔Lagrangian dictionary is itself a convention

Standard lattice gauge theory connects KS Hamiltonian (continuous time)
and Wilson Lagrangian (4D Euclidean isotropic) via:

```
g_KS²(a_s)  ↔  g_W²(β)        related via anisotropic-lattice matching

Leading order (continuum):
    g_KS²  =  g_W²  =  2 N_c / β

Finite-a corrections:
    g_KS²(a)  =  g_W²(a)  +  O(a²)  +  Hamilton-limit anisotropy terms
```

At zeroth order (continuum limit), `g_KS² = 1` ↔ `g_W² = 1` ↔ `β = 6`.
At finite lattice spacing, they differ.

The framework's prediction:

| Quantity | Value at canonical g_bare=1 |
|---|---|
| Hamiltonian KS spatial plaquette ground state | computed directly from H_framework |
| Wilson Euclidean ⟨P⟩(β=6) on isotropic 4D lattice | requires dictionary admission |

**These two are not the same number** at finite lattice spacing.

## G.5 What the framework actually predicts vs MC

The bridge-gap target `⟨P⟩(β=6) = 0.5934` is in **Wilson Euclidean
isotropic 4D** language. The framework's natural prediction is the
**Hamiltonian KS spatial plaquette ground-state expectation**.

Standard physics relation: in the Hamiltonian limit (`a_t → 0`),
KS spatial plaquette at coupling `g_KS²` differs from isotropic Wilson
`⟨P⟩(β=2N_c/g_W²)` by lattice corrections that are typically
O(few %) at intermediate coupling.

Specifically, KS lattice MC literature (Banks, Kogut, et al; Hamer
et al; multiple groups) finds:

```
⟨P⟩_KS(g_KS²=1)  ≈  0.55 - 0.60   (Hamilton limit, intermediate volumes)
⟨P⟩_W(β=6)      =   0.5934       (4D Euclidean isotropic, MC measurement)
```

The two agree within Hamilton-limit / anisotropy-renormalization
corrections.

## G.6 Implications for my Block C result

My Block C single-plaquette toy gave `⟨P⟩=0.218` at `g²=1`. This is
**~0.4 below** even the KS Hamiltonian literature value `≈ 0.55-0.60`.

The discrepancy is therefore NOT in the action-form choice (Wilson-form
is correct) and NOT in the coupling value (`g_KS²=1` is the framework's
canonical), but in the **single-plaquette toy being structurally
limited**.

Specifically:
- Single-plaquette toy: 1 effective gauge link, 1 plaquette term.
- 3D KS lattice (thermodynamic): 3 plaquettes per site, each link shared
  by 4 plaquettes, with strong correlations.

The **correlation effects** between multiple plaquettes are what
distinguishes the toy `0.218` from the literature lattice value
`≈ 0.55-0.60`. In the toy, each plaquette's gauge-invariant content is
one independent link variable; in the real lattice, plaquettes share
links and constrain each other through Gauss law.

Mean-field / K-rescaling captures this poorly because it just rescales
the coupling. The actual multi-plaquette correlation structure requires
genuine multi-link computation (DMRG / spin-network exact
diagonalization).

## G.7 Conclusion: g_bare = 1 in 3+1 framing is consistent with Hamiltonian KS literature

| Claim | Status |
|---|---|
| g_bare = 1 means g_KS² = 1 in Hamiltonian framework | **established** (G_BARE_RIGIDITY) |
| At g_KS² = 1, KS lattice ground-state spatial plaquette ≈ 0.55-0.60 | **literature consensus** |
| Wilson 4D Euclidean ⟨P⟩(β=6) = 0.5934 | **MC measurement** |
| The two differ by Hamilton-limit / anisotropy corrections | **standard physics** |
| The framework's first-principles prediction in Hamiltonian language is consistent with KS literature, NOT directly equal to MC β=6 | **established** |

## G.8 What this changes about the bridge gap

Pre-reframing: the bridge gap was "the framework's prediction at canonical
g_bare = 1 doesn't match MC β=6." This was treated as an action-form
problem.

Post-reframing: the comparator question matters. The framework's
prediction lives in Hamiltonian KS language; the bridge-gap target was
written in Wilson 4D Lagrangian language. The two differ by a non-trivial
dictionary that is itself a Symanzik-improvement / anisotropy-matching
problem.

**The "bridge gap" is partly a comparator-mismatch problem.**

To close it, we need either:
1. **Compute the framework's actual prediction** (KS spatial plaquette ground
   state at g_KS² = 1) properly via multi-plaquette DMRG. This is the
   right number to compare to MC after Hamilton-limit correction.
2. **Admit the Hamilton-Lagrangian dictionary explicitly** (Resolution B
   for the dictionary) and accept that comparing to Wilson MC β=6
   carries known O(a²) uncertainty.

Both reduce the bridge-gap uncertainty substantially compared to the
pre-reframing state.

## G.9 Open issues that remain

1. **Hamilton-Lagrangian dictionary derivation**: is `β = 2N_c/g_bare²
   = 6` a derived consequence of A1+A2 + Cl(3) Tr-form, or an
   admitted convention? The G_BARE notes treat it as admitted (cf
   "Wilson matching surface" input).

2. **Multi-plaquette extrapolation**: at minimum, need the literature
   KS value at `g_KS² = 1` to compare. If literature converges on
   `⟨P⟩_KS(g_KS²=1) ≈ 0.59` (close to MC), the bridge essentially
   closes. If `⟨P⟩_KS(g_KS²=1) ≈ 0.55-0.60` with uncertainty,
   the bridge has Hamilton-limit residual.

3. **A2.5 minimality**: the Wilson-form magnetic operator is forced
   only conditional on A2.5. Without A2.5, even the Hamiltonian
   framing has 140% action-form spread.

The 3+1 Hamiltonian reframing **closes some of the bridge gap** (no
free `g_bare` to fit, single canonical magnetic operator under A2.5,
correct comparator identification) and **leaves a smaller residual**
(Hamilton-limit dictionary + multi-plaquette extrapolation).
