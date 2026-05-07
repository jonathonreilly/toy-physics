# N_F Bounded Z2 Reduction Theorem

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Primary runner:** [`scripts/cl3_n_f_derivation_2026_05_07_w2_check.py`](../scripts/cl3_n_f_derivation_2026_05_07_w2_check.py)

## Claim

The `N_F` normalization choice in the `g_bare` chain is not derived all the
way to `N_F = 1/2` by `Cl(3)` / `Z^3` alone. The source calculation does,
however, narrow the practical normalization ambiguity from an arbitrary
positive scalar to two framework-natural trace surfaces:

```text
N_F in {1/2, 1}.
```

The two values are:

| Trace surface | Definition | Value |
|---|---|---:|
| color carrier | `Tr_{V_3}(T_a T_b)` | `1/2` |
| full framework Hilbert space | `Tr_V(T_a^V T_b^V)` | `1` |

Their ratio is exactly the weak/taste fiber multiplicity:

```text
Tr_V / Tr_{V_3} = dim(C^2) = 2.
```

So the current framework can say: once the `su(3)` carrier and full
`V = C^8` embedding are imported, the normalization admission is a binary
trace-surface choice. It cannot yet say that the color-carrier trace is
uniquely forced by the primitives.

## Dependencies

- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  for the Hilbert-Schmidt/Killing-form up-to-scale rigidity surface.
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  for the parent convention-layer framing.
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  for the `Cl(3) -> End(V) -> su(3)` carrier surface.
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  for the `V_3` color-carrier embedding.
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
  for the `C^2` per-site fiber dimension.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews the claim and dependency
chain.

## Boundaries

This note does not claim:

- a unique derivation of `N_F = 1/2`;
- a zero-input derivation of `g_bare = 1`;
- a parent status update for `G_BARE_DERIVATION_NOTE.md`.

The remaining open step is the binary choice between tracing on the irreducible
color carrier `V_3` and tracing on the full framework Hilbert space `V`.

## Verification

Run:

```bash
python3 scripts/cl3_n_f_derivation_2026_05_07_w2_check.py
```

Expected:

```text
TOTAL   : PASS = 22, FAIL = 0
```
