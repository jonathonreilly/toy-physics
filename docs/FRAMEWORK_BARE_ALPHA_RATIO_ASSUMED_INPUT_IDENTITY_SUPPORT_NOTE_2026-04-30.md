# Framework Bare Alpha Ratio Assumed-Input Identity Support Note

**Primary runner:** scripts/frontier_framework_bare_alpha_3_alpha_em_dimension_fixed_ratio.py

**Date:** 2026-04-30
**Status:** support. Salvage note for algebraic identities preserved after
the dimension-fixed bare-coupling wrapper failed audit.

---

## 0. Provenance

The source wrapper
[`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](../archive_unlanded/framework-bare-alpha-assumed-input-salvage-2026-04-30/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
is archived under recovery tag
`archive_unlanded/framework-bare-alpha-assumed-input-salvage-2026-04-30/`.
The audit rejected the wrapper as an authority-boundary over-claim: the
verifier itself treats the coupling inputs as assumed support-side inputs,
not as a closed minimal-input derivation.

## 1. Surviving observations

The following identities survive as assumed-input algebra:

- if `g_3^2 = 1`, `g_2^2 = 1/(d + 1)`, and `g_Y^2 = 1/(d + 2)`, then
  `1/g_em^2 = 2d + 3`;
- under the same assumptions, `g_em^2 = 1/(2d + 3)`;
- for `d = 3`, the assumed-input ratio gives
  `alpha_3(bare) / alpha_em(bare) = 9`;
- the same substitution gives the support-side bookkeeping identity
  `sin^2(theta_W)(bare) = (d + 1)/(2d + 3)`, hence `4/9` at `d = 3`.

## 2. Boundary

This note does not derive the coupling inputs or promote the framework
bare-coupling packet. It only preserves the algebraic consequences that
follow after those support-side inputs are assumed.
