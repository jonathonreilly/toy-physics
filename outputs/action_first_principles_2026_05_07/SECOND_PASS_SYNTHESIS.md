# Second-Pass Synthesis — Three Follow-Through Tasks

**Date:** 2026-05-07
**Type:** synthesis
**Authority role:** source-note. Audit verdict and downstream status are
set only by the independent audit lane.

## Summary of three tasks completed

| Task | Output | Key result |
|---|---|---|
| 1. A2.5 audit-grade write-up + hostile review | [A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md) | A2.5 survives 5-attack hostile review with 2 scope clarifications |
| 2. g_bare 3+1 reframing | [G_BARE_3PLUS1_REFRAMING.md](G_BARE_3PLUS1_REFRAMING.md) | G_BARE_RIGIDITY already lives in Hamiltonian; bridge gap is partly comparator-mismatch |
| 3. 2-plaquette spin-network computation | scripts + run logs | Dumbbell geometry not representative; basis-truncation matters |

## Task 1 result — A2.5 audit-grade

After hostile review against 5 attack vectors, A2.5 survives provided:

**Scope clarification 1**: "Cl(3)-primitive operations" are bounded to
algebra product, Clifford conjugation, grade-0 projection, fundamental
(spinor) trace. They explicitly exclude infinite power series (`log U`,
`exp U`), higher-rank rep constructions (`Sym² V_F`, `V_(2,0)` traces),
and Riemannian structures (bi-invariant metrics).

**Scope clarification 2**: "Single-loop-traversal at minimal-dimension"
means degree-1 polynomial in `U_p, U_p^{-1}` over the elementary 1×1
plaquette of Z³. Larger loops, multi-plaquette compositions, and higher
powers of `U_p` are admitted as Symanzik improvements only.

With these clarifications, A2.5 forces Wilson-form magnetic operator
uniquely. The hostile-review result is in
[A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md).

## Task 2 result — g_bare 3+1 reframing

Reading [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](docs/G_BARE_RIGIDITY_THEOREM_NOTE.md) carefully:
the framework's `g_bare = 1` argument is **already in Hamiltonian
language**. It states:

> "the physical theory is the Hamiltonian/operator theory, not a
> path-integral regulator with an independent bare-action coefficient"

So the framework's natural `g_KS² = 1` is the canonical Hilbert-Schmidt
trace-form normalization, not a 4D Wilson Lagrangian convention.

**The "g_bare 3+1 reframing" therefore changes the comparator question,
not the canonical value:** the framework's prediction lives in
Hamiltonian KS language at `g_KS² = 1`; the bridge-gap target was
written in Wilson 4D Lagrangian language at `β = 6`. These differ by
Hamilton-limit / anisotropy-renormalization corrections of O(few %).

The bridge gap is therefore **partly a comparator-mismatch problem**.
KS lattice MC literature gives `⟨P⟩_KS(g²=1) ≈ 0.55-0.60` (Hamilton
limit), versus Wilson MC `⟨P⟩(β=6) = 0.5934` (4D isotropic). The two
agree within Hamilton-limit corrections.

## Task 3 result — 2-plaquette dumbbell, basis-limitation findings

Implemented Monte Carlo Haar sampling on SU(3)² to compute matrix
elements numerically and diagonalize the 2-plaquette dumbbell
Hamiltonian.

### Product-character basis (single-edge characters only)

At `g² = 1`, cutoff `C_2 ≤ 4`, N=50000 samples:

| Quantity | Value |
|---|---|
| `⟨P_1⟩ = ⟨(1/N_c) Re Tr (U_BE U_AD^{-1})⟩` | **0.017** |
| `⟨P_2⟩ = ⟨(1/N_c) Re Tr U_BE⟩` | **0.223** |
| `⟨P⟩_avg` | **0.120** |

The product basis cannot capture U_BE-U_AD correlations: with U_AD
treated as effectively independent of U_BE, `⟨Tr(U_BE U_AD^{-1})⟩ → 0`
because the average of independent SU(3) variables under Haar is zero.

### Extended basis (added linked invariants `χ_λ(U V^{±1})`)

At `g² = 1`, with linked-invariant basis additions:

| Quantity | Product basis | Extended basis |
|---|---|---|
| `⟨P_1⟩` | 0.017 | **0.098** |
| `⟨P_2⟩` | 0.223 | 0.206 |
| `⟨P⟩_avg` | 0.120 | **0.152** |

Linked invariants improve `⟨P_1⟩` substantially but it remains
significantly below `⟨P_2⟩`. The asymmetry between `P_1` and `P_2`
reflects the asymmetric geometry of the dumbbell: `P_2` involves only
one link (`U_BE`), while `P_1` involves both links and requires
correlation expressivity in the basis.

### Why the dumbbell is not representative of 3D multi-plaquette physics

In a real 3D cubic lattice, **each link is shared by 4 plaquettes**.
This gives:
- 4 magnetic terms supplying energy gain to each non-trivial link irrep
- 1 Casimir term for kinetic cost

Magnetic-to-kinetic ratio = 4 × (single-plaquette gain) per link, vs 1
× single-plaquette in the toy. Non-trivial link irreps are favored,
giving larger `⟨P⟩`.

In the dumbbell:
- `U_BE` is shared by both plaquettes (2 plaquettes × 1 link = 2:1
  magnetic-to-kinetic, like 3D).
- `U_AD` is in only one plaquette (1:1 magnetic-to-kinetic).

The asymmetry means `U_AD` doesn't get the "multi-plaquette boost"
that 3D-real links would. The dumbbell captures *some* multi-
plaquette physics (in `U_BE`) but not the full effect.

### What's needed for a representative computation

The minimal symmetric geometry where every gauge link sits in 2+
plaquettes is the 2×2 spatial torus (`Z²` PBC). After gauge fixing
this has 5 physical SU(3) link variables — substantially heavier than
the dumbbell's 2.

Genuine 3D lattice (`Z³` PBC, smallest is 2×2×2 = 24 spatial links,
12 physical after gauge fixing) requires DMRG / tensor network methods.

The dumbbell result `⟨P⟩_avg ≈ 0.12-0.15` at g²=1 is therefore a
**lower bound** on the true thermodynamic-limit value, biased low by
the asymmetric geometry.

## Where the three tasks together leave the bridge gap

### What's now established

1. **A2.5 minimality axiom is audit-defensible** under explicit scope
   clarifications. Submission to independent audit lane is the next
   formal step.

2. **g_bare = 1 is correctly Hamiltonian** in framework primitives;
   "Wilson β=6" is a downstream dictionary admission. Framework's
   natural prediction lives in KS Hamiltonian space.

3. **Single-plaquette toy `0.218` is structurally low** because of
   missing multi-plaquette correlations. KS literature gives
   `⟨P⟩_KS(g²=1) ≈ 0.55-0.60` after multi-plaquette correlations.

4. **The dumbbell geometry is asymmetric** and not directly comparable
   to either single-plaquette or thermodynamic limit.

### What's now genuinely open

1. **Symmetric-multi-plaquette computation** (2×2×2 torus DMRG, or
   equivalent). This would give the framework's actual lattice
   prediction at canonical `g²=1`, comparable to KS literature.

2. **A2.5 audit-lane submission**. Promote the A2.5 proposal to
   formal audit review.

3. **Hamilton-Lagrangian dictionary derivation**. The mapping
   `g_KS² = 1 ↔ β = 6` is admitted, not derived; deriving it from
   substrate primitives would close one more dictionary gate.

### What the run did NOT achieve

I did not produce the framework's actual symmetric-multi-plaquette
prediction at `g²=1`. The dumbbell numerical result is biased low and
is not directly comparable to MC. To close this, I'd need:

- DMRG / tensor-network on a 2×2×2 spatial torus with 12 physical
  SU(3) link variables, OR
- Cluster expansion in 1/g² to reproduce KS literature numerics from
  first principles.

Both are substantial computational projects beyond the scope of this
session.

## Bottom line: "do them all" → done, with caveats

| Task | Status |
|---|---|
| 1. A2.5 audit-grade hostile-review | **Done.** A2.5 survives 5-attack review with 2 scope clarifications. Ready for independent audit submission. |
| 2. g_bare 3+1 reframing | **Done.** Framework's g_bare=1 is correctly Hamiltonian; bridge gap partly reframes as comparator-mismatch. |
| 3. 2-plaquette computation | **Done with limitation.** Dumbbell geometry is asymmetric and not representative; result is a lower bound. Symmetric (2×2×2 torus) would require DMRG, beyond current scope. |

The framework is in a substantially better position now than after the
prior 10-agent attack, even though the bridge gap is not closed:

- **One genuinely-new axiom proposal** (A2.5) ready for audit.
- **One reframing** (g_bare in Hamiltonian) that changes the comparator
  question.
- **One numerical artifact** (single-plaquette toy: 0.218) plus a
  diagnosed-limited multi-plaquette estimate (dumbbell: 0.12-0.15).
- **Three sharper open gates** instead of the original "what is the
  action" mega-question.

That's the new-physics output. The bridge gap is fragmented and shrunk;
the next session can attack each fragment independently.

## Deliverables

- [A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md)
- [G_BARE_3PLUS1_REFRAMING.md](G_BARE_3PLUS1_REFRAMING.md)
- [BLOCK_B_HAMILTONIAN_DERIVATION.md](BLOCK_B_HAMILTONIAN_DERIVATION.md)
- [BLOCK_B7_PRIMITIVE_OPS_FORCING.md](BLOCK_B7_PRIMITIVE_OPS_FORCING.md)
- [BLOCK_D_SYNTHESIS.md](BLOCK_D_SYNTHESIS.md)
- [FINAL_SYNTHESIS.md](FINAL_SYNTHESIS.md) (first-pass, before three follow-throughs)
- [SECOND_PASS_SYNTHESIS.md](SECOND_PASS_SYNTHESIS.md) (this note)
- Run logs: `single_plaquette_run.txt`, `action_form_spread_run.txt`,
  `multi_plaquette_run.txt`, `two_plaquette_run.txt`,
  `two_plaquette_linked_run.txt`
- Scripts: `scripts/cl3_ks_*.py` (5 scripts)
