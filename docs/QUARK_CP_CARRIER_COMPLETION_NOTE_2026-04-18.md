# Quark CP-Carrier Completion on the Live Mass-Ratio Lane

**Date:** 2026-04-18
**Status:** bounded one-primitive full-closure extension
**Primary runner:** `scripts/frontier_quark_cp_carrier_completion.py`

This note is now complemented by a stronger reduced closure:
[QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md](./QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md).
That newer note shows the full quark package can already be closed on a fixed
projector ray with only two real sector amplitudes plus one shared phase.
The present note remains the broader existence proof with freer complex
sector-specific carriers.

## Safe statement

The minimal Schur-NNI quark full-solve note remains valid:

- the minimal surface closes the quark magnitudes well;
- the same surface does **not** close the CKM CP area;
- phase-only relaxation on that surface does not repair `J`.

This note adds the next bounded step:

- keep the live down-type anchor and the historical `c12/c23` surface;
- keep the quark mass ratios `m_u/m_c`, `m_c/m_t` on their observation comparators;
- add one independent complex `1-3` carrier in each sector,
  `xi_u`, `xi_d`, on top of the Schur-generated `1-3` term;
- require the full atlas target surface
  `(|V_us|, |V_cb|, |V_ub|, J)`.

On that bounded extended surface there is a numerical full quark closure:

- `m_u/m_c = 1.688494 x 10^-3`
- `m_c/m_t = 7.400356 x 10^-3`
- `|V_us| = 0.227270122`
- `|V_cb| = 0.042179824`
- `|V_ub| = 0.003917067`
- `J = 3.313653 x 10^-5`

all within about `1%` or better of the chosen comparator/atlas targets, while
`arg det(M_u M_d) = 0 mod 2pi` stays closed numerically.

So the live quark work can now be stated more sharply:

- no self-contained full closure on the minimal Schur-NNI carrier;
- bounded full closure **does** exist once one adds an explicit complex
  determinant-neutral `1-3` carrier in each sector;
- this is still bounded support, not a retained theorem, because `xi_u`,
  `xi_d` are solved rather than derived.

## Carrier form

The completed `1-3` coefficients are taken to be

```text
c13_u(total) = c12_u c23_u sqrt(m_u/m_t) + xi_u
c13_d(total) = c12_d c23_d sqrt(m_d/m_b) + xi_d
```

with `xi_u`, `xi_d` complex and sector-specific.

The solved completion on this branch is:

```text
xi_u = +0.340735 - 0.063203 i
xi_d = +0.078186 + 0.108371 i
```

The corresponding Schur-base terms are:

```text
c13_u(base) = 3.400566 x 10^-3
c13_d(base) = 2.011511 x 10^-2
```

so the completion is numerically strong, not perturbative:

- `|xi_u| / c13_u(base) ~ 101.9`
- `|xi_d| / c13_d(base) ~ 6.64`

That is the key caveat. This is a real bounded completion surface, but not yet
the small retained correction one would ideally want.

## What closes

1. **Full quark package on a bounded extended surface.**
   The quark mass ratios and full atlas CKM package can be matched at once.
2. **Determinant-neutral completion.**
   The solve keeps `arg det(M_u M_d) = 0 mod 2pi`, so this is a weak-sector
   CP completion, not a strong-CP reopening.
3. **Sharper primitive target.**
   The missing ingredient is no longer a generic “more phase.” It is an
   independent complex `1-3` carrier.

## What does not close

1. **Retained derivation of `xi_u`, `xi_d`.**
   These remain numerical bounded carrier coefficients.
2. **Perturbative-small correction.**
   The completion dominates the bare Schur `1-3` term, especially in the
   up sector.
3. **Minimal-surface theorem upgrade.**
   The old minimal Schur-NNI note remains a CP no-go on its own carrier.

## Cross-checks on this branch

Two independent bounded scans reinforce the same endpoint:

- [scripts/frontier_quark_jarlskog_closure_scan.py](../scripts/frontier_quark_jarlskog_closure_scan.py)
  finds local `c13`-enhanced families that reach `J ~ J_atlas` inside the
  current CKM corridor, while phase-only motion fails.
- [scripts/frontier_quark_cp_primitive_projector_scan.py](../scripts/frontier_quark_cp_primitive_projector_scan.py)
  finds that wide projector-like `1+5` deformations can supply the missing
  area, while the literal `1/42` tensor lower-row dressing stays far too weak.

So the branch now has three aligned statements:

- minimal surface: strong quark magnitudes, CP no-go;
- bounded scan surface: `c13`/projector deformations can lift `J`;
- bounded completion surface: an explicit complex `1-3` carrier closes the
  full quark package numerically.

## Validation

Run:

```bash
python3 scripts/frontier_quark_cp_carrier_completion.py
python3 scripts/frontier_quark_jarlskog_closure_scan.py
python3 scripts/frontier_quark_cp_primitive_projector_scan.py
```

Current expected results on this branch:

- `frontier_quark_cp_carrier_completion.py`: `PASS=11 FAIL=0`
- `frontier_quark_jarlskog_closure_scan.py`: `PASS=5 FAIL=0`
- `frontier_quark_cp_primitive_projector_scan.py`: summary scan with strongest
  candidate `J/J_atlas = 1.075`
