# Staggered-Dirac AC Upgrade — DHR Framing Audit (Block 01)

**Date:** 2026-05-07
**Type:** scoping audit
**Claim type:** open_gate audit + framing reanalysis
**Status:** scoping note auditing the DHR-superselection framing of
substep 4 in the prior staggered-Dirac realization campaign (Block 05,
PR #635). Identifies that the DHR framing is INCOMPATIBLE with the
framework's retained Reeh-Schlieder + cluster decomposition (which
together imply unique vacuum, no DHR superselection sectors on
canonical surface). Proposes reformulation as direct three-state
derivation in single H_phys.
**Authority role:** branch-local scoping note. Audit verdict and
effective status are set only by the independent audit lane.
**Loop:** staggered-dirac-ac-upgrade-20260507 (Block 01)
**Branch:** physics-loop/staggered-dirac-ac-upgrade-block01-20260507

## Question

Block 05 of the prior staggered-dirac-realization-gate-20260507
campaign (PR #635 OPEN, [`STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md))
closed substep 4 of the staggered-Dirac realization gate as
`bounded_theorem` with admitted-context AC (Hilbert/no-proper-quotient
semantics for DHR superselection on the framework's accepted physical-
Hilbert surface). The DHR framing was the load-bearing closure step.

**Question:** is the DHR framing CORRECT given the framework's
retained primitive stack? Or is there a structural mismatch that
would allow a simpler closure WITHOUT admitted-context AC?

## Answer

**The DHR framing is structurally incompatible with the framework's
retained primitive stack.** Three retained theorems jointly imply
H_phys has UNIQUE VACUUM with NO DHR superselection sectors:

1. **Reflection positivity A11** (retained per
   [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)):
   OS reconstruction yields a single GNS-like Hilbert space `H_phys`
   with global cyclic vacuum |Ω⟩.

2. **Reeh-Schlieder cyclicity** (retained per
   [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)):
   For any nonempty open region `O ⊂ Λ`, the local algebra `A(O)`
   acts cyclically on |Ω⟩: `A(O)|Ω⟩` is dense in `H_phys`.

3. **Cluster decomposition** (retained per
   [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)):
   Connected correlators decay exponentially, GUARANTEEING the
   vacuum is unique (verbatim from RS note Section "Retained inputs":
   "guaranteeing the vacuum is unique (no superselection sectors on
   the canonical surface)").

These three together imply: **the framework's H_phys has a unique
vacuum and a single superselection sector on the canonical surface.**

This is INCOMPATIBLE with Block 05's DHR framing, which appealed to
"three superselection sectors of H_phys."

## DHR's three classical assumptions vs retained primitives

DHR superselection theory (Doplicher-Haag-Roberts 1971-1974) requires:

### DHR Assumption 1: Local algebra net structure A(O)

**Retained equivalent:** `RP A11 OS reconstruction` provides
`A(O) := { polynomials in fields restricted to lattice sites in O }`
on each open region `O ⊂ Λ`. The `A(O)` net structure IS retained.

**Status:** ✓ retained.

### DHR Assumption 2: Translation covariance

**Retained equivalent:** `Lattice translations T_x, T_y, T_z` act on
`A(O)` by spatial translation. Single-clock evolution + Lieb-Robinson
provide unitary translation operators on `H_phys`.

**Status:** ✓ retained.

### DHR Assumption 3: Existence of distinct superselection sectors

**This is where DHR FAILS for the framework.**

DHR's third assumption requires the Hilbert space to admit
DECOMPOSITION into superselection sectors `H_phys = ⊕_α H_α` where
each `H_α` is invariant under `A(O)` (i.e., local operators don't
mix sectors). DHR sectors are constructed via charged intertwiners
that map between sectors but commute with translations.

**Per Reeh-Schlieder + cluster decomposition retained:** The
framework's `H_phys` has a UNIQUE vacuum |Ω⟩. By RS, `A(O)|Ω⟩` is
DENSE in `H_phys`. This means `H_phys` has only ONE superselection
sector — the vacuum sector — because the local algebra acting on
the unique vacuum reaches every state in `H_phys`.

If `H_phys = ⊕_α H_α` had α ≥ 2, the local algebra acting on |Ω⟩ ∈ H_α=0
could only reach `H_α=0` (locality preserves sectors). But RS says
`A(O)|Ω⟩` is dense in ALL of `H_phys`. Contradiction. Hence α = 1
(single sector).

**Status:** ✗ INCOMPATIBLE with retained primitive stack.

## Block 05's misframing — explicit

Block 05's Step 4 wrote:

> "Apply to the framework: the M_3(C) algebra on hw=1 is irreducible
>  under the C_3[111] generator. The three corners (1,0,0), (0,1,0),
>  (0,0,1) provide three minimal projectors `P_(1,0,0), P_(0,1,0),
>  P_(0,0,1)` in M_3(C) ... by DHR, the three projectors define three
>  superselection sectors of H_phys."

This is wrong. The three corners are three orthogonal STATES within
`H_phys`, not three superselection sectors. The M_3(C) algebra is a
sub-algebra of the FULL local operator algebra `A(Λ)`, and the three
corner-states are three DISTINCT MOMENTUM EIGENSTATES connected by
the C_3[111] generator (which is also in `A(Λ)`).

States connected by elements of `A(Λ)` are in the SAME superselection
sector by definition. C_3[111] is an element of `A(Λ)` (a lattice
symmetry operator). Therefore the three corner states are in the same
superselection sector.

## The correct framing: three states in single H_phys

The retained framework's "physical species" reading of three matter
generations is:

```
Three matter generations = three quantum-mechanically distinct STATES
in H_phys, characterized by:
  - Distinct simultaneous-eigenvalues of T_x, T_y, T_z
    (translations diag(−1,+1,+1), diag(+1,−1,+1), diag(+1,+1,−1))
  - Connected by C_3[111] cyclic generator (within A(Λ))
  - Carrying the M_3(C) algebra structure (irreducible, no proper
    quotient)
```

These are three flavor states (three "types" of fermion mode), not
three superselection sectors. They live in one H_phys. The C_3[111]
generator transitions between them.

This matches the SM phenomenology: three generations of fermions are
three flavor states connected by W-boson-mediated charged-current
interactions (which transition between flavors); they are NOT three
separate Hilbert spaces.

## Direct framework-derived three-state theorem (Block 02 target)

The target reformulated substep-4 theorem:

```
On A1+A2 + Block 02-04 of prior campaign + retained primitives:

The hw=1 BZ-corner triplet of the staggered-Dirac realization
identifies as three quantum-mechanically distinct STATES in the
RP-OS-reconstructed physical Hilbert space H_phys, with:
  (a) distinct joint translation eigenvalues (Block 04 retained),
  (b) connected by C_3[111] within A(Λ) (Block 04 retained),
  (c) M_3(C) algebra structure (THREE_GENERATION_OBSERVABLE retained),
  (d) no proper exact quotient (THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT retained).

These three states are the framework's three SM matter generations.
```

**Crucially:** this derivation uses ONLY retained primitives (RP A11,
Reeh-Schlieder, cluster decomposition, Lieb-Robinson, lattice Noether,
single-clock evolution, M_3(C) on hw=1, no-proper-quotient,
translation algebra on Z³). NO HK + DHR appeal. NO admitted-context AC.

The substep-4 status would upgrade from `bounded_theorem` (with AC)
to **positive_theorem** (no admitted-context).

The synthesis Block 06 (`STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07`)
would then upgrade from `bounded_theorem` (synthesis tier) to
**positive_theorem** (full retained synthesis), conditional only on
S2 re-audit (the Block 02 dependency, audit-lane work).

## Status

```yaml
actual_current_surface_status: scoping audit + framing reanalysis
target_claim_type: open_gate audit
conditional_surface_status: |
  Conditional on:
   (a) the cited retained Reeh-Schlieder + cluster decomposition
       theorems being correctly interpreted as ruling out DHR
       superselection sectors on the canonical surface;
   (b) the M_3(C) algebra and translation characters retained per
       the prior campaign Block 04;
   (c) the C_3[111] cyclic generator being an element of A(Λ)
       (lattice symmetry operator).
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  This is a scoping note auditing Block 05's DHR framing of substep 4.
  Identifies a structural incompatibility with the retained primitive
  stack and proposes a reformulated direct three-state derivation
  that closes substep 4 without admitted-context AC.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- Identifies the structural mismatch between Block 05's DHR framing
  and the retained Reeh-Schlieder + cluster decomposition theorems
- Proposes the reformulated direct three-state derivation as the
  Block 02 target
- Sets up the AC upgrade path: substep 4 from `bounded_theorem` (with
  AC) to `positive_theorem` (no admitted-context)

## What this does NOT close

- The substep-4 reformulation itself (Block 02 task)
- The AC upgrade itself (Blocks 02-05 of this campaign)
- The synthesis upgrade (Block 06 of prior campaign — to be promoted
  upon AC closure)

## Cross-references

- Sister campaign (prior): staggered-dirac-realization-gate-20260507
- Prior synthesis: [`STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md)
- Prior substep 4 (DHR framing — this audit identifies as misframed): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md)
- Reeh-Schlieder retained: [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
- Cluster decomposition retained: [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- RP A11 retained: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Three-generation observable retained: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Three-generation no-proper-quotient retained: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
- Standard methodology: Streater-Wightman 1964, Haag 1992 (Reeh-Schlieder + cluster decomposition exclude DHR superselection in single Hilbert space)
