# Bounded Crank-Nicolson Lieb-Robinson Diagnostic for Light-Cone Framing

**Date:** 2026-05-09
**Type:** bounded_theorem
**Claim scope:** For finite-dimensional nearest-neighbor toy
Hamiltonians with local density bound `J` and subcritical
Crank-Nicolson step size, the Cayley transform
`U_CN = (I - i a_tau H/2)(I + i a_tau H/2)^(-1)` is unitary, its
single-step kernel has a Neumann-series exponential tail, repeated
steps obey the standard Lieb-Robinson-shaped bound on the tested
finite volumes, and `U_CN^n -> exp(-i t H)` with the expected
`O(a_tau^2)` convergence at fixed `t`. This is bounded diagnostic
support for `LIGHT_CONE_FRAMING_NOTE.md`; it does not prove a closed
framework-wide Crank-Nicolson Lieb-Robinson constant for the exact
reconstructed Hamiltonian.
**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome.
**Primary runner:** `scripts/light_cone_crank_nicolson_lr_2026_05_09.py`

## Why this note exists

The light-cone framing note records 1+1d staggered-Dirac dispersion and
finite-spacing Crank-Nicolson containment behavior. A prior review
flagged that the note identified the containment behavior with standard
Lieb-Robinson behavior without deriving a constant for the actual
Crank-Nicolson time-step kernel.

The Hamiltonian-side work now available in
[`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md)
is itself bounded action-support evidence, not an exact retained
finite-range theorem for `H = -log(T)/a_tau`. Therefore this note keeps
the Crank-Nicolson layer at bounded-support strength.

## Setup

Let `H` be a finite-dimensional Hermitian Hamiltonian. The
Crank-Nicolson step is the Cayley transform

```text
    U_CN(a_tau) = (I - i a_tau H/2) (I + i a_tau H/2)^(-1).
```

For a local finite-range Hamiltonian toy model with density bound `J`,
define `epsilon = a_tau J / 2`. The Neumann expansion of the resolvent

```text
    (I + i a_tau H/2)^(-1) = sum_{n >= 0} (-i a_tau H/2)^n
```

is the source of the finite-step exponential tail when the step is
subcritical. For the exact framework Hamiltonian, a separate
finite-range or quasilocal estimate remains required before this
diagnostic can be promoted into a closed theorem.

## Bounded Statements

**(CN-A) Cayley unitarity.** For Hermitian `H`, `U_CN(a_tau)` is unitary
because the numerator and denominator are adjoints and commute as
polynomials in `H`.

**(CN-B) Single-step Neumann tail.** In finite-range toy models with
subcritical `epsilon`, the first nonzero contribution to a commutator
at distance `d` appears at Neumann order proportional to `d`; the
single-step commutator is therefore exponentially small in distance.

**(CN-C) Tested n-step LR-shaped bound.** Repeated Crank-Nicolson steps
on the runner's random nearest-neighbor Hamiltonians obey

```text
    ||[alpha_t^CN(O_x), O_y]|| <= 2 ||O_x|| ||O_y|| exp(-d(x,y) + v_CN |t|)
```

with the diagnostic velocity

```text
    v_CN = v_LR(H) / (1 - a_tau J / 2)
```

on the tested finite volumes and step sizes. This formula should be
read as a bounded diagnostic extrapolation of the Neumann-series
resolvent factor, not as a framework-retained constant.

**(CN-D) Continuum agreement.** At fixed time `t`, repeated
Crank-Nicolson steps converge to `exp(-i t H)` with the expected
second-order error. This supports treating the Crank-Nicolson cone as a
finite-step approximation to the Hamiltonian LR cone in the small-step
regime.

## Runner Coverage

The companion runner checks:

- Cayley-transform unitarity for random finite-range Hermitian `H`.
- Per-step commutator decay from the Neumann-series tail.
- An n-step LR-shaped inequality on finite nearest-neighbor chains.
- `O(a_tau^2)` convergence of `U_CN^n` to `exp(-i t H)`.
- Small-step agreement between Crank-Nicolson and continuous-time
  commutators.

The runner is intentionally finite and diagnostic. It does not build
the exact framework transfer-matrix logarithm and does not prove a
non-perturbative quasilocal bound for the repo's full dynamics.

## Hypothesis and Import Boundary

Load-bearing inputs:

- Bounded Hamiltonian-side action-support/J-budget context from
  [`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md).
- Hermiticity of the finite toy Hamiltonians built by the runner.
- Standard Cayley-transform and Neumann-series linear algebra.
- Standard Lieb-Robinson combinatorial machinery as an admitted
  theorem context.

Not imported as proof inputs: observed containment percentages,
fitted velocities, or a retained exact-H locality theorem.

## Audit Boundary

This note does not close the light-cone framing audit gap by itself.
It makes the Crank-Nicolson part more auditable by separating:

- what the finite-step Cayley transform can be checked to do on
  bounded finite-range toy Hamiltonians;
- what remains open for the framework, namely an exact finite-range or
  quasilocal estimate for the reconstructed Hamiltonian and its
  Crank-Nicolson kernel.

## References

- Hamiltonian-side bounded support:
  [`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md)
- Parent framing context, non-load-bearing here:
  `LIGHT_CONE_FRAMING_NOTE.md`
- Standard external theorem context:
  Lieb-Robinson 1972; Hastings 2004; Nachtergaele-Sims 2010; standard
  Padé/Crank-Nicolson second-order convergence.
