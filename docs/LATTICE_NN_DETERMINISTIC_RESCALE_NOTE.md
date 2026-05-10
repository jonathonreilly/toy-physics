# Lattice NN Deterministic Rescale Note

**Date:** 2026-04-03  
**Status:** bounded Born-clean refinement window through `h = 0.0625` (the
original bounded scope) PLUS continuum-operator-stable decoherence observables
(`MI`, `1-pur`, `d_TV`, `Born`) identified by the geodesic-continuum bridge
(see
`NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md` /
`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md` /
`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`); audit-repair
packet added 2026-05-06; continuum-bridge identification addendum 2026-05-10.
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is pipeline-derived after independent review.

This note freezes the deterministic-rescale follow-up to the raw nearest-neighbor
lattice continuum harness.

The question is deliberately narrow:

- can a fixed, geometry-only rescale schedule push the NN lattice below
  `h = 0.25` while keeping the Born check clean enough to matter?

Artifacts:

- primary runner:
  [`scripts/lattice_nn_deterministic_rescale.py`](../scripts/lattice_nn_deterministic_rescale.py)
- SHA-pinned runner cache:
  [`logs/runner-cache/lattice_nn_deterministic_rescale.txt`](../logs/runner-cache/lattice_nn_deterministic_rescale.txt)
- cache command:
  `python3 scripts/cached_runner_output.py scripts/lattice_nn_deterministic_rescale.py`
- upstream raw NN refinement:
  [`scripts/lattice_nn_continuum.py`](../scripts/lattice_nn_continuum.py)

## Audit Closure Packet

The re-audit packet is closed by the repo-local runner/cache pair above, not by
the older machine-local absolute-path log. The cache header pins the stdout to
runner SHA-256
`b958225c40bc8b6c917c0c1f530d87b17a6ad10b0ad257ecfd218e6f4361adda` and records:

- `timeout_sec: 120`
- `exit_code: 0`
- `status: ok`
- `elapsed_sec: 6.63`

The load-bearing schedule is explicit in the runner:

- `generate_nn_lattice(spacing)` builds the raw forward NN lattice with
  straight, up, and down edges only.
- `propagate(...)` sets `step_scale = spacing / math.sqrt(FANOUT)` with
  `FANOUT = 3.0`.
- The scale factor is applied inside the edge propagation update and depends
  only on `spacing` and the fixed fanout.
- The blocked slit sets select the geometry for each propagation run; they do
  not change the scale factor.
- `main()` evaluates exactly `h = 1.0, 0.5, 0.25, 0.125, 0.0625` and prints
  the rows reproduced below.

## Schedule

The schedule is fixed and deterministic:

- raw NN geometry
- 3 forward edges per node
- per-step rescale factor `spacing / sqrt(3)`
- the factor is geometry-only and is applied identically across all propagation
  runs
- no layer normalization and no amplitude-dependent rescaling

## Canonical Rows

These are the rows in the SHA-pinned cache
`logs/runner-cache/lattice_nn_deterministic_rescale.txt`.

| `h` | nodes | `MI` | `1-pur_cl` | `d_TV` | gravity | `k=0` | Born `|I3|/P` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 1,681 | `0.5022` | `0.4229` | `0.7455` | `-0.116678` | `+0.00e+00` | `4.74e-16` |
| 0.5 | 6,561 | `0.7420` | `0.4844` | `0.9072` | `+0.138226` | `+0.00e+00` | `5.09e-16` |
| 0.25 | 25,921 | `0.9470` | `0.4989` | `0.9878` | `+0.077415` | `+0.00e+00` | `6.04e-16` |
| 0.125 | 103,041 | `0.9972` | `0.5000` | `0.9996` | `+0.034466` | `+0.00e+00` | `7.86e-16` |
| 0.0625 | 410,881 | `1.0000` | `0.5000` | `1.0000` | `+0.014810` | `+0.00e+00` | `3.00e-16` |

## Interpretation

The deterministic schedule does what the raw NN branch suggested might be
possible:

- it extends the lattice cleanly below `h = 0.25`
- Born stays at machine precision at every tested spacing
- `k=0` stays exactly zero
- MI rises smoothly toward `1.0` bit
- decoherence rises smoothly toward `50%`
- `d_TV` rises smoothly toward `1.0`
- gravity is positive on the sub-`0.25` extension rows, but it shrinks toward
  zero as the lattice is refined

The key distinction from the earlier periodic-rescale attempt is that this
schedule is fixed by geometry, not by amplitude or by the specific blocked-set
configuration of a given propagation run.

## Safe Conclusion

The review-safe result is:

- **Born-safe deterministic extension works through `h = 0.0625`**
- the observables converge smoothly under the fixed schedule
- the remaining open question is not Born safety, but how to interpret the
  vanishing gravity scale in the finer-spacing limit; on the decoherence
  observables, the smooth limit has now been identified with a continuum-stable
  geodesic operator (see the 2026-05-10 addendum below)

Do **not** overstate this as a finished continuum theory. The canonical claim is
the narrower one above: a deterministic, Born-clean refinement path exists on
the raw NN lattice through the tested sub-`0.25` regime, with continuum-stable
decoherence observables on that path.

## 2026-05-10 Continuum-Bridge Identification (Scope Extension)

This addendum lifts the load-bearing decoherence-observable claims (`MI`,
`1-pur`, `d_TV`, `Born`) on the bounded deterministic-rescale window from
"fixed-`h` finite values" to "continuum-operator-stable values" by citing the
upstream continuum-bridge identification produced on this same rescaled NN
harness. The bounded harness scope (`BETA = 0.8`, `K_PHYS = 5.0`, slits at
`±3`, `L = 40`) is unchanged; this is a **scope extension, not a tier
upgrade**.

Upstream load-bearing dependencies (each a single open PR against `main`):

- [`NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md)
  (PR #957) — `T_∞` exists on the 15-dim observable subspace of this rescaled
  NN harness; Cauchy convergence at `r ≥ 1.51`; tail-bound `7.7e-3` at
  `h = 0.03125`.
- [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md)
  (PR #968) — `T_∞` identified as the geodesic operator on the slit-detector
  decoherence subblock; `σ_arm(h) = C_arm · h^0.526`, `R² = 0.9996`; the
  Gaussian-arm prediction matches `MI` / `d_TV` to `5e-4`.
- [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
  (PR #1003) — closed-form analytic derivation of `C_arm = 2.4855` with `8.3%`
  residual against the numerical `C_arm = 2.7107`.

Consequences for this note:

- the `MI`, `1-pur`, `d_TV`, `Born` columns of the canonical rows are no longer
  load-bearing only as "bounded fixed-`h` finite values" — they are now
  load-bearing as continuum-operator-stable values matching the geodesic
  identification within `7.7e-3` at `h = 0.03125` (PR #957) and within `5e-4`
  on the Gaussian-arm prediction (PR #968).
- the gravity centroid at fixed strength remains bounded on this note; the
  bound is now identified as **structural** (the geodesic limit gives 0, and
  the strength-saturation observation in PR #945 explains why simple
  strength-rescaling cannot lift it). This identification does **not** widen
  the gravity claim — it only labels its known bound, which is exactly the
  "vanishing gravity scale in the finer-spacing limit" open point already
  noted above.
- `claim_type` stays `bounded_theorem`; the rows are still bounded by the
  fixed harness parameters above (`BETA = 0.8`, `K_PHYS = 5.0`, slits at
  `±3`, `L = 40`). The audit ledger is untouched here — that revision is the
  reviewer's call.
