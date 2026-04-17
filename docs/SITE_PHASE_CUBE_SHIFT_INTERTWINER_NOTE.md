# Site-Phase / Cube-Shift Intertwiner Theorem

**Status:** AIRTIGHT — composition of the cube-shift joint-eigenstructure
theorem, translation-eigenvalue theorem, and Hamming-distance selection rule.
**Runner:** `scripts/frontier_site_phase_cube_shift_intertwiner.py` (60/60 PASS)
**Reusability:** this is the canonical bridge between C^8 taste-cube
arguments and C^{L³} lattice arguments.

## Theorem

Let Z_L³ (L even) be the periodic lattice with BZ corner states |X_α⟩
(α ∈ {0,1}³). Let S_μ be the cube-shift operators on C^8 and P_μ be
the site-phase operators on C^{L³}, defined
```
S_μ on C^8:   σ_x in tensor position μ, I elsewhere.
P_μ on C^{L³}:  (P_μ ψ)(x) = (−1)^{x_μ} ψ(x).
```
Let Φ: C^8 ↪ C^{L³} be the linear isometry mapping the computational
basis |α⟩ ↦ |X_α⟩ for α ∈ {0,1}³.

Then:

1. P_μ |X_α⟩ = |X_{α ⊕ e_μ}⟩.
2. On C^8: Φ^† P_μ Φ = S_μ (intertwining).
3. Joint-eigenstate spectral structure of S_μ on C^8 transfers exactly
   to P_μ on the BZ-corner subspace of C^{L³}: the joint P_μ eigenstate
   with eigenvalue triple (s_1, s_2, s_3) ∈ {±1}³ is
   ```
   |ψ_s^lattice⟩ = (1/√8) Σ_α (∏_μ s_μ^{α_μ}) |X_α⟩.
   ```

## Proof

1. (P_μ |X_α⟩)(x) = (−1)^{x_μ} · (1/√L³) (−1)^{α·x}
   = (1/√L³) (−1)^{(α ⊕ e_μ)·x}
   = |X_{α ⊕ e_μ}⟩(x).

2. From (1), P_μ on the BZ-corner basis acts as α → α ⊕ e_μ. From the
   cube-shift joint-eigenstructure theorem, S_μ on C^8 also acts as
   α → α ⊕ e_μ in the computational basis. Conjugating by Φ identifies
   the two.

3. Because P_μ and S_μ are intertwined by Φ (isometry), all spectral
   structure of S_μ on C^8 (from the joint-eigenstructure theorem)
   transfers to P_μ on the BZ-corner subspace of C^{L³}.

QED.

## Composition structure

This theorem composes three earlier results:
- **Cube-shift joint-eigenstructure** (on C^8): S_μ bit-flip action +
  joint eigenbasis.
- **Translation-eigenvalue on BZ corners** (on C^{L³}): |X_α⟩ explicit
  structure.
- **Hamming-distance selection rule** (on C^{L³}): Part 1 matrix
  element ⟨X_β|P_μ|X_α⟩ = δ_{α⊕β, e_μ}, which is the scalar form of
  the bit-flip action.

The intertwiner theorem packages these three into the canonical
C^8 ↔ C^{L³}_{BZ} isomorphism.

## Relation to main

The note `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` on main
restricts this intertwiner to the hw=1 subspace (generating a
3-dim Φ into the 3-dim hw=1 subspace). The present theorem is the
full 8-dim version.

## Reusability

This is the canonical bridge between:
- abstract taste-cube results stated on C^8 (V_sel selector
  derivation, S_3 axis symmetry, cube-shift algebra, projector
  structures)
- concrete lattice-level statements on C^{L³} (BZ corner transitions,
  gauge-mediated taste changing, hw-sector dynamics)

Any downstream derivation that bridges the two pictures can cite this
theorem to move freely between them.

## Scope

Pure math. No structural identifications. No imports.

## Verification

```bash
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py
# Expected: TOTAL: PASS=60, FAIL=0
```
