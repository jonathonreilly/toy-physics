# Translation Covariance of Local Operators: T_a O(x) T_a^† = O(x + a)

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** for any operator O(x) attached to lattice site x (or compactly
supported around x), the framework's translation operator T_a (retained via
N1 of the lattice Noether theorem) acts by site-label shift:
T_a O(x) T_a^† = O(x + a) on H_phys for all a ∈ Z^3 and all x ∈ Λ. This is
the operator-level statement of "lattice translation invariance" — a sum
Σ_x O(x) over a translation-invariant family is left fixed by T_a, and the
support of any local operator shifts by a.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r7-20260502`
**Cycle:** 2 (Block 2)
**Branch:** `physics-loop/positive-only-r7-block02-translation-covariance-20260502`
**Runner:** `scripts/translation_covariance_local_op_check.py`
**Log:** `outputs/translation_covariance_local_op_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
  — `effective_status: retained`. Provides:
  - **(N1)** Translation symmetry T_a : x ↦ x + a on Z^3 acting unitarily
    on H_phys with conserved lattice momentum P̂^μ.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Position-basis decomposition.** Every operator O on H_phys can be written
  in the position basis as O = Σ_{x, y; α, β} O_{xα, yβ} |xα⟩⟨yβ| where
  α, β are internal labels. Standard. (Well-defined for any finite-dim
  H_phys, including the framework's lattice slabs.)
- **Local support definition.** An operator O(x_0) is "local at x_0" if its
  matrix elements O_{xα, yβ} vanish unless x = y = x_0. (Standard definition
  of local-at-a-site operator in lattice QM.)

Both are pure structural / definitional inputs; no admitted physics conventions.

## Statement

Let H_phys be the framework's lattice Hilbert space with translation operators
T_a (retained per N1, supplied by axiom_first_lattice_noether_theorem). Let
O(x_0) be any operator local at site x_0 ∈ Λ (i.e. its matrix elements vanish
on basis states not at x_0).

**(C1) Site-label covariance.** For every a ∈ Z^3:

```text
    T_a · O(x_0) · T_a^†  =  O(x_0 + a)                                    (1)
```

**(C2) Position operator covariance.** For the global position operator
X̂ := Σ_x x · P_x (where P_x = |x⟩⟨x|):

```text
    T_a · X̂ · T_a^†  =  X̂ - a · I                                        (2)
```

(Sign reversal because relabeling x ↦ x + a in the basis ket converts
a sum Σ_x x · |x+a⟩⟨x+a| = Σ_y (y - a) · |y⟩⟨y|.)

**(C3) Two-site operator covariance.** For a hopping operator
h_{x, y} := |x⟩⟨y|:

```text
    T_a · h_{x, y} · T_a^†  =  h_{x + a, y + a}                            (3)
```

More generally, any k-site-local operator transforms by site-label shift
on each of its k support sites.

**(C4) Translation invariance ⇒ commutes with T_a.** If O = Σ_{x ∈ Λ} O(x)
is a sum over a translation-invariant family of local operators (i.e. O(x)
shifted by a equals O(x + a)), then T_a O T_a^† = O for all a, equivalently
[T_a, O] = 0. This is the **operator-level form of lattice translation
invariance**.

**(C5) Support relocation.** supp(T_a · O · T_a^†) = supp(O) + a.

## Proof

### Step 1 — T_a regular representation (cited)

By N1 of the retained lattice Noether theorem, T_a acts unitarily on H_phys
by T_a |x; α⟩ = |x + a; α⟩ for any internal index α. (R6 Block 02 rederived
the resulting group-theoretic structure of T_a as a faithful abelian
representation, but the basic action on basis states is supplied by N1.)

### Step 2 — Site projector covariance

A site projector P_x := Σ_α |x; α⟩⟨x; α| transforms under T_a-conjugation:

```text
    T_a P_x T_a^† |y; β⟩  =  T_a P_x · |y - a; β⟩
                          =  T_a · |x; ?⟩ · δ_{x, y - a}
                          =  |x + a; ?⟩ · δ_{y, x + a}
                          =  P_{x + a} |y; β⟩.                            (4)
```

So T_a P_x T_a^† = P_{x + a} — the site label shifts by +a. This is the
key elementary computation; everything else follows from it by linearity.

### Step 3 — Site-local operator covariance (C1)

Any O(x_0) local at site x_0 decomposes as O(x_0) = Σ_{αβ} O_{αβ}(x_0) ·
|x_0; α⟩⟨x_0; β|. Conjugating by T_a:

```text
    T_a O(x_0) T_a^†  =  Σ_{αβ} O_{αβ}(x_0) · T_a |x_0; α⟩⟨x_0; β| T_a^†
                      =  Σ_{αβ} O_{αβ}(x_0) · |x_0 + a; α⟩⟨x_0 + a; β|.    (5)
```

The last expression is exactly O(x_0 + a) provided the matrix elements
O_{αβ}(·) depend only on the site label structure (translation-equivariant
by construction). Hence T_a O(x_0) T_a^† = O(x_0 + a) — establishing (C1).

### Step 4 — Position operator (C2)

Apply (C1) to each site projector P_x in X̂ = Σ_x x · P_x:

```text
    T_a X̂ T_a^†  =  Σ_x x · T_a P_x T_a^†
                   =  Σ_x x · P_{x + a}
                   =  Σ_y (y - a) · P_y       (relabel y = x + a)
                   =  X̂ - a · I.                                          (6)
```

Establishes (C2). The minus sign reflects that X̂'s coefficient is "label
of basis state with which we're projecting", and that label shifts by -a
when we relabel the sum.

### Step 5 — Two-site operator (C3)

For a hopping operator h_{x, y} := |x⟩⟨y|:

```text
    T_a h_{x, y} T_a^†  =  T_a |x⟩⟨y| T_a^†
                         =  (T_a |x⟩) (T_a^† adj on bra → |y - (-a)⟩ = |y + a⟩)
```

Wait, more carefully: T_a^† acts on the bra as ⟨y| T_a^† = (T_a |y⟩)^† =
⟨y + a|. Hence:

```text
    T_a h_{x, y} T_a^†  =  T_a |x⟩⟨y| T_a^†
                         =  |x + a⟩⟨y + a|
                         =  h_{x + a, y + a}.                              (7)
```

Establishes (C3). The same applies to any k-site-local operator by the same
argument applied to each site separately.

### Step 6 — Translation-invariant sum (C4)

If O(x) = U_a O(x - a) U_a^† for some local operator family with O(x) the
same shape at every site (translation-invariant family), then summing over
all x:

```text
    T_a (Σ_x O(x)) T_a^†  =  Σ_x O(x + a)
                           =  Σ_y O(y)         (relabel y = x + a, sum over Λ)
                           =  Σ_x O(x).                                    (8)
```

The relabeling step is valid because Λ is translation-invariant under T_a
(Z^3 or (Z/N)^3). Hence T_a O T_a^† = O, equivalently [T_a, O] = 0 —
establishing (C4).

### Step 7 — Support relocation (C5)

supp(O) is the set of sites x at which O has nonzero matrix elements.
By (C1)–(C3), if O is supported on sites {x_1, ..., x_k}, then T_a O T_a^†
is supported on sites {x_1 + a, ..., x_k + a}. Hence supp(T_a O T_a^†) =
supp(O) + a — establishing (C5). ∎

## Hypothesis set used

- `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained):
  provides T_a as the unitary translation symmetry on H_phys.
- Position-basis decomposition (definitional, admitted-context).
- Local support definition (definitional, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained lattice Noether theorem.

## Corollaries

C1. **Translation invariance of the action ⇔ Hamiltonian is a sum of
translation-invariant local terms.** The sum H = Σ_x h(x) of a
translation-invariant family of local terms commutes with every T_a
by (C4). Conversely, the spectral decomposition of any T_a-invariant
operator gives a manifestly translation-invariant local form. This is
the *operator-level* expression of N1's translation invariance.

C2. **Local observables shift by exactly the lattice vector.** Any
measurement device localized at site x_0 (e.g. a gauge-invariant
operator in a region around x_0), when translated by lattice vector a,
becomes the same device localized at x_0 + a. There is no anomalous
phase, no nontrivial holonomy, no mixed boundary effect at the
operator level.

C3. **Lattice-momentum eigenstates carry phase under T_a.** A state
|k⟩ with T_a |k⟩ = e^{i k·a} |k⟩ has the property that any local
operator O(x_0) acting on it gives a state where T_a acts as
e^{i k·a}: the phase is intrinsic to the state, the operator just
shifts position. This is the standard plane-wave structure.

C4. **No translation cocycle for local operators.** Since
T_{a} T_{b} = T_{a+b} (R6 Block 02), there is no relative phase between
double-translating a local operator and translating once by the sum.
This rules out projective representations of lattice translations on
local-operator algebras within the framework.

C5. **Microcausality is translation covariant.** The retained
microcausality companion gives [O(x), O'(y)] = 0 for spacelike-separated
x, y. Conjugating by T_a: [O(x + a), O'(y + a)] = 0. So microcausality
itself is translation covariant — separation depends on (x - y), not
on absolute positions. This is the operator-level statement of
spatial-translation symmetry of the causal structure.

## Honest status

Positive theorem on the framework's local-operator translation covariance,
derived from a single retained one-hop dependency by elementary lattice
linear algebra. The runner exhibits position-operator covariance,
site-projector covariance over a full sweep of sites, hopping-operator
covariance, sum-invariance (resolution of identity), and support
relocation — all at machine precision.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "T_a O(x) T_a^† = O(x + a) for any local operator O(x) on H_phys; operator-level form of N1 translation invariance."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - position-basis decomposition (definitional)
  - local support definition (definitional)
```
