# Derivation: Cl(3) Conditional Minimality — Support for `d_s = 3`

## Date

2026-04-17 (narrowed 2026-04-17 after first review)

## Status

PROPOSED — conditional compatibility / minimality **support** note.

**This note does not close the axiom-depth question** for `d_s = 3`. It
supplies a conditional minimality statement that holds *given* three
retained framework requirements that are already on `main`.

Review correctness history:
- v1 overclaimed "absorb `d_s = 3` into the axiom" / "close the remaining
  half" / structural four-generation exclusion. Reviewer correctly flagged
  those as too strong.
- v2 (this version): narrowed to conditional minimality support, runner
  strengthened to explicitly construct `Cl(3;C) = M_2(C) (+) M_2(C)`,
  terminology corrected (`so(n)` / `spin(n)`, not `su(n)`), four-generation
  claim demoted to bounded tension.

## Scope And Claim Boundary

### What this note claims

> Given the retained native SU(2) bivector requirement, the retained
> cubic three-generation 8-state orbit algebra (`8 = 1 + 1 + 3 + 3`), and
> the retained anomaly-forced chirality parity requirement
> (`d_s + d_t` even with `d_t = 1`), the unique compatible Clifford
> dimension is `n = d_s = 3`.

This is a **conditional minimality support theorem**. It demonstrates
that the retained framework's three structural requirements are jointly
compatible at `n = 3` only.

### What this note does NOT claim

- **Does NOT** constitute a first-principles derivation of `d_s = 3`
  from framework-internal structure alone.
- **Does NOT** absorb `d_s = 3` into the axiom.
- **Does NOT** derive `d_s = 3` independently of the retained cubic
  orbit surface. The `2^n = 8` requirement itself conditions on the
  retained `8 = 1 + 1 + 3 + 3` structure, which is proven on a cubic
  `Z^3` surface. The note therefore does not escape the axiom's own
  premise — it verifies internal consistency.
- **Does NOT** structurally exclude four-generation matter. Higher-
  dimensional `Cl(n)` with `n >= 5` can carry four generations plus
  additional sectors; a structural four-generation exclusion theorem
  would require separate work.
- **Does NOT** derive the `Z^n` cubic lattice geometry; the cubic
  selector is a separate question.

### What this note is good for

- internal-consistency diagnostic for the retained framework
- companion / support tool for reviewers asking "why `Cl(3)` and not
  `Cl(1)` or `Cl(5)`?" — the answer is "because the retained cubic
  surface plus retained native SU(2) plus retained anomaly-forced
  parity pick out `n = 3` uniquely among small `n`"
- atlas-level support tool if the minimality diagnostic has reuse
  downstream

## Axioms Used

**A1.** `Cl(3)` on `Z^3` is the physical theory.

### Retained theorems reused

- **Native SU(2) closure**: three independent bivectors in `Cl(d_s)`
  close into the weak algebra on `Z^{d_s}`. Authority:
  `docs/NATIVE_GAUGE_CLOSURE_NOTE.md`.
- **Anomaly-forced `3+1` closure**: chirality requires `d_s + d_t` even
  and the single-clock codimension-1 theorem forces `d_t = 1`. Authority:
  `docs/ANOMALY_FORCES_TIME_THEOREM.md`.
- **Three-generation orbit algebra** `8 = 1 + 1 + 3 + 3` on the retained
  cubic surface. Authority:
  `docs/THREE_GENERATION_STRUCTURE_NOTE.md`.

The note derives no new retained axioms. It is a consistency check
across the three retained theorems.

## The Three Framework Requirements

### R1 — Native SU(2) needs at least three bivectors

The retained native `SU(2)` closure uses three linearly independent
bivectors `{e_1 e_2, e_2 e_3, e_3 e_1}` closing under commutator into
`su(2)`. The number of bivectors in `Cl(n)` is `C(n, 2) = n(n-1)/2`.
These bivectors generate the Lie algebra `spin(n)` (equivalently
`so(n)`), not `su(n)`. For three SU(2) generators we need

```
n(n-1)/2 ≥ 3,  i.e.,  n ≥ 3.
```

At `n = 3` we have exactly 3 bivectors and no selector is needed — all
bivectors are weak generators. At `n ≥ 4` the `spin(n)` algebra of
dimension `n(n-1)/2` contains more generators than `su(2)`, and some
rule is needed to pick out three "weak" generators; that rule is
external to the retained native SU(2) closure.

### R2 — Dimensional match for the retained 8-state orbit

The retained three-generation structure decomposes the `hw=1` orbit on
the cubic `Z^3` surface as

```
8 = 1 + 1 + 3 + 3
```

**Note carefully**: this 8-state decomposition is proven on the cubic
`Z^3` surface itself, so requiring `dim(Cl(n)) = 2^n = 8` conditions on
`n = 3`-specific retained input. This is the conditional step that
prevents the note from closing axiom-depth.

Under this conditional requirement, `2^n = 8` forces `n = 3` exactly.

### R3 — Odd parity from anomaly-forced chirality

The anomaly-forced `3+1` theorem requires even total Clifford dimension
to support chirality: `d_s + d_t ≡ 0 (mod 2)`. Combined with `d_t = 1`,
this forces `d_s` odd.

## Intersection Table

| Requirement | `n=0` | `n=1` | `n=2` | `n=3` | `n=4` | `n=5` | `n=6` | `n=7` |
|---|---|---|---|---|---|---|---|---|
| R1 (≥ 3 bivectors) | · | · | · | ✓ | ✓ | ✓ | ✓ | ✓ |
| R2 (`2^n = 8`) | · | · | · | ✓ | · | · | · | · |
| R3 (odd) | · | ✓ | · | ✓ | · | ✓ | · | ✓ |
| **All three** | · | · | · | **✓** | · | · | · | · |

The unique `n` satisfying R1 ∧ R2 ∧ R3 is `n = 3`.

R2 alone forces `n = 3` exactly. R1 and R3 are consistency checks that
`n = 3` simultaneously satisfies all three retained requirements — no
other `n` does.

## Explicit `Cl(3;C) = M_2(C) ⊕ M_2(C)` Construction

The runner builds the 4-dimensional reducible representation

```
e_i = diag(σ_i, -σ_i)     for i = 1, 2, 3
```

which satisfies `{e_i, e_j} = 2 δ_{ij} I_4` and produces a pseudoscalar

```
ω = e_1 e_2 e_3 = diag(iI_2, -iI_2),  ω^2 = -I_4.
```

The chirality projectors

```
P_R = (I_4 - iω) / 2 = diag(I_2, 0),
P_L = (I_4 + iω) / 2 = diag(0, I_2)
```

satisfy `P_R^2 = P_R`, `P_L^2 = P_L`, `P_R P_L = 0`, `P_R + P_L = I_4`.
Restricting `{I, e_1, e_2, e_3}` to the R block gives
`{I_2, σ_x, σ_y, σ_z}` (rank 4, spans `M_2(C)` as a complex vector
space), and to the L block gives `{I_2, -σ_x, -σ_y, -σ_z}` (also rank
4). This is the explicit `M_2(C) ⊕ M_2(C)` structure the runner verifies.

The even subalgebra `Cl^+(3)`, spanned by `{1, e_1 e_2, e_2 e_3, e_3 e_1}`,
is block-diagonal with identical action on the R and L blocks —
`Cl^+(3)` is embedded diagonally in `M_2(C) ⊕ M_2(C)`. Restricted to a
single block it has complex rank 4, i.e. it spans a full `M_2(C)` factor,
consistent with `Cl^+(3) ≅ M_2(C)`.

## Small-`n` Fails and Large-`n` Richness

### Cl(1) and Cl(2) fail R1 explicitly

- `Cl(1)`: zero bivectors — SU(2) cannot be built at all
- `Cl(2)`: one bivector — its self-commutator is zero, so no non-abelian
  Lie algebra emerges

### Cl(5), Cl(7), ... are "over-rich"

At `n = 5`, `Cl(5)` has `C(5,2) = 10` bivectors, generating `spin(5)`
(of dimension 10). Embedding SU(2) into `spin(5)` requires a selector
to pick three of the ten generators as weak. The retained native SU(2)
theorem does not supply such a selector; going to `n = 5` therefore adds
axiom content.

Analogously at `n = 7, 9, 11`, the bivector algebras are `spin(n)` of
dimension `n(n-1)/2`.

## Runner

**Target:** `scripts/frontier_cl3_minimality.py`.

**Structure:**

- Part A — requirement-table intersection, `n` sweep to `[0, 20]`
- Part B — explicit `Cl(3;C) = M_2(C) ⊕ M_2(C)` via the 4-dim rep,
  pseudoscalar, chirality projectors, even subalgebra diagonal embedding,
  Pauli-block M_2(C) rank verification, bivector commutator closure
- Part C — explicit SU(2)-closure failure for Cl(1) and Cl(2)
- Part D — bivector counts for `n ∈ {5, 7, 9, 11}` and their
  `spin(n)` / `so(n)` interpretation
- Part E — Bott periodicity cross-check for `Cl(n;C)` dimension and
  `A ⊕ A` structure
- Part F — **bounded tension** against a clean four-generation fit on
  the retained cubic surface, with explicit disclaimer that higher-dim
  `Cl(n)` embeddings are not excluded

### Runner results

**13 THEOREM + 33 SUPPORT, 0 FAIL.**

- The intersection of R1 ∧ R2 ∧ R3 across `n ∈ [0, 20]` is uniquely `n = 3`.
- The 4-dim reducible rep explicitly realizes `Cl(3;C) = M_2(C) ⊕ M_2(C)`
  with chirality projectors verified by the algebra `P_R^2 = P_R`,
  `P_R + P_L = I_4`, etc.
- Each chirality block carries a full `M_2(C)` with rank-4 Pauli basis.
- Cl^+(3) is diagonally embedded with complex rank 4 on each block —
  the Cl^+(3) ≅ M_2(C) isomorphism is explicit at the matrix level.
- Bivectors close under commutator with structure constants
  `f_{ijk} = -2 ε_{ijk}` reproducing `su(2)` exactly (residuals < 1e-14).

## Bounded Tension With Four Generations

Four-generation matter with orbit size 10, 12, or 14 would require a
Clifford dimension that is not a power of 2, which is incompatible with
`Cl(n)` over the retained cubic surface. The nearest power of 2 is
`2^4 = 16`, which would require `n = 4` (even), violating R3.

**This is bounded support / tension, NOT a structural exclusion
theorem.** Higher-dimensional `Cl(n)` embeddings with `n ≥ 5` can carry
four generations plus additional sectors, and nothing in this note
rules them out. A true four-generation exclusion theorem would require
a separate derivation.

## Weakest Link — Why This Is Not Axiom-Depth Closure

**R2 (`2^n = 8`) is not framework-internal in the strong sense.** The
`8 = 1 + 1 + 3 + 3` orbit decomposition is a theorem on the cubic `Z^3`
surface, which is precisely the surface the axiom specifies. Using that
decomposition to "force" `n = 3` is therefore a consistency check, not
an independent derivation.

Genuinely closing axiom-depth for `d_s = 3` would require either:

- (a) an independent non-cubic derivation of the 8-state requirement,
  from a retained principle that does not presuppose `d_s = 3`, or
- (b) an independent retained theorem selecting `n = 3` without
  importing the cubic orbit algebra.

This note provides neither. The contribution is strictly a retained-
theorem consistency diagnostic.

## What A Reviewer Should Conclude

- The math replays: 13 THEOREM + 33 SUPPORT, 0 FAIL.
- The claim is retained-framework-compatibility, not axiom-depth closure.
- The runner now actually builds `Cl(3;C) = M_2(C) ⊕ M_2(C)` explicitly
  (Part B), so the note's explicit-construction claim is supported by
  the runner output.
- Terminology fixed: bivectors generate `spin(n) / so(n)`, not `su(n)`.
- Four-generation language demoted to bounded tension.
- If useful, this can be packaged as a retained-framework consistency
  companion / support tool. It is **not** a retained flagship closure.

## Next

This note does not pursue Path 2 (genuine axiom-depth closure) — that
requires new science. If that program is later undertaken, candidates
include:

- a retained non-cubic orbit theorem that derives the 8-state structure
  independently
- a retained theorem selecting `Cl(n)` for `n = 3` via some intrinsic
  property (e.g. the specific combination of `spin(n) ⊃ su(2)` +
  anomaly parity + minimal triality structure), without importing the
  cubic surface

Until such work lands, the axiom-depth gap for `d_s = 3` remains open.
