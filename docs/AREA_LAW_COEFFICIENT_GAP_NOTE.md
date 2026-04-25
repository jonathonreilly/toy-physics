# Area-Law Coefficient Gap Audit

**Date:** 2026-04-25
**Status:** Planck Target 2 audit / support note

## Purpose

This note audits the gap between the exact primitive-cell coefficient

```text
c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4
```

in the conditional Planck packet and the entanglement carriers already tested
on the `Cl(3)/Z^3` surface. The outcome is negative for the current
free-fermion carrier, but not closed for every conceivable carrier.

## Carriers already tried

1. **2D half-filled NN free fermion, straight cut.**
   The retained no-go
   [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)
   identifies the actual asymptotic coefficient as the Widom-Gioev-Klich
   coefficient
   `c_Widom = 1/6`, not `1/4`. The earlier `~0.24` value at `L <= 32`
   is a finite-size artifact; the `L <= 96` probe drifts toward `1/6`.

2. **3D half-filled NN cubic free fermion, straight cut.**
   The same no-go records `c_Widom(3D) ~ 0.105` for the cubic
   half-filled Fermi surface. This is also not `1/4`.

3. **Finite-L RT bond-dimension comparison.**
   [BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md) remains a
   bounded companion: its finite lattice ratio is useful as a comparison
   diagnostic, but the correct asymptotic form is
   `r(L) = c_inf + a / log L + ...`, with `c_inf = 1/6` on the retained
   carrier.

4. **Dirac-sea boundary-law probes.**
   [HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md](./HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)
   and
   [BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md](./BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md)
   support a bounded boundary-law preference on a staggered 2D periodic
   lattice. The recorded slopes (`0.211399` free, `0.186053` with
   self-gravity in the probe note) are model coefficients, not
   Bekenstein-Hawking coefficients, and the review queue correctly says not
   to overread them as holography.

5. **Historical transfer / multi-source diagnostics.**
   `frontier_entanglement_area_law.py` and
   `frontier_multi_source_entropy.py` are source-to-cut transfer diagnostics,
   not canonical many-body entanglement carriers. They do not identify a
   primitive `1/4` entropy coefficient.

The retained tree has not yet probed a genuine NNN/multi-pocket Fermi surface,
an interacting Hubbard descendant, a topological edge sector, a Schur-block
horizon sector from the DM lane, or a plaquette-first horizon sector as an
exact entropy carrier.

## Meaning of the Planck `1/4`

The Planck packet's `1/4` is a source-free primitive counting-trace statement
on the time-locked event cell

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16.
```

With `P_A` the four-dimensional Hamming-weight-one event packet,
`rank(P_A)=4`, so

```text
Tr((I_16/16) P_A) = 1/4.
```

[PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](./PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
then proves that, if this primitive count is accepted as the microscopic
gravitational area/action carrier, locality and additivity extend it uniquely
to finite boundary patches. This is not yet an entanglement theorem. To make it
one, a carrier must show either:

- a Widom leading-log coefficient exactly `1/4` on the same primitive boundary
  count; or
- a gapped/horizon area law whose entropy per primitive face is derived as the
  same `Tr((I_16/16)P_A)`, not imposed after the fact.

## Available but unclosed carrier routes

- **NN arbitrary filling:** analytically available and not numerically
  exhausted in the retained runner. However, for the usual one-band NN surface,
  each transverse momentum fiber has at most one occupied interval, so the
  broader no-go in
  [AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md](./AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md)
  bounds the coefficient by `1/6`.
- **NNN or other finite-range hoppings:** potentially evade the simple-fiber
  bound only by producing multi-pocket or multi-interval Fermi fibers. No
  retained physical principle currently selects an exact pocket geometry with
  the required projected multiplicity.
- **Schur blocks from the DM lane:** available as algebraic block carriers,
  but direct sums of simple-fiber Slater determinants remain bounded by `1/6`
  under the same boundary-rank normalization. A nontrivial Schur-block entropy
  law would need an additional horizon-sector axiom.
- **Interacting Hubbard / Fermi-liquid descendants:** physically motivated,
  but the leading `L^{d-1} log L` coefficient is still controlled by Fermi
  surface geometry in the Fermi-liquid regime. Interactions do not by
  themselves turn a simple-fiber projected multiplicity into the value needed
  for `1/4`.
- **Gapped/topological horizon sectors:** avoid the free-fermion logarithm and
  are the cleanest positive direction in principle. The obstruction is that
  mass-gap area-law theorems give existence or bounds, not the exact
  ultraviolet area coefficient. Topological entanglement entropy is a universal
  subleading constant, not the leading area coefficient.
- **Plaquette-first sector:** plausible as a gravitational/action bridge, but
  not yet formulated as an entropy carrier whose primitive face count is
  provably the same `16`-state event-cell count.

## Minimal Widom geometry that could hit `1/4`

For a straight cut with normal `e_x`, the Widom coefficient is

```text
c_Widom = I_x / (12 (2*pi)^(d-1)),
I_x = integral_{partial Gamma} |n_x . n_k| dS_k.
```

To obtain `c_Widom = 1/4`, one needs

```text
I_x = 3 (2*pi)^(d-1).
```

By the coarea/fiber-count identity, `I_x` is the transverse integral of the
number of Fermi-surface crossings along each `k_x` fiber. A simple one-interval
Fermi sea has at most two crossings per fiber and therefore

```text
I_x <= 2 (2*pi)^(d-1),   c_Widom <= 1/6.
```

Thus a Widom route to `1/4` requires multi-interval fibers, pocket multiplicity,
or a boundary-rank normalization different from the primitive count. That is a
real residual axiom, not a numerical tuning problem.

## Audit conclusion

The question is not implicitly closed by the existing single-carrier no-go, but
the available positive routes are not theorem-ready. The clean retained result
is a broader Widom-class no-go for simple-fiber free-fermion and
Schur/direct-sum descendants. A future positive Target 2 route must add a
physical axiom selecting
either:

1. a non-engineered multi-pocket/multi-interval Fermi carrier with projected
   crossing multiplicity exactly `3`; or
2. a gapped horizon/edge carrier deriving the leading area coefficient from the
   same `16`-state primitive boundary count.

The second route is more compatible with the Planck packet, but it still needs a
new carrier-identification theorem rather than another bounded area-law probe.

## Post-audit update

[AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md](./AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md)
implements the first route conditionally. It supplies the missing
multi-pocket measure by the self-dual half-zone of the primitive transverse
nearest-neighbor Laplacian, so the average crossing count is exactly `3` and
the Widom coefficient is exactly `1/4`. This resolves the coefficient problem
if the rank-four primitive boundary block is accepted as that two-orbital
Laplacian-gated edge carrier. Otherwise, the broader no-go packet remains the
retained status.
