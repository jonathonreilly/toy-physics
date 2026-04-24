# Koide Q Bridge: Traceless-Source Lagrange-Multiplier No-Go Note

**Date:** 2026-04-23
**Status:** support / bridge-target sharpening on the charged-lepton Koide
`Q = 2/3` lane. Not a closure theorem.
**Runner:** `scripts/frontier_koide_q_traceless_source_lagrange_multiplier_no_go.py`
**Result:** `23/23 PASS`.

## 1. Question

The April 22 second-order support batch compressed the open `Q` bridge to one
explicit primitive: why is the physical charged-lepton selector source-free
(`K = 0`) on the normalized second-order reduced carrier
`Y >= 0, Tr(Y) = 2, Y = diag(y, 2 - y)`?

The existing no-hidden-source audit
([`KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md`](./KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md))
treats `K_+` and `K_perp` symmetrically, leaving the open primitive at **two**
scalar conditions (`K_+ = 0` and `K_perp = 0`). This note reduces it to
**one**.

## 2. Statement

On the normalized trace-2 second-order reduced charged-lepton carrier with
`C_3`-equivariant block source `K = diag(K_+, K_perp)`, define the
trace + traceless decomposition

```text
K_trace := (K_+ + K_perp) / 2,
K_TL    := (K_+ - K_perp) / 2,
K       =  K_trace * I + K_TL * diag(+1, -1).
```

Then:

1. **`C_3` equivariance** on the cyclic image (singlet `B_+` plus real 2D irrep
   `B_perp`) forces `K` to be diagonal in `(B_+, B_perp)`. There are at most
   two independent real scalars `(K_+, K_perp)`, equivalently
   `(K_trace, K_TL)`.

2. **Trace-2 normalization** turns `K_trace` into the KKT/Lagrange multiplier
   dual to the constraint `Tr(Y) = 2`. The constrained KKT relation reads
   ```text
   Y^{-1} = (1 - lambda - K_trace) * I  -  K_TL * diag(+1, -1),
   ```
   so `lambda` and `K_trace` enter only through their sum
   `lambda' := lambda + K_trace`. The reparameterization `lambda -> lambda'`
   eliminates `K_trace` exactly. `K_trace` is therefore physically gauge.

3. **Constrained-dual relation** on the trace-2 cone: `K_*(Y) = Y^{-1} - I`
   gives
   ```text
   K_TL(y)    = (1 - y) / (y * (2 - y)),
   K_trace(y) = (1 - y(2 - y)) / (y(2 - y)).
   ```
   `K_TL(y)` is strictly monotonically decreasing on `(0, 2)` and is a
   bijection onto `R`, with `K_TL(1) = 0`.

4. **Equivalence:**
   ```text
   K_TL = 0   <=>   y = 1   <=>   Y = I_2   <=>   E_+ = E_perp
              <=>   kappa = 2   <=>   Q = 2/3.
   ```

The open primitive is therefore the strictly weaker single-scalar condition
`K_TL = 0`, replacing the previous two-scalar `K = 0`.

## 3. Adversarial stress

The runner verifies the no-go under three adversarial perturbations:

- **Pure trace shift** `K = c * I`: solving the trace-2 KKT eq gives
  `lambda(c) = -c` and `Y` stays at `I_2` for any `c in R`. Confirms
  `K_trace` is gauge.
- **Pure traceless source** `K = K_TL_val * diag(+1, -1)` with
  `K_TL_val = 1/5`: the trace-2 KKT eq gives `y_1 = 1.193`, `y_2 = 0.807`,
  off the symmetric point. `Y` moves; `Q != 2/3`.
- **Off-diagonal (`B_+` <-> `B_perp`) source**: the cyclic-rotation
  commutator is nonzero (Schur on inequivalent irreps). Such sources
  require explicit `C_3` breaking input and are excluded by the retained
  three-generation `C_3` symmetry on the cyclic carrier.

## 4. Negative control

A numeric sweep `K_TL in {-0.4, -0.3, ..., +0.4}` (with `K_trace = 0`) gives
`Q != 2/3` at every sampled point, with deviations growing monotonically in
`|K_TL|`. The sweep is asymmetric in sign because `kappa = 2 * y_1 / y_2`
maps `K_TL` and `-K_TL` to non-reciprocal `kappa` values (the `+` block has
multiplicity `1` and the `perp` block has multiplicity `2` in the Frobenius
split).

A separate gauge-invariance check verifies that, at fixed `K_TL = 0.2`, the
output `Q` is exactly invariant (spread = `0.000e+00`) under
`K_trace in [-0.5, 0.5]`. This is the operational confirmation of the
Lagrange-multiplier identification.

## 5. What this does and does not change

### What this changes

- The bridge primitive is now **one** scalar (`K_TL = 0`), strictly
  weaker than the previous **two** scalar condition (`K_+ = K_perp = 0`).
- The trace component of any `C_3`-equivariant block source is identified
  explicitly as the multiplier of the trace-2 constraint and carries no
  `Q`-relevant content.
- The remaining open work is to derive `K_TL = 0` from retained
  `Cl(3)/Z^3` charged-lepton physics. This is strictly easier than the
  `K = 0` problem.

### What this does not change

- It does **not** prove that retained `Cl(3)/Z^3` charged-lepton physics
  forces the traceless component `K_TL` to vanish on the normalized
  second-order carrier. That is the remaining single-scalar bridge.
- It does **not** affect the separate `delta = 2/9` Brannen-phase bridge.
- It does **not** promote `Q = 2/3` from open flagship to retained.
- It does **not** modify the public package surface beyond strengthening
  one element of the open Koide support stack.

## 6. Falsifier

The result is falsified by exhibiting any of:

- **(a)** a `C_3`-equivariant block source `K` on the cyclic image with
  `K_TL != 0` that does not move `y` away from `1`;
- **(b)** a KKT/Lagrange analysis where `K_trace` contributes physical
  information independent of the multiplier `lambda`;
- **(c)** a reparameterization of the trace-2 cone that makes `K_+` and
  `K_perp` independently physical (rather than reducing to one
  traceless degree of freedom).

None of these is exhibited by the existing support package or by the
runner's adversarial sweep.

## 7. Boundary

Carry this note as a **support sharpening** of the open `Q` bridge:

- **closed (algebraic):** the Lagrange-multiplier gauge of `K_trace` and
  the dual-relation bijection `K_TL(y)` on the normalized trace-2 cone;
- **open (physical):** the derivation of `K_TL = 0` from retained
  `Cl(3)/Z^3` charged-lepton physics on the second-order carrier. This is
  one scalar, not two.

The next honest target on this lane is to enumerate retained
`Cl(3)/Z^3` charged-lepton scalar inputs that could couple to `K_TL` at
the second-order reduced carrier order, and either show they all
identically vanish (closing the bridge) or exhibit one that forces a
nonzero `K_TL` (refuting the candidate).

## 8. Provenance

- Runner: `scripts/frontier_koide_q_traceless_source_lagrange_multiplier_no_go.py`
- Result: `23/23 PASS`
- Runtime caveat: the validation host is Python 3.12.8, numpy 2.4.1,
  scipy 1.17.0, sympy 1.14.0; the pinned release environment is Python
  3.13.5, numpy 2.4.4, scipy 1.17.1. The runner's content is symbolic
  (sympy) plus low-precision numpy sweeps and is robust to this drift.
