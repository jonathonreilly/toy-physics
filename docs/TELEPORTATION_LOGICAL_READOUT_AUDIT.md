# Teleportation Logical Readout/Extraction Audit

**Date:** 2026-04-25
**Status:** planning / first artifact; not a promotion claim
**Runner:** `scripts/frontier_teleportation_logical_readout_audit.py`

## Scope

This note audits the logical extraction currently used by the native
taste-qubit teleportation lane:

```text
full two-species Poisson/CHSH state
  -> keep the last KS taste bit per species
  -> trace cells and spectator tastes
  -> two-qubit logical resource
```

The key distinction is:

- the environment trace is mathematically valid and gives correct probabilities
  for taste-only observables `O_logical tensor I_env`;
- that is not yet an operational readout primitive unless an apparatus/control
  model is supplied that really measures, prepares, and corrects only the
  retained taste bit while remaining blind to cells and spectator tastes.

The audit is ordinary quantum state teleportation only. It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_logical_readout_audit.py
python3 scripts/frontier_teleportation_logical_readout_audit.py
```

Both commands completed successfully.

Default settings:

```text
seed = 20260425
input probes = 134 (six Pauli-axis states plus 128 random states)
high-fidelity threshold = 0.900
fixed-env probability floor = 1e-15
```

## Trace Extraction Validity

| case | full CHSH | traced Bell | traced CHSH | purity | negativity | trace valid |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `1d_poisson_chsh` | `2.822668` | `0.997963` (`Phi+`) | `2.822668` | `0.997967` | `0.497963` | yes |
| `2d_poisson_chsh` | `2.668376` | `0.970283` (`Phi+`) | `2.745662` | `0.971783` | `0.470283` | yes |

Trace diagnostics:

| case | trace error | Hermitian error | min eigenvalue | branch probability sum |
| --- | ---: | ---: | ---: | ---: |
| `1d_poisson_chsh` | `0.000e+00` | `0.000e+00` | `-7.331e-17` | `1.000000000000` |
| `2d_poisson_chsh` | `0.000e+00` | `0.000e+00` | `-2.718e-18` | `1.000000000000` |

The tiny negative eigenvalues are numerical roundoff. The trace extraction is a
valid reduced density matrix construction on these cases.

## Fixed-Environment Branch Variation

| case | branches | active | effective branch count | probability range | best-Bell range | weighted best-Bell mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_poisson_chsh` | `16` | `16` | `4.008158` | `2.056839e-13 .. 0.249745` | `0.499964 .. 0.999984` | `0.998472` |
| `2d_poisson_chsh` | `64` | `64` | `8.757659` | `5.854540e-08 .. 0.119428` | `0.984720 .. 0.999428` | `0.985011` |

Overlap with the traced resource's selected label, `Phi+`:

| case | `Phi+` overlap range | weighted mean | weighted std |
| --- | ---: | ---: | ---: |
| `1d_poisson_chsh` | `0.000016 .. 0.998981` | `0.997963` | `0.031860` |
| `2d_poisson_chsh` | `0.000572 .. 0.996406` | `0.970283` | `0.118622` |

Best-label probability mass:

| case | `Phi+` mass | `Psi+` mass |
| --- | ---: | ---: |
| `1d_poisson_chsh` | `0.998982` across `4` branches | `0.001018` across `12` branches |
| `2d_poisson_chsh` | `0.985011` across `32` branches | `0.014989` across `32` branches |

High-fidelity postselection:

| case | best-Bell high-fidelity mass | traced-label high-fidelity mass | best postselected branch |
| --- | ---: | ---: | --- |
| `1d_poisson_chsh` | `0.998982` (`8` branches) | `0.998982` (`4` branches) | `Psi+`, Bell `0.999984`, p `2.056839e-13`, expected attempts `4.86183e+12` |
| `2d_poisson_chsh` | `1.000000` (`64` branches) | `0.985011` (`32` branches) | `Psi+`, Bell `0.999428`, p `5.854540e-08`, expected attempts `1.70808e+07` |

The fixed-env scan is the main readout warning. Some rare branches are excellent
Bell resources but in a different Bell sector than the traced `Phi+` resource.
Those branches are diagnostics only unless an explicit environment measurement,
heralding rule, and branch-conditioned logical operation are supplied.

## Bob Pre-Message Marginal

| case | Bob marginal bias from `I/2` | max no-record to resource marginal | max pairwise input distance | max branch probability span |
| --- | ---: | ---: | ---: | ---: |
| `1d_poisson_chsh` | `3.189e-02` | `4.163e-16` | `2.220e-16` | `3.189e-02` |
| `2d_poisson_chsh` | `1.213e-01` | `4.441e-16` | `2.220e-16` | `1.213e-01` |

Bob's marginal can be biased because the extracted resource is imperfect, but
the no-record state is input-independent to numerical precision. The input
state becomes available to Bob only after the classical Bell record and
correction.

## Gatekeeping

Established:

- tracing cells and spectator tastes gives a valid logical density matrix on
  the audited Poisson cases;
- the traced density matrix gives correct statistics for strictly taste-only
  measurements of the form `O_logical tensor I_env`;
- under the audited traced extraction, Bob's pre-message no-record state is
  independent of Alice's input to numerical precision.

Not established:

- a native apparatus that addresses only the retained taste qubit;
- a physical measurement showing cells/spectators are readout-blind;
- a dynamic preparation/cooling path for the Poisson ground state;
- deterministic fixed-environment selection or postselection as a protocol;
- non-ideal encoded Bell measurement, feed-forward, or Bob correction;
- any matter, mass, charge, energy, object, or faster-than-light transfer.

Cells and spectators can be ignored only under one of the following future
conditions:

1. all implemented preparation, Bell measurement, and correction operators are
   proven to factor as logical taste operators tensor identity on the
   environment;
2. the apparatus is proven readout-blind to environment labels and does not
   condition on them;
3. branch variation is bounded below the target protocol tolerance for every
   logical observable used by the protocol;
4. an explicit environment measurement and heralding workflow is supplied, with
   branch-conditioned logical operations and the quoted postselection cost.

Bottom line: the current trace extraction is mathematically sound and remains
positive as an ideal logical-resource diagnostic, but operational logical/taste
readout is still open.
