# Quark Mass-Ratio Full Solve on the Minimal Schur-NNI Surface

**Date:** 2026-04-18
**Status:** bounded magnitude closure plus quantified CP-area ceiling
**Primary runner:** `scripts/frontier_quark_mass_ratio_full_solve.py`

## Safe statement

The current branch now carries a strongest-current quark full-solve attempt on
the minimal Schur-NNI surface:

- the down-type ratios remain fixed by the Phase 1 CKM-dual lane
- the promoted CKM atlas supplies `|V_us|`, `|V_cb|`, `|V_ub|`, and
  `delta_std`
- the historical minimal Schur-NNI coefficient surface supplies the bounded
  texture carrier
- the up-sector ratios `m_u/m_c` and `m_c/m_t` can then be inverted from the
  CKM magnitudes alone

On that surface the magnitude solve is strong:

- `m_u/m_c ~ 1.68 x 10^-3`
- `m_c/m_t ~ 7.32 x 10^-3`

both close to the usual observation comparators.

But the same surface does **not** close the full CP sector. Its intrinsic
Jarlskog area stays near `~5 x 10^-6`, and even after relaxing the up/down
`1-3` phases while keeping the CKM magnitudes close to the atlas values, the
best current ceiling stays near `~6 x 10^-6`, still far below the atlas
`J ~ 3.33 x 10^-5`.

So the honest current endpoint is:

- quark **magnitude** closure on the minimal Schur-NNI surface
- no full CKM CP closure on that same surface
- one extra CP-area primitive still missing

A separate bounded completion note now exists:
[QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md](./QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md).
That new note does **not** change the verdict here. It adds one explicit
complex `1-3` carrier per sector and closes the full quark package on a
bounded extended surface. The present note remains the honest statement about
the minimal Schur-NNI carrier by itself.

## Inputs consumed

- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
- [UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md](./UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md)
- historical bounded NNI support:
  [work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md](./work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md)

## What closes

1. **Magnitude inversion.** The current down-type anchor plus the atlas CKM
   magnitude package is already strong enough to numerically invert the
   up-sector ratios on the minimal Schur-NNI carrier.
2. **Comparator accuracy.** The solved `m_u/m_c` and `m_c/m_t` land near the
   usual quark-mass comparators without importing those ratios into the solve.
3. **Full-lane diagnosis.** The remaining failure is sharply localized:
   not the magnitudes, but the CP area.

## What does not close

1. **Intrinsic `J` on the minimal surface.** The current Schur-generated
   `1-3` structure still undershoots the atlas Jarlskog by a large factor.
2. **Phase-only rescue.** Allowing independent up/down `1-3` phases while
   keeping the CKM magnitudes near the atlas values does not repair the gap.
3. **Retained full quark theorem.** This remains bounded support, not a
   retained theorem-grade closure.

## Interpretation

This is not the same endpoint as the current charged-lepton lane.

The lepton lane on current `main` still depends on an explicit observational
pin for the hierarchy itself. Here, by contrast, the quark lane already has a
real magnitude solve on a bounded microscopic carrier. The blocker is narrower:
one missing CP-area primitive, not the entire hierarchy/magnitude structure.

## Validation

Run:

```bash
python3 scripts/frontier_quark_mass_ratio_full_solve.py
```

Current expected result on this branch:

- `frontier_quark_mass_ratio_full_solve.py`: `PASS=15 FAIL=0`
