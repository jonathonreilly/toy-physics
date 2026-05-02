# Teleportation Adiabatic Preparation Probe

Status: planning / first artifact. This note records a bounded adiabatic/gap
diagnostic for the Poisson-derived encoded Bell resource used for ordinary
quantum state teleportation.

It does not claim matter teleportation, mass transfer, charge transfer, energy
transfer, or faster-than-light transport. It also does not prove preparation.

## Script

Runner:

```bash
python3 scripts/frontier_teleportation_adiabatic_prep_probe.py
```

The runner probes the native linear coupling path

```text
H(s) = H(G=0) + s * (H(G_target) - H(G=0)),  s in [0, 1].
```

For each small default case it records:

1. sampled spectral gap along the path;
2. overlap with the final target ground state;
3. deterministic traced logical resource quality after keeping the last
   Kogut-Susskind taste bit per species;
4. `Phi+` resource overlap, best Bell overlap, logical CHSH, and negativity;
5. exact eigenbasis adiabatic diagnostic
   `max_k |<k|dH/ds|0>| / gap_k^2`;
6. conservative warning diagnostic `||dH/ds||_2 / gap_1^2`.

The exact diagnostic is schedule-free and should be read as a rough runtime
scale for a unit-speed linear ramp. The conservative norm bound is intentionally
pessimistic and flags sensitivity to small gaps and symmetry-breaking leakage.

## Commands Run

```bash
python3 -m py_compile scripts/frontier_teleportation_adiabatic_prep_probe.py
python3 scripts/frontier_teleportation_adiabatic_prep_probe.py
```

Both commands completed successfully.

Default grid and thresholds:

- `41` uniformly spaced `s` values;
- high resource endpoint: `Phi+` overlap `>= 0.900`;
- sampled gap floor: `>= 1e-3`;
- exact adiabatic diagnostic threshold: `<= 1000`;
- conservative norm-bound threshold: `<= 100000`.

## Null Controls

Both `G_target=0` controls were clean.

| case | min gap | final `Phi+` overlap | final best Bell overlap | logical CHSH | negativity | max exact diagnostic | max norm bound |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_null` | `0.585786` | `0.500000` | `0.500000` | `2.000000` | `0.000000` | `0` | `0` |
| `2d_null` | `2.000000` | `0.500000` | `0.500000` | `2.000000` | `0.000000` | `0` | `0` |

The null paths are constant Hamiltonian paths, so `dH/ds=0`. They do not
produce an entangled Bell resource under the deterministic traced extraction.

## Poisson Path Summaries

| case | min sampled gap | gap location | initial target-ground overlap | final `Phi+` overlap | final logical CHSH | final negativity | max exact diagnostic | max norm bound | verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `1d_poisson_chsh` | `0.018683` | `s=1.000` | `0.141330` | `0.997963` | `2.822668` | `0.497963` | `155.558660` | `1.880033e+06` | plausible clean-path diagnostic; fragile by norm bound |
| `2d_poisson_chsh` | `0.246378` | `s=1.000` | `0.145230` | `0.970283` | `2.745662` | `0.470283` | `1.456812` | `4418.777061` | plausible bounded diagnostic |

The 1D path reaches the strongest endpoint resource, but the final spectral
gap is small. The exact eigenbasis diagnostic remains below the default
threshold because the direct near-gap coupling is symmetry-suppressed, while
the conservative norm bound is very large. That makes the 1D path fragile
rather than a robust preparation story.

The 2D `4x4` path has a larger sampled minimum gap, reaches `Phi+` overlap
`0.970283`, and stays below both default adiabatic diagnostic thresholds.
Within this bounded probe it is the cleaner candidate path.

Representative sampled rows:

| case | s | gap | target-ground overlap | `Phi+` overlap | max exact diagnostic | norm bound |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_poisson_chsh` | `0.000` | `0.585786` | `0.141330` | `0.500000` | `155.558660` | `1912.452650` |
| `1d_poisson_chsh` | `0.250` | `0.071302` | `0.983377` | `0.969916` | `0.039222` | `1.290818e+05` |
| `1d_poisson_chsh` | `0.500` | `0.037002` | `0.998021` | `0.991988` | `0.005546` | `4.793010e+05` |
| `1d_poisson_chsh` | `1.000` | `0.018683` | `1.000000` | `0.997963` | `0.000716` | `1.880033e+06` |
| `2d_poisson_chsh` | `0.000` | `2.000000` | `0.145230` | `0.500000` | `1.413460` | `67.057292` |
| `2d_poisson_chsh` | `0.250` | `0.722825` | `0.800135` | `0.784931` | `0.229804` | `513.380655` |
| `2d_poisson_chsh` | `0.500` | `0.449531` | `0.959790` | `0.905991` | `0.071795` | `1327.355180` |
| `2d_poisson_chsh` | `1.000` | `0.246378` | `1.000000` | `0.970283` | `0.013655` | `4418.777061` |

## Interpretation

The coupling-ramp path is not a diagnostic no-go on the small default cases.
The null controls stay clean, and both Poisson endpoints reproduce high-quality
deterministic traced encoded Bell resources. The `2D 4x4` case is especially
plausible as a next preparation target because both the exact eigenbasis
diagnostic and conservative norm-bound diagnostic remain moderate on this
grid.

This remains a planning artifact. The run only samples a finite path grid and
does not simulate finite-time dynamics, choose an optimized schedule, bound
diabatic error, model control noise, test larger lattices, or implement encoded
Bell measurement/readout operations.

## Limitation Status

What moved:

- A concrete native adiabatic path was specified.
- Null/control paths were included and stayed clean.
- At least one small 1D and one small 2D Poisson target were probed.
- Gap, target-ground overlap, target Bell-resource overlap, and adiabatic
  diagnostics were recorded.

What remains open:

- No preparation proof.
- No runtime/error theorem for any schedule.
- No robustness analysis under symmetry-breaking perturbations.
- No scaling beyond `1D N=8` and `2D 4x4`.
- No physical cooling, control, readout, or deterministic branch-selection
  implementation.
- Strict scope remains ordinary quantum state teleportation only.
