# g_bare Constraint vs Convention — Convention-Layer Restatement

**Date:** 2026-05-07
**Claim type:** positive_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide its audit and effective status.
**Primary runner:** [`scripts/frontier_g_bare_audit_residual_closure.py`](../scripts/frontier_g_bare_audit_residual_closure.py)

## 0. Audit context

This note strengthens
`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`
in response to the audit verdict that classified the 2026-05-03
candidate as `audited_conditional`:

The prior blocker was that the 2026-05-03 row relied on a rescaling-freedom
authority that the audit lane classified as decoration rather than an active
theorem-grade authority. The present note therefore has to stand or fall on a
strengthened, independently auditable dependency rather than on a status label.

The present note follows the *first* repair path: it cites the
**strengthened** rescaling-freedom closure
[`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md),
which is a positive_theorem candidate (not a decoration) under the
joint trace-AND-Casimir rigidity argument.

In addition, this note **cleanly characterizes the convention layer**
in the framework's `g_bare` chain by exhibiting it precisely as the
overall normalization scalar `N_F` of the Hilbert–Schmidt trace form
on `g_conc = su(3) ⊂ End(V)`. Everything else in the chain is
derived. This is the cleanest convention-vs-derivation framing the
parent note's "constraint or convention?" question can take, and it
is independent of any specific basis choice.

## 1. Claim scope

> **Theorem (Constraint-vs-convention restatement, four-layer
> stratification).** Let `V = C^8` carry the framework Hilbert-space
> inner product (axiom-level, imported through the physical-lattice
> retention chain). Let `g_conc = su(3) ⊂ End(V)` be the derived
> gauge subalgebra in the canonical triplet block as fixed by
> [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
> Claim 1, with Hilbert–Schmidt rigidity on `g_conc` as in
> [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
> (R1)–(R5). Then the framework's `g_bare = 1` chain has exactly
> **four** layers, of which exactly **one** is a convention:
>
> | Layer | Statement | Status | Evidence |
> |---|---|---|---|
> | L1 | `Cl(3)` algebra structure on `V = C^8` (anticommutator `{G_μ, G_ν} = 2δ_{μν}`) | **DERIVED** (axiom A1) | minimal axioms note |
> | L2 | Hilbert–Schmidt trace form `B_HS` on `g_conc` is the unique Ad-invariant form up to overall scalar | **DERIVED** (Killing rigidity) | HS rigidity theorem (R1) |
> | L3 | Overall scalar `N_F` of `B_HS` (i.e. `Tr(T_a T_b) = N_F · δ_{ab}`) | **CONVENTION** (admitted) | choice = `1/2` (canonical Gell-Mann) |
> | L4 | `g_bare = 1` (i.e. Wilson `β = 2 N_c / g_bare² = 6` at `N_c = 3`, `N_F = 1/2`) | **DERIVED** (constraint) | algebra below |
>
> Equivalently:
>
> **(C1) Cl(3) gives a unique HS trace structure.** The
> Hilbert–Schmidt trace form `B_HS` on `g_conc ⊂ End(V)` is structurally
> determined by the Cl(3) → End(V) embedding plus Killing rigidity.
> No basis or scalar choice enters at this stage (Layer L2).
>
> **(C2) The normalization of the trace is the convention layer.** The
> overall positive scalar `N_F` of `B_HS` (equivalently, `T_F` in the
> particle-physics literature) is the single admitted convention. The
> framework adopts `N_F = 1/2` (canonical Gell-Mann), but any other
> positive `N_F'` would equally well preserve all the structural
> theorems — only the *numerical face* of `g_bare` would change
> (Layer L3).
>
> **(C3) The Casimir is derived.** Once `N_F` is fixed, the quadratic
> Casimir `C_F = (8/3) N_F` follows by Schur + Tr_3 evaluation. At
> `N_F = 1/2` this gives `C_F = 4/3` (Layer L4 input).
>
> **(C4) `g_bare = 1` is a derived constraint.** Under the canonical
> normalization `N_F = 1/2`, the Wilson plaquette small-`a` matching
> forces `β = 2 N_c / g_bare²`. At `N_c = 3` and `β = 2 N_c = 6`
> (the value forced by canonical normalization in the absence of any
> scalar pre-factor on `A_op`), the unique rational solution is
> `g_bare² = 1`, i.e. `g_bare = 1`. This is class (A) algebra; no
> separate convention layer at `g_bare` (Layer L4).
>
> **(C5) Alternative `g_bare ≠ 1` requires a non-canonical `N_F`.**
> Any alternative `g_bare² ≠ 1` at `N_c = 3` and `β = 6` either:
> - violates `N_F = 1/2` by introducing a hidden generator dilation
>   (forbidden by Hilbert–Schmidt rigidity (R3)), or
> - requires an external scale beyond A1 + A2 (no such scale exists
>   in the framework axioms).
>
> Therefore the framework has **exactly one convention layer** in the
> `g_bare` chain — the choice `N_F = 1/2` of the overall HS scalar —
> and `g_bare = 1` is a derived constraint relative to that
> convention.

The theorem **does not** claim:

- that `N_F = 1/2` itself is uniquely forced by `A1` (Cl(3)) and `A2`
  (Z^3) alone — the absolute convention status of `N_F` is the
  remaining open foundational question;
- that the Wilson plaquette action form is uniquely forced (separate
  retention via A2.5);
- closure of the deeper "absolute derivation of `g_bare = 1` from A1+A2"
  Nature-grade target.

## 2. Why the four-layer stratification is the cleanest framing

The parent's "constraint or convention?" question is genuinely
ambiguous because it conflates *several* potential convention layers.
Pre-2026-05-03, the literature framing oscillated between:

1. *"`g_bare = 1` is itself the Wilson canonical-normalization
   convention"* — the narrow convention-theorem reading
   (`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`);
2. *"`g_bare = 1` is a structural constraint relative to the canonical
   `Tr(T_a T_b) = δ/2` normalization"* — the 2026-05-03 constraint
   reading
   (`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`);
3. *"`g_bare = 1` is a Hamiltonian no-independent-coupling fact"* —
   the rigidity-theorem reading
   (`G_BARE_RIGIDITY_THEOREM_NOTE.md`).

The four-layer stratification reconciles all three:

- **The narrow convention reading (1)** lives at L4 and is *false* as
  stated. `g_bare = 1` is not itself the convention; it is the derived
  constraint at L4.
- **The 2026-05-03 constraint reading (2)** lives at L4 and is *correct*
  but its load-bearing input was insufficiently distinguished from the
  basis-specific values (resulting in the decoration demotion).
- **The rigidity reading (3)** lives at L2 (and, in coordinate-form,
  at L4). It correctly identifies that there is no independent scalar
  parameter at the Hamiltonian operator level — the form is fixed up
  to overall scalar by Killing rigidity.

The stratification places the convention exactly at L3 — the **scalar
choice** `N_F` — and is silent about basis (basis is L2 ambiguity, no
content) and silent about `g_bare` being a separate convention (it is
not — `g_bare = 1` is the L4 derived constraint).

## 3. Declared audit dependencies (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) | unaudited (positive_theorem candidate in this landing) | provides the joint trace-AND-Casimir rigidity statement (R3); the load-bearing input that no `c ≠ ±1` preserves both invariants simultaneously |
| [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) | unaudited | provides Cl(3) -> End(V) embedding canonicity (Claim 1) and Ad-invariant form identification (Claim 2), used in the four-layer stratification proof |

The dependency on `cl3_color_automorphism_theorem` propagates as
two-hop via either parent and is therefore not load-bearing for the
present argument. The HS rigidity theorem is **not** a decoration of
`cl3_color_automorphism_theorem`, so the present note's dependency
chain is well-founded under the strengthened rescaling-removal route.

## 4. Load-bearing step (class A)

```text
Inputs:
  V = C^8 with fixed Hilbert-space inner product (axiom-level)
  g_conc = su(3) ⊂ End(V)                  (structural normalization Cl. 1)
  B_HS Ad-invariant on g_conc, unique up to scalar k > 0 (HS rigidity R1)
  Joint rigidity: no c ≠ ±1 preserves both Tr Gram AND Casimir (HS rigidity R3)
  Wilson small-a matching: β = 2 N_c / g_bare²              (standard QCD)

Layer L1 (axiom A1):
  Cl(3) anticommutator {G_μ, G_ν} = 2δ_{μν} I_8 holds in the chiral rep
  on V = C^8. (Verified algebraically; no convention.)

Layer L2 (Killing rigidity, derived):
  B_HS is the unique Ad-invariant form on g_conc up to overall scalar.
  No basis or scalar enters at L2; only the FORM is fixed.

Layer L3 (overall scalar N_F, ADMITTED CONVENTION):
  Choose B_HS-orthonormal basis {T_a} with
       Tr_{V_3}(T_a T_b) = N_F · δ_{ab}.                    (NF)
  The framework adopts N_F = 1/2 (canonical Gell-Mann). Any other
  N_F' > 0 would equally well close the framework theorems; only the
  numerical face of g_bare changes.

Layer L4 (derived constraint):
  Step 4a (Casimir derivation):
    Schur + Tr_3 gives 3 C_F = Σ_a Tr_3(T_a T_a) = 8 N_F,
    so C_F = (8/3) N_F.                                     (CF)
    At N_F = 1/2: C_F = 4/3 (matches SU3_CASIMIR_FUNDAMENTAL).

  Step 4b (Wilson coefficient derivation):
    Under canonical normalization (N_F = 1/2), the connection is
    A_op = Σ_a A^a T_a with no scalar pre-factor. The Wilson
    small-a matching at this normalization gives
       β = 2 N_c                                              (β-WM)
    (verified explicitly in the runner Section C). At N_c = 3,
       β = 6.

  Step 4c (g_bare derivation as constraint):
    The Wilson β formula β = 2 N_c / g_bare² (Wilson matching identity)
    combined with β-WM gives
       2 N_c = 2 N_c / g_bare²
       g_bare² = 1                                           (g-DR)
    i.e. g_bare = 1 as a class (A) rational identity.

  Step 4d (No alternative without violating L2-L3):
    Any g_bare² ≠ 1 at N_c = 3, β = 6 either:
    (a) requires a generator dilation T_a → c T_a with c² = g_bare^{-2}
        ≠ 1, which violates the canonical N_F = 1/2 (a Layer L3
        choice); under HS rigidity (R3) this also violates the joint
        trace-Casimir rigidity. Forbidden.
    (b) requires an external scale that A1 + A2 do not provide. No
        such scale exists; would require additional axiom. Forbidden.

Conclusion (class A):
  The framework's g_bare chain has exactly one convention layer
  (L3: the choice N_F = 1/2), and g_bare = 1 is the derived constraint
  at L4. There is no separate g_bare convention layer.
```

The load-bearing step is class (A) — algebraic identities throughout,
with classical Lie-algebra inputs (Killing rigidity, Schur lemma) at
L2 and Wilson small-`a` matching at L4b.

## 5. Why this differs from the 2026-05-03 candidate

The 2026-05-03 candidate addressed the constraint reading via a
load-bearing rescaling-removal input that was subsequently demoted to
decoration. The present candidate addresses the *same* constraint
reading via the strengthened
[`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
rescaling-removal input, plus an additional **four-layer
stratification** that exhibits the convention layer explicitly at L3
(the overall HS scalar `N_F`).

The four-layer framing is the genuine independent content beyond the
2026-05-03 candidate. It reformulates the constraint reading not as a
two-line algebraic substitution under an upstream normalization, but
as an explicit characterization of *which layer* is the convention
(L3) and *why every other layer* is structurally forced (L1: axiom;
L2: Killing rigidity; L4: derived from L1-L3 under Wilson matching).
This characterization is independent of any basis-specific value
statement.

## 6. Why this differs from the narrow convention theorem

The
`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`
classifies `g_bare = 1` itself as the Wilson canonical-normalization
convention. Under the four-layer stratification, this reading places
the convention layer at L4 (i.e., at `g_bare`), which is *incorrect*
under the strengthened argument: L4 is the derived constraint, and the
true convention is at L3 (the overall HS scalar).

The narrow theorem is therefore a *historically valuable but
imprecise* convention reading. It is correct in spirit ("`g_bare = 1`
is admitted, not derived from absolute principles") but incorrect in
location ("`g_bare = 1` is the convention itself"). The honest
convention layer is one level upstream, at the choice of `N_F`.

The present theorem subsumes the narrow theorem's reading: anyone
adopting the narrow theorem can equivalently say "I am admitting
`N_F = 1/2`, and `g_bare = 1` follows as a derived constraint." This
is a more honest framing because it locates the convention precisely
and shows that `g_bare` itself is forced by the rest of the chain.

## 7. Verification

```bash
python3 scripts/frontier_g_bare_audit_residual_closure.py
```

Verifies, in `Section I`:

1. The four-layer stratification is exhibited algebraically:
   L1 (axiom Cl(3)), L2 (HS form rigidity, numerical Ad-invariance
   check), L3 (overall scalar `N_F` admitted), L4 (`g_bare = 1`
   derived).
2. The Casimir identity `C_F = (8/3) N_F` is verified at multiple
   `N_F ∈ {1/2, 1, 2, 1/4}` (each preserves the structural form;
   only the numerical face of `g_bare` changes).
3. The Wilson coefficient `β = 2 N_c = 6` at `N_c = 3` and `N_F = 1/2`
   is verified by exact rational arithmetic (Layer L4b).
4. The unique `g_bare² = 1` at `β = 6` is verified by exact rational
   arithmetic (Layer L4c).
5. Alternative `g_bare² ∈ {1/2, 2, 4}` requires `β ∈ {12, 3, 3/2}`
   respectively, all incompatible with the canonical-normalization
   forced `β = 6` (Layer L4d, case a).
6. The convention layer at L3 is shown to be *single-valued*: only one
   convention scalar `N_F` is admitted; everything else (basis, form,
   Casimir, `g_bare`) is derived from it.

Representative runner checks:

```
[PASS] L1 (axiom A1): {G_μ, G_ν} = 2δ_{μν} I_8 (Cl(3) anticommutator)
[PASS] L2 (Killing rigidity): B_HS is Ad-invariant on g_conc
[PASS] L3 (convention): N_F = 1/2 admitted, alternatives N_F ∈ {1, 2, 1/4} also valid form choices
[PASS] L4a (Casimir derived): C_F = (8/3) N_F at all tested N_F values
[PASS] L4b (Wilson coeff derived): β = 2 N_c = 6 at N_F = 1/2, N_c = 3
[PASS] L4c (g_bare derived): g_bare² = 1 at β = 6 (exact rational)
[PASS] L4d (no alternative): g² ≠ 1 incompatible with canonical normalization
[PASS] Single convention layer: only L3 is admitted; L1, L2, L4 all derived
```

## 8. Review-lane disposition (audit queued)

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  The framework's g_bare chain has exactly one convention layer (Layer
  L3: the overall scalar N_F of the Hilbert-Schmidt trace form, set to
  N_F = 1/2 in canonical Gell-Mann normalization), and g_bare = 1 is
  the derived constraint at Layer L4 (Wilson small-a matching combined
  with the canonical-normalization-forced β = 2 N_c). All other layers
  (L1: Cl(3) axiom; L2: HS form rigidity; L4: g_bare value) are
  derived. The honest convention status is: ONE admitted scalar; no
  separate g_bare convention layer.
proposed_load_bearing_step_class: A
declared_one_hop_deps:
  - g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07
  - g_bare_structural_normalization_theorem_note_2026-04-18
independent_audit_required_before_effective_status_change: true
parent_update_allowed_only_after_independent_audit_accepts_child_rows: true
distinguishing_content_from_2026-05-03: |
  The 2026-05-03 candidate's rescaling-removal dep was demoted to
  decoration. The present candidate cites the strengthened (joint
  trace-AND-Casimir rigidity) HS rigidity theorem instead, which is
  not a decoration. In addition, the present candidate adds the
  four-layer stratification that exhibits the convention layer
  explicitly at L3 (overall HS scalar) — this is the cleanest
  characterization of the convention status, independent of basis.
```

## 9. What this candidate can support after independent audit acceptance

- The constraint reading of `g_bare = 1` as the L4 derived constraint
  under the L3 admitted convention `N_F = 1/2`.
- A future re-audit of `G_BARE_DERIVATION_NOTE.md`,
  after the independent audit lane has reviewed this row and the companion HS
  rigidity theorem note.
- A clean handoff to downstream rows depending on `g_bare = 1`: such
  rows may cite this note for the constraint reading after audit acceptance,
  with the convention status explicitly localized at L3.

## 10. What this theorem does NOT close

- The convention-vs-derivation status of `N_F = 1/2` itself (the
  Layer L3 convention). This is **not** closed here; it is precisely
  the *one* convention layer in the framework's `g_bare` chain.
  Reclassifying `N_F = 1/2` from convention to derivation would require
  closing the deeper question of whether the canonical Gell-Mann
  normalization is uniquely forced by Cl(3) algebraic structure
  alone — a separate Nature-grade target.
- The choice of the Wilson plaquette action form (Symanzik / improved
  actions remain outside this scope; A2.5 is a separate audit target).
- The deeper question of whether the framework's normalization
  axioms are themselves derivable from `A1 + A2` alone.
- The parent-status update of
  `G_BARE_DERIVATION_NOTE.md`
  itself; this candidate addresses one of the three named repair
  targets but does not close the full parent-update path by itself.

## 11. Cross-references

- `G_BARE_DERIVATION_NOTE.md` — parent
  note that may cite this candidate as the strengthened constraint-
  vs-convention restatement after independent audit acceptance.
- `G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`
  — the 2026-05-03 candidate that the present theorem strengthens.
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — declared one-hop dep providing the joint trace-AND-Casimir
  rigidity statement (R3).
- `G_BARE_RIGIDITY_THEOREM_NOTE.md`
  — sister Hamiltonian-level rigidity argument (no independent scalar
  coupling). The present theorem is its Wilson-action-side packaging
  with explicit four-layer stratification.
- `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`
  — historical narrow convention reading; subsumed by the four-layer
  stratification (which places the convention precisely at L3 rather
  than at L4).
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  — declared one-hop dep providing the Cl(3) → End(V) embedding
  canonicity (Claim 1) and Ad-invariant form identification (Claim 2).
- `SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`
  — provides `C_F = 4/3` at canonical `N_F = 1/2`, the L4a derived
  consequence at the canonical normalization.
- `MINIMAL_AXIOMS_2026-05-03.md`
  — current framework axiom set (A1, A2). The present theorem
  documents that `g_bare = 1` is derived relative to the L3 admitted
  convention `N_F = 1/2`; this is consistent with the open-gate
  treatment in the minimal axioms note.

## 12. Honest scoping summary

The four-layer stratification (L1 axiom; L2 Killing rigidity; L3
admitted scalar `N_F`; L4 derived `g_bare = 1`) is the cleanest
convention-vs-derivation framing the parent note's question can take.
It is independent of basis, it locates the convention precisely at
the overall scalar `N_F`, and it shows that `g_bare = 1` is a derived
constraint at L4 — not a separate convention.

What this theorem is honestly **not**: a derivation of `N_F = 1/2`
itself from `A1 + A2`. That is the genuine remaining open
foundational question, and this theorem cleanly identifies it as
the *single* remaining convention layer. If a future Nature-grade
result derived `N_F = 1/2` from Cl(3) algebraic structure alone, the
framework would be complete on the `g_bare` lane; until then, `N_F`
remains the one explicit convention scalar.
