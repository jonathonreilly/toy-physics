# Dynamic Poisson Resource Generation From Product States

**Date:** 2026-04-25
**Status:** planning / first artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_dynamical_resource_generation.py`

## Scope

This note records a bounded audit of native taste-qubit resource generation by
time evolution. Two distinguishable species start in simple product site states,
evolve under the existing small Poisson-derived two-species Hamiltonian, and are
then traced to the logical taste-qubit sector over time.

The audited object is an ordinary quantum state teleportation resource only. It
is not matter teleportation, charge transfer, mass transfer, energy transfer,
object transport, or faster-than-light signaling.

## Method

The runner uses the same Hamiltonian ingredients as the existing Poisson/CHSH
lane:

```text
H = H1 x I + I x H1 + G V_Poisson
```

For each sampled time:

1. evolve a product site state under exact diagonalization;
2. trace cells and spectator taste bits;
3. keep the last Kogut-Susskind taste bit per species as the logical pair;
4. measure best Bell overlap, logical CHSH, negativity, and purity;
5. estimate mean teleportation fidelity after fixed Bell-frame alignment;
6. audit Bob's pre-message state for input-independence on the best candidate.

The useful threshold is strict `Bell* > 0.5`, equivalent to mean fidelity above
the classical `2/3` threshold after fixed Bell-frame alignment. The
high-fidelity threshold used here is `Bell* >= 0.90`.

## Command

```bash
python3 scripts/frontier_teleportation_dynamical_resource_generation.py
```

Input probes for the candidate teleportation/no-signaling audit:

```text
70 states = 6 Pauli-axis states + 64 random states, seed=20260425
```

## Default Results

All default cases use `dim=1`, `side=8`, `mass=0`, `t_max=20`,
`samples=401`, and `dt=0.05`.

| case | `G` | init | best `t` | best Bell overlap | label | framed mean fidelity | standard `Phi+` mean fidelity | logical CHSH | negativity | useful windows | high windows |
| --- | ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_null_site01` | `0` | `(0, 1)` | `0.000` | `0.500000` | `Psi+` | `0.666667` | `0.333333` | `2.000000` | `0.000000` | `0` | `0` |
| `1d_poisson_site01_G50` | `50` | `(0, 1)` | `13.000` | `0.616298` | `Psi+` | `0.744199` | `0.345224` | `2.068829` | `0.182205` | `7` | `0` |
| `1d_poisson_site03_G100` | `100` | `(0, 3)` | `19.750` | `0.631187` | `Psi-` | `0.754125` | `0.348982` | `1.974538` | `0.138343` | `12` | `0` |

Best useful windows:

| case | best useful window | high-fidelity window |
| --- | --- | --- |
| `1d_null_site01` | none | none |
| `1d_poisson_site01_G50` | `[3.900, 20.000]`, peak `0.616298` at `t=13.000`, `323` samples | none |
| `1d_poisson_site03_G100` | `[16.850, 20.000]`, peak `0.631187` at `t=19.750`, `64` samples | none |

Sampled teleportation fidelity at the best candidate:

| case | sampled mean | sampled min | sampled max | output trace error |
| --- | ---: | ---: | ---: | ---: |
| `1d_null_site01` | `0.685810` | `0.500000` | `1.000000` | `9.993e-16` |
| `1d_poisson_site01_G50` | `0.757946` | `0.622398` | `0.976064` | `7.773e-16` |
| `1d_poisson_site03_G100` | `0.765845` | `0.640317` | `0.967398` | `8.882e-16` |

The sampled null mean is finite-sample dependent; the exact framed estimate at
the null candidate is the classical boundary value `2/3`, and the strict useful
gate does not pass.

## Null And No-Signaling Checks

The `G=0` control stays non-useful:

```text
best Bell overlap = 0.500000
max negativity over scan = 0.000000
useful windows = 0
high-fidelity windows = 0
null control = PASS
```

Bob's pre-message/no-record state remains input-independent for every best
candidate:

| case | distance to resource marginal | pairwise input distance | Bob marginal bias from `I/2` |
| --- | ---: | ---: | ---: |
| `1d_null_site01` | `4.441e-16` | `2.220e-16` | `5.000e-01` |
| `1d_poisson_site01_G50` | `4.857e-16` | `3.053e-16` | `2.612e-01` |
| `1d_poisson_site03_G100` | `4.718e-16` | `3.053e-16` | `9.674e-02` |

The marginal bias from `I/2` is not input information. The relevant
no-signaling condition is the pairwise input independence of Bob's no-record
state, which holds at numerical precision here.

## Interpretation

No high-fidelity Bell-resource window appears in this bounded product-state
scan at the `0.90` Bell-overlap threshold.

The interacting cases do open useful but low-fidelity Bell-resource windows
after fixed Bell-frame alignment. The best audited point reaches Bell overlap
`0.631187` and framed mean fidelity `0.754125`, which is above the classical
`2/3` threshold but far below a high-fidelity teleportation resource.

The result is therefore not a promotion of the teleportation lane. It is a
bounded dynamic generation artifact showing that simple product-state
evolution can create some logical taste-qubit entanglement, but not enough for
the high-fidelity resource target on this surface.

## Limitations

- Small surface only: default runs are `1D N=8` exact diagonalization probes.
- Initial states are simple localized site-product states; no optimized native
  preparation schedule is claimed.
- Time is sampled on a fixed grid with `dt=0.05`; narrow windows between samples
  are not excluded.
- Bell-frame alignment is a pre-agreed local correction convention; the
  standard `Phi+` convention remains poor for the best `Psi+`/`Psi-` candidates.
- Bell measurement and Bob correction are ideal logical operations.
- The audit does not transfer matter, mass, charge, energy, or information
  faster than light.
