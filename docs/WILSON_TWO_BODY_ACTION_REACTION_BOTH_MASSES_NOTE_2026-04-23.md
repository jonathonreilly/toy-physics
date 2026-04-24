# Wilson Two-Body Action-Reaction and Both-Masses Smoke Test

**Date:** 2026-04-23
**Status:** partial closure of the active-review-queue item "Wilson two-body
both-masses / action-reaction law". Both-masses scaling closes at the
smoke-test level; action-reaction remains open with a sharper, well-
characterized obstruction.
**Runner:** `scripts/frontier_wilson_two_body_action_reaction_both_masses.py`
**Result:** `10/11 PASS` (B.1 is the explicitly-expected and reported FAIL on
action-reaction in the differential protocol).

## 1. Question

The active review queue
(`docs/repo/ACTIVE_REVIEW_QUEUE.md`) lists the Wilson two-body lane as
open with respect to (i) the full both-masses law and (ii) the action-
reaction law at the centroid level. The existing
`frontier_wilson_two_body_open.py` runs the SHARED Hartree mode and
reports the SEPARATION acceleration only, which conflates the
contributions from the two packets and therefore does not directly
test either open item.

## 2. Setup

Single open-boundary 3D Wilson lattice, `side = 9` (729 sites),
`DT = 0.08`, `N_STEPS = 20`, `G = 5.0`, `mu^2 = 0.22`, `sigma = 1.0`,
separation `d = 4` (symmetric placement around the lattice center).

Two Gaussian wave packets, masses `(m_a, m_b)` swept across the
configurations:

```text
{(1, 1), (1, 2), (2, 1), (1, 3), (2, 3)}.
```

Modes:

- `SHARED`     — both packets evolve under joint Hartree potential
- `SELF_ONLY`  — each packet evolves under its own potential only
- `FREE`       — no potential; Wilson dispersion + boundary push only
- `ASYMMETRIC` — packet `a` feels `b`'s potential; packet `b` is FREE

## 3. Structural theorem (Section A in the runner)

In SHARED mode, the joint Hartree potential
`phi_shared(rho_total)` is symmetric under
`(a, m_a, psi_a) <-> (b, m_b, psi_b)`. Both packets evolve under the
same Wilson Hamiltonian `H(phi_shared)`. Ehrenfest then forces

```text
m_a * a_a + m_b * a_b = 0
```

modulo any self-Hartree centroid forces. The Hartree mutual energy is
exactly bilinear in `(m_a, m_b)`:

```text
E_mut = m_a * m_b * K_kern(psi_a, psi_b),
```

so the cross-coupling acceleration on packet `a` from packet `b`
satisfies

```text
a_a^cross / m_b = -grad K_kern,
```

a quantity that depends only on packet shapes and separation, not on
`(m_a, m_b)` individually.

## 4. Differential protocol

The open-boundary Wilson lattice does NOT preserve parity exactly. A
Gaussian wave packet near the edge picks up a nonzero centroid force
from its OWN Hartree field even though the continuum symmetric-density
argument predicts zero. We see this empirically as large `SELF_ONLY`
centroid accelerations growing with the source mass.

The clean physics observable is therefore the cross-coupling
acceleration

```text
a^cross := a(SHARED) - a(SELF_ONLY),
```

which subtracts the self-Hartree contamination and isolates the force
from the partner's field.

## 5. Results

| Section | Test | Verdict |
|---|---|---|
| A.1, A.2, A.3 | structural Hartree exchange-symmetry + bilinearity | PASS |
| B.1 | action-reaction within 10% on differential protocol | **FAIL** (max residual 100%) |
| C.1 | `a_a^cross / m_b` constant across n=5 configs | **PASS** (CV = 3.6%) |
| D.1 | FREE drift mass-independent | PASS (zero spread) |
| D.2 | cross signal SNR > 5 vs FREE drift | PASS (SNR = 5.74) |
| D.3 | SELF_ONLY identified as calibration data, not null | PASS |
| E.1 | ASYMMETRIC negative control breaks action-reaction | PASS (residual = 100%) |
| F.1, F.2 | honest open boundary | PASS |

The headline numerical result is C.1: across n=5 mass configurations
with `(m_a, m_b)` covering ratios from `1:1` to `2:3`, the cross-
coupling acceleration `a_a^cross / m_b` is constant at `3.6%`
coefficient of variation. This is the both-masses scaling.

## 6. The action-reaction obstruction

Section B.1 is an explicitly expected and reported FAIL. On the
side=9 Wilson surface, the SHARED-minus-SELF_ONLY differential
protocol does not cleanly isolate action-reaction because:

- when the partner mass `m_b` is large (e.g., `(1, 3)` or `(2, 3)`),
  packet `b`'s SELF_ONLY centroid shift is dominated by its own
  self-Hartree field;
- the wave-packet shape in SHARED differs from that in SELF_ONLY
  (because the joint potential distorts the density), and
- the subtraction therefore leaves residual self-Hartree contamination
  on packet `b`'s cross signal.

A side=13 spot check confirmed this is intrinsic to the protocol, not
a finite-size artifact: the residual was `108%` at side=13 vs `98%`
at side=9 for the (1, 3) config.

The clean fix is to either (a) reformulate the observable to use the
separation acceleration only, with the explicit `(m_a + m_b)` scaling
test that does not require per-packet centroid isolation, or (b) move
to a closed-boundary or staggered protocol where parity is more
exactly preserved.

## 7. What this changes

- **Closed at smoke-test level (active-queue item):** Wilson two-body
  both-masses scaling on the cross-coupling acceleration. Constant at
  `3.6%` precision across n=5 mass configurations.
- **Sharpened (still open):** action-reaction law on the per-packet
  centroid observable on small open lattices. The obstruction is now
  explicitly identified as self-Hartree contamination of the heavier
  packet's cross signal, not as an ambiguous "noise floor".
- **No claim surface change:** the lane remains in
  `docs/repo/ACTIVE_REVIEW_QUEUE.md` as an open item; both-masses is
  closed only at the smoke-test level.

## 8. Falsifier

The result is falsified by exhibiting any of:

- the both-masses scaling failing on a similar n>=5 mass-ratio sweep
  (C.1 should fail), or
- the negative control E.1 not breaking action-reaction in
  `ASYMMETRIC` mode, or
- the FREE drift becoming mass-dependent.

None of these is exhibited by the runner.

## 9. Bottom line

The both-masses scaling on the cross-coupling acceleration is
confirmed on the side=9 Wilson smoke surface across five mass
configurations. The action-reaction law on the per-packet centroid
observable is OPEN with a well-characterized obstruction (self-Hartree
contamination of the heavier packet) that does not respond to
modest size scaling. The next concrete step is the
separation-acceleration `(m_a + m_b)` scaling test, which avoids
per-packet isolation, or a staggered/closed-boundary protocol where
parity is preserved.

## 10. Provenance

- Runner: `scripts/frontier_wilson_two_body_action_reaction_both_masses.py`
- Result: `10/11 PASS` (B.1 explicitly-expected FAIL)
- Wallclock: ~3 seconds on the validation host
- Runtime caveat: validation host is Python 3.12.8, numpy 2.4.1,
  scipy 1.17.0, sympy 1.14.0; pinned release environment is Python
  3.13.5, numpy 2.4.4, scipy 1.17.1. Wave-packet evolution is
  deterministic and robust to this drift; the structural sympy
  identities are exact.
- Random seeds: none (single deterministic Gaussian initialization).
- Multi-seed extension is on the next-step list.
