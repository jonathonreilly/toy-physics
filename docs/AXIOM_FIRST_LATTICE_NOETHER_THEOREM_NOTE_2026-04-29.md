# Axiom-First Lattice Noether's Theorem on Cl(3) ⊗ Z^3

**Date:** 2026-04-29 (originally); 2026-05-03 (sublattice repair); 2026-05-10 (gate-recategorization repair); 2026-05-10 (g_bare-removal repair)
**Status:** source-note proposal — author-declared `bounded_theorem`; effective
status set only by the independent audit lane.
**Claim type:** bounded_theorem
**Loop:** `axiom-first-foundations`
**Cycle:** 5 (Route R5)
**Runner:** `scripts/axiom_first_lattice_noether_check.py`
**Log:** `outputs/axiom_first_lattice_noether_check_2026-04-29.txt`

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. The `claim_type`, scope, named
admissions, and bounded classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Gate-recategorization repair (2026-05-10)

The 2026-05-05 audit verdict identified two gaps on the post-2026-05-03
note:

1. **Open-gate dependency.** The note's hypothesis section listed
   the staggered-Dirac/Grassmann action as an `A_min` axiom (former
   `A3`). Under the current public framework memo
   `MINIMAL_AXIOMS_2026-05-03.md` the
   staggered-Dirac realization is **not** a current framework axiom; it
   is an explicit `open_gate` derivation target listed there. Lanes
   (including `lattice_noether`) that depend on this gate must be
   reviewed as `bounded_theorem` surfaces with the gate named in
   `admitted_context_inputs` until the gate closes.

2. **Missing `(5) → (3)` verification.** The runner E5 checked the
   bilateral-current closure `(5) → (4)` for U(1) phase, but did not
   verify the analogous `(5) → (3)` specialization to the
   `(2Z)^3` sublattice momentum-density form. The note's textual
   reduction `(5) → (3)` was not independently validated.

This 2026-05-10 repair addresses both gaps:

- **(R1) Authority rebase.** The hypothesis set is rebased on
  `MINIMAL_AXIOMS_2026-05-03.md`. Only
  `A1` (Cl(3) per-site algebra) and `A2` (`Z^3` substrate, restricted
  to its `(2Z)^3` sublattice) are framework axioms here. The
  staggered-Dirac/Grassmann action `M_KS` is admitted as a named
  open-gate input under `admitted_context_inputs`; the canonical
  normalization surface is admitted as a separate named open-gate
  input. The proof is then a bounded Noether identity on the admitted
  staggered/Grassmann carrier. This matches the recategorization in
  `MINIMAL_AXIOMS_2026-05-03.md` line 173 (`lattice_noether` listed
  among lanes depending on the staggered-Dirac realization gate).
- **(R2) Direct `(5) → (3)` verification.** The runner now includes
  `E6`, an explicit numerical check that the canonical staggered
  sublattice-momentum density `(3)` is on-shell divergence-free
  (`∂^L_μ P^μ_x = 0` to machine precision) on a free pure-staggered
  block. `E6` provides the runner-level verification of the
  specialization claim; the textual reduction `(5) → (3)` is now
  recorded with an explicit caveat that it is a discrete Ward-identity
  rearrangement (not a literal infinitesimal-generator substitution),
  and the runner numerically confirms the resulting current.

## Sublattice repair (2026-05-03 — recapped)

The 2026-05-03 review follow-up identified that the staggered
Kogut–Susskind action `M_KS` is **not** invariant under one-site
shifts `T_μ̂` because the staggered phase factor `η_μ(x)` flips sign
under such shifts; only the index-2 sublattice `(2Z)^3` of two-step
shifts is an exact symmetry of `M_KS` (and the runner's E2 exhibit
verifies precisely two-step shifts). One-site shifts generate a
**larger** symmetry group together with compensating staggered/taste
rotations, but they are not pure translations.

The 2026-05-03 repair restated (N1) on the `(2Z)^3` sublattice that
the runner actually verifies. The conserved current (3) is the
`(2Z)^3` momentum density. The full taste-shift structure (one-site
shift composed with a staggered sign rotation) is acknowledged as a
separate, larger symmetry whose Noether current is not in scope
here. The U(1) phase result (N2) is unaffected by the repair.

## Scope

This note derives, on the current public framework memo
`MINIMAL_AXIOMS_2026-05-03.md` plus the
explicitly admitted staggered-Dirac realization gate, a lattice analogue
of Noether's theorem: for any one-parameter Lie symmetry of the admitted
canonical action that maps Grassmann variables to Grassmann variables,
there is an explicit *conserved lattice current* `J^μ_x` with discrete
divergence

```text
    ∂^L_μ J^μ_x   :=   Σ_μ  ( J^μ_x  -  J^μ_{x - μ̂} )   =   0  on shell.   (1)
```

The theorem is established for the two physically-load-bearing
symmetries of the admitted canonical action:

- **(N1) `(2Z)^3` sublattice translation symmetry → discrete
  sublattice-momentum conservation.** (Pure `Z^3` one-site shifts
  are not symmetries of `M_KS`; see the staggered-shift caveat
  below.) The translation case is **discrete**; its conserved
  current arises from a finite-difference Ward identity on the
  admitted staggered carrier (Step 4b below) rather than from a
  literal infinitesimal-generator substitution into (5).
- **(N2) Global U(1) phase symmetry of the matter sector →
  conserved fermion-number current.** This case IS a clean
  infinitesimal Lie-generator substitution into (5).

This is a `bounded_theorem`: it closes the Noether identity given the
staggered-Dirac/Grassmann action as an admitted carrier. When the
staggered-Dirac realization derivation target (open gate per
`MINIMAL_AXIOMS_2026-05-03.md`) closes,
the row becomes eligible for retagging as `positive_theorem` by the
independent audit lane.

After this note, any package lane that quotes "the canonical action
has a conserved current of type X" can cite this bounded lattice
Noether identity, provided it uses the `(2Z)^3` sublattice momentum
(not the naive Z^3 momentum) for the translation current and
acknowledges the same admitted gate.

## Hypothesis set used

The proof uses two framework axioms from
`MINIMAL_AXIOMS_2026-05-03.md`, plus
two **named admitted inputs** corresponding to the open gates in that
memo:

**Framework axioms (current):**

- **A1 — local algebra `Cl(3)`.** Used only via the existence of a
  faithful local representation of the Cl(3) algebra on each site.
- **A2 — substrate `Z^3`.** Used via the discrete translation
  action `T_a : x ↦ x + a`, restricted to the `(2Z)^3` index-2
  sublattice that is an exact symmetry of `M_KS`. One-site shifts
  `T_μ̂` flip the staggered sign factor `η_μ(x)` and require
  compensation by a staggered/taste rotation to give a symmetry; the
  Noether theorem in this note applies to the `(2Z)^3` sublattice
  generators only.

**Admitted context input (open gate per current axiom memo):**

- **`staggered_dirac_realization_gate`.** The Grassmann partition
  with staggered Dirac action

  ```text
      S_F[χ̄, χ]  =  Σ_{x,y}  χ̄_x  M_xy  χ_y                            (2)
  ```

  with `M = m + M_KS`, `M_KS` the staggered Kogut–Susskind hop, is
  admitted as a named carrier. Recategorized from the prior `A3`
  axiom by `MINIMAL_AXIOMS_2026-05-03.md`
  to an open derivation target whose canonical parent note is
  pending packaging. The action is invariant under both `T_{2a}`
  (two-site shift acting on lattice indices) and global `U(1)` phase
  (acting as `χ → e^{iα} χ`, `χ̄ → e^{-iα} χ̄`).

**Note on `g_bare` (not a load-bearing admission of this note).** The
`g_bare = 1` canonical SU(3) normalization recategorized from the prior
`A4` axiom (parent: `G_BARE_DERIVATION_NOTE.md`) is not a
load-bearing input to (N1)–(N3). The Noether identities are quantitatively
`g_bare`-independent: the gauge action `S_G` enters only through the
gauge-invariance hypothesis carried by the admitted canonical-action surface,
not through the `g_bare` numerical normalization gate.
Per the 2026-05-10 audit verdict's repair-target option "separately
close or remove the structural `g_bare` dependency if it is not
load-bearing", the `g_bare` gate is therefore **removed** from this
note's named-admission list (2026-05-10 g_bare-removal repair below).

When the staggered_dirac_realization_gate closes on the current
physical `Cl(3)` local algebra plus `Z^3` spatial substrate framework
surface, the row becomes eligible for retagging by the independent
audit lane.

## Statement

Let `S = S_F + S_G` be the canonical action on `A_min`, and let
`G` be a one-parameter symmetry group that maps the action into
itself: `S[g · ϕ] = S[ϕ]` for all `g ∈ G`. Then on `A_min`:

**(N1) `(2Z)^3` sublattice momentum conservation.** For the
discrete sublattice translation symmetry `T_a ∈ (2Z)^3` (two-site
shifts in any axis direction, generated by `T_{2μ̂}` for `μ ∈ {1,2,3}`),
the conserved lattice current is the canonical staggered
sublattice-momentum density

```text
    P^μ_x  =  - (i/2) η_μ(x)  ( χ̄_x  ∂^L_μ χ_x  -  ∂^L_μ χ̄_x · χ_x ),   (3)
```

with `∂^L_μ` the symmetric lattice difference. The lattice
divergence `∂^L_μ P^μ_x = 0` holds on shell (i.e. when the
classical equations of motion `M_xy χ_y = 0` are satisfied).

**(N2) Fermion-number current.** For the global `U(1)` phase
symmetry `χ → e^{iα} χ`, the conserved current is

```text
    J^μ_x  =  - (1/2) η_μ(x)  ( χ̄_x  χ_{x + μ̂}  +  χ̄_{x + μ̂}  χ_x ),    (4)
```

with lattice divergence `∂^L_μ J^μ_x = 0` on shell. Integration over
a Cauchy surface (lattice time slice) gives the conserved fermion
number `Q = Σ_x χ̄_x χ_x`.

**(N3) General lattice Noether identity.** For any infinitesimal
symmetry `δ_α χ_x = α^A T^A_{xy} χ_y` (and the conjugate variation
`δ_α χ̄_x = -α^A χ̄_z (T^A)_{zx}`) of the canonical action with
nearest-neighbour staggered hop `M_{x, x±μ̂} = ±(1/2) η_μ(x)`, the
on-shell conserved current splits over the two staggered-hop
directions and reads

```text
    J^{μ,A}_x  =  (1/2) η_μ(x) [ χ̄_x  T̂^A  χ_{x+μ̂}  +  χ̄_{x+μ̂}  T̂^A  χ_x ]
                                                                    (5)
```

where `T̂^A` is the field-index action of the symmetry generator
(`T̂^A χ`)_x := T^A_{xy} χ_y (suppressing summation), and the
two-term structure `χ̄_x χ_{x+μ̂} + χ̄_{x+μ̂} χ_x` arises from the
**bilateral staggered hop** (forward `M_{x,x+μ̂}` and backward
`M_{x,x-μ̂} = -M_{x,x+μ̂}` reindexed with `x' = x - μ̂`). The proof
of the bilateral form is given explicitly in Step 2 below.

The proof of (N2) is the specialisation of (N3) to the U(1) phase
generator (clean infinitesimal-Lie substitution into (5); runner E5
verifies). The proof of (N1) follows a discrete Ward-identity route
(Step 4b below) because two-site translation is a *discrete* symmetry
of `M_KS`, not an infinitesimal Lie generator; the runner E6
verifies the on-shell `∂^L_μ P^μ_x = 0` directly on the explicit (3)
form.

**Review-loop repair clarification (2026-05-03 second pass, then
2026-05-10 gate-recategorization repair):** the original
(5) form `... (χ̄_x χ_{x+μ̂} - χ̄_{x+μ̂} χ_x)/2` (with a minus sign and
only one bilinear term) cannot specialise to (4)'s plus-sign bilateral
form. The corrected (5) above factors the bilateral contribution
explicitly and now closes algebraically when specialised to U(1) phase
(giving (4); E5). The (2Z)^3 sublattice translation case requires a
*discrete* Ward identity (not a literal substitution into (5)) and is
verified directly on (3) by E6. The 2026-05-10 repair retracts the
prior literal-substitution claim `(5) → (3)` and replaces it with the
discrete Ward-identity argument plus the E6 numerical check.

## Proof

The proof is the standard variational Noether argument adapted to
the finite Grassmann lattice action.

### Step 1 — variation of the action under an infinitesimal symmetry

Write `δχ_x = α^A T^A_{xy} χ_y` with `α^A` infinitesimal. The
variation of the action `S_F = χ̄ M χ` is

```text
    δS_F  =  α^A  ( χ̄_x  T^A_{xy}  M_yz  χ_z   +   χ̄_x  M_xy (-T^A_{yz})  χ_z ).
```

For `T^A` to be a *symmetry*, the variation must vanish for arbitrary
χ̄, χ:

```text
    [ T^A , M ]_{xz}   =   T^A_{xy} M_{yz} - M_{xy} T^A_{yz}   =   0.    (6)
```

This is the symmetry condition.

### Step 2 — promote `α` to a slowly-varying lattice field

Now allow `α^A` to depend on the lattice site: `α^A → α^A_x`. The
variation of the action under `δχ_y = α^A_y T^A_{yz} χ_z` and
`δχ̄_x = -α^A_x χ̄_z (T^A)_{zx}` reads

```text
    δS_F[α(x)]
      = Σ_{x,y,z} ( α^A_y - α^A_x )  χ̄_x  M_{xy}  T^A_{yz}  χ_z       (7a)
```

(the constant-α piece `α (T^A M - M T^A)` vanishes by the symmetry
condition (6)).

For the canonical staggered hop `M_{x, x+μ̂} = +(1/2) η_μ(x)` and
`M_{x, x-μ̂} = -(1/2) η_μ(x)`, only nearest-neighbour pairs contribute,
so the sum (7a) splits into a forward-hop piece and a backward-hop
piece:

```text
  forward (y = x+μ̂):
    Σ_{x,μ}  (1/2) η_μ(x) χ̄_x T̂^A χ_{x+μ̂}  ·  ( α^A_{x+μ̂} - α^A_x )
  backward (y = x-μ̂):
    Σ_{x,μ} -(1/2) η_μ(x) χ̄_x T̂^A χ_{x-μ̂}  ·  ( α^A_{x-μ̂} - α^A_x ).
                                                                     (7b)
```

Reindex the backward piece with `x' = x - μ̂` (so `x = x' + μ̂` and
`η_μ(x) = η_μ(x' + μ̂) = η_μ(x')` because `η_μ` depends on the
coordinates `x_1, …, x_{μ-1}` not on `x_μ`):

```text
  backward (after reindex):
    Σ_{x',μ}  (1/2) η_μ(x') χ̄_{x'+μ̂} T̂^A χ_{x'}  ·  ( α^A_{x'+μ̂} - α^A_{x'} ).
```

Combining the forward and (reindexed) backward pieces:

```text
    δS_F[α(x)]
      = Σ_{x,μ}  (1/2) η_μ(x) [ χ̄_x T̂^A χ_{x+μ̂} + χ̄_{x+μ̂} T̂^A χ_x ]
                              ·  ( α^A_{x+μ̂} - α^A_x ).               (7c)
```

Identifying the coefficient of the discrete forward derivative
`(∂^L_μ α^A)_x = α^A_{x+μ̂} - α^A_x`, the conserved current
`J^{μ,A}_x` is the **bilateral form (5)** above. This is the explicit
algebraic derivation requested by the review follow-up.

### Step 3 — on-shell conservation

When the equations of motion `(M χ)_x = 0` and `(χ̄ M)_x = 0` are
satisfied (i.e. classical solutions of the Grassmann action), the
"bulk" piece of `δS_F[α(x)]` vanishes for *any* `α^A_x`, including
constant `α^A`. By global symmetry (`α^A` constant), the action
itself is invariant: `δS_F[constant α] = 0`.

Conversely, for non-constant `α^A_x`, the bulk piece still vanishes
on shell, so

```text
    Σ_x  α^A_x · ∂^L_μ J^{μ,A}_x   =   0                              (9)
```

for any `α^A_x`. By choosing `α^A_x = δ_{x, x_0}` (delta-function
test field), we obtain

```text
    ∂^L_μ J^{μ,A}_{x_0}   =   0   on shell.                          (10)
```

This is the lattice Noether identity.

### Step 4 — specialisation to `(2Z)^3` sublattice translation and U(1) phase

#### Step 4a — U(1) phase → fermion-number current (4)

For `U(1)` phase, `T̂^A χ_y = i χ_y` (the generator is `i` acting as
a multiple of identity). Substituting into the bilateral (5):

```text
    J^μ_x  =  (1/2) η_μ(x) [ χ̄_x · i · χ_{x+μ̂}  +  χ̄_{x+μ̂} · i · χ_x ]
           =  (i/2) η_μ(x) [ χ̄_x χ_{x+μ̂}  +  χ̄_{x+μ̂} χ_x ].          (4a)
```

The `i` factor is the imaginary phase generator. The fermion-number
current (4) is the corresponding **real** charge current, related by
the convention `J^μ_x [real] := -i · J^μ_x [imaginary phase generator]`,
giving

```text
    J^μ_x  =  -(1/2) η_μ(x) [ χ̄_x χ_{x+μ̂}  +  χ̄_{x+μ̂} χ_x ]
                                                                     (4)
```

exactly as stated in (N2). The substitution closes algebraically.

#### Step 4b — `(2Z)^3` sublattice translation → momentum density (3)

**Discrete-vs-infinitesimal caveat (2026-05-10 honest framing).** Two-site
translation is a **discrete** symmetry of `M_KS`, not an infinitesimal
Lie generator on the lattice. The bilateral form (5) is the conserved
current associated with an *infinitesimal* generator `T^A` via the local-α
Ward identity of Step 2. For a discrete generator, the corresponding
conserved current arises from a *finite-difference* Ward identity rather
than a literal `α(x) → α(x+2μ̂) - α(x)` substitution into (5). The
appropriate construction is sketched below; the runner exhibit `E6`
provides direct numerical verification that the canonical staggered
sublattice-momentum density (3) is on-shell divergence-free, which is
what (N1) actually asserts.

**Symmetry condition.** For `(2Z)^3` sublattice translation in direction
`μ`, let `S^{(2μ̂)}` be the two-site shift operator on field indices,
`(S^{(2μ̂)} χ)_y := χ_{y + 2μ̂}`. The symmetry condition is
`M_KS S^{(2μ̂)} = S^{(2μ̂)} M_KS`. Direct check:

```text
    (M_KS)_{x+2μ̂, y+2μ̂}
      = (1/2) η_ν(x + 2μ̂) [ δ_{y+2μ̂, x+2μ̂+ν̂} - δ_{y+2μ̂, x+2μ̂-ν̂} ]
      = (1/2) η_ν(x) [ δ_{y, x+ν̂} - δ_{y, x-ν̂} ]
      = (M_KS)_{xy}
```

(the key step uses `η_ν(x + 2μ̂) = η_ν(x)` for every direction `ν`
because each component of `2μ̂` is even, so the parity sum that
defines `η_ν` is unchanged). The runner's E2 exhibit verifies this
identity to machine precision for all three axis directions.

**Discrete Ward identity.** From the symmetry `[M, S^{(2μ̂)}] = 0`,
the action `S_F[χ̄, χ]` is invariant under `χ → S^{(2μ̂)} χ` ⇔
`χ → S^{(2μ̂)} χ`, `χ̄ → χ̄ S^{(-2μ̂)}`. Promoting this finite shift
to a *site-dependent* discrete shift parameter — equivalent, on the
lattice, to keeping each pair of sites at fixed separation but
modulating an envelope — yields a finite-difference Ward identity
of the form

```text
    Σ_x  ω_x · ∂^L_μ P^μ_x  =  0   on shell,
```

valid for arbitrary lattice envelopes `ω_x`, where `P^μ_x` is the
canonical staggered sublattice-momentum density obtained by inserting
the lattice analogue of `i ∂_μ` into the Grassmann bilinear:

```text
    P^μ_x  =  -(i/2) η_μ(x)  [ χ̄_x ∂^L_μ χ_x  -  ∂^L_μ χ̄_x · χ_x ]
                                                                     (3)
```

with `∂^L_μ χ_x = (χ_{x+μ̂} - χ_{x-μ̂})/2`. By the same argument as
Step 3 applied to `ω_x`, the on-shell identity (10) holds:

```text
    ∂^L_μ P^μ_x   =   0   on shell.
```

This is (N1).

**Honest position on (5) → (3).** The bilateral form (5) is the
infinitesimal Lie current. The canonical staggered momentum density (3)
is the discrete-translation current. The two are *not* related by a
literal infinitesimal-generator substitution `T̂^μ χ_y = χ_{y + 2μ̂}`
into (5) (such a substitution gives a length-3 staggered bilinear, not
the length-1 derivative form (3)). They are related by a **discrete
Ward-identity rearrangement** at the level of the on-shell divergence.
The runner's `E6` exhibit verifies this directly: the explicit (3)
expression has on-shell `∂^L_μ P^μ = 0` to machine precision on a free
pure-staggered block, which is the operational content of (N1). The
prior text claimed `(5) → (3)` as a literal substitution; that claim
is retracted by this 2026-05-10 repair.

#### Step 4c — combined: closure of (5) → (4) and Ward identity for (3)

The bilateral (5) form, derived in Step 2 from the local-α expansion
of the canonical action, specialises to (4) under U(1) phase
substitution (a clean Lie-generator substitution; runner E5 confirms
algebraically). The (2Z)^3 sublattice translation case is handled by
the discrete Ward identity of Step 4b above and is verified directly
by runner E6 on the explicit (3) form. The review follow-up's
"specialisation does not close algebraically" gap is closed for the
U(1) case (E5) and the translation case is closed by the runner-level
direct verification (E6) of the actual claim (N1: `∂^L_μ P^μ_x = 0`
on shell). ∎

### Step 5 — why one-site shifts are not pure translations

For one-site shifts `T_μ̂` (which are NOT in `(2Z)^3`), `η_ν(x +
μ̂)` differs from `η_ν(x)` by a sign for those `ν` where the
parity-sum definition of `η` includes the index `μ`. Concretely
`η_1(x) = +1`, `η_2(x) = (-1)^{x_1}`, `η_3(x) = (-1)^{x_1+x_2}`,
and a shift `x_1 → x_1 + 1` flips both `η_2` and `η_3`. The
substituted operator `S^{(μ̂)} M_KS S^{(-μ̂)}` therefore differs
from `M_KS` by a global sign on the shifted directions; the symmetry
condition (6) fails as stated. The composite operator `S^{(μ̂)}` ⋅
(staggered sign rotation) IS a symmetry — that is the staggered
**taste shift symmetry**, which generates a larger group than `(2Z)^3`
translation. Its conserved current is the staggered taste current,
which is **not** the (2Z)^3 momentum density of (3) and is out of
scope for this note.

## Hypothesis-set summary (after gate-recategorization repair)

The proof uses the two current framework axioms `A1` (Cl(3)) and `A2`
(`(2Z)^3` sublattice translation action) from
`MINIMAL_AXIOMS_2026-05-03.md`, plus
the one named admitted input `staggered_dirac_realization_gate`. The
`g_bare` normalization gate, formerly listed alongside the carrier
gate, is **removed** from the load-bearing input list per the
2026-05-10 audit verdict's explicit option to "remove the structural
`g_bare` dependency if it is not load-bearing": the Noether
identities (N1)–(N3) are quantitatively `g_bare`-independent (see
§"Hypothesis set used" near the top of this note for the precise
non-load-bearing role of `S_G`'s normalization). No imports from the
forbidden list.

The "external import" is the variational Noether technique itself,
which is an elementary finite-Grassmann manipulation, not a primitive
imported as a black box.

## Corollaries (downstream tools)

C1. *Conserved fermion number on the canonical surface.* The
`U(1)` charge `Q = Σ_x χ̄_x χ_x` is a conserved quantum number,
which underlies any "baryon number" / "lepton number" lane on
A_min.

C2. *Discrete sublattice-momentum quantum number.* On a finite
block `Λ` with periodic boundary that respects the `(2Z)^3`
sublattice (i.e. `L_μ` even in every direction), the sublattice
translation symmetry gives discrete `(2Z)^3` momenta `k_μ ∈ {0, 2π/L,
…, π}` as good quantum numbers — the basis on which the package's
spectral / band-structure language depends. The first Brillouin
zone is correspondingly halved in each direction relative to the
naive `Z^3` zone.

C3. *Compatibility with reflection positivity (R2).* The conserved
charge `Q` is `Θ_RP`-invariant (charge is even under reflection
positivity), so the physical Hilbert space `H_phys` decomposes into
fixed-`Q` superselection sectors. This is the structural support
for the package's separate fermion-number / gauge-charge sectors.

C4. *Anomaly slot.* Lattice Noether by itself does not say whether
a *quantum* current remains conserved (anomalies). The
gauge-invariance + flavour-anomaly closure of the package — captured
in the anomaly-forced 3+1 row — is the next layer above the
classical Noether identity here. This note does not claim to
discharge anomaly cancellation.

## Honest status (post-2026-05-10 gate-recategorization repair)

**Bounded theorem on the admitted staggered/Grassmann carrier.** (N1)–
(N3) are proved by the standard variational argument adapted to the
finite Grassmann staggered action, with the `(2Z)^3` sublattice scope
matching what the runner verifies. One named open gate is admitted
explicitly per `MINIMAL_AXIOMS_2026-05-03.md`:
the staggered-Dirac realization gate (carrier of the action `M_KS`).
The `g_bare = 1` canonical-normalization gate, formerly admitted
alongside, is **removed** from this note's load-bearing input list
per the 2026-05-10 audit verdict (Noether identities (N1)–(N3) are
quantitatively `g_bare`-independent).

**Sub-claim status:**

- **(N2) U(1) fermion-number current.** The bilateral form (5)
  specialises cleanly to (4) by infinitesimal Lie-generator
  substitution. Runner E5 verifies `(5) → (4)` to machine precision.
  **Closed form on the admitted staggered carrier.**
- **(N1) `(2Z)^3` sublattice momentum current.** Two-site translation
  is a *discrete* symmetry; the conserved current (3) arises from a
  finite-difference Ward identity, not a literal infinitesimal
  substitution into (5). Runner E2 verifies the symmetry condition
  for `M_KS` under two-site shifts; runner E6 verifies the
  on-shell `∂^L_μ P^μ_x = 0` directly on the explicit (3) form.
  **Closed form on the admitted staggered carrier; the prior
  literal-substitution claim `(5) → (3)` is retracted by this
  repair and replaced by the discrete Ward-identity argument plus
  E6 numerical verification.**
- **(N3) General lattice Noether identity.** The bilateral (5) is
  the conserved current for an *infinitesimal Lie* generator. For
  discrete generators the corresponding current is constructed by
  a discrete Ward identity per Step 4b. Runner E5 + E6 jointly
  confirm both regimes on the admitted staggered carrier.

**When admitted gates close.** When
`MINIMAL_AXIOMS_2026-05-03.md`'s
staggered-Dirac realization derivation target closes (canonical
parent note pending packaging), this row becomes eligible for
retagging from `bounded_theorem` to `positive_theorem` by the
independent audit lane. The structural Noether-identity content
of the proof is unchanged by that closure; only the input-tier of
the carrier moves from "admitted open gate" to "derived from
A1+A2+infrastructure".

**Not in scope.**

- Anomaly closure for the conserved currents at the quantum level.
  That requires the index theorem / anomaly-forced 3+1 row of the
  package's existing retained closure, not the classical Noether
  identity established here.
- Lattice analogue of full energy-momentum tensor conservation.
  We give the discrete `(2Z)^3` sublattice momentum density; the
  full `T^{μν}` requires more careful identifications which are
  deferred.
- The full staggered taste-shift symmetry group (one-site shift
  composed with a staggered sign rotation). That is a strictly
  larger symmetry group than `(2Z)^3` translation alone; its
  conserved current is the staggered taste current and is out of
  scope. Step 5 of the proof documents why one-site shifts alone
  are not pure translations of `M_KS`.

## Load-bearing Dependencies

- Current public framework memo:
  `MINIMAL_AXIOMS_2026-05-03.md`
  (supersedes `MINIMAL_AXIOMS_2026-04-11.md`).

## Citations

- prior cycles in this loop, cited for context rather than as
  load-bearing inputs:
  - `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
- assumption / derivation ledger, cited for package context:
  `docs/ASSUMPTION_DERIVATION_LEDGER.md`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md) —
  current public framework memo; sole upstream framework dependency
  after the 2026-05-10 gate-recategorization repair.

## Admitted context inputs

Per the 2026-05-10 gate-recategorization repair, the following named
admitted inputs are explicitly carried by this row in addition to its
framework-axiom dependency on `minimal_axioms_2026-05-03`:

- `staggered_dirac_realization_gate` — the Grassmann partition with
  staggered Dirac action `M_KS`. Recategorized from prior axiom `A3`
  to an open-gate derivation target by `MINIMAL_AXIOMS_2026-05-03.md`;
  canonical parent note pending packaging. Closure of this gate makes
  this row eligible for retagging from `bounded_theorem` to
  `positive_theorem`.

**Removed (2026-05-10 g_bare-removal repair):**
- `g_bare_canonical_normalization_gate` — formerly listed here as a
  named admission. The 2026-05-10 audit verdict's repair-target option
  "separately close or remove the structural `g_bare` dependency if it
  is not load-bearing" applies: the Noether identities (N1)–(N3) are
  quantitatively `g_bare`-independent, with `S_G` entering only via
  the gauge-invariance hypothesis carried by the admitted
  canonical-action surface, not through the `g_bare` numerical
  normalization gate. The gate is therefore removed from this note's
  named-admission list. Sister authorities and other rows that
  genuinely depend on `g_bare` are unchanged; this removal is local to
  this Noether note's load-bearing chain.
