# Conditional Poisson Forcing under the Self-Consistency Identification (Bounded)

**Status:** bounded conditional theorem. The note proves a class-A algebraic
implication: *if* the field operator `L` and the propagator Green's function
`G_0 = H^{-1}` (with `H = -Delta_lat` on `Z^3`) satisfy the closure
identification `L^{-1} = G_0`, *then* `L = G_0^{-1} = H = -Delta_lat`. The
load-bearing identification `L^{-1} = G_0` is **stipulated**, not derived
from the Cl(3)-on-Z^3 axiom in this note. The note is therefore a
**conditional Poisson-forcing statement under a stipulated closure identity**,
not an unconditional derivation.
**Date:** 2026-04-14 (audit-narrowing refresh: 2026-05-10)
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only.

## Status

**Conditional closure (under stipulated identity).** Once the closure identity
`L^{-1} = G_0` is stipulated, the Poisson-forcing step `L = H = -Delta_lat`
follows by class-A inversion. The earlier "no restriction on the operator
class" framing referred to the algebraic step downstream of the stipulated
identity — it does **not** address whether the identity itself is forced by
the Cl(3) axiom.

This note **does not** upgrade the Poisson derivation from "unique within the
TI + SA + NN class" to "uniquely forced by the framework axiom." It only
records a bounded conditional implication: *given the stipulated closure
identity*, the operator-class restrictions follow as algebraic consequences.

## Theorem / Claim (conditional, bounded)

**Conditional claim.** Let `H = -Delta_lat` be the nearest-neighbor hopping
Hamiltonian on `Z^3`. Let `G_0 = H^{-1}` be the propagator's Green's function.
Let `L` be the linear operator in the field equation `L phi = -rho`.
**Hypothesis** (stipulated, not derived in this note): the closure
identification `L^{-1} = G_0` holds. **Conclusion:** `L = G_0^{-1} = H =
-Delta_lat` (Poisson), and the NN / TI / SA properties are algebraic
consequences of this conclusion.

The hypothesis `L^{-1} = G_0` is a **stipulated closure identification**
within this note, not a theorem of pure algebra and not a derivation from
the Cl(3) axiom. The audit verdict explicitly flags this: a separate retained
bridge theorem is required to derive `L^{-1} = G_0` from the framework axiom
rather than to identify it by closure.

**Conditional corollary.** *Under the stipulated identity*, a non-nearest-
neighbor operator cannot arise. Without the stipulated identity, this note
makes no claim about which operator classes can or cannot arise.

## Assumptions

1. **A1: Cl(3) on Z^3** (the framework axiom — does not by itself imply A2).
2. **A2 (stipulated, not derived in this note): closure identification** —
   `L^{-1} = G_0`.

A2 is treated here as a stipulated identification, not as a derived
consequence of A1. The earlier phrasing "framework's own closure requirement"
is retained below for context but should be read as a *physical-modelling
identification* that this note imposes as a hypothesis, not as a class-A
algebraic consequence of A1. The retained bridge theorem deriving A2 from A1
is the open D-row gap (see "What Remains Open").

Absent from the assumption list (algebraic consequences of A2, not extra
inputs):

- L is translation-invariant (consequence of `L = H` *given A2*)
- L is self-adjoint (consequence of `L = H` *given A2*)
- L is nearest-neighbor (consequence of `L = H` *given A2*)

These are algebraic consequences of the conditional claim. They are **not**
unconditional — they hold only given the stipulated closure identification
A2.

## What Is Actually Proved (conditional, bounded)

**The conditional algebraic chain (given A2):**

1. The NN hopping Hamiltonian on `Z^3` is `H = -Delta_lat` (lattice structure).

2. The propagator's Green's function is `G_0 = H^{-1}` (propagator definition
   on this lattice).

3. **Hypothesis A2 (stipulated):** `L^{-1} = G_0`. This is the load-bearing
   identification; the audit verdict flags it as not derived from A1 in this
   note.

4. By class-A inversion of A2: `L = G_0^{-1} = H = -Delta_lat`.

This chain is a class-A algebraic implication conditional on A2. Step 3 is
the open derivation gap; steps 1, 2, and 4 are routine.

**Numerical verification (downstream of stipulated A2; the runner does NOT
verify A2 itself):**

- CHECK 1: `G_0^{-1} = H` verified on 12^3 lattice, 50 random columns,
  max residual 6.66e-16. (Class-A inversion check.)

- CHECK 2: `H` has nonzero entries ONLY at diagonal and NN sites
  (1000 diagonal + 5400 NN off-diagonal, zero beyond-NN). (Sparsity
  diagnostic of `H`.)

- CHECK 3: `H` is self-adjoint (`||H - H^T||_F = 0`) and translation-invariant
  (uniform stencil at all 200 tested interior sites). (Symmetry diagnostic
  of `H`.)

- CHECK 4: Closure-condition consistency check: when `L = H`, the field
  Green's function equals the propagator Green's function with zero
  mismatch. (Tautological once A2 is stipulated; documents that A2 is
  consistent with `L = H`, not that A2 is forced by A1.)

- CHECK 5: NNN perturbations `L_eps = H + eps * H_NNN` break the closure
  identity. Mismatch at `eps = 0`: 0.00e+00. Mismatch at `eps = 0.001`:
  3.36e-03. Mismatch grows monotonically with `eps`. (Documents that
  candidate non-NN operators violate A2 if A2 is imposed; does not
  derive A2 from A1.)

- CHECK 6: Dense verification on 8^3 lattice: `G_0^{-1} = H` entry-by-entry
  to 1.15e-14. `G_0` itself is dense (100% fill, long-range), but `G_0^{-1}`
  is sparse (NN only, 1296 nonzeros). (Class-A inversion fidelity.)

- CHECK 7: All 11 preceding checks pass.

Total: PASS=12, FAIL=0. The runner output supports the conditional
class-A inversion `L = H` *given A2*; it does **not** support deriving A2
from A1.

## What Remains Open

The hypothesis A2 (`L^{-1} = G_0`) is **stipulated**, not derived from A1
in this note. The audit verdict explicitly identifies the open derivation
gap as: **a retained bridge theorem deriving `L^{-1} = G_0` from the Cl(3)
on Z^3 axiom rather than identifying it by closure**.

Heuristic motivation (not a proof, recorded for context only):

- the propagator generates the density `rho = |psi|^2`;
- the density sources the field via `L phi = -rho`;
- the field modifies the propagator via `H(phi) = H + phi`;
- at a stipulated linearized fixed point one can identify `L^{-1} = G_0`.

These four bullets are **physical-modelling motivation**, not a class-A or
class-B proof. They do not constitute a derivation of A2 from A1. A retained
bridge theorem closing this gap is the open D-row deliverable for this row.

**What this does NOT close:**

- A2 itself (the stipulated closure identification — the open D-row gap);
- the unconditional Poisson-forcing claim (which would require A2 derived
  from A1, not stipulated);
- the broader gravity bundle (Tier 3-4 claims like conformal metric,
  geodesic equation, strong-field regime) which remains bounded per the
  sub-bundle note.

This note records only the bounded conditional implication "given A2, the
Poisson operator class follows as algebraic consequences."

## How This Changes The Paper

### Before this note

Codex status: "The new Poisson uniqueness theorem is good, but it only closes
the narrowed TI + self-adjoint + nearest-neighbor family."

The open question: could a non-NN operator arise from the framework's
self-consistency loop?

### After this note (conditional, bounded)

This note **does not** close that question unconditionally. It records a
**conditional implication**: *given the stipulated closure identification
`L^{-1} = G_0`*, the Poisson operator class follows by class-A inversion.
The stipulated identification is the open D-row gap — see "What Remains
Open."

The class-A conditional implication is summarized as:

| | Narrowed unconditional theorem (other note) | Conditional implication (this note) |
|---|---|---|
| **Input** | `L` is TI + SA + NN | **Hypothesis A2 (stipulated):** `L^{-1} = G_0` |
| **Method** | Search over operator family | Class-A inversion of stipulated identity |
| **Output** | Poisson unique in the class | **Conditional**: `L = H = -Delta` *given A2* |
| **TI/SA/NN** | Assumed | Algebraic consequences *given A2* |
| **A2 itself** | not at issue | **stipulated, not derived from A1** (open) |

### Paper-safe wording (conditional, narrowed)

> Conditional on the closure identification `L^{-1} = G_0` between the
> field operator and the propagator's Green's function on `Z^3`, the
> Poisson equation `L = H = -Delta_lat` (graph Laplacian) follows by
> class-A inversion. The closure identification itself is treated here as
> a stipulated physical-modelling hypothesis, not as a theorem derived
> from the Cl(3)-on-Z^3 axiom; the retained bridge theorem deriving the
> identification from the axiom remains open. The nearest-neighbor
> structure of `L` is an algebraic consequence of `L = H` given the
> stipulated identification, not an unconditional restriction on the
> operator class.

## Relation to Existing Notes

- **GRAVITY_POISSON_DERIVED_NOTE.md**: Proves Poisson uniqueness within the
  TI + SA + NN class via mismatch analysis. This note does **not** supersede
  that result; it records a different conditional statement (operator-class
  restrictions follow as consequences of the stipulated closure identity A2).
  The unrestricted-operator-class question remains open until a retained
  bridge theorem derives A2 from A1.

- **GRAVITY_SUB_BUNDLE_NOTE.md**: The sub-bundle note marks Tier 1a (Poisson
  from self-consistency) as BOUNDED. With this note's narrowed scope, Tier 1a
  remains BOUNDED — this note records only a conditional implication under
  a stipulated closure identification, not an unconditional axiom-first
  derivation. The retained bridge theorem deriving `L^{-1} = G_0` from the
  Cl(3)-on-Z^3 axiom is the open D-row gap and would be the deliverable
  required to upgrade Tier 1a beyond bounded.

- **frontier_gravity_poisson_derived.py**: The existing script tests Poisson
  against alternative operators within a restricted class. The script
  `frontier_gravity_full_self_consistency.py` verifies the conditional
  algebraic argument: *given the stipulated closure identification*, the
  inversion `L = G_0^{-1} = H` is exact. The runner does **not** verify
  the closure identification itself — it operates downstream of the
  stipulated identity.

## Commands Run

```bash
cd /Users/jonBridger/Toy\ Physics
python3 scripts/frontier_gravity_full_self_consistency.py
```

Exit code: 0. PASS=12, FAIL=0 (of 12 checks). The checks confirm the
class-A inversion `L = G_0^{-1} = H = -Delta_lat` *given* the stipulated
closure identification. They do **not** confirm the closure identification
itself, which remains the open D-row gap (a retained bridge theorem
deriving `L^{-1} = G_0` from the Cl(3)-on-Z^3 axiom).
