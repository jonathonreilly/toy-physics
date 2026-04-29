# Reduced Quark Closure on a Fixed Projector Ray

**Date:** 2026-04-18
**Status:** bounded reduced full-closure extension
**Primary runner:** `scripts/frontier_quark_projector_ray_phase_completion.py`

Sharper parameter audit:
`QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`.
That newer note shows the current projector/tensor surface already supports
the exact projector ray, an exact-support down amplitude `1/sqrt(42)`, and a
small support-angle probe `-1/42 rad`, leaving only one up-sector scalar
amplitude law non-derived.

## Safe statement

The live quark branch now has a stronger bounded closure than the earlier free
complex-carrier completion.

The minimal Schur-NNI surface still has the same honest verdict:

- strong quark-magnitude closure;
- no self-contained CKM CP closure;
- phase-only rescue fails.

The earlier bounded carrier-completion note then showed existence of full
closure once one adds two explicit complex sector-specific `1-3` carriers
`xi_u`, `xi_d`.

This note compresses that closure much further.

## Reduced ansatz

Use the exact CKM projector direction

```text
projector_ray = sqrt(1/6) + i sqrt(5/6)
```

and test two additive reduced carriers:

```text
phase-free:
  c13_u = c13_u(base) + a_u * projector_ray
  c13_d = c13_d(base) + a_d * projector_ray

shared-phase:
  c13_u = c13_u(base) + a_u * projector_ray * exp(i phi_shared)
  c13_d = c13_d(base) + a_d * projector_ray * exp(i phi_shared)
```

with only:

- `a_u`, `a_d` as real sector amplitudes,
- `phi_shared` as one common extra phase for the second ansatz,
- and the two up-sector mass ratios as nuisance variables.

## Numerical result

### Phase-free reduced projector carrier

Even the phase-free reduced carrier already lands very close:

- `m_u/m_c = 1.690666 x 10^-3`
- `m_c/m_t = 7.363099 x 10^-3`
- `|V_us| = 0.227271045`
- `|V_cb| = 0.042170230`
- `|V_ub| = 0.003931984`
- `J = 3.275493 x 10^-5`

So the exact projector ray with two amplitudes alone already gets within
about `1.7%` of the atlas `J`.

### Shared-phase reduced projector carrier

Adding one shared phase closes the full quark package numerically:

- `m_u/m_c = 1.699915 x 10^-3`
- `m_c/m_t = 7.365992 x 10^-3`
- `a_u = -0.814324`
- `a_d = -0.158080`
- `phi_shared = 177.721 deg`
- `|V_us| = 0.227270860`
- `|V_cb| = 0.042170694`
- `|V_ub| = 0.003911693`
- `J = 3.337768 x 10^-5`

while keeping

- `arg det(M_u M_d) = 0 mod 2pi`

numerically closed.

## Interpretation

This is the strongest current bounded closure statement on the quark branch.

Compared with the earlier free-carrier completion:

- the carrier is now compressed to one exact repo-native ray;
- only two real sector amplitudes and one shared phase remain;
- the full quark package still closes numerically.

So the current closure target is now much sharper:

- not arbitrary complex `1-3` carriers;
- not phase-only rescue on the minimal surface;
- but a fixed projector ray with minimal bounded dressing.

## What closes

1. **Reduced bounded closure.**
   Full quark closure survives after strong compression of the extra carrier.
2. **Projector-native carrier.**
   The added `1-3` term now sits on the exact `1⊕5` CKM projector direction.
3. **Determinant-neutral weak-sector CP completion.**
   The solve keeps `arg det(M_u M_d) = 0 mod 2pi`.

## What does not close

1. **Retained derivation of `a_u`, `a_d`, `phi_shared`.**
   These are still solved bounded parameters.
2. **Minimal-surface theorem upgrade.**
   The old minimal Schur-NNI carrier is still a CP no-go by itself.
3. **Exact proof that the shared phase is forced.**
   This note shows a sharp bounded closure, not a retained projector theorem.

## Relation to the earlier bounded completion

[QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md](./QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
remains valid as a general existence proof using sector-specific complex
carriers.

This note is stronger because it shows that the same closure can be compressed
to a much smaller ansatz that is visibly aligned with the exact CKM projector
surface already present in the repo.

## Validation

Run:

```bash
python3 scripts/frontier_quark_projector_ray_phase_completion.py
```

Current expected result on this branch:

- `frontier_quark_projector_ray_phase_completion.py`: `PASS=8 FAIL=0`
